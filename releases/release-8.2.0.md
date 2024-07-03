---
title: TiDB 8.2.0 Release Notes
summary: 了解 TiDB 8.2.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.2.0 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：8.2.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.2/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.2.0-DMR#version-list)

在 8.2.0 版本中，你可以获得以下关键特性：

<table>
<thead>
  <tr>
    <th>分类</th>
    <th>功能/增强</th>
    <th>描述</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="3">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.2/tiproxy-load-balance">TiProxy 支持多种负载均衡策略</a></td>
    <td>在 TiDB v8.2.0 中，TiProxy 支持从多个维度（包括状态、连接数、健康度、内存、CPU 和地理位置）对 TiDB 节点进行评估和排序，并支持通过 <code>policy</code> 配置项配置这些负载均衡策略的优先级。TiProxy 将根据 <code>policy</code> 动态选择最优 TiDB 节点执行数据库操作，从而优化 TiDB 节点的整体资源使用率，提升集群性能和吞吐。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.2/system-variables#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入">并行 HashAgg 算法支持数据落盘成为正式功能 (GA)</a></td>
    <td>HashAgg 是 TiDB 中常用的聚合算子，用于快速聚合具有相同字段值的行。TiDB v8.0.0 引入并行 HashAgg 作为实验特性，以进一步提升处理速度。当内存资源不足时，并行 HashAgg 可以将临时排序数据落盘，避免因内存使用过度而导致的 OOM 风险，从而提升查询性能和节点稳定性。该功能在 v8.2.0 成为正式功能，并默认开启，用户可以通过 <code>tidb_executor_concurrency</code> 安全地设置并行 HashAgg 的并发度。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.2/tidb-configuration-file#stats-load-concurrency-从-v540-版本开始引入">统计信息加载效率提升 10 倍</a></td>
    <td>对于拥有大量表和分区的集群，比如 SaaS 或 PaaS 服务，统计信息加载效率的提升能够解决 TiDB 实例启动缓慢的问题，从而减少由于统计信息加载失败造成的性能回退，提升集群的稳定性。</td>
  </tr>
  <tr>
    <td rowspan="1">数据库管理与可观测性</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.2/tidb-resource-control#绑定资源组">为切换资源组引入权限控制</a></td>
    <td>随着资源管控功能被广泛应用，对资源组切换操作的权限控制能够避免数据库用户对资源的滥用，强化管理员对整体资源使用的保护，从而提升集群的稳定性。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 性能

