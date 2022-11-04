---
title: TiDB 6.4.0 Release Notes
---

# TiDB v6.4.0 Release Notes

发版日期：2022 年 x 月 xx 日

TiDB 版本：6.4.0-DMR

在 6.4.0-DMR 版本中，你可以获得以下关键特性：

- TiDB 全局内存限制
- TiFlash 静态加密支持国密算法 SM4。
- 支持通过 FLASHBACK CLUSTER 命令将集群快速回退到过去某一个指定的时间点
- 关键特性 3
- ......

## 新功能

### SQL

* 支持通过 SQL 语句对指定 Partition 的 TiFlash 副本立即触发物理数据整理 (Compaction)

    v6.2.0 版本发布了针对全表的 TiFlash 副本立即触发 [物理数据整理 (Compaction)](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) 功能，支持用户自行选择合适的时机、手动执行 SQL 语句来对 TiFlash 中的物理数据立即进行整理，从而减少存储空间占用，并提升查询性能。v6.4.0 版本细化了 TiFlash 副本物理数据整理的粒度，支持对表中的指定 Partition 的 TiFlash 副本立即触发物理数据整理。
    通过 SQL 语句 `ALTER TABLE table_name COMPACT [PARTITION PartitionNameList] [engine_type REPLICA]` 可以立即触发指定 Partition 的 TiFlash 副本物理数据整理。

    [用户文档](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) [#5315](https://github.com/pingcap/tiflash/issues/5315) @[hehechen](https://github.com/hehechen)

* 支持通过 FLASHBACK CLUSTER 命令将集群快速回退到过去某一个指定的时间点

    FLASHBACK CLUSTER 支持在 Garbage Collection (GC) life time 时间内，快速回退整个集群到指定的时间点。使用该特性可以轻松快速撤消 DML 误操作，例如，用户误执行了没有 WHERE 子句的 DELETE，FLASHBACK CLUSTER 能够在几分钟内回退原数据库集群到指点时间点。该特性不依赖于数据库备份，支持在时间线上反复回退以确定特定数据更改发生的时间。FLASHBACK CLUSTER 不能替代数据库备份。[#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303)  @[Defined2014](https://github.com/Defined2014) @[bb7133](https://github.com/bb7133) @[JmPotato](https://github.com/JmPotato) @[Connor1996](https://github.com/Connor1996) @[HuSharp](https://github.com/HuSharp) @[CalvinNeo](https://github.com/CalvinNeo)

    [用户文档](/sql-statements/sql-statement-flashback-to-timestamp.md)

### 安全

* TiKFlash 静态加密支持国密算法 SM4

    TiFlash 的静态加密新增 SM4 算法，用户可以修改配置文件 tiflash-learner.toml 中的 data-encryption-method 参数，设置为 sm4-ctr，以启用基于国密算法 SM4 的静态加密能力。 [#5953](https://github.com/pingcap/tiflash/issues/5953) @[lidezhu](https://github.com/lidezhu)

    [用户文档](/encryption-at-rest.md)

### 可观测性

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 性能

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

* 增加了动态规划算法来决定表的连接顺序

    在之前的版本中， TiDB 采用贪心算法来决定表的连接顺序。 在版本 v6.4.0 中， 优化器引入了[动态规划算法](/join-reorder.md#join-reorder-算法实例)，相比贪心算法， 动态规划算法会枚举更多可能的连接顺序，进而有机会发现更好的执行计划，提升部分场景下 SQL 执行效率。

    由于动态规划算法的枚举过程可能消耗更多的时间，目前 Join Reorder 算法由变量 [`tidb_opt_join_reorder_threshold`](/system-variables.md#tidboptjoinreorderthreshold) 控制，当参与 Join Reorder 的节点个数大于该阈值时选择贪心算法，反之选择动态规划算法。

    [#18969](https://github.com/pingcap/tidb/issues/18969) @[winoros](https://github.com/winoros)

    [用户文档](/join-reorder.md)

* 前缀索引支持对空值的过滤

    这是对前缀索引使用上的优化。当表中某列存在前缀索引，那么 SQL 中对该列的 `IS NULL` 或 `IS NOT NULL` 条件可以直接利用前缀进行过滤，避免了这种情况下的回表，提升了 SQL 的执行性能。 [#21145](https://github.com/pingcap/tidb/issues/21145) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    [用户文档](/system-variables.md#tidboptpreindexsinglescan-span-classversion-mark从-v640-版本开始引入span)

### 事务

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 稳定性

* 磁盘故障，I/O 无响应等极端情况下的故障恢复加速

    数据库的可用性是企业用户最为关注的指标之一，但是在复杂的硬件环境下，如何快速检测故障，快速恢复一直是数据库面临的挑战之一。TiDB 在 6.4 版本，全面优化了 TiKV 节点的状态检测机制，即使在磁盘故障，I/O 无响应等极端情况，依然可以快速上报节点状态，同时搭配主动唤醒机制，提前发起选主，加速集群自愈。通过这次优化，TiDB 在磁盘故障场景下，集群恢复时间可以缩短 50% 左右。 [#issue]() @[贡献者 GitHub ID]()

* TiDB 全局内存限制

    在 v6.4.0 中，我们引入了一个实验特性，对 TiDB 实例的全局内存使用进行追踪。 用户可以通过系统变量 [`tidb_server_memory_limit`](/system-variables.md#tidbservermemorylimit-span-classversion-mark从-v640-版本开始引入span) 设置全局内存的使用上限。 当内存使用量逼近预设的上限时， TiDB 会尝试对内存进行回收，释放更多的可用内存； 当内存使用量超出预设的上限时， TiDB 会识别出当前内存使用量最大的 SQL 操作，并取消这个操作，避免因为内存使用过度而产生的系统性问题。

    同时，TiDB 提供了视图 [`information_schame.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md) 和 [`information_schame.MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md) 用来展示内存使用情况及历史操作， 可以帮助客户清晰了解内存使用状况。

    全局内存限制是 TiDB 内存管理的重要一步， 实例采用全局视角，引入系统性方法对内存的使用进行管理， 这将会极大提升数据库的稳定性，提高服务的可用性，支持 TiDB 在更多重要场景平稳运行。

    [#37816](https://github.com/pingcap/tidb/issues/37816) @[wshwsh12](https://github.com/wshwsh12)

    [用户文档](/configure-memory-usage.md)

* 控制优化器在构造范围时的内存占用

    v6.4.0 引入了系统变量 [`tidb_opt_range_max_size`](/system-variables.md#tidb-opt-range-max-size-从-v640-版本开始引入) 用来限制优化器在构造范围时消耗的内存上限。 当内存使用超出这个限制，则放弃构造精确的范围，转而构建更粗粒度的范围，以此降低内存消耗。 当 SQL 中的 `IN` 条件特别多时， 这个优化可以显著降低编译时的内存使用量，保证系统的稳定性。 [#37176](https://github.com/pingcap/tidb/issues/37176) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    [用户文档](/system-variables.md#tidb-opt-range-max-size-从-v640-版本开始引入)

### 易用性

* TiKV API V2 GA

    在 v6.1.0 之前，TiKV 的 RawKV 接口仅存储客户端传入的原始数据，因此只提供基本的 Key Value 读写能力。此外，由于编码方式不同、数据范围没有隔离，因此在同一个 TiKV 集群中，TiDB、事务 KV、RawKV 无法同时使用，对于不同使用方式并存的场景，必须部署多套集群，增加了机器和部署成本。

    TiKV API V2 提供了新的存储格式，包括：

    * RawKV 数据以 MVCC 方式存储，记录数据的变更时间戳，并在此基础上提供 Change Data Capture 能力（实验特性，见 [TiKV-CDC](https://github.com/tikv/migration/blob/main/cdc/README.md)）。
    * 数据根据使用方式划分范围，支持单一集群 TiDB、事务 KV、RawKV 应用共存。
    * 预留 Key Space 字段，可以为多租户等特性提供支持。

    使用 TiKV API V2 请在 TiKV 的 `[storage]` 配置中增加或修改 `api-version = 2`。详见[用户文档](/tikv-configuration-file.md#api-version-从-v610-版本开始引入)。

  <Warning>

    * 由于底层存储格式发生了重大变化，因此仅当 TiKV 只有 TiDB 数据时，可以平滑启用或关闭 API V2。其他情况下，需要新建集群，并使用 [TiKV-BR](https://github.com/tikv/migration/blob/main/br/README-cn.md) 进行数据迁移。

    * 启用 API V2 后，不能将 TiKV 集群回退到 v6.1.0 之前的版本，否则可能导致数据损坏。

  </Warning>

    [#11745](https://github.com/tikv/tikv/issues/11745) @[pingyu](https://github.com/pingyu)

    [用户文档](/tikv-configuration-file.md#api-version-从-v610-版本开始引入)

* 优化 TiFlash 数据同步进度的准确性

    TiDB 的 `information_schema.tiflash_replica` 表中的 `PROGRESS` 字段表示 TiFlash 副本与 TiKV 中对应表数据的同步进度。在之前的版本中，`PROCESS` 字段只显示 TiFlash 副本创建过程中的数据同步进度。在 TiFlash 副本创建完后，当在 TiKV 相应的表中导入新的数据时，该值不会更新数据的同步进度。
    v6.3.0 版本改进了 TiFlash 副本数据同步进度更新机制，在创建 TiFlash 副本后，进行数据导入等操作，TiFlash 副本需要和 TiKV 数据进行同步时，[`information_schema.tiflash_replica`](/information-schema/information-schema-tiflash-replica.md) 表中的 `PROGRESS` 值将会更新，显示实际的数据同步进度。通过此优化，你可以方便地查看 TiFlash 数据同步的实际进度。

    [用户文档](/information-schema/information-schema-tiflash-replica.md) [#4902](https://github.com/pingcap/tiflash/issues/4902) @[hehechen](https://github.com/hehechen)

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### MySQL 兼容性

* TiDB 分区表兼容 Linear Hash 分区

    TiDB 现有的分区方式支持 Hash，Range，List 分区。TiDB v6.4.0 增加了对 [MySQL Linear Hash](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html) 分区语法的兼容，方便原 MySQL 用户迁移到 TiDB。
    用户现有的 MySQL Linear Hash 分区的 DDL 可以不经修改直接在 TiDB 上执行，产生一个 TiDB Hash 分区表（TiDB 内部实际不存在 Linear Hash 分区）。用户已有的查询/访问原 Linear Hash 分区的 SQL（DML）也可以不经修改，直接访问对应的 TiDB Hash 分区，得到正常结果。此功能保证了对 MySQL Linear Hash 分区的语法兼容，方便用户的应用无缝迁移到 TiDB。[#issue](https://github.com/pingcap/tidb/issues/38450) @[贡献者 GitHub ID](mjonss)

    [用户文档](/mysql-compatibility.md)

* 支持高性能、全局单调递增的 AUTO_INCREMENT 列属性

    TiDB 现有的 AUTO_INCREMENT 列属性的全局单调性和性能不可兼得，提供高性能、全局单调递增的 AUTO_INCREMENT 列属性能够更完美的兼容 MySQL AUTO_INCREMENT 的功能，降低用户从 MySQL 迁移到 TiDB 的改造成本。例如，使用该特性能够轻松解决用户的查询结果需要按照自增 ID 排序的问题。[#38442](https://github.com/pingcap/tidb/issues/38442) @[tiancaiamao](https://github.com/tiancaiamao)

    [用户文档](/auto-increment.md#mysql-兼容模式)

* 对 JSON 类型中的 Array 做范围选择

    新版本支持 MySQL 兼容的范围选择语法。 用关键字 `to` 指定元素起始和结束的位置，用来选择 Array 中连续范围的元素，起始位置记为 `0` 。 比如 `$[0 to 2]` 选择 Array 中的前三个元素。  `last` 关键字代表 Array 中最后一个元素的位置，能够实现从右到左的位置设定, 比如 `$[last-2 to last]` 用来选择最后三个元素。 这个能力简化了 SQL 的编写能力，进一步提升的 JSON 类型的兼容能力，降低了 MySQL 应用向 TiDB 迁移的难度。

    [用户文档](/data-type-json.md)

* 支持对数据库用户增加额外说明

    新版本扩展了 `Create User` 和 `Alter User` 的语法，能够为数据库用户添加额外的说明。 说明支持两种格式，利用 `COMMENT` 添加一段文本，或者用 `ATTRIBUTE` 添加一组 JSON 格式的结构化属性。 这个特性加强了 TiDB 对 MySQL 的语法的兼容性， 使得 TiDB 更容易融入 MySQL 生态的工具或平台。 [#38172](https://github.com/pingcap/tidb/issues/38172) @[CbcWestwolf](https://github.com/CbcWestwolf)

    [用户文档](/information-schema/information-schema-user-attributes.md)

### 备份和恢复

* 基于 AWS EBS snapshot 的集群备份和恢复

    如果你的TiDB 集群部署在 EKS 上，使用了 AWS EBS 卷，并且对数据备份有以下要求，可考虑使用 TiDB Operator 将 TiDB 集群数据以卷快照以及元数据的方式备份至 AWS S3：

    - 备份的影响降到最小，如备份对 QPS 和事务耗时影响小于 5%，不占用集群 CPU 以及内存。
    - 快速备份和恢复，比如 1 小时内完成备份，2 小时内完成恢复。

     [#issue](https://github.com/pingcap/tidb/issues/33849) @[fengou1](https://github.com/fengou1)

    [用户文档](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)

### 数据迁移

* 支持在分库分表迁移场景，下游的表支持增加扩展列并赋值，用于标记下游表中的记录来之上游哪个分库分表。

    在上游分库分表合并到 TiDB 的场景，用户可以在目标表手动额外增加几个字段（扩展列），并在配置 DM 任务时，对这几个扩展列赋值，如赋予上游分库分表的名称，则通过 DM 写入到下游的记录会带上上游分库分表的名称，在一些数据异常的场景，用户可以通过该功能快速定位目标表的问题数据时来自于上游哪个分库分表。） [#37790](https://github.com/pingcap/tidb/pull/37790) @lichunzhu

    [用户文档](https://github.com/pingcap/docs-cn/pull/11536/files)

* 优化 DM 的前置检查项,将部分必须通过项改为非必须通过项。

    将“检查字符集是否存在兼容性差异”、“检查上游表中是否存在主键或唯一键约束”，“数据库主从配置，上游数据库必须设置数据库 ID server_id” 这 3 个前置检查从必须通过项，改为非必须通过项，提升用户前置检查的通过率。 [#无](无) @lichunzhu

    用户文档无，对用户无感知

* 解决了上游数据库的建表 sql  TiDB 不兼容，导致 DM 全量迁移报错的问题。[#issue](https://github.com/pingcap/tidb/issues/37984) @lance6716

    DM 会默认使用上游数据库的建表 SQL 去 TiDB 执行，帮用户创建好目标表。当上游的建表 SQL  TiDB 不兼容时，DM 使用该 SQL 帮用户创建目标表会失败，导致 DM 任务中断。这时候用户可以提前在 TiDB 手动创建好目标表，DM 检查到已存在的目标表时会忽略掉这个建表 SQL 报错，让全量迁移任务继续运行。

    [用户文档](https://github.com/pingcap/docs-cn/pull/11718
    https://github.com/pingcap/docs/pull/10974)

* 配置DM 增量迁移任务，支持 binlog_name 和 GTID 的参数可作为选配项。

    用户只配置 DM 增量迁移任务时，如果不指定 binlog_name 和 GTID 的参数取值，则默认按任务的启动时间去上游获取该时间之后的 binlog file，并将这些增量数据迁移到下游 ，降低了用户的理解成本和配置复杂度。
    [#7393](https://github.com/pingcap/tiflow/issues/7393) @GMHDBJD

    [用户文档](
    https://github.com/pingcap/docs-cn/pull/11790
    https://github.com/pingcap/docs/pull/11096)

* DM 任务增加一些状态信息的展示

    * 增加了  DM 任务当前数据导出、数据导入的性能，单位 bytes / s
    * 将当前  DM 写入目标库的性能指标命名 从 TPS 改为 RPS （rows / second）
    * 新增了 DM 全量任务数据导出的进度展示
         [#7343](https://github.com/pingcap/tiflow/issues/7343) @okJiang

         [用户文档](https://github.com/pingcap/docs-cn/pull/11755,
https://github.com/pingcap/docs/pull/11123)

### 数据共享与订阅

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 部署及运维

* 集群诊断功能 GA

    集群诊断功能是在指定的时间范围内，对集群可能存在的问题进行诊断，并将诊断结果和一些集群相关的负载监控信息汇总成一个诊断报告。诊断报告是网页形式，通过浏览器保存后可离线浏览和传阅。

    用户可以通过该报告快速了解集群内的基本诊断信息，包括负载、组件、耗时和配置信息。若用户的集群存在一些常见问题，在[诊断信息](https://docs.pingcap.com/zh/tidb/stable/dashboard-diagnostics-report#%E8%AF%8A%E6%96%AD%E4%BF%A1%E6%81%AF)部分可以了解 TiDB 内置自动诊断的结果。

    详细内容见[用户文档](https://docs.pingcap.com/zh/tidb/stable/dashboard-diagnostics-access)

## 兼容性变更

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`last_sql_use_alloc`](/system-variables.md#last_sql_use_alloc-从-v640-版本开始引入) | 新增 | 这个变量是一个只读变量，用来显示上一个语句是否使用了缓存的 Chunk 对象 (Chunk allocation)。 |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-从-v640-版本开始引入) | 新增 | 该变量用于设置 TiDB [自动 analyze](/statistics.md#自动更新) 分区表（即自动收集分区表上的统计信息）时，每次同时 analyze 分区的个数。 |
| [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-从-v640-版本开始引入) | 新增 | 默认值为`OFF`。当此变量设置为 `ON` 时，TiDB 会读取 [`tidb_external_ts`](/system-variables.md#tidb_external_ts-从-v640-版本开始引入) 指定时间戳前的历史数据。 |
| [`tidb_enable_gogc_tuner`](/system-variables.md#tidb_enable_gogc_tuner-从-v640-版本开始引入) | 新增 | 这个变量用来控制 GOGC Tuner 自动调节的最大内存阈值，超过阈值后 GOGC Tuner 会停止工作。 |
| [`tidb_enable_reuse_chunk`](/system-variables.md#last_sql_use_alloc-从-v640-版本开始引入) | 新增 | 该变量用于控制 TiDB 是否启用 Chunk 对象缓存，默认为 `ON`，代表 TiDB 优先使用缓存中的 Chunk 对象，缓存中找不到申请的对象时才会从系统内存中申请。如果为 `OFF`，则直接从系统内存中申请 Chunk 对象。 |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-从-v610-版本开始引入) | 修改 | 这个变量用来控制是否开启 [Prepared Plan Cache](/sql-prepared-plan-cache.md)。v6.4.0 新增了 SESSION 作用域。 |
| [`tidb_enable_prepared_plan_cache_memory_monitor`](/system-variables.md#tidb_enable_prepared_plan_cache_memory_monitor-从-v640-版本开始引入) | 新增 | 这个变量用来控制是否统计 Prepared Plan Cache 中所缓存的执行计划占用的内存。|
| [`tidb_gogc_tuner_threshold`](/system-variables.md#tidb_gogc_tuner_threshold-从-v640-版本开始引入) | 新增 | 该变量来用控制是否开启 GOGC Tuner，默认为 ON。 |
| [`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-从-v640-版本开始引入) | 新增 | 当 tidb-server 内存占用超过内存报警阈值并触发报警时，TiDB 默认只保留最近 5 次报警时所生成的状态文件。通过该变量可以调整该次数。 |
| [`tidb_opt_agg_push_down`](/system-variables.md#tidboptaggpushdown) | 修改 | 这个变量用来设置优化器是否执行聚合函数下推到 Join，Projection 和 UnionAll 之前的优化操作。本次增加了 Global 的作用域。 |
| [`tidb_opt_prefix_index_single_scan`](/system-variables.md#tidb-opt-prefix-index-single-scan-从-v640-版本开始引入) | 新增 | 这个变量默认开启，用于控制 TiDB 优化器是否将某些过滤条件下推到前缀索引，尽量避免不必要的回表，从而提高查询性能。 |
| [`tidb_opt_range_max_size`](/system-variables.md#tidb-opt-range-max-size-从-v640-版本开始引入) | 新增 | 该变量用于指定优化器构造扫描范围的内存用量上限。当该变量为 `0` 时，表示对扫描范围没有内存限制。如果构造精确的扫描范围会超出内存用量限制，优化器会使用更宽松的扫描范围。 |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_enable_prepared_plan_cache-从-v610-版本开始引入) | 修改 | 这个变量用来控制单个 `SESSION` 的 Prepared Plan Cache 最多能够缓存的计划数量。v6.4.0 新增了 SESSION 作用域。|
| [`tidb_server_memory_limit`](/system-variables.md#tidb-server-memory-limit-从-v640-版本开始引入) | 新增 | 该变量指定 TiDB 实例的内存限制。TiDB 会在内存用量达到该限制时，对当前内存用量最高的 SQL 语句进行取消 (Cancel) 操作。 |
| [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb-server-memory-limit-gc-trigger-从-v640-版本开始引入) | 新增 | 该变量用于控制 TiDB 尝试触发 GC 的阈值。当 TiDB 的内存使用达到 `tidb_server_memory_limit` 值 \* `tidb_server_memory_limit_gc_trigger` 值时，则会主动触发一次 Golang GC。在一分钟之内只会主动触发一次 GC。|
| [`tidb_server_memory_limit_sess_min_size`](tidb-server-memory-limit-session-min-size-从-v640-版本开始引入) | 新增 | 开启内存限制后，TiDB 会终止当前实例上内存用量最高的 SQL 语句。本变量指定此情况下 SQL 语句被终止的最小内存用量。 |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-从-v540-版本开始引入) | 修改 | 该变量默认值从 `OFF` 修改为 `ON`，表示统计信息同步加载超时后，TiDB 默认使用 pseudo 的统计信息（`ON`）。 |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-从-v540-版本开始引入) | 修改 | 该变量默认值从 `0` 修改为 `100`，代表 SQL 执行同步加载完整统计信息默认等待 100 毫秒后会超时。 |
| [`tidb_external_ts`](/system-variables.md#tidb_external_ts-从-v640-版本开始引入) | 新增 | 默认值：`0`。当 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-从-v640-版本开始引入) 设置为 `ON` 时，TiDB 会依据该变量指定的时间戳读取历史数据。 |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-从-v630-版本开始引入) | 修改 | 这个变量从 v6.4.0 开始生效，用来控制 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) 的并发数。默认值为 `64`。 |
| [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) | 修改 | 该变量用于设置触发 tidb-server 内存告警的内存使用比率，默认值从 `0.8` 修改为`0.7`。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`tidb_max_reuse_chunk`](/tidb-configuration-file.md#tidb_max_reuse_chunk-从-v640-版本开始引入) | 新增 | 用于控制每个连接最多缓存的 Chunk 对象数，默认值为 64。配置过大会增加 OOM 的风险。 |
| TiDB | [`tidb_max_reuse_column`](/tidb-configuration-file.md#tidb_max_reuse_column-从-v640-版本开始引入) | 新增 | 用于控制每个连接最多缓存的 column 对象数，默认值为 256。配置过大会增加 OOM 的风险。 |
| TiDB | `memory-usage-alarm-ratio` | 废弃 | 自 v6.4.0 版本起该配置项被废弃，被系统变量 [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) 所取代。|
| TiDB | [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-从-v409-版本开始引入) | 废弃 | 自 v6.4.0 版本起该配置项被废弃，被系统变量 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 所取代。|
| TiKV | [`alloc-ahead-buffer`](/tikv-configuration-file.md#alloc-ahead-buffer-从-v640-版本开始引入) | 新增 | TiKV 预分配给 TSO 的缓存大小（以时长计算），默认值为 3 秒。|
| TiKV | [`apply-yield-write-size`](#apply-yield-write-size-从-v640-版本开始引入) | 新增 | Apply 线程每一轮处理单个状态机写入的最大数据量，这是个软限制。 |
| TiKV | [`renew-batch-max-size`](/tikv-configuration-file.md#renew-batch-max-size-从-v640-版本开始引入)| 新增 | 单次时间戳请求的最大数量，默认值为 8192。 |
| TiKV | [`raw-min-ts-outlier-threshold`](/tikv-configuration-file.md#raw-min-ts-outlier-threshold-从-v620-版本开始引入) | 废弃 | 废弃对 RawKV 的 Resolved TS 进行异常检测的阈值。|
| PD | [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval) | 新增 | TSO 物理时钟更新周期，默认值为 50ms。 |
| TiFlash | [data-encryption-method](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) | 修改 | 扩展可选值范围：增加 sm4-ctr。设置为 sm4-ctr 时，数据将采用国密算法 SM4 加密后进行存储。 |

### 其他

- TiCDC 下游可支持的 Kafka 的最高版本从 `3.1.0` 变为 `3.2.0`。
- 从 v6.4.0 开始，TiCDC 使用 Syncpoint 功能需要同步任务拥有下游集群的 `SYSTEM_VARIABLES_ADMIN` 或者 `SUPER` 权限。

## 废弃功能

## 改进提升

+ TiDB

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ TiKV

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ PD

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ TiFlash

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ Tools

    + TiDB Dashboard
        - Monitoring 页面展示 TiFlash 相关指标，并且优化指标的展示方式。 [#1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @[baurine](https://github.com/baurine)
        - 在 Slow Query 列表 和 SQL Statement 列表展示结果行数。 [#1407](https://github.com/pingcap/tidb-dashboard/pull/1407) @[baurine](https://github.com/baurine)
        - 优化 Dashboard 的报错信息。  [#1407](https://github.com/pingcap/tidb-dashboard/pull/1407) @[baurine](https://github.com/baurine)

    + Backup & Restore (BR)

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiCDC

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Data Migration (DM)

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Lightning

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiUP

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

## 错误修复

+ TiDB

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ TiKV

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ PD

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ TiFlash

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ Tools

    + TiDB Dashboard

        - 避免查询 Statement 执行计划的时候造成 TiDB OOM。 [#1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @[baurine](https://github.com/baurine)

    + Backup & Restore (BR)

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiCDC

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Data Migration (DM)

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Lightning

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiUP

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()
