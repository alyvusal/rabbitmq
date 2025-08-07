# Notes

enable port-forward for 5672 (amqp)

```bash
kubectl -n rabbitmq-dev port-forward service/rabbitmq-cluster-dev 5672
```
