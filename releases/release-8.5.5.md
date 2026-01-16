---
title: TiDB 8.5.5 Release Notes
summary: 了解 TiDB 8.5.5 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.5 Release Notes

发版日期：2026 年 1 月 15 日

TiDB 版本：8.5.5

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://pingkai.cn/download#tidb-community)

## 新功能

### 性能

* 大幅提升特定有损 DDL 操作（例如 `BIGINT → INT`、`CHAR(120) → VARCHAR(60)`）的执行效率：在未发生数据截断的前提下，这类操作的执行耗时可从数小时缩短至分钟级、秒级甚至毫秒级，性能提升可达到数十倍至数十万倍 [#63366](https://github.com/pingcap/tidb/issues/63366) @[wjhuang2016](https://github.com/wjhuang2016), @[tangenta](https://github.com/tangenta), @[fzzf678](https://github.com/fzzf678)

    优化策略包括：

    - 在严格 SQL 模式下，预先检查类型转换过程中是否存在数据截断风险。
    - 若不存在数据截断风险，则仅更新元数据，避免不必要的索引重建。
    - 如需重建索引，则采用更高效的 Ingest 流程，大幅提升索引重建性能。

  以下为性能提升示例。该示例基于一张包含 114 GiB 数据、6 亿行记录的表进行基准测试。测试集群由 3 个 TiDB 节点、6 个 TiKV 节点和 1 个 PD 节点组成，所有节点均配置 16 核 CPU 和 32 GiB 内存。

    | 场景 | 操作类型 | 优化前 | 优化后 | 性能提升 |
    |------|----------|--------|--------|----------|
    | 无索引列 | `BIGINT → INT` | 2 小时 34 分钟 | 1 分 5 秒 | 142 倍 |
    | 有索引列 | `BIGINT → INT` | 6 小时 25 分钟 | 0.05 秒 | 460,000 倍 |
    | 有索引列 | `CHAR(120) → VARCHAR(60)` | 7 小时 16 分钟 | 12 分 56 秒 | 34 倍 |

    注：以上数据基于 DDL 执行过程中未发生数据截断的前提。对于字符集之间的类型转换，有符号与无符号整数类型之间的转换，或是包含 TiFlash 副本的表，上述优化不适用。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-modify-column.md)。

