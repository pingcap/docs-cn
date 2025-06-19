---
title: SELECT | TiDB SQL 语句参考
summary: TiDB 数据库中 SELECT 的使用概述。
---

# SELECT

`SELECT` 语句用于从 TiDB 读取数据。

## 语法图

```ebnf+diagram
SelectStmt ::=
    ( SelectStmtBasic | SelectStmtFromDualTable | SelectStmtFromTable )
    OrderBy? SelectStmtLimit? SelectLockOpt? SelectStmtIntoOption

SelectStmtBasic ::=
    "SELECT" SelectStmtOpts Field ("," Field)* ( "HAVING" Expression)?

SelectStmtFromDualTable ::=
    "SELECT" SelectStmtOpts Field ("," Field)* "FROM" "DUAL" WhereClause?

SelectStmtFromTable ::=
    "SELECT" SelectStmtOpts Field ("," Field)* "FROM" TableRefsClause
    WhereClause? GroupByClause? ( "HAVING" Expression)? WindowClause?

SelectStmtOpts ::=
    TableOptimizerHints DefaultFalseDistictOpt PriorityOpt SelectStmtSQLSmallResult
    SelectStmtSQLBigResult SelectStmtSQLBufferResult SelectStmtSQLCache SelectStmtCalcFoundRows
    SelectStmtStraightJoin

TableRefsClause ::=
    TableRef AsOfClause? ( ',' TableRef AsOfClause? )*

AsOfClause ::=
    'AS' 'OF' 'TIMESTAMP' Expression

SelectStmtLimit ::=
    ("LIMIT" LimitOption ( ("," | "OFFSET") LimitOption )?
| "FETCH" ("FIRST" | "NEXT") LimitOption? ("ROW" | "ROWS") "ONLY" )

SelectLockOpt ::= 
    ( 'FOR' 'UPDATE' ( 'OF' TableList )? 'NOWAIT'?
|   'LOCK' 'IN' 'SHARE' 'MODE' )

TableList ::=
    TableName ( ',' TableName )*

WindowClause ::=
    "WINDOW" WindowDefinition ("," WindowDefinition)*

TableSampleOpt ::=
    'TABLESAMPLE' 'REGIONS' '(' ')'
```

## 语法元素说明

