# Install

## [RabbitMQ Kubernetes Operators](https://www.rabbitmq.com/kubernetes/operator/operator-overview)

1. via manifest

    ```bash
    kubectl create ns rabbitmq-dev
    # install the operator
    kubectl apply -f https://github.com/rabbitmq/cluster-operatoreleases/latest/download/cluster-operator.yml

    # deploy a RabbitMQ cluster
    kubectl apply -f k8s/kubernetes-operator/kustomize/base/cluster/cluster.yaml
    ```

2. via kubectl rabbitmq plugin

    ```bash
    kubectl create ns rabbitmq-dev
    # install the operator
    kubectl rabbitmq install-cluster-operator

    # deploy a RabbitMQ cluster
    kubectl -n rabbitmq-dev rabbitmq create rabbitmq-cluster-dev
    ```

3. Install with Helm

    ```bash
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm install rabbitmq-operator bitnami/rabbitmq-cluster-operator -n rabbitmq-dev --create-namespace
    ```

4. or all-ine-one with kustomize

    ```bash
    # install operator
    kubectl apply -k k8s/kubernetes-operator/kustomize/operator

    # install cluster 1
    kubectl apply -k k8s/kubernetes-operator/kustomize/kind

    # install cluster 2 to test ha, shovel, failover, cluster
    kubectl apply -k k8s/kubernetes-operator/kustomize/kind-ha
    ```

check result

```bash
curl -s -uadmin:admin http://rabbitmq-192.168.0.100.nip.io/api/overview | jq
curl -s -uadmin:admin http://rabbitmq-192.168.0.100.nip.io/api/nodes | jq
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
