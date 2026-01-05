---
title: TiDB 8.5.5 Release Notes
summary: 了解 TiDB 8.5.5 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.5 Release Notes

发版日期：2026 年 xx 月 xx 日

TiDB 版本：8.5.5

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://pingkai.cn/download#tidb-community)

## 新功能

### 性能

* 大幅提升特定有损 DDL 操作（例如 `BIGINT → INT`、`CHAR(120) → VARCHAR(60)`）的执行效率：在未发生数据截断的前提下，这类操作的执行耗时可从数小时缩短至分钟级、秒级甚至毫秒级，性能提升可达到数十倍至数十万倍 [#63366](https://github.com/pingcap/tidb/issues/63366) [@wjhuang2016](https://github.com/wjhuang2016), [@tangenta](https://github.com/tangenta), [@fzzf678](https://github.com/fzzf678)**tw@qiancai** <!--2292-->

    优化策略包括：

    - 在严格 SQL 模式下，预先检查类型转换过程中是否存在数据截断风险。
    - 若不存在数据截断风险，则仅更新元数据，尽量避免索引重建。
    - 如需重建索引，则采用更高效的 Ingest 流程，大幅提升索引重建性能。

    以下为性能提升示例。该示例基于一张包含 114 GiB 数据、6 亿行记录的表进行基准测试。测试集群由 3 个 TiDB 节点、6 个 TiKV 节点和 1 个 PD 节点组成，所有节点均为 16 核 CPU、32 GiB 内存。

    | 场景 | 操作类型 | 优化前 | 优化后 | 性能提升 |
    |------|----------|--------|--------|----------|
    | 无索引列 | `BIGINT → INT` | 2 小时 34 分 | 1 分 5 秒 | 142 倍 |
    | 有索引列 | `BIGINT → INT` | 6 小时 25 分 | 0.05 秒 | 460,000 倍 |
    | 有索引列 | `CHAR(120) → VARCHAR(60)` | 7 小时 16 分 | 12 分 56 秒 | 34 倍 |

    注：以上数据基于 DDL 执行过程中未发生数据截断的前提。对于包含 TiFlash 副本的表，以及涉及有符号与无符号整数类型相互转换（signed ↔ unsigned）的变更场景，上述优化不适用。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-modify-column.md)。

