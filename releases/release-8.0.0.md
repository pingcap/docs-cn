---
title: TiDB 8.0.0 Release Notes
summary: 了解 TiDB 8.0.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.0.0 Release Notes

发版日期：2024 年 3 月 29 日

TiDB 版本：8.0.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.0/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.0.0-DMR#version-list)

在 8.0.0 版本中，你可以获得以下关键特性：

<table>
<thead>
  <tr>
    <th>分类</th>
    <th>功能/增强</th>
    <th>描述</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="4">可扩展性与性能</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.0/pd-microservices">支持拆分 PD 功能为微服务，提高可扩展性（实验特性）</a></td>
    <td>Placement Driver (PD) 包含了多个确保 TiDB 集群能正常运行的关键模块。当集群的工作负载增加时，PD 中各模块的资源消耗也会随之增加，造成这些模块间功能的相互干扰，进而影响整个集群的服务质量。为了解决该问题，从 v8.0.0 起，TiDB 支持将 PD 的 TSO 和调度模块拆分成可独立部署的微服务，可以显著降低当集群规模扩大时模块间的互相影响。通过这种架构，TiDB 能够支持更大规模、更高负载的集群。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.0/system-variables#tidb_dml_type-从-v800-版本开始引入">用于处理更大事务的批量 DML 执行方式（实验特性）</a></td>
    <td>大批量的 DML 任务，例如大规模的清理任务、连接或聚合，可能会消耗大量内存，并且在非常大的规模上受到限制。批量 DML (<code>tidb_dml_type = "bulk"</code>) 是一种新的 DML 类型，用于更高效地处理大批量 DML 任务，同时提供事务保证并减轻 OOM 问题。该功能与用于数据加载的导入、加载和恢复操作不同。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.0/br-snapshot-guide#恢复快照备份数据">提升 BR 快照恢复速度 (GA) </a></td>
    <td>通过该功能，BR 可以充分利用集群的规模优势，使 TiKV 集群中的所有节点都能参与到数据恢复的准备阶段，从而显著提升大规模集群中大数据集的恢复速度。实际测试表明，该功能可将下载带宽打满，下载速度可提升 8 到 10 倍，端到端恢复速度大约提升 1.5 到 3 倍。</td>
  </tr>
  <tr>
    <td>增强在有大量表时缓存 schema 信息的稳定性</td>
    <td>对于使用 TiDB 作为多租户应用程序记录系统的 SaaS 公司，经常需要存储大量的表。在以前的版本中，尽管支持处理百万级或更大数量的表，但可能会影响用户体验。TiDB v8.0.0 支持在 <code>auto analyze</code> 中配置<a href="https://docs.pingcap.com/zh/tidb/v8.0/system-variables#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入">优先队列</a>，使流程更加流畅，并在大量表的情况下提高稳定性。</td>
  </tr>
  <tr>
    <td rowspan="1">数据库管理与可观测性</td>
    <td>支持观测索引使用情况 </td>
    <td>正确的索引设计是提升数据库性能的重要前提。TiDB v8.0.0 引入内存表 <a href="https://docs.pingcap.com/zh/tidb/v8.0/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a> 和视图 <a href="https://docs.pingcap.com/zh/tidb/v8.0/sys-schema-unused-indexes"><code>sys.schema_unused_indexes</code></a> ，用于记录索引的使用情况。该功能有助于用户评估数据库中索引的效率并优化索引设计。</td>
  </tr>
  <tr>
    <td rowspan="2">数据迁移</td>
    <td>TiCDC 支持 <a href="https://docs.pingcap.com/zh/tidb/v8.0/ticdc-simple-protocol">Simple 协议</a> </td>
    <td>TiCDC 支持了新的 Simple 消息协议，该协议通过在 DDL 和 BOOTSTRAP 事件中嵌入表的 schema 信息，实现了对 schema 信息的动态追踪 (in-band schema tracking)。</td>
  </tr>
  <tr>
    <td>TiCDC 支持 <a href="https://docs.pingcap.com/zh/tidb/v8.0/ticdc-debezium">Debezium 协议</a> </td>
    <td>TiCDC 支持了新的 Debezium 协议，TiCDC 可以使用该协议生成 Debezium 格式的数据变更事件并发送给 Kafka sink。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

