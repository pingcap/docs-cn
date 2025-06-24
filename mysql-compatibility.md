---
title: MySQL 兼容性
summary: 了解 TiDB 与 MySQL 的兼容性，以及不支持和有差异的功能。
---

# MySQL 兼容性

<CustomContent platform="tidb">

TiDB 高度兼容 MySQL 协议以及 MySQL 5.7 和 MySQL 8.0 的常用功能和语法。MySQL 生态系统工具（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver 和[更多](/develop/dev-guide-third-party-support.md#gui)）以及 MySQL 客户端都可以用于 TiDB。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB 高度兼容 MySQL 协议以及 MySQL 5.7 和 MySQL 8.0 的常用功能和语法。MySQL 生态系统工具（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver 和[更多](https://docs.pingcap.com/tidb/v7.2/dev-guide-third-party-support#gui)）以及 MySQL 客户端都可以用于 TiDB。

</CustomContent>

然而，TiDB 不支持 MySQL 的某些功能。这可能是因为现在有更好的解决方案（比如使用 JSON 而不是 XML 函数），或者当前需求相对于所需工作量较小（比如存储过程和函数）。此外，某些功能在分布式系统中可能难以实现。

<CustomContent platform="tidb">

需要注意的是，TiDB 不支持 MySQL 复制协议。相反，提供了特定工具来与 MySQL 进行数据复制：

- 从 MySQL 复制数据：[TiDB Data Migration (DM)](/dm/dm-overview.md) 是一个支持从 MySQL 或 MariaDB 到 TiDB 进行全量数据迁移和增量数据复制的工具。
- 复制数据到 MySQL：[TiCDC](/ticdc/ticdc-overview.md) 是一个通过拉取 TiKV 变更日志来复制 TiDB 增量数据的工具。TiCDC 使用 [MySQL sink](/ticdc/ticdc-overview.md#replication-consistency) 将 TiDB 的增量数据复制到 MySQL。

</CustomContent>

<CustomContent platform="tidb">

> **注意：**
>
> 本页描述了 MySQL 和 TiDB 之间的一般差异。有关安全性和悲观事务模式方面与 MySQL 的兼容性的更多信息，请参阅专门的[安全性](/security-compatibility-with-mysql.md)和[悲观事务模式](/pessimistic-transaction.md#difference-with-mysql-innodb)页面。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 关于 MySQL 和 TiDB 之间的事务差异信息，请参阅[悲观事务模式](/pessimistic-transaction.md#difference-with-mysql-innodb)。

</CustomContent>

你可以在 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=mysql_compatibility) 上试用 TiDB 功能。

## 不支持的功能

+ 存储过程和函数
+ 触发器
+ 事件
+ 用户定义函数
+ `FULLTEXT` 语法和索引 [#1793](https://github.com/pingcap/tidb/issues/1793)
+ `SPATIAL`（也称为 `GIS`/`GEOMETRY`）函数、数据类型和索引 [#6347](https://github.com/pingcap/tidb/issues/6347)
+ 除 `ascii`、`latin1`、`binary`、`utf8`、`utf8mb4` 和 `gbk` 之外的字符集
+ 优化器跟踪
+ XML 函数
+ X-Protocol [#1109](https://github.com/pingcap/tidb/issues/1109)
+ 列级权限 [#9766](https://github.com/pingcap/tidb/issues/9766)
+ `XA` 语法（TiDB 内部使用两阶段提交，但这不通过 SQL 接口暴露）
+ `CREATE TABLE tblName AS SELECT stmt` 语法 [#4754](https://github.com/pingcap/tidb/issues/4754)
+ `CHECK TABLE` 语法 [#4673](https://github.com/pingcap/tidb/issues/4673)
+ `CHECKSUM TABLE` 语法 [#1895](https://github.com/pingcap/tidb/issues/1895)
+ `REPAIR TABLE` 语法
+ `OPTIMIZE TABLE` 语法
+ `HANDLER` 语句
+ `CREATE TABLESPACE` 语句
+ "会话跟踪器：在 OK 数据包中添加 GTIDs 上下文"
+ 降序索引 [#2519](https://github.com/pingcap/tidb/issues/2519)
+ `SKIP LOCKED` 语法 [#18207](https://github.com/pingcap/tidb/issues/18207)
+ 横向派生表 [#40328](https://github.com/pingcap/tidb/issues/40328)
+ JOIN ON 子查询 [#11414](https://github.com/pingcap/tidb/issues/11414)

## 与 MySQL 的差异

### 自增 ID

+ 在 TiDB 中，自增列值（ID）在单个 TiDB 服务器内是全局唯一且递增的。要使 ID 在多个 TiDB 服务器之间递增，你可以使用 [`AUTO_INCREMENT` MySQL 兼容模式](/auto-increment.md#mysql-compatibility-mode)。但是，ID 不一定是连续分配的，因此建议避免混合使用默认值和自定义值，以防遇到 `Duplicated Error` 消息。

+ 你可以使用 `tidb_allow_remove_auto_inc` 系统变量来允许或禁止移除 `AUTO_INCREMENT` 列属性。要移除列属性，请使用 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 语法。

+ TiDB 不支持添加 `AUTO_INCREMENT` 列属性，一旦移除，就无法恢复。

+ 对于 TiDB v6.6.0 及更早版本，TiDB 中的自增列的行为与 MySQL InnoDB 相同，要求它们是主键或索引前缀。从 v7.0.0 开始，TiDB 移除了这个限制，允许更灵活的表主键定义。[#40580](https://github.com/pingcap/tidb/issues/40580)

更多详情，请参阅 [`AUTO_INCREMENT`](/auto-increment.md)。

> **注意：**
>
> + 如果在创建表时未指定主键，TiDB 使用 `_tidb_rowid` 来标识行。此值的分配与自增列（如果存在）共享一个分配器。如果将自增列指定为主键，TiDB 使用该列来标识行。在这种情况下，可能会出现以下情况：

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

如图所示，由于共享分配器，`id` 每次增加 2。在 [MySQL 兼容模式](/auto-increment.md#mysql-compatibility-mode)下，此行为会改变，因为没有共享分配器，因此不会跳过数字。

<CustomContent platform="tidb">

> **注意：**
>
> `AUTO_INCREMENT` 属性可能在生产环境中造成热点问题。详情请参阅[热点问题处理](/troubleshoot-hot-spot-issues.md)。建议改用 [`AUTO_RANDOM`](/auto-random.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> `AUTO_INCREMENT` 属性可能在生产环境中造成热点问题。详情请参阅[热点问题处理](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)。建议改用 [`AUTO_RANDOM`](/auto-random.md)。

</CustomContent>

### Performance schema

<CustomContent platform="tidb">

TiDB 使用 [Prometheus 和 Grafana](/tidb-monitoring-api.md) 的组合来存储和查询性能监控指标。在 TiDB 中，大多数[性能 schema 表](/performance-schema/performance-schema.md)不返回任何结果。

</CustomContent>

<CustomContent platform="tidb-cloud">

要在 TiDB Cloud 中检查性能指标，你可以查看 TiDB Cloud 控制台中的集群概览页面，或使用[第三方监控集成](/tidb-cloud/third-party-monitoring-integrations.md)。在 TiDB 中，大多数[性能 schema 表](/performance-schema/performance-schema.md)返回空结果。

</CustomContent>

### 查询执行计划

TiDB 中查询执行计划（`EXPLAIN`/`EXPLAIN FOR`）的输出格式、内容和权限设置与 MySQL 有显著差异。

在 TiDB 中，MySQL 系统变量 `optimizer_switch` 是只读的，对查询计划没有影响。虽然优化器提示可以使用类似 MySQL 的语法，但可用的提示及其实现可能有所不同。

更多信息，请参阅[理解查询执行计划](/explain-overview.md)。

### 内置函数

TiDB 支持 MySQL 中的大多数内置函数，但不是全部。你可以使用 [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md) 语句获取可用函数列表。

### DDL 操作

在 TiDB 中，所有支持的 DDL 更改都可以在线执行。但是，与 MySQL 相比，TiDB 中的 DDL 操作有一些主要限制：

* 使用单个 `ALTER TABLE` 语句修改表的多个架构对象（如列或索引）时，不支持在多个更改中指定相同的对象。例如，如果执行 `ALTER TABLE t1 MODIFY COLUMN c1 INT, DROP COLUMN c1` 命令，将输出 `Unsupported operate same column/index` 错误。
* 不支持使用单个 `ALTER TABLE` 语句修改多个 TiDB 特定的架构对象，如 `TIFLASH REPLICA`、`SHARD_ROW_ID_BITS` 和 `AUTO_ID_CACHE`。
* TiDB 不支持使用 `ALTER TABLE` 更改某些数据类型。例如，TiDB 不支持从 `DECIMAL` 类型更改为 `DATE` 类型。如果数据类型更改不受支持，TiDB 会报告 `Unsupported modify column: type %d not match origin %d` 错误。更多详情请参阅 [`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)。
* `ALGORITHM={INSTANT,INPLACE,COPY}` 语法在 TiDB 中仅作为断言功能，不会修改 `ALTER` 算法。更多详情请参阅 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)。
* 不支持添加/删除 `CLUSTERED` 类型的主键。关于 `CLUSTERED` 类型的主键的更多详情，请参阅[聚簇索引](/clustered-indexes.md)。
* 不支持不同类型的索引（`HASH|BTREE|RTREE|FULLTEXT`），指定时会被解析并忽略。
* TiDB 支持 `HASH`、`RANGE`、`LIST` 和 `KEY` 分区类型。对于不支持的分区类型，TiDB 返回 `Warning: Unsupported partition type %s, treat as normal table`，其中 `%s` 是具体的不支持的分区类型。
* Range、Range COLUMNS、List 和 List COLUMNS 分区表支持 `ADD`、`DROP`、`TRUNCATE` 和 `REORGANIZE` 操作。其他分区操作将被忽略。
* Hash 和 Key 分区表支持 `ADD`、`COALESCE` 和 `TRUNCATE` 操作。其他分区操作将被忽略。
* 分区表不支持以下语法：

    - `SUBPARTITION`
    - `{CHECK|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD} PARTITION`

    关于分区的更多详情，请参阅[分区表](/partitioned-table.md)。

### 分析表

在 TiDB 中，[统计信息收集](/statistics.md#manual-collection)与 MySQL 不同，它完全重建表的统计信息，使其成为一个更耗费资源且需要更长时间完成的操作。相比之下，MySQL/InnoDB 执行的是相对轻量级且短暂的操作。

更多信息，请参阅 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)。

### `SELECT` 语法的限制

TiDB 不支持以下 `SELECT` 语法：

- `SELECT ... INTO @variable`
- `SELECT .. GROUP BY expr` 不像在 MySQL 5.7 中那样隐含 `GROUP BY expr ORDER BY expr`

更多详情，请参阅 [`SELECT`](/sql-statements/sql-statement-select.md) 语句参考。

### `UPDATE` 语句

请参阅 [`UPDATE`](/sql-statements/sql-statement-update.md) 语句参考。

### 视图

TiDB 中的视图不可更新，不支持写操作，如 `UPDATE`、`INSERT` 和 `DELETE`。

### 临时表

更多信息，请参阅 [TiDB 本地临时表与 MySQL 临时表的兼容性](/temporary-tables.md#compatibility-with-mysql-temporary-tables)。

### 字符集和排序规则

* 要了解 TiDB 支持的字符集和排序规则，请参阅[字符集和排序规则概述](/character-set-and-collation.md)。

* 关于 GBK 字符集的 MySQL 兼容性信息，请参阅 [GBK 兼容性](/character-set-gbk.md#mysql-compatibility)。

* TiDB 继承表中使用的字符集作为国家字符集。

### 存储引擎

TiDB 允许使用替代存储引擎创建表。尽管如此，TiDB 描述的元数据是针对 InnoDB 存储引擎的，这是为了确保兼容性。

<CustomContent platform="tidb">

要使用 [`--store`](/command-line-flags-for-tidb-configuration.md#--store) 选项指定存储引擎，需要启动 TiDB 服务器。这个存储引擎抽象功能类似于 MySQL。

</CustomContent>

### SQL 模式

TiDB 支持大多数 [SQL 模式](/sql-mode.md)：

- 兼容模式，如 `Oracle` 和 `PostgreSQL` 会被解析但被忽略。兼容模式在 MySQL 5.7 中已弃用，在 MySQL 8.0 中已移除。
- `ONLY_FULL_GROUP_BY` 模式与 MySQL 5.7 相比有细微的[语义差异](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql)。
- MySQL 中的 `NO_DIR_IN_CREATE` 和 `NO_ENGINE_SUBSTITUTION` SQL 模式为了兼容性而被接受，但不适用于 TiDB。

### 默认值差异

TiDB 与 MySQL 5.7 和 MySQL 8.0 相比有默认值差异：

- 默认字符集：
    - TiDB 的默认值是 `utf8mb4`。
    - MySQL 5.7 的默认值是 `latin1`。
    - MySQL 8.0 的默认值是 `utf8mb4`。
- 默认排序规则：
    - TiDB 的默认排序规则是 `utf8mb4_bin`。
    - MySQL 5.7 的默认排序规则是 `utf8mb4_general_ci`。
    - MySQL 8.0 的默认排序规则是 `utf8mb4_0900_ai_ci`。
- 默认 SQL 模式：
    - TiDB 的默认 SQL 模式包括这些模式：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`。
    - MySQL 的默认 SQL 模式：
        - MySQL 5.7 中的默认 SQL 模式与 TiDB 相同。
        - MySQL 8.0 中的默认 SQL 模式包括这些模式：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`。
- `lower_case_table_names` 的默认值：
    - TiDB 中的默认值是 `2`，目前仅支持 `2`。
    - MySQL 默认值如下：
        - 在 Linux 上：`0`。这意味着表和数据库名称按照 `CREATE TABLE` 或 `CREATE DATABASE` 语句中指定的字母大小写存储在磁盘上。名称比较区分大小写。
        - 在 Windows 上：`1`。这意味着表名以小写形式存储在磁盘上，名称比较不区分大小写。MySQL 在存储和查找时将所有表名转换为小写。这种行为也适用于数据库名称和表别名。
        - 在 macOS 上：`2`。这意味着表和数据库名称按照 `CREATE TABLE` 或 `CREATE DATABASE` 语句中指定的字母大小写存储在磁盘上，但 MySQL 在查找时将它们转换为小写。名称比较不区分大小写。
- `explicit_defaults_for_timestamp` 的默认值：
    - TiDB 中的默认值是 `ON`，目前仅支持 `ON`。
    - MySQL 默认值如下：
        - MySQL 5.7：`OFF`。
        - MySQL 8.0：`ON`。

### 日期和时间

TiDB 支持命名时区，但有以下注意事项：

+ TiDB 使用系统中当前安装的所有时区规则进行计算，通常是 `tzdata` 包。这使得可以使用所有时区名称，而无需导入时区表数据。导入时区表数据不会改变计算规则。
+ 目前，MySQL 默认使用本地时区，然后依赖系统内置的当前时区规则（例如，夏令时开始时）进行计算。如果不[导入时区表数据](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation)，MySQL 无法通过名称指定时区。

### 类型系统差异

以下列类型被 MySQL 支持但**不**被 TiDB 支持：

- `SQL_TSI_*`（包括 SQL_TSI_MONTH、SQL_TSI_WEEK、SQL_TSI_DAY、SQL_TSI_HOUR、SQL_TSI_MINUTE 和 SQL_TSI_SECOND，但不包括 SQL_TSI_YEAR）

### 正则表达式

关于 TiDB 正则表达式与 MySQL 的兼容性信息，包括 `REGEXP_INSTR()`、`REGEXP_LIKE()`、`REGEXP_REPLACE()` 和 `REGEXP_SUBSTR()`，请参阅[正则表达式与 MySQL 的兼容性](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql)。

### 由于弃用功能导致的不兼容性

TiDB 不实现 MySQL 中已弃用的特定功能，包括：

- 为浮点类型指定精度。MySQL 8.0 [弃用](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html)此功能，建议改用 `DECIMAL` 类型。
- `ZEROFILL` 属性。MySQL 8.0 [弃用](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html)此功能，建议在应用程序中对数值进行填充。

### `CREATE RESOURCE GROUP`、`DROP RESOURCE GROUP` 和 `ALTER RESOURCE GROUP` 语句

以下用于创建、修改和删除资源组的语句支持的参数与 MySQL 不同。详情请参阅以下文档：

- [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)
- [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)
- [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)
