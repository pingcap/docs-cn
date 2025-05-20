---
title: TiDB 9.0.0 Release Notes
summary: 了解 TiDB 9.0.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 9.0.0 Release Notes

<EmailSubscriptionWrapper />

发版日期：2025 年 xx 月 xx 日

TiDB 版本：9.0.0

<!--
试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v9.0/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v9.0/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v9.0.0#version-list)
-->

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
    <td rowspan="2">可扩展性与性能</td>
    <td>PD 支持的<a href="https://docs.pingcap.com/zh/tidb/dev/pd-microservices/">微服务模式</a>成为正式功能（从 v8.0.0 开始引入）</td>
    <td>PD 微服务模式通过将 PD 的不同功能模块解耦为独立服务，提升了系统的可扩展性、稳定性和部署灵活性，为大规模集群部署提供了更好的架构基础。</td>
  </tr>
    <tr>
    <td>按时间点恢复 (Point-in-time recovery, PITR) 支持从<a href="https://docs.pingcap.com/zh/tidb/dev/br-compact-log-backup/">压缩后的日志备份</a>中恢复，以加快恢复速度 tw@lilin90</td>
    <td>从 v9.0.0 开始，压缩日志备份功能提供了离线压缩能力，将非结构化的日志备份数据转换为结构化的 SST 文件。与重新应用原始日志相比，这些 SST 文件可以更快地恢复到集群中，从而提升了恢复性能。</td>
  </tr>
  <tr>
    <td rowspan="1">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/tiproxy-traffic-replay/">TiProxy 流量回放</a>成为正式功能（从 v8.4.0 开始引入）</td>
    <td>在进行集群升级、迁移或部署变更等重要操作之前，使用 TiProxy 捕获 TiDB 生产集群的真实负载，并在测试的目标集群中重现该工作负载，从而验证性能，确保变更成功。</td>
  </tr>
  <tr>
    <td rowspan="3">数据库管理与可观测性</td>
    <td>新增 <a href="https://docs.pingcap.com/zh/tidb/dev/workload-repository/">TiDB Workload Repository</a> 功能，支持将历史工作负载数据持久化存储到 TiKV 中 tw@lilin90</td>
    <td>TiDB Workload Repository 可以将数据库运行时的历史状态持久化，能够显著提升历史故障和性能问题的诊断效率，帮助你快速定位和解决问题，同时为健康检查和自动调优提供关键的数据基础。</td>
  </tr>
  <tr>
    <td>TiDB 索引推荐 (Index Advisor) tw@Oreoxmt</td>
    <td>TiDB 索引推荐 (Index Advisor) 通过分析实际查询负载，自动识别缺失或冗余的索引，帮助你在无需深入了解业务的情况下完成索引优化。该功能可降低手动分析和调优的成本，并提升查询性能和系统稳定性。</td>
  </tr>
  <tr>
    <td>SQL 跨可用区流量观测 tw@Oreoxmt</td>
    <td>跨可用区流量观测可用于识别 TiDB 集群中 SQL 查询产生的跨可用区网络流量，帮助你分析流量来源、优化部署架构，并控制云服务中的跨区传输成本，从而提升资源使用效率和成本可见性。</td>
  </tr>
  <tr>
    <td rowspan="3">数据迁移</td>
    <td>支持对 Data Migration (DM) 日志中的查询参数进行脱敏 tw@Oreoxmt</td>
    <td>Data Migration (DM) 引入 <code>redact-info-log</code> 配置项，支持对 DM 日志中的查询参数进行脱敏处理，防止敏感数据出现在日志中。</td>
  </tr>
  <tr>
    <td>TiDB Lightning 与 TiDB <code>sql_require_primary_key=ON</code> 兼容 tw@Oreoxmt</td>
    <td>当在 TiDB 中启用系统变量 <code>sql_require_primary_key</code> 时，TiDB Lightning 会在数据导入过程中自动为其内部的错误日志表和冲突检测表添加默认主键，以避免数据导入过程中表创建失败。</td>
  </tr>
  <tr>
    <td>将 sync-diff-inspector 从 <code>pingcap/tidb-tools</code> 迁移至 <code>pingcap/tiflow</code> 代码仓库 tw@Oreoxmt</td>
    <td>将 sync-diff-inspector 整合至已包含 DM 和 TiCDC 等迁移与同步工具的 <code>pingcap/tiflow</code> 仓库。现在你可以通过 TiUP 或专用 Docker 镜像安装 sync-diff-inspector 工具。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* PD 支持的微服务模式成为正式功能 (GA) [#5766](https://github.com/tikv/pd/issues/5766) @[binshi-bing](https://github.com/binshi-bing) tw@hfxsd <!--2052-->

    在 v8.0.0，PD 支持的微服务模式作为实验特性发布。从 v9.0.0 开始，该特性成为正式功能。该模式可将 PD 的时间戳分配和集群调度功能拆分为以下微服务单独部署，从而实现 PD 的性能扩展，解决大规模集群下 PD 的性能瓶颈问题。

    - `tso` 微服务：为整个集群提供单调递增的时间戳分配。
    - `scheduling` 微服务：为整个集群提供调度功能，包括但不限于负载均衡、热点处理、副本修复、副本放置等。

  每个微服务都以独立进程的方式部署。当设置某个微服务的副本数大于 1 时，该微服务会自动实现主备的容灾模式，以确保服务的高可用性和可靠性。

    目前 PD 微服务仅支持通过 TiDB Operator 进行部署。当 PD 出现明显的性能瓶颈且无法升级配置的情况下，建议考虑使用该模式。

    更多信息，请参考[用户文档](/pd-microservices.md)。

### 性能

* 在几十万甚至上百万用户数的场景下，创建用户、修改用户信息的性能提升了 77 倍 [#55563](https://github.com/pingcap/tidb/issues/55563) @[tiancaiamao](https://github.com/tiancaiamao)  **tw@hfxsd**<!--1941-->

    之前的版本，当集群的用户数超过 20 万时，创建和修改用户的性能 QPS 会降低到 1。在一些 SaaS 场景，如果需要创建百万个用户，以及定期批量修改用户的密码信息，需要 2 天甚至更久的时间，对于一些 SaaS 业务是不可接受的。
    
    v9.0.0 对这部分 DCL 的性能进行了优化，创建 200 万用户仅需 37 分钟，大大提升了 DCL 语句的执行性能，提升了 TiDB 在此类 SaaS 场景的用户体验。

    更多信息，请参考[用户文档](/system-variables.md#tidb_accelerate_user_creation_update-从-v900-版本开始引入)。

* 新增支持下推以下函数到 TiFlash [#59317](https://github.com/pingcap/tidb/issues/59317) @[guo-shaoge](https://github.com/guo-shaoge) **tw@Oreoxmt** <!--1918-->

    * `TRUNCATE()`

  更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* 新增支持下推包含以下聚合函数的窗口函数到 TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai**<!--1382-->

    * `MAX()`
    * `MIN()`
    * `COUNT()`
    * `SUM()`
    * `AVG()`

  更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* 支持下推以下日期函数到 TiKV [#59365](https://github.com/pingcap/tidb/issues/59365) @[gengliqi](https://github.com/gengliqi) **tw@Oreoxmt** <!--1837-->

    * `FROM_UNIXTIME()`
    * `TIMESTAMPDIFF()`
    * `UNIX_TIMESTAMP()`

  更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* TiFlash 支持新的存储格式以提升字符串类型扫描效率 [#9673](https://github.com/pingcap/tiflash/issues/9673) @[JinheLin](https://github.com/JinheLin) **tw@qiancai**<!--2066-->

    在 v9.0.0 版本之前，TiFlash 存储字符串类型数据的格式在扫描时需要逐行读取，导致短字符串的扫描效率较低。在 v9.0.0 中，TiFlash 引入了新的存储格式，针对字符串格式数据的存储进行了优化，提升了长度小于 64 字节的字符串数据的扫描效率，且不会影响其他数据的存储和扫描性能。

    - 对于新建的 v9.0.0 或之后版本的 TiDB 集群，TiFlash 默认会采用新的存储格式。
    - 对于升级到 v9.0.0 或之后版本的 TiDB 集群，建议用户在升级前阅读 [TiFlash 升级帮助](/tiflash-upgrade-guide.md)。
        - 如果升级前未指定过 [`format_version`](/tiflash/tiflash-configuration.md#format_version)，升级后 TiFlash 默认采用新的存储格式。
        - 如果升级前指定过 [`format_version`](/tiflash/tiflash-configuration.md#format_version)，升级后 `format_version` 的值保持不变，TiFlash 会继续使用 `format_version` 指定的存储格式。此时如需启用新的存储格式，请在 TiFlash 配置文件中将 `format_version` 设置为 `8`。配置生效后，新写入 TiFlash 的数据将采用新的存储格式，而现有数据的存储格式则不受影响。
        
  更多信息，请参考[用户文档](/tiflash/tiflash-configuration.md#format_version)。

* 按时间点恢复 (Point-in-time recovery, PITR) 支持从压缩后的日志备份中恢复，以加快恢复速度 [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen) **tw@lilin90** <!--2001-->

    从 v9.0.0 开始，压缩日志备份功能提供了离线压缩能力，将非结构化的日志备份数据转换为结构化的 SST 文件，从而实现以下改进：

    - SST 可以被快速导入集群，从而**提升恢复性能**。
    - 压缩过程中消除重复记录，从而**减少空间消耗**。
    - 在确保 RTO (Recovery Time Objective) 的前提下，你可以设置更长的全量备份间隔，从而**降低对业务的影响**。

  更多信息，请参考[用户文档](/br/br-compact-log-backup.md)。

### 高可用

* TiProxy 支持流量回放功能正式发布 (GA) [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832)   **tw@hfxsd**<!--2062-->

    TiProxy v1.3.0 将流量回放功能作为实验特性发布。在 TiProxy v1.4.0 版本，流量回放功能正式发布 (GA)。TiProxy 提供专有的 SQL 命令进行流量捕获和流量回放功能。你可以更加方便地捕获 TiDB 生产集群中的访问流量，并在测试集群中按照指定的速率回放这些流量，完成业务验证。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-traffic-replay.md)。

### 稳定性

* 新增系统变量 `MAX_USER_CONNECTIONS`，用于限制不同用户可以建立的连接数 [#59203](https://github.com/pingcap/tidb/issues/59203) @[joccau](https://github.com/joccau) **tw@hfxsd**<!--2017-->

    从 v9.0.0 版本开始，你可通过设置系统变量 `MAX_USER_CONNECTIONS` ，来限制单个用户对单个 TiDB 节点可建立的连接数，避免由于单个用户消耗过多的 [token](/tidb-configuration-file.md#token-limit) 导致其他用户提交的请求得不到及时响应的问题。 

    更多信息，请参考[用户文档](/system-variables.md#max_user_connections-从-v900-版本开始引入)。

### SQL 功能

* 支持对分区表的非唯一列创建全局索引 [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss) **tw@qiancai**<!--2057-->

    从 v8.3.0 开始，TiDB 支持用户在分区表的唯一列上创建全局索引以提高查询性能，但不支持在非唯一列上创建全局索引。从 v9.0.0 起，TiDB 取消了这一限制，允许用户在分区表的非唯一列上创建全局索引，提升了全局索引的易用性。

    更多信息，请参考[全局索引](/partitioned-table.md#全局索引)。

### 数据库管理

* TiDB 索引推荐 (Index Advisor) [#12303](https://github.com/pingcap/tidb/issues/12303) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--2081-->

    索引设计在数据库性能优化中至关重要。从 v8.5.0 开始，TiDB 引入索引推荐 (Index Advisor) 功能，并持续进行改进和增强。该功能可以分析高频查询模式，推荐最优索引策略，帮助你更高效地进行性能调优，并降低索引设计的门槛。

    你可以使用 [`RECOMMEND INDEX`](/index-advisor.md#使用-recommend-index-语句推荐索引) SQL 语句为某条 SQL 语句生成索引推荐，或自动分析历史负载中的高频 SQL 语句，实现批量推荐。推荐结果存储在 `mysql.index_advisor_results` 表中，你可以查询此表以查看推荐的索引。

    更多信息，请参考[用户文档](/index-advisor.md)。

* 提升进行中的日志备份与快照恢复的兼容性 [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger) **tw@lilin90** <!--2000-->

    从 v9.0.0 开始，当日志备份任务正在运行时，在满足特定条件的情况下，仍然可以执行快照恢复，并且恢复的数据可以被进行中的日志备份正常记录。这样，日志备份可以持续进行，无需在恢复数据期间中断。

    更多信息，请参考[用户文档](/br/br-pitr-manual.md#进行中的日志备份与快照恢复的兼容性)。

### 可观测性

* 新增 TiDB Workload Repository 功能，支持将历史工作负载数据持久化存储到 TiKV 中 [#58247](https://github.com/pingcap/tidb/issues/58247) @[xhebox](https://github.com/xhebox) @[henrybw](https://github.com/henrybw) @[wddevries](https://github.com/wddevries) **tw@lilin90**<!--1953-->

    很多高频更新的负载指标和状态信息被维护在实例的内存中，这些历史负载数据可以作为数据库的一部分持久化下来。主要用于以下目的：
    
    * **故障诊断**：在对过往问题的诊断过程中，需要回顾历史活动和事件。持久化的负载数据可以帮助用户复盘过去某个时间段内的状态信息变化，找出异常点；或者精确定位某个数据库会话或 SQL 语句在特定时刻的具体行为。
    
    * **自动化运维**：数据库自治是提升用户体验并降低使用门槛的必然趋势，而实现数据库自动调优需要历史数据作为支撑。基于持久化的历史工作负载数据，TiDB 可以逐步向自动化运维迈进，例如：索引推荐 (Index Advisor)、统计信息推荐 (Statistics Advisor)、SQL 绑定推荐 (SQL Binding Advisor) 等。

  在 v9.0.0 中，通过设置变量 [`tidb_workload_repository_dest`](/system-variables.md#tidb_workload_repository_dest-从-v900-版本开始引入) 启用 Workload Repository，TiDB 会把一部分内存表的快照持续写入 `workload_schema`，并持久化到 TiKV 中。当前版本默认关闭。被持久化的内存表分为以下两类：

    * **存储累计指标的内存表**体积较大，快照和存储成本较高，这些表会依据 [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval-从-v900-版本开始引入) 的设置做批量快照，最小间隔为 15 分钟。通过比较任意两个快照间指标的变化，得出这一段时间各个指标的增量。包括以下内存表：

        * [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)
        * [`INFORMATION_SCHEMA.TIDB_STATEMENTS_STATS`](/statement-summary-tables.md) (由 `STATEMENTS_SUMMARY` 派生的内存表，计划在未来取代 `STATEMENTS_SUMMARY`。)
        * [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md)
        * [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md)
        * [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md)

    * **保存即时状态的内存表**刷新很快，通常体积不大，需要做很小间隔的快照才有作用。通过设置 [`tidb_workload_repository_active_sampling_interval`](/system-variables.md#tidb_workload_repository_active_sampling_interval-从-v900-版本开始引入) 的值指定时间间隔，默认为 5 秒。设置为 0 则关闭此类型的快照。被持久化的这类内存表包括：

        * [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)
        * [`INFORMATION_SCHEMA.DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
        * [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)
        * [`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)
        * [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    
    `Workload Repository` 中的数据会被自动清理，默认保存 7 天。通过设置 [`tidb_workload_repository_retention_days`](/system-variables.md#tidb_workload_repository_retention_days-从-v900-版本开始引入) 修改保存时间。

    通过持久化数据库的历史工作负载，TiDB 可以更好地进行故障排查和优化推荐，并在未来推出一系列围绕历史负载的自动化工具，提升数据库运维和诊断的用户体验。

    更多信息，请参考[用户文档](/workload-repository.md)。

* SQL 跨可用区流量观测 [#57543](https://github.com/pingcap/tidb/issues/57543) @[nolouch](https://github.com/nolouch) @[yibin87](https://github.com/yibin87) **tw@Oreoxmt** <!--2021-->

    跨可用区 (Availability Zone, AZ) 部署可以增强 TiDB 集群的容灾能力。然而，在云服务环境中，这种部署方式会产生额外的跨区网络传输成本，例如 AWS 会对跨区域和跨可用区的流量进行计费。因此，对于运行在云服务上的 TiDB 集群，精确地监控和分析网络流量对于成本控制至关重要。

    从 v9.0.0 开始，TiDB 会记录 SQL 处理过程中产生的网络流量，并区分哪些是跨可用区传输产生的流量。相关数据会写入 [`statements_summary` 表](/statement-summary-tables.md)和[慢查询日志](/identify-slow-queries.md)。该功能有助于用户跟踪 TiDB 集群内部的主要数据传输路径，分析跨可用区流量的来源，从而更好地理解和控制相关成本。
    
    需要注意的是，当前版本仅监测 SQL 查询在**集群内部**（TiDB、TiKV 和 TiFlash）之间的网络流量，不包括 DML 和 DDL 操作产生的流量。另外，记录的流量数据为解包后的流量，与实际物理流量存在差异，因此不能直接作为网络计费的依据。

    更多信息，请参考[用户文档](/statement-summary-tables.md#statements_summary-字段介绍)。

* 优化 `EXPLAIN ANALYZE` 输出结果中的 `execution info` 的信息 [#56232](https://github.com/pingcap/tidb/issues/56232) @[yibin87](https://github.com/yibin87) **tw@hfxsd**<!--1697-->

    [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 可以执行的 SQL 语句，并在 `execution info` 中记录执行过程的细节，同样的信息在[慢日志](/identify-slow-queries.md)中也会被捕捉。这些信息对分析和理解 SQL 的时间花费有至关重要的作用。

    在 v9.0.0 优化了 `execution info` 的输出结果，使每个指标的表达更加准确。比如，`time` 表示算子执行的时钟时间，`loops` 是当前算子被父算子调用的次数，`total_time` 代表所有并发的累加时间。这些优化可以帮助你更准确地理解 SQL 语句的执行过程，做出有针对性的优化策略。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-explain-analyze.md)。

### 安全

### 数据迁移

* TiCDC 引入新架构，显著提升性能、可扩展性和稳定性（实验特性）[#442](https://github.com/pingcap/ticdc/issues/442) @[CharlesCheung96](https://github.com/CharlesCheung96) **tw@qiancai** <!--2027-->

    在 v9.0.0 中，TiCDC 引入了新架构（实验特性），显著提升了实时数据复制的性能、可扩展性与稳定性，同时降低了资源成本。新架构重新设计了 TiCDC 的核心组件并优化了数据处理流程。

    在新架构下，TiCDC 同步能力接近线性扩展，并能以更低的资源成本完成百万级表的同步任务。在高流量、频繁 DDL 操作及集群扩缩容等场景下，Changefeed 的延迟更低且更加稳定。

<!--
    更多信息，请参考[用户文档](/ticdc/ticdc-new-arch.md)。
-->

* TiCDC 为 Debezium 协议支持 DDL 事件和 WATERMARK 事件 [#11566](https://github.com/pingcap/tiflow/issues/11566) @[wk989898](https://github.com/wk989898) **tw@lilin90** <!--2009-->

    TiCDC 支持以 Debezium 的格式输出 DDL 和 WATERMARK 事件。当上游 DDL 操作成功执行后，TiCDC 会将该 DDL 事件编码为 Kafka 消息，其 key 和 message 均采用 Debezium 格式。WATERMARK 事件是 TiCDC 的扩展功能（通过在 Kafka sink 中配置 [`enable-tidb-extension`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka) 来启用），用于表示一个特殊的时间点，在这个时间点之前收到的事件是完整的。

    更多信息，请参考[用户文档](/ticdc/ticdc-debezium.md)。

* TiCDC 新增安全机制，避免将数据同步回同一个 TiDB 集群 [#12062](https://github.com/pingcap/tiflow/issues/12062) @[wlwilliamx](https://github.com/wlwilliamx) **tw@qiancai** <!--2063-->

    TiCDC 支持从上游的一个 TiDB 集群同步数据到下游的多个其他系统，包括其他 TiDB 集群。在 v9.0.0 之前，如果在 TiCDC 配置中误将同一个 TiDB 集群同时配置为数据源集群和目标集群，可能会导致数据同步循环，从而引发数据一致性问题。从 v9.0.0 开始，TiCDC 会自动检查源和目标 TiDB 集群是否相同，从而避免这种配置错误。

    更多信息，请参考[用户文档](/ticdc/ticdc-manage-changefeed.md#安全机制)。

* 支持对 Data Migration (DM) 日志中的查询参数进行脱敏 [#11489](https://github.com/pingcap/tiflow/issues/11489) @[db-will](https://github.com/db-will) **tw@Oreoxmt** <!--2030-->

    从 v9.0.0 开始，你可以通过 `redact-info-log` 配置项控制是否启用 DM 日志脱敏功能。启用后，DM 日志中包含敏感数据的查询参数将被替换为 `?` 占位符。如需开启该功能，你可以在 DM-worker 配置文件中设置 `redact-info-log` 为 `true`，或在启动 DM 时传入参数 `--redact-info-log=true`。该功能仅对查询参数进行脱敏，不会脱敏整个 SQL 语句，并且需要重启 DM-worker 才能生效。

<!--
    更多信息，请参考[用户文档](/dm/dm-worker-configuration-file.md#redact-info-log-从-v900-版本开始引入)。
-->

* TiDB Lightning 与 TiDB `sql_require_primary_key=ON` 兼容 [#57479](https://github.com/pingcap/tidb/issues/57479) @[lance6716](https://github.com/lance6716) **tw@Oreoxmt** <!--2026-->

    当在 TiDB 中启用系统变量 [`sql_require_primary_key`](/system-variables.md#sql_require_primary_key-从-v630-版本开始引入) 后，表必须包含主键。为避免表创建失败，TiDB Lightning 为其内部的错误日志表和冲突检测表（`conflict_error_v4`、`type_error_v2` 和 `conflict_records_v2`）添加了默认主键。如果你的自动化脚本使用了这些内部表，请更新脚本以适配包含主键的新表结构。

* 将 sync-diff-inspector 从 `pingcap/tidb-tools` 迁移至 `pingcap/tiflow` 代码仓库 [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh) **tw@Oreoxmt** <!--2070-->

    从 v9.0.0 开始，sync-diff-inspector 工具从 GitHub 代码仓库 [`pingcap/tidb-tools`](https://github.com/pingcap/tidb-tools) 迁移至 [`pingcap/tiflow`](https://github.com/pingcap/tiflow)。通过该变更，`sync-diff-inspector` 现在与 [DM](/dm/dm-overview.md) 和 [TiCDC](/ticdc/ticdc-overview.md) 一起在同一个代码仓库中维护，实现了这些数据同步和迁移工具的统一管理。

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
| [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-从-v840-版本开始引入) | 修改 | 经进一步的测试后，默认值从 `legacy` 变更为 `optimized`，即 TiDB 在执行 Hash Join 算子时使用 [Hash Join 算子的优化版](/sql-statements/sql-statement-explain-analyze.md#hashjoinv2)，以提升 Hash Join 性能。 |
| [`max_user_connections`](/system-variables.md#max_user_connections-从-v900-版本开始引入) | 新增 | 用于限制单个用户对单个 TiDB 节点可建立的连接数，避免单个用户消耗过多的 [token](/tidb-configuration-file.md#token-limit) 导致其他用户提交的请求得不到及时响应的问题。 |
| [`tidb_accelerate_user_creation_update`](/system-variables.md#tidb_accelerate_user_creation_update-从-v900-版本开始引入)| 新增 | 用于在用户数量过多的场景下，提升创建用户、修改用户信息的性能。 |
| [`tidb_max_dist_task_nodes`](/system-variables.md#tidb_max_dist_task_nodes-从-v900-版本开始引入)| 新增 | 控制分布式框架任务可使用的最大 TiDB 节点数上限。默认值为 `-1`，表示自动模式。在此模式下，系统将自动选择合适的节点数量。 |
| [`mpp_version`](/system-variables.md#mpp_version-从-v660-版本开始引入) | 修改 | 该变量新增可选值 `3`，用于开启 TiFlash 新的字符串数据交换格式。当该变量的值未指定时，TiDB 将自动选择 MPP 执行计划的最新版本 `3`，以提高字符串的序列化和反序列化效率，从而提升查询性能。 |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-从-v760-版本开始引入) | 修改 | 默认值从 `OFF` 变更为 `ON`。当该值为 `ON` 时，TiDB 在获取 Region 信息时会将请求均匀地发送到所有 PD 节点上，因此 PD follower 也可以处理 Region 信息请求，从而减轻 PD leader 的 CPU 压力。从 v9.0.0 开始，当该变量值为 `ON` 时，TiDB Lightning 的 Region 信息请求也会被均匀发送到所有 PD 节点。 |
| [`tidb_pipelined_dml_resource_policy`](/system-variables.md#tidb_pipelined_dml_resource_policy-从-v900-版本开始引入) | 新增 | 该变量控制 [Pipelined DML](/pipelined-dml.md) 的资源使用策略，仅在 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-从-v800-版本开始引入) 为 `bulk` 时生效。|
| [`tidb_workload_repository_dest`](/system-variables.md#tidb_workload_repository_dest-从-v900-版本开始引入)| 新增 | 设置 [Workload Repository](/workload-repository.md) 的写入目标。默认为空，不启用。 设置为 `table` 写入 TiKV 。|
| [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval-从-v900-版本开始引入) | 新增 | 设置 [Workload Repository](/workload-repository.md) 统一快照的时间间隔。 |
| [`tidb_workload_repository_active_sampling_interval`](/system-variables.md#tidb_workload_repository_active_sampling_interval-从-v900-版本开始引入) | 新增 | 设置 [Workload Repository](/workload-repository.md) 快速时间快照的间隔。 |
| [`tidb_workload_repository_retention_days`](/system-variables.md#tidb_workload_repository_retention_days-从-v900-版本开始引入) | 新增 | 设置 [Workload Repository](/workload-repository.md) 中数据保存的天数。 |

### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV | [`storage.max-ts.action-on-invalid-update`](/tikv-configuration-file.md#action-on-invalid-update-从-v900-版本开始引入) | 新增 | 指定当检测到非法的 `max-ts` 更新请求时，TiKV 的处理方式。默认值为 `"panic"`，代表 TiKV 检测到非法的 `max-ts` 更新请求时会 panic。 |
| TiKV | [`storage.max-ts.cache-sync-interval`](/tikv-configuration-file.md#cache-sync-interval-从-v900-版本开始引入) | 新增 | 控制 TiKV 更新本地 PD TSO 缓存的时间间隔。默认值为 `"15s"`。 |
| TiKV | [`storage.max-ts.max-drift`](/tikv-configuration-file.md#max-drift-从-v900-版本开始引入) | 新增 | 定义当读写请求使用的 TS 超过 TiKV 缓存的 PD TSO 时，所允许的最长超出时间。默认值为`"60s"`。 |
| TiFlash | [`hashagg_use_magic_hash`](/tiflash/tiflash-configuration.md#hashagg_use_magic_hash-从-v900-版本开始引入) | 新增 | 控制 TiFlash 在进行聚合操作时使用的哈希函数。 |
| TiFlash | [`format_version`](/tiflash/tiflash-configuration.md#format_version) | 修改 | 默认值从 `7` 变更为 `8`，代表 v9.0.0 以及以后版本 DTFile 文件的默认格式 `8`。该格式用于支持新的字符串序列化方案，可提升字符串的读写性能。 |
<!--
| TiCDC | [`newarch`](/ticdc/ticdc-server-config.md#newarch) | 新增 | 控制是否开启 [TiCDC 新架构](/ticdc/ticdc-new-arch.md)。默认值为不设置，表示使用老架构。该配置项仅用于新架构，如果在 TiCDC 老架构的配置文件中添加该配置项，可能会导致解析失败。 |
| BR | [`--checkpoint-storage`](br/br-checkpoint-restore.md#实现细节-将断点数据存储在下游集群) | 新增 | 用于指定断点数据存储的外部存储。 | 
| DM | [`redact-info-log`](/dm/dm-worker-configuration-file.md#redact-info-log-从-v900-版本开始引入) | 新增 | 控制是否开启 DM 日志脱敏。 |
-->
| TiProxy | [`enable-traffic-replay`](/tiproxy/tiproxy-configuration.md#enable-traffic-replay)  | 新增 | 用于指定是否开启[流量回放](/tiproxy/tiproxy-traffic-replay.md)功能。如果为 `false`，则在流量捕获和流量回放时会报错。|
| TiProxy | [`encryption-key-path`](/tiproxy/tiproxy-configuration.md#encryption-key-path)  | 新增 | 用于指定流量捕获时用于加密流量文件的密钥的文件路径。|

### 离线包变更

从 v9.0.0 开始，[sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 工具在 `TiDB-community-toolkit` [二进制软件包](/binary-package.md)中的离线包位置从 `sync_diff_inspector` 变更为 `tiflow-{version}-linux-{arch}.tar.gz`。

### 操作系统支持变更

升级 TiDB 前，请务必确保你的操作系统版本符合[操作系统及平台要求](/hardware-and-software-requirements.md#操作系统及平台要求)。

### 系统表变更

| 系统表 | 变更类型 | 描述 |
| -------- | -------- | -------- |
| [`mysql.tidb`](/mysql-schema/mysql-schema.md#集群状态系统表) | 修改 | 新增 `cluster_id` 字段，用于记录 TiDB 集群的唯一标识，注意该值为只读，不可修改。 |

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
* 作为测试用途的优化器提示 [`NTH_PLAN(N)`](/optimizer-hints.md#nth_plann) 计划在未来版本废弃。

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

<!--
如需了解 TiDB v9.0.0 的性能表现，你可以参考 TiDB Cloud Dedicated 集群的[性能测试报告](https://docs.pingcap.com/tidbcloud/v9.0-performance-highlights)（英文版）。
-->

## 贡献者

感谢来自 TiDB 社区的贡献者们：
