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
    <td rowspan="3">可扩展性和性能</td>
    <td> <a href="https://docs.pingcap.com/zh/tidb/v8.3/partitioned-table#全局索引">分区表全局索引（实验特性）</a></td> **tw@hfxsd** <!--1531-->
    <td>全局索引能够有效提升对非分区键的检索效率，同时也解除了分区键一定要包含唯一键 (Unique Key) 的限制，扩展了 TiDB 分区表的使用场景，也能够避免数据迁移可能遇到的部分应用改造工作。</td>
  </tr>
  <tr>
    <td>默认将 <code>Projection</code> 算子下推到存储引擎</td>**tw@Oreoxmt** <!--1872-->
    <td><code>Projection</code> 算子下推可以将负载分散到存储节点，同时减少节点间的数据传输。这有助于降低部分 SQL 的执行时间，提升数据库的整体性能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.3/statistics#收集部分列的统计信息">统计信息收集忽略不必要的列</a></td>**tw@lilin90** <!--1753-->
    <td>在保证优化器能够获取到必要信息的前提下，加快了统计信息收集的速度，提升统计信息的时效性，进而保证选择最优的执行计划，提升集群性能。同时也降低了系统开销，改善了资源利用率。</td>
  </tr>
  <tr>
    <td rowspan="1">稳定性与高可用</td>
    <td>TiProxy 内置虚拟 IP 管理</td>**tw@Oreoxmt** <!--1887-->
    <td>在 v8.3.0 中，TiProxy 内置虚拟 IP 管理功能，支持自动切换虚拟 IP，而无需依赖外部平台或工具。这简化了 TiProxy 的部署，降低了数据库接入层的复杂度。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 优化器默认将 `Projection` 算子下推到存储引擎 [#51876](https://github.com/pingcap/tidb/issues/51876) @[yibin87](https://github.com/yibin87) **tw@Oreoxmt** <!--1872-->

    将 `Projection` 算子下推到存储引擎可以减少计算引擎和存储引擎之间的数据传输量。这在处理 [JSON 查询类函数](/functions-and-operators/json-functions/json-functions-search.md)或 [JSON 值属性类函数](/functions-and-operators/json-functions/json-functions-return.md)时尤其有效。从 v8.3.0 开始，TiDB 默认开启 `Projection` 算子下推功能，控制该功能的系统变量 [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-从-v610-版本开始引入) 的默认值从 `OFF` 修改为 `ON`。启用该功能后，优化器会自动将符合条件的 JSON 查询类函数、JSON 值属性类函数等下推到存储引擎。

    更多信息，请参考[用户文档](/system-variables.md#tidb_opt_projection_push_down-从-v610-版本开始引入)。

* 优化 KV 请求的批处理策略 [#55206](https://github.com/pingcap/tidb/issues/55206) @[zyguan](https://github.com/zyguan) **tw@Oreoxmt** <!--1897-->

    TiDB 通过 KV 请求读取数据。将 KV 请求攒批并进行批处理，可以有效提高执行效率。在 v8.3.0 之前，TiDB 的批处理策略效率不高。从 v8.3.0 开始，TiDB 在现有的 KV 请求批处理策略基础上，引入更高效的策略。你可以通过配置项 [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-从-v830-版本开始引入) 设置不同的批处理策略，以适应不同的业务场景。

    更多信息，请参考[用户文档](/tidb-configuration-file.md#batch-policy-从-v830-版本开始引入)。

* TiFlash 新增 HashAgg 聚合计算模式，提升高 NDV 数据的聚合计算性能 [#9196](https://github.com/pingcap/tiflash/issues/9196) @[guo-shaoge](https://github.com/guo-shaoge) **tw@Oreoxmt** <!--1855-->

    在 v8.3.0 之前，TiFlash 在 HashAgg 聚合计算中处理高 NDV (number of distinct rows) 数据时，第一阶段的聚合计算效率较低。从 v8.3.0 开始，TiFlash 引入多种 HashAgg 聚合计算模式，以提升不同特征数据的聚合计算性能。你可以通过系统变量 [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入) 设置 HashAgg 聚合计算模式。

    更多信息，请参考[用户文档](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入)。

* 统计信息收集忽略不必要的列 [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/hi-rustin) **tw@lilin90** <!--1753-->

    当优化器生成执行计划时，只需要部分列的统计信息，例如过滤条件上的列、连接键上的列、聚合目标用到的列。从 v8.3.0 起，TiDB 会持续观测 SQL 语句对列的使用历史，默认只收集有索引的列，以及被观测到的有必要收集统计信息的列。这将会提升统计信息的收集速度，避免不必要的资源浪费。

    从 v8.3.0 之前的版本升级到 v8.3.0 或更高版本时，TiDB 默认保留原有行为，即收集所有列的统计信息。如果要启用该功能，需要手动将系统变量 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 设置为 `PREDICATE`，新部署的集群默认开启该功能。

    对于随机查询比较多的偏分析型系统，可以将系统变量 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 设置为 `ALL` 来收集所有列的统计信息，以保证随机查询的性能。对于其余类型的系统，推荐保留 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 的默认设置 `PREDICATE`，只收集必要列的统计信息。

    更多信息，请参考[用户文档](/statistics.md#收集部分列的统计信息)。

* 提升部分系统表的查询性能 [#50305](https://github.com/pingcap/tidb/issues/50305) @[tangenta](https://github.com/tangenta) **tw@hfxsd** <!--1865-->

    在之前的版本，当集群规模变大，表数量较多时，查询系统表性能较慢。

    在 v8.0.0 优化了以下 4 个系统表的查询性能：

    - INFORMATION_SCHEMA.TABLES
    - INFORMATION_SCHEMA.STATISTICS
    - INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    - INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS

    在 v8.3.0 版本优化了以下系统表的查询性能，相比 v8.2.0 性能有数倍的提升：

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

* 分区表达式使用 `EXTRACT(YEAR_MONTH...)` 函数时，支持分区裁剪，提升查询性能 [#54209](https://github.com/pingcap/tidb/pull/54209) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1885-->

    之前的版本中，当分区表达式使用 `EXTRACT(YEAR_MONTH...)` 函数时，不支持分区裁剪，导致查询性能较差。从 v8.3.0 开始，当分区表达式使用该函数时，支持分区裁剪，提升了查询性能。

    更多信息，请参考[用户文档](/partition-pruning.md#场景三)。

* 批量建表 (`CREATE TABLE`) 的性能提升了 1.4 倍，批量建库 (`CREATE DATABASE`) 的性能提升了 2.1 倍，批量加列 (`ADD COLUMN`) 的性能提升了 2 倍 [#54436](https://github.com/pingcap/tidb/issues/54436) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1863-->

    v8.0.0 引入了系统变量 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)，用于在批量建表的场景中提升建表的性能。在 v8.3.0 中，通过 10 个 session 在单个库内并发提交建表的 DDL，相比 v8.2.0 性能有 1.4 倍的提升。

    在 v8.3.0 中，逻辑 DDL (General DDL) 在批量执行时的性能相比 v8.2.0 也均有提升，其中通过 10 个 session 并发批量建库 (`CREATE DATABASE`) 的性能相比 v8.1.0 提升了 19 倍，相比 v8.2.0 提升了 2.1 倍。10 个 session 对同个库内的多个表批量加列 (`ADD COLUMN`) 性能相比 v8.1.0 提升了 10 倍，相比 v8.2.0 提升了 2 倍。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)。

* 分区表支持全局索引 (Global Index)（实验特性）[#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1531-->

    之前版本的分区表，因为不支持全局索引有较多的限制，比如唯一键必须包含分区键，如果查询条件不带分区键，查询时会扫描所有分区，导致性能较差。从 v7.6.0 开始，引入了系统变量 [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-从-v760-版本开始引入) 用于开启全局索引特性，但该功能当时处于开发中，不够完善，不建议开启。

    从 v8.3.0 开始，全局索引作为实验特性正式发布。你可通过关键字 `Global` 为分区表显式创建一个 Global Index，从而去除分区表唯一建必须包含全部分区键的限制，满足灵活的业务需求。同时基于全局索引也提升了不带分区键的唯一索引的查询性能。

    更多信息，请参考[用户文档](/partitioned-table.md#全局索引)。

### 稳定性

* 支持以流式获取游标的结果集（实验特性）[#54526](https://github.com/pingcap/tidb/issues/54526) @[YangKeao](https://github.com/YangKeao) **tw@lilin90** <!--1891-->

    当应用代码通过 [Cursor Fetch](/develop/dev-guide-connection-parameters.md#使用-streamingresult-流式获取执行结果) 获取结果集时，TiDB 通常会先将完整结果保存至 TiDB 内存，再分批返回给客户端。如果结果集过大，可能会触发落盘临时将结果写入硬盘。

    从 v8.3.0 开始，如果将系统变量 [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入) 设置为 `ON`，TiDB 不再把所有数据读取到 TiDB 节点，而是会随着客户端的读取逐步将数据读到 TiDB 节点。在处理较大的结果集时，这将减少 TiDB 节点的内存使用，提升集群的稳定性。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入)。

* 增强 SQL 执行计划绑定 [#55280](https://github.com/pingcap/tidb/issues/55280) [#issue2](to-be-added) @[time-and-fate](https://github.com/time-and-fate) **tw@lilin90** <!--1760-->

    在 OLTP 负载环境中，绝大部分 SQL 的最优执行计划是固定不变的。对业务中的重要 SQL 实施执行计划绑定，可以降低执行计划变差的几率，提升系统稳定性。为了满足创建大量 SQL 执行计划绑定的场景需求，TiDB 对 SQL 绑定的能力和体验进行了增强，其中包括：

    - 用单条 SQL 语句从多个历史执行计划中创建 SQL 执行计划绑定，提升创建绑定的效率。
    - SQL 执行计划绑定支持更多的优化器提示，并优化了对复杂执行计划的转换方法，使得绑定能够更稳定地还原执行计划。

  更多信息，请参考[用户文档](/sql-plan-management.md)。

### 高可用

* TiProxy 内置虚拟 IP 管理功能 [#583](https://github.com/pingcap/tiproxy/issues/583) @[djshow832](https://github.com/djshow832) **tw@Oreoxmt** <!--1887-->

    在 v8.3.0 之前，当使用主从模式以保证高可用性时，TiProxy 需要额外的组件管理虚拟 IP。从 v8.3.0 开始，TiProxy 内置虚拟 IP 管理功能。在主从模式下，当主节点发生切换时，新的主节点会自动绑定指定的虚拟 IP，确保客户端始终能通过虚拟 IP 连接到可用的 TiProxy。

    要启用虚拟 IP 管理功能，需要通过 TiProxy 配置项 [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip) 指定虚拟 IP 地址，以及 [`ha.interface`](/tiproxy/tiproxy-configuration.md#interface) 指定绑定虚拟 IP 的网络接口。如果这两个配置项均未设置，则表示不启用该功能。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。

### SQL 功能

* 支持将 `SELECT LOCK IN SHARE MODE` 升级为排它锁 [#54999](https://github.com/pingcap/tidb/issues/54999) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1871-->

    TiDB 暂不支持 `SELECT LOCK IN SHARE MODE`。在 v8.3.0 版本中，TiDB 支持将 `SELECT LOCK IN SHARE MODE` 升级为排它锁，实现对 `SELECT LOCK IN SHARE MODE` 语法的支持。你可以使用系统变量 [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-从-v830-版本开始引入) 控制是否启用该功能。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_shared_lock_promotion-从-v830-版本开始引入)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 展示初始统计信息的加载进度 [#53564](https://github.com/pingcap/tidb/issues/53564) @[hawkingrei](https://github.com/hawkingrei) **tw@lilin90** <!--1792-->

    TiDB 在启动时要加载基础统计信息，在表或者分区数量很多的情况下，该过程要耗费一定时间。当配置项 [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入) 设置为 `ON` 时，初始统计信息加载完成前，TiDB 不会对外提供服务。在这种情况下，你需要对加载过程进行观测，从而预估服务开启时间。

    从 v8.3.0 开始，TiDB 会在日志中分阶段打印初始统计信息的加载进度，以便了解运行情况。为了给外部工具提供格式化的结果，TiDB 增加了额外的[监控 API](/tidb-monitoring-api.md)，以便能够在启动阶段随时获取初始统计信息的加载进度。

### 安全

* 增强 PD 日志脱敏 [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhe](https://github.com/xhebox) **tw@hfxsd** <!--1861-->

    TiDB v8.0.0 增强了日志脱敏功能，支持控制是否使用标记符号 `‹ ›` 包裹 TiDB 日志中的用户数据。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理，从而提升日志脱敏功能的灵活性。在 v8.2.0 中，TiFlash 实现了类似的日志脱敏功能增强。

    在 v8.3.0 中，PD 实现了类似的日志脱敏功能增强。要使用该功能，可以将 PD 配置项 `security.redact-info-log` 的值设置为 `marker`。

    更多信息，请参考[用户文档](/log-redaction.md#pd-组件日志脱敏)。

* 增强 TiKV 日志脱敏 [#17206](https://github.com/tikv/tikv/issues/17206) @[lucasliang](https://github.com/LykxSassinator) **tw@hfxsd** <!--1862-->

    TiDB v8.0.0 增强了日志脱敏功能，支持控制是否使用标记符号 `‹ ›` 包裹 TiDB 日志中的用户数据。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理，从而提升日志脱敏功能的灵活性。在 v8.2.0 中，TiFlash 实现了类似的日志脱敏功能增强。

    在 v8.3.0 中，TiKV 实现了类似的日志脱敏功能增强。要使用该功能，可以将 TiKV 配置项 `security.redact-info-log` 的值设置为 `marker`。

    更多信息，请参考[用户文档](/log-redaction.md#tikv-组件日志脱敏)。

### 数据迁移

* TiCDC 支持通过双向复制模式 (Bi-Directional Replication, BDR) 同步 DDL 语句 (GA) [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @okJiang @asddongmen **tw@hfxsd** <!--1689-->

    从 v7.6.0 开始，TiCDC 支持在配置了双向复制的情况下同步 DDL 语句。以前，TiCDC 不支持复制 DDL 语句，因此要使用 TiCDC 双向复制必须将 DDL 语句分别应用到两个 TiDB 集群。有了该特性，TiCDC 可以为一个集群分配 `PRIMARY` BDR role，并将该集群的 DDL 语句复制到下游集群。

    在 v8.3.0，该功能成为正式功能 (GA)。

    更多信息，请参考[用户文档](/ticdc-bidirectional-replication.md)。

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
| [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入) | 新增 | 控制下推到 TiFlash 的两阶段或三阶段 HashAgg 的第一阶段采用哪种预聚合策略。 |
| [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)     | 修改   | 之前该变量仅支持 `GLOBAL` 级别设置。从 v8.3.0 开始，该变量也支持 `SESSION`级别设置。     |
| [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)    | 修改   | 之前该变量仅支持 `GLOBAL` 级别设置。从 v8.3.0 开始，该变量也支持 `SESSION` 级别设置。     |
| [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-从-v50-版本开始引入) | 修改 | 从 v8.3.0 起，该变量可以控制 [GC（垃圾回收）](/garbage-collection-overview.md) 过程中 [Resolve Locks（清理锁）] 和 [Delete Range（删除区间）](/garbage-collection-overview.md#Delete-Ranges删除区间) 的并发线程数。在 v8.3.0 之前，该变量只能控制 Resolve Locks（清理锁）的线程数。|
| [`tidb_enable_shared_lock_upgrade`](/system-variables.md#tidb_enable_shared_lock_upgrade-从-v830-版本开始引入)       | 新增  | 控制是否启用共享锁升级为排他锁的功能。默认值为 `OFF`，表示不启用共享锁升级为排他锁的功能。  |
| [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) | 修改 | 增加 GLOBAL 作用域。|
| [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-从-v610-版本开始引入) | 修改 | 增加 GLOBAL 作用域，变量值可以持久化到集群。经进一步的测试，默认值从 `OFF` 修改为 `ON`，即默认允许优化器将 `Projection` 算子下推到 TiKV。|

### 配置文件参数

| 配置文件           | 配置项                | 修改类型 | 描述                                 |
|----------------|--------------------|------|------------------------------------|
| TiDB | [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-从-v830-版本开始引入) | 新增 | 控制 TiDB 向 TiKV 发送请求时的批处理策略。 |
| PD   |  [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-从-v50-版本开始引入) |  修改 | 支持将 PD 配置项 `security.redact-info-log` 的值设置为 `marker`，使用标记符号 `‹ ›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。  |
| PD   |  [`schedule.max-merge-region-keys`](/pd-configuration-file.md#max-merge-region-keys) |  修改 | 默认值从 `200000` 修改为 `540000`，以兼容 `schedule.max-merge-region-size` 的调整，减小随着集群规模增大后 Region 个数过多带来的管理压力。 |
| PD   |  [`schedule.max-merge-region-size`](/pd-configuration-file.md#max-merge-region-size) |  修改 | 将默认值从 `20` MiB 修改为 `54` MiB，以兼容 TiKV 侧默认 Region 大小扩大为 `256` MiB 的调整，减小随着集群规模增大后 Region 个数过多带来的管理压力。 |
| TiKV  | [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-从-v408-版本开始引入)  | 修改 | 支持将 TiKV 配置项 `security.redact-info-log` 的值设置为 `marker`，使用标记符号 `‹ ›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。   |
| TiKV  | [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size)  | 修改 | 默认值从 `96` MiB 修改为 `256` MiB，减小随着集群规模增大后 Region 个数过多带来的管理压力。   |
| TiKV  | [`coprocessor.region-max-size`](/tikv-configuration-file.md#region-max-size)  | 修改 | 默认值从 `144` MiB 修改为 `384` MiB，以兼容 `coprocessor.region-split-size` 调整为 `256` MiB 的修改。   |
| TiKV  | [`backup.sst-max-size`](/tikv-configuration-file.md#sst-max-size)  | 修改 | 默认值从 `144` MiB 修改为 `384` MiB，以兼容 `coprocessor.region-max-size` 调整为 `384` MiB 的修改。   |
| TiFlash   | [`security.redact_info_log`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)  | 修改 | 支持将 TiFlash Server 配置项 `security.redact-info-log` 的值设置为 `marker`，使用标记符号 `‹ ›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。    |
| TiFlash   | [`security.redact-info-log`](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) | 修改 | 支持将 TiFlash Learner 配置项 `security.redact-info-log` 的值设置为 `marker`，使用标记符号 `‹ ›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。   |
|  BR  |  [`--allow-pitr-from-incremental`](/br/br-incremental-guide.md#使用限制)
) | 新增  |  控制增量备份和后续的日志备份是否兼容。默认值为 `true`，即增量备份兼容后续的日志备份。兼容的情况下，增量恢复开始前会对需要回放的 DDL 进行严格检查。 |

### 系统表

* 在系统表 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 和 [`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist) 中新增 `ROWS_AFFECTED` 字段，用于显示 DML 语句当前影响的数据行数。[#46889](https://github.com/pingcap/tidb/issues/46889) @[lcwangchao](https://github.com/lcwangchao) **tw@qiancai** <!--1903-->

### 其他

## 离线包变更

## 废弃功能

* 以下为计划将在未来版本中废弃的功能：

    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将被废弃。
    * TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 将被废弃。
    * 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。

## 改进提升

+ TiDB

    - TopN 算子支持数据落盘功能 [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1715-->
    - TiDB 支持 `WITH ROLLUP` 修饰符和 `GROUPING` 函数 [#42631](https://github.com/pingcap/tidb/issues/42631) @[Arenatlx](https://github.com/Arenatlx) **tw@Oreoxmt** <!--1714-->
    - 系统变量 [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso-从-v830-版本开始引入) 增加全局作用域 [#55022](https://github.com/pingcap/tidb/issues/55022) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1857-->
    - GC（垃圾回收）支持并发 Delete Range（删除区间）以提升处理效率，可以通过 [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-从-v50-版本开始引入) 控制并发线程数 [#54570](https://github.com/pingcap/tidb/issues/54570) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1890-->

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

        - 在第一次进行按时间点恢复 (PITR) 前，新增对全量备份是否存在的检查；如果未找到全量备份，会终止恢复并返回错误 [#54418](https://github.com/pingcap/tidb/issues/54418) @[Leavrth](https://github.com/Leavrth) **tw@qiancai** <!--1915-->
        - 在恢复快照备份的数据之前，新增对 TiKV 和 TiFlash 是否有足够的磁盘空间的检查；如果空间不足，会终止恢复并返回错误 [#54316](https://github.com/pingcap/tidb/issues/54316) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1890-->
        - 在 TiKV 下载每个 SST 文件之前，新增对 TiKV 是否有足够的磁盘空间的检查；如果空间不足，会终止恢复并返回错误 [#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1890-->
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