* 支持下推以下字符串函数到 TiKV [#50601](https://github.com/pingcap/tidb/issues/50601) @[dbsid](https://github.com/dbsid) **tw@Oreoxmt** <!--1663-->

    * `JSON_ARRAY_APPEND()`
    * `JSON_MERGE_PATCH()`
    * `JSON_REPLACE()`

  更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* TiDB 支持并行排序 [#49217](https://github.com/pingcap/tidb/issues/49217) [#50746](https://github.com/pingcap/tidb/issues/50746) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1665-->

    在 v8.2.0 之前，TiDB 只能以非并行的方式执行排序计算，当需要对大量数据进行排序时，查询性能会受到影响。

    从 v8.2.0 开始，TiDB 支持并行排序功能，显著提升了排序计算的性能。该功能无需手动开启，TiDB 会根据系统变量 [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-从-v50-版本开始引入) 的值自动选择并行或非并行排序。

    更多信息，请参考[用户文档](/system-variables.md#tidb_executor_concurrency-从-v50-版本开始引入)。

* TiDB 的并行 HashAgg 算法支持数据落盘成为正式功能 (GA) [#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1842-->

    TiDB v8.0.0 以实验特性引入了并行 HashAgg 算法支持数据落盘功能。在 v8.2.0 中，该功能成为正式功能 (GA)。TiDB 在使用并行 HashAgg 算法时，将根据内存使用情况自动触发数据落盘，从而兼顾查询性能和数据处理量。该功能默认开启，控制该功能的变量 `tidb_enable_parallel_hashagg_spill` 将在未来版本中废弃。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)。

### 稳定性

* 统计信息加载效率提升 10 倍 [#52831](https://github.com/pingcap/tidb/issues/52831) @[hawkingrei](https://github.com/hawkingrei) **tw@hfxsd** <!--1754-->

    SaaS 或 PaaS 类业务应用中可能存在大量的数据表，这些表不但会拖慢初始统计信息的加载速度，也会增加高负载情况下同步负载的失败率。TiDB 的启动时间以及执行计划的准确性都会受到影响。在 v8.2.0 中，TiDB 从并发模型、内存分配方式等多个角度优化了统计信息的加载过程，降低延迟，提升吞吐，避免由于统计信息加载速度过慢，影响业务扩容。

    新增支持自适应的并行加载。默认情况下，配置项 [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-从-v540-版本开始引入) 的值为 `0`，统计信息加载的并行度会根据硬件规格自动选择。

    更多信息，请参考[用户文档](/tidb-configuration-file.md#stats-load-concurrency-从-v540-版本开始引入)。

### 高可用

* TiProxy 支持多种负载均衡策略 [#465](https://github.com/pingcap/tiproxy/issues/465) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@Oreoxmt** <!--1777-->

    TiProxy 是 TiDB 的官方代理组件，位于客户端和 TiDB server 之间，为 TiDB 集群提供负载均衡和连接保持功能。在 v8.2.0 之前，TiProxy 默认使用 v1.0.0 版本，仅支持基于 TiDB server 状态和连接数的负载均衡策略。

    从 v8.2.0 开始，TiProxy 默认使用 v1.1.0 版本，新增多种负载均衡策略，除了状态和连接数，还支持根据健康度、内存、CPU、地理位置对 TiDB 集群的连接进行动态负载均衡调度，提高整个 TiDB 集群的稳定性。

    你可以通过 TiProxy 配置项 [`policy`](/tiproxy/tiproxy-configuration.md#policy) 配置负载均衡策略的组合和优先级，具体策略包括：

    * `resource`：资源优先策略，优先级顺序依次为基于状态、健康度、内存、CPU、地理位置、连接数的负载均衡。
    * `location`：地理优先策略，优先级顺序依次为基于状态、地理位置、健康度、内存、CPU、连接数的负载均衡。
    * `connection`：最小连接数策略，优先级顺序依次为基于状态、连接数的负载均衡。

  更多信息，请参考[用户文档](/tiproxy/tiproxy-load-balance.md)。

### SQL 功能

* TiDB 支持 JSON Schema Validation 函数 [#52779](https://github.com/pingcap/tidb/issues/52779) @[dveeden](https://github.com/dveeden) **tw@hfxsd** <!--1840-->

    在 v8.2.0 之前，你需要依赖外部工具或自定义验证逻辑进行 JSON 数据验证，开发和维护比较复杂，开发效率低。从 v8.2.0 版本开始，引入了 `JSON_SCHEMA_VALID()` 函数，你可以在 TiDB 中直接验证 JSON 数据的有效性，提高数据的完整性和一致性，提升了开发效率。

    更多信息，请参考[用户文档](/functions-and-operators/json-functions.md#验证函数)。

### 数据库管理

* TiUP 支持部署 PD 微服务 [#5766](https://github.com/tikv/pd/issues/5766) @[rleungx](https://github.com/rleungx) **tw@qiancai** <!--1841-->

    PD 从 v8.0.0 开始支持微服务模式。该模式通过将 PD 的时间戳分配和集群调度功能拆分为独立的服务进行部署和管理，可以更好地控制资源的使用和隔离，减少不同服务之间的相互影响。但是，在 v8.2.0 之前的版本中，PD 微服务仅支持通过 TiDB Operator 进行部署。

    从 v8.2.0 开始，PD 微服务支持通过 TiUP 进行部署。你可以在集群中单独部署 `tso` 微服务和 `scheduling` 微服务，从而实现 PD 的性能扩展，解决大规模集群下 PD 的性能瓶颈问题。当 PD 出现明显的性能瓶颈且无法升级配置的情况下，建议考虑使用该模式。

    更多信息，请参考[用户文档](/pd-microservices.md)。

* 为切换资源组的操作增加权限控制 [#53440](https://github.com/pingcap/tidb/issues/53440) @[glorv](https://github.com/glorv) **tw@lilin90** <!--1740-->

    TiDB 允许用户使用命令 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 或 Hint [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 切换到其他资源组，这可能会造成部分数据库用户对资源组的滥用。TiDB v8.2.0 增加了对资源组切换行为的管控，只有被授予动态权限 `RESOURCE_GROUP_ADMIN` 或者 `RESOURCE_GROUP_USER` 的数据库用户，才能切换到其他资源组，以加强对系统资源的保护。

    为了维持兼容性，从旧版本升级到 v8.2.0 及之后版本的集群维持原行为不变。通过设置新增变量 [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-从-v820-版本开始引入) 为 `ON`，来开启上述的增强权限控制。

    更多信息，请参考[用户文档](/tidb-resource-control.md#绑定资源组)。

### 可观测性

* 记录执行计划没有被缓存的原因 [#50618](https://github.com/pingcap/tidb/issues/50618) @[qw4990](https://github.com/qw4990) **tw@hfxsd** <!--1819-->

    在一些场景下，用户希望多数执行计划能够被缓存，以节省执行开销，并降低延迟。目前执行计划缓存对 SQL 有一定限制，部分形态 SQL 的执行计划无法被缓存，但是用户很难识别出无法被缓存的 SQL 以及对应的原因。因此，从 v8.2.0 开始，为系统表 [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 增加了新的列 `PLAN_CACHE_UNQUALIFIED` 和 `PLAN_CACHE_UNQUALIFIED_LAST_REASON`，来解释计划无法被缓存的原因，协助用户做性能调优。

    更多信息，请参考[用户文档](/statement-summary-tables.md#表的字段介绍)。

### 安全

* 增强 TiFlash 日志脱敏 [#8977](https://github.com/pingcap/tiflash/issues/8977) @[JaySon-Huang](https://github.com/JaySon-Huang) **tw@Oreoxmt** <!--1818-->

    TiDB v8.0.0 增强了日志脱敏功能，支持控制是否使用标记符号 `‹ ›` 包裹 TiDB 日志中的用户数据。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理，从而提升日志脱敏功能的灵活性。在 v8.2.0 中，TiFlash 进行了类似的日志脱敏功能增强。要使用该功能，可以将 TiFlash 配置项 `security.redact_info_log` 的值设置为 `marker`。

    更多信息，请参考[用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)。

### 数据迁移

* 对齐不同 changefeed 的 Syncpoint [#11212](https://github.com/pingcap/tiflow/issues/11212) @[hongyunyan](https://github.com/hongyunyan) **tw@lilin90** <!--1869-->

    在 v8.2.0 之前，对齐多个 changefeed 的 Syncpoint 很有挑战性。在创建 changefeed 时，必须谨慎选择 changefeed 的 `startTs`，以便与其他 changefeed 的 Syncpoint 对齐。从 v8.2.0 开始，为 changefeed 创建的 Syncpoint 是 changefeed 的 `sync-point-interval` 配置的倍数。这个调整可以让你对齐具有相同 `sync-point-interval` 配置的多个 changefeed 的 Syncpoint，简化和提高了对齐多个下游集群的能力。

    更多信息，请参考[用户文档](/ticdc/ticdc-upstream-downstream-check.md#注意事项)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.1.0 升级至当前版本 (v8.2.0) 所需兼容性变更信息。如果从 v8.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 使用 TiDB Lightning 导入 CSV 文件时，如果设置了严格格式 `strict-format = true` 将一个大 CSV 文件切分为多个小 CSV 文件来提升并发和导入性能，需要显式指定行结束符 `terminator`，参数的取值为 `\r`、`\n` 或 `\r\n`。如果没有指定行结束符，可能导致 CSV 文件数据解析异常。[#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

* 使用 `IMPORT INTO` 导入 CSV 文件时，如果指定 `SPLIT_FILE` 参数将一个大 CSV 文件切分为多个小 CSV 文件来提升并发和导入性能，需显式指定行结束符 `LINES_TERMINATED_BY`，参数的取值为 `\r`、`\n` 或 `\r\n`。如果没有指定行结束符，可能导致 CSV 文件数据解析异常。[#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

* 在 BR v8.2.0 之前的版本中，当集群存在 TiCDC 同步任务时，BR 不支持进行[数据恢复](/br/backup-and-restore-overview.md)。从 BR 8.2.0 起，BR 数据恢复对 TiCDC 的限制被放宽：如果所恢复数据的 BackupTS（即备份时间）早于 Changefeed 的 [CheckpointTS](/ticdc/ticdc-architecture.md#checkpointts)（即记录当前同步进度的时间戳），BR 数据恢复可以正常进行。考虑到 BackupTS 的时间通常较早，此时可以认为绝大部分场景下，当集群存在 TiCDC 同步任务时，BR 都可以进行数据恢复。[#53131](https://github.com/pingcap/tidb/issues/53131) @[YuJuncen](https://github.com/YuJuncen) **tw@qiancai** <!--1843-->

### MySQL 兼容性

* 在 v8.2.0 之前，执行带有 `PASSWORD REQUIRE CURRENT DEFAULT` 选项的 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 语句会返回错误，因为 TiDB 不支持且无法解析该选项。从 v8.2.0 开始，TiDB 支持解析并忽略该选项，以便与 MySQL 兼容 [#53305](https://github.com/pingcap/tidb/issues/53305) @[dveeden](https://github.com/dveeden)

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-从-v760-版本开始引入) | 修改 | 最小值从 `1` 改为 `0`。当设置为 `0` 时，TiDB 会根据集群规模自适应调整并发度。**tw@hfxsd** <!--xxx--> |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入) | 修改 | 从 v8.2.0 开始，默认设置下，TiDB 不会收集类型为 `mediumtext` 和 `longtext` 的列，避免潜在的 OOM 风险。**tw@hfxsd** <!--1759--> |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats) | 修改 | 默认值改为 `OFF`，即关闭历史统计信息，避免潜在的稳定性问题。 **tw@hfxsd** <!--1759--> |
| [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-从-v50-版本开始引入) | 修改 | 新增支持对 `sort` 算子的并发度进行设置。 |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-从-v650-版本开始引入) | 修改 | 最小值从 `1` 改为 `0`。当设置为 `0` 时，TiDB 会根据集群规模自适应调整并发度。**tw@hfxsd** <!--xxx--> |
| [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-从-v820-版本开始引入) | 新增 | [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 和优化器 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) Hint 权限控制的开关。 **tw@lilin90** <!--1740--> |

### 配置文件参数

| 配置文件           | 配置项                | 修改类型 | 描述                                 |
|----------------|--------------------|------|------------------------------------|
| TiDB | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-从-v540-版本开始引入) | 修改 | 默认值从 `5` 修改为 `0`，最小值从 `1` 修改为 `0`。`0` 为自动模式，根据服务器情况，自动调节并发度。 |
| TiDB | [`token-limit`](/tidb-configuration-file.md#token-limit) | 修改 | 最大值从 `18446744073709551615` （64 位平台）和 `4294967295`（32 位平台）修改为 `1048576`，代表同时执行请求的 session 个数最多可以设置为 `1048576`，避免设置过大导致 TiDB Server OOM。|
| TiKV | [`max-apply-unpersisted-log-limit`](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-从-v820-版本开始引入) | 修改 | 默认值从 ` 0` 修改为 `1024`，代表允许 apply 已经 `commit` 但尚未持久化的 Raft 日志的最大数量为 1024，用于降低 TiKV 节点上因 IO 抖动导致的长尾延迟。 |
| TiKV | [`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type) | 修改 | 该配置项现在也会影响 TiKV 向 TiDB 发送的响应消息的压缩算法。开启压缩可能消耗更多 CPU 资源。 |
| TiFlash | [`security.redact_info_log`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) | 修改 | 可选值新增 `marker` 选项。该选项被启用时，日志中的用户数据会被标记符号 `‹ ›` 包裹。 |

### 编译器版本

* 为了提升 TiFlash 的开发体验，编译和构建 TiDB 所需的 LLVM 的最低版本从 13.0 升级到了 17.0。如果你是 TiDB 开发者，为了保证顺利编译，请对应升级你的 LLVM 编译器版本。[#7193](https://github.com/pingcap/tiflash/issues/7193) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

## 废弃功能

* 以下为从 v8.2.0 开始已废弃的功能：

    * 从 v8.2.0 开始，TiDB 的配置项 `enable-replica-selector-v2` 被废弃。向 TiKV 发送 RPC 请求时，默认使用新版本的 Region 副本选择器。
    * 从 v8.2.0 开始，BR 快照恢复参数 `--concurrency` 被废弃。作为替代，你可以通过 [`--tikv-max-restore-concurrency`](/use-br-command-line-tool#常用选项) 配置快照恢复阶段单个 TiKV 节点的任务最大并发数。 **tw@qiancai** <!--1850-->
    * 从 v8.2.0 开始，BR 快照恢复参数 `--granularity` 被废弃，[粗粒度打散 Region 算法](/br/br-snapshot-guide.md#恢复快照备份数据)默认启用。**tw@qiancai** <!--1850-->

* 以下为计划将在未来版本中废弃的功能：

    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将被废弃。
    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)，用于控制 TiDB 是否支持并行 HashAgg 进行落盘。在未来版本中，系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) 将被废弃。
    * TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 将被废弃。
    * 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
    * TiDB Lightning 参数 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 计划在未来版本中废弃，并在后续版本中删除。该参数将由 `conflict.threshold` 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。

* 以下为计划将在未来版本中移除的功能：

    * 从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) 参数统一控制逻辑导入和物理导入模式的冲突检测策略。旧版冲突检测的参数 [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) 将在未来版本中被移除。

## 改进提升

+ TiDB <!--tw@hfxsd: 13 条-->
    - 支持并行执行[逻辑 DDL 语句 (General DDL)](/ddl-introduction.md#ddl-语句类型简介)。相比 v8.1.0，在使用 10 个会话并发提交不同 DDL 语句的场景下，性能提升了 3 到 6 倍 [#53246](https://github.com/pingcap/tidb/issues/53246) @[D3Hunter](https://github.com/D3Hunter)
    - 改进形如 `((a = 1 and b = 2 and c > 3) or (a = 4 and b = 5 and c > 6)) and d > 3` 的表达式匹配多列索引的逻辑，使其能生成更加精准的 `Range` [#41598](https://github.com/pingcap/tidb/issues/41598) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    - 优化对大数据量的表进行简单查询时获取数据分布信息的性能 [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)  **tw@Oreoxmt** <!--1561-->
    - 聚合的结果集能够作为 IndexJoin 的内表，使更多的复杂查询可以匹配到 IndexJoin，从而可以通过索引提升查询效率 [#37068](https://github.com/pingcap/tidb/issues/37068) @[elsa0520](https://github.com/elsa0520) **tw@hfxsd** <!--1510-->
    - 通过批量删除 TiFlash placement rule 的方式，提升对分区表执行 `TRUNCATE`、`DROP` 后数据 GC 的处理速度 [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 升级 Azure Identity Libraries 和 Microsoft Authentication Library 的版本，增强安全性 [#53990](https://github.com/pingcap/tidb/issues/53990) @[hawkingrei](https://github.com/hawkingrei)
    - 将 `token-limit` 的最大值设置为 `1048576`，避免设置过大导致 TiDB Server OOM [#53312](https://github.com/pingcap/tidb/issues/53312) @[djshow832](https://github.com/djshow832)
    - 改进对于 MPP 执行计划的列裁剪功能，以提升 TiFlash MPP 的执行性能 [#52133](https://github.com/pingcap/tidb/issues/52133) @[yibin87](https://github.com/yibin87)
    - 优化 `IndexLookUp` 算子在回表数据量较多（大于 1024 行）时的性能开销 [#53871](https://github.com/pingcap/tidb/issues/53871) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.10.md > 改进提升> TiDB - 在 MPP 负载均衡时移除不包含任何 Region 的 Store [#52313](https://github.com/pingcap/tidb/issues/52313) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ TiKV <!--tw@lilin90: 9 条-->
    - 增加 **Compaction Job Size(files)** 指标来呈现单个 compaction job 涉及的 SST 文件数 [#16837](https://github.com/tikv/tikv/issues/16837) @[zhangjinpeng87](https://github.com/zhangjinpeng87)
    - 默认开启[提前 apply](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-从-v810-版本开始引入) 特性，开启后，Raft leader 在多数 peer 完成 Raft log 持久化之后即可进行 apply，不再要求 leader 自身完成 Raft log 的持久化，降低少数 TiKV 抖动对写请求延迟的影响 [#16717](https://github.com/tikv/tikv/issues/16717) @[glorv](https://github.com/glorv)
    - 在 Raft 日志持久化之前，将 Raft 日志保留在缓存中，以提升 follower 对日志的读取性能 [#16717](https://github.com/tikv/tikv/issues/16717) @[glorv](https://github.com/glorv)
    - 增加 **Raft dropped messages** 事件的可观测性，以便定位写入慢的根本原因 [#17093](https://github.com/tikv/tikv/issues/17093) @[Connor1996](https://github.com/Connor1996)
    - 增加对 ingest file 的延迟可观测性，以便排查集群的延迟问题 [#17078](https://github.com/tikv/tikv/issues/17078) @[LykxSassinator](https://github.com/LykxSassinator)
    - 利用单独的线程来进行副本清理工作，保证 Raft 读写关键路径的延迟稳定 [#16001](https://github.com/tikv/tikv/issues/16001) @[hbisheng](https://github.com/hbisheng)
    - 提升正在进行 apply 的副本数的可观测性 [#17078](https://github.com/tikv/tikv/issues/17078) @[hbisheng](https://github.com/hbisheng)

+ PD <!--tw@lilin90: 2 条-->

    - 优化提升 Region 心跳处理的性能 [#7897](https://github.com/tikv/pd/issues/7897) @[nolouch](https://github.com/nolouch) @[rleungx](https://github.com/rleungx) @[JmPotato](https://github.com/JmPotato)
    - pd-ctl 支持通过 byte 或 query 维度来查询热点 Region [#7369](https://github.com/tikv/pd/issues/7369) @[lhy1024](https://github.com/lhy1024)

+ TiFlash <!--tw@hfxsd: 5 条-->

    - 减少数据高并发读取下的锁冲突，优化短查询性能 [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)
    - 消除 `Join` 算子中对于 Join Key 的冗余拷贝 [#9057](https://github.com/pingcap/tiflash/issues/9057) @[gengliqi](https://github.com/gengliqi)
    - 将 `HashAgg` 算子中转换两级哈希表的过程并行化 [#8956](https://github.com/pingcap/tiflash/issues/8956) @[gengliqi](https://github.com/gengliqi)
    - 移除 `HashAgg` 算子的冗余的聚合函数以减少计算开销 [#8891](https://github.com/pingcap/tiflash/issues/8891) @[guo-shaoge](https://github.com/guo-shaoge)

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 7 条-->

        - 优化备份功能，提升在大量表备份过程中遇到节点重启、扩容或网络抖动时的备份性能和稳定性 [#52534](https://github.com/pingcap/tidb/issues/52534) @[3pointer](https://github.com/3pointer) **tw@qiancai** <!--1844-->
        - 优化恢复过程中对 TiCDC Changefeed 的细粒度检查，如果 Changefeed 的 [CheckpointTS](/ticdc/ticdc-architecture.md#checkpointts) 晚于数据的备份时间，则不会影响恢复操作，从而减少不必要的等待时间，提升用户体验 [#53131](https://github.com/pingcap/tidb/issues/53131) @[YuJuncen](https://github.com/YuJuncen) **tw@qiancai** <!--1843-->
        - 为 [`BACKUP`](/sql-statements/sql-statement-backup.md) 语句和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 语句添加了多个常用参数选项，例如 `CHECKSUM_CONCURRENCY` [#53040](https://github.com/pingcap/tidb/issues/53040) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1849-->
        - 去掉除了 `br log restore` 子命令之外其它 `br log` 子命令对 TiDB `domain` 数据结构的载入，降低内存消耗 [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - 支持对日志备份过程中生成的临时文件进行加密 [#15083](https://github.com/tikv/tikv/issues/15083) @[YuJuncen](https://github.com/YuJuncen)
        - 在 Grafana 面板中新增 `tikv_log_backup_pending_initial_scan` 监控指标 [#16656](https://github.com/tikv/tikv/issues/16656) @[3pointer](https://github.com/3pointer)
        - 优化 PITR 日志的输出格式，并在日志中新增 `RestoreTS` 字段 [#53645](https://github.com/pingcap/tidb/issues/53645) @[dveeden](https://github.com/dveeden)

    + TiCDC

        - (dup): release-6.5.10.md > 改进提升> Tools> TiCDC - 支持当下游为消息队列 (Message Queue, MQ) 或存储服务时直接输出原始事件 [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 错误修复

+ TiDB <!--tw@qiancai: 以下 9 条-->

    - 修复当 SQL 语句包含 Outer Join，且 Join 条件包含 `false IN (column_name)` 表达式时，查询结果缺少部分数据的问题 [#49476](https://github.com/pingcap/tidb/issues/49476) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    - 在收集表中 `PREDICATE COLUMNS` 的统计信息时，不再收集系统表中列的统计信息 [#53403](https://github.com/pingcap/tidb/issues/53403) @[hi-rustin](https://github.com/hi-rustin)
    - 修复系统变量 `tidb_persist_analyze_options` 为 `OFF` 时，系统变量 `tidb_enable_column_tracking` 未生效的问题 [#53478](https://github.com/pingcap/tidb/issues/53478) @[hi-rustin](https://github.com/hi-rustin)
    - 修复在 `(*PointGetPlan).StatsInfo()` 执行过程中可能遇到数据竞争的问题 [#49803](https://github.com/pingcap/tidb/issues/49803) [#43339](https://github.com/pingcap/tidb/issues/43339) @[qw4990](https://github.com/qw4990)
    - 修复在包含数据修改操作的事务中查询带有虚拟列的表时，查询结果可能错误的问题 [#53951](https://github.com/pingcap/tidb/issues/53951) @[qw4990](https://github.com/qw4990)
    - 修复在自动收集统计信息时，系统变量 `tidb_enable_async_merge_global_stats` 和 `tidb_analyze_partition_concurrency` 未生效的问题 [#53972](https://github.com/pingcap/tidb/issues/53972) @[hi-rustin](https://github.com/hi-rustin)
    - 修复查询 `TABLESAMPLE` 时可能遇到 `plan not supported` 报错的问题 [#54015](https://github.com/pingcap/tidb/issues/54015) @[tangenta](https://github.com/tangenta)
    - 修复执行 `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` 查询时结果出错的问题 [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在客户端读取数据超时后查询无法被终止的问题 [#44009](https://github.com/pingcap/tidb/issues/44009) @[wshwsh12](https://github.com/wshwsh12)  **tw@Oreoxmt** <!--1636-->
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 `Longlong` 类型在谓词中溢出的问题 [#45783](https://github.com/pingcap/tidb/issues/45783) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复窗口函数中有某些子查询时可能会 panic 的问题 [#42734](https://github.com/pingcap/tidb/issues/42734) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 TopN 算子可能被错误地下推的问题 [#37986](https://github.com/pingcap/tidb/issues/37986) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.2.md > 错误修复> TiDB - 修复在聚簇索引作为谓词时 `SELECT INTO OUTFILE` 不生效的问题 [#42093](https://github.com/pingcap/tidb/issues/42093) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 information schema 缓存未命中导致 stale read 查询延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 `YEAR` 类型的列与超出范围的无符号整数进行比较导致错误结果的问题 [#50235](https://github.com/pingcap/tidb/issues/50235) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复重启 TiDB 后，主键列统计信息中的直方图和 TopN 未被加载的问题 [#37548](https://github.com/pingcap/tidb/issues/37548) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.2.md > 错误修复> TiDB - 修复 Massively Parallel Processing (MPP) 中 `final` AggMode 和 `non-final` AggMode 无法共存的问题 [#51362](https://github.com/pingcap/tidb/issues/51362) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复执行谓词总是为 `true` 的 `SHOW ERRORS` 语句导致 TiDB panic 的问题 [#46962](https://github.com/pingcap/tidb/issues/46962) @[elsa0520](https://github.com/elsa0520)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复在递归 CTE 中无法使用视图的问题 [#49721](https://github.com/pingcap/tidb/issues/49721) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.2.md > 错误修复> TiDB - 修复 TiDB 启动加载统计信息时可能因为 GC 推进报错的问题 [#53592](https://github.com/pingcap/tidb/issues/53592) @[you06](https://github.com/you06)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复使用 `PREPARE`/`EXECUTE` 方式执行带 `CONV` 表达式的语句，且 `CONV` 表达式包含 `?` 参数时，多次执行可能导致查询结果错误的问题 [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复将数据从 `FLOAT` 类型转换为 `UNSIGNED` 类型时结果错误的问题 [#41736](https://github.com/pingcap/tidb/issues/41736) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复创建带有外键的表时，TiDB 未创建对应的统计信息元信息 (`stats_meta`) 的问题 [#53652](https://github.com/pingcap/tidb/issues/53652) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复查询中的某些过滤条件可能导致 planner 模块发生 `invalid memory address or nil pointer dereference` 报错的问题 [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复并发执行 `CREATE OR REPLACE VIEW` 可能报错 `table doesn't exist` 的问题 [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 `INFORMATION_SCHEMA.TIDB_TRX` 表中 `STATE` 字段的 `size` 未定义导致 `STATE` 显示为空的问题 [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复关闭 `tidb_enable_async_merge_global_stats` 时，GlobalStats 中的 `Distinct_count` 信息可能错误的问题 [#53752](https://github.com/pingcap/tidb/issues/53752) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复使用 Optimizer Hints 时，可能输出错误的 WARNINGS 信息的问题 [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei) <!--tw@Oreoxmt: 以下 18 条-->
    - 修复对时间类型执行取负操作结果不正确的问题 [#52262](https://github.com/pingcap/tidb/issues/52262) @[solotzg](https://github.com/solotzg)
    - 修复 `REGEXP()` 函数对空模式参数未显式报错的问题 [#53221](https://github.com/pingcap/tidb/issues/53221) @[yibin87](https://github.com/yibin87)
    - 修复将 JSON 转换为时间格式在某些情况下可能会丢失精度的问题 [#53352](https://github.com/pingcap/tidb/issues/53352) @[YangKeao](https://github.com/YangKeao)
    - 修复 `JSON_QUOTE()` 函数在某些情况下返回结果不正确的问题 [#37294](https://github.com/pingcap/tidb/issues/37294) @[dveeden](https://github.com/dveeden)
    - 修复执行 `ALTER TABLE ... REMOVE PARTITIONING` 后可能导致数据丢失的问题 [#53385](https://github.com/pingcap/tidb/issues/53385) @[mjonss](https://github.com/mjonss)
    - 修复使用 `auth_socket` 认证插件时，TiDB 在某些情况下未能拒绝不符合身份认证的用户连接的问题 [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 JSON 相关函数在某些情况下报错信息与 MySQL 不一致的问题 [#53799](https://github.com/pingcap/tidb/issues/53799) @[dveeden](https://github.com/dveeden)
    - 修复分区表在 `INFORMATION_SCHEMA.PARTITIONS` 中的 `INDEX_LENGTH` 列显示不正确的问题 [#54173](https://github.com/pingcap/tidb/issues/54173) @[Defined2014](https://github.com/Defined2014)
    - 修复 `INFOMATION_SCHEMA.TABLES` 中 `TIDB_ROW_ID_SHARDING_INFO` 列显示不正确的问题 [#52330](https://github.com/pingcap/tidb/issues/52330) @[tangenta](https://github.com/tangenta)
    - 修复生成列返回非法时间戳的问题 [#52509](https://github.com/pingcap/tidb/issues/52509) @[lcwangchao](https://github.com/lcwangchao)
    - 修复通过分布式执行框架添加索引时，设置 `max-index-length` 导致 TiDB panic 的问题 [#53281](https://github.com/pingcap/tidb/issues/53281) @[zimulala](https://github.com/zimulala)
    - 修复某些情况下可以创建非法的 `DECIMAL(0,0)` 列类型的问题 [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - 修复使用 `CURRENT_DATE()` 作为列默认值时查询结果错误的问题 [#53746](https://github.com/pingcap/tidb/issues/53746) @[tangenta](https://github.com/tangenta)
    - 修复 `ALTER DATABASE ... SET TIFLASH REPLICA` 语句错误地给 `SEQUENCE` 表添加 TiFlash 副本的问题 [#51990](https://github.com/pingcap/tidb/issues/51990) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `INFORMATION_SCHEMA.KEY_COLUMN_USAGE` 表中 `REFERENCED_TABLE_SCHEMA` 字段显示不正确的问题 [#52350](https://github.com/pingcap/tidb/issues/52350) @[wd0517](https://github.com/wd0517)
    - 修复 `AUTO_ID_CACHE=1` 时，单条语句插入多行导致 `AUTO_INCREMENT` 列不连续的问题 [#52465](https://github.com/pingcap/tidb/issues/52465) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复弃用警告的格式 [#52515](https://github.com/pingcap/tidb/issues/52515) @[dveeden](https://github.com/dveeden)
    - 修复 `TRACE` 命令在 `copr.buildCopTasks` 中丢失的问题 [#53085](https://github.com/pingcap/tidb/issues/53085) @[time-and-fate](https://github.com/time-and-fate)
    - 修复包含 `memory_quota` 的绑定在子查询中可能不生效的问题 [#53834](https://github.com/pingcap/tidb/issues/53834) @[qw4990](https://github.com/qw4990)
    - 修复在某些情况下，元数据锁使用不当可能导致使用 plan cache 时写入异常数据的问题 [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)

+ TiKV <!--tw@lilin90: 以下 8 条-->

    - 修复将 `JSON_ARRAY_APPEND()` 函数下推至 TiKV 导致 TiKV panic 的问题 [#16930](https://github.com/tikv/tikv/issues/16930) @[dbsid](https://github.com/dbsid)
    - 修复 leader 未及时清理发送失败的 snapshot 文件的问题 [#16976](https://github.com/tikv/tikv/issues/16976) @[hbisheng](https://github.com/hbisheng)
    - 修复高并发的 Coprocessor 请求可能导致 TiKV OOM 的问题 [#16653](https://github.com/tikv/tikv/issues/16653) @[overvenus](https://github.com/overvenus)
    - 修复在线变更 `raftstore.periodic-full-compact-start-times` 配置项可能会导致 TiKV panic 的问题 [#17066](https://github.com/tikv/tikv/issues/17066) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复 `make docker` 和 `make docker_test` 失败的问题 [#17075](https://github.com/tikv/tikv/issues/17075) @[shunki-fujita](https://github.com/shunki-fujita)
    - 修复 **gRPC request sources duration** 在监控中显示错误的问题 [#17133](https://github.com/tikv/tikv/issues/17133) @[King-Dylan](https://github.com/King-Dylan)
    - 修复设置 gRPC 消息的压缩算法 (`grpc-compression-type`) 对 TiKV 发送到 TiDB 的消息不起作用的问题 [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.5.2.md > 错误修复> TiKV - 修复 tikv-ctl 的 `raft region` 命令的输出中未包含 Region 状态信息的问题 [#17037](https://github.com/tikv/tikv/issues/17037) @[glorv](https://github.com/glorv)
    - 修复 `advance-ts-interval` 配置未被用于限制 CDC 和 log-backup 模块中 `check_leader` 操作的 timeout，导致在某些情况下 TiKV 正常重启时 `resolved_ts` lag 过大的问题 [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - (dup): release-7.5.2.md > 错误修复> PD - 修复 `ALTER PLACEMENT POLICY` 无法修改 placement policy 的问题 [#52257](https://github.com/pingcap/tidb/issues/52257) [#51712](https://github.com/pingcap/tidb/issues/51712) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-7.1.5.md > 错误修复> PD - 修复写热点调度可能会违反放置策略 (placement policy) 约束的问题 [#7848](https://github.com/tikv/pd/issues/7848) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-6.5.10.md > 错误修复> PD - 修复使用 Placement Rules 的情况下，down peer 可能无法恢复的问题 [#7808](https://github.com/tikv/pd/issues/7808) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.2.md > 错误修复> PD - 修复取消资源组查询导致大量重试的问题 [#8217](https://github.com/tikv/pd/issues/8217) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.5.2.md > 错误修复> PD - 修复手动切换 PD leader 可能失败的问题 [#8225](https://github.com/tikv/pd/issues/8225) @[HuSharp](https://github.com/HuSharp)

+ TiFlash <!--tw@hfxsd: 1 条-->

    - (dup): release-7.5.2.md > 错误修复> TiFlash - 修复在含空分区的分区表上执行查询时，可能会超时的问题 [#9024](https://github.com/pingcap/tiflash/issues/9024) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.5.2.md > 错误修复> TiFlash - 修复在存算分离架构下，DDL 新增带有 not null 属性的列后，查询可能返回错误的 null 值的问题 [#9084](https://github.com/pingcap/tiflash/issues/9084) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-6.5.10.md > 错误修复> TiFlash - 修复函数 `SUBSTRING_INDEX()` 可能导致 TiFlash Crash 的问题 [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - 修复通过 BR 或 TiDB Lightning 导入数据后，FastScan 模式下可能读到大量重复数据的问题 [#9118](https://github.com/pingcap/tiflash/issues/9118) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 5 条-->

        - (dup): release-7.5.2.md > 错误修复> Tools> Backup & Restore (BR) - 修复由于 `EndKey` 为空导致恢复事务 KV 集群失败的问题 [#52574](https://github.com/pingcap/tidb/issues/52574) @[3pointer](https://github.com/3pointer)
        - (dup): release-6.5.10.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PD 连接失败导致日志备份 advancer owner 所在的 TiDB 可能崩溃的问题 [#52597](https://github.com/pingcap/tidb/issues/52597) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.10.md > 错误修复> Tools> Backup & Restore (BR) - 修复日志备份在 advancer owner 发生迁移后可能被暂停的问题 [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-6.5.10.md > 错误修复> Tools> Backup & Restore (BR) - 修复在恢复过程中，由于多层重试导致 BR 无法正确识别错误的问题 [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)
        - 修复用于获取 TiKV 配置的连接可能未被关闭的问题 [#52595](https://github.com/pingcap/tidb/issues/52595) @[RidRisR](https://github.com/RidRisR)
        - 修复测试用例 `TestStoreRemoved` 不稳定的问题 [#52791](https://github.com/pingcap/tidb/issues/52791) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 PITR 恢复过程中 TiFlash 崩溃的问题 [#52628](https://github.com/pingcap/tidb/issues/52628) @[RidRisR](https://github.com/RidRisR)
        - 修复增量备份过程中扫描 DDL 作业的效率较低的问题 [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - 修复断点备份过程中查找 Region leader 中断导致备份性能受影响问题 [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)

    + TiCDC <!--tw@hfxsd: 2 条-->

        - 修复 Grafana 监控中的 **Kafka Outgoing Bytes** 面板显示不准确的问题 [#10777](https://github.com/pingcap/tiflow/issues/10777) @[asddongmen](https://github.com/asddongmen)
        - 修复在多节点环境下进行大量 `UPDATE` 操作时，反复重启 Changefeed 可能导致的数据不一致问题 [#11219](https://github.com/pingcap/tiflow/issues/11219) @[lidezhu](https://github.com/lidezhu)

    + TiDB Data Migration (DM) <!--tw@Oreoxmt: 1 条-->

        - (dup): release-7.5.2.md > 错误修复> Tools> TiDB Data Migration (DM) - 升级 `go-mysql` 以修复连接阻塞的问题 [#11041](https://github.com/pingcap/tiflow/issues/11041) @[D3Hunter](https://github.com/D3Hunter)
        - 修复同步 MariaDB 数据时 `SET` 语句导致 DM panic 的问题 [#10206](https://github.com/pingcap/tiflow/issues/10206) @[dveeden](https://github.com/dveeden)

    + TiDB Lightning <!--tw@Oreoxmt: 1 条-->

        - 修复 TiDB Lightning 导入 zstd 压缩文件时可能报错的问题 [#53587](https://github.com/pingcap/tidb/issues/53587) @[lance6716](https://github.com/lance6716)

    + Dumpling

        - (dup): release-6.5.10.md > 错误修复> Tools> Dumpling - 修复 Dumpling 在同时导出表和视图时报错的问题 [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    + TiDB Binlog

        - (dup): release-6.5.10.md > 错误修复> Tools> TiDB Binlog - 修复开启 TiDB Binlog 后，在 `ADD COLUMN` 执行过程中删除行可能报错 `data and columnID count not match` 的问题 [#53133](https://github.com/pingcap/tidb/issues/53133) @[tangenta](https://github.com/tangenta)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [CabinfeverB](https://github.com/CabinfeverB)
- [DanRoscigno](https://github.com/DanRoscigno)（首次贡献者）
- [ei-sugimoto](https://github.com/ei-sugimoto)（首次贡献者）
- [eltociear](https://github.com/eltociear)
- [jiyfhust](https://github.com/jiyfhust)
- [michaelmdeng](https://github.com/michaelmdeng)（首次贡献者）
- [mittalrishabh](https://github.com/mittalrishabh)
- [onlyacat](https://github.com/onlyacat)
- [qichengzx](https://github.com/qichengzx)（首次贡献者）
- [SeaRise](https://github.com/SeaRise)
- [shawn0915](https://github.com/shawn0915)
- [shunki-fujita](https://github.com/shunki-fujita)（首次贡献者）
- [tonyxuqqi](https://github.com/tonyxuqqi)
- [wwu](https://github.com/wwu)（首次贡献者）
- [yzhan1](https://github.com/yzhan1)
