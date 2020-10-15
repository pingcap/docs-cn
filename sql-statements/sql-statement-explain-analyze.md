---
title: EXPLAIN ANALYZE
summary: TiDB 数据库中 EXPLAIN ANALYZE 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-explain-analyze/','/docs-cn/dev/reference/sql/statements/explain-analyze/']
---

# EXPLAIN ANALYZE

`EXPLAIN ANALYZE` 语句的工作方式类似于 `EXPLAIN`，主要区别在于前者实际上会执行语句。这样可以将查询计划中的估计值与执行时所遇到的实际值进行比较。如果估计值与实际值显著不同，那么应考虑在受影响的表上运行 `ANALYZE TABLE`。

> **注意：**
>
> 在使用 `EXPLAIN ANALYZE` 执行 DML 语句时，数据的修改操作会被正常执行。但目前 DML 语句还无法展示执行计划。

## 语法图

**ExplainSym:**

![ExplainSym](/media/sqlgram/ExplainSym.png)

**ExplainStmt:**

![ExplainStmt](/media/sqlgram/ExplainStmt.png)

**ExplainableStmt:**

![ExplainableStmt](/media/sqlgram/ExplainableStmt.png)

## EXPLAIN ANALYZE 输出格式

和 `EXPLAIN` 不同，`EXPLAIN ANALYZE` 会执行对应的 SQL 语句，记录其运行时信息，和执行计划一并返回出来。因此，可以将 `EXPLAIN ANALYZE` 视为 `EXPLAIN` 语句的扩展。`EXPLAIN ANALYZE` 语句的返回结果相比 `EXPLAIN`，增加了 `actRows`，`execution info`，`memory`，`disk` 这几列信息：

| 属性名          | 含义 |
|:----------------|:---------------------------------|
| actRows       | 算子实际输出的数据条数。 |
| execution info  | 算子的实际执行信息。time 表示从进入算子到离开算子的全部 wall time，包括所有子算子操作的全部执行时间。如果该算子被父算子多次调用 (loops)，这个时间就是累积的时间。loops 是当前算子被父算子调用的次数。 |
| memory  | 算子占用内存空间的大小。 |
| disk  | 算子占用磁盘空间的大小。 |

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
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

```
+-----------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------+--------------------------------+-----------+------+
| id                    | estRows  | actRows | task      | access object | execution info                                                         | operator info                  | memory    | disk |
+-----------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------+--------------------------------+-----------+------+
| TableReader_5         | 10000.00 | 3       | root      |               | time:454.744µs, loops:2, rpc num: 1, rpc time:328.334µs, proc keys:0   | data:TableFullScan_4           | 199 Bytes | N/A  |
| └─TableFullScan_4     | 10000.00 | 3       | cop[tikv] | table:t1      | time:148.227µs, loops:4                                                | keep order:false, stats:pseudo | N/A       | N/A  |
+-----------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------+--------------------------------+-----------+------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

`EXPLAIN ANALYZE` 是 MySQL 8.0 的功能，但该语句在 MySQL 中的输出格式和可能的执行计划都与 TiDB 有较大差异。

## 另请参阅

* [Understanding the Query Execution Plan](/query-execution-plan.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
