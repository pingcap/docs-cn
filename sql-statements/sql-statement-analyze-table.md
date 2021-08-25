---
title: ANALYZE
summary: TiDB 数据库中 ANALYZE 的使用概况。
---

# ANALYZE

`ANALYZE` 语句用于更新 TiDB 在表和索引上留下的统计信息。执行大批量更新或导入记录后，或查询执行计划不是最佳时，建议运行 `ANALYZE`。

当 TiDB 逐渐发现这些统计数据与预估不一致时，也会自动更新其统计数据。

目前 TiDB 收集统计信息分为全量收集和增量收集两种方式，分别通过 `ANALYZE TABLE` 和 `ANALYZE INCREMENTAL TABLE` 语句来实现。关于这两种语句的详细使用方式，可参考[统计信息简介](/statistics.md)。

## 语法图

```ebnf+diagram
AnalyzeTableStmt ::=
    'ANALYZE' ( 'TABLE' ( TableNameList | TableName ( 'INDEX' IndexNameList | 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList )? ) ) | 'INCREMENTAL' 'TABLE' TableName ( 'PARTITION' PartitionNameList )? 'INDEX' IndexNameList ) AnalyzeOptionListOpt

TableNameList ::=
    TableName (',' TableName)*

TableName ::=
    Identifier ( '.' Identifier )?
```

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 ADD INDEX (c1);
```

```
Query OK, 0 rows affected (0.30 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
analyze table t1;
```

```
Query OK, 0 rows affected (0.13 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```
+------------------------+---------+-----------+------------------------+-------------------------------+
| id                     | estRows | task      | access object          | operator info                 |
+------------------------+---------+-----------+------------------------+-------------------------------+
| IndexReader_6          | 1.00    | root      |                        | index:IndexRangeScan_5        |
| └─IndexRangeScan_5     | 1.00    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false |
+------------------------+---------+-----------+------------------------+-------------------------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

* `ANALYZE TABLE` 在语法上与 MySQL 类似。但 `ANALYZE TABLE` 在 TiDB 上的执行时间可能长得多，因为它的内部运行方式不同。

* 在 MySQL 上不支持 `ANALYZE INCREMENTAL TABLE` 语句，它的使用可参考[增量收集文档](/statistics.md#增量收集)。

TiDB 与 MySQL 在以下方面存在区别：所收集的统计信息，以及查询执行过程中统计信息是如何被使用的。虽然 TiDB 中的 `ANALYZE` 语句在语法上与 MySQL 类似，但存在以下差异：

+ 执行 `ANALYZE TABLE` 时，TiDB 可能不包含最近提交的更改。若对行进行了批量更改，在执行 `ANALYZE TABLE` 之前，你可能需要先执行 `sleep(1)`，这样统计信息更新才能反映这些更改。参见 [#16570](https://github.com/pingcap/tidb/issues/16570)。
+ `ANALYZE TABLE` 在 TiDB 中的执行时间比在 MySQL 中的执行时间要长得多。但你可以通过执行 `SET GLOBAL tidb_enable_fast_analyze=1` 来启用快速分析，这样能部分抵消这种执行上的性能差异。快速分析利用了采样，会导致统计信息的准确性降低。因此快速分析仍是一项实验特性。

## 另请参阅

* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
