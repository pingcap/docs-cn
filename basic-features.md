---
title: TiDB 基本功能
summary: 了解 TiDB 的基本功能。
---

# TiDB 基本功能

本文列出了 TiDB 功能在各版本的支持变化情况。请注意，实验特性的支持可能会在最终版本发布前发生变化。

## 数据类型，函数和操作符

| 数据类型，函数，操作符                                                                     | 5.2          | 5.1          | 5.0          | 4.0          |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| [数值类型](/data-type-numeric.md)                                                                   | Y            | Y            | Y            | Y            |
| [日期和时间类型](/data-type-date-and-time.md)                                                       | Y            | Y            | Y            | Y            |
| [字符串类型](/data-type-string.md)                                                                     | Y            | Y            | Y            | Y            |
| [JSON 类型](/data-type-json.md)                                                                          | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [控制流程函数](/functions-and-operators/control-flow-functions.md)                             | Y            | Y            | Y            | Y            |
| [字符串函数](/functions-and-operators/string-functions.md)                                         | Y            | Y            | Y            | Y            |
| [数值函数与操作符](/functions-and-operators/numeric-functions-and-operators.md)           | Y            | Y            | Y            | Y            |
| [日期和时间函数](/functions-and-operators/date-and-time-functions.md)                           | Y            | Y            | Y            | Y            |
| [位函数和操作符](/functions-and-operators/bit-functions-and-operators.md)                   | Y            | Y            | Y            | Y            |
| [Cast 函数和操作符](/functions-and-operators/cast-functions-and-operators.md)                 | Y            | Y            | Y            | Y            |
| [加密和压缩函数](/functions-and-operators/encryption-and-compression-functions.md) | Y            | Y            | Y            | Y            |
| [信息函数](/functions-and-operators/information-functions.md)                               | Y            | Y            | Y            | Y            |
| [JSON 函数](/functions-and-operators/json-functions.md)                                             | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [聚合函数](/functions-and-operators/aggregate-group-by-functions.md)                        | Y            | Y            | Y            | Y            |
| [窗口函数](/functions-and-operators/window-functions.md)                                         | Y            | Y            | Y            | Y            |
| [其他函数](/functions-and-operators/miscellaneous-functions.md)                           | Y            | Y            | Y            | Y            |
| [操作符](/functions-and-operators/operators.md)                                                       | Y            | Y            | Y            | Y            |
| [字符集和排序规则](/character-set-and-collation.md) [^1]                                    | Y            | Y            | Y            | Y            |

## 索引和约束

