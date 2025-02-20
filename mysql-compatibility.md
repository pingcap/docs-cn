---
title: 与 MySQL 兼容性对比
summary: 本文对 TiDB 和 MySQL 二者之间从语法和功能特性上做出详细的对比。
---

# 与 MySQL 兼容性对比

TiDB 高度兼容 MySQL 协议，以及 MySQL 5.7 和 MySQL 8.0 常用的功能及语法。MySQL 生态中的系统工具（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver 和[其他工具](/develop/dev-guide-third-party-support.md#gui)）、客户端等均适用于 TiDB。

但 TiDB 尚未支持一些 MySQL 功能，可能的原因如下：

- 有更好的解决方案，例如 JSON 取代 XML 函数。
- 目前对这些功能的需求度不高，例如存储过程和函数。
- 一些功能在分布式系统上的实现难度较大。

除此以外，TiDB 不支持 MySQL 复制协议，但提供了专用工具用于与 MySQL 复制数据：

- 从 MySQL 复制：[TiDB Data Migration (DM)](/dm/dm-overview.md) 是将 MySQL/MariaDB 数据迁移到 TiDB 的工具，可用于增量数据的复制。
- 向 MySQL 复制：[TiCDC](/ticdc/ticdc-overview.md) 是一款通过拉取 TiKV 变更日志实现的 TiDB 增量数据同步工具，可通过 [MySQL sink](/ticdc/ticdc-sink-to-mysql.md) 将 TiDB 增量数据复制到 MySQL。

> **注意：**
>
> 本页内容仅涉及 MySQL 与 TiDB 的总体差异。关于[安全特性](/security-compatibility-with-mysql.md)、[悲观事务模式](/pessimistic-transaction.md#和-mysql-innodb-的差异)相关的兼容信息，请查看各自具体页面。

## 不支持的功能特性

* 存储过程与函数
* 触发器
* 事件
* 自定义函数
* 全文语法与索引 [#1793](https://github.com/pingcap/tidb/issues/1793)
* 空间类型的函数（即 `GIS`/`GEOMETRY`）、数据类型和索引 [#6347](https://github.com/pingcap/tidb/issues/6347)
* 非 `ascii`、`latin1`、`binary`、`utf8`、`utf8mb4`、`gbk` 的字符集
* MySQL 追踪优化器
* XML 函数
* X-Protocol [#1109](https://github.com/pingcap/tidb/issues/1109)
* 列级权限 [#9766](https://github.com/pingcap/tidb/issues/9766)
* `XA` 语法（TiDB 内部使用两阶段提交，但并没有通过 SQL 接口公开）
* `CREATE TABLE tblName AS SELECT stmt` 语法 [#4754](https://github.com/pingcap/tidb/issues/4754)
* `CHECK TABLE` 语法 [#4673](https://github.com/pingcap/tidb/issues/4673)
* `CHECKSUM TABLE` 语法 [#1895](https://github.com/pingcap/tidb/issues/1895)
* `REPAIR TABLE` 语法
* `OPTIMIZE TABLE` 语法
* `HANDLER` 语句
* `CREATE TABLESPACE` 语句
* "Session Tracker: 将 GTID 上下文信息添加到 OK 包中"
* 降序索引 [#2519](https://github.com/pingcap/tidb/issues/2519)
* `SKIP LOCKED` 语法 [#18207](https://github.com/pingcap/tidb/issues/18207)
* 横向派生表 [#40328](https://github.com/pingcap/tidb/issues/40328)
* JOIN 的 ON 子句的子查询 [#11414](https://github.com/pingcap/tidb/issues/11414)

## 与 MySQL 有差异的特性详细说明

### 自增 ID

- TiDB 的自增列既能保证唯一，也能保证在单个 TiDB server 中自增，使用 [`AUTO_INCREMENT` MySQL 兼容模式](/auto-increment.md#mysql-兼容模式)能保证多个 TiDB server 中自增 ID，但不保证自动分配的值的连续性。建议避免将缺省值和自定义值混用，以免出现 `Duplicated Error` 的错误。

- TiDB 可通过 `tidb_allow_remove_auto_inc` 系统变量开启或者关闭允许移除列的 `AUTO_INCREMENT` 属性。删除列属性的语法是：`ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE`。

- TiDB 不支持添加列的 `AUTO_INCREMENT` 属性，移除该属性后不可恢复。

- 对于 v6.6.0 及更早的 TiDB 版本，TiDB 的自增列行为与 MySQL InnoDB 保持一致，要求自增列必须为主键或者索引前缀。从 v7.0.0 开始，TiDB 移除了该限制，允许用户更灵活地定义表的主键。关于此更改的详细信息，请参阅 [#40580](https://github.com/pingcap/tidb/issues/40580)

自增 ID 详情可参阅 [AUTO_INCREMENT](/auto-increment.md)。

> **注意：**
>
> 若创建表时没有指定主键时，TiDB 会使用 `_tidb_rowid` 来标识行，该数值的分配会和自增列（如果存在的话）共用一个分配器。如果指定了自增列为主键，则 TiDB 会用该列来标识行。因此会有以下的示例情况：

```sql
mysql> CREATE TABLE t(id INT UNIQUE KEY AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> SELECT _tidb_rowid, id FROM t;
+-------------+------+
| _tidb_rowid | id   |
+-------------+------+
|           2 |    1 |
|           4 |    3 |
|           6 |    5 |
+-------------+------+
3 rows in set (0.01 sec)
```

可以看到，由于共用分配器，id 每次自增步长是 2。在 [MySQL 兼容模式](/auto-increment.md#mysql-兼容模式)中改掉了该行为，没有共用分配器，因此不会跳号。

> **注意：**
>
> 使用 `AUTO_INCREMENT` 可能会给生产环境带热点问题，因此推荐使用 [`AUTO_RANDOM`](/auto-random.md) 代替。详情请参考 [TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md#tidb-热点问题处理)。

### Performance schema

TiDB 主要使用 Prometheus 和 Grafana 来存储及查询相关的性能监控指标。因此，TiDB 的大多数 [performance schema 表](/performance-schema/performance-schema.md)返回空结果。

### 查询计划

TiDB 中，执行计划（`EXPLAIN` 和 `EXPLAIN FOR`）在输出格式、内容、权限设置方面与 MySQL 有较大差别。

MySQL 系统变量 `optimizer_switch` 在 TiDB 中是只读的，对查询计划没有影响。你还可以在 [optimizer hints](/optimizer-hints.md) 中使用与 MySQL 类似的语法，但可用的 hint 和实现原理可能会有所不同。

详情参见[理解 TiDB 执行计划](/explain-overview.md)。

### 内建函数

支持常用的 MySQL 内建函数，有部分函数并未支持。可通过执行 [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md) 语句查看可用的内建函数。

### DDL 的限制

TiDB 中，所有支持的 DDL 变更操作都是在线执行的。与 MySQL 相比，TiDB 中的 DDL 存在以下限制：

* 使用 `ALTER TABLE` 语句修改一个表的多个模式对象（如列、索引）时，不允许在多个更改中指定同一个模式对象。例如，`ALTER TABLE t1 MODIFY COLUMN c1 INT, DROP COLUMN c1` 在两个更改中都指定了 `c1` 列，执行该语句会输出 `Unsupported operate same column/index` 的错误。
* 不支持使用单个 `ALTER TABLE` 语句同时修改多个 TiDB 特有的模式对象，包括 `TIFLASH REPLICA`，`SHARD_ROW_ID_BITS`，`AUTO_ID_CACHE` 等。
* `ALTER TABLE` 不支持少部分类型的变更。比如，TiDB 不支持从 `DECIMAL` 到 `DATE` 的变更。当遇到不支持的类型变更时，TiDB 将会报 `Unsupported modify column: type %d not match origin %d` 的错误。更多细节，请参考 [`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)。
* TiDB 中，`ALGORITHM={INSTANT,INPLACE,COPY}` 语法只作为一种指定，并不更改 `ALTER` 算法，详情参阅 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)。
* 不支持添加或删除 `CLUSTERED` 类型的主键。要了解关于 `CLUSTERED` 主键的详细信息，请参考[聚簇索引](/clustered-indexes.md)。
* 不支持指定不同类型的索引 (`HASH|BTREE|RTREE|FULLTEXT`)。若指定了不同类型的索引，TiDB 会解析并忽略这些索引。
* 分区表支持 `HASH`、`RANGE`、`LIST` 和 `KEY` 分区类型。对于不支持的分区类型，TiDB 会报 `Warning: Unsupported partition type %s, treat as normal table` 错误，其中 `%s` 为不支持的具体分区类型。
* Range、Range COLUMNS、List、List COLUMNS 分区表支持 `ADD`、`DROP`、`TRUNCATE`、`REORGANIZE` 操作，其他分区操作会被忽略。
* Hash 和 Key 分区表支持 `ADD`、`COALESCE`、`TRUNCATE` 操作，其他分区操作会被忽略。
* TiDB 不支持以下分区表语法：

    + `SUBPARTITION`
    + `{CHECK|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD} PARTITION`

  更多详情，请参考[分区表文档](/partitioned-table.md)。

### `ANALYZE TABLE`

TiDB 中的[信息统计](/statistics.md#手动收集)与 MySQL 中的有所不同：TiDB 中的信息统计会完全重构表的统计数据，语句消耗较多资源，执行过程较长，但在 MySQL/InnoDB 中，它是一个轻量级语句，执行过程较短。

更多信息统计的差异请参阅 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)。

### `SELECT` 的限制

TiDB 的 `SELECT` 语法有以下限制：

- 不支持 `SELECT ... INTO @变量` 语法。
- TiDB 中的 `SELECT .. GROUP BY expr` 的返回结果与 MySQL 5.7 并不一致。MySQL 5.7 的结果等价于 `GROUP BY expr ORDER BY expr`。

详情参见 [`SELECT`](/sql-statements/sql-statement-select.md)。

### `UPDATE` 语句

详情参见 [`UPDATE`](/sql-statements/sql-statement-update.md)。

### 视图

TiDB 中的视图不可更新，不支持 `UPDATE`、`INSERT`、`DELETE` 等写入操作。

### 临时表

详见 [TiDB 本地临时表与 MySQL 临时表的兼容性](/temporary-tables.md#与-mysql-临时表的兼容性)。

### 字符集和排序规则

* 关于 TiDB 对字符集和排序规则的支持情况，详见[字符集和排序规则](/character-set-and-collation.md)。

* 关于 GBK 字符集与 MySQL 的兼容情况，详见 [GBK 兼容情况](/character-set-gbk.md#与-mysql-的兼容性)。

* TiDB 继承表中使用的字符集作为国家字符集。

### 存储引擎

- 仅在语法上兼容创建表时指定存储引擎，实际上 TiDB 会将元信息统一描述为 InnoDB 存储引擎。TiDB 支持类似 MySQL 的存储引擎抽象，但需要在系统启动时通过 [`--store`](/command-line-flags-for-tidb-configuration.md#--store) 配置项来指定存储引擎。

### SQL 模式

TiDB 支持大部分 [SQL 模式](/sql-mode.md)。不支持的 SQL 模式如下：

- 不支持兼容模式，例如：`Oracle` 和 `PostgreSQL`（TiDB 解析但会忽略这两个兼容模式），MySQL 5.7 已弃用兼容模式，MySQL 8.0 已移除兼容模式。
- TiDB 的 `ONLY_FULL_GROUP_BY` 模式与 MySQL 5.7 相比有细微的[语义差别](/functions-and-operators/aggregate-group-by-functions.md#与-mysql-的区别)。
- `NO_DIR_IN_CREATE` 和 `NO_ENGINE_SUBSTITUTION` 仅用于解决与 MySQL 的兼容性问题，并不适用于 TiDB。

### 默认设置

TiDB 的默认设置与 MySQL 5.7 和 MySQL 8.0 有以下区别：

- 字符集：
    + TiDB 默认：`utf8mb4`。
    + MySQL 5.7 默认：`latin1`。
    + MySQL 8.0 默认：`utf8mb4`。

- 排序规则：
    + TiDB 中 `utf8mb4` 字符集默认：`utf8mb4_bin`。
    + MySQL 5.7 中 `utf8mb4` 字符集默认：`utf8mb4_general_ci`。
    + MySQL 8.0 中 `utf8mb4` 字符集默认：`utf8mb4_0900_ai_ci`。

- SQL mode：
    + TiDB 默认：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`。
    + MySQL 5.7 默认与 TiDB 相同。
    + MySQL 8.0 默认 `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`。

- `lower_case_table_names`：
    + TiDB 默认：`2`，且仅支持设置该值为 `2`。
    + MySQL 默认如下：
        - Linux 系统中该值为 `0`，表示表名和数据库名按照在 `CREATE TABLE` 或 `CREATE DATABASE` 语句中指定的字母大小写存储在磁盘上，且名称比较时区分大小写。
        - Windows 系统中该值为 `1`，表示表名按照小写字母存储在磁盘上，名称比较时不区分大小写。MySQL 在存储和查询时将所有表名转换为小写。该行为也适用于数据库名称和表的别名。
        - macOS 系统中该值为 `2`，表示表名和数据库名按照在 `CREATE TABLE` 或 `CREATE DATABASE` 语句中指定的字母大小写存储在磁盘上，但 MySQL 在查询时将它们转换为小写。名称比较时不区分大小写。

- `explicit_defaults_for_timestamp`：
    + TiDB 默认：`ON`，且仅支持设置该值为 `ON`。
    + MySQL 5.7 默认：`OFF`。
    + MySQL 8.0 默认：`ON`。

### 日期时间处理的区别

TiDB 与 MySQL 在日期时间处理上有如下差异：

- TiDB 采用系统当前安装的所有时区规则进行计算（一般为 `tzdata` 包），不需要导入时区表数据就能使用所有时区名称，导入时区表数据不会修改计算规则。

- MySQL 默认使用本地时区，依赖于系统内置的当前的时区规则（例如什么时候开始夏令时等）进行计算；且在未[导入时区表数据](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation)的情况下不能通过时区名称来指定时区。

### 类型系统

MySQL 支持 `SQL_TSI_*`（包括 `SQL_TSI_MONTH`、`SQL_TSI_WEEK`、`SQL_TSI_DAY`、`SQL_TSI_HOUR`、`SQL_TSI_MINUTE` 和 `SQL_TSI_SECOND`，但不包括 `SQL_TSI_YEAR`），但 TiDB 不支持。

### 正则函数

关于 TiDB 中正则函数 `REGEXP_INSTR()`、`REGEXP_LIKE()`、`REGEXP_REPLACE()`、`REGEXP_SUBSTR()` 与 MySQL 的兼容情况，请参考[正则函数与 MySQL 的兼容性](/functions-and-operators/string-functions.md#正则函数与-mysql-的兼容性)。

### MySQL 弃用功能导致的不兼容问题

TiDB 不支持 MySQL 中标记为弃用的功能，包括：

* 指定浮点类型的精度。MySQL 8.0 [弃用](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html)了此功能，建议改用 `DECIMAL` 类型。
* `ZEROFILL` 属性。MySQL 8.0 [弃用](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html)了此功能，建议在业务应用中填充数字值。

### `CREATE RESOURCE GROUP`，`DROP RESOURCE GROUP` 和 `ALTER RESOURCE GROUP`

TiDB 资源组创建与修改语句的语法与 MySQL 官方不同，详情参见：

- [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)
- [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)
- [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)
