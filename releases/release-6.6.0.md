---
title: TiDB 6.6.0 Release Notes
---

# TiDB 6.6.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.6.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.6/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 6.6.0 版本中，你可以获得以下关键特性：

- 绑定历史执行计划 GA，支持根据任意节点产生的历史执行计划创建 SQL Binding，进一步产品易用性。
- TiDB Data Migration (DM) 集成 TiDB Lightning 的 Physical Import 模式，使得 DM 全量数据迁移时的性能最高提升 10 倍，大幅缩短大数据量场景下的迁移时间。
- 允许用户在 TiDB Dashboard 界面上快速完成 SQL 语句与特定执行计划的绑定，提升计划绑定过程的效率和体验。
- 支持 MySQL 语法兼容的外键约束，帮助保持数据一致性和提升数据质量。
- TiFlash 支持 Stale Read 功能，进一步提高查询性能。
- 扩展 `PLAN REPLAYER` 命令，自动捕获执行计划的生成，提升执行计划不稳定问题的诊断效率。
- 支持基于资源组的资源管控，将不用的数据库用户映射到对应的资源组中，根据实际需要设置每个资源组的配额（实验特性）。
- 引入 MySQL 兼容的多值索引，增强 JSON 类型，提升 TiDB 对 MySQL 8.0 的兼容性（实验特性）。

## 新功能

### SQL

