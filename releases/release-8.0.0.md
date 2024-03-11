---
title: TiDB 8.0.0 Release Notes
summary: 了解 TiDB 8.0.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.0.0 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：8.0.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.0/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.0.0-DMR#version-list)

在 8.0.0 版本中，你可以获得以下关键特性：

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature/Enhancement</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="4">Scalability and Performance</td>
    <td>Disaggregation of PD to improve scale (experimental) **tw@qiancai** <!--1553, 1558--></td>
    <td>PD (Placement Driver) has a lot of critical modules for the running of TiDB. Each module's resource consumption can increase as certain workloads scale, meaning they can each interfere with other functions in PD, ultimately impacting quality of service of the cluster.
By separating PD modules into separately-deployable services, their blast radii are massively mitigated as the cluster scales. Much larger clusters with much larger workloads are possible with this architecture.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.0/system-variables#tidb_dml_type-从-v800-版本开始引入">用于处理更大事务的批量 DML 执行方式（实验特性）</a>**tw@Oreoxmt** <!--1694--></td>
    <td>大批量的 DML 任务，例如大规模的清理任务、连接或聚合，可能会消耗大量内存，并且在非常大的规模上受到限制。批量 DML (<code>tidb_dml_type = "bulk"</code>) 是一种新的 DML 类型，用于更高效地处理大批量 DML 任务，同时提供事务保证并减轻 OOM 问题。该功能与用于数据加载的导入、加载和恢复操作不同。</td>
  </tr>
  <tr>
    <td>Acceleration of cluster snapshot restore speed **tw@qiancai** <!--1681--></td>
    <td>An optimization to involve all TiKV nodes in the preparation step for cluster restores was introduced to leverage scale such that restore speeds for a cluster are much faster for larger sets of data on larger clusters. Real world tests exhibit restore acceleration of ~300% in slower cases.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_schema_cache_size-new-in-v800">Enhanced stability of a massive number of tables </a>**tw@hfxsd** <!--16408--></td>
    <td>SaaS companies using TiDB as the system of record for their multi-tenant applications often need to store a substantial number of tables. In previous versions, handling table counts in the order of a million or more was feasible, but it had the potential to degrade the overall user experience. TiDB v8.0.0 improves the situation with the following enhancements:
  <ul>
    <li>- Introduce a new information schema caching system, incorporating a lazy-loading Least Recently Used (LRU) cache for table metadata and more efficiently managing schema version changes.</li>
    <li>- Implement a priority queue for `auto analyze`, making the process less rigid and enhancing stability across a wider array of tables.</li>
  </ul>
    </td>
  </tr>
  <tr>
    <td rowspan="1">DB Operations and Observability</td>
    <td>支持观测索引使用情况 **tw@Oreoxmt** <!--1400--></td>
    <td>TiDB v8.0.0 引入 <a href="https://docs.pingcap.com/zh/tidb/v8.0/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a> 表和 <a href="https://docs.pingcap.com/zh/tidb/v8.0/sys-schema.md"><code>sys.schema_unused_index</code></a> 视图，以提供索引的使用统计信息。该功能有助于用户评估所有索引的重要性并优化索引设计。</td>

    </td>
  </tr>
  <tr>
    <td rowspan="3">Data Migration</td>
    <td><a href="https://docs.pingcap.com/tidb/v8.0/ticdc-bidirectional-replication">TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (GA) </a>**tw@hfxsd** <!--1682/1689--></td>
    <td>With this feature, TiCDC allows for a cluster to be assigned the `PRIMARY` BDR role, and enables the replication of DDL statements from that cluster to the downstream cluster.</td>
    </td>
  </tr>
  <tr>
    <td>TiCDC adds support for the Simple protocol **tw@lilin90** <!--1646--></td>
    <td>TiCDC introduces support for a new protocol, the Simple protocol. This protocol includes support for in-band schema tracking capabilities.</td>
  </tr>
  <tr>
    <td>TiCDC adds support for the Debezium format protocol **tw@lilin90** <!--1652--></td>
    <td>TiCDC can now publish replication events to a Kafka sink using a protocol that generates Debezium style messages.</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

