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
    <td>TiDB 不断优化数据处理细节，持续提升性能，以更好地满足金融领域对 SQL 处理低延迟的高要求。 关键更新包括：
    <li> <a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_executor_concurrency-从-v50-版本开始引入">并行排序</a> (从 v8.2.0 开始引入) </li>
    <li>  <a href="https://docs.pingcap.com/zh/tidb/v8.5/tidb-configuration-file#batch-policy-从-v830-版本开始引入">优化 KV 请求批处理策略</a> (从 v8.3.0 开始引入) </li>
    <li>  <a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_tso_client_rpc_mode-从-v840-版本开始引入">并行获取 TSO</a> (从 v8.4.0 开始引入) </li>
    <li>降低<a href="https://docs.pingcap.com/tidb/v8.5/sql-statement-delete">DELETE</a> 操作的资源开销 (从 v8.4.0 开始引入) </li>
    <li>  优化<a href="https://docs.pingcap.com/zh/tidb/v8.4/cached-tables#缓存表">缓存表</a>场景性能</a> (v8.4.0 引入) </li>
    <li>  <a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_hash_join_version-从-v840-版本开始引入">Hash Join 算法优化</a> (实验特性，从 v8.4.0 开始引入) </li>
    </td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/tune-region-performance#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力">通过 Active PD Follower 提升 PD Region 信息查询服务的扩展能力</a>（从 v8.5.0 开始成为正式功能）**tw@Oreoxmt 2015**</td>
    <td>TiDB v7.6.0 实验性地引入了 Active PD Follower 特性，允许 PD follower 提供 Region 信息查询服务。在 TiDB 节点数量较多和 Region 数量较多的集群中，该特性可以提升 PD 集群处理 <code>GetRegion</code>、<code>ScanRegions</code> 请求的能力，减轻 PD leader 的 CPU 压力。在 v8.5.0，Active PD Follower 成为正式功能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_instance_plan_cache-从-v840-版本开始引入">实例级执行计划缓存</a>（实验特性，从 v8.4.0 开始引入）</td>
    <td>实例级执行计划缓存允许同一个 TiDB 实例的所有会话共享执行计划缓存。与现有的会话级执行计划缓存相比，实例级执行计划缓存能够在内存中缓存更多执行计划，减少 SQL 编译时间，从而降低 SQL 整体运行时间，提升 OLTP 的性能和吞吐，同时更好地控制内存使用，提升数据库稳定性。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/partitioned-table#全局索引">分区表全局索引</a>（从 v8.4.0 开始成为正式功能）</td>
    <td>全局索引可以有效提高检索非分区列的效率，并且消除了唯一键必须包含分区键的限制。该功能扩展了 TiDB 分区表的使用场景，避免了数据迁移过程中的一些应用修改工作。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_opt_projection_push_down-从-v610-版本开始引入">默认允许将 <code>Projection</code> 算子下推到存储引擎</a>（从 v8.3.0 开始引入）</td>
    <td> <code>Projection</code> 算子下推可以将负载分散到存储节点，同时减少节点间的数据传输。这有助于降低部分 SQL 的执行时间，提升数据库的整体性能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/statistics#收集部分列的统计信息">统计信息收集忽略不必要的列</a>（从 v8.3.0 开始引入）</td>
    <td> 在保证优化器能够获取到必要信息的前提下，加快了统计信息收集的速度，提升统计信息的时效性，进而保证选择最优的执行计划，提升集群性能。同时也降低了系统开销，改善了资源利用率。</td>
  </tr>
  <tr>
    <td rowspan="5">稳定性与高可用</td>
    <td>提升超大规模集群的稳定性 **tw@hfxsd 1976**</td>
    <td>对于使用 TiDB 运行多租户应用或者 SaaS 应用的公司，经常需要存储大量的表，TiDB 在 v8.5.0 着力增强了大规模集群的稳定性。<a href="https://docs.pingcap.com/zh/tidb/v8.5/schema-cache">Schema 缓存控制</a>以及<a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_stats_cache_mem_quota-从-v610-版本开始引入">内部统计信息缓存控制</a>成为正式功能，减少了内存过度消耗带来的稳定性问题。PD 通过 <a href="https://docs.pingcap.com/zh/tidb/v8.5/tune-region-performance#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力">Active Follower</a> 可应对大量 Region 带来的压力，并<a href="https://docs.pingcap.com/zh/tidb/v8.5/pd-microservices">将 PD 所承担的服务逐步解耦</a>，独立部署。通过<a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-从-v840-版本开始引入">增加并发度</a>，以及<a href="https://docs.pingcap.com/zh/tidb/v8.5/statistics#收集部分列的统计信息">减少收集对象的数量</a>，统计信息收集和加载效率得到提升，保证了大集群执行计划的稳定性。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/tidb-resource-control#query_limit-参数说明">Runaway Queries 支持更多触发条件，并能够切换资源组</a>（从 v8.4.0 开始引入）</td>
    <td>Runaway Queries 提供了有效的手段来降低突发的 SQL 性能问题对系统产生的影响。v8.4.0 中新增 Coprocessor 处理的 Key 的数量 (PROCESSED_KEYS) 和 Request Unit (RU) 作为识别条件，并可以将识别到的查询置入指定资源组，对 Runaway Queries 进行更精确的识别与控制。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/tidb-resource-control#background-参数说明">支持为资源管控的后台任务设置资源使用上限</a> (实验特性，从 v8.4.0 开始引入）</td>
    <td>为资源管控的后台任务设置百分比上限，针对不同业务系统的需求，控制后台任务的消耗，从而将后台任务的消耗限制在一个很低的水平，保证在线业务的服务质量。</td>
  </tr>
  <tr>
    <td>增强并扩展 TiProxy 的使用场景 **tw@Oreoxmt**</td>
    <td>作为 TiDB 高可用的重要组成，<a href="https://docs.pingcap.com/zh/tidb/v8.5/tiproxy-overview">TiProxy</a> 除了提供 SQL 流量接入和转发功能外，扩展支持评估集群变更的能力。主要包括：
    <li><a href="https://docs.pingcap.com/zh/tidb/v8.5/tiproxy-traffic-replay">TiProxy 流量捕获和回放</a>（实验特性，从 v8.4.0 开始引入）</li>
    <li><a href="https://docs.pingcap.com/zh/tidb/v8.5/tiproxy-overview">TiProxy 内置虚拟 IP 管理</a>（从 v8.3.0 开始引入）</li>
    <li><a href="https://docs.pingcap.com/zh/tidb/v8.5/tiproxy-load-balance">TiProxy 支持多种负载均衡策略</a>（从 v8.2.0 开始引入）</li>
    </td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入">并行 HashAgg 算法支持数据落盘</a>（从 v8.2.0 开始成为正式功能）</td>
    <td>HashAgg 是 TiDB 中常用的聚合算子，用于快速聚合具有相同字段值的行。TiDB v8.0.0 引入并行 HashAgg 作为实验特性，以进一步提升处理速度。当内存资源不足时，并行 HashAgg 可以将临时排序数据落盘，避免因内存使用过度而导致的 OOM 风险，从而提升查询性能和节点稳定性。该功能在 v8.2.0 成为正式功能，并默认开启，用户可以通过 <code>tidb_executor_concurrency</code> 安全地设置并行 HashAgg 的并发度。</td>
  </tr>
  <tr>
    <td rowspan="2"> SQL </td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/foreign-key">外键约束</a>（从 v8.5.0 开始成为正式功能）**tw@lilin90 1894**</td>
    <td>外键 (Foreign Key) 是数据库中的一种约束，用于建立表与表之间的关联关系，确保数据一致性和完整性。它可以限制子表中引用的数据必须存在于主表中，防止无效数据插入。同时，外键支持级联操作（如删除或更新时自动同步），简化了业务逻辑的实现，减少了手动维护数据关联的复杂性。</td>
  </tr>
  <tr>
    <td>支持<a href="https://docs.pingcap.com/zh/tidb/v8.5/vector-search-overview">向量搜索功能</a>（实验特性，从 v8.4.0 开始引入）</td>
    <td>向量搜索是一种基于数据语义的搜索方法，可以提供更相关的搜索结果。作为 AI 和大语言模型 (LLM) 的核心功能之一，向量搜索可用于检索增强生成 (Retrieval-Augmented Generation, RAG)、语义搜索、推荐系统等多种场景。</td>
  </tr>
  <tr>
    <td rowspan="3">数据库管理与可观测性</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/information-schema-processlist">在内存表中显示 TiKV 和 TiDB 的 CPU 时间</a>（从 v8.4.0 开始引入）</td>
    <td>将 CPU 时间合入系统表中展示，与会话或 SQL 的其他指标并列，方便你从多角度对高 CPU 消耗的操作进行观测，提升诊断效率。尤其适用于诊断实例 CPU 飙升或集群读写热点等场景。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/top-sql#使用-top-sql">按表或数据库维度聚合 TiKV 消耗的 CPU 时间</a>（从 v8.4.0 开始引入）</td>
    <td>当热点问题不是由个别 SQL 语句引起时，利用 Top SQL 中按表或者数据库聚合的 CPU 时间，能够协助用户快速发现造成热点的表或者应用程序，从而大大提升热点问题和 CPU 消耗问题的诊断效率。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/backup-and-restore-storages#鉴权">支持对开启了 IMDSv2 服务的 TiKV 实例做备份</a>（从 v8.4.0 开始引入）</td>
    <td><a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">目前 AWS EC2 的默认元数据服务是 IMDSv2</a>。TiDB 支持从开启了 IMDSv2 的 TiKV 实例中备份数据，协助你更好地在公有云服务中运行 TiDB 集群。</td>
  </tr>
  <tr>
    <td rowspan="1">安全</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/br-snapshot-manual#备份数据加密">快照备份数据</a>和<a href="https://docs.pingcap.com/zh/tidb/v8.5/br-pitr-manual#加密日志备份数据">日志备份数据</a>支持客户端加密（从 v8.5.0 开始成为正式功能）**tw@qiancai 1998**</td>
    <td>在上传快照备份和日志备份到备份存储之前，你可以对备份数据进行加密，确保数据在存储和传输过程中的安全性。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* Schema 缓存可用的内存上限成为正式功能 (GA)，减少了大规模数据场景的内存占用 [#50959](https://github.com/pingcap/tidb/issues/50959) @[tiancaiamao](https://github.com/tiancaiamao) @[wjhuang2016](https://github.com/wjhuang2016) @[gmhdbjd](https://github.com/gmhdbjd) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--1976-->

    在一些 SaaS 场景下，当表的数量达到几十万甚至上百万时，schema meta 会占用较多的内存。开启该功能后，系统将使用 Least Recently Used (LRU) 算法缓存和淘汰相应的 schema meta 信息，有效减少内存占用。
    
    从 v8.4.0 开始，该功能默认开启，默认值为 `536870912`（即 512 MiB），你可以通过系统变量 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800) 按需调整。

    更多信息，请参考[用户文档](/schema-cache.md)。