* 优化了存在大量外键场景下的 DDL 性能，逻辑 DDL 性能最高可提升 25 倍 [#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1896-->

    在 v8.5.5 版本之前，在超大规模表场景下（如集群表总量达 1000 万级别且包含数十万张外键表），创建表或添加列等逻辑 DDL 操作的 QPS 会下降至 4 左右。这导致多租户 SaaS 等场景下的运维效率非常低。

    v8.5.5 版本针对该场景进行了专项优化。测试数据显示，在拥有 1000 万张表（其中 20 万张含外键）的极端环境下，逻辑 DDL 的处理性能可稳定保持在 100 QPS，相比之前版本提升了 25 倍，显著增强了超大规模集群的运维响应能力。

* 支持将索引查询下推到 TiKV 提升查询性能 [#62575](https://github.com/pingcap/tidb/issues/62575) @[lcwangchao](https://github.com/lcwangchao) **tw@Oreoxmt** <!--1899-->

    TiDB 从 v8.5.5 开始支持通过 Optimizer Hints 将索引查询 `IndexLookUp` 下推到 TiKV 节点执行，从而减少远程调用次数并提升查询性能。实际性能提升比例因业务场景而异，需要进行测试验证。

    使用 [`INDEX_LOOKUP_PUSHDOWN(t1_name, idx1_name [, idx2_name ...])`](https://docs.pingcap.com/zh/tidb/stable/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--从-v855-版本开始引入) Hint，可以显式指示优化器将指定表的索引查询下推到 TiKV。建议将该 Hint 与表的 AFFINITY 属性配合使用，例如为普通表设置 `AFFINITY="table"`，为分区表设置 `AFFINITY="partition"`。

    如果需要禁止某个表的索引查询下推到 TiKV，可以使用 [`NO_INDEX_LOOKUP_PUSHDOWN(t1_name)`](https://docs.pingcap.com/zh/tidb/stable/optimizer-hints#no_index_lookup_pushdownt1_name-从-v855-版本开始引入) Hint。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/stable/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--从-v855-版本开始引入)。

* 支持表级数据亲和性（AFFINITY），提升查询性能（实验特性） [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024) **tw@qiancai** <!--2317-->

    从 v8.5.5 起，在创建或修改表时，你可以设置表的 `AFFINITY` 选项为 `table` 或 `partition`。设置后，PD 会将同一张表或同一个分区的 Region 归入同一个亲和性分组，并在调度过程中优先将这些 Region 的 Leader 和 Voter 副本放置到相同的少数 TiKV 节点上。此时，通过在查询中使用 [`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/zh/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--从-v855-版本开始引入) Hint，可以显式指示优化器将索引查询下推到 TiKV 执行，减少跨节点分散查询带来的延迟，提升查询性能。

    需要注意的是，表级数据亲和性目前为实验特性，默认关闭。如需开启，请将 PD 配置项 [`schedule.affinity-schedule-limit`](https://docs.pingcap.com/zh/tidb/v8.5/pd-configuration-file#affinity-schedule-limit-从-v855-版本开始引入) 设置为大于 `0` 的值。该配置项用于控制 PD 同时可进行的亲和性调度任务数。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/table-affinity)。

* 按时间点恢复 (Point-in-time recovery, PITR) 支持从压缩后的日志备份中恢复，以加快恢复速度 [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen) **tw@lilin90** <!--2001-->

    从 v8.5.5 开始，压缩日志备份功能提供了离线压缩能力，将非结构化的日志备份数据转换为结构化的 SST 文件，从而实现以下改进：

    - **提升恢复性能**：SST 可以更快地导入到集群中。
    - **降低存储空间占用**：在压缩过程中会去除冗余数据。
    - **减少对业务的影响**：在确保 RPO (Recovery Point Objective) 的前提下，可以设置更长的全量备份间隔。

  更多信息，请参考[用户文档](/br/br-compact-log-backup.md)。

* 加速从备份中恢复系统表 [#58757](https://github.com/pingcap/tidb/issues/58757) @[Leavrth](https://github.com/Leavrth) **tw@lilin90** <!--2109-->

    从 v8.5.5 开始，对于从备份中恢复系统表，BR 引入了新参数 `--fast-load-sys-tables`，用物理恢复替代逻辑恢复。该参数开启状态下，BR 会完全替换或覆盖现有的系统表，而不是向其中写入数据，从而显著提升大规模部署场景下的数据恢复性能。

    更多信息，请参考[用户文档](/br/br-snapshot-guide.md#恢复-mysql-数据库下的表)。

### 稳定性

* 提升 TiKV 在网络抖动时的调度稳定性 [#9359](https://github.com/tikv/pd/issues/9359) @[okJiang](https://github.com/okJiang) **tw@qiancai** <!--2260-->

    从 v8.5.5 起，TiKV 引入网络慢节点检测与反馈机制。启用该机制后，TiKV 会在节点之间探测网络延时，计算网络慢节点分数，并将该分数上报给 PD。PD 基于该分数判断 TiKV 节点的网络状态并进行相应的调度调整：当检测到某个 TiKV 节点存在网络抖动时，PD 会限制向该节点调度新的 Leader；如果网络抖动持续存在，PD 会主动将该节点上的现有 Leader 驱逐到其他 TiKV 节点，从而降低网络异常对集群的影响。

    更多信息，请参阅[用户文档](/pd-control.md#scheduler-config-evict-slow-store-scheduler)。

### 高可用

* 为 PD 引入客户端熔断模式 (Circuit Breaker) [#8678](https://github.com/tikv/pd/issues/8678) @[Tema](https://github.com/Tema) **tw@hfxsd** <!--2051-->

    为了防止 PD Leader 因重试风暴或类似的反馈循环而过载，TiDB 引入了熔断模式。当错误率达到预设阈值时，该模式会限制进入的流量，从而使系统能够恢复稳定。你可以通过系统变量 `tidb_cb_pd_metadata_error_rate_threshold_ratio` 来控制熔断器的触发。

    更多信息，请参考[用户文档](/system-variables.md#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855).

### SQL 功能

* 支持在线修改分布式 `ADD INDEX` 任务的并发和吞吐 [#62120](https://github.com/pingcap/tidb/pull/62120) @[joechenrh](https://github.com/joechenrh) **tw@qiancai** <!--2326-->

    在 v8.5.5 之前，如果集群开启了分布式执行框架 [`tidb_enable_dist_task`](/system-variables/#tidb_enable_dist_task-从-v710-版本开始引入) ，TiDB 不支持在 `ADD INDEX` 任务执行期间修改该任务的 `THREAD`、`BATCH_SIZE`、`MAX_WRITE_SPEED` 参数。要调整这些参数，你需要先取消当前 `ADD INDEX` 任务，重新设置参数后再提交，效率较低。

    从 v8.5.5 起，在分布式 `ADD INDEX` 任务执行期间，你可以根据当前业务负载和对 `ADD INDEX` 性能的需求，通过 `ADMIN ALTER DDL JOBS` 语句在线灵活调整这些参数，而无需中断任务。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-admin-alter-ddl.md)。

### 数据库管理

* TiKV 支持优雅关闭 (graceful shutdown) [#17221](https://github.com/tikv/tikv/issues/17221) @[hujiatao0](https://github.com/hujiatao0) **tw@qiancai** <!--2297-->

    在关闭 TiKV 服务器时，TiKV 会在配置的等待期内尽量先将节点上的 leader 副本转移到其他 TiKV 节点，然后再关闭。该等待期默认为 20 秒，可通过 [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入) 配置项进行调整。若达到该超时时间后仍有 leader 未完成转移，TiKV 将跳过剩余 leader 的转移，直接进入关闭流程。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入)。

* 提升进行中的日志备份与快照恢复的兼容性 [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger) **tw@lilin90** <!--2000-->

    从 v8.5.5 开始，当日志备份任务正在运行时，在满足特定条件的情况下，仍然可以执行快照恢复。这样，日志备份可以持续进行，无需在恢复数据期间中断。并且，恢复的数据可以被进行中的日志备份正常记录。

    更多信息，请参考[用户文档](/br/br-pitr-manual.md#进行中的日志备份与快照恢复的兼容性)。

* 支持从日志备份中进行表级恢复 [#57613](https://github.com/pingcap/tidb/issues/57613) @[Tristan1900](https://github.com/Tristan1900) **tw@lilin90** <!--2005-->

    从 v8.5.5 开始，你可以使用过滤器从日志备份中对单个表执行按时间点恢复 (PITR)。相比将整个集群恢复到指定时间点，表级恢复提供了更加灵活、且对业务影响更小的恢复方式。

    更多信息，请参考[用户文档](/br/br-pitr-manual.md#使用过滤器恢复)。

### 可观测性

* 在 Statement Summary Tables 和慢日志中增加存储引擎标识 [#61736](https://github.com/pingcap/tidb/issues/61736) @[henrybw](https://github.com/henrybw) **tw@Oreoxmt**<!--2034 beta.2-->

    当集群中同时部署了 TiKV 和 TiFlash 时，用户在数据库诊断和性能优化过程中经常需要根据存储引擎筛选 SQL 语句。例如，当用户发现 TiFlash 负载较高时，需要筛选出在 TiFlash 上运行的 SQL 语句，以便识别可能导致 TiFlash 负载过高的查询语句。为解决此需求，TiDB 从 v9.0.0 开始，在 Statement Summary Tables 和慢日志中新增了存储引擎标识字段。

    在 [Statement Summary Tables](/statement-summary-tables.md) 中新增的字段：

    * `STORAGE_KV`：值为 `1` 时表示该 SQL 语句访问了 TiKV。
    * `STORAGE_MPP`：值为 `1` 时表示该 SQL 语句访问了 TiFlash。

    在[慢日志](/identify-slow-queries.md)中新增的字段：

    * `Storage_from_kv`：值为 `true` 时表示该 SQL 语句访问了 TiKV。
    * `Storage_from_mpp`：值为 `true` 时表示该 SQL 语句访问了 TiFlash。

    该功能可以简化部分诊断和性能优化场景的工作流程，提升问题诊断效率。

    更多信息，请参考 [Statement Summary Tables](/statement-summary-tables.md) 和[慢日志](/identify-slow-queries.md)。

### 安全

* Backup & Restore (BR) 支持通过 Azure 托管标识（Managed Identity, MI）访问 Azure Blob Storage [#19006](https://github.com/tikv/tikv/issues/19006) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--2308-->

    从 v8.5.5 起，BR 支持使用 Azure 托管标识（MI）对 Azure Blob Storage 进行身份验证，无需使用静态 SAS Token。该方式实现了安全、无密钥且短期有效的认证，符合 Azure 安全最佳实践。

    利用该功能，BR 及内嵌于 TiKV 的 BR Worker 可直接从 Azure 实例元数据服务（IMDS）获取访问令牌，有效降低了凭证泄露的风险，并简化了本地或云上 Azure 环境中的凭据轮换管理。

    该功能尤其适用于在 Azure Kubernetes Service (AKS) 或其他 Azure 环境中运行 TiDB 的企业用户，这些环境通常对备份和恢复操作有严格的安全管控要求。

    更多信息，请参考[用户文档](/br/backup-and-restore-storages.md#鉴权)。

## 兼容性变更

### 系统变量


### 配置参数

- 新增 BR 配置项 [`--checkpoint-storage`](/br/br-checkpoint-restore.md#实现细节将断点数据存储在下游集群)，用于指定断点数据存储的外部存储。 

### 行为变更

* When using [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) with [Global Sort](/tidb-global-sort.md) enabled, primary key or unique index conflicts are now automatically resolved by removing all conflicting rows (none of the conflicting rows are preserved), instead of causing the task to fail. The number of conflicted rows appears in the `Result_Message` column of `SHOW IMPORT JOBS` output, and detailed conflict information is stored in cloud storage. For more information, see [`IMPORT INTO` conflict resolution](/sql-statements/sql-statement-import-into.md#conflict-resolution).

### MySQL 兼容性

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| `tidb_advancer_check_point_lag_limit`       |  新增   | 控制日志备份任务 Checkpoint 的滞后时间限制。如果日志备份任务 Checkpoint 的滞后时间超过了限制，TiDB Advancer 会暂停该任务。 |
| `tidb_cb_pd_metadata_error_rate_threshold_ratio`    |  新增  | 控制 TiDB 何时触发熔断器。设置为 `0`（默认值）表示禁用熔断器。设置为 `0.01` 到 `1` 之间的值时，表示启用熔断器，当发送到 PD 的特定请求的错误率达到或超过该阈值时，熔断器会被触发。|
| `tidb_index_lookup_pushdown_policy` |  新增  | 控制 TiDB 是否以及在什么条件下将 `IndexLookUp` 算子下推到 TiKV。 |
|        |                              |      |
|        |                              |      |

### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### 系统表

### 其他

## 改进提升

+ TiDB

    - improve the error message for import into when there are encoding errors [#63763](https://github.com/pingcap/tidb/issues/63763) @[D3Hunter](https://github.com/D3Hunter)
    - change the parser for parquet format to get better performance [#62906](https://github.com/pingcap/tidb/issues/) @[joechenrh](https://github.com/joechenrh)
    - 将 `tidb_analyze_column_options` 的默认值设置为 `all` [#64992](https://github.com/pingcap/tidb/issues/64992) @[0xPoe](https://github.com/0xPoe)
    - 优化 IndexHashJoin 的执行方式，在部分 JOIN 场景下采用增量处理以避免一次性加载大量数据，显著降低内存占用并提升执行性能 [#63303](https://github.com/pingcap/tidb/issues/63303) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - (dup): release-9.0.0.md > 改进提升> TiDB - 优化分布式执行框架 (Distributed eXecution Framework, DXF) 内部 SQL 语句的 CPU 使用率 [#59344](https://github.com/pingcap/tidb/issues/59344) @[D3Hunter](https://github.com/D3Hunter)

+ TiKV

    - Introduces CPU-aware scaling for the unified read pool to avoid CPU starvation under hot read workloads. [#18464](https://github.com/tikv/tikv/issues/18464) @[mittalrishabh](https://github.com/mittalrishabh)
    - Adds network latency awareness to slow score to avoid scheduling leaders on TiKV nodes with unstable network conditions. [#18797](https://github.com/tikv/tikv/issues/18797) @[okJiang](https://github.com/okJiang)
    - Optimizes hibernate behavior by allowing leaders to enter hibernation once a majority vote is reached, without waiting for down non-voter peers. [#19070](https://github.com/tikv/tikv/issues/19070) @[jiadebin](https://github.com/jiadebin)
    - (dup): release-9.0.0.md > 改进提升> TiKV - 在 TiKV 内存占用高时，对 BR 的日志恢复请求进行限流，防止 TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

+ PD

    - 优化了高基数指标 [#9357](https://github.com/tikv/pd/issues/9357) @[rleungx](https://github.com/rleungx)
    - 优化了时间戳推进和选举逻辑 [#9981](https://github.com/tikv/pd/issues/9981) @[bufferflies](https://github.com/bufferflies)
    - 支持批量设置 TiKV 的 store limit [#9970](https://github.com/tikv/pd/issues/9970) @[bufferflies](https://github.com/bufferflies)
    - `pd_cluster_status` 增加了 store 标签 [#9855](https://github.com/tikv/pd/issues/9855) @[SerjKol80](https://github.com/SerjKol80)

+ Tools

    + TiCDC

        - 为创建 changefeed 增加更全面的检查 [#12253](https://github.com/pingcap/tiflow/issues/12253) @[wk989898](https://github.com/wk989898)

## 错误修复

+ TiDB

    - 修复 TiDB 初始化时无法读取最新的 tidb_mem_quota_binding_cache 变量值初始化 binding 的问题 [#65381](https://github.com/pingcap/tidb/issues/65381) @[qw4990](https://github.com/qw4990)
    - 修复了在 `extractBestCNFItemRanges` 中错误地跳过候选项导致查询范围计算不精确的问题 [#62547](https://github.com/pingcap/tidb/issues/62547) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了 `plan replayer` 无法加载 binding 的问题 [#64811](https://github.com/pingcap/tidb/issues/64811) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了 `PointGet` 在有足够内存时仍不复用 chunk 导致不必要内存分配的问题 [#63920](https://github.com/pingcap/tidb/issues/63920) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了 `LogicalProjection.DeriveStats` 分配过多内存的问题 [#63810](https://github.com/pingcap/tidb/issues/63810) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了当查询发生 panic 时 `plan replayer` 无法 dump 的问题 [#64835](https://github.com/pingcap/tidb/issues/64835) @[hawkingrei](https://github.com/hawkingrei)
    - 提升了 `expression.Contains` 函数的性能 [#61373](https://github.com/pingcap/tidb/issues/61373) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当计划缓存开启时，关联子查询可能产生非预期的全表扫描的问题 [#64645](https://github.com/pingcap/tidb/issues/64645) @[winoros](https://github.com/winoros)
    - 修复系统表会污染表健康度监控的问题 [#57176](https://github.com/pingcap/tidb/issues/57176), [#64080](https://github.com/pingcap/tidb/issues/64080) @[0xPoe](https://github.com/0xPoe)
    - 修复 auto-anlyze 关闭之后 `mysql.tidb_ddl_notifier` 不能被清理的问题 [#64038](https://github.com/pingcap/tidb/issues/64038) @[0xPoe](https://github.com/0xPoe)
    - 修复了在 `newLocalColumnPool` 中重复分配 column 的问题 [#63809](https://github.com/pingcap/tidb/issues/63809) @[hawkingrei](https://github.com/hawkingrei)
    - 减少无效的 sync load 加载失败警告日志 [#63880](https://github.com/pingcap/tidb/issues/63880) @[0xPoe](https://github.com/0xPoe)
    - 修复手动 kill 正在执行事务的 connection 可能导致 tidb 发生 panic 异常退出的问题 [#63956](https://github.com/pingcap/tidb/issues/63956) @[wshwsh12](https://github.com/wshwsh12)
    - 修复缓存表在走 TiFlash 副本读取时可能出现的 goroutine 和内存泄漏问题 [#63329](https://github.com/pingcap/tidb/issues/63329) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - fix the problem that foreign key is not updated after modify column [#issue](https://github.com/pingcap/tidb/issues/59705) @[fzzf678](https://github.com/fzzf678)
    - fix error decoding `RENAME TABLE` job arg from older version TiDB [#issue](https://github.com/pingcap/tidb/issues/64413) @[joechenrh](https://github.com/joechenrh)
    - fix missing rebase auto increment not executed if BR restore failed [#issue](https://github.com/pingcap/tidb/issues/64761) @[joechenrh](https://github.com/joechenrh)
    - fix OOM issue when querying `information_schema` tables [#issue](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)
    - fix the problem that TiDB node may stuck during upgrade [#issue](https://github.com/pingcap/tidb/issues/64539) @[joechenrh](https://github.com/joechenrh)
    - fix unexpected successful admin check when there are no index record [#issue](https://github.com/pingcap/tidb/issues/63698) @[wjhuang2016](https://github.com/wjhuang2016)
    - fix data-index inconsistency when chaning collation with modify column [#issue](https://github.com/pingcap/tidb/issues/61668) @[tangenta](https://github.com/tangenta)
    - fix incorrect initialization for foreign key related fields when copying table info [#issue](https://github.com/pingcap/tidb/issues/61668) @[tangenta](https://github.com/tangenta)
    - fix the problem that embedded analyze may be not triggered for multi schema change [#issue](https://github.com/pingcap/tidb/issues/65040) @[joechenrh](https://github.com/joechenrh)
    - fix the problem that the DXF task was not cancelled after canceling the add index job [#issue](https://github.com/pingcap/tidb/issues/64129) @[tangenta](https://github.com/tangenta)
    - fix incorrect check to determing whether to load table info for tables contain foreign key [#issue](https://github.com/pingcap/tidb/issues/60444) @[JQWong7](https://github.com/JQWong7)
    - fix incorrect auto ID setting after cross-database rename table [#issue](https://github.com/pingcap/tidb/issues/64561) @[joechenrh](https://github.com/joechenrh)
    - fix incorrect handling meta key for older version of TiDB [#issue](https://github.com/pingcap/tidb/issues/64323) @[wjhuang2016](https://github.com/wjhuang2016)
    - fix ligtning doesnt' report error for schema files without trailing semicolon [#issue](https://github.com/pingcap/tidb/issues/63414) @[GMHDBJD](https://github.com/GMHDBJD)
    - fix the dead loop when reading files during IMPORT INTO global sort [#issue](https://github.com/pingcap/tidb/issues/61177) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - fix the panic when processing generated columns for IMPORT INTO [#issue](https://github.com/pingcap/tidb/issues/64657) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-9.0.0.md > 错误修复> TiDB - 修复查询 `information_schema.tables` 可能出现 OOM 问题，优化系统表查询过程中的内存使用监控 [#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)


+ TiKV

    - Fix the bug that analyze scan kv operation metric is always 0 [#19206](https://github.com/tikv/tikv/issues/19206) @[glorv](https://github.com/glorv)
    - Fix the bug that pd heartbeat may report wrong region size/keys statistics data after leader change. [#19180](https://github.com/tikv/tikv/issues/19180) @[glorv](https://github.com/glorv)
    - Fixes unsafe recovery getting stuck by removing tombstoned TiFlash learners from the unsafe recovery demotion list. [#18458](https://github.com/tikv/tikv/issues/18458) @[v01dstar](https://github.com/v01dstar)
    - Fixes an issue where snapshots could be canceled indefinitely under continuous writes, blocking replica recovery. [#18872](https://github.com/tikv/tikv/issues/18872) @[exit-code-1](https://github.com/exit-code-1)
    - Fixes compaction slowdowns caused by increased flow-control thresholds. [#18708](https://github.com/tikv/tikv/issues/18708) @[hhwyt](https://github.com/hhwyt)
    - Fix the bug that pd heartbeat may report wrong region size/keys statistics data after leader change. [#19180](https://github.com/tikv/tikv/issues/19180) @[glorv](https://github.com/glorv)
    - Fixes a corner case where Raft peers could enter hibernation prematurely, causing them to remain busy and block leader transfers after TiKV restart. [#19203](https://github.com/tikv/tikv/issues/19203) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - 修复节点在上线过程中可能无法下线的问题 [#8997](https://github.com/tikv/pd/issues/8997) @[lhy1024](https://github.com/lhy1024)
    - 修复因大量 leader transfer 可能导致 region size 跳变的问题 [#10014](https://github.com/tikv/pd/issues/10014) @[lhy1024](https://github.com/lhy1024)
    - 修复调度过程中可能导致 PD panic 的问题 [#9951](https://github.com/tikv/pd/issues/9951) @[bufferflies](https://github.com/bufferflies)
    - 修复导入过程中数据不均衡的问题 [#9088](https://github.com/tikv/pd/issues/9088) @[GMHDBJD](https://github.com/GMHDBJD)
    - 修复开启 PD follower handle 后遇到错误时，无法将请求回退到 leader 处理的问题 [#64933](https://github.com/pingcap/tidb/issues/64933) @[okJiang](https://github.com/okJiang)
    - 修复微服务请求没有正常转发的问题 [#9825](https://github.com/tikv/pd/issues/9825) @[lhy1024](https://github.com/lhy1024) [#9825](https://github.com/tikv/pd/issues/9825) @[lhy1024](https://github.com/lhy1024)
    - 修复微服务 TLS 配置问题 [#9367](https://github.com/tikv/pd/issues/9367) @[rleungx](https://github.com/rleungx)
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiFlash

    - 修复在 BR restore 的过程中，TiFlash 可能 panic 的问题 [#10606](https://github.com/pingcap/tiflash/issues/10606) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复在 BR restore 的过程中，TiFlash 不能充分利用超过 16 核 CPU 进行数据恢复的问题 [#10605](https://github.com/pingcap/tiflash/issues/10605) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 GROUP_CONCAT 触发落盘时可能导致 TiFlash 异常退出的问题 [#10553](https://github.com/pingcap/tiflash/issues/10553) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - Fixed an issue that memory usage may be unacceptable when log backup enabled and many regions in cluster. [#18719](https://github.com/tikv/tikv/issues/18719) @[YuJuncen](https://github.com/YuJuncen)
        - Fixed an issue that Azure SDK cannot found suitable key from environment. [#18206](https://github.com/tikv/tikv/issues/18206) @[YuJuncen](https://github.com/YuJuncen)
        - Fixed an issue that foreign keys cannot be properly fixed during `restore point`. [#61642](https://github.com/pingcap/tidb/issues/61642) @[Leavrth](https://github.com/Leavrth)
        - Fixed an issue that restore cannot be performed if system table collations are incompatible between backup and target cluster by introducing the parameter --sys-check-collation to support restore privileges tables from v6.5 to v7.5 [#64667](https://github.com/pingcap/tidb/issues/64667) @[Leavrth](https://github.com/Leavrth)
        - Fixed an issue that caused `restore log` cannot be performed after a failed `restore point` though the latter is safe to be execued. [#64908](https://github.com/pingcap/tidb/issues/64908) @[RidRisR](https://github.com/RidRisR)
        - Fixed an issue that Azure managed identity is unavailable.[#19006](https://github.com/tikv/tikv/issues/19006) @[RidRisR](https://github.com/RidRisR)
        - Fixed an issue that may cause `restore point` from checkpoint panic when the log backup was mixed with a full backup. [#58685](https://github.com/pingcap/tidb/issues/58685) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复同步到存储类型下游时可能因为 writer close 操作失败而导致的数据丢失问题 [#12436](https://github.com/pingcap/tiflow/issues/12436) @[wk989898](https://github.com/wk989898)
        - 修复同步 truncate partition 操作可能导致 changefeed 失败的问题 [#12430](https://github.com/pingcap/tiflow/issues/12430) @[wk989898](https://github.com/wk989898)
        - 修复同步多表 DDL语句时产生的不正确的 DDL 执行顺序 [#12449](https://github.com/pingcap/tiflow/issues/12449) @[wlwilliamx](https://github.com/wlwilliamx)
        - 升级 aws-sdk-go-v2 依赖以修复 glue schema 的注册问题[#12424](https://github.com/pingcap/tiflow/issues/12424) @[wk989898](https://github.com/wk989898)
        - 修复引起 memory quota 无法正常释放的问题[#18169](https://github.com/tikv/tikv/issues/18169) @[asddongmen](https://github.com/asddongmen)
        - 修复引起 memory quota 无法正常释放的问题[#18915](https://github.com/tikv/tikv/issues/18915) @[asddongmen](https://github.com/asddongmen)