从 v8.0.0 开始，PD 支持微服务部署模式 [#5766](https://github.com/tikv/pd/issues/5766) @[binshi-bing](https://github.com/binshi-bing) **tw@qiancai** <!--1553/1558-->

该模式可将 PD 的时间戳分配和集群调度功能拆分为独立的服务，单独部署，从而实现 PD 的性能扩展，在超大规模集群下解决 PD 性能瓶颈问题。我们通常建议当 PD 出现明显的性能瓶颈且无法升配的情况下，考虑使用该模式。
当前支持以下两种服务独立部署
- TSO 微服务：为整个集群提供单调递增的时间戳分配。 
- Scheduling 微服务：为整个集群提供调度功能，包括但不限于负载均衡、热点处理、副本修复、副本放置等。 
每种微服务都以独立进程的方式部署，当相应服务设置的副本数量大于 1 时，提供主备的容灾模式。 

* 增强 Titan 引擎  [#issue号](链接) @[Connor1996](https://github.com/Connor1996) **tw@qiancai** <!--1708-->

    TiDB v8.0.0 版本引入了 Titan 一系列的性能优化和功能增强，主要包括优化 GC 算法、默认开启字典压缩等功能。其中，我们调整了 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 的默认阈值，从 `32KB` 调整为 `?KB` ，进一步扩大 Titan 引擎的适用场景。此外，我们还允许用户动态修改 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 阈值配置，以提升用户使用 Titan 引擎时的性能和灵活性。这些改进和功能增强将为用户提供更加稳定和高效的数据库服务。

    更多信息，请参考[用户文档](/storage-engine/titan-overview.md)。
    
### 性能


* BR 快照恢复速度最高提升 10 倍 GA [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer) @[Leavrth](https://github.com/Leavrth) **tw@qiancai** <!--1681-->

    从 TiDB v8.0.0 起，快照恢复提速正式发布，并默认启用。通过采用粗粒度打散 Region 算法、批量创建库表、降低 SST 文件下载和 Ingest 操作之间的相互影响、加速表统计信息恢复等改进措施，在保持数据充分打散的前提下，快照恢复的速度最高提升约 10 倍。该功能充分利用了每个 TiKV 节点的所有资源，实现并行快速恢复。根据实际案例的测试结果，单个 TiKV 节点的数据恢复速度稳定在 1.2 GB/s，能够在 1 小时内完成对 100 TB 数据的恢复。
    
    这意味着即使在高负载环境下，BR 工具也能够充分利用每个 TiKV 节点的资源，显著减少数据库恢复时间，增强数据库的可用性和可靠性，减少因数据丢失或系统故障引起的停机时间和业务损失。
 
    更多信息，请参考[用户文档](/br/br-snapshot-guide.md#恢复快照备份数据)。
    
* 新增支持下推以下函数到 TiFlash [#50975](https://github.com/pingcap/tidb/issues/50975) [#50485](https://github.com/pingcap/tidb/issues/50485) @[yibin87](https://github.com/yibin87) @[windtalker](https://github.com/windtalker) **tw@Oreoxmt** <!--1662--><!--1664-->

    * `CAST(DECIMAL AS DOUBLE)`
    * `POWER()`

  更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* TiDB 的并发 HashAgg 算法支持数据落盘（实验特性）[#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1365-->

    在之前的 TiDB 版本中，HashAgg 算子的并发算法不支持数据落盘。当 SQL 语句的执行计划包含并发的 HashAgg 算子时，该 SQL 语句的所有数据都只能在内存中进行处理。这导致内存需要处理大量数据，当超过内存限制时，TiDB 只能选择非并发 HashAgg 算法，无法通过并发提升性能。

    在 v8.0.0 中，TiDB 的并发 HashAgg 算法支持数据落盘。在任意并发条件下，HashAgg 算子都可以根据内存使用情况自动触发数据落盘，从而兼顾性能和数据处理量。目前，该功能作为实验特性，引入变量 `tidb_enable_concurrent_hashagg_spill` 控制是否启用支持落盘的并发 HashAgg 算法。当该变量为 `ON` 时，代表启用。该变量将在功能正式发布时废弃。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_concurrent_hashagg_spill-从-v800-版本开始引入)。

* 自动统计信息收集引入优先级队列 [#50132](https://github.com/pingcap/tidb/issues/50132) @[hi-rustin](https://github.com/hi-rustin) **tw@hfxsd** <!--1640-->

    维持优化器统计信息的时效性是稳定数据库性能的关键，绝大多数用户依赖 TiDB 提供的[自动统计信息收集](/statistics.md#自动更新)来保持统计信息的更新。自动统计信息收集轮询所有对象的统计信息状态，并把健康度不足的对象加入队列，逐个收集并更新。在过去的版本中，收集顺序是随机设置的，这可能造成更有收集价值的对象需要长时间等待才被更新，引发潜在的数据库性能回退。

    从 v8.0.0 开始，自动统计信息收集会结合多种条件为对象动态设置优先级，确保更有收集价值的对象优先被处理，比如新创建的索引、发生分区变更的分区表等，健康度更低的对象也会倾向于排在队列前端。该增强提升了收集顺序的合理性，能减少一部分统计信息过旧引发的性能问题，因此提升了数据库稳定性。

    更多信息，请参考[用户文档](/statistics.md#自动更新)。

* 解除执行计划缓存的部分限制 [#49161](https://github.com/pingcap/tidb/pull/49161) @[mjonss](https://github.com/mjonss) @[qw4990](https://github.com/qw4990) **tw@hfxsd** <!--1622/1585-->

    TiDB 支持[执行计划缓存](/sql-prepared-plan-cache.md)，能够有效降低交易类业务系统的处理时延，是提升性能的重要手段。在 v8.0.0 中，TiDB 解除了执行计划缓存的几个限制，含有以下内容的执行计划均能够被缓存：

    - [分区表](/partitioned-table.md)
    - [生成列](/generated-columns.md)，包含依赖生成列的对象（比如[多值索引](/choose-index.md)）

  该增强扩展了执行计划缓存的使用场景，提升了复杂场景下数据库的整体性能。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* 优化器增强对多值索引的支持 [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate) **tw@hfxsd** <!--1405/1584-->

    TiDB 自 v6.6.0 开始引入[多值索引](/sql-statements/sql-statement-create-index.md#多值索引)，提升对 JSON 数据类型的检索性能。在 v8.0.0 中，优化器增强了对多值索引的支持能力，在复杂使用场景下，能够正确识别和利用多值索引来优化查询。

    * 多值索引上的统计信息会被收集，并应用于优化器估算。当一条 SQL 可能选择到数个多值索引时，优化器可以识别开销更小的索引。
    * 当出现用 `OR` 连接的多个 `member of` 条件时，优化器能够为每个 DNF Item（`member of` 条件）匹配一个有效的 Index Partial Path 路径，并将多条路径以 Union 的方式综合起来组成 `Index Merge` 来做更高效的条件过滤和数据读取。

  更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

* 支持设置低精度 TSO 的更新间隔 [#51081](https://github.com/pingcap/tidb/issues/51081) @[Tema](https://github.com/Tema) **tw@hfxsd** <!--1725-->

    TiDB 的[低精度 TSO 功能](/system-variables.md#tidb_low_resolution_tso)使用定期更新的 TSO 作为事务时间戳，在可以容忍读到旧数据的情况下，通过牺牲一定的实时性，降低小的只读事务获取 TSO 的开销，提升高并发读的能力。

    在 v8.0.0 之前，低精度 TSO 功能的 TSO 更新周期固定，无法根据实际业务需要进行调整。在 v8.0.0 版本中，TiDB 引入变量 `tidb_low_resolution_tso_update_interval` 来控制低精度 TSO 功能更新 TSO 的周期。该功能仅在低精度 TSO 功能启用时有效。
    
    更多信息，请参考[用户文档](/system-variables.md#tidb_low_resolution_tso_update_interval-从-v800-版本开始引入)。

### 稳定性

* 支持根据 LRU 算法缓存所需的 schema 信息来减少对 TiDB server 的内存消耗（实验特性）[#50959](https://github.com/pingcap/tidb/issues/50959) @[gmhdbjd](https://github.com/gmhdbjd) **tw@hfxsd** <!--1691-->

    在 v8.0.0 之前，每个 TiDB 节点都会缓存所有表的 schema 信息，一旦表的数量较多，如达到几十万的场景，仅缓存这些表的 schema 信息就会占用大量内存。
    
    从 v8.0.0 开始，引入了参数 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入)，你可以设置缓存 schema 信息可以使用的内存上限，避免占用过多的内存。开启该功能后，将使用 Least Recently Used (LRU) 算法来缓存所需的表，有效减小 schema 信息占用的内存。

    更多信息，请参考[用户文档](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入)。
    
### 高可用

* 代理组件 TiProxy 成为正式功能 (GA) [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@Oreoxmt** <!--1698-->

    TiDB v7.6.0 引入了代理组件 TiProxy 作为实验特性。TiProxy 是 TiDB 的官方代理组件，位于客户端和 TiDB server 之间，为 TiDB 提供负载均衡、连接保持功能，让 TiDB 集群的负载更加均衡，并在维护操作期间不影响用户对数据库的连接访问。
    
    在 v8.0.0 中，TiProxy 成为正式功能，完善了签名证书自动生成、监控等功能。
    
    TiProxy 的应用场景如下：

    * 在 TiDB 集群进行滚动重启、滚动升级、缩容等维护操作时，TiDB server 会发生变动，导致客户端与发生变化的 TiDB server 的连接中断。通过使用 TiProxy，可以在这些维护操作过程中平滑地将连接迁移至其他 TiDB server，从而让客户端不受影响。
    * 所有客户端对 TiDB server 的连接都无法动态迁移至其他 TiDB server。当多个 TiDB server 的负载不均衡时，可能出现整体集群资源充足，但某些 TiDB server 资源耗尽导致延迟大幅度增加的情况。为解决此问题，TiProxy 提供连接动态迁移功能，在客户端无感的前提下，将连接从一个 TiDB server 迁移至其他 TiDB server，从而实现 TiDB 集群的负载均衡。

  TiProxy 已集成至 TiUP、TiDB Operator、TiDB Dashboard 等 TiDB 基本组件中，可以方便地进行配置、部署和运维。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。

### SQL 功能

* 支持处理大量数据的 DML 类型（实验特性）[#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium) **tw@Oreoxmt** <!--1694-->

    在 TiDB v8.0.0 之前，所有事务数据在提交之前均存储在内存中。当处理大量数据时，事务所需的内存成为限制 TiDB 处理事务大小的瓶颈。虽然 TiDB 非事务 DML 功能通过拆分 SQL 语句的方式尝试解决事务大小限制，但该功能存在多种限制，在实际应用中的体验并不理想。

    从 v8.0.0 开始，TiDB 支持处理大量数据的 DML 类型。该 DML 类型在执行过程中将数据及时写入 TiKV，避免将所有事务数据持续存储在内存中，从而支持处理超过内存限制的大量数据。这种 DML 类型在保证事务完整性的同时，采用与标准 DML 相同的语法。`INSERT`、`UPDATE`、`REPLACE` 和 `DELETE` 语句均可使用这种新的 DML 类型来执行大数据量的 DML 操作。

    支持处理大量数据的 DML 类型依赖于 [Pipelined DML](https://github.com/pingcap/tidb/blob/master/docs/design/2024-01-09-pipelined-DML.md) 特性，仅支持在自动提交的事务中使用。你可以通过 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-从-v800-版本开始引入) 系统变量控制是否启用该 DML 类型。

    更多信息，请参考[用户文档](/system-variables.md#tidb_dml_type-从-v800-版本开始引入)。

* TiDB 建表时，支持更多的表达式来设置列的默认值（实验特性）[#50936](https://github.com/pingcap/tidb/issues/50936) @[zimulala](https://github.com/zimulala) **tw@hfxsd** <!--1690-->

    在 v8.0.0 之前，在建表时，列默认值只能为固定的字符串、数字、以及日期。从 v8.0.0 开始，支持使用部分表达式作为列的默认值，如将列的默认值设置为 `UUID()`，从而满足多样化的业务需求。

    更多信息，请参考[用户文档](/data-type-default-values.md#表达式默认值)。

### 数据库管理

* PITR 支持 Amazon S3 对象锁定 [#51184](https://github.com/pingcap/tidb/issues/51184) @[RidRisR](https://github.com/RidRisR) **tw@lilin90** <!--1604-->

    Amazon S3 对象锁定功能支持用户通过设置留存期，有效防止备份数据在指定时间内被意外或故意删除，提升了数据的安全性和完整性。从 v6.3.0 起，BR 为快照备份引入了对 Amazon S3 对象锁定功能的支持，为全量备份增加了额外的安全性保障。从 v8.0.0 起，PITR 也引入了对 Amazon S3 对象锁定功能的支持，无论是全量备份还是日志数据备份，都可以通过对象锁定功能提供更可靠的数据保护，进一步加强了数据备份和恢复的安全性，并满足了监管方面的需求。
    
    更多信息，请参考[用户文档](/br/backup-and-restore-storages.md#存储服务其他功能支持)。
    
* PITR 支持备份恢复由 TiDB Lightning 物理模式导入的数据（实验特性）[#issue号](链接) @[BornChanger](https://github.com/BornChanger) **tw@qiancai** <!--1086-->

    TiDB v8.0.0 版本之前，由于 Lightning 的物理导入模式会“重写历史”，导致 PITR 无法感知到被”重写的历史” ，因此无法对数据进行备份。用户需要在完成数据导入后执行一次全量备份。从 TiDB v8.0.0 版本起，PITR 通过对解析时间戳（ResolvedTs）和 `Ingest SST` 操作进行兼容性设计，使得通过 Lightning 的物理模式导入的数据可以被 PITR 正确的识别、备份和恢复。这项改进为客户提供了更加完善的数据保护和恢复方案。

    更多信息，请参考[用户文档](链接)。

* 支持在会话级将不可见索引 (Invisible Indexes) 调整为可见 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1401-->

    在优化器选择索引以优化查询执行时，默认情况下不会选择[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)。这一机制通常用于在评估是否删除某个索引之前。如果担心删除索引可能导致性能下降，可以先将索引设置为不可见，以便在必要时快速将其恢复为可见。
    
    从 v8.0.0 开始，你可以将会话级系统变量 [`tidb_opt_use_invisible_indexes`](/system-variables.md#) 设置为 `ON`，让当前会话识别并使用不可见索引。利用这个功能，在添加新索引并希望测试其效果时，可以先将索引创建为不可见索引，然后通过修改该系统变量在当前会话中进行测试新索引的性能，而不影响其他会话。这一改进提高了进行性能调优的安全性，并有助于增强生产数据库的稳定性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#不可见索引)。

* 支持将 general log 写入独立文件 [#51248](https://github.com/pingcap/tidb/issues/51248) @[Defined2014](https://github.com/Defined2014) **tw@hfxsd** <!--1632-->

    general log 是 MySQL 兼容的功能，开启后会记录数据库执行的全部 SQL 语句，为问题诊断提供依据。TiDB 也支持此功能，你可以通过设置变量 [`tidb_general_log`](/system-variables.md#tidb_general_log) 开启该功能。但是在过去的版本中，general log 的内容只能和其他信息一起写入实例日志，对需要长期保存的用户不够友好。

    从 v8.0.0 开始，你可以通过配置项 [`log.general-log-file`](/tidb-configuration-file.md#general-log-file) 设置文件名，TiDB 可以把 general log 写入该文件。和实例日志一样，general log 也遵循日志的轮询和保存策略。
   
    另外，为了减少历史日志文件所占用的磁盘空间，TiDB 在 v8.0.0 支持了原生的日志压缩选项。你可以将配置项 [`log.file.compression`](/tidb-configuration-file.md#compression) 设置为 `gzip`，轮询出的历史日志将自动以 [`gzip`](https://www.gzip.org/) 格式压缩。

    更多信息，请参考[用户文档](/tidb-configuration-file.md#general-log-file)。
        
### 可观测性

* 支持观测索引使用情况 [#49830](https://github.com/pingcap/tidb/issues/49830) @[YangKeao](https://github.com/YangKeao) **tw@Oreoxmt** <!--1400-->

    正确的索引设计是提升数据库性能的重要前提。TiDB v8.0.0 新增内存表 [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)，用于记录当前 TiDB 节点中所有索引的访问统计信息，包括：

    * 扫描该索引的语句的累计执行次数
    * 访问该索引时扫描的总行数
    * 扫描索引时的选择率分布
    * 最近一次访问该索引的时间

  通过这些信息，你可以识别未被优化器使用的索引以及过滤效果不佳的索引，从而优化索引设计，提升数据库性能。

    此外，TiDB v8.0.0 新增与 MySQL 兼容的视图 [`sys.schema_unused_index`](/sys-schema.md)，用于记录自 TiDB 上次启动以来未被使用的索引信息。对于从 v8.0.0 之前版本升级的集群，`sys` 中的内容不会自动创建。你可以参考 [`sys`](/sys-schema.md)手动创建。

    更多信息，请参考[用户文档](/information-schema/information-schema-tidb-index-usage.md)。

### 安全

* TiKV 静态加密支持 GCP KMS [#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv) **tw@qiancai** <!--1612-->

    TiKV 基于静态加密功能对存储的数据进行加密，确保数据的安全性。静态加密的安全核心点在于密钥管理，此次在静态加密的密钥管理类型中引入了对 GCP KMS 的支持。TiKV 静态加密支持 GCP KMS 可以帮助用户构建基于 GCP KMS 的静态加密能力，可以保证用户数据的安全性。要是用此功能请完成 TiKV 配置文件的 `[security.encryption.master-key]` 部分的内容，即正确实现 TiKV 与 GCP KMS的关联。

    更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/16737)。

* TiDB 日志脱敏增强 [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhebox](https://github.com/xhebox) **tw@qiancai** <!--1229-->

    TiDB 日志脱敏增强是基于对日志文件中 SQL 文本信息的数据进行标记，以便支持用户在查看时进行敏感数据的安全展示。用户可以更灵活自主地在展示环节控制是否对日志信息进行脱敏，以支持 TiDB 日志在不同场景下的安全使用，提升了客户使用日志脱敏能力的安全性和灵活性。要使用此功能请通过修改系统变量 `tidb_redact_log` 的值设置为 `marker`，此时 TiDB 的运行日志将对 SQL 文本进行标记，查看时将基于标记进行数据的安全展示，从而实现日志信息的保护。

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* TiCDC 支持通过双向复制模式 (Bi-Directional Replication, BDR) 同步 DDL 语句 (GA) [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen) **tw@hfxsd** <!--1689/1682-->

    TiDB v7.6.0 引入了通过双向复制模式同步 DDL 语句的功能。以前，TiCDC 不支持复制 DDL 语句，因此要使用 TiCDC 双向复制必须将 DDL 语句分别应用到两个 TiDB 集群。有了该特性，TiCDC 可以为一个集群分配 `PRIMARY` BDR role，并将该集群的 DDL 语句复制到下游集群。该功能在 v8.0.0 成为正式功能。

    更多信息，请参考[用户文档](/ticdc/ticdc-bidirectional-replication.md)。

* DM 支持使用用户提供的密钥对源和目标数据库的密码进行加密和解密 [#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1497-->

    之前 DM 使用的是自带的一个固定秘钥，安全性较低。而从 8.0 版本开始，用户可以传入自定义的密钥文件，对上下游的数据库的密码进行加密和解密操作，也可以按需替换秘钥，提升了安全性。

    更多信息，请参考[用户文档](链接)。

* Import into 功能增强，支持 Import into... from select 语法（实验特性） [#49883](https://github.com/pingcap/tidb/issues/49883) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1680-->

    在一些大数据量的场景使用 insert into ... select，数据导入的性能较慢，而从 8.0 版本开始，支持用户使用 Import into... from select 来导入查询结果到目标表中，且导入的性能最高可达  insert into ... select 的 8 倍，大大缩短了把查询结果导入目标表的所需时间。此外，该功能还支持导入使用 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

    更多信息，请参考[用户文档](链接)。        
    
* TiDB Lightning 冲突策略简化，同时支持 Replace 的方式处理冲突的数据（实验特性） [#51036](https://github.com/pingcap/tidb/issues/51036) @[lyzx2001](https://github.com/lyzx2001) **tw@qiancai** <!--1684-->

    原先 TiDB Lightning 逻辑导入模式时有一套冲突处理策略，物理导入模式时也有一套冲突策略，同时物理导入模式还有一套前置冲突策略，导致配置复杂。从 v8.0.0 开始，将这三种冲突策略合并成了一套，简化了配置操作。同时在物理导入模式下，还首次引入了通过 `replace` 的方式处理导入过程中冲突的数据，遇到主键或唯一键冲突的数据时，保留最新的数据、覆盖旧的数据。最新数据的定义取决于 TiDB Lightning 内部机制。

    更多信息，请参考[用户文档](链接)。    
    
  * 全局排序功能成为正式功能 (GA)，可提升 `IMPORT INTO` 任务的导入性能和稳定性，支持 40 TiB 的数据导入 [#45719](https://github.com/pingcap/tidb/issues/45719) @[lance6716](https://github.com/lance6716) **tw@qiancai** <!--1580-->

    原先 import into 任务调度到多个 TiDB 节点进行数据导入时，使用节点本地的磁盘对当前节点负责导入的数据进行本地局部排序，无法将所有节点要导入的数据进行全局排序，因此节点间的数据存在重叠时，在导入 TiKV 过程中， TiKV 需要执行较多的 compaction 操作，导致 TiKV 的稳定性和性能下降。而引入全局排序后，可将所有需要导入的数据进行全局排序后再导入 TiKV，数据全局有序，TiKV 也就无需执行 compaction 操作，稳定性以及写入性能都会有较大的提升。同时最高支持 40 TiB 的数据导入。

    更多信息，请参考[用户文档](链接)。    
    
* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.6.0 升级至当前版本 (v8.0.0) 所需兼容性变更信息。如果从 v7.5.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 在开启 `tidb_ddl_enable_fast_reorg` 实现索引加速功能时，编码后的索引键值 ingest 数据到 TiKV 时使用的是固定并发值 (`16`)，无法根据下游 TiKV 的承载能力动态调整。从 v8.0.0 开始，支持使用 [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt-从-v800-版本开始引入) 调整并发。该参数默认值为 `4`，相比之前的默认值 `16`，在 ingest 索引键值对时性能会比之前的版本有所降低。你可以根据集群的负载按需调整该参数。**tw@hfxsd** <!--无 FD-->

* 行为变更 2

### MySQL 兼容性

* `KEY` 分区类型支持分区字段列表为空的语句，具体行为和 MySQL 保持一致。**tw@hfxsd** <!--无 FD-->

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_opt_use_invisible_indexes`](/system-variables.md#) | 新增 | 控制会话中是否能够选择[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)。当修改变量为`ON`时，针对该会话执行的查询，优化能够使用[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)进行优化。|
| [tidb_redact_log](/system-variables.md#) | 修改 | 控制在记录 TiDB 日志和慢日志时如何处理 SAL 文本中的用户信息，可选值为 `OFF`、`ON`、`MARKER`，以分别支持记录信息明文、信息屏蔽、信息标记。当变量值为 `MARKER` 时，日志中的用户信息将被标记处理，可以在之后决定是否对日志信息进行脱敏。 |
|  [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入)      |   新增                           |  设置缓存 schema 信息可以使用的内存上限，避免占用过多的内存。开启该功能后，将使用 LRU 算法来缓存所需的表，有效减小 schema 信息占用的内存。    |
| [`tidb_low_resolution_tso_update_interval`](/system-variables.md#tidb_low_resolution_tso_update_interval-从-v800-版本开始引入) | 新增 | 设置更新 TiDB [缓存 timestamp](system-variables#tidb_low_resolution_tso) 的间隔。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB  |  [`log.general-log-file`]() | 新增 | 指定 `General Query Log` 的保存文件。默认为空，`General Query Log` 将会写入实例文件。 |
| TiDB  |  [`log.file.compression`]() | 新增 | 指定轮询日志的压缩格式。默认为空，即不压缩轮询日志。 |
| TiDB Lightning  |  `duplicate-resolution`  | 废弃 | 用于在物理导入模式下设置是否检测和解决唯一键冲突的记录。从 v8.0.0 开始使用新参数 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代。 |
| TiKV | [`security.encryption.master-key.vendor`] | 新增 | 指定住密钥的服务商类型，支持可选值为 `gcp`、`azure` |
| TiDB Lightning  |  `logical-import-batch-size`  | 新增| 用于在逻辑导入模式下设置一个 batch 里提交的数据大小，取值为字符串类型，默认值为 "96KiB"，单位可以为 KB,KiB,MB,MiB 等存储单位 |
| TiDB Lightning  |  `logical-import-batch-rows` | 新增| 用于在逻辑导入模式下设置一个 batch 里提交的数据行数，默认值为 `65536`。 |
## 离线包变更

## 废弃功能

* 从 v8.0.0 开始，[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 变量被废弃。废弃后，TiDB 不再支持乐观事务的自动重试。作为替代，当使用乐观事务模式发生冲突时，请在应用里捕获错误并重试，或改用[悲观事务模式](/pessimistic-transaction.md)。**tw@lilin90** <!--1671-->
* 从 v8.0.0 开始，TiDB 不再支持 TLSv1.0 和 TLSv1.1 协议。请升级 TLS 至 TLSv1.2 或 TLSv1.3。
* 废弃功能 1

* 废弃功能 2

## 改进提升

+ TiDB

    - 优化 Sort 算子的数据落盘性能 [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1609-->
    - 优化数据落盘功能的退出机制，提升数据落盘时取消查询的性能 [#50511](https://github.com/pingcap/tidb/issues/50511) @[wshwsh12](https://github.com/wshwsh12) **tw@qiancai** <!--1635-->
    - 用多个等值条件做表连接时，支持利用匹配到部分条件的索引做 Index Join [#47233](https://github.com/pingcap/tidb/issues/47233) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--1601-->
    - Index Join 允许被连接的一侧为聚合数据集 [#37068](https://github.com/pingcap/tidb/issues/37068) @[elsa0520](https://github.com/elsa0520) **tw@Oreoxmt** <!--1510-->
    - Import into SQL 功能增强，原先只有在一个导入任务运行完成后才能提交第二个任务，现在可以同时提交 16 个 import into 的任务，大大提升导入的性能，同时方便用户批量导入数据到所需的目标表，提升数据导入效率。 [#49008](https://github.com/pingcap/tidb/issues/49008) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1680-->

+ TiKV

    - 强化 TSO 校验检测，提升使用不当时集群 TSO 的鲁棒性 [#16545](https://github.com/tikv/tikv/issues/16545) @[cfzjywxk](https://github.com/cfzjywxk) **tw@qiancai** <!--1624-->
    - 优化清理悲观锁逻辑，提升未提交事务处理性能 [#16158](https://github.com/tikv/tikv/issues/16158) @[cfzjywxk](https://github.com/cfzjywxk) **tw@qiancai** <!--1661-->
    - 增加 TiKV 统一健康控制，降低单个 TiKV 节点异常对集群访问性能的影响 [#16297](https://github.com/tikv/tikv/issues/16297) [#1104](https://github.com/tikv/client-go/issues/1104) [#1167](https://github.com/tikv/client-go/issues/1167) @[MyonKeminta](https://github.com/MyonKeminta) @[zyguan](https://github.com/zyguan) @[crazycs520](https://github.com/crazycs520) **tw@qiancai** <!--1707-->

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - `MariaDB` 主从复制的场景，即 `MariaDB_主实例` -> `MariaDB_从实例` -> `DM` -> `TiDB` 的迁移场景，当 `gtid_strict_mode = off`，且 `Mariadb_从实例`的 GTID 不严格递增时（比如有业务数据在写 `MariaDB_从实例` ），此时 DM 任务会报错 `less than global checkpoint position`。从 v8.0.0 开始，TiDB 兼容该场景，数据可以正常迁移到下游。 [#issue](链接) @[okJiang](https://github.com/okJiang) **tw@hfxsd** <!--1683-->

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 错误修复

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()
