---
title: EXPLAIN ANALYZE
summary: TiDB 数据库中 EXPLAIN ANALYZE 的使用概况。
category: reference
---

# EXPLAIN ANALYZE

`EXPLAIN ANALYZE` 语句的工作方式类似于 `EXPLAIN`，主要区别在于前者实际上会执行语句。这样可以将查询计划中的估计值与执行时所遇到的实际值进行比较。如果估计值与实际值显著不同，那么应考虑在受影响的表上运行 `ANALYZE TABLE`。

## 语法图

**ExplainSym:**

![ExplainSym](/media/sqlgram/ExplainSym.png)

**ExplainStmt:**

![ExplainStmt](/media/sqlgram/ExplainStmt.png)

**ExplainableStmt:**

![ExplainableStmt](/media/sqlgram/ExplainableStmt.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1 WHERE id = 1;
```

```
+-------------+-------+------+--------------------+---------------------------+
| id          | count | task | operator info      | execution info            |
+-------------+-------+------+--------------------+---------------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 | time:0ns, loops:0, rows:0 |
+-------------+-------+------+--------------------+---------------------------+
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1;
```

```
+-------------------+----------+------+-------------------------------------------------------------+----------------------------------+
| id                | count    | task | operator info                                               | execution info                   |
+-------------------+----------+------+-------------------------------------------------------------+----------------------------------+
| TableReader_5     | 10000.00 | root | data:TableScan_4                                            | time:931.759µs, loops:2, rows:3  |
| └─TableScan_4     | 10000.00 | cop  | table:t1, range:[-inf,+inf], keep order:false, stats:pseudo | time:0s, loops:0, rows:3         |
+-------------------+----------+------+-------------------------------------------------------------+----------------------------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [Understanding the Query Execution Plan](/reference/performance/understanding-the-query-execution-plan.md)
* [EXPLAIN](/reference/sql/statements/explain.md)
* [ANALYZE TABLE](/reference/sql/statements/analyze-table.md)
* [TRACE](/reference/sql/statements/trace.md)
