---
title: TiCDC 架构设计与原理
summary: 了解 TiCDC 软件的架构设计和运行原理。
---

# TiCDC 架构设计与原理

## TiCDC 软件架构

TiCDC 集群由多个 TiCDC 对等节点组成，是一种分布式无状态的架构设计。 TiCDC 集群自身的架构和 TiCDC 节点内部组件的设计如下图所示：

![TiCDC architecture](/media/ticdc/ticdc-architecture-1.jpg)

在上面的图形中， TiCDC 集群由多个运行了 TiCDC 实例的节点组成，每个 TiCDC 实例上都会运行一个 Capture 进程。在众多的 Capture 进程中，会有一个 Capture 进程被选举成为 owner Capture 进程，这个进程负责完成 TiCDC 集群的各种工作负载调度工作，DDL 语句的同步工作和一些其他的管理任务。另外，每个Capture 进程对会包含一个或多个 processor 线程，顾名思义，processor 就是 TiCDC 用来同步上游 TiDB 集群中的表数据的工作组件了，由于 TiCDC 同步数据的最小单位是表，所以 Processor 是由一条条的 table pipeline 构成的，每一条 pipeline 包含了下面的模块，各个模块之间是串行的关系，组合在一起完成了从上游拉去数据，排序，加载和同步到下游的过程。下面的图形描述了一条 table pipeline 的各个组成部分：

![TiCDC architecture](/media/ticdc/ticdc-architecture-2.jpg)

其中：

- Puller：负责从 TiKV 节点获取 DDL 和行改变信息 
- Sorter：负责将接收到的改变在 TiCDC 内按照时间戳进行升序排序 
- Mounter：会将改变按照对应的 Schema 信息转换成 TiCDC 可以处理的格式 
- Sink：负责将对应的改变应用到下游系统 

从高可用的角度来讲，每个 TiCDC 集群都包含了多个 TiCDC 节点，这些节点定期向 PD 集群中的 etcd 集群汇报自己的状态，并选举出其中的一个节点作为 TiCDC 集群的 owner，owner 采用 etcd 统一存储状态来进行调度，owner 将调度结果直接写入 etcd，processor 按照状态完成对应的任务，processor 所在节点出现异常后集群会将 table 调度到其他节点。如果 owner 节点出现异常，其他节点的 Capture 进程会选举出新的 owner，如下图所示：

![TiCDC architecture](/media/ticdc/ticdc-architecture-3.PNG)

## Changefeed 和 Task

在了解了以上的 TiCDC 的软件架构和重要的组件及模块之后，接下来介绍两个逻辑概念： Changefeed 和 Task。 首先，Changefeed 在 TiCDC 的中代表一个同步任务，Changefeed 携带了需要同步的表信息，以及对应的下游信息和一些其他的配置信息。当 TiCDC 接收到对应的同步任务之后，就会把这个任务拆分为若干个称之为 Task 的子任务，分配给 TiCDC 集群的各个节点上的 Capture 进程进行处理。所以，Changefeed 是用户用来给 TiCDC 分配同步任务的方式，而 Task 则是 TiCDC 将同步任务拆分后的子任务名称。

例如：

```
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
cat changefeed.toml
......
[sink]
dispatchers = [
    {matcher = ['test1.tab1', 'test2.tab2'], topic = "{schema}_{table}"},
    {matcher = ['test3.tab3', 'test4.tab4'], topic = "{schema}_{table}"},
]
```

说明：对于以上命令的详细含义，详见：[TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)

以上命令创建了一个到 Kafka 集群的 Changefeed，在这个 Changefeed 中，需要同步 `test1.tab1`, `test1.tab2`, `test3.tab3`, `test4.tab4` 这四张表。TiCDC 在接收到这个命令之后，会执行下面的步骤：

1. 将这个任务发送给 TiCDC 的 owner Capture 进程。 
2. Owner Capture 进程将这个任务的相关定义信息保存在 PD 的 etcd 当中 
3. Owner Capture 将这个任务拆分成若干个 Task，并将各个 Task 需要完成的任务通知其他 Capture 进程。 
4. 各个 Capture 进程开始从对应的 TiKV 节点上拉去信息，并进行处理后同步。 

如果，将 changefeed， Task 也包含到上文中提及的架构图当中，完整的 TiCDC 架构图如下图所示：

![TiCDC architecture](/media/ticdc/ticdc-architecture-4.jpg)