- PD 支持微服务模式（实验特性）[#5766](https://github.com/tikv/pd/issues/5766) @[binshi-bing](https://github.com/binshi-bing)

    从 v8.0.0 开始，PD 支持微服务模式。该模式可将 PD 的时间戳分配和集群调度功能拆分为以下微服务单独部署，从而实现 PD 的性能扩展，解决大规模集群下 PD 的性能瓶颈问题。

    - `tso` 微服务：为整个集群提供单调递增的时间戳分配。
    - `scheduling` 微服务：为整个集群提供调度功能，包括但不限于负载均衡、热点处理、副本修复、副本放置等。

  每个微服务都以独立进程的方式部署。当设置某个微服务的副本数大于 1 时，该微服务会自动实现主备的容灾模式，以确保服务的高可用性和可靠性。

    目前 PD 微服务仅支持通过 TiDB Operator 进行部署。当 PD 出现明显的性能瓶颈且无法升级配置的情况下，建议考虑使用该模式。

    更多信息，请参考[用户文档](/pd-microservices.md)。

* 增强 Titan 引擎的易用性 [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996)

    - 默认启用 Titan Blob 文件和 RocksDB Block 文件的共享缓存（[`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache从-v800-版本开始引入) 默认为 `true`），无需再单独配置 [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size)。
    - 支持动态修改 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size)、[`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression)、[`discardable-ratio`](/tikv-configuration-file.md#min-blob-size)，以提升使用 Titan 引擎时的性能和灵活性。

  更多信息，请参考[用户文档](/storage-engine/titan-configuration.md)。

### 性能

* BR 快照恢复速度提升 GA [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer) @[Leavrth](https://github.com/Leavrth)

    从 TiDB v8.0.0 版本起，BR 快照恢复提速功能正式发布并默认启用。通过采用粗粒度打散 Region 算法、批量创建库表、降低 SST 文件下载和 Ingest 操作之间的相互影响、加速表统计信息恢复等改进措施，快照恢复的速度有大幅提升。在实际案例中，单个 TiKV 节点的数据恢复速度稳定在 1.2 GiB/s，并且能够在 1 小时内完成对 100 TiB 数据的恢复。

    这意味着即使在高负载环境下，BR 工具也能够充分利用每个 TiKV 节点的资源，显著减少数据库恢复时间，增强数据库的可用性和可靠性，减少因数据丢失或系统故障引起的停机时间和业务损失。需要注意的是，恢复速度的提升是因为使用了大量的 goroutine 来并行工作，会有比较大的内存消耗，特别是在表或者 Region 数很多的时候，推荐使用内存规格较高的机器来运行 BR 的客户端。如果机器的内存规格较小，建议改用细粒度的 Region 分裂打散策略。此外，因为粗粒度打散 Region 算法会占用大量的外部存储带宽，请避免因为外部带宽不足导致的对其他业务的影响。

    更多信息，请参考[用户文档](/br/br-snapshot-guide.md#恢复快照备份数据)。

* 新增支持下推以下函数到 TiFlash [#50975](https://github.com/pingcap/tidb/issues/50975) [#50485](https://github.com/pingcap/tidb/issues/50485) @[yibin87](https://github.com/yibin87) @[windtalker](https://github.com/windtalker)

    * `CAST(DECIMAL AS DOUBLE)`
    * `POWER()`

  更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* TiDB 的并行 HashAgg 算法支持数据落盘（实验特性）[#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008)

    在之前的 TiDB 版本中，HashAgg 算子的并发算法不支持数据落盘。当 SQL 语句的执行计划包含并发的 HashAgg 算子时，该 SQL 语句的所有数据都只能在内存中进行处理。这导致内存需要处理大量数据，当超过内存限制时，TiDB 只能选择非并行 HashAgg 算法，无法通过并发提升性能。

    在 v8.0.0 中，TiDB 的并行 HashAgg 算法支持数据落盘。在任意并发条件下，HashAgg 算子都可以根据内存使用情况自动触发数据落盘，从而兼顾性能和数据处理量。目前，该功能作为实验特性，引入变量 `tidb_enable_parallel_hashagg_spill` 控制是否启用支持落盘的并行 HashAgg 算法。当该变量为 `ON` 时，代表启用。该变量将在功能正式发布后废弃。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)。

* 自动统计信息收集引入优先级队列 [#50132](https://github.com/pingcap/tidb/issues/50132) @[hi-rustin](https://github.com/hi-rustin)

    维持优化器统计信息的时效性是稳定数据库性能的关键，绝大多数用户依赖 TiDB 提供的[自动统计信息收集](/statistics.md#自动更新)来保持统计信息的更新。自动统计信息收集轮询所有对象的统计信息状态，并把健康度不足的对象加入队列，逐个收集并更新。在之前的版本中，这些对象的收集顺序是随机的，可能导致更需要更新的对象等待时间过长，从而引发潜在的数据库性能回退。

    从 v8.0.0 开始，自动统计信息收集引入了优先级队列，根据多种条件动态地为对象分配优先级，确保更有收集价值的对象优先被处理，比如新创建的索引、发生分区变更的分区表等。同时，TiDB 也会优先处理那些健康度较低的表，将它们安排在队列的前端。这一改进优化了收集顺序的合理性，能减少一部分统计信息过旧引发的性能问题，进而提升了数据库稳定性。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)。

* 解除执行计划缓存的部分限制 [#49161](https://github.com/pingcap/tidb/pull/49161) @[mjonss](https://github.com/mjonss) @[qw4990](https://github.com/qw4990)

    TiDB 支持[执行计划缓存](/sql-prepared-plan-cache.md)，能够有效降低交易类业务系统的处理时延，是提升性能的重要手段。在 v8.0.0 中，TiDB 解除了执行计划缓存的几个限制，含有以下内容的执行计划均能够被缓存：

    - [分区表](/partitioned-table.md)
    - [生成列](/generated-columns.md)，包含依赖生成列的对象（比如[多值索引](/choose-index.md#多值索引与执行计划缓存)）

  该增强扩展了执行计划缓存的使用场景，提升了复杂场景下数据库的整体性能。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* 优化器增强对多值索引的支持 [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate)

    TiDB 自 v6.6.0 开始引入[多值索引](/sql-statements/sql-statement-create-index.md#多值索引)，提升对 JSON 数据类型的检索性能。在 v8.0.0 中，优化器增强了对多值索引的支持能力，使其在复杂场景下能够正确识别和利用多值索引来优化查询。

    * 优化器能够收集多值索引的统计信息，并利用这些信息来估算查询。当一条 SQL 可能选择到数个多值索引时，优化器可以识别开销更小的索引。
    * 在查询条件中使用 `OR` 连接多个 `member of` 条件时，优化器能够为每个 DNF Item（`member of` 条件）匹配一个有效的 Index Partial Path 路径，并通过 Union 操作将这些路径集合起来，形成一个 `Index Merge`，以实现更高效的条件过滤和数据读取。

  更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

* 支持设置低精度 TSO 的更新间隔 [#51081](https://github.com/pingcap/tidb/issues/51081) @[Tema](https://github.com/Tema)

    TiDB 的[低精度 TSO 功能](/system-variables.md#tidb_low_resolution_tso)使用定期更新的 TSO 作为事务时间戳。在可以容忍读到旧数据的情况下，该功能通过牺牲一定的实时性，降低小的只读事务获取 TSO 的开销，从而提升高并发读的能力。

    在 v8.0.0 之前，低精度 TSO 功能的 TSO 更新周期固定，无法根据实际业务需要进行调整。在 v8.0.0 中，TiDB 引入变量 `tidb_low_resolution_tso_update_interval` 来控制低精度 TSO 功能更新 TSO 的周期。该功能仅在低精度 TSO 功能启用时有效。

    更多信息，请参考[用户文档](/system-variables.md#tidb_low_resolution_tso_update_interval-从-v800-版本开始引入)。

### 高可用

* 代理组件 TiProxy 成为正式功能 (GA) [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox)

    TiDB v7.6.0 引入了代理组件 TiProxy 作为实验特性。TiProxy 是 TiDB 的官方代理组件，位于客户端和 TiDB server 之间，为 TiDB 提供负载均衡、连接保持功能，让 TiDB 集群的负载更加均衡，并在维护操作期间不影响用户对数据库的连接访问。

    在 v8.0.0 中，TiProxy 成为正式功能，完善了签名证书自动生成、监控等功能。

    TiProxy 的应用场景如下：

    * 在 TiDB 集群进行滚动重启、滚动升级、缩容等维护操作时，TiDB server 会发生变动，导致客户端与发生变化的 TiDB server 的连接中断。通过使用 TiProxy，可以在这些维护操作过程中平滑地将连接迁移至其他 TiDB server，从而让客户端不受影响。
    * 所有客户端对 TiDB server 的连接都无法动态迁移至其他 TiDB server。当多个 TiDB server 的负载不均衡时，可能出现整体集群资源充足，但某些 TiDB server 资源耗尽导致延迟大幅度增加的情况。为解决此问题，TiProxy 提供连接动态迁移功能，在客户端无感的前提下，将连接从一个 TiDB server 迁移至其他 TiDB server，从而实现 TiDB 集群的负载均衡。

  TiProxy 已集成至 TiUP、TiDB Operator、TiDB Dashboard 等 TiDB 基本组件中，可以方便地进行配置、部署和运维。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。

### SQL 功能

* 支持处理大量数据的 DML 类型（实验特性）[#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium)

    在 TiDB v8.0.0 之前，所有事务数据在提交之前均存储在内存中。当处理大量数据时，事务所需的内存成为限制 TiDB 处理事务大小的瓶颈。虽然 TiDB 非事务 DML 功能通过拆分 SQL 语句的方式尝试解决事务大小限制，但该功能存在多种限制，在实际应用中的体验并不理想。

    从 v8.0.0 开始，TiDB 支持处理大量数据的 DML 类型。该 DML 类型在执行过程中将数据及时写入 TiKV，避免将所有事务数据持续存储在内存中，从而支持处理超过内存限制的大量数据。这种 DML 类型在保证事务完整性的同时，采用与标准 DML 相同的语法。`INSERT`、`UPDATE`、`REPLACE` 和 `DELETE` 语句均可使用这种新的 DML 类型来执行大数据量的 DML 操作。

    支持处理大量数据的 DML 类型依赖于 [Pipelined DML](https://github.com/pingcap/tidb/blob/master/docs/design/2024-01-09-pipelined-DML.md) 特性，仅支持在自动提交的事务中使用。你可以通过 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-从-v800-版本开始引入) 系统变量控制是否启用该 DML 类型。

    更多信息，请参考[用户文档](/system-variables.md#tidb_dml_type-从-v800-版本开始引入)。

* 支持在 TiDB 建表时使用更多的表达式设置列的默认值（实验特性）[#50936](https://github.com/pingcap/tidb/issues/50936) @[zimulala](https://github.com/zimulala)

    在 v8.0.0 之前，建表时指定列的默认值仅限于固定的字符串、数字和日期。从 v8.0.0 开始，TiDB 支持使用部分表达式作为列的默认值，例如将列的默认值设置为 `UUID()`，从而满足多样化的业务需求。

    更多信息，请参考[用户文档](/data-type-default-values.md#表达式默认值)。

* 支持系统变量 `div_precision_increment` [#51501](https://github.com/pingcap/tidb/issues/51501) @[yibin87](https://github.com/yibin87)

    MySQL 8.0 增加了变量 `div_precision_increment`，用于指定除法 `/` 运算结果增加的小数位数。在 v8.0.0 之前，TiDB 不支持该变量，而是按照 4 位小数进行除法计算。从 v8.0.0 开始，TiDB 支持该变量，你可以根据需要指定除法运算结果增加的小数位数。

    更多信息，请参考[用户文档](/system-variables.md#div_precision_increment-从-v800-版本开始引入)。

### 数据库管理

* PITR 支持 Amazon S3 对象锁定 [#51184](https://github.com/pingcap/tidb/issues/51184) @[RidRisR](https://github.com/RidRisR)

    Amazon S3 对象锁定功能支持用户通过设置数据留存期，有效防止备份数据在指定时间内被意外或故意删除，提升了数据的安全性和完整性。从 v6.3.0 起，BR 为快照备份引入了对 Amazon S3 对象锁定功能的支持，为全量备份增加了额外的安全性保障。从 v8.0.0 起，PITR 也引入了对 Amazon S3 对象锁定功能的支持，无论是全量备份还是日志数据备份，都可以通过对象锁定功能提供更可靠的数据保护，进一步加强了数据备份和恢复的安全性，并满足了监管方面的需求。

    更多信息，请参考[用户文档](/br/backup-and-restore-storages.md#存储服务其他功能支持)。

* 支持在会话级将不可见索引 (Invisible Indexes) 调整为可见 [#50653](https://github.com/pingcap/tidb/issues/50653) @[hawkingrei](https://github.com/hawkingrei)

    在优化器选择索引时，默认情况下不会选择[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)。这一机制通常用于在评估是否删除某个索引之前。如果担心删除索引可能导致性能下降，可以先将索引设置为不可见，以便在必要时快速将其恢复为可见。

    从 v8.0.0 开始，你可以将会话级系统变量 [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-从-v800-版本开始引入) 设置为 `ON`，让当前会话识别并使用不可见索引。利用这个功能，在添加新索引并希望测试其效果时，可以先将索引创建为不可见索引，然后通过修改该系统变量在当前会话中测试新索引的性能，而不影响其他会话。这一改进提高了性能调优的安全性，并有助于增强生产数据库的稳定性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#不可见索引)。

* 支持将 general log 写入独立文件 [#51248](https://github.com/pingcap/tidb/issues/51248) @[Defined2014](https://github.com/Defined2014)

    general log 是与 MySQL 兼容的功能，开启后能够记录数据库执行的所有 SQL 语句，为问题诊断提供依据。TiDB 也支持此功能，你可以通过设置变量 [`tidb_general_log`](/system-variables.md#tidb_general_log) 开启该功能。在之前的版本中，general log 的内容只能和其他信息一起写入实例日志中，这对于需要长期保存日志的用户来说并不方便。

    从 v8.0.0 开始，你可以通过配置项 [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-从-v800-版本开始引入) 指定一个文件名，将 general log 单独写入该文件。和实例日志一样，general log 也遵循日志的轮询和保存策略。

    另外，为了减少历史日志文件所占用的磁盘空间，TiDB 在 v8.0.0 支持了原生的日志压缩选项。你可以将配置项 [`log.file.compression`](/tidb-configuration-file.md#compression-从-v800-版本开始引入) 设置为 `gzip`，使得轮询出的历史日志自动以 [`gzip`](https://www.gzip.org/) 格式压缩。

    更多信息，请参考[用户文档](/tidb-configuration-file.md#general-log-file-从-v800-版本开始引入)。

### 可观测性

* 支持观测索引使用情况 [#49830](https://github.com/pingcap/tidb/issues/49830) @[YangKeao](https://github.com/YangKeao)

    正确的索引设计是提升数据库性能的重要前提。TiDB v8.0.0 新增内存表 [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)，用于记录当前 TiDB 节点中所有索引的访问统计信息，包括：

    * 扫描该索引的语句的累计执行次数
    * 访问该索引时扫描的总行数
    * 扫描索引时的选择率分布
    * 最近一次访问该索引的时间

  通过这些信息，你可以识别未被优化器使用的索引以及过滤效果不佳的索引，从而优化索引设计，提升数据库性能。

    此外，TiDB v8.0.0 新增与 MySQL 兼容的视图 [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)，用于记录自 TiDB 上次启动以来未被使用的索引信息。对于从 v8.0.0 之前版本升级的集群，`sys` 中的内容不会自动创建。你可以参考 [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md#手动创建-schema_unused_indexes-视图) 手动创建。

    更多信息，请参考[用户文档](/information-schema/information-schema-tidb-index-usage.md)。

### 安全

* TiKV 静态加密支持 Google [Key Management Service (Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive?hl=zh-cn)（实验特性）[#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv)

    TiKV 通过静态加密功能对存储的数据进行加密，以确保数据的安全性。静态加密的安全核心点在于密钥管理。从 v8.0.0 起，你可以通过 Google Cloud KMS 管理 TiKV 的主密钥，构建基于 Cloud KMS 的静态加密能力，从而提高用户数据的安全性。

    要启用基于 Google Cloud KMS 的静态加密，你需要在 Google Cloud 上创建一个密钥，然后在 TiKV 配置文件中添加 `[security.encryption.master-key]` 部分的配置。

    更多信息，请参考[用户文档](/encryption-at-rest.md#tikv-静态加密)。

* 增强 TiDB 日志脱敏 [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhebox](https://github.com/xhebox)

    TiDB 日志脱敏增强是通过对日志文件中的 SQL 文本信息进行标记，支持在查看时安全展示敏感数据。你可以控制是否对日志信息进行脱敏，以实现在不同场景下安全使用 TiDB 日志，提升了使用日志脱敏能力的安全性和灵活性。要使用此功能，可以将系统变量 `tidb_redact_log` 的值设置为 `MARKER`，此时 TiDB 的运行日志中的 SQL 文本会被标记，查看时将基于标记进行数据的安全展示，从而保护日志信息。

    更多信息，请参考[用户文档](/system-variables.md#tidb_redact_log)。

### 数据迁移

* TiCDC 支持 Simple 协议 [#9898](https://github.com/pingcap/tiflow/issues/9898) @[3AceShowHand](https://github.com/3AceShowHand)

    TiCDC 支持了新的 Simple 消息协议，该协议通过在 DDL 和 BOOTSTRAP 事件中嵌入表的 schema 信息，实现了对 schema 信息的动态追踪 (in-band schema tracking)。

    更多信息，请参考[用户文档](/ticdc/ticdc-simple-protocol.md)。

* TiCDC 支持 Debezium 协议 [#1799](https://github.com/pingcap/tiflow/issues/1799) @[breezewish](https://github.com/breezewish)

    通过 Debezium 协议，TiCDC 可以生成 Debezium 格式的数据变更事件，并将这些事件发送到 Kafka sink。这有助于为当前使用 Debezium 从 MySQL 拉取数据进行下游处理的用户简化从 MySQL 迁移到 TiDB 的过程。

    更多信息，请参考[用户文档](/ticdc/ticdc-debezium.md)。

* DM 支持使用用户提供的密钥对源数据库和目标数据库的密码进行加密和解密 [#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter)

    在之前的版本中，DM 使用了一个内置的固定秘钥，安全性相对较低。从 v8.0.0 开始，你可以上传并指定一个密钥文件，用于对上下游数据库的密码进行加密和解密操作。此外，你还可以按需替换秘钥文件，以提升数据的安全性。

    更多信息，请参考[用户文档](/dm/dm-customized-secret-key.md)。

* 支持 `IMPORT INTO ... FROM SELECT` 语法（实验特性），增强 `IMPORT INTO` 功能 [#49883](https://github.com/pingcap/tidb/issues/49883) @[D3Hunter](https://github.com/D3Hunter)

    在之前的 TiDB 版本中，将查询结果导入目标表只能通过 `INSERT INTO ... SELECT` 语句，但该语句在一些大数据量的场景中的导入效率较低。从 v8.0.0 开始，TiDB 新增支持通过 `IMPORT INTO ... FROM SELECT` 将 `SELECT` 的查询结果导入到一张空的 TiDB 目标表中，其性能最高可达 `INSERT INTO ... SELECT` 的 8 倍，可以大幅缩短导入所需的时间。

    此外，你还可以通过 `IMPORT INTO ... FROM SELECT` 导入使用 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-import-into.md)。

* TiDB Lightning 简化冲突处理策略，同时支持以 `replace` 方式处理冲突数据（实验特性）[#51036](https://github.com/pingcap/tidb/issues/51036) @[lyzx2001](https://github.com/lyzx2001)

    在之前的版本中，TiDB Lightning 逻辑导入模式有[一套数据冲突处理策略](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md#冲突数据检测)，而物理导入模式有[两套数据冲突处理策略](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#冲突数据检测)，不易理解和配置。

    从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) 参数统一控制逻辑导入和物理导入模式的冲突检测策略，并简化了该参数的配置。此外，在物理导入模式下，当导入遇到主键或唯一键冲突的数据时，`replace` 策略支持保留最新的数据、覆盖旧的数据。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-configuration.md)。

* 全局排序成为正式功能 (GA)，可显著提升 `IMPORT INTO` 任务的导入性能和稳定性 [#45719](https://github.com/pingcap/tidb/issues/45719) @[lance6716](https://github.com/lance6716)

    在 v7.4.0 以前，当使用[分布式执行框架](/tidb-distributed-execution-framework.md)执行 `IMPORT INTO` 任务时，由于本地存储空间有限，TiDB 只能对部分数据进行局部排序后再导入到 TiKV。这导致了导入到 TiKV 的数据存在较多的重叠，需要 TiKV 在导入过程中执行额外的 compaction 操作，影响了 TiKV 的性能和稳定性。

    随着 v7.4.0 引入全局排序实验特性，TiDB 支持将需要导入的数据暂时存储在外部存储（如 Amazon S3）中进行全局排序后再导入到 TiKV 中，使 TiKV 无需在导入过程中执行 compaction 操作。全局排序在 v8.0.0 成为正式功能 (GA)，可以降低 TiKV 对资源的额外消耗，显著提升 `IMPORT INTO` 的性能和稳定性。启用全局排序后，单个 `IMPORT INTO` 任务支持导入 40 TiB 以内的数据。

    更多信息，请参考[用户文档](/tidb-global-sort.md)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.6.0 升级至当前版本 (v8.0.0) 所需兼容性变更信息。如果从 v7.5.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

- 由 TiUP 默认部署的 Prometheus 版本从 2.27.1 升级到 2.49.1
- 由 TiUP 默认部署的 Grafana 版本从 7.5.11 升级到 7.5.17
- 移除未 GA 但默认启用的 witness 相关调度器 [#7765](https://github.com/tikv/pd/pull/7765) @[rleungx](https://github.com/rleungx)

### 行为变更

* 在安全增强模式 (SEM) 下禁止设置 [`require_secure_transport`](/system-variables.md#require_secure_transport-从-v610-版本开始引入) 为 `ON`，避免用户无法连接的问题 [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
* DM 移除了固定的加解密 key，并支持设置自定义加解密 key。如果升级前[数据源配置](/dm/dm-source-configuration-file.md)和[迁移任务配置](/dm/task-configuration-file-full.md)里使用了加密密码，需参考 [DM 自定义加解密 key](/dm/dm-customized-secret-key.md) 中的升级步骤进行额外操作。[#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter)
* 在之前版本中，启用添加索引加速功能 (`tidb_ddl_enable_fast_reorg = ON`) 后，编码后的索引键值 ingest 到 TiKV 的过程使用了固定的并发数 (`16`)，并未根据下游 TiKV 的处理能力进行动态调整。从 v8.0.0 开始，支持使用 [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt) 设置并发数。该变量默认值为 `4`，相比之前的默认值 `16`，在 ingest 索引键值对时性能可能会有所下降。你可以根据集群的负载按需调整该参数。

### MySQL 兼容性

* `KEY` 分区类型支持分区字段列表为空的语句，具体行为和 MySQL 保持一致。

### 系统变量

| 变量名  | 修改类型  | 描述 |
|--------|------------------------------|------|
| [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)  | 废弃 | 从 v8.0.0 开始，该系统变量被废弃，TiDB 不再支持乐观事务的自动重试。推荐使用[悲观事务模式](/pessimistic-transaction.md)。如果使用乐观事务模式发生冲突，请在应用里捕获错误并重试。 |
| `tidb_ddl_version` | 更名 | 用于控制是否开启 TiDB DDL V2。为了使变量名称更直观，从 v8.0.0 起，该变量更名为 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)。 |
| [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) | 修改 | 增加控制是否维护[访问索引有关的统计信息](/information-schema/information-schema-tidb-index-usage.md)，默认值为 `ON`。 |
| [`tidb_redact_log`](/system-variables.md#tidb_redact_log) | 修改 | 控制在记录 TiDB 日志和慢日志时如何处理 SAL 文本中的用户信息，可选值为 `OFF`（对用户输入的信息不做任何处理）和 `ON`（屏蔽日志中的用户信息）。为了提供更丰富的处理日志中用户信息的方式，v8.0.0 中增加了 `MARKER` 选项，支持标记日志信息。 |
| [`div_precision_increment`](/system-variables.md#div_precision_increment-从-v800-版本开始引入) | 新增 | 用于指定使用运算符 `/` 执行除法操作时，结果增加的小数位数。该功能与 MySQL 保持一致。 |
| [`tidb_dml_type`](/system-variables.md#tidb_dml_type-从-v800-版本开始引入) | 新增 | 设置 DML 语句的执行方式，可选值为 `"standard"` 和 `"bulk"`。 |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) | 新增 | 控制是否启用优先队列来调度自动收集统计信息的任务。开启该变量后，TiDB 会优先收集那些最需要收集统计信息的表的统计信息。 |
| [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) | 新增 | 控制 TiDB 是否支持并行 HashAgg 进行落盘。当该变量设置为 `ON` 时，并行 HashAgg 将支持落盘。该变量将在功能正式发布时废弃。 |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入) | 新增 | 用于控制是否开启 [TiDB 加速建表](/accelerated-table-creation.md)。将该变量的值设置为 `ON` 可以开启该功能，设置为 `OFF` 关闭该功能。默认值为 `OFF`。开启后，将使用 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 加速建表。 |
| [`tidb_load_binding_timeout`](/system-variables.md#tidb_load_binding_timeout-从-v800-版本开始引入) | 新增 | 控制加载绑定的超时时间。当加载绑定的执行时间超过该值时，会停止加载。 |
| [`tidb_low_resolution_tso_update_interval`](/system-variables.md#tidb_low_resolution_tso_update_interval-从-v800-版本开始引入) | 新增 | 设置 TiDB [缓存 timestamp](/system-variables.md#tidb_low_resolution_tso) 的更新时间间隔。 |
| [`tidb_opt_ordering_index_selectivity_ratio`](/system-variables.md#tidb_opt_ordering_index_selectivity_ratio-从-v800-版本开始引入) | 新增 | 当一个索引满足 SQL 语句中的 `ORDER BY` 和 `LIMIT` 子句，但有部分过滤条件未被该索引覆盖时，该系统变量用于控制该索引的估算行数。默认值为 `-1`，表示禁用此系统变量。  |
| [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-从-v800-版本开始引入) | 新增 | 控制当前会话中是否允许优化器选择[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)。当修改变量为 `ON` 时，对该会话中的查询，优化器可以选择不可见索引进行查询优化。|
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入)  |  新增 |  设置缓存 schema 信息可以使用的内存上限，避免占用过多的内存。开启该功能后，将使用 LRU 算法来缓存所需的表，有效减少 schema 信息占用的内存。    |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info) | 修改 | 增加控制是否维护[访问索引有关的统计信息](/information-schema/information-schema-tidb-index-usage.md)，默认值为 `true`。 |
| TiDB | [`tls-version`](/tidb-configuration-file.md#tls-version) | 修改 | 该参数不再支持 `"TLSv1.0"` 和 `"TLSv1.1"`，只支持 `"TLSv1.2"` 和 `"TLSv1.3"`。   |
| TiDB | [`log.file.compression`](/tidb-configuration-file.md#compression-从-v800-版本开始引入) | 新增 | 指定轮询日志的压缩格式。默认为空，即不压缩轮询日志。 |
| TiDB | [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-从-v800-版本开始引入) | 新增 | 指定 general log 的保存文件。默认为空，general log 将会写入实例文件。 |
| TiDB | [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-从-v800-版本开始引入) | 新增 | 控制给 TiKV 发送 RPC 请求时，是否使用新版本的 Region 副本选择器。默认值为 `true`。 |
| TiKV | [`log-backup.initial-scan-rate-limit`](/tikv-configuration-file.md#initial-scan-rate-limit-从-v620-版本开始引入) | 修改 | 增加了最小值为 `1MiB` 的限制。 |
| TiKV | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-从-v530-版本开始引入) | 修改 | 为了提升 TiKV 性能，该参数默认值从 `0` 修改为 `1`，表示 StoreWriter 线程池的大小默认为 `1`。|
| TiKV | [`rocksdb.defaultcf.titan.blob-cache-size`](/tikv-configuration-file.md#blob-cache-size) | 修改 | 从 v8.0.0 开始，TiKV 引入了 `shared-blob-cache` 配置项并默认开启，因此无需再单独设置 `blob-cache-size`。只有当 `shared-blob-cache` 设置为 `false` 时，`blob-cache-size` 的设置才生效。|
| TiKV | [`security.encryption.master-key.vendor`](/encryption-at-rest.md#通过-kms-指定主密钥) | 修改 | 主密钥可选的服务商类型新增 `gcp`。 |
| TiKV | [`rocksdb.defaultcf.titan.shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache从-v800-版本开始引入) | 新增 | 控制是否启用 Titan Blob 文件和 RocksDB Block 文件的共享缓存。默认值为 `true`。|
| TiKV | [`security.encryption.master-key.gcp.credential-file-path`](/encryption-at-rest.md#通过-kms-指定主密钥) | 新增 | 在 `security.encryption.master-key.vendor` 为 `gcp` 时，用于指定 Google Cloud 认证凭证文件的路径。|
| TiDB Lightning  | [`tikv-importer.duplicate-resolution`](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)  | 废弃 | 用于在物理导入模式下设置是否检测和解决唯一键冲突的记录。从 v8.0.0 开始被参数 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代。 |
| TiDB Lightning  | [`conflict.precheck-conflict-before-import`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)  | 新增 | 控制是否开启前置冲突检测，即导入数据到 TiDB 前，先检查所需导入的数据是否存在冲突。该参数默认值为 `false`，表示仅开启后置冲突检测。仅当导入模式为物理导入模式 (`tikv-importer.backend = "local"`) 时可以使用该参数。 |
| TiDB Lightning  | [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) | 新增 | 在逻辑导入模式下，用于限制每个事务中可插入的最大行数，默认值为 `65536`。 |
| TiDB Lightning  | [`logical-import-batch-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) | 新增 | 在逻辑导入模式下，用于设置下游 TiDB 服务器上执行的每条 SQL 语句的最大值。默认值为 `"96KiB"`，单位可以为 KB、KiB、MB、MiB 等存储单位。 |
| Data Migration  | [`secret-key-path`](/dm/dm-master-configuration-file.md) | 新增 | 用于指定加解密上下游密码的密钥文件所在的路径。该文件内容必须是长度为 64 个字符的十六进制的 AES-256 密钥。 |
| TiCDC | [`tls-certificate-file`](/ticdc/ticdc-sink-to-pulsar.md) | 新增 | 用于指定 Pulsar 启用 TLS 加密传输时，客户端的加密证书文件路径。 |
| TiCDC | [`tls-key-file-path`](/ticdc/ticdc-sink-to-pulsar.md) | 新增 | 用于指定 Pulsar 启用 TLS 加密传输时，客户端的加密私钥路径。 |

### 系统表

* 新增系统表 [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) 和 [`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage) 用于记录 TiDB 节点中索引的访问统计信息。
* 新增系统数据库 [`sys`](/sys-schema/sys-schema.md) 和 [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 视图，用于记录自 TiDB 上次启动以来未被使用的索引信息。

## 废弃功能

* 从 v8.0.0 开始，[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 变量被废弃。废弃后，TiDB 不再支持乐观事务的自动重试。作为替代，当使用乐观事务模式发生冲突时，请在应用里捕获错误并重试，或改用[悲观事务模式](/pessimistic-transaction.md)。
* 从 v8.0.0 开始，TiDB 不再支持 TLSv1.0 和 TLSv1.1 协议。请升级 TLS 至 TLSv1.2 或 TLSv1.3。
* 从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) 参数统一控制逻辑导入和物理导入模式的冲突检测策略。旧版冲突检测的参数 [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) 将在未来版本中被移除。
* 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。

## 改进提升

+ TiDB

    - DDL 创建表语句 `CREATE TABLE` 执行性能加速 10 倍，并且可线性扩展 [#50052](https://github.com/pingcap/tidb/issues/50052) @[GMHDBJD](https://github.com/GMHDBJD)
    - 支持同时提交 16 个 `IMPORT INTO ... FROM FILE` 任务，方便批量导入数据到目标表，极大地提升了数据文件导入的效率和性能 [#49008](https://github.com/pingcap/tidb/issues/49008) @[D3Hunter](https://github.com/D3Hunter)
    - 提升 `Sort` 算子的数据落盘性能 [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 优化数据落盘功能的退出机制，支持在数据落盘过程中取消查询 [#50511](https://github.com/pingcap/tidb/issues/50511) @[wshwsh12](https://github.com/wshwsh12)
    - 在处理包含多个等值条件的表连接查询时，支持使用匹配部分条件的索引构造 Index Join [#47233](https://github.com/pingcap/tidb/issues/47233) @[winoros](https://github.com/winoros)
    - 增强 Index Merge 能力，使其能识别查询中的排序需求，并能选中满足排序要求的索引 [#48359](https://github.com/pingcap/tidb/issues/48359) @[AilinKid](https://github.com/AilinKid)
    - 当 `Apply` 算子没有并发执行时，支持通过执行 `SHOW WARNINGS` 查看阻碍并发的算子名 [#50256](https://github.com/pingcap/tidb/issues/50256) @[hawkingrei](https://github.com/hawkingrei)
    - 优化点查的索引选择，在所有的索引都支持点查时选择其中性能最优的一个用于查询 [#50184](https://github.com/pingcap/tidb/issues/50184) @[elsa0520](https://github.com/elsa0520)
    - 将统计信息同步加载任务的优先级暂时调整为 `High`，避免在 TiKV 高负载时同步加载任务大面积超时，从而导致统计信息无法加载 [#50332](https://github.com/pingcap/tidb/issues/50332) @[winoros](https://github.com/winoros)
    - 在 `PREPARE` 语句无法命中执行计划缓存时，支持通过执行 `SHOW WARNINGS` 查看原因 [#50407](https://github.com/pingcap/tidb/issues/50407) @[hawkingrei](https://github.com/hawkingrei)
    - 提升当多次更新同一行的数据时查询估算信息的准确性 [#47523](https://github.com/pingcap/tidb/issues/47523) @[terry1purcell](https://github.com/terry1purcell)
    - Index Merge 支持在 `AND` 谓词中内嵌多值索引和 `OR` 操作符 [#51778](https://github.com/pingcap/tidb/issues/51778) @[time-and-fate](https://github.com/time-and-fate)
    - 当设置 `force-init-stats` 为 `true` 时，即 TiDB 启动时等待统计信息初始化完成后再对外提供服务，这一设置不再影响 HTTP server 提供服务，用户仍可查看监控 [#50854](https://github.com/pingcap/tidb/issues/50854) @[hawkingrei](https://github.com/hawkingrei)
    - 支持 MemoryTracker 追踪 `IndexLookup` 算子的内存使用情况 [#45901](https://github.com/pingcap/tidb/issues/45901) @[solotzg](https://github.com/solotzg)
    - 支持 MemoryTracker 追踪 `MemTableReaderExec` 算子的内存使用情况 [#51456](https://github.com/pingcap/tidb/issues/51456) @[wshwsh12](https://github.com/wshwsh12)
    - 支持从 PD 批量加载 Region，加快在对大表进行查询时，从 KV Range 到 Regions 的转换过程 [#51326](https://github.com/pingcap/tidb/issues/51326) @[SeaRise](https://github.com/SeaRise)
    - 优化系统表 `INFORMATION_SCHEMA.TABLES`、`INFORMATION_SCHEMA.STATISTICS`、`INFORMATION_SCHEMA.KEY_COLUMN_USAGE`、`INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS` 的查询性能。相比之前版本，性能提升最高可达 100 倍 [#50305](https://github.com/pingcap/tidb/issues/50305) @[ywqzzy](https://github.com/ywqzzy)

+ TiKV

    - 增强 TSO 校验检测，提升配置或操作不当时集群 TSO 的鲁棒性 [#16545](https://github.com/tikv/tikv/issues/16545) @[cfzjywxk](https://github.com/cfzjywxk)
    - 优化清理悲观锁的逻辑，提高未提交事务的处理性能 [#16158](https://github.com/tikv/tikv/issues/16158) @[cfzjywxk](https://github.com/cfzjywxk)
    - 增加 TiKV 统一健康控制，降低单个 TiKV 节点异常对集群访问性能的影响。可通过 [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-从-v800-版本开始引入) 禁用该优化 [#16297](https://github.com/tikv/tikv/issues/16297) [#1104](https://github.com/tikv/client-go/issues/1104) [#1167](https://github.com/tikv/client-go/issues/1167) @[MyonKeminta](https://github.com/MyonKeminta) @[zyguan](https://github.com/zyguan) @[crazycs520](https://github.com/crazycs520)
    - PD client 使用元数据存储接口代替原有的全局配置接口 [#14484](https://github.com/tikv/tikv/issues/14484) @[HuSharp](https://github.com/HuSharp)
    - 通过 write cf stats 决定数据加载行为，以提升扫描性能 [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996)
    - 在 Raft conf change 过程中，增加了检查删除节点和 Voter 降级的最近一次心跳，确保此行为不会导致该 Region 不可访问 [#15799](https://github.com/tikv/tikv/issues/15799) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 为 Pipelined DML 增加 Flush 和 BufferBatchGet 接口 [#16291](https://github.com/tikv/tikv/issues/16291) @[ekexium](https://github.com/ekexium)
    - 增加 cgroup CPU 和内存限制的监控 [#16392](https://github.com/tikv/tikv/issues/16392) @[pingandb](https://github.com/pingandb)
    - 增加 Region worker 和快照生成 worker 的 CPU 监控 [#16562](https://github.com/tikv/tikv/issues/16562) @[Connor1996](https://github.com/Connor1996)
    - 增加 peer 和 store 消息的 slow log [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD

    - 增强 PD 客户端的服务发现能力，提升其高可用性和负载平衡 [#7576](https://github.com/tikv/pd/issues/7576) @[CabinfeverB](https://github.com/CabinfeverB)
    - 增强 PD 客户端的重试机制 [#7673](https://github.com/tikv/pd/issues/7673) @[JmPotato](https://github.com/JmPotato)
    - 增加 cgroup CPU 和内存的监控和告警 [#7716](https://github.com/tikv/pd/issues/7716) [#7918](https://github.com/tikv/pd/issues/7918) @[pingandb](https://github.com/pingandb) @[rleungx](https://github.com/rleungx)
    - 提升使用 etcd watch 的性能和高可用性 [#7738](https://github.com/tikv/pd/issues/7738) [#7724](https://github.com/tikv/pd/issues/7724) [#7689](https://github.com/tikv/pd/issues/7689) @[lhy1024](https://github.com/lhy1024)
    - 增加更多心跳监控，以便更好地分析性能瓶颈 [#7868](https://github.com/tikv/pd/issues/7868) @[nolouch](https://github.com/nolouch)
    - 减少 etcd leader 对 PD leader 的影响 [#7499](https://github.com/tikv/pd/issues/7499) @[JmPotato](https://github.com/JmPotato) @[HuSharp](https://github.com/HuSharp)
    - 增强对不健康的 etcd 节点的检测机制 [#7730](https://github.com/tikv/pd/issues/7730) @[JmPotato](https://github.com/JmPotato) @[HuSharp](https://github.com/HuSharp)
    - 优化 pd-ctl 中 GC safepoint 的相关显示 [#7767](https://github.com/tikv/pd/issues/7767) @[nolouch](https://github.com/nolouch)
    - 支持动态修改热点调度器中的历史窗口配置 [#7877](https://github.com/tikv/pd/issues/7877) @[lhy1024](https://github.com/lhy1024)
    - 减少创建 operator 中的锁争用问题 [#7837](https://github.com/tikv/pd/issues/7837) @[Leavrth](https://github.com/Leavrth)
    - 调整 GRPC 配置以提升可用性 [#7821](https://github.com/tikv/pd/issues/7821) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 支持 `JSON_EXTRACT()` 函数中的 `json_path` 参数为非常量 [#8510](https://github.com/pingcap/tiflash/issues/8510) @[SeaRise](https://github.com/SeaRise)
    - 支持 `JSON_LENGTH(json, path)` 函数 [#8711](https://github.com/pingcap/tiflash/issues/8711) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)

        - 支持通过 `br` 命令行工具新增的恢复参数 `--load-stats` 控制是否恢复统计信息  [#50568](https://github.com/pingcap/tidb/issues/50568) @[Leavrth](https://github.com/Leavrth)
        - 支持通过 `br` 命令行工具新增的恢复参数 `--tikv-max-restore-concurrency` 控制每个 TiKV 节点的最大 download 和 ingest 文件数量，并通过控制作业队列的最大长度，进而控制 BR 节点的内存消耗 [#51621](https://github.com/pingcap/tidb/issues/51621) @[3pointer](https://github.com/3pointer)
        - 粗粒度打散 Region 算法支持自适应获取并发参数，提升恢复性能 [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer)
        - 在 `br` 的命令行帮助信息中显示 `log` 命令 [#50927](https://github.com/pingcap/tidb/issues/50927) @[RidRisR](https://github.com/RidRisR)
        - 支持在恢复过程中提前分配好 Table ID，从而最大限度地复用 Table ID，提升恢复性能 [#51736](https://github.com/pingcap/tidb/issues/51736) @[Leavrth](https://github.com/Leavrth)
        - 使用 BR 时，禁用 TiDB 内部的 GC memory limit tuner 功能，避免 OOM 问题 [#51078](https://github.com/pingcap/tidb/issues/51078) @[Leavrth](https://github.com/Leavrth)
        - 使用更优的算法，提升数据恢复过程中 SST 文件合并的速度 [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - 支持在数据恢复过程中批量创建数据库 [#50767](https://github.com/pingcap/tidb/issues/50767) @[Leavrth](https://github.com/Leavrth)
        - 在日志备份过程中，增加了在日志和监控指标中打印影响 global checkpoint 推进的最慢的 Region 的信息 [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - 提升了 `RESTORE` 语句在大数据量表场景下的建表性能 [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 优化 `RowChangedEvent` 的内存占用，降低 TiCDC 同步数据时的内存消耗 [#10386](https://github.com/pingcap/tiflow/issues/10386) @[lidezhu](https://github.com/lidezhu)
        - 增加在创建和恢复 changefeed 任务时验证 `start-ts` 参数是否合法 [#10499](https://github.com/pingcap/tiflow/issues/10499) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - 在 MariaDB 主从复制的场景中，即 MariaDB 主实例 -> MariaDB 从实例 -> DM -> TiDB 的迁移场景，当 `gtid_strict_mode = off` 且 MariaDB 从实例的 GTID 不严格递增时（例如，有业务数据写入 MariaDB 从实例），此时 DM 任务会报错 `less than global checkpoint position`。从 v8.0.0 开始，TiDB 兼容该场景，数据可以正常迁移到下游。[#10741](https://github.com/pingcap/tiflow/issues/10741) @[okJiang](https://github.com/okJiang)

    + TiDB Lightning

        - 在逻辑导入模式下，支持使用 [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 配置批处理的最大行数 [#46607](https://github.com/pingcap/tidb/issues/46607) @[kennytm](https://github.com/kennytm)
        - 当 TiFlash 的导入空间不足时，TiDB Lightning 会报错 [#50324](https://github.com/pingcap/tidb/issues/50324) @[okJiang](https://github.com/okJiang)

## 错误修复

+ TiDB

    - 修复在无数据变更的情况下，`auto analyze` 被多次触发的问题 [#51775](https://github.com/pingcap/tidb/issues/51775) @[hi-rustin](https://github.com/hi-rustin)
    - 修复 `auto analyze` 并发设置错误的问题 [#51749](https://github.com/pingcap/tidb/issues/51749) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用单个 SQL 语句添加多个索引导致的索引不一致问题 [#51746](https://github.com/pingcap/tidb/issues/51746) @[tangenta](https://github.com/tangenta)
    - 修复查询使用 `NATURAL JOIN` 时可能报错 `Column ... in from clause is ambiguous` 的问题 [#32044](https://github.com/pingcap/tidb/issues/32044) @[AilinKid](https://github.com/AilinKid)
    - 修复 TiDB 错误地消除 `group by` 中的常量值导致查询结果出错的问题 [#38756](https://github.com/pingcap/tidb/issues/38756) @[hi-rustin](https://github.com/hi-rustin)
    - 修复 `LEADING` hint 在 `UNION ALL` 语句中无法生效的问题 [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `BIT` 类型的列在参与一些函数计算时，可能会因为 decode 失败导致查询出错的问题 [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - 修复通过 `tiup cluster upgrade/start` 方式进行滚动升级时，与 PD 交互出现问题可能导致 TiDB panic 的问题 [#50152](https://github.com/pingcap/tidb/issues/50152) @[zimulala](https://github.com/zimulala)
    - 修复执行包含 `ORDER BY` 的 `UNIQUE` 索引点查时可能报错的问题 [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - 修复常量传播在处理 `ENUM` 或 `SET` 类型时结果出错的问题 [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)
    - 修复包含 Apply 操作的查询在报错 `fatal error: concurrent map writes` 后导致 TiDB 崩溃的问题 [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - 修复使用 `SET_VAR` 控制字符串类型的变量可能会失效的问题 [#50507](https://github.com/pingcap/tidb/issues/50507) @[qw4990](https://github.com/qw4990)
    - 修复当 `tidb_sysdate_is_now` 设置为 `1` 时，`SYSDATE()` 函数错误地使用了计划缓存中的时间的问题 [#49299](https://github.com/pingcap/tidb/issues/49299) @[hawkingrei](https://github.com/hawkingrei)
    - 修复执行 `CREATE GLOBAL BINDING` 语句时，如果数据库名为大写，则绑定不生效的问题 [#50646](https://github.com/pingcap/tidb/issues/50646) @[qw4990](https://github.com/qw4990)
    - 修复 `Index Path` 选中重复索引的问题 [#50496](https://github.com/pingcap/tidb/issues/50496) @[AilinKid](https://github.com/AilinKid)
    - 修复当 `CREATE GLOBAL BINDING` 语句中包含 `IN()` 时，`PLAN REPLAYER` 无法加载绑定的问题 [#43192](https://github.com/pingcap/tidb/issues/43192) @[King-Dylan](https://github.com/King-Dylan)
    - 修复当多个 `analyze` 任务失败时，没有正确记录失败原因的问题 [#50481](https://github.com/pingcap/tidb/issues/50481) @[hi-rustin](https://github.com/hi-rustin)
    - 修复系统变量 `tidb_stats_load_sync_wait` 设置不生效的问题 [#50872](https://github.com/pingcap/tidb/issues/50872) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `max_execute_time` 多层设置相互影响的问题 [#50914](https://github.com/pingcap/tidb/issues/50914) @[jiyfhust](https://github.com/jiyfhust)
    - 修复并发更新统计信息导致的线程安全问题 [#50835](https://github.com/pingcap/tidb/issues/50835) @[hi-rustin](https://github.com/hi-rustin)
    - 修复对分区表执行 `auto analyze` 可能导致 TiDB panic 的问题 [#51187](https://github.com/pingcap/tidb/issues/51187) @[hi-rustin](https://github.com/hi-rustin)
    - 修复 SQL 语句中 `IN()` 谓词包含的值的个数不同时，可能导致 SQL 绑定不生效的问题 [#51222](https://github.com/pingcap/tidb/issues/51222) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 TiDB 无法正确转换表达式中系统变量类型的问题 [#43527](https://github.com/pingcap/tidb/issues/43527) @[hi-rustin](https://github.com/hi-rustin)
    - 修复在配置 `force-init-stats` 的情况下，TiDB 没有监听对应端口的问题 [#51473](https://github.com/pingcap/tidb/issues/51473) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在 `determinate` 模式下 (`tidb_opt_objective='determinate'`)，如果查询不包含谓词，可能无法加载统计信息的问题 [#48257](https://github.com/pingcap/tidb/issues/48257) @[time-and-fate](https://github.com/time-and-fate)
    - 修复 `init-stats` 流程可能导致 TiDB panic 以及 `load stats` 流程直接退出的问题 [#51581](https://github.com/pingcap/tidb/issues/51581) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `IN()` 谓词中包含 `NULL` 时，查询结果错误的问题 [#51560](https://github.com/pingcap/tidb/issues/51560) @[winoros](https://github.com/winoros)
    - 修复当 DDL 任务中包含多张表时，MDL View 中不显示 blocked DDL 的问题 [#47743](https://github.com/pingcap/tidb/issues/47743) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复表的 `ANALYZE` 任务统计的 `processed_rows` 可能超过表的总行数的问题 [#50632](https://github.com/pingcap/tidb/issues/50632) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当 `HashJoin` 算子落盘失败时 goroutine 可能泄露的问题 [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 CTE 查询使用的内存超限时可能会导致 goroutine 泄露的问题 [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复使用聚合函数分组计算时可能报错 `Can't find column ...` 的问题 [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990)
    - 修复当 `CREATE TABLE` 语句中包含特定分区或约束的表达式时，表名变更等 DDL 操作会卡住的问题 [#50972](https://github.com/pingcap/tidb/issues/50972) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 Grafana 监控指标 `tidb_statistics_auto_analyze_total` 没有显示为整数的问题 [#51051](https://github.com/pingcap/tidb/issues/51051) @[hawkingrei](https://github.com/hawkingrei)
    - 修复修改变量 `tidb_server_memory_limit` 后，`tidb_gogc_tuner_threshold` 未进行相应调整的问题 [#48180](https://github.com/pingcap/tidb/issues/48180) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当查询语句涉及 JOIN 操作时可能出现 `index out of range` 报错的问题 [#42588](https://github.com/pingcap/tidb/issues/42588) @[AilinKid](https://github.com/AilinKid)
    - 修复当列的默认值被删除时，获取该列的默认值会报错的问题 [#50043](https://github.com/pingcap/tidb/issues/50043) [#51324](https://github.com/pingcap/tidb/issues/51324) @[crazycs520](https://github.com/crazycs520)
    - 修复 TiFlash 延迟物化在处理关联列时结果可能出错的问题 [#49241](https://github.com/pingcap/tidb/issues/49241) [#51204](https://github.com/pingcap/tidb/issues/51204) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 `LIKE()` 函数在处理 binary collation 的输入时可能结果错误的问题 [#50393](https://github.com/pingcap/tidb/issues/50393) @[yibin87](https://github.com/yibin87)
    - 修复 `JSON_LENGTH()` 函数在第二个参数为 `NULL` 时结果错误的问题 [#50931](https://github.com/pingcap/tidb/issues/50931) @[SeaRise](https://github.com/SeaRise)
    - 修复 `CAST(AS DATETIME)` 在特定情况下可能会丢失时间精度的问题 [#49555](https://github.com/pingcap/tidb/issues/49555) @[SeaRise](https://github.com/SeaRise)
    - 修复并行 Apply 在表为聚簇索引时可能导致结果错误的问题 [#51372](https://github.com/pingcap/tidb/issues/51372) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复主键类型是 `VARCHAR` 时，执行 `ALTER TABLE ... COMPACT TIFLASH REPLICA` 可能会错误地提前结束的问题 [#51810](https://github.com/pingcap/tidb/issues/51810) @[breezewish](https://github.com/breezewish)
    - 修复 `EXCHANGE PARTITION` 语句交换分区表时，对 `DEFAULT NULL` 属性产生的 `NULL` 值检查有错误的问题 [#47167](https://github.com/pingcap/tidb/issues/47167) @[jiyfhust](https://github.com/jiyfhust)
    - 修复使用非 UTF8 字符集时，分区表定义可能导致错误行为的问题 [#49251](https://github.com/pingcap/tidb/issues/49251) @[YangKeao](https://github.com/YangKeao)
    - 修复一些系统变量的默认值在 `INFORMATION_SCHEMA.VARIABLES_INFO` 表中显示错误的问题 [#49461](https://github.com/pingcap/tidb/issues/49461) @[jiyfhust](https://github.com/jiyfhust)
    - 修复一些情况下使用了空字符串作为数据库名但没有报错的问题 [#45873](https://github.com/pingcap/tidb/issues/45873) @[yoshikipom](https://github.com/yoshikipom)
    - 修复 `SPLIT TABLE ... INDEX` 语句可能会导致 TiDB panic 的问题 [#50177](https://github.com/pingcap/tidb/issues/50177) @[Defined2014](https://github.com/Defined2014)
    - 修复查询 `KeyPartition` 类型的分区表可能会报错的问题 [#50206](https://github.com/pingcap/tidb/issues/50206) [#51313](https://github.com/pingcap/tidb/issues/51313) [#51196](https://github.com/pingcap/tidb/issues/51196) @[time-and-fate](https://github.com/time-and-fate) @[jiyfhust](https://github.com/jiyfhust) @[mjonss](https://github.com/mjonss)
    - 修复查询 Hash 分区类型的分区表时，结果可能不正确的问题 [#50427](https://github.com/pingcap/tidb/issues/50427) @[Defined2014](https://github.com/Defined2014)
    - 修复 opentracing 不能正常工作的问题 [#50508](https://github.com/pingcap/tidb/issues/50508) @[Defined2014](https://github.com/Defined2014)
    - 修复 `ALTER INSTANCE RELOAD TLS` 报错时，错误信息不完整的问题 [#50699](https://github.com/pingcap/tidb/issues/50699) @[dveeden](https://github.com/dveeden)
    - 修复 `AUTO_INCREMENT` 属性在分配自增 ID 时，由于不必要的事务冲突导致 ID 不连续的问题 [#50819](https://github.com/pingcap/tidb/issues/50819) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 TiDB 日志中某些报错的栈信息不完整的问题 [#50849](https://github.com/pingcap/tidb/issues/50849) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复当 `LIMIT` 子句中的数字过大时，一些查询的内存使用过大的问题 [#51188](https://github.com/pingcap/tidb/issues/51188) @[Defined2014](https://github.com/Defined2014)
    - 修复 TTL 功能在某些情况下因为没有正确切分数据范围而造成数据热点的问题 [#51527](https://github.com/pingcap/tidb/issues/51527) @[lcwangchao](https://github.com/lcwangchao)
    - 修复当 `SET` 语句出现在显式事务的第一行时不生效的问题 [#51387](https://github.com/pingcap/tidb/issues/51387) @[YangKeao](https://github.com/YangKeao)
    - 修复一些情况下查询 `BINARY` 类型的 JSON 可能会报错的问题 [#51547](https://github.com/pingcap/tidb/issues/51547) @[YangKeao](https://github.com/YangKeao)
    - 修复 TTL 在计算过期时间时，不能正确处理夏令时跳变的问题 [#51675](https://github.com/pingcap/tidb/issues/51675) @[lcwangchao](https://github.com/lcwangchao)
    - 修复某些情况下 `SHOW CREATE PLACEMENT POLICY` 语句不显示 `SURVIVAL_PREFERENCES` 属性的问题 [#51699](https://github.com/pingcap/tidb/issues/51699) @[lcwangchao](https://github.com/lcwangchao)
    - 修复当配置文件中出现不合规的配置项时，配置文件不生效的问题 [#51399](https://github.com/pingcap/tidb/issues/51399) @[Defined2014](https://github.com/Defined2014)

+ TiKV

    - 修复开启 `tidb_enable_row_level_checksum` 可能导致 TiKV panic 的问题 [#16371](https://github.com/tikv/tikv/issues/16371) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复休眠的 Region 在异常情况下未被及时唤醒的问题 [#16368](https://github.com/tikv/tikv/issues/16368) @[LykxSassinator](https://github.com/LykxSassinator)
    - 通过在执行下线节点操作前检查该 Region 所有副本的上一次心跳时间，修复下线一个副本导致整个 Region 不可用的问题 [#16465](https://github.com/tikv/tikv/issues/16465) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复 JSON 整型数值在大于 `INT64` 最大值但小于 `UINT64` 最大值时会被 TiKV 解析成 `FLOAT64` 导致结果和 TiDB 不一致的问题 [#16512](https://github.com/tikv/tikv/issues/16512) @[YangKeao](https://github.com/YangKeao)
    - 修复监控指标 `tikv_unified_read_pool_thread_count` 有时没有数据的问题 [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)

+ PD

    - 修复调用 `MergeLabels` 函数时存在数据竞争的问题 [#7535](https://github.com/tikv/pd/issues/7535) @[lhy1024](https://github.com/lhy1024)
    - 修复调用 `evict-leader-scheduler` 接口时没有输出结果的问题 [#7672](https://github.com/tikv/pd/issues/7672) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复 PD 监控项 `learner-peer-count` 在发生 Leader 切换后未同步旧监控值的问题 [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复 `watch etcd` 没有正确关闭导致内存泄露的问题 [#7807](https://github.com/tikv/pd/issues/7807) @[rleungx](https://github.com/rleungx)
    - 修复 TSO 部分日志没有打印报错原因的问题 [#7496](https://github.com/tikv/pd/issues/7496) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复重启后 PD 部分监控出现非预期负数的问题 [#4489](https://github.com/tikv/pd/issues/4489) @[lhy1024](https://github.com/lhy1024)
    - 修复 Leader 租约的过期时间晚于日志时间的问题 [#7700](https://github.com/tikv/pd/issues/7700) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复在 TiDB（PD 客户端）和 PD 之间的 TLS 开关不一致时，TiDB panic 的问题 [#7900](https://github.com/tikv/pd/issues/7900) [#7902](https://github.com/tikv/pd/issues/7902) [#7916](https://github.com/tikv/pd/issues/7916) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复 Goroutine 由于没有正确关闭而泄露的问题 [#7782](https://github.com/tikv/pd/issues/7782) @[HuSharp](https://github.com/HuSharp)
    - 修复 pd-ctl 无法移除包含特殊字符的调度器的问题 [#7798](https://github.com/tikv/pd/issues/7798) @[JmPotato](https://github.com/JmPotato)
    - 修复 PD 客户端获取 TSO 可能被阻塞的问题 [#7864](https://github.com/tikv/pd/issues/7864) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiFlash

    - 修复副本迁移时，因 TiFlash 与 PD 之间网络连接不稳定可能引发的 TiFlash panic 的问题 [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复慢查询导致内存使用显著增加的问题 [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - 修复移除 TiFlash 副本后重新添加可能导致 TiFlash 数据损坏的问题 [#8695](https://github.com/pingcap/tiflash/issues/8695) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在执行 PITR 恢复任务或 `FLASHBACK CLUSTER TO` 后，TiFlash 副本数据可能被意外删除，导致数据异常的问题 [#8777](https://github.com/pingcap/tiflash/issues/8777) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在执行 `ALTER TABLE ... MODIFY COLUMN ... NOT NULL` 时，将原本可为空的列修改为不可为空之后，导致 TiFlash panic 的问题 [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复存算分离架构下，出现网络隔离后查询可能会被永久阻塞的问题 [#8806](https://github.com/pingcap/tiflash/issues/8806) @[JinheLin](https://github.com/JinheLin)
    - 修复存算分离架构下，TiFlash 关闭过程中可能 panic 的问题 [#8837](https://github.com/pingcap/tiflash/issues/8837) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 在发生远程读时可能会因为数据竞争导致 crash 的问题 [#8685](https://github.com/pingcap/tiflash/issues/8685) @[solotzg](https://github.com/solotzg)
    - 修复 `CAST(AS JSON)` 函数中没有对 JSON object key 去重的问题 [#8712](https://github.com/pingcap/tiflash/issues/8712) @[SeaRise](https://github.com/SeaRise)
    - 修复 `ENUM` 列在 chunk encode 时可能会导致 TiFlash crash 的问题 [#8674](https://github.com/pingcap/tiflash/issues/8674) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR)

        - 修复在 Region 成为 Leader 后立刻分裂或合并，导致日志备份 Checkpoint 不推进的问题 [#16469](https://github.com/tikv/tikv/issues/16469) @[YuJuncen](https://github.com/YuJuncen)
        - 修复在某些极端情况下，全量备份因找不到 peer 导致 TiKV panic 的问题 [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)
        - 修复在同一节点上更改 TiKV IP 地址导致日志备份卡住的问题 [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)
        - 修复从 S3 读文件内容时出错后无法重试的问题 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)
        - 修复数据恢复失败后，使用断点重启报错 `the target cluster is not fresh` 的问题 [#50232](https://github.com/pingcap/tidb/issues/50232) @[Leavrth](https://github.com/Leavrth)
        - 修复停止日志备份任务导致 TiDB crash 的问题 [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - 修复由于某个 TiKV 节点缺少 Leader 导致数据恢复变慢的问题 [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - 修复全量恢复指定 `--filter` 选项后，仍然要求目标集群为空的问题 [#51009](https://github.com/pingcap/tidb/issues/51009) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 修复使用 storage sink 时，在存储服务生成的文件序号可能出现回退的问题 [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复并发创建多个 changefeed 时 TiCDC 返回 `ErrChangeFeedAlreadyExists` 错误的问题 [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在 `ignore-event` 中设置了过滤掉 `add table partition` 事件后，TiCDC 未将相关分区的其它类型 DML 变更事件同步到下游的问题 [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复上游表执行了 `TRUNCATE PARTITION` 后 changefeed 报错的问题 [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - 修复恢复 changefeed 时 changefeed 的 `checkpoint-ts` 小于 TiDB 的 GC safepoint，没有及时报错 `snapshot lost caused by GC` 的问题 [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - 修复 TiCDC 在开启单行数据正确性校验后由于时区不匹配导致 `TIMESTAMP` 类型 checksum 验证失败的问题 [#10573](https://github.com/pingcap/tiflow/issues/10573) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 Syncpoint 表可能被错误同步的问题 [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - 修复当使用 Apache Pulsar 作为下游时，无法正常启用 OAuth2.0、TLS 和 mTLS 的问题 [#10602](https://github.com/pingcap/tiflow/issues/10602) @[asddongmen](https://github.com/asddongmen)
        - 修复当 TiKV 升级、重启或驱逐 Leader 时，changefeed 可能卡住的问题 [#10584](https://github.com/pingcap/tiflow/issues/10584) @[asddongmen](https://github.com/asddongmen)
        - 修复在频繁执行 DDL 的场景中，由于错误的 BarrierTS 导致数据被写入到错误的 CSV 文件的问题 [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        - 修复 KV Client 数据争用导致 TiCDC panic 的问题 [#10718](https://github.com/pingcap/tiflow/issues/10718) @[asddongmen](https://github.com/asddongmen)
        - 修复在调度表的同步任务时 TiCDC panic 的问题 [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - 修复上游为 binary 类型主键时丢失数据的问题 [#10672](https://github.com/pingcap/tiflow/issues/10672) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - 修复检查 TiKV 空间导致的性能回退的问题 [#43636](https://github.com/pingcap/tidb/issues/43636) @[lance6716](https://github.com/lance6716)
        - 修复在扫描数据文件时，遇到不合法符号链接文件而报错的问题 [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)
        - 修复当 `sql_mode` 中不包含 `NO_ZERO_IN_DATE` 时，TiDB Lightning 无法正确解析包含 `0` 的日期值的问题 [#50757](https://github.com/pingcap/tidb/issues/50757) @[GMHDBJD](https://github.com/GMHDBJD)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [Aoang](https://github.com/Aoang)
- [bufferflies](https://github.com/bufferflies)
- [daemon365](https://github.com/daemon365)
- [eltociear](https://github.com/eltociear)
- [lichunzhu](https://github.com/lichunzhu)
- [jiyfhust](https://github.com/jiyfhust)
- [pingandb](https://github.com/pingandb)
- [shenqidebaozi](https://github.com/shenqidebaozi)
- [Smityz](https://github.com/Smityz)
- [songzhibin97](https://github.com/songzhibin97)
- [tangjingyu97](https://github.com/tangjingyu97)
- [Tema](https://github.com/Tema)
- [ub-3](https://github.com/ub-3)
- [yoshikipom](https://github.com/yoshikipom)
