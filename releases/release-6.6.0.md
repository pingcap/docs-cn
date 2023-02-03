---
title: TiDB 6.6.0 Release Notes
---

# TiDB 6.6.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.6.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.6/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 6.6.0 版本中，你可以获得以下关键特性：

- MySQL 8.0 兼容的多值索引 (Multi-Valued Index) (实验特性)
- 基于资源组的资源管控 (实验特性)
- 悲观锁队列的稳定唤醒模型
- 数据请求的批量聚合

## 新功能

### SQL

* 支持 DDL 动态资源管控（实验性特性） [#issue](链接)  @[hawkingrei](https://github.com/hawkingrei) **tw@ran-huang**

    TiDB v6.6.0 版本引入了 DDL 动态资源管控， 通过自动控制 DDL 的 CPU 和内存使用量，尽量降低 DDL 变更任务对线上业务的影响。

    更多信息，请参考[用户文档](链接)。

* 支持 MySQL 语法兼容的外键约束 （实验特性）[#18209](https://github.com/pingcap/tidb/issues/18209) @[crazycs520](https://github.com/crazycs520) **tw@Oreoxmt**

    TiDB 在 v6.6.0 引入了 MySQL 语法兼容的外键约束特性，支持表内，表间的数据关联和约束校验能力，支持集联操作。该特性有助于保持数据一致性，提升数据质量，也方便客户进行数据建模。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-foreign-key.md)。

* 支持通过`FLASHBACK CLUSTER TO TIMESTAMP` 命令闪回 DDL 操作 [#14088](https://github.com/tikv/tikv/pull/14088) @[Defined2014](https://github.com/Defined2014) @[JmPotato](https://github.com/JmPotato) **tw@ran-huang**

    [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) 语句支持在 Garbage Collection (GC) life time 内快速回退整个集群到指定的时间点，该功能在 TiDB v6.6.0 版本新增支持撤销 DDL 操作，适用于快速撤消集群的 DML 或 DDL 误操作、支持集群分钟级别的快速回退、支持在时间线上多次回退以确定特定数据更改发生的时间。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-flashback-to-timestamp.md)。

* 支持 DDL 分布式并行执行框架（实验性特性） [#issue](链接)  @[zimulala](https://github.com/zimulala) **tw@ran-huang**

    在过去的版本中，整个 TiDB 集群中仅允许一个 TiDB 实例作为 DDL Owner 有权处理 Schema 变更任务，为了进一步提升 DDL 的并发性，TiDB v6.6.0 版本引入了 DDL 分布式并行执行框架，支持集群中所有的 TiDB 实例可以并发执行同一个任务的 `StateWriteReorganization` 阶段，加速 DDL 的执行。目前只支持 `Add Index` 操作。


* MySQL 兼容的多值索引(Multi-Valued Index) (实验特性) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) **tw@TomShawn**

    TiDB 在 v6.6.0 引入了 MySQL 兼容的多值索引 (Multi-Valued Index)。 过滤 JSON 类型中某个数组的值是一个常见操作， 但普通索引对这类操作起不到加速作用，而在数组上创建多值索引能够大幅提升过滤的性能。 如果 JSON 类型中的某个数组上存在多值索引，  带有`MEMBER OF()`，`JSON_CONTAINS()`，`JSON_OVERLAPS()` 这几个函数的检索条件可以利用多值索引进行过滤，减少大量的 I/O 消耗，提升运行速度。

    多值索引的引入， 是对 JSON 类型的进一步增强， 同时也提升了 TiDB 对 MySQL 8.0 的兼容性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

* 绑定历史执行计划 GA [#39199](https://github.com/pingcap/tidb/issues/39199) @[fzzf678](https://github.com/fzzf678) **tw@TomShawn**

    在 v6.5 中，TiDB 扩展了 [`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md) 语句中的绑定对象，支持根据历史执行计划创建绑定。在 v6.6 中这个功能 GA， 执行计划的选择不仅限在当前 TiDB 节点，任意 TiDB 节点产生的历史执行计划都可以被选为 [SQL Binding]((/sql-statements/sql-statement-create-binding.md)) 的目标，进一步提升了功能的易用性。

    更多信息，请参考[用户文档](/sql-plan-management.md#根据历史执行计划创建绑定)。

* [Placement Rules in SQL](https://docs.pingcap.com/zh/tidb/dev/placement-rules-in-sql) 支持指定 `SURVIVAL_PREFERENCE` [#38605](https://github.com/pingcap/tidb/issues/38605) @nolouch[https://github.com/nolouch] **tw@qiancai**

    `SURVIVAL_PREFERENCES` 为数据提供了生存偏好设置，从而提高数据的容灾生存能力。通过指定 `SURVIVAL_PREFERENCE`，你可以：
        - 对于跨区域部署的 TiDB 集群，你可以控制当指定数据库或表在某个区域产生故障时，也能在另一个区域提供服务。
        - 对于单区域部署的 TiDB 集群，你可以控制当指定数据库或表在某个可用区产生故障时，也能在另一个可用区提供服务。

     更多信息，请参考[用户文档](/placement-rules-in-sql.md#生存偏好)。

### 安全

* TiFlash 支持 TLS 证书自动轮换 [#5503](https://github.com/pingcap/tiflash/issues/5503) @[ywqzzy](https://github.com/ywqzzy) **tw@qiancai**

    TiFlash TLS 证书自动轮换指在开启组件间加密传输的 TiDB 集群上，当 TiFlash 的 TLS 证书过期需要重新签发一个新 TLS 证书给 TiFlash 时，支持自动加载新的 TiFlash TLS 证书，无需重启 TiDB 集群。TiDB 集群内部组件之间 TLS 过期轮换不影响 TiDB 集群的正常使用，保障了 TiDB 集群的高可用。

    更多信息，请[用户文档](/enable-tls-between-components.md)。

### 可观测性

* 快速绑定执行计划 [#781](https://github.com/pingcap/tidb-dashboard/issues/781) @[YiniXu9506](https://github.com/YiniXu9506) **tw@ran-huang**

    TiDB 的执行计划快速绑定功能：允许用户在 TiDB Dashboard 中一分钟内完成 SQL 与特定计划的绑定。

    通过提供友好的界面简化在 TiDB 上绑定计划的过程，减少计划绑定过程的复杂性，提高计划绑定过程的效率和用户体验。

    更多信息，请参考[用户文档](/dashboard/dashboard-statement-details.md)。

* 为执行计划缓存增加告警 [#issue号](链接) @[qw4990](https://github.com/qw4990) **tw@TomShawn**

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

* 在慢查询中增加告警字段 [#39893](https://github.com/pingcap/tidb/issues/39893) @[time-and-fate](https://github.com/time-and-fate) **tw@Oreoxmt**

    向慢查询日志中增加一个新的字段 `Warnings` ，以 JSON 格式记录该慢查询语句在执行过程中产生的警告，用来协助查询性能问题的诊断。

    用户也可以在 TiDB Dashboard 中的慢查询页面中查看。

    更多信息，请参考[用户文档](/identify-slow-queries.md)。

* 自动捕获执行计划的生成 [#38779](https://github.com/pingcap/tidb/issues/38779) @[Yisaer](https://github.com/Yisaer) **tw@ran-huang**

    在执行计划问题的排查过程中，`PLAN REPLAYER` 能够协助保存现场，提升诊断的效率。 但在个别场景中，一些执行计划的生成无法任意重现，给诊断工作增加了难度。 针对这类问题， `PLAN REPLAYER` 扩展了自动捕获的能力。 通过 `PLAN REPLAYER CAPTURE` 命令字，用户可提前注册目标 SQL，也可以同时指定目标执行计划， 当 TiDB 检测到执行的 SQL 和执行计划与注册目标匹配时， 会自动生成并打包 `PLAN REPLAYER` 的信息，提升执行计划不稳定问题的诊断效率。

    启用这个功能需要设置系统变量 [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) 为 `ON`。

    更多信息，请参考[用户文档](/sql-plan-replayer.md#使用-plan-replayer-capture-抓取目标计划)。

* Statements Summary 持久化（实验特性） [#40812](https://github.com/pingcap/tidb/issues/40812) @[mornyx](https://github.com/mornyx) **tw@shichun-0415**

    Statements Summary 过去只在内存中维护，一旦 TiDB 发生重启数据便会全部丢失。开启持久化配置后历史数据将会定期被写入磁盘，相关系统表的查询数据源也将由内存变为磁盘，TiDB 发生重启后历史数据将依然保持存在。

    更多信息，请参考[用户文档](/statement-summary-tables.md#持久化-statements-summary)。

### 性能

* 使用 Witness 节约成本  [#12876](https://github.com/tikv/tikv/issues/12876) [@Connor1996](https://github.com/Connor1996) [@ethercflow](https://github.com/ethercflow) **tw@Oreoxmt**

    在云环境中，当 TiKV 使用如 AWS EBS 或 GCP 的 Persistent Disk 作为单节点存储时，它们提供的持久性相比物理磁盘更高。此时，TiKV 使用 3 个 Raft 副本虽然可行，但并不必要。为了降低成本，TiKV 引入了 Witness 功能，即 2 Replicas With 1 Log Only 机制。其中 1 Log Only 副本仅存储 Raft 日志但不进行数据 apply，依然可以通过 Raft 协议保证数据一致性。与标准的 3 副本架构相比，Witness 可以节省存储资源及 CPU 使用率。

    更多信息，请参考[用户文档](/use-witness-to-save-costs.md)。

* TiFlash 支持 Stale Read 功能 [#4483](https://github.com/pingcap/tiflash/issues/4483) @[hehechen](https://github.com/hehechen) **tw@qiancai**

    在 v5.1.1 中，TiDB 正式发布了 Stale Read 功能，支持读取指定时间点或时间范围内的历史数据。Stale Read 允许直接读取 TiKV 本地副本数据，可以降低读取延迟，提升查询性能。在 v6.6.0 之前的版本中， TiFlash 并不支持 Stale Read 功能，即使 Stale Read 查询的表包含 TiFlash 副本，TiDB 也只能使用 TiKV 副本进行查询。在 v6.6.0 中，TiFlash 实现了对 Stale Read 功能的支持。当使用 `AS OF TIMESTAMP` 语法或 `tidb_read_staleness` 系统变量等方式查询指定时间点或时间范围内的历史数据时，如果查询的表包含 TiFlash 副本，优化器可以选择 TiFlash 副本读取对应的数据，从而进一步提高查询性能。

    更多信息，请参考[用户文档](/stale-read.md)。

* 支持下推字符串函数 `regexp_replace` 至 TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai**

* 批量聚合数据请求 [#39361](https://github.com/pingcap/tidb/issues/39361) @[cfzjywxk](https://github.com/cfzjywxk) @[you06](https://github.com/you06) **tw@TomShawn**

    当 TiDB 向 TiKV 发送数据请求时， 会根据数据所在的 Region 将请求编入不同的子任务，每个子任务只处理单个 Region 的请求。 当访问的数据离散度很高时， 即使数据量不大，也会生成众多的子任务，进而产生大量 RPC 请求，消耗额外的时间。 在 v6.6.0 中，TiDB 支持将发送到相同 TiKV 实例的数据请求部分合并，减少子任务的数量和 RPC 请求的开销。 在数据离散度高且 gRPC 线程池资源紧张的情况下，批量化请求能够将性能提升 50% 以上。

    此特性默认打开， 通过系统变量 [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) 设置批量请求的大小。

* 新增一系列优化器 Hint [#39964](https://github.com/pingcap/tidb/issues/39964) @[Reminiscent](https://github.com/Reminiscent) **tw@TomShawn**

    TiDB 在新版本中增加了优化器 Hint， 用来控制 `LIMIT` 操作的执行计划选择。 其中包括：

    - [`ORDER_INDEX()`](/optimizer-hints.md#keep_ordert1_name-idx1_name--idx2_name-): 提示优化器使用指定的索引，读取数据时保持索引的顺序。 生成类似 `Limit + IndexScan(keep order: true)` 的计划。
    - [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_keep_ordert1_name-idx1_name--idx2_name-): 提示优化器使用指定的索引，读取数据时不保持顺序。 生成类似 `TopN + IndexScan(keep order: false)` 的计划。

    优化器 Hint 的持续引入，为用户提供了更多的干预手段，有助于 SQL 性能问题的解决，并提升了整体性能的稳定性。

* 解除执行计划缓存对 `LIMIT` 子句的限制 [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678) **tw@shichun-0415**

    TiDB 移除了执行计划缓存的限制，`LIMIT` 后带有变量的子句可进入执行计划缓存， 如 `Limit ?` 或者 `Limit 10, ?`。这使得更多的 SQL 能够从计划缓存中获益，提升执行效率。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* 悲观锁队列的稳定唤醒模型 [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta) **tw@TomShawn**

    如果业务场景存在单点悲观锁冲突频繁的情况，原有的唤醒机制无法保证事务获取锁的时间，造成长尾延迟高，甚至获取超时。 在 v6.6.0 中，通过设置系统变量 [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入) 为 `ON` 可以开启悲观锁的稳定唤醒模型。 在新的唤醒模型下， 队列的唤醒顺序可被严格控制，避免无效的唤醒造成的资源浪费，在锁冲突严重的场景中，能够减少长尾延时，降低 P99 响应时间。

    更多信息，请参考[用户文档](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入)。

* TiFlash 引擎支持带压缩的数据交换 [#6620](https://github.com/pingcap/tiflash/issues/6620) @[solotzg](https://github.com/solotzg)

    为了协同多节点进行计算，TiFlash 引擎需要在不同节点中进行数据交换。当需要交换的数据量非常大时，数据交换性能可能影响整体计算效率。在 v6.6 版本中，TiFlash 引擎引入压缩机制，在必要时对需要交换的数据进行压缩，然后进行交换，从而提升数据交换效率。

### 事务

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 稳定性

* 基于资源组的资源管控 (实验特性) #[38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp) **tw@hfxsd**

    TiDB 集群支持创建资源组，将不用的数据库用户映射到对应的资源组中，根据实际需要设置每个资源组的配额。当集群资源紧张时，来自同一个资源组的会话所使用的全部资源将被限制在配额内，避免其中一个资源组过度消耗从而抑制其他资源组中的会话正常运行。系统内置视图会对资源的实际使用情况进行反馈和展示，协助用户更合理地配置资源。

    资源管控技术的引入对 TiDB 具有里程碑的意义，它能够将一个分布式数据库集群中划分成多个逻辑单元，即使个别单元对资源过度使用，也不会完全挤占其他单元所需的资源。利用这个技术，你可以将数个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载提升，不会影响其他业务的正常运行；而在系统负载较低的时候，繁忙的应用即使超过限额，也仍旧可以被分配到所需的系统资源，达到资源的最大化利用。 同样的，你可以选择将所有测试环境合入一个集群，或者将消耗较大的批量任务编入一个单独的资源组，在保证重要应用获得必要资源的同时，提升硬件利用率，降低运行成本。另外，合理利用资源管控技术可以减少集群数量，降低运维难度及管理成本。

    在 v6.6 中， 启用资源管控技术需要同时打开 TiDB 的全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) 及 TiKV 的配置项 [`resource_control.enabled`](/tikv-configuration-file.md#tidb_enable_resource_control-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5)。 当前支持的限额方式是基于"[用量](/tidb-RU.md)" (即 Request Unit 或 RU )，RU 是 TiDB 对 CPU、IO 等系统资源的统一抽象单位。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* 使用临时 Witness 副本来加速副本恢复 [#12876](https://github.com/tikv/tikv/issues/12876) [@Connor1996](https://github.com/Connor1996) [@ethercflow](https://github.com/ethercflow) **tw@Orexmt**

    Witness 功能可用于快速恢复 failover，以提高系统可用性。例如在 3 缺 1 的情况下，虽然满足多数派要求，但是系统很脆弱，而完整恢复一个新成员的时间通常很长（需要先拷贝 snapshot 然后 apply 最新的日志），特别是 Region snapshot 比较大的情况。而且拷贝副本的过程可能会对不健康的副本造成更多的压力。因此，先添加一个 Witness 可以快速下掉不健康的节点，保证恢复数据的过程中日志的安全性，后续再由 PD 的 rule checker 将 Witness 副本变为普通的 Voter。

    更多信息，请参考[用户文档](/use-witness-to-speed-up-failover.md)。

* 支持配置专属的只读存储节点来承载高资源消耗的任务  [@v01dstar](https://github.com/v01dstar)

    在实际生产中，可能有部分只读操作定期消耗大量资源，进而影响整个集群的性能，比如备份，大规模数据读取分析等。 受传统 Acitve-Passive 模式的启发， 结合 Placement Rule 和 Follower Reader 技术，TiDB 同样能构建出专属的只读存储节点， 来承载重度资源消耗的只读任务，避免对线上业务的影响。 在 v6.6.0 中，有条件的用户可以按照[推荐步骤](/readonly-nodes.md#操作步骤)配置只读存储节点， 然后通过设置系统变量指定 TiDB 读取只读节点的数据，或者通过客户端参数引导 BR 或 TiSpark 将负载发送至只读存储节点，进而保证整个集群的性能稳定。

     更多信息，请参考[用户文档](/best-practices/readonly-nodes.md)。

### 易用性

* 支持动态修改参数 store-io-pool-size [#13964](https://github.com/tikv/tikv/issues/13964) @[LykxSassinator](https://github.com/LykxSassinator) **tw@shichun-0415**

    TiKV 中的 raftstore.store-io-pool-size 参数用于设定处理 Raft I/O 任务的线程池中线程的数量，需要在 TiKV 性能调优时进行修改调整。在 v6.6.0 版本之前，这个参数无法动态修改。v6.6.0 支持对该参数的动态修改功能，提高了 TiKV 性能调优的灵活性。

    更多信息，请参考[用户文档](/dynamic-config.md)。

* 可通过命令行参数或者配置项在 TiDB 集群初次启动时指定执行的初始化 SQL 脚本 [#35625](https://github.com/pingcap/tidb/pull/35625) @[morgo](https://github.com/morgo) **tw@TomShawn**

    命令行参数 `--initialize-sql-file` 用于指定 TiDB 集群初次启动时执行的 SQL 脚本，可用于修改系统变量的值，或者创建用户、分配权限等。

    更多信息，请参考[配置项 `initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-从-v660-版本开始引入)。

### MySQL 兼容性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* Data Migration(DM) 集成了 Lightning 的 Physical Import Mode ，全量迁移性能最高提升  10 倍  @[lance6716](https://github.com/lance6716) **tw@ran-huang**

    功能描述 ：Data Migration (DM)的全量迁移能力，集成了 Lightning 的 Physical Import Mode ，使得 DM 做全量数据迁移时的性能最高可提升 10 倍，大大缩短了大数据量场景下的迁移时间。原先客户数据量较多时，客户得单独配置 Lightning 的 Physical Import Mode 的任务来做快速的全量数据迁移，之后再用 DM 来做增量数据迁移，配置复杂。现在集成该能力后，用户迁移大数据量的场景，无需再配置 Lightning 的任务，在一个 DM 任务里就可以搞定了。

    更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/12296)。

### 数据共享与订阅

* TiKV-CDC 工具 GA，支持 RawKV 的 Change Data Capture [#48](https://github.com/tikv/migration/issues/48) @[zeminzhou](https://github.com/zeminzhou) @[haojinming](https://github.com/haojinming) @[pingyu](https://github.com/pingyu) **tw@Oreoxmt**

    TiKV-CDC 是一个 TiKV 集群的 CDC (Change Data Capture) 工具。TiKV 可以独立于 TiDB，与 PD 构成 KV 数据库，此时的产品形态为 RawKV。TiKV-CDC 支持订阅 RawKV 的数据变更，并实时同步到下游 TiKV 集群，从而实现 RawKV 的跨集群复制能力。

    更多信息，请参考[用户文档](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc-cn/)。

* 同步到下游 Kafka 的 Changefeed 可将上游单表的同步任务下发到多个 TiCDC Nodes 执行，实现单表同步性能的水平扩展 [#7720](https://github.com/pingcap/tiflow/issues/7720) @[overvenus](https://github.com/overvenus) **tw@Oreoxmt**

    功能描述：下游为 Kafka 的 Changefeed 可将上游单表的复制任务调度到多个 TiCDC Nodes 执行，实现单张表同步性能的水平扩展。在这个功能发布之前，上游单表写入数据量较大时，无法水平扩展单表的复制能力，导致同步延迟增加。该功能发布后，就可以通过水平扩展，解决单表同步性能的问题。

    更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/12693)。

### 部署及运维

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_amend_pessimistic_txn`](/system-variables.md#tidb_enable_amend_pessimistic_txn-从-v407-版本开始引入) | 删除  | 在 v6.5.0 中该变量被废弃。自 v6.6.0 起，该变量以及 `AMEND TRANSACTION` 特性被删除。TiDB 会使用[元数据锁机制](/metadata-lock.md)解决 `Information schema is changed` 报错的问题。  |
| [`tidb_enable_concurrent_ddl`](/system-variables.md#tidb_enable_concurrent_ddl-从-v620-版本开始引入) | 删除 | 这个变量用于控制是否让 TiDB 使用并发 DDL 语句。自 v6.6.0 前，该变量被删除。 |
| [`tidb_ttl_job_run_interval`](/system-variables.md#tidb_ttl_job_run_interval-从-v650-版本开始引入) | 删除 | 这个变量用于控制 TTL 后台清理任务的调度周期。比如，如果当前值设置成了 `1h0m0s`，则代表每张设置了 TTL 属性的表会每小时清理一次过期数据。自 v6.6.0 起删除该变量，因为 **tw@ran-huang** https://github.com/pingcap/docs-cn/pull/12857 |
| [`foreign_key_checks`](/system-variables.md#foreign_key_checks) | 修改 | 用于控制是否开启外键约束检查。默认值由 `OFF` 修改为 `ON`，表示默认开启外键检查。|
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-从-v630-版本开始引入) | 修改 | 用于控制是否开启外键功能。默认值由 `OFF` 修改为 `ON`，表示默认开启外键功能。|
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) | 修改 | 从 v6.6.0 起新增选项 `prefer-leader`， 以提高 TiDB 集群整体的读可用性。该选项被启用时，TiDB 会优先选择 Leader 副本进行读取操作；当 Leader 副本的处理性能显著下降时，TiDB 会自动将读操作转发给 Follower 副本。|
| [`tidb_ddl_distribute_reorg`](/system-variables.md#tidb_ddl_distribute_reorg-从-v660-版本开始引入) | 新增 | 这个变量用来控制是否开启分布式执行 DDL reorg 阶段，来提升此阶段的速度。默认值为 `OFF`，表示默认不开启分布式执行 DDL reorg 阶段。目前此开关只对 `ADD INDEX` 语句有效。|
| [`tidb_enable_plan_cache_for_param_limit`](/system-variables.md#tidb_enable_plan_cache_for_param_limit-从-v660-版本开始引入) | 新增 | 用来控制 Prepared Plan Cache 是否缓存 `limit` 后带有参数的执行计划。默认值为 `ON`，表示 Prepared Plan Cache 默认缓存 `limit` 后带有参数的执行计划。 |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) | 新增  | 该变量是资源管控特性的开关。该变量设置为 `ON` 后，集群支持应用按照资源组做资源隔离。 |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) | 修改 | 此变量可用于生产环境。 设置 `IndexLookUp` 算子回表时多个 Coprocessor Task 的 batch 大小。`0` 代表不使用 batch。当 `IndexLookUp` 算子的回表 Task 数量特别多，出现极长的慢查询时，可以适当调大该参数以加速查询。 |
| [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入) | 新增 | 是否对悲观锁启用加强的悲观锁唤醒模型。默认值为 `OFF`，表示默认不对悲观锁启用加强的悲观锁唤醒模型。 |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) | 新增 | 这个变量用来控制是否开启 [`PLAN REPLAYER CAPTURE`](/sql-plan-replayer.md#使用-plan-replayer-capture-抓取目标计划)。默认值 `OFF`，代表关闭 `PLAN REPLAYER CAPTURE`。 |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) | 修改 | 新增选项 learner ， 指定 TiDB 从只读节点中读取数据的 learner 副本。  |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV  |  `enable-statistics`  |  删除   |  该配置项指定是否开启 RocksDB 的统计信息收集功能。从 v6.6.0 起，删除该配置项。。更多细节，参见 [tikv/tikv#13942](https://github.com/tikv/tikv/pull/13942)。  |
| TiKV | [`resource_control.enabled`](/tikv-configuration-file.md#tidb_enable_resource_control-从-v660-版本开始引入) | 新增 | 是否支持按照资源组配额调度。默认为 `false`，即关闭按照资源组配额调度。 |
| TiKV | `storage.block-cache.shared` | 删除 | 从 v6.6.0 起删除该配置项，默认开启 block cache 且无法关闭。 |
| TiKV | `storage.block-cache.block-cache-size` | 修改 | 从 v6.6.0 起，该配置项仅用于计算 `storage.block-cache.capacity` 的默认值。 |
| TiFlash |  `profile.default.max_memory_usage_for_all_queries`  |  修改  |  表示所有查询过程中，节点对中间数据的内存限制。自 v6.6.0 起默认值由 `0` 改为 `0.8`，表示节点占总内存的 80%。 **tw@shichun-0415** |
| TiCDC  | `consistent.storage`  |  修改  | https://github.com/pingcap/docs-cn/pull/12653/files  **tw@shichun-0415**  |
| TiDB  | [`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-从-v660-版本开始引入)  | 用于指定 TiDB 集群初次启动时执行的 SQL 脚本。默认值为空。  |
| TiDB  | `tidb_stmt_summary...`  |  新增  |  https://github.com/pingcap/docs-cn/pull/12677/files **tw@shichun-0415**  |
| PD   | [`switch-witness-interval`](/pd-configuration-file.md#switch-witness-interval-从-v660-版本开始引入)    |   新增       | 控制对同一个 Region 做切换为 Witness 和切换为 Non-Witness 操作的间隔，即对于一个新切换为 Non-Witness 的 Region 在一段时间内不会被切换为 Witness。默认值为 1 小时。         |
| PD   | [`witness-schedule-limit`](/pd-configuration-file.md#witness-schedule-limit-从-v660-版本开始引入)    |   新增       | 控制同时进行的 Witness 调度的任务个数。默认为 4 个。         |
| TiCDC   |   新增       |  `scheduler.region-per-span`        |    **tw@Oreoxmt**      |
| DM   | 新增    |    https://github.com/pingcap/docs-cn/pull/12296       |    **tw@ran-huang**      |
| sync-diff-inspector   | `skip-non-existing-table`   |  新增 | https://github.com/pingcap/docs-cn/pull/12776/files **tw@shichun-0415**  |
|  .... |  新增  |  https://github.com/pingcap/docs-cn/pull/12819/files **tw@Oreoxmt**  |

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

        - 优化了 DM 的告警规则和内容。

        之前 DM_XXX_process_exits_with_error 类告警是遇到错误就报警，有些告警实际是由于 db conn 长时间 idle 导致，重连后即可恢复，为了降低这类 false alerm，现在细分为可自动恢复错误和不可恢复错误

        对不可自动恢复错误，维持旧的行为，立即 alert

        对可自动回复错误，只有在 2m 内发生超过 3 次时才报警
        [7376](https://github.com/pingcap/tiflow/issues/7376) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd**

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - 修复在部分场景下 TiDB/TiKV 重启导致 Lightning 重试耗费更长时间的问题。[33714](https://github.com/pingcap/tidb/issues/33714) @[lichunzhu](https://github.com/lichunzhu) **tw@shichun-0415**
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + Sync-diff-inspector

        - 新增 `skip-non-existing-table` 参数，当对比的上下游存在上游或下游表全部缺失的情况时，可配置该参数跳过对上下游表数据不一致的校验并输出到结果集与日志中，而不是任务中断退出。 @[lichunzhu](https://github.com/lichunzhu) @[liumengya94](https://github.com/liumengya9) **tw@shichun-0415**
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
