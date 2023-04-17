---
title: TiDB 7.1.0 Release Notes
summary: 了解 TiDB 7.1.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.1.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/dev/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 7.1.0 版本中，你可以获得以下关键特性：

## 功能详情

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可扩展性

* TiFlash 支持存算分离和对象存储 (GA) [#6882](https://github.com/pingcap/tiflash/issues/6882) @[flowbehappy](https://github.com/flowbehappy) @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin) @[lidezhu](https://github.com/lidezhu) @[CalvinNeo](https://github.com/CalvinNeo) **tw:qiancai**

    在 v7.0.0 版本中，TiFlash 在已有的存算一体架构之外，新增存算分离架构。在此架构下，TiFlash 节点分为 Compute Node（计算节点）和 Write Node（写入节点）两种类型，并支持兼容 S3 API 的对象存储。这两种节点都可以单独扩缩容，独立调整计算或数据存储能力。

    从 v7.1.0 版本开始，TiFlash 存算分离架构正式 GA。TiFlash 的存算分离架构和存算一体架构不能混合使用、相互转换，需要在部署 TiFlash 时进行相应的配置指定使用其中的一种架构。

    更多信息，请参考[用户文档](/tiflash/tiflash-disaggregated-and-s3.md)。

### 性能

* 下一代 [`Partitioned Raft KV`](/partitioned-raft-kv.md) 存储引擎 GA [#issue号](链接) @[busyjay](https://github.com/busyjay) @[tonyxuqqi](https://github.com/tonyxuqqi) @[tabokie](https://github.com/tabokie) @[bufferflies](https://github.com/bufferflies) @[5kbpers](https://github.com/5kbpers) @[SpadeA-Tang](https://github.com/SpadeA-Tang) @[nolouch](https://github.com/nolouch) **tw:Oreoxmt**

    TiDB v6.6.0 引入的全新的 TiKV 存储引擎 [`Partitioned Raft KV`](/partitioned-raft-kv.md) 在 TiDB v7.1.0 版本正式 GA。该引擎使用多个 RocksDB 实例存储 TiKV 的 Region 数据，为每个 Region 提供独立的 RocksDB 实例。此外，该引擎能够更好地管理 RocksDB 实例的文件数和层级，实现 Region 间的数据操作物理隔离，并支持更多数据的平滑扩展。与原 TiKV 存储引擎相比，使用该引擎在相同硬件条件和读写混合场景下，可实现约 2 倍的写入吞吐、3 倍的读取吞吐，并缩短约 4/5 的弹性伸缩时间。该引擎与 TiFlash 引擎兼容，支持 Lightning / BR / TiCDC 等周边工具。该引擎目前仅支持在新集群中使用，暂不支持从原 TiKV 存储引擎直接升级到该引擎。

    更多信息，请参考[用户文档](/partitioned-raft-kv.md)。

* TiFlash 查询支持延迟物化功能 (GA) [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) **tw:qiancai**

    在 v7.0.0 中，TiFlash 引入了延迟物化实验特性，用于优化查询性能。该特性默认关闭（系统变量 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) 默认为 `OFF`）。当 `SELECT` 语句中包含过滤条件（`WHERE` 子句）时，TiFlash 默认会先读取该查询所需列的全部数据，然后再根据查询条件对数据进行过滤、聚合等计算任务。开启该特性后，TiFlash 支持下推部分过滤条件到 TableScan 算子，即先扫描过滤条件相关的列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少 IO 扫描和数据处理的计算量。

    从 v7.1.0 开始，TiFlash 延迟物化功能正式 GA，默认开启（系统变量 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) 默认为 `ON`），TiDB 优化器会根据统计信息和查询的过滤条件，决定哪些过滤条件会被下推到 TableScan 算子。

    更多信息，请参考[用户文档](/tiflash/tiflash-late-materialization.md)。

