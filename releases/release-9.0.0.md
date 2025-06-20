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
    <td>按时间点恢复 (Point-in-time recovery, PITR) 支持从<a href="https://docs.pingcap.com/zh/tidb/dev/br-compact-log-backup/">压缩后的日志备份</a>中恢复，以加快恢复速度</td>
    <td>从 v9.0.0 开始，压缩日志备份功能提供了离线压缩能力，将非结构化的日志备份数据转换为结构化的 SST 文件。与重新应用原始日志相比，这些 SST 文件可以更快地恢复到集群中，从而提升了恢复性能。</td>
  </tr>
  <tr>
    <td rowspan="1">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/tiproxy-traffic-replay/">TiProxy 流量回放</a>成为正式功能（从 v8.4.0 开始引入）</td>
    <td>在进行集群升级、迁移或部署变更等重要操作之前，使用 TiProxy 捕获 TiDB 生产集群的真实负载，并在测试的目标集群中重现该工作负载，从而验证性能，确保变更成功。</td>
  </tr>
  <tr>
    <td rowspan="3">数据库管理与可观测性</td>
    <td>新增 <a href="https://docs.pingcap.com/zh/tidb/dev/workload-repository/">TiDB Workload Repository</a> 功能，支持将历史工作负载数据持久化存储到 TiKV 中</td>
    <td>TiDB Workload Repository 可以将数据库运行时的历史状态持久化，能够显著提升历史故障和性能问题的诊断效率，帮助你快速定位和解决问题，同时为健康检查和自动调优提供关键的数据基础。</td>
  </tr>
  <tr>
    <td>TiDB 索引推荐 (Index Advisor)</td>
    <td>TiDB 索引推荐 (Index Advisor) 通过分析实际查询负载，自动识别缺失或冗余的索引，帮助你在无需深入了解业务的情况下完成索引优化。该功能可降低手动分析和调优的成本，并提升查询性能和系统稳定性。</td>
  </tr>
  <tr>
    <td>SQL 跨可用区流量观测</td>
    <td>跨可用区流量观测可用于识别 TiDB 集群中 SQL 查询产生的跨可用区网络流量，帮助你分析流量来源、优化部署架构，并控制云服务中的跨区传输成本，从而提升资源使用效率和成本可见性。</td>
  </tr>
  <tr>
    <td rowspan="3">数据迁移</td>
    <td>支持对 Data Migration (DM) 日志中的查询参数进行脱敏</td>
    <td>Data Migration (DM) 引入 <code>redact-info-log</code> 配置项，支持对 DM 日志中的查询参数进行脱敏处理，防止敏感数据出现在日志中。</td>
  </tr>
  <tr>
    <td>TiDB Lightning 与 TiDB <code>sql_require_primary_key=ON</code> 兼容</td>
    <td>当在 TiDB 中启用系统变量 <code>sql_require_primary_key</code> 时，TiDB Lightning 会在数据导入过程中自动为其内部的错误日志表和冲突检测表添加默认主键，以避免数据导入过程中表创建失败。</td>
  </tr>
  <tr>
    <td>将 sync-diff-inspector 从 <code>pingcap/tidb-tools</code> 迁移至 <code>pingcap/tiflow</code> 代码仓库</td>
    <td>将 sync-diff-inspector 整合至已包含 DM 和 TiCDC 等迁移与同步工具的 <code>pingcap/tiflow</code> 仓库。现在你可以通过 TiUP 或专用 Docker 镜像安装 sync-diff-inspector 工具。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* PD 支持的微服务模式成为正式功能 (GA) [#5766](https://github.com/tikv/pd/issues/5766) @[binshi-bing](https://github.com/binshi-bing)

    在 v8.0.0，PD 支持的微服务模式作为实验特性发布。从 v9.0.0 开始，该特性成为正式功能。该模式可将 PD 的时间戳分配和集群调度功能拆分为以下微服务单独部署，从而实现 PD 的性能扩展，解决大规模集群下 PD 的性能瓶颈问题。

    - `tso` 微服务：为整个集群提供单调递增的时间戳分配。
    - `scheduling` 微服务：为整个集群提供调度功能，包括但不限于负载均衡、热点处理、副本修复、副本放置等。

  每个微服务都以独立进程的方式部署。当设置某个微服务的副本数大于 1 时，该微服务会自动实现主备的容灾模式，以确保服务的高可用性和可靠性。

    目前 PD 微服务仅支持通过 TiDB Operator 进行部署。当 PD 出现明显的性能瓶颈且无法升级配置的情况下，建议考虑使用该模式。

    更多信息，请参考[用户文档](/pd-microservices.md)。

### 性能

* 在几十万甚至上百万用户数的场景下，创建用户、修改用户信息的性能提升了 77 倍 [#55563](https://github.com/pingcap/tidb/issues/55563) @[tiancaiamao](https://github.com/tiancaiamao)

    之前的版本，当集群的用户数超过 20 万时，创建和修改用户的性能 QPS 会降低到 1。在一些 SaaS 场景，如果需要创建百万个用户，以及定期批量修改用户的密码信息，需要 2 天甚至更久的时间，对于一些 SaaS 业务是不可接受的。
    
    v9.0.0 对这部分 DCL 的性能进行了优化，创建 200 万用户仅需 37 分钟，大大提升了 DCL 语句的执行性能，提升了 TiDB 在此类 SaaS 场景的用户体验。

    更多信息，请参考[用户文档](/system-variables.md#tidb_accelerate_user_creation_update-从-v900-版本开始引入)。

* 新增支持下推以下函数到 TiFlash [#59317](https://github.com/pingcap/tidb/issues/59317) @[guo-shaoge](https://github.com/guo-shaoge)

    * `TRUNCATE()`

  更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* 新增支持下推包含以下聚合函数的窗口函数到 TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) [#59509](https://github.com/pingcap/tidb/issues/59509) @[xzhangxian1008](https://github.com/xzhangxian1008)

    * `MAX()`
    * `MIN()`
    * `COUNT()`
    * `SUM()`
    * `AVG()`

  更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* 支持下推以下日期函数到 TiKV [#59365](https://github.com/pingcap/tidb/issues/59365) [#18184](https://github.com/tikv/tikv/issues/18184) [#58940](https://github.com/pingcap/tidb/issues/58940) [#59497](https://github.com/pingcap/tidb/issues/59497) @[wshwsh12](https://github.com/wshwsh12) @[xzhangxian1008] @[gengliqi](https://github.com/gengliqi)

    * `FROM_UNIXTIME()`
    * `TIMESTAMPDIFF()`
    * `UNIX_TIMESTAMP()`

  更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* TiFlash 支持新的存储格式以提升字符串类型扫描效率 [#9673](https://github.com/pingcap/tiflash/issues/9673) @[JinheLin](https://github.com/JinheLin)

    在 v9.0.0 版本之前，TiFlash 存储字符串类型数据的格式在扫描时需要逐行读取，导致短字符串的扫描效率较低。在 v9.0.0 中，TiFlash 引入了新的存储格式，针对字符串格式数据的存储进行了优化，提升了长度小于 64 字节的字符串数据的扫描效率，且不会影响其他数据的存储和扫描性能。

    - 对于新建的 v9.0.0 或之后版本的 TiDB 集群，TiFlash 默认会采用新的存储格式。
    - 对于升级到 v9.0.0 或之后版本的 TiDB 集群，建议用户在升级前阅读 [TiFlash 升级帮助](/tiflash-upgrade-guide.md)。
        - 如果升级前未指定过 [`format_version`](/tiflash/tiflash-configuration.md#format_version)，升级后 TiFlash 默认采用新的存储格式。
        - 如果升级前指定过 [`format_version`](/tiflash/tiflash-configuration.md#format_version)，升级后 `format_version` 的值保持不变，TiFlash 会继续使用 `format_version` 指定的存储格式。此时如需启用新的存储格式，请在 TiFlash 配置文件中将 `format_version` 设置为 `8`。配置生效后，新写入 TiFlash 的数据将采用新的存储格式，而现有数据的存储格式则不受影响。
        
  更多信息，请参考[用户文档](/tiflash/tiflash-configuration.md#format_version)。

* 按时间点恢复 (Point-in-time recovery, PITR) 支持从压缩后的日志备份中恢复，以加快恢复速度 [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen)

    从 v9.0.0 开始，压缩日志备份功能提供了离线压缩能力，将非结构化的日志备份数据转换为结构化的 SST 文件，从而实现以下改进：

    - SST 可以被快速导入集群，从而**提升恢复性能**。
    - 压缩过程中消除重复记录，从而**减少空间消耗**。
    - 在确保 RTO (Recovery Time Objective) 的前提下，你可以设置更长的全量备份间隔，从而**降低对业务的影响**。

  更多信息，请参考[用户文档](/br/br-compact-log-backup.md)。

### 高可用

* TiProxy 支持流量回放功能正式发布 (GA) [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832)

    TiProxy v1.3.0 将流量回放功能作为实验特性发布。在 TiProxy v1.4.0 版本，流量回放功能正式发布 (GA)。TiProxy 提供专有的 SQL 命令进行流量捕获和流量回放功能。你可以更加方便地捕获 TiDB 生产集群中的访问流量，并在测试集群中按照指定的速率回放这些流量，完成业务验证。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-traffic-replay.md)。

### 稳定性

* 新增系统变量 `MAX_USER_CONNECTIONS`，用于限制不同用户可以建立的连接数 [#59203](https://github.com/pingcap/tidb/issues/59203) @[joccau](https://github.com/joccau)

    从 v9.0.0 版本开始，你可通过设置系统变量 `MAX_USER_CONNECTIONS` ，来限制单个用户对单个 TiDB 节点可建立的连接数，避免由于单个用户消耗过多的 [token](/tidb-configuration-file.md#token-limit) 导致其他用户提交的请求得不到及时响应的问题。 

    更多信息，请参考[用户文档](/system-variables.md#max_user_connections-从-v900-版本开始引入)。

### SQL 功能

* 支持对分区表的非唯一列创建全局索引 [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss)

    从 v8.3.0 开始，TiDB 支持用户在分区表的唯一列上创建全局索引以提高查询性能，但不支持在非唯一列上创建全局索引。从 v9.0.0 起，TiDB 取消了这一限制，允许用户在分区表的非唯一列上创建全局索引，提升了全局索引的易用性。

    更多信息，请参考[全局索引](/partitioned-table.md#全局索引)。

### 数据库管理

* TiDB 索引推荐 (Index Advisor) [#12303](https://github.com/pingcap/tidb/issues/12303) @[qw4990](https://github.com/qw4990)

    索引设计在数据库性能优化中至关重要。从 v8.5.0 开始，TiDB 引入索引推荐 (Index Advisor) 功能，并持续进行改进和增强。该功能可以分析高频查询模式，推荐最优索引策略，帮助你更高效地进行性能调优，并降低索引设计的门槛。

    你可以使用 [`RECOMMEND INDEX`](/index-advisor.md#使用-recommend-index-语句推荐索引) SQL 语句为某条 SQL 语句生成索引推荐，或自动分析历史负载中的高频 SQL 语句，实现批量推荐。推荐结果存储在 `mysql.index_advisor_results` 表中，你可以查询此表以查看推荐的索引。

    更多信息，请参考[用户文档](/index-advisor.md)。

* 提升进行中的日志备份与快照恢复的兼容性 [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger)

    从 v9.0.0 开始，当日志备份任务正在运行时，在满足特定条件的情况下，仍然可以执行快照恢复，并且恢复的数据可以被进行中的日志备份正常记录。这样，日志备份可以持续进行，无需在恢复数据期间中断。

    更多信息，请参考[用户文档](/br/br-pitr-manual.md#进行中的日志备份与快照恢复的兼容性)。

### 可观测性

* 新增 TiDB Workload Repository 功能，支持将历史工作负载数据持久化存储到 TiKV 中 [#58247](https://github.com/pingcap/tidb/issues/58247) @[xhebox](https://github.com/xhebox) @[henrybw](https://github.com/henrybw) @[wddevries](https://github.com/wddevries)

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

* SQL 跨可用区流量观测 [#57543](https://github.com/pingcap/tidb/issues/57543) @[nolouch](https://github.com/nolouch) @[yibin87](https://github.com/yibin87)

    跨可用区 (Availability Zone, AZ) 部署可以增强 TiDB 集群的容灾能力。然而，在云服务环境中，这种部署方式会产生额外的跨区网络传输成本，例如 AWS 会对跨区域和跨可用区的流量进行计费。因此，对于运行在云服务上的 TiDB 集群，精确地监控和分析网络流量对于成本控制至关重要。

    从 v9.0.0 开始，TiDB 会记录 SQL 处理过程中产生的网络流量，并区分哪些是跨可用区传输产生的流量。相关数据会写入 [`statements_summary` 表](/statement-summary-tables.md)和[慢查询日志](/identify-slow-queries.md)。该功能有助于用户跟踪 TiDB 集群内部的主要数据传输路径，分析跨可用区流量的来源，从而更好地理解和控制相关成本。
    
    需要注意的是，当前版本仅监测 SQL 查询在**集群内部**（TiDB、TiKV 和 TiFlash）之间的网络流量，不包括 DML 和 DDL 操作产生的流量。另外，记录的流量数据为解包后的流量，与实际物理流量存在差异，因此不能直接作为网络计费的依据。

    更多信息，请参考[用户文档](/statement-summary-tables.md#statements_summary-字段介绍)。

* 优化 `EXPLAIN ANALYZE` 输出结果中的 `execution info` 的信息 [#56232](https://github.com/pingcap/tidb/issues/56232) @[yibin87](https://github.com/yibin87)

    [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 可以执行的 SQL 语句，并在 `execution info` 中记录执行过程的细节，同样的信息在[慢日志](/identify-slow-queries.md)中也会被捕捉。这些信息对分析和理解 SQL 的时间花费有至关重要的作用。

    在 v9.0.0 优化了 `execution info` 的输出结果，使每个指标的表达更加准确。比如，`time` 表示算子执行的时钟时间，`loops` 是当前算子被父算子调用的次数，`total_time` 代表所有并发的累加时间。这些优化可以帮助你更准确地理解 SQL 语句的执行过程，做出有针对性的优化策略。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-explain-analyze.md)。

### 安全

### 数据迁移

* TiCDC 引入新架构，显著提升性能、可扩展性和稳定性（实验特性）[#442](https://github.com/pingcap/ticdc/issues/442) @[CharlesCheung96](https://github.com/CharlesCheung96)

    在 v9.0.0 中，TiCDC 引入了新架构（实验特性），显著提升了实时数据复制的性能、可扩展性与稳定性，同时降低了资源成本。新架构重新设计了 TiCDC 的核心组件并优化了数据处理流程。

    在新架构下，TiCDC 同步能力接近线性扩展，并能以更低的资源成本完成百万级表的同步任务。在高流量、频繁 DDL 操作及集群扩缩容等场景下，Changefeed 的延迟更低且更加稳定。

    更多信息，请参考[用户文档](/ticdc/ticdc-new-arch.md)。

* TiCDC 为 Debezium 协议支持 DDL 事件和 WATERMARK 事件 [#11566](https://github.com/pingcap/tiflow/issues/11566) @[wk989898](https://github.com/wk989898)

    TiCDC 支持以 Debezium 的格式输出 DDL 和 WATERMARK 事件。当上游 DDL 操作成功执行后，TiCDC 会将该 DDL 事件编码为 Kafka 消息，其 key 和 message 均采用 Debezium 格式。WATERMARK 事件是 TiCDC 的扩展功能（通过在 Kafka sink 中配置 [`enable-tidb-extension`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka) 来启用），用于表示一个特殊的时间点，在这个时间点之前收到的事件是完整的。

    更多信息，请参考[用户文档](/ticdc/ticdc-debezium.md)。

* TiCDC 新增安全机制，避免将数据同步回同一个 TiDB 集群 [#11767](https://github.com/pingcap/tiflow/issues/11767) [#12062](https://github.com/pingcap/tiflow/issues/12062) @[wlwilliamx](https://github.com/wlwilliamx)

    TiCDC 支持从上游的一个 TiDB 集群同步数据到下游的多个其他系统，包括其他 TiDB 集群。在 v9.0.0 之前，如果在 TiCDC 配置中误将同一个 TiDB 集群同时配置为数据源集群和目标集群，可能会导致数据同步循环，从而引发数据一致性问题。从 v9.0.0 开始，TiCDC 会自动检查源和目标 TiDB 集群是否相同，从而避免这种配置错误。

    更多信息，请参考[用户文档](/ticdc/ticdc-manage-changefeed.md#安全机制)。

* 支持对 Data Migration (DM) 日志中的查询参数进行脱敏 [#11489](https://github.com/pingcap/tiflow/issues/11489) @[db-will](https://github.com/db-will)

    从 v9.0.0 开始，你可以通过 `redact-info-log` 配置项控制是否启用 DM 日志脱敏功能。启用后，DM 日志中包含敏感数据的查询参数将被替换为 `?` 占位符。如需开启该功能，你可以在 DM-worker 配置文件中设置 `redact-info-log` 为 `true`，或在启动 DM 时传入参数 `--redact-info-log=true`。该功能仅对查询参数进行脱敏，不会脱敏整个 SQL 语句，并且需要重启 DM-worker 才能生效。

    更多信息，请参考[用户文档](/dm/dm-worker-configuration-file.md#redact-info-log-从-v900-版本开始引入)。

* TiDB Lightning 与 TiDB `sql_require_primary_key=ON` 兼容 [#57479](https://github.com/pingcap/tidb/issues/57479) @[lance6716](https://github.com/lance6716)

    当在 TiDB 中启用系统变量 [`sql_require_primary_key`](/system-variables.md#sql_require_primary_key-从-v630-版本开始引入) 后，表必须包含主键。为避免表创建失败，TiDB Lightning 为其内部的错误日志表和冲突检测表（`conflict_error_v4`、`type_error_v2` 和 `conflict_records_v2`）添加了默认主键。如果你的自动化脚本使用了这些内部表，请更新脚本以适配包含主键的新表结构。

* 将 sync-diff-inspector 从 `pingcap/tidb-tools` 迁移至 `pingcap/tiflow` 代码仓库 [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh)

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
| TiCDC | [`newarch`](/ticdc/ticdc-server-config.md#newarch) | 新增 | 控制是否开启 [TiCDC 新架构](/ticdc/ticdc-new-arch.md)。默认值为不设置，表示使用老架构。该配置项仅用于新架构，如果在 TiCDC 老架构的配置文件中添加该配置项，可能会导致解析失败。 |
| BR | [`--checkpoint-storage`](br/br-checkpoint-restore.md#实现细节-将断点数据存储在下游集群) | 新增 | 用于指定断点数据存储的外部存储。 | 
| DM | [`redact-info-log`](/dm/dm-worker-configuration-file.md#redact-info-log-从-v900-版本开始引入) | 新增 | 控制是否开启 DM 日志脱敏。 |
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

    - (dup): release-8.5.1.md > 改进提升> TiDB - 支持将只读的用户自定义变量折叠为常量 [#52742](https://github.com/pingcap/tidb/issues/52742) @[winoros](https://github.com/winoros)
    - (dup): release-8.5.1.md > 改进提升> TiDB - 将统计信息内存缓存的默认阈值调整为总内存的 20% [#58014](https://github.com/pingcap/tidb/issues/58014) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.6.md > 改进提升> TiDB - 将 TTL 表的 GC 及相关统计信息收集任务限定在 owner 节点执行，从而降低开销 [#59357](https://github.com/pingcap/tidb/issues/59357) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-8.5.1.md > 改进提升> TiDB - 将统计信息内存缓存的默认阈值调整为总内存的 20% [#58014](https://github.com/pingcap/tidb/issues/58014) @[hawkingrei](https://github.com/hawkingrei)
    - 优化分布式执行框架 (Distributed eXecution Framework, DXF) 内部 SQL 语句的 CPU 使用率 [#59344](https://github.com/pingcap/tidb/issues/59344) @[D3Hunter](https://github.com/D3Hunter)
    - 在 `EXPLAIN ANALYZE` 的执行结果中新增更多 Spill 的细节信息 [#59076](https://github.com/pingcap/tidb/issues/59076) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 在 Hash Join v2 中支持 Left Outer Anti Semi Join [#58479](https://github.com/pingcap/tidb/pull/58479) @[wshwsh12](https://github.com/wshwsh12)
    - 跳过乐观事务中自动提交语句的锁清理阶段以提升性能 [#58675](https://github.com/pingcap/tidb/issues/58675) @[ekexium](https://github.com/ekexium)
    - TTL 关闭 `tidb_enable_paging`，以减少扫描行数，提升性能 [#58342](https://github.com/pingcap/tidb/issues/58342) @[lcwangchao](https://github.com/lcwangchao)
    - 在构建 Semi Join 和 Anti Semi Join 时，支持选择左侧作为构建侧 [#58325](https://github.com/pingcap/tidb/issues/58325) @[hawkingrei](https://github.com/hawkingrei)
    - 对于形如 `a = 1 AND (b = 2 OR c = 3 OR d = 4)` 的查询条件，支持生成使用 `(a,b), (a,c), (a,d)` 的 `IndexMerge` 计划，无需人工展开表达式 [#58361](https://github.com/pingcap/tidb/issues/58361) @[time-and-fate](https://github.com/time-and-fate)
    - 支持由 `IN` 子查询而来的 Semi Join 使用 `semi_join_rewrite` 的 Hint [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)
    - 自动删除由 `OR` 连接的过滤条件中的冗余表达式 [#58998](https://github.com/pingcap/tidb/issues/58998) @[time-and-fate](https://github.com/time-and-fate)

+ TiKV

    - (dup): release-6.5.12.md > 改进提升> TiKV - 增加对非法 `max_ts` 更新的检测机制 [#17916](https://github.com/tikv/tikv/issues/17916) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.2.0.md > 改进提升> TiKV - 默认开启[提前 apply](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-从-v810-版本开始引入) 特性，开启后，Raft leader 在多数 peer 完成 Raft log 持久化之后即可进行 apply，不再要求 leader 自身完成 Raft log 的持久化，降低少数 TiKV 抖动对写请求延迟的影响 [#16717](https://github.com/tikv/tikv/issues/16717) @[glorv](https://github.com/glorv)
    - 优化残留数据清理机制，减少对请求延迟的影响 [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 TiKV MVCC 内存引擎在迁移 Leader 时的预热机制，减少迁移 Leader 期间对 Coprocessor 请求延时的影响 [#17782](https://github.com/tikv/tikv/issues/17782) @[overvenus](https://github.com/overvenus)
    - 优化 TiKV MVCC 内存引擎的自动淘汰机制，减少对 Coprocessor 请求延时的影响 [#18130](https://github.com/tikv/tikv/issues/18130) @[overvenus](https://github.com/overvenus)
    - 在 TiKV 内存占用高时，对 BR 的日志恢复请求进行限流，防止 TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

+ PD

    - 支持当 `max-replicas` 小于当前副本数时打印警告信息 [#8959](https://github.com/tikv/pd/issues/8959) @[lhy1024](https://github.com/lhy1024)
    - 新增 `gRPC Received commands rate` 监控面板 [#8920](https://github.com/tikv/pd/issues/8920) @[okJiang](https://github.com/okJiang)
    - 支持设置 `evict-slow-store-scheduler` 的 `batch` 大小 [#7156](https://github.com/tikv/pd/issues/7156) @[rleungx]
(https://github.com/rleungx)
    - 为 `UpdateTSO` 增加了重试机制 [#9020](https://github.com/tikv/pd/issues/9020) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - 提升 TiFlash `TableScan` 算子性能，跳过不必要的数据读取 [#9875](https://github.com/pingcap/tiflash/issues/9875) @[gengliqi](https://github.com/gengliqi)
    - 通过内存预取，提升特定场景中 Aggregation 的性能 [#9680](https://github.com/pingcap/tiflash/issues/9680) @[guo-shaoge](https://github.com/guo-shaoge)
    - 引入 [HashJoinV2](/sql-statements/sql-statement-explain-analyze.md#hashjoinv2)，提升部分 inner join 场景的性能 [#9060](https://github.com/pingcap/tiflash/issues/9060) @[gengliqi](https://github.com/gengliqi)
    
+ Tools

    + Backup & Restore (BR)

        - 在全量备份日志中记录 TiKV 节点返回的错误信息，便于问题诊断 [#58666](https://github.com/pingcap/tidb/issues/58666) @[Leavrth](https://github.com/Leavrth)
        - 优化备份恢复 summary 日志的结构和内容 [#56493](https://github.com/pingcap/tidb/issues/56493) @[Leavrth](https://github.com/Leavrth)
        - 更新不可恢复的系统表列表 [#52530](https://github.com/pingcap/tidb/issues/52530) @[Leavrth](https://github.com/Leavrth)
        - 采用并行方式，提升 PITR 恢复过程中的索引修复速度 [#59158](https://github.com/pingcap/tidb/issues/59158) @[Leavrth](https://github.com/Leavrth)
        - 备份扫描过程中支持忽略特定 lock，提高备份效率 [#53224](https://github.com/pingcap/tidb/issues/53224) @[3pointer](https://github.com/3pointer)
        - 移除对 AWS region 名称的检查，避免新支持的 AWS region 因无法通过检查而导致备份报错的问题 [#18159](https://github.com/tikv/tikv/issues/18159) @[3pointer](https://github.com/3pointer)
    <!-- + TiCDC

         - 为 Canal-JSON 协议的 TiDB 扩展字段中新增 `tableId` 和 `partitionId` 字段 [#11874](https://github.com/pingcap/tiflow/issues/11874) @[3AceShowHand](https://github.com/3AceShowHand) --> <!-- for-beta.2 -->

    + TiDB Data Migration (DM)

        - (dup): release-6.6.0.md > 改进提升> Tools> TiDB Data Migration (DM) - 新增 async/batch relay writer 以优化 relay 性能 [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)
        - DM 支持多安全配置 [#11831](https://github.com/pingcap/tiflow/issues/11831) @[River2000i](https://github.com/River2000i)

    + TiDB Lightning

        - (dup): release-6.5.12.md > 改进提升> Tools> TiDB Lightning - 在解析 CSV 文件时，新增行宽检查以防止 OOM 问题 [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)

## 错误修复

+ TiDB

    - 修复在 TiDB 升级过程中执行 `MODIFY COLUMN` 语句可能失败的问题 [#58843](https://github.com/pingcap/tidb/issues/58843) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在 TiDB 升级过程中执行 `DROP COLUMN` 语句可能失败的问题 [#58863](https://github.com/pingcap/tidb/issues/58863) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在添加索引过程中动态调整 Worker 数量可能导致的数据竞争问题 [#59016](https://github.com/pingcap/tidb/issues/59016) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在添加索引过程中减少 Worker 数量可能导致任务卡住的问题 [#59267](https://github.com/pingcap/tidb/issues/59267) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在添加索引过程中 kill PD Leader 可能导致数据索引不一致的问题 [#59701](https://github.com/pingcap/tidb/issues/59701) @[tangenta](https://github.com/tangenta)
    - 修复使用全局排序添加唯一索引可能失败的问题 [#59725](https://github.com/pingcap/tidb/issues/59725) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复 `ADMIN SHOW DDL JOBS` 语句无法正确显示行数的问题 [#59897](https://github.com/pingcap/tidb/issues/59897) @[tangenta](https://github.com/tangenta)
    - 修复使用 `IMPORT INTO ... FROM SELECT` 导入 TiFlash 时发生错误的问题 [#58443](https://github.com/pingcap/tidb/issues/58443) @[D3Hunter](https://github.com/D3Hunter)
    - 修复 `IMPORT INTO ... FROM SELECT` 没有正确转换负数的问题 [#58613](https://github.com/pingcap/tidb/issues/58613) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在部分 TiDB 节点未同步 schema 版本时，日志中没有打印相应节点信息的问题 [#58480](https://github.com/pingcap/tidb/issues/58480) @[D3Hunter](https://github.com/D3Hunter)
    - 修复一个可能导致创建多个同名视图的问题 [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在分布式执行框架下执行添加索引操作没有正确更新行数的问题 [#58573](https://github.com/pingcap/tidb/issues/58573) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在存在大量索引的表上进行全局排序时可能导致 OOM 的问题 [#59508](https://github.com/pingcap/tidb/issues/59508) @[D3Hunter](https://github.com/D3Hunter)
    - 修复当 `truncate` 表达式的第一个参数为 `0` 且第二个参数值较大时，计算结果错误的问题 [#57651](https://github.com/pingcap/tidb/issues/57651) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 Hash Aggregation 算子可能存在 goroutine 泄漏的问题 [#58004](https://github.com/pingcap/tidb/issues/58004) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 Hash Join 算子在触发 spill 后统计信息不准确的问题 [#58571](https://github.com/pingcap/tidb/issues/58571) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 `json_extract` 表达式计算结果不准确的问题 [#49513](https://github.com/pingcap/tidb/issues/49513) @[YangKeao](https://github.com/YangKeao)
    - 修复 Hash Join 执行出错时返回错误结果但未报错的问题 [#59377](https://github.com/pingcap/tidb/issues/59377) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复当 `json_keys` 表达式包含两个参数且第一个参数为 `JSONTypeCodeArray` 类型时，计算结果错误的问题 [#56788](https://github.com/pingcap/tidb/issues/56788) @[zimulala](https://github.com/zimulala)
    - 修复 MPP coordinator 潜在的内存泄漏问题 [#59703](https://github.com/pingcap/tidb/issues/59703) @[yibin87](https://github.com/yibin87)
    - 修复并行排序过程可能卡住的问题 [#59655](https://github.com/pingcap/tidb/issues/59655) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复在修改 `tidb_ttl_delete_rate_limit` 时，部分 TTL 任务可能挂起的问题 [#58484](https://github.com/pingcap/tidb/issues/58484) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-8.5.1.md > 错误修复> TiDB - 修复查询慢日志时，更改时区导致返回结果错误的问题 [#58452](https://github.com/pingcap/tidb/issues/58452) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复在构造 `IndexMerge` 时可能丢失部分谓词的问题 [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 DDL owner 变更时，作业状态被覆盖的问题 [#52747](https://github.com/pingcap/tidb/issues/52747) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复在查询包含生成列的分区表时报错的问题 [#58475](https://github.com/pingcap/tidb/issues/58475) @[joechenrh](https://github.com/joechenrh)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复手动加载统计信息时，统计信息文件中包含 null 可能导致加载失败的问题 [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    - (dup): release-8.4.0.md > 错误修复> TiDB - 废弃统计信息相关的无用配置，减少冗余代码 [#55043](https://github.com/pingcap/tidb/issues/55043) @[Rustin170506](https://github.com/Rustin170506)
    - (dup): release-8.5.1.md > 错误修复> TiDB - 修复在超过 3000 维向量类型的列上创建向量搜索索引报错 `KeyTooLong` 的问题 [#58836](https://github.com/pingcap/tidb/issues/58836) @[breezewish](https://github.com/breezewish)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复当集群中存在存算分离架构 TiFlash 节点时，执行 `ALTER TABLE ... PLACEMENT POLICY ...` 之后，Region peer 可能会被意外地添加到 TiFlash Compute 节点的问题 [#58633](https://github.com/pingcap/tidb/issues/58633) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.1.md > 错误修复> TiDB - 修复执行 `REORGANIZE PARTITION` 时，数据回填可能导致并发更新被回滚的问题 [#58226](https://github.com/pingcap/tidb/issues/58226) @[mjonss](https://github.com/mjonss)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复查询 `cluster_slow_query` 表时，使用 `ORDER BY` 可能导致结果乱序的问题 [#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复某些情况下查询临时表会产生 TiKV 请求的问题 [#58875](https://github.com/pingcap/tidb/issues/58875) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复在 Prepare 协议中，客户端使用非 UTF8 相关字符集报错的问题 [#58870](https://github.com/pingcap/tidb/issues/58870) @[xhebox](https://github.com/xhebox)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复创建两个相同名称的视图而没有报错的问题 [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 TTL 任务可能被忽略或处理多次的问题 [#59347](https://github.com/pingcap/tidb/issues/59347) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 exchange partition 错误判断导致执行失败的问题 [#59534](https://github.com/pingcap/tidb/issues/59534) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 Join 的等值条件两边数据类型不同，可能导致 TiFlash 产生错误结果的问题 [#59877](https://github.com/pingcap/tidb/issues/59877) @[yibin87](https://github.com/yibin87)
    - 修复 TiDB 在特定场景下无法正常退出的问题 [#58418](https://github.com/pingcap/tidb/issues/58418) @[tiancaiamao](https://github.com/tiancaiamao)
    - 避免在更新 Infoschema v2 时 TiDB 可能 panic 的问题 [#58712](https://github.com/pingcap/tidb/issues/58712) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复部分 gRPC 客户端无法连接 TiDB Server 状态接口的问题 [#59093](https://github.com/pingcap/tidb/issues/59093) @[iosmanthus](https://github.com/iosmanthus)
    - 修复在使用游标时 TiDB 可能 panic，并且可能泄露文件的问题 [#59976](https://github.com/pingcap/tidb/issues/59976) [#59963](https://github.com/pingcap/tidb/issues/59963) @[YangKeao](https://github.com/YangKeao)
    - 修复向量化执行时 `json_search` 在搜索路径为 `NULL` 时未返回 `NULL` 的问题 [#59463](https://github.com/pingcap/tidb/issues/59463) @[YangKeao](https://github.com/YangKeao)
    - 修复慢日志在库名或表名包含冒号 (`:`) 时无法正确解析的问题 [#39940](https://github.com/pingcap/tidb/issues/39940) @[Defined2014](https://github.com/Defined2014)
    - 修复 `MOD()` 函数不支持使用表达式作为参数的问题 [#59000](https://github.com/pingcap/tidb/issues/59000) @[Defined2014](https://github.com/Defined2014)
    - 修复启用 `tidb_enable_dist_task` 导致 TiDB 升级失败的问题 [#54061](https://github.com/pingcap/tidb/issues/54061) @[tangenta](https://github.com/tangenta)
    - 修复创建索引后产生写热点的问题，支持在创建索引前预先划分 Region [#57551](https://github.com/pingcap/tidb/issues/57551) @[tangenta](https://github.com/tangenta)
    - 修复在大量表的场景下重启 TiDB 时，InfoSchema 加载速度过慢的问题 [#58821](https://github.com/pingcap/tidb/issues/58821) @[GMHDBJD](https://github.com/GMHDBJD)
    - 修复查询 `information_schema.tables` 可能出现 OOM 问题，优化系统表查询过程中的内存使用监控 [#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)
    - 修复收集统计信息失败时没有收集耗时的问题 [#58797](https://github.com/pingcap/tidb/issues/58797) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在异步加载统计信息时，加载的信息可能比当前同步加载的信息多 [#59107](https://github.com/pingcap/tidb/issues/59107) @[winoros](https://github.com/winoros)   
    - 修复 `sql_mode=only-full-group_by` 时，`UNION ALL` 语句不报错的问题 [#59211](https://github.com/pingcap/tidb/issues/59211) @[AilinKid](https://github.com/AilinKid) 
    - 修复统计信息使用的内部会话在遇到错误时可能没有被释放的问题，该问题可能导致内存泄漏 [#59524](https://github.com/pingcap/tidb/issues/59524) @[Rustin170506](https://github.com/Rustin170506)
    - 修复当 `column.hist.NDV` 的值大于 `column.topN.num()` 的值时，统计信息评估错误的问题 [#59563](https://github.com/pingcap/tidb/issues/59563) @[AilinKid](https://github.com/AilinKid)
    - 修复合并全局统计信息失败的问题 [#59274](https://github.com/pingcap/tidb/issues/59274) @[winoros](https://github.com/winoros)
    - 修复当 Fix Control #44855 开启时，TiDB 的会话可能崩溃的问题 [#59762](https://github.com/pingcap/tidb/issues/59762) @[winoros](https://github.com/winoros)
    - 修复在没有 hint 且 Join Key 不完全匹配的情况下，TiDB 选择 Merge Join 的问题 [#20710](https://github.com/pingcap/tidb/issues/20710) @[winoros](https://github.com/winoros)

+ TiKV

    - (dup): release-8.5.1.md > 错误修复> TiKV - 修复因 TiKV MVCC 内存引擎 (In-Memory Engine, IME) 预加载尚未初始化的副本导致 TiKV panic 的问题 [#18046](https://github.com/tikv/tikv/issues/18046) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复处理 GBK/GB18030 编码的数据时可能出现编码失败的问题 [#17618](https://github.com/tikv/tikv/issues/17618) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup): release-7.5.6.md > 错误修复> TiKV - 修复 Resolved-TS 监控和日志可能显示异常的问题 [#17989](https://github.com/tikv/tikv/issues/17989) @[ekexium](https://github.com/ekexium)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复在仅启用一阶段提交 (1PC) 而未启用异步提交 (Async Commit) 时，可能无法读取最新写入数据的问题 [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复时钟回退导致 RocksDB 流控异常，进而引发性能抖动的问题 [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.6.md > 错误修复> TiKV - 修复 Region 合并时可能因 Raft index 匹配异常而导致 TiKV 异常退出的问题 [#18129](https://github.com/tikv/tikv/issues/18129) @[glorv](https://github.com/glorv)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复 GC Worker 负载过高时可能出现的死锁问题 [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    - (dup): release-7.5.6.md > 错误修复> TiKV - 修复 CDC 连接在遇到异常时可能发生资源泄漏的问题 [#18245](https://github.com/tikv/tikv/issues/18245) @[wlwilliamx](https://github.com/wlwilliamx)
    - 修复错误的线程内存监控指标 [#18125](https://github.com/tikv/tikv/issues/18125) @[Connor1996](https://github.com/Connor1996)
    - 修复 TiKV 重启后出现非预期的 `Server is busy` 报错 [#18233](https://github.com/tikv/tikv/issues/18233) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复 Online Unsafe Recovery 因 Tiflash Learner 而卡住的问题 [#18197](https://github.com/tikv/tikv/issues/18197) @[v01dstar](https://github.com/v01dstar)

+ PD

    - (dup): release-6.5.12.md > 错误修复> PD - 修复设置 `tidb_enable_tso_follower_proxy` 系统变量可能不生效的问题 [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    - (dup): release-7.5.6.md > 错误修复> PD - 修复启用 `tidb_enable_tso_follower_proxy` 系统变量后，PD 可能出现 panic 的问题 [#8950](https://github.com/tikv/pd/issues/8950) @[okJiang](https://github.com/okJiang)
    - (dup): release-7.5.6.md > 错误修复> PD - 修复在导入或添加索引场景中，因 PD 网络不稳定可能导致操作失败的问题 [#8962](https://github.com/tikv/pd/issues/8962) @[okJiang](https://github.com/okJiang)
    - (dup): release-7.5.6.md > 错误修复> PD - 修复重启后 `flow-round-by-digit` 配置项的值可能被覆盖的问题 [#8980](https://github.com/tikv/pd/issues/8980) @[nolouch](https://github.com/nolouch)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复 TSO 分配过程中可能出现的内存泄漏问题 [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.6.md > 错误修复> PD - 修复单个日志文件 `max-size` 默认值未被正确设置的问题 [#9037](https://github.com/tikv/pd/issues/9037) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复长期运行的集群中可能出现的内存泄漏问题 [#9047](https://github.com/tikv/pd/issues/9047) @[bufferflies](https://github.com/bufferflies)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复当某个 PD 节点不是 Leader 时，仍可能生成 TSO 的问题 [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复 PD Leader 切换过程中，Region syncer 未能及时退出的问题 [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    - 修复 `minResolvedTS` 没有初始化导致 TiDB panic 的问题 [#8964](https://github.com/tikv/pd/issues/8964) @[rleungx](https://github.com/rleungx)
    - 修复 PD Client 重试策略没有正确初始化的问题 [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    - 修复通过 API 查询不存在的 Region 时报错信息有误的问题 [#8868](https://github.com/tikv/pd/issues/8868) @[lhy1024](https://github.com/lhy1024)
    - 修复 ping API 被错误转发的问题 [#9031](https://github.com/tikv/pd/issues/9031) @[rleungx](https://github.com/rleungx)
    - 修复 TTL cache goroutine 泄露的问题 [#9047](https://github.com/tikv/pd/issues/9047) @[bufferflies](https://github.com/bufferflies)
    - 修复微服务模式下转发 TSO 可能导致 TiDB panic 的问题 [#9091](https://github.com/tikv/pd/issues/9091) @[lhy1024](https://github.com/lhy1024)
    - 修复 PD 网络问题可能导致 TSO Client 无法初始化的问题 [#58239](https://github.com/pingcap/tidb/issues/58239) @[okJiang](https://github.com/okJiang)

+ TiFlash

    - 修复 TiFlash 处理包含时区的 `IN(Timestamp)` 或 `IN(Time)` 表达式时结果错误的问题 [#9778](https://github.com/pingcap/tiflash/issues/9778) @[solotzg](https://github.com/solotzg)
    - 修复 TiFlash 在处理溢出错误时行为与 TiDB 不兼容，导致 `IMPORT INTO` 语句执行失败的问题 [#9752](https://github.com/pingcap/tiflash/issues/9752) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 TiFlash 在执行作为窗口函数使用的聚合函数时出现内存泄漏的问题 [#9930](https://github.com/pingcap/tiflash/issues/9930) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 TiFlash 在执行作为窗口函数使用的聚合函数时可能出现空指针的问题 [#9964](https://github.com/pingcap/tiflash/issues/9964) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复 TiFlash 在内存占用较低的情况下，可能意外拒绝处理 Raft 消息的问题 [#9745](https://github.com/pingcap/tiflash/issues/9745) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在分区表上执行 `ALTER TABLE ... RENAME COLUMN` 后，查询该表可能报错的问题 [#9787](https://github.com/pingcap/tiflash/issues/9787) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-6.5.12.md > 错误修复> TiFlash - 修复在导入大量数据后，TiFlash 可能持续占用较高内存的问题 [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在存算分离架构下，TiFlash 计算节点可能被错误选为添加 Region peer 的目标节点的问题 [#9750](https://github.com/pingcap/tiflash/issues/9750) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在某些情况下 TiFlash 意外退出时无法打印错误堆栈的问题 [#9902](https://github.com/pingcap/tiflash/issues/9902) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复当 `profiles.default.init_thread_count_scale` 设置为 `0` 时，TiFlash 启动可能会卡住的问题 [#9906](https://github.com/pingcap/tiflash/issues/9906) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在查询涉及虚拟列并且触发远程读时，可能会出现 `Not found column` 错误的问题 [#9561](https://github.com/pingcap/tiflash/issues/9561) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在向包含向量索引的表中插入数据后，部分磁盘数据可能未能及时清理，从而导致磁盘空间异常占用的问题 [#9946](https://github.com/pingcap/tiflash/issues/9946) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当集群中表包含大量 `ENUM` 类型列时，TiFlash 内存占用异常升高的问题 [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在存算分离架构下 TiFlash 可能打印大量 `tag=EnumParseOverflowContainer` 日志的问题 [#9955](https://github.com/pingcap/tiflash/issues/9955) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-6.5.12.md > 错误修复> Tools> Backup & Restore (BR) - 修复使用 `br log status --json` 查询日志备份任务时，返回结果中缺少任务状态 `status` 字段的问题 [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.6.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 无法恢复大于 3072 字节的索引的问题 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.12.md > 错误修复> Tools> Backup & Restore (BR) - 修复 BR 向 TiKV 发送请求时收到 `rpcClient is idle` 错误导致恢复失败的问题 [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        - (dup): release-7.5.6.md > 错误修复> Tools> Backup & Restore (BR) - 修复日志备份在无法访问 PD 时，遇到致命错误无法正确退出的问题 [#18087](https://github.com/tikv/tikv/issues/18087) @[YuJuncen](https://github.com/YuJuncen)
        - 修复在断点恢复时额外检查存储节点可用空间的问题 [#54316](https://github.com/pingcap/tidb/issues/54316) @[Leavrth](https://github.com/Leavrth)
        - 修复在全量备份过程中 RangeTree 结果内存使用效率低下的问题 [#58587](https://github.com/pingcap/tidb/issues/58587) @[3pointer](https://github.com/3pointer)
        - 修复当集群存在大量表但实际数据量较小时，PITR 数据恢复任务可能出现 `Information schema is out of date` 报错的问题 [#57743](https://github.com/pingcap/tidb/issues/57743) @[Leavrth](https://github.com/Leavrth)
        - 修复解析外部存储 URL 导致外部存储的 Backend 错误的问题 [#59548](https://github.com/pingcap/tidb/issues/59548) @[Leavrth](https://github.com/Leavrth)
        - 修复恢复过程中 Table ID 预分配错误的问题 [#59718](https://github.com/pingcap/tidb/issues/59718) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 修复 PD 切换 leader 后，changefeed 同步延迟显著增加的问题 [#11997](https://github.com/pingcap/tiflow/issues/11997) @[lidezhu](https://github.com/lidezhu)
        - 修复当 changefeed 下游的连接协议为 `pulsar + http` 或 `pulsar + https` 时，部分配置项未生效的问题 [#12068](https://github.com/pingcap/tiflow/issues/12068) @[SandeepPadhi](https://github.com/SandeepPadhi)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 TiCDC 同步 `CREATE TABLE IF NOT EXISTS` 或 `CREATE DATABASE IF NOT EXISTS` 语句时可能出现 panic 的问题 [#11839](https://github.com/pingcap/tiflow/issues/11839) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复在集群扩容出新的 TiKV 节点后 Changefeed 可能会卡住的问题 [#11766](https://github.com/pingcap/tiflow/issues/11766) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复由于 Sarama 客户端乱序重发消息导致 Kafka 消息乱序的问题 [#11935](https://github.com/pingcap/tiflow/issues/11935) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 TiCDC 在 `RENAME TABLE` 操作中使用了错误的表名进行过滤的问题 [#11946](https://github.com/pingcap/tiflow/issues/11946) @[wk989898](https://github.com/wk989898)
        - (dup): release-7.5.6.md > 错误修复> Tools> TiCDC - 修复在删除 Changefeed 后 goroutine 泄漏的问题 [#11954](https://github.com/pingcap/tiflow/issues/11954) @[hicqu](https://github.com/hicqu)
        - (dup): release-8.5.1.md > 错误修复> Tools> TiCDC - 修复 Debezium 协议中 NOT NULL timestamp 类型字段的默认值不正确的问题 [#11966](https://github.com/pingcap/tiflow/issues/11966) @[wk989898](https://github.com/wk989898)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 TiCDC 通过 Avro 协议同步 `default NULL` SQL 语句时报错的问题 [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 PD 缩容后 TiCDC 无法正确连接 PD 的问题 [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复当上游将一个新增的列的默认值从 `NOT NULL` 修改为 `NULL` 后，下游默认值错误的问题 [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)

    + TiDB Data Migration (DM)

        - 修复未将系统表加入默认过滤列表导致 dump 任务失败的问题 [#11984](https://github.com/pingcap/tiflow/issues/11984) @[River2000i](https://github.com/River2000i)
        - 修复 DM 仅检查 `LightningTableEmptyChecking` 导致任务失败的问题 [#11945](https://github.com/pingcap/tiflow/issues/11945) @[River2000i](https://github.com/River2000i)
        - 修复 DM 不能备份至 Azure 的问题 [#11912](https://github.com/pingcap/tiflow/issues/11912) @[River2000i](https://github.com/River2000i)

    + TiDB Lightning

        - (dup): release-6.5.12.md > 错误修复> Tools> TiDB Lightning - 修复日志没有正确脱敏的问题 [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)

## 性能测试

<!--
如需了解 TiDB v9.0.0 的性能表现，你可以参考 TiDB Cloud Dedicated 集群的[性能测试报告](https://docs.pingcap.com/tidbcloud/v9.0-performance-highlights)（英文版）。
-->

## 贡献者

感谢来自 TiDB 社区的贡献者们：
