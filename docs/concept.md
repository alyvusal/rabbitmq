# Architecture

similar products: aws kinesis, kafka

- kafka: after message consumed, it is still available in kafka queueu
- rabbitmq: after message consumed, it is **not** available in rabbitmq queue

Message flow in RabbitMQ:

- Publisher send message to Exchange
- Exchange routes traffic to Queue via Binding (A binding is a link between a queue and an exchange)
- Consumer takes mesaage from Queue

Publisher <-> Exchange (Binding) <-> Queue <-> (Ack?) Consumer

Messages sent with Advanced Message Queuing Protocol ([AMQP](https://www.rabbitmq.com/docs/next/amqp))

[AMQP 0-9-1 Model Explained](https://www.rabbitmq.com/tutorials/amqp-concepts)

|Protocol|Bound to Port|
|-|-|
|amqp|5672|
|clustering|25672|
|http/management|15672|
|http/prometheus|15692|
|stream|5552|

## Queue

- [RabbitMQ Queue Types 101](https://hevodata.com/learn/rabbitmq-queue-types/)
- [RabbitMQ Queue Types Explained](https://www.cloudamqp.com/blog/rabbitmq-queue-types.html)
- [RabbitMQ 3.8 Feature Focus - Quorum Queues](https://www.cloudamqp.com/blog/rabbitmq-quorum-queues.html)

## Exchange

[Exchange types](https://jmcle.github.io/rabbitmq-visualizer):

- `default` (default name: `(AMQP default)`): create binding like `direct` but automatic for every queue, binding key = queue name, useful for simple apps
- `direct` (default name: `amq.direct`): have a name, binding not create automatic. The message is routed to the queues whose binding key exactly matches the routing key of the message. For example, if the queue is bound to the exchange with the binding key pdfprocess, a message published to the exchange with a routing key pdfprocess is routed to that queue.
- `fanout` (default name: `amq.fanout`): routing key does not have any effect, A fanout exchange routes messages to all of the queues bound to it.
- `headers` (default name: `amq.match` and `amq.headers`): message header used to route message, routed to where message header == binding header

  - if x*match=all: then all attributes must match
  - if xmatch=any:  then any attribute must match

- `topic` (default name: `amq.topic`): similar to `direct` but routing key is compared with binding pattern to route messages, does a wildcard match between the routing key and the routing pattern specified in the binding:

  - *Binding key*: exact string that matches routing key
  - *Binding pattern*: text pattern that matches one or more routing key

[RabbitMQ Exchange Types: Trendyol](https://medium.com/trendyol-tech/rabbitmq-exchange-types-d7e1f51ec825)
