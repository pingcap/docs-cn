---
title: SELECT | TiDB SQL Statement Reference
summary: An overview of the usage of SELECT for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-select/','/docs/dev/reference/sql/statements/select/']
---

# SELECT

The `SELECT` statement is used to read data from TiDB.

## Synopsis

**SelectStmt:**

![SelectStmt](/media/sqlgram/SelectStmt.png)

**FromDual:**

![FromDual](/media/sqlgram/FromDual.png)

**SelectStmtOpts:**

![SelectStmtOpts](/media/sqlgram/SelectStmtOpts.png)

**SelectStmtFieldList:**

![SelectStmtFieldList](/media/sqlgram/SelectStmtFieldList.png)

**TableRefsClause:**

```ebnf+diagram
TableRefsClause ::=
    TableRef AsOfClause? ( ',' TableRef AsOfClause? )*

AsOfClause ::=
    'AS' 'OF' 'TIMESTAMP' Expression
```

**WhereClauseOptional:**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

**SelectStmtGroup:**

![SelectStmtGroup](/media/sqlgram/SelectStmtGroup.png)

**HavingClause:**

![HavingClause](/media/sqlgram/HavingClause.png)

**OrderByOptional:**

![OrderByOptional](/media/sqlgram/OrderByOptional.png)

**SelectStmtLimit:**

![SelectStmtLimit](/media/sqlgram/SelectStmtLimit.png)

**FirstOrNext:**

![FirstOrNext](/media/sqlgram/FirstOrNext.png)

**FetchFirstOpt:**

![FetchFirstOpt](/media/sqlgram/FetchFirstOpt.png)

**RowOrRows:**

![RowOrRows](/media/sqlgram/RowOrRows.png)

**SelectLockOpt:**

```ebnf+diagram
SelectLockOpt ::= 
    ( ( 'FOR' 'UPDATE' ( 'OF' TableList )? 'NOWAIT'? )
|   ( 'LOCK' 'IN' 'SHARE' 'MODE' ) )?

TableList ::=
    TableName ( ',' TableName )*
```

**WindowClauseOptional**

![WindowClauseOptional](/media/sqlgram/WindowClauseOptional.png)

**TableSampleOpt**

```ebnf+diagram
TableSampleOpt ::=
    'TABLESAMPLE' 'REGIONS()'
```

## Description of the syntax elements

