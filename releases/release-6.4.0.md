---
title: TiDB 6.4.0 Release Notes
---

# TiDB 6.4.0 Release Notes

发版日期：2022 年 11 月 17 日

TiDB 版本：6.4.0-DMR

> **注意：**
>
> TiDB 6.4.0-DMR 的用户文档已[归档](https://docs-archive.pingcap.com/zh/tidb/v6.4)。如无特殊需求，建议使用 TiDB 数据库的[最新 LTS 版本](https://docs.pingcap.com/zh/tidb/stable)。

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.4/quick-start-with-tidb)

在 6.4.0-DMR 版本中，你可以获得以下关键特性：

- 支持通过 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md) 命令将集群快速回退到特定的时间点 (实验特性）。
- 支持对 TiDB 实例的[全局内存使用进行追踪](/configure-memory-usage.md)（实验特性）。
- TiDB 分区表[兼容 LINEAR HASH 分区语法](/partitioned-table.md#tidb-对-linear-hash-分区的处理)。
- 支持高性能、全局单调递增的 [`AUTO_INCREMENT`](/auto-increment.md#mysql-兼容模式) 列属性（实验特性）。
- 支持对 [JSON 类型](/data-type-json.md)中的 Array 数据做范围选择。
- 实现磁盘故障、I/O 无响应等极端情况下的故障恢复加速。
- 新增[动态规划算法](/join-reorder.md#join-reorder-动态规划算法实例)来决定表的连接顺序。
- 引入[新的优化器提示 `NO_DECORRELATE`](/optimizer-hints.md#no_decorrelate) 来控制关联优化的解除。
- [集群诊断功能](/dashboard/dashboard-diagnostics-access.md) GA。
- [TiFlash 静态加密](/encryption-at-rest.md#tiflash)支持国密算法 SM4。
- 支持通过 SQL 语句立即对指定分区的 TiFlash 副本进行[物理数据整理 (Compaction)](/sql-statements/sql-statement-alter-table-compact.md)。
- 支持[基于 AWS EBS snapshot 的集群备份和恢复](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)。
- 支持在分库分表合并迁移场景中[标记下游表中的数据来自上游哪个分库、分表和数据源](/dm/dm-table-routing.md#提取分库分表数据源信息写入合表)。

## 新功能

### SQL

* 支持通过 SQL 语句立即对指定分区的 TiFlash 副本进行物理数据整理 (Compaction) [#5315](https://github.com/pingcap/tiflash/issues/5315) @[hehechen](https://github.com/hehechen)

    TiDB v6.2.0 发布了针对全表的 TiFlash 副本立即进行[物理数据整理 (Compaction)](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) 的功能，支持用户自行选择合适的时机，手动执行 SQL 语句立即对 TiFlash 中的物理数据进行整理，从而减少存储空间占用，并提升查询性能。v6.4.0 细化了 TiFlash 副本数据整理的粒度，支持对表中指定分区的 TiFlash 副本立即进行数据整理。

    通过 SQL 语句 `ALTER TABLE table_name COMPACT [PARTITION PartitionNameList] [engine_type REPLICA]`，你可以立即对指定分区的 TiFlash 副本进行数据整理。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-alter-table-compact.md#对分区表中指定分区的-tiflash-副本进行数据整理)。

* 支持通过 `FLASHBACK CLUSTER TO TIMESTAMP` 命令将集群快速回退到特定的时间点（实验特性）[#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303) @[Defined2014](https://github.com/Defined2014) @[bb7133](https://github.com/bb7133) @[JmPotato](https://github.com/JmPotato) @[Connor1996](https://github.com/Connor1996) @[HuSharp](https://github.com/HuSharp) @[CalvinNeo](https://github.com/CalvinNeo)

    `FLASHBACK CLUSTER TO TIMESTAMP` 支持在 Garbage Collection (GC) life time 内快速回退整个集群到指定的时间点。使用该特性可以快速撤消 DML 误操作。例如，在误执行了没有 `WHERE` 子句的 `DELETE` 后，使用 `FLASHBACK CLUSTER TO TIMESTAMP` 能够在几分钟内将集群数据恢复到指定的时间点。该特性不依赖于数据库备份，并支持在时间线上多次回退以确定特定数据更改发生的时间。需要注意的是，`FLASHBACK CLUSTER TO TIMESTAMP` 不能替代数据库备份。

    在执行 `FLASHBACK CLUSTER TO TIMESTAMP` 之前，需要暂停 PITR 和 TiCDC 等工具上运行的同步任务，待 `FLASHBACK` 执行完成后再启动，否则会造成同步失败等问题。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-flashback-cluster.md)。

* 支持通过 `FLASHBACK DATABASE` 命令来恢复被删除的数据库 [#20463](https://github.com/pingcap/tidb/issues/20463) @[erwadba](https://github.com/erwadba)

    `FLASHBACK DATABASE` 支持在 Garbage Collection (GC) life time 时间内恢复被 `DROP` 删除的数据库以及数据。该特性不依赖任何外部工具，可以轻松快速地通过 SQL 语句进行数据和元信息的恢复。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-flashback-database.md)。

### 安全

* TiFlash 静态加密支持国密算法 SM4 [#5953](https://github.com/pingcap/tiflash/issues/5953) @[lidezhu](https://github.com/lidezhu)

    TiFlash 的静态加密新增 SM4 算法，你可以将配置文件 `tiflash-learner.toml` 中的 `data-encryption-method` 参数的值设置为 `sm4-ctr`，以启用基于国密算法 SM4 的静态加密能力。

    更多信息，请参考[用户文档](/encryption-at-rest.md#tiflash)。

### 可观测性

* 集群诊断功能 GA [#1438](https://github.com/pingcap/tidb-dashboard/issues/1438) @[Hawkson-jee](https://github.com/Hawkson-jee)

    [集群诊断功能](/dashboard/dashboard-diagnostics-access.md)是在指定的时间范围内，对集群可能存在的问题进行诊断，并将诊断结果和一些集群相关的负载监控信息汇总成一个[诊断报告](/dashboard/dashboard-diagnostics-report.md)。诊断报告是网页形式，通过浏览器保存后可离线浏览和传阅。

    你可以通过该报告快速了解集群内的基本诊断信息，包括负载、组件、耗时和配置信息。若集群存在一些常见问题，在[诊断信息](/dashboard/dashboard-diagnostics-report.md#诊断信息)部分可以了解 TiDB 内置自动诊断的结果。

### 性能

* 引入 Coprocessor Task 并发度自适应机制 [#37724](https://github.com/pingcap/tidb/issues/37724) @[you06](https://github.com/you06)

    随着 Coprocessor Task 任务数增加，TiDB 将结合 TiKV 处理速度自动增加任务并发度（调整 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)），减少 Coprocessor Task 任务排队，降低延迟。

* 新增动态规划算法来决定表的连接顺序 [#37825](https://github.com/pingcap/tidb/issues/37825) @[winoros](https://github.com/winoros)

    在之前的版本中，TiDB 采用贪心算法来决定表的连接顺序。在 v6.4.0 中，优化器引入了[动态规划算法](/join-reorder.md#join-reorder-动态规划算法实例)。相比贪心算法，动态规划算法会枚举更多可能的连接顺序，进而有机会发现更好的执行计划，提升部分场景下 SQL 执行效率。

    由于动态规划算法的枚举过程可能消耗更多的时间，目前 Join Reorder 算法由变量 [`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold) 控制，当参与 Join Reorder 的节点个数大于该阈值时选择贪心算法，反之选择动态规划算法。

    更多信息，请参考[用户文档](/join-reorder.md)。

* 前缀索引支持对空值进行过滤 [#21145](https://github.com/pingcap/tidb/issues/21145) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    该特性是对前缀索引使用上的优化。当表中某列存在前缀索引，那么 SQL 语句中对该列的 `IS NULL` 或 `IS NOT NULL` 条件可以直接利用前缀进行过滤，避免了这种情况下的回表，提升了 SQL 语句的执行性能。

    更多信息，请参考[用户文档](/system-variables.md#tidb_opt_prefix_index_single_scan-从-v640-版本开始引入)。

* 增强 TiDB Chunk 复用机制 [#38606](https://github.com/pingcap/tidb/issues/38606) @[keeplearning20221](https://github.com/keeplearning20221)

    在之前的版本中，TiDB 只在 `writechunk` 函数中复用 Chunk。TiDB v6.4.0 扩展 Chunk 复用机制到 Executor 的算子中，通过复用 Chunk 减少 TiDB 申请释放内存频率，进而提升部分场景下的 SQL 查询执行效率。你可以通过系统变量 [`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-从-v640-版本开始引入) 来控制是否启用 Chunk 对象复用，默认为开启。

* 引入新的优化器提示 `NO_DECORRELATE` 来控制关联优化的解除 [#37789](https://github.com/pingcap/tidb/issues/37789) @[time-and-fate](https://github.com/time-and-fate)

    默认情况下，TiDB 总是会尝试重写关联子查询以解除关联，这通常会提高执行效率。但是在一部分场景下，解除关联反而会降低执行效率。TiDB 在 v6.4.0 版本中引入了 hint `NO_DECORRELATE`，用来提示优化器不要对指定的查询块解除关联，以提升部分场景下的查询性能。

    更多信息，请参考[用户文档](/optimizer-hints.md#no_decorrelate)。

* 提升了分区表统计信息收集的性能 [#37977](https://github.com/pingcap/tidb/issues/37977) @[Yisaer](https://github.com/Yisaer)

    在 v6.4.0 版本中，TiDB 优化了分区表统计信息的收集策略。你可以通过系统变量 [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-从-v640-版本开始引入) 定义并发度，用并行的方式同时收集多个分区的统计信息，从而加快统计信息收集的速度，减少 analyze 所需的时间。

### 稳定性

* 磁盘故障、I/O 无响应等极端情况下的故障恢复加速 [#13648](https://github.com/tikv/tikv/issues/13648) @[LykxSassinator](https://github.com/LykxSassinator)

   数据库的可用性是企业用户最为关注的指标之一，但是在复杂的硬件环境下，如何快速检测故障并恢复一直是数据库面临的挑战之一。TiDB v6.4.0 全面优化了 TiKV 节点的状态检测机制。即使在磁盘故障或 I/O 无响应等极端情况下，TiDB 依然可以快速上报节点状态，同时搭配主动唤醒机制，提前发起 Leader 选举，加速集群自愈。通过这次优化，TiDB 在磁盘故障场景下，集群恢复时间可以缩短 50% 左右。

* TiDB 全局内存控制（实验特性）[#37816](https://github.com/pingcap/tidb/issues/37816) @[wshwsh12](https://github.com/wshwsh12)

    v6.4.0 引入了全局内存控制，对 TiDB 实例的全局内存使用进行追踪。你可以通过系统变量 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 设置全局内存的使用上限。当内存使用量接近预设的上限时，TiDB 会尝试对内存进行回收，释放更多的可用内存；当内存使用量超出预设的上限时，TiDB 会识别出当前内存使用量最大的 SQL 操作，并取消这个操作，避免因为内存使用过度而产生的系统性问题。

    当 TiDB 实例的内存消耗存在潜在风险时，TiDB 会预先收集诊断信息并写入指定目录，方便对问题的诊断。同时，TiDB 提供了系统表视图 [`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md) 和 [`INFORMATION_SCHEMA.MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md) 用来展示内存使用情况及历史操作，帮助用户清晰了解内存使用状况。

    全局内存控制是 TiDB 内存管理的重要一步，对实例采用全局视角，引入系统性方法对内存用量进行管理，这可以极大提升数据库的稳定性，提高服务的可用性，支持 TiDB 在更多重要场景平稳运行。

    更多信息，请参考[用户文档](/configure-memory-usage.md)。

* 控制优化器在构造范围时的内存占用 [#37176](https://github.com/pingcap/tidb/issues/37176) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    v6.4.0 引入了系统变量 [`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-从-v640-版本开始引入) 来限制优化器在构造范围时消耗的内存上限。当内存使用超出这个限制，则放弃构造精确的范围，转而构建更粗粒度的范围，以此降低内存消耗。当 SQL 语句中的 `IN` 条件较多时，这个优化可以显著降低编译时的内存使用量，保证系统的稳定性。

    更多信息，请参考[用户文档](/system-variables.md#tidb_opt_range_max_size-从-v640-版本开始引入)。

* 支持统计信息的同步加载（GA）[#37434](https://github.com/pingcap/tidb/issues/37434) @[chrysan](https://github.com/chrysan)

    TiDB v6.4.0 起，正式开启了统计信息同步加载的特性（默认开启），支持在执行当前 SQL 语句时将直方图、TopN、CMSketch 等占用空间较大的统计信息同步加载到内存，提高优化该 SQL 语句时统计信息的完整性。

    更多信息，请参考[用户文档](/system-variables.md#tidb_stats_load_sync_wait-从-v540-版本开始引入)。

* 降低批量写入请求对轻量级事务写入的响应时间的影响 [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)

    定时批量 DML 任务存在于一部分系统的业务逻辑中。在此场景下，处理这些批量写入任务会增加在线交易的时延。在 v6.3.0 中，TiKV 对混合负载场景下读请求的优先级进行了优化，你可以通过 [`readpool.unified.auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-从-v630-版本开始引入) 配置项开启 TiKV 对统一处理读请求的线程池 (UnifyReadPool) 大小的自动调整。在 v6.4.0 中，TiKV 对写入请求也进行了动态识别和优先级调整，控制 Apply 线程每一轮处理单个状态机写入的最大数据量，从而降低批量写入对交易事务写入的响应时间的影响。

### 易用性

* TiKV API V2 成为正式功能 [#11745](https://github.com/tikv/tikv/issues/11745) @[pingyu](https://github.com/pingyu)

    在 v6.1.0 之前，TiKV 的 RawKV 接口仅存储客户端传入的原始数据，因此只提供基本的 Key-Value 读写能力。此外，由于编码方式不同、数据范围没有隔离等，同一个 TiKV 集群中，TiDB、事务 KV、RawKV 无法同时使用，因此对于不同使用方式并存的场景，必须部署多个集群，增加了机器和部署成本。

    TiKV API V2 提供了新的存储格式，功能亮点如下：

    * RawKV 数据以 MVCC 方式存储，记录数据的变更时间戳，并在此基础上提供 Change Data Capture 能力（实验特性，见 [TiKV-CDC](https://github.com/tikv/migration/blob/main/cdc/README.md)）。
    * 数据根据使用方式划分范围，支持单一集群 TiDB、事务 KV、RawKV 应用共存。
    * 预留 Key Space 字段，为多租户等特性提供支持。

  你可以通过在 TiKV 的 `[storage]` 配置中设置 `api-version = 2` 来启用 TiKV API V2。

  更多信息，请参考[用户文档](/tikv-configuration-file.md#api-version-从-v610-版本开始引入)。

* 优化 TiFlash 数据同步进度的准确性 [#4902](https://github.com/pingcap/tiflash/issues/4902) @[hehechen](https://github.com/hehechen)

    TiDB 的 `INFORMATION_SCHEMA.TIFLASH_REPLICA` 表中的 `PROGRESS` 字段表示 TiFlash 副本与 TiKV 中对应表数据的同步进度。在之前的版本中，`PROCESS` 字段只显示 TiFlash 副本创建过程中的数据同步进度。在 TiFlash 副本创建完后，当在 TiKV 相应的表中导入新的数据时，该值不会更新数据的同步进度。

    v6.4.0 版本改进了 TiFlash 副本数据同步进度更新机制。在创建 TiFlash 副本后，进行数据导入等操作，TiFlash 副本需要和 TiKV 数据进行同步时，[`INFORMATION_SCHEMA.TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md) 表中的 `PROGRESS` 值将会更新，显示实际的数据同步进度。通过此优化，你可以方便地查看 TiFlash 数据同步的实际进度。

    更多信息，请参考[用户文档](/information-schema/information-schema-tiflash-replica.md)。

### MySQL 兼容性

* TiDB 分区表兼容 Linear Hash 分区语法 [#38450](https://github.com/pingcap/tidb/issues/38450) @[mjonss](https://github.com/mjonss)

    TiDB 现有的分区方式支持 Hash、Range、List 分区。TiDB v6.4.0 增加了对 [MySQL LINEAR HASH](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html) 分区语法的兼容。

    在 TiDB 上，你可以直接执行原有的 MySQL Linear Hash 分区的 DDL 语句，TiDB 将创建一个常规的非线性 Hash 分区表（注意 TiDB 内部实际不存在 LINEAR HASH 分区）。你也可以直接执行原有的 MySQL LINEAR HASH 分区的 DML 语句，TiDB 将正常返回对应的 TiDB Hash 分区的查询结果。此功能保证了 TiDB 对 MySQL LINEAR HASH 分区的语法兼容，方便基于 MySQL 的应用无缝迁移到 TiDB。

   当分区数是 2 的幂时，TiDB Hash 分区表中行的分布情况与 MySQL Linear Hash 分区表相同，但当分区数不是 2 的幂时，TiDB Hash 分区表中行的分布情况与 MySQL Linear Hash 分区表会有所区别。

    更多信息，请参考[用户文档](/partitioned-table.md#tidb-对-linear-hash-分区的处理)。

* 支持高性能、全局单调递增的 `AUTO_INCREMENT` 列属性（实验特性）[#38442](https://github.com/pingcap/tidb/issues/38442) @[tiancaiamao](https://github.com/tiancaiamao)

    TiDB v6.4.0 引入了 `AUTO_INCREMENT` 的 MySQL 兼容模式，通过中心化分配自增 ID，实现了自增 ID 在所有 TiDB 实例上单调递增。使用该特性能够更容易地实现查询结果按自增 ID 排序。要使用 MySQL 兼容模式，你需要在建表时将 `AUTO_ID_CACHE` 设置为 `1`。

    ```sql
    CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
    ```

    更多信息，请参考[用户文档](/auto-increment.md#mysql-兼容模式)。

* 支持对 JSON 类型中的 Array 数据做范围选择 [#13644](https://github.com/tikv/tikv/issues/13644) @[YangKeao](https://github.com/YangKeao)

    从 v6.4.0 起，TiDB 支持 [MySQL 兼容的范围选择语法](https://dev.mysql.com/doc/refman/8.0/en/json.html#json-paths)。

    - 通过关键字 `to`，你可以指定元素起始和结束的位置，并选择 Array 中连续范围的元素，起始位置记为 `0`。例如，使用 `$[0 to 2]` 可以选择 Array 中的前三个元素。
    - 通过关键字 `last`，你可以指定 Array 中最后一个元素的位置，实现从右到左的位置设定。例如，使用 `$[last-2 to last]` 可以选择 Array 中的最后三个元素。

    该特性简化了 SQL 的编写过程，进一步提升了 JSON 类型的兼容能力，降低了 MySQL 应用向 TiDB 迁移的难度。

* 支持对数据库用户增加额外说明 [#38172](https://github.com/pingcap/tidb/issues/38172) @[CbcWestwolf](https://github.com/CbcWestwolf)

    在 TiDB v6.4.0 中，你可以通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句为数据库用户添加额外的说明信息。TiDB 提供了两种说明格式，你可以通过 `COMMENT` 添加一段文本注释，也可以通过 `ATTRIBUTE` 添加一组 JSON 格式的结构化属性。

    此外，TiDB v6.4.0 新增了 [`USER_ATTRIBUTES`](/information-schema/information-schema-user-attributes.md) 表。你可以在该表中查看用户的注释和属性信息。

    ```sql
    CREATE USER 'newuser1'@'%' COMMENT 'This user is created only for test';
    CREATE USER 'newuser2'@'%' ATTRIBUTE '{"email": "user@pingcap.com"}';
    SELECT * FROM INFORMATION_SCHAME.USER_ATTRIBUTES;
    ```

    ```sql
    +-----------+------+---------------------------------------------------+
    | USER      | HOST | ATTRIBUTE                                         |
    +-----------+------+---------------------------------------------------+
    | newuser1  | %    | {"comment": "This user is created only for test"} |
    | newuser1  | %    | {"email": "user@pingcap.com"}                     |
    +-----------+------+---------------------------------------------------+
    2 rows in set (0.00 sec)
    ```

    这个特性提升了 TiDB 对 MySQL 的语法的兼容性，使得 TiDB 更容易融入 MySQL 生态的工具或平台。

### 备份和恢复

* 基于 AWS EBS snapshot 的集群备份和恢复 [#33849](https://github.com/pingcap/tidb/issues/33849) @[fengou1](https://github.com/fengou1)

    如果你的 TiDB 集群部署在 EKS 上，使用了 AWS EBS 卷，并且对数据备份有以下要求，可考虑使用 TiDB Operator 将 TiDB 集群数据以卷快照以及元数据的方式备份至 Amazon S3：

    - 备份的影响降到最小，如备份对 QPS 和事务耗时影响小于 5%，不占用集群 CPU 以及内存。
    - 快速备份和恢复，比如 1 小时内完成备份，2 小时内完成恢复。

  更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)。

### 数据迁移

* 支持将上游数据源信息以扩展列形式写入下游合表 [#37797](https://github.com/pingcap/tidb/issues/37797) @[lichunzhu](https://github.com/lichunzhu)

    在上游分库分表合并到 TiDB 的场景，你可以在目标表中手动额外增加几个字段（扩展列），并在配置 DM 任务时，对这几个扩展列赋值。例如，当赋予上游分库分表的名称时，通过 DM 写入到下游的记录会包含上游分库分表的名称。在一些数据异常的场景，你可以通过该功能快速定位目标表的问题数据源信息，如该数据来自上游哪个分库，哪个分表。

    更多信息，请参考[提取分库分表数据源信息写入合表](/dm/dm-table-routing.md#提取分库分表数据源信息写入合表)。

* 优化 DM 的前置检查项，将部分必须通过项改为非必须通过项 [#7333](https://github.com/pingcap/tiflow/issues/7333) @[lichunzhu](https://github.com/lichunzhu)

    为了使数据迁移任务顺利进行，DM 在启动迁移任务时会自动触发[任务前置检查](/dm/dm-precheck.md)，并返回检查结果。只有当前置检查通过后，DM 才开始执行迁移任务。

    在 v6.4.0，DM 将如下三个检查项由必须通过项改为非必须通过项，提升了前置检查通过率：

    - 检查字符集是否存在兼容性差异
    - 检查上游表中是否存在主键或唯一键约束
    - 数据库主从配置，上游数据库必须设置数据库 ID `server_id`

* 增量迁移任务支持 binlog position 和 GTID 作为选配参数 [#7393](https://github.com/pingcap/tiflow/issues/7393) @[GMHDBJD](https://github.com/GMHDBJD)

    v6.4.0 之前，只配置增量迁移任务时，需要传入 binlog position 或者 GTID 才能启动任务，配置复杂，用户理解成本高。自 v6.4.0 起，如果只需要执行增量迁移任务，则可以不指定 binlog position 或者 GTID 的参数取值，DM 将默认按任务的启动时间从上游获取该时间之后的 binlog file，并将这些增量数据迁移到下游 ，降低了使用时的理解成本和配置复杂度。

    更多信息，请参考 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)。

* DM 任务增加一些状态信息的展示 [#7343](https://github.com/pingcap/tiflow/issues/7343) @[okJiang](https://github.com/okJiang)

    在 v6.4.0，DM 数据迁移任务新增了一些性能指标和进度指标，方便用户更直观地了解迁移性能和进度，同时为问题排查提供参考信息：

    * 增加了 DM 任务当前数据导出、数据导入的性能指标，单位 bytes/s。
    * 将当前 DM 写入目标库的性能指标命名从 TPS 改为 RPS (rows/second)。
    * 新增了 DM 全量任务数据导出的进度展示。

  关于这些指标的详细介绍，请参考 [TiDB Data Migration 查询状态](/dm/dm-query-status.md)。

### 数据共享与订阅

- TiCDC 支持同步数据到 `3.2.0` 版本的 Kafka [#7191](https://github.com/pingcap/tiflow/issues/7191) @[3AceShowHand](https://github.com/3AceShowHand)

    TiCDC 下游支持的 Kafka 最高版本从 `3.1.0` 变为 `3.2.0`。你可以通过 TiCDC 将数据同步到不高于 `3.2.0` 版本的 Kafka。

## 兼容性变更

### 系统变量

| 变量名  | 修改类型                      | 描述 |
|--------|------------------------------|------|
| [`max_execution_time`](/system-variables.md#max_execution_time) | 修改 | 在 v6.4.0 之前，该变量对所有类型的语句生效。从 v6.4.0 开始，该变量只用于控制只读语句的最大执行时长。 |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) | 修改 | 该变量用于控制悲观事务中唯一约束检查的时间点。v6.4.0 去掉了它的 GLOBAL 作用域并支持通过配置项 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-从-v640-版本开始引入) 控制它的默认值。 |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-从-v630-版本开始引入) | 修改 | 该变量从 v6.4.0 开始生效，用来控制 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md) 的并发数。默认值为 `64`。 |
| [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-从-v50-版本开始引入) | 修改 | 该变量默认值从 `INT_ONLY` 修改为 `ON`，表示表的主键默认使用聚簇索引。 |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-从-v540-版本开始引入) | 修改 | 该变量默认值 `OFF` 修改为 `ON`，表示默认使用分页 (paging) 方式发送 Coprocessor 请求。 |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-从-v610-版本开始引入) | 修改 | 该变量用来控制是否开启 [Prepared Plan Cache](/sql-prepared-plan-cache.md)。v6.4.0 新增了 SESSION 作用域。 |
| [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) | 修改 | 该变量用于设置触发 tidb-server 内存告警的内存使用比率，默认值从 `0.8` 修改为 `0.7`。 |
| [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down) | 修改 | 该变量用来设置优化器是否执行聚合函数下推到 Join，Projection 和 UnionAll 之前的优化操作。v6.4.0 新增了 GLOBAL 的作用域。 |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-从-v610-版本开始引入) | 修改 | 该变量用来控制单个 session 的 Prepared Plan Cache 最多能够缓存的计划数量。v6.4.0 新增了 SESSION 作用域。|
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-从-v540-版本开始引入) | 修改 | 该变量默认值从 `0` 修改为 `100`，代表 SQL 执行同步加载完整统计信息默认等待 100 毫秒后会超时。 |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-从-v540-版本开始引入) | 修改 | 该变量默认值从 `OFF` 修改为 `ON`，代表统计信息同步加载超时后，SQL 会退回使用 pseudo 的统计信息。|
| [`last_sql_use_alloc`](/system-variables.md#last_sql_use_alloc-从-v640-版本开始引入) | 新增 | 该变量是一个只读变量，用来显示上一个语句是否使用了缓存的 Chunk 对象 (Chunk allocation)。默认值为 `OFF`。 |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-从-v640-版本开始引入) | 新增 | 该变量用于设置 TiDB [自动 analyze](/statistics.md#自动更新) 分区表（即自动收集分区表上的统计信息）时，每次同时 analyze 分区的个数。默认值为 `1`。 |
| [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-从-v640-版本开始引入) | 新增 | 该变量用于控制 TiDB 是否会读取 [`tidb_external_ts`](/system-variables.md#tidb_external_ts-从-v640-版本开始引入) 指定的时间戳前的历史数据。默认值为 `OFF`。 |
| [`tidb_enable_gogc_tuner`](/system-variables.md#tidb_enable_gogc_tuner-从-v640-版本开始引入) | 新增 | 该变量来用控制是否开启 GOGC Tuner，默认为 `ON`。 |
| [`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-从-v640-版本开始引入) | 新增 | 该变量用于控制 TiDB 是否启用 Chunk 对象缓存，默认为 `ON`，代表 TiDB 优先使用缓存中的 Chunk 对象，缓存中找不到申请的对象时才会从系统内存中申请。如果为 `OFF`，则直接从系统内存中申请 Chunk 对象。 |
| [`tidb_enable_prepared_plan_cache_memory_monitor`](/system-variables.md#tidb_enable_prepared_plan_cache_memory_monitor-从-v640-版本开始引入) | 新增 | 该变量用来控制是否统计 Prepared Plan Cache 中所缓存的执行计划占用的内存，默认为 `ON`。|
| [`tidb_external_ts`](/system-variables.md#tidb_external_ts-从-v640-版本开始引入) | 新增 | 默认值为 `0`。当 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-从-v640-版本开始引入) 设置为 `ON` 时，TiDB 会依据该变量指定的时间戳读取历史数据。 |
| [`tidb_gogc_tuner_threshold`](/system-variables.md#tidb_gogc_tuner_threshold-从-v640-版本开始引入) | 新增 | 该变量用来控制 GOGC Tuner 自动调节的最大内存阈值，超过阈值后 GOGC Tuner 会停止工作。默认值为 `0.6`。 |
| [`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-从-v640-版本开始引入) | 新增 | 当 tidb-server 内存占用超过内存报警阈值并触发报警时，TiDB 默认只保留最近 5 次报警时所生成的状态文件。通过该变量可以调整该次数。 |
| [`tidb_opt_prefix_index_single_scan`](/system-variables.md#tidb_opt_prefix_index_single_scan-从-v640-版本开始引入) | 新增 | 该变量用于控制 TiDB 优化器是否将某些过滤条件下推到前缀索引，尽量避免不必要的回表，从而提高查询性能。默认为 `ON`。 |
| [`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-从-v640-版本开始引入) | 新增 | 该变量用于指定优化器构造扫描范围的内存用量上限。默认值为 `67108864`（即 64 MiB）。 |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) | 新增 | 该变量用于指定 TiDB 实例的内存限制（实验特性）。默认值为 `0`，表示不设内存限制。 |
| [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-从-v640-版本开始引入) | 新增 | 该变量用于控制 TiDB 尝试触发 GC 的阈值（实验特性）。默认值为 `70%`。|
| [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-从-v640-版本开始引入) | 新增 | 开启内存限制后，TiDB 会终止当前实例上内存用量最高的 SQL 语句。本变量指定此情况下 SQL 语句被终止的最小内存用量（实验特性），默认值为 `134217728`（即 128 MiB）。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | `tidb_memory_usage_alarm_ratio` | 废弃 | 该配置不再生效。|
| TiDB | `memory-usage-alarm-ratio` | 废弃 | 该配置项被系统变量 [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) 所取代。如果在升级前设置过该配置项，升级后原配置将不再生效。|
| TiDB | [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-从-v640-版本开始引入) | 新增 | 用于控制系统变量 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) 的默认值，默认值为 `true`。|
| TiDB | [`tidb-max-reuse-chunk`](/tidb-configuration-file.md#tidb-max-reuse-chunk-从-v640-版本开始引入) | 新增 | 用于控制每个连接最多缓存的 Chunk 对象数，默认值为 `64`。 |
| TiDB | [`tidb-max-reuse-column`](/tidb-configuration-file.md#tidb-max-reuse-column-从-v640-版本开始引入) | 新增 | 用于控制每个连接最多缓存的 column 对象数，默认值为 `256`。 |
| TiKV | [`cdc.raw-min-ts-outlier-threshold`](https://docs.pingcap.com/zh/tidb/v6.2/tikv-configuration-file#raw-min-ts-outlier-threshold-从-v620-版本开始引入) | 废弃 | 该配置不再生效。|
| TiKV | [`causal-ts.alloc-ahead-buffer`](/tikv-configuration-file.md#alloc-ahead-buffer-从-v640-版本开始引入) | 新增 | 预分配给 TSO 的缓存大小（以时长计算），默认值为 `3s`。|
| TiKV | [`causal-ts.renew-batch-max-size`](/tikv-configuration-file.md#renew-batch-max-size-从-v640-版本开始引入)| 新增 | 单次时间戳请求的最大数量，默认值为 `8192`。 |
| TiKV | [`raftstore.apply-yield-write-size`](/tikv-configuration-file.md#apply-yield-write-size-从-v640-版本开始引入) | 新增 | Apply 线程每一轮处理单个状态机写入的最大数据量，默认值为 `32KiB`。这是个软限制。|
| PD | [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval) | 新增 | 这个配置项从 v6.4.0 开始生效，用来控制 TSO 物理时钟更新周期，默认值为 `50ms`。 |
| TiFlash | [`data-encryption-method`](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) | 修改 | 扩展可选值范围：增加 `sm4-ctr`。设置为 `sm4-ctr` 时，数据将采用国密算法 SM4 加密后进行存储。 |
| DM | [`routes.route-rule-1.extract-table`](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | 可选配置。用于提取分库分表场景中分表的源信息，提取的信息写入下游合表，用于标识数据来源。如果配置该项，需要提前在下游手动创建合表。 |
| DM | [`routes.route-rule-1.extract-schema`](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | 可选配置。用于提取分库分表场景中分库的源信息，提取的信息写入下游合表，用于标识数据来源。如果配置该项，需要提前在下游手动创建合表。 |
| DM | [`routes.route-rule-1.extract-source`](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | 可选配置。用于提取分库分表场景中的源信息，提取的信息写入下游合表，用于标识数据来源。如果配置该项，需要提前在下游手动创建合表。 |
| TiCDC | [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#sink-uri-配置-mysqltidb) | 修改 | 默认值由 `table` 改为 `none`。该修改可降低同步延迟，减少系统出现 OOM 的风险。同时，修改默认值后，系统只拆分少量的事务（即超过 1024 行的事务），而不是拆分所有事务。 |

### 其他

- 从 v6.4.0 开始，`mysql.user` 表新增 `User_attributes` 和 `Token_issuer` 两个字段。如果从 v6.4.0 之前版本的备份数据[恢复 `mysql` schema 下的系统表](/br/br-snapshot-guide.md#恢复-mysql-数据库下的表) 到 v6.4.0 集群，BR 将返回 `mysql.user` 表的 `column count mismatch` 错误。如果你未选择恢复 `mysql` schema 下的系统表，则不会报错。
- 针对命名规则符合 Dumpling [输出文件格式](/dumpling-overview.md#输出文件格式)但后缀名并非 gzip 压缩格式的文件（例如 `test-schema-create.sql.origin` 和 `test.table-schema.sql.origin`），Lightning 的处理方式发生了变化。在 v6.4.0 之前的版本中，如果待导入的文件中包含这类文件，Lightning 将跳过对这类文件的导入。从 v6.4.0 起，Lightning 将认为这些文件使用了不支持的压缩格式，导致导入失败。
- 从 v6.4.0 开始，TiCDC 使用 Syncpoint 功能需要同步任务拥有下游集群的 `SYSTEM_VARIABLES_ADMIN` 或者 `SUPER` 权限。

## 改进提升

+ TiDB

    - 允许修改 noop 系统变量 `lc_messages` [#38231](https://github.com/pingcap/tidb/issues/38231) @[djshow832](https://github.com/djshow832)
    - 允许 `AUTO_RANDOM` 列作为聚簇复合索引中的第一列 [#38572](https://github.com/pingcap/tidb/issues/38572) @[tangenta](https://github.com/tangenta)
    - 内部事务重试使用悲观模式避免重试失败，降低耗时 [#38136](https://github.com/pingcap/tidb/issues/38136) @[jackysp](https://github.com/jackysp)

+ TiKV

    - 新增 `apply-yield-write-size` 配置项，以限制 Apply 线程每一轮处理单个状态机写入的数据大小，缓解 Raftstore 线程在 Apply 写入过大时的阻塞现象 [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)
    - 在 Region 的 Leader 迁移前增加缓存预热阶段，缓解 Leader 迁移时造成的 QPS 剧烈抖动 [#13060](https://github.com/tikv/tikv/issues/13060) @[cosven](https://github.com/cosven)
    - 支持将 `json_contains` 算子下推至 Coprocessor [#13592](https://github.com/tikv/tikv/issues/13592) @[lizhenhuan](https://github.com/lizhenhuan)
    - 新增 `CausalTsProvider` 的异步实现，提升某些场景下刷盘的性能 [#13428](https://github.com/tikv/tikv/issues/13428) @[zeminzhou](https://github.com/zeminzhou)

+ PD

    - 热点均衡调度器 v2 版本算法成为正式功能，在特定场景下 v2 版本算法可以在配置的两个维度均取得更好的均衡效果，并减少无效调度 [#5021](https://github.com/tikv/pd/issues/5021) @[HundunDM](https://github.com/hundundm)
    - 改进 Operator step 超时机制，防止过早超时 [#5596](https://github.com/tikv/pd/issues/5596) @[bufferflies](https://github.com/bufferflies)
    - 优化调度器在大集群下的性能 [#5473](https://github.com/tikv/pd/issues/5473) @[bufferflies](https://github.com/bufferflies)
    - 支持使用非 PD 提供的外部时间戳 [#5637](https://github.com/tikv/pd/issues/5637) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - 重构了 TiFlash MPP 的错误处理流程，进一步提升了 MPP 的稳定性 [#5095](https://github.com/pingcap/tiflash/issues/5095) @[windtalker](https://github.com/windtalker)
    - 优化了 TiFlash 计算过程中的排序操作，以及对 Join 和 Aggregation 的 Key 的处理 [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)
    - 优化了 TiFlash 编解码的内存使用，去除了冗余传输列以提升 Join 性能 [#6157](https://github.com/pingcap/tiflash/issues/6157) @[yibin87](https://github.com/yibin87)

+ Tools

    + TiDB Dashboard

        - 支持在 Monitoring 页面展示 TiFlash 相关指标，并且优化了该页面指标的展示方式 [#1440](https://github.com/pingcap/tidb-dashboard/issues/1440) @[YiniXu9506](https://github.com/YiniXu9506)
        - 支持在 Slow Queries 列表和 SQL Statements 列表展示结果行数 [#1443](https://github.com/pingcap/tidb-dashboard/issues/1443) @[baurine](https://github.com/baurine)
        - 当集群没有 Alertmanager 时不显示报错信息 [#1444](https://github.com/pingcap/tidb-dashboard/issues/1444) @[baurine](https://github.com/baurine)

    + Backup & Restore (BR)

        - 改进加载元数据的机制，仅在需要时才将元数据加载到内存中，显著减少 PITR 过程中的内存压力 [#38404](https://github.com/pingcap/tidb/issues/38404) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 支持同步 Exchange Partition 的 DDL 语句 [#639](https://github.com/pingcap/tiflow/issues/639) @[asddongmen](https://github.com/asddongmen)
        - 提升 MQ sink 模块非攒批发送的性能 [#7353](https://github.com/pingcap/tiflow/issues/7353) @[hi-rustin](https://github.com/Rustin170506)
        - 提升单表大量 Region 场景下 TiCDC puller 的性能 [#7078](https://github.com/pingcap/tiflow/issues/7078) [#7281](https://github.com/pingcap/tiflow/issues/7281) @[sdojjy](https://github.com/sdojjy)
        - 支持在 Syncpoint 功能开启时在下游 TiDB 集群使用 `tidb_enable_external_ts_read` 来读取历史数据 [#7419](https://github.com/pingcap/tiflow/issues/7419) @[asddongmen](https://github.com/asddongmen)
        - 默认情况下关闭 safeMode 并开启大事务拆分功能，提升同步的稳定性 [#7505](https://github.com/pingcap/tiflow/issues/7505) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - 移除 dmctl 中无用的 `operate-source update` 指令 [#7246](https://github.com/pingcap/tiflow/issues/7246) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - 解决了 TiDB 不兼容上游数据库的建表 SQL 导致 DM 全量迁移报错的问题，当上游的建表 SQL TiDB 不兼容时，用户可以提前在 TiDB 手动创建好目标表，让全量迁移任务继续运行 [#37984](https://github.com/pingcap/tidb/issues/37984) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 优化文件扫描逻辑，提升 Schema 类型文件的扫描速度 [#38598](https://github.com/pingcap/tidb/issues/38598) @[dsdashun](https://github.com/dsdashun)

## 错误修复

+ TiDB

    - 修复新建索引之后有可能导致数据索引不一致的问题 [#38165](https://github.com/pingcap/tidb/issues/38165) @[tangenta](https://github.com/tangenta)
    - 修复 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 表的权限问题 [#38407](https://github.com/pingcap/tidb/issues/38407) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复 `mysql.tables_priv` 表中 `grantor` 字段缺失的问题 [#38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复公共表表达式在 join 时可能得到错误结果的问题 [#38170](https://github.com/pingcap/tidb/issues/38170) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复公共表表达式在 union 时可能得到错误结果的问题 [#37928](https://github.com/pingcap/tidb/issues/37928) @[YangKeao](https://github.com/YangKeao)
    - 修复监控面板 **transaction region num** 信息不准确的问题 [#38139](https://github.com/pingcap/tidb/issues/38139) @[jackysp](https://github.com/jackysp)
    - 修复 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) 可能影响内部事务问题，修改该变量作用域为 SESSION [#38766](https://github.com/pingcap/tidb/issues/38766) @[ekexium](https://github.com/ekexium)
    - 修复条件在某些场景下被错误下推至 projection 的问题 [#35623](https://github.com/pingcap/tidb/issues/35623) @[Reminiscent](https://github.com/Reminiscent)
    - 修复 `AND` 和 `OR` 条件的 `isNullRejected` 检查错误导致查询结果错误的问题 [#38304]( https://github.com/pingcap/tidb/issues/38304) @[Yisaer](https://github.com/Yisaer)
    - 修复外连接消除时没有考虑 `GROUP_CONCAT` 内部的 `ORDER BY` 导致查询出错的问题 [#18216](https://github.com/pingcap/tidb/issues/18216) @[winoros](https://github.com/winoros)
    - 修复错误下推的条件被 Join Reorder 丢弃后导致查询结果错误的问题 [#38736](https://github.com/pingcap/tidb/issues/38736) @[winoros](https://github.com/winoros)

+ TiKV

    - 修复 Gitpod 环境中存在多个 `cgroup` 和 `mountinfo` 时 TiDB 启动异常的问题 [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie)
    - 修复 TiKV 监控 `tikv_gc_compaction_filtered` 表达式错误的问题 [#13537](https://github.com/tikv/tikv/issues/13537) @[Defined2014](https://github.com/Defined2014)
    - 修复 `delete_files_in_range` 存在异常导致的性能问题 [#13534](https://github.com/tikv/tikv/issues/13534) @[tabokie](https://github.com/tabokie)
    - 修复获取 Snapshot 时 Lease 过期引发的异常竞争问题 [#13553](https://github.com/tikv/tikv/issues/13553) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复第一次 `FLASHBACK` 失败时存在异常的问题 [#13672](https://github.com/tikv/tikv/issues/13672) [#13704](https://github.com/tikv/tikv/issues/13704) [#13723](https://github.com/tikv/tikv/issues/13723) @[HuSharp](https://github.com/HuSharp)

+ PD

    - 修复 Stream 超时问题，提高 Leader 切换的速度 [#5207](https://github.com/tikv/pd/issues/5207) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiFlash

    - 修复由于 PageStorage GC 未能正确清除 Page 删除标记导致 WAL 文件过大从而导致 TiFlash OOM 的问题 [#6163](https://github.com/pingcap/tiflash/issues/6163) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Dashboard

        - 修复查询某些复杂 SQL 语句的执行计划时 TiDB OOM 的问题 [#1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @[baurine](https://github.com/baurine)
        - 修复 NgMonitoring 丢失对 PD 节点的连接时可能导致 Top SQL 开关无效的问题 [#164](https://github.com/pingcap/ng-monitoring/issues/164) @[zhongzc](https://github.com/zhongzc)

    + Backup & Restore (BR)

        - 修复恢复过程中由于 PD leader 切换导致恢复失败的问题 [#36910](https://github.com/pingcap/tidb/issues/36910) @[MoCuishle28](https://github.com/MoCuishle28)
        - 修复了无法暂停日志备份任务的问题 [#38250](https://github.com/pingcap/tidb/issues/38250) @[joccau](https://github.com/joccau)
        - 修复 BR 删除日志备份数据时，会删除不应被删除的数据的问题 [#38939](https://github.com/pingcap/tidb/issues/38939) @[Leavrth](https://github.com/leavrth)
        - 修复 BR 首次删除存储在 Azure Blob Storage 或 Google Cloud Storage 的日志备份数据时执行失败的问题 [#38229](https://github.com/pingcap/tidb/issues/38229) @[Leavrth](https://github.com/leavrth)

    + TiCDC

        - 修复 `changefeed query` 的输出中 `sasl-password` 显示为明文的问题 [#7182](https://github.com/pingcap/tiflow/issues/7182) @[dveeden](https://github.com/dveeden)
        - 修复在一个 etcd 事务中提交太多数据导致 TiCDC 服务不可用问题 [#7131](https://github.com/pingcap/tiflow/issues/7131) @[asddongmen](https://github.com/asddongmen)
        - 修复 redo log 文件可能被错误删除的问题 [#6413](https://github.com/pingcap/tiflow/issues/6413) @[asddongmen](https://github.com/asddongmen)
        - 修复 Kafka Sink V2 协议在同步宽表时性能回退的问题 [#7344](https://github.com/pingcap/tiflow/issues/7344) @[hi-rustin](https://github.com/Rustin170506)
        - 修复 checkpoint ts 可能被提前推进的问题 [#7274](https://github.com/pingcap/tiflow/issues/7274) @[hi-rustin](https://github.com/Rustin170506)
        - 修复 mounter 模块的日志级别设置不当导致 log 打印太多的问题 [#7235](https://github.com/pingcap/tiflow/issues/7235) @[hi-rustin](https://github.com/Rustin170506)
        - 修复一个 TiCDC 集群可能存在两个 owner 的问题 [#4051](https://github.com/pingcap/tiflow/issues/4051) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - 修复 DM WebUI 产生错误 `allow-list` 参数的问题 [#7096](https://github.com/pingcap/tiflow/issues/7096) @[zoubingwu](https://github.com/zoubingwu)
        - 修复 DM-worker 在启动、停止时有一定概率触发 data race 的问题 [#6401](https://github.com/pingcap/tiflow/issues/6401) @[liumengya94](https://github.com/liumengya94)
        - 修复当同步 `UPDATE`、`DELETE` 语句且下游行数据不存在时，DM 静默忽略的问题 [#6383](https://github.com/pingcap/tiflow/issues/6383) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复运行 `query-status` 命令后未显示 `secondsBehindMaster` 字段的问题 [#7189](https://github.com/pingcap/tiflow/issues/7189) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复更新 Checkpoint 时可能触发大事务的问题 [#5010](https://github.com/pingcap/tiflow/issues/5010) @[lance6716](https://github.com/lance6716)
        - 修复在全量任务模式下，任务进入 sync 阶段且立刻失败时，DM 可能丢失上游表结构信息的问题 [#7159](https://github.com/pingcap/tiflow/issues/7159) @[lance6716](https://github.com/lance6716)
        - 修复开启一致性校验时可能触发死锁的问题 [#7241](https://github.com/pingcap/tiflow/issues/7241) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - 修复任务预检查对 `INFORMATION_SCHEMA` 表需要 `SELECT` 权限的问题 [#7317](https://github.com/pingcap/tiflow/issues/7317) @[lance6716](https://github.com/lance6716)
        - 修复空的 TLS 配置导致报错的问题 [#7384](https://github.com/pingcap/tiflow/issues/7384) @[liumengya94](https://github.com/liumengya94)

    + TiDB Lightning

        - 修复当导入 Apache Parquet 格式的数据时，如果目标表存在 binary 编码格式的字符串类型列，导入性能下降的问题 [#38351](https://github.com/pingcap/tidb/issues/38351) @[dsdashun](https://github.com/dsdashun)

    + TiDB Dumpling

        - 修复导出大量表时可能导致超时的问题 [#36549](https://github.com/pingcap/tidb/issues/36549) @[lance6716](https://github.com/lance6716)
        - 修复加锁模式下，上游不存在对应表时导致加锁报错的问题 [#38683](https://github.com/pingcap/tidb/issues/38683) @[lance6716](https://github.com/lance6716)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [645775992](https://github.com/645775992)
- [An-DJ](https://github.com/An-DJ)
- [AndrewDi](https://github.com/AndrewDi)
- [erwadba](https://github.com/erwadba)
- [fuzhe1989](https://github.com/fuzhe1989)
- [goldwind-ting](https://github.com/goldwind-ting)（首次贡献者）
- [h3n4l](https://github.com/h3n4l)
- [igxlin](https://github.com/igxlin)（首次贡献者）
- [ihcsim](https://github.com/ihcsim)
- [JigaoLuo](https://github.com/JigaoLuo)
- [morgo](https://github.com/morgo)
- [Ranxy](https://github.com/Ranxy)
- [shenqidebaozi](https://github.com/shenqidebaozi)（首次贡献者）
- [taofengliu](https://github.com/taofengliu)（首次贡献者）
- [TszKitLo40](https://github.com/TszKitLo40)
- [wxbty](https://github.com/wxbty)（首次贡献者）
- [zgcbj](https://github.com/zgcbj)
