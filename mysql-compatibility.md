---
title: 与 MySQL 兼容性对比
summary: 本文对 TiDB 和 MySQL 二者之间从语法和功能特性上做出详细的对比。
aliases: ['/docs-cn/stable/mysql-compatibility/','/docs-cn/v4.0/mysql-compatibility/','/docs-cn/stable/reference/mysql-compatibility/']
---

# 与 MySQL 兼容性对比概览

- TiDB 100% 兼容 MySQL 5.7 协议、MySQL 5.7 常用的功能及语法。MySQL 5.7 生态中的系统工具（PHPMyAdmin、Navicat、MySQL Workbench、mysqldump、Mydumper/Myloader）、客户端等均适用于 TiDB。

- 但 TiDB 尚未支持一些 MySQL 功能，可能的原因如下：
    - 有更好的解决方案，例如 JSON 取代 XML 函数。
    - 目前对这些功能的需求度不高，例如存储流程和函数。
    - 一些功能在分布式系统上的实现难度较大。

> **注意：**
>
> 本页内容仅涉及 MySQL 与 TiDB 的总体差异。关于[安全特性](/security-compatibility-with-mysql.md)、[悲观事务模型](/pessimistic-transaction.md#和-mysql-innodb-的差异) 相关的兼容信息请查看各自具体页面。

## 不支持的功能特性

* 存储过程与函数
* 触发器
* 事件
* 自定义函数
* 外键约束 [#18209](https://github.com/pingcap/tidb/issues/18209)
* 临时表
* 全文/空间函数与索引 [#1793](https://github.com/pingcap/tidb/issues/1793)
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
* `GET_LOCK` 和 `RELEASE_LOCK` 函数 [#14994](https://github.com/pingcap/tidb/issues/14994)

## 与 MySQL 有差异的特性详细说明

### 自增 ID

- TiDB 的自增列仅保证唯一，也能保证在单个 TiDB server 中自增，但不保证多个 TiDB server 中自增，不保证自动分配的值的连续性，建议不要将缺省值和自定义值混用，若混用可能会收 `Duplicated Error` 的错误信息。

- TiDB 可通过 `tidb_allow_remove_auto_inc` 系统变量开启或者关闭允许移除列的 `AUTO_INCREMENT` 属性。删除列属性的语法是：`alter table modify` 或 `alter table change`。

- TiDB 不支持添加列的 `AUTO_INCREMENT` 属性，移除该属性后不可恢复。

自增 ID 详情可参阅 [AUTO_INCREMENT](/auto-increment.md)。

> **注意：**
>
> * `tidb_allow_remove_auto_inc` 要求版本号 >= v2.1.18 或者 >= v3.0.4。
> * 表的 `AUTO_ID_CACHE` 属性要求版本号 >= v3.0.14 或者 >= v3.1.2 或者 >= v4.0.0-rc.2。
> * 若创建表时没有指定主键时，TiDB 会使用 `_tidb_rowid` 来标识行，该数值的分配会和自增列（如果存在的话）共用一个分配器。如果指定了自增列为主键，则 TiDB 会用该列来标识行。因此会有以下的示例情况：

```sql
mysql> create table t(id int unique key AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> insert into t values(),(),();
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> select _tidb_rowid, id from t;
+-------------+------+
| _tidb_rowid | id   |
+-------------+------+
|           4 |    1 |
|           5 |    2 |
|           6 |    3 |
+-------------+------+
3 rows in set (0.01 sec)
```

### Performance schema

TiDB 主要使用 Prometheus 和 Grafana 来存储及查询相关的性能监控指标，所以 Performance schema 部分表是空表。

### 查询计划

`EXPLAIN`/`EXPLAIN FOR` 输出格式、内容、权限设置与 MySQL 有比较大的差别，参见[理解 TiDB 执行计划](/query-execution-plan.md)。

### 内建函数

支持常用的 MySQL 内建函数，有部分函数并未支持。可通过执行 `SHOW BUILTINS` 语句查看可用的内建函数。参考 [SQL 语法文档](https://pingcap.github.io/sqlgram/#functioncallkeyword)。

### DDL 的限制

TiDB 中，所有支持的 DDL 变更操作都是在线执行的。可能与 MySQL 不同的是，在 TiDB 中，`ALGORITHM=INSTANT` 和 `ALGORITHM=INPLACE` 这两种 MySQL DDL 算法可用于指定使用哪种算法来修改表。

与 MySQL 相比，TiDB 中的 DDL 存在以下限制：

* 不能在单条 `ALTER TABLE` 语句中完成多个操作。例如，不能在单个语句中添加多个列或索引，否则，可能会输出 `Unsupported multi schema change` 的错误。
* 不支持不同类型的索引 (`HASH|BTREE|RTREE|FULLTEXT`)。若指定了不同类型的索引，TiDB 会解析并忽略这些索引。
* 不支持添加/删除主键，除非开启了 [`alter-primary-key`](/tidb-configuration-file.md#alter-primary-key) 配置项。
* 不支持将字段类型修改为其超集，例如不支持从 `INTEGER` 修改为 `VARCHAR`，或者从 `TIMESTAMP` 修改为 `DATETIME`，否则可能输出的错误信息 `Unsupported modify column: type %d not match origin %d`。
* 更改/修改数据类型时，尚未支持“有损更改”，例如不支持从 BIGINT 更改为 INT。
* 更改/修改十进制列时，不支持更改预置。
* 更改/修改整数列时，不允许更改 `UNSIGNED` 属性。
* 分区表支持 Hash、Range 和 `Add`/`Drop`/`Truncate`/`Coalesce`。其他分区操作将被忽略，可能会报 `Warning: Unsupported partition type, treat as normal table` 错误。不支持以下分区表语法：
    + `PARTITION BY LIST`
    + `PARTITION BY KEY`
    + `SUBPARTITION`
    + `{CHECK|EXCHANGE|TRUNCATE|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD|REORGANIZE} PARTITION`

### `ANALYZE TABLE`

TiDB 中的[信息统计](/statistics.md#手动收集) 与 MySQL 中的有所不同：TiDB 中的信息统计会完全重构表的统计数据，语句执行过程较长，但在 MySQL/InnoDB 中，它是一个轻量级语句，执行过程较短。

更多信息统计的差异请参阅 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)。

### `SELECT` 的限制

- 不支持 `SELECT ... INTO @变量` 语法。
- 不支持 `SELECT ... GROUP BY ... WITH ROLLUP` 语法。

### 视图

TiDB 中的视图不可更新，不支持 `UPDATE`、`INSERT`、`DELETE` 等写入操作。

### 存储引擎

- 仅在语法上兼容创建表时指定存储引擎，实际上 TiDB 会将元信息统一描述为 InnoDB 存储引擎。TiDB 支持类似 MySQL 的存储引擎抽象，但需要在系统启动时通过[`--store`](/command-line-flags-for-tidb-configuration.md#--store) 配置项来指定存储引擎。

### SQL 模式

TiDB 支持大部分 [SQL 模式](/sql-mode.md)。不支持的 SQL 模式如下：

- 不支持兼容模式，例如：`ORACLE` 和 `POSTGRESQL`（TiDB 解析但会忽略这两个兼容模式），MySQL 5.7 已弃用兼容模式，MySQL 8.0 已移除兼容模式。
- TiDB 的 `ONLY_FULL_GROUP_BY` 模式与 MySQL 5.7 相比有细微的[语义差别](/functions-and-operators/aggregate-group-by-functions.md#与-mysql-的区别)。
- `NO_DIR_IN_CREATE` 和 `NO_ENGINE_SUBSTITUTION` 仅用于解决与 MySQL 的兼容性问题，并不适用于 TiDB。

### 默认设置

- 字符集：
    + TiDB 默认：`utf8mb4`。
    + MySQL 5.7 默认：`latin1`。
    + MySQL 8.0 默认：`utf8mb4`。

- 排序规则：
    + TiDB 中 `utf8mb4` 字符集默认：`utf8mb4_bin`。
    + MySQL 5.7 中 `utf8mb4` 字符集默认：`utf8mb4_general_ci`。
    + MySQL 8.0 中 `utf8mb4` 字符集默认：`utf8mb4_0900_ai_ci`。

- `foreign_key_checks`：
    + TiDB 默认：`OFF`，且仅支持设置该值为 `OFF`。
    + MySQL 5.7 默认：`ON`。

- SQL mode：
    + TiDB 默认：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`。
    + MySQL 5.7 默认 与 TiDB 相同。
    + MySQL 8.0 默认 `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`。

- `lower_case_table_names`：
    + TiDB 默认：`2`，且仅支持设置该值为 `2`。
    + MySQL 默认如下：
        - Linux 系统中该值为 `0`
        - Windows 系统中该值为 `1`
        - macOS 系统中该值为 `2`

- `explicit_defaults_for_timestamp`：
    + TiDB 默认：`ON`，且仅支持设置该值为 `ON`。
    + MySQL 5.7 默认：`OFF`。
    + MySQL 8.0 默认：`ON`。

### 日期时间处理的区别

#### 时区

- TiDB 采用系统当前安装的所有时区规则进行计算（一般为 `tzdata` 包），不需要导入时区表数据就能使用所有时区名称，无法通过导入时区表数据的形式修改计算规则。

- MySQL 默认使用本地时区，依赖于系统内置的当前的时区规则（例如什么时候开始夏令时等）进行计算；且在未[导入时区表数据](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation)的情况下不能通过时区名称来指定时区。

#### 零月和零日

- 与 MySQL 一样，TiDB 默认启用了 `NO_ZERO_DATE` 和 `NO_ZERO_IN_DATE` 模式，但是 TiDB 与 MySQL 在处理这两个 SQL 模式有以下不同：
    - TiDB 在非严格模式下启用以上两个 SQL 模式，插入零月/零日/零日期不会给出警告，MySQL 则会给出对应的警告。
    - TiDB 在严格模式下，启用了 `NO_ZERO_DATE`，仍然能够插入零日期；如果启用了 `NO_ZERO_IN_DATE` 则无法插入零月/零日日期。MySQL 在严格模式下则都无法插入两种类型的日期。

### 类型系统

+ 不支持 FLOAT4/FLOAT8。

+ 不支持 FIXED (alias for DECIMAL)。

+ 不支持 SERIAL (alias for BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE)。

+ 不支持 `SQL_TSI_*`（包括 `SQL_TSI_YEAR`、`SQL_TSI_MONTH`、`SQL_TSI_WEEK`、`SQL_TSI_DAY`、`SQL_TSI_HOUR`、`SQL_TSI_MINUTE` 和 `SQL_TSI_SECOND`）。