| 索引和约束                                                                             | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| [表达式索引](/sql-statements/sql-statement-create-index.md#表达式索引)                     | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [列式存储 (TiFlash)](/tiflash/tiflash-overview.md)                                               | Y            | Y            | Y            | Y            |
| [RocksDB 引擎](/storage-engine/rocksdb-overview.md)                                                    | Y            | Y            | Y            | Y            |
| [Titan 插件](/storage-engine/titan-overview.md)                                                        | Y            | Y            | Y            | Y            |
| [不可见索引](/sql-statements/sql-statement-add-index.md)                                          | Y            | Y            | Y            | N            |
| [复合主键](/constraints.md#主键约束)                                                               | Y            | Y            | Y            | Y            |
| [唯一约束](/constraints.md#唯一约束)                                                                        | Y            | Y            | Y            | Y            |
| [整型主键上的聚簇索引](/constraints.md)                                              | Y            | Y            | Y            | Y            |
| [复合或非整型主键上的聚簇索引](/constraints.md)                                       | Y            | Y            | Y            | N            |

## SQL 语句

| SQL 语句 [^2]                                                                                  | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| `SELECT`，`INSERT`，`UPDATE`，`DELETE`，`REPLACE`                                                  | Y            | Y            | Y            | Y            |
| `INSERT ON DUPLICATE KEY UPDATE`                                                                         | Y            | Y            | Y            | Y            |
| `LOAD DATA INFILE`                                                                                       | Y            | Y            | Y            | Y            |
| `SELECT INTO OUTFILE`                                                                                    | Y            | Y            | Y            | Y            |
| `INNER JOIN`, `LEFT\|RIGHT [OUTER] JOIN`                                                                 | Y            | Y            | Y            | Y            |
| `UNION`，`UNION ALL`                                                                                     | Y            | Y            | Y            | Y            |
| [`EXCEPT` 和 `INTERSECT` 运算符](/functions-and-operators/set-operators.md)                          | Y            | Y            | Y            | N            |
| `GROUP BY`，`ORDER BY`                                                                                   | Y            | Y            | Y            | Y            |
| [窗口函数](/functions-and-operators/window-functions.md)                                         | Y            | Y            | Y            | Y            |
| [公共表表达式 (CTE)](/sql-statements/sql-statement-with.md)                                  | Y            | Y            | N            | N            |
| `START TRANSACTION`，`COMMIT`，`ROLLBACK`                                                                | Y            | Y            | Y            | Y            |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                                                    | Y            | Y            | Y            | Y            |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)                                    | Y            | Y            | Y            | Y            |
| [用户自定义变量](/user-defined-variables.md)                                                     | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [表级锁 (Table Lock)](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)            | 实验特性 | 实验特性 | 实验特性 | 实验特性 |

## 高级 SQL 功能

| 高级 SQL 功能                                                                                | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| [执行计划缓存](/sql-prepare-plan-cache.md)                                                   | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [执行计划管理 (SPM)](/sql-plan-management.md)                                                     | Y            | Y            | Y            | Y            |
| [下推计算结果缓存 (Coprocessor Cache)](/coprocessor-cache.md)                                                               | Y            | Y            | Y            | 实验特性 |
| [Stale Read](/stale-read.md)                                                                             | Y            | Y            | N            | N            |
| [Follower Read](/follower-read.md)                                                                      | Y            | Y            | Y            | Y            |
| [通过系统变量 tidb_snapshot 读取历史数据](/read-historical-data.md)                                         | Y            | Y            | Y            | Y            |
| [Optimizer hints](/optimizer-hints.md)                                                                   | Y            | Y            | Y            | Y            |
| [MPP 执行引擎](/explain-mpp.md)                                                                   | Y            | Y            | Y            | N            |
| [Index Merge Join](/explain-index-merge.md)                                                              | 实验特性 | 实验特性 | 实验特性 | 实验特性 |

## 数据定义语言 (DDL)

| 数据定义语言 (DDL)                                                                       | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| `CREATE`，`DROP`，`ALTER`，`RENAME`，`TRUNCATE`                                                    | Y            | Y            | Y            | Y            |
| [生成列](/generated-columns.md)                                                               | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [视图](/views.md)                                                                                       | Y            | Y            | Y            | Y            |
| [序列](/sql-statements/sql-statement-create-sequence.md)                                            | Y            | Y            | Y            | Y            |
| [`AUTO_INCREMENT` 列](/auto-increment.md)                                                                     | Y            | Y            | Y            | Y            |
| [`AUTO_RANDOM` 列](/auto-random.md)                                                                           | Y            | Y            | Y            | Y            |
| [DDL 算法断言](/sql-statements/sql-statement-alter-table.md)                                 | Y            | Y            | Y            | Y            |
| [在单条语句中添加多列](/system-variables.md#tidb_enable_change_multi_schema)                                                                       | 实验特性            | 实验特性           | 实验特性            | 实验特性           |
| [更改列类型](/sql-statements/sql-statement-modify-column.md)                                     | Y            | Y            | N            | N            |

## 事务

| 事务                                                                                         | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| [Async commit](/system-variables.md#tidb_enable_async_commit-从-v50-版本开始引入)                                 | Y            | Y            | Y            | N            |
| [1PC](/system-variables.md#tidb_enable_1pc-从-v50-版本开始引入)                                                   | Y            | Y            | Y            | N            |
| [大事务 (10 GB)](/transaction-overview.md#事务限制)                             | Y            | Y            | Y            | Y            |
| [悲观事务](/pessimistic-transaction.md)                                                  | Y            | Y            | Y            | Y            |
| [乐观事务](/optimistic-transaction.md)                                                    | Y            | Y            | Y            | Y            |
| [可重复读隔离（快照隔离）](/transaction-isolation-levels.md)                       | Y            | Y            | Y            | Y            |
| [读已提交隔离](/transaction-isolation-levels.md)                                             | Y            | Y            | Y            | Y            |

## 分区

| 分区                                                                                         | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| [Range 分区](/partitioned-table.md)                                                              | Y            | Y            | Y            | Y            |
| [Hash 分区](/partitioned-table.md)                                                               | Y            | Y            | Y            | Y            |
| [List 分区](/partitioned-table.md)                                                               | 实验特性 | 实验特性 | 实验特性 | N            |
| [List COLUMNS 分区](/partitioned-table.md)                                                       | 实验特性 | 实验特性 | 实验特性 | N            |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                                                            | 实验特性 | 实验特性 | 实验特性 | N            |
| [动态裁剪](/partitioned-table.md#动态裁剪模式)                                            | 实验特性 | 实验特性 | N            | N            |

## 统计信息

| 统计信息                                                                                           | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| [CM-Sketch](/statistics.md)                                                                               | 已废弃   | 已废弃   | 已废弃   | Y            |
| [直方图](/statistics.md)                                                                             | Y            | Y            | Y            | Y            |
| 扩展统计信息（多列）                                                 | 实验特性 | 实验特性 | 实验特性 | N            |
| [统计反馈](/statistics.md#自动更新)                                                   | 实验特性 | 实验特性 | 实验特性 | 实验特性 |

## 安全

| 安全                                                                                             | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| [传输层加密 (TLS)](/enable-tls-between-clients-and-servers.md)                           | Y            | Y            | Y            | Y            |
| [静态加密 (TDE)](/encryption-at-rest.md)                                                       | Y            | Y            | Y            | Y            |
| [基于角色的访问控制 (RBAC)](/role-based-access-control.md)                                        | Y            | Y            | Y            | Y            |
| [证书鉴权](/certificate-authentication.md)                                       | Y            | Y            | Y            | Y            |
| `caching_sha2_password` 认证                                                                   | Y            | N            | N            | N            |
| [与 MySQL 兼容的 `GRANT` 权限管理](/privilege-management.md)                                              | Y            | Y            | Y            | Y            |
| [动态权限](/privilege-management.md#动态权限)                                        | Y            | Y            | N            | N            |
| [安全增强模式](/system-variables.md#tidb_enable_enhanced_security)                             | Y            | Y            | N            | N            |
| [日志脱敏](/log-redaction.md)                                                                  | Y            | Y            | Y            | N            |

## 数据导入和导出

| 数据导入和导出                                                                               | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| [快速导入 (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md)                             | Y            | Y            | Y            | Y            |
| mydumper 逻辑导出                                                                                  | 已废弃   | 已废弃   | 已废弃   | 已废弃   |
| [Dumpling 逻辑导出](/dumpling-overview.md)                                                         | Y            | Y            | Y            | Y            |
| [事务 `LOAD DATA`](/sql-statements/sql-statement-load-data.md)                                  | Y            | Y            | Y            | N            |
| [数据迁移工具](/migration-overview.md)                                                | Y            | Y            | Y            | Y            |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)                                                      | Y   | Y   | Y   | Y   |
| [Change data capture (CDC)](/ticdc/ticdc-overview.md)                                                    | Y            | Y            | Y            | Y            |

## 管理，可视化和工具

| 管理，可视化诊断和工具                                                                  | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|
| [TiDB Dashboard](/dashboard/dashboard-intro.md)                                                          | Y            | Y            | Y            | Y            |
| [SQL 诊断](/information-schema/information-schema-sql-diagnostics.md)                             | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [Information schema](/information-schema/information-schema.md)                                          | Y            | Y            | Y            | Y            |
| [Metrics schema](/metrics-schema.md)                                                                     | Y            | Y            | Y            | Y            |
| [Statements summary tables](/statement-summary-tables.md)                                                | Y            | Y            | Y            | Y            |
| [慢查询日志](/identify-slow-queries.md)                                                              | Y            | Y            | Y            | Y            |
| [TiUP 部署](/tiup/tiup-overview.md)                                                                | Y            | Y            | Y            | Y            |
| Ansible 部署                                                                                       | N            | N            | N            | 已废弃   |
| [Kubernetes operator](https://docs.pingcap.com/tidb-in-kubernetes/stable)                                      | Y            | Y            | Y            | Y            |
| [内置物理备份](/br/backup-and-restore-use-cases.md)                                          | Y            | Y            | Y            | Y            |
| Top SQL                                                                                                  | Y            | N            | N            | N            |
| [Global Kill](/sql-statements/sql-statement-kill.md)                                                     | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [Lock View](/information-schema/information-schema-data-lock-waits.md)                                   | Y            | 实验特性 | 实验特性 | 实验特性 |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)                                            | Y | Y | Y | Y |
| [`SET CONFIG`](/dynamic-config.md)                                                                       | 实验特性 | 实验特性 | 实验特性 | 实验特性 |

[^1]: TiDB 误将 latin1 处理为 utf8 的子集。见 [TiDB #18955](https://github.com/pingcap/tidb/issues/18955)。

[^2]: TiDB 支持的完整 SQL 列表，见[语句参考](/sql-statements/sql-statement-select.md)。