* 支持 DDL 动态资源管控（实验性特性） [#issue](链接)  @[hawkingrei](https://github.com/hawkingrei) **tw@ran-huang**

    TiDB v6.6.0 版本引入了 DDL 动态资源管控， 通过自动控制 DDL 的 CPU 和内存使用量，尽量降低 DDL 变更任务对线上业务的影响。

* 支持兼容 MySQL 语法的外键约束 [#18209](https://github.com/pingcap/tidb/issues/18209) @[crazycs520](https://github.com/crazycs520) **tw@Oreoxmt**

    TiDB v6.6.0 引入了兼容 MySQL 语法的外键约束功能，支持在表内、表间关联数据并进行约束校验，并且支持集联操作。该特性有助于保持数据一致性，提升数据质量，也方便数据建模。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-foreign-key.md)。

* 支持通过 `FLASHBACK CLUSTER TO TIMESTAMP` 命令闪回 DDL 操作 [#14088](https://github.com/tikv/tikv/issues/14045) @[Defined2014](https://github.com/Defined2014) @[JmPotato](https://github.com/JmPotato) **tw@ran-huang**

    [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) 语句支持在 Garbage Collection (GC) life time 内快速回退整个集群到指定的时间点。在 TiDB v6.6.0 版本中，该功能新增了支持撤销 DDL 操作，适用于快速撤消集群的 DML 或 DDL 误操作、支持分钟级别的快速回退集群、支持在时间线上多次回退以确定特定数据更改发生的时间。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-flashback-to-timestamp.md)。

* 支持 DDL 分布式并行执行框架（实验特性） [#issue](https://github.com/pingcap/tidb/issues/37125)  @[zimulala](https://github.com/zimulala) **tw@ran-huang**

    在过去的版本中，整个 TiDB 集群中仅允许一个 TiDB 实例作为 DDL Owner 有权处理 Schema 变更任务。为了进一步提升 DDL 的并发性，TiDB v6.6.0 版本引入了 DDL 分布式并行执行框架，支持集群中所有的 TiDB 实例可以并发执行同一个任务的 `StateWriteReorganization` 阶段，加速 DDL 的执行。该功能由系统变量 [`tidb_ddl_distribute_reorg`](/system-variables.md#tidb_ddl_distribute_reorg-从-v660-版本开始引入) 控制是否开启，目前只支持 `Add Index` 操作。

    更多信息，请参考[用户文档](/system-variables.md#tidb_ddl_distribute_reorg-从-v660-版本开始引入)。

* 支持 MySQL 兼容的多值索引 (Multi-Valued Index)（实验特性）[#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) **tw@TomShawn**

    TiDB 在 v6.6.0 引入了 MySQL 兼容的多值索引 (Multi-Valued Index)。过滤 JSON 列类型中某个数组的值是常见的操作，但普通索引对这类操作起不到加速作用。在数组上创建多值索引能够大幅提升过滤的性能。如果 JSON 类型中的某个数组上存在多值索引，那么可以利用多值索引过滤带有 `MEMBER OF()`、`JSON_CONTAINS()`、`JSON_OVERLAPS()` 函数的检索条件，从而减少大量的 I/O 消耗，提升运行速度。

    多值索引的引入， 进一步增强了 JSON 类型， 同时也提升了 TiDB 对 MySQL 8.0 的兼容性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

* 绑定历史执行计划 GA [#39199](https://github.com/pingcap/tidb/issues/39199) @[fzzf678](https://github.com/fzzf678) **tw@TomShawn**

    在 v6.5.0 中，TiDB 扩展了 [`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md) 语句中的绑定对象，支持根据历史执行计划创建绑定。在 v6.6.0 中该功能 GA，执行计划的选择不仅限于当前 TiDB 节点，任意 TiDB 节点产生的历史执行计划都可以被选为 [SQL Binding](/sql-statements/sql-statement-create-binding.md) 的目标，进一步提升了功能的易用性。

    更多信息，请参考[用户文档](/sql-plan-management.md#根据历史执行计划创建绑定)。

* [Placement Rules in SQL](/placement-rules-in-sql.md) 支持指定 `SURVIVAL_PREFERENCE` [#38605](https://github.com/pingcap/tidb/issues/38605) @nolouch[https://github.com/nolouch] **tw@qiancai**

    `SURVIVAL_PREFERENCES` 为数据提供了生存偏好设置，从而提高数据的容灾生存能力。通过指定 `SURVIVAL_PREFERENCE`，你可以：

    - 对于跨区域部署的 TiDB 集群，你可以控制当指定数据库或表在某个区域产生故障时，也能在另一个区域提供服务。
    - 对于单区域部署的 TiDB 集群，你可以控制当指定数据库或表在某个可用区产生故障时，也能在另一个可用区提供服务。

    更多信息，请参考[用户文档](/placement-rules-in-sql.md#生存偏好)。

### 安全

* TiFlash 支持 TLS 证书自动轮换 [#5503](https://github.com/pingcap/tiflash/issues/5503) @[ywqzzy](https://github.com/ywqzzy) **tw@qiancai**

    TiFlash TLS 证书自动轮换指在开启组件间加密传输的 TiDB 集群上，当 TiFlash 的 TLS 证书过期需要重新签发一个新 TLS 证书给 TiFlash 时，支持自动加载新的 TiFlash TLS 证书，无需重启 TiDB 集群。TiDB 集群内部组件之间 TLS 过期轮换不影响 TiDB 集群的正常使用，保障了 TiDB 集群的高可用。

    更多信息，请[用户文档](/enable-tls-between-components.md)。

### 可观测性

* 支持在 TiDB Dashboard 中快速绑定执行计划 [#781](https://github.com/pingcap/tidb-dashboard/issues/781) @[YiniXu9506](https://github.com/YiniXu9506) **tw@ran-huang**

    TiDB v6.6.0 中引入了执行计划快速绑定功能，允许用户在 TiDB Dashboard 中一分钟内完成 SQL 与特定计划的绑定。

    通过提供友好的界面，简化了在 TiDB 上绑定计划的过程，减少计划绑定过程的复杂性，提高计划绑定过程的效率和用户体验。

    更多信息，请参考[用户文档](/dashboard/dashboard-statement-details.md#快速绑定执行计划)。

* 为执行计划缓存增加告警 @[qw4990](https://github.com/qw4990) **tw@TomShawn**

    当执行计划无法被缓存时，TiDB 会通过告警的方式提示该计划无法被缓存的原因，降低诊断的难度。例如：

    ```sql
    mysql> PREPARE st FROM 'SELECT * FROM t WHERE a<?';
    Query OK, 0 rows affected (0.00 sec)

    mysql> SET @a='1';
    Query OK, 0 rows affected (0.00 sec)

    mysql> EXECUTE st USING @a;
    Empty set, 1 warning (0.01 sec)

    mysql> SHOW WARNINGS;
    +---------+------+----------------------------------------------+
    | Level   | Code | Message                                      |
    +---------+------+----------------------------------------------+
    | Warning | 1105 | skip plan-cache: '1' may be converted to INT |
    +---------+------+----------------------------------------------+
    ```

    在以上例子中，优化器进行了非 INT 类型到 INT 类型的转换，产生的执行计划可能随着参数变化而存在风险，因此 TiDB 不缓存该计划。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md#prepared-plan-cache-诊断)。

* 在慢查询中增加告警字段 [#39893](https://github.com/pingcap/tidb/issues/39893) @[time-and-fate](https://github.com/time-and-fate) **tw@Oreoxmt**

    慢查询日志新增 `Warnings` 字段，以 JSON 格式记录该慢查询语句在执行过程中产生的警告，以帮助诊断查询性能问题。你也可以在 TiDB Dashboard 中的慢查询页面中查看。

    更多信息，请参考[用户文档](/identify-slow-queries.md)。

* 自动捕获执行计划的生成 [#38779](https://github.com/pingcap/tidb/issues/38779) @[Yisaer](https://github.com/Yisaer) **tw@ran-huang**

    在执行计划问题的排查过程中，`PLAN REPLAYER` 能够协助保存现场，提升诊断的效率。 但在个别场景中，一些执行计划的生成无法任意重现，给诊断工作增加了难度。针对这类问题，在 TiDB v6.6.0 中，`PLAN REPLAYER` 扩展了自动捕获的能力。 通过 `PLAN REPLAYER CAPTURE` 命令字，用户可提前注册目标 SQL，也可以同时指定目标执行计划。当 TiDB 检测到执行的 SQL 和执行计划与注册目标匹配时，会自动生成并打包 `PLAN REPLAYER` 的信息，提升执行计划不稳定时的诊断效率。

    启用这个功能需要设置系统变量 [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) 为 `ON`。

    更多信息，请参考[用户文档](/sql-plan-replayer.md#使用-plan-replayer-capture-抓取目标计划)。

* 持久化 statements summary（实验特性） [#40812](https://github.com/pingcap/tidb/issues/40812) @[mornyx](https://github.com/mornyx) **tw@shichun-0415**

    v6.6.0 之前版本，statements summary 数据在内存中维护，一旦 TiDB 发生重启，数据便会全部丢失。开启 statements summary 持久化特性后，历史数据将会定期被写入磁盘，相关系统表的查询数据源也将由内存变为磁盘。TiDB 重启后，历史数据将依然保持存在。

    更多信息，请参考[用户文档](/statement-summary-tables.md#持久化-statements-summary)。

### 性能

* 在高可靠存储环境中使用 Witness 节约成本 [#12876](https://github.com/tikv/tikv/issues/12876) @[Connor1996](https://github.com/Connor1996) @[ethercflow](https://github.com/ethercflow) **tw@Oreoxmt**

    在云环境中，当 TiKV 使用如 Amazon Elastic Block Store 或 Google Cloud Platform 的 Persistent Disk 作为单节点存储时，它们提供的持久性相比物理磁盘更高。此时，TiKV 使用 3 个 Raft 副本虽然可行，但并不必要。为了降低成本，TiKV 引入了 Witness 功能，即 2 Replicas With 1 Log Only 机制。其中 1 Log Only 副本仅存储 Raft 日志但不进行数据 apply，依然可以通过 Raft 协议保证数据一致性。与标准的 3 副本架构相比，Witness 可以节省存储资源及 CPU 使用率。

    更多信息，请参考[用户文档](/use-witness-to-save-costs.md)。

* TiFlash 支持 Stale Read 功能 [#4483](https://github.com/pingcap/tiflash/issues/4483) @[hehechen](https://github.com/hehechen) **tw@qiancai**

    Stale Read 功能是从 TiDB v5.1.1 开始正式引入的，支持读取指定时间点或时间范围内的历史数据。Stale Read 允许直接读取 TiKV 本地副本数据，可以降低读取延迟，提升查询性能。在 v6.6.0 之前的版本中， TiFlash 并不支持 Stale Read 功能，即使 Stale Read 查询的表包含 TiFlash 副本，TiDB 也只能使用 TiKV 副本进行查询。

    在 v6.6.0 中，TiFlash 实现了对 Stale Read 功能的支持。当使用 `AS OF TIMESTAMP` 语法或 `tidb_read_staleness` 系统变量等方式查询历史数据时，如果查询的表包含 TiFlash 副本，优化器可以选择 TiFlash 副本读取对应的数据，从而进一步提高查询性能。

    更多信息，请参考[用户文档](/stale-read.md)。

* 支持下推字符串函数 `regexp_replace` 至 TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai**

* 批量聚合数据请求 [#39361](https://github.com/pingcap/tidb/issues/39361) @[cfzjywxk](https://github.com/cfzjywxk) @[you06](https://github.com/you06) **tw@TomShawn**

    TiDB 向 TiKV 发送数据请求时，会根据数据所在的 Region 将请求编入不同的子任务，每个子任务只处理单个 Region 的请求。当访问的数据离散度很高时，即使数据量不大，也会生成众多的子任务，进而产生大量 RPC 请求，消耗额外的时间。自 v6.6.0 起，TiDB 支持将发送到相同 TiKV 实例的数据请求部分合并，减少子任务的数量和 RPC 请求的开销。在数据离散度高且 gRPC 线程池资源紧张的情况下，批量化请求能够将性能提升 50% 以上。

    此特性默认打开，可通过系统变量 [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) 设置批量请求的大小。

* 新增若干优化器 Hint [#39964](https://github.com/pingcap/tidb/issues/39964) @[Reminiscent](https://github.com/Reminiscent) **tw@TomShawn**

    TiDB 在 v6.6.0 中增加了若干优化器 Hint，用来控制 `LIMIT` 操作的执行计划选择：

    - [`ORDER_INDEX()`](/optimizer-hints.md#keep_ordert1_name-idx1_name--idx2_name-)：提示优化器使用指定的索引，读取数据时保持索引的顺序，生成类似 `Limit + IndexScan(keep order: true)` 的计划。
    - [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_keep_ordert1_name-idx1_name--idx2_name-)：提示优化器使用指定的索引，读取数据时不保持顺序，生成类似 `TopN + IndexScan(keep order: false)` 的计划。

    持续引入优化器 Hint 为用户提供了更多的干预手段，有助于解决 SQL 性能问题，并提升了整体性能的稳定性。

* 解除执行计划缓存对 `LIMIT` 子句的限制 [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678) **tw@shichun-0415**

    TiDB 移除了执行计划缓存的限制，`LIMIT` 后带有变量的子句可进入执行计划缓存， 如 `Limit ?` 或者 `Limit 10, ?`。这使得更多的 SQL 能够从计划缓存中获益，提升执行效率。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* 支持悲观锁队列的稳定唤醒模型 [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta) **tw@TomShawn**

    如果业务场景存在单点悲观锁冲突频繁的情况，原有的唤醒机制无法保证事务获取锁的时间，造成长尾延迟高，甚至获取锁超时。自 v6.6.0 起，用户可通过设置系统变量 [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入) 为 `ON` 开启悲观锁的稳定唤醒模型。在该唤醒模型下，队列的唤醒顺序可被严格控制，避免无效唤醒造成的资源浪费。在锁冲突严重的场景中，能够减少长尾延时，降低 P99 响应时间。

    更多信息，请参考[用户文档](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入)。

* TiFlash 引擎支持带压缩的数据交换 [#6620](https://github.com/pingcap/tiflash/issues/6620) @[solotzg](https://github.com/solotzg) **tw@TomShawn**

    为了协同多节点进行计算，TiFlash 引擎需要在不同节点中进行数据交换。当需要交换的数据量非常大时，数据交换的性能可能影响整体计算效率。在 v6.6.0 版本中，TiFlash 引擎引入压缩机制，在必要时对需要交换的数据进行压缩，然后进行交换，从而提升数据交换效率。

    更多信息，参见[用户文档](/explain-mpp.md#启用-mpp-数据压缩的执行计划)。

### 事务

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 稳定性

* 基于资源组的资源管控 (实验特性) #[38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp) **tw@hfxsd**

    TiDB 集群支持创建资源组，将不同的数据库用户映射到对应的资源组中，根据需要设置每个资源组的配额。当集群资源紧张时，来自同一个资源组的会话所使用的全部资源将被限制在配额内，避免其中一个资源组过度消耗从而抑制其他资源组中的会话正常运行。系统内置视图会对资源的实际使用情况进行展示，协助用户更合理地配置资源。

    资源管控特性的引入对 TiDB 具有里程碑的意义。它能够将一个分布式数据库集群划分成多个逻辑单元，即使个别单元对资源过度使用，也不会挤占其他单元所需的资源。利用该特性：

    - 你可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载提升，不会影响其他业务的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。
    - 你可以选择将所有测试环境合入一个集群，或者将消耗较大的批量任务编入一个单独的资源组，在保证重要应用获得必要资源的同时，提升硬件利用率，降低运行成本。

    此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

    在 v6.6 中， 启用资源管控技术需要同时打开 TiDB 的全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 及 TiKV 的配置项 [`resource_control.enabled`](/tikv-configuration-file.md#tidb_enable_resource_control)。 当前支持的限额方式是基于"[用量](/tidb-resource-control.md#什么是-request-unit-ru)" (即 Request Unit 或 RU )，RU 是 TiDB 对 CPU、IO 等系统资源的统一抽象单位。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* 使用临时 Witness 副本来加速副本恢复 [#12876](https://github.com/tikv/tikv/issues/12876) @[Connor1996](https://github.com/Connor1996) @[ethercflow](https://github.com/ethercflow) **tw@Oreoxmt**

    Witness 功能可用于快速恢复 failover，以提高系统可用性和数据持久性。例如在 3 缺 1 的情况下，虽然满足多数派要求，但是系统很脆弱，而完整恢复一个新成员的时间通常很长（需要先拷贝 snapshot 然后 apply 最新的日志），特别是 Region snapshot 比较大的情况。而且拷贝副本的过程可能会对不健康的副本造成更多的压力。因此，先添加一个 Witness 可以快速下掉不健康的节点，保证恢复数据过程中日志的安全性。

    更多信息，请参考[用户文档](/use-witness-to-speed-up-failover.md)。

* 支持配置只读存储节点来执行资源消耗型任务 [#issue号](链接) @[v01dstar](https://github.com/v01dstar) **tw@Oreoxmt**

    在生产环境中，可能有部分只读操作定期消耗大量资源，对整个集群的性能产生影响，比如备份和大规模数据读取分析等。TiDB v6.6.0 支持配置只读存储节点，用来执行重度资源消耗的只读任务，避免对线上业务的影响。目前支持 TiDB、TiSpark 和 BR 读取只读节点上的数据。你可以按照[操作步骤](/readonly-nodes.md#操作步骤)配置只读存储节点，并通过 TiDB 系统变量 `tidb_replica_read`、TiSpark 配置项 `spark.tispark.replica_read` 或 br 命令行参数 `--backup-replica-read-label` 指定数据读取位置，以保证集群性能稳定。

     更多信息，请参考[用户文档](/best-practices/readonly-nodes.md)。

### 易用性

* 支持动态修改参数 `store-io-pool-size` [#13964](https://github.com/tikv/tikv/issues/13964) @[LykxSassinator](https://github.com/LykxSassinator) **tw@shichun-0415**

    TiKV 中的 [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-从-v530-版本开始引入)用于设定处理 Raft I/O 任务的线程池中线程的数量，需要在 TiKV 性能调优时进行修改调整。在 v6.6.0 版本之前，这个参数无法动态修改。v6.6.0 支持动态修改该参数，提高了 TiKV 性能调优的灵活性。

    更多信息，请参考[用户文档](/dynamic-config.md)。

* 支持指定集群初次启动时的初始化 SQL 脚本 [#35624](https://github.com/pingcap/tidb/issues/35624) @[morgo](https://github.com/morgo) **tw@shichun-0415**

    TiDB 集群初次启动时，可通过命令行参数 `--initialize-sql-file` 指定执行的 SQL 脚本。该功能可用于修改系统变量的值，或者创建用户、分配权限等。

    更多信息，请参考[配置项 `initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-从-v660-版本开始引入)。

### MySQL 兼容性

* 支持兼容 MySQL 语法的外键约束 [#18209](https://github.com/pingcap/tidb/issues/18209) @[crazycs520](https://github.com/crazycs520) **tw@Oreoxmt**

    更多信息，请参考 v6.6.0 Release Notes 中 [SQL 部分](#sql)以及[用户文档](/sql-statements/sql-statement-foreign-key.md)。

### 数据迁移

* TiDB Data Migration(DM) 集成了 TiDB Lightning 的 Physical Import Mode，全量迁移性能提升最高达到 10 倍  @[lance6716](https://github.com/lance6716) **tw@ran-huang**

    在 v6.6.0 版本中，DM 的全量迁移能力集成了 TiDB Lightning 的 Physical Import Mode，使得 DM 全量数据迁移的性能最高可提升 10 倍，大大缩短了大数据量场景下的迁移时间。在 v6.6.0 以前，数据量较多的场景下，需要单独配置 TiDB Lightning 的 Physical Import Mode 任务来进行快速的全量数据迁移，再用 DM 来进行增量数据迁移，配置较为复杂。从 v6.6.0 起，用户迁移大数据量的场景，无需再配置 TiDB Lightning 的任务，使用一个 DM 任务即可完成。

    更多信息，请参考[用户文档](/dm/dm-precheck.md#physical-import-检查项)。

### 数据共享与订阅

* TiKV-CDC 工具 GA，支持订阅 RawKV 的数据变更 [#48](https://github.com/tikv/migration/issues/48) @[zeminzhou](https://github.com/zeminzhou) @[haojinming](https://github.com/haojinming) @[pingyu](https://github.com/pingyu) **tw@Oreoxmt**

    TiKV-CDC 是一个 TiKV 集群的 CDC (Change Data Capture) 工具。TiKV 可以独立于 TiDB，与 PD 构成 KV 数据库，此时的产品形态为 RawKV。TiKV-CDC 支持订阅 RawKV 的数据变更，并实时同步到下游 TiKV 集群，从而实现 RawKV 的跨集群复制。

    更多信息，请参考[用户文档](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc-cn/)。

* TiCDC 支持在 Kafka 同步任务上开启单表的横向扩展功能，将单表的同步任务下发到多个 TiCDC 节点上执行 [#7720](https://github.com/pingcap/tiflow/issues/7720) @[overvenus](https://github.com/overvenus) **tw@Oreoxmt**

    在 v6.6.0 之前，当上游单表写入量较大时，单表的复制能力无法横向扩展导致同步延迟增加。自 TiCDC v6.6.0 起，下游为 Kafka 的同步任务可以将上游单表的同步任务下发到多个 TiCDC 节点上执行，实现单表同步性能的横向扩展。

    更多信息，请参考[用户文档](/ticdc/ticdc-sink-to-kafka.md#横向扩展大单表的负载到多个-ticdc-节点)。

### 部署及运维

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_amend_pessimistic_txn`](/system-variables.md#tidb_enable_amend_pessimistic_txn-从-v407-版本开始引入) | 删除  | 在 v6.5.0 中该变量被废弃。自 v6.6.0 起，该变量以及 `AMEND TRANSACTION` 特性被删除。TiDB 会使用[元数据锁机制](/metadata-lock.md)解决 `Information schema is changed` 报错的问题。  |
| [`tidb_enable_concurrent_ddl`](/system-variables.md#tidb_enable_concurrent_ddl-从-v620-版本开始引入) | 删除 | 这个变量用于控制是否让 TiDB 使用并发 DDL 语句。自 v6.6.0 起，该变量被删除。 |
| [`tidb_ttl_job_run_interval`](/system-variables.md#tidb_ttl_job_run_interval-从-v650-版本开始引入) | 删除 | 这个变量用于控制 TTL 后台清理任务的调度周期。自 v6.6.0 起删除该变量，因为自 v6.6.0 起 TiDB 为每张表提供了属性 `TTL_JOB_INTERVAL` 用于配置 TTL 运行的间隔，允许用户为每张表设置不同的运行间隔，比系统变量更加灵活。 |
| [`foreign_key_checks`](/system-variables.md#foreign_key_checks) | 修改 | 用于控制是否开启外键约束检查。默认值由 `OFF` 修改为 `ON`，表示默认开启外键检查。|
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-从-v630-版本开始引入) | 修改 | 用于控制是否开启外键功能。默认值由 `OFF` 修改为 `ON`，表示默认开启外键功能。|
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) | 修改 | 新增选项 `prefer-leader`，以提高 TiDB 集群整体的读可用性。该选项被启用时，TiDB 会优先选择 Leader 副本进行读取操作；当 Leader 副本的处理性能显著下降时，TiDB 会自动将读操作转发给 Follower 副本。|
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) | 修改 | 新增选项 `learner`，指定 TiDB 从只读节点中读取数据的 learner 副本。  |
| [`tidb_store_batch_size`](/[system-variables.md](http://system-variables.md/)#tidb_store_batch_size) | 修改 | 该变量设置 `IndexLookUp` 算子回表时多个 Coprocessor Task 的 batch 大小。`0` 代表不使用 batch。自 v6.6.0 起，默认值由 `0` 调整为 `4`，即每批请求会有 4 个 Coprocessor Task 被 batch 到一个 task 中。 |
| [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-从-v660-版本开始引入)  |  新增  |  https://github.com/pingcap/docs-cn/pull/12922/files **tw@TomShawn**  |
| [`mpp_version`](/system-variables.md#mpp_version-从-v660-版本开始引入)  |  新增  |  https://github.com/pingcap/docs-cn/pull/12922/files **tw@TomShawn**   |
| [`tidb_ddl_distribute_reorg`](/system-variables.md#tidb_ddl_distribute_reorg-从-v660-版本开始引入) | 新增 | 这个变量用来控制是否开启分布式执行 DDL reorg 阶段，来提升此阶段的速度。默认值为 `OFF`，表示默认不开启分布式执行 DDL reorg 阶段。目前此开关只对 `ADD INDEX` 语句有效。|
| [`tidb_enable_plan_cache_for_param_limit`](/system-variables.md#tidb_enable_plan_cache_for_param_limit-从-v660-版本开始引入) | 新增 | 用来控制 Prepared Plan Cache 是否缓存 `limit` 后带有参数的执行计划。默认值为 `ON`，表示 Prepared Plan Cache 默认缓存 `limit` 后带有参数的执行计划。目前不支持缓存 `Limit` 后面的 `Count` 具体参数值大于 10000 的执行计划。 |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) | 新增 | 这个变量用来控制是否开启 [`PLAN REPLAYER CAPTURE`](/sql-plan-replayer.md#使用-plan-replayer-capture-抓取目标计划)。默认值 `OFF`，代表关闭 `PLAN REPLAYER CAPTURE`。 |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) | 新增  | 该变量是资源管控特性的开关。该变量设置为 `ON` 后，集群支持应用按照资源组做资源隔离。 |
| [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入) | 新增 | 是否对悲观锁启用加强的悲观锁唤醒模型。默认值为 `OFF`，表示默认不对悲观锁启用加强的悲观锁唤醒模型。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV  |  `enable-statistics`  |  删除   |  该配置项指定是否开启 RocksDB 的统计信息收集功能。从 v6.6.0 起，删除该配置项。所有集群默认开启统计信息收集，以便于故障排查。详情参见 [tikv/tikv#13942](https://github.com/tikv/tikv/pull/13942)。  |
| TiKV | `storage.block-cache.shared` | 删除 | 从 v6.6.0 起删除该配置项，默认开启 block cache 且无法关闭，详情参见 [#12936](https://github.com/tikv/tikv/issues/12936)。 |
| TiKV | `storage.block-cache.block-cache-size` | 修改 | 从 v6.6.0 起，该配置项仅用于计算 `storage.block-cache.capacity` 的默认值。详情参见 [#12936](https://github.com/tikv/tikv/issues/12936)。 |
| TiFlash |  [`profile.default.max_memory_usage_for_all_queries`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)  |  修改  |  表示所有查询过程中，节点对中间数据的内存限制。自 v6.6.0 起默认值由 `0` 改为 `0.8`，表示节点占总内存的 80%。  |
| TiCDC  | [`consistent.storage`](/ticdc/ticdc-sink-to-mysql.md#使用前提)  |  修改  | redo log 备份文件的地址，除了 NFS，支持的 `scheme` 新增了 GCS 和 Azure。  |
| TiDB  | [`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-从-v660-版本开始引入)  | 新增 | 用于指定 TiDB 集群初次启动时执行的 SQL 脚本。默认值为空。  |
| TiDB  | [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-从-v660-版本开始引入)  |  新增  |  用于控制是否开启 statements summary 持久化。默认值为 `false`，即不开启该功能。  |
| TiDB | [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-从-v660-版本开始引入) | 新增 | 当开启了 statements summary 持久化时，该配置用于指定持久化数据所写入的文件名称，默认为 `tidb-statements.log`。 |
| TiDB | [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-从-v660-版本开始引入) | 新增 | 当开启了 statements summary 持久化时，该配置用于指定持久化数据文件所保留的最大天数，默认为 3 天。 |
| TiDB | [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-从-v660-版本开始引入) | 新增 | 当开启了 statements summary 持久化时，该配置用于限制持久化数据单个文件的大小 (MiB)，默认值为 `64`。 |
| TiDB | [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-从-v660-版本开始引入) | 新增 | 当开启了 statements summary 持久化时，该配置用于限制持久化数据文件最大数量，`0` 表示不限制，默认值为 `0`。 |
| TiKV | [`resource_control.enabled`](/tikv-configuration-file.md#tidb_enable_resource_control-从-v660-版本开始引入) | 新增 | 是否支持按照资源组配额调度。默认为 `false`，即关闭按照资源组配额调度。 |
| PD   | [`switch-witness-interval`](/pd-configuration-file.md#switch-witness-interval-从-v660-版本开始引入)    |   新增       | 控制对同一个 Region 做切换为 Witness 和切换为 Non-Witness 操作的间隔，即对于一个新切换为 Non-Witness 的 Region 在一段时间内不会被切换为 Witness。默认值为 1 小时。         |
| PD   | [`witness-schedule-limit`](/pd-configuration-file.md#witness-schedule-limit-从-v660-版本开始引入)    |   新增       | 控制同时进行的 Witness 调度的任务个数。默认为 4 个。         |
| TiCDC | [`scheduler.region-per-span`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 将表按 Region 个数划分成多个同步范围，这些范围可由多个 TiCDC 节点同步。 |
| DM   | 新增    |    https://github.com/pingcap/docs-cn/pull/12296       |    **tw@ran-huang**      |
| sync-diff-inspector   | [`skip-non-existing-table`](/sync-diff-inspector/sync-diff-inspector-overview.md#配置文件说明)   |  新增 | 当下游数据库的表在上游不存在时，该配置项决定是否跳过对上下游数据库表数量不一致场景的校验。  |
| TiSpark | [`spark.tispark.replica_read`](/tispark-overview.md#tispark-配置) | 新增 | 控制读取副本的类型，可选值为 `leader`、`follower`、`learner`。 |
| TiSpark | [`spark.tispark.replica_read.label`](/tispark-overview.md#tispark-配置) | 新增 | 设置目标 TiKV 节点的标签。 |

### 其他

- 支持动态修改参数 `store-io-pool-size`，增加了 TiKV 性能调优的灵活性。
- 解除了执行计划缓存对 `LIMIT` 子句的限制，提升了执行效率。

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

    - 提供独立的 MVCC 位图过滤器，解耦 TiFlash 整体数据扫描流程中的 MVCC 过滤操作，为后续优化数据扫描流程提供基础 [#6296](https://github.com/pingcap/tiflash/issues/6296) @[JinheLin] **tw@qiancai**
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        优化了 DM 的告警规则和内容。[7376](https://github.com/pingcap/tiflow/issues/7376) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd**

        之前 "DM_XXX_process_exits_with_error" 类告警是遇到错误就报警，有些告警实际是由于数据库链接 长时间 idle 导致，重连后即可恢复。为了减少这类报警，将告警分为可自动恢复错误和不可恢复错误。

        - 对于可自动恢复的错误，只有在 2 分钟内发生超过 3 次时才报警。
        - 对于不可自动恢复的错误，维持原有行为，立即报警。

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + Sync-diff-inspector

        - 新增一个参数 `skip-non-existing-table`，当下游数据库的表在上游不存在时，可配置该参数跳过对上下游数据库表数量不一致场景的校验 [#692](https://github.com/pingcap/tidb-tools/issues/692) @[lichunzhu](https://github.com/lichunzhu) @[liumengya94](https://github.com/liumengya9) **tw@shichun-0415**
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

        - 修复了部分场景下 TiDB 重启导致 TiDB Lightning timeout 卡住的问题 [#33714](https://github.com/pingcap/tidb/issues/33714) @[lichunzhu](https://github.com/lichunzhu) **tw@shichun-0415**
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()