* TiFlash 支持根据网络交换数据量自动选择 MPP 模式的 Join 算法 [#7084](https://github.com/pingcap/tiflash/issues/7084) @[solotzg](https://github.com/solotzg) **tw:qiancai**

    TiFlash MPP 模式有多种 Join 算法。在 v7.1.0 之前的版本中，TiDB 根据变量 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 以及实际数据量决定 TiFlash MPP 模式是否使用 Broadcast Hash Join 算法。

    在 v7.1.0 中，TiDB 引入变量 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-从-v710-版本开始引入)，控制是否基于最小网络数据交换策略选择 MPP Join 算法。该变量默认关闭，表示默认保持 v7.1.0 之前的算法选择策略。如需开启，请设置该变量为 `ON`。开启后，你无需再手动调整 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 的阈值（此时这两个变量将不再生效），TiDB 会自动估算不同 Join 算法所需进行网络交换的数据量，然后选择综合开销较小的算法，从而减少网络流量，提升 MPP 查询性能。

    更多信息，请参考[用户文档](/tiflash/use-tiflash-mpp-mode.md#mpp-模式的算法支持)。

* 自适应副本读来缓解读热点 [#14151](https://github.com/tikv/tikv/issues/14151) @[sticnarf](https://github.com/sticnarf) @[you06](https://github.com/you06) **tw:Oreoxmt**

    发生读热点场景，其他 TiKV 节点可能仍存在闲置资源，与其在数据主节点持续排队等待，转而从其他节点读取副本可能带来更低的延迟。TiDB 在新版本开始支持负载自适应副本读，通过 [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-从-v700-版本开始引入) 参数来设置排队时间的临界值，当估算的排队时间超过设定时，TiDB 会尝试从副本节点读取数据。在读热点的情况下，相比于不打散有 70%-200% 的读取吞吐量提升。

    更多信息，请参考[用户文档](/troubleshoot-hot-spot-issues.md#打散读热点)。

* 非 Prepare 语句的执行计划缓存 GA [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990) **tw:Oreoxmt**

    TiDB 在 v7.0.0 支持缓存非 Prepare 语句的执行计划，以提升在线交易场景的并发能力。v7.1.0 持续优化了这个能力，支持更多模式的 SQL 进入缓存，并正式将这个能力 GA。

    GA 之后，非 Prepare 与 Prepare SQL 的缓存池合并，以提升内存利用率，缓存大小通过变量 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size) 设置。原有的变量 [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size) 和 [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) 将被废弃。

    为了保持设置向前兼容，对于从低版本升级到 v7.1.0 的客户，缓存池大小 `tidb_session_plan_cache_size` 将会继承 `tidb_prepared_plan_cache_size`的设置，非 Parepare 语句的缓存保持关闭。经过性能测试后，用户可通过 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 打开。对于新部署的客户，非 Parepare 语句的缓存则默认打开。

    更多信息，请参考[用户文档](/sql-non-prepared-plan-cache.md)。

### 稳定性

* 资源管控 GA [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp) **tw:hfxsd**

    TiDB 持续增强资源管控能力，并将这个特性 GA。该特性将会极大地提升 TiDB 集群的资源利用效率和性能表现。资源管控特性的引入对 TiDB 具有里程碑的意义，你可以将一个分布式数据库集群划分成多个逻辑单元，将不同的数据库用户映射到对应的资源组中，并根据需要设置每个资源组的配额。当集群资源紧张时，来自同一个资源组的会话所使用的全部资源将被限制在配额内，避免其中一个资源组过度消耗，从而影响其他资源组中的会话正常运行。

    该特性也可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载提升，不会影响其他应用的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

    在 v7.1.0 中，TiDB 增加了基于实际负载来估算系统容量上限的能力，为客户的容量规划提供了更准确的参考，协助客户更好地管理 TiDB 的资源分配，从而满足企业级场景的稳定性需要。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* 支持 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 的检查点机制，提升容错性和自动恢复能力 [#issue](https://github.com/pingcap/tidb/issues/issue) @[tangenta](https://github.com/tangenta) **tw:ran-huang**

    TiDB v7.1.0 版本引入 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 的检查点机制，可以大幅提升 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 的容错性和自动恢复能力。即使在 TiDB DDL Owner 切换的情况下，也能够通过周期性记录并同步 DDL 进度，让新的 TiDB DDL Owner 仍能以 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 方式执行切换前的 DDL 语句，无需手动取消和重新执行 DDL 语句，从而让 DDL 执行更加稳定高效。

    更多信息，请参考[用户文档](/ddl-introduction.md)。

* BR 备份恢复工具支持断点恢复 [#issue](https://github.com/pingcap/tidb/issues/issue) @[Leavrth](https://github.com/Leavrth) **tw:Oreoxmt**

    如果用户的 TiDB 集群规模较大，之前在进行数据库的快照恢复或日志恢复时，可能会出现一些意外情况导致恢复过程提前结束，例如硬盘空间占满、节点宕机等等。在 TiDB v7.1.0 之前的版本中，这些意外情况会导致之前恢复的进度作废，需要重新进行恢复，给用户带来大量额外成本和麻烦。

    为了解决这个问题，TiDB v7.1.0 引入了备份恢复的断点恢复功能。该功能可以在意外中断后保留上一次恢复的大部分进度，使得用户能够尽可能地继续上一次的恢复的进度，避免不必要的成本和麻烦。

    更多信息，请参考[用户文档](/br/br-checkpoint-restore.md)。

* 统计信息缓存加载策略优化 [#issue](https://github.com/pingcap/tidb/issues/issue) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw:hfxsd**

    在开启[统计信息同步加载](/statistics.md#统计信息的加载)的前提下，TiDB 大幅减少了启动时必须载入的统计信息的数量，并且在加载完成前不接受用户连接。一方面提升了启动时统计信息的加载速度，另一方面，避免了在启动初始阶段由于统计信息不全而引起的性能回退。提升了 TiDB 在复杂运行环境下的稳定性，降低了个别 TiDB 节点重启对整体服务的影响。

    更多信息，请参考[用户文档]()。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 支持通过 `INSERT INTO SELECT` 语句保存 TiFlash 查询结果 (GA) [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi) **tw:qiancai**

    从 v6.5.0 起，TiDB 支持下推 `INSERT INTO SELECT` 语句中的 `SELECT` 子句（分析查询）到 TiFlash，你可以将 TiFlash 的查询结果方便地保存到 `INSERT INTO` 指定的 TiDB 表中供后续分析使用，起到了结果缓存（即结果物化）的效果。

    在 v7.1.0 版本中，该功能正式 GA。当 TiDB 执行 `INSERT INTO SELECT` 语句中的 `SELECT` 子句时，优化器将根据 SQL Mode 及 TiFlash 副本的代价估算自行决定是否将查询下推至 TiFlash。因此，在实验特性阶段引入的系统变量 `tidb_enable_tiflash_read_for_write_stmt` 将被移除。需要注意的是，TiFlash 对于 `INSERT INTO SELECT` 语句的计算规则不满足 `STRICT SQL Mode` 要求，因此只有当前会话的 SQL Mode 是除 `STRICT_TRANS_TABLES`, `STRICT_ALL_TABLES` 之外的值时，TiDB 才允许将 `INSERT INTO SELECT` 语句中的查询下推至 TiFlash。

    更多信息，请参考[用户文档](/tiflash/tiflash-results-materialization.md)。

* MySQL 兼容的多值索引 (Multi-Valued Index) GA [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) @[YangKeao](https://github.com/YangKeao) **tw:ran-huang**

    过滤 JSON 列中某个数组的值是一个常见的操作，但普通索引起不到加速作用。在数组上创建多值索引能够大幅提升过滤的性能。如果 JSON 列中的某个数组上存在多值索引，那么函数 `MEMBER OF()`、`JSON_CONTAINS()`、`JSON_OVERLAPS()` 的检索条件可以利用多值索引过滤，从而减少大量的 I/O 消耗，提升执行速度。

    在 v7.1.0 中，TiDB 多值索引 (Multi-Valued Index) GA，支持更完整的数据类型，并与 TiDB 的工具链兼容。用户可以在生产环境利用“多值索引”加速对 JSON 数组的检索操作。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)

* 支持完善的分区管理 [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss) **tw:qiancai**

    在 v7.1.0 版本之前，TiDB 支持的分区类型包括 `RANGE`、`LIST`、`HASH`、`KEY` ，其中 `RANGE` 和 `LIST` 分区支持分区管理功能。从 v7.1.0 版本开始，TiDB 新增 `HASH` 和 `KEY` 分区的 `ADD PARTITION` 和 `COALESCE PARTITION` 管理功能，并支持修改分区表类型（包括分区表和非分表之间的相互转换、不同分区类型之间的修改），整体完善了分表表的分区管理能力。你可以根据需要，灵活地对表的分区方式进行调整。

    更多信息，请参考[用户文档](/partitioned-table.md#)。

* `LOAD DATA` SQL 支持从 S3、GCS 导入数据，支持任务管理等功能 GA [#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716) **tw:hfxsd**

    以下 `LOAD DATA` 新增的功能在 7.1 版本 GA：

    - 支持从 S3、GCS 导入数据
    - 支持导入 Parquet 文件数据
    - 支持解析源文件中 ascii、latin1、binary、gbk、utf8mbd 字符集
    - 支持设置 FIELDS DEFINED NULL BY 将源文件的指定的值转换为 Null 写入目标表。
    - 支持设置一个 bath_size 即 1 个 batch 插入到目标表的行数，提升写入性能。
    - 支持设置 detached，允许该 job 在后台运行。
    - 支持 show load data jobs, show load data jobid, drop load data jobid 来管理任务。

    更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/13344)。

* `LOAD DATA` SQL 集成 Lightning local backend（physical import mode） 的导入功能，提升导入性能（实验特性）[#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter) **tw:hfxsd**

    用户通过 `LOAD DATA` SQL 导入数据时，可以指定 import_mode = physical 来实现 Lightning local backend （physical 导入模式）的导入效果，相比 Load data 原先的 logical 导入模式，可成倍提升导入数据的性能。

    更多信息，请参考[用户文档](链接)。

* `LOAD DATA` SQL 支持并行导入，提升导入性能（实验特性）[#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716) **tw:hfxsd**

    原先 load data sql 无法并行导入数据，性能较差。在该版本中支持设置并行导入的参数，通过提升并发，来提升导入的性能。在实验室环境，相比上个版本，测试逻辑导入性能有接近 4 倍的提升。

    更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/13676)。

* 生成列 (Generated Columns) GA [#issue号](链接) @[bb7133](https://github.com/bb7133) **tw:ran-huang**

    生成列 (Generated Columns) 是 MySQL 数据库很有价值的一个功能。在创建表时定义一列的值由表中其他列的值计算而来，而不是由用户显式插入或更新，它可以是虚拟列 (Virtual Column) 或存储列(Stored Column)。TiDB 在早期版本就提供了 MySQL 兼容的生成列，在 v7.1.0 中将这个功能 GA。

    生成列提升了 TiDB 对 MySQL 的兼容性，方便用户从 MySQL 平滑迁移，同时也简化数据维护的复杂度、增强数据的一致性、提高查询效率。

    更多信息，请参考[用户文档](/generated-columns.md)。

### 数据库管理

* DDL 任务支持暂停和恢复操作 [#issue号](链接) @[godouxm](https://github.com/godouxm) **tw:ran-huang**

    TiDB v7.1.0 之前的版本中，当 DDL 任务执行期间遇到业务高峰时间点时，为了减少对业务的影响，用户只能手动取消 DDL 任务。为了减轻 DDL 操作对业务负载的影响，TiDB v7.1.0 引入了 DDL 任务的暂停和恢复操作，用户可以在高峰时间点暂停 DDL 任务，等到业务高峰时间结束后再恢复 DDL 任务，从而避免了对业务的影响。

    例如，可以通过如下 [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) 或 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) 子句暂停或者恢复多个 DDL 任务：

    ```sql
    SQL> admin pause ddl jobs 1,2;

    SQL> admin resume ddl jobs 1,2;
    ```

    更多信息，请参考 [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) 和 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)。

* 无需取消 DDL 的平滑集群升级功能 [#issue号](链接) @[zimulala](https://github.com/zimulala) @[hawkingrei](https://github.com/hawkingrei) **tw:ran-huang**

    TiDB v7.1.0 之前的版本在升级集群时需要先手动取消正在运行或排队的 DDL 任务，在升级完毕后再手动添加这些任务。为了让用户享受更加平滑的升级体验，TiDB v7.1.0 引入了自动暂停和恢复 DDL 任务的功能。从 v7.1.0 版本开始，用户可以在不需要手动取消 DDL 任务的情况下升级集群。系统会自动暂停正在执行或排队的 DDL 任务，等待整个集群完成滚动升级后再自动恢复这些任务，让用户可以更加轻松地升级 TiDB 集群。

### 可观测性

* 增加优化器诊断信息 [#issue号](链接) @[time-and-fate](https://github.com/time-and-fate) **tw:hfxsd**

    获取充足的信息是 SQL 性能诊断的关键，在 v7.1.0 中，TiDB 持续向各种诊断工具中添加优化器运行信息，可以更好地解释执行计划如何被选择，协助用户和技术支持对 SQL 性能问题进行定位。其中包括：

    * [`PLAN REPLAYER`](/sql-plan-replayer.md#使用-plan-replayer-保存和恢复集群现场信息) 的输出中增加 `debug_trace.json` 文件。
    * [`EXPLAIN`](/explain-walkthrough.md) 的输出中，为 `operator info` 添加部分统计信息详情。
    * 为[`慢日志`](/identify-slow-queries.md)的 `Stats` 字段添加部分统计信息详情。

  更多信息，请参考[使用 `PLAN REPLAYER` 保存和恢复集群线程信息](/sql-plan-replayer.md#使用-plan-replayer-保存和恢复集群现场信息)，[使用 `EXPLAIN` 解读执行计划](/explain-walkthrough.md)和[`慢日志查询`](/identify-slow-queries.md)。

### 安全

* 更换 TiFlash 系统表信息的查询接口 [#6941](https://github.com/pingcap/tiflash/issues/6941) @[flowbehappy](https://github.com/flowbehappy) **tw:qiancai**

    从 v7.1.0 起，TiFlash 在向 TiDB 提供 [`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) 和 [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md) 系统表查询服务的端口时，不再使用 HTTP 端口，而是使用 gRPC 端口，从而避免 HTTP 服务的安全风险。

### 数据迁移

* TiCDC 支持 E2E 单行数据正确性校验功能 [#issue号](链接) @[3AceShowHand](https://github.com/3AceShowHand) @[zyguan](https://github.com/zyguan) **tw:Oreoxmt**

    从 v7.1.0 版本开始，TiCDC 新增了单行数据正确性校验功能，该功能基于 Checksum 算法对单行数据的正确性进行校验。通过该功能可以校验一行数据从 TiDB 写入、经由 TiCDC 流出，再写入到 Kafka 集群的过程中是否发生了数据错误。该功能仅支持下游是 Kafka Sink 的 Changefeed，支持 Canal-JSON / Avro / Open-Protocol 等协议。

    更多信息，请参考[用户文档](/ticdc/ticdc-integrity-check.md)。

* TiCDC 优化 DDL 同步操作 [#8686](https://github.com/pingcap/tiflow/issues/8686) @[nongfushanquan](https://github.com/nongfushanquan) **tw:ran-huang**

   在 v7.1.0 版本之前，当用户在一个大表上运行需要影响所有行的 DDL 操作，例如添加 / 删除列时，TiCDC 的同步延迟会显著增加。从 v7.1.0 版本开始，TiCDC 对于这种情况进行了优化，将同步延迟降低到不到 10 秒，以减轻 DDL 操作对下游延迟的影响。

    更多信息，请参考[用户文档](链接)。

* Lightning local backend (physical import mode) 支持在导入数据之前检测冲突的记录，并支持通过 insert ignore 和 replace 解决导入过程中的冲突记录 (实验特性) [#41629](https://github.com/pingcap/tidb/issues/41629) @[gozssky](https://github.com/gozssky) **tw:hfxsd**

    在之前的版本使用 Lightning local backend (physical import mode) 导入数据时，当遇到冲突的记录时，无法通过 insert ignore 和 replace 来处理导入过程中的 pk、uk 冲突记录，需要用户自行去重。而本次版本，支持在导入数据之前，检查冲突的记录，并通过 replace 和 insert ignore 的语义来处理 pk、uk 冲突的记录。简化用户的操作，提升处理冲突的性能。

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.0.0 升级至当前版本 (v7.1.0) 所需兼容性变更信息。如果从 v6.6.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 行为变更

* 为了提高安全性，TiFlash 废弃了 HTTP 服务端口（默认 `8123`），采用 gRPC 端口作为替代 **tw:qiancai**

    如果你已经将 TiFlash 升级到 v7.1.0，那么在升级 TiDB 到 v7.1.0 的过程中，TiFlash 系统表（[`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) 和 [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md)）不可读。

* 行为变更 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
|        |                              |      |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiFlash | `http_port` | 删除 | 废弃 TiFlash HTTP 服务端口（默认 `8123`）。|
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
