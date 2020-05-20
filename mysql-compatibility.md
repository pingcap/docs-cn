---
title: 与 MySQL 兼容性对比
summary: 本文对 TiDB 和 MySQL 二者之间从语法和功能特性上做出详细的对比。
category: reference
aliases: ['/docs-cn/dev/reference/mysql-compatibility/']
---

# 与 MySQL 兼容性对比

TiDB 支持 MySQL 传输协议及其绝大多数的语法。这意味着您现有的 MySQL 连接器和客户端都可以继续使用。大多数情况下您现有的应用都可以迁移至 TiDB，无需任何代码修改。

当前 TiDB 服务器官方支持的版本为 MySQL 5.7。大部分 MySQL 运维工具（如 PHPMyAdmin, Navicat, MySQL Workbench 等），以及备份恢复工具（如 mysqldump, Mydumper/myloader）等都可以直接使用。

不过一些特性由于在分布式环境下没法很好的实现，目前暂时不支持或者是表现与 MySQL 有差异。一些 MySQL 语法在 TiDB 中可以解析通过，但是不会做任何后续的处理，例如 `Create Table` 语句中 `Engine`，是解析并忽略。

> **注意：**
>
> 本页内容仅涉及 MySQL 与 TiDB 的总体差异。关于[安全特性](/security-compatibility-with-mysql.md)、[悲观事务模型](/pessimistic-transaction.md#和-mysql-innodb-的差异)的兼容信息请查看各自具体页面。

## 不支持的特性

* 存储过程与函数
* 触发器
* 事件
* 自定义函数
* 外键约束
* 全文/空间函数与索引
* 非 `ascii`/`latin1`/`binary`/`utf8`/`utf8mb4` 的字符集
* SYS schema
* MySQL 追踪优化器
* XML 函数
* X Protocol
* Savepoints
* 列级权限
* `XA` 语法（TiDB 内部使用两阶段提交，但并没有通过 SQL 接口公开）
* `CREATE TABLE tblName AS SELECT stmt` 语法
* `CREATE TEMPORARY TABLE` 语法
* `CHECK TABLE` 语法
* `CHECKSUM TABLE` 语法
* `SELECT INTO FILE` 语法

## 与 MySQL 有差异的特性

### 自增 ID

TiDB 中，对于自增列隐式分配的值，只保证单节点的自增和全局节点的唯一，不保证连续性。TiDB 目前采用批量分配 ID 的方式，如果在多台 TiDB 上同时插入数据，分配的自增 ID 会不连续。此外，不恰当地混用自定义值和缺省值可能会破坏数据唯一性。详情参见 [AUTO_INCREMENT](/auto-increment.md)。

### Performance schema

Performance schema 表在 TiDB 中返回结果为空。TiDB 使用 [Prometheus 和 Grafana](/monitor-a-tidb-cluster.md) 来监测性能指标。

针对 SQL 性能相关的问题，从 TiDB 4.0.0-rc.1 版本开始，TiDB 支持 `statements_summary`（和 MySQL 中的 `events_statements_summary_by_digest` 功能相似），用于监控和统计 SQL 语句。参见 [Statement Summary Table](/statement-summary-tables.md)。

### 查询计划

TiDB 的查询计划（`EXPLAIN`/`EXPLAIN FOR`）输出格式与 MySQL 差别较大，同时 `EXPLAIN FOR` 的输出内容与权限设置与 MySQL 不一致，参见[理解 TiDB 执行计划](/query-execution-plan.md)。

### 内建函数

TiDB 支持常用的 MySQL 内建函数，但是不是所有的函数都已经支持，具体请参考[语法文档](https://pingcap.github.io/sqlgram/#functioncallkeyword)。

### DDL

在 TiDB 中，运行的 DDL 操作不会影响对表的读取或写入。但是，目前 DDL 以下变更和 MySQL 的 DDL 变更有所区别：

| 语句类型 | 描述 | 错误信息示例 |
| ------ | ---- | ------ | ------ |
| Alter Table | 不支持在单个 alter 语句中指定多个 alter 选项 | Unsupported multi schema change |
| Table Option | 表选项除了 `AUTO_INCREMENT`、`CHARACTER SET`、`COLLATE`、`COMMENT` 以外，其他所有的选项都会被忽略 | N/A |
| Add Column | 不支持将新列设为主键、唯一索引或自增 | unsupported add column '%s' constraint PRIMARY/UNIQUE/AUTO_INCREMENT KEY |
| Change/Modify Column | 不支持列类型有损变更，例如 `BIGINT` -> `INT`，或者 `VARCHAR(255)` -> `VARCHAR(10)` | length %d is less than origin %d |
| Change/Modify Column | 不支持修改 `DECIMAL` 类型的精度 | can't change decimal column precision |
| Change/Modify Column | 不支持更改 `UNSIGNED` 属性 | can't change unsigned integer to signed or vice versa |
| Drop Column | 不支持删除主键列或索引列 | Unsupported drop integer primary key/column a with index covered |
| Add Index | 仅支持 `VISIBLE`/`INVISIBLE` 索引选项，其他索引选项将被忽略 | N/A |
| Drop Primary Key | 仅支持删除建表时启用了 `alter-primary-key` 配置项的表的主键 | Unsupported drop primary key when alter-primary-key is false' |
| Order By | 所有列排序选项将被忽略 | N/A |
| Lock | 所有锁选项将被忽略，TiDB 的 DDL 变更都不会锁表 | N/A |
| Algorithm | 运行过程与 MySQL 有所不同，MySQL 中的一些 `INPLACE` 操作实际上是 TiDB 中的 `INSTANT` 操作；`ALGORITHM=COPY` 语法在 TiDB 中不会生效，会返回警告信息。| N/A |
| Partition | 分区类型仅支持 Hash/Range；分区管理操作仅支持 Add/Drop/Truncate/Coalese；其他分区操作、分区类型和子分区语句会被忽略 | Warning: Unsupported partition type, treat as normal table |

### `ANALYZE TABLE`

- [`ANALYZE TABLE`](/statistics.md#手动收集) 语句在 TiDB 和 MySQL 中表现不同。在 MySQL/InnoDB 中，它是一个轻量级语句，执行过程较短；而在 TiDB 中，它会完全重构表的统计数据，语句执行过程较长。

### 视图

目前 TiDB 不支持对视图进行 `UPDATE`、`INSERT`、`DELETE` 等写入操作。

### 存储引擎

出于兼容性原因，TiDB 支持使用备用存储引擎创建表的语法。元数据命令将表描述为 InnoDB 存储引擎：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT) ENGINE=MyISAM;
```

```
Query OK, 0 rows affected (0.14 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE t1\G;
```

```
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

从架构上讲，TiDB 确实支持类似 MySQL 的存储引擎抽象，在启动 TiDB（通常是 `tikv`）时 [`--store`](/command-line-flags-for-tidb-configuration.md#store) 选项指定的引擎中创建用户表。

### SQL 模式

TiDB 支持 MySQL 5.7 中 **绝大多数的 SQL 模式**，以下几种模式除外：

- TiDB 不支持兼容模式（例如 `ORACLE` 和 `POSTGRESQL`）。MySQL 5.7 已弃用兼容模式，MySQL 8.0 已移除兼容模式。
- TiDB 中的 `ONLY_FULL_GROUP_BY` 与 MySQL 5.7 相比有细微的[语义差别](/functions-and-operators/aggregate-group-by-functions.md#与-mysql-的区别)，此问题日后将予以解决。
- `NO_DIR_IN_CREATE` 和 `NO_ENGINE_SUBSTITUTION` 这两种 SQL 模式用于解决兼容问题，但并不适用于 TiDB。

### 默认设置

+ 默认字符集与 MySQL 不同：
    + TiDB 中为 `utf8mb4`
    + MySQL 5.7 中为 `latin1`，MySQL 8.0 中修改为 `utf8mb4`
+ 默认排序规则不同：
    + TiDB 中，`utf8mb4` 的默认排序规则为 `utf8mb4_bin`
    + MySQL 5.7 中，`utf8mb4` 的默认排序规则为 `utf8mb4_general_ci`，MySQL 8.0 中修改为 `utf8mb4_0900_ai_ci`
    + 请使用 [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) 语句查看所有字符集的默认排序规则
+ `foreign_key_checks` 的默认值不同：
    + TiDB 中该值默认为 `OFF`，并且目前 TiDB 只支持设置该值为 `OFF`。
    + MySQL 5.7 中该值默认为 `ON`。
+ 默认 SQL mode 与 MySQL 5.7 相同，与 MySQL 8.0 不同：
    + TiDB 中为 `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
    + MySQL 中默认设置：
        + MySQL 5.7 的默认 SQL mode 与 TiDB 相同
        + MySQL 8.0 中相对 5.7 少了 `NO_AUTO_CREATE_USER`， 即 `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`
+ `lower_case_table_names` 的默认值不同：
    + TiDB 中该值默认为 2，并且目前 TiDB 只支持设置该值为 2
    + MySQL 中默认设置：
        + Linux 系统中该值为 0
        + Windows 系统中该值为 1
        + macOS 系统中该值为 2
+ `explicit_defaults_for_timestamp` 的默认值不同：
    + TiDB 中该值默认为 `ON`，并且目前 TiDB 只支持设置该值为 `ON`
    + MySQL 中默认设置：
        + MySQL 5.7：`OFF`
        + MySQL 8.0：`ON`

### 日期时间处理的区别

#### 时区

MySQL 默认使用本地时区，依赖于系统内置的当前的时区规则（例如什么时候开始夏令时等）进行计算；且在未[导入时区表数据](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation)的情况下不能通过时区名称来指定时区。

TiDB 不需要导入时区表数据也能使用所有时区名称，采用系统当前安装的所有时区规则进行计算（一般为 `tzdata` 包），且无法通过导入时区表数据的形式修改计算规则。

> **注意：**
>
> 能下推到 TiKV 的时间相关表达式会由 TiKV 进行计算。TiKV 总是采用 TiKV 内置时区规则计算，而不依赖于系统所安装的时区规则。若系统安装的时区规则与 TiKV 内置的时区规则版本不匹配，则在少数情况下可能发生能插入的时间数据无法再读出来的问题。例如，若系统上安装了 tzdata 2018a 时区规则，则在时区设置为 Asia/Shanghai 或时区设置为本地时区且本地时区为 Asia/Shanghai 的情况下，时间 `1988-04-17 02:00:00` 可以被正常插入 TiDB 3.0 RC.1，但该记录对于特定类型 SQL 则无法再读出来，原因是 TiKV 3.0 RC.1 依据的 tzdata 2018i 规则中该时间在 Asia/Shanghai 时区中不存在（夏令时时间后移一小时）。
>
> TiKV 各个版本内置的时区规则如下：
>
> - 3.0.0 RC.1 及以后：[tzdata 2018i](https://github.com/eggert/tz/tree/2018i)
> - 2.1.0 RC.1 及以后：[tzdata 2018e](https://github.com/eggert/tz/tree/2018e)

#### 零月和零日

与 MySQL 一样，TiDB 默认启用了 `NO_ZERO_DATE` 和 `NO_ZERO_IN_DATE` 模式，不建议将这两个模式设为禁用。尽管将这些模式设为禁用时 TiDB 仍可正常使用，但 TiKV coprocessor 会受到影响，具体表现为，执行特定类型的语句，将日期和时间处理函数下推到 TiKV 时可能会导致语句错误。

### 类型系统的区别

以下的列类型 MySQL 支持，但 TiDB 不支持：

+ FLOAT4/FLOAT8
+ FIXED (alias for DECIMAL)
+ SERIAL (alias for BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE)
+ SQL_TSI_* （包括 SQL_TSI_YEAR、SQL_TSI_MONTH、SQL_TSI_WEEK、SQL_TSI_DAY、SQL_TSI_HOUR、SQL_TSI_MINUTE 和 SQL_TSI_SECOND）
