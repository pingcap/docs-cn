---
title: TiDB 基本功能
summary: 了解 TiDB 的基本功能。
aliases: ['/docs-cn/stable/basic-features/','/docs-cn/v4.0/basic-features/']
---

# TiDB 基本功能

本文详细介绍 TiDB 具备的基本功能。

## 数据类型

- 数值类型：BIT、BOOL|BOOLEAN、SMALLINT、MEDIUMINT、INT|INTEGER、BIGINT、FLOAT、DOUBLE、DECIMAL。

- 日期和时间类型：DATE、TIME、DATETIME、TIMESTAMP、YEAR。

- 字符串类型：CHAR、VARCHAR、TEXT、TINYTEXT、MEDIUMTEXT、LONGTEXT、BINARY、VARBINARY、BLOB、TINYBLOB、MEDIUMBLOB、LONGBLOB、ENUM、SET。

- JSON 类型。

## 运算符

- 算术运算符、位运算符、比较运算符、逻辑运算符、日期和时间运算符等。

## 字符集及排序规则 

- 字符集：UTF8、UTF8MB4、BINARY、ASCII、LATIN1。

- 排序规则：UTF8MB4_GENERAL_CI、UTF8MB4_GENERAL_BIN、UTF8_GENERAL_CI、UTF8_GENERAL_BIN、BINARY。

## 函数

- 控制流函数、字符串函数、日期和时间函数、位函数、数据类型转换函数、数据加解密函数、压缩和解压函数、信息函数、JSON 函数、聚合函数、窗口函数等。

## SQL 语句

<<<<<<< HEAD
- 完全支持标准的 Data Definition Language (DDL) 语句，例如：CREATE、DROP、ALTER、RENAME、TRUNCATE 等。

- 完全支持标准的 Data Manipulation Language (DML) 语句，例如：INSERT、REPLACE、SELECT、Subqueries、UPDATE、LOAD DATA 等。

- 完全支持标准的 Transactional and Locking 语句，例如：START TRANSACTION、COMMIT、ROLLBACK、SET TRANSACTION 等。

- 完全支持标准的 Database Administration 语句，例如：SHOW、SET 等。

- 完全支持标准的 Utility 语句，例如：DESCRIBE、EXPLAIN、USE 等。

- 完全支持 SQL GROUP BY 和 ORDER BY 子语句。

- 完全支持标准 SQL 语法的 LEFT OUTER JOIN 和 RIGHT OUTER JOIN。

- 完全支持标准 SQL 要求的表和列别名。

## 分区表

- 支持 Range 分区。

- 支持 Hash 分区。

## 视图

- 支持普通视图。

## 约束

- 支持非空约束。

- 支持主键约束。

- 支持唯一约束。

## 安全

- 支持基于 RBAC (role-based access control) 的权限管理。

- 支持密码管理。

- 支持通信、数据加密。

- 支持 IP 白名单。

- 支持审计功能。

## 工具

- 支持快速备份功能。

- 支持通过工具从 MySQL 迁移数据到 TiDB。

- 支持通过工具部署、运维 TiDB。
=======
| SQL 语句 [^2]                                                               |   6.1  |   6.0  |   5.4    |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| --------------------------------------------------------------------------- | :------: | :------: | :------: | :------: | :------: | :------: | :------: | :------: |
| `SELECT`，`INSERT`，`UPDATE`，`DELETE`，`REPLACE`                           |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| `INSERT ON DUPLICATE KEY UPDATE`                                            |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| `LOAD DATA INFILE`                                                          |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| `SELECT INTO OUTFILE`                                                       |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| `INNER JOIN`, `LEFT\|RIGHT [OUTER] JOIN`                                    |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| `UNION`，`UNION ALL`                                                        |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [`EXCEPT` 和 `INTERSECT` 运算符](/functions-and-operators/set-operators.md) |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    N     |
| `GROUP BY`，`ORDER BY`                                                      |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [窗口函数](/functions-and-operators/window-functions.md)                    |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [公共表表达式 (CTE)](/sql-statements/sql-statement-with.md)                 |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    N     |    N     |
| `START TRANSACTION`，`COMMIT`，`ROLLBACK`                                   |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                       |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)       |   Y     |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [用户自定义变量](/user-defined-variables.md)                                | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md) | Y | N | N | N | N | N | N | N |

## 高级 SQL 功能