在上面的图形中，用户创建了一个 Changefeed，需要同步 4 张表， 这个 Changefeed 被拆分成了 3 个任务，均匀的分发到了 TiCDC 集群的 3 个 Capture 节点上，在 TiCDC 对这些数据进行了处理之后，数据同步到了下游的系统，目前 TiCDC 支持的下游系统包含了 MySQL，TiDB 和 Kafka。上面的过程只是讲解了 Changefeed 级别数据流转的基本过程，下面，以处理表 `table1` 的任务 Task1 为例，从更加详细的层面来描述 TiCDC 处理数据的过程：

![TiCDC architecture](/media/ticdc/ticdc-architecture-5.jpg)

首先，TiKV 集群会在发生数据改变的时候会将数据主动推送给 puller 模块 ———— 我们称之为推流，而 puller 模块在发现收到的数据改变不连续的时候，也会向 TiKV 节点主动拉去需要的数据 ———— 我们称之为增量扫。在拿到了需要的数据之后，Sorter 模块开始对数据按照改变的时间进行排序，并将排好序的数据发送给 mounter。 Mounter 模块收到了数据改变之后，根据表的 schema 信息，将数据改变装载成TiCD sink 可以理解的格式，最后，sink 模块根据下游的类型将数据改变同步到下游中去。

通过上面的内容，用户可以了解 TiCDC 的基本工作原理，并且对于 TiCDC 同步数据的过程进行了介绍。但是，TiCDC 的上游是 TiDB ———— 一款分布式的关系型数据库，对于关系型数据库，支持事务是其最大的同时也是最重要的特点之一，而 TiCDC 面对的下游除了像Kafka 这种消息系统之外，还需要面对像 TiDB 或 MySQL 这种关系型数据库系统。所以，TiCDC 在同步数据的时候，如何保证数据的一致性，以及在同步多张表的时候，如何保证事务的一致性，都是很大的挑战。在下面的章节中会介绍 TiCDC 在确保事务特性时所使用的关键技术和概念。

## TiCDC 关键概念

当 TiCDC 对应的下游系统是关系型数据库时，TiCDC 在同步数据的时候会确保单表事务的数据一致性，以及多表事务的最终一致性。另外，TiCDC 会确保上游 TiDB 集群发生过的数据改变能够被 TiCDC 向任意下游最少同步一次。

首先，对软件架构部分涉及到的主要的 TiCDC 相关的概念进行详细的解释：

- Capture： TiCDC 节点的运行进程，多个 Capture 进程构成了 TiCDC集群，Capture 进程负责 TiKV 的数据改变的同步--包括了接受和主动拉取两种方式--，并向下游同步数据。 
  - Capture Owner：是一种 capture 的角色，每个 CDC 集群同一时刻最多只存在一个 capture 具有 owner 角色，负责集群内部的调度。
- processor：是 capture 内部的逻辑线程，每个 processor 负责处理同一个同步流中一个或多个 table 的数据。一个 capture 节点可以运行多个 processor。
- ChangeFeed：一个由用户启动的从上游 TiDB 同步到下游的任务，其中包含多个 task，task 会分布在不同的 capture 节点进行数据同步处理。

接下来，对于 TiCDC 中与时间相关的概念进行介绍。由于 TiCDC 需要确保数据被至少一次同步到下游，并且确保一定的一致性，就需要一系列的时间戳来对数据同步的各种状态进行描述。

**ResolvedTS**：这个时间戳在 TiKV 和 TiCDC 中都存在。对于TiKV 节点，这个时间戳代表了某一个 Region leader 上开始时间最早的事务的开始时间，即：ResolvedTS = max(ResolvedTS, min(StartTS))。 因为每个 TiDB 集群包含多个 TiKV 节点，所有 TiKV 节点上的 Region leader 的 ResolvedTS 的最小值，被称为 Global ResolvedTS。 TiDB 集群确保 Global ResolvedTS 之前的事务都被提交了，或者可以认为这个时间戳之前不存在未提交的事务。 

对于 TiCDC 节点，每张表都会有一个表级别的 ResolvedTS， 称之为 table ResolvedTS,  表示这张表已经从 TiKV 接收到的数据改变的最低水位，可以简单的认为和 TiKV 节点上这张表的各个 region 的 ResolvedTS 的最小值是相同的。 由于 TiCDC 每个节点上都会存在一个或多个 Processor，每个 processor 又对应多个 table pipeline, 可以认为 processor ResolvedTS 为某一个 TiCDC 节点上各个 processor 的 ResolvedTS 的最小值， 而各个 TiCDC 节点上的 processor ResolvedTS 的最小值就被称为 global ResolvedTS。 另外，对于 TiCDC 节点来说， TiKV 节点发送过来的 ResolvedTS 信息是一种特殊的事件，它只包含一个格式为 `<resolvedTS:  时间戳>` 的特殊事件。通常情况下, ResolvedTS 满足以下约束：

