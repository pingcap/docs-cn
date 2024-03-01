---
title: TiDB 8.0.0 Release Notes
summary: 了解 TiDB 8.0.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.0.0 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：8.0.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.0/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.0.0-DMR#version-list)

在 8.0.0 版本中，你可以获得以下关键特性：

## 功能详情

### 可扩展性

* 增强 Titan 引擎  [#issue号](链接) @[Connor1996](https://github.com/Connor1996) **tw@qiancai** <!--1708-->

    TiDB v8.0.0 版本引入了 Titan 一系列的性能优化和功能增强，主要包括优化 GC 算法、默认开启字典压缩等功能。其中，我们调整了 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 的默认阈值，从 `32KB` 调整为 `?KB` ，进一步扩大 Titan 引擎的适用场景。此外，我们还允许用户动态修改 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 阈值配置，以提升用户使用 Titan 引擎时的性能和灵活性。这些改进和功能增强将为用户提供更加稳定和高效的数据库服务。

    更多信息，请参考[用户文档](/storage-engine/titan-overview.md)。
    
### 性能


* BR 快照恢复速度最高提升 10 倍 GA [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer) @[Leavrth](https://github.com/Leavrth) **tw@qiancai** <!--1681-->

    TiDB v8.0.0 版本起，快照恢复提速的改进正式 GA，并默认启用。通过采用粗粒度打散 Region 算法、批量创建库表、降低 SST 文件下载和 Ingest 操作的相互影响以及加速表统计信息恢复等改进措施，在保持数据充分打散的前提下，快照恢复的速度最高提升 10 倍。这一改进充分利用了每个 TiKV 节点的资源并行恢复，使得每个 TiKV 节点的数据恢复能够充分利用硬件的磁盘和网络带宽。根据实际案例的测试结果，单个 TiKV 节点的数据恢复速度稳定在 1.2 GB/s，能够在 1 小时内完成对 100 TB 数据的恢复。
    
    这意味着即使在高负载环境下，BR 工具也能够充分利用每个 TiKV 节点的资源，实现了横向和纵向扩展性。通过这一改进，我们成功缩短了数据库恢复时间，提高了数据库的可用性和可靠性，从而降低了因数据丢失或故障而导致的停机时间和业务损失。
 
    更多信息，请参考[用户文档](/br/br-snapshot-guide.md#恢复快照备份数据)。
    
* 新增支持下推以下 函数到 TiFlash [#48350](https://github.com/pingcap/tidb/issues/48350) [#xxx](https://github.com/pingcap/tidb/issues/xxx) @[xxx](https://github.com/xxx) **tw@Oreoxmt** <!--1662--><!--1664-->

    * `POWER()`
    * `CAST(DECIMAL AS DOUBLE)`

    更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* TiDB 的并发 HashAgg 算法支持数据落盘（实验特性）[#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1365-->

    在之前的 TiDB 版本中，HashAgg 算子的并发算法不支持数据落盘。当 SQL 语句的执行计划包含并发的 HashAgg 算子时，该 SQL 语句的所有数据都只能在内存中进行处理。这导致内存需要处理大量数据，当超过内存限制时，TiDB 只能选择非并发 HashAgg 算法，无法通过并发提升性能。

    在 v8.0.0 中，TiDB 的并发 HashAgg 算法支持数据落盘。在任意并发条件下，HashAgg 算子都可以根据内存使用情况自动触发数据落盘，从而兼顾性能和数据处理量。目前，该功能作为实验特性，引入变量 `tidb_enable_concurrent_hashagg_spill` 控制是否启用支持落盘的并发 HashAgg 算法。当该变量为 `ON` 时，代表启用。该变量将在功能正式发布时废弃。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_concurrent_hashagg_spill-从-v800-版本开始引入)。

* 自动统计信息收集引入优先级队列 [#50132](https://github.com/pingcap/tidb/issues/50132) @[hi-rustin](https://github.com/hi-rustin) **tw@hfxsd** <!--1640-->

    维持优化器统计信息的时效性是稳定数据库性能的关键，绝大多数用户依赖 TiDB 提供的[自动统计信息收集](/statistics.md#自动更新) 来保持统计信息的更新。自动统计信息收集轮询所有对象的统计信息状态，并把健康度不足的对象加入队列，逐个收集并更新。在过去的版本中，收集顺序是随机设置的，这可能造成更有收集价值的对象需要长时间等待才被更新，引发潜在的数据库性能回退。

    从 v8.0.0 开始，自动统计信息收集会结合多种条件为对象动态设置优先级，确保更有收集价值的对象优先被处理，比如新创建的索引、发生分区变更的分区表等，健康度更低的对象也会倾向于排在队列前端。该增强提升了收集顺序的合理性，能减少一部分统计信息过旧引发的性能问题，因此提升了数据库稳定性。

    更多信息，请参考[用户文档](/statistics.md#自动更新)。

* 解除执行计划缓存的部分限制 [#49161](https://github.com/pingcap/tidb/pull/49161) @[mjonss](https://github.com/mjonss) @[qw4990](https://github.com/qw4990) **tw@hfxsd** <!--1622/1585-->

    TiDB 支持[执行计划缓存](/sql-prepared-plan-cache.md)，它能够有效减低交易类业务系统的处理时延，是提升性能的重要手段。在 v8.0.0 中，TiDB 解除了执行计划缓存的几个限制：
    
    * 含有[分区表](/partitioned-table.md)的执行计划能够被缓存
    * 含有[生成列](/generated-columns.md)的执行计划能够被缓存
    
    当执行计划中含有分区表、生成列、或者依赖生成列的对象(比如[多值索引](/choose-index.md))时，执行计划仍旧可以被缓存。这些增强扩展了执行计划缓存的使用场景，提升了复杂场景下数据库的整体性能。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* 优化器增强对多值索引的支持 [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate) **tw@hfxsd** <!--1405/1584-->

    TiDB 自 v6.6.0 开始引入[多值索引](/sql-statements/sql-statement-create-index.md#多值索引)，提升对 JSON 数据类型的检索性能。在 v8.0.0 中，优化器增强了对多值索引的支持能力，在复杂使用场景下，能够正确识别和利用多值索引来优化查询。

    * 多值索引上的统计信息会被收集，并应用于优化器估算。当一条 SQL 可能选择到数个多值索引时，优化器可以识别开销更小的索引。
    * 当出现用 `OR` 连接的多个 `member of` 条件时，优化器能够为每个 DNF Item（`member of` 条件）匹配一个有效的 Index Partial Path 路径，并将多条路径以 Union 的方式综合起来组成 `Index Merge` 来做更高效的条件过滤和数据读取。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

### 稳定性

* 支持根据 LRU 算法缓存所需的 schema 信息来减少对 TiDB 接的内存消耗（实验特性）[#issue号](链接) @[gmhdbjd](https://github.com/gmhdbjd) **tw@hfxsd** <!--1691-->

    在 v8.0.0 之前，每个 TiDB 节点都会 cache 所有表的 schema 信息，一旦表的数量较多，如达到几十万的场景，光缓存这些表的 schema 信息就会占用较多的内存。从 v8.0.0 版本开始，引入了参数 `tidb_schema_cache_size`，用户设置缓存 schema 可以使用的内存上限，避免占用过多的内存，而且开启该功能后，将使用 LRU 算法来缓存所需的表，有效减小所需换成的 schema 信息。

    更多信息，请参考[用户文档](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入)。
    
### 高可用

* 支持代理组件 TiProxy [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@Oreoxmt** <!--1698-->

    TiProxy 是 TiDB 的官方代理组件，位于客户端和 TiDB server 之间，为 TiDB 提供负载均衡、连接保持功能，让 TiDB 集群的负载更加均衡，并在维护操作期间不影响用户对数据库的连接访问。
    
    在 v7.6.0 版本中，TiProxy 以实验特性发布。在 v8.0.0 版本中，TiProxy 完善了签名证书自动生成、监控等功能，并正式发布。
    
    TiProxy 主要应用于以下场景：

    * 在 TiDB 集群进行滚动重启、滚动升级、缩容等维护操作时，TiDB server 会发生变动，导致客户端与发生变化的 TiDB server 的连接中断。通过使用 TiProxy，可以在这些维护操作过程中平滑地将连接迁移至其他 TiDB server，从而让客户端不受影响。
    * 所有客户端对 TiDB server 的连接都无法动态迁移至其他 TiDB server。当多个 TiDB server 的负载不均衡时，可能出现整体集群资源充足，但某些 TiDB server 资源耗尽导致延迟大幅度增加的情况。为解决此问题，TiProxy 提供连接动态迁移功能，在客户端无感的前提下，将连接从一个 TiDB server 迁移至其他 TiDB server，从而实现 TiDB 集群的负载均衡。

    TiProxy 已集成至 TiUP、TiDB Operator、TiDB Dashboard 等 TiDB 基本组件中，可以方便地进行配置、部署和运维。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。

### SQL 功能

* 新增支持处理大量数据的 DML 类型 [#16291](https://github.com/tikv/tikv/issues/16291) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1694-->

    在之前的 TiDB 版本中，所有的事务数据在提交之前，都保存在内存中。当处理大量数据时，事务所需的内存成为瓶颈，限制了 TiDB 可以处理的事务大小。TiDB 曾经发布了非事务 DML 功能，通过拆分 SQL 的方式尝试解决事务大小限制，但是功能存在较多限制，在实际使用时并不友好。
    
    在 v8.0.0 中，TiDB 新增支持处理大量数据的 DML 类型。这种 DML 类型在执行时，通过及时将数据写入 TiKV 的方式，避免将所有事务数据保存在内存中，从而实现对超过内存上限的大量数据的处理。该 DML 类型保证事务的完整性，并且使用和标准 DML 完全一致的语法。任何 TiDB 的合法 DML，都可以使用这种 DML 类型，以处理大数据量 DML 操作。
    
    支持处理大量数据的 DML 类型依赖于 [Pipelined DML](/ new doc path)，只支持在自动提交事务中使用，并且引入变量 `tidb_dml_type` 控制是否使用该 DML 类型。目前，该功能作为实验特性发布。

    更多信息，请参考[用户文档](/... tidb_dml_type 变量)。

* TiDB 建表时，支持更多的表达式来设置列的默认值 [#issue号](链接) @[zimulala](https://github.com/zimulala) **tw@qiancai** <!--1690-->

    之前的版本建表时，列默认值只能为固定的字符串，数字，以及日期，而从 v8.0.0 版本开始，支持将部分表达式作为列的默认值，如将列的默认值设置为 UUID() ，从而来满足用户多样化的业务需求。

    更多信息，请参考[用户文档](链接)。
### 数据库管理

* PITR 支持 Amazon S3 对象锁定 [#51184](https://github.com/pingcap/tidb/issues/51184) @[RidRisR](https://github.com/RidRisR) **tw@lilin90** <!--1604-->

    Amazon S3 对象锁定功能支持通过客户定义的留存期，有效防止备份数据在指定时间内被意外或故意删除，提升了数据的安全性和完整性。BR 从 v6.3.0 版本开始为快照备份引入了对 Amazon S3 对象锁定功能的支持，为全量备份增加了额外的安全性保障。从 v8.0.0 版本开始，PITR 也引入了对 Amazon S3 对象锁定功能的支持，无论是全量还是日志数据备份，都可以通过对象锁定功能提供更可靠的数据保护，进一步加强了数据备份和恢复的安全性，并满足监管方面的需求。
    
    更多信息，请参考[用户文档](链接)。
    
    * PITR 支持备份恢复 Lightning 物理模式导入的数据 （实验性功能） [#issue号](链接) @[BornChanger](https://github.com/BornChanger) **tw@qiancai** <!--1086-->

    TiDB v8.0.0 版本之前，由于 Lightning 的物理导入模式会“重写历史”，导致 PITR 无法感知到被”重写的历史” ，因此无法对数据进行备份。用户需要在完成数据导入后执行一次全量备份。从 TiDB v8.0.0 版本起，PITR 通过对解析时间戳（ResolvedTs）和 `Ingest SST` 操作进行兼容性设计，使得通过 Lightning 的物理模式导入的数据可以被 PITR 正确的识别、备份和恢复。这项改进为客户提供了更加完善的数据保护和恢复方案。

    更多信息，请参考[用户文档](链接)。

* "不可见索引 (invisible index)"能够在会话级设置可见 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1401-->

    "[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)" 是不能够被优化器选择的索引。通常用在删除索引之前，如果不确定删除索引的操作是否会造成性能回退，可以暂时将该索引修改为不可见，万一需要恢复索引可立即修改回可见状态。
    
    在 v8.0.0 中，如果将新引入的会话级变量 [`tidb_opt_use_invisible_indexes`](/system-variables.md#) 设置为 `ON`，那么在该会话中执行的查询可以选择到"不可见索引"。利用这个能力，在添加新索引时，如果不确定索引的作用，则可以先将索引创建为不可见索引，通过修改会话变量后，在这个会话中对相关的查询语句进行测试，而不影响其他会话的行为。这个扩展改进能够提升性能调优的安全性，增强生产数据库的稳定性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#不可见索引)。

* 支持将 `General Query Log` 写入独立文件 [#issue号](链接) @[Defined2014](https://github.com/Defined2014) **tw@hfxsd** <!--1632-->

   `General Query Log` 是 MySQL 兼容的功能，开启后会记录数据库执行的全部 SQL 语句，为问题诊断提供依据。TiDB 也支持此功能，通过设置变量 [`tidb_general_log`](/system-variables.md#tidb_general_log) 开启，但是在过去的版本中，`General Query Log` 的内容只能和其他信息一起写入实例日志，对需要长期保存的用户并不友好。

   在新版本中，通过把配置项 [`log.general-log-file`]() 设置为有效的文件名，TiDB 可以把 `General Query Log` 写入指定的文件。和实例日志一样，"General Query Log" 也同样遵循日志的轮询和保存策略。
   
   另外，为了减少历史日志文件所占用的磁盘空间，TiDB 在 v8.0.0 支持了原生的日志压缩选项。将配置项 [`log.file.compression`] 设置为 `gzip`，轮询出的历史日志将自动以[`gzip`](https://www.gzip.org/)格式压缩。

        更多信息，请参考[用户文档](链接))。
        
### 可观测性

* 引入对索引使用情况的观测 [#issue号](链接) @[YangKeao](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1400-->

    正确的索引设计是提升数据库性能的重要前提。TiDB 在 v8.0.0 新加入了内存表 [`information_schema.tidb_index_usage`](/information-schema/information-schema-tidb-index-usage.md)，记录每个 TiDB 节点上索引的使用情况，其中包括：
    * 扫描该索引的语句的累计执行次数
    * 累计在该索引中扫描的行数
    * 扫描索引时的选择率分布
    * 索引上次被选择的时间
    
    这些信息能够协助用户识别出没有被优化器选到的索引，以及过滤性很差的索引。另外，本次更新还加入了 MySQL 兼容的视图 [`sys.schema_unused_indexes`](/sys-schema.md)，视图根据所有 TiDB 节点上的索引运行情况，列出节点启动后，所有没有被选择过的索引。
    
    需要注意的几点：
     * 如果用户从 v8.0.0 之前的版本升级上来，`sys` 中的内容不会被自动创建，需要根据[文档]((/sys-schema.md))手动创建。
    * [`information_schema.tidb_index_usage`](/information-schema/information-schema-tidb-index-usage.md) 只在内存中维护，重启 TiDB 节点后该节点的信息会丢失。
    * [`information_schema.tidb_index_usage`](/information-schema/information-schema-tidb-index-usage.md) 默认会被维护。可以通过修改配置项 [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info) 或者变量[`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) 将其关闭。
   

    更多信息，请参考[用户文档](/information-schema/information-schema-tidb-index-usage.md)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移
* DM 支持使用用户提供的密钥对源和目标数据库的密码进行加密和解密 [#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1497-->

    之前 DM 使用的是自带的一个固定秘钥，安全性较低。而从 8.0 版本开始，用户可以传入自定义的密钥文件，对上下游的数据库的密码进行加密和解密操作，也可以按需替换秘钥，提升了安全性。

    更多信息，请参考[用户文档](链接)。

* Import into 功能增强，支持 Import into... from select 语法 [#49883](https://github.com/pingcap/tidb/issues/49883) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1680-->

    在一些大数据量的场景使用 insert into ... select，数据导入的性能较慢，而从 8.0 版本开始，支持用户使用 Import into... from select 来导入查询结果到目标表中，且导入的性能最高可达  insert into ... select 的 8 倍，大大缩短了把查询结果导入目标表的所需时间。此外，该功能还支持导入使用 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

    更多信息，请参考[用户文档](链接)。        
    
* Lightning 冲突策略简化，同时支持 Replace 的方式处理冲突的数据 [#issue 号](链接) @[lyzx2001](https://github.com/lyzx2001) **tw@qiancai** <!--1684-->

    原先 Lightning 逻辑导入模式时有一套冲突处理策略，物理导入模式时也有一套冲突策略，同时物理导入模式还有一套前置冲突策略，导致用户配置复杂。从 8.0 开始，将这 3 种冲突策略合并成了一套，简化了用户的配置操作。同时在物理导入模式下，还首次引入了通过 replace 的方式处理导入过程中冲突的数据。

    更多信息，请参考[用户文档](链接)。    
    
  * 全局功能称为正式功能（GA），可提升 import into 任务的导入性能和稳定性，支持 40 TiB 的数据导入 [#i45719](https://github.com/pingcap/tidb/issues/45719) @[lance6716](https://github.com/lance6716) **tw@qiancai** <!--1684-->

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

* 行为变更 1

* 行为变更 2

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_opt_use_invisible_indexes`](/system-variables.md#) | 新增 | 控制会话中是否能够选择[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)。当修改变量为`ON`时，针对该会话执行的查询，优化能够使用[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)进行优化。|
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB  |  [`log.general-log-file`]() | 新增 | 指定 `General Query Log` 的保存文件。默认为空，`General Query Log` 将会写入实例文件。 |
| TiDB  |  [`log.file.compression`]() | 新增 | 指定轮询日志的压缩格式。默认为空，即不压缩轮询日志。 |

### 其他

## 离线包变更

## 废弃功能

* 从 v8.0.0 开始，[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 变量被废弃。废弃后，TiDB 不再支持乐观事务的自动重试。作为替代，当使用乐观事务模式发生冲突时，请在应用里捕获错误并重试，或改用[悲观事务模式](/pessimistic-transaction.md)。**tw@lilin90** <!--1671-->
* 从 v8.0.0 开始，TiDB 不再支持 TLSv1.0 和 TLSv1.1 协议。请升级 TLS 至 TLSv1.2 或 TLSv1.3。
* 废弃功能 1

* 废弃功能 2

## 改进提升

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - 优化 Sort 算子的数据落盘性能 [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1609-->
    - 优化数据落盘功能的退出机制，提升数据落盘时取消查询的性能 [#50511](https://github.com/pingcap/tidb/issues/50511) @[wshwsh12](https://github.com/wshwsh12) **tw@qiancai** <!--1635-->
    - 用多个等值条件做表连接时，支持利用匹配到部分条件的索引做 Index Join [#47233](https://github.com/pingcap/tidb/issues/47233) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--1601-->
    - Index Join 允许被连接的一侧为聚合数据集 [#37068](https://github.com/pingcap/tidb/issues/37068) @[elsa0520](https://github.com/elsa0520) **tw@Oreoxmt** <!--1510-->


+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
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

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

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