# HA, Clustering and Failover

- [HA, Clustering and Failover](#ha-clustering-and-failover)
  - [Cluster](#cluster)
  - [Federation](#federation)
  - [Queue replication (mirroring)(legacy)](#queue-replication-mirroringlegacy)
    - [Create Policy to enable this functionality](#create-policy-to-enable-this-functionality)
    - [Define master Queue location](#define-master-queue-location)
    - [Quorum Queues](#quorum-queues)
  - [Shovel Plugin](#shovel-plugin)

## Cluster

Remeber:

- nodes are in same or compatible version
- decide on recovery mode (partitions)
- choose number of ndoes wisely (perf tets, cluster reliablity etc)

Kubernetes operator creates this types of cluster with statefulSet replicas.

Exchange metdata, vhosts, binding metadata replicates to all nodes but for queues: if queues lives on node1 then on other ones metadata replicated. if node1 goes down, client could not get messages, other nodes will try to redirect request to node1.

## Federation

With federation messages ditributed across RabbitMQ clusters.

Federation link created downstream (destination cluster) then federated cluster will pull a copy of message from upstream like amqp client.

|Cluster|federation|
|-|-|
|Not WAN Friendly|Not WAN Friendly|
|Can't apply clustering for specific resource|Can federate particular queue or exchange|
|Depend to version|Independent to versions|

Types of federation:

- **[Federated Exchanges](https://www.rabbitmq.com/docs/federated-exchanges)**
  - Exchange ⟷ Exchange
  - **Flow**: Upstream (source) RabbitMQ ➙ Federated RabbitMQ 1 ➙ Federated RabbitMQ 2 ➙ ... ➙ Federated RabbitMQ N ➙ Queue ➙ Consumer. Messages are **copied** to federated cluster and **will be available** on upstearm queue.
  - **Test**: From UI senf message from exchange, if you send from Queue it will send to default Queue and routing key and bound Exchange will not work
  - **Topologies**
    - *Pair*
      - RabbitMQ1 🗘 RabbitMQ2
      - both will be upstream and federated for each other
      - publisher/consumer coould send/receive message to/from any of them
      - to prevent message sync loop `Maxhop=1` defined in both RabbitMQ clusters to prevent same message will not be synched back again
      - used when we want 2 copy of same message to be available (1 copy in each cluster)
    - *Complete Graph*
      - same as Pair topology but here we have more than 2 RabbitMQ
      - to prevent message sync loop `Maxhop=1` defined in both RabbitMQ clusters to prevent same message will not be synched back again
      - used when we want >3 copy of same message to be available (1 copy in each cluster)
      - 🗘: RabbitMQ1 ⟷ RabbitMQ2 ⟷ RabbitMQ3 ⟷ RabbitMQ1
    - *Fanout*
      - Tree ⭃ like topology
      - Used if we want to trasnmit message to large number of clusters
      - `Maxhop=Tree Depth -1`
      - Publisher send message to LB and randomly will be routed to any of cluster
      - Consumer should listen to all clusters, because don't know where message resides
      - Publisher ➙ Load Balancer (LB) ➙ RabbitMQ{1,2..N}
        - To resovle this one common cluster is created as downstearm and from all upstream clusters messages federated to this common cluster then to consumer
        - RabbitMQ{1,2..N} ➙ RabbitMQ Common ➙ Consumer
- **[Federated Queues](https://www.rabbitmq.com/docs/federated-queues)**
  - Queue ⟷ Queue
  - **Flow**: Consumer could connect to any Queue on upstream or downstream cluster. Messaged are **moved** to downsteram custers.
  - Message consumed by the downstream (federated) queue **will be deleted** from upstearm queue.
  - If messages consumed in downstream cluster, new ones will be transferred from upstream tp downstream if there is demand. if we put load balancer in from of consumer and accidentally his request routed to empty queue, then federated instance will request it from upstream
  - RabbitMQ UI does not support testing and always shows emtpy queue on federated insatnce, it send `basic-get`method. Instead use script to send `basic-consume` method

## Queue replication (mirroring)(legacy)

Check [Policy-Queue-HA.yaml](../k8s/topology-operator/examples/Policy-Queue-HA.yaml) and [publisher-queue-master-location.py](../scripts/publisher-queue-master-location.py)for example

### [Create Policy to enable this functionality](https://www.rabbitmq.com/docs/parameters#combining-policy-definitions)

|HA Mode (`ha-mode`)|HA Params (`ha-params`)|Functionality|
|-|-|-|
|`all`|Not requried|All nodes in cluster mirrored|
|`exactly`|N|Exactly `N` number of nodes mirrored|
|`nodes`|Node names|Node names mentioned are mirrored|

|`ha-sync-mode`|Functionality|
|-|-|
|`automatic`|Automatic Syncing|
|`manual`|Manual Syncing|

### Define master Queue location

We can do this with following options:

|`x-queue-master-location`|Functionality|
|-|-|
|`Min-masters`|Select node hosting minimum master Queues|
|`Client-local`|Select node in which Queue declared first|
|`Random`|Randomly select master node|

### Quorum Queues

Thus type of Queues automatically mirrored and should be used instead of Classic Queues unless we need some features of Classic Queues

## [Shovel Plugin](https://www.rabbitmq.com/docs/shovel)

Takes messages from a source (typically a queue) in one cluster and move them to destination (an exchange, topic, etc) in another cluster. The source and destination can be in the same cluster (typically in different vhosts) or distinct ones.

There is two flavors of Shovels: [dynamic shovels](https://www.rabbitmq.com/docs/shovel-dynamic) from CLI or UI and [static shovels](https://www.rabbitmq.com/docs/shovel-static) with advanced configuration.

Shovel plugins acts as consumer client app, in source queue you can see it in consumers list.

Requirements:

- Enable plugins: `rabbitmq_shovel` and `rabbitmq_shovel_management`

  ```bash
  rabbitmq-plugins enable rabbitmq_shovel
  rabbitmqctl shovel_status
  ```

[Example topology file](../k8s/topology-operator/examples/Shovel.yaml)