* 优化了存在大量外键场景下的 DDL 性能，逻辑 DDL 性能最高可提升 25 倍 [#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD)

    在 v8.5.5 版本之前，在超大规模表场景下（如集群表总量达 1000 万级别且包含数十万张外键表），创建表或添加列等逻辑 DDL 操作的 QPS 会下降至 4 左右。这导致多租户 SaaS 等场景下的运维效率非常低。

    v8.5.5 版本针对该场景进行了专项优化。测试数据显示，在拥有 1000 万张表（其中 20 万张含外键）的极端环境下，逻辑 DDL 的处理性能可稳定保持在 100 QPS，相比之前版本提升了 25 倍，显著增强了超大规模集群的运维响应能力。

* 支持将索引查询下推到 TiKV，提升查询性能 [#62575](https://github.com/pingcap/tidb/issues/62575) @[lcwangchao](https://github.com/lcwangchao)

    TiDB 从 v8.5.5 开始支持通过 [Optimizer Hints](/optimizer-hints.md) 将索引查询算子 `IndexLookUp` 下推到 TiKV 节点执行，从而减少远程调用次数并提升查询性能。实际性能提升比例因业务场景而异，需要进行测试验证。

    如果需要显式指示优化器将指定表的索引查询下推到 TiKV，可以使用 [`INDEX_LOOKUP_PUSHDOWN(t1_name, idx1_name [, idx2_name ...])`](https://docs.pingcap.com/zh/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--从-v855-版本开始引入) Hint。建议将该 Hint 与表的 AFFINITY 属性配合使用，例如为普通表设置 `AFFINITY="table"`，为分区表设置 `AFFINITY="partition"`。

    如果需要禁止某个表的索引查询下推到 TiKV，可以使用 [`NO_INDEX_LOOKUP_PUSHDOWN(t1_name)`](https://docs.pingcap.com/zh/tidb/v8.5/optimizer-hints#no_index_lookup_pushdownt1_name-从-v855-版本开始引入) Hint。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--从-v855-版本开始引入)。

* 支持表级数据亲和性 (AFFINITY)，提升查询性能（实验特性） [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024)

    从 v8.5.5 起，你可以在创建或修改表时将 `AFFINITY` 选项设置为 `table` 或 `partition`。配置后，PD 会将同一张表或同一个分区的 Region 归入同一个亲和性分组，并在调度过程中优先将这些 Region 的 Leader 和 Voter 副本放置到相同的少数 TiKV 节点上。此时，通过在查询中使用 [`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/zh/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--从-v855-版本开始引入) Hint，可以显式指示优化器将索引查询下推到 TiKV 执行，从而减少跨节点分散查询带来的延迟，提升查询性能。

    需要注意的是，表级数据亲和性目前为实验特性，默认关闭。如需开启，请将 PD 配置项 [`schedule.affinity-schedule-limit`](https://docs.pingcap.com/zh/tidb/v8.5/pd-configuration-file#affinity-schedule-limit-从-v855-版本开始引入) 设置为大于 `0` 的值。该配置项用于控制 PD 同时可执行的亲和性调度任务数。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/table-affinity)。

* 按时间点恢复 (Point-in-time recovery, PITR) 支持从压缩后的日志备份中恢复，以加快恢复速度 [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen)

    从 v8.5.5 开始，压缩日志备份功能提供了离线压缩能力，将非结构化的日志备份数据转换为结构化的 SST 文件，从而实现以下改进：

    - **提升恢复性能**：SST 可以更快地导入到集群中。
    - **降低存储空间占用**：在压缩过程中会去除冗余数据。
    - **减少对业务的影响**：在确保 RPO (Recovery Point Objective) 的前提下，可以设置更长的全量备份间隔。

  更多信息，请参考[用户文档](/br/br-compact-log-backup.md)。

* 加速从备份中恢复系统表 [#58757](https://github.com/pingcap/tidb/issues/58757) @[Leavrth](https://github.com/Leavrth)

    从 v8.5.5 开始，对于从备份中恢复系统表，BR 引入了新参数 `--fast-load-sys-tables`，用物理恢复替代逻辑恢复。该参数开启状态下，BR 会完全替换或覆盖现有的系统表，而不是向其中写入数据，从而显著提升大规模部署场景下的数据恢复性能。

    更多信息，请参考[用户文档](/br/br-snapshot-guide.md#恢复-mysql-数据库下的表)。

### 稳定性

* 提升 TiKV 在网络抖动时的调度稳定性 [#9359](https://github.com/tikv/pd/issues/9359) @[okJiang](https://github.com/okJiang)

    从 v8.5.5 起，TiKV 引入网络慢节点检测与反馈机制。启用该机制后，TiKV 会探测节点之间的网络延时，计算网络慢节点分数，并将该分数上报给 PD。PD 基于该分数判断 TiKV 节点的网络状态，并进行相应的调度调整：当检测到某个 TiKV 节点存在网络抖动时，PD 会限制向该节点调度新的 Leader。如果网络抖动持续存在，PD 会主动将该节点上的现有 Leader 驱逐到其他 TiKV 节点，从而降低网络异常对集群的影响。

    更多信息，请参考[用户文档](/pd-control.md#scheduler-config-evict-slow-store-scheduler)。

### 高可用

* 为 PD 引入客户端熔断模式 (Circuit Breaker) [#8678](https://github.com/tikv/pd/issues/8678) @[Tema](https://github.com/Tema)

    为了防止 PD Leader 因重试风暴或类似的反馈循环而过载，TiDB 引入了熔断模式。当错误率达到预设阈值时，该模式会限制进入的流量，从而使系统能够恢复稳定。你可以通过系统变量 `tidb_cb_pd_metadata_error_rate_threshold_ratio` 来控制熔断器的触发。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855)。

### SQL 功能

* 支持在线修改分布式 `ADD INDEX` 任务的并发和吞吐 [#64947](https://github.com/pingcap/tidb/issues/64947) @[joechenrh](https://github.com/joechenrh)

    在 v8.5.5 之前，如果集群开启了分布式执行框架 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入)，TiDB 不支持在 `ADD INDEX` 任务执行期间修改该任务的 `THREAD`、`BATCH_SIZE` 和 `MAX_WRITE_SPEED` 参数。要调整这些参数，你需要先取消当前 `ADD INDEX` 任务，重新设置参数后再提交，效率较低。

    从 v8.5.5 起，在分布式 `ADD INDEX` 任务执行期间，你可以根据当前业务负载和对 `ADD INDEX` 性能的需求，通过 `ADMIN ALTER DDL JOBS` 语句在线灵活调整这些参数，而无需中断任务。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-admin-alter-ddl.md)。

### 数据库管理

* TiKV 支持优雅关闭 (graceful shutdown) [#17221](https://github.com/tikv/tikv/issues/17221) @[hujiatao0](https://github.com/hujiatao0)

    在关闭 TiKV 服务器时，TiKV 会在配置的等待期内尽量先将节点上的 Leader 副本转移到其他 TiKV 节点，然后再关闭。该等待期默认为 20 秒，可通过 [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入) 配置项进行调整。若达到该超时时间后仍有 Leader 未完成转移，TiKV 将跳过剩余 Leader 的转移，直接进入关闭流程。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入)。

* 提升进行中的日志备份与快照恢复的兼容性 [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger)

    从 v8.5.5 开始，当日志备份任务正在运行时，在满足特定条件的情况下，仍然可以执行快照恢复。这样，日志备份可以持续进行，无需在恢复数据期间中断。并且，恢复的数据可以被进行中的日志备份正常记录。

    更多信息，请参考[用户文档](/br/br-pitr-manual.md#进行中的日志备份与快照恢复的兼容性)。

* 支持从日志备份中进行表级恢复 [#57613](https://github.com/pingcap/tidb/issues/57613) @[Tristan1900](https://github.com/Tristan1900)

    从 v8.5.5 开始，你可以使用过滤器从日志备份中对单个表执行按时间点恢复 (PITR)。相比将整个集群恢复到指定时间点，表级恢复提供了更加灵活、且对业务影响更小的恢复方式。

    更多信息，请参考[用户文档](/br/br-pitr-manual.md#使用过滤器恢复)。

### 可观测性

* 在 Statement Summary Tables 和慢日志中增加存储引擎标识 [#61736](https://github.com/pingcap/tidb/issues/61736) @[henrybw](https://github.com/henrybw)

    当集群中同时部署了 TiKV 和 TiFlash 时，用户在数据库诊断和性能优化过程中经常需要根据存储引擎筛选 SQL 语句。例如，当用户发现 TiFlash 负载较高时，需要筛选出在 TiFlash 上运行的 SQL 语句，以便识别可能导致 TiFlash 负载过高的查询语句。为解决此需求，TiDB 从 v8.5.5 开始，在 Statement Summary Tables 和慢日志中新增了存储引擎标识字段。

    在 [Statement Summary Tables](/statement-summary-tables.md) 中新增的字段：

    * `STORAGE_KV`：值为 `1` 时表示该 SQL 语句访问了 TiKV。
    * `STORAGE_MPP`：值为 `1` 时表示该 SQL 语句访问了 TiFlash。

    在[慢日志](/identify-slow-queries.md)中新增的字段：

    * `Storage_from_kv`：值为 `true` 时表示该 SQL 语句访问了 TiKV。
    * `Storage_from_mpp`：值为 `true` 时表示该 SQL 语句访问了 TiFlash。

    该功能可以简化部分诊断和性能优化场景的工作流程，提升问题诊断效率。

    更多信息，请参考 [Statement Summary Tables](/statement-summary-tables.md) 和[慢日志](/identify-slow-queries.md)。

### 安全

* Backup & Restore (BR) 支持通过 Azure 托管标识 (Managed Identity, MI) 访问 Azure Blob Storage [#19006](https://github.com/tikv/tikv/issues/19006) @[RidRisR](https://github.com/RidRisR)

    从 v8.5.5 起，BR 支持使用 Azure 托管标识 (MI) 对 Azure Blob Storage 进行身份验证，无需使用静态 SAS Token。该方式实现了安全、无密钥且短期有效的认证，符合 Azure 安全最佳实践。

    利用该功能，BR 及内嵌于 TiKV 的 BR Worker 可直接从 Azure 实例元数据服务 (IMDS) 获取访问令牌，从而有效降低凭证泄露的风险，并简化本地或云上 Azure 环境中的凭据轮换管理。

    该功能适用于在 Azure Kubernetes Service (AKS) 或其他 Azure 环境中运行 TiDB 的场景，尤其是在备份和恢复操作需满足严格安全管控要求的企业环境中。

    更多信息，请参考[用户文档](/br/backup-and-restore-storages.md#鉴权)。

## 兼容性变更

对于新部署的 TiDB v8.5.4 集群（即不是从早于 v8.5.3 的版本升级而来的集群），你可以平滑升级到 v8.5.5。v8.5.5 的大多数变更对常规升级是安全的，但也包含了若干行为变更、MySQL 兼容性变更、系统变量变更、配置参数变更以及系统表变更。在升级前，请务必仔细阅读本节内容。

### 行为变更

* 从 v8.5.5 开始，在数据恢复期间，目标表的 Table Mode 会自动设置为 `restore`，处于 `restore` 模式的表禁止用户执行任何读写操作。当数据恢复完成后，Table Mode 会自动切换为 `normal` 状态，用户可以正常读写该表，从而确保数据恢复期间的任务稳定性和数据一致性。
* 从 v8.5.5 开始，当参数 `--load-stats` 设置为 `false` 时，BR 不再向 `mysql.stats_meta` 表写入恢复表的统计信息。你可以在恢复完成后手动执行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)，以更新相关统计信息。

### MySQL 兼容性

* 从 v8.5.5 起，数据表新增 `AFFINITY` 属性，用于控制表或分区数据的亲和性，可以通过 `CREATE TABLE` 或 `ALTER TABLE` 语句配置。更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/table-affinity)。
* 从 v8.5.5 起，TiDB 新增 `SHOW AFFINITY` 语句，用于查看表的亲和性信息。该语句是 TiDB 对 MySQL 语法的扩展。更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/sql-statement-show-affinity)。

### 系统变量

| 变量名  | 修改类型    | 描述 |
|--------|------------------------------|------|
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) | 修改 | 默认值从 `PREDICATE` 修改为 `ALL`，以提升 OLAP 和 HTAP 场景下的统计信息完整性。 |
| [`tidb_advancer_check_point_lag_limit`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_advancer_check_point_lag_limit-从-v855-版本开始引入) | 新增 | 控制日志备份任务 Checkpoint 的滞后时间限制，默认值为 `48h0m0s`。如果日志备份任务 Checkpoint 的滞后时间超过了限制，TiDB Advancer 会暂停该任务。 |
| [`tidb_cb_pd_metadata_error_rate_threshold_ratio`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_cb_pd_metadata_error_rate_threshold_ratio-从-v855-版本开始引入) | 新增 | 控制 TiDB 何时触发熔断器。默认值为 `0`，表示禁用熔断器。设置为 `0.01` 到 `1` 之间的值时，表示启用熔断器，当发送到 PD 的特定请求的错误率达到或超过该阈值时，熔断器会被触发。|
| [`tidb_index_lookup_pushdown_policy`](https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_index_lookup_pushdown_policy-从-v855-版本开始引入) |  新增  | 控制 TiDB 是否以及在什么条件下将 `IndexLookUp` 算子下推到 TiKV。默认值为 `hint-only`，表示仅在 SQL 中显式指定 [`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/zh/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--从-v855-版本开始引入) Hint 时，才将 `IndexLookUp` 算子下推到 TiKV。 |

### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`performance.enable-async-batch-get`](https://docs.pingcap.com/zh/tidb/v8.5/tidb-configuration-file#enable-async-batch-get-从-v855-版本开始引入) | 新增 | 控制 TiDB 是否使用异步方式执行 Batch Get 算子，默认值为 `false`。 |
| TiKV | [<code>rocksdb.\(defaultcf\|writecf\|lockcf\|raftcf\).level0-slowdown-writes-trigger</code>](/tikv-configuration-file.md#level0-slowdown-writes-trigger) | 修改 | 从 v8.5.5 起，当开启流控机制（[`storage.flow-control.enable`](/tikv-configuration-file.md#enable) 为 `true`）时，该配置项仅在其值大于 [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold) 时会被 `storage.flow-control.l0-files-threshold` 覆盖，以避免在调大流控阈值时削弱 RocksDB 的 compaction 加速机制。在 v8.5.4 以及之前版本中，当开启流控机制时，该配置项会被 `storage.flow-control.l0-files-threshold` 直接覆盖。 |
| TiKV | [<code>rocksdb.\(defaultcf\|writecf\|lockcf\|raftcf\).soft-pending-compaction-bytes-limit</code>](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1) | 修改 | 从 v8.5.5 起，当开启流控机制（[`storage.flow-control.enable`](/tikv-configuration-file.md#enable) 为 `true`）时，该配置项仅在其值大于 [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) 时会被 `storage.flow-control.soft-pending-compaction-bytes-limit` 覆盖，以避免在调大流控阈值时削弱 RocksDB 的 compaction 加速机制。在 v8.5.4 以及之前版本中，当开启流控机制时，该配置项会被 `storage.flow-control.soft-pending-compaction-bytes-limit` 直接覆盖。 |
| TiKV | [`readpool.cpu-threshold`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#cpu-threshold-从-v855-版本开始引入) | 新增 | 限制统一处理读请求的线程池 (UnifyReadPool) 可使用的最大 CPU 资源比例。默认值为 `0.0`，表示不限制 UnifyReadPool 的 CPU 资源比例，该线程池的规模完全由繁忙线程伸缩算法决定，该算法会根据当前处理任务的线程数量动态调整。 |
| TiKV | [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入) | 新增 | 控制 TiKV 优雅关闭 (graceful shutdown) 的超时时长，默认值为 `20s`。 |
| TiKV | [`server.inspect-network-interval`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#inspect-network-interval-从-v855-版本开始引入) | 新增 | 控制 TiKV HealthChecker 主动向 PD 以及其他 TiKV 节点发起网络探测的周期，默认值为 `100ms`。 |
| PD | [`schedule.max-affinity-merge-region-size`](https://docs.pingcap.com/zh/tidb/v8.5/pd-configuration-file#max-affinity-merge-region-size-从-v855-版本开始引入) | 新增 | 控制属于同一[亲和性](https://docs.pingcap.com/zh/tidb/v8.5/table-affinity)分组中相邻的小 Region 自动合并的阈值，默认值为 `256`，单位为 MiB。 |
| PD  | [`schedule.affinity-schedule-limit`](https://docs.pingcap.com/zh/tidb/v8.5/pd-configuration-file#affinity-schedule-limit-从-v855-版本开始引入) | 新增 | 控制同时进行的[亲和性](https://docs.pingcap.com/zh/tidb/v8.5/table-affinity)调度任务数量，默认值为 `0`，表示亲和性调度默认关闭。 |
| BR | [`--checkpoint-storage`](/br/br-checkpoint-restore.md#实现细节将断点数据存储在下游集群) | 新增 | 用于指定断点数据存储的外部存储。 |
| BR | [`--fast-load-sys-tables`](/br/br-snapshot-guide.md#恢复-mysql-数据库下的表) | 新增 | 用于在全新的集群上物理恢复系统表。该参数默认开启。 |
| BR | [`--filter`](/br/br-pitr-manual.md#使用过滤器恢复) | 新增 | 用于恢复特定的数据库或表。 |

### 系统表

* 系统表 [`INFORMATION_SCHEMA.TABLES`](/information-schema/information-schema-tables.md) 和 [`INFORMATION_SCHEMA.PARTITIONS`](/information-schema/information-schema-partitions.md) 新增 `TIDB_AFFINITY` 列，用于查看数据亲和性等级。

### 其他

* 为了提升 TiDB 性能，TiDB 的 Go 编译器版本从 go1.23.6 升级到了 go1.25.5。如果你是 TiDB 的开发者，为了能保证顺利编译，请对应升级你的 Go 编译器版本。

* 使用 BR v8.5.5 对较低版本的 TiDB 集群（例如 v8.5.4 或 v8.1.2）执行 PITR 恢复时，日志恢复阶段会失败并报错。

    数据全量备份与恢复不受此问题影响。

    建议使用与目标 TiDB 集群版本一致的 BR 版本。例如，在 TiDB v8.5.4 集群上执行 PITR 时，使用 BR v8.5.4。

## 改进提升

+ TiDB

    - 优化 `IMPORT INTO` 在遇到编码错误时的报错信息，帮助用户更准确地定位问题 [#63763](https://github.com/pingcap/tidb/issues/63763) @[D3Hunter](https://github.com/D3Hunter)
    - 改进 Parquet 文件的解析机制，提升 Parquet 格式数据的导入性能 [#62906](https://github.com/pingcap/tidb/issues/62906) @[joechenrh](https://github.com/joechenrh)
    - 将 `tidb_analyze_column_options` 的默认值修改为 `ALL`，默认对所有列进行统计信息收集 [#64992](https://github.com/pingcap/tidb/issues/64992) @[0xPoe](https://github.com/0xPoe)
    - 优化 `IndexHashJoin` 算子的执行逻辑，在特定 JOIN 场景下采用增量处理以避免一次性加载大量数据，显著降低内存占用并提升执行性能 [#63303](https://github.com/pingcap/tidb/issues/63303) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - 优化分布式执行框架 (Distributed eXecution Framework, DXF) 内部 SQL 语句的 CPU 使用率 [#59344](https://github.com/pingcap/tidb/issues/59344) @[D3Hunter](https://github.com/D3Hunter)
    - 提升 `expression.Contains` 函数的性能 [#61373](https://github.com/pingcap/tidb/issues/61373) @[hawkingrei](https://github.com/hawkingrei)

+ TiKV

    - 为统一读取池 (Unified Read Pool) 引入 CPU 感知扩缩容机制，以避免在热点读取负载下出现 CPU 饥饿 (CPU Starvation) 问题 [#18464](https://github.com/tikv/tikv/issues/18464) @[mittalrishabh](https://github.com/mittalrishabh)
    - 在慢节点评分 (Slow Score) 中增加网络延迟感知，避免将 Leader 调度到网络环境不稳定的 TiKV 节点上 [#18797](https://github.com/tikv/tikv/issues/18797) @[okJiang](https://github.com/okJiang)
    - 优化静默 Region (Hibernate Region) 的行为，允许 Leader 在获得多数派投票后立即进入静默状态，无需等待离线的非投票副本 (Non-voter Peers) [#19070](https://github.com/tikv/tikv/issues/19070) @[jiadebin](https://github.com/jiadebin)
    - 在 TiKV 内存占用高时，对 BR 的日志恢复请求进行限流，防止 TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

+ PD

    - 优化了高基数指标，降低 PD 的内存占用和监控系统压力 [#9357](https://github.com/tikv/pd/issues/9357) @[rleungx](https://github.com/rleungx)
    - 优化时间戳推进和 Leader 选举的逻辑 [#9981](https://github.com/tikv/pd/issues/9981) @[bufferflies](https://github.com/bufferflies)
    - 支持按照存储引擎（TiKV 或 TiFlash）批量配置 Store Limit [#9970](https://github.com/tikv/pd/issues/9970) @[bufferflies](https://github.com/bufferflies)
    - 为 `pd_cluster_status` 指标添加 `store` 标签 [#9855](https://github.com/tikv/pd/issues/9855) @[SerjKol80](https://github.com/SerjKol80)

+ Tools

    + TiCDC

        - 增强 Changefeed 的配置检查逻辑，在创建或更新 Changefeed 时，若 Dispatcher 配置引用的列不存在，TiCDC 会直接报错并拒绝操作，避免任务运行失败 [#12253](https://github.com/pingcap/tiflow/issues/12253) @[wk989898](https://github.com/wk989898)

## 错误修复

+ TiDB

    - 修复 TiDB 初始化时无法读取最新的 `tidb_mem_quota_binding_cache` 变量值进行初始化绑定的问题 [#65381](https://github.com/pingcap/tidb/issues/65381) @[qw4990](https://github.com/qw4990)
    - 修复在 `extractBestCNFItemRanges` 中错误地跳过候选项，导致查询范围计算不精确的问题 [#62547](https://github.com/pingcap/tidb/issues/62547) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `plan replayer` 无法加载绑定的问题 [#64811](https://github.com/pingcap/tidb/issues/64811) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `PointGet` 在有足够内存的情况下没有复用 chunk，导致不必要的内存分配的问题 [#63920](https://github.com/pingcap/tidb/issues/63920) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `LogicalProjection.DeriveStats` 分配过多内存的问题 [#63810](https://github.com/pingcap/tidb/issues/63810) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当查询发生 panic 时，`plan replayer` 无法正常导出 (dump) 的问题 [#64835](https://github.com/pingcap/tidb/issues/64835) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在特定场景下，TTL 表的 `SHOW CREATE TABLE` 输出中，属性顺序显示不正确的问题 [#64876](https://github.com/pingcap/tidb/issues/64876) @[YangKeao](https://github.com/YangKeao)
    - 修复 TTL 任务超时时，其执行摘要信息为空的问题 [#61509](https://github.com/pingcap/tidb/issues/61509) @[YangKeao](https://github.com/YangKeao)
    - 修复当计划缓存开启时，关联子查询可能产生非预期的全表扫描的问题 [#64645](https://github.com/pingcap/tidb/issues/64645) @[winoros](https://github.com/winoros)
    - 修复系统表导致表健康度监控不正确的问题 [#57176](https://github.com/pingcap/tidb/issues/57176), [#64080](https://github.com/pingcap/tidb/issues/64080) @[0xPoe](https://github.com/0xPoe)
    - 修复关闭自动更新表的统计信息后 (`tidb_enable_auto_analyze = OFF`)，`mysql.tidb_ddl_notifier` 不能被清理的问题 [#64038](https://github.com/pingcap/tidb/issues/64038) @[0xPoe](https://github.com/0xPoe)
    - 修复在 `newLocalColumnPool` 中重复分配列的问题 [#63809](https://github.com/pingcap/tidb/issues/63809) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `syncload` 加载失败警告日志无效的问题 [#63880](https://github.com/pingcap/tidb/issues/63880) @[0xPoe](https://github.com/0xPoe)
    - 修复手动停止正在执行事务的连接时，可能导致 TiDB 发生 panic 而异常退出的问题 [#63956](https://github.com/pingcap/tidb/issues/63956) @[wshwsh12](https://github.com/wshwsh12)
    - 修复缓存表在读取 TiFlash 副本时，可能出现 goroutine 和内存泄漏的问题 [#63329](https://github.com/pingcap/tidb/issues/63329) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复执行 `ALTER TABLE child CHANGE COLUMN` 修改列后，外键 (Foreign Key) 没有更新的问题 [#59705](https://github.com/pingcap/tidb/issues/59705) @[fzzf678](https://github.com/fzzf678)
    - 修复解码旧版本 TiDB 的 `RENAME TABLE` 任务参数时出现错误的问题 [#64413](https://github.com/pingcap/tidb/issues/64413) @[joechenrh](https://github.com/joechenrh)
    - 修复当 BR 恢复失败时，未能正常设置自增 ID (Rebase) 的问题 [#60804](https://github.com/pingcap/tidb/issues/60804) @[joechenrh](https://github.com/joechenrh)
    - 修复在升级时 TiDB 节点可能会卡住的问题 [#64539](https://github.com/pingcap/tidb/issues/64539) @[joechenrh](https://github.com/joechenrh)
    - 修复当没有索引数据时，admin check 没有报错的问题 [#63698](https://github.com/pingcap/tidb/issues/63698) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复执行 `MODIFY COLUMN` 修改排序规则导致数据索引不一致的问题 [#61668](https://github.com/pingcap/tidb/issues/61668) @[tangenta](https://github.com/tangenta)
    - 修复多个 schema 变更时，内嵌于 DDL 的 Analyze 特性没有启用的问题 [#65040](https://github.com/pingcap/tidb/issues/65040) @[joechenrh](https://github.com/joechenrh)
    - 修复取消 `ADD INDEX` 任务后，分布式执行框架 (Distributed eXecution Framework, DXF) 任务没有取消的问题 [#64129](https://github.com/pingcap/tidb/issues/64129) @[tangenta](https://github.com/tangenta)
    - 修复在判断是否加载包含外键的表信息时，校验逻辑不正确的问题 [#60044](https://github.com/pingcap/tidb/issues/60044) @[JQWong7](https://github.com/JQWong7)
    - 修复在复制表信息时，外键相关字段初始化不正确的问题 [#60044](https://github.com/pingcap/tidb/issues/60044) @[JQWong7](https://github.com/JQWong7)
    - 修复跨数据库重命名表格后，auto ID 设置不正确的问题 [#64561](https://github.com/pingcap/tidb/issues/64561) @[joechenrh](https://github.com/joechenrh)
    - 修复错误处理 meta key 导致 CPU 负载过高的问题 [#64323](https://github.com/pingcap/tidb/issues/64323) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 TiDB Lightning 在 schema file 缺失末尾分号时未正常报错的问题 [#63414](https://github.com/pingcap/tidb/issues/63414) @[GMHDBJD](https://github.com/GMHDBJD)
    - 修复在启用全局排序 (Global Sort) 时，执行 `IMPORT INTO` 读取文件导致死循环的问题 [#61177](https://github.com/pingcap/tidb/issues/61177) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复在执行 `IMPORT INTO` 时，处理生成列过程中发生 panic 的问题 [#64657](https://github.com/pingcap/tidb/issues/64657) @[D3Hunter](https://github.com/D3Hunter)
    - 修复当一个 SQL 语句包含多个 `AS OF TIMESTAMP` 表达式时，可能误报错的问题 [#65090](https://github.com/pingcap/tidb/issues/65090) @[you06](https://github.com/you06)
    - 修复查询 `information_schema.tables` 可能出现 OOM 问题，优化系统表查询过程中的内存使用监控 [#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)

+ TiKV

    - 修复 Analyze 请求的 `KV Cursor Operations` 监控指标始终为 `0` 的问题 [#19206](https://github.com/tikv/tikv/issues/19206) @[glorv](https://github.com/glorv)
    - 修复 Leader 变更后 Region 心跳可能向 PD 上报错误的 Region 大小或 key 统计信息的问题 [#19180](https://github.com/tikv/tikv/issues/19180) @[glorv](https://github.com/glorv)
    - 通过从 Unsafe Recovery 降级列表中移除 tombstone 状态的 TiFlash Learner，修复 Unsafe Recovery 进程卡住的问题 [#18458](https://github.com/tikv/tikv/issues/18458) @[v01dstar](https://github.com/v01dstar)
    - 修复在持续写入期间快照可能被反复取消，从而阻塞副本恢复的问题 [#18872](https://github.com/tikv/tikv/issues/18872) @[exit-code-1](https://github.com/exit-code-1)
    - 修复流控阈值过高导致 compaction 变慢的问题 [#18708](https://github.com/tikv/tikv/issues/18708) @[hhwyt](https://github.com/hhwyt)
    - 修复特定场景下 Raft peer 可能过早进入休眠状态，导致 TiKV 重启后 peer 保持繁忙并阻塞 Leader 迁移的问题 [#19203](https://github.com/tikv/tikv/issues/19203) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - 修复节点在上线过程中可能无法被移除的问题 [#8997](https://github.com/tikv/pd/issues/8997) @[lhy1024](https://github.com/lhy1024)
    - 修复大量的 Leader 迁移可能导致 Region 大小出现跳变的问题 [#10014](https://github.com/tikv/pd/issues/10014) @[lhy1024](https://github.com/lhy1024)
    - 修复调度过程中可能导致 PD panic 的问题 [#9951](https://github.com/tikv/pd/issues/9951) @[bufferflies](https://github.com/bufferflies)
    - 修复导入过程中数据不均衡的问题 [#9088](https://github.com/tikv/pd/issues/9088) @[GMHDBJD](https://github.com/GMHDBJD)
    - 修复开启 Active PD Follower 特性后，若请求在 Follower 节点处理失败，无法正确回退到 Leader 节点重试的问题 [#64933](https://github.com/pingcap/tidb/issues/64933) @[okJiang](https://github.com/okJiang)
    - 修复 PD 微服务模式下部分请求未能正确转发的问题 [#9825](https://github.com/tikv/pd/issues/9825) @[lhy1024](https://github.com/lhy1024)
    - 修复 `tso` 和 `scheduling` 微服务中 TLS 配置加载不正确导致连接失败的问题 [#9367](https://github.com/tikv/pd/issues/9367) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 修复在 BR 恢复数据的过程中，TiFlash 可能 panic 的问题 [#10606](https://github.com/pingcap/tiflash/issues/10606) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复在 BR 恢复数据的过程中，TiFlash 不能充分利用超过 16 核 CPU 进行数据恢复的问题 [#10605](https://github.com/pingcap/tiflash/issues/10605) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 `GROUP_CONCAT` 触发落盘时可能导致 TiFlash 异常退出的问题 [#10553](https://github.com/pingcap/tiflash/issues/10553) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)

+ Tools

    + Backup & Restore (BR)

        - 修复集群中存在大量 Region 时，开启日志备份导致内存占用过高的问题 [#18719](https://github.com/tikv/tikv/issues/18719) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 Azure SDK 无法从环境变量中获取合适的密钥的问题 [#18206](https://github.com/tikv/tikv/issues/18206) @[YuJuncen](https://github.com/YuJuncen)
        - 修复执行 `restore point` 时无法正确恢复外键的问题 [#61642](https://github.com/pingcap/tidb/issues/61642) @[Leavrth](https://github.com/Leavrth)
        - 修复备份集群与目标集群的系统表字符集排序规则不兼容导致恢复失败的问题，通过添加 `--sys-check-collation` 参数支持将权限表从 v6.5 恢复到 v7.5 [#64667](https://github.com/pingcap/tidb/issues/64667) @[Leavrth](https://github.com/Leavrth)
        - 修复在 `restore point` 失败后，即使操作安全也无法执行 `restore log` 的问题 [#64908](https://github.com/pingcap/tidb/issues/64908) @[RidRisR](https://github.com/RidRisR)
        - 修复当日志备份数据与全量备份数据混合时，从 checkpoint 进行 `restore point` 可能导致 panic 的问题 [#58685](https://github.com/pingcap/tidb/issues/58685) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复同步数据到对象存储时，可能因未正确捕获 Writer 关闭错误而导致数据丢失的问题 [#12436](https://github.com/pingcap/tiflow/issues/12436) @[wk989898](https://github.com/wk989898)
        - 修复同步分区表的 `TRUNCATE` 操作可能导致 Changefeed 失败的问题 [#12430](https://github.com/pingcap/tiflow/issues/12430) @[wk989898](https://github.com/wk989898)
        - 修复同步多表重命名 DDL 时，下游执行顺序可能不正确的问题 [#12449](https://github.com/pingcap/tiflow/issues/12449) @[wlwilliamx](https://github.com/wlwilliamx)
        - 升级 `aws-sdk-go-v2` 依赖版本，以修复使用 Glue Schema Registry 时可能遇到的连接错误 [#12424](https://github.com/pingcap/tiflow/issues/12424) @[wk989898](https://github.com/wk989898)
        - 修复 TiKV CDC 组件重启后可能无法正确释放内存配额，导致 Changefeed 任务卡住的问题 [#18169](https://github.com/tikv/tikv/issues/18169) @[asddongmen](https://github.com/asddongmen)
        - 修复 TiKV CDC 在增量扫描任务堆积时，gRPC 连接可能因误判为空闲而被异常断开的问题 [#18915](https://github.com/tikv/tikv/issues/18915) @[asddongmen](https://github.com/asddongmen)
