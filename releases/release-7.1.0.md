---
title: TiDB 7.1.0 Release Notes
summary: 了解 TiDB 7.1.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.0 Release Notes

发版日期：xxxx 年 xx 月 xx 日

TiDB 版本：7.1.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.1.0#version-list)

TiDB 7.1.0 为长期支持版本 (Long-Term Support Release, LTS)。

相比于前一个 LTS（即 6.5.0 版本），7.1.0 版本包含 [6.6.0-DMR](/releases/release-6.6.0.md) 和 [7.0.0-DMR](/releases/release-7.0.0.md) 中已发布的新功能、提升改进和错误修复，并引入了以下关键特性：

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
    <td rowspan="4">可扩展性与性能</td>
    <td>TiFlash 支持<a href="https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3" target="_blank">存储计算分离和 S3 共享存储</a>（实验特性，从 v7.0.0 开始引入）</td>
    <td>TiFlash 增加云原生架构的支持作为可选项：
      <ul>
        <li>支持存算分离架构，提升 HTAP 资源的弹性能力。</li>
        <li>支持基于 S3 的存储引擎，以更低的成本提供共享存储。</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>TiKV 支持<a href="https://docs.pingcap.com/zh/tidb/dev/system-variables#tidb_store_batch_size" target="_blank">批量聚合数据请求</a>（从 v6.6.0 开始引入）</td>
    <td>TiDB 支持将发送到相同 TiKV 实例的数据请求部分合并，减少子任务的数量和 RPC 请求的开销。在数据离散分布且 gRPC 线程池资源紧张的情况下，批量化请求能够提升性能超 50%。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/troubleshoot-hot-spot-issues#打散读热点" target="_blank">基于负载的副本读取</a></td>
    <td>在读热点场景中，TiDB 可以将热点 TiKV 节点的读请求转发到副本。该功能有效地打散了读热点并优化了集群资源的利用。你可以通过调整系统变量 <a href="https://docs.pingcap.com/zh/tidb/dev/system-variables#tidb_load_based_replica_read_threshold-从-v700-版本开始引入" target="_blank"><code>tidb_load_based_replica_read_threshold</code></a> 控制基于负载的副本读取的触发阈值。</td>
  </tr>
  <tr>
      <td>TiKV 支持<a href="https://docs.pingcap.com/tidb/dev/partitioned-raft-kv" target="_blank"> 分区 Raft KV 存储引擎 </a>（实验特性）</td>
    <td>TiKV 引入下一代存储引擎分区 Raft KV，通过每个数据 Region 独享 RocksDB 实例，可将集群的存储能力从 TB 级扩展到 PB 级，并提供更稳定的写入延迟和更强大的扩容能力。</td>
  </tr>
  <tr>
    <td rowspan="2">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/tidb-resource-control" target="_blank">资源管控</a> (GA)</td>
   <td>支持基于资源组的资源管控，为同一集群中的不同工作负载分配并隔离资源。该功能显著提升了多应用集群的稳定性，并为多租户奠定了基础。在 v7.1.0 中，资源管控引入了根据实际负载或硬件部署估算集群容量的能力。</td>
  </tr>
  <tr>
    <td>TiFlash 支持<a href="https://docs.pingcap.com/zh/tidb/dev/tiflash-spill-disk" target="_blank">数据落盘</a>（从 v7.0.0 开始引入）</td>
    <td>TiFlash 支持将中间结果落盘，以缓解数据密集型操作（如聚合、排序和 Hash Join）中的 OOM 问题。</td>
  </tr>
  <tr>
    <td rowspan="3">SQL</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/sql-statement-create-index#多值索引" target="_blank">多值索引</a> (GA)</td>
    <td>引入 MySQL 兼容的多值索引，增强 JSON 类型，提升 TiDB 对 MySQL 8.0 的兼容性。该功能提升了对多值列进行成员检查的效率。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/time-to-live" target="_blank">行级 TTL</a>（从 v7.0.0 开始 GA）</td>
    <td>支持通过后台任务自动删除超过生命周期 (Time to live) 的数据，并以此来自动管理数据规模并提高性能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/generated-columns" target="_blank">生成列</a> (GA)</td>
    <td>生成列 (Generated Columns) 的值是通过实时计算列定义中的 SQL 表达式得到的。该功能将一些应用逻辑推向数据库层，从而提升查询效率。</td>
  </tr>
  <tr>
    <td rowspan="2">安全</td>
    <td><a href="https://docs.pingcap.com/tidb/dev/security-compatibility-with-mysql" target="_blank">LDAP 身份认证</a></td>
    <td>TiDB 支持与 <a href="https://dev.mysql.com/doc/refman/8.0/en/ldap-pluggable-authentication.html" target="_blank"> MySQL 8.0</a> 兼容的 LDAP 身份认证。</td>
  </tr>
  <tr>
    <td>增强数据库审计功能（<a href="https://www.pingcap.com/tidb-enterprise/" target="_blank">企业版</a>）</td>
    <td>TiDB 企业版增强了数据库审计功能，通过更细粒度的事件过滤控制、更友好的过滤条件设置方式、新增的 JSON 格式输出文件和审计日志的生命周期管理，大幅提升了系统的审计能力。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 性能

* 增强分区 Raft KV 存储引擎（实验特性）[#11515](https://github.com/tikv/tikv/issues/11515) [#12842](https://github.com/tikv/tikv/issues/12842) @[busyjay](https://github.com/busyjay) @[tonyxuqqi](https://github.com/tonyxuqqi) @[tabokie](https://github.com/tabokie) @[bufferflies](https://github.com/bufferflies) @[5kbpers](https://github.com/5kbpers) @[SpadeA-Tang](https://github.com/SpadeA-Tang) @[nolouch](https://github.com/nolouch) **tw:Oreoxmt**

    TiDB v6.6.0 引入了分区 Raft KV 存储引擎作为实验特性，该引擎使用多个 RocksDB 实例存储 TiKV 的 Region 数据，每个 Region 的数据都独立存储在单独的 RocksDB 实例中。分区 Raft KV 能够更好地控制 RocksDB 实例的文件数和层级，实现 Region 间数据操作的物理隔离，并支持平稳管理更多的数据。与原 TiKV 存储引擎相比，使用分区 Raft KV 引擎在相同硬件条件和读写混合场景下，可以实现大约两倍的写入吞吐量、三倍的读取吞吐量，并缩短大约 4/5 的弹性扩展时间。

    在 TiDB v7.1.0 中，分区 Raft KV 引擎与 TiFlash 兼容，并支持 TiDB Lightning、BR 和 TiCDC 等工具。

    该功能目前是实验特性，不推荐在生产环境中使用。目前仅支持在新集群中使用新引擎，暂不支持从原 TiKV 存储引擎直接升级到该引擎。

    更多信息，请参考[用户文档](/partitioned-raft-kv.md)。

* TiFlash 查询支持延迟物化功能 (GA) [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

    在 v7.0.0 中，TiFlash 引入了延迟物化实验特性，用于优化查询性能。该特性默认关闭（系统变量 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) 默认为 `OFF`）。当 `SELECT` 语句中包含过滤条件（`WHERE` 子句）时，TiFlash 默认会先读取该查询所需列的全部数据，然后再根据查询条件对数据进行过滤、聚合等计算任务。开启该特性后，TiFlash 支持下推部分过滤条件到 TableScan 算子，即先扫描过滤条件相关的列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少 IO 扫描和数据处理的计算量。

    从 v7.1.0 开始，TiFlash 延迟物化功能正式 GA，默认开启（系统变量 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) 默认为 `ON`），TiDB 优化器会根据统计信息和查询的过滤条件，决定哪些过滤条件会被下推到 TableScan 算子。

    更多信息，请参考[用户文档](/tiflash/tiflash-late-materialization.md)。

