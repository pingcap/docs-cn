---
title: TiDB 8.3.0 Release Notes
summary: 了解 TiDB 8.3.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.3.0 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：8.3.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.3/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.3.0-DMR#version-list)

在 8.3.0 版本中，你可以获得以下关键特性：

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
    <td rowspan="4">可扩展性和性能</td>
    <td> <a href="https://docs.pingcap.com/zh/tidb/v8.3/partitioned-table#全局索引">分区表全局索引（实验特性）</a></td> **tw@hfxsd** <!--1531-->
    <td>全局索引能够有效提升对非分区键的检索效率，同时也解除了分区键一定要包含唯一键 (Unique Key) 的限制，扩展了 TiDB 分区表的使用场景，也能够避免数据迁移可能遇到的部分应用改造工作。</td>
  </tr>
  <tr>
    <td>Projection 下推成为正式功能</td>**tw@Oreoxmt** <!--1872-->
    <td> Projection 下推能够尽可能将负载分散到存储节点，也可以减少节点间的数据传输，这能够降低一部分 SQL 的执行时间，提升数据库整体性能。</td>
  </tr>
  <tr>
    <td>统计信息收集忽略不必要的列</td>**tw@lilin90** <!--1753-->
    <td>在保证优化器能够获取到必要信息的前提下，加快了统计信息收集的速度，提升统计信息的时效性，进而保证最优的执行计划的选择，提升集群性能。同时也降低的系统开销，改善资源利用率。</td>
  </tr>
  <tr>
    <td>读写性能的细粒度优化</td>**tw@qiancai** <!--1893-->
    <td>通过优化 KV 请求的策略，增加获取 TSO 的模式等多重手段，进一步提升 TiDB 的读写性能，降低业务的执行时间，改善延迟。</td>
  </tr>
  <tr>
    <td rowspan="1">稳定性与高可用</td>
    <td>TiProxy 管理虚拟 IP</td>**tw@Oreoxmt** <!--1887-->
    <td>在 TiProxy 内实现了对连接地址的管理，支持自动的地址切换，而不依赖外部平台或工具。这能够简化 TiProxy 的部署形式，降低了数据库接入层的复杂度。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* Projection 下推功能正式发布 [#51876](https://github.com/pingcap/tidb/issues/51876) @[yibin87](https://github.com/yibin87) **tw@Oreoxmt** <!--1872-->

    将 `Projection` 算子下推到存储引擎可以减少计算引擎和存储引擎之间的传输的数据量，特别是对 [JSON 查询类函数](/functions-and-operators/json-functions/json-functions-search.md)或 [JSON 值属性类函数](/functions-and-operators/json-functions/json-functions-return.md)，效果更加显著。在 v8.3.0 版本中，TiDB 正式发布 Projection 下推功能。在该功能启用时，优化器会自动将符合条件的 JSON 查询类函数、JSON 值属性类函数等下推至存储引擎。
    
    变量 [tidb_opt_projection_push_down](/system-variables.md#tidb_opt_projection_push_down-从-v610-版本开始引入) 控制是否启用 Projection 下推功能。该变量的默认值将调整为 `ON`，表示默认启用该功能。

    更多信息，请参考[用户文档](/system-variables.md#tidb_opt_projection_push_down-从-v610-版本开始引入)。
    
* 优化 KV 请求的批处理策略 [#xxx](https://github.com/pingcap/tidb/issues/xxx) @[zyguan](https://github.com/zyguan) **tw@Oreoxmt** <!--1897-->

    TiDB 读取数据需要通过 KV 请求进行。通过将 KV 请求攒批并进行批处理，可以有效提高执行效率。在 v8.3.0 版本之前，TiDB 批处理策略的效率不高。在 v8.3.0 版本，TiDB 在现有的基础 KV 请求批处理策略基础上，引入更加高效的策略。通过新增的配置项 [`tikv-client.batch-policy·](/tidb-configuration-file.md#batch-policy-从-v830-版本开始引入) 设定不同的批处理策略。
    
    更多信息，请参考[用户文档](/tidb-configuration-file.md#batch-policy-从-v830-版本开始引入)。
    
* 增加获取 TSO 的 RPC 模式，降低获取 TSO 的延迟 [#54960](https://github.com/pingcap/tidb/issues/54960) @[MyonKeminta](https://github.com/MyonKeminta) **tw@qiancai** <!--1893-->

    TiDB 在向 PD 请求 TSO 时，会汇总一定时间段的请求并以同步的方式进行批处理以减少 RPC 请求数量、降低 PD 负载。对于延迟敏感的场景，这种模式的性能并不理想。在 v8.3.0 版本中，TiDB 新增 TSO 请求的异步批处理模式，并提供不同的并发能力，以增加相应的 PD 负载为代价，降低获取 TSO 的延迟。通过新增的变量 [tidb_tso_client_rpc_mode](/system-variables.md#tidb_tso_client_rpc_mode-从-v830-版本开始引入) 设定获取 TSO 的 RPC 模式。
    
    更多信息，请参考[用户文档](/system-variables.md#tidb_tso_client_rpc_mode-从-v830-版本开始引入)。
    
* TiFlash 新增 Hashagg 聚合计算模式，提升高 NDV 数据的聚集计算性能 [#9196](https://github.com/pingcap/tiflash/issues/9196) @[guo-shaoge](https://github.com/guo-shaoge) **tw@Oreoxmt** <!--1855-->

    TiFlash 的 Hashagg 聚合计算中，第一阶段也会进行聚集计算。对于高 NDV 数据，这种模式效率较低。在 v8.3.0 版本中，TiFlash 引入多种 Hashagg 聚合计算模式，提升不同特征数据的聚集计算性能。通过新增的变量 [tiflash_hashagg_preaggregation_mode](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入) 设定 Hashagg 聚合计算模式。
    
    更多信息，请参考[用户文档](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入)。

* 统计信息收集忽略不必要的列 [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/hi-rustin) **tw@lilin90** <!--1753-->

    当优化器生成执行计划时，只需要部分列的统计信息，例如过滤条件上的列，连接键上的列，聚合目标用到的列。从 v8.3.0 起，TiDB 会持续观测 SQL 语句对列的使用历史，默认只收集有索引的列，以及被观测到的有必要收集统计信息的列。这将会提升统计信息的收集速度，避免不必要的资源浪费。

    从旧版本升级到 v8.3.0 或更高版本的用户，默认保留原有行为，收集所有列的统计信息，需要手工设置变量 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 为 `PREDICATE` 来启用，新部署默认开启。
    
    对于随机查询比较多的偏分析型系统，可以设置 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 为 `ALL` 收集所有列的统计信息，保证随机查询的性能。其余类型的系统推荐保留 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 为 `PREDICATE` 只收集必要的列。

    更多信息，请参考[用户文档](/statistics.md#收集部分列的统计信息)。

* 提升了一些系统表的查询性能 [#]() @[tangenta](https://github.com/tangenta) **tw@hfxsd** <!--1865-->

    在之前的版本，当集群规模变大，表数量较多时，查询系统表性能较慢。

    在 v8.0.0 优化了以下 4 个系统表的查询性能:
    
    - INFORMATION_SCHEMA.TABLES
    - INFORMATION_SCHEMA.STATISTICS
    - INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    - INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS

    在 v8.3.0 版本优化了以下系统表的查询性能，相比 v8.2.0 性能有数倍的提升:

    - INFORMATION_SCHEMA.CHECK_CONSTRAINTS
    - INFORMATION_SCHEMA.COLUMNS
    - INFORMATION_SCHEMA.PARTITIONS
    - INFORMATION_SCHEMA.SCHEMATA
    - INFORMATION_SCHEMA.SEQUENCES
    - INFORMATION_SCHEMA.TABLE_CONSTRAINTS
    - INFORMATION_SCHEMA.TIDB_CHECK_CONSTRAINTS
    - INFORMATION_SCHEMA.TiDB_INDEXES
    - INFORMATION_SCHEMA.TIDB_INDEX_USAGE
    - INFORMATION_SCHEMA.VIEWS

    更多信息，请参考[用户文档](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入)。

* 分区表达式使用 `EXTRACT(YEAR_MONTH...)` 函数时，支持分区裁剪，提升查询性能 [#54209](https://github.com/pingcap/tidb/pull/54209) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1885-->

    之前的版本，当分区表达式使用 `EXTRACT(YEAR_MONTH...)` 函数时，不支持分区裁剪，导致查询性能较差。从 v8.3.0 开始，当分区表达式使用该函数时，支持分区裁剪，提升了查询性能。

    更多信息，请参考[用户文档](/partition-pruning.md#场景三)。
    
* 批量建库 (`CREATE DATABASE`) 的性能提升近 5 倍 [#54436 ](https://github.com/pingcap/tidb/issues/54436) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1863-->

    v8.0.0 引入了参数 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)，用于在批量建表的场景提升建表的性能。从 v8.3.0 版本开始，该参数对批量建库的性能也有提升，相比 v8.2.0，性能有近 5 倍的提升。 

    更多信息，请参考[用户文档](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入)。    

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiProxy 支持虚拟 IP 管理功能 [#583](https://github.com/pingcap/tiproxy/issues/583) @[djshow832](https://github.com/djshow832) **tw@Oreoxmt** <!--1887-->

    在 v8.3.0 版本之前，使用主从模式保证高可用时，TiProxy 还需要额外的组件管理虚拟 IP 功能。在 v8.3.0 版本，TiProxy 支持虚拟 IP 管理功能。在主动模式下，当出现主从节点切换时，主节点自动绑定指定的虚拟 IP，保证客户端的正常访问。 
    
    通过设定 TiProxy 配置项 [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip) 指定虚拟 IP。如果未指定，则表示不启用该功能。
    
    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。

* 新增以流式获取游标的结果集 （实验特性） [#54526](https://github.com/pingcap/tidb/issues/54526) @[YangKeao](https://github.com/YangKeao) **tw@lilin90** <!--1891-->

    当应用代码通过 [Cursor Fetch](/develop/dev-guide-connection-parameters.md#使用-streamingresult-流式获取执行结果) 获取结果集时，TiDB 通常会将完整结果保存至 TiDB ，再分批返回给客户端。如果结果集过大，可能会触发临时落盘。自 v8.3.0 开始，通过设置系统变量[`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入) 为 `ON`，TiDB 不再把所有数据读取到 TiDB 节点，而是会随着客户端的读取逐步将数据传送至 TiDB 节点。在处理较大结果集时，这将会减少 TiDB 节点的内存使用，提升集群的稳定性。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入)。

* SQL 绑定的增强 [#issue号](链接) @[time-and-fate](https://github.com/time-and-fate) **tw@lilin90** <!--1760-->

    在 OLTP 负载环境中，绝大部分 SQL 的最优执行计划是固定的，因此对业务中的重要 SQL 实施执行计划绑定，可以减少执行计划变差的机会，提升系统稳定性。为了满足客户创建大量 SQL 绑定的需求，TiDB 对 SQL 绑定的能力和体验进行了增强，其中包括：

    - 用单条 SQL 从多个历史执行计划中创建 SQL 绑定
    - 从历史执行计划创建绑定不再受表数量的限制
    - SQL 绑定支持更多的优化器提示，能够更稳定重现原执行计划

    更多信息，请参考[用户文档](/sql-plan-management.md)。
    
### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 支持 `Shared Lock` 升级为 `Exclusive Lock` [#54999](https://github.com/pingcap/tidb/issues/54999) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1857-->

    TiDB 暂不支持 `Shared Lock`. 在 v8.3.0 版本中，TiDB 支持将 `Shared Lock` 升级为 `Exclusive Lock`，实现对 `Shared Lock` 语法的支持。通过新增的变量 [tidb_enable_shared_lock_upgrade](/system-variables.md#tidb_enable_shared_lock_upgrade-从-v830-版本开始引入) 控制是否启用该功能。

* 分区表支持全局索引 (Global Index)（实验特性） [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1531-->

    之前版本的分区表，因为不支持全局索引有较多的限制，比如唯一键必须包含分区建，如果查询条件不带分区建，查询时会扫描所有分区，导致性能较差。从 v7.6.0 开始，引入了参数 [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-从-v760-版本开始引入) 用于开启全局索引特性，但该功能当时处于开发中，不够完善，不建议开启。
    
    从 v8.3.0 开始，全局索引作为实验特性正式发布了。你可以显式地创建全局索引，唯一键也不需要强制包含分区建，满足灵活的业务需求。同时基于全局索引也提升了不带分区建的索引的查询性能。

    更多信息，请参考[用户文档](/partitioned-table.md#全局索引)。
### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 系统视图 `PROCESS LIST` 增加 `ROWS_AFFECTED` 字段 [#54486](https://github.com/pingcap/tidb/issues/54486) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1903-->

    TiDB 并不能显示当前 DML 语句已经处理的数据行数。在 v8.3.0 版本中，系统视图 `PROCESS LIST` 增加 `ROWS_AFFECTED` 字段，展示当前 DML 语句已经写入的数据行数。
    
    更多信息，请参考[用户文档](/information-schema/information-schema-processlist.md)。

* 展示初始统计信息加载的进度 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@lilin90** <!--1792-->

    TiDB 在启动时要对基础统计信息进行加载，在表或者分区数量很多的情况下，这个过程要耗费一定时间，当配置项 [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入) 为 `ON` 时，初始统计信息加载完成前 TiDB 不会对外提供服务。在这种情况下，用户需要对加载过程进行观测，从而能够预期服务开启时间。自 v8.3.0，TiDB 会在日志中分阶段打印初始统计信息加载的进度，让客户了解运行情况。为了给外部工具提供格式化的结果，TiDB 增加了额外的监控 [API](/tidb-monitoring-api.md)，能够在启动阶段随时获取初始统计信息的加载进度。
    
### 安全

* 增强 PD 日志脱敏 [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhe](https://github.com/xhebox)

    TiDB v8.0.0 增强了日志脱敏功能，支持控制是否使用标记符号 `‹ ›` 包裹 TiDB 日志中的用户数据。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理，从而提升日志脱敏功能的灵活性。在 v8.2.0 中，TiFlash 实现了类似的日志脱敏功能增强。在 v8.3.0 中，PD 实现了类似的日志脱敏功能增强，要使用该功能，可以将 PD 配置项 `security.redact_info_log` 的值设置为 `marker`。

    更多信息，请参考[用户文档](/log-redaction.md)。

  * 增强 TiKV 日志脱敏 [#17206](https://github.com/tikv/tikv/issues/17206) @[lucasliang](https://github.com/LykxSassinator)

    TiDB v8.0.0 增强了日志脱敏功能，支持控制是否使用标记符号 `‹ ›` 包裹 TiDB 日志中的用户数据。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理，从而提升日志脱敏功能的灵活性。在 v8.2.0 中，TiFlash 实现了类似的日志脱敏功能增强。在 v8.3.0 中，TiKV 实现了类似的日志脱敏功能增强，要使用该功能，可以将 TiKV 配置项 `security.redact_info_log` 的值设置为 `marker`。

    更多信息，请参考[用户文档](/log-redaction.md)。

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.2.0 升级至当前版本 (v8.3.0) 所需兼容性变更信息。如果从 v8.1.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 行为变更 1
* 行为变更 2

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) | 新增 | 控制 `ANALYZE TABLE` 语句默认收集的列。将其设置为 `PREDICATE` 表示仅收集 [predicate columns](/statistics.md#收集部分列的统计信息) 的统计信息；将其设置为 `ALL` 表示收集所有列的统计信息。 |
| [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入) | 新增 | 这个变量用于控制 [Cursor Fetch](/develop/dev-guide-connection-parameters.md#使用-streamingresult-流式获取执行结果) 功能的行为。|
|        |                              |      |
|        |                              |      |

### 系统表

### 其他

## 离线包变更

## 废弃功能

* 以下为计划将在未来版本中废弃的功能：

    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将被废弃。
    * TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 将被废弃。
    * 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。

## 改进提升

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - TopN 算子支持数据落盘功能 [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1715-->
    - TiDB 支持 `WITH ROLLUP` 修饰符和 `GROUPING` 函数 [#42631](https://github.com/pingcap/tidb/issues/42631) @[Arenatlx](https://github.com/Arenatlx) **tw@Oreoxmt** <!--1714-->
    - 变量 `tidb_low_resolution_tso` 增加全局作用域 [#55022](https://github.com/pingcap/tidb/issues/55022) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1857-->
    - 优化 MemDB 实现，降低写事务延迟 [#xxx](https://github.com/pingcap/tidb/issues/xxx) @[you06](https://github.com/you06) **tw@hfxsd** <!--1892-->
    - GC 支持并发删除 Range 以提升处理效率 [#xxx](https://github.com/pingcap/tidb/issues/xxx) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1890-->

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
