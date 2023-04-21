---
title: TiDB 7.1.0 Release Notes
summary: 了解 TiDB 7.1.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.0 Release Notes

在 7.1.0 版本中，你可以获得以下关键特性：

## 功能详情

### 可扩展性

### 性能

* TiFlash 查询支持延迟物化功能 (GA) [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) **tw:qiancai**

    在 v7.0.0 中，TiFlash 引入了延迟物化实验特性，用于优化查询性能。该特性默认关闭（系统变量 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) 默认为 `OFF`）。当 `SELECT` 语句中包含过滤条件（`WHERE` 子句）时，TiFlash 默认会先读取该查询所需列的全部数据，然后再根据查询条件对数据进行过滤、聚合等计算任务。开启该特性后，TiFlash 支持下推部分过滤条件到 TableScan 算子，即先扫描过滤条件相关的列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少 IO 扫描和数据处理的计算量。

    从 v7.1.0 开始，TiFlash 延迟物化功能正式 GA，默认开启（系统变量 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) 默认为 `ON`），TiDB 优化器会根据统计信息和查询的过滤条件，决定哪些过滤条件会被下推到 TableScan 算子。

    更多信息，请参考[用户文档](/tiflash/tiflash-late-materialization.md)。

* TiFlash 支持根据网络交换数据量自动选择 MPP 模式的 Join 算法 [#7084](https://github.com/pingcap/tiflash/issues/7084) @[solotzg](https://github.com/solotzg) **tw:qiancai**

    TiFlash MPP 模式有多种 Join 算法。在 v7.1.0 之前的版本中，TiDB 根据变量 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 以及实际数据量决定 TiFlash MPP 模式是否使用 Broadcast Hash Join 算法。

    在 v7.1.0 中，TiDB 引入变量 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-从-v710-版本开始引入)，控制是否基于最小网络数据交换策略选择 MPP Join 算法。该变量默认关闭，表示默认保持 v7.1.0 之前的算法选择策略。如需开启，请设置该变量为 `ON`。开启后，你无需再手动调整 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 的阈值（此时这两个变量将不再生效），TiDB 会自动估算不同 Join 算法所需进行网络交换的数据量，然后选择综合开销较小的算法，从而减少网络流量，提升 MPP 查询性能。

    更多信息，请参考[用户文档](/tiflash/use-tiflash-mpp-mode.md#mpp-模式的算法支持)。

* 支持自适应副本读取缓解读热点 [#14151](https://github.com/tikv/tikv/issues/14151) @[sticnarf](https://github.com/sticnarf) @[you06](https://github.com/you06) **tw:Oreoxmt**

    在读热点场景中，热点 TiKV 无法及时处理读请求，导致读请求排队。但是，此时并非所有 TiKV 资源都已耗尽。为了降低延迟，TiDB v7.1.0 引入了负载自适应副本读取功能，允许从其他有可用资源的 TiKV 节点读取副本，而无需在热点 TiKV 节点排队等待。你可以通过 [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-从-v700-版本开始引入) 系统变量控制读请求的排队长度。当 leader 节点的预估排队时间超过该阈值时，TiDB 会优先从 follower 节点读取数据。在读热点的情况下，与不打散读热点相比，该功能可提高读取吞吐量 70%～200%。

    更多信息，请参考[用户文档](/troubleshoot-hot-spot-issues.md#打散读热点)。

* 支持缓存非 Prepare 语句的执行计划 (GA) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990) **tw:Oreoxmt**

    TiDB v7.0.0 引入了非 Prepare 语句的执行计划缓存作为实验特性，以提升在线交易场景的并发处理能力。该功能在 v7.1.0 正式 GA 并默认打开，支持缓存更多模式的 SQL。

    为了提升内存利用率，TiDB v7.1.0 将非 Prepare 与 Prepare 语句的缓存池合并。你可以通过系统变量 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 设置缓存大小。原有的系统变量 [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-从-v610-版本开始引入) 和 [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) 被废弃。

    为保持向前兼容，从旧版本升级到 v7.1.0 时，缓存池大小 `tidb_session_plan_cache_size` 的值与 `tidb_prepared_plan_cache_size` 保持一致，[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 保持升级前的设置。经过性能测试后，你可通过 `tidb_enable_non_prepared_plan_cache` 开启非 Parepare 语句的执行计划缓存功能。对于新创建的 v7.1.0 集群，非 Parepare 语句的缓存功能默认打开。

    更多信息，请参考[用户文档](/sql-non-prepared-plan-cache.md)。

### 稳定性

* 资源管控 GA [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp) **tw:hfxsd**

    TiDB 持续增强资源管控能力，并将这个特性 GA。该特性将会极大地提升 TiDB 集群的资源利用效率和性能表现。资源管控特性的引入对 TiDB 具有里程碑的意义，你可以将一个分布式数据库集群划分成多个逻辑单元，将不同的数据库用户映射到对应的资源组中，并根据需要设置每个资源组的配额。当集群资源紧张时，来自同一个资源组的会话所使用的全部资源将被限制在配额内，避免其中一个资源组过度消耗，从而影响其他资源组中的会话正常运行。

    该特性也可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载提升，不会影响其他应用的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

    在 TiDB v7.1.0 中，该特性增加了基于实际负载和硬件部署来估算系统容量上限的能力，为你进行容量规划提供了更准确的参考，协助你更好地管理 TiDB 的资源分配，从而满足企业级场景的稳定性需要。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* 支持 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 的检查点机制，提升容错性和自动恢复能力 [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta) **tw:ran-huang**

    TiDB v7.1.0 引入 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 的检查点机制，可以大幅提升 Fast Online DDL 的容错性和自动恢复能力。即使在 DDL Owner 切换的情况下，TiDB 也能够通过周期性记录并同步 DDL 进度，让新的 DDL Owner 仍能以 Fast Online DDL 的方式执行切换前的 DDL 语句，无需手动取消和重新执行 DDL 语句，从而让 DDL 执行更加稳定高效。

    更多信息，请参考[用户文档](/ddl-introduction.md)。

* BR 备份恢复工具支持断点恢复 [#42339](https://github.com/pingcap/tidb/issues/42339) @[Leavrth](https://github.com/Leavrth) **tw:Oreoxmt**

    快照恢复或日志恢复会因为一些可恢复性错误导致提前结束，例如硬盘空间占满、节点宕机等突发情况。在 TiDB v7.1.0 之前，即使错误被及时处理，之前恢复的进度也会作废，你需要重新进行恢复。对大规模集群来说，会造成大量额外成本。
    
    为了尽可能继续上一次的恢复，从 TiDB v7.1.0 起，备份恢复特性引入了断点恢复的功能。该功能可以在意外中断后保留上一次恢复的大部分进度。

    更多信息，请参考[用户文档](/br/br-checkpoint-restore.md)。

* 统计信息缓存加载策略优化 [#42160](https://github.com/pingcap/tidb/issues/42160) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw:hfxsd**

    开启[统计信息同步加载](/statistics.md#统计信息的加载)后，TiDB 可以大幅减少启动时必须载入的统计信息的数量，并且在加载完成前不接受用户连接。一方面提升了启动时统计信息的加载速度，另一方面也避免了在启动初始阶段由于统计信息不全而引起的性能回退。该特性提升了 TiDB 在复杂运行环境下的稳定性，降低了个别 TiDB 节点重启对整体服务的影响。

    更多信息，请参考[用户文档](/statistics.md#统计信息的加载)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 支持通过 `INSERT INTO SELECT` 语句保存 TiFlash 查询结果 (GA) [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi) **tw:qiancai**

    从 v6.5.0 起，TiDB 支持下推 `INSERT INTO SELECT` 语句中的 `SELECT` 子句（分析查询）到 TiFlash，你可以将 TiFlash 的查询结果方便地保存到 `INSERT INTO` 指定的 TiDB 表中供后续分析使用，起到了结果缓存（即结果物化）的效果。

    在 v7.1.0 版本中，该功能正式 GA。当 TiDB 执行 `INSERT INTO SELECT` 语句中的 `SELECT` 子句时，优化器将根据 [SQL 模式](/sql-mode.md) 及 TiFlash 副本的代价估算自行决定是否将查询下推至 TiFlash。因此，在实验特性阶段引入的系统变量 `tidb_enable_tiflash_read_for_write_stmt` 将被废弃。需要注意的是，TiFlash 对于 `INSERT INTO SELECT` 语句的计算规则不满足 `STRICT SQL Mode` 要求，因此只有当前会话的 [SQL 模式](/sql-mode.md)为非严格模式（即 `sql_mode` 值不包含 `STRICT_TRANS_TABLES` 和 `STRICT_ALL_TABLES`），TiDB 才允许将 `INSERT INTO SELECT` 语句中的 `SELECT` 子句下推至 TiFlash。

    更多信息，请参考[用户文档](/tiflash/tiflash-results-materialization.md)。

* MySQL 兼容的多值索引 (Multi-Valued Index) 成为正式功能 (GA) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) @[YangKeao](https://github.com/YangKeao) **tw:ran-huang**

    过滤 JSON 列中某个数组的值是一种常见操作，但使用普通索引无法加速此过程。在数组上创建多值索引可以大幅提升过滤性能。如果 JSON 列中的某个数组上存在多值索引，则函数 `MEMBER OF()`、`JSON_CONTAINS()` 和 `JSON_OVERLAPS()` 的检索条件可以利用该多值索引进行过滤，从而减少大量的 I/O 消耗，提升执行速度。

    在 v7.1.0 中，TiDB 多值索引成为正式功能 (GA)，支持更完整的数据类型，并与 TiDB 的工具链兼容。你可以在生产环境利用多值索引来加速对 JSON 数组的检索操作。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)

* 完善 Hash 分区表和 Key 分区表的分区管理功能 [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss) **tw:qiancai**

    在 v7.1.0 之前，TiDB 中的 Hash 分区表和 Key 分区表只支持 `TRUNCATE PARTITION` 分区管理。从 v7.1.0 开始，Hash 分区表和 Key 分区表新增支持 `ADD PARTITION` 和 `COALESCE PARTITION` 分区管理。你可以根据需要灵活调整 Hash 分区表和 Key 分区表的分区数量。例如，通过 `ADD PARTITION` 语句增加分区数量，或通过 `COALESCE PARTITION` 语句减少分区数量。

    更多信息，请参考[用户文档](/partitioned-table.md#)。

* Range INTERVAL 分区定义语法成为正式功能 (GA) [#35683](https://github.com/pingcap/tidb/issues/35683) @[mjonss](https://github.com/mjonss) **tw:qiancai**

    在 v6.3.0 中引入的 Range INTERVAL 的分区定义语法成为正式功能 (GA)。通过该语法，你可以根据规则定义 Range 分区，不需要枚举所有分区，可大幅度缩短 Range 分区表的定义语句长度。语义与原有 Range 分区等价。

    更多信息，请参考[用户文档](/partitioned-table.md#range-interval-分区)。

* `LOAD DATA` SQL 支持从 S3、GCS 导入数据，支持任务管理等功能 GA [#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716) **tw:hfxsd**

    以下 `LOAD DATA` 新增的功能在 TiDB v7.1.0 GA：

    - 支持从 S3、GCS 导入数据。
    - 支持导入 Parquet 文件数据。
    - 支持解析源文件中的下列字符集：`ascii`、`latin1`、`binary`、`gbk`、`utf8mbd` 字符集
    - 支持设置 `FIELDS DEFINED NULL BY` 将源文件的指定的值转换为 `NULL` 写入目标表。
    - 支持设置 1 个 `bath_size` 即 1 个 batch 插入到目标表的行数，提升写入性能。
    - 支持设置 `detached`，允许该 job 在后台运行。
    - 支持使用 `SHOW LOAD DATA` 和 `DROP LOAD DATA` 来管理任务。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-load-data.md)。

* `LOAD DATA` SQL 集成 TiDB Lightning Physical Import Mode） 的导入功能，提升导入性能（实验特性）[#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter) **tw:hfxsd**

    `LOAD DATA` 集成 TiDB Lightning 的物理导入模式 (Physical Import Mode)，你可以通过设置 `WITH import_mode = 'PHYSICAL'` 开启。相比逻辑导入模式 (Logical Import Mode)，可成倍提升导入数据的性能。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-load-data.md)。

* `LOAD DATA` 支持并发导入，提升导入性能（实验特性）[#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716) **tw:hfxsd**

    之前 `LOAD DATA` 不支持并发导入数据，性能较差。在 TiDB v7.1.0 开始支持设置并发导入的参数 `WITH thread=<number>`，通过提升并发可以提升导入的性能。在实验室环境，相比上个版本，测试逻辑导入性能有接近 4 倍的提升。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-load-data.md)。

* 生成列 (Generated Columns) 成为正式功能 (GA) @[bb7133](https://github.com/bb7133) **tw:ran-huang**

    生成列是数据库中非常有价值的一个功能。在创建表时，可以定义一列的值由表中其他列的值计算而来，而不是由用户显式插入或更新。这个生成列可以是虚拟列 (Virtual Column) 或存储列 (Stored Column)。TiDB 在早期版本就提供了与 MySQL 兼容的生成列功能，在 v7.1.0 中这个功能正式 GA。

    使用生成列可以提升 TiDB 对 MySQL 的兼容性，方便从 MySQL 平滑迁移到 TiDB，同时也能简化数据维护复杂度，增强数据一致性并提高查询效率。

    更多信息，请参考[用户文档](/generated-columns.md)。

### 数据库管理

* DDL 任务支持暂停和恢复操作（实验特性）[#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm) **tw:ran-huang**

    TiDB v7.1.0 之前的版本中，当 DDL 任务执行期间遇到业务高峰时间点时，为了减少对业务的影响，只能手动取消 DDL 任务。TiDB v7.1.0 引入了 DDL 任务的暂停和恢复功能，你可以在高峰时间点暂停 DDL 任务，等到业务高峰时间结束后再恢复 DDL 任务，从而避免了 DDL 操作对业务负载的影响。

    例如，可以通过如下 [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) 或 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) 语句暂停或者恢复多个 DDL 任务：

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;

    ADMIN RESUME DDL JOBS 1,2;
    ```

    更多信息，请参考 [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) 和 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)。

### 可观测性

* 增加优化器诊断信息 [#43122](https://github.com/pingcap/tidb/issues/43122) @[time-and-fate](https://github.com/time-and-fate) **tw:hfxsd**

    获取充足的信息是 SQL 性能诊断的关键。在 v7.1.0 中，TiDB 持续向各种诊断工具中添加优化器运行信息，可以更好地解释执行计划如何被选择，协助对 SQL 性能问题进行定位。这些信息包括：

    * [`PLAN REPLAYER`](/sql-plan-replayer.md#使用-plan-replayer-保存和恢复集群现场信息) 的输出中增加 `debug_trace.json` 文件。
    * [`EXPLAIN`](/explain-walkthrough.md) 的输出中，为 `operator info` 添加部分统计信息详情。
    * 为[`慢日志`](/identify-slow-queries.md)的 `Stats` 字段添加部分统计信息详情。

  更多信息，请参考[使用 `PLAN REPLAYER` 保存和恢复集群线程信息](/sql-plan-replayer.md#使用-plan-replayer-保存和恢复集群现场信息)，[使用 `EXPLAIN` 解读执行计划](/explain-walkthrough.md)和[`慢日志查询`](/identify-slow-queries.md)。

### 安全

* 更换 TiFlash 系统表信息的查询接口 [#6941](https://github.com/pingcap/tiflash/issues/6941) @[flowbehappy](https://github.com/flowbehappy) **tw:qiancai**

    从 v7.1.0 起，TiFlash 在向 TiDB 提供 [`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) 和 [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md) 系统表的查询服务时，不再使用 HTTP 端口，而是使用 gRPC 端口，从而避免 HTTP 服务的安全风险。

### 数据迁移

* TiCDC 优化 DDL 同步操作 [#8686](https://github.com/pingcap/tiflow/issues/8686) @[nongfushanquan](https://github.com/nongfushanquan) **tw:ran-huang**

    在 v7.1.0 之前，当用户在一个大表上进行 DDL 操作时，如果 DDL 操作影响该表中的所有行（例如添加或删除列），TiCDC 的同步延迟会显著增加。从 v7.1.0 开始，TiCDC 对此进行了优化，将同步延迟降低到 10 秒以内，以减轻 DDL 操作对下游延迟的影响。

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

    如果你已经将 TiFlash 升级到 v7.1.0，那么在升级 TiDB 到 v7.1.0 的过程中，TiDB 无法读取 TiFlash 系统表（[`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) 和 [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md)）。

* [`SHOW LOAD DATA`](/sql-statements/sql-statement-show-load-data.md) 的返回值中废弃了参数 `Loaded_File_Size`，替换为参数 `Imported_Rows` **tw:hfxsd**

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| `tidb_ddl_distribute_reorg` | 删除 | 重命名为 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入)。 |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-从-v630-版本开始引入) | 废弃 | 默认值从 `OFF` 修改为 `ON`，当 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-从-v50-版本开始引入) 时，优化器将根据 [SQL 模式](/sql-mode.md) 及 TiFlash 副本的代价估算自行决定是否将查询下推至 TiFlash。 |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) | 修改 | 默认值从 `OFF` 修改为 `ON`，代表 [TiFlash 延迟物化](/tiflash/tiflash-late-materialization.md)功能默认开启。 |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入) | 新增 | 控制是否开启分布式执行框架。开启分布式执行后，DDL、Import 等支持的后端任务将会由集群中多个 TiDB 节点共同完成。该变量由 `tidb_ddl_distribute_reorg` 改名而来。|
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-从-v710-版本开始引入) |  新增        |                              |  通过设置该变量，你可以更细粒度地控制优化器的行为，并且避免集群升级后优化器行为变化导致的性能回退。    |
| [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-从-v710-版本开始引入) | 新增 | 控制是否使用最小网络数据交换策略。使用该策略时，TiDB 会估算 Broadcast Hash Join 和 Shuffled Hash Join 两种算法所需进行网络交换的数据量，并选择网络交换数据量较小的算法。该功能开启后，[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 将不再生效。 |
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiFlash | `http_port` | 删除 | 废弃 TiFlash HTTP 服务端口（默认 `8123`）。|
|   TiDB       |    [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-从-v710-版本开始引入)      |    新增     |   用于控制 TiDB 启动时是否采用轻量级的统计信息初始化。     |
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
    - 提升 TiFlash 在存算分离架构下的性能和稳定性 [#6882](https://github.com/pingcap/tiflash/issues/6882)  @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin) **tw:qiancai**

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