* 通过 Active PD Follower 提升 PD 上 Region 信息查询服务的扩展能力成为正式功能 (GA) [#7431](https://github.com/tikv/pd/issues/7431) @[okJiang](https://github.com/okJiang) tw@Oreoxmt <!--2015-->

    当集群的 Region 数量较多时，PD leader 处理心跳和调度任务的开销也较大，可能导致 CPU 资源紧张。如果同时集群中的 TiDB 实例数量较多，查询 Region 信息请求并发量较大，PD leader CPU 压力将变得更大，可能会造成 PD 服务不可用。

    为确保服务的高可用性，TiDB v7.6.0 引入 Active PD Follower 作为实验特性，以提升 PD 上 Region 信息查询服务的扩展能力。在 v8.5.0 中，该功能成为正式功能 (GA)。你可以通过设置系统变量 [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-从-v760-版本开始引入) 开启 Active PD Follower 特性。启用该特性后，TiDB 在获取 Region 信息时会将请求均匀地发送到所有 PD 节点上，使 PD follower 也可以处理 Region 请求，从而减轻 PD leader 的 CPU 压力。

    更多信息，请参考[用户文档](/tune-region-performance.md#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiDB 加速建表成为正式功能 (GA)，显著缩短数据迁移和集群初始化时间 [#50052](https://github.com/pingcap/tidb/issues/50052) @[D3Hunter](https://github.com/D3Hunter) @[gmhdbjd](https://github.com/gmhdbjd) tw@Oreoxmt <!--1977-->

    TiDB v7.6.0 引入加速建表功能作为实验特性，并通过系统变量 [`tidb_ddl_version`](https://docs.pingcap.com/zh/tidb/v7.6/system-variables#tidb_ddl_version-从-v760-版本开始引入) 控制。从 v8.0.0 开始，该系统变量更名为 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)。

    在 v8.5.0 中，TiDB 加速建表功能成为正式功能 (GA) 并默认开启。在数据迁移或集群初始化时，该功能支持快速创建百万级规模的表，从而显著减少相关操作的耗时。

    更多信息，请参考[用户文档](/accelerated-table-creation.md)。

* TiKV 支持 MVCC 内存引擎 (In-memory Engine, IME)，可加速需要扫描大量 MVCC 历史版本的查询 [#16141](https://github.com/tikv/tikv/issues/16141) [@SpadeA-Tang](https://github.com/SpadeA-Tang) [@glorv](https://github.com/glorv) [@overvenus](https://github.com/overvenus) tw@hfxsd <!--1706-->

    当频繁更新记录或者需要 TiDB 保留较长时间的历史版本（例如 24 小时）数据时，堆积的 MVCC 版本会导致扫描性能下降。TiKV 的 MVCC 内存引擎可以将最新的 MVCC 版本缓存在内存中，并通过快速的 GC 机制删除内存中的历史版本，从而提升扫描性能。

    从 v8.5.0 开始，TiKV 引入 MVCC 内存引擎。当 TiKV 集群中的 MVCC 版本堆积导致扫描性能下降时，你可以通过设置 TiKV 参数 [`in-memory-engine.enable`](/tikv-in-memory-engine.md#使用方式) 来开启 TiKV MVCC 内存引擎，提升扫描性能。

    更多信息，请参考[用户文档](/tikv-in-memory-engine.md)。

### 稳定性

* 支持限制 PD 处理请求的最大速率和并发度 [#5739](https://github.com/tikv/pd/issues/5739) @[rleungx](https://github.com/rleungx) **tw@qiancai** <!--2018-->

    当突然有大量请求发送到 PD 时，这些请求可能导致 PD 高工作负载，进行影响 PD 性能表现。从 v8.5.0 开始，你可以使用 [`pd-ctl`](/pd-control.md) 来限制 PD 处理请求的最大速率和并发度，提升 PD 的稳定性。

    更多信息，请参考[用户文档](/pd-control.md)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 外键成为正式功能 (GA) [#36982](https://github.com/pingcap/tidb/issues/36982) @[YangKeao](https://github.com/YangKeao) @[crazycs520](https://github.com/crazycs520) tw@lilin90 <!--1894-->

    在 v8.5.0 中，TiDB 的外键功能成为正式功能 (GA)，支持使用外键约束提升数据一致性和保障完整性。你可以轻松创建表间的外键关联，实现级联更新和删除操作，使得数据管理更加便捷。这一功能为复杂数据关联的应用场景提供了更好的支持。

    更多信息，请参考[用户文档](/foreign-key.md)。

* 引入 `ADMIN ALTER DDL JOBS` 语法，支持在线修改 DDL 任务参数 [#57229](hhttps://github.com/pingcap/tidb/issues/57229) @[fzzf678](https://github.com/fzzf678) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--2016-->

    从 v8.3.0 开始，TiDB 支持在会话级别设置变量 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) 和  [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)，因此通过 Global 设置这两个变量已不再影响所有运行中的 DDL 任务。如需更改这些变量的值，需要先取消 DDL 任务，调整变量取值后再重新提交。

    从 v8.5.0 开始，引入了 `ADMIN ALTER DDL JOBS` 语句。你可以在线调整指定的 DDL 任务的变量值，以便灵活平衡资源消耗与性能，并将变更限定于单个任务，使影响范围更加可控。例如：

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

* BR 支持在客户端进行快照备份数据和日志备份数据加密 (GA) [#28640](https://github.com/pingcap/tidb/issues/28640) [#56433](https://github.com/pingcap/tidb/issues/56433) @[joccau](https://github.com/joccau) @[Tristan1900](https://github.com/Tristan1900) **tw@qiancai** <!--1998-->

    * 通过快照备份数据的客户端加密功能（在 TiDB v5.3.0 中以实验特性引入），你可以使用自定义的固定密钥在客户端加密备份数据。

    * 通过日志备份数据的客户端加密功能（在 TiDB v8.4.0 中以实验特性引入），你使用以下方式之一在客户端加密日志备份数据：

        * 使用自定义的固定密钥加密
        * 使用本地磁盘的主密钥加密
        * 使用 KMS（密钥管理服务）的主密钥加密

  从 v8.5.0 开始，这两个加密功能都成为了正式功能 (GA)，进一步增强了客户端数据的安全性。

  更多信息，请参考[加密备份数据](/br/br-snapshot-manual.md#encrypt-the-backup-data)和[加密日志备份数据](/br/br-pitr-manual.md#encrypt-the-log-backup-data)。

* TiKV 静态加密支持 Google [Key Management Service (Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive?hl=zh-cn) (GA) [#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv) tw@qiancai <!--1876-->

      TiKV 通过静态加密功能对存储的数据进行加密，以确保数据的安全性。静态加密的安全核心点在于密钥管理。在 v8.0.0 中，TiKV 静态加密以实验特性的形式支持了基于 Google Cloud KMS 的主密钥管理。
      
    从 v8.5.0 起，基于 Google Cloud KMS 的静态加密成为正式功能 (GA）。要使用该功能，你需要在 Google Cloud 上创建一个密钥，然后在 TiKV 配置文件中添加 `[security.encryption.master-key]` 部分的配置。

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
    - 提升关闭分布式框架的 fast reorg 加索引任务对任务取消的响应速度 [#56017](https://github.com/pingcap/tidb/issues/56017) @[lance6716](https://github.com/lance6716)
    - 提升小表加索引的速度 [#54230](https://github.com/pingcap/tidb/issues/54230) @[tangenta](https://github.com/tangenta)
    - 增加系统变量 tidb_ddl_reorg_max_write_speed 来限制加索引时 ingest 阶段速度上限 [#57156](https://github.com/pingcap/tidb/issues/57156) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 提升某些情况下查询 information_schema.tables 的性能 [#57295](https://github.com/pingcap/tidb/issues/57295) @[tangenta](https://github.com/tangenta)
    - 支持动态调整更多 DDL 任务参数 [#57526](https://github.com/pingcap/tidb/issues/57526) @[fzzf678](https://github.com/fzzf678)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - (dup): release-7.1.6.md > 改进提升> TiFlash - 提升聚簇索引表在后台回收过期数据的速度 [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 提升带有更新数据场景下 Vector Search 的查询性能 [#9599](https://github.com/pingcap/tiflash/issues/9599) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 添加关于构建 Vector Index CPU 使用率的监控指标 [#9032](https://github.com/pingcap/tiflash/issues/9032) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 优化逻辑运算符的执行速度 [#9146](https://github.com/pingcap/tiflash/issues/9146) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - (dup): release-7.1.6.md > 改进提升> Tools> Backup & Restore (BR) - 减少备份过程中无效日志的打印 [#55902](https://github.com/pingcap/tidb/issues/55902) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - 在 DM 集群启动时，增加 dm-worker 连接到 dm-master 的重试 [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)
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
    - (dup): release-7.1.6.md > 错误修复> TiDB - 修复写冲突时 TTL 任务可能无法取消的问题 [#56422](https://github.com/pingcap/tidb/issues/56422) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.1.6.md > 错误修复> TiDB - 修复取消 TTL 任务时，没有强制 Kill 对应 SQL 的问题 [#56511](https://github.com/pingcap/tidb/issues/56511) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.1.6.md > 错误修复> TiDB - 修复集群从 v6.5 升级到 v7.5 或更高版本后，已有 TTL 任务执行意外频繁的问题 [#56539](https://github.com/pingcap/tidb/issues/56539) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.1.6.md > 错误修复> TiDB - 修复 `INSERT ... ON DUPLICATE KEY` 语句不兼容 `mysql_insert_id` 的问题 [#55965](https://github.com/pingcap/tidb/issues/55965) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.1.6.md > 错误修复> TiDB - 修复 TTL 在未选用 TiKV 作为存储引擎时可能失败的问题 [#56402](https://github.com/pingcap/tidb/issues/56402) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.1.6.md > 错误修复> TiDB - 修复通过 `IMPORT INTO` 导入数据后，`AUTO_INCREMENT` 字段没有正确设置的问题 [#56476](https://github.com/pingcap/tidb/issues/56476) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-7.1.6.md > 错误修复> TiDB - 修复执行 `ADD INDEX` 时，未检查索引长度限制的问题 [#56930](https://github.com/pingcap/tidb/issues/56930) @[fzzf678](https://github.com/fzzf678)
    - (dup): release-7.1.6.md > 错误修复> TiDB - 修复执行 `RECOVER TABLE BY JOB JOB_ID;` 可能导致 panic 的问题 [#55113](https://github.com/pingcap/tidb/issues/55113) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-7.1.6.md > 错误修复> TiDB - 修复由于 stale read 未对读操作的时间戳进行严格校验，导致 TSO 和真实物理时间存在偏移，有小概率影响事务一致性的问题 [#56809](https://github.com/pingcap/tidb/issues/56809) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复 DDL owner 节点切换时，reorg 类型的 DDL 任务无法从切换前的进度继续的问题 [#56506](https://github.com/pingcap/tidb/issues/56506) @[tangenta](https://github.com/tangenta)
    - 修复分布式执行框架监控面板不准确的问题 [#57172](https://github.com/pingcap/tidb/issues/57172) @[fzzf678](https://github.com/fzzf678) [#56942](https://github.com/pingcap/tidb/issues/56942) @[fzzf678](https://github.com/fzzf678)
    - 修复某些情况下 REORGANIZE PARTITION 无法展示报错原因的问题 [#56634](https://github.com/pingcap/tidb/issues/56634) @[mjonss](https://github.com/mjonss)
    - 修复查询 information_schema.tables 大小写敏感的问题 [#56987](https://github.com/pingcap/tidb/issues/56987) @[joechenrh](https://github.com/joechenrh)
    - 修复 `CTE` 有多个数据消费者，且某个消费者在没有读取任何数据情况下退出可能导致的非法内存访问问题 [#57294](https://github.com/pingcap/tidb/issues/57294) @[windtalker](https://github.com/windtalker)
    - 修复 `IndexHashJoin` 在非正常退出情况下可能卡住问题 [#54055](https://github.com/pingcap/tidb/issues/54055) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `TRUNCATE` 处理 `NULL` 值不正确的问题 [#53546](https://github.com/pingcap/tidb/issues/53546) @[tuziemon](https://github.com/tuziemon)    
    - 修复类型推导错误导致的 `CAST AS CHAR` 函数结果问题 [#56640](https://github.com/pingcap/tidb/issues/56640) @[zimulala](https://github.com/zimulala)
    -  修复类型推导错误导致的字符串被截断问题 [#56587](https://github.com/pingcap/tidb/issues/56587) @[joechenrh](https://github.com/joechenrh)  
    -  修复 `ADDTIME` 和 `SUBTIME` 函数第一个参数是日期类型时结果错误问题 [#57569](https://github.com/pingcap/tidb/issues/57569) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -  修复在非严格模式下 (sql_mode = '')，非法空值被插入的问题 [#56381](https://github.com/pingcap/tidb/issues/56381) @[joechenrh](https://github.com/joechenrh)         

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - (dup): release-7.1.6.md > 错误修复> TiKV - 修复读线程在从 Raft Engine 中的 MemTable 读取过时索引时出现的 panic 问题 [#17383](https://github.com/tikv/tikv/issues/17383) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.4.md > 错误修复> TiKV - 修复当大量事务在排队等待同一个 key 上的锁被释放且该 key 被频繁更新时，TiKV 可能因死锁检测压力过大而出现 OOM 的问题 [#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - (dup): release-7.1.6.md > 错误修复> PD - 修复热点缓存中可能存在的内存泄露问题 [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - (dup): release-7.1.6.md > 错误修复> TiFlash - 修复 `SUBSTRING()` 函数不支持部分整数类型的 `pos` 和 `len` 参数导致查询报错的问题 [#9473](https://github.com/pingcap/tiflash/issues/9473) @[gengliqi](https://github.com/gengliqi)
    - 修复在存算分离架构下，Vector Search 查询性能在 TiFlash write node 扩容之后，可能出现性能下降的问题 [#9637](https://github.com/pingcap/tiflash/issues/9637) @[kolafish](https://github.com/kolafish)
    - 修复当 `SUBSTRING` 函数的第二个参数为负数时，可能产生错误结果的问题 [#9604](https://github.com/pingcap/tiflash/issues/9604) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当 `REPLACE` 函数的第一个参数为常数时，可能报错的问题 [#9522](https://github.com/pingcap/tiflash/issues/9522) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当 `LPAD` 和 `RPAD` 函数在某些情况下返回错误结果的问题 [#9465](https://github.com/pingcap/tiflash/issues/9465) @[guo-shaoge](https://github.com/guo-shaoge)    

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - (dup): release-7.5.4.md > 错误修复> Tools> Backup & Restore (BR) - 修复 BR 集成测试用例不稳定的问题，并新增用于模拟快照或者日志备份文件损坏的测试用例 [#53835](https://github.com/pingcap/tidb/issues/53835) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - (dup): release-7.1.6.md > 错误修复> Tools> TiDB Lightning - 修复 TiDB Lightning 因 TiKV 发送的消息过大而接收失败的问题 [#56114](https://github.com/pingcap/tidb/issues/56114) @[fishiu](https://github.com/fishiu)
        - 修复物理导入后 AUTO INCREMENT 值设置过大的问题 [#56814](https://github.com/pingcap/tidb/issues/56814) @[D3Hunter](https://github.com/D3Hunter)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [Contributor-GitHub-ID](id-link)