* TiFlash 支持根据网络交换数据量自动选择 MPP 模式的 Join 算法 [#7084](https://github.com/pingcap/tiflash/issues/7084) @[solotzg](https://github.com/solotzg)

    TiFlash MPP 模式有多种 Join 算法。在 v7.1.0 之前的版本中，TiDB 根据变量 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 以及实际数据量决定 TiFlash MPP 模式是否使用 Broadcast Hash Join 算法。

    在 v7.1.0 中，TiDB 引入变量 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-从-v710-版本开始引入)，控制是否基于最小网络数据交换策略选择 MPP Join 算法。该变量默认关闭，表示默认保持 v7.1.0 之前的算法选择策略。如需开启，请设置该变量为 `ON`。开启后，你无需再手动调整 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 的阈值（此时这两个变量将不再生效），TiDB 会自动估算不同 Join 算法所需进行网络交换的数据量，然后选择综合开销较小的算法，从而减少网络流量，提升 MPP 查询性能。

    更多信息，请参考[用户文档](/tiflash/use-tiflash-mpp-mode.md#mpp-模式的算法支持)。

* 支持自适应副本读取缓解读热点 [#14151](https://github.com/tikv/tikv/issues/14151) @[sticnarf](https://github.com/sticnarf) @[you06](https://github.com/you06)

    在读热点场景中，热点 TiKV 无法及时处理读请求，导致读请求排队。但是，此时并非所有 TiKV 资源都已耗尽。为了降低延迟，TiDB v7.1.0 引入了负载自适应副本读取功能，允许从其他有可用资源的 TiKV 节点读取副本，而无需在热点 TiKV 节点排队等待。你可以通过 [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-从-v700-版本开始引入) 系统变量控制读请求的排队长度。当 leader 节点的预估排队时间超过该阈值时，TiDB 会优先从 follower 节点读取数据。在读热点的情况下，与不打散读热点相比，该功能可提高读取吞吐量 70%～200%。

    更多信息，请参考[用户文档](/troubleshoot-hot-spot-issues.md#打散读热点)。

* 增强缓存非 Prepare 语句执行计划的能力（实验特性）[#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990) **tw:Oreoxmt**

    TiDB v7.0.0 引入了非 Prepare 语句的执行计划缓存作为实验特性，以提升在线交易场景的并发处理能力。在 v7.1.0 中，TiDB 继续增强非 Prepare 语句执行计划，支持缓存更多模式的 SQL。

    为了提升内存利用率，TiDB v7.1.0 将非 Prepare 与 Prepare 语句的缓存池合并。你可以通过系统变量 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 设置缓存大小。原有的系统变量 [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-从-v610-版本开始引入) 和 [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) 被废弃。

    为了保持向前兼容，从旧版本升级到 v7.1.0 时，缓存池大小 `tidb_session_plan_cache_size` 的值与 `tidb_prepared_plan_cache_size` 保持一致，[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 保持升级前的设置。经过性能测试后，你可通过 `tidb_enable_non_prepared_plan_cache` 开启非 Parepare 语句的执行计划缓存功能。

    非 Prepare 语句执行计划缓存默认不支持 DML 语句，若要启用支持，你可以将 [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-从-v710-版本开始引入) 系统变量设置为 `ON`。

    更多信息，请参考[用户文档](/sql-non-prepared-plan-cache.md)。

* DDL 支持分布式并行执行框架（实验特性）[#41495](https://github.com/pingcap/tidb/issues/41495) @[benjamin2037](https://github.com/benjamin2037) **tw:ran-huang**

    TiDB v7.1.0 之前的版本中，在同一时间只有一个 TiDB 节点能够担任 DDL Owner 并执行 DDL 任务。从 TiDB v7.1.0 开始，在新的分布式并行执行框架下，多个 TiDB 节点可以并行执行同一项 DDL 任务，从而更好地利用 TiDB 集群的资源，大幅提升 DDL 的性能。此外，你还可以通过增加 TiDB 节点来线性提升 DDL 的性能。需要注意的是，该特性是实验性特性，目前仅支持 `ADD INDEX` 操作。

    如果要使用分布式并行执行框架，只需将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task) 的值设置为 `ON`：

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    更多信息，请参考[用户文档](/tidb-distributed-execution-framework.md)。

### 稳定性

* 资源管控成为正式功能 (GA) [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp) **tw:hfxsd**

    TiDB 持续增强资源管控能力，在 v7.1.0 该功能正式 GA。该特性将极大地提升 TiDB 集群的资源利用率和性能表现。资源管控特性的引入对 TiDB 具有里程碑的意义，你可以将一个分布式数据库集群划分成多个逻辑单元，将不同的数据库用户映射到对应的资源组中，并根据实际需求设置每个资源组的配额。当集群资源紧张时，同一资源组内的会话所使用的全部资源将受到配额限制，防止某一资源组的过度消耗对其他资源组的会话造成影响。

    该特性也可以将多个来自不同系统的中小型应用整合到同一个 TiDB 集群中。即使某个应用的负载增加，也不会影响其他应用的正常运行。而在系统负载较低的时候，繁忙的应用即使超出设定的读写配额，仍可获得所需系统资源，实现资源的最大化利用。此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

    在 TiDB v7.1.0 中，该特性增加了基于实际负载和硬件部署来估算系统容量上限的能力，为你进行容量规划提供更准确的参考。这有助于你更好地管理 TiDB 的资源分配，从而满足企业级场景的稳定性需求。

    为了更好的用户体验，TiDB Dashboard 增加了[资源管控的管理页面](/dashboard/dashboard-resource-control.md)。你可以在该页面查看资源组配置，并通过可视化的方式进行容量预估，便于合理配置资源。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* 支持 Fast Online DDL 的检查点机制，提升容错性和自动恢复能力 [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta)

    TiDB v7.1.0 引入 [Fast Online DDL](/ddl-introduction.md) 的检查点机制，可以大幅提升 Fast Online DDL 的容错性和自动恢复能力。即使 TiDB owner 因故障重启或者切换，TiDB 也能够通过自动定期保存的检查点恢复部分进度，从而让 DDL 执行更加稳定高效。

    更多信息，请参考[用户文档](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)。

* BR 备份恢复工具支持断点恢复 [#42339](https://github.com/pingcap/tidb/issues/42339) @[Leavrth](https://github.com/Leavrth)

    快照恢复或日志恢复会因为一些可恢复性错误导致提前结束，例如硬盘空间占满、节点宕机等突发情况。在 TiDB v7.1.0 之前，即使错误被及时处理，之前恢复的进度也会作废，你需要重新进行恢复。对大规模集群来说，会造成大量额外成本。

    为了尽可能继续上一次的恢复，从 TiDB v7.1.0 起，备份恢复特性引入了断点恢复的功能。该功能可以在意外中断后保留上一次恢复的大部分进度。

    更多信息，请参考[用户文档](/br/br-checkpoint-restore.md)。

* 优化统计信息缓存加载策略 [#42160](https://github.com/pingcap/tidb/issues/42160) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw:hfxsd**

    TiDB v7.1.0 引入了轻量级的统计信息初始化功能作为实验特性。轻量级的统计信息初始化可以大幅减少启动时必须加载的统计信息的数量，从而提升启动过程中统计信息的加载速度。该功能提升了 TiDB 在复杂运行环境下的稳定性，并降低了部分 TiDB 节点重启对整体服务的影响。你可以通过修改 TiDB 配置参数 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-从-v710-版本开始引入) 为 `true` 来开启该特性。

    在 TiDB 启动阶段，如果在初始统计信息加载完成之前执行 SQL，可能会产生不合理的执行计划，进而造成性能问题。为了避免这种情况，TiDB v7.1.0 引入了配置项 [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v710-版本开始引入)。你可以控制 TiDB 是否在统计信息初始化完成后再对外提供服务。该配置项默认关闭。

    更多信息，请参考[用户文档](/statistics.md#统计信息的加载)。

* TiCDC 支持单行数据正确性校验功能 [#8718](https://github.com/pingcap/tiflow/issues/8718) [#42747](https://github.com/pingcap/tidb/issues/42747) @[3AceShowHand](https://github.com/3AceShowHand) @[zyguan](https://github.com/zyguan) **tw:Oreoxmt**

    从 v7.1.0 开始，TiCDC 引入了单行数据正确性校验功能。该功能基于 Checksum 算法对单行数据的正确性进行校验，可以校验一行数据从 TiDB 写入、通过 TiCDC 同步，到写入 Kafka 集群的过程中是否出现错误。TiCDC 数据正确性校验功能仅支持下游是 Kafka 的 Changefeed，目前支持 Avro 协议。

    更多信息，请参考[用户文档](/ticdc/ticdc-integrity-check.md)。

* TiCDC 优化 DDL 同步操作 [#8686](https://github.com/pingcap/tiflow/issues/8686) @[hi-rustin](https://github.com/hi-rustin) **tw:ran-huang**

    在 v7.1.0 之前，当用户在一个大表上进行 DDL 操作时，如果 DDL 操作影响该表中的所有行（例如添加或删除列），TiCDC 的同步延迟会显著增加。从 v7.1.0 开始，TiCDC 对此进行了优化，减轻 DDL 操作对下游延迟的影响。

    更多信息，请参考[用户文档](/ticdc/ticdc-faq.md#ticdc-是否会将有损-ddl-产生的数据变更同步到下游)。

* 提升 TiDB Lightning 导入 TiB 级别数据时的稳定性 [#43510](https://github.com/pingcap/tidb/issues/43510) [#43657](https://github.com/pingcap/tidb/issues/43657) @[D3Hunter](https://github.com/D3Hunter) @[lance6716](https://github.com/lance6716) **tw:hfxsd**

    从 v7.1.0 开始，TiDB Lightning 增加了四个配置项，可以提升在导入 TiB 级数据时的稳定性。

    - `tikv-importer.region-split-batch-size` 用于控制批量 split Region 时的 Region 个数，默认值为 `4096`。
    - `tikv-importer.region-split-concurrency` 用于控制 Split Region 时的并发度，默认值为 CPU 核心数。
    - `tikv-importer.region-check-backoff-limit` 用于控制 split 和 scatter 操作后等待 Region 上线的重试次数，默认值为 `1800`。重试符合指数回退策略，最大重试间隔为 2 秒。若两次重试之间有任何 Region 上线，该次操作不会被计为重试次数。
    - `tikv-importer.pause-pd-scheduler-scope` 用于控制导入数据过程中暂停 PD 调度的范围。该配置项可选值为 `"table"` 或 `"global"`，默认值为 `"table"`。对于 TiDB v6.1.0 之前的版本，只能配置 `"global"` 选项，即导入数据过程中暂停全局调度。从 v6.1.0 开始，支持 `"table"` 选项，表示仅暂停目标表数据范围所在 Region 的调度。在数据量较大的场景建议设置为 `"global"`，以提升稳定性。

  更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-configuration.md)。

### SQL 功能

* 支持通过 `INSERT INTO SELECT` 语句保存 TiFlash 查询结果 (GA) [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi)

    从 v6.5.0 起，TiDB 支持下推 `INSERT INTO SELECT` 语句中的 `SELECT` 子句（分析查询）到 TiFlash，你可以将 TiFlash 的查询结果方便地保存到 `INSERT INTO` 指定的 TiDB 表中供后续分析使用，起到了结果缓存（即结果物化）的效果。

    在 v7.1.0 版本中，该功能正式 GA。当 TiDB 执行 `INSERT INTO SELECT` 语句中的 `SELECT` 子句时，优化器将根据 [SQL 模式](/sql-mode.md)及 TiFlash 副本的代价估算自行决定是否将查询下推至 TiFlash。因此，在实验特性阶段引入的系统变量 `tidb_enable_tiflash_read_for_write_stmt` 将被废弃。需要注意的是，TiFlash 对于 `INSERT INTO SELECT` 语句的计算规则不满足 `STRICT SQL Mode` 要求，因此只有当前会话的 [SQL 模式](/sql-mode.md)为非严格模式（即 `sql_mode` 值不包含 `STRICT_TRANS_TABLES` 和 `STRICT_ALL_TABLES`），TiDB 才允许将 `INSERT INTO SELECT` 语句中的 `SELECT` 子句下推至 TiFlash。

    更多信息，请参考[用户文档](/tiflash/tiflash-results-materialization.md)。

* MySQL 兼容的多值索引 (Multi-Valued Index) 成为正式功能 (GA) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) @[YangKeao](https://github.com/YangKeao)

    过滤 JSON 列中某个数组的值是一种常见操作，但使用普通索引无法加速此过程。在数组上创建多值索引可以大幅提升过滤性能。如果 JSON 列中的某个数组上存在多值索引，则函数 `MEMBER OF()`、`JSON_CONTAINS()` 和 `JSON_OVERLAPS()` 的检索条件可以利用该多值索引进行过滤，从而减少大量的 I/O 消耗，提升执行速度。

    在 v7.1.0 中，TiDB 多值索引成为正式功能 (GA)，支持更完整的数据类型，并与 TiDB 的工具链兼容。你可以在生产环境利用多值索引来加速对 JSON 数组的检索操作。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

* 完善 Hash 分区表和 Key 分区表的分区管理功能 [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss)

    在 v7.1.0 之前，TiDB 中的 Hash 分区表和 Key 分区表只支持 `TRUNCATE PARTITION` 分区管理。从 v7.1.0 开始，Hash 分区表和 Key 分区表新增支持 `ADD PARTITION` 和 `COALESCE PARTITION` 分区管理。你可以根据需要灵活调整 Hash 分区表和 Key 分区表的分区数量。例如，通过 `ADD PARTITION` 语句增加分区数量，或通过 `COALESCE PARTITION` 语句减少分区数量。

    更多信息，请参考[用户文档](/partitioned-table.md#管理-hash-分区和-key-分区)。

* Range INTERVAL 分区定义语法成为正式功能 (GA) [#35683](https://github.com/pingcap/tidb/issues/35683) @[mjonss](https://github.com/mjonss)

    在 v6.3.0 中引入的 Range INTERVAL 的分区定义语法成为正式功能 (GA)。通过该语法，你可以根据所需的间隔 (interval) 定义 Range 分区，不需要枚举所有分区，可大幅度缩短 Range 分区表的定义语句长度。语义与原有 Range 分区等价。

    更多信息，请参考[用户文档](/partitioned-table.md#range-interval-分区)。

* 生成列 (Generated Columns) 成为正式功能 (GA) @[bb7133](https://github.com/bb7133)

    生成列是数据库中非常有价值的一个功能。在创建表时，可以定义一列的值由表中其他列的值计算而来，而不是由用户显式插入或更新。这个生成列可以是虚拟列 (Virtual Column) 或存储列 (Stored Column)。TiDB 在早期版本就提供了与 MySQL 兼容的生成列功能，在 v7.1.0 中这个功能正式 GA。

    使用生成列可以提升 TiDB 对 MySQL 的兼容性，方便从 MySQL 平滑迁移到 TiDB，同时也能简化数据维护复杂度，增强数据一致性并提高查询效率。

    更多信息，请参考[用户文档](/generated-columns.md)。

### 数据库管理

* DDL 任务支持暂停和恢复操作（实验特性）[#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm)

    TiDB v7.1.0 之前的版本中，当 DDL 任务执行期间遇到业务高峰时间点时，为了减少对业务的影响，只能手动取消 DDL 任务。TiDB v7.1.0 引入了 DDL 任务的暂停和恢复功能，你可以在高峰时间点暂停 DDL 任务，等到业务高峰时间结束后再恢复 DDL 任务，从而避免了 DDL 操作对业务负载的影响。

    例如，可以通过如下 `ADMIN PAUSE DDL JOBS` 或 `ADMIN RESUME DDL JOBS` 语句暂停或者恢复多个 DDL 任务：

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    更多信息，请参考[用户文档](/ddl-introduction.md#ddl-相关的命令介绍)。

* 支持无需手动取消 DDL 的平滑升级集群功能 [#39751](https://github.com/pingcap/tidb/issues/39751) @[zimulala](https://github.com/zimulala)**tw:ran-huang**

    在 TiDB v7.1.0 之前的版本中，升级集群时需要先手动取消正在运行或排队的 DDL 任务，并在升级完成后再手动添加这些任务。

    为了提供更平滑的升级体验，TiDB v7.1.0 引入了自动暂停和恢复 DDL 任务的功能。从 v7.1.0 开始，你在升级集群前无需手动取消 DDL 任务。系统会自动暂停正在执行或排队的用户 DDL 任务，等待整个集群完成滚动升级后再自动恢复这些任务，让你可以更加轻松地升级 TiDB 集群。

    更多信息，请参考[用户文档](/smooth-upgrade-tidb.md)。

### 可观测性

* 增加优化器诊断信息 [#43122](https://github.com/pingcap/tidb/issues/43122) @[time-and-fate](https://github.com/time-and-fate)

    获取充足的信息是 SQL 性能诊断的关键。在 v7.1.0 中，TiDB 持续为各种诊断工具增加优化器运行信息，以便更好地解释执行计划如何被选择，从而协助定位 SQL 性能问题。这些信息包括：

    * 在 [`PLAN REPLAYER`](/sql-plan-replayer.md) 的输出中增加 `debug_trace.json` 文件。
    * 在 [`EXPLAIN`](/explain-walkthrough.md) 的输出中为 `operator info` 添加部分统计信息详情。
    * 为[慢日志](/identify-slow-queries.md)的 `Stats` 字段添加部分统计信息详情。

  更多信息，请参考[使用 `PLAN REPLAYER` 保存和恢复集群线程信息](/sql-plan-replayer.md)、[使用 `EXPLAIN` 解读执行计划](/explain-walkthrough.md)和[慢日志查询](/identify-slow-queries.md)。

### 安全

* 更换 TiFlash 系统表信息的查询接口 [#6941](https://github.com/pingcap/tiflash/issues/6941) @[flowbehappy](https://github.com/flowbehappy)

    从 v7.1.0 起，TiFlash 在向 TiDB 提供 [`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) 和 [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md) 系统表的查询服务时，不再使用 HTTP 端口，而是使用 gRPC 端口，从而避免 HTTP 服务的安全风险。

* 支持 LDAP 身份认证 [#43580](https://github.com/pingcap/tidb/issues/43580) @[YangKeao](https://github.com/YangKeao) **tw:ran-huang**

    从 v7.1.0 起，TiDB 支持 LDAP 身份认证，并提供了两种认证插件：`authentication_ldap_sasl` 和 `authentication_ldap_simple`。

    更多信息，请参考[用户文档](/security-compatibility-with-mysql.md)。

* 增强数据库审计功能（企业版）**tw:hfxsd**

    在 v7.1.0 中，TiDB 企业版增强了数据库审计功能，大幅提升了能力范围，改善了使用体验，以满足企业对数据库安全合规的需要：

    - 引入“过滤器” (Filter) 与“规则” (Rule) 的概念，提供了更细分的审计事件定义，并支持更细粒度的审计设置。
    - 支持 JSON 格式的规则定义，提供了更加友好的设置方式。
    - 新增自动日志轮替 (Log Rotation) 和空间管理功能，支持保存时间和日志大小两个维度的设置。
    - 支持输出 TEXT 和 JSON 两种格式的审计日志，便于集成第三方工具。
    - 支持日志内容脱敏，可以替换所有字面值以增强安全性。

  数据库审计是 TiDB 企业版的重要功能之一，为企业提供了强大的监管和审计工具，以保证数据安全和合规性。TiDB 企业版的数据库审计功能可以帮助企业管理人员追踪数据库操作的来源和影响，确保数据不被非法窃取或篡改。同时，数据库审计还可以帮助企业遵守各种法规和合规要求，确保企业在法律和道德方面的合规性。该功能对企业信息安全具有非常重要的应用价值。

    该功能为企业版特性，要获取数据库审计功能及其文档，请在 [TiDB 产品页面](https://pingcap.com/zh/product/#SelectProduct)**企业版**区域点击**立即咨询**联系 PingCAP。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.0.0 升级至当前版本 (v7.1.0) 所需兼容性变更信息。如果从 v6.6.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 为了提高安全性，TiFlash 废弃了 HTTP 服务端口（默认 `8123`），采用 gRPC 端口作为替代

    如果你已经将 TiFlash 升级到 v7.1.0，那么在升级 TiDB 到 v7.1.0 的过程中，TiDB 无法读取 TiFlash 系统表（[`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) 和 [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md)）。

* TiDB v6.2.0 ~ v7.0.0 版本的 TiDB Lightning 会根据 TiDB 集群的版本决定是否暂停全局调度。当 TiDB 集群版本 >= v6.1.0 时，TiDB Lightning 只会暂停目标表数据范围所在 Region 的调度，并在目标表导入完成后恢复调度。其他版本的 TiDB Lightning 则会暂停全局调度。自 TiDB v7.1.0 开始，你可以通过 [`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md) 来控制是否暂停全局调度，默认暂停目标表数据范围所在 Region 的调度。如果目标集群版本低于 v6.1.0 则报错，此时将参数取值改为 `"global"` 后重试即可。 **tw:hfxsd**

### 系统变量

| 变量名 | 修改类型 | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-从-v630-版本开始引入) | 废弃 | 从 v7.1.0 开始，该变量废弃并且默认值从 `OFF` 修改为 `ON`。当 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-从-v50-版本开始引入) 时，优化器将根据 [SQL 模式](/sql-mode.md)及 TiFlash 副本的代价估算自行决定是否将查询下推至 TiFlash。 |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) | 废弃 | 从 v7.1.0 起，该变量被废弃，你可以使用 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 控制 Plan Cache 最多能够缓存的计划数量。 |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-从-v610-版本开始引入) | 废弃 | 从 v7.1.0 起，该变量被废弃，你可以使用 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 控制 Plan Cache 最多能够缓存的计划数量。 |
| `tidb_ddl_distribute_reorg` | 删除 | 重命名为 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入)。 |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) | 修改 | 扩展可选值范围：增加 `authentication_ldap_sasl` 和 `authentication_ldap_simple`。 |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-从-v700-版本开始引入) | 修改 | 该变量从 v7.1.0 开始生效，用于设置基于负载的 replica read 的触发阈值。经进一步的测试后，该变量默认值从 `"0s"` 修改为 `"1s"`。 |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) | 修改 | 默认值从 `OFF` 修改为 `ON`，代表 [TiFlash 延迟物化](/tiflash/tiflash-late-materialization.md)功能默认开启。 |
| [`authentication_ldap_sasl_auth_method_name`](/system-variables.md#authentication_ldap_sasl_auth_method_name-从-v710-版本开始引入) | 新增 | 在 LDAP SASL 身份验证中，验证方法的名称。 |
| [`authentication_ldap_sasl_bind_base_dn`](/system-variables.md#authentication_ldap_sasl_bind_base_dn-从-v710-版本开始引入) | 新增 | 在 LDAP SASL 身份验证中，搜索用户的范围。如果创建用户时没有通过 `AS ...` 指定 `dn`，TiDB 会自动在 LDAP Server 的该范围中根据用户名搜索用户 `dn`。 |
| [`authentication_ldap_sasl_bind_root_dn`](/system-variables.md#authentication_ldap_sasl_bind_root_dn-从-v710-版本开始引入) | 新增 | 在 LDAP SASL 身份验证中，TiDB 登录 LDAP Server 搜索用户时使用的 `dn`。 |
| [`authentication_ldap_sasl_bind_root_pwd`](/system-variables.md#authentication_ldap_sasl_bind_root_pwd-从-v710-版本开始引入) | 新增 | 在 LDAP SASL 身份验证中，TiDB 登录 LDAP Server 搜索用户时使用的密码。 |
| [`authentication_ldap_sasl_ca_path`](/system-variables.md#authentication_ldap_sasl_ca_path-从-v710-版本开始引入) | 新增 | 在 LDAP SASL 身份验证中，TiDB 对 StartTLS 连接使用的 CA 证书的路径。 |
| [`authentication_ldap_sasl_init_pool_size`](/system-variables.md#authentication_ldap_sasl_init_pool_size-从-v710-版本开始引入) | 新增 | 在 LDAP SASL 身份验证中，TiDB 与 LDAP Server 间连接池的初始连接数。 |
| [`authentication_ldap_sasl_max_pool_size`](/system-variables.md#authentication_ldap_sasl_max_pool_size-从-v710-版本开始引入) | 新增 | 在 LDAP SASL 身份验证中，TiDB 与 LDAP Server 间连接池的最大连接数。 |
| [`authentication_ldap_sasl_server_host`](/system-variables.md#authentication_ldap_sasl_server_host-从-v710-版本开始引入) | 新增 | 在 LDAP SASL 身份验证中，LDAP Server 的主机名或地址。 |
| [`authentication_ldap_sasl_server_port`](/system-variables.md#authentication_ldap_sasl_server_port-从-v710-版本开始引入) | 新增 | 在 LDAP SASL 身份验证中，LDAP Server 的 TCP/IP 端口号。 |
| [`authentication_ldap_sasl_tls`](/system-variables.md#authentication_ldap_sasl_tls-从-v710-版本开始引入) | 新增 | 在 LDAP SASL 身份验证中，是否使用 StartTLS 对连接加密。 |
| [`authentication_ldap_simple_auth_method_name`](/system-variables.md#authentication_ldap_simple_auth_method_name-从-v710-版本开始引入) | 新增 | 在 LDAP simple 身份验证中，验证方法的名称。现在仅支持 `SIMPLE`。 |
| [`authentication_ldap_simple_bind_base_dn`](/system-variables.md#authentication_ldap_simple_bind_base_dn-从-v710-版本开始引入) | 新增 | 在 LDAP simple 身份验证中，搜索用户的范围。如果创建用户时没有通过 `AS ...` 指定 `dn`，TiDB 会自动在 LDAP Server 的该范围中根据用户名搜索用户 `dn`。 |
| [`authentication_ldap_simple_bind_root_dn`](/system-variables.md#authentication_ldap_simple_bind_root_dn-从-v710-版本开始引入) | 新增 | 在 LDAP simple 身份验证中，TiDB 登录 LDAP Server 搜索用户时使用的 `dn`。 |
| [`authentication_ldap_simple_bind_root_pwd`](/system-variables.md#authentication_ldap_simple_bind_root_pwd-从-v710-版本开始引入) | 新增 | 在 LDAP simple 身份验证中，TiDB 登录 LDAP Server 搜索用户时使用的密码。 |
| [`authentication_ldap_simple_ca_path`](/system-variables.md#authentication_ldap_simple_ca_path-从-v710-版本开始引入) | 新增 | 在 LDAP simple 身份验证中，TiDB 对 StartTLS 连接使用的 CA 证书的路径。 |
| [`authentication_ldap_simple_init_pool_size`](/system-variables.md#authentication_ldap_simple_init_pool_size-从-v710-版本开始引入) | 新增 | 在 LDAP simple 身份验证中，TiDB 与 LDAP Server 间连接池的初始连接数。 |
| [`authentication_ldap_simple_max_pool_size`](/system-variables.md#authentication_ldap_simple_max_pool_size-从-v710-版本开始引入) | 新增 | 在 LDAP simple 身份验证中，TiDB 与 LDAP Server 间连接池的最大连接数。 |
| [`authentication_ldap_simple_server_host`](/system-variables.md#authentication_ldap_simple_server_host-从-v710-版本开始引入) | 新增 | 在 LDAP simple 身份验证中，LDAP Server 的主机名或地址。 |
| [`authentication_ldap_simple_server_port`](/system-variables.md#authentication_ldap_simple_server_port-从-v710-版本开始引入) | 新增 | 在 LDAP simple 身份验证中，LDAP Server 的 TCP/IP 端口号。 |
| [`authentication_ldap_simple_tls`](/system-variables.md#authentication_ldap_simple_tls-从-v710-版本开始引入) | 新增 | 在 LDAP simple 身份验证中，是否使用 StartTLS 对连接加密。 |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入) | 新增 | 控制是否开启分布式执行框架。开启分布式执行后，DDL、Import 等支持的后端任务将会由集群中多个 TiDB 节点共同完成。该变量由 `tidb_ddl_distribute_reorg` 改名而来。|
| [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-从-v710-版本开始引入) | 新增 | 控制非 Prepare 语句执行计划缓存是否支持 DML 语句。 |
| [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-从-v710-版本开始引入) | 新增 | 控制是否开启 TiCDC 单行数据正确性校验。|
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-从-v710-版本开始引入) | 新增 | 通过设置该变量，你可以更细粒度地控制优化器的行为，并且避免集群升级后优化器行为变化导致的性能回退。 |
| [`tidb_plan_cache_invalidation_on_fresh_stats`](/system-variables.md#tidb_plan_cache_invalidation_on_fresh_stats-从-v710-版本开始引入) | 新增 | 控制当某张表上的统计信息更新后，与该表相关的 Plan Cache 是否自动失效。 |
| [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-从-v710-版本开始引入) | 新增 | 控制可以缓存的 Prepare 或非 Prepare 语句执行计划的最大大小。 |
| [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-从-v710-版本开始引入) | 新增 | 控制是否使用最小网络数据交换策略。使用该策略时，TiDB 会估算 Broadcast Hash Join 和 Shuffled Hash Join 两种算法所需进行网络交换的数据量，并选择网络交换数据量较小的算法。该功能开启后，[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 将不再生效。 |
| [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) | 新增 | 控制 Plan Cache 最多能够缓存的计划数量。其中，Prepare 语句执行计划缓存和非 Prepare 语句执行计划缓存共用一个缓存。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v710-版本开始引入) | 新增 | 用于控制 TiDB 启动时是否在统计信息初始化完成后再对外提供服务。 |
| TiDB | [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-从-v710-版本开始引入) | 新增 | 用于控制 TiDB 启动时是否采用轻量级的统计信息初始化。 |
| TiDB | [`timeout`](/tidb-configuration-file.md#timeout-从-v710-版本开始引入) | 新增 | 用于控制 TiDB 写日志操作的超时时间，当磁盘故障导致日志无法写入时，该配置可以让 TiDB 进程崩溃而不是卡死。默认值为 `0`，即不设定超时时间。 |
| TiKV | [`optimize-filters-for-memory`](/tikv-configuration-file.md#optimize-filters-for-memory-从-v710-版本开始引入) | 新增 | 控制是否生成能够最小化内存碎片的 Bloom/Ribbon filter。 |
| TiKV | [`ribbon-filter-above-level`](/tikv-configuration-file.md#ribbon-filter-above-level-从-v710-版本开始引入) | 新增 | 控制是否对于大于等于该值的 level 使用 Ribbon filter，对于小于该值的 level，使用非 block-based bloom filter。 |
| TiKV | [`split.byte-threshold`](/tikv-configuration-file.md#byte-threshold-从-v50-版本开始引入) | 修改 | 当 [`region-split-size`](/tikv-configuration-file.md#region-split-size) 大于等于 4 GB 时，默认值从 `30MiB` 修改为 `100MiB`。 |
| TiKV | [`split.qps-threshold`](/tikv-configuration-file.md#qps-threshold) | 修改 | 当 [`region-split-size`](/tikv-configuration-file.md#region-split-size) 大于等于 4 GB 时，默认值从 `3000` 修改为 `7000`。 |
| TiKV | [`split.region-cpu-overload-threshold-ratio`](/tikv-configuration-file.md#region-cpu-overload-threshold-ratio-从-v620-版本开始引入) | 修改 | 当 [`region-split-size`](/tikv-configuration-file.md#region-split-size) 大于等于 4 GB 时，默认值从 `0.25` 修改为 `0.75`。 |
| PD | [`store-limit-version`](/pd-configuration-file.md#store-limit-version-从-v710-版本开始引入) | 新增 | 用于设置 store limit 工作模式。可选值为 `"v1"` 和 `"v2"`。 |
| PD | [`schedule.enable-diagnostic`](/pd-configuration-file.md#enable-diagnostic-从-v630-版本开始引入) | 修改 | 默认值从 `false` 修改为 `true`，默认打开调度器的诊断功能。 |
| TiFlash | `http_port` | 删除 | 废弃 TiFlash HTTP 服务端口（默认 `8123`）。 |
| TiDB Lightning | [`tikv-importer.pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | 用于控制导入数据过程中暂停 PD 调度的范围。默认值为 `"table"`，可选值为 `"global"` 和 `"table"`。 |
| TiDB Lightning | [`tikv-importer.region-check-backoff-limit`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | 用于控制 split 和 scatter 操作后等待 Region 上线的重试次数，默认值为 `1800`。重试符合指数回退策略，最大重试间隔为 2 秒。若两次重试之间有任何 Region 上线，该次操作不会被计为重试次数。 |
| TiDB Lightning | [`tikv-importer.region-split-batch-size`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | 用于控制一个 batch 中执行 split 和 scatter 操作的最大 Region 数量，默认值为 `4096`。 |
| TiDB Lightning | [`tikv-importer.region-split-concurrency`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | 用于控制 Split Region 时的并发度，默认值为 CPU 核心数。 |
| TiCDC | [`integrity.corruption-handle-level`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 用于控制当单行数据的 Checksum 校验失败时，Changefeed 打印错误行数据相关日志的级别。默认值为 `"warn"`，可选值为 `"warn"` 和 `"error"`。 |
| TiCDC | [`integrity.integrity-check-level`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 用于控制是否开启单行数据的 Checksum 校验功能，默认值为 `"none"`，即不开启。 |
| TiCDC | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 修改 | 默认值从 `false` 修改为 `true`，代表默认会将表中各个分区的数据分不同的目录来存储。建议保持该配置项为 `true` 以避免同步分区表到存储服务时可能丢数据的问题。 |

## 废弃功能

TiDB 计划在未来版本废弃[乐观事务模式](/optimistic-transaction.md)。从 v7.1.0 开始，不推荐设置 [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode) 的值为 `"optimistic"` 或 `""`。

## 改进提升

+ TiDB

  <!-- **tw:hfxsd** (5) -->

    - 使用 `SQL_NO_CACHE` 来避免 TTL Scan 查询对 TiKV block cache 造成影响 [#43206](https://github.com/pingcap/tidb/issues/43206) @[lcwangchao](https://github.com/lcwangchao)
    - 提升 `MAX_EXECUTION_TIME` 相关错误信息的 MySQL 兼容性 [#43031](https://github.com/pingcap/tidb/issues/43031) @[dveeden](https://github.com/dveeden)
    - `SHOW INDEX` 结果中的 Cardinality 列可以展示统计信息中对应列的不同值的个数 [#42227](https://github.com/pingcap/tidb/issues/42227) @[winoros](https://github.com/winoros)
    - 在 IndexLookUp 中支持对分区表的 MergeSort [#26166](https://github.com/pingcap/tidb/issues/26166) @[Defined2014](https://github.com/Defined2014)
    - 增强了在使用 caching_sha2_password 时与 MySQL 实现的兼容性 [#43576](https://github.com/pingcap/tidb/issues/43576) @[asjdf](https://github.com/asjdf)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - 分区 Raft KV 下降低 Split 对写 QPS 的影响 [#14447](https://github.com/tikv/tikv/issues/14447) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 分区 Raft KV 优化 snapshot 占用的空间[#14581](https://github.com/tikv/tikv/issues/14581) @[bufferflies](https://github.com/bufferflies)
    - status API 增加 `GET /engine_type` 以获得当前 TiKV 是否正在运行分区 Raft KV [#12842](https://github.com/tikv/tikv/issues/12842) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 根据 Region 的大小，优化 load based split 的默认参数 [#14834](https://github.com/tikv/tikv/issues/14834) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 在已有数据的 TiKV 上更新 `storage.engine` 类型不能导致 TiKV 无法启动，应该忽略不正确的修改 [#12842](https://github.com/tikv/tikv/issues/12842) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 记录更新详细的 TiKV 处理请求各个阶段的时间 [#12362](https://github.com/tikv/tikv/issues/12362) @[cfzjywxk](https://github.com/cfzjywxk)
    -  使用 PD 作为 metastore [#13867](https://github.com/tikv/tikv/issues/13867) @[YuJuncen](https://github.com/YuJuncen)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - 新增基于 snapshot 执行细节来自动调整 store limit 大小的控制器。将 `store-limit-version` 设置为 `v2` 后启用，用户无需手动调整配置来控制 scale in 和 scale out 的速度 [#6147](https://github.com/tikv/pd/issues/6147) @[bufferflies](https://github.com/bufferflies)
    - 新增历史负载信息，避免 storage engine 为 raft-kv2 时，热点调度器对不稳定负载所在 region 进行频繁调度 [#6297](https://github.com/tikv/pd/issues/6297) @[bufferflies](https://github.com/bufferflies)
    - 新增 leader 健康检查机制，当 etcd leader 所在 PD server 无法当选 leader 时，主动切换 etcd leader 来保证 PD leader 可用 [#6403](https://github.com/tikv/pd/issues/6403) @[nolouch](https://github.com/nolouch)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - 提升 TiFlash 在存算分离架构下的性能和稳定性 [#6882](https://github.com/pingcap/tiflash/issues/6882) @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin)
    - 支持在 Semi Join 或 Anti Semi Join 中，通过选择较小的表作为 Build 端来优化查询性能 [#7280](https://github.com/pingcap/tiflash/issues/7280) @[yibin87](https://github.com/yibin87)
    - (dup) 提升默认参数下 BR 和 TiDB Lightning 向 TiFlash 导入数据的性能 [#7272](https://github.com/pingcap/tiflash/issues/7272) @[breezewish](https://github.com/breezewish)

+ Tools
    + Backup & Restore (BR)
       - 支持在线修改 `tikv.log-backup.max-flush-interval` 配置 [#14433](https://github.com/tikv/tikv/issues/14433) @[joccau](https://github.com/joccau) 


    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning
      <!-- **tw:hfxsd** (3) -->
        - Region 分布 precheck 项由 Critical 改为 Warn [#42836](https://github.com/pingcap/tidb/issues/42836) @[okJiang](https://github.com/okJiang)
        - 导入期间对 unknown RPC 错误增加 retry [#43291](https://github.com/pingcap/tidb/issues/43291) @[D3Hunter](https://github.com/D3Hunter)
        - 增强 Region job retry [#43682](https://github.com/pingcap/tidb/issues/43682) @[lance6716](https://github.com/lance6716)

## 错误修复

+ TiDB

  <!-- **tw:Oreoxmt** (18) -->

    - 在 reorganize 分区之后增加了手动 analyze table 的提示 [#42183](https://github.com/pingcap/tidb/issues/42183) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup) 修复对于执行中的 `DROP TABLE` 操作，`ADMIN SHOW DDL JOBS` 的结果中缺少表名的问题 [#42268](https://github.com/pingcap/tidb/issues/42268) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在监控面板中有时候无法看到 `Ignore Event Per Minute` 和 `Stats Cache LRU Cost` 这两个图表的问题 [#42562](https://github.com/pingcap/tidb/issues/42562) @[pingandb](https://github.com/pingandb)
    - 修复查询表 `INFORMATION_SCHEMA.COLUMNS` 返回的 `ORDINAL_POSITION` 列结果错误的问题 [#43379](https://github.com/pingcap/tidb/issues/43379) @[bb7133](https://github.com/bb7133)
    - 修复权限表一些列大小写敏感的问题 [#41048](https://github.com/pingcap/tidb/issues/41048) @[bb7133](https://github.com/bb7133)
    - (dup) 修复缓存表执行新增列操作后，新增列值为 `NULL` 而非列的默认值的问题 [#42928](https://github.com/pingcap/tidb/issues/42928) @[lqs](https://github.com/lqs)
    - 修复谓词下推的情况下 CTE 结果的正确性问题 [#43645](https://github.com/pingcap/tidb/issues/43645) @[winoros](https://github.com/winoros)
    - (dup) 修复分区特别多并且带有 TiFlash 副本的分区表在执行 `TRUNCATE TABLE` 时，出现写冲突导致 DDL 重试的问题 [#42940](https://github.com/pingcap/tidb/issues/42940) @[mjonss](https://github.com/mjonss)
    - 如果用户在创建分区表时使用了 subpartition，给出 Warning 的提示 [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    - 修复生成列在处理值溢出问题时与 MySQL 不兼容的问题 [#40066](https://github.com/pingcap/tidb/issues/40066) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 reorganize partition 和其他 DDL 操作不能并发的问题 [#42442](https://github.com/pingcap/tidb/issues/42442) @[bb7133](https://github.com/bb7133)
    - 修复查询使用 `FLOOR` 函数分区的分区表时报错的问题 [#42323](https://github.com/pingcap/tidb/issues/42323) @[jiyfhust](https://github.com/jiyfhust)
    - 修复在取消 DDL 的 reorganize partition 任务后导致后续其他 DDL 报错的问题 [#42448](https://github.com/pingcap/tidb/issues/42448) @[lcwangchao](https://github.com/lcwangchao)
    - 修复某些情况下对删除操作的 assertion 不正确的问题 [#42426](https://github.com/pingcap/tidb/issues/42426) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup) 修复读取 cgroup 信息出错导致 TiDB Server 无法启动的问题，报错信息为 "can't read file memory.stat from cgroup v1: open /sys/memory.stat no such file or directory" [#42659](https://github.com/pingcap/tidb/issues/42659) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在有 global index 的分区表上更新行的 partition key 的数据报错 `Duplicate Key` 的问题 [#42312](https://github.com/pingcap/tidb/issues/42312) @[L-maple](https://github.com/L-maple)
    - 修复 TTL 监控面板中 Scan Worker Time By Phase 的图表不显示数据的问题 [#42515](https://github.com/pingcap/tidb/issues/42515) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在有 global index 的分区表上进行某些查询返回结果错误的问题 [#41991](https://github.com/pingcap/tidb/issues/41991) [#42065](https://github.com/pingcap/tidb/issues/42065) @[L-maple](https://github.com/L-maple)
  <!-- **tw:ran-huang** (17) -->
    - 修复在重组分区表的过程中会显示错误日志的问题 [#42180](https://github.com/pingcap/tidb/issues/42180) @[mjonss](https://github.com/mjonss)
    - 修复 `INFORMATION_SCHEMA.DDL_JOBS` 表中 `QUERY` 列的数据长度可能超出列定义的问题 [#42440](https://github.com/pingcap/tidb/issues/42440) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复表 `INFORMATION_SCHEMA.CLUSTER_HARDWARE` 在容器中可能显示错误的值的问题 [#42851](https://github.com/pingcap/tidb/issues/42851) @[hawkingrei](https://github.com/hawkingrei)
    - 修复通过 `ORDER BY` + `LIMIT` 的方式查询分区表时，返回结果错误的问题 [#43158](https://github.com/pingcap/tidb/issues/43158) @[Defined2014](https://github.com/Defined2014)
    - 修复可能出现多个使用 injest 的方式的 DDL 任务同时运行的问题 [#42903](https://github.com/pingcap/tidb/issues/42903) @[tangenta](https://github.com/tangenta)
    - (dup) 修复查询分区表时使用 `Limit` 返回错误值的问题 [#24636](https://github.com/pingcap/tidb/issues/24636) @[winoros](https://github.com/winoros)
    - 修复 IPv6 环境下显示错误的 TiDB 地址的问题 [#43260](https://github.com/pingcap/tidb/issues/43260) @[nexustar](https://github.com/nexustar)
    - 修复系统变量 `tidb_enable_tiflash_read_for_write_stmt` 和 `tidb_enable_exchange_partition` 显示错误的值的问题 [#43281](https://github.com/pingcap/tidb/issues/43281) @[gengliqi](https://github.com/gengliqi)
    - 修复代理协议在处理某些错误数据时报错 `Header read timeout` 的问题 [#43205](https://github.com/pingcap/tidb/issues/43205) @[blacktear23](https://github.com/blacktear23)
    - 修复当 `tidb_scatter_region` 变量设置为开启时，对某个 partition 进行 truncate 操作后没有自动分裂 Region 的问题 [#43174](https://github.com/pingcap/tidb/issues/43174) [#43028](https://github.com/pingcap/tidb/issues/43028) @[jiyfhust](https://github.com/jiyfhust)
    - 在具有生成列的表上增加一些检查，并对一些不支持的列的 DDL 操作报错 [#38988](https://github.com/pingcap/tidb/issues/38988) [#24321](https://github.com/pingcap/tidb/issues/24321) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在某些类型转换出错的情况下报错信息不对的问题 [#41730](https://github.com/pingcap/tidb/issues/41730) @[hawkingrei](https://github.com/hawkingrei)
    - 解决 TiDB 节点在正常 shutdown 后，在此节点上触发的 DDL 任务会被取消的问题 [#43854](https://github.com/pingcap/tidb/issues/43854) @[zimulala](https://github.com/zimulala)
    - 修复当 PD 成员地址发生变化时，为 AUTO_INCREMENT 列分配 ID 会长时间阻塞的问题 [#42643](https://github.com/pingcap/tidb/issues/42643) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复执行 DDL 期间报 `GC lifetime is shorter than transaction duration` 错误的问题 [#40074](https://github.com/pingcap/tidb/issues/40074) @[tangenta](https://github.com/tangenta)
    - 修复元数据锁非预期地阻塞 DDL 执行的问题 [#43755](https://github.com/pingcap/tidb/issues/43755) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 IPv6 环境下的集群无法查询部分系统视图的问题 [#43286](https://github.com/pingcap/tidb/issues/43286) @[Defined2014](https://github.com/Defined2014)
  <!-- **tw:qiancai** (16) -->
    - 修复在 add 或者 coalesce 分区过程中，新的行被写入错误分区的问题 [#43892](https://github.com/pingcap/tidb/issues/43892) @[mjonss](https://github.com/mjonss)
    - 修复动态裁剪模式下内连接表时找不到分区的问题 [#43686](https://github.com/pingcap/tidb/issues/43686) @[mjonss](https://github.com/mjonss)
    - 修复 analyze 表时报语法错误的问题 [#43392](https://github.com/pingcap/tidb/issues/43392) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在重命名表期间 TiCDC 可能丢失部分行变更的问题 [#43338](https://github.com/pingcap/tidb/issues/43338) @[tangenta](https://github.com/tangenta)
    - 修复在客户端使用游标读导致 TiDB server 崩溃的问题 [#38116](https://github.com/pingcap/tidb/issues/38116) @[YangKeao](https://github.com/YangKeao)
    - 修复 `ADMIN SHOW DDL JOBS LIMIT` 返回错误结果的问题 [#42298](https://github.com/pingcap/tidb/issues/42298) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复使用 UNION 查询联合视图和临时表时 TiDB panic 的问题 [#42563](https://github.com/pingcap/tidb/issues/42563) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在一个事务中提交多条语句时重命名表不生效的问题 [#39664](https://github.com/pingcap/tidb/issues/39664) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复时间转换时 Prepared Plan Cache 与 Non-Prepared Plan Cache 的行为不兼容性的问题 [#42439](https://github.com/pingcap/tidb/issues/42439) @[qw4990](https://github.com/qw4990)
    - 修复 Plan Cache 导致 Decimal 类型的结果出错的问题 [#43311](https://github.com/pingcap/tidb/issues/43311) @[qw4990](https://github.com/qw4990)
    - 修复 NAAJ 中错误的类型检查导致 TiDB panic 的问题 [#42459](https://github.com/pingcap/tidb/issues/42459) @[AilinKid](https://github.com/AilinKid)
    - 修复 RC 隔离级别下悲观事务中执行失败的 DML 可能导致数据索引不一致的问题 [#43294](https://github.com/pingcap/tidb/issues/43294) @[ekexium](https://github.com/ekexium)
    - 修复在一些极端情况下，悲观事务的第一条语句发生重试时，对该事务进行 resolve lock 可能影响事务正确性的问题 [#42937](https://github.com/pingcap/tidb/issues/42937) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复在一些罕见的情况下，悲观事务的残留悲观锁在 GC resolve lock 时可能被影响数据正确性的问题 [#43243](https://github.com/pingcap/tidb/issues/43243) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复 LOCK 转 PUT 优化导致特定查询返回重复数据的问题 [#28011](https://github.com/pingcap/tidb/issues/28011) @[zyguan](https://github.com/zyguan)
    - 修复唯一索引加锁行为不一致的问题 [#36438](https://github.com/pingcap/tidb/issues/36438) @[zyguan](https://github.com/zyguan)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

  <!-- **tw:hfxsd** (1)-->

    - 修复在 `tidb_pessimistic_txn_fair_locking` 启用时，在一些极端情况下，RPC 失败重试导致的过期请求有可能影响数据正确性的问题 [#14551](https://github.com/tikv/tikv/issues/14551) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复加密 Key ID 冲突会导致旧的 Key 被删除 [#14585](https://github.com/tikv/tikv/issues/14585) @[tabokie](https://github.com/tabokie)
    - 修复旧的悲观锁请求在 force-lock 模式下导致当 lock 被 resolve 之后数据破坏或者不一致[#14551](https://github.com/tikv/tikv/issues/14551) @[MyonKeminta] (https://github.com/MyonKeminta)
    - 修复集群从之前版本升级到 v6.5 或更高版本时由于累计的 lock 记录带来的性能问题 [#14780](https://github.com/tikv/tikv/issues/14780) @[MyonKeminta] (https://github.com/MyonKeminta)
    - 修复 PITR 恢复过程中出现的 `raft entry is too large` 问题 @[YuJuncen] (https://github.com/YuJuncen)
    - 修复 PITR 恢复过程中 TiKV 由于 log_batch 超过 2G 导致 panic 的问题 @[YuJuncen] (https://github.com/YuJuncen)
    - 修复 Replay 悲观锁请求导致正确性问题 @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - 修复了在 TiKV panic 后，PD 监控面板 low space store 数量异常的问题 [#6252](https://github.com/tikv/pd/issues/6252) @[HuSharp](https://github.com/HuSharp)
    - 修复了在 PD leader 切换后，Region stats 监控数据被删除的问题 [#6366](https://github.com/tikv/pd/issues/6366) @[iosmanthus](https://github.com/iosmanthus)
    - 修复了 Rule checker 无法修复 label 为 `schedule=deny` 的不健康 Region 的问题 [#6426](https://github.com/tikv/pd/issues/6426) @[nolouch](https://github.com/nolouch)
    - 修复了 TiKV/TiFlash 重启后，部分已有 label 丢失的问题 [#6467](https://github.com/tikv/pd/issues/6467) @[JmPotato](https://github.com/JmPotato)
    - 修复了复制模式存在 learner 节点时可能无法切换状态的问题 [#14704](https://github.com/tikv/tikv/issues/14704) @[nolouch](https://github.com/nolouch)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

  <!-- **tw:qiancai** (2) -->

    - 修复开启延迟物化 (Late Materialization) 后查询 TIMESTAMP 或者 TIME 类型报错的问题 [#7455](https://github.com/pingcap/tiflash/issues/7455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复大更新事务可能会导致 TiFlash 反复报错重启的问题 [#7316](https://github.com/pingcap/tiflash/issues/7316) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)
      <!-- **tw:hfxsd** (2)-->
        - 修复当集群中 TiKV 出现宕机导致备份缓慢的问题 [#42973](https://github.com/pingcap/tidb/issues/42973) @[YuJuncen](https://github.com/YuJuncen)
        - 修复某些情况下备份失败丢失错误信息的问题 [#43236](https://github.com/pingcap/tidb/issues/43236) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC
- 修复设置 timezone 时相关的问题 [#8798](https://github.com/pingcap/tiflow/issues/8798)
- 修复 PD 地址或 leader 出现故障时 TiCDC 不能自动恢复的问题 [#8812](https://github.com/pingcap/tiflow/issues/8812)[#8877](https://github.com/pingcap/tiflow/issues/8877)
- 修复上游 tikv 节点 crash 时 checkpoint lag 上升的问题 [#8858](https://github.com/pingcap/tiflow/issues/8858)
- 优化同步到对象存储场景下发生 DDL 时的目录结构 [#8890](https://github.com/pingcap/tiflow/issues/8890)
-  优化 CDC 的同步任务失败时对上游的 GC TLS 设置方法 [#8887](https://github.com/pingcap/tiflow/issues/8887)
- 增加支持同步到 KOP 下游  [#8892](https://github.com/pingcap/tiflow/issues/8892)
- 同步到 Kafka 时，支持采用 open-protocol 协议发生 update 只同步发生变更的列 [#8706](https://github.com/pingcap/tiflow/issues/8706)
- 修复同步到对象存储场景下上游做 exchange partition 时不能正常同步到下游的问题 [#8914](https://github.com/pingcap/tiflow/issues/8914)
- 优化下游出现故障等场景下 CDC 对错误处理的方式 [#8657](https://github.com/pingcap/tiflow/issues/8657)
- 增加一个配置可以控制在打开 TLS 场景是否设置认证算法 [#8867](https://github.com/pingcap/tiflow/issues/8867)
- 修复在某些特殊场景下 sorter 组件内存使用过多导致 OOM 问题 [#8974](https://github.com/pingcap/tiflow/issues/8974)
- 修复下游 Kafka 滚动重启 CDC 节点 发生 panic 的问题 [#9023](https://github.com/pingcap/tiflow/issues/9023)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - (dup) 修复数据同步过程中，latin1 字符集数据可能损坏的问题 [#7028](https://github.com/pingcap/tiflow/issues/7028) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning
      <!-- **tw:hfxsd** (8)-->
        - 修复 Lightning 导入性能退化的问题 [#42456](https://github.com/pingcap/tidb/issues/42456) @[lance6716](https://github.com/lance6716)
        - 修复大数据量导入时报 `write to tikv with no leader returned` 错误的问题 [#43055](https://github.com/pingcap/tidb/issues/43055) @[lance6716](https://github.com/lance6716)
        - 修复导入期间输出过多 `keys within region is empty, skip doIngest` 日志的问题 [#43197](https://github.com/pingcap/tidb/issues/43197) @[D3Hunter](https://github.com/D3Hunter)
        - 修复 range 部分写入时可能 panic 的问题 [#43363](https://github.com/pingcap/tidb/issues/43363) @[lance6716](https://github.com/lance6716)
        - 修复宽表导入时可能 OOM 的问题 [#43728](https://github.com/pingcap/tidb/issues/43728) @[D3Hunter](https://github.com/D3Hunter)
        - 修复 Lightning Grafana 面板缺失数据的问题 [#43357](https://github.com/pingcap/tidb/issues/43357) @[lichunzhu](https://github.com/lichunzhu)
        - 修复未正确设置 keyspace name 导致导入失败的问题 [#43684](https://github.com/pingcap/tidb/issues/43684) @[zeminzhou](https://github.com/zeminzhou)
        - 修复当 range 部分写入时在一定情况会跳过数据导入的问题 [#43768](https://github.com/pingcap/tidb/issues/43768) @[lance6716](https://github.com/lance6716)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [ethercflow](https://github.com/ethercflow)
- [hihihuhu](https://github.com/hihihuhu)
- [jiyfhust](https://github.com/jiyfhust)
- [L-maple](https://github.com/L-maple)
- [lqs](https://github.com/lqs)
- [pingandb](https://github.com/pingandb)
- [yorkhellen](https://github.com/yorkhellen)
- [yujiarista](https://github.com/yujiarista)
