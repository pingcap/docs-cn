---
title: TiDB 8.5.6 Release Notes
summary: 了解 TiDB 8.5.6 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.6 Release Notes

发版日期：2026 年 4 月 14 日

TiDB 版本：8.5.6

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://pingkai.cn/download#tidb-community)

## 新功能

### 性能

- 外键检查支持使用共享锁 [#66154](https://github.com/pingcap/tidb/issues/66154) @[you06](https://github.com/you06)

    在悲观事务中，当对带有外键约束的子表执行 `INSERT` 或 `UPDATE` 时，外键检查默认会对父表中的对应行加排他锁。在子表高并发写入的场景下，如果大量事务访问相同的父表行，可能出现较严重的锁冲突。

    从 v8.5.6 起，你可以将系统变量 [`tidb_foreign_key_check_in_shared_lock`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_foreign_key_check_in_shared_lock-从-v856-版本开始引入) 设置为 `ON`，使外键检查在父表上使用共享锁，从而降低锁冲突，提升子表并发写入性能。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/foreign-key#锁)。

### 稳定性

- 为资源管控的后台任务设置资源上限的特性成为正式功能 (GA) [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv)

    TiDB 资源管控能够识别并降低后台任务的运行优先级。在某些场景下，即使有空闲资源，用户也希望后台任务的资源消耗能够保持在较低水平。从 v8.4.0 开始，你可以使用参数 `UTILIZATION_LIMIT` 为资源管控的后台任务设置最大资源使用百分比，从而将每个节点所有后台任务的总使用量控制在该限制以内。该功能可以让你精细控制后台任务的资源占用，进一步提升集群稳定性。

    在 v8.5.6 中，该功能成为正式功能 (GA)。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/tidb-resource-control-background-tasks)。

### 可观测性

