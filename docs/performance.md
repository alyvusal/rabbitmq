# Tuning and Performance

## [Perfomance test](https://www.rabbitmq.com/kubernetes/operator/using-operator#verify-instance)

[Github: rabbitmq-perf-test](https://github.com/rabbitmq/rabbitmq-perf-test)

```bash
instance=rabbitmq-cluster-dev
username=$(kubectl -n rabbitmq-dev get secret ${instance}-default-user -o jsonpath="{.data.username}" | base64 --decode)
password=$(kubectl -n rabbitmq-dev get secret ${instance}-default-user -o jsonpath="{.data.password}" | base64 --decode)
service=${instance}
username=$(kubectl -n rabbitmq-dev get secret ${instance}-default-user-external-dev -o jsonpath="{.data.username}" | base64 --decode)
password=$(kubectl -n rabbitmq-dev get secret ${instance}-default-user-external-dev -o jsonpath="{.data.password}" | base64 --decode)
kubectl -n rabbitmq-dev run perf-test --image=pivotalrabbitmq/perf-test -- --uri "amqp://${username}:${password}@${service}"
kubectl -n rabbitmq-dev logs -f perf-test
kubectl -n rabbitmq-dev delete pod perf-test

# or if default users created
kubectl  -n rabbitmq-dev rabbitmq perf-test rabbitmq-cluster-dev --rate 100 -C 10000
```

Sometimes manually put one of cluster node and monitor throughput
