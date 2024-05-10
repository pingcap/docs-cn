---
title: TiDB 8.1.0 Release Notes
summary: 了解 TiDB 8.1.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.1.0 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：8.1.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.1.0#version-list)

TiDB 8.1.0 为长期支持版本 (Long-Term Support Release, LTS)。

相比于前一个 LTS（即 7.5.0 版本），8.1.0 版本包含 [7.6.0-DMR](/releases/release-7.6.0.md) 和 [8.0.0-DMR](/releases/release-8.0.0.md) 中已发布的新功能、提升改进和错误修复。当你从 7.5.x 升级到 8.1.0 时，可以下载 [TiDB Release Notes PDF](https://download.pingcap.org/tidb-v7.6-to-v8.1-zh-release-notes.pdf) 查看两个 LTS 版本之间的所有 release notes。下表列出了从 7.6.0 到 8.1.0 的一些关键特性：

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
    <td rowspan="5">可扩展性与性能</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/br-snapshot-guide#恢复快照备份数据">提升 BR 快照恢复速度（从 v8.0.0 开始 GA）</a></td>
    <td>通过该功能，BR 可以充分利用集群的规模优势，使 TiKV 集群中的所有节点都能参与到数据恢复的准备阶段，从而显著提升大规模集群中大数据集的恢复速度。实际测试表明，该功能可将下载带宽打满，下载速度可提升 8 到 10 倍，端到端恢复速度大约提升 1.5 到 3 倍。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/ddl-v2">建表性能提升 10 倍</a>（实验特性，从 v7.6.0 开始引入）</td>
    <td>在 v7.6.0 中引入了新的 DDL 架构，批量建表的性能提高了 10 倍。这一重大改进极大地缩短了创建大量表所需的时间。特别是在 SaaS 场景中，快速创建大量表（从数万到数十万不等）是一个常见的挑战，使用该特性能显著提升 SaaS 场景的建表速度。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/tune-region-performance#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力">通过 Active PD Follower 提升 PD Region 信息查询服务的扩展能力（实验特性，从 v7.6.0 开始引入）</a></td>
    <td>TiDB v7.6.0 实验性地引入了 Active PD Follower 特性，允许 PD follower 提供 Region 信息查询服务。在 TiDB 节点数量较多和 Region 数量较多的集群中，该特性可以提升 PD 集群处理 <code>GetRegion</code>、<code>ScanRegions</code> 请求的能力，减轻 PD leader 的 CPU 压力。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/system-variables#tidb_dml_type-从-v800-版本开始引入">用于处理更大事务的批量 DML 执行方式（实验特性，从 v8.0.0 开始引入）</a></td>
    <td>大批量的 DML 任务，例如大规模的清理任务、连接或聚合，可能会消耗大量内存，并且在非常大的规模上受到限制。批量 DML (<code>tidb_dml_type = "bulk"</code>) 是一种新的 DML 类型，用于更高效地处理大批量 DML 任务，同时提供事务保证并减轻 OOM 问题。该功能与用于数据加载的导入、加载和恢复操作不同。</td>
  </tr>
  <tr>
    <td>增强在有大量表时缓存 schema 信息的稳定性（实验特性，从 v8.0.0 开始引入）</td>
    <td>对于使用 TiDB 作为多租户应用程序记录系统的 SaaS 公司，经常需要存储大量的表。在以前的版本中，尽管支持处理百万级或更大数量的表，但可能会影响用户体验。TiDB v8.0.0 通过以下增强功能改善了这一问题：
      <ul>
      <li>引入新的 <a href="https://docs.pingcap.com/zh/tidb/v8.1/system-variables#tidb_schema_cache_size-从-v800-版本开始引入">schema 缓存系统</a>，为表元数据提供了基于 LRU (Least Recently Used) 算法的缓存策略，优先将最近访问频率较高的表元数据存储在缓存中，从而减少表数量较多场景下的内存占用。</li>
      <li>支持在 <code>auto analyze</code> 中配置<a href="https://docs.pingcap.com/zh/tidb/v8.1/system-variables#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入">优先队列</a>，使流程更加流畅，并在大量表的情况下提高稳定性。</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td rowspan="5">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/tidb-global-sort">全局排序成为正式功能</a>（从 v8.0.0 开始 GA）**tw@qiancai**</td>
    <td>全局排序功能旨在提高 <code>IMPORT INTO</code> 和 <code>CREATE INDEX</code> 的稳定性与效率。通过对需要处理的数据进行全局排序，可以提高数据写入 TiKV 的稳定性、可控性和可扩展性，从而提升数据导入与索引添加的用户体验和服务质量。启用全局排序后，单条 <code>IMPORT INTO</code> 或 <code>CREATE INDEX</code> 语句目前已经支持对高达 40 TiB 的数据进行导入或者添加索引。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/sql-plan-management#跨数据库绑定执行计划-cross-db-binding">跨数据库绑定执行计划</a>（从 v7.6.0 开始引入）</td>
    <td>在处理上百个 schema 相同的数据库时，针对其中一个数据库的 SQL binding 通常也适用于其它的数据库。例如，在 SaaS 或 PaaS 数据平台中，每个用户通常各自维护单独的数据库，这些数据库具有相同的 schema 并运行着类似的 SQL。在这种情况下，逐一为每个数据库做 SQL 绑定是不切实际的。TiDB v7.6.0 引入跨数据库绑定执行计划，支持在所有 schema 相同的数据库之间匹配绑定计划。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/tiproxy-overview">支持 TiProxy（从 v8.0.0 开始 GA）</a></td>
    <td>全面支持 TiProxy，可通过部署工具轻松部署。TiProxy 可以管理和维护客户端与 TiDB 的连接，在滚动重启、升级以及扩缩容过程中保持连接。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/dm-compatibility-catalog">Data Migration (DM) 正式支持迁移 MySQL 8.0（从 v7.6.0 开始 GA）</a></td>
    <td>在 v7.6.0 之前，DM 迁移 MySQL 8.0 仅为实验特性，不能用于生产环境。TiDB v7.6.0 增强了该功能的稳定性、兼容性，可在生产环境帮助你平滑、快速地将数据从 MySQL 8.0 迁移到 TiDB。在 v7.6.0 中，该功能正式 GA。</td>
  </tr>
  <tr>
    <td>资源管控支持<a href="https://docs.pingcap.com/zh/tidb/v8.1/tidb-resource-control#管理资源消耗超出预期的查询-runaway-queries">管理资源消耗超出预期的查询</a> (GA) **tw@lilin90**</td>
    <td>通过资源组的规则，TiDB 能够自动识别出运行超出预期的查询，并对该查询进行限流或取消处理。即使没有被规则识别，你仍然可以手动添加查询特征以及采取对应的措施，从而降低突发的查询性能问题对整个数据库的影响。</td>
  </tr>
  <tr>
    <td rowspan="1">数据库管理与可观测性</td>
    <td>支持观测索引使用情况（从 v8.0.0 开始引入）</td>
    <td>正确的索引设计是提升数据库性能的重要前提。TiDB v8.0.0 引入内存表 <a href="https://docs.pingcap.com/zh/tidb/v8.1/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a> 和视图 <a href="https://docs.pingcap.com/zh/tidb/v8.1/sys-schema-unused-indexes"><code>sys.schema_unused_indexes</code></a>，用于记录索引的使用情况。该功能有助于用户评估数据库中索引的效率并优化索引设计。</td>
  </tr>
  <tr>
    <td rowspan="3">数据迁移</td>
    <td>TiCDC 支持 <a href="https://docs.pingcap.com/zh/tidb/v8.1/ticdc-simple-protocol">Simple 协议</a>（从 v8.0.0 开始引入）</td>
    <td>TiCDC 支持了新的 Simple 消息协议，该协议通过在 DDL 和 BOOTSTRAP 事件中嵌入表的 schema 信息，实现了对 schema 信息的动态追踪 (in-band schema tracking)。</td>
  </tr>
  <tr>
    <td>TiCDC 支持 <a href="https://docs.pingcap.com/zh/tidb/v8.1/ticdc-debezium">Debezium 协议</a>（从 v8.0.0 开始引入）</td>
    <td>TiCDC 支持了新的 Debezium 协议，TiCDC 可以使用该协议生成 Debezium 格式的数据变更事件并发送给 Kafka sink。</td>
  </tr>
  <tr>
    <td>TiCDC 支持<a href="https://docs.pingcap.com/zh/tidb/v8.1/ticdc-client-authentication.md">客户端鉴权</a>（从 v8.1.0 开始引入）**tw@Oreoxmt**</td>
    <td>TiCDC 支持使用 mTLS（双向传输层安全性协议）或 TiDB 用户名密码进行客户端鉴权。该功能允许命令行工具或 OpenAPI 客户端验证与 TiCDC 的连接。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 稳定性

* 管理资源消耗超出预期的查询 (GA) [#43691](https://github.com/pingcap/tidb/issues/43691) @[nolouch](https://github.com/nolouch) **tw@lilin90** <!--1447-->

    突发的 SQL 性能问题引发数据库整体性能下降，是数据库稳定性最常见的挑战。造成 SQL 性能问题的原因有很多，例如未经充分测试的新 SQL、数据量剧烈变化、执行计划突变等，这些问题很难从源头上完全规避。在过去的版本中，TiDB 增加了对资源超出预期的查询的管理能力，以快速减小 SQL 性能造成的影响范围，这个功能在 v8.1.0 成为正式功能。

    你可以针对某个资源组 (Resource Group) 设置查询的最长执行时间。当查询的执行时间超过设置值时，自动降低查询的优先级或者取消查询。你还可以设置在一段时间内通过文本或者执行计划立即匹配已经识别出的查询，从而避免问题查询的并发度太高时，在识别阶段就造成大量资源消耗的情况。

    TiDB 同时支持手动标记查询的功能。利用命令 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)，你可以根据 SQL 的文本、SQL Digest 或执行计划标记查询，命中的查询可以被降级或取消，达到添加 SQL 黑名单的目的。

    对资源消耗超出预期的查询的自动管理能力为用户提供了有效的手段，在根本原因被定位之前，该功能可以快速缓解查询问题对整体性能的影响，从而提升数据库的稳定性。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

### SQL 功能

* 支持在 TiDB 建表时使用更多的表达式设置列的默认值成为正式功能 (GA) [#50936](https://github.com/pingcap/tidb/issues/50936) @[zimulala](https://github.com/zimulala) **tw@hfxsd** <!--1794-->

    在 v8.0.0 之前，建表时指定列的默认值仅限于固定的字符串、数字、日期和个别表达式。从 v8.0.0 开始，TiDB 支持使用更多表达式作为列的默认值，例如将列的默认值设置为 `DATE_FORMAT`，从而满足多样化的业务需求。在 v8.1.0 中，该特性成为正式功能。
    
    从 v8.1.0 开始，支持在使用 `ADD COLUMN` 添加列时使用表达式作为默认值。

    更多信息，请参考[用户文档](/data-type-default-values.md#表达式默认值)。

### 数据库管理

* 默认开启 TiDB 分布式执行框架，提升并行执行 `ADD INDEX` 或 `IMPORT INTO` 任务的性能和稳定性 [#52441](https://github.com/pingcap/tidb/issues/52441) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai**

    TiDB 分布式执行框架在 v7.5.0 中成为正式功能 (GA)，但默认关闭，即一个 `ADD INDEX` 或 `IMPORT INTO` 任务默认只能由一个 TiDB 节点执行。

    从 v8.1.0 起，该功能默认开启（[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入) 默认为 `ON`）。开启后，分布式执行框架可以调度多个 TiDB 节点并行执行同一个 `ADD INDEX` 或 `IMPORT INTO` 任务，从而充分利用 TiDB 集群的资源，大幅提升这些任务的性能。此外，你还可以通过增加 TiDB 节点并为新增的节点配置 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) 来线性提升 `ADD INDEX` 和 `IMPORT INTO` 任务的性能。

    更多信息，请参考[用户文档](/tidb-distributed-execution-framework.md)。

### 安全

* 增强 TiDB 日志脱敏 (GA) [#52364](https://github.com/pingcap/tidb/issues/52364) @[xhebox](https://github.com/xhebox) **tw@hfxsd** <!--1817-->

    TiDB 日志脱敏增强是通过对日志文件中的 SQL 文本信息进行标记，支持在查看日志时删除敏感数据。你可以控制是否对日志信息进行标记，以实现在不同场景下安全使用 TiDB 日志，提升了使用日志脱敏能力的安全性和灵活性。要使用此功能，可以将系统变量 `tidb_redact_log` 的值设置为 `MARKER`，此时 TiDB 运行日志中的 SQL 文本会被标记。还可以通过 TiDB server 的 `collect-log` 子命令将日志中标记的敏感数据删除，在数据安全的情况下展示日志；或移除所有标记，获取正常日志。该功能在 v8.1.0 成为正式功能。

    更多信息，请参考[用户文档](/system-variables.md#tidb_redact_log)。

### 数据迁移

* `IMPORT INTO ... FROM SELECT` 语法成为正式功能 (GA) [#49883](https://github.com/pingcap/tidb/issues/49883) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1791-->

    在 v8.0.0 之前的版本中，将查询结果导入目标表只能通过 `INSERT INTO ... SELECT` 语句，但该语句在一些大数据量的场景中导入效率较低。在 v8.0.0 中，TiDB 以实验特性新增支持通过 `IMPORT INTO ... FROM SELECT` 将 `SELECT` 的查询结果导入到一张空的 TiDB 目标表中，其性能最高可达 `INSERT INTO ... SELECT` 的 8 倍，可以大幅缩短导入所需的时间。此外，你还可以通过 `IMPORT INTO ... FROM SELECT` 导入使用 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

    在 v8.1.0 中，`IMPORT INTO ... FROM SELECT` 语法成为正式功能 (GA)，丰富了 `IMPORT INTO` 语句的功能场景。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-import-into.md)。

* TiDB Lightning 简化冲突处理策略，同时支持以 `replace` 方式处理冲突数据的功能成为正式功能 (GA) [#51036](https://github.com/pingcap/tidb/issues/51036) @[lyzx2001](https://github.com/lyzx2001) **tw@qiancai** <!--1795-->

    在 v8.0.0 之前的版本中，TiDB Lightning 逻辑导入模式有[一套数据冲突处理策略](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md#冲突数据检测)，而物理导入模式有[两套数据冲突处理策略](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#冲突数据检测)，不易理解和配置。

    在 v8.0.0 中，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，并以实验特性支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) 参数统一控制逻辑导入和物理导入模式的冲突检测策略，并简化了该参数的配置。此外，在物理导入模式下，当导入遇到主键或唯一键冲突的数据时，`replace` 策略支持保留最新的数据、覆盖旧的数据。在 v8.1.0 中，以 `replace` 方式处理冲突数据的功能成为正式功能 (GA)。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-configuration.md)。

* TiCDC 支持客户端鉴权 [#10636](https://github.com/pingcap/tiflow/issues/10636) @[CharlesCheung96](https://github.com/CharlesCheung96) **tw@Oreoxmt** <!--1717-->

    在 v8.1.0 中，当使用 TiCDC CLI 或 OpenAPI 时，TiCDC 支持客户端鉴权。你可以配置 TiCDC 要求客户端使用证书进行鉴权，以实现 mTLS（双向传输层安全性协议）。此外，你还可以使用 TiDB 用户名密码进行客户端鉴权。

    更多信息，请参考[用户文档](/ticdc/ticdc-client-authentication.md)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.0.0 升级至当前版本 (v8.1.0) 所需兼容性变更信息。如果从 v7.6.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 行为变更 1

* 行为变更 2

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型 | 描述 |
|--------|------------------------------|------|
|        |                              |      |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入) | 修改 | 默认值从 `OFF` 修改为 `ON`，代表默认开启分布式执行框架，从而充分利用 TiDB 集群的资源，大幅提升 `ADD INDEX` 和 `IMPORT INTO` 任务的性能。如果要从低版本的集群升级到 v8.1.0 或更高版本，且该集群已开启分布式执行框架，为了避免升级期间 `ADD INDEX` 操作可能导致数据索引不一致的问题，请在升级前关闭分布式执行框架（即将 `tidb_enable_dist_task` 设置为 `OFF`），升级后再手动开启。|
| [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) | 修改  | 该变量的可选值从 "" 或 `background` 修改为长度小于或等于 64 的字符串，可用合法字符包括数字 `0-9`、字母 `a-zA-Z`、下划线 `_` 和连字符 `-`，从而更灵活地控制各 TiDB 节点的服务范围。分布式执行框架将会根据该变量的值决定将分布式任务调度到哪些 TiDB 节点上执行，具体规则请参考[`任务调度`](/tidb-distributed-execution-framework.md#任务调度)。 |
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件           | 配置项                | 修改类型 | 描述                                 |
|----------------|--------------------|------|------------------------------------|
| TiDB Lightning | [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) | 修改   | 默认值从 `9223372036854775807` 修改为 `10000`，从而迅速中断异常任务，以便用户尽快进行相应调整。这避免了在导入完成后，才发现是因为数据源异常或表结构定义错误导致导入了大量冲突数据，从而节省时间和计算资源。 |
| TiDB Lightning | [conflict.max-record-rows](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) | 修改   | 从 v8.1.0 开始，TiDB Lightning 会自动将 `conflict.max-record-rows` 的值设置为 `conflict.threshold` 的值，并忽略用户输入，因此无需再单独配置 `conflict.max-record-rows`。`conflict.max-record-rows` 将在未来版本中废弃。 |
| TiCDC | [security.client-allowed-user](ticdc/ticdc-server-config.md#cdc-server-配置文件说明) | 新增 | 指定可用于客户端鉴权的用户名，列表中不存在的用户的鉴权请求将被直接拒绝。默认值为 null。|
| TiCDC | [security.client-user-required](ticdc/ticdc-server-config.md#cdc-server-配置文件说明) | 新增 | 控制是否使用 TiDB 的用户名和密码进行客户端鉴权，默认值为 `false`。|
| TiCDC | [security.mtls](ticdc/ticdc-server-config.md#cdc-server-配置文件说明)            | 新增 | 控制是否开启 TLS 客户端鉴权，默认值为 `false`。|
| TiCDC | [sink.open.output-old-value](ticdc/ticdc-changefeed-config.md#TiCDC-Changefeed-配置文件说明) | 新增 | 控制是否输出行数据更改前的值。默认值为 `true`。关闭后，Update 事件不会输出 "p" 字段的数据。 |
| TiCDC | [sink.debezium.output-old-value](ticdc/ticdc-changefeed-config.md#TiCDC-Changefeed-配置文件说明) | 新增 | 控制是否输出行数据更改前的值。默认值为 `true`。关闭后，Update 事件不会输出 "before" 字段的数据。 |
|                |                    |      |                                    |

### 其他

## 离线包变更

## 废弃功能

* 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
* TiDB Lightning 参数 `conflict.max-record-rows` 计划在未来版本中废弃，并在后续版本中删除。该参数将由 `conflict.threshold` 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。
* 从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) 参数统一控制逻辑导入和物理导入模式的冲突检测策略。旧版冲突检测的参数 [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) 将在未来版本中被移除。

## 改进提升

+ TiDB
  <!--tw@Oreoxmt 7 -->
    - 优化外键在 `SHOW CREATE TABLE` 结果中的 MySQL 兼容性 [#51837](https://github.com/pingcap/tidb/issues/51837) @[negachov](https://github.com/negachov)
    - 优化表达式默认值在 `SHOW CREATE TABLE` 结果中的 MySQL 兼容性 [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 允许使用 ingest 模式并发添加多个索引 [#52596](https://github.com/pingcap/tidb/issues/52596) @[lance6716](https://github.com/lance6716)
    - 允许将系统变量 `tidb_service_scope` 设置为不同的值，以更好地利用分布式框架功能 [#52441](https://github.com/pingcap/tidb/issues/52441) @[ywqzzy](https://github.com/ywqzzy)
    - 增强 TiDB 对总是 `false` 的 DNF 的处理，直接忽略这种过滤条件 [#40997](https://github.com/pingcap/tidb/issues/40997) @[hi-rustin](https://github.com/hi-rustin)
    - 不允许将系统变量 `tidb_auto_analyze_ratio` 设置为 `0` [#51582](https://github.com/pingcap/tidb/issues/51582) @[hi-rustin](https://github.com/hi-rustin)
    - 当查询可以选择除全表扫描以外的单索引扫描方式时，支持以 Optimizer Fix Controls 的方式解除优化器不会自动选择索引合并的限制 [#52869](https://github.com/pingcap/tidb/issues/52869) @[time-and-fate](https://github.com/time-and-fate)
    - 在 Coprocessor 算子的实际执行信息 `execution info` 中添加 `total_kv_read_wall_time` 指标 [#28937](https://github.com/pingcap/tidb/issues/28937) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-7.1.5.md > 改进提升> TiDB - 为 LDAP 身份认证添加超时机制，避免资源锁 (RLock) 无法及时释放的问题 [#51883](https://github.com/pingcap/tidb/issues/51883) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    - (dup): release-6.5.9.md > 改进提升> TiKV - 在 raftstore 线程中避免进行快照文件的 IO 操作，提高 TiKV 稳定性 [#16564](https://github.com/tikv/tikv/issues/16564) @[Connor1996](https://github.com/Connor1996)

+ PD
  <!--tw@qiancai 1 -->
    - 优化调度 operator 相关逻辑竞争锁的开销 [#7897](https://github.com/tikv/pd/issues/7897) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)
      <!--tw@hfxsd 2 -->
        - (dup): release-7.1.5.md > 改进提升> Tools> Backup & Restore (BR) - 增加 PITR 集成测试用例，覆盖对日志备份与添加索引加速功能的兼容性测试 [#51987](https://github.com/pingcap/tidb/issues/51987) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.1.5.md > 改进提升> Tools> Backup & Restore (BR) - 移除日志备份启动时检查是否存在活动 DDL job 的无效检查 [#52733](https://github.com/pingcap/tidb/issues/52733) @[Leavrth](https://github.com/Leavrth)
        - 增加测试用例测试 PITR 和添加索引加速兼容性 [#51988](https://github.com/pingcap/tidb/issues/51988) @[Leavrth](https://github.com/Leavrth)
        - BR 恢复过程中清理空 sst 文件 [#16005](https://github.com/tikv/tikv/issues/16005) @[Leavrth](https://github.com/Leavrth)

    + TiCDC
      <!--tw@hfxsd 2 -->
        - 提升使用 redo log 恢复数据过程中的内存稳定性，减少 OOM 的概率 [#10900](https://github.com/pingcap/tiflow/issues/10900) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 显著提升事务冲突场景中的数据同步的稳定性，性能最高提升可达 10 倍 [#10896](https://github.com/pingcap/tiflow/issues/10896) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + Dumpling

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Binlog

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 错误修复

+ TiDB
  <!--tw@Oreoxmt 以下 12 条 -->
    - 修复当 SQL 语句涉及包含多值索引的表时，执行可能报错 `Can't find a proper physical plan for this query` 的问题 [#49438](https://github.com/pingcap/tidb/issues/49438) @[qw4990](https://github.com/qw4990)
    - 修复自动分析在 OOM 后卡住的问题 [#51993](https://github.com/pingcap/tidb/issues/51993) @[hi-rustin](https://github.com/hi-rustin)
    - 修复使用 BR 恢复一张表后，即使该表没有统计信息，统计信息健康度仍然显示为 100% 的问题 [#29769](https://github.com/pingcap/tidb/issues/29769) @[winoros](https://github.com/winoros)
    - 修复 TiDB 在升级过程中会为系统表创建统计信息的问题 [#52040](https://github.com/pingcap/tidb/issues/52040) @[hi-rustin](https://github.com/hi-rustin)
    - 修复 TiDB 在统计信息初始化完成前就进行自动分析的问题 [#52346](https://github.com/pingcap/tidb/issues/52346) @[hi-rustin](https://github.com/hi-rustin)
    - 修复启用 `tidb_mem_quota_analyze` 时，自动分析使用的内存超过限制可能导致 TiDB crash 的问题 [#52601](https://github.com/pingcap/tidb/issues/52601) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 TiDB 统计信息同步加载机制无限重试加载空统计信息并打印 `fail to get stats version for this histogram` 日志的问题 [#52657](https://github.com/pingcap/tidb/issues/52657) @[hawkingrei](https://github.com/hawkingrei)
    - 修复关闭新排序规则框架时，涉及不同排序规则的表达式可能导致查询 panic 的问题 [#52772](https://github.com/pingcap/tidb/issues/52772) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 `CPS by type` 监控项显示错误的问题 [#52605](https://github.com/pingcap/tidb/issues/52605) @[nolouch](https://github.com/nolouch)
    - 修复查询 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 出现空指针的问题 [#52013](https://github.com/pingcap/tidb/issues/52013) @[JmPotato](https://github.com/JmPotato)
    - 修复指定非法列默认值时的错误提示信息 [#51592](https://github.com/pingcap/tidb/issues/51592) @[danqixu](https://github.com/danqixu)
    - 修复 ingest 模式添加索引时，在某些特殊情况下导致数据索引不一致的问题 [#51954](https://github.com/pingcap/tidb/issues/51954) @[lance6716](https://github.com/lance6716)
  <!--tw@lilin90 以下 18 条 -->
    - 修复了恢复含有外键的表时，DDL 卡住的问题 [#51838](https://github.com/pingcap/tidb/issues/51838) @[YangKeao](https://github.com/YangKeao)
    - 修复了加索引期间 TiDB 网络隔离导致加索引失败的问题 [#51846](https://github.com/pingcap/tidb/issues/51846) @[ywqzzy](https://github.com/ywqzzy)
    - 修复了重命名索引后再添加同名索引时的报错问题 [#51431](https://github.com/pingcap/tidb/issues/51431) @[lance6716](https://github.com/lance6716)
    - 修复了添加索引期间升级集群导致的数据索引不一致问题 [#52411](https://github.com/pingcap/tidb/issues/52411) @[tangenta](https://github.com/tangenta)
    - 修复了开启分布式框架后为大数据量表添加索引不成功的问题 [#52640](https://github.com/pingcap/tidb/issues/52640) @[tangenta](https://github.com/tangenta)
    - 修复了并发添加索引时报 “文件不存在” 错误的问题 [#52475](https://github.com/pingcap/tidb/issues/52475) @[tangenta](https://github.com/tangenta)
    - 修复了添加索引失败后清理不掉临时数据的问题 [#52639](https://github.com/pingcap/tidb/issues/52639) @[lance6716](https://github.com/lance6716)
    - 修复了元数据锁在 plan cache 场景下未能阻止 DDL 推进的问题 [#51407](https://github.com/pingcap/tidb/issues/51407) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复了执行 IMPORT INTO 大数据量任务时卡住的问题 [#52884](https://github.com/pingcap/tidb/issues/52884) @[lance6716](https://github.com/lance6716)
    - 修复了记录 GRPC 错误时 TIDB 意外重启的问题 [#52179](https://github.com/pingcap/tidb/issues/52179) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复了 IndexHashJoin 在执行 Anti Left Outer Semi Join 计算时输出冗余数据的问题 [#52923](https://github.com/pingcap/tidb/issues/52923) @[yibin87](https://github.com/yibin87)
    - 修复了 HashJoin Probe 执行时间统计不精确的问题 [#52227](https://github.com/pingcap/tidb/issues/52227) @[windtalker](https://github.com/windtalker)
    - 修复了在分区裁剪模式为 static 情况下，使用 tablesample 返回错误结果的问题 [#52282](https://github.com/pingcap/tidb/issues/52282) @[tangenta](https://github.com/tangenta)
    - 修复 TTL 功能在非默认时区下的错误 [#51675](https://github.com/pingcap/tidb/issues/51675) @[lcwangchao](https://github.com/lcwangchao)
    - 修复监控面板中链接数的计算和显示错误 [#51889](https://github.com/pingcap/tidb/issues/51889) @[YangKeao](https://github.com/YangKeao)
    - 修复回滚改写分区 DDL 任务时，状态卡住的问题 [#51090](https://github.com/pingcap/tidb/issues/51090) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 lighting 导入后 TiDB 意外重启 [#52827](https://github.com/pingcap/tidb/issues/52827) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 TiDB `explain analyze` 结果中 `max_remote_stream` 显示不正确的问题 [#52646](https://github.com/pingcap/tidb/issues/52646) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复查询 `TIDB_HOT_REGIONS` 表时结果返回内存表的问题 [#50810](https://github.com/pingcap/tidb/issues/50810) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复当某些列的统计信息没有完全加载时，`EXPLAIN` 语句的结果中可能会显示错误的列 ID 的问题 [#52207](https://github.com/pingcap/tidb/issues/52207) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复 `IFNULL` 函数返回的类型和 MySQL 不一致的问题 [#51765](https://github.com/pingcap/tidb/issues/51765) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复添加唯一索引可能导致 TiDB panic 的问题 [#52312](https://github.com/pingcap/tidb/issues/52312) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV

    - (dup): release-7.1.5.md > 错误修复> TiKV - 修复由于过时的 Region peer 忽略 GC 消息导致 resolve-ts 被阻塞的问题 [#16504](https://github.com/tikv/tikv/issues/16504) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.9.md > 错误修复> TiKV - 修复 RocksDB 中非活跃的 WAL (Write Ahead Log) 可能损毁数据的问题 [#16705](https://github.com/tikv/tikv/issues/16705) @[Connor1996](https://github.com/Connor1996)

+ PD
  <!--tw@qiancai 9 -->
    - 修复切换 PD 模式时 TSO 可能卡住的问题 [#7849](https://github.com/tikv/pd/issues/7849) @[JmPotato](https://github.com/JmPotato)
    - 修复 DR Auto Sync 监控状态显示的问题 [#7974](https://github.com/tikv/pd/issues/7974) @[lhy1024](https://github.com/lhy1024)
    - 修复检查 binary 版本时可能导致的 panic 问题 [#7978](https://github.com/tikv/pd/issues/7978) @[JmPotato](https://github.com/JmPotato)
    - 修复 TTL 参数类型转换错误的问题 [#7980](https://github.com/tikv/pd/issues/7980) @[HuSharp](https://github.com/HuSharp)
    - 修复两中心部署切换时 leader 无法迁移的问题 [#7992](https://github.com/tikv/pd/issues/7992) @[TonsnakeLin](https://github.com/TonsnakeLin)
    - 修复 pd-ctl 标准错误重定向的问题 [#8022](https://github.com/tikv/pd/issues/8022) @[HuSharp](https://github.com/HuSharp)
    - 修复在生成 merge 调度时可能出现的 panic 问题 [#8049](https://github.com/tikv/pd/issues/8049) @[nolouch](https://github.com/nolouch)
    - 修复 `GetAdditionalInfo` 导致的 panic 问题 [#8079](https://github.com/tikv/pd/issues/8079) @[HuSharp](https://github.com/HuSharp)
    - 修复 scatter range 调度器监控显示的问题 [#8125](https://github.com/tikv/pd/issues/8125) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-6.5.9.md > 错误修复> PD - 修复 `SHOW CONFIG` 的查询结果包含已废弃的 `trace-region-flow` 配置项的问题 [#7917](https://github.com/tikv/pd/issues/7917) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.9.md > 错误修复> PD - 修复扩缩容进度显示不准确的问题 [#7726](https://github.com/tikv/pd/issues/7726) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiFlash
  <!--tw@qiancai 2 -->
    - (dup): release-6.5.9.md > 错误修复> TiFlash - 修复在非严格 `sql_mode` 下插入数据到带有异常默认值的列可能导致 TiFlash panic 的问题 [#8803](https://github.com/pingcap/tiflash/issues/8803) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 TiFlash 在高并发读的情况下，可能返回瞬时不正确的结果的问题 [#8845](https://github.com/pingcap/tiflash/issues/8845) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复存算分离架构下，计算节点的本地缓存容量配置项的值修改后，上报 PD 的硬盘使用量不正确的问题 [#8920](https://github.com/pingcap/tiflash/issues/8920) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)
      <!--tw@hfxsd 7 -->
        - (dup): release-6.5.9.md > 错误修复> Tools> Backup & Restore (BR) - 修复在包含 `AUTO_RANDOM` 列的联合聚簇索引中，BR 无法备份 `AUTO_RANDOM` ID 分配进度的问题 [#52255](https://github.com/pingcap/tidb/issues/52255) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.9.md > 错误修复> Tools> Backup & Restore (BR) - 修复在日志备份任务被暂停后，移除任务无法立即恢复 GC safepoint 的问题 [#52082](https://github.com/pingcap/tidb/issues/52082) @[3pointer](https://github.com/3pointer)
        - (dup): release-7.1.5.md > 错误修复> Tools> Backup & Restore (BR) - 修复在小概率情况下，由于特殊的事件时序导致日志备份数据丢失的问题 [#16739](https://github.com/tikv/tikv/issues/16739) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.1.5.md > 错误修复> Tools> Backup & Restore (BR) - 修复因 TiKV 重启，日志备份的 global checkpoint 推进提前于实际备份文件写入点，可能导致少量备份数据丢失的问题 [#16809](https://github.com/tikv/tikv/issues/16809) @[YuJuncen](https://github.com/YuJuncen)
        - 修复全量备份时日志中出现无效的 concurrency 相关信息的问题 [#50837](https://github.com/pingcap/tidb/issues/50837) @[BornChanger](https://github.com/BornChanger)
        - 修复在 BR 恢复数据或 TiDB Lightning 物理导入模式下导入数据时，从 PD 获取到的 Region 没有 Leader 的问题 [#51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth) 
        - 修复日志备份在暂停、停止、再重建任务操作后，虽然任务状态显示正常，但 Checkpoint 不推进的问题 [#53047](https://github.com/pingcap/tidb/issues/53047) @[RidRisR](https://github.com/RidRisR) 
        - 修复不稳定测试用例 `TestClearCache` [#51671](https://github.com/pingcap/tidb/issues/51671) @[zxc111](https://github.com/zxc111)
        - 修复不稳定测试用例 `TestGetMergeRegionSizeAndCount` [#52095](https://github.com/pingcap/tidb/issues/52095) @[3pointer](https://github.com/3pointer)
        - 修复不稳定集成测试 `br_tikv_outage` [#52673](https://github.com/pingcap/tidb/issues/52673) @[Leavrth](https://github.com/Leavrth)
        - 修复测试用例 `TestGetTSWithRetry` 执行时间过长的问题 [#52547](https://github.com/pingcap/tidb/issues/52547) @[Leavrth](https://github.com/Leavrth)

    + TiCDC
      <!--tw@hfxsd 7 -->
        - 修复调用驱逐 TiCDC Owner 节点的 API (/api/v2/owner/resign) 导致 TiCDC 任务意外重启的问题 [#10781](https://github.com/pingcap/tiflow/issues/10781) @[sdojjy](https://github.com/sdojjy)
        - 修复当下游 pulsar 下线后，移除 changefeed 会导致 TiCDC 正常流程卡住，从而引起其他 changefeed 进度卡住的问题 [#10629](https://github.com/pingcap/tiflow/issues/10629) @[asddongmen](https://github.com/asddongmen)
        - 修复 Grafana 监控中的 **Ownership history** 面板显示不稳定的问题 [#10796](https://github.com/pingcap/tiflow/issues/10796) @[hongyunyan](https://github.com/hongyunyan)
        - 修复重启 PD 可能导致 TiCDC 节点报错重启的问题 [#10799](https://github.com/pingcap/tiflow/issues/10799) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 PD 磁盘 IO 延迟较大导致 TiCDC 同步大幅延迟的问题 [#9054](https://github.com/pingcap/tiflow/issues/9054) @[asddongmen](https://github.com/asddongmen)
        - 修复没有按照正确的时区设置默认值的问题 [#10931](https://github.com/pingcap/tiflow/issues/10931) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复没有正确同步 `DROP PRIMARY KEY` 和 `DROP UNIQUE KEY` 的问题 [#10890](https://github.com/pingcap/tiflow/issues/10890) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.1.5.md > 错误修复> Tools> TiCDC - 修复上游写入 `Exchange Partition ... With Validation` DDL 后，TiCDC 向下游执行该 DDL 时失败，导致 changefeed 卡住的问题 [#10859](https://github.com/pingcap/tiflow/issues/10859) @[hongyunyan](https://github.com/hongyunyan)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning
      <!--tw@qiancai 4 -->
        - 修复了 lightning 导入时，因源文件存在不兼容的 SQL 而报 “no database selected” 的问题 [#51800](https://github.com/pingcap/tidb/issues/51800) @[lance6716](https://github.com/lance6716)
        - 修复了 lightning 在 server 模式下可能会打印敏感信息到日志的问题 [#36374](https://github.com/pingcap/tidb/issues/36374) @[kennytm](https://github.com/kennytm)
        - 修复了 lightning 导入期间报 “invalid store ID 0” 错误的问题 [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - 修复了 lighting 使用 replace 作为去重算法时报 “Unknown column in where clause” 错误的问题 [#52886](https://github.com/pingcap/tidb/issues/52886) @[lyzx2001](https://github.com/lyzx2001)
        - (dup): release-7.1.5.md > 错误修复> Tools> TiDB Lightning - 修复导入 Parquet 格式的空表时，TiDB Lightning panic 的问题 [#52518](https://github.com/pingcap/tidb/issues/52518) @[kennytm](https://github.com/kennytm)

    + Dumpling

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Binlog

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 性能测试

如需了解 TiDB v8.1.0 的性能表现，你可以参考 TiDB Dedicated 集群的 [TPC-C 性能测试报告](https://docs.pingcap.com/tidbcloud/v8.1.0-performance-benchmarking-with-tpcc)和 [Sysbench 性能测试报告](https://docs.pingcap.com/tidbcloud/v8.1.0-performance-benchmarking-with-sysbench)（英文版）。

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [arturmelanchyk](https://github.com/arturmelanchyk)（首次贡献者）
- [CabinfeverB](https://github.com/CabinfeverB)
- [danqixu](https://github.com/danqixu)（首次贡献者）
- [imalasong](https://github.com/imalasong)（首次贡献者）
- [jiyfhust](https://github.com/jiyfhust)
- [negachov](https://github.com/negachov)（首次贡献者）
- [testwill](https://github.com/testwill)
- [yzhan1](https://github.com/yzhan1)（首次贡献者）
- [zxc111](https://github.com/zxc111)（首次贡献者）
