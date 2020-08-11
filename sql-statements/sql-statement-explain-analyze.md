---
title: EXPLAIN ANALYZE | TiDB SQL Statement Reference
summary: An overview of the usage of EXPLAIN ANALYZE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-explain-analyze/','/docs/dev/reference/sql/statements/explain-analyze/']
---

# EXPLAIN ANALYZE

The `EXPLAIN ANALYZE` statement works similar to `EXPLAIN`, with the major difference being that it will actually execute the statement. This allows you to compare the estimates used as part of query planning to actual values encountered during execution.  If the estimates differ significantly from the actual values, you should consider running `ANALYZE TABLE` on the affected tables.

> **Note:**
>
> When you use `EXPLAIN ANALYZE` to execute DML statements, modification to data is normally executed. Currently, the execution plan for DML statements **cannot** be shown yet.

## Synopsis

**ExplainSym:**

![ExplainSym](/media/sqlgram/ExplainSym.png)

**ExplainStmt:**

![ExplainStmt](/media/sqlgram/ExplainStmt.png)

**ExplainableStmt:**

![ExplainableStmt](/media/sqlgram/ExplainableStmt.png)

## EXPLAIN ANALYZE output format

Different from `EXPLAIN`, `EXPLAIN ANALYZE` executes the corresponding SQL statement, records its runtime information, and returns the information together with the execution plan. Therefore, you can regard `EXPLAIN ANALYZE` as an extension of the `EXPLAIN` statement. Compared to `EXPLAIN`, the return results of `EXPLAIN ANALYZE` include columns of information such as `actRows`, `execution info`, `memory`, and `disk`. The details of these columns are shown as follows:

| attribute name          | description |
|:----------------|:---------------------------------|
| actRows       | Number of rows output by the operator. |
| execution info  | Execution information of the operator. `time` represents the total `wall time` from entering the operator to leaving the operator, including the total execution time of all sub-operators. If the operator is called many times by the parent operator (in loops), then the time refers to the accumulated time. `loops` is the number of times the current operator is called by the parent operator. |
| memory  | Memory space occupied by the operator. |
| disk  | Disk space occupied by the operator. |

## Examples

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```sql
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1 WHERE id = 1;
```

```sql
+-------------+---------+---------+------+---------------+--------------------------+---------------+--------+------+
| id          | estRows | actRows | task | access object | execution info           | operator info | memory | disk |
+-------------+---------+---------+------+---------------+--------------------------+---------------+--------+------+
| Point_Get_1 | 1.00    | 1       | root | table:t1      | time:177.183µs, loops:2  | handle:1      | N/A    | N/A  |
+-------------+---------+---------+------+---------------+--------------------------+---------------+--------+------+
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1;
```

```sql
+-----------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------+--------------------------------+-----------+------+
| id                    | estRows  | actRows | task      | access object | execution info                                                         | operator info                  | memory    | disk |
+-----------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------+--------------------------------+-----------+------+
| TableReader_5         | 10000.00 | 3       | root      |               | time:454.744µs, loops:2, rpc num: 1, rpc time:328.334µs, proc keys:0   | data:TableFullScan_4           | 199 Bytes | N/A  |
| └─TableFullScan_4     | 10000.00 | 3       | cop[tikv] | table:t1      | time:148.227µs, loops:4                                                | keep order:false, stats:pseudo | N/A       | N/A  |
+-----------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------+--------------------------------+-----------+------+
2 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Understanding the Query Execution Plan](/query-execution-plan.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
