---
title: TiDB 6.6.0 Release Notes
summary: 了解 TiDB 6.6.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.6.0 Release Notes

发版日期：2023 年 2 月 20 日

TiDB 版本：6.6.0-[DMR](/releases/versioning.md#开发里程碑版本)

> **注意：**
>
> TiDB 6.6.0-DMR 的用户文档已[归档](https://docs-archive.pingcap.com/zh/tidb/v6.6)。如无特殊需求，建议使用 TiDB 数据库的[最新 LTS 版本](https://docs.pingcap.com/zh/tidb/stable)。

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.6/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.6.0-DMR#version-list)

在 6.6.0 版本中，你可以获得以下关键特性：

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
    <td rowspan="3">可扩展性与性能<br /></td>
      <td>TiKV 支持 <a href="https://docs.pingcap.com/zh/tidb/v6.6/partitioned-raft-kv" target="_blank">Partitioned Raft KV 存储引擎</a>（实验特性）</td>
      <td>TiKV 引入下一代存储引擎 Partitioned Raft KV，通过每个数据 Region 独享 RocksDB 实例，可将集群的存储能力从 TB 级扩展到 PB 级，并提供更稳定的写入延迟和更强大的扩容能力。</td>
  </tr>
  <tr>
      <td>TiKV 支持<a href="https://docs.pingcap.com/zh/tidb/v6.6/system-variables#tidb_store_batch_size" target="_blank">批量聚合数据请求</a></td>
      <td>TiDB 支持将发送到相同 TiKV 实例的数据请求部分合并，减少子任务的数量和 RPC 请求的开销。在数据离散分布且 gRPC 线程池资源紧张的情况下，批量化请求能够提升性能超 50%。</td>
  </tr>
  <tr>
    <td>TiFlash 支持 <a href="https://docs.pingcap.com/zh/tidb/v6.6/stale-read" target="_blank">Stale Read</a> 和<a href="https://docs.pingcap.com/zh/tidb/v6.6/explain-mpp#mpp-version-和-exchange-数据压缩" target="_blank">压缩数据交换</a></td>
    <td>TiFlash 支持 Stale Read 功能，在非实时性要求的场景可提升查询性能。TiFlash 默认支持带压缩的数据交换，可提升并行处理的数据交换效率，TPC-H 总体性能提升约 10%，流量节省超 50%。</td>
  </tr>
  <tr>
    <td rowspan="2">稳定性与高可用<br /></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v6.6/tidb-resource-control" target="_blank">资源管控</a>（实验特性）</td>
    <td>引入资源管控框架，支持将资源配额映射到用户定义的资源组，在集群资源发生争用时，对资源组内用户的资源使用进行限制。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v6.6/sql-plan-management#根据历史执行计划创建绑定" target="_blank">绑定历史执行计划</a></td>
    <td>支持绑定历史执行计划，支持通过 TiDB Dashboard 快速绑定执行计划。</td>
  </tr>
  <tr>
    <td rowspan="2">功能特性与兼容性<br /></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v6.6/foreign-key" target="_blank">外键约束</a>（实验特性）</td>
    <td>支持 MySQL 兼容的外键约束，帮助保持数据一致性和提升数据质量。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v6.6/sql-statement-create-index/#多值索引" target="_blank">多值索引</a>（实验特性）</td>
    <td>引入 MySQL 兼容的多值索引，增强 JSON 类型，提升 TiDB 对 MySQL 8.0 的兼容性。</td>
  </tr>
  <tr>
    <td>数据库管理与可观测性<br /></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v6.6/dm-precheck/#physical-import-检查项" target="_blank">DM 集成物理导入模式</a>（实验特性）</td>
    <td>TiDB Data Migration (DM) 集成 TiDB Lightning 的物理导入模式模式，提升 DM 全量数据迁移时的性能，大数据量场景下的迁移时间最多可提升 10 倍。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* 支持下一代 Partitioned Raft KV 存储引擎（实验特性）[#11515](https://github.com/tikv/tikv/issues/11515) [#12842](https://github.com/tikv/tikv/issues/12842) @[busyjay](https://github.com/busyjay) @[tonyxuqqi](https://github.com/tonyxuqqi) @[tabokie](https://github.com/tabokie) @[bufferflies](https://github.com/bufferflies) @[5kbpers](https://github.com/5kbpers) @[SpadeA-Tang](https://github.com/SpadeA-Tang) @[nolouch](https://github.com/nolouch)

    TiDB v6.6.0 之前，TiKV 基于 Raft 的存储引擎使用一个单一的 RocksDB 实例存储该 TiKV 实例所有 Region 的数据。为了更平稳地支持更大的集群，从 TiDB v6.6.0 开始，引入了一个全新的 TiKV 存储引擎，该引擎使用多个 RocksDB 实例来存储 TiKV 的 Region 数据，每个 Region 的数据都独立存储在单独的 RocksDB 实例中。新引擎能够更好地控制 RocksDB 实例的文件数和层级，并实现 Region 间数据操作的物理隔离，避免互相影响，还支持平稳管理更多的数据。可以理解为 TiKV 通过分区管理多个 RocksDB 实例，这也是该特性 Partitioned Raft KV 名字的由来。该功能的主要优势在于更好的写入性能，更快的扩缩容，相同硬件下可以支持更大的数据，也能支持更大的集群规模。

    该功能目前是实验特性，不推荐在生产环境中使用。

    更多信息，请参考[用户文档](/partitioned-raft-kv.md)。

* 支持 DDL 分布式并行执行框架（实验特性）[#37125](https://github.com/pingcap/tidb/issues/37125) @[zimulala](https://github.com/zimulala)

    在过去的版本中，整个 TiDB 集群中仅允许一个 TiDB 实例作为 DDL Owner 处理 Schema 变更任务。为了进一步提升 DDL 的并发性，TiDB v6.6.0 版本引入了 DDL 分布式并行执行框架，支持集群中所有的 TiDB 实例并发执行同一个任务的 `StateWriteReorganization` 阶段，加速 DDL 的执行。该功能由系统变量 [`tidb_ddl_distribute_reorg`](https://docs.pingcap.com/zh/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-从-v660-版本开始引入) 控制是否开启，目前只支持 `Add Index` 操作。

### 性能

* 支持悲观锁队列的稳定唤醒模型 [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta)

    如果业务场景存在单点悲观锁冲突频繁的情况，原有的唤醒机制无法保证事务获取锁的时间，造成长尾延迟高，甚至获取锁超时。自 v6.6.0 起，你可以通过设置系统变量 [`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/zh/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) 为 `ON` 开启悲观锁的稳定唤醒模型。在该唤醒模型下，队列的唤醒顺序可被严格控制，避免无效唤醒造成的资源浪费。在锁冲突严重的场景中，能够减少长尾延时，降低 P99 响应时间。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5)。

* 批量聚合数据请求 [#39361](https://github.com/pingcap/tidb/issues/39361) @[cfzjywxk](https://github.com/cfzjywxk) @[you06](https://github.com/you06)

    TiDB 向 TiKV 发送数据请求时，会根据数据所在的 Region 将请求编入不同的子任务，每个子任务只处理单个 Region 的请求。当访问的数据离散度很高时，即使数据量不大，也会生成众多的子任务，进而产生大量 RPC 请求，消耗额外的时间。自 v6.6.0 起，TiDB 支持将发送到相同 TiKV 实例的数据请求部分合并，减少子任务的数量和 RPC 请求的开销。在数据离散度高且 gRPC 线程池资源紧张的情况下，批量化请求能够将性能提升 50% 以上。

    此特性默认打开，可通过系统变量 [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) 设置批量请求的大小。

* 解除执行计划缓存对 `LIMIT` 子句的限制 [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678)

    TiDB v6.6.0 移除了执行计划缓存的限制，带有变量的 `LIMIT` 子句可以进入执行计划缓存，如 `LIMIT ?` 或者 `LIMIT 10, ?`。这使得更多的 SQL 能够从计划缓存中获益，提升执行效率。目前出于安全考虑，仅支持缓存 `?` 参数值不大于 10000 的执行计划。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* TiFlash 引擎支持带压缩的数据交换 [#6620](https://github.com/pingcap/tiflash/issues/6620) @[solotzg](https://github.com/solotzg)

    为了协同多节点进行计算，TiFlash 引擎需要在不同节点中进行数据交换。当需要交换的数据量非常大时，数据交换的性能可能影响整体计算效率。在 v6.6.0 版本中，TiFlash 引擎引入压缩机制，在必要时对需要交换的数据进行压缩，然后进行交换，从而提升数据交换效率。

    更多信息，请参考[用户文档](/explain-mpp.md#mpp-version-和-exchange-数据压缩)。

* TiFlash 支持 Stale Read 功能 [#4483](https://github.com/pingcap/tiflash/issues/4483) @[hehechen](https://github.com/hehechen)

    Stale Read 功能是从 TiDB v5.1.1 开始正式引入的，支持读取指定时间点或时间范围内的历史数据。Stale Read 允许直接读取 TiKV 本地副本数据，可以降低读取延迟，提升查询性能。在 v6.6.0 之前的版本中，TiFlash 并不支持 Stale Read 功能，即使 Stale Read 查询的表包含 TiFlash 副本，TiDB 也只能使用 TiKV 副本进行查询。

    在 v6.6.0 中，TiFlash 开始支持 Stale Read 功能。当使用 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 语法或 [`tidb_read_staleness`](/tidb-read-staleness.md) 系统变量等方式查询历史数据时，如果查询的表包含 TiFlash 副本，优化器可以选择 TiFlash 副本读取对应的数据，从而进一步提高查询性能。

    更多信息，请参考[用户文档](/stale-read.md)。

* 支持下推字符串函数 `regexp_replace` 至 TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008)

### 稳定性

* 支持基于资源组的资源管控（实验特性）[#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    你可以为 TiDB 集群创建资源组，将不同的数据库用户映射到对应的资源组中，根据需要设置每个资源组的配额。当集群资源紧张时，来自同一个资源组的会话所使用的全部资源将被限制在配额内，避免其中一个资源组过度消耗，从而影响其他资源组中的会话正常运行。TiDB 在 Grafana 上提供了内置视图展示资源的实际使用情况，协助你更合理地配置资源。

    资源管控特性的引入对 TiDB 具有里程碑的意义。它能够将一个分布式数据库集群划分成多个逻辑单元，即使个别单元对资源过度使用，也不会挤占其他单元所需的资源。利用该特性：

    - 你可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载提升，不会影响其他应用的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。
    - 你可以选择将所有测试环境合入一个集群，或者将消耗较大的批量任务编入一个单独的资源组，在保证重要应用获得必要资源的同时，提升硬件利用率，降低运行成本。

  此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

  在 v6.6.0 中，启用资源管控特性需要同时打开 TiDB 的全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 及 TiKV 的配置项 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)。当前支持的限额方式基于“[用量](/tidb-resource-control.md#什么是-request-unit-ru)”（Request Unit，即 RU），RU 是 TiDB 对 CPU、I/O 等系统资源的统一抽象单位。

  更多信息，请参考[用户文档](/tidb-resource-control.md)。

* 绑定历史执行计划 GA [#39199](https://github.com/pingcap/tidb/issues/39199) @[fzzf678](https://github.com/fzzf678)

    在 v6.5.0 中，TiDB 扩展了 [`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md) 语句中的绑定对象，支持根据历史执行计划创建绑定。在 v6.6.0 中该功能 GA，执行计划的选择不仅限于当前 TiDB 节点，任意 TiDB 节点产生的历史执行计划都可以被选为 [SQL Binding](/sql-statements/sql-statement-create-binding.md) 的目标，进一步提升了功能的易用性。

    更多信息，请参考[用户文档](/sql-plan-management.md#根据历史执行计划创建绑定)。

* 新增若干优化器 Hint [#39964](https://github.com/pingcap/tidb/issues/39964) @[Reminiscent](https://github.com/Reminiscent)

    TiDB 在 v6.6.0 中增加了若干优化器 Hint，用来控制 `LIMIT` 操作的执行计划选择：

    - [`ORDER_INDEX()`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-)：提示优化器使用指定的索引，读取数据时保持索引的顺序，生成类似 `Limit + IndexScan(keep order: true)` 的计划。
    - [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-)：提示优化器使用指定的索引，读取数据时不保持顺序，生成类似 `TopN + IndexScan(keep order: false)` 的计划。

  持续引入优化器 Hint 为用户提供了更多的干预手段，有助于解决 SQL 性能问题，并提升了整体性能的稳定性。

* 支持 DDL 动态资源管控（实验特性）[#38025](https://github.com/pingcap/tidb/issues/38025) @[hawkingrei](https://github.com/hawkingrei)

    TiDB v6.6.0 版本引入了 DDL 动态资源管控，通过自动控制 DDL 的 CPU 使用量，尽量降低 DDL 变更任务对线上业务的影响。该功能仅在开启 [DDL 分布式并行执行框架](https://docs.pingcap.com/zh/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-从-v660-版本开始引入)后生效。

### 高可用

* [Placement Rules in SQL](/placement-rules-in-sql.md) 支持指定 `SURVIVAL_PREFERENCE` [#38605](https://github.com/pingcap/tidb/issues/38605) @[nolouch](https://github.com/nolouch)

    `SURVIVAL_PREFERENCES` 为数据提供了生存偏好设置，从而提高数据的容灾生存能力。通过指定 `SURVIVAL_PREFERENCE`，你可以控制：

    - 对于跨云区域部署的 TiDB 集群，当某个云区域产生故障时，指定数据库或表能在另一个云区域继续提供服务。
    - 对于单个云区域内部署的 TiDB 集群，当某个可用区产生故障时，指定数据库或表能在另一个可用区继续提供服务。

  更多信息，请参考[用户文档](/placement-rules-in-sql.md#指定生存偏好)。

* 支持通过 `FLASHBACK CLUSTER TO TIMESTAMP` 命令闪回 DDL 操作 [#14045](https://github.com/tikv/tikv/issues/14045) @[Defined2014](https://github.com/Defined2014) @[JmPotato](https://github.com/JmPotato)

    [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md) 语句支持在 Garbage Collection (GC) life time 内快速回退整个集群到指定的时间点。在 TiDB v6.6.0 版本中，该功能新支持撤销 DDL 操作，适用于快速撤消集群的 DML 或 DDL 误操作、支持分钟级别的快速回退集群、支持在时间线上多次回退以确定特定数据更改发生的时间。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-flashback-cluster.md)。

### SQL 功能

* 支持兼容 MySQL 语法的外键约束（实验特性）[#18209](https://github.com/pingcap/tidb/issues/18209) @[crazycs520](https://github.com/crazycs520)

    TiDB v6.6.0 引入了兼容 MySQL 语法的外键约束功能，支持在表内、表间关联数据并进行约束校验，并且支持级联操作。该特性有助于将 MySQL 上的应用迁移到 TiDB、保持数据一致性、提升数据质量并且方便数据建模。

    更多信息，请参考[用户文档](/foreign-key.md)。

* 支持 MySQL 兼容的多值索引 (Multi-Valued Indexes)（实验特性）[#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990)

    TiDB 在 v6.6.0 引入了 MySQL 兼容的多值索引 (Multi-Valued Indexes)。过滤 JSON 列中某个数组的值是常见的操作，但普通索引对这类操作起不到加速作用。在数组上创建多值索引能够大幅提升过滤的性能。如果 JSON 列中的某个数组上存在多值索引，那么可以利用多值索引过滤带有 `MEMBER OF()`、`JSON_CONTAINS()`、`JSON_OVERLAPS()` 函数的检索条件，从而减少大量的 I/O 消耗，提升运行速度。

    多值索引的引入，进一步增强了 TiDB 对 JSON 类型的支持，同时也提升了 TiDB 对 MySQL 8.0 的兼容性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

### 数据库管理

* 支持配置只读存储节点来执行资源消耗型任务 @[v01dstar](https://github.com/v01dstar)

    在生产环境中，可能有部分只读操作定期消耗大量资源，对整个集群的性能产生影响，比如备份和大规模数据读取分析等。TiDB v6.6.0 支持配置只读存储节点，用来执行重度资源消耗的只读任务，避免对线上业务的影响。目前支持 TiDB、TiSpark 和 BR 读取只读节点上的数据。你可以按照[操作步骤](/best-practices/readonly-nodes.md#操作步骤)配置只读存储节点，并通过 TiDB 系统变量 `tidb_replica_read`、TiSpark 配置项 `spark.tispark.replica_read` 或 br 命令行参数 `--replica-read-label` 指定数据读取位置，以保证集群性能稳定。

    更多信息，请参考[用户文档](/best-practices/readonly-nodes.md)。

* 支持动态修改参数 `store-io-pool-size` [#13964](https://github.com/tikv/tikv/issues/13964) @[LykxSassinator](https://github.com/LykxSassinator)

    TiKV 中的 [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-从-v530-版本开始引入) 用于设定处理 Raft I/O 任务的线程池中线程的数量，需要在 TiKV 性能调优时进行调整。在 v6.6.0 之前，这个参数无法动态修改。v6.6.0 支持动态修改该参数，提高了 TiKV 性能调优的灵活性。

    更多信息，请参考[用户文档](/dynamic-config.md)。

* 支持指定集群初次启动时的初始化 SQL 脚本 [#35624](https://github.com/pingcap/tidb/issues/35624) @[morgo](https://github.com/morgo)

    TiDB 集群初次启动时，可通过命令行参数 `--initialize-sql-file` 指定执行的 SQL 脚本。该功能可用于修改系统变量的值、创建用户或分配权限等。

    更多信息，请参考[用户文档](/tidb-configuration-file.md#initialize-sql-file-从-v660-版本开始引入)。

- TiDB Data Migration (DM) 集成了 TiDB Lightning 的物理导入模式（实验特性）@[lance6716](https://github.com/lance6716)

    在 v6.6.0 版本中，DM 的全量迁移能力集成了 TiDB Lightning 的物理导入模式，使得 DM 全量数据迁移的性能最高可提升 10 倍，大大缩短了大数据量场景下的迁移时间。在 v6.6.0 以前，数据量较多的场景下，需要单独配置 TiDB Lightning 的物理导入模式任务来进行快速的全量数据迁移，再用 DM 来进行增量数据迁移，配置较为复杂。从 v6.6.0 起，在迁移大数据量的场景，无需再配置 TiDB Lightning 的任务，使用一个 DM 任务即可完成。

    更多信息，请参考[用户文档](/dm/dm-precheck.md#physical-import-检查项)。

- TiDB Lightning 新增配置文件参数 `"header-schema-match"` 用于解决源文件里的列名和目标表的列名不匹配的问题 @[dsdashun](https://github.com/dsdashun)

    在 v6.6.0 版本中，TiDB Lightning 新增配置文件参数 `"header-schema-match"`，默认取值为 `true`，表示源 CSV 文件第一行有表的列名信息，且和目标表列名保持一致。如果 CSV 表头中的字段名和目标表的列名不匹配，此时可以将该配置设置为 `false`，TiDB Lightning 将忽略不匹配的问题，继续按目标表中的列顺序导入数据。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)。

- TiDB Lightning 向 TiKV 传输键值对时支持启用压缩传输 [#41163](https://github.com/pingcap/tidb/issues/41163) @[sleepymole](https://github.com/sleepymole)

    自 v6.6.0 起，TiDB Lightning 支持将本地编码排序后的键值对在网络传输时进行压缩再发送到 TiKV，从而减少网络传输的数据量，降低网络带宽开销。之前版本不支持该功能，在数据量较大的情况下，TiDB Lightning 对网络带宽要求相对较高，且会产生较高的流量费。

    该功能默认关闭，你可以通过将 TiDB Lightning 配置项 `compress-kv-pairs` 设置为 `"gzip"` 或者 `"gz"` 开启此功能。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)。

- TiKV-CDC 工具 GA，支持订阅 RawKV 的数据变更 [#48](https://github.com/tikv/migration/issues/48) @[zeminzhou](https://github.com/zeminzhou) @[haojinming](https://github.com/haojinming) @[pingyu](https://github.com/pingyu)

    TiKV-CDC 是一个 TiKV 集群的 CDC (Change Data Capture) 工具。TiKV 可以独立于 TiDB，与 PD 构成 KV 数据库，此时的产品形态为 RawKV。TiKV-CDC 支持订阅 RawKV 的数据变更，并实时同步到下游 TiKV 集群，从而实现 RawKV 的跨集群复制。

    更多信息，请参考[用户文档](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc-cn/)。

- TiCDC 支持在 Kafka 同步任务上开启单表的横向扩展功能，将单表的同步任务下发到多个 TiCDC 节点上执行（实验特性）[#7720](https://github.com/pingcap/tiflow/issues/7720) @[overvenus](https://github.com/overvenus)

    在 v6.6.0 之前，当上游单表写入量较大时，单表的复制能力无法横向扩展导致同步延迟增加。自 TiCDC v6.6.0 起，下游为 Kafka 的同步任务可以将上游单表的同步任务下发到多个 TiCDC 节点上执行，实现单表同步性能的横向扩展。

    更多信息，请参考[用户文档](/ticdc/ticdc-sink-to-kafka.md#横向扩展大单表的负载到多个-ticdc-节点)。

- [GORM](https://github.com/go-gorm/gorm) 已添加 TiDB 集成测试。目前 TiDB 已成为 GORM 默认支持的数据库 [#6014](https://github.com/go-gorm/gorm/pull/6014) @[Icemap](https://github.com/Icemap)

    - [GORM MySQL driver](https://github.com/go-gorm/mysql) 在 `v1.4.6` 中，新增 TiDB `AUTO_RANDOM` 特性适配 [#104](https://github.com/go-gorm/mysql/pull/104)
    - [GORM MySQL driver](https://github.com/go-gorm/mysql) 在 `v1.4.6` 中，修复了连接 TiDB 时，在 `AutoMigrate` 期间无法更改 `Unique` 字段的非 `Unique` 属性的问题 [#105](https://github.com/go-gorm/mysql/pull/105)
    - [GORM 文档](https://github.com/go-gorm/gorm.io)提及 TiDB 作为默认数据库 [#638](https://github.com/go-gorm/gorm.io/pull/638)

  更多信息，请参考 [GORM 用户文档](https://gorm.io/docs/index.html)。

### 可观测性

* 支持在 TiDB Dashboard 中快速绑定执行计划 [#781](https://github.com/pingcap/tidb-dashboard/issues/781) @[YiniXu9506](https://github.com/YiniXu9506)

    TiDB v6.6.0 中引入了执行计划快速绑定功能，你可以在 TiDB Dashboard 中快速完成 SQL 语句与特定计划的绑定。

    通过提供友好的界面，简化了在 TiDB Dashboard 上绑定 SQL 执行计划的过程，提高绑定过程的效率和用户体验。

    更多信息，请参考[用户文档](/dashboard/dashboard-statement-details.md#快速绑定执行计划)。

* 为执行计划缓存增加告警 @[qw4990](https://github.com/qw4990)

    当执行计划无法被缓存时，TiDB 会通过告警的方式提示该计划无法被缓存的原因，降低诊断的难度。例如：

    ```sql
    mysql> PREPARE st FROM 'SELECT * FROM t WHERE a<?';
    Query OK, 0 rows affected (0.00 sec)

    mysql> SET @a='1';
    Query OK, 0 rows affected (0.00 sec)

    mysql> EXECUTE st USING @a;
    Empty set, 1 warning (0.01 sec)

    mysql> SHOW WARNINGS;
    +---------+------+----------------------------------------------+
    | Level   | Code | Message                                      |
    +---------+------+----------------------------------------------+
    | Warning | 1105 | skip plan-cache: '1' may be converted to INT |
    +---------+------+----------------------------------------------+
    ```

    在以上例子中，优化器进行了非 INT 类型到 INT 类型的转换，产生的执行计划可能随着参数变化而存在风险，因此 TiDB 不缓存该计划。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md#诊断-prepared-plan-cache)。

* 在慢查询中增加告警字段 [#39893](https://github.com/pingcap/tidb/issues/39893) @[time-and-fate](https://github.com/time-and-fate)

    TiDB v6.6.0 慢查询日志中新增了 `Warnings` 字段，以帮助诊断查询性能问题。该字段以 JSON 格式记录慢查询语句在执行过程中产生的警告信息。你也可以在 TiDB Dashboard 的慢查询页面中查看 Warnings 信息。

    更多信息，请参考[用户文档](/identify-slow-queries.md)。

* 自动捕获执行计划的生成 [#38779](https://github.com/pingcap/tidb/issues/38779) @[Yisaer](https://github.com/Yisaer)

    在执行计划问题的排查过程中，`PLAN REPLAYER` 能够协助保存现场，提升诊断的效率。但在个别场景中，一些执行计划的生成无法任意重现，给诊断工作增加了难度。

    针对这类场景，在 TiDB v6.6.0 中，`PLAN REPLAYER` 扩展了自动捕获的能力。通过 `PLAN REPLAYER CAPTURE` 命令，你可以提前注册目标 SQL 语句，也可以同时指定目标执行计划。当 TiDB 检测到执行的 SQL 语句或执行计划与注册目标匹配时，会自动生成并打包 `PLAN REPLAYER` 的信息，提升执行计划不稳定时的诊断效率。

    要启用该功能，需要将系统变量 [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) 的值设为 `ON`。

    更多信息，请参考[用户文档](/sql-plan-replayer.md#使用-plan-replayer-capture-抓取目标计划)。

* 持久化 statements summary（实验特性）[#40812](https://github.com/pingcap/tidb/issues/40812) @[mornyx](https://github.com/mornyx)

    在 TiDB v6.6.0 之前的版本中，statements summary 数据维护在内存中，一旦 TiDB 发生重启，数据便会全部丢失。开启 statements summary 持久化特性后，历史数据将定期被写入磁盘，相关系统表的查询数据源也将由内存变为磁盘。此时，TiDB 重启后，历史数据仍然会保留。

    更多信息，请参考[用户文档](/statement-summary-tables.md#持久化-statements-summary)。

### 安全

* TiFlash 支持 TLS 证书自动轮换 [#5503](https://github.com/pingcap/tiflash/issues/5503) @[ywqzzy](https://github.com/ywqzzy)

    TiDB v6.6.0 引入了 TiFlash TLS 证书自动轮换功能。在开启组件间加密传输的 TiDB 集群上，当 TiFlash 的 TLS 证书过期需要重新签发时，支持自动加载新的 TiFlash TLS 证书，无需重启 TiDB 集群。而且，TiDB 集群内部组件之间 TLS 过期轮换不影响 TiDB 集群的正常使用，保障了 TiDB 集群的高可用。

    更多信息，请参考[用户文档](/enable-tls-between-components.md)。

* TiDB Lightning 支持通过 AWS IAM 角色的密钥以及会话令牌来访问 S3 数据 [#40750](https://github.com/pingcap/tidb/issues/40750) @[okJiang](https://github.com/okJiang)

    在 v6.6.0 之前，TiDB Lightning 仅支持通过 AWS IAM **用户密钥**访问 S3 的数据，无法使用临时会话令牌。自 v6.6.0 起，TiDB Lightning 支持通过 AWS IAM **角色密钥 + 会话令牌**的方式来访问 S3 数据，以提高安全性。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-data-source.md#从-amazon-s3-导入数据)。

### 遥测

- 自 2023 年 2 月 20 日起，新发布的 TiDB 和 TiDB Dashboard 版本（含 v6.6.0），默认关闭[遥测功能](/telemetry.md)，即默认不再收集使用情况信息分享给 PingCAP。如果升级至这些版本前使用默认的遥测配置，则升级后遥测功能处于关闭状态。具体的版本可参考 [TiDB 版本发布时间线](/releases/release-timeline.md)。
- 从 v1.11.3 起，新部署的 TiUP 默认关闭遥测功能，即默认不再收集使用情况信息。如果从 v1.11.3 之前的 TiUP 版本升级至 v1.11.3 或更高 TiUP 版本，遥测保持升级前的开启或关闭状态。

## 兼容性变更

> **注意：**
>
> 以下为从 v6.5.0 升级至当前版本 (v6.6.0) 所需兼容性变更信息。如果从 v6.4.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### MySQL 兼容性

* 支持兼容 MySQL 语法的外键约束（实验特性）[#18209](https://github.com/pingcap/tidb/issues/18209) @[crazycs520](https://github.com/crazycs520)

    更多信息，请参考本文的 [SQL 部分](#sql-功能)以及[用户文档](/foreign-key.md)。

* 支持兼容 MySQL 语法的多值索引（实验特性）[#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990)

    更多信息，请参考本文的 [SQL 部分](#sql-功能)以及[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

### 系统变量

| 变量名  | 修改类型    | 描述 |
|--------|------------------------------|------|
| `tidb_enable_amend_pessimistic_txn` | 删除  | 在 v6.5.0 中该变量被废弃。自 v6.6.0 起，该变量以及 `AMEND TRANSACTION` 特性被删除。TiDB 会使用[元数据锁机制](/metadata-lock.md)解决 `Information schema is changed` 报错的问题。  |
| `tidb_enable_concurrent_ddl` | 删除 | 这个变量用于控制是否让 TiDB 使用并发 DDL 语句。关闭该变量时 TiDB 采用旧的 DDL 执行框架，对 DDL 的并发支持有限。自 v6.6.0 起，该变量被删除，即不再支持旧的 DDL 执行框架。 |
| `tidb_ttl_job_run_interval` | 删除 | 这个变量用于控制 TTL 后台清理任务的调度周期。自 v6.6.0 起删除该变量，因为自 v6.6.0 起 TiDB 为每张表提供了属性 `TTL_JOB_INTERVAL` 用于配置 TTL 运行的间隔，允许用户为每张表设置不同的运行间隔，比系统变量更加灵活。 |
| [`foreign_key_checks`](/system-variables.md#foreign_key_checks) | 修改 | 用于控制是否开启外键约束检查。默认值由 `OFF` 修改为 `ON`，表示默认开启外键检查。|
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-从-v630-版本开始引入) | 修改 | 用于控制是否开启外键功能。默认值由 `OFF` 修改为 `ON`，表示默认开启外键功能。|
| `tidb_enable_general_plan_cache` |  修改  |   这个变量用来控制是否开启 General Plan Cache。自 v6.6.0 起，该变量更名为 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)。 |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats) | 修改 | 这个变量用来控制是否开启历史统计信息。默认值由 `OFF` 修改为 `ON`，表示默认开启历史统计信息。 |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) | 修改 | 这个变量从 v6.6.0 开始生效，用来控制是否开启 [`PLAN REPLAYER CAPTURE`](/sql-plan-replayer.md#使用-plan-replayer-capture-抓取目标计划)。默认值由 `OFF` 修改为 `ON`，代表默认开启 `PLAN REPLAYER CAPTURE`。 |
| [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-从-v402-版本开始引入从-v810-版本开始废弃) |  修改  |  默认值由 `ON` 修改为 `OFF`，表示默认关闭 TiDB 的遥测功能。 |
|  `tidb_general_plan_cache_size` |  修改   |   这个变量用来控制 General Plan Cache 最多能够缓存的计划数量。自 v6.6.0 起，该变量更名为 [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)。 |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) | 修改 | 新增选项 `learner`，指定 TiDB 从只读节点中读取数据的 learner 副本。 |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) | 修改 | 新增选项 `prefer-leader`，以提高 TiDB 集群整体的读可用性。该选项被启用时，TiDB 会优先选择 Leader 副本进行读取操作；当 Leader 副本的处理性能显著下降时，TiDB 会自动将读操作转发给 Follower 副本。|
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) | 修改 | 该变量设置 `IndexLookUp` 算子回表时多个 Coprocessor Task 的 batch 大小。`0` 代表不使用 batch。自 v6.6.0 起，默认值由 `0` 调整为 `4`，即每批请求会有 4 个 Coprocessor Task 被 batch 到一个 task 中。 |
| [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-从-v660-版本开始引入) |  新增  |  该变量用于选择 MPP Exchange 算子的数据压缩模式，当 TiDB 选择版本号为 `1` 的 MPP 执行计划时生效。默认值为 `UNSPECIFIED`，表示 TiDB 自动选择 `FAST` 压缩模式。|
| [`mpp_version`](/system-variables.md#mpp_version-从-v660-版本开始引入) |  新增  |  该变量用于指定不同版本的 MPP 执行计划。指定后，TiDB 会选择指定版本的 MPP 执行计划。默认值为 `UNSPECIFIED`，表示 TiDB 自动选择最新版本 `1`。 |
| [`tidb_ddl_distribute_reorg`](https://docs.pingcap.com/zh/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-从-v660-版本开始引入) | 新增 | 这个变量用来控制是否开启分布式执行 DDL reorg 阶段，来提升此阶段的速度。默认值为 `OFF`，表示默认不开启分布式执行 DDL reorg 阶段。目前此开关只对 `ADD INDEX` 语句有效。|
| [`tidb_enable_historical_stats_for_capture`](/system-variables.md#tidb_enable_historical_stats_for_capture) | 新增 | 这个变量用来控制 `PLAN REPLAYER CAPTURE` 抓取的内容是否默认带历史统计信息。默认值为 `OFF`，表示默认不带历史统计信息。 |
| [`tidb_enable_plan_cache_for_param_limit`](/system-variables.md#tidb_enable_plan_cache_for_param_limit-从-v660-版本开始引入) | 新增 | 这个变量用来控制 Prepared Plan Cache 是否缓存 `Limit` 后带有 `COUNT` 的执行计划。默认值为 `ON`，表示默认缓存这样的执行计划。目前不支持缓存 `Limit` 后面的 `COUNT` 具体参数值大于 10000 的执行计划。 |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) | 新增  | 该变量是[资源管控特性](/tidb-resource-control.md)的开关。默认值为 `OFF`。该变量设置为 `ON` 后，集群支持应用按照资源组做资源隔离。 |
| [`tidb_historical_stats_duration`](/system-variables.md#tidb_historical_stats_duration-从-v660-版本开始引入) | 新增 | 这个变量用来控制历史统计信息在存储中的保留时间，默认值为 7 天。 |
| [`tidb_index_join_double_read_penalty_cost_rate`](/system-variables.md#tidb_index_join_double_read_penalty_cost_rate-从-v660-版本开始引入) | 新增 | 用于控制是否给 index join 增加一些惩罚性代价。默认值为 `0`，即不开启该功能。 |
| [`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/zh/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) | 新增 | 是否对悲观锁启用加强的悲观锁唤醒模型。默认值为 `OFF`，表示默认不对悲观锁启用加强的悲观锁唤醒模型。 |
| [`tidb_stmt_summary_enable_persistent`](/system-variables.md#tidb_stmt_summary_enable_persistent-从-v660-版本开始引入) | 新增 | 只读变量。表示是否开启 [statement summary tables 持久化](/statement-summary-tables.md#持久化-statements-summary)。该变量的值与配置文件中 [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-从-v660-版本开始引入) 的取值相同。 |
| [`tidb_stmt_summary_filename`](/system-variables.md#tidb_stmt_summary_filename-从-v660-版本开始引入) | 新增 | 只读变量。表示当开启 [statement summary tables 持久化](/statement-summary-tables.md#持久化-statements-summary)后持久化数据所写入的文件。该变量的值与配置文件中 [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-从-v660-版本开始引入) 的取值相同。 |
| [`tidb_stmt_summary_file_max_backups`](/system-variables.md#tidb_stmt_summary_file_max_backups-从-v660-版本开始引入) | 新增 | 只读变量。表示当开启 [statement summary tables 持久化](/statement-summary-tables.md#持久化-statements-summary)后持久化数据文件的最大数量限制。该变量的值与配置文件中 [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-从-v660-版本开始引入) 的取值相同。 |
| [`tidb_stmt_summary_file_max_days`](/system-variables.md#tidb_stmt_summary_file_max_days-从-v660-版本开始引入) | 新增 | 只读变量。表示当开启 [statement summary tables 持久化](/statement-summary-tables.md#持久化-statements-summary)后持久化数据文件所保留的最大天数。该变量的值与配置文件中 [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-从-v660-版本开始引入) 的取值相同。 |
| [`tidb_stmt_summary_file_max_size`](/system-variables.md#tidb_stmt_summary_file_max_size-从-v660-版本开始引入) | 新增 | 只读变量。表示当开启 [statement summary tables 持久化](/statement-summary-tables.md#持久化-statements-summary)后持久化数据单个文件的大小限制。该变量的值与配置文件中 [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-从-v660-版本开始引入) 的取值相同。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV  |  `rocksdb.enable-statistics`  |  删除   |  该配置项指定是否开启 RocksDB 的统计信息收集功能。从 v6.6.0 起，删除该配置项。所有集群默认开启统计信息收集，以便于故障排查。详情参见 [#13942](https://github.com/tikv/tikv/pull/13942)。  |
| TiKV  |  `raftdb.enable-statistics`  |  删除   |  该配置项指定是否开启 Raft RocksDB 的统计信息收集功能。从 v6.6.0 起，删除该配置项。所有集群默认开启统计信息收集，以便于故障排查。详情参见 [#13942](https://github.com/tikv/tikv/pull/13942)。  |
| TiKV | `storage.block-cache.shared` | 删除 | 从 v6.6.0 起删除该配置项，默认开启 block cache 且无法关闭，详情参见 [#12936](https://github.com/tikv/tikv/issues/12936)。 |
| DM | `on-duplicate` | 删除 | 该配置项控制全量导入阶段针对冲突数据的解决方式。自 v6.6.0 起，引入新的配置项 `on-duplicate-logical` 和 `on-duplicate-physical`，取代 `on-duplicate`。 |
| TiDB  |  [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入从-v810-版本开始废弃)  |  修改 |  自 v6.6.0 起，该配置项默认值由 `true` 改为 `false`，表示默认关闭 TiDB 的遥测功能。  |
| TiKV  | [`rocksdb.defaultcf.block-size`](/tikv-configuration-file.md#block-size) 和 [`rocksdb.writecf.block-size`](/tikv-configuration-file.md#block-size)  |  修改  |   默认值由 `64K` 调整为 `32K`。  |
| TiKV | [`rocksdb.defaultcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size), [`rocksdb.writecf.block-cache-size`](/tikv-configuration-file.md#block-cache-size), [`rocksdb.lockcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) | 修改 | 从 v6.6.0 起，这三个配置项被废弃。详情参见 [#12936](https://github.com/tikv/tikv/issues/12936)。 |
| PD   |  [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)  |  修改  |   从 v6.6.0 起，该配置项的默认值由 `true` 改为 `false`，表示默认关闭 TiDB Dashboard 的遥测功能。  |
| TiFlash |  [`profile.default.max_memory_usage_for_all_queries`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)  |  修改  |  表示所有查询过程中，节点对中间数据的内存限制。自 v6.6.0 起默认值由 `0` 改为 `0.8`，表示节点占总内存的 80%。  |
| TiCDC  | [`consistent.storage`](/ticdc/ticdc-sink-to-mysql.md#使用前提)  |  修改  | redo log 备份文件的地址，除了 NFS，支持的 `scheme` 新增了 GCS 和 Azure。  |
| DM | [`import-mode`](/dm/task-configuration-file-full.md) | 修改 | 该配置项的可选值由 `"sql"` 和 `"loader"` 变更为 `"logical"` 和 `"physical"`。默认值为 `"logical"`，即使用 TiDB Lightning 的逻辑导入模式进行导入。 |
| TiDB  | [`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-从-v660-版本开始引入)  | 新增 | 用于指定 TiDB 集群初次启动时执行的 SQL 脚本。默认值为空。  |
| TiDB  | [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-从-v660-版本开始引入)  |  新增  |  用于控制是否开启 statements summary 持久化。默认值为 `false`，即不开启该功能。  |
| TiDB | [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-从-v660-版本开始引入) | 新增 | 当开启了 statements summary 持久化时，该配置用于限制持久化数据文件最大数量，默认值为 `0`，表示不限制文件数量。 |
| TiDB | [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-从-v660-版本开始引入) | 新增 | 当开启了 statements summary 持久化时，该配置用于指定持久化数据文件所保留的最大天数，默认为 3 天。 |
| TiDB | [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-从-v660-版本开始引入) | 新增 | 当开启了 statements summary 持久化时，该配置用于限制持久化数据单个文件的大小 (MiB)，默认值为 `64`。 |
| TiDB | [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-从-v660-版本开始引入) | 新增 | 当开启了 statements summary 持久化时，该配置用于指定持久化数据所写入的文件名称，默认为 `tidb-statements.log`。 |
| TiKV | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) | 新增 | 控制是否支持对用户前台的读写请求按照对应的资源组配额做优先级调度。默认为 `false`，即关闭按照资源组配额调度。 |
| TiKV | [`storage.engine`](/tikv-configuration-file.md#engine-从-v660-版本开始引入) | 新增 | 用于设置存储引擎类型，可选值有 `"raft-kv"` 和 `"partitioned-raft-kv"`。该配置只能在创建新集群时指定，且后续无法更改。 |
| TiKV | [`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-从-v660-版本开始引入) | 新增 | 用于设置当 RocksDB 当前 memtable 内存占用达到阈值之后的 Flush 策略。 |
| TiKV | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-从-v660-版本开始引入) | 新增 | 用于设置单个 TiKV 中所有 RocksDB 实例使用的 memtable 的总内存上限，默认值为本机内存的 25%。 |
| PD  | [`pd-server.enable-gogc-tuner`](/pd-configuration-file.md#enable-gogc-tuner-从-v660-版本开始引入) | 新增 | 控制是否开启 GOGC Tuner。默认关闭。 |
| PD  | [`pd-server.gc-tuner-threshold`](/pd-configuration-file.md#gc-tuner-threshold-从-v660-版本开始引入) | 新增 | GOGC Tuner 自动调节的最大内存阈值比例。默认值为 `0.6`。 |
| PD  | [`pd-server.server-memory-limit`](/pd-configuration-file.md#server-memory-limit-从-v660-版本开始引入) | 新增 | PD 实例的内存限制比例。`0` 表示不设内存限制。 |
| PD  |  [`pd-server.server-memory-limit-gc-trigger`](/pd-configuration-file.md#server-memory-limit-gc-trigger-从-v660-版本开始引入) | 新增 | PD 尝试触发 GC 的阈值比例。默认值为 `0.7`。 |
| TiCDC | [`scheduler.region-per-span`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | 该配置项用于将表按 Region 个数划分成多个同步范围，这些范围可由多个 TiCDC 节点同步，默认值为 `50000`。 |
| TiDB Lightning | [`compress-kv-pairs`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) | 新增 | 该配置项控制物理导入模式向 TiKV 发送 KV 时是否启用压缩，默认值为空，表示不启用压缩。 |
| DM | [`checksum-physical`](/dm/task-configuration-file-full.md) | 新增 | 该配置项控制物理导入模式在导入完成一张表后，对每一个表执行 `ADMIN CHECKSUM TABLE <table>` 进行数据校验。默认值为 `"required"`，表示导入完成后进行数据校验，如果校验失败会暂停任务，需要你手动处理。|
| DM | [`disk-quota-physical`](/dm/task-configuration-file-full.md) | 新增 | 该配置项设置了磁盘的空间限制，对应 TiDB Lightning 的 [`disk-quota` 配置](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#磁盘资源配额-从-v620-版本开始引入)。|
| DM | [`on-duplicate-logical`](/dm/task-configuration-file-full.md) | 新增 | 该配置项控制物理导入模式针对冲突数据的解决方式。默认值为 `"replace"`，表示用最新数据替代已有数据。 |
| DM | [`on-duplicate-physical`](/dm/task-configuration-file-full.md) | 新增 | 该配置项控制物理导入模式针对冲突数据的解决方式。默认值为 `"none"`，表示遇到冲突数据时不进行处理。该模式性能最佳，但下游数据库会出现数据索引不一致的问题。  |
| DM | [`sorting-dir-physical`](/dm/task-configuration-file-full.md) | 新增 | 该配置项控制物理导入模式用作本地排序的目录位置，该选项的默认值与 `dir` 配置项一致。 |
| sync-diff-inspector   | [`skip-non-existing-table`](/sync-diff-inspector/sync-diff-inspector-overview.md#配置文件说明)   |  新增 | 当下游数据库的表在上游不存在时，该配置项决定是否跳过对上下游数据库表数量不一致场景的校验。  |
| TiSpark | [`spark.tispark.replica_read`](/tispark-overview.md#tispark-配置) | 新增 | 控制读取副本的类型，可选值为 `leader`、`follower`、`learner`。 |
| TiSpark | [`spark.tispark.replica_read.label`](/tispark-overview.md#tispark-配置) | 新增 | 设置目标 TiKV 节点的标签。 |

### 其他

- 支持动态修改参数 [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-从-v530-版本开始引入)，增加了 TiKV 性能调优的灵活性。
- 解除了执行计划缓存对 `LIMIT` 子句的限制，提升了执行效率。
- v6.6.0 及以上的 BR 版本不支持恢复数据到 v6.1.0 及以下版本的集群。
- 自 v6.6.0 起，由于可能存在正确性问题，分区表目前不再支持修改列类型。

## 改进提升

+ TiDB

    - 改进了 TTL 后台清理任务的调度机制，允许将单个表的清理任务拆分成若干子任务并调度到多个 TiDB 节点同时运行 [#40361](https://github.com/pingcap/tidb/issues/40361) @[YangKeao](https://github.com/YangKeao)
    - 优化了在设置了非默认的 delimiter 后多语句返回结果的列名显示 [#39662](https://github.com/pingcap/tidb/issues/39662) @[mjonss](https://github.com/mjonss)
    - 优化了生成警告信息后的语句执行效率 [#39702](https://github.com/pingcap/tidb/issues/39702) @[tiancaiamao](https://github.com/tiancaiamao)
    - 为 `ADD INDEX` 支持分布式数据回填（实验特性）[#37119](https://github.com/pingcap/tidb/issues/37119) @[zimulala](https://github.com/zimulala)
    - 允许使用 `CURDATE()` 作为列的默认值 [#38356](https://github.com/pingcap/tidb/issues/38356) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 增加了 `partial order prop push down` 对 LIST 类型分区表的支持 [#40273](https://github.com/pingcap/tidb/issues/40273) @[winoros](https://github.com/winoros)
    - 为 Optimizer Hints 和执行计划绑定的冲突新增报错信息 [#40910](https://github.com/pingcap/tidb/issues/40910) @[Reminiscent](https://github.com/Reminiscent)
    - 优化了 Plan Cache 策略，避免在一些场景使用 Plan Cache 时产生不优计划 [#40312](https://github.com/pingcap/tidb/pull/40312) [#40218](https://github.com/pingcap/tidb/pull/40218) [#40280](https://github.com/pingcap/tidb/pull/40280) [#41136](https://github.com/pingcap/tidb/pull/41136) [#40686](https://github.com/pingcap/tidb/pull/40686) @[qw4990](https://github.com/qw4990)
    - 定期清理过期的 Region 缓存，避免内存泄漏和性能下降问题 [#40461](https://github.com/pingcap/tidb/issues/40461) @[sticnarf](https://github.com/sticnarf)
    - 不支持在分区表上执行 `MODIFY COLUMN` [#39915](https://github.com/pingcap/tidb/issues/39915) @[wjhuang2016](https://github.com/wjhuang2016)
    - 禁止重命名分区表所依赖的列 [#40150](https://github.com/pingcap/tidb/issues/40150) @[mjonss](https://github.com/mjonss)
    - 优化了删除分区表所依赖的列的错误提示 [#38739](https://github.com/pingcap/tidb/issues/38739) @[jiyfhust](https://github.com/jiyfhust)
    - 增加了 `FLASHBACK CLUSTER` 在检查 `min-resolved-ts` 失败后的重试机制 [#39836](https://github.com/pingcap/tidb/issues/39836) @[Defined2014](https://github.com/Defined2014)

+ TiKV

    - 在 partitioned-raft-kv 模式下优化了一些参数的默认值：TiKV 配置项 `storage.block-cache.capacity` 的默认值由 45% 调整为 30%，`region-split-size` 的默认值由 `96MiB` 调整为 `10GiB`。当沿用 raft-kv 模式且 `enable-region-bucket` 为 `true` 时，`region-split-size` 默认调整为 `1GiB` [#12842](https://github.com/tikv/tikv/issues/12842) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 支持在 Raftstore 异步写入中进行优先级调度 [#13730](https://github.com/tikv/tikv/issues/13730) @[Connor1996](https://github.com/Connor1996)
    - 支持在小于 1 core 的 CPU 下启动 TiKV [#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db)
    - 优化 Raftstore slow score 探测的新机制，新增 `evict-slow-trend-scheduler` [#14131](https://github.com/tikv/tikv/issues/14131) @[innerr](https://github.com/innerr)
    - 强制 RocksDB 的 block cache 为共享的，不再支持按照 CF 单独设置 block cache [#12936](https://github.com/tikv/tikv/issues/12936) @[busyjay](https://github.com/busyjay)

+ PD

    - 增加全局内存阈值管理功能以缓解 OOM 问题（实验特性）[#5827](https://github.com/tikv/pd/issues/5827) @[hnes](https://github.com/hnes)
    - 增加 GC Tuner 功能以缓解 GC 压力（实验特性）[#5827](https://github.com/tikv/pd/issues/5827) @[hnes](https://github.com/hnes)
    - 新增 `evict-slow-trend-scheduler` 调度器用于检测和调度异常节点 [#5808](https://github.com/tikv/pd/pull/5808) @[innerr](https://github.com/innerr)
    - 新增 keyspace manager，支持对 keyspace 的管理 [#5293](https://github.com/tikv/pd/issues/5293) @[AmoebaProtozoa](https://github.com/AmoebaProtozoa)

+ TiFlash

    - 提供独立的 MVCC 位图过滤器，解耦 TiFlash 整体数据扫描流程中的 MVCC 过滤操作，为后续优化数据扫描流程提供基础 [#6296](https://github.com/pingcap/tiflash/issues/6296) @[JinheLin](https://github.com/JinheLin)
    - 减少 TiFlash 在没有查询的情况下的内存使用，最高减少 30% [#6589](https://github.com/pingcap/tiflash/pull/6589) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - 优化 TiKV 端下载日志备份文件的并发度，提升常规场景下 PITR 恢复的性能 [#14206](https://github.com/tikv/tikv/issues/14206) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 支持 Batch UPDATE DML 语句，提升 TiCDC 的同步性能 [#8084](https://github.com/pingcap/tiflow/issues/8084) @[amyangfei](https://github.com/amyangfei)
        - 采用异步模式实现 MQ sink 和 MySQL sink，提升 sink 的吞吐能力 [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu) @[hi-rustin](https://github.com/Rustin170506)

    + TiDB Data Migration (DM)

        - 优化了 DM 的告警规则和内容 [#7376](https://github.com/pingcap/tiflow/issues/7376) @[D3Hunter](https://github.com/D3Hunter)

            之前 "DM_XXX_process_exits_with_error" 类告警是遇到相关错误即报警，但有些告警是由于数据库连接长时间 idle 导致的，重连后即可恢复。为了减少此类报警，DM 将错误分为了可自动恢复错误和不可自动恢复错误：

            - 对于可自动恢复的错误，只有在 2 分钟内发生超过 3 次时才报警。
            - 对于不可自动恢复的错误，维持原有行为，立即报警。

        - 新增 async/batch relay writer 以优化 relay 性能 [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - 物理导入模式支持 Keyspace [#40531](https://github.com/pingcap/tidb/issues/40531) @[iosmanthus](https://github.com/iosmanthus)
        - 支持通过 `lightning.max-error` 设置最大冲突个数 [#40743](https://github.com/pingcap/tidb/issues/40743) @[dsdashun](https://github.com/dsdashun)
        - 支持导入带有 BOM header 的 CSV 数据文件 [#40744](https://github.com/pingcap/tidb/issues/40744) @[dsdashun](https://github.com/dsdashun)
        - 优化遇到 TiKV 限流错误时的处理逻辑，改为尝试其他空闲的 Region [#40205](https://github.com/pingcap/tidb/issues/40205) @[lance6716](https://github.com/lance6716)
        - 导入时关闭对表外键的检查 [#40027](https://github.com/pingcap/tidb/issues/40027) @[sleepymole](https://github.com/sleepymole)

    + Dumpling

        - 支持导出外键相关设置 [#39913](https://github.com/pingcap/tidb/issues/39913) @[lichunzhu](https://github.com/lichunzhu)

    + sync-diff-inspector

        - 新增 `skip-non-existing-table` 参数，当下游数据库的表在上游不存在时，可配置该参数为 `true` 跳过对上下游数据库表数量不一致场景的校验 [#692](https://github.com/pingcap/tidb-tools/issues/692) @[lichunzhu](https://github.com/lichunzhu) @[liumengya94](https://github.com/liumengya94)

## 错误修复

+ TiDB

    - 修复了收集统计信息任务因为错误的 `datetime` 值而失败的问题 [#39336](https://github.com/pingcap/tidb/issues/39336) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复了创建表之后 `stats_meta` 未创建的问题 [#38189](https://github.com/pingcap/tidb/issues/38189) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复了 DDL 回填数据时频繁出现的事务写冲突问题 [#24427](https://github.com/pingcap/tidb/issues/24427) @[mjonss](https://github.com/mjonss)
    - 修复了部分情况下空表无法使用 ingest 模式添加索引的问题 [#39641](https://github.com/pingcap/tidb/issues/39641) @[tangenta](https://github.com/tangenta)
    - 修复了同一事务中不同 SQL 的慢日志 `wait_ts` 相同的问题 [#39713](https://github.com/pingcap/tidb/issues/39713) @[TonsnakeLin](https://github.com/TonsnakeLin)
    - 修复了在添加列的过程中删除行记录时报 `Assertion Failed` 错误的问题 [#39570](https://github.com/pingcap/tidb/issues/39570) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复了修改列类型时报 `not a DDL owner` 错误的问题 [#39643](https://github.com/pingcap/tidb/issues/39643) @[zimulala](https://github.com/zimulala)
    - 修复了在 `AUTO_INCREMENT` 列自动分配值耗尽后插入一行不报错的问题 [#38950](https://github.com/pingcap/tidb/issues/38950) @[Dousir9](https://github.com/Dousir9)
    - 修复了创建表达式索引时报 `Unknown column` 错误的问题 [#39784](https://github.com/pingcap/tidb/issues/39784) @[Defined2014](https://github.com/Defined2014)
    - 修复了当生成的列表达式包含表名时，重命名表后无法插入数据的问题 [#39826](https://github.com/pingcap/tidb/issues/39826) @[Defined2014](https://github.com/Defined2014)
    - 修复了当列处于 write-only 状态时 `INSERT ignore` 语句无法正确填充默认值的问题 [#40192](https://github.com/pingcap/tidb/issues/40192) @[YangKeao](https://github.com/YangKeao)
    - 修复了关闭资源管控模块时未能释放资源的问题 [#40546](https://github.com/pingcap/tidb/issues/40546) @[zimulala](https://github.com/zimulala)
    - 修复了 TTL 任务不能及时触发统计信息更新的问题 [#40109](https://github.com/pingcap/tidb/issues/40109) @[YangKeao](https://github.com/YangKeao)
    - 修复了 TiDB 构造 key 范围时对 `NULL` 值处理不当，导致读取非预期数据的问题 [#40158](https://github.com/pingcap/tidb/issues/40158) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复了 `MODIFY COLUMN` 同时修改列默认值导致写入非法值的问题 [#40164](https://github.com/pingcap/tidb/issues/40164) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复了表 Region 比较多时因 Region 缓存失效导致加索引效率低下的问题 [#38436](https://github.com/pingcap/tidb/issues/38436) @[tangenta](https://github.com/tangenta)
    - 修复了分配自增 ID 时的数据竞争问题 [#40584](https://github.com/pingcap/tidb/issues/40584) @[Dousir9](https://github.com/Dousir9)
    - 修复了 JSON 的 not 表达式实现与 MySQL 实现不兼容的问题 [#40683](https://github.com/pingcap/tidb/issues/40683) @[YangKeao](https://github.com/YangKeao)
    - 修复了并发视图模式可能会造成 DDL 操作卡住的问题 [#40352](https://github.com/pingcap/tidb/issues/40352) @[zeminzhou](https://github.com/zeminzhou)
    - 修复了并发对分区表执行 `MODIFY COLUMN` 的 DDL 操作时有可能会造成数据不一致的问题 [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss) @[mjonss](https://github.com/mjonss)
    - 修复了使用 `caching_sha2_password` 方式进行认证但不指定密码导致的 "Malformed packet" 问题 [#40831](https://github.com/pingcap/tidb/issues/40831) @[dveeden](https://github.com/dveeden)
    - 修复了在执行 TTL 任务时，如果表的主键包含 `ENUM` 类型的列任务会失败的问题 [#40456](https://github.com/pingcap/tidb/issues/40456) @[lcwangchao](https://github.com/lcwangchao)
    - 修复了某些被 MDL 阻塞的 DDL 操作无法在 `mysql.tidb_mdl_view` 中查询到的问题 [#40838](https://github.com/pingcap/tidb/issues/40838) @[YangKeao](https://github.com/YangKeao)
    - 修复了 DDL 在 ingest 过程中可能会发生数据竞争的问题 [#40970](https://github.com/pingcap/tidb/issues/40970) @[tangenta](https://github.com/tangenta)
    - 修复了在改变时区后 TTL 任务可能会错误删除某些数据的问题 [#41043](https://github.com/pingcap/tidb/issues/41043) @[lcwangchao](https://github.com/lcwangchao)
    - 修复了 `JSON_OBJECT` 在某些情况下会报错的问题 [#39806](https://github.com/pingcap/tidb/issues/39806) @[YangKeao](https://github.com/YangKeao)
    - 修复了 TiDB 在初始化时有可能死锁的问题 [#40408](https://github.com/pingcap/tidb/issues/40408) @[Defined2014](https://github.com/Defined2014)
    - 修复了内存重用导致的在某些情况下系统变量的值会被错误修改的问题 [#40979](https://github.com/pingcap/tidb/issues/40979) @[lcwangchao](https://github.com/lcwangchao)
    - 修复了 ingest 模式下创建唯一索引可能会导致数据和索引不一致的问题 [#40464](https://github.com/pingcap/tidb/issues/40464) @[tangenta](https://github.com/tangenta)
    - 修复了并发 truncate 同一张表时，部分 truncate 操作无法被 MDL 阻塞的问题 [#40484](https://github.com/pingcap/tidb/issues/40484) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复了 `SHOW PRIVILEGES` 命令显示的权限列表不完整的问题 [#40591](https://github.com/pingcap/tidb/issues/40591) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复了在添加唯一索引时有可能会 panic 的问题 [#40592](https://github.com/pingcap/tidb/issues/40592) @[tangenta](https://github.com/tangenta)
    - 修复了执行 `ADMIN RECOVER` 语句可能会造成索引数据损坏的问题 [#40430](https://github.com/pingcap/tidb/issues/40430) @[xiongjiwei](https://github.com/xiongjiwei)
    - 修复了表达式索引中含有 `CAST` 时对表进行查询可能出错的问题 [#40130](https://github.com/pingcap/tidb/issues/40130) @[xiongjiwei](https://github.com/xiongjiwei)
    - 修复了某些情况下唯一索引仍然可能产生重复数据的问题 [#40217](https://github.com/pingcap/tidb/issues/40217) @[tangenta](https://github.com/tangenta)
    - 修复了使用 `Prepare` 或 `Execute` 查询某些虚拟表时无法将表 ID 下推，导致在大量 Region 的情况下 PD OOM 的问题 [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    - 修复了添加索引时可能导致数据竞争的问题 [#40879](https://github.com/pingcap/tidb/issues/40879) @[tangenta](https://github.com/tangenta)
    - 修复了由虚拟列引发的 `can't find proper physical plan` 问题 [#41014](https://github.com/pingcap/tidb/issues/41014) @[AilinKid](https://github.com/AilinKid)
    - 修复了当动态裁剪模式下的分区表有 global binding 时，TiDB 重启失败的问题 [#40368](https://github.com/pingcap/tidb/issues/40368) @[Yisaer](https://github.com/Yisaer)
    - 修复了 `auto analyze` 导致 graceful shutdown 耗时长的问题 [#40038](https://github.com/pingcap/tidb/issues/40038) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复了 IndexMerge 算子在触发内存限制行为时可能导致 TiDB server 崩溃的问题 [#41036](https://github.com/pingcap/tidb/pull/41036) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复了在分区表上执行 `SELECT * FROM table_name LIMIT 1` 查询时，执行速度慢的问题 [#40741](https://github.com/pingcap/tidb/pull/40741) @[solotzg](https://github.com/solotzg)

+ TiKV

    - 修复转换 `const Enum` 类型到其他类型时报错的问题 [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 Resolved TS 导致网络流量升高的问题 [#14092](https://github.com/tikv/tikv/issues/14092) @[overvenus](https://github.com/overvenus)
    - 修复 TiDB 中事务在执行悲观 DML 失败后，再执行其他 DML 时，如果 TiDB 和 TiKV 之间存在网络故障，可能会造成数据不一致的问题 [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - 修复 Region Scatter 任务会生成非预期的多余副本的问题 [#5909](https://github.com/tikv/pd/issues/5909) @[HundunDM](https://github.com/HunDunDM)
    - 修复 Online Unsafe Recovery 功能在 `auto-detect` 模式下卡住并超时的问题 [#5753](https://github.com/tikv/pd/issues/5753) @[Connor1996](https://github.com/Connor1996)
    - 修复 `replace-down-peer` 在特定条件下执行变慢的问题 [#5788](https://github.com/tikv/pd/issues/5788) @[HundunDM](https://github.com/HunDunDM)
    - 修复调用 `ReportMinResolvedTS` 过于频繁导致 PD OOM 的问题 [#5965](https://github.com/tikv/pd/issues/5965) @[HundunDM](https://github.com/HunDunDM)

+ TiFlash

    - 修复查询 TiFlash 相关的系统表可能会卡住的问题 [#6745](https://github.com/pingcap/tiflash/pull/6745) @[lidezhu](https://github.com/lidezhu)
    - 修复半连接在计算笛卡尔积时，使用内存过量的问题 [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    - 修复对 DECIMAL 数据类型进行除法运算时结果不舍入的问题 [#6393](https://github.com/pingcap/tiflash/issues/6393) @[LittleFall](https://github.com/LittleFall)
    - 修复了 TiFlash 查询中由于 `start_ts` 无法唯一标识一个 MPP query 导致 MPP query 可能会被误取消的问题 [#43426](https://github.com/pingcap/tidb/issues/43426) @[hehechen](https://github.com/hehechen)

+ Tools

    + Backup & Restore (BR)

        - 修复恢复日志备份时热点 Region 导致恢复失败的问题 [#37207](https://github.com/pingcap/tidb/issues/37207) @[Leavrth](https://github.com/Leavrth)
        - 修复恢复数据到正在运行日志备份的集群，导致日志备份文件无法恢复的问题 [#40797](https://github.com/pingcap/tidb/issues/40797) @[Leavrth](https://github.com/Leavrth)
        - 修复 PITR 功能不支持 CA-bundle 认证的问题 [#38775](https://github.com/pingcap/tidb/issues/38775) @[YuJuncen](https://github.com/YuJuncen)
        - 修复恢复时重复的临时表导致的 panic 问题 [#40797](https://github.com/pingcap/tidb/issues/40797) @[joccau](https://github.com/joccau)
        - 修复 PITR 不支持 PD 集群配置变更的问题 [#14165](https://github.com/tikv/tikv/issues/14165) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 PD 与 TiDB server 的连接故障导致 PITR 备份进度不推进的问题 [#41082](https://github.com/pingcap/tidb/issues/41082) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 PD 与 TiKV 的连接故障导致 TiKV 不能监听 PITR 任务的问题 [#14159](https://github.com/tikv/tikv/issues/14159) @[YuJuncen](https://github.com/YuJuncen)
        - 修复当 TiDB 集群不存在 PITR 备份任务时，`resolve lock` 频率过高的问题 [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - 修复 PITR 备份任务被删除时，存在备份信息残留导致新任务出现数据不一致的问题 [#40403](https://github.com/pingcap/tidb/issues/40403) @[joccau](https://github.com/joccau)

    + TiCDC

        - 修复不能通过配置文件修改 `transaction_atomicity` 和 `protocol` 参数的问题 [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 redo log 存储路径没做权限预检查的问题 [#6335](https://github.com/pingcap/tiflow/issues/6335) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 redo log 容忍 S3 存储故障的时间过短的问题 [#8089](https://github.com/pingcap/tiflow/issues/8089) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 changefeed 在 TiKV、TiCDC 节点扩缩容等特殊场景下卡住的问题 [#8174](https://github.com/pingcap/tiflow/issues/8174) @[hicqu](https://github.com/hicqu)
        - 修复 TiKV 节点之间流量过大的问题 [#14092](https://github.com/tikv/tikv/issues/14092) @[overvenus](https://github.com/overvenus)
        - 优化 pull-based sink 打开时 TiCDC 在 CPU 利用率、内存控制、吞吐等方面若干性能问题 [#8142](https://github.com/pingcap/tiflow/issues/8142) [#8157](https://github.com/pingcap/tiflow/issues/8157) [#8001](https://github.com/pingcap/tiflow/issues/8001) [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu) @[hi-rustin](https://github.com/Rustin170506)

    + TiDB Data Migration (DM)

        - 修复 `binlog-schema delete` 命令执行失败的问题 [#7373](https://github.com/pingcap/tiflow/issues/7373) @[liumengya94](https://github.com/liumengya94)
        - 修复当最后一个 binlog 是被 skip 的 DDL 时，checkpoint 不推进的问题 [#8175](https://github.com/pingcap/tiflow/issues/8175) @[D3Hunter](https://github.com/D3Hunter)
        - 修复当在某个表上同时指定 `UPDATE` 和非 `UPDATE` 类型的表达式过滤规则 `expression-filter` 时，所有 `UPDATE` 操作被跳过的问题 [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716](https://github.com/lance6716)
        - 修复当某个表上仅指定 `update-old-value-expr` 或 `update-new-value-expr` 时，过滤规则不生效或 DM 发生 panic 的问题 [#7774](https://github.com/pingcap/tiflow/issues/7774) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复了部分场景下 TiDB 重启导致 TiDB Lightning 卡住的问题 [#33714](https://github.com/pingcap/tidb/issues/33714) @[lichunzhu](https://github.com/lichunzhu)
        - 修复在并行导入时，当除最后一个 TiDB Lightning 实例外的其他实例都遇到本地重复记录时，TiDB Lightning 可能会错误地跳过冲突处理的问题 [#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)
        - 修复 precheck 无法准确检测目标集群是否存在运行中的 TiCDC 的问题 [#41040](https://github.com/pingcap/tidb/issues/41040) @[lance6716](https://github.com/lance6716)
        - 修复 TiDB Lightning 在 split-region 阶段发生 panic 的问题 [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        - 修复冲突处理逻辑 (`duplicate-resolution`) 可能导致 checksum 不一致的问题 [#40657](https://github.com/pingcap/tidb/issues/40657) @[sleepymole](https://github.com/sleepymole)
        - 修复当数据文件中存在未闭合的 delimiter 时可能 OOM 的问题 [#40400](https://github.com/pingcap/tidb/issues/40400) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - 修复报错中的文件 offset 超过文件大小的问题 [#40034](https://github.com/pingcap/tidb/issues/40034) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - 修复新版 PD client 可能导致并行导入失败的问题 [#40493](https://github.com/pingcap/tidb/issues/40493) @[AmoebaProtozoa](https://github.com/AmoebaProtozoa)
        - 修复 precheck 检查项有时无法监测到之前的导入失败遗留的脏数据的问题 [#39477](https://github.com/pingcap/tidb/issues/39477) @[dsdashun](https://github.com/dsdashun)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [morgo](https://github.com/morgo)
- [jiyfhust](https://github.com/jiyfhust)
- [b41sh](https://github.com/b41sh)
- [sourcelliu](https://github.com/sourcelliu)
- [songzhibin97](https://github.com/songzhibin97)
- [mamil](https://github.com/mamil)
- [Dousir9](https://github.com/Dousir9)
- [hihihuhu](https://github.com/hihihuhu)
- [mychoxin](https://github.com/mychoxin)
- [xuning97](https://github.com/xuning97)
- [andreid-db](https://github.com/andreid-db)
