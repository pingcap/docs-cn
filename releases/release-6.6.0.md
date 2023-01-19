---
title: TiDB 6.6.0 Release Notes
---

# TiDB 6.6.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.6.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.6/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 6.6.0 版本中，你可以获得以下关键特性：

- MySQL 8.0 兼容的多值索引(Multi-Valued Index) (实验特性)
- 基于资源组的资源管控 (实验特性)
- 悲观锁队列的稳定唤醒模型
- 数据请求的批量聚合

## 新功能

### SQL

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* MySQL 兼容的多值索引(Multi-Valued Index) (实验特性) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei)  @[qw4990](https://github.com/qw4990)

    TiDB 在 v6.6.0 引入了 MySQL 兼容的多值索引 (Multi-Valued Index)。 过滤 JSON 类型中某个数组的值是一个常见操作， 但普通索引对这类操作起不到加速作用，而在数组上创建多值索引能够大幅提升过滤的性能。 如果 JSON 类型中的某个数组上存在多值索引，  带有`MEMBER OF()`，`JSON_CONTAINS()`，`JSON_OVERLAPS()` 这几个函数的检索条件可以利用多值索引进行过滤，减少大量的 I/O 消耗，提升运行速度。

    多值索引的引入， 是对 JSON 类型的进一步增强， 同时也提升了 TiDB 对 MySQL 8.0 的兼容性。

    更多信息，请参考[用户文档](/choose-index.md#使用多值索引)。

* 绑定历史执行计划 GA [#39199](https://github.com/pingcap/tidb/issues/39199) @[fzzf678](https://github.com/fzzf678)

    在 v6.5 中，TiDB 扩展了 [`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md) 语句中的绑定对象，支持根据历史执行计划创建绑定。在 v6.6 中这个功能 GA， 执行计划的选择不仅限在当前 TiDB 节点，任意 TiDB 节点产生的历史执行计划都可以被选为 [SQL Binding]((/sql-statements/sql-statement-create-binding.md)) 的目标，进一步提升了功能的易用性。 

    更多信息，请参考[用户文档](/sql-plan-management.md#根据历史执行计划创建绑定)。 

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 为执行计划缓存增加告警 [#issue号](链接) @[qw4990](https://github.com/qw4990)

    当执行计划无法进入执行计划缓存时， TiDB 会通过 warning 的方式说明其无法被缓存的原因， 降低诊断的难度。例如：

    ```sql
    mysql> prepare st from 'select * from t where a<?';
    Query OK, 0 rows affected (0.00 sec)

    mysql> set @a='1'; 
    Query OK, 0 rows affected (0.00 sec)

    mysql> execute st using @a;  
    Empty set, 1 warning (0.01 sec)

    mysql> show warnings;
    +---------+------+----------------------------------------------+
    | Level   | Code | Message                                      |
    +---------+------+----------------------------------------------+
    | Warning | 1105 | skip plan-cache: '1' may be converted to INT |
    +---------+------+----------------------------------------------+
    ```
    
    上述例子中， 优化器进行了非 INT 类型到 INT 类型的转换，产生的计划可能随着参数变化有风险，因此不缓存。 

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md#prepared-plan-cache-诊断)。

* 在慢查询中增加告警字段 [#39893](https://github.com/pingcap/tidb/issues/39893) @[time-and-fate](https://github.com/time-and-fate)

    向慢查询日志中增加一个新的字段 `Warning` ，以 JSON 格式记录该慢查询语句在执行过程中产生的警告，用来协助查询性能问题的诊断。 

    更多信息，请参考[用户文档](/identify-slow-queries.md)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiFlash 引擎支持 Stale Read 功能 [#4483](https://github.com/pingcap/tiflash/issues/4483) @[hehechen](https://github.com/hehechen)

    在 v5.1.1 中，TiDB 正式发布了 Stale Read 功能，TiDB 可以读取指定的时间点或时间范围内的历史数据。Stale Read 允许引擎直接读取本地副本数据，降低读取延迟，提升查询性能。但是，只有 TiKV 引擎支持 Stale Read 功能，TiFlash 引擎并不支持 Stale Read 功能，即使查询的表包含 TiFlash 副本，TiDB 也只能使用 TiKV 副本进行指定时间点或时间范围内的历史数据查询。在 v6.6.0 中，TiFlash 引擎实现了对 Stale Read 功能的支持。使用语法 `AS OF TIMESTAMP` 进行指定时间点或时间范围内的历史数据查询时，如果查询的表包含 TiFlash 副本，优化器可以选择 TiFlash 引擎读取指定的时间点或时间范围内的历史数据。

    更多信息，请参考[用户文档](/stale-read.md)。

* 新增支持下推以下字符串函数至 TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008)

    * `regexp_replace`

* TiFlash 引擎支持独立的 MVCC 位图过滤器 [#6296](https://github.com/pingcap/tiflash/issues/6296) @[JinheLin](https://github.com/JinheLin)

    TiFlash 引擎的数据扫描流程包含 MVCC 过滤和扫描列数据等操作。由于 MVCC 过滤和其他数据扫描操作具有较高的耦合性，导致无法对数据扫描流程进行优化改进。在 v6.6.0 中，TiFlash 将整体数据扫描流程中的 MVCC 过滤操作进行解耦，提供独立的 MVCC 位图过滤器，为后续优化数据扫描流程提供基础。

* 批量聚合数据请求 [#39361](https://github.com/pingcap/tidb/issues/39361) @[cfzjywxk](https://github.com/cfzjywxk) @[you06](https://github.com/you06)

    当 TiDB 向 TiKV 发送数据请求时， 会根据数据所在的 Region 将请求编入不同的子任务，每个子任务只处理单个 Region 的请求。 当访问的数据离散度很高时， 即使数据量不大，也会生成众多的子任务，进而产生大量 RPC 请求，消耗额外的时间。 在 v6.6.0 中，TiDB 支持将发送到相同 TiKV 实例的数据请求部分合并，减少子任务的数量和 RPC 请求的开销。 在数据离散度高的情况下，批量化请求能够将性能提升 50% 以上。 

    此特性默认关闭， 通过系统变量 [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) 设置批量请求的大小即可开启。

* 新增一系列优化器 Hint [#39964](https://github.com/pingcap/tidb/issues/39964) @[Reminiscent](https://github.com/Reminiscent)

    TiDB 在新版本中增加了一系列优化器 Hint， 用来控制 `LIMIT` 操作的执行计划选择，以及 MPP 执行过程中的部分行为。 其中包括：

    - [`KEEP_ORDER()`](/optimizer-hints.md#keep_ordert1_name-idx1_name--idx2_name-): 提示优化器使用指定的索引，读取时保持索引的顺序。 生成类似 `Limit + IndexScan(keep order: true)` 的计划。
    - [`NO_KEEP_ORDER()`](/optimizer-hints.md#no_keep_ordert1_name-idx1_name--idx2_name-): 提示优化器使用指定的索引，读取时不保持顺序。 生成类似 `TopN + IndexScan(keep order: false)` 的计划。
    - [`SHUFFLE_JOIN()`](/optimizer-hints.md#shuffle_joint1_name--tl_name-): 针对 MPP 生效。 提示优化器对指定表使用 Shuffle Join 算法。 
    - [`BROADCAST_JOIN()`](/optimizer-hints.md#broadcast_joint1_name--tl_name-): 针对 MPP 生效。提示优化器对指定表使用 Broadcast Join 算法。
    - [`MPP_1PHASE_AGG()`](/optimizer-hints.md#mpp_1phase_agg): 针对 MPP 生效。提示优化器对指定查询块中所有聚合函数使用一阶段聚合算法。
    - [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg): 针对 MPP 生效。 提示优化器对指定查询块中所有聚合函数使用二阶段聚合算法。

    优化器 Hint 的持续引入，为用户提供了更多的干预手段，有助于 SQL 性能问题的解决，并提升了整体性能的稳定性。

* 带有子查询和 `LIMIT` 子句的 SQL 可进入计划缓存 [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678)

    TiDB 移除了执行计划缓存的一部分限制， 从而使更多的 SQL 从计划缓存中获益，提升执行效率。

    * 带有子查询的 SQL 可进入执行计划缓存，如 `select * from t where a > (select ...)`。
    * `LIMIT` 后带有变量的子句可进入执行计划缓存， 如 `Limit ?` 或者 `Limit 10, ?`。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* 悲观锁队列的稳定唤醒模型 [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta)

    如果业务场景存在单点悲观锁冲突频繁的情况，原有的随机唤醒机制会造成事务响应时间的不确定性，长尾延迟高，甚至获取超时。 在 v6.6.0 中，通过设置系统变量 [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入) 为 `ON` 可以开启悲观锁的稳定唤醒模型。 在新的唤醒模型下， 队列的唤醒顺序可被严格控制，避免无效的唤醒造成的资源浪费，在锁冲突严重的场景中，能够减少长尾延时，降低 P99 响应时间。

    更多信息，请参考[用户文档](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入)。

### 事务

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 基于资源组的资源管控 (实验特性) #[38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    TiDB 集群支持创建资源组， 将不用的数据库用户映射到对应的资源组中，根据实际需要设置每个资源组的配额。 当集群资源紧张时， 来自同一个资源组的会话所使用的全部资源将被限制在配额内， 避免其中一个资源组过度消耗从而抑制其他资源组中的会话正常运行。 系统内置视图会对资源的实际使用情况进行反馈和展示， 协助用户更合理地配置资源。 

    资源管控技术的引入对 TiDB 具有里程碑的意义， 它能够将一个分布式数据库集群中划分成多个逻辑单元， 即使个别单元对资源过度使用，也不会完全挤占其他单元所需的资源。 利用这个技术， 用户可以将数个来自不同系统的中小型应用合入一个 TiDB 集群中， 个别应用的负载提升，不会影响其他业务的正常运行；而在系统负载较低的时候，繁忙的应用即使超过限额，也仍旧可以被分配到需要的系统资源，达到资源的最大化利用。  同样的， 用户可以选择将所有测试环境合入一个集群，或者将消耗较大的批量任务编入一个单独的资源组， 在保证重要应用获得必要资源的同时，提升硬件利用率， 降低运行成本。 另外，合理利用资源管控技术将会减少集群数量，降低运维难度及管理成本。

    在 v6.6 中， 启用资源管控技术需要同时打开 TiDB 的全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) 及 TiKV 的配置项 [`resource_control.enabled`](/tikv-configuration-file.md#tidb_enable_resource_control-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5)。 当前支持的限额方式是基于"[用量](/tidb-RU.md)" (即 Request Unit 或 RU )，RU 是 TiDB 对 CPU、IO 等系统资源的统一抽象单位。 

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

### 易用性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 支持动态修改参数 store-io-pool-size [#13964](https://github.com/tikv/tikv/issues/13964) @[LykxSassinator](https://github.com/LykxSassinator)

    TiKV 中的 raftstore.store-io-pool-size 参数用于设定处理 Raft I/O 任务的线程池中线程的数量，需要在 TiKV 性能调优时进行修改调整。在 v6.6.0 版本之前，这个参数无法动态修改。v6.6.0 支持对该参数的动态修改功能，提高了 TiKV 性能调优的灵活性。

    更多信息，请参考[用户文档](/dynamic-config.md)。

### MySQL 兼容性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据共享与订阅

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 部署及运维

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) | 新增  | 该变量是资源管控特性的开关。该变量设置为 `ON` 后，集群支持应用按照资源组做资源隔离。 |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) | 修改 | 此变量可用于生产环境。 设置 `IndexLookUp` 算子回表时多个 Coprocessor Task 的 batch 大小。`0` 代表不使用 batch。当 `IndexLookUp` 算子的回表 Task 数量特别多，出现极长的慢查询时，可以适当调大该参数以加速查询。 |
| [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入) | 新增 | 是否对悲观锁启用加强的悲观锁唤醒模型。 |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV | [`resource_control.enabled`](/tikv-configuration-file.md#tidb_enable_resource_control-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) | 新增 | 是否支持按照资源组配额调度。 默认 `false` ，即关闭按照资源组配额调度。 |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### 其他

## 废弃功能

## 改进提升

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 错误修复

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()
