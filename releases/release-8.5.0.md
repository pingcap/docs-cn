---
title: TiDB 8.5.0 Release Notes
summary: 了解 TiDB 8.5.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.0 Release Notes

<EmailSubscriptionWrapper />

发版日期：2024 年 x 月 x 日

TiDB 版本：8.5.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.5.0#version-list)

TiDB 8.5.0 为长期支持版本 (Long-Term Support Release, LTS)。

相比于前一个 LTS（即 8.1.0 版本），8.5.0 版本包含 [8.2.0-DMR](/releases/release-8.2.0.md)、[8.3.0-DMR](/releases/release-8.3.0.md), 和 [8.4.0-DMR](/releases/release-8.4.0.md) 中已发布的新功能、提升改进和错误修复。当你从 8.1.x 升级到 8.5.0 时，可以下载 [TiDB Release Notes PDF](https://download.pingcap.org/tidb-v8.1-to-v8.5-zh-release-notes.pdf) 查看两个 LTS 版本之间的所有 Release Notes。下表列出了从 8.1.0 到 8.5.0 的一些关键特性：

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
    <td>多维度降低数据处理延迟</td>
    <td>TiDB 不断优化数据处理细节，持续提升性能，以更好地满足金融领域对 SQL 处理低延迟的高要求。关键更新包括：
    <li><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_executor_concurrency-从-v50-版本开始引入">并行排序</a>（从 v8.2.0 开始引入）</li>
    <li><a href="https://docs.pingcap.com/zh/tidb/v8.5/tidb-configuration-file#batch-policy-从-v830-版本开始引入">优化 KV 请求批处理策略</a>（从 v8.3.0 开始引入）</li>
    <li><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_tso_client_rpc_mode-从-v840-版本开始引入">并行获取 TSO</a>（从 v8.4.0 开始引入）</li>
    <li>降低 <a href="https://docs.pingcap.com/tidb/v8.5/sql-statement-delete">DELETE</a> 操作的资源开销（从 v8.4.0 开始引入）</li>
    <li>优化<a href="https://docs.pingcap.com/zh/tidb/v8.5/cached-tables#缓存表">缓存表</a>场景性能（从 v8.4.0 开始引入）</li>
    <li><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_hash_join_version-从-v840-版本开始引入">Hash Join 算法优化</a>（实验特性，从 v8.4.0 开始引入）</li>
    </td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/tune-region-performance#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力">通过 Active PD Follower 提升 PD Region 信息查询服务的扩展能力</a>（从 v8.5.0 开始成为正式功能）</td>
    <td>TiDB v7.6.0 实验性地引入了 Active PD Follower 特性，允许 PD follower 提供 Region 信息查询服务。在 TiDB 节点数较多和 Region 数较多的集群中，该特性可以提升 PD 集群处理 <code>GetRegion</code> 和 <code>ScanRegions</code> 请求的能力，减轻 PD leader 的 CPU 压力。在 v8.5.0，Active PD Follower 成为正式功能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_instance_plan_cache-从-v840-版本开始引入">实例级执行计划缓存</a>（实验特性，从 v8.4.0 开始引入）</td>
    <td>实例级执行计划缓存允许同一个 TiDB 实例的所有会话共享执行计划缓存。与现有的会话级执行计划缓存相比，实例级执行计划缓存能够在内存中缓存更多执行计划，减少 SQL 编译时间，从而降低 SQL 整体运行时间，提升 OLTP 的性能和吞吐，同时更好地控制内存使用，提升数据库稳定性。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/partitioned-table#全局索引">分区表全局索引</a>（从 v8.4.0 开始成为正式功能）</td>
    <td>全局索引可以有效提高检索非分区列的效率，并且消除了唯一键必须包含分区键的限制。该功能扩展了 TiDB 分区表的使用场景，提升了分区表的性能，降低了分区表在一些查询场景的资源消耗。</td>
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
    <td>提升超大规模集群的稳定性</td>
    <td>对于使用 TiDB 运行多租户应用或者 SaaS 应用的公司，经常需要存储大量的表，TiDB 在 v8.5.0 着力增强了大规模集群的稳定性。
   <li><a href="https://docs.pingcap.com/zh/tidb/v8.5/schema-cache">Schema 缓存控制</a>以及<a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_stats_cache_mem_quota-从-v610-版本开始引入">设置统计信息缓存使用内存的上限</a>成为正式功能，减少了内存过度消耗带来的稳定性问题。</li>
    <li>PD 通过 <a href="https://docs.pingcap.com/zh/tidb/v8.5/tune-region-performance#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力">Active Follower</a> 可应对大量 Region 带来的压力，并<a href="https://docs.pingcap.com/zh/tidb/v8.5/pd-microservices">将 PD 所承担的服务逐步解耦</a>，独立部署。</li>
    <li>PD 优化提升 Region 心跳处理的性能，并支持集群中千万级 Regions 的规模。</li>
    <li>通过<a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-从-v840-版本开始引入">增加并发度</a>，以及<a href="https://docs.pingcap.com/zh/tidb/v8.5/statistics#收集部分列的统计信息">减少收集对象的数量</a>，统计信息收集和加载效率得到提升，保证了大集群执行计划的稳定性。</li>
    </td>
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
    <td>增强并扩展 TiProxy 的使用场景</td>
    <td>作为 TiDB 高可用的重要组件，<a href="https://docs.pingcap.com/zh/tidb/v8.5/tiproxy-overview">TiProxy</a> 除了提供 SQL 流量接入和转发功能外，新增了对集群变更的评估能力。主要包括：
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
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/foreign-key">外键约束</a>（从 v8.5.0 开始成为正式功能）</td>
    <td>外键 (Foreign Key) 是数据库中的一种约束，用于建立表与表之间的关联关系，确保数据一致性和完整性。它可以确保子表中引用的数据必须存在于主表中，防止无效数据插入。同时，外键支持级联操作（如删除或更新时自动同步），简化了业务逻辑的实现，减少了手动维护数据关联的复杂性。</td>
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
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/backup-and-restore-overview">Backup & Restore (BR)</a> 启用 <a href="https://aws.amazon.com/sdk-for-rust/">AWS SDK for Rust</a> 访问外部存储（从 v8.5.0 开始引入）</td>
    <td>BR 使用 <a href="https://aws.amazon.com/cn/sdk-for-rust/">AWS Rust SDK</a> 替换掉原有的 Rusoto 库，从 TiKV 访问 Amazon S3 等外部存储，以更好地兼容 AWS 的 <a href="https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html">IMDSv2</a> 以及 <a href="https://docs.aws.amazon.com/zh_cn/eks/latest/userguide/pod-identities.html">EKS Pod Identity</a> 等新特性。</td>
  </tr>
  <tr>
    <td rowspan="1">安全</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/br-snapshot-manual#备份数据加密">快照备份数据</a>和<a href="https://docs.pingcap.com/zh/tidb/v8.5/br-pitr-manual#加密日志备份数据">日志备份数据</a>支持客户端加密（从 v8.5.0 开始成为正式功能）</td>
    <td>在上传快照备份和日志备份到备份存储之前，你可以对备份数据进行加密，确保数据在存储和传输过程中的安全性。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* Schema 缓存可用的内存上限成为正式功能 (GA)，当表的数量达到几十万甚至上百万时，可以显示减少 Schema 元数据的内存占用 [#50959](https://github.com/pingcap/tidb/issues/50959) @[tiancaiamao](https://github.com/tiancaiamao) @[wjhuang2016](https://github.com/wjhuang2016) @[gmhdbjd](https://github.com/gmhdbjd) @[tangenta](https://github.com/tangenta)

    在一些 SaaS 场景下，当表的数量达到几十万甚至上百万时，Schema 元数据会占用较多的内存。开启该功能后，系统将使用 Least Recently Used (LRU) 算法缓存和淘汰相应的 Schema 元数据信息，有效减少内存占用。

    从 v8.4.0 开始，该功能默认开启，默认值为 `536870912`（即 512 MiB），你可以通过系统变量 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入) 按需调整。

    更多信息，请参考[用户文档](/schema-cache.md)。

* 通过 Active PD Follower 提升 PD 上 Region 信息查询服务的扩展能力 (GA) [#7431](https://github.com/tikv/pd/issues/7431) @[okJiang](https://github.com/okJiang)

    当集群的 Region 数量较多时，PD leader 处理心跳和调度任务的开销也较大，可能导致 CPU 资源紧张。如果同时集群中的 TiDB 实例数量较多，查询 Region 信息请求并发量较大，PD leader CPU 压力将变得更大，可能会造成 PD 服务不可用。

    为确保服务的高可用性，TiDB v7.6.0 引入 Active PD Follower 作为实验特性，以提升 PD 上 Region 信息查询服务的扩展能力。在 v8.5.0 中，该功能成为正式功能 (GA)。你可以通过设置系统变量 [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-从-v760-版本开始引入) 开启 Active PD Follower 特性。启用该特性后，TiDB 在获取 Region 信息时会将请求均匀地发送到所有 PD 节点上，使 PD follower 也可以处理 Region 请求，从而减轻 PD leader 的 CPU 压力。

    更多信息，请参考[用户文档](/tune-region-performance.md#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力)。

### 性能

* TiDB 加速建表成为正式功能 (GA)，显著缩短数据迁移和集群初始化时间 [#50052](https://github.com/pingcap/tidb/issues/50052) @[D3Hunter](https://github.com/D3Hunter) @[gmhdbjd](https://github.com/gmhdbjd)

    TiDB v7.6.0 引入加速建表功能作为实验特性，并通过系统变量 [`tidb_ddl_version`](https://docs.pingcap.com/zh/tidb/v7.6/system-variables#tidb_ddl_version-从-v760-版本开始引入) 控制。从 v8.0.0 开始，该系统变量更名为 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)。

    在 v8.5.0 中，TiDB 加速建表功能成为正式功能 (GA) 并默认开启。在数据迁移或集群初始化时，该功能支持快速创建百万级规模的表，从而显著缩短相关操作的耗时。

    更多信息，请参考[用户文档](/accelerated-table-creation.md)。

* TiKV 支持 MVCC 内存引擎 (In-memory Engine, IME)，可加速需要扫描大量 MVCC 历史版本的查询 [#16141](https://github.com/tikv/tikv/issues/16141) [@SpadeA-Tang](https://github.com/SpadeA-Tang) [@glorv](https://github.com/glorv) [@overvenus](https://github.com/overvenus)

    当频繁更新记录或者需要 TiDB 保留较长时间的历史版本（例如 24 小时）数据时，堆积的 MVCC 版本会导致扫描性能下降。TiKV 的 MVCC 内存引擎可以将最新的 MVCC 版本缓存在内存中，并通过快速的 GC 机制删除内存中的历史版本，从而提升扫描性能。

    从 v8.5.0 开始，TiKV 引入 MVCC 内存引擎。当 TiKV 集群中的 MVCC 版本堆积导致扫描性能下降时，你可以通过设置 TiKV 参数 [`in-memory-engine.enable`](/tikv-in-memory-engine.md#使用方式) 来开启 TiKV MVCC 内存引擎，提升扫描性能。

    更多信息，请参考[用户文档](/tikv-in-memory-engine.md)。

### 稳定性

* 支持限制 PD 处理请求的最大速率和并发度 [#5739](https://github.com/tikv/pd/issues/5739) @[rleungx](https://github.com/rleungx)

    当突然有大量请求发送到 PD 时，这些请求可能导致 PD 工作负载过高，进行影响 PD 性能表现。从 v8.5.0 开始，你可以使用 [`pd-ctl`](/pd-control.md) 来限制 PD 处理请求的最大速率和并发度，提升 PD 的稳定性。

    更多信息，请参考[用户文档](/pd-control.md)。

### SQL 功能

* 外键成为正式功能 (GA) [#36982](https://github.com/pingcap/tidb/issues/36982) @[YangKeao](https://github.com/YangKeao) @[crazycs520](https://github.com/crazycs520)

    在 v8.5.0 中，TiDB 的外键功能成为正式功能 (GA)，支持使用外键约束提升数据一致性和保障完整性。你可以轻松创建表间的外键关联，实现级联更新和删除操作，使得数据管理更加便捷。这一功能为复杂数据关联的应用场景提供了更好的支持。

    更多信息，请参考[用户文档](/foreign-key.md)。

* 引入 `ADMIN ALTER DDL JOBS` 语法，支持在线修改 DDL 任务参数 [#57229](https://github.com/pingcap/tidb/issues/57229) @[fzzf678](https://github.com/fzzf678) @[tangenta](https://github.com/tangenta)

    从 v8.3.0 开始，TiDB 支持在会话级别设置变量 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) 和 [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)，因此通过 Global 设置这两个变量已不再影响所有运行中的 DDL 任务。如需更改这些变量的值，需要先取消 DDL 任务，调整变量取值后再重新提交。

    从 v8.5.0 开始，引入了 `ADMIN ALTER DDL JOBS` 语句。你可以在线调整指定的 DDL 任务的变量值，以便灵活平衡资源消耗与性能，并将变更限定于单个任务，使影响范围更加可控。例如：

    - `ADMIN ALTER DDL JOBS job_id THREAD = 8;`：在线调整该 DDL 任务的 `tidb_ddl_reorg_worker_cnt`
    - `ADMIN ALTER DDL JOBS job_id BATCH_SIZE = 256;`：在线调整该 DDL 任务的 `tidb_ddl_reorg_batch_size`
    - `ADMIN ALTER DDL JOBS job_id MAX_WRITE_SPEED = '200MiB';`：在线调整写入每个 TiKV 节点的索引数据流量大小

  更多信息，请参考[用户文档](/sql-statements/sql-statement-admin-alter-ddl.md)。

### 安全

* BR 支持在客户端进行快照备份数据和日志备份数据加密 (GA) [#28640](https://github.com/pingcap/tidb/issues/28640) [#56433](https://github.com/pingcap/tidb/issues/56433) @[joccau](https://github.com/joccau) @[Tristan1900](https://github.com/Tristan1900)

    * 通过快照备份数据的客户端加密功能（在 TiDB v5.3.0 中以实验特性引入），你可以使用自定义的固定密钥在客户端加密备份数据。

    * 通过日志备份数据的客户端加密功能（在 TiDB v8.4.0 中以实验特性引入），你使用以下方式之一在客户端加密日志备份数据：

        * 使用自定义的固定密钥加密
        * 使用本地磁盘的主密钥加密
        * 使用 KMS（密钥管理服务）的主密钥加密

  从 v8.5.0 开始，这两个加密功能都成为了正式功能 (GA)，进一步增强了客户端数据的安全性。

  更多信息，请参考[加密备份数据](/br/br-snapshot-manual.md#备份数据加密)和[加密日志备份数据](/br/br-pitr-manual.md#加密日志备份数据)。

* TiKV 静态加密支持 [Google Cloud Key Management Service (Google Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive?hl=zh-cn) (GA) [#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv)

    TiKV 通过静态加密功能对存储的数据进行加密，以确保数据的安全性。静态加密的安全核心点在于密钥管理。在 v8.0.0 中，TiKV 静态加密以实验特性的形式支持了基于 Google Cloud KMS 的主密钥管理。

    从 v8.5.0 起，基于 Google Cloud KMS 的静态加密成为正式功能 (GA)。要使用该功能，你需要在 Google Cloud 上创建一个密钥，然后在 TiKV 配置文件中添加 `[security.encryption.master-key]` 部分的配置。

    更多信息，请参考[用户文档](/encryption-at-rest.md#tikv-静态加密)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.4.0 升级至当前版本 (v8.5.0) 所需兼容性变更信息。如果从 v8.3.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

- 为了与 MySQL 兼容，在非严格模式下 (`sql_mode = ''`) 向非 `NULL` 列插入 `NULL` 值会报错。 [#55457](https://github.com/pingcap/tidb/issues/55457) @[joechenrh](https://github.com/joechenrh)
- 不再支持 `ALTER TABLE ... DROP FOREIGN KEY IF EXISTS ...` 语句。 [#56703](https://github.com/pingcap/tidb/pull/56703) @[YangKeao](https://github.com/YangKeao)

### 系统变量

| 变量名  | 修改类型    | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入) | 修改 | 经进一步的测试后，默认值从 `OFF` 修改为 `ON`，即默认开启 [TiDB 加速建表](/accelerated-table-creation.md)。|
| [`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-从-v850-版本开始引入) | 新增 | 限制每个 TiKV 节点写入的带宽，仅在开启添加索引加速功能时生效（由变量 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 控制）。例如，当该值设置为 `200MiB` 时，最大写入速度限制为 200 MiB/s。 |

### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`deprecate-integer-display-length`](/tidb-configuration-file.md#deprecate-integer-display-length) | 修改 | 从 v8.5.0 开始，整数显示宽度功能已废弃，该配置项的默认值从 `false` 修改为 `true`。 |
| TiKV | [`raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size) | 修改 | 默认值从 `8192` 修改为 `16384`。|
| PD | [`patrol-region-worker-count`](/pd-configuration-file.md#patrol-region-worker-count-从-v850-版本开始引入) | 新增 | 控制 checker 检查 Region 健康状态时，创建 [operator](/glossary.md#operator) 的并发数。|
| BR | [`--checksum`](/br/br-snapshot-manual.md) | 修改 | 默认值从 `true` 修改为 `false`，即 BR 进行全量备份时，默认不计算表级别的校验和，以提升备份性能。 |

## 废弃功能

以下为计划将在未来版本中废弃的功能：

* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，该系统变量将被废弃。
* TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，该系统变量将被废弃。
* 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)，用于控制 TiDB 是否支持并行 HashAgg 进行落盘。在未来版本中，该系统变量将被废弃。
* TiDB 在 v5.1 引入了系统变量 [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-从-v51-版本开始引入)，用于设置是否开启分区表动态裁剪模式。从 v8.5.0 开始，将该变量设置为 `static` 或 `static-only` 时会产生警告。在未来版本中，该系统变量将被废弃。
* TiDB Lightning 参数 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 计划在未来版本中废弃，并在后续版本中删除。该参数将由 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。
* 从 v6.3.0 开始，分区表默认使用[动态裁剪模式](/partitioned-table.md#动态裁剪模式)，相比静态裁剪模式，动态裁剪模式支持 IndexJoin、Plan Cache 等特性，性能表现更好。在未来版本中，静态裁剪模式将被废弃。

## 改进提升

+ TiDB

    - 提升关闭分布式执行框架时，`ADD INDEX` 加速功能对任务取消的响应速度 [#56017](https://github.com/pingcap/tidb/issues/56017) @[lance6716](https://github.com/lance6716)
    - 提升小表加索引的速度 [#54230](https://github.com/pingcap/tidb/issues/54230) @[tangenta](https://github.com/tangenta)
    - 新增系统变量 `tidb_ddl_reorg_max_write_speed`，用于限制加索引时 ingest 阶段速度的上限 [#57156](https://github.com/pingcap/tidb/issues/57156) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 提升某些情况下查询 `information_schema.tables` 的性能 [#57295](https://github.com/pingcap/tidb/issues/57295) @[tangenta](https://github.com/tangenta)
    - 支持动态调整更多 DDL 任务参数 [#57526](https://github.com/pingcap/tidb/issues/57526) @[fzzf678](https://github.com/fzzf678)
    - 支持全局索引包含分区表达式中的所有列 [#56230](https://github.com/pingcap/tidb/issues/56230) @[Defined2014](https://github.com/Defined2014)
    - 支持 List 分区表在 Range 查询的场景中进行分区裁剪 [#56673](https://github.com/pingcap/tidb/issues/56673) @[Defined2014](https://github.com/Defined2014)
    - 默认开启 FixControl#46177，修复在某些情况下错误地选择了全表扫描，而没有选择索引范围扫描的问题 [#46177](https://github.com/pingcap/tidb/issues/46177) @[terry1purcell](https://github.com/terry1purcell)
    - 改进内部估算逻辑，使其能够更充分地利用多列多值索引的统计信息，提升某些涉及多值索引的查询的估算精度 [#56915](https://github.com/pingcap/tidb/issues/56915) @[time-and-fate](https://github.com/time-and-fate)
    - 提高特定情况下全表扫描的代价估算，减少错误地选择全表扫描的概率 [#57085](https://github.com/pingcap/tidb/issues/57085) @[terry1purcell](https://github.com/terry1purcell)
    - 优化统计信息同步加载所需的数据量，提升加载性能 [#56812](https://github.com/pingcap/tidb/issues/56812) @[winoros](https://github.com/winoros)
    - 优化特定情况下，`OUTER JOIN` 含有唯一索引且有 `ORDER BY ... LIMIT` 子句时的执行计划，提高执行效率 [#56321](https://github.com/pingcap/tidb/issues/56321) @[winoros](https://github.com/winoros)

+ TiKV

    - 利用单独的线程清理副本，保证 Raft 读写关键路径的延迟稳定 [#16001](https://github.com/tikv/tikv/issues/16001) @[hbisheng](https://github.com/hbisheng)
    - 向量距离函数支持 SIMD 以提升性能 [#17290](https://github.com/tikv/tikv/issues/17290) @[EricZequan](https://github.com/EricZequan)

+ PD

    - 支持 `tso` 服务在微服务模式和非微服务模式之间动态切换 [#8477](https://github.com/tikv/pd/issues/8477) @[rleungx](https://github.com/rleungx)
    - 优化 `pd-ctl config` 输出中部分字段的大小写 [#8694](https://github.com/tikv/pd/issues/8694) @[lhy1024](https://github.com/lhy1024)
    - [Store limit v2](/configure-store-limit.md#store-limit-v2-原理) 成为正式功能 (GA) [#8865](https://github.com/tikv/pd/issues/8865) @[lhy1024](https://github.com/lhy1024)
    - 支持配置 Region 巡检的并行度（实验特性）[#8866](https://github.com/tikv/pd/issues/8866) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - 提升聚簇索引表在后台回收过期数据的速度 [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 提升数据更新场景下向量搜索的查询性能 [#9599](https://github.com/pingcap/tiflash/issues/9599) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 新增关于构建向量索引 CPU 使用率的监控指标 [#9032](https://github.com/pingcap/tiflash/issues/9032) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 提升逻辑运算符的执行效率 [#9146](https://github.com/pingcap/tiflash/issues/9146) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - 减少备份过程中无效日志的打印 [#55902](https://github.com/pingcap/tidb/issues/55902) @[Leavrth](https://github.com/Leavrth)
        - 优化加密密钥 `--crypter.key` 的错误提示信息 [#56388](https://github.com/pingcap/tidb/issues/56388) @[Tristan1900](https://github.com/Tristan1900)
        - 增加 BR 创建数据库时的并发度，以提升数据恢复性能 [#56866](https://github.com/pingcap/tidb/issues/56866) @[Leavrth](https://github.com/Leavrth)
        - 在进行全量备份时，默认不计算表级别的 checksum (`--checksum=false`) 以提升备份性能 [#56373](https://github.com/pingcap/tidb/issues/56373) @[Tristan1900](https://github.com/Tristan1900)
        - 新增对每个存储节点的连接超时进行独立追踪和重置的机制，增强了对慢节点的处理能力，从而避免备份卡住的问题 [#57666](https://github.com/pingcap/tidb/issues/57666) @[3pointer](https://github.com/3pointer)

    + TiDB Data Migration (DM)

        - 在 DM 集群启动时，增加 DM-worker 连接到 DM-master 的重试 [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)

## 错误修复

+ TiDB

    - 修复当从 PD 返回的 Region 元数据中未包含 Leader 信息时，TiDB 未自动重试请求可能导致执行报错的问题 [#56757](https://github.com/pingcap/tidb/issues/56757) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复写冲突时 TTL 任务可能无法取消的问题 [#56422](https://github.com/pingcap/tidb/issues/56422) @[YangKeao](https://github.com/YangKeao)
    - 修复取消 TTL 任务时，没有强制 Kill 对应 SQL 的问题 [#56511](https://github.com/pingcap/tidb/issues/56511) @[lcwangchao](https://github.com/lcwangchao)
    - 修复集群从 v6.5 升级到 v7.5 或更高版本后，已有 TTL 任务执行意外频繁的问题 [#56539](https://github.com/pingcap/tidb/issues/56539) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 `INSERT ... ON DUPLICATE KEY` 语句不兼容 `mysql_insert_id` 的问题 [#55965](https://github.com/pingcap/tidb/issues/55965) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 TTL 在未选用 TiKV 作为存储引擎时可能失败的问题 [#56402](https://github.com/pingcap/tidb/issues/56402) @[YangKeao](https://github.com/YangKeao)
    - 修复通过 `IMPORT INTO` 导入数据后，`AUTO_INCREMENT` 字段没有正确设置的问题 [#56476](https://github.com/pingcap/tidb/issues/56476) @[D3Hunter](https://github.com/D3Hunter)
    - 修复执行 `ADD INDEX` 时，未检查索引长度限制的问题 [#56930](https://github.com/pingcap/tidb/issues/56930) @[fzzf678](https://github.com/fzzf678)
    - 修复执行 `RECOVER TABLE BY JOB JOB_ID;` 可能导致 panic 的问题 [#55113](https://github.com/pingcap/tidb/issues/55113) @[crazycs520](https://github.com/crazycs520)
    - 修复由于 stale read 未对读操作的时间戳进行严格校验，导致 TSO 和真实物理时间存在偏移，有小概率影响事务一致性的问题 [#56809](https://github.com/pingcap/tidb/issues/56809) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复 DDL owner 节点切换后，无法按照切换前的进度继续执行 Reorg DDL 任务的问题 [#56506](https://github.com/pingcap/tidb/issues/56506) @[tangenta](https://github.com/tangenta)
    - 修复分布式执行框架的监控面板上部分指标不准确的问题 [#57172](https://github.com/pingcap/tidb/issues/57172) @[fzzf678](https://github.com/fzzf678) [#56942](https://github.com/pingcap/tidb/issues/56942) @[fzzf678](https://github.com/fzzf678)
    - 修复某些情况下 `REORGANIZE PARTITION` 无法显示报错原因的问题 [#56634](https://github.com/pingcap/tidb/issues/56634) @[mjonss](https://github.com/mjonss)
    - 修复查询 `INFORMATION_SCHEMA.TABLES` 时由于大小写敏感导致返回结果错误的问题 [#56987](https://github.com/pingcap/tidb/issues/56987) @[joechenrh](https://github.com/joechenrh)
    - 修复当公共表表达式 (CTE) 有多个数据消费者时，如果某个消费者在未读取数据时就退出，可能导致非法内存访问的问题 [#55881](https://github.com/pingcap/tidb/issues/55881) @[windtalker](https://github.com/windtalker)
    - 修复 `INDEX_HASH_JOIN` 在异常退出时可能卡住的问题 [#54055](https://github.com/pingcap/tidb/issues/54055) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `TRUNCATE` 语句在处理 `NULL` 值时返回结果错误的问题 [#53546](https://github.com/pingcap/tidb/issues/53546) @[tuziemon](https://github.com/tuziemon)
    - 修复由于类型推导错误导致 `CAST AS CHAR` 函数结果不正确的问题 [#56640](https://github.com/pingcap/tidb/issues/56640) @[zimulala](https://github.com/zimulala)
    - 修复由于类型推导错误导致部分函数的输出结果中字符串被截断的问题 [#56587](https://github.com/pingcap/tidb/issues/56587) @[joechenrh](https://github.com/joechenrh)
    - 修复 `ADDTIME()` 和 `SUBTIME()` 函数的第一个参数为日期类型时返回错误结果的问题 [#57569](https://github.com/pingcap/tidb/issues/57569) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复在非严格模式下 (`sql_mode = ''`) ，非法空值能被插入的问题 [#56381](https://github.com/pingcap/tidb/issues/56381) @[joechenrh](https://github.com/joechenrh)
    - 修复 `UPDATE` 语句更新 `ENUM` 类型的值时更新错误的问题 [#56832](https://github.com/pingcap/tidb/issues/56832) @[xhebox](https://github.com/xhebox)
    - 修复开启 `tidb_low_resolution_tso` 变量后，执行 `SELECT FOR UPDATE` 语句出现资源泄漏的问题 [#55468](https://github.com/pingcap/tidb/issues/55468) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `JSON_TYPE()` 函数未检查其参数类型导致传入非 JSON 数据类型时未报错的问题 [#54029](https://github.com/pingcap/tidb/issues/54029) @[YangKeao](https://github.com/YangKeao)
    - 修复在 `PREPARE` 语句中使用 JSON 函数可能导致执行失败的问题 [#54044](https://github.com/pingcap/tidb/issues/54044) @[YangKeao](https://github.com/YangKeao)
    - 修复将数据从 `BIT` 类型换为 `CHAR` 类型时可能导致 TiKV 崩溃的问题 [#56494](https://github.com/pingcap/tidb/issues/56494) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在 `CREATE VIEW` 语句中使用变量或参数时未报错的问题 [#53176](https://github.com/pingcap/tidb/issues/53176) @[mjonss](https://github.com/mjonss)
    - 修复 `JSON_VALID()` 函数返回结果错误的问题 [#56293](https://github.com/pingcap/tidb/issues/56293) @[YangKeao](https://github.com/YangKeao)
    - 修复关闭 `tidb_ttl_job_enable` 变量后 TTL 任务未被取消的问题 [#57404](https://github.com/pingcap/tidb/issues/57404) @[YangKeao](https://github.com/YangKeao)
    - 修复同时使用 `RANGE COLUMNS` 分区函数和 `utf8mb4_0900_ai_ci` 排序规则时，查询结果错误的问题 [#57261](https://github.com/pingcap/tidb/issues/57261) @[Defined2014](https://github.com/Defined2014)
    - 修复执行以换行符开头的 Prepared 语句会导致数组越界的运行错误 [#54283](https://github.com/pingcap/tidb/issues/54283) @[Defined2014](https://github.com/Defined2014)
    - 修复 `UTC_TIMESTAMP()` 函数中的精度相关问题，比如精度设置得太大 [#56451](https://github.com/pingcap/tidb/issues/56451) @[chagelo](https://github.com/chagelo)
    - 修复 `UPDATE`、`INSERT`、`DELETE IGNORE` 语句中没有忽略外键错误的问题 [#56678](https://github.com/pingcap/tidb/issues/56678) @[YangKeao](https://github.com/YangKeao)
    - 修复查询 `information_schema.cluster_slow_query` 表时，如果不加时间过滤条件，则只会查询最新的慢日志文件的问题 [#56100](https://github.com/pingcap/tidb/issues/56100) @[crazycs520](https://github.com/crazycs520)
    - 修复 TTL 表的内存泄漏问题 [#56934](https://github.com/pingcap/tidb/issues/56934) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 `write_only` 状态的表外键约束未生效的问题，以避免使用 `non-public` 状态的表 [#55813](https://github.com/pingcap/tidb/issues/55813) @[YangKeao](https://github.com/YangKeao)
    - 修复使用 `NATURAL JOIN` 或者 `USING` 子句之后，再使用子查询可能会报错的问题 [#53766](https://github.com/pingcap/tidb/issues/53766) @[dash12653](https://github.com/dash12653)
    - 修复如果 CTE 包含 `ORDER BY`、`LIMIT`、`SELECT DISTINCT` 子句，并且被另外一个 CTE 的递归部分所引用时，可能被错误地 inline 导致执行报错的问题 [#56603](https://github.com/pingcap/tidb/issues/56603) @[elsa0520](https://github.com/elsa0520)
    - 修复 `VIEW` 中定义的 CTE 被错误 inline 的问题 [#56582](https://github.com/pingcap/tidb/issues/56582) @[elsa0520](https://github.com/elsa0520)
    - 修复使用 `PLAN REPLAYER` 导入含有外键的表结构时可能报错的问题 [#56456](https://github.com/pingcap/tidb/issues/56456) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用 `PLAN REPLAYER` 导入含有 Placement Rule 的表结构时可能报错的问题 [#54961](https://github.com/pingcap/tidb/issues/54961) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用 `ANALYZE` 收集表的统计信息时，如果该表包含虚拟生成列的表达式索引，执行会报错的问题 [#57079](https://github.com/pingcap/tidb/issues/57079) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `DROP DATABASE` 语句没有正确触发统计信息对应变更的问题 [#57227](https://github.com/pingcap/tidb/issues/57227) @[Rustin170506](https://github.com/Rustin170506)
    - 修复在 CTE 中解析数据库名时，返回错误的数据库名的问题 [#54582](https://github.com/pingcap/tidb/issues/54582) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在使用 `DUMP STATS` 将统计信息转为 JSON 的过程中，直方图上下界数据受损的问题 [#56083](https://github.com/pingcap/tidb/issues/56083) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `EXISTS` 子查询的结果继续参与代数运算时，结果和 MySQL 不一致的问题 [#56641](https://github.com/pingcap/tidb/issues/56641) @[windtalker](https://github.com/windtalker)
    - 修复无法为带别名的多表删除语句 `DELETE` 创建执行计划绑定的问题 [#56726](https://github.com/pingcap/tidb/issues/56726) @[hawkingrei](https://github.com/hawkingrei)
    - 修复优化器在简化复杂谓词时，由于没有考虑字符集及排序规则，可能导致执行报错的问题 [#56479](https://github.com/pingcap/tidb/issues/56479) @[dash12653](https://github.com/dash12653)
    - 修复 Grafana 中 **Stats Healthy Distribution** 面板的数据可能错误的问题 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在包含聚簇索引的表上执行向量搜索查询时，结果可能错误的问题 [#57627](https://github.com/pingcap/tidb/issues/57627) @[winoros](https://github.com/winoros)

+ TiKV

    - 修复读线程在从 Raft Engine 中的 MemTable 读取过时索引时出现的 panic 问题 [#17383](https://github.com/tikv/tikv/issues/17383) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复当大量事务在排队等待同一个 key 上的锁被释放且该 key 被频繁更新时，TiKV 可能因死锁检测压力过大而出现 OOM 的问题 [#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复资源管控后台任务 CPU 使用率可能被重复统计的问题 [#17603](https://github.com/tikv/tikv/issues/17603) @[glorv](https://github.com/glorv)
    - 修复由于 CDC 内部任务堆积过多导致 TiKV OOM 的问题 [#17696](https://github.com/tikv/tikv/issues/17696) @[3AceShowHand](https://github.com/3AceShowHand)
    - 修复 `raft-entry-max-size` 设置过高时，写入 batch 可能过大引起性能抖动的问题 [#17701](https://github.com/tikv/tikv/issues/17701) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复 Region Split 后可能无法快速选出 Leader 的问题 [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复使用 `RADIANS()` 或 `DEGREES()` 函数时可能导致 TiKV panic 的问题 [#17852](https://github.com/tikv/tikv/issues/17852) @[gengliqi](https://github.com/gengliqi)
    - 修复所有休眠的 Region 被集中唤醒时，可能导致写入抖动的问题 [#17101](https://github.com/tikv/tikv/issues/17101) @[hhwyt](https://github.com/hhwyt)

+ PD

    - 修复热点缓存中可能存在的内存泄露问题 [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)
    - 修复资源组 (Resource Group) 选择器对所有面板都未生效的问题 [#56572](https://github.com/pingcap/tidb/issues/56572) @[glorv](https://github.com/glorv)
    - 修复已删除的资源组仍然出现在监控面板中的问题 [#8716](https://github.com/tikv/pd/issues/8716) @[AndreMouche](https://github.com/AndreMouche)
    - 修复 Region syncer 加载过程中日志描述不清晰的问题 [#8717](https://github.com/tikv/pd/issues/8717) @[lhy1024](https://github.com/lhy1024)
    - 修复 label 统计中的内存泄露问题 [#8700](https://github.com/tikv/pd/issues/8700) @[lhy1024](https://github.com/lhy1024)
    - 修复配置 `tidb_enable_tso_follower_proxy` 为 `0` 或 `OFF` 时无法关闭 TSO Follower Proxy 特性的问题 [#8709](https://github.com/tikv/pd/issues/8709) @[JmPotato](https://github.com/JmPotato)

+ TiFlash

    - 修复 `SUBSTRING()` 函数不支持部分整数类型的 `pos` 和 `len` 参数导致查询报错的问题 [#9473](https://github.com/pingcap/tiflash/issues/9473) @[gengliqi](https://github.com/gengliqi)
    - 修复在存算分离架构下，扩容 TiFlash 写节点后向量搜索性能可能下降的问题 [#9637](https://github.com/pingcap/tiflash/issues/9637) @[kolafish](https://github.com/kolafish)
    - 修复当 `SUBSTRING()` 函数的第二个参数为负数时，可能返回错误结果的问题 [#9604](https://github.com/pingcap/tiflash/issues/9604) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当 `REPLACE()` 函数的第一个参数为常数时，可能报错的问题 [#9522](https://github.com/pingcap/tiflash/issues/9522) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当 `LPAD()` 和 `RPAD()` 函数在某些情况下返回错误结果的问题 [#9465](https://github.com/pingcap/tiflash/issues/9465) @[guo-shaoge](https://github.com/guo-shaoge)

+ Tools

    + Backup & Restore (BR)

        - 修复备份过程中还未备份完成的 range 空洞过多时出现 OOM 的问题，减少了预先分配的内存 [#53529](https://github.com/pingcap/tidb/issues/53529) @[Leavrth](https://github.com/Leavrth)
        - 修复备份时无法备份全局索引的问题 [#57469](https://github.com/pingcap/tidb/issues/57469) @[Defined2014](https://github.com/Defined2014)
        - 修复日志可能打印加密信息的问题 [#57585](https://github.com/pingcap/tidb/issues/57585) @[kennytm](https://github.com/kennytm)
        - 修复 advancer 无法处理锁冲突的问题 [#57134](https://github.com/pingcap/tidb/issues/57134) @[3pointer](https://github.com/3pointer)
        - 升级 `k8s.io/api` 库的版本以修复潜在的安全漏洞 [#57790](https://github.com/pingcap/tidb/issues/57790) @[BornChanger](https://github.com/BornChanger)
        - 修复当集群存在大量表但实际数据量较小时，PITR 数据恢复任务可能出现 `Information schema is out of date` 报错的问题 [#57743](https://github.com/pingcap/tidb/issues/57743) @[Tristan1900](https://github.com/Tristan1900)

    + TiCDC

        - 修复使用 Debezium 协议时 Kafka 消息中缺少 Key 的问题 [#1799](https://github.com/pingcap/tiflow/issues/1799) @[wk989898](https://github.com/wk989898)
        - 修复 redo 模块无法正确上报错误的问题 [#11744](https://github.com/pingcap/tiflow/issues/11744) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 TiDB DDL owner 变更导致 DDL 任务的 schema 版本出现非递增时，TiCDC 错误丢弃 DDL 任务的问题 [#11714](https://github.com/pingcap/tiflow/issues/11714) @[wlwilliamx](https://github.com/wlwilliamx)

    + TiDB Lightning

        - 修复 TiDB Lightning 因 TiKV 发送的消息过大而接收失败的问题 [#56114](https://github.com/pingcap/tidb/issues/56114) @[fishiu](https://github.com/fishiu)
        - 修复使用物理导入模式导入数据后，`AUTO_INCREMENT` 值设置过大的问题 [#56814](https://github.com/pingcap/tidb/issues/56814) @[D3Hunter](https://github.com/D3Hunter)

## 性能测试

如需了解 TiDB v8.5.0 的性能表现，你可以参考 TiDB Cloud Dedicated 集群的 [TPC-C 性能测试报告](https://docs.pingcap.com/tidbcloud/v8.5-performance-benchmarking-with-tpcc)和 [Sysbench 性能测试报告](https://docs.pingcap.com/tidbcloud/v8.5-performance-benchmarking-with-sysbench)（英文版）。

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [dash12653](https://github.com/dash12653)（首次贡献者）
- [chagelo](https://github.com/chagelo)（首次贡献者）
- [LindaSummer](https://github.com/LindaSummer)
- [songzhibin97](https://github.com/songzhibin97)
- [Hexilee](https://github.com/Hexilee)
