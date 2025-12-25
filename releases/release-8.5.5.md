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

* 大幅提升特定有损 DDL 操作的执行效率，例如 `BIGINT → INT`、`CHAR(120) → VARCHAR(60)`。在未发生数据截断的前提下，执行耗时可从数小时缩短至分钟级、秒级甚至毫秒级，性能提升可达到数十倍至数十万倍。  [#63366](https://github.com/pingcap/tidb/issues/63366)  [@wjhuang2016](https://github.com/wjhuang2016), [@tangenta](https://github.com/tangenta), [@fzzf678](https://github.com/fzzf678)**tw@qiancai** <!--2292-->

    优化策略包括：

    - 在严格 SQL 模式下，预先检查类型转换过程中是否存在数据截断风险；
    - 若不存在数据截断风险，则仅更新元数据，尽量避免索引重建；
    - 如需重建索引，则采用更高效的 Ingest 流程，大幅提升索引重建性能。

    性能提升示例（基于 100 GiB 表的基准测试）：

    | 场景 | 操作类型 | 优化前 | 优化后 | 性能提升 |
    |------|----------|--------|--------|----------|
    | 无索引列 | `BIGINT → INT` | 2 小时 34 分 | 1 分 5 秒 | 142× |
    | 有索引列 | `BIGINT → INT` | 6 小时 25 分 | 0.05 秒 | 460,000× |
    | 有索引列 | `CHAR(120) → VARCHAR(60)` | 7 小时 16 分 | 12 分 56 秒 | 34× |

    注：以上数据基于 DDL 执行过程中未发生数据截断的前提。以上优化对于有 TiFlash 副本的表，以及 sign <--> unsign 数据类型修改的场景不会生效。

    更多信息，请参考[用户文档](链接)。

* 优化了存在大量外键场景下的 DDL 性能，逻辑 DDL 性能最高可提升 25 倍 [#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1896-->

    在 v8.5.5 版本之前，当一些用户单个集群的表数量达到 1000 万级别，且其中有几十万张表有外键的场景，创建表，给表加列这些逻辑 DDL 的性能 QPS 会降低到 4，使得一些多租户的 SaaS 场景下的运维操作变得非常低效。在 v8.5.5 对该场景做了优化。经测试，1000 万张表，其中 20 万张表有外键的场景下，创建表，加列这类逻辑 DDL 的性能 QPS 稳定保持在 100，性能有 25 倍的提升。

    更多信息，请参考[用户文档](链接)。

* 支持将索引查询下推到 TiKV 提升查询性能 [#62575](https://github.com/pingcap/tidb/issues/62575) @[lcwangchao](https://github.com/lcwangchao) **tw@Oreoxmt** <!--1899-->

    TiDB 从 v8.5.5 开始支持通过 Optimizer Hints 将索引查询 `IndexLookUp` 下推到 TiKV 节点执行，从而减少远程调用次数并提升查询性能。实际性能提升比例因业务场景而异，需要进行测试验证。


    使用 [`INDEX_LOOKUP_PUSHDOWN(t1_name, idx1_name [, idx2_name ...])`](https://docs.pingcap.com/zh/tidb/stable/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--从-v855-版本开始引入) Hint，可以显式指示优化器将指定表的索引查询下推到 TiKV。建议将该 Hint 与表的 AFFINITY 属性配合使用，例如为普通表设置 `AFFINITY="table"`，为分区表设置 `AFFINITY="partition"`。

    如果需要禁止某个表的索引查询下推到 TiKV，可以使用 [`NO_INDEX_LOOKUP_PUSHDOWN(t1_name)`](https://docs.pingcap.com/zh/tidb/stable/optimizer-hints#no_index_lookup_pushdownt1_name-从-v855-版本开始引入) Hint。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/stable/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--从-v855-版本开始引入)。

* 表级和分区级亲和性属性 AFFINITY [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024) **tw@qiancai** <!--2317-->

    为表或者分区表新增亲和性属性，设置亲和性属性后，PD会将表或分区的Region归为相同的一个亲和性分组中，这些Region的Leader、Voter 会被优先调度到指定TiKV Store上。有AFFNITY属性的表和分区在查询时，由于索引、表数据的Region都在一个TiKV Store上，因此优化器可结合 hint INDEX_LOOKUP_PUSHDOWN 指定将对应索引查询下推，减少跨节点分散查询带来的延迟，提升性能。

    更多信息，请参考[table-affinity.md](table-affinity.md)。

* 按时间点恢复 (Point-in-time recovery, PITR) 支持从压缩后的日志备份中恢复，以加快恢复速度 [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen) **tw@lilin90** <!--2001-->

    从 v9.0.0 开始，压缩日志备份功能提供了离线压缩能力，将非结构化的日志备份数据转换为结构化的 SST 文件，从而实现以下改进：

    - SST 可以被快速导入集群，从而**提升恢复性能**。
    - 压缩过程中消除重复记录，从而**减少空间消耗**。
    - 在确保 RTO (Recovery Time Objective) 的前提下，你可以设置更长的全量备份间隔，从而**降低对业务的影响**。

  更多信息，请参考[用户文档](/br/br-compact-log-backup.md)。

* Accelerated recovery of system tables from backups [#58757](https://github.com/pingcap/tidb/issues/58757) @[Leavrth](https://github.com/Leavrth) **tw@lilin90** <!--2109-->

    When restoring system tables from a backup, BR now introduces a new `--fast-load-sys-tables` parameter to use physical restoration instead of logical restoration. This option completely overwrites/replaces the existing tables, instead of restoring into them, for faster restoration for large scale deployments.

    For more information, see [Documentation](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema).

### 稳定性

* Improved store scheduling in presence of network jitter [#9359](https://github.com/tikv/pd/issues/9359) @[okJiang](https://github.com/okJiang) **tw@qiancai** <!--2260-->

    Provides a network status feedback mechanism to PD to avoid re-scheduling the leaders back to a problematic node (experiencing network jitter) after the leaders had been transferred off the node by TiKV raft mechanism. If the network continues to jitter, PD will actively evict leader from jittering node.

### 高可用

* Introduce Client Circuit Breaker Pettern for PD [#8678](https://github.com/tikv/pd/issues/8678) @[Tema](https://github.com/Tema) **tw@hfxsd** <!--2051-->

    To protect the PD leader from overloading due to retry storms or similar feedback loops, a circuit breaker pattern is introduced to limit incoming traffic (when a threshold of errors is reached) to enable the system to stabilize. The `tidb_cb_pd_metadata_error_rate_threshold_ratio` system variable is used to control the application of the circuit breaker.

    For more information, see [Documentation](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855).

### SQL 功能

* 支持在线修改分布式 ADD Index 任务的并发和吞吐 [#62120](https://github.com/pingcap/tidb/pull/62120) @[joechenrh](https://github.com/joechenrh) **tw@qiancai** <!--2326-->

   在 v8.5.5 版本之前，当集群开启了分布式执行框架 [tidb_enable_dist_task](/system-variables/#tidb_enable_dist_task-从-v710-版本开始引入) ，在 ADD Index 任务执行期间，是无法修改该任务的 `THREAD`， `BATCH_SIZE`，`MAX_WRITE_SPEED`  参数。需要取消该 DDL 任务，重新设置参数后再提交，效率较低。支持该功能后，用户可以根据业务负载和对 ADD Index 的性能要求，在线灵活调整这些参数。

    更多信息，请参考[ADMIN ALTER DDL JOBS](/sql-statement-admin-alter-ddl/#admin-alter-ddl-jobs)。

### 数据库管理

* TiKV 支持优雅关闭 (graceful shutdown) [#17221](https://github.com/tikv/tikv/issues/17221) @[hujiatao0](https://github.com/hujiatao0) **tw@qiancai** <!--2297-->

    在关闭 TiKV 服务器时，TiKV 会尽量将其上的 leader 副本转移到其他 TiKV 节点，然后再关闭。该等待期默认为 20 秒，可通过 [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入) 配置项进行调整。若达到该超时时间后仍有 leader 未完成转移，TiKV 将跳过剩余 leader 的转移，直接进入关闭流程。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入)。

* 提升进行中的日志备份与快照恢复的兼容性 [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger) **tw@lilin90** <!--2000-->

    从 v9.0.0 开始，当日志备份任务正在运行时，在满足特定条件的情况下，仍然可以执行快照恢复，并且恢复的数据可以被进行中的日志备份正常记录。这样，日志备份可以持续进行，无需在恢复数据期间中断。

    更多信息，请参考[用户文档](/br/br-pitr-manual.md#进行中的日志备份与快照恢复的兼容性)。

* Table level restores from Log Backups [#57613](https://github.com/pingcap/tidb/issues/57613) @[Tristan1900](https://github.com/Tristan1900) **tw@lilin90** <!--2005-->

    Starting from v8.5.5, individual table level point in time recoveries can now be performed from log backups using filters. Being able to restore individual tables, instead of the full cluster, to a specific point in time enables much more flexible, and less impactful, recovery options.

    For more information, see [documentation](/br/br-pitr-manual.md#restore-data-using-filters).

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 安全

* Enable Azure Managed Identity (MI) authentication for Backup & Restore (BR) to Azure Blob Storage [#19006](https://github.com/tikv/tikv/issues/19006) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--2308-->

    Starting from v8.5.5, TiDB Backup & Restore supports Azure Managed Identity (MI) for authenticating to Azure Blob Storage, eliminating the need for static SAS tokens. This enables secure, keyless, and ephemeral authentication aligned with Azure best practices.

    With this feature, BR and the embedded BR worker in TiKV can acquire access tokens directly from Azure Instance Metadata Service (IMDS), reducing credential leakage risk and simplifying credential rotation for self-managed and cloud deployments on Azure.

    This enhancement is particularly useful for enterprise customers running TiDB on Azure Kubernetes Service (AKS) or other Azure environments that require strict security controls for backup and restore workflows.

    更多信息，请参考[用户文档](链接)。

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
|        |                              |      |
|        |                              |      |
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

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-9.0.0.md > 改进提升> TiDB - 优化分布式执行框架 (Distributed eXecution Framework, DXF) 内部 SQL 语句的 CPU 使用率 [#59344](https://github.com/pingcap/tidb/issues/59344) @[D3Hunter](https://github.com/D3Hunter)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-9.0.0.md > 改进提升> TiKV - 在 TiKV 内存占用高时，对 BR 的日志恢复请求进行限流，防止 TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 错误修复

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-9.0.0.md > 错误修复> TiDB - 修复查询 `information_schema.tables` 可能出现 OOM 问题，优化系统表查询过程中的内存使用监控 [#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Other dup notes

- (dup): release-9.0.0.md > # 可观测性 * 在 Statement Summary Tables 和慢日志中增加存储引擎标识 [#61736](https://github.com/pingcap/tidb/issues/61736) @[henrybw](https://github.com/henrybw) **tw@Oreoxmt**<!--2034 beta.2-->
