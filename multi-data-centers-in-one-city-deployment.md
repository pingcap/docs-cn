# TiDB 同城多数据中心

## 一、透析 Raft 协议

### 1.1 Raft 协议简概

Raft 是一种分布式一致性算法，在 TiDB 集群的多种组件中，PD 和 TiKV 都通过 Raft 实现了数据的容灾。Raft 的灾难恢复能力通过如下机制实现：

- Raft 成员的本质是日志复制和状态机。Raft 成员之间通过复制日志来实现数据同步；Raft 成员在不同条件下切换自己的成员状态，其目标是选出 leader 以提供对外服务。 
- Raft 是一个表决系统，它遵循多数派协议，在一个 Raft Group 中，某成员获得大多数投票，它的成员状态就会转变为 leader。也就是说，当一个 Raft Group 还保有大多数节点（majority）时，它就能够选出 leader 以提供对外服务。

### 1.2 Raft 副本数选择

Raft 算法本身以及 TiDB 中的 Raft 实现都没有限制一个 Raft Group 的副本数，这个副本数可以为任意正整数，当副本数为 n 的时候，一个 Raft Group 的可靠性如下：

- 若 n 为奇数，该 Raft Group 可以容忍 (n-1)/2 个副本同时发生故障
- 若 n 为偶数，该 Raft Group 可以容忍 n/2 -1 个副本同时发生故障

在一般情况下，我们建议将 Raft Group 的副本数设置为奇数，其原因如下：

- 避免造成存储空间的浪费：三副本可以容忍 1 副本故障，增加 1 个副本变为 4 副本后，容灾能力维持不变。
- 当副本数为偶数时，如果发生了一个网络隔离，刚好将隔离开的两侧的副本数划分为两个 n/2 副本的话，由于两边都得不到大多数成员，因此都无法选出 leader 提供服务，这个网络隔离将直接导致整体的服务不可用。
- 当副本数为奇数时，在只发生一个网络隔离的情况中，网络隔离的两侧中总有一侧能分到大多数的成员，可以选出 leader 以提供服务。

### 1.3 Raft 原生限制

遵循 Raft 可靠性的特点，放到现实场景中：

- 想克服任意 1 台服务器的故障，应至少提供 3 台服务器。
- 想克服任意 1 个机柜的故障，应至少提供 3 个机柜。
- 想克服任意 1 个数据中心（机房）的故障，应至少提供 3 个数据中心。
- 想应对任意 1 个城市的灾难场景，应至少规划 3 个城市用于部署。

可见，原生 Raft 协议对于偶数副本的支持并不是很友好，考虑跨城网络延迟影响，或许同城三数据中心是最适合部署 Raft 的高可用及容灾方案。

## 二、同城三数据中心方案

同城三数据中心方案，即同城存有三个机房部署 TiDB 集群，同城三数据中心间的数据同步通过集群自身内部（Raft 协议）完成。同城三数据中心可同时对外进行读写服务，任意中心发生故障不影响数据一致性。

### 2.1 简易架构图

集群 TiDB，TiKV，PD 组件分别分布在 3 个不同的数据中心，这是最常规，高可用性最高的方案。

![三中心部署](/media/deploy-3dc.png)

**优点**

- 所有数据的副本分布在三个数据中心，具备高可用和容灾能力
- 任何一个数据中心失效后，不会产生任何数据丢失（RPO = 0）
- 任何一个数据中心失效后，其他两个数据中心会自动发起 leader election，并在合理长的时间内（通常情况 20s 以内）自动恢复服务（RTO <= 20s）

![三中心部署容灾](/media/deploy-3dc-dr.png)

**缺点**

性能受网络延迟影响。

- 对于写入的场景，所有写入的数据需要同步复制到至少 2 个数据中心，由于 TiDB 写入过程使用两阶段提交，故写入延迟至少需要 2 倍数据中心间的延迟。
- 对于读请求来说，如果数据 leader 与发起读取的 TiDB 节点不在同一个数据中心，也会受网络延迟影响。
- TiDB 中的每个事务都需要向 PD leader 获取 TSO，当 TiDB 与 PD leader 不在同一个数据中心时，它上面运行的事务也会因此受网络延迟影响，每个有写入的事务会获取两次 TSO。

### 2.2 架构优化图