```
table resolved TS >= local resolved TS >= global Resolved TS 
```

**CheckpointTS**：这个时间戳只在 TiCDC 中存在，它表示 TiCDC 已经同步给下游的数据的最低水位线，即 TiCDC 认为在这个时间戳之前的数据已经被同步到下游系统了。由于 TiCDC 同步数据的单位是表，所以 table checkpointTS 表示表级别的同步数据的水位线，processor checkpointTS 表示各个 processor 中最低的 checkpointTS；Global checkpointTS 表示各个 processor checkpointTS 中最低的 checkpointTS。通常情况下，Checkpoint TS 满足以下约束：

```
table checkpoint TS >= local checkpoint TS >= global checkpoint TS
```

如果将 ResolvedTS 和 checkpointTS 结合来看，完整的关系可以表达为：

```
table resolved TS >= local resolved TS >= global Resolved TS >= table checkpoint TS >= local checkpoint TS >= global checkpoint TS
```

随着数据的改变和事务的提交，TiKV 节点上的 resolvedTS 会不断的向前推进，TiCDC 节点的 puller 模块也会不断的收到 TiKV 推流过来的数据，并且根据收到的信息决定是否执行增量扫的过程，从而确保数据改变都能够被发送到 TiCDC 节点上。 Sorter 模块则负责将 puller 模块收到的信息按照时间戳（Timestamp，简称TS）进行升序排序，从而确保数据在表级别是满足一致性的。接下来， mounter 模块把上游的数据改变装配成 sink 模块可以消费的格式，并发送给 sink，而 sink 则负责把 checkpointTS 到 ResolvedTS 之间的数据改变，按照发生的 TS 顺序同步到下游，并在下游返回后推进 checkpointTS。

上面的内容只介绍了和 DML 语句相关的数据改变，并没有包含 DDL 相关的内容。下面对 DDL 语句相关的关键概念进行介绍。 

**Barrier TS**：当系统发生 DDL 语句或者使用了 TiCDC 的 sync point 时会产生的一个时间戳。

  - 对于 DDL 语句，这个时间戳会用来确保在这个 DDL 语句之前的改变都被应用到下游，之后执行对应的 DDL 语句，在 DDL 语句同步完成之后再同步其他的数据改变。由于 DDL 语句的处理是 owner 角色的 Capture 负责的，DDL 语句对应的 Barrier TS 只会由 owner 节点的 processor 线程产生。
  - sync point Barrier TS 也是一个时间戳，当用户启用 TiCDC 的 sync point 特性后，TiCDC 会根据用户指定的间隔产生一个 Barrier TS，当所有的表都同步到了这个Barrier TS 之后，记录一下对应的时间点，之后继续向下同步数据。 

TiCDC 是通过对 global checkpoint TS 和 barrier TS 进行比较来确定数据是否已经同步到 barrier TS 的。如果 global checkpoint TS = barrier TS，则说明所有表都至少推进到 barrier TS 了。如果等式不成立，说明有表还没推进到该 barrier TS ，在这种情况下也不会更新 barrier TS ，因此不会有表的 sink 节点对应 resolved TS 会超过 barrier TS，即不会有表的 check point TS 超过 barrier TS。

## 主要流程

最后，对 TiCDC 软件的常见操作所对应的主要流程进行介绍，帮助用户更好的理解 TiCDC 的工作原理。
启动 TiCDC 节点：

启动非 owner 的 TiCDC 节点：

  1. 启动 Capture 进程
  2. 启动 processor 
  3. 接受 Owner 下发的 Task 调度命令
  4. 根据调度命令启动或停止 tablePipeline 

对于 owner 的 TiCDC 节点：

  1. 启动 Capture 进程
  2. 当选 Owner 并启动对应的线程
  3. 读取 Changefeed 信息
  4. 启动 Changefeed 管理逻辑
  5. 根据 Changefeed 配置和最新 checkpointTS, 读取 TiKV 中的 schema 信息，确定需要被同步的表
  6. 读取各 Processor 当前同步的表的列表，分发需要添加的表
  7. 更新进度信息

停止 TiCDC 节点:  通常来说，停止 TiCDC 节点是为了对 TiCDC 进行升级或者对 TiCDC 所在的节点进行一些计划的维护操作。 在停止一个 TiCDC 节点时：

  1. 这个节点会收到停止的信号
  2. 将自己的服务状态置为不可用状态
  3. 节点停止接收新的复制表任务
  4. 通知 Owner 节点将自己节点的数据复制任务转移到其他节点
  5. 在复制任务移走之后，该节点停止完成。
