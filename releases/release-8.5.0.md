---
title: TiDB 8.5.0 Release Notes
summary: 了解 TiDB 8.5.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.0 Release Notes

<EmailSubscriptionWrapper />

发版日期：2024 年 5 月 24 日

TiDB 版本：8.5.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.5.0#version-list)

TiDB 8.5.0 为长期支持版本 (Long-Term Support Release, LTS)。

相比于前一个 LTS（即 8.1.0 版本），8.5.0 版本包含 [8.2.0-DMR](/releases/release-8.2.0.md)、[8.3.0-DMR](/releases/release-8.3.0.md), 和 [8.4.0-DMR] 中已发布的新功能、提升改进和错误修复。当你从 8.1.x 升级到 8.5.0 时，可以下载 [TiDB Release Notes PDF](https://download.pingcap.org/tidb-v8.1-to-v8.5-zh-release-notes.pdf) 查看两个 LTS 版本之间的所有 Release Notes。下表列出了从 8.1.0 到 8.5.0 的一些关键特性：

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
    <td rowspan="6">可扩展性与性能</td>
    <td> 多维度降低数据处理延迟 **tw@qiancai**</td>
    <td>通过不断挖掘数据处理的细节，TiDB 持续提升自身性能，力求满足金融场景对 SQL 处理时延的要求。 包括以下关键更新：
    <li> 并行排序 (v8.2.0 引入) </li>
    <li> 优化 KV 请求批处理策略 (v8.3.0 引入) </li>
    <li> 并行获取 TSO (v8.4.0 引入) </li>
    <li> 删除语句只获取必要的列 (v8.4.0 引入) </li>
    <li> 优化缓存表场景性能 (v8.4.0 引入) </li>
    <li> Hash Join 算法演进 (v8.4.0 引入) </li>
    </td>
  </tr>
  <tr>
    <td>Active PD Follower 成为正式功能  **tw@Oreoxmt 2015**</td>
    <td>TiDB v7.6.0 引入了 Active PD Follower 特性，允许 PD follower 提供 Region 信息查询服务。在 TiDB 节点数量较多和 Region 数量较多的集群中，该特性可以提升 PD 集群处理 <code>GetRegion</code>、<code>ScanRegions</code> 请求的能力，减轻 PD leader 的 CPU 压力。在 v8.5.0，Active PD Follower 成为正式功能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_instance_plan_cache-从-v840-版本开始引入">实例级执行计划缓存</a>（实验特性）（v8.4.0 引入）</td>
    <td>实例级执行计划缓存允许同一个 TiDB 实例的所有会话共享执行计划缓存。与现有的会话级执行计划缓存相比，实例级执行计划缓存能够在内存中缓存更多执行计划，减少 SQL 编译时间，从而降低 SQL 整体运行时间，提升 OLTP 的性能和吞吐，同时更好地控制内存使用，提升数据库稳定性。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/partitioned-table#全局索引">分区表全局索引</a>（v8.4.0  起成为正式功能）</td>
    <td>全局索引可以有效提高检索非分区列的效率，并且消除了唯一键必须包含分区键的限制。该功能扩展了 TiDB 分区表的使用场景，避免了数据迁移过程中的一些应用修改工作。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_opt_projection_push_down-从-v610-版本开始引入">默认允许将 <code>Projection</code> 算子下推到存储引擎</a>（v8.3.0 引入）</td>
    <td> <code>Projection</code> 算子下推可以将负载分散到存储节点，同时减少节点间的数据传输。这有助于降低部分 SQL 的执行时间，提升数据库的整体性能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/statistics#收集部分列的统计信息">统计信息收集忽略不必要的列</a>（v8.3.0 引入）</td>
    <td> 在保证优化器能够获取到必要信息的前提下，加快了统计信息收集的速度，提升统计信息的时效性，进而保证选择最优的执行计划，提升集群性能。同时也降低了系统开销，改善了资源利用率。</td>
  </tr>
  <tr>
    <td rowspan="5">稳定性与高可用</td>
    <td>提升超大规模集群的稳定性 **tw@hfxsd 1976**</td>
    <td>对于使用 TiDB 运行多租户应用或者 SaaS 应用的公司，经常需要存储大量的表，TiDB 在 v8.5.0 着力增强了大规模集群的稳定性。 <a href="https://docs.pingcap.com/zh/tidb/v8.5/schema-cache">Schema 缓存控制</a>以及<a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_stats_cache_mem_quota-从-v610-版本开始引入">Stats 缓存控制</a>已经成为正式功能，减少了内存过度消耗带来的稳定性问题。 PD 通过 <a href="https://docs.pingcap.com/zh/tidb/v8.5/tune-region-performance#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力">Active Follower</a> 应对大量 Region 带来的压力，并<a href="https://docs.pingcap.com/zh/tidb/v8.5/pd-microservices">将 PD 所承担的服务逐步解耦</a>，独立部署。通过<a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-从-v840-版本开始引入">增加并发度</a>，以及<a href="https://docs.pingcap.com/zh/tidb/v8.5/statistics#收集部分列的统计信息">减少收集对象的数量</a>，统计信息收集和加载效率得到提升，保证了大集群执行计划的稳定性。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/tidb-resource-control#query_limit-参数说明">Runaway Queries 支持更多触发条件，并能够切换资源组</a> （v8.4.0 引入）</td>
    <td>Runaway Queries 提供了有效的手段来降低突发的 SQL 性能问题对系统产生的影响。v8.4.0 中新增 Coprocessor 处理的 Key 的数量 (PROCESSED_KEYS) 和 Request Unit (RU) 作为识别条件，并可以将识别到的查询置入指定资源组，对 Runaway Queries 进行更精确的识别与控制。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/tidb-resource-control#background-参数说明">支持为资源管控的后台任务设置资源使用上限</a> (实验特性)（v8.4.0 引入）</td>
    <td>为资源管控的后台任务设置百分比上限，针对不同业务系统的需求，控制后台任务的消耗，从而将后台任务的消耗限制在一个很低的水平，保证在线业务的服务质量。</td>
  </tr>
  <tr>
    <td>增强并扩展 TiProxy 的使用场景 **tw@Oreoxmt**</td>
    <td>作为 TiDB 高可用的重要组成，TiProxy 在做好 SQL 流量接入和转发的同时，开始尝试对集群变更进行评估。主要包括：
    <li> TiProxy 流量捕获和回放（实验特性）（v8.4.0 引入）</li>
    <li> TiProxy 内置虚拟 IP 管理（v8.3.0 引入）</li>
    <li> TiProxy 支持多种负载均衡策略 （v8.2.0 引入）</li>
    </td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入">并行 HashAgg 算法支持数据落盘</a> （v8.2.0 起成为正式功能）</td>
    <td>HashAgg 是 TiDB 中常用的聚合算子，用于快速聚合具有相同字段值的行。TiDB v8.0.0 引入并行 HashAgg 作为实验特性，以进一步提升处理速度。当内存资源不足时，并行 HashAgg 可以将临时排序数据落盘，避免因内存使用过度而导致的 OOM 风险，从而提升查询性能和节点稳定性。该功能在 v8.2.0 成为正式功能，并默认开启，用户可以通过 <code>tidb_executor_concurrency</code> 安全地设置并行 HashAgg 的并发度。</td>
  </tr>
  <tr>
    <td rowspan="2"> SQL </td>
    <td>外键约束成为正式功能 **tw@lilin90 1894**</td>
    <td>外键（Foreign Key）是数据库中的一种约束，用于建立表与表之间的关联关系，确保数据一致性和完整性。它可以限制子表中引用的数据必须存在于主表中，防止无效数据插入。同时，外键支持级联操作（如删除或更新时自动同步），简化了业务逻辑的实现，减少了手动维护数据关联的复杂性。</td>
  </tr>
  <tr>
    <td>支持<a href="https://docs.pingcap.com/zh/tidb/v8.5/vector-search-overview">向量搜索功能</a>（实验特性）(v8.4.0 引入）</td>
    <td>向量搜索是一种基于数据语义的搜索方法，可以提供更相关的搜索结果。作为 AI 和大语言模型 (LLM) 的核心功能之一，向量搜索可用于检索增强生成 (Retrieval-Augmented Generation, RAG)、语义搜索、推荐系统等多种场景。</td>
  </tr>
  <tr>
    <td rowspan="3">数据库管理与可观测性</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/information-schema-processlist">在内存表中显示 TiKV 和 TiDB 的 CPU 时间</a> （v8.4.0 引入）</td>
    <td>将 CPU 时间合入系统表中展示，与会话或 SQL 的其他指标并列，方便你从多角度对高 CPU 消耗的操作进行观测，提升诊断效率。尤其适用于诊断实例 CPU 飙升或集群读写热点等场景。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/top-sql#使用-top-sql">按表或数据库维度聚合 TiKV 消耗的 CPU 时间</a>（v8.4.0 引入）</td>
    <td>当热点问题不是由个别 SQL 语句引起时，利用 Top SQL 中按表或者数据库聚合的 CPU 时间，能够协助用户快速发现造成热点的表或者应用程序，从而大大提升热点问题和 CPU 消耗问题的诊断效率。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/backup-and-restore-storages#鉴权">支持对开启了 IMDSv2 服务的 TiKV 实例做备份</a> （v8.4.0 引入）</td>
    <td><a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">目前 AWS EC2 的默认元数据服务是 IMDSv2</a>。TiDB 支持从开启了 IMDSv2 的 TiKV 实例中备份数据，协助你更好地在公有云服务中运行 TiDB 集群。</td>
  </tr>
  <tr>
    <td rowspan="1">安全</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/br-pitr-manual#加密日志备份数据">日志备份数据支持客户端加密</a></td>
    <td>在上传日志备份到备份存储之前，你可以对日志备份数据进行加密，确保数据在存储和传输过程中的安全性。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* Schema 缓存内存上限功能成为正式功能 (GA)，减少了大规模数据场景的内存占用 [#50959](https://github.com/pingcap/tidb/issues/50959) @[tiancaiamao](https://github.com/tiancaiamao) @[wjhuang2016](https://github.com/wjhuang2016) @[gmhdbjd](https://github.com/gmhdbjd) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--1976-->

    在一些 SaaS 场景下，当表的数据量达到几十万甚至上百万时，Schema meta 会占用较多的内存。开启该功能后，系统将使用 LRU 算法缓存和淘汰相应 schema meta 信息，有效减少内存占用。
    
    从 v8.4.0 开始，该功能默认开启，默认值为 `536870912`（即 512 MiB），你可通过配置系统变量 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)，按需调整。

    更多信息，请参考[用户文档](/schema-cache.md)。

* Use the Active PD Follower feature to enhance the scalability of PD's Region information query service (General Availability) [#7431](https://github.com/tikv/pd/issues/7431) @[okJiang](https://github.com/okJiang) tw@Oreoxmt <!--2015-->

    In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances, and there is a high concurrency of requests for Region information, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.

    To ensure high availability and also enhance the scalability of PD's Region information query service. You can enable the Active PD Follower feature by setting the system variable [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) to `ON`. After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader.

    For more information, see [documentation](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiDB 加速建表成为正式功能 (GA)，显著缩短数据迁移和集群初始化时间 [#50052](https://github.com/pingcap/tidb/issues/50052) @[D3Hunter](https://github.com/D3Hunter) @[gmhdbjd](https://github.com/gmhdbjd) tw@Oreoxmt <!--1977-->

    TiDB v7.6.0 引入加速建表功能作为实验特性，并通过系统变量 [`tidb_ddl_version`](https://docs.pingcap.com/zh/tidb/v7.6/system-variables#tidb_ddl_version-从-v760-版本开始引入) 控制。从 v8.0.0 开始，该系统变量更名为 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)。

    在 v8.5.0 中，TiDB 加速建表功能成为正式功能 (GA) 并默认开启。在数据迁移或集群初始化时，该功能支持快速创建百万级规模的表，从而显著减少相关操作的耗时。

    更多信息，请参考[用户文档](/accelerated-table-creation.md)。

### 稳定性

* Enabling rate limiter can protect PD from being crash under a large number of sudden requests and improve the stability of PD [#5739](https://github.com/tikv/pd/issues/5739) @[rleungx](https://github.com/rleungx)

    You can adjust the rate limiter configuration through pd-ctl.

    For more information, see [Documentation](/stable/pd-control.md).

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 外键的功能成为正式功能（GA） [#36982](https://github.com/pingcap/tidb/issues/36982) @[YangKeao](https://github.com/YangKeao) @[crazycs520](https://github.com/crazycs520) tw@lilin90 <!--1894-->

    TiDB 的外键功能现已 GA，支持通过使用外键约束提升数据一致性和完整性保障。用户可以轻松创建表间的外键关联，实现级联更新和删除操作，使得数据管理更加便捷。这一功能为复杂数据关联的应用场景提供了更好的支持。

    更多信息，请参考[用户文档](链接)。

* 引入 `ADMIN ALTER DDL JOBS` 的语法，支持在线修改 DDL 任务参数 [#57229](hhttps://github.com/pingcap/tidb/issues/57229) @[fzzf678](https://github.com/fzzf678) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--2016-->

    从 v8.3.0 版本开始，支持在会话级别设置变量 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) 和  [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)，因此通过 Global 设置这两个变量已不再影响所有运行中的 DDL 任务。如需更改这些变量的值，需要先取消 DDL 任务，调整变量取值后再重新提交。

    从 8.5.0 版本开始，引入了 `ADMIN ALTER DDL JOBS` 语句，你可以在线调整指定的 DDL 任务的变量值，以便灵活平衡资源消耗与性能，并将变更限定于单个任务，使影响范围更加可控。例如：

    - `ADMIN ALTER DDL JOBS job_id THREAD = 8;`：在线调整该 DDL 任务的 `tidb_ddl_reorg_worker_cnt`
    - `ADMIN ALTER DDL JOBS job_id BATCH_SIZE = 256;`：在线调整该 DDL 任务的 `tidb_ddl_reorg_batch_size`
    - `ADMIN ALTER DDL JOBS job_id MAX_WRITE_SPEED = '200MiB';`：在线调整写入每个 TiKV 节点的索引数据流量大小

  更多信息，请参考[用户文档](/sql-statements/sql-statement-admin-alter-ddl.md)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 安全

* BR supports client-side encryption of log backup data (GA) [#56433](https://github.com/pingcap/tidb/issues/56433) @[Tristan1900](https://github.com/Tristan1900) tw@qiancai <!--1998-->

    TiDB v8.4.0 introduced an experimental feature to encrypt, on the client side, log backup data. Starting from v8.5.0, this feature is now Generally Avaialble. Before uploading log backup data to your backup storage, you can encrypt the backup data to ensure its security via one of the following methods:

    - Encrypt using a custom fixed key
    - Encrypt using a master key stored on a local disk
    - Encrypt using a master key managed by a Key Management Service (KMS)

  For more information, see [documentation](/br/br-pitr-manual.md#encrypt-the-log-backup-data).

* TiKV 静态加密支持 Google [Key Management Service (Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive?hl=zh-cn)（GA）[#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv)

  在 v8.0.0 中，TiKV以实验特性的形式支持静态加密配置基于 Google Cloud KMS 的主密钥。从 v8.5.0起，这个功能已经GA。要启用基于 Google Cloud KMS 的静态加密，你需要在 Google Cloud 上创建一个密钥，然后在 TiKV 配置文件中添加 `[security.encryption.master-key]` 部分的配置。

  更多信息，请参考[用户文档](/encryption-at-rest.md#tikv-静态加密)。

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.4.0 升级至当前版本 (v8.5.0) 所需兼容性变更信息。如果从 v8.3.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

### MySQL 兼容性

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
|tidb_ddl_reorg_max_write_speed | Newly added |Used to control the speed at which TiDB writes index data to a single TiKV node. For example, setting the value to 200 MiB limits the maximum write speed to 200 MiB/s. |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入) | 修改 | 经进一步的测试后，默认值从 `OFF` 修改为 `ON`，即默认开启 [TiDB 加速建表](/accelerated-table-creation.md)。|
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

## 离线包变更

## 移除功能

## 废弃功能

以下为计划将在未来版本中废弃的功能：

* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将被废弃。
* TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 将被废弃。
* 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)，用于控制 TiDB 是否支持并行 HashAgg 进行落盘。在未来版本中，系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) 将被废弃。
* TiDB Lightning 参数 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 计划在未来版本中废弃，并在后续版本中删除。该参数将由 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。
* 从 v6.3.0 开始，分区表默认使用[动态裁剪模式](/partitioned-table.md#动态裁剪模式)，相比静态裁剪模式，动态裁剪模式支持 IndexJoin、Plan Cache 等特性，性能表现更好。在未来版本中，静态裁剪模式将被废弃。

## 改进提升

+ TiDB

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## 错误修复

+ TiDB

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [Contributor-GitHub-ID](id-link)
