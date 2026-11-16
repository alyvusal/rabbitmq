# Install

## [RabbitMQ Kubernetes Operators](https://www.rabbitmq.com/kubernetes/operator/operator-overview)

```bash
# install cert manager as it is dependency (wait to deploy fully)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.21.3/cert-manager.yaml

# install operator
kubectl apply -k k8s/kubernetes-operator/kustomize/operator

# install cluster 1
kubectl apply -k k8s/kubernetes-operator/kustomize/k3d

# install cluster 2 to test ha, shovel, failover, cluster
kubectl apply -k k8s/kubernetes-operator/kustomize/k3d-slave
```

check result

```bash
curl -s -uadmin:admin http://rabbitmq-192.168.0.100.nip.io/api/overview | jq
curl -s -uadmin:admin http://rabbitmq-192.168.0.100.nip.io/api/nodes | jq
```

[TLS Conf](https://www.rabbitmq.com/kubernetes/operator/using-operator#tls-conf)

Set `spec.tls.interNode` before the first start. Enabling it on a running cluster changes the Erlang distribution protocol, and a rolling update cannot finish: the restarted pod speaks TLS while the others still speak plaintext.

Stop the whole cluster, then start it again. The operator's preStop hook runs `rabbitmq-upgrade await_online_quorum_plus_one` and waits up to 7 days (`terminationGracePeriodSeconds: 604800`). With every node stopping, that check never passes. Label the pods so the hook exits, then change `spec.replicas` on the `RabbitmqCluster`. The operator owns the StatefulSet replica count.

```bash
kubectl -n rabbitmq-system label pod -l app.kubernetes.io/name=rabbitmq-cluster skipPreStopChecks=true

# replicas: 0 in cluster.yaml, or patch the live object. Wait until no server pods are left.
kubectl -n rabbitmq-system patch rabbitmqcluster rabbitmq-cluster --type merge -p '{"spec":{"replicas":0}}'
kubectl -n rabbitmq-system get pods -l app.kubernetes.io/name=rabbitmq-cluster -w

# replicas: 3. All pods must start together with inet_tls.
kubectl -n rabbitmq-system patch rabbitmqcluster rabbitmq-cluster --type merge -p '{"spec":{"replicas":3}}'
```

Wait until none are `Terminating`. Force-deleting a Pod drops it from the API while the old container can keep running, so the UI shows the new pods Ready and the old process still connects under the same node name. On k3d, one sandbox per node means the UI matches the node:

```bash
docker exec k3d-k3s-default-server-0 crictl pods --name rabbitmq-cluster-server
```

`kubectl apply -k` uses `spec.replicas` from `cluster.yaml`. A later apply overwrites a live replica patch.

Client certificate rotation is a different change. RabbitMQ reloads that TLS secret without a restart. To pick it up immediately:

```bash
kubectl -n rabbitmq-system exec -it rabbitmq-cluster-server-0 -c rabbitmq -- rabbitmqctl eval 'ssl:clear_pem_cache().'
```

mTLS test

```bash
cd /tmp

kubectl -n rabbitmq-system get secret rabbitmq-cluster-cert \
  -o jsonpath='{.data.tls\.crt}' | base64 -d >| client.crt

kubectl -n rabbitmq-system get secret rabbitmq-cluster-cert \
  -o jsonpath='{.data.tls\.key}' | base64 -d >| client.key

kubectl -n rabbitmq-system get secret rabbitmq-cluster-cert \
  -o jsonpath='{.data.ca\.crt}' | base64 -d >| ca.crt

kubectl -n rabbitmq-system port-forward svc/rabbitmq-cluster 5671:5671

openssl s_client \
  -connect localhost:5671 \
  -cert client.crt \
  -key client.key \
  -CAfile ca.crt \
  -verify_return_error \
< /dev/null

kubectl -n rabbitmq-system exec -it rabbitmq-cluster-server-0 -c rabbitmq -- openssl s_client -connect rabbitmq-cluster-nodes.rabbitmq-system.svc.cluster.local:5671 </dev/null
```

get username and password

```bash
kubectl -n rabbitmq-dev get secret rabbitmq-cluster-dev-default-user -o jsonpath='{.data.username}' | base64 --decode
kubectl -n rabbitmq-dev  get secret rabbitmq-cluster-dev-default-user -o jsonpath='{.data.password}' | base64 --decode
```

Access UI via forward port:

```bash
# with plugin
kubectl rabbitmq manage rabbitmq-cluster

# native port forward
kubectl -n rabbitmq port-forward "service/rabbitmq-cluster" 15672
```

For pubslisher/consumer test

```bash
kubectl -n rabbitmq port-forward service/rabbitmq-cluster 5672
```

- [Using the RabbitMQ Cluster Kubernetes Operator](https://www.rabbitmq.com/kubernetes/operator/using-operator)
- [How to change operator defaults](https://www.rabbitmq.com/kubernetes/operator/configure-operator-defaults)

## Monitoring

```bash
kubectl apply -k k8s/monitoring
```

## [RabbitMQ Messaging Topology Operator](https://www.rabbitmq.com/kubernetes/operator/install-topology-operator)

A Messaging topology is the collection of objects such as exchanges, queues, bindings and policies that provides specific messaging or streaming scenario. This operator is used with RabbitMQ clusters deployed via the RabbitMQ Cluster Kubernetes Operator.

Requiements:

- `cert-manager` must be installed before before deploying topology operator
- default user must be created and used by topology resources
- [Namespace scope to allow](https://www.rabbitmq.com/kubernetes/operator/using-topology-operator#namespace-scope)

Following resources will be created and we can manage to configure RabbitMQ

- [queues](../k8s/topology-operator/examples/Queue.yaml)
- [exchanges](../k8s/topology-operator/examples/Exchange.yaml)
- [bindings](./k8s/topology-operator/examples/Binding.yaml)
- [policies](../k8s/topology-operator/examples/Policy.yaml)
- [vhosts](../k8s/topology-operator/examples/Vhost.yaml)
- [users](../k8s/topology-operator/examples/User.yaml)
- [permissions](../k8s/topology-operator/examples/Permission.yaml)
- [topicpermissions](.//k8s/topology-operator/examples/TopicPermission.yaml)
- [federations](../k8s/topology-operator/examples/Federation-Exchange.yaml)
- [shovels](../k8s/topology-operator/examples/Shovel.yaml)
- operatorpolicies
- schemareplications
- superstreams

1. via manifest

    ```bash
    # with cert-manager
    kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.3.1/cert-manager.yaml
    # install topology operator
    kubectl -n rabbitmq apply -f https://github.com/rabbitmq/messaging-topology-operator/releases/latest/download/messaging-topology-operator-with-certmanager.yaml

    # without cert-manager
    https://github.com/rabbitmq/messaging-topology-operator/releases/latest/download/messaging-topology-operator-with-certmanager.yaml
    ```

2. or all-ine-one with kustomize

    ```bash
    kubectl apply -k k8s/topology-operator/kustomize/kind
    ```

[Using the RabbitMQ Messaging Topology Kubernetes Operator](https://www.rabbitmq.com/kubernetes/operator/using-topology-operator)