|Syntax Element|Description|
|:--------------------- | :-------------------------------------------------- |
|`TableOptimizerHints`| This is the hint to control the behavior of TiDB's optimizer. For more information, refer to [Optimizer Hints](/optimizer-hints.md). |
|`ALL`, `DISTINCT`, `DISTINCTROW` | The `ALL`, `DISTINCT`/`DISTINCTROW` modifiers specify whether duplicate rows should be returned. ALL (the default) specifies that all matching rows should be returned.|
|`HIGH_PRIORITY` | `HIGH_PRIORITY` gives the current statement higher priority than other statements. |
|`SQL_CALC_FOUND_ROWS`| TiDB does not support this feature, and will return an error unless [`tidb_enable_noop_functions=1`](/system-variables.md#tidb_enable_noop_functions-new-in-v40) is set. |
|`SQL_CACHE`, `SQL_NO_CACHE` | `SQL_CACHE` and `SQL_NO_CACHE` are used to control whether to cache the request results to the `BlockCache` of TiKV (RocksDB). For a one-time query on a large amount of data, such as the `count(*)` query, it is recommended to fill in `SQL_NO_CACHE` to avoid flushing the hot user data in `BlockCache`. |
|`STRAIGHT_JOIN`| `STRAIGHT_JOIN` forces the optimizer to do a union query in the order of the tables used in the `FROM` clause. When the optimizer chooses a join order that is not good, you can use this syntax to speed up the execution of the query. |
|`select_expr` | Each `select_expr` indicates a column to retrieve. including the column names and expressions. `\*` represents all the columns.|
|`FROM table_references` | The `FROM table_references` clause indicates the table (such as `select * from t;`), or tables (such as `select * from t1 join t2;`) or even 0 tables (such as `select 1+1 from dual;` which is equivalent to `select 1+1;`) from which to retrieve rows.|
|`WHERE where_condition` | The `WHERE` clause, if given, indicates the condition or conditions that rows must satisfy to be selected. The result contains only the data that meets the condition(s).|
|`GROUP BY` | The `GROUP BY` statement is used to group the result-set.|
|`HAVING where_condition` | The `HAVING` clause and the `WHERE` clause are both used to filter the results. The `HAVING` clause filters the results of `GROUP BY`, while the `WHERE` clause filter the results before aggregation. |
|`ORDER BY` | The `ORDER BY` clause is used to sort the data in ascending or descending order, based on columns, expressions or items in the `select_expr` list.|
|`LIMIT` | The `LIMIT` clause can be used to constrain the number of rows. `LIMIT` takes one or two numeric arguments. With one argument, the argument specifies the maximum number of rows to return, the first row to return is the first row of the table by default; with two arguments, the first argument specifies the offset of the first row to return, and the second specifies the maximum number of rows to return. TiDB also supports the `FETCH FIRST/NEXT n ROW/ROWS ONLY` syntax, which has the same effect as `LIMIT n`. You can omit `n` in this syntax and its effect is the same as `LIMIT 1`. |
|`Window window_definition`| This is the syntax for window function, which is usually used to do some analytical computation. For more information, refer to [Window Function](/functions-and-operators/window-functions.md). |
| `FOR UPDATE`  | The `SELECT FOR UPDATE` clause locks all the data in the result sets to detect concurrent updates from other transactions. Data that match the query conditions but do not exist in the result sets are not read-locked, such as the row data written by other transactions after the current transaction is started. When TiDB uses the [Optimistic Transaction Mode](/optimistic-transaction.md), the transaction conflicts are not detected in the statement execution phase. Therefore, the current transaction does not block other transactions from executing `UPDATE`, `DELETE` or `SELECT FOR UPDATE` like other databases such as PostgreSQL. In the committing phase, the rows read by `SELECT FOR UPDATE` are committed in two phases, which means they can also join the conflict detection. If write conflicts occur, the commit fails for all transactions that include the `SELECT FOR UPDATE` clause. If no conflict is detected, the commit succeeds. And a new version is generated for the locked rows, so that write conflicts can be detected when other uncommitted transactions are being committed later. When TiDB uses the [Pessimistic Transaction Mode](/pessimistic-transaction.md), the behavior is basically the same as other databases. Refer to [Difference with MySQL InnoDB](/pessimistic-transaction.md#difference-with-mysql-innodb) to see the details. TiDB supports the `NOWAIT` modifier for `FOR UPDATE`. See [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md#behaviors) for details. |
|`LOCK IN SHARE MODE` | To guarantee compatibility, TiDB parses these three modifiers, but will ignore them. |
| `TABLESAMPLE` | To get a sample of rows from the table. |

## Examples

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

The above example uses data generated with `tiup bench tpcc prepare`. The first query shows the use of `TABLESAMPLE`.

### SELECT ... INTO OUTFILE

The `SELECT ... INTO OUTFILE` statement is used to write the result of a query to a file.

> **Note:**
>
> - This statement is only applicable to TiDB Self-Hosted and not available on [TiDB Cloud](https://docs.pingcap.com/tidbcloud/).
> - This statement does not support writing query results to any [external storages](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages) such as Amazon S3 or GCS.

In the statement, you can specify the format of the output file by using the following clauses:

- `FIELDS TERMINATED BY`: specifies the field delimiter in the file. For example, you can specify it as `','` to output comma-separated values (CSV) or `'\t'` to output tab-separated values (TSV).
- `FIELDS ENCLOSED BY`: specifies the enclosing character that wraps around each field in the file.
- `LINES TERMINATED BY`: specifies the line terminator in the file, if you want to end a line with a certain character.

Assume that there is a table `t` with three columns as follows:

```sql
mysql> CREATE TABLE t (a INT, b VARCHAR(10), c DECIMAL(10,2));
Query OK, 0 rows affected (0.02 sec)

mysql> INSERT INTO t VALUES (1, 'a', 1.1), (2, 'b', 2.2), (3, 'c', 3.3);
Query OK, 3 rows affected (0.01 sec)
```

The following examples show how to use the `SELECT ... INTO OUTFILE` statement to write the query result to a file.

**Example 1:**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file1';
Query OK, 3 rows affected (0.00 sec)
```

In this example, you can find the query result in `/tmp/tmp_file1` as follows:

```
1       a       1.10
2       b       2.20
3       c       3.30
```

**Example 2:**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file2' FIELDS TERMINATED BY ',' ENCLOSED BY '"';
Query OK, 3 rows affected (0.00 sec)
```

In this example, you can find the query result in `/tmp/tmp_file2` as follows:

```
"1","a","1.10"
"2","b","2.20"
"3","c","3.30"
```

**Example 3:**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file3'
    -> FIELDS TERMINATED BY ',' ENCLOSED BY '\'' LINES TERMINATED BY '<<<\n';
Query OK, 3 rows affected (0.00 sec)
```

In this example, you can find the query result in `/tmp/tmp_file3` as follows:

```
'1','a','1.10'<<<
'2','b','2.20'<<<
'3','c','3.30'<<<
```

## MySQL compatibility

- The syntax `SELECT ... INTO @variable` is not supported.
- The syntax `SELECT ... INTO DUMPFILE` is not supported.
- The syntax `SELECT .. GROUP BY expr` does not imply `GROUP BY expr ORDER BY expr` as it does in MySQL 5.7. TiDB instead matches the behavior of MySQL 8.0 and does not imply a default order.
- The syntax `SELECT ... TABLESAMPLE ...` is a TiDB extension designed for compatibility with other database systems and the [ISO/IEC 9075-2](https://standards.iso.org/iso-iec/9075/-2/ed-6/en/) standard, but currently it is not supported by MySQL.

## See also

* [INSERT](/sql-statements/sql-statement-insert.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [UPDATE](/sql-statements/sql-statement-update.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)