- 支持多维度、多粒度定义慢查询日志的触发规则 [#62959](https://github.com/pingcap/tidb/issues/62959), [#64010](https://github.com/pingcap/tidb/issues/64010) @[zimulala](https://github.com/zimulala)

    在 v8.5.6 之前，TiDB 定位慢查询语句的主要方法是设置系统变量 [`tidb_slow_log_threshold`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_slow_log_threshold)，该机制触发慢查询日志的控制粒度粗（整个实例级别全局控制，不支持会话和 SQL 级别精细化控制）、触发条件仅执行时间 (`Query_time`) 一种，无法满足复杂场景慢查询日志抓取以精细化定位问题的需求。

    从 v8.5.6 起，TiDB 增强了慢查询日志的控制能力。你可以使用 [`tidb_slow_log_rules`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_slow_log_rules-从-v856-版本开始引入) 系统变量在实例、会话、SQL 级别定义多维度（如 `Query_time`、`Digest`、`Mem_max`、`KV_total`）的慢查询日志输出规则，使用 [`tidb_slow_log_max_per_sec`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_slow_log_max_per_sec-从-v856-版本开始引入) 系统变量限制每秒的日志输出数量，并通过 [`WRITE_SLOW_LOG`](https://docs.pingcap.com/zh/tidb/v8.5/optimizer-hints) Hint 强制记录指定 SQL 的慢查询日志，从而实现对慢查询日志更灵活的精细化控制。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/identify-slow-queries)。

- TiDB Dashboard 的 Top SQL 页面支持收集和展示 TiKV 网络流量和逻辑 I/O 指标 [#62916](https://github.com/pingcap/tidb/issues/62916) @[yibin87](https://github.com/yibin87)

    在之前的版本中，TiDB Dashboard 在识别 Top SQL 时仅基于 CPU 相关指标，在复杂场景下难以从网络或存储访问角度定位性能瓶颈。

    从 v8.5.6 起，你可以在 Top SQL 设置中打开 **TiKV 网络 IO 采集（多维度）**开关，以查看 TiKV 节点的 `Network Bytes` 和 `Logical IO Bytes` 等指标，并可以按 `By Query`、`By Table`、`By DB` 或 `By Region` 维度进行聚合分析，从而更全面地定位资源消耗热点。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/top-sql)。

### SQL 功能

- 支持列级权限管理 [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf) @[fzzf678](https://github.com/fzzf678)

    在 v8.5.6 之前，TiDB 的权限控制仅覆盖数据库和表级别，不支持像 MySQL 那样对特定列授予或回收权限，因此无法限制用户访问表中的部分敏感列。

    从 v8.5.6 开始，TiDB 支持列级权限管理。你可以使用 `GRANT` 和 `REVOKE` 语句管理特定列的权限。TiDB 在查询处理和执行计划构建过程中会基于列级权限进行校验，从而实现更细粒度的访问控制，增强敏感数据隔离能力，并更好地支持最小权限原则。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/column-privilege-management)。

- 支持在 `FOR UPDATE OF` 子句中使用表别名 [#63035](https://github.com/pingcap/tidb/issues/63035) @[cryo-zd](https://github.com/cryo-zd)

    在 v8.5.6 之前，当 `SELECT ... FOR UPDATE OF <table>` 语句在加锁子句中引用表别名时，TiDB 可能无法正确解析该别名，即使别名是有效的，也会返回 `table not exists` 错误。

    从 v8.5.6 起，TiDB 支持在 `FOR UPDATE OF` 子句中使用表别名。TiDB 现在可以从 `FROM` 子句中正确解析加锁目标，包括使用别名的表，从而确保行锁按预期生效。这提升了与 MySQL 的兼容性，使 `SELECT ... FOR UPDATE OF` 语句在使用表别名的查询场景下更加稳定可靠。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/sql-statement-select)。

### 数据库管理

- 支持指定分布式执行框架 (Distributed eXecution Framework, DXF) 任务可使用的节点数量 [#58944](https://github.com/pingcap/tidb/issues/58944) @[tangenta](https://github.com/tangenta) @[D3Hunter](https://github.com/D3Hunter)

    在 v8.5.6 之前，TiDB 无法限制分布式执行框架任务可使用的节点数量。当需要控制分布式任务执行的资源使用时，TiDB 没有提供专门的选项来约束最大节点数。

    从 v8.5.6 开始，TiDB 引入了 `tidb_max_dist_task_nodes` 系统变量，用于指定分布式执行框架任务可使用的 TiDB 节点最大数量，从而实现更好的资源控制，并支持基于工作负载的调优。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_max_dist_task_nodes-从-v856-版本开始引入)。

### 数据迁移

- 将 sync-diff-inspector 从 `pingcap/tidb-tools` 迁移至 `pingcap/tiflow` 代码仓库 [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh)

## 兼容性变更

对于新部署的 TiDB v8.5.5 集群（即不是从早于 v8.5.4 的版本升级而来的集群），你可以平滑升级到 v8.5.6。v8.5.6 的大多数变更对常规升级是安全的，但仍包含若干 MySQL 兼容性变更、系统变量变更、配置参数变更以及废弃功能。在升级前，请务必仔细阅读本节内容。

### MySQL 兼容性

- 从 v8.5.6 开始，TiDB 支持兼容 MySQL 的列级权限管理机制。你可以在表级别为指定列授予或回收 `SELECT`、`INSERT`、`UPDATE`、`REFERENCES` 权限。更多信息参见[列级权限管理](https://docs.pingcap.com/zh/tidb/v8.5/column-privilege-management)。
- 从 v8.5.6 开始，TiDB 支持在 `FOR UPDATE OF` 子句中使用表别名。为保持向后兼容性，在定义了别名的情况下，你仍然可以引用基础表名，但这会触发一条推荐使用显式别名的警告。更多信息参见 [`SELECT`](https://docs.pingcap.com/zh/tidb/v8.5/sql-statement-select) 文档。
- 从 v8.5.6 开始，Dumpling 已适配 MySQL 8.4 更新后的二进制日志命名，支持从 MySQL 8.4 导出数据。[#53082](https://github.com/pingcap/tidb/issues/53082) @[dveeden](https://github.com/dveeden)
- 从 v8.5.6 开始，TiDB Data Migration (DM) 新增对 MySQL 8.4 作为上游数据源的支持，适配该版本引入的新术语和版本检测逻辑。[#11020](https://github.com/pingcap/tiflow/issues/11020) @[dveeden](https://github.com/dveeden)

### 系统变量

| 变量名  | 修改类型    | 描述 |
|--------|------------------------------|------|
| [`tidb_analyze_version`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_analyze_version-从-v510-版本开始引入) | 修改 | 从 v8.5.6 开始，统计信息版本 1 (`tidb_analyze_version = 1`) 已废弃，并将在未来的版本中移除。建议使用统计信息版本 2 (`tidb_analyze_version = 2`)。 |
| [`tidb_ignore_inlist_plan_digest`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_ignore_inlist_plan_digest-从-v760-版本开始引入) | 修改 | 默认值从 `OFF` 修改为 `ON`。默认值 `ON` 表示 TiDB 在生成执行计划摘要时，会忽略 `IN` 列表中的元素差异（包括元素数量的差异），并使用 `...` 代替 `IN` 列表中的元素。 |
| [`tidb_service_scope`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_service_scope-从-v740-版本开始引入)   | 修改  | 从 v8.5.6 开始，该变量的取值大小写不敏感。TiDB 会将输入值转换为小写形式进行存储和比较。 |
| [`InPacketBytes`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#inpacketbytes-从-v856-版本开始引入) | 新增 | 这个变量只做内部统计使用，对用户不可见。 |
| [`OutPacketBytes`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#outpacketbytes-从-v856-版本开始引入) | 新增 | 这个变量只做内部统计使用，对用户不可见。 |
| [`tidb_foreign_key_check_in_shared_lock`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_foreign_key_check_in_shared_lock-从-v856-版本开始引入) | 新增 | 用于控制在悲观事务中，外键约束检查对父表中的行加锁时是否使用共享锁（而非排他锁）。默认值为 `OFF`，代表默认使用排他锁。 |
| [`tidb_max_dist_task_nodes`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_max_dist_task_nodes-从-v856-版本开始引入)  | 新增 | 用于定义分布式框架任务可使用的 TiDB 节点数上限。默认值为 `-1`，表示启用自动模式。在自动模式下，TiDB 将按照 `min(3, tikv_nodes / 3)` 动态计算该值，其中 `tikv_nodes` 表示集群中 TiKV 节点的数量。 |
| [`tidb_opt_join_reorder_through_sel`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_opt_join_reorder_through_sel-从-v856-版本开始引入)  | 新增 | 用于提升部分多表 JOIN 查询的连接顺序优化 (Join Reorder) 效果。当该变量值为 `ON` 时，在满足安全条件的前提下，优化器会将多个连续 JOIN 之间的过滤条件 (`Selection`) 一并纳入连接顺序优化的候选范围。在重建 JOIN 树时，优化器会将这些条件下推至更合适的位置，从而使更多表参与连接顺序优化。 |
| [`tidb_opt_partial_ordered_index_for_topn`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_opt_partial_ordered_index_for_topn-从-v856-版本开始引入) | 新增 | 用于控制在 `ORDER BY ... LIMIT` 查询中是否启用基于索引部分有序性 (partial order) 的 TopN 优化。默认值为 `DISABLE`，表示关闭该优化。 |
| [`tidb_slow_log_max_per_sec`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_slow_log_max_per_sec-从-v856-版本开始引入)  | 新增 | 控制每个 TiDB 节点每秒打印的慢查询日志的数量上限。<ul><li>当值为 `0`（默认值）时，表示不限制每秒打印的慢查询日志数量。</li><li>当值大于 `0` 时，TiDB 每秒最多打印指定数量的慢查询日志，超过部分将被丢弃，不会写入慢查询日志文件。</li></ul>  |
| [`tidb_slow_log_rules`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_slow_log_rules-从-v856-版本开始引入)  | 新增 | 用于定义慢查询日志的触发规则，支持基于多维度指标的组合条件，实现更加灵活和精细化的日志记录控制。   |

### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV | [`gc.auto-compaction.mvcc-read-aware-enabled`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#mvcc-read-aware-enabled-从-v856-版本开始引入) | 新增 | 控制是否启用 MVCC-read-aware compaction。默认值为 `false`。 |
| TiKV | [`gc.auto-compaction.mvcc-read-weight`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#mvcc-read-weight-从-v856-版本开始引入) | 新增 | 在计算 Region 的压缩优先级分数时，对 MVCC 读取活动应用的权重乘数。默认值为 `3.0`。 |
| TiKV | [`gc.auto-compaction.mvcc-scan-threshold`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#mvcc-scan-threshold-从-v856-版本开始引入) | 新增 | 每次读取请求扫描的 MVCC 版本数量的最小值，用于将 Region 标记为 compaction 候选。默认值为 `1000`。 |
| TiKV | [`resource-metering.enable-network-io-collection`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#enable-network-io-collection-从-v856-版本开始引入) | 新增 | 控制是否在 [Top SQL](https://docs.pingcap.com/zh/tidb/v8.5/top-sql) 中额外采集 TiKV 网络流量和逻辑 I/O 信息。默认值为 `false`。 |
| TiCDC | [`sink.csv.output-field-header`](https://docs.pingcap.com/zh/tidb/v8.5/ticdc-csv#使用-csv) | 新增 | 控制 CSV 文件是否输出表头行。默认值为 `false`。仅适用于 TiCDC 新架构。 |

## 废弃功能

- 从 v8.5.6 开始，统计信息版本 1 (`tidb_analyze_version = 1`) 已废弃，并将在未来的版本中移除。建议使用统计信息版本 2 (`tidb_analyze_version = 2`)，并[将目前已有统计信息版本 1 的对象迁移至版本 2](https://docs.pingcap.com/zh/tidb/v8.5/statistics#切换统计信息版本)，以获得更准确的统计信息。
- 从 v8.5.6 开始，TiDB Lightning Web 界面已废弃，并将在 v8.5.7 中移除。该 Web UI 自 v8.4.0 起已无法正常构建。请改用 [CLI](https://docs.pingcap.com/zh/tidb/v8.5/tidb-lightning-overview) 或 [`IMPORT INTO`](https://docs.pingcap.com/zh/tidb/v8.5/sql-statement-import-into) 语句。如果这对你的工作流程产生影响，请在 [#67697](https://github.com/pingcap/tidb/issues/67697) 中反馈。

## 改进提升

+ TiDB

    - 改进包含 `IN` 条件且作用于索引前缀列的查询的执行计划选择。TiDB 现在可以使用 merge sort 在 `ORDER BY ... LIMIT` 查询中保持顺序，从而减少不必要的扫描并提升性能 [#63449](https://github.com/pingcap/tidb/issues/63449) [#34882](https://github.com/pingcap/tidb/issues/34882) @[time-and-fate](https://github.com/time-and-fate)
    - 将不可打印的预处理语句参数以十六进制的形式输出，从而提升慢查询日志的可读性 [#65383](https://github.com/pingcap/tidb/issues/65383) @[dveeden](https://github.com/dveeden)
    - 在 `mysql.tidb` 中新增 `cluster_id` 字段，使外部工具能够判断两个 TiDB 实例是否属于同一集群 [#59476](https://github.com/pingcap/tidb/issues/59476) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    - 新增 Load-based Compaction 机制，该机制可感知 MVCC 读取开销，并优先对读取开销较高的 Region 执行 Compaction 操作，以提升查询性能 [#19133](https://github.com/tikv/tikv/issues/19133) @[mittalrishabh](https://github.com/mittalrishabh)
    - 优化集群扩缩容过程中 stale range 的清理逻辑，不再通过 ingest SST 文件执行清理，而是直接删除过期 key，以降低对在线请求延迟的影响 [#18042](https://github.com/tikv/tikv/issues/18042) @[LykxSassinator](https://github.com/LykxSassinator)
    - 为 Top SQL 新增 TiKV 网络流量和逻辑 I/O 信息的采集支持，帮你更准确地诊断 SQL 性能问题 [#18815](https://github.com/tikv/tikv/issues/18815) @[yibin87](https://github.com/yibin87)

+ PD

    - 删除不存在的 label 时，返回 `404` 而非 `200` [#10089](https://github.com/tikv/pd/issues/10089) @[lhy1024](https://github.com/lhy1024)
    - 减少非必要的错误日志 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + TiDB Data Migration (DM)

        - 在 DM syncer 中新增外键因果依赖支持，确保多 worker 场景下行变更按照父表至子表的外键顺序执行 [#12350](https://github.com/pingcap/tiflow/issues/12350) @[OliverS929](https://github.com/OliverS929)

## 错误修复

+ TiDB

    - 修复从 `release-8.5-20250606-v8.5.2` 升级到上游 `release-8.5` 时可能跳过 PITR 元数据升级，并导致 PITR 操作失败的问题 [#66994](https://github.com/pingcap/tidb/issues/66994) @[fzzf678](https://github.com/fzzf678)
    - 修复在执行 `EXCHANGE PARTITION` 后，非聚簇分区表上的非唯一全局索引或可为空的唯一全局索引可能出现不一致并返回不完整结果的问题 [#65289](https://github.com/pingcap/tidb/issues/65289) @[mjonss](https://github.com/mjonss)
    - 修复 `KILL QUERY` 错误终止空闲连接的问题 [#65447](https://github.com/pingcap/tidb/issues/65447) @[gengliqi](https://github.com/gengliqi)
    - 修复设置 `tidb_service_scope` 时，其值未被正确转换为小写的问题 [#66749](https://github.com/pingcap/tidb/issues/66749) @[D3Hunter](https://github.com/D3Hunter)
    - 修复 TiDB 重启后无法正确显示亲和力表的问题 [#66284](https://github.com/pingcap/tidb/issues/66284) @[lcwangchao](https://github.com/lcwangchao)
    - 修复由于统计信息缓存 (Stats Cache) 未排除系统表，导致 Stats Healthy 监控指标显示不准确的问题 [#64080](https://github.com/pingcap/tidb/issues/64080) @[0xPoe](https://github.com/0xPoe)
    - 修复由于 `modify_count` 更新异常，导致统计信息可能无法及时刷新的问题 [#65426](https://github.com/pingcap/tidb/issues/65426) @[0xPoe](https://github.com/0xPoe)
    - 修复在悲观事务中，当首条语句使用公平锁 (Fair Locking) 模式加锁时，可能导致事务保活 (Keep Alive) 机制失效，进而引发事务被意外回滚的问题 [#66571](https://github.com/pingcap/tidb/issues/66571) @[MyonKeminta](https://github.com/MyonKeminta)

+ TiKV

    - 修复 crossbeam skiplist 存在内存泄漏的问题 [#19285](https://github.com/tikv/tikv/issues/19285) @[ekexium](https://github.com/ekexium)
    - 修复在某些情况下，分区表中非唯一列的全局索引可能不一致，并导致查询返回错误结果的问题 [#19262](https://github.com/tikv/tikv/issues/19262) @[mjonss](https://github.com/mjonss)
    - 修复 Coprocessor 快照获取卡住时，可能长时间占用统一读取池 (Unified Read Pool) 工作线程直至请求超时，进而延迟其他读请求的问题 [#18491](https://github.com/tikv/tikv/issues/18491) @[AndreMouche](https://github.com/AndreMouche)
    - 修复当 TiKV 节点磁盘写满时，Follower Read 可能持续阻塞的问题 [#19201](https://github.com/tikv/tikv/issues/19201) @[glorv](https://github.com/glorv)
    - 修复当 resolved-ts worker 繁忙时，resolved-ts 任务积压可能导致 OOM 的问题 [#18359](https://github.com/tikv/tikv/issues/18359) @[overvenus](https://github.com/overvenus)
    - 修复 Leader 迁移期间 Follower Read 可能出现长尾延迟的问题 [#18417](https://github.com/tikv/tikv/issues/18417) @[gengliqi](https://github.com/gengliqi)
    - 修复悲观事务中 prewrite 请求重试在极少数情况下影响数据一致性的风险 [#11187](https://github.com/tikv/tikv/issues/11187) @[wk989898](https://github.com/wk989898)

+ PD

    - 修复在 Merge Region 调度操作较多的场景下，执行 `DISTRIBUTE TABLE` 语句可能导致 panic 的问题 [#10293](https://github.com/tikv/pd/issues/10293) @[bufferflies](https://github.com/bufferflies)
    - 修复配置 Store Limit 后可能无法立即生效的问题 [#10108](https://github.com/tikv/pd/issues/10108) @[okJiang](https://github.com/okJiang)

+ TiFlash

    - 修复执行移除列 `NOT NULL` 约束的 DDL 后，可能导致 TiFlash 与 TiKV 数据不一致的问题 [#10680](https://github.com/pingcap/tiflash/issues/10680) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 Grafana 监控面板中 Raft throughput 指标数值可能异常偏大的问题 [#10701](https://github.com/pingcap/tiflash/issues/10701) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复开启 Runtime Filter 时，若 Join Key 数据类型不一致，可能导致 Join 结果不正确的问题 [#10699](https://github.com/pingcap/tiflash/issues/10699) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)

+ Tools

    + Backup & Restore (BR)

        - 修复 Log Backup 的 `flush_ts` 可能为 `0` 的问题 [#19406](https://github.com/tikv/tikv/issues/19406) @[YuJuncen](https://github.com/YuJuncen)
        - 修复在通过兼容 Amazon S3 的 API（使用 S3 风格凭证）访问 Google Cloud Storage 时，因缺少 `Content-Length` 请求头导致 BR 在分片上传过程中可能失败的问题 [#19352](https://github.com/tikv/tikv/issues/19352) @[Leavrth](https://github.com/Leavrth)
        - 修复 BR 的 `restore point` 可能长时间卡在 `waiting for schema info finishes reloading` 状态，并在 15 分钟后因超时而失败的问题 [#66110](https://github.com/pingcap/tidb/issues/66110) @[kennytm](https://github.com/kennytm)
        - 修复 BR 在恢复带有 `SHARD_ROW_ID_BITS`、`PRE_SPLIT_REGIONS` 和 `merge_option` 属性的表时，无法正确预分裂 Region 的问题 [#65060](https://github.com/pingcap/tidb/issues/65060) @[JoyC-dev](https://github.com/JoyC-dev)

    + TiCDC

        - 修复服务器重启后，changefeed 可能重复创建无效 dispatcher 的问题 [#4452](https://github.com/pingcap/ticdc/issues/4452) @[wlwilliamx](https://github.com/wlwilliamx)
        - 修复当上游 TiDB 版本为 v8.1.x 或更早版本时，TiCDC 无法正确同步表重命名操作的问题 [#4392](https://github.com/pingcap/ticdc/issues/4392) @[lidezhu](https://github.com/lidezhu)
        - 修复启用 TiCDC 时，TiKV 在数据扫描过程中可能崩溃的问题 [#19404](https://github.com/tikv/tikv/issues/19404) @[wk989898](https://github.com/wk989898)
        - 为 Azure Blob Storage 下游新增 Azure 托管标识 (Managed Identity) 认证支持，并修复云存储上传可能卡住的问题 [#3093](https://github.com/pingcap/ticdc/issues/3093) @[wlwilliamx](https://github.com/wlwilliamx)

    + TiDB Data Migration (DM)

        - 修复 DM 在上游 binlog 文件切换后全局 checkpoint 位置未推进的问题 [#12339](https://github.com/pingcap/tiflow/issues/12339) @[OliverS929](https://github.com/OliverS929)
        - 修复 DM 在安全模式下处理含外键约束表的更新时，在未修改主键或唯一键的情况下仍可能误触发外键级联并导致数据被错误删除的问题 [#12350](https://github.com/pingcap/tiflow/issues/12350) @[OliverS929](https://github.com/OliverS929)
        - 修复 DM validator 在处理 `UNSIGNED` 列时误报校验错误的问题 [#12178](https://github.com/pingcap/tiflow/issues/12178) @[OliverS929](https://github.com/OliverS929)