如果我们不需要每个数据中心同时对外提供服务，可以将业务流量全部派发到一个数据中心，并通过调度策略把 Region leader 和 PD leader 都迁移到同一个数据中心。这样一来，不管是从 PD 获取 TSO 还是读取 Region 都不受数据中心间网络的影响。当该数据中心失效后，PD leader 和 Region leader 会自动在其它数据中心选出，只需要把业务流量转移至其他存活的数据中心即可。

![三中心部署读性能优化](/media/deploy-3dc-optimize.png)

**优点**

集群 TSO 获取能力以及读取性能有所提升，具体调度策略设置模板参照如下：

```
-- 其他机房统一驱逐 leader 到业务流量机房
config set label-property reject-leader LabelName labelValue
-- 迁移 PD leader 并设置优先级
member leader transfer pdName1
member leader_priority pdName1 5
member leader_priority pdName2 4
member leader_priority pdName3 3
```

**缺点**

- 写入场景仍受数据中心网络延迟影响，这是因为遵循 Raft 多数派协议，所有写入的数据需要同步复制到至少 2 个数据中心
- TiDB Server 数据中心级别单点
- 业务流量纯走单数据中心，性能受限于单数据中心网络带宽压力
- TSO 获取能力以及读取性能受限于业务流量数据中心集群 PD、TiKV 组件是否正常，否则仍受跨数据中心网络交互影响

### 2.3 样例部署图

#### 2.3.1 样例拓扑架构

下面我们假设某城存有 IDC1、IDC2、IDC3 三机房，机房 IDC 中存有两套机架，每个机架存有三台服务器，不考虑混布以及单台机器多实例部署下，同城三数据中心架构集群（3 副本）部署参考如下：

![sample-tidb](/media/multi-data-centers-in-one-city-deployment-sample.png)

#### 2.3.2 TiKV Labels 规划

对于 TiKV Labels 需要根据已有的物理资源、用户容灾能力容忍度等方面因素设计与规划，进而提升系统的可用性和容灾能力。根据已规划的拓扑架构，配置相关 tidb-ansible inventory.ini 文件（此处省略其他非重点项）

```ini
[tikv_servers]
TiKV-30   ansible_host=10.63.10.30     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170 tikv_status_port=20180 labels="zone=z1,dc=d1,rack=r1,host=30"  
TiKV-31   ansible_host=10.63.10.31     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z1,dc=d1,rack=r1,host=31"  
TiKV-32   ansible_host=10.63.10.32     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z1,dc=d1,rack=r2,host=30"  
TiKV-33   ansible_host=10.63.10.33     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z1,dc=d1,rack=r2,host=30"  

TiKV-34   ansible_host=10.63.10.34     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z2,dc=d1,rack=r1,host=34"  
TiKV-35   ansible_host=10.63.10.35     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z2,dc=d1,rack=r1,host=35"  
TiKV-36   ansible_host=10.63.10.36     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z2,dc=d1,rack=r2,host=36"  
TiKV-37   ansible_host=10.63.10.36     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z2,dc=d1,rack=r2,host=37"  

TiKV-38   ansible_host=10.63.10.38     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z3,dc=d1,rack=r1,host=38"  
TiKV-39   ansible_host=10.63.10.39     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z3,dc=d1,rack=r1,host=39"  
TiKV-40   ansible_host=10.63.10.40     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z3,dc=d1,rack=r2,host=40"  
TiKV-41   ansible_host=10.63.10.41     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z3,dc=d1,rack=r2,host=41"

## Group variables
[pd_servers:vars]
location_labels = ["zone","dc","rack","host"]
```

在本案例中，zone 表示逻辑可用区层级，用于控制副本的隔离（当前集群 3 副本）。而不直接采用 dc，rack，host 三层 Label 结构的原因是考虑到将来可能发生 dc (数据中心) 的扩容，假设新扩容的 dc 编号是 d2，d3，d4，则只需在对应可用区下扩容 dc ，rack 扩容只需在对应 dc 下扩容即可，如果直接采用 dc，rack，host 三层 Label 结构，那么扩容 dc 操作可能需重打 Lable，TiKV 数据整体 Rebalance

### 2.4 高可用和容灾分析

对于同城多数据中心方案，我们能得到的保障是任意一个数据中心故障时，集群能自动恢复服务，不需要人工介入，并能保证数据一致性。注意各种调度策略都是用于帮助性能优化的，当发生故障时调度机制总是第一优先考虑可用性而不是性能。
