---
title: TiDB 9.0.0 Release Notes
summary: 了解 TiDB 9.0.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 9.0.0 Release Notes

<EmailSubscriptionWrapper />

发版日期：2025 年 xx 月 xx 日

TiDB 版本：9.0.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v9.0/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v9.0.0#version-list)

在 9.0.0 版本中，你可以获得以下关键特性：

<table>
<thead>
  <tr>
    <th>分类</th>
    <th>功能</th>
    <th>描述</th>
  </tr>
</thead>
<tbody>
  <tr>

  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性


### 性能

* 在几十万甚至上百万用户数的场景下，创建用户、修改用户信息的性能提升了 77 倍 [#55563](https://github.com/pingcap/tidb/issues/55563) @[tiancaiamao](https://github.com/tiancaiamao)  **tw@hfxsd**<!--1941-->

    之前的版本，当集群的用户数超过 20 万时，创建和修改用户的性能 QPS 会降低到 1。在一些 SaaS 场景，如果需要创建百万个用户，以及定期批量修改用户的密码信息，需要 2 天甚至更久的时间，对于一些 SaaS 业务是不可接受的。
    
    v9.0.0 对这部分 DCL 的性能进行了优化，创建 200 万用户仅需 37 分钟，大大提升了 DCL 语句的执行性能，提升了 TiDB 在此类 SaaS 场景的用户体验。

    更多信息，请参考[用户文档](/system-variables.md/#tidb_accelerate_user_creation_update-从-v900-版本开始引入)。

* 新增支持下推以下函数到 TiFlash [#59317](https://github.com/pingcap/tidb/issues/59317) @[guo-shaoge](https://github.com/guo-shaoge) **tw@Oreoxmt** <!--1918-->

    * `TRUNCATE()`

  更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* 新增支持下推包含以下聚合函数的窗口函数到 TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai**<!--1382-->

    * `MAX`
    * `MIN`
    * `COUNT`
    * `SUM`
    * `AVG`

  更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* 支持下推以下日期函数到 TiKV [#59365](https://github.com/pingcap/tidb/issues/59365) @[gengliqi](https://github.com/gengliqi) **tw@Oreoxmt** <!--1837-->

    * `FROM_UNIXTIME()`
    * `TIMESTAMPDIFF()`
    * `UNIX_TIMESTAMP()`

  更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* TiFlash 支持新的存储格式以提升字符串类型扫描效率 [#9673](https://github.com/pingcap/tiflash/issues/9673) @[JinheLin](https://github.com/JinheLin) **tw@qiancai**<!--2066-->

    在 v9.0.0 版本之前，TiFlash 存储字符串类型数据的格式在扫描时需要逐行读取，因此对于长度较小的字符串数据，扫描效率不高。在 v9.0.0 中，TiFlash 引入了新的存储格式，针对长度小于 64 字节的字符串数据的存储进行了优化，提升了扫描效率，且不会影响其他数据的存储和扫描性能。如需启用新的存储格式，你可以在 TiFlash 配置文件中将 `format_version` 设置为 8。配置生效后，新写入 TiFlash 的数据将采用新的存储格式，而现有数据的存储格式则不受影响。

    建议用户在升级前阅读 [TiFlash 升级帮助](/tiflash-upgrade-guide.md)。

    更多信息，请参考[用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)。

### 高可用

* TiProxy 支持流量回放功能正式发布 (GA) [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832)   **tw@hfxsd**<!--2062-->

    TiProxy v1.3.0 将流量回放功能作为实验特性发布。在 TiProxy v1.4.0 版本，流量回放功能正式发布 (GA)。TiProxy 提供专有的 SQL 命令进行流量捕获和流量回放功能。你可以更加方便地捕获 TiDB 生产集群中的访问流量，并在测试集群中按照指定的速率回放这些流量，完成业务验证。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-traffic-replay.md)。

### 稳定性

* 新增系统变量 `MAX_USER_CONNECTIONS`，用于限制不同用户可以建立的连接数 [#59203](https://github.com/pingcap/tidb/issues/59203) @[joccau](https://github.com/joccau) **tw@hfxsd**<!--2017-->

    从 v9.0.0 版本开始，你可通过设置系统变量 `MAX_USER_CONNECTIONS` ，来限制单个用户对单个 TiDB 节点可建立的连接数，避免由于单个用户消耗过多的 [token](/tidb-configuration-file.md/#token-limit) 导致其他用户提交的请求得不到及时响应的问题。 

    更多信息，请参考[用户文档](/system-variables.md/#max_user_connections-从-v900-版本开始引入)。


### SQL 功能

* 支持对分区表的非唯一列创建全局索引 [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss) **tw@qiancai**<!--2057-->

    从 v8.3.0 开始，TiDB 支持用户在分区表的唯一列上创建全局索引以提高查询性能，但不支持在非唯一列上创建全局索引。从 v9.0 版本起，TiDB 取消了这一限制，允许用户在分区表的非唯一列上创建全局索引，提升了全局索引的易用性。

    更多信息，请参考[全局索引](/partitioned-table.md#全局索引)。

### 数据库管理

* TiDB 索引推荐 [#12303](https://github.com/pingcap/tidb/issues/12303) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt**<!--2081-->

    索引设计在数据库性能优化中扮演非常重要的作用。自 v9.0.0 起，TiDB 在内核中加入了索引推荐。索引推荐能够分析高频查询的模式并推荐最佳索引策略，协助用户快速实现数据库性能调优，同时降低技术团队的学习门槛。

    通过 [`RECOMMEND INDEX`](/index-advisor.md) 语法，用户可以选择为某条 SQL 语句生成索引推荐，也可以自动读取历史负载中的高频 SQL 语句，做批量索引推荐。推荐结果保存在 `mysql.index_advisor_results` 中，可在后续随时查看。

    更多信息，请参考[用户文档](/index-advisor.md)。

### 可观测性

* TiDB Workload Repository [#58247](https://github.com/pingcap/tidb/issues/58247) @[xhebox](https://github.com/xhebox) @[henrybw](https://github.com/henrybw) @[wddevries](https://github.com/wddevries) **tw@lilin90**<!--1953-->

    很多高频更新的负载指标和状态信息被维护在实例的内存中，这些历史负载数据可以作为数据库的一部分持久化下来。主要用于以下目的：
    
    * **故障诊断：** 在对过往问题的诊断过程中，需要回顾历史活动和事件。持久化的负载数据可以帮助用户复盘过去某个时间段内的状态信息变化，找出异常点；或者精确定位某个数据库会话或 SQL 语句在特定时刻的具体行为。
    
    * **自动化运维：** 数据库自治是提升用户体验并降低使用门槛的必然趋势，而实现数据库自动调优需要历史数据作为支撑。基于持久化的历史工作负载数据，TiDB 可以逐步向自动化运维迈进，例如：索引推荐（Index Advisor）、统计信息推荐（Statistics Advisor）、SQL 绑定推荐（SQL Binding Advisor）等。

    在 v9.0.0 中，通过设置变量 [`tidb_workload_repository_dest`](/system-variables.md#tidb_workload_repository_dest) 启用 `Workload Repository`，TiDB 会把一部分内存表的快照持续写入 `workload_schema`，持久化到 TiKV 中。当前版本默认关闭。被持久化的内存表分为两类：

    * **存储累计指标的内存表**体积较大，快照和存储成本比较高，这些表会依据 [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval) 的设置做批量快照，最小间隔 15 分钟。通过比较任意两个快照间指标的变化，得出这一段时间各个指标的增量。包括以下内存表：

        * [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)
        * [`INFORMATION_SCHEMA.TIDB_STATEMENTS_STATS`](/statement-summary-tables.md) (由 `STATEMENTS_SUMMARY` 派生的内存表，计划在未来取代 `STATEMENTS_SUMMARY`。)
        * [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md)
        * [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md)
        * [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md)

    * **保存即时状态的内存表**刷新很快，通常体积不大，需要做很小间隔的快照才有作用。通过设置 [`tidb_workload_repository_active_sampling_interval`](/system-variables.md#tidb_workload_repository_active_sampling_interval) 的值指定时间间隔，默认为 5 秒。设置为 0 则关闭这个类型的快照。被持久化的这类内存表包括：

        * [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)
        * [`INFORMATION_SCHEMA.DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
        * [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)
        * [`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)
        * [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    
    `Workload Repository` 中的数据会被自动清理，默认保存 7 天。通过设置 [`tidb_workload_repository_retention_days`](/system-variables.md#tidb_workload_repository_retention_days) 修改保存时间。

    通过持久化数据库的历史工作负载，TiDB 可以更好地进行故障排查和优化推荐，并在未来推出一系列围绕历史负载的自动化工具，提升数据库运维和诊断的用户体验。

    更多信息，请参考[用户文档](/workloadrepo.md)。

* SQL 跨可用区流量观测 [#57543](https://github.com/pingcap/tidb/issues/57543) @[nolouch](https://github.com/nolouch) @[yibin87](https://github.com/yibin87) **tw@Oreoxmt** <!--2021-->

    跨可用区 (Availability Zone, AZ) 部署可以增强 TiDB 集群的容灾能力。然而，在云服务环境中，这种部署方式会产生额外的网络流量费用，例如 AWS 对跨区域和跨可用区的流量进行计费。因此，对于运行在云服务上的 TiDB 集群，更精确地监控和分析网络流量对于成本控制至关重要。

    从 v9.0.0 开始，TiDB 记录 SQL 处理过程中产生的网络流量，并区分跨可用区的流量。相关数据会写入 [`statements_summary` 表](/statement-summary-tables.md)和[慢查询日志](/identify-slow-queries.md)。该功能有助于用户跟踪 TiDB 集群内部的主要数据传输路径，分析跨可用区流量的来源，从而更好地理解和控制相关成本。
    
    需要注意的是，当前版本仅监测 SQL 查询在**集群内部**（TiDB、TiKV 和 TiFlash）之间的网络传输，不包括 DML 和 DDL。另外，记录的流量数据为解包后的流量，与实际物理流量存在差异，因此不能直接作为网络计费的依据。

    更多信息，请参考[用户文档](/statement-summary-tables.md#statements_summary-字段介绍)。

* 优化 `EXPLAIN ANALYZE` 输出结果中的 `execution info` 的信息 [#56232](https://github.com/pingcap/tidb/issues/56232) @[yibin87](https://github.com/yibin87) **tw@hfxsd**<!--1697-->

    [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 可以执行的 SQL 语句，并在 `execution info` 中记录执行过程的细节，同样的信息在[慢日志](/identify-slow-queries.md)中也会被捕捉。这些信息对分析和理解 SQL 的时间花费有至关重要的作用。

    在 v9.0.0 优化了 `execution info` 的输出结果，使每个指标的表达更加准确。比如，`time` 表示算子执行的时钟时间，`loops` 是当前算子被父算子调用的次数，`total_time` 代表所有并发的累加时间。这些优化可以帮助你更准确地理解 SQL 语句的执行过程，做出有针对性的优化策略。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-explain-analyze.md)。

### 安全

### 数据迁移

* 将 sync-diff-inspector 从 `pingcap/tidb-tools` 迁移至 `pingcap/tiflow` 代码仓库 [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh) **tw@Oreoxmt** <!--2070-->

    从 v9.0.0 开始，sync-diff-inspector 工具从 [`pingcap/tidb-tools`](https://github.com/pingcap/tidb-tools) GitHub 代码仓库迁移至 [`pingcap/tiflow`](https://github.com/pingcap/tiflow)。该变更将数据同步和迁移工具（[DM](/dm/dm-overview.md)、[TiCDC](/ticdc/ticdc-overview.md) 和 sync-diff-inspector）统一到同一个代码仓库中。

    对于 TiDB v9.0.0 及之后版本，你可以使用以下方法之一安装 sync-diff-inspector：

    - TiUP：执行 `tiup install sync-diff-inspector`
    - Docker 镜像：执行 `docker pull pingcap/sync-diff-inspector:latest`
    - 二进制包：下载 [TiDB 工具包](/download-ecosystem-tools.md)

  [`pingcap/tidb-tools`](https://github.com/pingcap/tidb-tools) 代码仓库现已归档。如果你之前通过 `tidb-tools` 安装 sync-diff-inspector，请改用 TiUP、Docker 镜像或 TiDB 工具包。

    更多信息，请参考[用户文档](/sync-diff-inspector/sync-diff-inspector-overview.md)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.5.0 升级至当前版本 (v9.0.0) 所需兼容性变更信息。如果从 v8.4.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

- 从 v9.0.0 开始，为了优化字符串数据的读写性能，TiFlash 针对字符串数据的存储格式进行了改动。因此，升级 TiFlash 到 v9.0.0 或以上版本后，不支持原地降级到之前的版本。更多信息，请参考[TiFlash 升级帮助](/tiflash-upgrade-guide.md)。
- 从 v9.0.0 开始，TiCDC 新增[安全机制](/ticdc/ticdc-manage-changefeed.md#安全机制)，防止用户误将同一个 TiDB 集群同时作为上游和下游进行数据同步，避免由此引发的循环复制及数据异常问题。 在执行创建、更新或恢复数据同步任务时，TiCDC 会自动检查上下游 TiDB 集群的 `cluster_id` 是否相同。一旦发现上下游集群 `cluster_id` 相同，TiCDC 会拒绝执行该任务。

### 系统变量

| 变量名  | 修改类型    | 描述 |
|--------|------------------------------|------|
| `txn_scope` | 删除 | 在 v9.0.0 中，该变量被移除。 |
| [`max_user_connections`](/system-variables.md/#max_user_connections-从-v900-版本开始引入) | 新增 | 用于限制单个用户对单个 TiDB 节点可建立的连接数，避免单个用户消耗过多的 [token](tidb-configuration-file.md/#token-limit) 导致其他用户提交的请求得不到及时响应的问题。 |
| [`tidb_accelerate_user_creation_update`](/system-variables.md/#tidb_accelerate_user_creation_update-从-v900-版本开始引入)| 新增 | 用于在用户数量过多的场景下，提升创建用户、修改用户信息的性能。 |
| [`tidb_max_dist_task_nodes`](/system-variables.md/#tidb_max_dist_task_nodes-从-v900-版本开始引入)| 新增 | 控制分布式框架任务可使用的最大 TiDB 节点数上限。默认值为 `-1`，表示自动模式。在此模式下，系统将自动选择合适的节点数量。 |
| [`mpp_version`](/system-variables.md#mpp_version-从-v660-版本开始引入) | 修改 | 该变量新增可选值 `3`，用于开启 TiFlash 新的字符串数据交换格式。当该变量的值未指定时，TiDB 将自动选择 MPP 执行计划的最新版本 `3`，以提高字符串的序列化和反序列化效率，从而提升查询性能。 |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-从-v760-版本开始引入) | 修改 | 默认值从 `OFF` 变更为 `ON`。当该值为 `ON` 时，TiDB 在获取 Region 信息时会将请求均匀地发送到所有 PD 节点上，因此 PD follower 也可以处理 Region 信息请求，从而减轻 PD leader 的 CPU 压力。从 v9.0.0 开始，当该变量值为 `ON` 时，TiDB Lightning 的 Region 信息请求也会被均匀发送到所有 PD 节点。 |
| [`tidb_pipelined_dml_resource_policy`](/system-variables.md#tidb_pipelined_dml_resource_policy-从-v900-版本开始引入) | 新增 | 该变量控制 [Pipelined DML](/pipelined-dml.md) 的资源使用策略，仅在 [`tidb_dml_type`](#tidb_dml_type-从-v800-版本开始引入) 为 `bulk` 时生效。|
| [`tidb_workload_repository_dest`](/system-variables.md#tidb_workload_repository_dest)| 新增 | 这变量用户设置 [Workload Repository](/workloadrepo.md) 的写入目标。 默认为空，不启用。 设置为 `table` 写入 TiKV 。|
| [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval) | 新增 | 设置 [Workload Repository](/workloadrepo.md) 统一快照的时间间隔。 |
| [`tidb_workload_repository_active_sampling_interval`](/system-variables.md#tidb_workload_repository_active_sampling_interval) | 新增 | 设置 [Workload Repository](/workloadrepo.md) 快速时间快照的间隔。 |
| [`tidb_workload_repository_retention_days`](/system-variables.md#tidb_workload_repository_retention_days) | 新增 | 设置 [Workload Repository](/workloadrepo.md) 中数据保存的天数。 |
|  |  |  |

### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV | [`storage.max-ts.action-on-invalid-update`](/tikv-configuration-file.md#action-on-invalid-update-从-v900-版本开始引入) | 新增 | 指定当检测到非法的 `max-ts` 更新请求时，TiKV 的处理方式。默认值为 `"panic"`，代表 TiKV 检测到非法的 `max-ts` 更新请求时会 panic。 |
| TiKV | [`storage.max-ts.cache-sync-interval`](/tikv-configuration-file.md#cache-sync-interval-从-v900-版本开始引入) | 新增 | 控制 TiKV 更新本地 PD TSO 缓存的时间间隔。默认值为 `"15s"`。 |
| TiKV | [`storage.max-ts.max-drift`](/tikv-configuration-file.md#max-drift-从-v900-版本开始引入) | 新增 | 定义当读写请求使用的 TS 超过 TiKV 缓存的 PD TSO 时，所允许的最长超出时间。默认值为`"60s"`。 |
| TiFlash | [`format_version`](/tiflash/tiflash-configuration.md#format_version) | 修改 | 默认值从 `7` 变更为 `8`，代表 v9.0.0 以及以后版本 DTFile 文件的默认格式 `8`。该格式用于支持新的字符串序列化方案，可提升字符串的读写性能。 |
| TiCDC | [`newarch`](/ticdc/ticdc-server-config.md#newarch) | 新增 | 控制是否开启 [TiCDC 新架构](/ticdc/ticdc-new-arch.md)。默认值为不设置，表示使用老架构。该配置项仅用于新架构，如果在 TiCDC 老架构的配置文件中添加该配置项，可能会导致解析失败。 |
| BR | [`--checkpoint-storage`](br/br-checkpoint-restore.md#实现细节-将断点数据存储在下游集群) | 新增 | 用于指定断点数据存储的外部存储。 |
| TiProxy | [`enable-traffic-replay`](/tiproxy/tiproxy-configuration.md#enable-traffic-replay)  | 新增 | 用于指定是否开启[流量回放](/tiproxy/tiproxy-traffic-replay.md)功能。如果为 `false`，则在流量捕获和流量回放时会报错。|
| TiProxy | [`encryption-key-path`](/tiproxy/tiproxy-configuration.md#encryption-key-path)  | 新增 | 用于指定流量捕获时用于加密流量文件的密钥的文件路径。|

### 离线包变更

从 v9.0.0 开始，[sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 工具在 `TiDB-community-toolkit` [二进制软件包](/binary-package.md)中的离线包位置从 `sync_diff_inspector` 变更为 `tiflow-{version}-linux-{arch}.tar.gz`。

### 操作系统支持变更

升级 TiDB 前，请务必确保你的操作系统版本符合[操作系统及平台要求](/hardware-and-software-requirements.md#操作系统及平台要求)。


### 系统表变更

| 系统表 | 变更类型 | 描述 |
| -------- | -------- | -------- |
| `mysql.user` | 修改 | 新增 `cluster_id` 列，用于记录 TiDB 集群的唯一标识，注意该值为只读，不可修改。 |



## 移除功能

* 以下为已移除的功能：

  * 原有的[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)已经被移除，后续推出增强的功能替代。

* 以下为计划在未来版本中移除的功能：

    * 从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 参数统一控制逻辑导入和物理导入模式的冲突检测策略。旧版冲突检测的参数 [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) 将在未来版本中被移除。

## 废弃功能

以下为计划将在未来版本中废弃的功能：

* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，该系统变量将被废弃。
* TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，该系统变量将被废弃。
* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)，用于控制 TiDB 是否支持并行 HashAgg 进行落盘。在未来版本中，该系统变量将被废弃。
* TiDB 在 v5.1 引入了系统变量 [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-从-v51-版本开始引入)，用于设置是否开启分区表动态裁剪模式。从 v8.5.0 开始，将该变量设置为 `static` 或 `static-only` 时会产生警告。在未来版本中，该系统变量将被废弃。
* TiDB Lightning 参数 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 计划在未来版本中废弃，并在后续版本中删除。该参数将由 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。
* 从 v6.3.0 开始，分区表默认使用[动态裁剪模式](/partitioned-table.md#动态裁剪模式)，相比静态裁剪模式，动态裁剪模式支持 IndexJoin、Plan Cache 等特性，性能表现更好。在未来版本中，静态裁剪模式将被废弃。
* 配置项 [`concurrently-init-stats`](/tidb-configuration-file.md#concurrently-init-stats-从-v810-和-v752-版本开始引入) 用于控制初始化统计信息缓存的并发模式，并从 v8.2 开始默认启用。计划在后续版本中仅支持并发模式，因此该配置项将被移除。
* 算子 `indexMergeJoin` 是表连接的一种方式，目前已经被其他连接方式取代，`indexMergeJoin` 计划在未来版本废弃。对应的系统变量[`tidb_enable_index_merge_join`](/system-variables.md#tidb_enable_index_merge_join) 也将被一同废弃。

## 改进提升

+ TiDB
* 优化了全局排序功能对 CPU 的资源开销，对 CPU 的最低配置要求从 8c 降低到了 1c，提升了全局排序在小规格机型上的易用性。 [#58680](https://github.com/pingcap/tidb/issues/58680) @[joccau](https://github.com/joccau)
    

+ TiKV

    

+ PD

    

+ TiFlash

    

+ Tools

    + Backup & Restore (BR)

       

    + TiDB Data Migration (DM)

        
## 错误修复

+ TiDB

    

+ TiKV

   

+ PD

    

+ TiFlash

    

+ Tools

    + Backup & Restore (BR)

        

    + TiCDC

        

    + TiDB Lightning

       

## 性能测试

如需了解 TiDB v9.0.0 的性能表现，你可以参考 TiDB Cloud Dedicated 集群的[性能测试报告](https://docs.pingcap.com/tidbcloud/v9.0-performance-highlights)（英文版）。

## 贡献者

感谢来自 TiDB 社区的贡献者们：

