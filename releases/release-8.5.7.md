---
title: TiDB 8.5.7 Release Notes
summary: 了解 TiDB 8.5.7 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.7 Release Notes

发版日期：2026 年 xx 月 xx 日

TiDB 版本：8.5.7

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup)

## 新功能

### 性能

* 支持基于 TiKV CPU 使用情况的热点 Region 调度，以提升读取负载均衡能力 [#5718](https://github.com/tikv/pd/issues/5718) [#19373](https://github.com/tikv/tikv/issues/19373) @[lhy1024](https://github.com/lhy1024) <!--2382--> <!--tw:qiancai-->

    在之前的版本中，热点 Region 调度器主要基于查询速率和字节吞吐量来平衡读取热点。在某些工作负载下，即使 QPS 和字节吞吐量看似均衡，TiKV 的 CPU 使用量仍可能不均匀，例如不同查询的 CPU 开销差异较大，或不同 TiKV 节点的性能特征不同。

    从 v8.5.7 起，TiKV 会在 store heartbeat 中上报热点 Region 的读取 CPU 使用量，PD 可以将 CPU 使用量作为读取热点 Region 调度的一个维度。借助这一机制，PD 能更准确地识别基于 CPU 的读取热点，并在各个 TiKV store 之间进行均衡。

    此外，PD 新增了与 CPU 相关的热点统计信息和调度器控制项，包括 [hot store statistics](https://docs.pingcap.com/zh/tidb/v8.5/pd-control#hot-read--write--store--history-start_time-end_time-key-value) 中的 `cpu-read-rate` 字段，以及 [`min-hot-cpu-rate` 和 `cpu-rate-rank-step-ratio`](https://docs.pingcap.com/zh/tidb/v8.5/pd-control#scheduler-config-balance-hot-region-scheduler) 调度器配置。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/troubleshoot-hot-spot-issues#scatter-read-hotspots)。

### 稳定性

* 支持限制 TiDB 实例中单个用户可建立的连接数 [#59203](https://github.com/pingcap/tidb/issues/59203) @[joccau](https://github.com/joccau) <!--2405--> <!--tw:lilin90-->

    从 v8.5.7 开始，你可以使用系统变量 `max_user_connections` 限制单个用户在单个 TiDB server 实例上可建立的最大连接数。这有助于防止某个用户过度消耗 [token](https://docs.pingcap.com/zh/tidb/v8.5/tidb-configuration-file#token-limit)，从而导致其他用户的请求响应出现延迟。

    此外，你也可以在 `CREATE USER` 和 `ALTER USER` 语句中使用 `WITH MAX_USER_CONNECTIONS N` 限制对应用户允许登录的最大连接数。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#max_user_connections-从-v857-版本开始引入)。

### SQL 功能

* 支持部分索引，以降低索引存储成本，减少 DML 维护开销 [#62664](https://github.com/pingcap/tidb/issues/62444) [#62761](https://github.com/pingcap/tidb/issues/62761) [#62758](https://github.com/pingcap/tidb/issues/62758) [#63447](https://github.com/pingcap/tidb/issues/63447) [#64344](https://github.com/pingcap/tidb/issues/64344) @[YangKeao](https://github.com/YangKeao) @[winoros](https://github.com/winoros) @[wjhuang2016](https://github.com/wjhuang2016) <!--21903--> <!--2270--> <!--tw:qiancai-->

    从 v8.5.7 起，TiDB 支持部分索引。部分索引仅为满足索引 `WHERE` 子句中谓词条件的行创建索引项。你可以通过 `CREATE INDEX ... WHERE ...`、`ALTER TABLE ... ADD INDEX ... WHERE ...`，或在 `CREATE TABLE` 中定义索引的方式创建部分索引。

    当你经常需要查询符合特定条件的部分行时，或者需要仅在特定条件下生效的唯一约束时，部分索引会非常有用。由于不满足谓词条件的行不会被写入索引，部分索引有助于节省索引存储空间，同时降低 `INSERT`、`UPDATE` 和 `DELETE` 操作期间的索引维护成本。

    为了更有效地使用部分索引，在定义部分索引时，建议使用与你常用查询的过滤条件相匹配的谓词。只有当查询中国的谓词与部分索引的谓词匹配或满足部分索引的谓词条件时，TiDB 才会选择使用部分索引。目前，部分索引谓词支持基本比较运算符（`=`、`!=`、`<`、`<=`、`>`、`>=`）、`IS NULL`、`IS NOT NULL`，以及带常量值的 `IN` 谓词。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/sql-statement-create-index/#部分索引-从-v857-开始引入)。

### 可观测性

* TiDB Dashboard 的 Top SQL 页面支持收集和展示 TiKV 网络流量和逻辑 I/O 指标 [#62916](https://github.com/pingcap/tidb/issues/62916) @[yibin87](https://github.com/yibin87) <!--tw:qiancai-->

    在之前的版本中，TiDB Dashboard 在识别 Top SQL 时仅基于 CPU 相关指标，在复杂场景下难以从网络或存储访问角度定位性能瓶颈。

    从 v8.5.7 起，你可以在 Top SQL 设置中打开 **TiKV 网络 IO 采集（多维度）**开关，以查看 TiKV 节点的 `Network Bytes` 和 `Logical IO Bytes` 等指标，并可以按 `By Query`、`By Table`、`By DB` 或 `By Region` 维度进行聚合分析，从而更全面地定位资源消耗热点。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/top-sql)。

### 数据迁移

* DM 支持静态一对一 schema/table 路由场景下的外键因果依赖 [#12350](https://github.com/pingcap/tiflow/issues/12350) @[OliverS929](https://github.com/OliverS929) <!--2427--> <!-- https://github.com/pingcap/tiflow/pull/12707 --> <!--tw:lilin90-->

    从 v8.5.7 开始，当 `foreign_key_checks=1` 且 `syncer.worker-count > 1` 时，DM 支持静态一对一 schema/table 路由场景下的外键因果依赖。

    在同步任务启动前，必须先在下游创建目标 schema 和外键定义。该功能不支持多对一或分片合并路由，不支持同步过程中的动态外键 DDL，不支持 `syncer.compact` 或 `syncer.multiple-rows` 等会改变 DML 语句边界的选项，也不支持在 safe mode 下同步修改主键或唯一键值的 `UPDATE` 语句。启用外键因果依赖后，DM 也不支持通过热更新方式修改 `worker-count`、`case-sensitive`、route rules、block-allow-list rules、binlog filter rules 或 `foreign_key_checks`。如需修改这些配置，请先停止任务，更新配置后再重新启动任务。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/dm-compatibility-catalog#外键-cascade-操作)。

* TiCDC 支持表路由 [#4655](https://github.com/pingcap/ticdc/issues/4655) [#4941](https://github.com/pingcap/ticdc/issues/4941) [#4702](https://github.com/pingcap/ticdc/issues/4702) @[3AceShowHand](https://github.com/3AceShowHand) <!--2471--><!--tw:qiancai-->

    从 v8.5.7 起，TiCDC 新架构支持表路由功能。你可以在 Changefeed 的 `sink.dispatchers` 配置中使用 `target-schema` 和 `target-table`，将上游表映射到指定的下游库名或表名。

    该功能适用于下游库表命名规范与上游不一致，或需要将多个源库同步到同一个目标库并保持目标表名唯一的场景。通过表路由，你可以为下游系统提供稳定且符合预期的目标库表名。

    该功能仅适用于 TiCDC 新架构。更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/ticdc-table-routing)。

## 兼容性变更

对于新部署的 TiDB v8.5.6 集群（即不是从早于 v8.5.5 的版本升级而来的集群），你可以平滑升级到 v8.5.7。v8.5.7 的大多数变更对常规升级是安全的，但本版本仍包含若干行为变更、MySQL 兼容性变更、系统变量变更、配置参数变更以及废弃功能。在升级前，请务必仔细阅读本节内容。

### 行为变更

* TiKV 现在默认会拒绝已确认无效的 `max_ts` 更新请求，而不再仅记录日志。此变更可以阻止无效时间戳更新，同时避免 TiKV panic，提升了安全性。如需保留此前仅记录日志的行为，请将 [`storage.max-ts.action-on-invalid-update`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#action-on-invalid-update-从-v857-版本开始引入) 设置为 `log` [#19755](https://github.com/tikv/tikv/issues/19755) @[ekexium](https://github.com/ekexium) <!-- component: tikv -->
* 从 v8.5.7 起，TiDB 默认启用[优化器修复控制项 `52869`](https://docs.pingcap.com/zh/tidb/v8.5/optimizer-fix-controls#52869-从-v810-版本开始引入)。该变更允许优化器在存在备选索引时自动考虑 `IndexMerge`，因此在某些情况下可能改变查询执行计划 [#26764](https://github.com/pingcap/tidb/issues/26764) @[time-and-fate](https://github.com/time-and-fate) <!--pr:<https://github.com/pingcap/docs-cn/pull/21744>;tw:qiancai-->

### MySQL 兼容性

* 支持解析横向派生表的 `LATERAL` 语法，以提升与 MySQL 8.0 的兼容性，支持包括用逗号连接、`CROSS JOIN LATERAL` 和 `INNER JOIN LATERAL` 等常见用法 <!--2432--><!--tw:qiancai-->

    当前，TiDB 仅支持解析 [`LATERAL` 派生表语法](https://docs.pingcap.com/zh/tidb/v8.5/lateral-derived-tables)，暂不支持执行使用该语法的查询。如果你尝试执行此类查询，TiDB 会返回错误。你可以在 issue [#40328](https://github.com/pingcap/tidb/issues/40328) 中跟踪该功能完整执行支持的进展。

* 支持在 `CREATE USER` 和 `ALTER USER` 中使用 `WITH MAX_USER_CONNECTIONS N`，以提升与 MySQL 的兼容性。TiDB 同时在 `mysql.user` 中新增 `max_user_connections` 列，并允许你使用 `max_user_connections` 系统变量控制单个用户在 TiDB server 实例上可建立的最大连接数。 <!--pr:<https://github.com/pingcap/docs-cn/pull/19898>;tw:lilin90-->

### 系统变量

| 变量名 | 修改类型 | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_telemetry`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_telemetry-从-v402-版本开始引入) | 废弃 | 从 v8.5.7 开始，TiDB 废弃该系统变量及 telemetry 功能。该变量仅为兼容性而保留，不再推荐使用。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21750>;tw:lilin90--> |
| [`tidb_auto_analyze_concurrency`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-从-v840-版本开始引入) | 修改 | 默认值从 `1` 修改为 `3`，加快统计信息收集任务的执行速度并提升自动 ANALYZE 效率。如果你的集群是从之前的版本升级而来的，升级后该变量的值保持不变。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21731>;tw:qiancai--> |
| [`tidb_auto_build_stats_concurrency`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_auto_build_stats_concurrency-从-v650-版本开始引入) | 修改 | 默认值从 `1` 修改为 `2`，以提升自动 `ANALYZE` 的默认性能。如果你的集群是从之前的版本升级而来的，升级后该变量的值保持不变。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21731>;tw:qiancai--> |
| [`tidb_sysproc_scan_concurrency`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_sysproc_scan_concurrency-从-v650-版本开始引入) | 修改 | 默认值从 `1` 修改为 `4`，以加快 TiDB 执行内部 SQL 语句时扫描操作的速度。如果你的集群是从之前的版本升级而来的，升级后该变量的值保持不变。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21731>;tw:qiancai--> |
| [`max_user_connections`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#max_user_connections-从-v857-版本开始引入) | 新增 | 用于控制单个用户在 TiDB server 实例上可建立的最大连接数。默认值为 `0`，表示不限制。如果该变量值超过 `max_connections`，TiDB 会使用 `max_connections` 作为实际限制。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21732>;tw:lilin90--> |
| [`performance_schema_session_connect_attrs_size`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#performance_schema_session_connect_attrs_size-从-v857-版本开始引入) | 新增 | 用于控制每个会话连接属性的总大小上限。默认值为 `4096` 字节。当大小超过该限制时，TiDB 会截断超出的属性，并新增 `_truncated` 来表示被截断的字节数。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21577>;tw:lilin90--> |
| [`tidb_enable_batch_query_region`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_batch_query_region-从-v857-版本开始引入) | 新增 | 用于控制 TiDB 是否通过 `QueryRegion` gRPC stream 向 PD 批量发起 Region 信息点查请求。默认值为 `OFF`。启用后，在某些场景下可以减少发送到 PD 的请求数量，并降低 PD leader 的 CPU 开销。 <!--pr:<https://github.com/pingcap/docs-cn/pull/20040>;tw:qiancai--> |
| [`tidb_enable_cache_prepare_stmt`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_cache_prepare_stmt-从-v857-版本开始引入) | 新增 | 用于控制是否缓存 `Prepare` 语句的结果。默认值为 `OFF`。目前该变量为实验特性，不建议在生产环境中启用。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21776/files>;tw:qiancai--> |
| [`tidb_enable_strict_not_null_check`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_strict_not_null_check-从-v857-版本开始引入) | 新增 | 用于控制当 `INSERT` 语句显式向 `NOT NULL` 列写入 `NULL` 值时，TiDB 是否执行严格校验。默认值为 `ON`。如果你的应用依赖此前写入隐式默认值的宽松行为，可以临时将该变量设置为 `OFF`，以降低升级兼容性风险。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21600>;tw:qiancai--> |
| [`tidb_opt_enable_alternative_logical_plans`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_opt_enable_alternative_logical_plans-从-v857-版本开始引入) | 新增 | 用于控制优化器是否在关联子查询去关联场景中额外构建一个“不去关联”的逻辑候选计划。默认值为 `OFF`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21775/files>;tw:qiancai--> |

### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`enable-telemetry`](https://docs.pingcap.com/zh/tidb/v8.5/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入) | 废弃 | 从 v8.5.7 开始，TiDB 废弃该配置项及 telemetry 功能。该配置项仅为兼容性而保留，不再推荐使用。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21750>;tw:lilin90--> |
| TiKV | [`backup.gcp-v2-enable`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#backupgcp-v2-enable-从-v857-版本开始引入) | 新增 | 用于控制 TiKV 在 GCS 全量备份与恢复中是否使用 `gcp_v2` 外部存储后端。默认值为 `true`。启用时，TiKV 使用 `gcp_v2`；关闭时，TiKV 使用旧版 GCS 实现。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21469>;tw:lilin90--> |
| TiKV | [`log-backup.gcp-v2-enable`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#log-backupgcp-v2-enable-从-v857-版本开始引入) | 新增 | 用于控制 TiKV 在 GCS 日志备份中是否使用 `gcp_v2` 外部存储后端。默认值为 `true`。启用时，TiKV 使用 `gcp_v2`；关闭时，TiKV 使用旧版 GCS 实现。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21469>;tw:lilin90--> |
| TiKV | [`resource-control.admission-max-delayed-count`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#admission-max-delayed-count-从-v857-版本开始引入) | 新增 | 用于指定 TiKV 在准入控制延迟队列中可保留的最大并发请求数（读写合计）。默认值为 `10000`。将该值设置为 `0` 表示并发延迟数不受限制。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-control.baseline-burst-pct`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#baseline-burst-pct-从-v857-版本开始引入) | 新增 | 用于指定资源组的历史 RU 基线之上可保留的余量百分比，超过该值后 TiKV 会认为该资源组超出基线。默认值为 `20.0`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-control.bg-compaction-pressure-threshold`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#bg-compaction-pressure-threshold-从-v857-版本开始引入) | 新增 | 用于指定开始对后台写 I/O 进行限流时的阈值，该阈值表示为 `storage.flow-control.soft-pending-compaction-bytes-limit` 的百分比。默认值为 `70.0`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-control.bg-cpu-throttle-threshold`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#bg-cpu-throttle-threshold-从-v857-版本开始引入) | 新增 | 用于指定开始对后台任务进行限流时的 CPU 使用率百分比阈值。默认值为 `60.0`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-control.bg-write-io-ceiling`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#bg-write-io-ceiling-从-v857-版本开始引入) | 新增 | 用于指定当 compaction 压力低于 `bg-compaction-pressure-threshold` 时，后台任务允许的最大写 I/O 速率。默认值为 `"100GB"`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-control.bg-write-io-floor`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#bg-write-io-floor-从-v857-版本开始引入) | 新增 | 用于指定即使在最大 compaction 压力下也能保证分配给后台任务的最小写 I/O 速率。默认值为 `"10MB"`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-control.enable-fair-scheduling`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#enable-fair-scheduling-从-v857-版本开始引入) | 新增 | 用于控制是否为读请求启用基于 RU 的两阶段公平调度。默认值为 `false`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-control.enable-read-admission-control`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#enable-read-admission-control-从-v857-版本开始引入) | 新增 | 用于控制是否为读请求启用准入控制。默认值为 `false`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-control.enable-write-admission-control`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#enable-write-admission-control-从-v857-版本开始引入) | 新增 | 用于控制是否为写请求启用准入控制。默认值为 `false`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-control.fg-cpu-throttle-threshold`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#fg-cpu-throttle-threshold-从-v857-版本开始引入) | 新增 | 用于指定完全激活前台流量保护时的 CPU 使用率百分比阈值。默认值为 `70.0`。该阈值必须大于 `bg-cpu-throttle-threshold`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-control.historical-usage-window-mins`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#historical-usage-window-mins-从-v857-版本开始引入) | 新增 | 用于指定 TiKV 计算各资源组历史 RU 基线的滑动时间窗口大小（单位：分钟）。默认值为 `15`。修改此配置后，需要重启 TiKV 才能生效。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21754/files>;tw:lilin90--> |
| TiKV | [`resource-metering.enable-network-io-collection`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#resource-meteringenable-network-io-collection-从-v857-版本开始引入) | 新增 | 用于控制 TiKV 除 CPU 数据外，是否还为 Top SQL 采集网络流量和逻辑 I/O 信息。默认值为 `false`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21717>;tw:qiancai--> |
| TiKV | [`storage.max-ts.action-on-invalid-update`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#action-on-invalid-update-从-v857-版本开始引入) | 新增 | 用于决定 TiKV 如何处理无效的 `max-ts` 更新请求。默认值为 `"error"`，表示当 TiKV 检测到无效的 `max-ts` 更新请求时，会返回错误并停止处理该请求。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21745>;tw:qiancai--> |
| TiKV | [`storage.max-ts.cache-sync-interval`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#cache-sync-interval-从-v857-版本开始引入) | 新增 | 用于控制 TiKV 更新本地 PD TSO 缓存的时间间隔。默认值为 `"15s"`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21745>;tw:qiancai--> |
| TiKV | [`storage.max-ts.max-drift`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#max-drift-从-v857-版本开始引入) | 新增 | 用于指定读写请求时间戳可超过 TiKV 中缓存的 PD TSO 的最大时间范围。默认值为 `"60s"`。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21745>;tw:qiancai--> |
| TiCDC | [`sink.dispatchers`](https://docs.pingcap.com/zh/tidb/v8.5/ticdc-changefeed-config#dispatchers) | 修改 | 当 Changefeed 下游为 MQ 类 Sink 时，可以通过 `dispatchers` 配置 event 分发器。从 v8.5.7 起，对于 [TiCDC 新架构](https://docs.pingcap.com/zh/tidb/v8.5/ticdc-architecture)，也可以通过 `dispatchers` 配置 [TiCDC 表路由](https://docs.pingcap.com/zh/tidb/v8.5/ticdc-table-routing)。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21723/files>;tw:qiancai--> |

### 编译器版本

* 为了提升 TiDB 性能，TiDB 的 Go 编译器版本从 go1.25.8 升级到了 go1.25.10。如果你是 TiDB 的开发者，为了确保顺利编译，请对应升级你的 Go 编译器版本。 [#953](https://github.com/PingCAP-QE/artifacts/pull/953) @[wuhuizuo](https://github.com/wuhuizuo) <!--2468--> <!--tw:lilin90-->
* 为了提升 TiKV 性能，TiKV v8.5 的 Rust 编译器版本从 nightly-2023-12-28 升级到了 nightly-2025-02-28。如果你是 TiKV 的开发者，为了确保顺利编译，请对应升级你的 Rust 编译器版本。

## 废弃功能

* 从 v8.5.7 开始，TiDB 和 TiDB Dashboard 中的[遥测](https://docs.pingcap.com/zh/tidb/v8.5/telemetry)功能已废弃。 <!--pr:<https://github.com/pingcap/docs-cn/pull/21750>;tw:lilin90-->

## 移除功能

* 从 TiDB v8.5.7 开始，TiDB Lightning 不再支持 Web 界面 [#67697](https://github.com/pingcap/tidb/issues/67697) @[D3Hunter](https://github.com/D3Hunter) <!--2273--> <!--tw:lilin90-->

    如需使用 TiDB Lightning 导入数据，请改用 TiDB Lightning 命令行工具：用于执行导入任务的 [`tidb-lightning`](https://docs.pingcap.com/zh/tidb/v8.5/tidb-lightning-command-line-full#tidb-lightning)，以及用于执行断点检查和故障排查的 [`tidb-lightning-ctl`](https://docs.pingcap.com/zh/tidb/v8.5/tidb-lightning-command-line-full#tidb-lightning-ctl)。

    对于新的数据导入工作负载，你也可以使用 [`IMPORT INTO`](https://docs.pingcap.com/zh/tidb/v8.5/sql-statement-import-into) 语句。

    如果此变更影响到你的工作流，请在 [#67697](https://github.com/pingcap/tidb/issues/67697) 中反馈。

## 改进提升

+ TiDB

    - 提升包含 `OR` 和 `IN` 条件的 `ORDER BY ... LIMIT` 查询性能。优化器现在可以更有效地选择 `IndexMerge`，并支持在 `IndexMerge` 的 `IN` 条件路径上使用 merge sort，从而将 `Limit` 下推到部分路径，减少不必要的行读取和 I/O 开销 [#65712](https://github.com/pingcap/tidb/issues/65712) @[time-and-fate](https://github.com/time-and-fate) <!-- component: planner --> <!--2262--> <!--tw:qiancai-->
    - 改进慢查询可观测性，在 slow query log 中记录客户端连接属性，并可在 `INFORMATION_SCHEMA.SLOW_QUERY` 和 `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` 中查询这些属性；`PERFORMANCE_SCHEMA_SESSION_CONNECT_ATTRS_SIZE` 现用于控制属性截断，并将被截断的字节数记录在 `_truncated` 中 [#66616](https://github.com/pingcap/tidb/issues/66616) @[jiong-nba](https://github.com/jiong-nba) <!-- component: observability --> <!--2374--> <!--tw:lilin90-->
    - 新增系统变量 `tidb_enable_strict_not_null_check`，用于控制 TiDB 是否对单行 `INSERT` 语句执行严格的 `NOT NULL` 检查，从而帮助依赖此前非严格行为的工作负载降低升级风险 [#68108](https://github.com/pingcap/tidb/issues/68108) @[xhebox](https://github.com/xhebox) <!-- component: sql-infra --> <!--2459-->
    - 提升 runaway query watch 处理的性能和稳定性，包括更可靠的 TiDB 实例间 watch 同步，以及更高效的后台 flush 和 sync [#65746](https://github.com/pingcap/tidb/issues/65746) @[JmPotato](https://github.com/JmPotato) <!-- component: pd (Although it is listed under the PD component label, in fact it only involves changes on the TiDB side )--> <!--2385-->
    - 新增全局系统变量 `tidb_enable_batch_query_region`，用于控制 TiDB 是否向 PD 批量查询 Region 信息，从而提升获取 Region 信息的效率；该变量默认关闭 [#58439](https://github.com/pingcap/tidb/issues/58439) [#8690](https://github.com/tikv/pd/issues/8690) @[JmPotato](https://github.com/JmPotato) <!-- component: pd (this is only a change on the TiDB side,) --> <!--2463-->
    - 改进多索引表查询的优化器性能，通过在代价估算前裁剪无关索引，降低查询规划时间，并避免不必要的全范围越界估算 [#63856](https://github.com/pingcap/tidb/issues/63856) @[terry1purcell](https://github.com/terry1purcell) @[qw4990](https://github.com/qw4990) <!-- component: planner --> <!--2315-->
    - 增强 Blackbox exporter dashboard 中的 **Ping Latency** 面板，通过使用 `max_over_time` 告警规则新增 `Max Ping Latency` 指标。该变更使 dashboard 展示与 TiDB 告警逻辑保持一致，有助于更容易地识别延迟峰值并验证告警触发情况 [#1071](https://github.com/pingcap/monitoring/issues/1071) @[yibin87](https://github.com/yibin87) <!--2424--> <!--tw:qiancai-->
    - 支持针对前缀索引上的 `TOPN` 查询进行部分有序索引优化，当 `tidb_opt_partial_ordered_index_for_topn` 设置为 `COST` 时，可提升 `ORDER BY ... LIMIT/OFFSET` 查询性能 [#66338](https://github.com/pingcap/tidb/issues/66338) @[xzhangxian1008](https://github.com/xzhangxian1008) @[winoros](https://github.com/winoros) <!-- component: execution -->
    - 优化使用 Stream Aggregate 的高基数 `GROUP BY` 查询性能，通过降低内存跟踪中的 CPU 开销实现 [#68475](https://github.com/pingcap/tidb/issues/68475) @[guo-shaoge](https://github.com/guo-shaoge) <!-- component: execution -->
    - 缓解高分区数且带本地索引的表上 `IndexLookUp` 查询的 coprocessor 请求突发问题，以提升查询稳定性并减少性能抖动 [#67545](https://github.com/pingcap/tidb/issues/67545) @[gengliqi](https://github.com/gengliqi) <!-- component: execution -->
    - 优化 `INSERT ... ON DUPLICATE KEY UPDATE` 语句的 CPU 和内存使用，通过减少执行过程中不必要的表达式缓冲区分配实现 [#65003](https://github.com/pingcap/tidb/issues/65003) @[windtalker](https://github.com/windtalker) <!-- component: execution, planner -->
    - 优化包含大型 `IN` 列表语句的查询规划性能，通过降低 range building 过程中的 CPU 和内存开销实现 [#67756](https://github.com/pingcap/tidb/issues/67756) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 提升自动 `ANALYZE` 的默认性能和一致性，使 `tidb_auto_build_stats_concurrency` 和 `tidb_sysproc_scan_concurrency` 的默认值与手动 `ANALYZE` 对齐 [#67195](https://github.com/pingcap/tidb/issues/67195) @[0xTars](https://github.com/0xTars) <!-- component: planner -->
    - 新增系统变量 `tidb_opt_enable_alternative_logical_plans`，用于启用针对子查询去关联的替代逻辑计划优化 [#66676](https://github.com/pingcap/tidb/issues/66676) @[AilinKid](https://github.com/AilinKid) <!-- component: planner -->
    - 新增系统变量 `tidb_enable_cache_prepare_stmt`，用于缓存同一会话中重复执行的预处理语句，从而降低 prepare-per-request 工作负载的 CPU 开销 [#67815](https://github.com/pingcap/tidb/issues/67815) @[guo-shaoge](https://github.com/guo-shaoge) <!-- component: planner -->
    - 改进 Join Reorder，使 TiDB 能处理 join group 之间的 projection，减少不必要的 Cartesian Join，并让 `LEADING` Hint 在更多查询中生效 [#50229](https://github.com/pingcap/tidb/issues/50229) @[Reminiscent](https://github.com/Reminiscent) <!-- component: planner -->
    - 支持在 `LEADING` optimizer hint 中使用嵌套括号来指定更复杂的连接顺序，例如 `LEADING((a, b), (c, d))` [#63253](https://github.com/pingcap/tidb/issues/63253) @[guo-shaoge](https://github.com/guo-shaoge) <!-- component: planner -->
    - 支持针对 `ORDER BY ... LIMIT` 查询进行部分有序索引优化，以减少全表扫描，该特性由系统变量 `tidb_opt_partial_ordered_index_for_topn` 控制 [#63280](https://github.com/pingcap/tidb/issues/63280) @[elsa0520](https://github.com/elsa0520) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 改进 Join 执行计划选择，避免在估算 probe 行数接近全表扫描时选择低效的 index join，从而提升某些 `HASHAGG` + join 场景下的查询性能 [#67610](https://github.com/pingcap/tidb/issues/67610) @[qw4990](https://github.com/qw4990) <!-- component: planner -->
    - 提升嵌套 `OR` 条件查询的性能，通过启用更高效的 `IndexMerge` 计划，并允许移除冗余全局过滤条件以便下推 `LIMIT` [#65822](https://github.com/pingcap/tidb/issues/65822) @[time-and-fate](https://github.com/time-and-fate) <!-- component: planner -->
    - 支持针对 `TOPN` 查询进行部分有序索引优化，当 `tidb_opt_partial_ordered_index_for_topn` 设置为 `COST` 时，可提升 `ORDER BY ... LIMIT` 查询性能 [#65813](https://github.com/pingcap/tidb/issues/65813) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 支持 `FLUSH STATS_DELTA` 语句，用于持久化全部、数据库级或表级范围内待写入的优化器统计信息增量 [#65668](https://github.com/pingcap/tidb/issues/65668) @[0xPoe](https://github.com/0xPoe) <!-- component: planner -->
    - 改进查询优化，默认启用用于在存在备选索引时考虑 `IndexMerge` 的优化器修复控制项，使 TiDB 能在更多适用查询中选择 `IndexMerge` 计划 [#26764](https://github.com/pingcap/tidb/issues/26764) @[time-and-fate](https://github.com/time-and-fate) <!-- component: planner -->
    - 支持缓存使用 `set_var` 和 `resource_group` Hint 的预处理与非预处理查询，以提升带 Hint 查询的 plan cache 命中率 [#60920](https://github.com/pingcap/tidb/issues/60920) @[qw4990](https://github.com/qw4990) <!-- component: planner -->
    - 优化使用 `IndexMerge` 的 `ORDER BY ... LIMIT` 和 `ORDER BY ... TOPN` 查询，在可能的情况下将 `Limit` 或 `TopN` 下推到各个 partial path，从而减少某些查询计划中不必要的扫描和排序 [#68773](https://github.com/pingcap/tidb/issues/68773) @[time-and-fate](https://github.com/time-and-fate) <!-- component: planner -->
    - 在新初始化的集群中，通过为 `mysql.stats_*` 系统表使用聚簇主键来提升 `ANALYZE` 性能 [#66751](https://github.com/pingcap/tidb/issues/66751) @[0xPoe](https://github.com/0xPoe) <!-- component: planner -->
    - 改进优雅关闭处理，通过对 `COM_PING` 请求返回错误，让代理和负载均衡器能够检测到 TiDB server 正在关闭，并停止发送新连接 [#58007](https://github.com/pingcap/tidb/issues/58007) @[dveeden](https://github.com/dveeden) <!-- component: sql-infra -->
    - 加速包含大量生成列的表上的 `INSERT` 语句，显著提升宽表工作负载的性能 [#67916](https://github.com/pingcap/tidb/issues/67916) @[bb7133](https://github.com/bb7133) <!-- component: sql-infra -->
    - 支持在 TiDB Dashboard 的 Slow Query 页面查看会话连接属性，包括可选的列表列和专用详情页签，同时兼容不提供该字段的早期 TiDB 版本 [#1899](https://github.com/pingcap/tidb-dashboard/issues/1899) @[yibin87](https://github.com/yibin87) <!-- component: tidb-dashboard -->
    - 改进事务时间戳校验，通过对非 TiDB 请求执行精确的 max-ts 检查，降低外部组件错误使用未来时间戳的风险 [#68799](https://github.com/pingcap/tidb/issues/68799) @[ekexium](https://github.com/ekexium) <!-- component: transaction -->
    - 优化自动提交的乐观事务，在首次执行时跳过锁解析，从而降低高冲突场景下的延迟 [#58675](https://github.com/pingcap/tidb/issues/58675) @[ekexium](https://github.com/ekexium) <!-- component: transaction -->

+ TiKV

    - 新增动态资源组隔离，通过降低超过历史 RU 基线的资源组请求优先级，并在高 CPU 负载下可选择延迟或拒绝超基线请求，以保护持续性工作负载免受流量突发影响；相关新的 `resource-control` 配置项默认关闭 [#19607](https://github.com/tikv/tikv/issues/19607) @[mittalrishabh](https://github.com/mittalrishabh) <!-- component: raft --> <!--2465-->
    - 对所有 TiKV 后台资源组使用全局速率限制器，并聚合相关后台资源管控指标而不再使用 `resource_group` 标签，因此受影响的 dashboard 和告警需要相应更新 [#19497](https://github.com/tikv/tikv/issues/19497) @[mittalrishabh](https://github.com/mittalrishabh) <!-- component: raft -->
    - 改进 TiKV Unified Read Pool 的调度公平性，当队列已满时允许高优先级请求驱逐低优先级排队任务，从而帮助在租户流量和后台流量之间实现更公平的资源分配 [#19386](https://github.com/tikv/tikv/issues/19386) @[mittalrishabh](https://github.com/mittalrishabh) <!-- component: raft -->
    - 在 apply log 处理期间，为 PITR 恢复产生的 `Put` 和 `Delete` write CF 记录打上物理导入事务来源标记，使 TiCDC 可以忽略 PITR 导入的数据 [#19669](https://github.com/tikv/tikv/issues/19669) @[YuJuncen](https://github.com/YuJuncen) <!-- component: tikv -->
    - 为检测到磁盘 I/O 卡顿的 TiKV 节点新增自动快速退出机制，以加快无响应 store 的恢复 [#19626](https://github.com/tikv/tikv/issues/19626) @[hbisheng](https://github.com/hbisheng) <!-- component: tikv -->
    - 通过升级 TiKV 8.5 中存在漏洞的第三方依赖并同步上游所需兼容性修复，提升 TiKV 的稳定性和安全性 [#19713](https://github.com/tikv/tikv/issues/19713) @[LykxSassinator](https://github.com/LykxSassinator) <!-- component: tikv -->
    - 支持 TiKV 中基于 rank 的 limit 处理，以便在使用 truncate key expression 的查询中返回更准确的结果 [#19388](https://github.com/tikv/tikv/issues/19388) @[xzhangxian1008](https://github.com/xzhangxian1008) <!-- component: tikv -->
    - 改进 TiKV 中基于负载的 Region 分裂，通过放宽默认分裂阈值，并增强 split-key 选择和 CPU fallback 决策的可观测性，帮助运维人员更有效地处理热点 Region [#18932](https://github.com/tikv/tikv/issues/18932) @[lhy1024](https://github.com/lhy1024) <!-- component: tikv -->

+ PD

    - 新增 PD maintenance endpoints 和 `pd-ctl` 命令，用于串行化 TiKV 维护任务，并通过确保任一时刻只有一个维护任务处于活动状态来防止 Raft quorum 丢失 [#9477](https://github.com/tikv/pd/issues/9477) @[SerjKol80](https://github.com/SerjKol80) @[HaoW30](https://github.com/HaoW30) <!-- component: pd --> <!--2467-->
    - 在 PD 中默认关闭 split scatter，以避免 Region split 后出现意外调度；如有需要，你仍可通过将 `schedule.split-scatter-schedule-limit` 设置为正值来启用 [#10592](https://github.com/tikv/pd/issues/10592) @[lhy1024](https://github.com/lhy1024) <!-- component: pd -->
    - 优化 unsafe recovery 中空 Region 计划的生成，以提升在包含大量 Region 和空洞的大型集群中的性能并降低超时风险 [#10638](https://github.com/tikv/pd/issues/10638) @[Connor1996](https://github.com/Connor1996) <!-- component: pd -->
    - 改进 PD 事务持续时间指标，使其更准确地反映生产环境中的延迟分布，并提升 dashboard 和告警中的可观测性 [#10705](https://github.com/tikv/pd/issues/10705) @[bufferflies](https://github.com/bufferflies) <!-- component: pd -->

+ TiFlash

    - 删除 TiFlash 中无用的 gRPC 连接，以减少 TiKV 节点缩容后重复出现的无效连接日志 [#9806](https://github.com/pingcap/tiflash/issues/9806) @[gengliqi](https://github.com/gengliqi) <!-- component: compute -->

+ Tools

    + Backup & Restore (BR)

        - 支持在 BR 中使用 Workload Identity Federation 访问 Google Cloud Storage 备份桶 [#19442](https://github.com/tikv/tikv/issues/19442) @[Leavrth](https://github.com/Leavrth) <!-- component: br --> <!--2457--> <!--2431-->
        - 通过仅加载必要的数据库 schema 信息，降低 schema 重新加载开销和 DDL 阻塞时间，从而缓解 BR 备份与恢复对在线 DDL 的影响 [#64833](https://github.com/pingcap/tidb/issues/64833) @[YuJuncen](https://github.com/YuJuncen) <!-- component: br --> <!--2369-->
        - 通过将 PITR 恢复产生的 write CF 条目标记为物理导入事务，提升 PITR 与 TiCDC 的兼容性，使 TiCDC 可以忽略 PITR 导入的数据 [#68660](https://github.com/pingcap/tidb/issues/68660) @[YuJuncen](https://github.com/YuJuncen) <!-- component: br -->
        - 新增 `--region-scan-concurrency` 参数，用于限制 BR 同时向 PD 发送的 Region 扫描请求数量，在需要发起大量 Region 扫描时提升恢复稳定性 [#66821](https://github.com/pingcap/tidb/issues/66821) @[Leavrth](https://github.com/Leavrth) <!-- component: br -->

    + TiCDC

        - 优化 TiCDC event store 的写入路径和 iterator 路径，以减少内存分配并提升事件处理性能 [#4928](https://github.com/pingcap/ticdc/issues/4928) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 移除 TiCDC 对 `tidb_ddl_history` 的依赖，转而依赖 `tidb_ddl_job` 来捕获 DDL，以支持加速表创建 [#2272](https://github.com/pingcap/ticdc/issues/2272) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc -->
        - 优化 TiCDC 热路径，以降低 CPU 开销并提升高吞吐场景下的复制性能 [#5107](https://github.com/pingcap/ticdc/issues/5107) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 新增 redo checkpoint 和 resolved timestamp 指标，以提升 TiCDC redo log 进度的可观测性 [#5264](https://github.com/pingcap/ticdc/issues/5264) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 通过避免持久化未变化的运行时状态，缓解大量 TiCDC changefeed 进入 warning 状态时的 etcd 压力 [#5268](https://github.com/pingcap/ticdc/issues/5268) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 增强 TiCDC 监控，在 Changefeed Error Details Grafana 面板中展示错误发生时间，帮助运维人员更高效地诊断 changefeed 故障 [#5085](https://github.com/pingcap/ticdc/issues/5085) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc -->
        - 通过将每次 checker 运行中每个 group 的 split table merge 调度限制为最多 8 个 merge operator，缓解 TiCDC 增量扫描的 CPU 峰值 [#5047](https://github.com/pingcap/ticdc/issues/5047) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc -->
        - 通过在 DML 事件进入写入流水线时即进行确认，而不是等待 flush 完成，提升 TiCDC cloud storage sink 的调度响应性和回调正确性，在保持 checkpoint 语义不变的前提下降低唤醒延迟 [#4269](https://github.com/pingcap/ticdc/issues/4269) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc -->
        - 减少 changefeed 之间的 TiCDC bootstrap 队首阻塞，在 sink 初始化较慢时提升 changefeed 创建和恢复吞吐量 [#5139](https://github.com/pingcap/ticdc/issues/5139) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc -->
        - 通过默认重试临时性的 producer send failure，提升 TiCDC Kafka sink 的稳定性 [#1920](https://github.com/pingcap/ticdc/issues/1920) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc -->
        - 新增 Kafka sink URI 参数 `max-retry`，并默认对临时性的 Kafka producer send failure 启用有界重试，以提升 TiCDC Kafka sink 的稳定性 [#12655](https://github.com/pingcap/tiflow/issues/12655) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc -->
        - 为 TiCDC cloud storage sink 新增本地 spool，用于在刷新到外部存储前先将已接收的编码 DML 暂存在本地，从而在对象存储较慢时降低内存压力并提升稳定性 [#3745](https://github.com/pingcap/ticdc/issues/3745) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc -->
        - 支持 TiCDC 同步部分索引相关的 DDL 语句 [#3698](https://github.com/pingcap/ticdc/issues/3698) @[YangKeao](https://github.com/YangKeao) <!-- component: cdc -->
        - 为 TiCDC blackhole sink 新增指标，以提升 changefeed 复制和 DDL 处理的可观测性 [#5362](https://github.com/pingcap/ticdc/issues/5362) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 优化 TiCDC log puller 性能，在处理 resolved-ts 密集型工作负载时，尤其是小批量场景下，降低 CPU 使用和内存分配 [#4697](https://github.com/pingcap/ticdc/issues/4697) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc -->
        - 优化 TiCDC MySQL sink 的冲突检测，以提升复制性能 [#4582](https://github.com/pingcap/ticdc/issues/4582) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 提升 TiCDC resolve lock 的可观测性，并避免对同一 Region 重复执行 resolve 尝试，以减少不必要的锁解析工作，并通过新增指标和 dashboard 让问题排查更容易 [#5016](https://github.com/pingcap/ticdc/issues/5016) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 在 TiCDC Grafana dashboard 中新增 Changefeed Operation History 面板，帮助排查最近由用户触发的 changefeed 操作，例如 create、update、pause、resume 和 delete [#5087](https://github.com/pingcap/ticdc/issues/5087) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc -->
        - 支持解析和同步使用部分索引的 DDL 语句，包括带有 `WHERE` 子句的 `CREATE TABLE`、`CREATE INDEX` 和 `ALTER TABLE ... ADD INDEX` [#12503](https://github.com/pingcap/tiflow/issues/12503) @[YangKeao](https://github.com/YangKeao) <!-- component: cdc -->
        - 支持 MySQL sink 的表路由，使经过路由的 changefeed 能将 DDL 和 DML 应用到目标 schema 和表名上 [#4818](https://github.com/pingcap/ticdc/issues/4818) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc -->
        - 新增 TiCDC 指标，用于展示 warning 或 failed 状态 changefeed 的错误信息，使运维人员无需查看日志即可通过监控更方便地诊断问题 [#4498](https://github.com/pingcap/ticdc/issues/4498) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->

    + TiDB Lightning

        - 支持在未指定 `FORMAT` 时，TiDB `IMPORT INTO` 根据文件名自动检测文件格式，从而简化对 CSV、SQL 和 Parquet 文件的数据导入 [#59540](https://github.com/pingcap/tidb/issues/59540) @[JQWong7](https://github.com/JQWong7) <!-- component: lightning -->

## 错误修复

+ TiDB

    - 修复当查询仍在运行时，TiDB 未能及时关闭已断开客户端连接，导致该连接在语句执行完成前仍保留在 `SHOW PROCESSLIST` 中的问题 [#57531](https://github.com/pingcap/tidb/issues/57531) @[Defined2014](https://github.com/Defined2014) <!-- component: sql-infra --> <!--2060-->
    - 修复在出现 `RegionNotFound` 错误后，过期的 Region cache 条目仍可能继续被使用，导致重复重试失败和 Region 重载延迟的问题 [#1892](https://github.com/tikv/client-go/issues/1892) @[ekexium](https://github.com/ekexium) <!-- component: client-go -->
    - 修复在使用常量字符串参数评估向量化 `ILIKE` 时可能发生崩溃的问题 [#67001](https://github.com/pingcap/tidb/issues/67001) @[zanmato1984](https://github.com/zanmato1984) <!-- component: execution -->
    - 修复对无符号数值列或 `SET` 列执行点更新 `UPDATE` 语句时，可能产生与普通 `UPDATE` 语义及 MySQL 兼容性不一致的错误结果的问题 [#63455](https://github.com/pingcap/tidb/issues/63455) @[fzzf678](https://github.com/fzzf678) <!-- component: execution -->
    - 修复 TiDB 在极少数并发查询执行场景下可能因 `SIGSEGV` 崩溃的问题 [#66391](https://github.com/pingcap/tidb/issues/66391) @[bb7133](https://github.com/bb7133) <!-- component: execution -->
    - 修复在使用大小写不同的用户变量时，查询可能生成次优执行计划并无法使用索引范围扫描的问题 [#66339](https://github.com/pingcap/tidb/issues/66339) @[qw4990](https://github.com/qw4990) <!-- component: planner -->
    - 修复多个会话并发命中全局绑定并破坏全局绑定缓存时，TiDB 可能发生内存耗尽的问题 [#68015](https://github.com/pingcap/tidb/issues/68015) @[qw4990](https://github.com/qw4990) <!-- component: planner -->
    - 修复带外连接和对 `NULL` 敏感条件的查询由于优化器错误评估 null-reject 而可能返回错误结果的问题 [#58793](https://github.com/pingcap/tidb/issues/58793) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复外连接内侧的 `WHERE` 条件可能导致 TiDB 返回错误查询结果或漏行的问题 [#59162](https://github.com/pingcap/tidb/issues/59162) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复某些带外连接和 `OR` 条件的查询可能返回错误结果的问题 [#60080](https://github.com/pingcap/tidb/issues/60080) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复对外连接结果使用 `IS NULL` 过滤条件的查询可能返回带有 `NULL` 值的错误行的问题 [#60081](https://github.com/pingcap/tidb/issues/60081) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复带外连接且 `WHERE` 子句中包含 `COALESCE()` 等对 `NULL` 敏感谓词的查询，可能因 TiDB 错误简化连接而返回错误结果的问题 [#60370](https://github.com/pingcap/tidb/issues/60370) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复带外连接且 `WHERE` 条件中包含 `NULLIF()` 和 `CAST()` 等表达式的查询可能返回错误结果的问题 [#67330](https://github.com/pingcap/tidb/issues/67330) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复带派生表和 `UNION ALL` 的查询可能因 TiDB 错误简化外连接而返回错误结果的问题 [#67373](https://github.com/pingcap/tidb/issues/67373) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复带 `LEFT JOIN` 或 `RIGHT JOIN` 且 `WHERE` 子句中包含对 `NULL` 敏感布尔表达式的查询可能返回错误结果的问题 [#66824](https://github.com/pingcap/tidb/issues/66824) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复 `LEFT JOIN` 查询中包含 `IN (NULL, ...)` 等对 `NULL` 敏感谓词时，可能因 TiDB 错误简化外连接而返回错误结果的问题 [#66825](https://github.com/pingcap/tidb/issues/66825) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复当 null-reject 检查与参数值无关时，外连接上的预处理语句可能跳过 prepared plan cache 的问题 [#67048](https://github.com/pingcap/tidb/issues/67048) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复点更新语句在无符号数值列或向 `SET` 列赋整数值时，可能使用与普通 `UPDATE` 语句不同的赋值转换语义，导致结果不一致或越界错误的问题 [#67534](https://github.com/pingcap/tidb/issues/67534) @[fzzf678](https://github.com/fzzf678) <!-- component: planner -->
    - 修复在为全范围索引扫描执行查询规划时，TiDB 可能记录不必要的异步索引直方图加载告警的问题 [#64791](https://github.com/pingcap/tidb/issues/64791) @[terry1purcell](https://github.com/terry1purcell) <!-- component: planner -->
    - 修复同步统计信息加载超时并回退到 pseudo 或 partial statistics 时生成的执行计划，可能在所需统计信息加载完成后仍被缓存和复用的问题 [#66585](https://github.com/pingcap/tidb/issues/66585) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复 TiDB 在外连接场景下可能生成错误 join order 并返回错误查询结果的问题 [#63887](https://github.com/pingcap/tidb/issues/63887) @[guo-shaoge](https://github.com/guo-shaoge) <!-- component: planner -->
    - 修复 TiDB 在某些包含外连接的查询中可能选择次优 join order，从而导致执行计划效率较低的问题 [#67774](https://github.com/pingcap/tidb/issues/67774) @[AilinKid](https://github.com/AilinKid) <!-- component: planner -->
    - 修复升级期间当 `mysql.global_variables` 中缺少对应行时，`tidb_ignore_inlist_plan_digest` 可能被意外重置的问题 [#68136](https://github.com/pingcap/tidb/issues/68136) @[qw4990](https://github.com/qw4990) <!-- component: planner -->
    - 修复在优化带 `ORDER BY` 和 `LIMIT` 的查询时，TiDB 可能因低估 `IndexFullScan` 代价而选择低效的 `MergeJoin` 计划，从而导致查询性能较差的问题 [#67595](https://github.com/pingcap/tidb/issues/67595) @[qw4990](https://github.com/qw4990) <!-- component: planner -->
    - 修复使用包含重复表达式的 expression index 的查询，可能因 TiDB 解析错误的隐藏生成列而返回 `Unexpected missing column` 错误的问题 [#67552](https://github.com/pingcap/tidb/issues/67552) @[AilinKid](https://github.com/AilinKid) <!-- component: planner -->
    - 修复 `ANALYZE` 在执行 `KILL QUERY` 或取消后可能无法及时停止，导致 analyze 任务卡住的问题 [#65818](https://github.com/pingcap/tidb/issues/65818) @[hawkingrei](https://github.com/hawkingrei) <!-- component: planner -->
    - 修复将集群从早于 v7.6 的版本升级后，手动 `ANALYZE` 可能变慢的问题，其原因是 `tidb_analyze_distsql_scan_concurrency` 未根据现有 `tidb_distsql_scan_concurrency` 设置完成初始化 [#65423](https://github.com/pingcap/tidb/issues/65423) @[winoros](https://github.com/winoros) <!-- component: planner -->
    - 修复 TiDB 无法将某些非关联 `IN` 子查询转换为关联执行计划，导致无法使用索引查找并生成较低效查询计划的问题 [#66320](https://github.com/pingcap/tidb/issues/66320) @[terry1purcell](https://github.com/terry1purcell) <!-- component: planner -->
    - 修复在带索引的字符串列上使用 `CAST(... AS BINARY)` 时，查询可能执行索引全扫描而非索引范围扫描的问题 [#67899](https://github.com/pingcap/tidb/issues/67899) @[terry1purcell](https://github.com/terry1purcell) <!-- component: planner -->
    - 修复对依赖被跳过列类型的已索引存储生成列执行 `ANALYZE TABLE` 时可能发生 panic 的问题 [#66359](https://github.com/pingcap/tidb/issues/66359) @[xhebox](https://github.com/xhebox) <!-- component: planner -->
    - 修复对依赖 `JSON` 等被跳过列类型的已索引存储生成列执行 `ANALYZE TABLE` 时可能发生 panic 的问题 [#66918](https://github.com/pingcap/tidb/issues/66918) @[xhebox](https://github.com/xhebox) <!-- component: planner -->
    - 修复带外连接的查询中，TiDB 可能生成错误 join order，从而导致错误查询结果的问题 [#67290](https://github.com/pingcap/tidb/issues/67290) @[guo-shaoge](https://github.com/guo-shaoge) <!-- component: planner -->
    - 修复当会话 `time_zone` 领先于 UTC 时，`SHOW ANALYZE STATUS` 可能显示负值 `Remaining_seconds` 的问题 [#67230](https://github.com/pingcap/tidb/issues/67230) @[0xPoe](https://github.com/0xPoe) <!-- component: planner -->
    - 修复在分区表上执行 `ANALYZE`（包括 auto-analyze）期间可能导致 TiDB server 崩溃，并报告 `fatal error: concurrent map read and map write` 的问题 [#68457](https://github.com/pingcap/tidb/issues/68457) @[mjonss](https://github.com/mjonss) <!-- component: planner -->
    - 修复部分索引可能被错误用于执行外键约束检查，导致删除或更新父表行时遗漏匹配的子表行并留下孤儿行的问题 [#68587](https://github.com/pingcap/tidb/issues/68587) @[YangKeao](https://github.com/YangKeao) <!-- component: sql-infra -->
    - 修复不包含生成列的表上的 `INSERT` 语句出现性能回退，导致常见工作负载吞吐下降的问题 [#68129](https://github.com/pingcap/tidb/issues/68129) @[bb7133](https://github.com/bb7133) <!-- component: sql-infra -->
    - 修复 `CONCAT_WS()` 将 `utf8mb4_0900_bin` 列与 `BLOB` 列组合时，返回 `ERROR 3854` 错误而非二进制结果的问题 [#68845](https://github.com/pingcap/tidb/issues/68845) @[tiancaiamao](https://github.com/tiancaiamao) <!-- component: sql-infra -->
    - 修复由于连接监控开销，autocommit `INSERT`、`UPDATE` 和 `DELETE` 语句出现性能回退的问题 [#68633](https://github.com/pingcap/tidb/issues/68633) @[King-Dylan](https://github.com/King-Dylan) <!-- component: sql-infra -->
    - 修复在 `new_collation_enabled` 被禁用时，对大小写混合的 schema 名执行 `GRANT` 和 `REVOKE` 可能创建重复权限行，或无法找到现有权限的问题 [#66867](https://github.com/pingcap/tidb/issues/66867) @[expxiaoli](https://github.com/expxiaoli) <!-- component: sql-infra -->
    - 修复在 `new_collation_enabled` 被禁用时，对大小写混合的 schema 名执行 `GRANT` 和 `REVOKE` 可能失败，或命中不一致权限行的问题 [#68406](https://github.com/pingcap/tidb/issues/68406) @[expxiaoli](https://github.com/expxiaoli) <!-- component: sql-infra -->
    - 修复客户端断开后，autocommit 写语句可能无法被及时中断的问题 [#68236](https://github.com/pingcap/tidb/issues/68236) @[King-Dylan](https://github.com/King-Dylan) <!-- component: sql-infra -->
    - 修复与非 TiDB 事务相关的请求可能错误通过未来时间戳校验，并在 `ScanLock`、backup range、`CheckTxnStatus`、`Cleanup` 和 `CheckSecondaryLocks` 中导致行为不一致的问题 [#19656](https://github.com/tikv/tikv/issues/19656) @[ekexium](https://github.com/ekexium) <!-- component: transaction -->
    - 修复在启用 `tidb_foreign_key_check_in_shared_lock` 时，悲观事务中的外键级联更新可能因 `use Op::SharedLock to prewrite on a shared lock` 而失败的问题 [#68133](https://github.com/pingcap/tidb/issues/68133) @[wfxr](https://github.com/wfxr) <!-- component: transaction -->
    - 修复在出现 `RegionNotFound` 错误后，过期的 Region cache 条目仍可能继续被使用，导致重复重试并产生额外跨可用区流量的问题 [#69197](https://github.com/pingcap/tidb/issues/69197) @[ekexium](https://github.com/ekexium) <!-- component: transaction -->

+ TiKV

    - 修复当 Region 数量较大时，resolved_ts 模块消耗过多内存的问题 [#19535](https://github.com/tikv/tikv/issues/19535) @[glorv](https://github.com/glorv) <!-- component: tikv -->
    - 修复在启用 MVCC read-aware compaction 时，TiKV 可能在一个长时间 compaction 轮次结束后立即开始下一轮 compaction，导致基于负载的 compaction 缺乏足够统计信息的问题 [#19362](https://github.com/tikv/tikv/issues/19362) @[mittalrishabh](https://github.com/mittalrishabh) <!-- component: tikv -->
    - 修复在使用 raft-engine 时，TiKV 在稳定工作负载下内存占用会随时间持续增长的问题 [#19544](https://github.com/tikv/tikv/issues/19544) @[LykxSassinator](https://github.com/LykxSassinator) <!-- component: tikv -->
    - 修复手动从 TiKV In-Memory Engine 驱逐 Region 后，这些 Region 会卡在 `Evicting` 状态并无法被自动重新加载的问题 [#19584](https://github.com/tikv/tikv/issues/19584) @[overvenus](https://github.com/overvenus) <!-- component: tikv -->
    - 修复当一个 store 使用多个 gRPC raft 连接时，TiKV 在 raft message 队列中消耗过多内存的问题 [#19542](https://github.com/tikv/tikv/issues/19542) @[glorv](https://github.com/glorv) <!-- component: tikv -->
    - 修复在 TiKV 中止 CPU profiling 请求后，profiling 仍卡在 active 状态，导致后续 profiling 请求返回 `Already in CPU Profiling` 错误的问题 [#19703](https://github.com/tikv/tikv/issues/19703) @[hujiatao0](https://github.com/hujiatao0) <!-- component: tikv -->
    - 修复在日志条目已持久化后，TiKV 仍可能在 Raft log 中保留过多内存，导致副本内存占用异常偏高的问题 [#19593](https://github.com/tikv/tikv/issues/19593) @[LykxSassinator](https://github.com/LykxSassinator) <!-- component: tikv -->
    - 修复当从 PD 解析已移除 tombstone store 的地址时，TiKV 可能陷入无限重试循环并反复记录 `invalid store ID ..., not found` 错误的问题 [#17875](https://github.com/tikv/tikv/issues/17875) @[LykxSassinator](https://github.com/LykxSassinator) <!-- component: tikv -->
    - 修复当访问令牌在长时间上传期间接近过期时，TiKV GCS 备份可能失败的问题 [#19659](https://github.com/tikv/tikv/issues/19659) @[RidRisR](https://github.com/RidRisR) <!-- component: tikv -->
    - 修复 TiKV `apply_msg_len` 指标在正常流量下无数据点，影响 apply message 长度分布监控的问题 [#18800](https://github.com/tikv/tikv/issues/18800) @[squalfof](https://github.com/squalfof) <!-- component: tikv -->
    - 修复当 PD 在 split 后立即 merge Region 时，TiKV 可能因在 Region heartbeat 中上报错误的 pending peer 信息而发生 panic 的问题 [#17992](https://github.com/tikv/tikv/issues/17992) @[hbisheng](https://github.com/hbisheng) <!-- component: tikv -->
    - 修复无法访问 TiKV In-Memory Engine 调试 API `/debug/ime/cached_regions` 的问题 [#19546](https://github.com/tikv/tikv/issues/19546) @[glorv](https://github.com/glorv) <!-- component: tikv -->
    - 修复 TiKV 中的 `server.grpc_memory_pool_quota` 配置无法动态修改的问题 [#19104](https://github.com/tikv/tikv/issues/19104) @[glorv](https://github.com/glorv) <!-- component: tikv -->
    - 修复当在线流量占用大部分 CPU 资源时，TiKV 不会限制后台流量，导致高负载场景下在线请求延迟升高的问题 [#19401](https://github.com/tikv/tikv/issues/19401) @[mittalrishabh](https://github.com/mittalrishabh) <!-- component: tikv -->

+ PD

    - 修复在高并发场景下，由于 token bucket 累积了过多令牌，PD 资源管控限速可能被削弱的问题 [#10744](https://github.com/tikv/pd/issues/10744) @[YuhaoZhang00](https://github.com/YuhaoZhang00) <!-- component: pd -->
    - 修复在重置 token bucket notification timer 时，resource group client controller 中发生 goroutine 泄漏的问题 [#9745](https://github.com/tikv/pd/issues/9745) @[lhy1024](https://github.com/lhy1024) <!-- component: pd -->
    - 修复当配置的 RU 填充速率远高于实际 RU 消耗时，发往 resource group 的 SQL 请求可能出现约 1 秒延迟尖峰的问题 [#10251](https://github.com/tikv/pd/issues/10251) @[JmPotato](https://github.com/JmPotato) <!-- component: pd --> <!--2413 -->
    - 修复当 placement rules 要求的最高隔离级别未满足时，PD affinity scheduling 仍可能将 Region 误判为已正确复制，导致错误副本放置决策的问题 [#10149](https://github.com/tikv/pd/issues/10149) @[HunDunDM](https://github.com/HunDunDM) <!-- component: pd -->
    - 修复当 region heartbeat breakdown 指标遇到主机 monotonic clock 短暂回退时，PD 可能因 `counter cannot decrease in value` 错误而 panic 的问题 [#10901](https://github.com/tikv/pd/issues/10901) @[JmPotato](https://github.com/JmPotato) <!-- component: pd -->
    - 修复当未配置 affinity groups 时，PD 错误上报 affinity checker operator limit 指标的问题 [#10687](https://github.com/tikv/pd/issues/10687) @[lhy1024](https://github.com/lhy1024) <!-- component: pd -->
    - 修复除非显式设置 `PD-Allow-Follower-Handle: true` 请求头，否则 PD follower 无法从本地已同步 Region cache 提供只读 region HTTP API 的问题 [#10681](https://github.com/tikv/pd/issues/10681) @[okJiang](https://github.com/okJiang) <!-- component: pd -->
    - 修复当 PD leader 未发送 region sync 响应或在关闭期间关闭 sync stream 时，PD follower 可能停止接收 region 更新的问题 [#10684](https://github.com/tikv/pd/issues/10684) @[okJiang](https://github.com/okJiang) <!-- component: pd -->
    - 修复 region syncer 的一个问题：当 PD leader 未发送更新并从内存中移除该 stream 后，PD follower 可能仍在等待一个过期的 stream [#10666](https://github.com/tikv/pd/issues/10666) @[okJiang](https://github.com/okJiang) <!-- component: pd -->
    - 修复在仅 flow 更新的 region heartbeat 后，PD 可能持续调度冗余 subtree update 任务，从而增加大型集群内存压力的问题 [#10722](https://github.com/tikv/pd/issues/10722) @[JmPotato](https://github.com/JmPotato) <!-- component: pd -->

+ Tools

    + Backup & Restore (BR)

        - 修复即使指定了 `--check-requirements=false`，BR restore 仍会因版本兼容性检查失败而无法继续执行的问题 [#67402](https://github.com/pingcap/tidb/issues/67402) @[RidRisR](https://github.com/RidRisR) <!-- component: br -->
        - 修复当 lock file 位于存储根目录时，BR `log truncate` 在兼容 S3 的存储中可能失败的问题 [#65897](https://github.com/pingcap/tidb/issues/65897) @[YuJuncen](https://github.com/YuJuncen) <!-- component: br -->
        - 修复当备份中包含大量 `mDB:*` 元键多个版本时，BR PITR 在恢复元数据期间可能耗尽内存的问题 [#67196](https://github.com/pingcap/tidb/issues/67196) @[vldmit](https://github.com/vldmit) <!-- component: br -->
        - 修复在启用 AWS FIPS endpoint 模式时，BR 可能无法访问自定义 AWS S3 endpoint 的问题 [#68966](https://github.com/pingcap/tidb/issues/68966) @[v01dstar](https://github.com/v01dstar) <!-- component: br -->
        - 修复当目标集群与备份集群的列数不一致时，BR 在 snapshot restore 期间仍会物理恢复 `mysql.user` 表，从而覆盖较新表结构而不是回退到逻辑恢复的问题 [#68861](https://github.com/pingcap/tidb/issues/68861) @[Leavrth](https://github.com/Leavrth) <!-- component: br -->
        - 修复 `br operator base64ify` 在生成的存储后端中无法保留 S3 Object Lock 状态的问题 [#68551](https://github.com/pingcap/tidb/issues/68551) @[YuJuncen](https://github.com/YuJuncen) <!-- component: br -->
        - 修复当 TiKV 未响应 flush subscription 请求时，BR log backup checkpoint 推进可能卡住的问题 [#68411](https://github.com/pingcap/tidb/issues/68411) @[Leavrth](https://github.com/Leavrth) <!-- component: br -->
        - 修复在使用表过滤器执行 BR PITR 时，同一数据库中的表被多次恢复可能创建重复数据库或意外修改目标数据库的问题 [#68908](https://github.com/pingcap/tidb/issues/68908) @[Leavrth](https://github.com/Leavrth) <!-- component: br -->
        - 修复 BR log backup 的当前最后一个 region ID 和 leader store ID 指标缺失于 `/metrics` 端点的问题 [#62839](https://github.com/pingcap/tidb/issues/62839) @[YuJuncen](https://github.com/YuJuncen) <!-- component: br -->
        - 修复在高写入压力下，BR 向 S3 执行日志备份时，可能因 multipart upload 超过 10000 分片限制而卡住的问题 [#19162](https://github.com/tikv/tikv/issues/19162) @[vldmit](https://github.com/vldmit) <!-- component: br -->
        - 修复当使用较旧 restore 工具恢复由较新 BR 版本创建的备份时，BR 可能静默丢失无法识别的备份元数据（如 `merge_option` 属性）的问题；现在会在 requirement checks 阶段报告该兼容性问题 [#67016](https://github.com/pingcap/tidb/issues/67016) @[JoyC-dev](https://github.com/JoyC-dev) <!-- component: br -->
        - 修复在 truncate 或 migration loading 失败时，BR log backup 可能泄漏外部备份目录或残留过期读锁的问题 [#67819](https://github.com/pingcap/tidb/issues/67819) @[RidRisR](https://github.com/RidRisR) <!-- component: br -->
        - 修复当凭证仅对配置的 prefix 范围有效时，BR 对 S3 权限的检查可能失败，导致备份或恢复任务在开始前就失败的问题 [#68583](https://github.com/pingcap/tidb/issues/68583) @[YuJuncen](https://github.com/YuJuncen) <!-- component: br -->
        - 修复在启用日志备份且恢复失败后，从 checkpoint 恢复 restore 时，BR 可能不会写入 PiTR blocklist 的问题 [#68171](https://github.com/pingcap/tidb/issues/68171) @[Leavrth](https://github.com/Leavrth) <!-- component: br -->
        - 修复当初始化的 Region 数量超过 32768 个时，BR 日志备份任务启动可能卡住的问题 [#19615](https://github.com/tikv/tikv/issues/19615) @[YuJuncen](https://github.com/YuJuncen) <!-- component: br -->
        - 修复在逻辑恢复系统表时，BR 可能因 `Transaction is too large` 错误而失败的问题，并新增 `--txn-total-size-limit` 参数用于调整事务内存配额 [#66806](https://github.com/pingcap/tidb/issues/66806) @[Leavrth](https://github.com/Leavrth) <!-- component: br -->

    + TiCDC

        - 修复 TiCDC Grafana dashboard 中面板重叠和分区顺序错误的问题 [#4508](https://github.com/pingcap/ticdc/issues/4508) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复当事件迭代器创建失败或首次读取失败时，TiCDC 不会上报实际错误，从而掩盖事件扫描失败根因的问题 [#5005](https://github.com/pingcap/ticdc/issues/5005) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复当发送 DDL 事件或 checkpoint 失败并触发重试时，TiCDC Kafka changefeed 可能泄漏 Kafka client 实例并导致内存持续增长的问题 [#12666](https://github.com/pingcap/tiflow/issues/12666) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc -->
        - 修复当增量扫描包含缺失旧值的 insert-like prewrite lock 时，TiCDC 可能消耗过多 CPU 且 checkpoint 推进缓慢的问题 [#19565](https://github.com/tikv/tikv/issues/19565) @[zier-one](https://github.com/zier-one) <!-- component: cdc -->
        - 修复在 dispatcher reset 之后，TiCDC 可能扫描到 checkpoint 以下数据，并可能导致 event store panic 的问题 [#4492](https://github.com/pingcap/ticdc/issues/4492) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复在组件初始化失败时，TiCDC 可能泄漏连接、存储句柄或后台 goroutine 的问题 [#4516](https://github.com/pingcap/ticdc/issues/4516) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复当可用内存配额为 0 时，TiCDC changefeed 可能因事件处理流水线死锁而停滞的问题 [#4899](https://github.com/pingcap/ticdc/issues/4899) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复当较晚的 changefeed remove 请求到达时，如果较早的 close 请求仍在处理中，TiCDC 可能跳过下游 remove-only 清理的问题 [#4825](https://github.com/pingcap/ticdc/issues/4825) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc -->
        - 修复当下游返回非标准 missing-table 错误码且 `tidb_cdc.ddl_ts_v1` 缺失时，TiCDC MySQL-compatible sink 可能卡住的问题 [#5003](https://github.com/pingcap/ticdc/issues/5003) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc -->
        - 修复当 Kafka sink 初始化失败或 sink 被关闭时，TiCDC 可能泄漏 Kafka client 连接和后台资源的问题 [#12572](https://github.com/pingcap/tiflow/issues/12572) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc -->
        - 修复在复制大量活跃表时，TiCDC resolved-ts 延迟和 CPU 使用率可能周期性升高的问题 [#4887](https://github.com/pingcap/ticdc/issues/4887) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复当本地 EventService 移除 dispatcher 后 collector 又在本地重新注册该 dispatcher 时，TiCDC 复制可能停滞的问题 [#5088](https://github.com/pingcap/ticdc/issues/5088) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复在初始化 TiCDC Pulsar sink 且 producer 初始化失败时可能发生 panic 的问题 [#4937](https://github.com/pingcap/ticdc/issues/4937) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复路径被移除后，TiCDC 仍可能保留不准确的内存计数，从而导致 dynstream 中出现错误 pause 或 release 反馈的问题 [#4644](https://github.com/pingcap/ticdc/issues/4644) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc -->
        - 修复 TiCDC 在优雅处理 `SIGTERM` 关闭时以 code 1 退出的问题 [#4563](https://github.com/pingcap/ticdc/issues/4563) @[pingyu](https://github.com/pingyu) <!-- component: cdc -->
        - 修复由于 redo 配置未正确初始化，TiCDC 可能无法启动 redo log sink 的问题 [#4512](https://github.com/pingcap/ticdc/issues/4512) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc -->
        - 修复 TiCDC 在应用包含 `CURRENT_TIMESTAMP` 等时间相关默认值列的 redo DDL 事件时可能发生 panic 的问题 [#4699](https://github.com/pingcap/ticdc/issues/4699) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复当多个 TiCDC 集群共享同一 PD/etcd 且 cluster ID 存在前缀关系时，TiCDC 在重启后可能加载其他集群 changefeed 的问题 [#4756](https://github.com/pingcap/ticdc/issues/4756) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复 TiCDC 在 bootstrap 和 failover 期间 redo readiness 中的数据竞争问题，该问题可能导致 failover 任务上报 `DATA RACE` 告警 [#4402](https://github.com/pingcap/ticdc/issues/4402) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc -->
        - 修复当未显式指定源数据库名时，TiCDC 无法复制跨库 `RENAME TABLE` 操作的问题 [#4424](https://github.com/pingcap/ticdc/issues/4424) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复当 log puller 遇到临时性 gRPC `EOF` 错误时，TiCDC changefeed 可能失败或卡住的问题 [#4880](https://github.com/pingcap/ticdc/issues/4880) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复当同步超大数量表时，TiCDC changefeed 初始化缓慢且 maintainer 延迟过高的问题 [#4951](https://github.com/pingcap/ticdc/issues/4951) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc -->
        - 修复查询不存在 changefeed 时，TiCDC CLI 不返回错误的问题 [#4648](https://github.com/pingcap/ticdc/issues/4648) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复调用 TiCDC `unsafe/service_gc_safepoint` API 时意外关闭 PD client 的问题 [#4638](https://github.com/pingcap/ticdc/issues/4638) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复在 bootstrap 失败后，TiCDC 重试 maintainer bootstrap 时可能发生 panic 的问题，现在 changefeed 会上报原始错误而不是直接崩溃 [#4509](https://github.com/pingcap/ticdc/issues/4509) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复在 stale lock 解析期间，TiCDC 可能留下未解析的 shared lock，从而影响 nextgen 部署中 shared-lock 的兼容性问题 [#5206](https://github.com/pingcap/ticdc/issues/5206) @[wfxr](https://github.com/wfxr) <!-- component: cdc -->
        - 修复 dispatcher 被移除后，TiCDC 仍可能意外重新调度该 dispatcher 的问题 [#4874](https://github.com/pingcap/ticdc/issues/4874) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc -->
        - 修复在重启后，如果重新创建的 dispatcher 从过期 checkpoint 启动，TiCDC 可能留下数据复制缺口的问题 [#3846](https://github.com/pingcap/ticdc/issues/3846) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc -->
        - 修复处理 coordinator 消息时，TiCDC 可能卡住并失去响应的问题 [#4440](https://github.com/pingcap/ticdc/issues/4440) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复 create、pause 和 remove changefeed 操作在请求上下文被取消后，仍可能长时间挂起或卡住的问题 [#4417](https://github.com/pingcap/ticdc/issues/4417) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复在 log pulling 期间处理 fast region error 或 replication worker shutdown 时可能发生 panic 的问题 [#4472](https://github.com/pingcap/ticdc/issues/4472) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复在启用 syncpoint 且频繁执行 DDL 的工作负载中，TiCDC 处理重复 block status 请求可能耗时过长，导致 maintainer slow log 和 barrier 处理延迟的问题 [#4957](https://github.com/pingcap/ticdc/issues/4957) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc -->
        - 修复在 etcd 集群成员变更后，TiCDC `cli changefeed list` 可能展示来自不同集群 changefeed 的问题 [#5137](https://github.com/pingcap/ticdc/issues/5137) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复在关闭过程中仍有任务被提交或重新调度时，TiCDC thread pool 关闭可能卡住的问题 [#4640](https://github.com/pingcap/ticdc/issues/4640) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复在某些 DDL（如 `CREATE TABLE ... LIKE ...`）场景下，当 dispatcher 的 `WAITING` 状态被 maintainer 暂时忽略时，TiCDC 需要等待约 5 秒才推进 barrier 的问题 [#4810](https://github.com/pingcap/ticdc/issues/4810) @[zier-one](https://github.com/zier-one) <!-- component: cdc -->
        - 修复在暂停并恢复大量 changefeed 后，TiCDC changefeed 延迟增加且 CPU 使用率升高的问题 [#4653](https://github.com/pingcap/ticdc/issues/4653) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复当未显式指定源表 schema 时，TiCDC 无法复制跨库 `CREATE TABLE ... LIKE` 语句的问题 [#5025](https://github.com/pingcap/ticdc/issues/5025) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复当视图定义中使用未限定的源表名时，TiCDC 复制跨 schema `CREATE VIEW` 语句可能出错，导致下游复制失败或视图引用错误表的问题 [#5026](https://github.com/pingcap/ticdc/issues/5026) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复在 PD 节点扩缩容后，TiCDC 使用错误 etcd endpoint，导致已移除 PD 成员被重复加回的问题 [#12368](https://github.com/pingcap/tiflow/issues/12368) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复当提交无效 global checkpoint 时，TiCDC redo dispatcher 可能卡在 `Initializing` 状态，导致 redo 元数据停止推进的问题 [#4703](https://github.com/pingcap/ticdc/issues/4703) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc -->
        - 修复处理超大数量表时，TiCDC changefeed 初始化缓慢的问题 [#5014](https://github.com/pingcap/ticdc/issues/5014) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复在最后一个 changefeed 被移除后，TiCDC 仍可能在 PD 中残留过期集群级 service GC safepoint，从而阻塞上游 GC 推进的问题 [#4610](https://github.com/pingcap/ticdc/issues/4610) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc -->
        - 修复当 `MultipleTableInfos` 非空时，TiCDC 可能无法正确解码或错误处理多表 DDL 事件的问题 [#4415](https://github.com/pingcap/ticdc/issues/4415) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc -->
        - 修复 TiCDC 在复制 `EXCHANGE PARTITION` DDL 语句时，会破坏包含转义反引号的分区名的问题 [#4450](https://github.com/pingcap/ticdc/issues/4450) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复在并发更新 subscription checkpoint 时，TiCDC 可能在 event store 中生成乱序 checkpoint 更新，导致复制进度跟踪不一致的问题 [#4992](https://github.com/pingcap/ticdc/issues/4992) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc -->
        - 修复当 EventCollector 在关闭期间仍接收消息时，TiCDC 可能发生死锁并阻塞清理的问题 [#4434](https://github.com/pingcap/ticdc/issues/4434) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复在复制匿名 `ADD INDEX` DDL 语句时，TiCDC 可能在下游生成不一致索引名的问题，尤其是在重试或复制 `CREATE TABLE LIKE` 场景下 [#2327](https://github.com/pingcap/ticdc/issues/2327) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复当连接 watchdog 中止后，TiCDC 可能保留过期 CDC 连接，导致连接清理延迟，并在 sink 内存耗尽时使 changefeed 复制卡住的问题 [#19610](https://github.com/tikv/tikv/issues/19610) @[wk989898](https://github.com/wk989898) <!-- component: cdc -->
        - 修复 TiCDC 中重新注册的 capture 在重新上线后，仍可能因过期的延迟删除 tombstone 再次被移除的问题 [#4695](https://github.com/pingcap/ticdc/issues/4695) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc -->

    + Dumpling

        - 修复当 `--rows/-r` 或 `--filesize/-F` 与 `--output-filename-template` 一起使用，且模板在条件块外未包含独立 `{{.Index}}` 时，Dumpling 可能覆盖 chunk 文件并生成不完整导出结果的问题 [#68611](https://github.com/pingcap/tidb/issues/68611) @[D3Hunter](https://github.com/D3Hunter) <!-- component: dumpling -->
