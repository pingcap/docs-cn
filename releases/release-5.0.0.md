---
title: What's New in TiDB 5.0
---

# What's New in TiDB 5.0

发版日期：2021 年 04 月 07 日

TiDB 版本：5.0.0

5.0 版本中，我们专注于帮助企业基于 TiDB 数据库快速构建应用程序，使企业在构建过程中无需担心数据库的性能、性能抖动、安全、高可用、容灾、SQL 语句的性能问题排查等问题。

在 5.0 版本中，你可以获得以下关键特性：

+ TiDB 通过 TiFlash 节点引入了 MPP 架构。这使得大型表连接类查询可以由不同 TiFlash 节点共同分担完成。当 MPP 模式开启后，TiDB 将会根据代价决定是否应该交由 MPP 框架进行计算。MPP 模式下，表连接将通过对 JOIN Key 进行数据计算时重分布（Exchange 操作）的方式把计算压力分摊到各个 TiFlash 执行节点，从而达到加速计算的目的。经测试，TiDB 5.0 在同等资源下，MPP 引擎的总体性能是 Greenplum 6.15.0 与 Apache Spark 3.1.1 两到三倍之间，部分查询可达 8 倍性能差异。
+ 引入聚簇索引功能，提升数据库的性能。例如，TPC-C tpmC 的性能提升了 39%。
+ 开启异步提交事务功能，降低写入数据的延迟。例如：Sysbench 设置 64 线程测试 Update index 时，平均延迟由 12.04 ms 降低到 7.01ms ，降低了 41.7%。
+ 通过提升优化器的稳定性及限制系统任务对 I/O、网络、CPU、内存等资源的占用，降低系统的抖动。例如：测试 8 小时，TPC-C 测试中 tpmC 抖动标准差的值小于等于 2%。
+ 通过完善调度功能及保证执行计划在最大程度上保持不变，提升系统的稳定性。
+ 引入 Raft Joint Consensus 算法，确保 Region 成员变更时系统的可用性。
+ 优化 `EXPLAIN` 功能、引入不可见索引等功能帮助提升 DBA 调试及 SQL 语句执行的效率。
+ 通过从 TiDB 备份文件到 Amazon S3、Google Cloud GCS，或者从 Amazon S3、Google Cloud GCS 恢复文件到 TiDB，确保企业数据的可靠性。
+ 提升从 Amazon S3 或者 TiDB/MySQL 导入导出数据的性能，帮忙企业在云上快速构建应用。例如：导入 1TiB TPC-C 数据性能提升了 40%，由 254 GiB/h 提升到 366 GiB/h。

## 兼容性变化

### 系统变量

