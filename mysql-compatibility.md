---
title: 与 MySQL 兼容性对比
summary: 本文对 TiDB 和 MySQL 二者之间从语法和功能特性上做出详细的对比。
aliases: ['/docs-cn/dev/mysql-compatibility/','/docs-cn/dev/reference/mysql-compatibility/']
---

# 与 MySQL 兼容性对比

- TiDB 100% 兼容 MySQL 5.7 协议、MySQL 5.7 常用的功能及语法。MySQL 5.7 生态中的系统工具 (PHPMyAdmin、Navicat、MySQL Workbench、mysqldump、Mydumper/Myloader)、客户端等均适用于 TiDB。

- 但 TiDB 尚未支持一些 MySQL 功能，可能的原因如下：
    - 有更好的解决方案，例如 JSON 取代 XML 函数。
    - 目前对这些功能的需求度不高，例如存储流程和函数。
    - 一些功能在分布式系统上的实现难度较大。

- 除此以外，TiDB 不支持 MySQL 复制协议，但提供了专用工具用于与 MySQL 复制数据
    - 从 MySQL 复制：[TiDB Data Migration (DM)](https://docs.pingcap.com/zh/tidb-data-migration/stable/overview) 是将 MySQL/MariaDB 数据迁移到 TiDB 的工具，可用于增量数据的复制。
    - 向 MySQL 复制：[TiCDC](/ticdc/ticdc-overview.md) 是一款通过拉取 TiKV 变更日志实现的 TiDB 增量数据同步工具，可通过 [MySQL sink](/ticdc/ticdc-overview.md#sink-支持) 将 TiDB 增量数据复制到 MySQL。

> **注意：**
>
> 本页内容仅涉及 MySQL 与 TiDB 的总体差异。关于[安全特性](/security-compatibility-with-mysql.md)、[悲观事务模型](/pessimistic-transaction.md#和-mysql-innodb-的差异)相关的兼容信息请查看各自具体页面。

## 不支持的功能特性

* 存储过程与函数
* 触发器
* 事件
* 自定义函数
* 外键约束 [#18209](https://github.com/pingcap/tidb/issues/18209)
* 临时表 [#1248](https://github.com/pingcap/tidb/issues/1248)
* 全文/空间函数与索引 [#1793](https://github.com/pingcap/tidb/issues/1793)
* 非 `ascii`/`latin1`/`binary`/`utf8`/`utf8mb4` 的字符集
* SYS schema
* MySQL 追踪优化器
* XML 函数
* X-Protocol [#1109](https://github.com/pingcap/tidb/issues/1109)
* Savepoints [#6840](https://github.com/pingcap/tidb/issues/6840)
* 列级权限 [#9766](https://github.com/pingcap/tidb/issues/9766)
* `XA` 语法（TiDB 内部使用两阶段提交，但并没有通过 SQL 接口公开）
* `CREATE TABLE tblName AS SELECT stmt` 语法 [#4754](https://github.com/pingcap/tidb/issues/4754)
* `CHECK TABLE` 语法 [#4673](https://github.com/pingcap/tidb/issues/4673)
* `CHECKSUM TABLE` 语法 [#1895](https://github.com/pingcap/tidb/issues/1895)
* `GET_LOCK` 和 `RELEASE_LOCK` 函数 [#14994](https://github.com/pingcap/tidb/issues/14994)
* [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) 和 `REPLACE` 关键字 [#24515](https://github.com/pingcap/tidb/issues/24515)

## 与 MySQL 有差异的特性详细说明

### 自增 ID

- TiDB 的自增列仅保证唯一，也能保证在单个 TiDB server 中自增，但不保证多个 TiDB server 中自增，不保证自动分配的值的连续性，建议不要将缺省值和自定义值混用，若混用可能会收到 `Duplicated Error` 的错误信息。

- TiDB 可通过 `tidb_allow_remove_auto_inc` 系统变量开启或者关闭允许移除列的 `AUTO_INCREMENT` 属性。删除列属性的语法是：`ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE`。

- TiDB 不支持添加列的 `AUTO_INCREMENT` 属性，移除该属性后不可恢复。

自增 ID 详情可参阅 [AUTO_INCREMENT](/auto-increment.md)。

> **注意：**
>
> 若创建表时没有指定主键时，TiDB 会使用 `_tidb_rowid` 来标识行，该数值的分配会和自增列（如果存在的话）共用一个分配器。如果指定了自增列为主键，则 TiDB 会用该列来标识行。因此会有以下的示例情况：

```sql
mysql> CREATE TABLE t(id INT UNIQUE KEY AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> INSERT INTO t VALUES(),(),();
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT _tidb_rowid, id FROM t;
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

`EXPLAIN`/`EXPLAIN FOR` 输出格式、内容、权限设置与 MySQL 有比较大的差别，参见[理解 TiDB 执行计划](/explain-overview.md)。

### 内建函数

支持常用的 MySQL 内建函数，有部分函数并未支持。可通过执行 `SHOW BUILTINS` 语句查看可用的内建函数。参考 [SQL 语法文档](https://pingcap.github.io/sqlgram/#functioncallkeyword)。

### DDL 的限制

TiDB 中，所有支持的 DDL 变更操作都是在线执行的。与 MySQL 相比，TiDB 中的 DDL 存在以下限制：

* 不能在单条 `ALTER TABLE` 语句中完成多个操作。例如，不能在单个语句中添加多个列或索引，否则，可能会输出 `Unsupported multi schema change` 的错误。
* `ALTER TABLE` 不支持少部分类型的变更。比如，TiDB 不支持从 `DECIMAL` 到 `DATE` 的变更。当遇到不支持的类型变更时，TiDB 将会报 `Unsupported modify column: type %d not match origin %d` 的错误。更多细节，请参考[`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)。
* TiDB 中，`ALGORITHM={INSTANT,INPLACE,COPY}` 语法只作为一种指定，并不更改 `ALTER` 算法，详情参阅 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)。
* 不支持添加或删除 `CLUSTERED` 类型的主键。要了解关于 `CLUSTERED` 主键的详细信息，请参考[聚簇索引](/clustered-indexes.md)。
* 不支持指定不同类型的索引 (`HASH|BTREE|RTREE|FULLTEXT`)。若指定了不同类型的索引，TiDB 会解析并忽略这些索引。
* 分区表支持 Hash、Range 和 `Add`/`Drop`/`Truncate`/`Coalesce`。其他分区操作将被忽略，可能会报 `Warning: Unsupported partition type, treat as normal table` 错误。不支持以下分区表语法：
    + `PARTITION BY LIST`
    + `PARTITION BY KEY`
    + `SUBPARTITION`
    + `{CHECK|EXCHANGE|TRUNCATE|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD|REORGANIZE} PARTITION`

### `ANALYZE TABLE`

TiDB 中的[信息统计](/statistics.md#手动收集)与 MySQL 中的有所不同：TiDB 中的信息统计会完全重构表的统计数据，语句执行过程较长，但在 MySQL/InnoDB 中，它是一个轻量级语句，执行过程较短。

更多信息统计的差异请参阅 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)。

### `SELECT` 的限制

- 不支持 `SELECT ... INTO @变量` 语法。
- 不支持 `SELECT ... GROUP BY ... WITH ROLLUP` 语法。
- TiDB 中的 `SELECT .. GROUP BY expr` 的返回结果与 MySQL 5.7 并不一致。MySQL 5.7 的结果等价于 `GROUP BY expr ORDER BY expr`。而 TiDB 中该语法所返回的结果并不承诺任何顺序，与 MySQL 8.0 的行为一致。

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
    + MySQL 5.7 默认与 TiDB 相同。
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

### 类型系统

+ 不支持 FLOAT4/FLOAT8。

+ 不支持 `SQL_TSI_*`（包括 `SQL_TSI_MONTH`、`SQL_TSI_WEEK`、`SQL_TSI_DAY`、`SQL_TSI_HOUR`、`SQL_TSI_MINUTE` 和 `SQL_TSI_SECOND`，但不包括 `SQL_TSI_YEAR`）。

### MySQL 弃用功能导致的不兼容问题

TiDB 不支持 MySQL 中标记为弃用的功能，包括：

* 指定浮点类型的精度。MySQL 8.0 [弃用](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html)了此功能，建议改用 `DECIMAL` 类型。
* `ZEROFILL` 属性。 MySQL 8.0 [弃用](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html)了此功能，建议在业务应用中填充数字值。