| 高级 SQL 功能                                                       |   6.1   |   6.0   |   5.4    |   5.3    |   5.2    |   5.1    |   5.0    | 4.0      |
| ------------------------------------------------------------------- | :------: | :------: | :------: | :------: | :------: | :------: | :------: | -------- |
| [执行计划缓存](/sql-prepared-plan-cache.md)                          |    Y    |    Y    |    Y     |    Y     | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [执行计划管理 (SPM)](/sql-plan-management.md)                       |    Y    |    Y    |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [下推计算结果缓存 (Coprocessor Cache)](/coprocessor-cache.md)       |    Y    |    Y    |    Y     |    Y     |    Y     |    Y     |    Y     | 实验特性 |
| [Stale Read](/stale-read.md)                                        |    Y    |    Y    |    Y     |    Y     |    Y     |    Y     |    N     | N        |
| [Follower Read](/follower-read.md)                                  |    Y    |    Y    |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [通过系统变量 tidb_snapshot 读取历史数据](/read-historical-data.md) |    Y    |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [Optimizer hints](/optimizer-hints.md)                              |    Y    |   Y     |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [MPP 执行引擎](/explain-mpp.md)                                     |    Y    |    Y    |    Y     |    Y     |    Y     |    Y     |    Y     | N        |
| [索引合并](/explain-index-merge.md)                                 |    Y    |    Y    |    Y     | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [基于 SQL 的数据放置规则](/placement-rules-in-sql.md)                |    Y    |    Y    | 实验特性 | 实验特性 |    N     |    N     |    N     | N        |

## 数据定义语言 (DDL)

| 数据定义语言 (DDL)                                           |   6.1   |   6.0   |   5.4    |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| ------------------------------------------------------------ | :------: | :------: | :------: | :------: | :------: | :------: | :------: | :------: |
| `CREATE`，`DROP`，`ALTER`，`RENAME`，`TRUNCATE`              |    Y    |    Y    |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [生成列](/generated-columns.md)                              | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [视图](/views.md)                                            |    Y    |    Y    |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [序列](/sql-statements/sql-statement-create-sequence.md)     |    Y    |   Y      |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [`AUTO_INCREMENT` 列](/auto-increment.md)                    |    Y    |  Y   |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [`AUTO_RANDOM` 列](/auto-random.md)                          |    Y    |    Y   |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| [DDL 算法断言](/sql-statements/sql-statement-alter-table.md) |    Y    |    Y    |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| 在单条语句中添加多列                                         | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [更改列类型](/sql-statements/sql-statement-modify-column.md) |    Y    |    Y    |    Y     |    Y     |    Y     |    Y     |    N     |    N     |
| [临时表](/temporary-tables.md)                               |    Y    |    Y    |    Y     |    Y     |    N     |    N     |    N     |    N     |

## 事务