+ 新增系统变量 [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-从-v50-版本开始引入)，用于统一控制算子并发度。原有的 tidb_*_concurrency（例如 `tidb_projection_concurrency`）设置仍然生效，使用过程中会提示已废弃警告。
+ 新增系统变量 [`tidb_skip_ascii_check`](/system-variables.md#tidb_skip_ascii_check-从-v50-版本开始引入)，用于决定在写入 ASCII 字符集的列时，是否对字符的合法性进行检查，默认为 OFF。
+ 新增系统变量 [`tidb_enable_strict_double_type_check`](/system-variables.md#tidb_enable_strict_double_type_check-从-v50-版本开始引入)，用于决定类似“double(N)”语法是否允许被定义在表结构中，默认为 OFF。
+ 系统变量 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 的默认值由 20000 修改为 0，即在 "LOAD/INSERT INTO SELECT ..." 等语法中，不再默认使用 Batch DML，而是通过大事务以满足严格的 ACID 语义。

    > **注意：**
    >
    > 该变量作用域从 session 改变为 global，且默认值从 20000 修改为 0，如果应用依赖于原始默认值，需要在升级之后使用 `set global` 语句修改该变量值为原始值。

+ 临时表的语法兼容性受到 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-从-v40-版本开始引入) 系统变量的控制：当 `tidb_enable_noop_functions` 为 `OFF` 时，`CREATE TEMPORARY TABLE` 语法将会报错。
+ 新增 [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-从-v50-版本开始引入)、[`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-从-v50-版本开始引入)、[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入)、[`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-从-v50-版本开始引入)、[`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-从-v50-版本开始引入) 系统变量，用于直接通过系统变量调整垃圾回收相关参数。
+ 系统变量 [`enable-joint-consensus`](/pd-configuration-file.md#enable-joint-consensus-从-v50-版本开始引入) 默认值由 `false` 改成 `ture`，默认开启 Joint consensus 功能。
+ 系统变量 [`tidb_enable_amend_pessimistic_txn`](/system-variables.md#tidb_enable_amend_pessimistic_txn-从-v407-版本开始引入) 的值由数字 0 或者 1 变更成 ON 或者 OFF。
+ 系统变量 [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-从-v50-版本开始引入) 默认值由 OFF 改成 INT_ONLY 且含义有如下变化：
    + ON：开启聚簇索引，支持添加或者删除非聚簇索引。
    + OFF：关闭聚簇索引，支持添加或者删除非聚簇索引。
    + INT_ONLY：默认值，行为与 v5.0 以下版本保持一致，与 `alter-primary-key = false` 一起使用可控制 INT 类型是否开启聚簇索引。

    > **注意：**
    >
    > 5.0 GA 中 `tidb_enable_clustered_index` 的 INT_ONLY 值和 5.0 RC 中的 OFF 值含义一致，从已设置 OFF 的 5.0 RC 集群升级至 5.0 GA 后，将展示为 INT_ONLY。

### 配置文件参数

+ 新增 [`index-limit`](/tidb-configuration-file.md#index-limit-从-v50-版本开始引入) 配置项，默认值为 64，取值范围是 [64, 512]。MySQL 一张表最多支持 64 个索引，如果该配置超过默认值并为某张表创建超过 64 个索引，该表结构再次导入 MySQL 将会报错。
+ 新增 [`enable-enum-length-limit`](/tidb-configuration-file.md#enable-enum-length-limit-从-v50-版本开始引入) 配置项，用于兼容 MySQL ENUM/SET 元素长度并保持一致（ENUM 长度 < 255），默认值为 true。
+ 删除 `pessimistic-txn.enable` 配置项，通过环境变量 [tidb_txn_mode](/system-variables.md#tidb_txn_mode) 替代。
+ 删除 `performance.max-memory` 配置项，通过 [performance.server-memory-quota](/tidb-configuration-file.md#server-memory-quota-从-v409-版本开始引入) 替代。
+ 删除 `tikv-client.copr-cache.enable` 配置项，通过 [tikv-client.copr-cache.capacity-mb](/tidb-configuration-file.md#capacity-mb) 替代，如果配置项的值为 0.0 代表关闭此功能，大于 0.0 代表开启此功能，默认：1000.0。
+ 删除 `rocksdb.auto-tuned` 配置项，通过 [rocksdb.rate-limiter-auto-tuned](/tikv-configuration-file.md#rate-limiter-auto-tuned-从-v50-版本开始引入) 替代。
+ 删除 `raftstore.sync-log` 配置项，默认会写入数据强制落盘，之前显式关闭 `raftstore.sync-log`，成功升级 v5.0 版本后，会强制改为 `true`。
+ `gc.enable-compaction-filter` 配置项的默认值由 `false` 改成 `true`。
+ `enable-cross-table-merge` 配置项的默认值由 `false` 改成 `true`。
+ [`rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-从-v50-版本开始引入) 配置项的默认值由 `false` 改成 `true`。
+ [`committer-concurrency`](/tidb-configuration-file.md#committer-concurrency) 配置项的默认值由 16 改成 128。

### 其他

+ 升级前，请检查 TiDB 配置项 [`feedback-probability`](/tidb-configuration-file.md#feedback-probability) 的值。如果不为 0，升级后会触发 "panic in the recoverable goroutine" 报错，但不影响升级。
+ 为了避免造成数据正确性问题，列类型变更不再允许 `VARCHAR` 类型和 `CHAR` 类型的互相转换。

## 新功能

### SQL

#### List 分区表 (List Partition)（**实验特性**）

[用户文档](/partitioned-table.md#list-分区)

采用 List 分区表后，你可以高效地查询、维护有大量数据的表。

List 分区表会按照 `PARTITION BY LIST(expr) PARTITION part_name VALUES IN (...)` 表达式来定义分区，定义如何将数据划分到不同的分区中。分区表的数据集合最多支持 1024 个值，值的类型只支持整数型，不能有重复的值。可通过 `PARTITION ... VALUES IN (...)` 子句对值进行定义。

你可以设置 session 变量 [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-从-v50-版本开始引入) 的值为 `ON`，开启 List 分区表功能。

#### List COLUMNS 分区表 (List COLUMNS Partition)（**实验特性**）

[用户文档](/partitioned-table.md#list-columns-分区)

List COLUMNS 分区表是 List 分区表的变体，主要的区别是分区键可以由多个列组成，列的类型不再局限于整数类型，也可以是字符串、DATE 和 DATETIME 等类型。

你可以设置 session 变量 [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-从-v50-版本开始引入) 的值为 `ON`，开启 List COLUMNS 分区表功能。

#### 不可见索引 (Invisible Indexes)

[用户文档](/sql-statements/sql-statement-alter-index.md)，[#9246](https://github.com/pingcap/tidb/issues/9246)

DBA 调试和选择相对最优的索引时，可以通过 SQL 语句将某个索引设置成 `Visible` 或者 `Invisible`，避免执行消耗资源较多的操作，如 `DROP INDEX` 或 `ADD INDEX`。

DBA 通过 `ALTER INDEX` 语句可以修改某个索引的可见性。修改后，查询优化器会根据索引的可见性决定是否将此索引加入到索引列表中。

#### `EXCEPT` 和 `INTERSECT` 操作符

[用户文档](/functions-and-operators/set-operators.md)，[#18031](https://github.com/pingcap/tidb/issues/18031)

`INTERSECT` 操作符是一个集合操作符，返回两个或者多个查询结果集的交集。一定程度上可以替代 `Inner Join` 操作符。

`EXCEPT` 操作符是一个集合操作符，返回两个查询结果集的差集，即在第一个查询结果中存在但在第二个查询结果中不存在的结果集。

### 事务

[用户文档](/system-variables.md#tidb_enable_amend_pessimistic_txn-从-v407-版本开始引入)，[#18005](https://github.com/pingcap/tidb/issues/18005)

悲观事务模式下，如果事务所涉及到的表存在并发的 DDL 操作或者 SCHEMA VERSION 变更，系统自动将该事务的 SCHEMA VERSION 更新到最新版本，以此确保事务会提交成功，避免事务因并发的 DDL 操作或者 SCHEMA VERSION 变更而中断时客户端收到 `Information schema is changed` 的错误信息。

系统默认关闭此功能，你可以通过修改 [`tidb_enable_amend_pessimistic_txn`](/system-variables.md#tidb_enable_amend_pessimistic_txn-从-v407-版本开始引入) 系统变量开启此功能，此功能从 4.0.7 版本开始提供，5.0 版本主要修复了以下问题：

+ TiDB Binlog 在执行 Add column 操作的兼容性问题
+ 与唯一索引一起使用时存在的数据不一致性的问题
+ 与添加索引一起使用时存在的数据不一致性的问题

当前此功能存在以下不兼容性问题：

+ 并发事务场景下事务的语义可能发生变化的问题
+ 与 TiDB Binlog 一起使用时，存在已知的兼容性问题 [#20996](https://github.com/pingcap/tidb/issues/20996)
+ 与 change column 功能不兼容 [#21470](https://github.com/pingcap/tidb/issues/21470)

### 字符集和排序规则

- 支持 `utf8mb4_unicode_ci` 和 `utf8_unicode_ci` 排序规则。 [用户文档](/character-set-and-collation.md#新框架下的排序规则支持)，[#17596](https://github.com/pingcap/tidb/issues/17596)
- 支持字符集比较排序时不区分大小写。

### 安全

[用户文档](/log-redaction.md)，[#18566](https://github.com/pingcap/tidb/issues/18566)

为满足各种安全合规（如《通用数据保护条例》(GDPR)）的要求，系统在输出错误信息和日志信息时，支持对敏感信息（例如，身份证信息、信用卡号）进行脱敏处理，避免敏感信息泄露。

TiDB 支持对输出的日志信息进行脱敏处理，你可以通过以下开关开启此功能：

+ 全局系统变量 [`tidb_redact_log`](/system-variables.md#tidb_redact_log)：默认值为 0，即关闭脱敏。设置变量值为 1 开启 tidb-server 的日志脱敏功能。
+ 配置项 `security.redact-info-log`：默认值为 false，即关闭脱敏。设置配置项值为 true 开启 tikv-server 的日志脱敏功能。[#2852](https://github.com/tikv/pd/issues/2852)
+ 配置项 `security.redact-info-log`：默认值为 false，即关闭脱敏。设置配置项值为 true 开启 pd-server 的日志脱敏功能。
+ 配置项 `security.redact_info_log`（对于 tiflash-server）和配置项 `security.redact-info-log`（对于 tiflash-learner）：两个配置项的默认值均为 false，即关闭脱敏。设置配置项值为 true 开启 tiflash-server 及 tiflash-learner 的日志脱敏功能。

此功能从 5.0 版本中开始提供，使用过程中必须开启以上所有系统变量及配置项。

## 性能优化

### MPP 架构

[用户文档](/tiflash/use-tiflash.md)

TiDB 通过 TiFlash 节点引入了 MPP 架构。这使得大型表连接类查询可以由不同 TiFlash 节点分担共同完成。

当 MPP 模式开启后，TiDB 会通过代价决策是否应该交由 MPP 框架进行计算。MPP 模式下，表连接将通过对 JOIN Key 进行数据计算时重分布（Exchange 操作）的方式把计算压力分摊到各个 TiFlash 执行节点，从而达到加速计算的目的。更进一步，加上之前 TiFlash 已经支持的聚合计算，MPP 模式下 TiDB 可以将一个查询的计算都下推到 TiFlash MPP 集群，从而借助分布式环境加速整个执行过程，大幅度提升分析查询速度。

经过 Benchmark 测试，在 TPC-H 100 的规模下，TiFlash MPP 提供了显著超越 Greenplum，Apache Spark 等传统分析数据库或数据湖上分析引擎的速度。借助这套架构，用户可以直接针对最新的交易数据进行大规模分析查询，且性能超越传统离线分析方案。经测试，TiDB 5.0 在同等资源下，MPP 引擎的总体性能是 Greenplum 6.15.0 与 Apache Spark 3.1.1 两到三倍之间，部分查询可达 8 倍性能差异。

当前 MPP 模式不支持的主要功能如下（详细信息请参阅[用户文档](/tiflash/use-tiflash.md)）：

+ 分区表
+ Window Function
+ Collation
+ 部分内置函数
+ 读取 TiKV 数据
+ OOM Spill
+ Union
+ Full Outer Join

### 聚簇索引

[用户文档](/clustered-indexes.md)，[#4841](https://github.com/pingcap/tidb/issues/4841)

DBA、数据库应用开发者在设计表结构时或者分析业务数据的行为时，如果发现有部分列经常分组排序、返回某范围的数据、返回少量不同的值的数据、有主键列及业务数据不会有读写热点时，建议选择聚簇索引。

聚簇索引 (Clustered Index)，部分数据库管理系统也叫索引组织表，是一种和表的数据相关联的存储结构。创建聚簇索引时可指定包含表中的一列或多列作为索引的键值。这些键存储在一个结构中，使 TiDB 能够快速有效地找到与键值相关联的行，提升查询和写入数据的性能。

开启聚簇索引功能后，TiDB 性能在一些场景下会有较大幅度的提升。例如，TPC-C tpmC 的性能提升了 39%。聚簇索引主要在以下场景会有性能提升：

+ 插入数据时会减少一次从网络写入索引数据。
+ 等值条件查询仅涉及主键时会减少一次从网络读取数据。
+ 范围条件查询仅涉及主键时会减少多次从网络读取数据。
+ 等值或范围条件查询涉及主键的前缀时会减少多次从网络读取数据。

每张表既可以采用聚簇索引排序存储数据，也可以采用非聚簇索引，两者区别如下：

+ 创建聚簇索引时，可指定包含表中的一列或多列作为索引的键值，聚簇索引根据键值对表的数据进行排序和存储，每张表只能有一个聚簇索引，当某张表有聚簇索引时，该表称为聚簇索引表。相反如果该表没有聚簇索引，称为非聚簇索引表。
+ 创建非聚簇索引时，表中的数据存储在无序结构中，用户无需显式指定非聚簇索引的键值，系统会自动为每一行数据分配唯一的 ROWID，标识一行数据的位置信息，查询数据时会用 ROWID 定位一行数据。查询或者写入数据时至少会有两次网络 I/O，因此查询或者写入数据的性能相比聚簇索引会有所下降。

当修改表的数据时，数据库系统会自动维护聚簇索引和非聚簇索引，用户无需参与。

系统默认采用非聚簇索引，用户可以通过以下两种方式选择使用聚簇索引或非聚簇索引：

+ 创建表时在语句上指定 `CLUSTERED | NONCLUSTERED`，指定后系统将按照指定的方式创建表。具体语法如下：

    ```sql
    CREATE TABLE `t` (`a` VARCHAR(255), `b` INT, PRIMARY KEY (`a`, `b`) CLUSTERED);
    ```

    或者：

    ```sql
    CREATE TABLE `t` (`a` VARCHAR(255) PRIMARY KEY CLUSTERED, `b` INT);
    ```

    通过 `SHOW INDEX FROM tbl-name` 语句可查询表是否有聚簇索引。

+ 设置 `tidb_enable_clustered_index` 控制聚簇索引功能，取值：ON|OFF|INT_ONLY

    + ON：开启聚簇索引，支持添加或者删除非聚簇索引。
    + OFF：关闭聚簇索引，支持添加或者删除非聚簇索引。
    + INT_ONLY：默认值，行为与 5.0 以下版本保持一致，与 `alter-primary-key = false` 一起使用可控制 INT 类型是否开启聚簇索引。

优先级方面，建表时有指定 `CLUSTERED | NONCLUSTERED` 时，优先级高于系统变量和配置项。

推荐创建表时在语句上指定 `CLUSTERED | NONCLUSTERED` 的方式使用聚簇索引和非聚簇索引，此方式对业务更加灵活，业务可以根据需求在同一个系统同时使用所有数据类型的聚簇索引和非聚簇索引。

不推荐使用 `tidb_enable_clustered_index = INT_ONLY`，原因是 INT_ONLY 是满足兼容性而临时设置的值，不推荐使用，未来会废弃。

聚簇索引功能有如下限制：

+ 不支持聚簇索引和非聚簇索引相互转换。
+ 不支持删除聚簇索引。
+ 不支持通过 `ALTER TABLE` SQL 语句增加、删除、修改聚簇索引。
+ 不支持重组织和重建聚簇索引。
+ 不支持启用、禁用索引，也就是不可见索引功能对聚簇索引不生效。
+ 不支持 `UNIQUE KEY` 作为聚簇索引。
+ 不支持与 TiDB Binlog 一起使用。开启 TiDB Binlog 后 TiDB 只允许创建单个整数列作为主键的聚簇索引；已创建的聚簇索引表的数据插入、删除和更新动作不会通过 TiDB Binlog 同步到下游。
+ 不支持与 `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS` 属性一起使用。
+ 集群升级回滚时，存量的表不受影响，新增表可以通过导入、导出数据的方式降级。

### 异步提交事务 (Async Commit)

[用户文档](/system-variables.md#tidb_enable_async_commit-从-v50-版本开始引入)，[#8316](https://github.com/tikv/tikv/issues/8316)

数据库的客户端会同步等待数据库系统通过两阶段 (2PC) 完成事务的提交，事务在第一阶段提交成功后就会返回结果给客户端，系统会在后台异步执行第二阶段提交操作，降低事务提交的延迟。如果事务的写入只涉及一个 Region，则第二阶段可以直接被省略，变成一阶段提交。

开启异步提交事务特性后，在硬件、配置完全相同的情况下，Sysbench 设置 64 线程测试 Update index 时，平均延迟由 12.04 ms 降低到 7.01ms ，降低了 41.7%。

开启异步提交事务特性时，数据库应用开发人员可以考虑将事务的一致性从线性一致性降低到[因果一致性](/transaction-overview.md#因果一致性事务)，减少 1 次网络交互降低延迟，提升数据写入的性能。开启因果一致性的 SQL 语句为 `START TRANSACTION WITH CAUSAL CONSISTENCY`。

开启因果一致性后，在硬件和配置完全相同的情况下，Sysbench 设置 64 线程测试 oltp_write_only 时，平均延迟由 11.86ms 降低到 11.19ms，降低了 5.6%。

事务的一致性从线性一致性降低到因果一致性后，如果应用程序中多个事务之间没有相互依赖关系时，事务没有全局一致的顺序。

**新创建的 5.0 集群默认开启异步提交事务功能。**

从旧版本升级到 5.0 的集群，默认不开启该功能，你可以执行 `set global tidb_enable_async_commit = ON;` 和 `set global tidb_enable_1pc = ON;` 语句开启该功能。

异步提交事务功能有如下限制：

+ 不支持直接降级

### 默认开启 Coprocessor cache 功能

[用户文档](/tidb-configuration-file.md#tikv-clientcopr-cache-从-v400-版本开始引入)

5.0 GA 默认开启 Coprocessor cache 功能。开启此功能后，TiDB 会在 tidb-server 中缓存算子下推到 tikv-server 计算后的结果，降低读取数据的延时。

要关闭 Coprocessor cache 功能，你可以修改 `tikv-client.copr-cache` 的 `capacity-mb` 配置项为 0.0。

### 提升 `delete * from table where id < ? limit ?` 语句执行的性能

[#18028](https://github.com/pingcap/tidb/issues/18028)

`delete * from table where id < ? limit ?` 语句执行的 p99 性能提升了 4 倍。

### 优化 load base 切分策略，解决部分小表热点读场景数据无法切分的性能问题

## 稳定性提升

### 优化因调度功能不完善引起的性能抖动问题

[#18005](https://github.com/pingcap/tidb/issues/18005)

TiDB 调度过程中会占用 I/O、网络、CPU、内存等资源，若不对调度的任务进行控制，QPS 和延时会因为资源被抢占而出现性能抖动问题。

通过以下几项的优化，测试 8 小时，TPC-C 测试中 tpm-C 抖动标准差的值小于等于 2%。

#### 引入新的调度算分公式，减少不必要的调度，减少因调度引起的性能抖动问题

当节点的总容量总是在系统设置的水位线附近波动或者 `store-limit` 配置项设置过大时，为满足容量负载的设计，系统会频繁地将 Region 调度到其他节点，甚至还会调度到原来的节点，调度过程中会占用 I/O、网络、CPU、内存等资源，引起性能抖动问题，但这类调度其实意义不大。

为缓解此问题，PD 引入了一套新的调度算分公式并默认开启，可通过 `region-score-formula-version = v1` 配置项切换回之前的调度算分公式。

#### 默认开启跨表合并 Region 功能

[用户文档](/pd-configuration-file.md#enable-cross-table-merge)

在 5.0 之前，TiDB 默认关闭跨表合并 Region 的功能。从 5.0 起，TiDB 默认开启跨表合并 Region 功能，减少空 Region 的数量，降低系统的网络、内存、CPU 的开销。你可以通过修改 `schedule.enable-cross-table-merge` 配置项关闭此功能。

#### 默认开启自动调整 Compaction 压缩的速度，平衡后台任务与前端的数据读写对 I/O 资源的争抢

[用户文档](/tikv-configuration-file.md#rate-limiter-auto-tuned-从-v50-版本开始引入)

在 5.0 之前，为了平衡后台任务与前端的数据读写对 I/O 资源的争抢，自动调整 Compaction 的速度这个功能默认是关闭的；从 5.0 起，TiDB 默认开启此功能并优化调整算法，开启之后延迟抖动比未开启此功能时的抖动大幅减少。

你可以通过修改 `rate-limiter-auto-tuned` 配置项关闭此功能。

#### 默认开启 GC in Compaction filter 功能，减少 GC 对 CPU、I/O 资源的占用

[用户文档](/garbage-collection-configuration.md#gc-in-compaction-filter-机制)，[#18009](https://github.com/pingcap/tidb/issues/18009)

TiDB 在进行垃圾回收和数据 Compaction 时，分区会占用 CPU、I/O 资源，系统执行这两个任务过程中存在数据重叠。

GC Compaction Filter 特性将这两个任务合并在同一个任务中完成，减少对 CPU、I/O 资源的占用。系统默认开启此功能，你可以通过设置 `gc.enable-compaction-filter = false` 关闭此功能。

#### TiFlash 限制压缩或整理数据占用 I/O 资源（**实验特性**）

该特性能缓解后台任务与前端的数据读写对 I/O 资源的争抢。

系统默认关闭该特性，你可以通过 `bg_task_io_rate_limit` 配置项开启限制压缩或整理数据 I/O 资源。

#### 增强检查调度约束的性能，提升大集群中修复不健康 Region 的性能

### 保证执行计划在最大程度保持不变，避免性能抖动

[用户文档](/sql-plan-management.md)

#### SQL BINDING 支持 `INSERT`、`REPLACE`、`UPDATE`、`DELETE` 语句

在数据库性能调优或者运维过程中，如果发现因为执行计划不稳定导致系统性能不稳定时，你可以根据自身的经验或者通过 `EXPLAIN ANALYZE` 测试选择一条人为优化过的 SQL 语句，通过 SQL BINDING 将优化过的 SQL 语句与业务代码执行的 SQL 语句绑定，确保性能的稳定性。

通过 SQL BINDING 语句手动的绑定 SQL 语句时，你需要确保优化过的 SQL 语句的语法与原来 SQL 语句的语法保持一致。

你可以通过 `SHOW {GLOBAL | SESSION} BINDINGS` 命令查看手工、系统自动绑定的执行计划信息。输出信息基本跟 5.0 之前的版本保持一致。

#### 自动捕获、绑定执行计划

在升级 TiDB 时，为避免性能抖动问题，你可以开启自动捕获并绑定执行计划的功能，由系统自动捕获并绑定最近一次执行计划然后存储在系统表中。升级完成后，你可以通过 `SHOW GLOBAL BINDINGS` 导出绑定的执行计划，自行分析并决策是否要删除绑定的执行计划。

系统默认关闭自动捕获并绑定执行计划的功能，你可以通过修改 Server 或者设置全局系统变量 `tidb_capture_plan_baselines = ON` 开启此功能。开启此功能后，系统每隔 `bind-info-lease`（默认 3 秒）从 Statement Summary 抓取出现过至少 2 次的 SQL 语句并自动捕获、绑定。

### TiFlash 查询稳定性提升

新增系统变量 [`tidb_allow_fallback_to_tikv`](/system-variables.md#tidb_allow_fallback_to_tikv-从-v50-版本开始引入)，用于决定在 TiFlash 查询失败时，自动将查询回退到 TiKV 尝试执行，默认为 OFF。

### TiCDC 稳定性提升，缓解同步过多增量变更数据的 OOM 问题

[用户文档](/ticdc/manage-ticdc.md#unified-sorter-功能)，[#1150](https://github.com/pingcap/ticdc/issues/1150)

自 v4.0.9 版本起，TiCDC 引入变更数据本地排序功能 Unified Sorter。在 5.0 版本，默认开启此功能以缓解类似场景下的 OOM 问题：

+ 场景一：TiCDC 数据订阅任务暂停中断时间长，其间积累了大量的增量更新数据需要同步。
+ 场景二：从较早的时间点启动数据订阅任务，业务写入量大，积累了大量的更新数据需要同步。

Unified Sorter 整合了老版本提供的 memory、file sort-engine 配置选择，不需要用户手动配置变更的运维操作。

限制与约束：

+ 用户需要根据业务数据更新量提供充足的磁盘空间，推荐使用大于 128G 的 SSD 磁盘。

## 高可用和容灾

### 提升 Region 成员变更时的可用性

[用户文档](/pd-configuration-file.md#enable-joint-consensus-从-v50-版本开始引入)，[#18079](https://github.com/pingcap/tidb/issues/18079)，[#7587](https://github.com/tikv/tikv/issues/7587)，[#2860](https://github.com/tikv/pd/issues/2860)

Region 在完成成员变更时，由于“添加”和“删除”成员操作分成两步，如果两步操作之间有故障发生会引起 Region 不可用并且会返回前端业务的错误信息。

TiDB 引入的 Raft Joint Consensus 算法将成员变更操作中的“添加”和“删除”合并为一个操作，并发送给所有成员，提升了 Region 成员变更时的可用性。在变更过程中，Region 处于中间的状态，如果任何被修改的成员失败，系统仍然可以使用。

系统默认开启此功能，你可以通过 `pd-ctl config set enable-joint-consensus` 命令设置选项值为 false 关闭此功能。

### 优化内存管理模块，降低系统 OOM 的风险

跟踪统计聚合函数的内存使用情况，系统默认开启该功能，开启后带有聚合函数的 SQL 语句在执行时，如果当前查询内存总的使用量超过 [`mem-quota-query`](/tidb-configuration-file.md#mem-quota-query) 阈值时，系统自动采用 [`oom-action`](/tidb-configuration-file.md#oom-action) 定义的相应操作。

### 提升系统在发生网络分区时的可用性

## 数据迁移

### 从 S3/Aurora 数据迁移到 TiDB

数据迁移类工具支持 Amazon S3（也包含支持 S3 协议的其他存储服务）作为数据迁移的中间转存介质，同时支持将 Aurora 快照数据直接初始化 TiDB 中，丰富了数据从 Amazon S3/Aurora 迁移到 TiDB 的选择。

该功能使用方法可以参照以下文档：

+ [将 MySQL/Aurora 数据导出到 Amazon S3](/dumpling-overview.md#导出到-amazon-s3-云盘)，[#8](https://github.com/pingcap/dumpling/issues/8)
+ [从 Amazon S3 将 Aurora Snapshot 数据初始化到 TiDB](/migrate-from-aurora-using-lightning.md)，[#266](https://github.com/pingcap/tidb-lightning/issues/266)

### TiDB Cloud 数据导入性能优化

数据导入工具 TiDB Lightning 针对 TiDB Cloud AWS T1.standard 配置（及其等同配置）的 TiDB 集群进行了数据导入性能优化，测试结果显式使用 TiDB Lightning 导入 1TB TPC-C 数据到 TiDB，性能提升了 40%，由 254 GiB/h 提升到了 366 GiB/h。

## TiDB 数据共享订阅

### TiCDC 集成第三方生态 Kafka Connect (Confluent Platform)（**实验特性**）

[用户文档](/ticdc/integrate-confluent-using-ticdc.md)，[#660](https://github.com/pingcap/ticdc/issues/660)

为满足将 TiDB 的数据流转到其他系统以支持相关的业务需求，该功能可以把 TiDB 数据流转到 Kafka、Hadoop、Oracle 等系统。

Confluent 平台提供的 kafka connectors 协议支持向不同协议关系型或非关系型数据库传输数据，在社区被广泛使用。TiDB 通过 TiCDC 集成到 Confluent 平台的 Kafka Connect，扩展了 TiDB 数据流转到其他异构数据库或者系统的能力。

### TiCDC 支持 TiDB 集群之间环形同步（**实验特性**）

[用户文档](/ticdc/manage-ticdc.md#环形同步)，[#471](https://github.com/pingcap/ticdc/issues/471)

由于地理位置差异导致的通讯延迟等问题，存在以下场景：用户部署多套 TiDB 集群到不同的地理区域来支撑其当地的业务，然后通过各个 TiDB 之间相互复制，或者汇总复制数据到一个中心 TiDB hub，来完成诸如分析、结算等业务。

TiCDC 支持在多个独立的 TiDB 集群间同步数据。比如有三个 TiDB 集群 A、B 和 C，它们都有一个数据表 test.user_data，并且各自对它有数据写入。环形同步功能可以将 A、B 和 C 对 test.user_data 的写入同步到其它集群上，使三个集群上的 test.user_data 达到最终一致。

该功能适用于以下场景：

+ 多套 TiDB 集群之间相互进行数据备份，灾难发生时业务切换到正常的 TiDB 集群
+ 跨地域部署多套 TiDB 集群支撑当地业务，TiDB 集群之间的同一业务表之间数据需要相互复制

限制与约束：

+ 无法支持业务在不同集群写入使用自增 ID 的业务表，数据复制会导致业务数据相互覆盖而造成数据丢失
+ 无法支持业务在不同集群写入相同业务表的相同数据，数据复制会导致业务数据相互覆盖而造成数据丢失

## 问题诊断

[用户文档](/sql-statements/sql-statement-explain.md#explain)

在排查 SQL 语句性能问题时，需要详细的信息来判断引起性能问题的原因。5.0 版本之前，`EXPLAIN` 收集的信息不够完善，DBA 只能通过日志信息、监控信息或者盲猜的方式来判断问题的原因，效率比较低。

5.0 版本中，通过以下几项优化提升排查问题的效率：

+ 支持对所有 DML 语句使用 `EXPLAIN ANALYZE` 语句以查看实际的执行计划及各个算子的执行详情。[#18056](https://github.com/pingcap/tidb/issues/18056)
+ 支持对正在执行的 SQL 语句使用 `EXPLAIN FOR CONNECTION` 语句以查看实时执行状态，例如各个算子的执行时间、已处理的数据行数等。[#18233](https://github.com/pingcap/tidb/issues/18233)
+ `EXPLAIN ANALYZE` 语句显示的算子执行详情中新增算子发送的 RPC 请求数、处理锁冲突耗时、网络延迟、RocksDB 已删除数据的扫描量、RocksDB 缓存命中情况等。[#18663](https://github.com/pingcap/tidb/issues/18663)
+ 慢查询日志中自动记录 SQL 语句执行时的详细执行状态，输出的信息与 `EXPLAIN ANALYZE` 语句输出信息保持一致，例如各个算子消耗的时间、处理数据行数、发送的 RPC 请求数等。[#15009](https://github.com/pingcap/tidb/issues/15009)

## 部署及运维

### 优化集群部署操作逻辑，帮助 DBA 更快地部署一套标准的 TiDB 生产集群

[用户文档](/production-deployment-using-tiup.md)

DBA 在使用 TiUP 部署 TiDB 集群过程发现环境初始化比较复杂、校验配置过多，集群拓扑文件比较难编辑等问题，导致 DBA 的部署效率比较低。5.0 版本通过以下几个事项提升 DBA 部署 TiDB 的效率：

+ TiUP Cluster 支持使用 `check topo.yaml` 命令，进行更全面一键式环境检查并给出修复建议。
+ TiUP Cluster 支持使用 `check topo.yaml --apply` 命令，自动修复检查过程中发现的环境问题。
+ TiUP Cluster 支持 `template` 命令，获取集群拓扑模板文件，供 DBA 编辑且支持修改全局的节点参数。
+ TiUP 支持使用 `edit-config` 命令编辑 `remote_config` 参数配置远程 Prometheus。
+ TiUP 支持使用 `edit-config` 命令编辑 `external_alertmanagers` 参数配置不同的 AlertManager。
+ 在 tiup-cluster 中使用 `edit-config` 子命令编辑拓扑文件时允许改变配置项值的数据类型。

### 提升升级稳定性

TiUP v1.4.0 版本以前，DBA 使用 tiup-cluster 升级 TiDB 集群时会导致 SQL 响应持续长时间抖动，PD 在线滚动升级期间集群 QPS 抖动时间维持在 10~30s。

TiUP v1.4.0 版本调整了逻辑，优化如下：

+ 升级 PD 时，会主动判断被重启的 PD 节点状态，确认就绪后再滚动升级下一个 PD 节点。
+ 主动识别 PD 角色，先升级 follower 角色 PD 节点，最后再升级 PD Leader 节点。

### 优化升级时长

TiUP v1.4.0 版本以前，DBA 使用 tiup-cluster 升级 TiDB 集群时，对于节点数比较多的集群，整个升级的时间会持续很长，不能满足部分有升级时间窗口要求的用户。

从 v1.4.0 版本起，TiUP 进行了以下几处优化：

+ 新版本 TiUP 支持使用 `tiup cluster upgrade --offline` 子命令实现快速的离线升级。
+ 对于使用滚动升级的用户，新版本 TiUP 默认会加速升级期间 Region Leader 的搬迁速度以减少滚动升级 TiKV 消耗的时间。
+ 运行滚动升级前使用 `check` 子命令，对 Region 监控状态的检查，确保集群升级前状态正常以减少升级失败的概率。

### 支持断点功能

TiUP v1.4.0 版本以前，DBA 使用 tiup-cluster 升级 TiDB 集群时，如果命令执行中断，那么整个升级操作都需重新开始。

新版本 TiUP 支持使用 tiup-cluster `replay` 子命令从断点处重试失败的操作，以避免升级中断后所有操作重新执行。

### 增强运维功能

新版本 TiUP 进一步强化了 TiDB 集群运维的功能：

+ 支持对已停机的 TiDB 和 DM 集群进行升级或 patch 操作，以适应更多用户的使用场景。
+ 为 tiup-cluster 的 `display` 子命令添加 `--version` 参数用于获取集群版本。
+ 在被缩容的节点中仅包含 Prometheus 时不执行更新监控配置的操作，以避免因 Prometheus 节点不存在而缩容失败
+ 在使用 TiUP 命令输入结果不正确时将用户输入的内容添加到错误信息中，以便用户更快定位问题原因。

## 遥测

TiDB 在遥测中新增收集集群的使用指标，包括数据表数量、查询次数、新特性是否启用等。

若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)文档。
