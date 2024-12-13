---
title: TiDB 8.3.0 Release Notes
summary: 了解 TiDB 8.3.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.3.0 Release Notes

发版日期：2024 年 8 月 22 日

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
    <td> <a href="https://docs.pingcap.com/zh/tidb/v8.3/partitioned-table#全局索引">分区表全局索引（实验特性）</a></td>
    <td>全局索引能够有效提升对非分区列的检索效率，同时也解除了唯一键 (Unique Key) 必须要包含分区键 (Partition Key) 的限制，扩展了 TiDB 分区表的使用场景，也能够避免数据迁移可能遇到的部分应用改造工作。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.3/system-variables#tidb_opt_projection_push_down-从-v610-版本开始引入">默认允许将 <code>Projection</code> 算子下推到存储引擎</a></td>
    <td><code>Projection</code> 算子下推可以将负载分散到存储节点，同时减少节点间的数据传输。这有助于降低部分 SQL 的执行时间，提升数据库的整体性能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.3/statistics#收集部分列的统计信息">统计信息收集忽略不必要的列</a></td>
    <td>在保证优化器能够获取到必要信息的前提下，加快了统计信息收集的速度，提升统计信息的时效性，进而保证选择最优的执行计划，提升集群性能。同时也降低了系统开销，改善了资源利用率。</td>
  </tr>
  <tr>
    <td rowspan="1">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.3/tiproxy-overview">TiProxy 内置虚拟 IP 管理</a></td>
    <td>TiProxy 内置了虚拟 IP 管理功能，配置后支持自动切换虚拟 IP，而无需依赖外部平台或工具。这简化了 TiProxy 的部署，降低了数据库接入层的复杂度。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 性能

