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
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.2/tiproxy-load-balance">TiProxy 支持多种负载均衡策略<!--tw@Oreoxmt--></td>
    <td>在 TiDB v8.2.0 中，TiProxy 支持从多个维度（包括状态、连接数、健康度、内存、CPU 和地理位置）对 TiDB 节点进行评估和排序，同时支持通过 <code>policy</code> 配置项配置这些负载均衡策略的优先级。TiProxy 将根据 <code>policy</code> 动态选择最优 TiDB 节点执行数据库操作，从而优化 TiDB 节点的整体资源使用率，提升集群性能和吞吐。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.2/system-variables#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入">并行 HashAgg 算法支持数据落盘成为正式功能 (GA)<!--tw@Oreoxmt--></td>
    <td>HashAgg 是 TiDB 中常用的聚合算子，用于快速聚合具有相同字段值的行。TiDB v8.0.0 引入并行 HashAgg 作为实验特性，以进一步提升处理速度。当内存资源不足时，并行 HashAgg 可以将临时排序数据落盘，避免因内存使用过度而导致的 OOM 风险，从而提升查询性能和节点稳定性。该功能在 v8.2.0 成为正式功能，并默认开启，用户可以安全地设置并行 HashAgg 的并发度。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.2/tidb-configuration-file#stats-load-concurrency-从-v540-版本开始引入">统计信息加载效率提升 10 倍<!--tw@hfxsd--></td>
    <td>对于拥有大量表和分区的集群，比如 SaaS 或 PaaS 服务，统计信息加载效率的提升能够解决 TiDB 实例启动缓慢的问题，从而减少由于统计信息加载失败造成的性能回退，提升集群的稳定性。</td>
  </tr>
  <tr>
    <td rowspan="1">数据库管理与可观测性</td>
    <td><a href="">为切换资源组引入权限控制<!--tw@lilin90--></td>
    <td>随着资源管控功能被广泛应用，对资源组切换操作的权限控制能够避免数据库用户对资源的滥用，强化管理员对整体资源使用的保护，从而提升集群的稳定性。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

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

    SaaS 或 PaaS 类业务应用中可能存在大量的数据表，这些表不但会拖慢初始统计信息的加载速度，也会增加高负载的情况下同步负载的失败率。TiDB 的启动时间以及执行计划的准确性都会受到影响。在 v8.2.0 中，TiDB 从并发模型、内存分配方式等多个角度优化了统计信息的加载过程，降低延迟，提升吞吐，避免由于统计信息加载速度过慢，影响业务扩容。

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

    在 v8.2.0 版本之前，你需要依赖外部工具或自定义验证逻辑进行 JSON 数据验证，开发和维护比较复杂，开发效率低。从 v8.2.0 版本开始，引入了 `JSON_SCHEMA_VALID()` 函数，你可以在 TiDB 中直接验证 JSON 数据的有效性，提高数据的完整性和一致性，提升了开发效率。

    更多信息，请参考[用户文档](/functions-and-operators/json-functions.md#验证函数)。

### 数据库管理

* TiUP 支持部署 PD 微服务 [#5766](https://github.com/tikv/pd/issues/5766) @[rleungx](https://github.com/rleungx) **tw@qiancai** <!--1841-->

     PD 从 v8.0.0 开始支持微服务模式。该模式通过将 PD 的时间戳分配和集群调度功能拆分为独立的服务进行部署和管理，可以更好地控制资源的使用和隔离，减少不同服务相互之间的影响。但是，在 v8.2.0 之前的版本中，PD 微服务仅支持通过 TiDB Operator 进行部署。

    从 v8.2.0 开始，PD 微服务支持通过 TiUP 进行部署。你可以在集群中单独部署 `tso` 微服务和 `scheduling` 微服务，从而实现 PD 的性能扩展，解决大规模集群下 PD 的性能瓶颈问题。当 PD 出现明显的性能瓶颈且无法升级配置的情况下，建议考虑使用该模式。

    更多信息，请参考[用户文档](/pd-microservices.md)。

* 为切换资源组的操作增加权限控制 [#53440](https://github.com/pingcap/tidb/issues/53440) @[glorv](https://github.com/glorv) **tw@lilin90** <!--1740-->

    TiDB 允许用户使用命令 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 或 Hint [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 切换到其他资源组，这可能会造成部分数据库用户对资源组的滥用。TiDB v8.2.0 增加了对资源组切换行为的管控，只有被授予动态权限 `RESOURCE_GROUP_ADMIN` 或者 `RESOURCE_GROUP_USER` 的数据库用户，才能切换到其他资源组，以加强对系统资源的保护。

    为了维持兼容性，从旧版本升级到 v8.2.0 及之后版本的集群维持原行为不变。通过设置新增变量 [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-从-v820-版本开始引入) 为 `ON`，来开启上述的增强权限控制。

    更多信息，请参考[用户文档](/tidb-resource-control.md#绑定资源组)。

### 可观测性

* 记录执行计划没有被缓存的原因 [#50618](https://github.com/pingcap/tidb/issues/50618) @[qw4990](https://github.com/qw4990) **tw@hfxsd** <!--1819-->

    在一些场景下，用户希望多数执行计划能够被缓存，以节省执行开销，并降低延迟。目前执行计划缓存对 SQL 有一定限制，部分形态 SQL 的执行计划无法被缓存，但是用户很难识别出无法被缓存的 SQL 以及对应的原因。因此，在新版本中，我们向系统表 [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 中增加了新的列，解释计划无法被缓存的原因，协助用户做性能调优。

    更多信息，请参考[用户文档](/statement-summary-tables.md#表的字段介绍)。

### 安全

* 增强 TiFlash 日志脱敏 [#8977](https://github.com/pingcap/tiflash/issues/8977) @[JaySon-Huang](https://github.com/JaySon-Huang) **tw@Oreoxmt** <!--1818-->

    TiDB v8.0.0 增强了日志脱敏功能，支持控制是否使用标记符号 `‹ ›` 包裹 TiDB 日志中的用户数据。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理，从而提升日志脱敏功能的灵活性。在 v8.2.0 中，TiFlash 进行了类似的日志脱敏功能增强。要使用该功能，可以将 TiFlash 配置项 `security.redact_info_log` 的值设置为 `marker`。

    更多信息，请参考[用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)。

### 数据迁移

* 对齐不同 changefeed 的 Syncpoint [#11212](https://github.com/pingcap/tiflow/issues/11212) @[hongyunyan](https://github.com/hongyunyan) **tw@lilin90** <!--1869-->

    在 v8.2.0 之前，对齐多个 changefeed 的 Syncpoint 很有挑战性。在创建 changefeed 时，必须谨慎选择 changefeed 的 `startTs`，以便与其他 changefeed 的 Syncpoint 对齐。从 v8.2.0 开始，为 changefeed 创建的 Syncpoint 是 changefeed 的 `sync-point-interval` 配置的倍数。这个调整可以让你对齐具有相同 `sync-point-interval` 配置的多个 changefeed 的 Syncpoint，简化和提高了对齐多个下游集群的能力。

    更多信息，请参考[用户文档](/ticdc/ticdc-upstream-downstream-check.md#注意事项)。

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.1.0 升级至当前版本 (v8.2.0) 所需兼容性变更信息。如果从 v8.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* TiDB Lightning，从 v8.2.0 开始当用户设置 strict-format = true，来切分大的 CSV 文件为多个小的 CSV 文件来提升并发和导入性能时，需要显式指定行结束符 terminator 参数的取值为  \r，\n 或 \r\n 。否则可能导致 CSV 文件数据解析异常。
* Import Into SQL 语法，从 v8.2.0 开始，当用户导入 CSV 文件，且指定 split 参数来切分大的 CSV 文件为多个小的 CSV 文件来提升并发和导入性能时，需显式指定行结束符 LINES_TERMINATED_BY 参数的取值为  \r，\n 或 \r\n 。否则可能导致 CSV 文件数据解析异常。

* 行为变更 2

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) | 废弃 | **tw@Oreoxmt** <!--1842--> |
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-从-v760-版本开始引入) | 修改 | 最小值从 `1` 改为 `0`。当设置为 `0` 时，TiDB 会根据集群规模自适应调整并发度。**tw@hfxsd** <!--xxx--> |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入) | 修改 | 从 v8.2.0 开始，默认设置下，TiDB 不会收集类型为 `mediumtext` 和 `longtext` 的列，避免潜在的 OOM 风险。**tw@hfxsd** <!--1759--> |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats) | 修改 | 默认值改为 `OFF`，即关闭历史统计信息，避免潜在的稳定性问题。 **tw@hfxsd** <!--1759--> |
| [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-从-v820-版本开始引入) | 新增 | [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 和优化器 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) Hint 权限控制的开关。 **tw@lilin90** <!--1740--> |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-从-v650-版本开始引入) | 修改 | 最小值从 `1` 改为 `0`。当设置为 `0` 时，TiDB 会根据集群规模自适应调整并发度。**tw@hfxsd** <!--xxx--> |
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件           | 配置项                | 修改类型 | 描述                                 |
|----------------|--------------------|------|------------------------------------|
| TiDB | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-从-v540-版本开始引入) | 修改 | 默认值从 `5` 修改为 `0`，最小值从 `1` 修改为 `0`。`0` 为自动模式，根据服务器情况，自动调节并发度。 |
| TiDB | [`token-limit`](/tidb-configuration-file.md#token-limit) | 修改 | 最大值从 `18446744073709551615` （64 位平台）和 `4294967295`（32 位平台）修改为 `1048576`，代表同时执行请求的 session 个数最多可以设置为 `1048576`。|
| TiKV | [`max-apply-unpersisted-log-limit`](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-从-v820-版本开始引入) | 新增 | 允许 apply 已经 `commit` 但尚未持久化的 Raft 日志的最大数量。 默认值为 `1024`。 |

### 系统表

### 其他

- 在 BR v8.2.0 之前的版本中，当集群存在 TiCDC 同步任务时，BR 不支持进行[数据恢复](/br/backup-and-restore-overview.md)。从 BR 8.2.0 起，BR 数据恢复对 TiCDC 的限制被放宽：如果所恢复数据的 BackupTS（即备份时间）早于 Changefeed 的 [CheckpointTS](/ticdc/ticdc-architecture.md#checkpointts)（即记录当前同步进度的时间戳），BR 数据恢复可以正常进行。考虑到 BackupTS 的时间通常较早，此时可以认为绝大部分场景下，当集群存在 TiCDC 同步任务时，BR 都可以进行数据恢复。 **tw@qiancai** <!--1843-->

## 离线包变更

## 废弃功能

* TiDB 在 v8.0.0 引入了 [Priority Queue](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用来优化统计信息收集的对象排序。[Priority Queue](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将会成为统计信息收集的唯一排序方式，变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 计划在未来版本废弃。
* TiDB 在 v7.5.0 增加了新的统计信息合并方法，用来避免分区统计信息合并时出现 OOM。原有的合并方法将在未来版本被移除，对应的变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 也将废弃。
* 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
* 从 v8.2.0 开始，BR 快照恢复参数 [`--concurrency`](/use-br-command-line-tool#常用选项) 被废弃。作为替代，你可以通过 [`--tikv-max-restore-concurrency`](/use-br-command-line-tool#常用选项) 配置快照恢复阶段的单个 TiKV 节点的任务最大并发数。 **tw@qiancai** <!--1850-->
* 从 v8.20 开始，BR 快照恢复参数 [`--granularity`](/br-snapshot-guide#快照恢复的性能与影响) 被废弃，[粗粒度打散 Region 算法](/br/br-snapshot-guide.md#恢复快照备份数据)默认启用。**tw@qiancai** <!--1850-->

## 改进提升

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - 优化对大数据量的表进行简单查询时获取数据分布信息的性能 [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)  **tw@Oreoxmt** <!--1561-->
    - 聚合的结果集能够作为 IndexJoin 的内表，使更多的复杂查询可以匹配到 IndexJoin，从而可以通过索引提升查询效率 [#37068](https://github.com/pingcap/tidb/issues/37068) @[elsa0520](https://github.com/elsa0520) **tw@hfxsd** <!--1510-->

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

        - 优化备份稳定性以及性能，提升在大量表备份过程发生节点重启、扩容、网络抖动时的备份性能 [#52534](https://github.com/pingcap/tidb/issues/52534) @[3pointer](https://github.com/3pointer) **tw@qiancai** <!--1844-->
        - 优化恢复过程中对 TiCDC Changefeed 的细粒度检查，如果 Changefeed 的 [CheckpointTS](/ticdc/ticdc-architecture.md#checkpointts) 晚于数据的备份时间，则不会影响恢复操作，从而减少不必要的等待时间，提升用户体验 [#53131](https://github.com/pingcap/tidb/issues/53131) @[YuJuncen](https://github.com/YuJuncen) **tw@qiancai** <!--1843-->
        - 为 [`BACKUP`](/sql-statements/sql-statement-backup.md) 语句和 [`RESTORE`](sql-statements/sql-statement-restore.md) 语句添加了若干常用的参数选项，例如 `CHECKSUM_CONCURRENCY` [#53040](https://github.com/pingcap/tidb/issues/53040) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1849-->
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
    - 修复在客户端读取数据超时后查询无法被终止的问题 [#44009](https://github.com/pingcap/tidb/issues/44009) @[wshwsh12](https://github.com/wshwsh12)  **tw@Oreoxmt** <!--1636-->

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

- [贡献者 GitHub ID](链接)