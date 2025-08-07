# RabbitMQ

[back](../README.md)

Currently RabbitMQ 3.x used with AMQP 0.9.1 by default, for 4.x AMQP 1.0 will be deault version.

[Native AMQP 1.0 in RabbitMQ 4.0](https://www.rabbitmq.com/blog/2024/08/05/native-amqp)

## [Architecture and concept](./docs/concept.md)

## [Installation](./docs/install.md)

## [Plugins](./docs/plugins.md)

## [Users](./docs/users.md)

## [API](./docs/api.md)

## [Tuning and Performance](./docs/performance.md)

## [Backup & Restore](./docs/backup.md)

## [HA, Clustering and Failover](./docs/ha.md)

## Topology operator

To get helm on spect elements

```bash
kubectl get crd policies.rabbitmq.com -o yaml  | yq .spec.versions[0].schema.openAPIV3Schema.properties.spec.properties
kubectl get crd shovels.rabbitmq.com -o yaml | yq .spec.versions[0].schema.openAPIV3Schema.properties.spec.properties
kubectl get crd federations.rabbitmq.com -o yaml  | yq .spec.versions[0].schema.openAPIV3Schema.properties.spec.properties
```

alias created for short usage `alias crd_spec='yq .spec.versions[0].schema.openAPIV3Schema.properties.spec.properties'`

## REFERENCE

- [Docs](https://www.rabbitmq.com/docs)
- [Github](https://github.com/rabbitmq/rabbitmq-server)
- [Modifying the RabbitMQ Cluster Operator Default Configuration](https://www.rabbitmq.com/kubernetes/operator/configure-operator-defaults)
- [Configuration](https://www.rabbitmq.com/docs/configure)
- [TLS Configuration](https://www.rabbitmq.com/kubernetes/operator/using-operator#tls-conf)([TLS Support](https://www.rabbitmq.com/docs/ssl))
- [Use HashiCorp Vault](https://www.rabbitmq.com/kubernetes/operator/using-operator#vault)
- [Deployment Guidelines](https://www.rabbitmq.com/docs/production-checklist)
- [RabbitMQ Simulator](https://tryrabbitmq.com/)
- [RabbitMQSimulator](https://github.com/RabbitMQSimulator/RabbitMQSimulator)
- [RabbitMQ Visualizer](https://jmcle.github.io/rabbitmq-visualizer/)
- [Parameters and Policies](https://www.rabbitmq.com/docs/parameters#overview)
- [The RabbitMQ Management Interface](https://www.cloudamqp.com/blog/part3-rabbitmq-for-beginners_the-management-interface.html)
- [Feature Flags](https://www.rabbitmq.com/docs/feature-flags)
- [AMQP 0.9.1 vs 1.0](https://seventhstate.io/amqp-091-vs-1/)
- [When to use RabbitMQ or Apache Kafka](https://www.cloudamqp.com/blog/when-to-use-rabbitmq-or-apache-kafka.html)