| 事务                                                                              | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| --------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [Async commit](/system-variables.md#tidb_enable_async_commit-从-v50-版本开始引入) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [1PC](/system-variables.md#tidb_enable_1pc-从-v50-版本开始引入)                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [大事务 (10 GB)](/transaction-overview.md#事务限制)                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [悲观事务](/pessimistic-transaction.md)                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [乐观事务](/optimistic-transaction.md)                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [可重复读隔离（快照隔离）](/transaction-isolation-levels.md)                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [读已提交隔离](/transaction-isolation-levels.md)                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |

## 分区

| 分区                                             | 6.1 | 6.0| 5.4          |   5.3    |   5.2    |   5.1    |   5.0    | 4.0 |
| ------------------------------------------------------------ | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :-----: |
| [Range 分区](/partitioned-table.md)                  | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |    Y    |
| [Hash 分区](/partitioned-table.md)                   | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |    Y    |
| [List 分区](/partitioned-table.md)                   | Y | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |    N    |
| [List COLUMNS 分区](/partitioned-table.md)           | Y | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |    N    |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |    N    |
| [动态裁剪](/partitioned-table.md#动态裁剪模式) | Y | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |      N       |    N    |

## 统计信息

| 统计信息                                                  |   6.1    |   6.0    |   5.4    |   5.3    |   5.2    |   5.1    |   5.0    | 4.0      |
| --------------------------------------------------------- | :------: | :------: | :------: | :------: | :------: | :------: | :------: | -------- |
| [CM-Sketch](/statistics.md)                               | 默认关闭 | 默认关闭 |  默认关闭  |  默认关闭  |  Y  |  Y  |  Y  | Y        |
| [直方图](/statistics.md)                                  |   Y   |   Y   |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| 扩展统计信息（多列）                    | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | N        |
| [统计反馈](/statistics.md#自动更新)                       | 已废弃 | 已废弃 |  已废弃  | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [统计信息自动更新](/statistics.md#自动更新) |   Y   |   Y   |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [快速分析](/system-variables.md#tidb_enable_fast_analyze) | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [动态剪裁](/partitioned-table.md#动态裁剪模式) | Y | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | N | N |

## 安全

| 安全                                                               | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [传输层加密 (TLS)](/enable-tls-between-clients-and-servers.md)     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [静态加密 (TDE)](/encryption-at-rest.md)                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [基于角色的访问控制 (RBAC)](/role-based-access-control.md)         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [证书鉴权](/certificate-authentication.md)                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `caching_sha2_password` 认证                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [与 MySQL 兼容的 `GRANT` 权限管理](/privilege-management.md)       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [动态权限](/privilege-management.md#动态权限)                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [安全增强模式](/system-variables.md#tidb_enable_enhanced_security) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [日志脱敏](/log-redaction.md)                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |

## 数据导入和导出

| 数据导入和导出                                                          |  6.1  |  6.0   |  5.4   |  5.3   |  5.2   |  5.1   |  5.0   |  4.0   |
| ----------------------------------------------------------------------- | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| [快速导入 (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md) |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |
| mydumper 逻辑导入                                                       | 已废弃 | 已废弃 | 已废弃 | 已废弃 | 已废弃 | 已废弃 | 已废弃 | 已废弃 |
| [Dumpling 逻辑导入](/dumpling-overview.md)                              |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |
| [事务 `LOAD DATA`](/sql-statements/sql-statement-load-data.md)          |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    | N [^3] |
| [数据迁移工具](/migration-overview.md)                                  |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)                     |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |
| [Change data capture (CDC)](/ticdc/ticdc-overview.md)                   |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |

## 管理，可视化和工具

| 管理，可视化诊断和工具                                                    |   6.1    |   6.0    |   5.4    |   5.3    |   5.2    |   5.1    |   5.0    | 4.0      |
| ------------------------------------------------------------------------- | :------: | :------: | :------: | :------: | :------: | :------: | :------: | :------: |
| [TiDB Dashboard 图形化展示](/dashboard/dashboard-intro.md)                      |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [TiDB Dashboard 持续性能分析功能](/dashboard/continuous-profiling.md)       |    Y     |    Y     | 实验特性 | 实验特性 |    N     |    N     |    N     | N        |
| [TiDB Dashboard Top SQL 功能](/dashboard/top-sql.md)                      |    Y     |    Y     | 实验特性 |    N     |    N     |    N     |    N     | N        |
| [TiDB Dashboard SQL 诊断功能](/information-schema/information-schema-sql-diagnostics.md)     | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [Information schema](/information-schema/information-schema.md)           |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [Metrics schema](/metrics-schema.md)                                      |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [Statements summary tables](/statement-summary-tables.md)                 |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [慢查询日志](/identify-slow-queries.md)                                   |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [TiUP 部署](/tiup/tiup-overview.md)                                       |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| Ansible 部署                                                              |    N     |    N     |    N     |    N     |    N     |    N     |    N     | 已废弃   |
| [Kubernetes operator](https://docs.pingcap.com/tidb-in-kubernetes/stable) |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [内置物理备份](/br/backup-and-restore-use-cases.md)                       |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     | Y        |
| [Global Kill](/sql-statements/sql-statement-kill.md)                      | Y | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [Lock View](/information-schema/information-schema-data-lock-waits.md)    |    Y     |    Y     |    Y     |    Y     |    Y     | 实验特性 | 实验特性 | 实验特性 |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)             | Y | Y | Y | Y | Y | Y | Y | Y |
| [`SET CONFIG`](/dynamic-config.md)                                        | Y | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
| [DM WebUI](/dm/dm-webui-guide.md)                                        | 实验特性 | 实验特性 |    N     |    N     |    N     |    N     |    N     | N        |

[^1]: TiDB 误将 latin1 处理为 utf8 的子集。见 [TiDB #18955](https://github.com/pingcap/tidb/issues/18955)。

[^2]: TiDB 支持的完整 SQL 列表，见[语句参考](/sql-statements/sql-statement-select.md)。

[^3]: 对于 TiDB v4.0，事务 `LOAD DATA` 不保证原子性。
>>>>>>> 3fa7d5cc6 (correct experimental information in docs (#10813))