|语法元素|说明|
|:--------------------- | :-------------------------------------------------- |
|`TableOptimizerHints`| 这是用于控制 TiDB 优化器行为的提示。更多信息，请参考[优化器提示](/optimizer-hints.md)。|
|`ALL`，`DISTINCT`，`DISTINCTROW` | `ALL`，`DISTINCT`/`DISTINCTROW` 修饰符指定是否应返回重复行。ALL（默认值）指定应返回所有匹配的行。|
|`HIGH_PRIORITY` | `HIGH_PRIORITY` 给当前语句比其他语句更高的优先级。|
|`SQL_CALC_FOUND_ROWS`| TiDB 不支持此功能，除非设置了 [`tidb_enable_noop_functions=1`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)，否则将返回错误。|
|`SQL_CACHE`，`SQL_NO_CACHE` | `SQL_CACHE` 和 `SQL_NO_CACHE` 用于控制是否将请求结果缓存到 TiKV（RocksDB）的 `BlockCache` 中。对于大量数据的一次性查询，如 `count(*)` 查询，建议填写 `SQL_NO_CACHE` 以避免刷新 `BlockCache` 中的热用户数据。|
|`STRAIGHT_JOIN`| `STRAIGHT_JOIN` 强制优化器按照 `FROM` 子句中使用的表的顺序进行联合查询。当优化器选择的联接顺序不好时，可以使用此语法来加快查询的执行速度。|
|`select_expr` | 每个 `select_expr` 表示要检索的列，包括列名和表达式。`\*` 代表所有列。|
|`FROM table_references` | `FROM table_references` 子句指示要从中检索行的表（如 `select * from t;`），或表（如 `select * from t1 join t2;`），甚至是 0 个表（如 `select 1+1 from dual;` 等同于 `select 1+1;`）。|
|`WHERE where_condition` | `WHERE` 子句（如果给定）指示行必须满足的条件才能被选择。结果只包含满足条件的数据。|
|`GROUP BY` | `GROUP BY` 语句用于对结果集进行分组。|
|`HAVING where_condition` | `HAVING` 子句和 `WHERE` 子句都用于过滤结果。`HAVING` 子句过滤 `GROUP BY` 的结果，而 `WHERE` 子句在聚合之前过滤结果。|
|`ORDER BY` | `ORDER BY` 子句用于根据列、表达式或 `select_expr` 列表中的项目按升序或降序对数据进行排序。|
|`LIMIT` | `LIMIT` 子句可用于限制返回的行数。`LIMIT` 接受一个或两个数字参数。使用一个参数时，该参数指定要返回的最大行数，默认情况下第一行是表的第一行；使用两个参数时，第一个参数指定要返回的第一行的偏移量，第二个参数指定要返回的最大行数。TiDB 还支持 `FETCH FIRST/NEXT n ROW/ROWS ONLY` 语法，其效果与 `LIMIT n` 相同。在此语法中可以省略 `n`，其效果与 `LIMIT 1` 相同。|
|`Window window_definition`| 这是窗口函数的语法，通常用于进行一些分析计算。更多信息，请参考[窗口函数](/functions-and-operators/window-functions.md)。|
| `FOR UPDATE`  | `SELECT FOR UPDATE` 子句锁定结果集中的所有数据以检测来自其他事务的并发更新。匹配查询条件但不存在于结果集中的数据不会被读锁定，例如在当前事务启动后由其他事务写入的行数据。当 TiDB 使用[乐观事务模式](/optimistic-transaction.md)时，在语句执行阶段不会检测事务冲突。因此，当前事务不会像其他数据库（如 PostgreSQL）那样阻止其他事务执行 `UPDATE`、`DELETE` 或 `SELECT FOR UPDATE`。在提交阶段，`SELECT FOR UPDATE` 读取的行以两阶段方式提交，这意味着它们也可以参与冲突检测。如果发生写冲突，包含 `SELECT FOR UPDATE` 子句的所有事务的提交都会失败。如果未检测到冲突，提交成功。并且会为锁定的行生成新版本，以便在稍后提交其他未提交的事务时可以检测到写冲突。当 TiDB 使用[悲观事务模式](/pessimistic-transaction.md)时，行为基本与其他数据库相同。请参考[与 MySQL InnoDB 的差异](/pessimistic-transaction.md#difference-with-mysql-innodb)了解详细信息。TiDB 支持 `FOR UPDATE` 的 `NOWAIT` 修饰符。有关详细信息，请参见 [TiDB 悲观事务模式](/pessimistic-transaction.md#behaviors)。|
|`LOCK IN SHARE MODE` | 为保证兼容性，TiDB 解析这三个修饰符，但会忽略它们。|
| `TABLESAMPLE` | 用于从表中获取行样本。|

> **注意：**
>
> 从 v6.6.0 开始，TiDB 支持[资源控制](/tidb-resource-control.md)。你可以使用此功能在不同的资源组中以不同的优先级执行 SQL 语句。通过为这些资源组配置适当的配额和优先级，你可以更好地控制不同优先级 SQL 语句的调度。当启用资源控制时，语句优先级（`HIGH_PRIORITY`）将不再生效。建议你使用[资源控制](/tidb-resource-control.md)来管理不同 SQL 语句的资源使用。

## 示例

### SELECT

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
5 rows in set (0.00 sec)
```

```sql
mysql> SELECT AVG(s_quantity), COUNT(s_quantity) FROM stock TABLESAMPLE REGIONS();
+-----------------+-------------------+
| AVG(s_quantity) | COUNT(s_quantity) |
+-----------------+-------------------+
|         59.5000 |                 4 |
+-----------------+-------------------+
1 row in set (0.00 sec)

mysql> SELECT AVG(s_quantity), COUNT(s_quantity) FROM stock;
+-----------------+-------------------+
| AVG(s_quantity) | COUNT(s_quantity) |
+-----------------+-------------------+
|         54.9729 |           1000000 |
+-----------------+-------------------+
1 row in set (0.52 sec)
```

上面的示例使用了通过 `tiup bench tpcc prepare` 生成的数据。第一个查询展示了 `TABLESAMPLE` 的使用。

### SELECT ... INTO OUTFILE

`SELECT ... INTO OUTFILE` 语句用于将查询结果写入文件。

> **注意：**
>
> - 此语句仅适用于 TiDB 自建集群，在 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/) 上不可用。
> - 此语句不支持将查询结果写入任何[外部存储](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)，如 Amazon S3 或 GCS。

在语句中，你可以使用以下子句指定输出文件的格式：

- `FIELDS TERMINATED BY`：指定文件中的字段分隔符。例如，你可以指定为 `','` 以输出逗号分隔值（CSV）或 `'\t'` 以输出制表符分隔值（TSV）。
- `FIELDS ENCLOSED BY`：指定包围文件中每个字段的封闭字符。
- `LINES TERMINATED BY`：指定文件中的行终止符，如果你想用某个字符结束一行。

假设有一个包含三列的表 `t`，如下所示：

```sql
mysql> CREATE TABLE t (a INT, b VARCHAR(10), c DECIMAL(10,2));
Query OK, 0 rows affected (0.02 sec)

mysql> INSERT INTO t VALUES (1, 'a', 1.1), (2, 'b', 2.2), (3, 'c', 3.3);
Query OK, 3 rows affected (0.01 sec)
```

以下示例展示如何使用 `SELECT ... INTO OUTFILE` 语句将查询结果写入文件。

**示例 1：**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file1';
Query OK, 3 rows affected (0.00 sec)
```

在此示例中，你可以在 `/tmp/tmp_file1` 中找到如下查询结果：

```
1       a       1.10
2       b       2.20
3       c       3.30
```

**示例 2：**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file2' FIELDS TERMINATED BY ',' ENCLOSED BY '"';
Query OK, 3 rows affected (0.00 sec)
```

在此示例中，你可以在 `/tmp/tmp_file2` 中找到如下查询结果：

```
"1","a","1.10"
"2","b","2.20"
"3","c","3.30"
```

**示例 3：**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file3'
    -> FIELDS TERMINATED BY ',' ENCLOSED BY '\'' LINES TERMINATED BY '<<<\n';
Query OK, 3 rows affected (0.00 sec)
```

在此示例中，你可以在 `/tmp/tmp_file3` 中找到如下查询结果：

```
'1','a','1.10'<<<
'2','b','2.20'<<<
'3','c','3.30'<<<
```

## MySQL 兼容性

- 不支持 `SELECT ... INTO @variable` 语法。
- 不支持 `SELECT ... INTO DUMPFILE` 语法。
- `SELECT .. GROUP BY expr` 语法不像在 MySQL 5.7 中那样隐含 `GROUP BY expr ORDER BY expr`。TiDB 反而匹配 MySQL 8.0 的行为，不隐含默认顺序。
- `SELECT ... TABLESAMPLE ...` 语法是 TiDB 的扩展，设计用于与其他数据库系统和 [ISO/IEC 9075-2](https://standards.iso.org/iso-iec/9075/-2/ed-6/en/) 标准兼容，但目前 MySQL 不支持此语法。

## 另请参阅

* [INSERT](/sql-statements/sql-statement-insert.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [UPDATE](/sql-statements/sql-statement-update.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)