* 优化器默认允许将 `Projection` 算子下推到存储引擎 [#51876](https://github.com/pingcap/tidb/issues/51876) @[yibin87](https://github.com/yibin87)

    将 `Projection` 算子下推到存储引擎可以减少计算引擎和存储引擎之间的数据传输量，从而提升 SQL 执行效率。这在处理包含 [JSON 查询类函数](/functions-and-operators/json-functions/json-functions-search.md)或 [JSON 值属性类函数](/functions-and-operators/json-functions/json-functions-return.md) 的查询时尤其有效。从 v8.3.0 开始，TiDB 默认开启 `Projection` 算子下推功能，控制该功能的系统变量 [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-从-v610-版本开始引入) 的默认值从 `OFF` 修改为 `ON`。启用该功能后，优化器会自动将符合条件的 JSON 查询类函数、JSON 值属性类函数等下推到存储引擎。

    更多信息，请参考[用户文档](/system-variables.md#tidb_opt_projection_push_down-从-v610-版本开始引入)。

* 优化 KV（键值）请求的批处理策略 [#55206](https://github.com/pingcap/tidb/issues/55206) @[zyguan](https://github.com/zyguan)

    TiDB 通过向 TiKV 发送 KV 请求读取数据。将多个 KV 请求攒批并进行批处理，可以有效提高执行效率。在 v8.3.0 之前，TiDB 的批处理策略效率不高。从 v8.3.0 开始，TiDB 在现有的 KV 请求批处理策略基础上，引入更高效的策略。你可以通过配置项 [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-从-v830-版本开始引入) 设置不同的批处理策略，以适应不同的业务场景。

    更多信息，请参考[用户文档](/tidb-configuration-file.md#batch-policy-从-v830-版本开始引入)。

* TiFlash 新增 HashAgg 聚合计算模式，提升高 NDV 数据的聚合计算性能 [#9196](https://github.com/pingcap/tiflash/issues/9196) @[guo-shaoge](https://github.com/guo-shaoge)

    在 v8.3.0 之前，TiFlash 在 HashAgg 聚合计算中处理高 NDV (number of distinct values) 数据时，第一阶段的聚合计算效率较低。从 v8.3.0 开始，TiFlash 引入多种 HashAgg 聚合计算策略，以提升不同特征数据的聚合计算性能。你可以通过系统变量 [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入) 设置所需的 HashAgg 聚合计算策略。

    更多信息，请参考[用户文档](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入)。

* 统计信息收集忽略不必要的列 [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/Rustin170506)

    当优化器生成执行计划时，只需要部分列的统计信息，例如过滤条件上的列、连接键上的列、聚合目标用到的列。从 v8.3.0 起，TiDB 会持续观测 SQL 语句对列的使用历史，默认只收集有索引的列，以及被观测到的有必要收集统计信息的列。这将会提升统计信息的收集速度，避免不必要的资源浪费。

    从 v8.3.0 之前的版本升级到 v8.3.0 或更高版本时，TiDB 默认保留原有行为，即收集所有列的统计信息。如果要启用该功能，需要手动将系统变量 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 设置为 `PREDICATE`，新部署的集群默认开启该功能。

    对于随机查询比较多的偏分析型系统，可以将系统变量 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 设置为 `ALL` 来收集所有列的统计信息，以保证随机查询的性能。对于其余类型的系统，推荐保留 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 的默认设置 `PREDICATE`，只收集必要列的统计信息。

    更多信息，请参考[用户文档](/statistics.md#收集部分列的统计信息)。

* 提升部分系统表的查询性能 [#50305](https://github.com/pingcap/tidb/issues/50305) @[tangenta](https://github.com/tangenta)

    之前的版本中，当集群规模变大、表数量较多时，查询系统表性能较差。

    在 v8.0.0 优化了以下 4 个系统表的查询性能：

    - `INFORMATION_SCHEMA.TABLES`
    - `INFORMATION_SCHEMA.STATISTICS`
    - `INFORMATION_SCHEMA.KEY_COLUMN_USAGE`
    - `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`

  在 v8.3.0 版本优化了以下系统表的查询性能，相比 v8.2.0，性能有数倍的提升：

    - `INFORMATION_SCHEMA.CHECK_CONSTRAINTS`
    - `INFORMATION_SCHEMA.COLUMNS`
    - `INFORMATION_SCHEMA.PARTITIONS`
    - `INFORMATION_SCHEMA.SCHEMATA`
    - `INFORMATION_SCHEMA.SEQUENCES`
    - `INFORMATION_SCHEMA.TABLE_CONSTRAINTS`
    - `INFORMATION_SCHEMA.TIDB_CHECK_CONSTRAINTS`
    - `INFORMATION_SCHEMA.TiDB_INDEXES`
    - `INFORMATION_SCHEMA.TIDB_INDEX_USAGE`
    - `INFORMATION_SCHEMA.VIEWS`

* 分区表达式使用 `EXTRACT(YEAR_MONTH...)` 函数时，支持分区裁剪，提升查询性能 [#54209](https://github.com/pingcap/tidb/pull/54209) @[mjonss](https://github.com/mjonss)

    之前的版本中，当分区表达式使用 `EXTRACT(YEAR_MONTH...)` 函数时，不支持分区裁剪，导致查询性能较差。从 v8.3.0 开始，当分区表达式使用该函数时，支持分区裁剪，提升了查询性能。

    更多信息，请参考[用户文档](/partition-pruning.md#场景三)。

* 批量建表 (`CREATE TABLE`) 的性能提升了 1.4 倍，批量建库 (`CREATE DATABASE`) 的性能提升了 2.1 倍，批量加列 (`ADD COLUMN`) 的性能提升了 2 倍 [#54436](https://github.com/pingcap/tidb/issues/54436) @[D3Hunter](https://github.com/D3Hunter)

    v8.0.0 引入了系统变量 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)，用于在批量建表的场景中提升建表的性能。在 v8.3.0 中，通过 10 个 session 在单个库内并发提交建表的 DDL，相比 v8.2.0，性能有 1.4 倍的提升。

    在 v8.3.0 中，逻辑 DDL (General DDL) 在批量执行时的性能相比 v8.2.0 也均有提升，其中通过 10 个 session 并发批量建库 (`CREATE DATABASE`) 的性能相比 v8.1.0 提升了 19 倍，相比 v8.2.0 提升了 2.1 倍。10 个 session 对同个库内的多个表批量加列 (`ADD COLUMN`) 的性能相比 v8.1.0 提升了 10 倍，相比 v8.2.0 提升了 2 倍。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)。

* 分区表支持全局索引 (Global Index)（实验特性）[#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) @[Defined2014](https://github.com/Defined2014) @[jiyfhust](https://github.com/jiyfhust) @[L-maple](https://github.com/L-maple)

    之前版本的分区表，因为不支持全局索引有较多的限制，比如唯一键必须包含分区表达式中用到的所有列，如果查询条件不带分区键，查询时会扫描所有分区，导致性能较差。从 v7.6.0 开始，引入了系统变量 [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-从-v760-版本开始引入) 用于开启全局索引特性，但该功能当时处于开发中，不够完善，不建议开启。

    从 v8.3.0 开始，全局索引作为实验特性正式发布。你可通过关键字 `Global` 为分区表显式创建一个全局索引，从而去除分区表唯一建必须包含分区表达式中用到的所有列的限制，满足灵活的业务需求。同时基于全局索引也提升了非分区列的查询性能。

    更多信息，请参考[用户文档](/partitioned-table.md#全局索引)。

### 稳定性

* 支持以流式获取游标的结果集（实验特性）[#54526](https://github.com/pingcap/tidb/issues/54526) @[YangKeao](https://github.com/YangKeao)

    当应用代码通过 [Cursor Fetch](/develop/dev-guide-connection-parameters.md#使用-streamingresult-流式获取执行结果) 获取结果集时，TiDB 通常会先将完整结果保存至 TiDB 内存，再分批返回给客户端。如果结果集过大，可能会触发落盘临时将结果写入硬盘。

    从 v8.3.0 开始，如果将系统变量 [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入) 设置为 `ON`，TiDB 不再把所有数据读取到 TiDB 节点，而是会随着客户端的读取逐步将数据读到 TiDB 节点。在处理较大的结果集时，这将减少 TiDB 节点的内存使用，提升集群的稳定性。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入)。

* 增强 SQL 执行计划绑定 [#55280](https://github.com/pingcap/tidb/issues/55280) [#55343](https://github.com/pingcap/tidb/issues/55343) @[time-and-fate](https://github.com/time-and-fate)

    在 OLTP 负载环境中，绝大部分 SQL 的最优执行计划是固定不变的。对业务中的重要 SQL 实施执行计划绑定，可以降低执行计划变差的几率，提升系统稳定性。为了满足创建大量 SQL 执行计划绑定的场景需求，TiDB 对 SQL 绑定的能力和体验进行了增强，其中包括：

    - 用单条 SQL 语句从多个历史执行计划中创建 SQL 执行计划绑定，提升创建绑定的效率。
    - SQL 执行计划绑定支持更多的优化器提示，并优化了对复杂执行计划的转换方法，使得绑定能够更稳定地还原执行计划。

  更多信息，请参考[用户文档](/sql-plan-management.md)。

### 高可用

* TiProxy 内置虚拟 IP 管理功能 [#583](https://github.com/pingcap/tiproxy/issues/583) @[djshow832](https://github.com/djshow832)

    在 v8.3.0 之前，当使用主从模式以保证高可用性时，TiProxy 需要额外的组件管理虚拟 IP。从 v8.3.0 开始，TiProxy 内置虚拟 IP 管理功能。在主从模式下，当主节点发生切换时，新的主节点会自动绑定指定的虚拟 IP，确保客户端始终能通过虚拟 IP 连接到可用的 TiProxy。

    要启用虚拟 IP 管理功能，需要通过 TiProxy 配置项 [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip) 指定虚拟 IP 地址，并通过 [`ha.interface`](/tiproxy/tiproxy-configuration.md#interface) 指定绑定虚拟 IP 的网络接口。只有这两个配置项都设置时，TiProxy 实例才能绑定虚拟 IP。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。

### SQL 功能

* 支持将 `SELECT LOCK IN SHARE MODE` 升级为排它锁 [#54999](https://github.com/pingcap/tidb/issues/54999) @[cfzjywxk](https://github.com/cfzjywxk)

    TiDB 暂不支持 `SELECT LOCK IN SHARE MODE`。从 v8.3.0 开始，TiDB 支持将 `SELECT LOCK IN SHARE MODE` 升级为排它锁，实现对 `SELECT LOCK IN SHARE MODE` 语法的支持。你可以使用系统变量 [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-从-v830-版本开始引入) 控制是否启用该功能。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_shared_lock_promotion-从-v830-版本开始引入)。

### 可观测性

* 展示初始统计信息的加载进度 [#53564](https://github.com/pingcap/tidb/issues/53564) @[hawkingrei](https://github.com/hawkingrei) 

    TiDB 在启动时要加载基础统计信息，在表或者分区数量很多的情况下，该过程要耗费一定时间。当配置项 [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入) 设置为 `ON` 时，初始统计信息加载完成前，TiDB 不会对外提供服务。在这种情况下，你需要对加载过程进行观测，从而预估服务开启时间。

    从 v8.3.0 开始，TiDB 会在日志中分阶段打印初始统计信息的加载进度，以便了解运行情况。为了给外部工具提供格式化的结果，TiDB 增加了额外的[监控 API](/tidb-monitoring-api.md)，以便能够在启动阶段随时获取初始统计信息的加载进度。

* 添加 Request Unit (RU) 配置监控指标 [#8444](https://github.com/tikv/pd/issues/8444) @[nolouch](https://github.com/nolouch)

### 安全

* 增强 PD 日志脱敏 [#8305](https://github.com/tikv/pd/issues/8305) @[JmPotato](https://github.com/JmPotato)

    TiDB v8.0.0 增强了日志脱敏功能，支持控制是否使用 `‹ ›` 包裹 TiDB 日志中的用户数据。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理，从而提升日志脱敏功能的灵活性。在 v8.2.0 中，TiFlash 实现了类似的日志脱敏功能增强。

    在 v8.3.0 中，PD 实现了类似的日志脱敏功能增强。要使用该功能，可以将 PD 配置项 `security.redact-info-log` 的值设置为 `"marker"`。

    更多信息，请参考[用户文档](/log-redaction.md#pd-组件日志脱敏)。

* 增强 TiKV 日志脱敏 [#17206](https://github.com/tikv/tikv/issues/17206) @[lucasliang](https://github.com/LykxSassinator)

    TiDB v8.0.0 增强了日志脱敏功能，支持控制是否使用 `‹ ›` 包裹 TiDB 日志中的用户数据。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理，从而提升日志脱敏功能的灵活性。在 v8.2.0 中，TiFlash 实现了类似的日志脱敏功能增强。

    在 v8.3.0 中，TiKV 实现了类似的日志脱敏功能增强。要使用该功能，可以将 TiKV 配置项 `security.redact-info-log` 的值设置为 `"marker"`。

    更多信息，请参考[用户文档](/log-redaction.md#tikv-组件日志脱敏)。

### 数据迁移

* TiCDC 支持通过双向复制模式 (Bi-Directional Replication, BDR) 同步 DDL 语句 (GA) [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen) 

    从 v7.6.0 开始，TiCDC 支持在配置了双向复制的情况下同步 DDL 语句。以前，TiCDC 不支持双向复制 DDL 语句，因此要使用 TiCDC 双向复制必须将 DDL 语句在两个 TiDB 集群分别执行。有了该特性，在为一个集群分配 `PRIMARY` BDR role 之后，TiCDC 可以将该集群的 DDL 语句复制到 `SECONDARY` 集群。

    在 v8.3.0，该功能成为正式功能 (GA)。

    更多信息，请参考[用户文档](/ticdc/ticdc-bidirectional-replication.md)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.2.0 升级至当前版本 (v8.3.0) 所需兼容性变更信息。如果从 v8.1.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 为了避免命令错误使用，`pd-ctl` 取消了前缀匹配的机制，例如 `store remove-tombstone` 不能通过 `store remove` 来调用 [#8413](https://github.com/tikv/pd/issues/8413) @[lhy1024](https://github.com/lhy1024)

### 系统变量

| 变量名  | 修改类型    | 描述 |
|--------|------------------------------|------|
| [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)     | 修改   | 增加 SESSION 作用域。     |
| [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)    | 修改   | 增加 SESSION 作用域。     |
| [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-从-v50-版本开始引入) | 修改 | 从 v8.3.0 起，该变量可以控制[垃圾回收 (GC)](/garbage-collection-overview.md) 过程中 [Resolve Locks（清理锁）](/garbage-collection-overview.md#resolve-locks清理锁)和 [Delete Range（删除区间）](/garbage-collection-overview.md#delete-ranges删除区间)的并发线程数。在 v8.3.0 之前，该变量只能控制 Resolve Locks（清理锁）的线程数。|
| [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) | 修改 | 增加 GLOBAL 作用域。|
| [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-从-v610-版本开始引入) | 修改 | 增加 GLOBAL 作用域，变量值可以持久化到集群。经进一步的测试，默认值从 `OFF` 修改为 `ON`，即默认允许优化器将 `Projection` 算子下推到 TiKV。|
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入)  | 修改 | 取值范围修改为 `0` 或 `[536870912, 9223372036854775807]`，其中最小值为 `536870912` bytes（即 512 MiB），避免设置了过小的 cache size 导致性能下降。|
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) | 新增 | 控制 `ANALYZE TABLE` 语句的行为。将其设置为默认值 `PREDICATE` 表示仅收集 [predicate columns](/statistics.md#收集部分列的统计信息) 的统计信息；将其设置为 `ALL` 表示收集所有列的统计信息。 |
| [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入) | 新增 | 这个变量用于控制 [Cursor Fetch](/develop/dev-guide-connection-parameters.md#使用-streamingresult-流式获取执行结果) 功能的行为。|
| [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-从-v830-版本开始引入)      | 新增  | 控制是否启用共享锁升级为排他锁的功能。默认值为 `OFF`，表示不启用共享锁升级为排他锁的功能。  |
| [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入) | 新增 | 控制下推到 TiFlash 的两阶段或三阶段 HashAgg 在第一阶段采用哪种预聚合策略。 |

### 配置文件参数

| 配置文件           | 配置项                | 修改类型 | 描述                                 |
|----------------|--------------------|------|------------------------------------|
| TiDB | [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-从-v830-版本开始引入) | 新增 | 控制 TiDB 向 TiKV 发送请求时的批处理策略。 |
| PD   |  [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-从-v50-版本开始引入) |  修改 | 支持将 PD 配置项 `security.redact-info-log` 的值设置为 `"marker"`，使用标记符号 `‹ ›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。  |
| TiKV  | [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-从-v408-版本开始引入)  | 修改 | 支持将 TiKV 配置项 `security.redact-info-log` 的值设置为 `"marker"`，使用标记符号 `‹ ›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。   |
| TiFlash | [`security.redact-info-log`](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) | 修改 | 支持将 TiFlash Learner 配置项 `security.redact-info-log` 的值设置为 `"marker"`，使用标记符号 `‹ ›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。   |
| BR  |  [`--allow-pitr-from-incremental`](/br/br-incremental-guide.md#使用限制) | 新增  | 控制增量备份和后续的日志备份是否兼容。默认值为 `true`，即增量备份兼容后续的日志备份。兼容的情况下，增量恢复开始前会对需要回放的 DDL 进行严格检查。 |

### 系统表

* 在系统表 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 和 [`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist) 中新增 `ROWS_AFFECTED` 字段，用于显示 DML 语句当前影响的数据行数。[#46889](https://github.com/pingcap/tidb/issues/46889) @[lcwangchao](https://github.com/lcwangchao)

## 废弃功能

* 以下为从 v8.3.0 开始已废弃的功能：

    * 从 v7.5.0 开始，[TiDB Binlog](https://docs.pingcap.com/zh/tidb/v8.3/tidb-binlog-overview) 的数据同步功能被废弃。从 v8.3.0 开始，TiDB Binlog 被完全废弃，并计划在未来版本中移除。如需进行增量数据同步，请使用 [TiCDC](/ticdc/ticdc-overview.md)。如需按时间点恢复 (point-in-time recovery, PITR)，请使用 [PITR](/br/br-pitr-guide.md)。
    * 从 v8.3.0 开始，系统变量 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-从-v540-版本开始引入) 被废弃。TiDB 默认收集 [predicate columns](/glossary.md#predicate-columns) 的统计信息。更多信息，参见 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入)。

* 以下为计划将在未来版本中废弃的功能：

    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将被废弃。
    * TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 将被废弃。
    * 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)，用于控制 TiDB 是否支持并行 HashAgg 进行落盘。在未来版本中，系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) 将被废弃。
    * TiDB Lightning 参数 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 计划在未来版本中废弃，并在后续版本中删除。该参数将由 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。

* 以下为计划将在未来版本中移除的功能：

    * 从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 参数统一控制逻辑导入和物理导入模式的冲突检测策略。旧版冲突检测的参数 [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) 将在未来版本中被移除。

## 改进提升

+ TiDB

    - 支持 `SELECT ... STRAIGHT_JOIN ... USING ( ... )` 语句 [#54162](https://github.com/pingcap/tidb/issues/54162) @[dveeden](https://github.com/dveeden)
    - 支持为形如 `((idx_col_1 > 1) or (idx_col_1 = 1 and idx_col_2 > 10)) and ((idx_col_1 < 10) or (idx_col_1 = 10 and idx_col_2 < 20))` 的过滤条件构造更精准的索引访问 Range [#54337](https://github.com/pingcap/tidb/issues/54337) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    - 支持形如 `WHERE idx_col_1 IS NULL ORDER BY idx_col_2` 的 SQL 查询利用索引顺序避免额外排序操作 [#54188](https://github.com/pingcap/tidb/issues/54188) @[ari-e](https://github.com/ari-e)
    - 在系统表 `mysql.analyze_jobs` 中显示被 `ANALYZE` 过的索引 [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/Rustin170506)
    - `EXPLAIN` 语句支持应用 `tidb_redact_log`，并进一步优化了日志记录的处理逻辑 [#54565](https://github.com/pingcap/tidb/issues/54565) @[hawkingrei](https://github.com/hawkingrei)
    - 支持在多值索引的 `IndexRangeScan` 上生成 `Selection`，以提高查询效率 [#54876](https://github.com/pingcap/tidb/issues/54876) @[time-and-fate](https://github.com/time-and-fate)
    - 支持在设定的自动 `ANALYZE` 时间窗口外终止正在执行的自动 `ANALYZE` 任务 [#55283](https://github.com/pingcap/tidb/issues/55283) @[hawkingrei](https://github.com/hawkingrei)
    - 当某个统计信息完全由 TopN 构成，且对应表的统计信息中修改行数不为 0 时，对于未命中 TopN 的等值条件，估算结果从 0 调整为 1 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - TopN 算子支持数据落盘功能 [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - TiDB 节点支持执行包含 `WITH ROLLUP` 修饰符和 `GROUPING` 函数的查询 [#42631](https://github.com/pingcap/tidb/issues/42631) @[Arenatlx](https://github.com/Arenatlx)
    - 系统变量 [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) 增加全局 (GLOBAL) 作用域 [#55022](https://github.com/pingcap/tidb/issues/55022) @[cfzjywxk](https://github.com/cfzjywxk)
    - GC（垃圾回收）支持并发 Delete Range（删除区间）以提升处理效率，可以通过 [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-从-v50-版本开始引入) 控制并发线程数 [#54570](https://github.com/pingcap/tidb/issues/54570) @[ekexium](https://github.com/ekexium)
    - 提升批量 DML 执行方式 (`tidb_dml_type = "bulk"`) 的性能 [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium)
    - 提升 schema 信息缓存相关接口 `SchemaByID` 的性能 [#54074](https://github.com/pingcap/tidb/issues/54074) @[ywqzzy](https://github.com/ywqzzy)
    - 提升 schema 信息缓存开启时部分系统表的查询性能 [#50305](https://github.com/pingcap/tidb/issues/50305) @[tangenta](https://github.com/tangenta)
    - 优化添加唯一索引时冲突键的报错信息 [#53004](https://github.com/pingcap/tidb/issues/53004) @[lance6716](https://github.com/lance6716)

+ PD

    - 支持通过 `pd-ctl` 修改 `evict-leader-scheduler` 的 `batch` 配置，以提升驱逐 Leader 的速度 [#8265](https://github.com/tikv/pd/issues/8265) @[rleungx](https://github.com/rleungx)
    - Grafana 上的 **Cluster > Label distribution** 面板新增 `store_id` 监控指标，用于显示不同 label 对应的 store ID [#8337](https://github.com/tikv/pd/issues/8337) @[HuSharp](https://github.com/HuSharp)
    - 当指定的资源组不存在时，支持回退到默认资源组 [#8388](https://github.com/tikv/pd/issues/8388) @[JmPotato](https://github.com/JmPotato)
    - 在 `pd-ctl` 的 `region` 命令输出的 Region 信息中，新增 `approximate_kv_size` 字段 [#8412](https://github.com/tikv/pd/issues/8412) @[zeminzhou](https://github.com/zeminzhou)
    - 优化调用 PD API 删除 TTL 配置时的输出信息 [#8450](https://github.com/tikv/pd/issues/8450) @[lhy1024](https://github.com/lhy1024)
    - 优化大查询读请求消耗 RU (Request Unit) 的行为，以减少对其他请求的影响 [#8457](https://github.com/tikv/pd/issues/8457) @[nolouch](https://github.com/nolouch)
    - 优化 PD 微服务设置错误时返回的错误信息 [#52912](https://github.com/pingcap/tidb/issues/52912) @[rleungx](https://github.com/rleungx)
    - PD 微服务新增 `--name` 启动参数，以便部署时更精确地显示服务名称 [#7995](https://github.com/tikv/pd/issues/7995) @[HuSharp](https://github.com/HuSharp)
    - 支持通过 Region 数量动态调整 `PatrolRegionScanLimit`，以减少扫描 Region 所需的时间 [#7963](https://github.com/tikv/pd/issues/7963) @[lhy1024](https://github.com/lhy1024)

+ TiKV

    - 优化 `async-io` 下写 Raft 日志的攒批策略，减少对磁盘 I/O 带宽资源的使用 [#16907](https://github.com/tikv/tikv/issues/16907) @[LykxSassinator](https://github.com/LykxSassinator)
    - 重新设计了 TiCDC 的 delegate 和 downstream 模块以更好地支持 Region 局部订阅 [#16362](https://github.com/tikv/tikv/issues/16362) @[hicqu](https://github.com/hicqu)
    - 减少单个慢日志的大小 [#17294](https://github.com/tikv/tikv/issues/17294) @[Connor1996](https://github.com/Connor1996)
    - 增加监控指标 `min safe ts` [#17307](https://github.com/tikv/tikv/issues/17307) @[mittalrishabh](https://github.com/mittalrishabh)
    - 减少 peer message channel 的内存使用 [#16229](https://github.com/tikv/tikv/issues/16229) @[Connor1996](https://github.com/Connor1996)

+ TiFlash

    - 支持生成 SVG 格式的堆内存分析结果 [#9320](https://github.com/pingcap/tiflash/issues/9320) @[CalvinNeo](https://github.com/CalvinNeo)

+ Tools

    + Backup & Restore (BR)

        - 在第一次进行按时间点恢复 (Point-in-time recovery, PITR) 前，新增对全量备份是否存在的检查；如果未找到全量备份，会终止恢复并返回错误 [#54418](https://github.com/pingcap/tidb/issues/54418) @[Leavrth](https://github.com/Leavrth)
        - 在恢复快照备份的数据之前，新增对 TiKV 和 TiFlash 是否有足够的磁盘空间的检查；如果空间不足，会终止恢复并返回错误 [#54316](https://github.com/pingcap/tidb/issues/54316) @[RidRisR](https://github.com/RidRisR)
        - 在 TiKV 下载每个 SST 文件之前，新增对 TiKV 是否有足够的磁盘空间的检查；如果空间不足，会终止恢复并返回错误 [#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR)
        - 支持通过环境变量设置阿里云访问身份 [#45551](https://github.com/pingcap/tidb/issues/45551) @[RidRisR](https://github.com/RidRisR)
        - 使用 BR 进行备份恢复时，会根据 BR 进程的可用内存自动设置环境变量 `GOMEMLIMIT`，避免出现 OOM [#53777](https://github.com/pingcap/tidb/issues/53777) @[Leavrth](https://github.com/Leavrth)
        - 使增量备份兼容按时间点恢复 (PITR) [#54474](https://github.com/pingcap/tidb/issues/54474) @[3pointer](https://github.com/3pointer)
        - 支持备份和恢复 `mysql.column_stats_usage` 表 [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/Rustin170506)

## 错误修复

+ TiDB

    - 通过重置 `PipelinedWindow` 的 `Open` 方法中的参数，修复当 `PipelinedWindow` 作为 apply 的子节点使用时，由于重复的打开和关闭操作导致重用之前的参数值而发生的意外错误 [#53600](https://github.com/pingcap/tidb/issues/53600) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复由于查询超出 `tidb_mem_quota_query` 设定的内存使用限制，导致终止查询时可能卡住的问题 [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - 修复 HashAgg 算子在并行计算过程中因落盘导致查询结果不正确的问题 [#55290](https://github.com/pingcap/tidb/issues/55290) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复从 `YEAR` 转换为 JSON 格式时 `JSON_TYPE` 错误的问题 [#54494](https://github.com/pingcap/tidb/issues/54494) @[YangKeao](https://github.com/YangKeao)
    - 修复系统变量 `tidb_schema_cache_size` 的取值范围错误的问题 [#54034](https://github.com/pingcap/tidb/issues/54034) @[lilinghai](https://github.com/lilinghai)
    - 修复当分区表达式为 `EXTRACT(YEAR FROM col)` 时没有分区裁剪的问题 [#54210](https://github.com/pingcap/tidb/issues/54210) @[mjonss](https://github.com/mjonss)
    - 修复表较多的情况下 `FLASHBACK DATABASE` 失败的问题 [#54415](https://github.com/pingcap/tidb/issues/54415) @[lance6716](https://github.com/lance6716)
    - 修复库较多的情况下 `FLASHBACK DATABASE` 死循环的问题 [#54915](https://github.com/pingcap/tidb/issues/54915) @[lance6716](https://github.com/lance6716)
    - 修复使用索引加速模式添加索引可能失败的问题 [#54568](https://github.com/pingcap/tidb/issues/54568) @[lance6716](https://github.com/lance6716)
    - 修复 `ADMIN CANCEL DDL JOBS` 可能导致 DDL 失败的问题 [#54687](https://github.com/pingcap/tidb/issues/54687) @[lance6716](https://github.com/lance6716)
    - 修复来自 DM 同步的表超过索引列最大长度 `max-index-length` 时，同步失败的问题 [#55138](https://github.com/pingcap/tidb/issues/55138) @[lance6716](https://github.com/lance6716)
    - 修复开启 `tidb_enable_inl_join_inner_multi_pattern` 时，执行 SQL 语句可能报错 `runtime error: index out of range` 的问题 [#54535](https://github.com/pingcap/tidb/issues/54535) @[joechenrh](https://github.com/joechenrh)
    - 修复 TiDB 在统计信息初始化的过程中，无法通过 <kbd>Control</kbd>+<kbd>C</kbd> 的方式退出 TiDB 的问题 [#54589](https://github.com/pingcap/tidb/issues/54589) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `INL_MERGE_JOIN` Optimizer Hint 返回错误结果的问题，将其废弃 [#54064](https://github.com/pingcap/tidb/issues/54064) @[AilinKid](https://github.com/AilinKid)
    - 修复关联子查询中包含 `WITH ROLLUP` 时 TiDB 可能 panic 并报错 `runtime error: index out of range` 的问题 [#54983](https://github.com/pingcap/tidb/issues/54983) @[AilinKid](https://github.com/AilinKid)
    - 修复当 SQL 查询的过滤条件中包含虚拟列，且执行条件中包含 `UnionScan` 时，谓词无法正常下推的问题 [#54870](https://github.com/pingcap/tidb/issues/54870) @[qw4990](https://github.com/qw4990)
    - 修复开启 `tidb_enable_inl_join_inner_multi_pattern` 时，执行 SQL 语句可能报错 `runtime error: invalid memory address or nil pointer dereference` 的问题 [#55169](https://github.com/pingcap/tidb/issues/55169) @[hawkingrei](https://github.com/hawkingrei)
    - 修复包含 `UNION` 的查询语句可能返回错误结果的问题 [#52985](https://github.com/pingcap/tidb/issues/52985) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复 `mysql.stats_histograms` 表的 `tot_col_size` 列可能为负数的潜在风险 [#55126](https://github.com/pingcap/tidb/issues/55126) @[qw4990](https://github.com/qw4990)
    - 修复 `columnEvaluator` 无法识别输入 chunk 中的列引用，导致执行 SQL 报错 `runtime error: index out of range` 的问题 [#53713](https://github.com/pingcap/tidb/issues/53713) @[AilinKid](https://github.com/AilinKid)
    - 修复 `STATS_EXTENDED` 变成保留关键字的问题 [#39573](https://github.com/pingcap/tidb/issues/39573) @[wddevries](https://github.com/wddevries)
    - 修复 `tidb_low_resolution` 开启时，`select for update` 可以被执行的问题 [#54684](https://github.com/pingcap/tidb/issues/54684) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复 `tidb_redact_log` 开启时，内部 SQL 在慢日志里无法显示的问题 [#54190](https://github.com/pingcap/tidb/issues/54190) @[lcwangchao](https://github.com/lcwangchao)
    - 修复事务占用的内存可能被多次重复统计的问题 [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - 修复使用 `SHOW WARNINGS;` 获取警告时可能导致 panic 的问题 [#48756](https://github.com/pingcap/tidb/issues/48756) @[xhebox](https://github.com/xhebox)
    - 修复加载索引统计信息可能会造成内存泄漏的问题 [#54022](https://github.com/pingcap/tidb/issues/54022) @[hi-rustin](https://github.com/Rustin170506)
    - 修复当排序规则为 `utf8_bin` 或 `utf8mb4_bin` 时意外消除 `LENGTH()` 条件的错误 [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    - 修复统计数据在遇到主键重复时没有更新 `stats_history` 表的问题 [#47539](https://github.com/pingcap/tidb/issues/47539) @[Defined2014](https://github.com/Defined2014)
    - 修复递归 CTE 查询可能导致无效指针的问题 [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - 修复某些连接在握手完成之前退出导致 Grafana 监控指标中的连接数 (Connection Count) 不正确的问题 [#54428](https://github.com/pingcap/tidb/issues/54428) @[YangKeao](https://github.com/YangKeao)
    - 修复使用 TiProxy 和资源组 (Resource Group) 功能时，每个资源组的连接数 (Connection Count) 显示不正确的问题 [#54545](https://github.com/pingcap/tidb/issues/54545) @[YangKeao](https://github.com/YangKeao)
    - 修复当查询包含非关联子查询和 `LIMIT` 子句时，列剪裁可能不完善导致计划不优的问题 [#54213](https://github.com/pingcap/tidb/issues/54213) @[qw4990](https://github.com/qw4990)
    - 修复针对 `SELECT ... FOR UPDATE` 复用了错误点查询计划的问题 [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)
    - 修复当第一个参数是 `month` 并且第二个参数是负数时，`TIMESTAMPADD()` 函数会进入无限循环的问题 [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复慢日志中内部语句中的 SQL 默认被脱敏为空的问题 [#54190](https://github.com/pingcap/tidb/issues/54190) [#52743](https://github.com/pingcap/tidb/issues/52743) [#53264](https://github.com/pingcap/tidb/issues/53264) @[lcwangchao](https://github.com/lcwangchao)
    - 修复可以生成 `_tidb_rowid` 的点查 (`PointGet`) 执行计划的问题 [#54583](https://github.com/pingcap/tidb/issues/54583) @[Defined2014](https://github.com/Defined2014)
    - 修复从 v7.1 升级后 `SHOW IMPORT JOBS` 报错 `Unknown column 'summary'` 的问题 [#54241](https://github.com/pingcap/tidb/issues/54241) @[tangenta](https://github.com/tangenta)
    - 修复当视图定义中使用子查询作为列定义时，通过 `information_schema.columns` 获取列信息返回告警 Warning 1356 的问题 [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    - 修复可以创建非严格自增的 RANGE 分区表的问题 [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - 修复当 SQL 异常中断时，`INDEX_HASH_JOIN` 无法正常退出的问题 [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - 修复使用分布式框架添加索引期间出现网络分区可能导致数据索引不一致的问题 [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)

+ PD

    - 修复将角色 (role) 绑定到资源组时未报错的问题 [#54417](https://github.com/pingcap/tidb/issues/54417) @[JmPotato](https://github.com/JmPotato)
    - 修复资源组在请求 token 超过 500 ms 时遇到超出配额限制的问题 [#8349](https://github.com/tikv/pd/issues/8349) @[nolouch](https://github.com/nolouch)
    - 修复 `INFORMATION_SCHEMA.RUNAWAY_WATCHES` 表中时间类型不正确的问题 [#54770](https://github.com/pingcap/tidb/issues/54770) @[HuSharp](https://github.com/HuSharp)
    - 修复资源组 (Resource Group) 在高并发场景下无法有效限制资源使用的问题 [#8435](https://github.com/tikv/pd/issues/8435) @[nolouch](https://github.com/nolouch)
    - 修复获取表属性时错误调用 PD API 的问题 [#55188](https://github.com/pingcap/tidb/issues/55188) @[JmPotato](https://github.com/JmPotato)
    - 修复开启 `scheduling` 微服务后，扩缩容进度显示错误的问题 [#8331](https://github.com/tikv/pd/issues/8331) @[rleungx](https://github.com/rleungx)
    - 修复加密管理器在使用前未初始化的问题 [#8384](https://github.com/tikv/pd/issues/8384) @[rleungx](https://github.com/rleungx)
    - 修复部分日志未脱敏的问题 [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    - 修复开启 PD 微服务时，重定向可能 panic 的问题 [#8406](https://github.com/tikv/pd/issues/8406) @[HuSharp](https://github.com/HuSharp)
    - 修复反复修改 `split-merge-interval` 的值（例如从 `1s` 改为 `1h`，再改回 `1s`）可能导致该配置不生效的问题 [#8404](https://github.com/tikv/pd/issues/8404) @[lhy1024](https://github.com/lhy1024)
    - 修复设置 `replication.strictly-match-label` 为 `true` 导致 TiFlash 启动失败的问题 [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    - 修复在 `ANALYZE` 大规模分区表时获取 TSO 慢导致 `ANALYZE` 性能下降的问题 [#8500](https://github.com/tikv/pd/issues/8500) @[rleungx](https://github.com/rleungx)
    - 修复了大规模集群下可能发生数据竞争的问题 [#8386](https://github.com/tikv/pd/issues/8386) @[rleungx](https://github.com/rleungx)
    - 修复 TiDB 在判断查询是否为 Runaway Queries 时，只统计了 Coprocessor 侧的时间消耗但未统计 TiDB 侧的时间消耗，导致一些查询未被识别为 Runaway Queries 的问题 [#51325](https://github.com/pingcap/tidb/issues/51325) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - 修复使用 `CAST()` 函数将字符串转换为带时区或非法字符的日期时间时，结果错误的问题 [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - 修复跨数据库对含空分区的分区表执行 `RENAME TABLE ... TO ...` 后，TiFlash 可能 panic 的问题 [#9132](https://github.com/pingcap/tiflash/issues/9132) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复开启延迟物化后，部分查询在执行时可能报列类型不匹配错误的问题 [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    - 修复开启延迟物化后，带有虚拟生成列的查询可能返回错误结果的问题 [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)
    - 修复将 TiFlash 中 SSL 证书配置项设置为空字符串会错误开启 TLS 并导致 TiFlash 启动失败的问题 [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复数据库创建后短时间内被删除时，TiFlash 可能 panic 的问题 [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 与任意 PD 之间发生网络分区（即网络连接断开），可能导致读请求超时报错的问题 [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在存算分离架构下，TiFlash 写节点可能重启失败的问题 [#9282](https://github.com/pingcap/tiflash/issues/9282) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在存算分离架构下，TiFlash 写节点的读快照可能没有被及时释放的问题 [#9298](https://github.com/pingcap/tiflash/issues/9298) @[JinheLin](https://github.com/JinheLin)

+ TiKV

    - 修复在清理旧 Region 时可能会误删数据的问题 [#17258](https://github.com/tikv/tikv/issues/17258) @[hbisheng](https://github.com/hbisheng)
    - 修复 Grafana TiKV 组件中的 `Ingestion picked level` 和 `Compaction Job Size(files)` 显示不正确的问题 [#15990](https://github.com/tikv/tikv/issues/15990) @[Connor1996](https://github.com/Connor1996)
    - 修复 `cancel_generating_snap` 错误地更新 `snap_tried_cnt` 导致 TiKV panic 的问题 [#17226](https://github.com/tikv/tikv/issues/17226) @[hbisheng](https://github.com/hbisheng)
    - 修复 `Ingest SST duration seconds` 统计信息说明错误的问题 [#17239](https://github.com/tikv/tikv/issues/17239) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复 CPU profiling flag 在出现错误时没有正确重置的问题 [#17234](https://github.com/tikv/tikv/issues/17234) @[Connor1996](https://github.com/Connor1996)
    - 修复早期版本（早于 v7.1）和之后的版本的 bloom filter 无法兼容的问题 [#17272](https://github.com/tikv/tikv/issues/17272) @[v01dstar](https://github.com/v01dstar)

+ Tools

    + Backup & Restore (BR)

        - 修复增量恢复过程中 `ADD INDEX`、`MODIFY COLUMN` 等需要回填的 DDL 可能无法正确恢复的问题 [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)
        - 修复备份恢复时进度条卡住的问题 [#54140](https://github.com/pingcap/tidb/issues/54140) @[Leavrth](https://github.com/Leavrth)
        - 修复备份恢复的断点路径在一些外部存储中不兼容的问题 [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 修复当下游 Kafka 无法访问时，Processor 可能卡住的问题 [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - 修复 schema tracker 无法正确处理 LIST 分区表导致 DM 报错的问题 [#11408](https://github.com/pingcap/tiflow/issues/11408) @[lance6716](https://github.com/lance6716)
        - 修复当索引长度超过 `max-index-length` 默认值时数据同步中断的问题 [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - 修复 DM 无法正确处理 `FAKE_ROTATE_EVENT` 的问题 [#11381](https://github.com/pingcap/tiflow/issues/11381) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复 TiDB Lightning 获取 keyspace 失败时输出的 `WARN` 日志可能引起用户混淆的问题 [#54232](https://github.com/pingcap/tidb/issues/54232) @[kennytm](https://github.com/kennytm)
        - 修复 TiDB Lightning 的 TLS 配置影响集群证书的问题 [#54172](https://github.com/pingcap/tidb/issues/54172) @[ei-sugimoto](https://github.com/ei-sugimoto)
        - 修复使用 TiDB Lightning 导入数据时报事务冲突的问题 [#49826](https://github.com/pingcap/tidb/issues/49826) @[lance6716](https://github.com/lance6716)
        - 修复导入大量库表时 checkpoint 文件过大导致性能下降的问题 [#55054](https://github.com/pingcap/tidb/issues/55054) @[D3Hunter](https://github.com/D3Hunter)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [ari-e](https://github.com/ari-e)
- [ei-sugimoto](https://github.com/ei-sugimoto)
- [HaoW30](https://github.com/HaoW30)
- [JackL9u](https://github.com/JackL9u)
- [michaelmdeng](https://github.com/michaelmdeng)
- [mittalrishabh](https://github.com/mittalrishabh)
- [qingfeng777](https://github.com/qingfeng777)
- [SandeepPadhi](https://github.com/SandeepPadhi)
- [yzhan1](https://github.com/yzhan1)
