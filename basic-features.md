---
title: TiDB 功能概览
summary: 了解 TiDB 的功能概览。
aliases: ['/docs-cn/dev/basic-features/','/docs-cn/dev/experimental-features-4.0/','/zh/tidb/dev/experimental-features-4.0/','/zh/tidb/dev/experimental-features']
---

# TiDB 功能概览

本文列出了 TiDB 功能在不同版本中的支持变化情况，包括[长期支持版本 (LTS)](/releases/versioning.md#长期支持版本) 和最新的 LTS 版本之后的[开发里程碑版本 (DMR)](/releases/versioning.md#开发里程碑版本)。

> **注意：**
>
> PingCAP 不提供基于 DMR 版本的 bug 修复版本，如有 bug，会在后续版本中修复。如无特殊需求，建议使用[最新 LTS 版本](https://docs.pingcap.com/zh/tidb/stable)。
>
> 下表中出现的缩写字母含义如下：
>
> - Y：已 GA 的功能，可以在生产环境中使用。注意即使某个功能在 DMR 版本中 GA，也建议在后续 LTS 版本中将该功能用于生产环境。
> - N：不支持该功能。
> - E：未 GA 的功能，即实验特性 (experimental)，请注意使用场景限制。实验特性会在未事先通知的情况下发生变化或删除。语法和实现可能会在 GA 前发生变化。如果遇到问题，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 数据类型，函数和操作符

| 数据类型，函数，操作符 | 8.2 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [数值类型](/data-type-numeric.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [日期和时间类型](/data-type-date-and-time.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [字符串类型](/data-type-string.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [JSON 类型](/data-type-json.md) |  Y |  Y |  Y  | Y | Y | E | E | E | E | E |
| [控制流程函数](/functions-and-operators/control-flow-functions.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [字符串函数](/functions-and-operators/string-functions.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [数值函数与操作符](/functions-and-operators/numeric-functions-and-operators.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [日期和时间函数](/functions-and-operators/date-and-time-functions.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [位函数和操作符](/functions-and-operators/bit-functions-and-operators.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [Cast 函数和操作符](/functions-and-operators/cast-functions-and-operators.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [加密和压缩函数](/functions-and-operators/encryption-and-compression-functions.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [信息函数](/functions-and-operators/information-functions.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [JSON 函数](/functions-and-operators/json-functions.md) |  Y |  Y |  Y  | Y | Y | E | E | E | E | E |
| [聚合函数](/functions-and-operators/aggregate-group-by-functions.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [窗口函数](/functions-and-operators/window-functions.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [其他函数](/functions-and-operators/miscellaneous-functions.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [操作符](/functions-and-operators/operators.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [字符集和排序规则](/character-set-and-collation.md) [^1] |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [用户级别锁](/functions-and-operators/locking-functions.md) |  Y |  Y |  Y  | Y | Y | Y | N | N | N | N |

## 索引和约束

| 索引和约束 | 8.2 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [表达式索引](/sql-statements/sql-statement-create-index.md#表达式索引) [^2] |  Y |  Y |  Y  | Y | Y | E | E | E | E | E |
| [列式存储 (TiFlash)](/tiflash/tiflash-overview.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [使用 FastScan 加速 OLAP 场景下的查询](/tiflash/use-fastscan.md) |  Y |  Y |  Y  | Y | E | N | N | N | N | N |
| [RocksDB 引擎](/storage-engine/rocksdb-overview.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [Titan 插件](/storage-engine/titan-overview.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [Titan Level Merge](/storage-engine/titan-configuration.md#level-merge实验功能) |  E |  E |  E  | E | E | E | E | E | E | E |
| [使用 bucket 提高数据扫描并发度](/tune-region-performance.md#使用-bucket-增加并发) |  E |  E |  E  | E | E | E | N | N | N | N |
| [不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [复合主键](/constraints.md#主键约束) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [`CHECK` 约束](/constraints.md#check-约束) |  Y |  Y |  Y  | N | N | N | N | N | N | N |
| [唯一约束](/constraints.md#唯一约束) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [整型主键上的聚簇索引](/clustered-indexes.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [复合或非整型主键上的聚簇索引](/clustered-indexes.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [多值索引](/sql-statements/sql-statement-create-index.md#多值索引) |  Y |  Y |  Y  | Y | N | N | N | N | N | N |
| [外键约束](/constraints.md#外键约束) |  E |  E |  E  | E | N | N | N | N | N | N |
| [TiFlash 延迟物化](/tiflash/tiflash-late-materialization.md) |  Y |  Y |  Y  | Y | N | N | N | N | N | N |

## SQL 语句

| SQL 语句 [^3] | 8.2 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `SELECT`，`INSERT`，`UPDATE`，`DELETE`，`REPLACE` |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| `INSERT ON DUPLICATE KEY UPDATE` |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| `LOAD DATA INFILE` |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| `SELECT INTO OUTFILE` |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| `INNER JOIN`, <code>LEFT\|RIGHT [OUTER] JOIN</code> |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| `UNION`，`UNION ALL` |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [`EXCEPT` 和 `INTERSECT` 运算符](/functions-and-operators/set-operators.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| `GROUP BY`，`ORDER BY` |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [窗口函数](/functions-and-operators/window-functions.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [公共表表达式 (CTE)](/sql-statements/sql-statement-with.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| `START TRANSACTION`，`COMMIT`，`ROLLBACK` |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [用户自定义变量](/user-defined-variables.md) |  E |  E |  E  | E | E | E | E | E | E | E |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md) |  Y |  Y |  Y  | Y | Y | Y | N | N | N | N |
| [`BATCH [ON COLUMN] LIMIT INTEGER INSERT/UPDATE/REPLACE`](/sql-statements/sql-statement-batch.md) |  Y |  Y |  Y  | Y | Y | N | N | N | N | N |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) |  Y |  Y |  Y  | Y | Y | E | N | N | N | N |
| [表级锁 (Table Lock)](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) |  E  |  E  |  E  | E | E | E | E | E | E | E |
| [物化列式存储的查询结果](/tiflash/tiflash-results-materialization.md) |  Y |  Y |  Y  | Y | E | N | N | N | N | N |

## 高级 SQL 功能

| 高级 SQL 功能 | 8.2 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [Prepare 语句执行计划缓存](/sql-prepared-plan-cache.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | E | E |
| [非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md) |  Y  |  Y  |  Y  | E | N | N | N | N | N | N |
| [执行计划绑定 (SQL Binding)](/sql-plan-management.md#执行计划绑定-sql-binding) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [跨数据库执行计划绑定 (Cross-DB Binding)](/sql-plan-management.md#跨数据库绑定执行计划-cross-db-binding) |  Y  |  Y  |  N  | N | N | N | N | N | N | N |
| [根据历史执行计划创建绑定](/sql-plan-management.md#根据历史执行计划创建绑定) |  Y  |  Y  |  Y  | Y | E | N | N | N | N | N |
| [下推计算结果缓存 (Coprocessor Cache)](/coprocessor-cache.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [Stale Read](/stale-read.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [Follower Read](/follower-read.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [通过系统变量 `tidb_snapshot` 读取历史数据](/read-historical-data.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [Optimizer hints](/optimizer-hints.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [MPP 执行引擎](/explain-mpp.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [MPP 执行引擎 - compression exchange](/explain-mpp.md#mpp-version-和-exchange-数据压缩) |  Y  |  Y  |  Y  | Y | N | N | N | N | N | N |
| [TiFlash Pipeline 执行模型](/tiflash/tiflash-pipeline-model.md) |  Y  |  Y  |  Y  | N | N | N | N | N | N | N |
| [TiFlash 副本选择策略](/system-variables.md#tiflash_replica_read-从-v730-版本开始引入) |  Y  |  Y  |  Y  | N | N | N | N | N | N | N |
| [索引合并](/explain-index-merge.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | E | E | E |
| [基于 SQL 的数据放置规则](/placement-rules-in-sql.md) |  Y  |  Y  |  Y  | Y | Y | Y | E | E | N | N |
| [Cascades Planner](/system-variables.md#tidb_enable_cascades_planner) |  E  |  E  |  E  | E | E | E | E | E | E | E |
| [Runtime Filter](/runtime-filter.md) |  Y  |  Y  |  Y  | N | N | N | N | N | N | N |

## 数据定义语言 (DDL)

| 数据定义语言 (DDL) | 8.2 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CREATE`，`DROP`，`ALTER`，`RENAME`，`TRUNCATE` |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [生成列](/generated-columns.md) |  Y  |  Y  |  Y  | Y | E | E | E | E | E | E |
| [视图](/views.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [序列](/sql-statements/sql-statement-create-sequence.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [`AUTO_INCREMENT` 列](/auto-increment.md) |  Y  |  Y  |  Y  | Y | Y[^4] | Y | Y | Y | Y | Y |
| [`AUTO_RANDOM` 列](/auto-random.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [TTL (Time to Live)](/time-to-live.md) |  Y  |  Y  |  Y  | Y | E | N | N | N | N | N |
| [DDL 算法断言](/sql-statements/sql-statement-alter-table.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| 在单条语句中添加多列 |  Y  |  Y  |  Y  | Y | Y | E | E | E | E | E |
| [更改列类型](/sql-statements/sql-statement-modify-column.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [临时表](/temporary-tables.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | N | N |
| 并行 DDL |  Y  |  Y  |  Y  | Y | Y | N | N | N | N | N |
| [添加索引加速](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) |  Y  |  Y  |  Y  | Y | Y | N | N | N | N | N |
| [元数据锁](/metadata-lock.md) |  Y  |  Y  |  Y  | Y | Y | N | N | N | N | N |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) |  Y  |  Y  |  Y  | Y | Y | N | N | N | N | N |
| [暂停](/sql-statements/sql-statement-admin-pause-ddl.md)/[恢复](/sql-statements/sql-statement-admin-resume-ddl.md) DDL |  Y  |  Y  | Y | N | N | N | N | N | N | N |
| [TiDB 加速建表](/accelerated-table-creation.md) | E | E | N | N | N | N | N | N | N | N |
| [设置 BDR Role 用于 TiCDC 双向同步时同步 DDL](/sql-statements/sql-statement-admin-bdr-role.md#admin-setshowunset-bdr-role) | E | E | N | N | N | N | N | N | N | N |

## 事务

| 事务 | 8.2 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [Async commit](/system-variables.md#tidb_enable_async_commit-从-v50-版本开始引入) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [1PC](/system-variables.md#tidb_enable_1pc-从-v50-版本开始引入) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [大事务 (10 GB)](/transaction-overview.md#事务限制) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [悲观事务](/pessimistic-transaction.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [乐观事务](/optimistic-transaction.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [可重复读隔离（快照隔离）](/transaction-isolation-levels.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [读已提交隔离](/transaction-isolation-levels.md) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [自动终止长时间未提交的空闲事务](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入) |  Y  |  Y  | N | N | N | N | N | N | N | N |

## 分区

| 分区 | 8.2 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [Range 分区](/partitioned-table.md#range-分区) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [Hash 分区](/partitioned-table.md#hash-分区) |  Y  |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [Key 分区](/partitioned-table.md#key-分区) |  Y  |  Y  |  Y  | Y | N | N | N | N | N | N |
| [List 分区](/partitioned-table.md#list-分区) |  Y  |  Y  |  Y  | Y | Y | Y | E | E | E | E |
| [List COLUMNS 分区](/partitioned-table.md#list-columns-分区) |  Y  |  Y  |  Y  | Y | Y | Y | E | E | E | E |
| [List 和 List COLUMNS 分区表的默认分区](/partitioned-table.md#默认的-list-分区) |  Y  |  Y  |  Y  | N | N | N | N | N | N | N |
| [`EXCHANGE PARTITION`](/partitioned-table.md) |  Y  |  Y  |  Y  | Y | Y | E | E | E | E | E |
| [`REORGANIZE PARTITION`](/partitioned-table.md#重组分区) |  Y  |  Y  |  Y  | Y | N | N | N | N | N | N |
| [`COALESCE PARTITION`](/partitioned-table.md#减少分区数量) |  Y  |  Y  |  Y  | Y | N | N | N | N | N | N |
| [动态裁剪](/partitioned-table.md#动态裁剪模式) |  Y  |  Y  |  Y  | Y | Y | Y | E | E | E | E |
| [Range COLUMNS 分区](/partitioned-table.md#range-columns-分区) |  Y  |  Y  |  Y  | Y | Y | N | N | N | N | N |
| [Range INTERVAL 分区](/partitioned-table.md#range-interval-分区) |  Y  |  Y  |  Y  | Y | E | N | N | N | N | N |
| [分区表转换为非分区表](/partitioned-table.md#将分区表转换为非分区表) |  Y  |  Y  |  Y  | N | N | N | N | N | N | N |
| [对现有表进行分区](/partitioned-table.md#对现有表进行分区) |  Y  |  Y  |  Y  | N | N | N | N | N | N | N |

## 统计信息

| 统计信息 | 8.2 | 8.1 | 7.5  | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:----:|:----:|:----:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [CM-Sketch](/statistics.md) | 默认关闭| 默认关闭| 默认关闭 | 默认关闭 | 默认关闭 | 默认关闭 | 默认关闭 | 默认关闭 | Y | Y |
| [直方图](/statistics.md) |  Y  |  Y  |  Y   | Y | Y | Y | Y | Y | Y | Y |
| [扩展统计信息](/extended-statistics.md) |  E  |  E  |  E   | E | E | E | E | E | E | E |
| 统计反馈 |  N  |  N  |  N   | N | N | 已废弃 | 已废弃 | E | E | E |
| [统计信息自动更新](/statistics.md#自动更新) |  Y  |  Y  | Y | Y | Y | Y | Y | Y | Y | Y |
| [动态裁剪](/partitioned-table.md#动态裁剪模式) |  Y   |  Y   |  Y   | Y | Y | Y | E | E | E | E |
| [收集部分列的统计信息](/statistics.md#收集部分列的统计信息) |  E   |  E   |  E   | E | E | E | E | N | N | N |
| [限制统计信息的内存使用量](/statistics.md#统计信息收集的内存限制) |  E  |  E  |  E   | E | E | E | N | N | N | N |
| [随机采样约 10000 行数据来快速构建统计信息](/system-variables.md#tidb_enable_fast_analyze) | 已废弃 | 已废弃 | 已废弃 | E | E | E | E | E | E | E |
| [锁定统计信息](/statistics.md#锁定统计信息) |  Y  |  Y  |  Y   | E | E | N | N | N | N | N |
| [轻量级统计信息初始化](/statistics.md#加载统计信息) |  Y  |  Y  |  Y   | E | N | N | N | N | N | N |
| [显示统计信息收集的进度](/sql-statements/sql-statement-show-analyze-status.md) |  Y  |  Y  |  Y   | N | N | N | N | N | N | N |

## 安全

| 安全 | 8.2 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [传输层加密 (TLS)](/enable-tls-between-clients-and-servers.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [静态加密 (TDE)](/encryption-at-rest.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [基于角色的访问控制 (RBAC)](/role-based-access-control.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [证书鉴权](/certificate-authentication.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [`caching_sha2_password` 认证](/system-variables.md#default_authentication_plugin) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | N |
| [`tidb_sm3_password` 认证](/system-variables.md#default_authentication_plugin) |  Y |  Y |  Y  | Y | Y | N | N | N | N | N |
| [`tidb_auth_token` 认证](/security-compatibility-with-mysql.md#tidb_auth_token) |  Y |  Y |  Y  | Y | Y | N | N | N | N | N |
| [`authentication_ldap_sasl` 认证](/system-variables.md#default_authentication_plugin) |  Y |  Y |  Y  | Y | N | N | N | N | N | N |
| [`authentication_ldap_simple` 认证](/system-variables.md#default_authentication_plugin) |  Y |  Y |  Y  | Y | N | N | N | N | N | N |
| [密码管理](/password-management.md) |  Y |  Y |  Y  | Y | Y | N | N | N | N | N |
| [与 MySQL 兼容的 `GRANT` 权限管理](/privilege-management.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [动态权限](/privilege-management.md#动态权限) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [安全增强模式](/system-variables.md#tidb_enable_enhanced_security) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |
| [日志脱敏](/log-redaction.md) |  Y |  Y |  Y  | Y | Y | Y | Y | Y | Y | Y |

## 数据导入和导出

| 数据导入和导出 | 8.2 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [快速导入 (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [快速导入 (`IMPORT INTO`)](/sql-statements/sql-statement-import-into.md) | Y | Y | Y | N | N | N | N | N | N | N |
| mydumper 逻辑导出 | 已废弃 | 已废弃 | 已废弃 | 已废弃 | 已废弃 | 已废弃 | 已废弃 | 已废弃 | 已废弃 | 已废弃 |
| [Dumpling 逻辑导出](/dumpling-overview.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [事务 `LOAD DATA`](/sql-statements/sql-statement-load-data.md) [^5] | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [数据迁移工具](/migration-overview.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) [^6] | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [Change data capture (CDC)](/ticdc/ticdc-overview.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [TiCDC 支持保存数据到存储服务 (Amazon S3/GCS/Azure Blob Storage/NFS)](/ticdc/ticdc-sink-to-cloud-storage.md) | Y | Y | Y | Y | E | N | N | N | N | N |
| [TiCDC 支持在两个 TiDB 集群之间进行双向复制](/ticdc/ticdc-bidirectional-replication.md) | Y | Y | Y | Y | Y | N | N | N | N | N |
| [TiCDC OpenAPI v2](/ticdc/ticdc-open-api-v2.md) | Y | Y | Y | Y | N | N | N | N | N | N |
| [DM](/dm/dm-overview.md) 支持迁移 MySQL 8.0  | Y | Y | E | E | E | E | N | N | N | N |

## 管理，可视化和工具

| 管理，可视化和工具 | 8.2 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [TiDB Dashboard 图形化展示](/dashboard/dashboard-intro.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [TiDB Dashboard 持续性能分析功能](/dashboard/continuous-profiling.md) | Y | Y | Y | Y | Y | Y | E | E | N | N |
| [TiDB Dashboard Top SQL 功能](/dashboard/top-sql.md) | Y | Y | Y | Y | Y | Y | E | N | N | N |
| [TiDB Dashboard SQL 诊断功能](/information-schema/information-schema-sql-diagnostics.md) | Y | Y | Y | Y | Y | E | E | E | E | E |
| [TiDB Dashboard 集群诊断功能](/dashboard/dashboard-diagnostics-access.md) | Y | Y | Y | Y | Y | E | E | E | E | E |
| [Grafana 中的 TiKV-FastTune 面板](/grafana-tikv-dashboard.md#tikv-fasttune-面板) | E | E | E | E | E | E | E | E | E | E |
| [Information schema](/information-schema/information-schema.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [Metrics schema](/metrics-schema.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [Statements summary tables](/statement-summary-tables.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [Statements summary tables - 持久化 statements summary](/statement-summary-tables.md#持久化-statements-summary) | E | E | E | E | N | N | N | N | N | N |
| [慢查询日志](/identify-slow-queries.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [TiUP 部署](/tiup/tiup-overview.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [Kubernetes operator](https://docs.pingcap.com/tidb-in-kubernetes/stable) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [内置物理备份](/br/backup-and-restore-use-cases.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [Global Kill](/sql-statements/sql-statement-kill.md) | Y | Y | Y | Y | Y | Y | E | E | E | E |
| [Lock View](/information-schema/information-schema-data-lock-waits.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | E |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [`SET CONFIG`](/dynamic-config.md) | Y | Y | Y | Y | Y | Y | E | E | E | E |
| [DM WebUI](/dm/dm-webui-guide.md) | E | E | E | E | E | E | N | N | N | N |
| [前台限流](/tikv-configuration-file.md#前台限流) | Y | Y | Y | Y | Y | E | N | N | N | N |
| [后台限流](/tikv-configuration-file.md#后台限流) | E | E | E | E | E | N | N | N | N | N |
| [基于 EBS 的备份和恢复](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.4/volume-snapshot-backup-restore) | Y | Y | Y | Y | Y | N | N | N | N | N |
| [PITR](/br/br-pitr-guide.md) | Y | Y | Y | Y | Y | N | N | N | N | N |
| [全局内存控制](/configure-memory-usage.md#如何配置-tidb-server-实例使用内存的阈值) | Y | Y | Y | Y | Y | N | N | N | N | N |
| [RawKV 跨集群复制](/tikv-configuration-file.md#api-version-从-v610-版本开始引入) | E | E | E| E | E | N | N | N | N | N |
| [Green GC](/system-variables.md#tidb_gc_scan_lock_mode-从-v50-版本开始引入) | E | E | E | E | E | E | E | E | E | E |
| [资源管控 (Resource Control)](/tidb-resource-control.md) | Y | Y | Y | Y | N | N | N | N | N | N |
| [Runaway Queries 自动管理](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries) | Y | Y | E | N | N | N | N | N | N | N |
| [后台任务资源管控](/tidb-resource-control.md#管理后台任务) | E | E | E | N | N | N | N | N | N | N |
| [TiFlash 存算分离架构与 S3 支持](/tiflash/tiflash-disaggregated-and-s3.md) | Y | Y | Y | E | N | N | N | N | N | N |
| [选择执行分布式执行框架任务的 TiDB 节点](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) | Y | Y | Y | N | N | N | N | N | N | N |
| 通过系统变量 [`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-从-v530-版本开始引入) 控制 PD Follower Proxy 功能 | Y | Y | Y | Y | Y | Y | Y | Y | N | N |
| 通过系统变量 [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-从-v760-版本开始引入) 控制 [Active PD Follower](/tune-region-performance.md#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力) 功能 | E | E | N | N | N | N | N | N | N | N |
| [PD 微服务](/pd-microservices.md) | E | E | N | N | N | N | N | N | N | N |
| [TiDB 分布式执行框架](/tidb-distributed-execution-framework.md) | Y | Y | Y | E | N | N | N | N | N | N |
| [全局排序](/tidb-global-sort.md) | Y | Y | E | N | N | N | N | N | N | N |
| [TiProxy](/tiproxy/tiproxy-overview.md) | Y | Y | N | N | N | N | N | N | N | N |

[^1]: TiDB 误将 latin1 处理为 utf8 的子集。见 [TiDB #18955](https://github.com/pingcap/tidb/issues/18955)。

[^2]: 从 v6.5.0 起，系统变量 [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-从-v520-版本开始引入) 所列出的函数已通过表达式索引的测试，可以在生产环境中创建并使用，未来版本会持续增加。对于没有列出的函数，则不建议在生产环境中使用相应的表达式索引。详情请参考[表达式索引](/sql-statements/sql-statement-create-index.md#表达式索引)。

[^3]: TiDB 支持的完整 SQL 列表，见[语句参考](/sql-statements/sql-statement-select.md)。

[^4]: 从 [TiDB v6.4.0](/releases/release-6.4.0.md) 开始，支持[高性能、全局单调递增的 `AUTO_INCREMENT` 列](/auto-increment.md#mysql-兼容模式)。

[^5]: 从 [TiDB v7.0.0](/releases/release-7.0.0.md) 开始新增的参数 `FIELDS DEFINED NULL BY` 以及新增支持从 S3 和 GCS 导入数据，均为实验特性。从 [TiDB v7.6.0](/releases/release-7.6.0.md) 开始 `LOAD DATA` 的事务行为与 MySQL 的事务行为一致，包括事务内的 `LOAD DATA` 语句本身不再自动提交当前事务，也不会开启新事务，并且事务内的 `LOAD DATA` 语句可以被显式提交或者回滚。此外，`LOAD DATA` 语句会受 TiDB 事务模式设置（乐观/悲观）影响。

[^6]: 从 v7.5.0 开始，不再提供 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) 数据同步功能的技术支持，强烈建议使用 [TiCDC](/ticdc/ticdc-overview.md) 实现高效稳定的数据同步。尽管 TiDB Binlog 在 v7.5.0 仍支持 Point-in-Time Recovery (PITR) 场景，但是该组件在未来 LTS 版本中将被完全废弃，推荐使用 [PITR](/br/br-pitr-guide.md) 替代。
