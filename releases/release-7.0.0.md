---
title: TiDB 7.0.0 Release Notes
---

# TiDB 7.0.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.0.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.0/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 7.0.0 版本中，你可以获得以下关键特性：

@yiwen92

## 功能详情

### 可扩展性

* TiFlash 引擎支持存算分离和对象存储（实验特性）[#6882](https://github.com/pingcap/tiflash/issues/6882) @[flowbehappy](https://github.com/flowbehappy) @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin) @[lidezhu](https://github.com/lidezhu) @[CalvinNeo](https://github.com/CalvinNeo) **tw:qiancai**

    在 v7.0.0 之前的版本中，TiFlash 引擎以存算一体的方式部署，即 TiFlash 节点即是存储节点，也是计算节点；同时，TiFlash 节点只能使用本地存储。存算一体的部署方式使得 TiFlash 的计算能力和存储能力无法独立扩展。在 v7.0.0 版本中，TiFlash 引擎新增存算分离架构，并在存算分离架构下，支持兼容 S3 API 的对象存储。在 TiFlash 存算分离架构下，TiFlash 节点分为计算节点和写节点。这两种节点都可以单独扩缩容，独立调整计算或数据存储能力。TiFlash 引擎的存算分离架构不能和存算一体架构混合使用、相互转换，需要在部署 TiFlash 时进行相应的配置设定，确定使用存算分离架构或者存算一体架构。

    更多信息，请参考[用户文档](/tiflash/tiflash-disaggregated-and-s3.md)。

### 性能

* 实现 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 和 PITR 的兼容 [#38045](https://github.com/pingcap/tidb/issues/38045) @[Leavrth](https://github.com/Leavrth) **tw:ran-huang**

    TiDB v6.5.0 版本支持的 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 功能和 [PITR](/br/backup-and-restore-overview.md) 未完全兼容，在 TiDB v6.5.0 版本建议通过先停止 [PITR](/br/backup-and-restore-overview.md) 后台备份任务，以 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 方式快速添加索引，然后再启动 [PITR](/br/backup-and-restore-overview.md) 备份任务实现全量数据备份。

    从 TiDB v7.0.0 版本开始，该功能和 [PITR](/br/backup-and-restore-overview.md) 已经完全兼容：通过 [PITR](../br/backup-and-restore-overview.md) 恢复集群数据时，将自动回放日志备份期间记录的通过[Fast Online DDL](/system-variables.md###tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 方式添加的索引操作，达到兼容效果。

    更多信息，请参考[用户文档](/ddl-introduction.md)。

* TiFlash 引擎支持 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子 [#6674](https://github.com/pingcap/tiflash/issues/6674) @[gengliqi](https://github.com/gengliqi) **tw:Oreoxmt**

    `IN`、`NOT IN`、`=ANY`、`!= ALL` 算子引导的关联子查询会转化为 `Semi Join` 或 `Anti Semi Join`，从而提升计算性能。当转换后的 JOIN KEY 的列可能为 NULL 时，需要具有 Null-Aware 特性的 Join 算法，即需要 [`Null-Aware Semi Join`](/explain-subqueries#null-aware-semi-joinin-和--any-子查询) 和 [`Null-Aware Anti Semi Join`](/explain-subqueries#null-aware-anti-semi-joinnot-in-和--all-子查询) 算子。

    在 v7.0.0 之前的版本中，TiFlash 引擎不支持 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子，所以这几种子查询无法直接下推至 TiFlash 引擎进行计算。在 v7.0.0 版本中，TiFlash 引擎支持了 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子。当 SQL 包含这几种关联子查询，查询的表包含 TiFlash 副本，且启用 [MPP 模式](/tiflash/use-tiflash-mpp-mode.md)时，优化器将自动判断是否将 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子下推至 TiFlash 引擎进行计算以提升整体性能。

    更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations)。

* TiFlash 引擎支持 FastScan 功能 [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan) **tw:Oreoxmt**

    TiFlash 引擎从 v6.3.0 版本发布了实验特性的快速扫描功能 (FastScan)。在 v7.0.0 版本中，该功能正式 GA。通过使用系统变量 [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-从-v630-版本开始引入) 可以启用快速扫描功能。快速扫描功能通过牺牲强一致性保证，可以大幅提升扫表性能。如果对应的表只有 INSERT 操作，没有 UPDATE/DELETE 操作，则快速扫描功能在提升扫表性能的同时，不会损失强一致性。

    更多信息，请参考[用户文档](/develop/dev-guide-use-fastscan.md)。

* TiFlash 引擎支持 Selection 延迟物化功能（实验特性） [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) **tw:qiancai**

    当 SELECT 语句中包含过滤条件（WHERE子句）时，普通的处理方式是扫描所有数据后进行过滤。Selection 延迟物化功能可以先扫描过滤条件相关列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少扫描 IO 和数据解析的计算量。在 v7.0.0 中，TiFlash 引擎支持 Selection 延迟物化功能，并通过 variable 控制是否启用该功能。当功能启用时，优化器会根据过滤条件的信息，自动判断选择哪些过滤条件下推到 TableScan 算子。

    更多信息，请参考[用户文档](/tiflash/tiflash-late-materialization.md)。

* 非 prepared 语句的执行计划可以被缓存（实验特性）[#qw4990](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990) **tw:Oreoxmt**

    执行计划缓存是提升并发 OLTP 负载能力的重要手段， TiDB 已经支持对 [prepared 语句的计划进行缓存](/sql-prepared-plan-cache.md)。 在 v7.0.0 中， 非 prepared 语句的执行计划也能够被缓存，使得执行计划缓存能够被应用在更广泛场景下，进而提升 TiDB 的并发处理能力。

    这个功能目前默认关闭， 用户通过变量 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 打开。 出于稳定性考虑，在当前版本中，TiDB 开辟了一块新的区域用于缓存非 prepare 语句的执行计划，通过变量 [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) 设置缓存大小；另外，对 SQL 的模式也有一定的限制，具体参见[文档](/sql-non-prepared-plan-cache.md#限制)。

    更多信息，请参考[用户文档](/sql-non-prepared-plan-cache.md)。

* 解除执行计划缓存对子查询的限制 [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678) **tw:Oreoxmt**

    TiDB v7.0.0 移除了计划缓存对子查询的限制，带有子查询的 SQL 语句的执行计划可以被缓存，比如 " `select * from t where a > (select ...)` "。 这进一步扩大了执行计划缓存的应用范围，提升 SQL 的执行效率。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* TiKV 默认打开 `enable-log-recycle` 特性 [#14379](https://github.com/tikv/tikv/issues/14379) @[LykxSassinator](https://github.com/LykxSassinator) **tw:ran-huang**

    TiKV 在 v6.3.0 中引入了 Raft [日志回收](../tikv-configuration-file.md###enable-log-recycle-从-v630-版本开始引入) 特性, 用以减少写负载的长尾延迟。在 v7.0.0 中，该特性将默认开启。

* TiKV 新增 `prefill-for-recycle` 特性[#14371](https://github.com/tikv/tikv/issues/14371) @[LykxSassinator](https://github.com/LykxSassinator) **tw:ran-huang**

    TiKV 在 v6.3.0 中引入了 Raft [日志回收](../tikv-configuration-file.md###enable-log-recycle-从-v630-版本开始引入) 特性, 用以减少写负载的长尾延迟。但是，"日志回收"需要 Raft 日志文件数量达到一定阈值后方可介入，使得用户无法直观感受该特性带来的写负载的吞吐提升。为了提升用户感受，v7.0.0 中正式引入了 `prefill-for-recycle` 功能，用以控制 TiKV 是否在进程启动时自动生成空的日志文件用于日志回收。该配置项启用时，TiKV 将在初始化时自动填充一批空日志文件用于日志回收，保证日志回收在初始化后立即生效。

* 新增从[窗口函数](/functions-and-operators/expressions-pushed-down.md)中推导出 TopN/Limit 的优化规则，提升窗口函数的性能 [#13936](https://github.com/tikv/tikv/issues/13936) @[windtalker](https://github.com/windtalker) **tw:qiancai**

    该功能默认关闭，需要将 session 变量 `tidb_opt_derive_topn` 设置为 ON 来开启。
    
    更多信息，请参考[用户文档]()。

* 支持通过 [Fast Online DDL](../system-variables.md###tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 创建唯一索引 [#40730](https://github.com/pingcap/tidb/issues/40730) @[tangenta](https://github.com/tangenta) **tw:ran-huang**

    TiDB v6.5.0 版本支持通过 [Fast Online DDL](../system-variables.md###tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 模式创建普通的二级索引，而 v7.0.0 版本开始则支持通过 [Fast Online DDL](../system-variables.md###tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 模式创建唯一索引。相比于 TiDB v6.1.0，预期大表添加唯一索引的性能约提升为 v6.1.0 的数倍。

    更多信息，请参考[用户文档](../ddl-introduction.md)。

### 稳定性

* 支持基于资源组的资源管控 [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp) **tw:hfxsd**

    TiDB 正式发布了基于资源组的资源管控特性，该特性将会极大地提升 TiDB 集群的资源利用效率和性能表现。资源管控特性的引入对 TiDB 具有里程碑的意义，它允许用户将一个分布式数据库集群划分成多个逻辑单元，将不同的数据库用户映射到对应的资源组中，并根据需要设置每个资源组的配额。当集群资源紧张时，来自同一个资源组的会话所使用的全部资源将被限制在配额内，避免其中一个资源组过度消耗，从而影响其他资源组中的会话正常运行。

    该特性也可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载提升，不会影响其他应用的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

    我们不仅提供了内置视图展示资源的实际使用情况，协助用户更合理地配置资源，还支持基于会话和语句级别（HINT）的动态资源管控能力。这些功能的引入将帮助用户更精确地掌控 TiDB 集群的资源使用情况，并根据实际需要动态调整配额。

    启用资源管控特性需要同时打开 TiDB 的全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 及 TiKV 的配置项 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)。当前支持的限额方式基于“[用量](/tidb-resource-control.md#什么是-request-unit-ru)”（Request Unit，即 RU），RU 是 TiDB 对 CPU、I/O 等系统资源的统一抽象单位。

    用户可以通过以下方式生效资源组：

    - 用户级别。通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句将用户绑定到特定的资源组。将资源组绑定用户后，使用对应的用户创建的会话会自动绑定对应的资源组。
    - 会话级别。通过 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 设置当前会话的资源组。
    - 语句级别。通过 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 设置当前语句使用的资源组。

  更多信息，请参考[用户文档](/tidb-resource-control.md)。

* 支持 [Fast Online DDL](../system-variables.md###tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 的检查点机制，提升容错性和自动恢复能力 [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta) **tw:ran-huang**

    TiDB v7.0.0 版本引入 [Fast Online DDL](../system-variables.md###tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 的检查点机制，可以大幅提升 [Fast Online DDL](../system-variables.md###tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 的容错性和自动恢复能力。即使在 TiDB DDL Owner 故障重启或切换时，通过周期性记录并同步 DDL 进度，正在执行中的 DDL 仍能以 [Fast Online DDL](../system-variables.md###tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 方式继续执行，从而让 DDL 执行更加稳定高效。

    更多信息，请参考[用户文档](../ddl-introduction.md)。

* TiFlash 引擎支持 Spill-to-disk 功能 [#6528](https://github.com/pingcap/tiflash/issues/6528) @[windtalker](https://github.com/windtalker) **tw:ran-huang**

    为了执行性能，TiFlash 引擎尽量将数据全部放在内存中运行。当数据量太大，超过内存总大小时，TiFlash 会终止查询，避免内存潮用引发系统崩溃。因此，TiFlash 可处理的数据量受限于内存大小。从 v7.0.0 版本开始，TiFlash 引擎支持 Spill-to-disk 功能，通过调整算子内存使用阈值 `tidb_max_bytes_before_tiflash_external_group_by`、`tidb_max_bytes_before_tiflash_external_sort`、`tidb_max_bytes_before_tiflash_external_join`，控制对应算子的最大内存使用量。当算子使用内存超过一定阈值时，会自动将数据落盘，牺牲一定的性能，从而处理更多数据。

    更多信息，请参考[用户文档](/tiflash/tiflash-spill-disk.md)。

* 提升统计信息的收集效率 [#41930](https://github.com/pingcap/tidb/issues/41930) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw:ran-huang**

    在 v7.0.0， TiDB 统计信息收集的逻辑被进一步优化，收集时间大概降低了 25% 左右。 提升了中大型数据库集群的运行效率和稳定性，减少了统计信息收集对集群性能的影响。

* 新增优化器 Hint 对 MPP 进行干预 [#39710](https://github.com/pingcap/tidb/issues/39710) @[Reminiscent](https://github.com/Reminiscent) **tw:ran-huang**

    TiDB 在 v7.0.0 中增加了一系列优化器 Hint，来影响 MPP 操作执行计划的生成。

    - [`SHUFFLE_JOIN()`](/optimizer-hints.md#shuffle_joint1_name-tl_name): 针对 MPP 生效。 提示优化器对指定表使用 Shuffle Join 算法。
    - [`BROADCAST_JOIN()`](/optimizer-hints.md#broadcast_joint1_name-tl_name): 针对 MPP 生效。提示优化器对指定表使用 Broadcast Join 算法。
    - [`MPP_1PHASE_AGG()`](/optimizer-hints.md#mpp_1phase_agg): 针对 MPP 生效。提示优化器对指定查询块中所有聚合函数使用一阶段聚合算法。
    - [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg): 针对 MPP 生效。 提示优化器对指定查询块中所有聚合函数使用二阶段聚合算法。

  MPP 优化器 Hint 能够协助客户对 HTAP 查询进行干预，提升 HTAP 负载下的性能和稳定性。

  更多信息，请参考[用户文档](/optimizer-hints.md)。

* 优化器 Hint 兼容连接方式与连接顺序的指定 [#36600](https://github.com/pingcap/tidb/issues/36600) @[Reminiscent](https://github.com/Reminiscent)

    在 v7.0.0 中，优化器 Hint [`LEADING()`](/optimizer-hints.md#leadingt1_name--tl_name-) 能够和影响连接方式的 Hint 配合使用，两者行为兼容。 这样在多表连接的情况下，可以有效指定最佳的连接方式和连接顺序，提升优化器 Hint 对执行计划的控制能力。

    新的 Hint 行为会有微小的变化。 为确保向前兼容，TiDB 引入了变量 [`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-从-v700-版本开始引入)， 当此变量为 `OFF` 时，行为向前兼容。 从旧版本升级到 v7.0.0 及之后版本的集群，该变量会被设置成 `OFF`。为了获取更灵活的 Hint 行为，强烈建议在确保无性能回退的情况下，将该变量切换为 `ON`。

    更多信息，请参考[用户文档](/optimizer-hints.md)。

### 高可用

* TiDB 支持 prefer-leader 选项，在网络不稳定的情况下提供更高的读可用性，降低响应延迟 [#40905](https://github.com/pingcap/tidb/issues/40905) @[LykxSassinator](https://github.com/LykxSassinator) **tw:ran-huang**

    TiDB 支持通过 `tidb_replica_read` 参数控制 TiDB 的数据读取行为，新增支持 `prefer-leader` 选项。当设置为 `prefer-leader` 时，TiDB 会优先选择 leader 副本执行读取操作。当 leader 副本的处理速度明显变慢时，例如由于磁盘或网络性能抖动，TiDB 将选择其他可用的 follower 副本来执行读取操作，从而提供更高的可用性，降低响应延迟。

    更多信息，请参考[用户文档](/develop/dev-guide-use-follower-read.md)

### SQL 功能

* Time to live (TTL) 已基本可用 [#39262](https://github.com/pingcap/tidb/issues/39262) @[lcwangchao](https://github.com/lcwangchao) @[YangKeao](https://github.com/YangKeao) **tw:ran-huang**

    TTL 提供了行级别的生命周期控制策略。在 TiDB 中，设置了 TTL 属性的表会根据配置自动检查并删除过期的行数据。TTL 设计的目标是在不影响在线读写负载的前提下，帮助用户周期性且及时地清理不需要的数据。

    更多信息，请参考[用户文档](/time-to-live.md)。

* 支持 `ALTER TABLE…REORGANIZE PARTITION` [#15000](https://github.com/pingcap/tidb/issues/15000) @[mjonss](https://github.com/mjonss) **tw:qiancai**

    TiDB 支持 `ALTER TABLE…REORGANIZE PARTITION` 语法。通过该语法，你可以对表的部分或所有分区进行重新组织，包括合并、拆分、或者其他修改，并且不丢失数据。

    更多信息，请参考[用户文档](/partitioned-table.md#重组分区)。

* 支持 Key Partitioning [#41364](https://github.com/pingcap/tidb/issues/41364) @[TonsnakeLin](https://github.com/TonsnakeLin) **tw:qiancai**

    TiDB 支持 Key 分区。Key 分区与 Hash 分区都可以保证将数据均匀地分散到一定数量的分区里面，区别是 Hash 分区只能根据一个指定的整数表达式或字段进行分区，而 Key 分区可以根据字段列表进行分区，且 Key 分区的分区字段不局限于整数类型。

    更多信息，请参考[用户文档](/partitioned-table.md#key-分区)

### 数据库管理

* TiCDC 支持 storage sink，可输出变更数据至 cloud storage (GA) [#6797](https://github.com/pingcap/tiflow/issues/6797) @[zhaoxinyu](https://github.com/zhaoxinyu) **tw:hfxsd**

    TiCDC 支持将 changed log 输出到兼容 Amazon S3 协议的存储服务、GCS、Azure Blob Storage以及 NFS 中。Cloud storage 价格便宜，使用方便。对于不使用 Kafka 的用户，可以选择使用 storage sink。使用该功能，TiCDC 会将 changed log 保存到文件，发送到存储系统中。用户自研的消费程序可以定时从存储系统读取新产生的 changed log 进行数据处理。

    Storage sink 支持格式为 canal-json 和 csv 的 changed log。更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/stable/ticdc-sink-to-cloud-storage)。

* TiCDC Open API V2 GA @[sdojjy](https://github.com/sdojjy) **tw:hfxsd**

    TiCDC 提供 OpenAPI 功能，用户可以通过 OpenAPI v2 对 TiCDC 集群进行查询和运维操作。OpenAPI 的功能是 [`cdc cli` 工具](/ticdc/ticdc-manage-changefeed.md)的一个子集。用户可以通过 OpenAPI 完成 TiCDC 集群的如下运维操作：

    - [获取 TiCDC 节点状态信息](#获取-ticdc-节点状态信息)
    - [检查 TiCDC 集群的健康状态](#检查-ticdc-集群的健康状态)
    - [创建同步任务](#创建同步任务)
    - [删除同步任务](#删除同步任务)
    - [更新同步任务配置](#更新同步任务配置)
    - [查询同步任务列表](#查询同步任务列表)
    - [查询特定同步任务](#查询特定同步任务)
    - [暂停同步任务](#暂停同步任务)
    - [恢复同步任务](#恢复同步任务)
    - [查询同步子任务列表](#查询同步子任务列表)
    - [查询特定同步子任务](#查询特定同步子任务)
    - [查询 TiCDC 服务进程列表](#查询-ticdc-服务进程列表)
    - [驱逐 owner 节点](#驱逐-owner-节点)
    - [动态调整 TiCDC Server 日志级别](#动态调整-ticdc-server-日志级别)

  更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/13224)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* Load data 语句集成 Lightning ，用户可以使用 Load data 命令完成原先需要单独使用 Lightning 才能完成的数据导入任务。    [#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716) **tw:hfxsd**

    在集成 Lightning 之前，Load data 语句只能用于导入位于客户端的数据文件，如果用户要从云存储导入数据，就得借助 Lightning 来实现。但是单独部署 Lightning 又会带来额外的部署成本和管理成本。将 Lightning 逻辑导入能力（TiDB backend ）集成到 Load data 命令后，不仅可以省去 Lightning 的部署和管理成本。还可以借助 Lightning 的功能大大扩展 load data 语句的能力。 部分增强的功能举例说明如下：

    - 支持从 S3 导入数据到 TiDB，且支持通配符一次性匹配多个源文件导入到 TiDB 。
    - 支持 CSV、TSV、Parquet、SQL(mydumper/dumpling) 格式的源文件。
    - 支持 precheck ，可在导入之前将所有不满足导入数据的问题检测出来，用户根据检测结果优化后，再次提交任务。提升任务配置体验。
    - 支持将任务设置为 Detached，让任务在后台执行。
    - 支持任务管理，可通过 show load data jobid 查询任务状态和进展详情。方便用户管理和维护。

  更多信息，请参考[用户文档](/sql-statements/sql-statement-load-data.md)。

* TiDB Lightning 向 TiKV 传输键值对时支持启用压缩传输 [#41163](https://github.com/pingcap/tidb/issues/41163) @[gozssky](https://github.com/gozssky) **tw:qiancai**

    自 v6.6.0 起，TiDB Lightning 支持将本地编码排序后的键值对在网络传输时进行压缩再发送到 TiKV，从而减少网络传输的数据量，降低网络带宽开销。之前版本不支持该功能，在数据量较大的情况下，TiDB Lightning 对网络带宽要求相对较高，且会产生较高的流量费。

    该功能默认关闭，你可以通过将 TiDB Lightning 配置项 compress-kv-pairs 设置为 "gzip" 或者 "gz" 开启此功能。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v6.6/tidb-lightning-configuration#tidb-lightning-%E4%BB%BB%E5%8A%A1%E9%85%8D%E7%BD%AE)。

## 兼容性变更

> **注意：**
>
> 以下为从 v6.6.0 升级至当前版本 (v7.0.0) 所需兼容性变更信息。如果从 v6.5.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### MySQL 兼容性

* TiDB 支持移除自增列必须是索引的约束 [#40580](https://github.com/pingcap/tidb/issues/40580) @[tiancaiamao](https://github.com/tiancaiamao) **tw:ran-huang**

    TiDB v7.0.0 开始支持移除自增列必须是索引或索引前缀的限制。这意味着用户现在可以更灵活地定义表的主键，并方便地使用自增列实现排序分页，同时避免自增列带来的写入热点问题，并通过使用 Cluster Indexed Table 提高查询性能。之前，TiDB 的行为与 MySQL 一致，要求自增列必须是索引或索引前缀。现在，通过此次更新，您可以使用以下语法创建表并成功移除自增列约束：

    ```sql
    create table test1 (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `k` int(11) NOT NULL DEFAULT '0',
        `c` char(120) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
        PRIMARY KEY(`k`, `id`)
    );
    ```

    此功能不影响 TiCDC 同步数据。

    更多信息，请参考[用户文档]()。

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
|[`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-从-v700-版本开始引入) |  新增  | 这个变量用来控制用于控制连接算法的 Join Method Hint 是否会影响 Join Reorder 的优化过程。 默认值为 `ON`，即采用新的兼容控制模式；`OFF` 则与 v7.0.0 以前的行为保持一致。为了向前兼容，从旧版本升级到 v7.0.0 及之后版本的集群，该变量会被设置成 `OFF`。|
|[`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-从-v700-版本开始引入) | 新增 | 是否对悲观锁启用加强的悲观锁唤醒模型，以降低单行冲突场景下事务的尾延迟。默认值为 `ON`，从旧版本升级到 v7.0.0 或之后版本，该变量会被设置成 `OFF` |
|[`tidb_pessimistic_txn_aggressive_locking`] | 删除 | 更名为 [`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-从-v700-版本开始引入) |
|[`tidb_opt_enable_late_materialization`]  |  新增  |   这个变量用来控制用于控制 TiFlash 延迟物化功能是否开启。 默认值为 `OFF`，即不开启 TiFlash 延迟物化功能。 |
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiFlash | [flash.disaggregated_mode](https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3) |  新增  |在 TiFlash 的存算分离架构中，表示此 TiFlash 节点是 Write Node 还是 Compute Node。有效值是 tiflash_write 或者 tiflash_compute|
| TiFlash | [storage.s3.endpoint](https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3) |  新增  | S3 的 endpoint 地址 |
| TiFlash | [storage.s3.bucket](https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3) |  新增  | TiFlash 的所有数据存储在这个 bucket 中 |
| TiFlash | [storage.s3.root](https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3) |  新增  | S3 bucket 中存储数据的根目录 |
| TiFlash | [storage.s3.access_key_id](https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3) |  新增  | 访问 S3 的 ACCESS_KEY_ID |
| TiFlash | [storage.s3.secret_access_key](https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3) |  新增  | 访问 S3 的 SECRET_ACCESS_KEY |
| TiFlash | [storage.remote.cache.dir](https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3) |  新增  | TiFlash Compute Node 的本地数据缓存目录 |
| TiFlash | [storage.remote.cache.capacity](https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3) |  新增  | TiFlash Compute Node 的本地数据缓存目录的大小 |
|          |          |          |          |
|          |          |          |          |

### 其他

## 废弃功能

## 改进提升

+ TiDB

    - 加强的悲观锁唤醒模型的开关变量由 `tidb_pessimistic_txn_aggressive_locking` 更名为 `tidb_pessimistic_txn_fair_locking`，并在新集群中默认启用 [#42147](https://github.com/pingcap/tidb/issues/42147) @[MyonKeminta](https://github.com/MyonKeminta)
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

        - TiCDC 在 v7.0.0 版本支持在 Kafka 为下游的场景中将单个大表的数据改变分布到多个 TiCDC 节点，从而解决用户在大规模 TiDB 集群的数据集成场景下的单表扩展性问题。

            用户可以通过设置 TiCDC 配置 `enable_table_across_nodes` 为 `true` 来启用这个功能，并通过设置`region_threshold` 来指定当一张表的 region 个数超过阀值时 TiCDC 开始将对应的表上的数据改变分布到多个 TiCDC 节点。

        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - 优化 Data Migration（DM）检查下游数据库账号权限的前置检查项 [#issue](链接-待补充) @[maxshuang](https://github.com/maxshuang)

            在之前的版本，Data Migration 进行前置检查，检查用户提供的下游数据库账号是具备所需的权限时，是非必须通过项，现改为必须通过项，避免该账号权限不足导致任务失败。

        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - Lightning local backend 支持导入数据和索引分离导入，提升导入速度和稳定性 [#42132](https://github.com/pingcap/tidb/issues/42132) @[gozssky](https://github.com/gozssky)

            Lightning 增加 add-index-by-sql 参数。默认取值为 true，表示在物理导入模式（ local backend）下，会在导入数据完成后，通过 add index 的 SQL 语句帮用户建索引，提升导入数据的速度和稳定性。取值为 false，和历史版本保存一致，表示仍然会用 Lightning  将行数据以及索引数据编码成 kv pairs 后再一同导入到 TiKV。

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
