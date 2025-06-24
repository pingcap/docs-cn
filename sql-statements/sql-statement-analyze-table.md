---
title: ANALYZE | TiDB SQL 语句参考
summary: TiDB 数据库中 ANALYZE 的使用概览。
---

# ANALYZE

该语句用于更新 TiDB 在表和索引上建立的统计信息。建议在执行大批量更新或导入记录后，或者当你发现查询执行计划不理想时运行 `ANALYZE`。

当 TiDB 发现统计信息与其自身估计不一致时，也会随着时间自动更新其统计信息。

目前，TiDB 通过使用 `ANALYZE TABLE` 语句进行完整收集来收集统计信息。有关更多信息，请参阅[统计信息简介](/statistics.md)。

## 语法图

```ebnf+diagram
AnalyzeTableStmt ::=
    'ANALYZE' ( 'TABLE' ( TableNameList ( 'ALL COLUMNS' | 'PREDICATE COLUMNS' ) | TableName ( 'INDEX' IndexNameList? | AnalyzeColumnOption | 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList? | AnalyzeColumnOption )? )? ) ) AnalyzeOptionListOpt

AnalyzeOptionListOpt ::=
( WITH AnalyzeOptionList )?

AnalyzeOptionList ::=
AnalyzeOption ( ',' AnalyzeOption )*

AnalyzeOption ::=
( NUM ( 'BUCKETS' | 'TOPN' | ( 'CMSKETCH' ( 'DEPTH' | 'WIDTH' ) ) | 'SAMPLES' ) ) | ( FLOATNUM 'SAMPLERATE' )

AnalyzeColumnOption ::=
( 'ALL COLUMNS' | 'PREDICATE COLUMNS' | 'COLUMNS' ColumnNameList )

TableNameList ::=
    TableName (',' TableName)*

TableName ::=
    Identifier ( '.' Identifier )?

ColumnNameList ::=
    Identifier ( ',' Identifier )*

IndexNameList ::=
    Identifier ( ',' Identifier )*

PartitionNameList ::=
    Identifier ( ',' Identifier )*
```

## 示例

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)
```

```sql
mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

```sql
mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)
```

```sql
mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

当前统计信息的状态是 `pseudo`，这意味着统计信息不准确。

```sql
mysql> ANALYZE TABLE t1;
Query OK, 0 rows affected (0.13 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+-------------------------------+
| id                     | estRows | task      | access object          | operator info                 |
+------------------------+---------+-----------+------------------------+-------------------------------+
| IndexReader_6          | 1.00    | root      |                        | index:IndexRangeScan_5        |
| └─IndexRangeScan_5     | 1.00    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false |
+------------------------+---------+-----------+------------------------+-------------------------------+
2 rows in set (0.00 sec)
```

统计信息现在已正确更新并加载。

## MySQL 兼容性

TiDB 在收集的统计信息和在查询执行期间如何使用统计信息方面**都**与 MySQL 不同。虽然此语句在语法上与 MySQL 类似，但以下差异适用：

+ 运行 `ANALYZE TABLE` 时，TiDB 可能不会包含最近提交的更改。在批量更新行后，你可能需要在执行 `ANALYZE TABLE` 之前执行 `sleep(1)`，以便统计信息更新能反映这些更改。参见 [#16570](https://github.com/pingcap/tidb/issues/16570)。
+ `ANALYZE TABLE` 在 TiDB 中的执行时间明显长于 MySQL。

## 另请参阅

* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
