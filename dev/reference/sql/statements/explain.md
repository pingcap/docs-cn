---
title: EXPLAIN
summary: TiDB 数据库中 EXPLAIN 的使用概况。
category: reference
---

# EXPLAIN

`EXPLAIN` 语句仅用于显示查询的执行计划，而不执行查询。`EXPLAIN ANALYZE` 可执行查询，补充 `EXPLAIN` 语句。如果 `EXPLAIN` 的输出与预期结果不匹配，可考虑在查询的每个表上执行 `ANALYZE TABLE`。

语句 `DESC` 和 `DESCRIBE` 是 `EXPLAIN` 的别名。`EXPLAIN <tableName>` 的替代用法记录在 [`SHOW [FULL] COLUMNS FROM`](dev/reference/sql/statements/show-columns-from.md) 下。

## 语法图

**ExplainSym:**

![ExplainSym](/media/sqlgram/ExplainSym.png)

**ExplainStmt:**

![ExplainStmt](/media/sqlgram/ExplainStmt.png)

**ExplainableStmt:**

![ExplainableStmt](/media/sqlgram/ExplainableStmt.png)

## 示例

```sql
mysql> EXPLAIN SELECT 1;
+-------------------+-------+------+---------------+
| id                | count | task | operator info |
+-------------------+-------+------+---------------+
| Projection_3      | 1.00  | root | 1             |
| └─TableDual_4     | 1.00  | root | rows:1        |
+-------------------+-------+------+---------------+
2 rows in set (0.00 sec)

mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 (c1) VALUES (1), (2), (3);
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE id = 1;
+-------------+-------+------+--------------------+
| id          | count | task | operator info      |
+-------------+-------+------+--------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 |
+-------------+-------+------+--------------------+
1 row in set (0.00 sec)

mysql> DESC SELECT * FROM t1 WHERE id = 1;
+-------------+-------+------+--------------------+
| id          | count | task | operator info      |
+-------------+-------+------+--------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 |
+-------------+-------+------+--------------------+
1 row in set (0.00 sec)

mysql> DESCRIBE SELECT * FROM t1 WHERE id = 1;
+-------------+-------+------+--------------------+
| id          | count | task | operator info      |
+-------------+-------+------+--------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 |
+-------------+-------+------+--------------------+
1 row in set (0.00 sec)

mysql> EXPLAIN INSERT INTO t1 (c1) VALUES (4);
ERROR 1105 (HY000): Unsupported type *core.Insert

mysql> EXPLAIN UPDATE t1 SET c1=5 WHERE c1=3;
+---------------------+----------+------+-------------------------------------------------------------+
| id                  | count    | task | operator info                                               |
+---------------------+----------+------+-------------------------------------------------------------+
| TableReader_6       | 10.00    | root | data:Selection_5                                            |
| └─Selection_5       | 10.00    | cop  | eq(test.t1.c1, 3)                                           |
|   └─TableScan_4     | 10000.00 | cop  | table:t1, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+-------------------------------------------------------------+
3 rows in set (0.00 sec)

mysql> EXPLAIN DELETE FROM t1 WHERE c1=3;
+---------------------+----------+------+-------------------------------------------------------------+
| id                  | count    | task | operator info                                               |
+---------------------+----------+------+-------------------------------------------------------------+
| TableReader_6       | 10.00    | root | data:Selection_5                                            |
| └─Selection_5       | 10.00    | cop  | eq(test.t1.c1, 3)                                           |
|   └─TableScan_4     | 10000.00 | cop  | table:t1, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+-------------------------------------------------------------+
3 rows in set (0.00 sec)
```

如果未指定 `FORMAT`，或未指定 `FORMAT ="row"`，那么 `EXPLAIN` 语句将以表格格式输出结果。更多信息，可参阅 [Understand the Query Execution Plan](https://pingcap.com/docs/dev/reference/performance/understanding-the-query-execution-plan/)。

除 MySQL 标准结果格式外，TiDB 还支持 DotGraph。需按照下列所示指定 `FORMAT ="dot"`：

```sql
create table t(a bigint, b bigint);
desc format = "dot" select A.a, B.b from t A join t B on A.a > B.b where A.a < 10;

TiDB > desc format = "dot" select A.a, B.b from t A join t B on A.a > B.b where A.a < 10;desc format = "dot" select A.a, B.b from t A join t B on A.a > B.b where A.a < 10;
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| dot contents                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|
digraph HashRightJoin_7 {
subgraph cluster7{
node [style=filled, color=lightgrey]
color=black
label = "root"
"HashRightJoin_7" -> "TableReader_10"
"HashRightJoin_7" -> "TableReader_12"
}
subgraph cluster9{
node [style=filled, color=lightgrey]
color=black
label = "cop"
"Selection_9" -> "TableScan_8"
}
subgraph cluster11{
node [style=filled, color=lightgrey]
color=black
label = "cop"
"TableScan_11"
}
"TableReader_10" -> "Selection_9"
"TableReader_12" -> "TableScan_11"
}
 |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

如果你的计算机上安装了 `dot` 程序（在 `graphviz` 包中），可使用以下方法生成 PNG 文件：

```bash
dot xx.dot -T png -O

The xx.dot is the result returned by the above statement.
```

如果你的计算机上未安装 `dot` 程序，可将结果复制到 [本网站](http://www.webgraphviz.com/) 以获取树形图：

![Explain Dot](/media/explain_dot.png)

## MySQL 兼容性

* `EXPLAIN` 的格式和 TiDB 中潜在的执行计划都与 MySQL 有很大不同。
* TiDB 不像 MySQL 那样支持 `EXPLAIN FORMAT = JSON`。
* TiDB 目前不支持插入语句的 `EXPLAIN`。

## 另请参阅

* [Understanding the Query Execution Plan](dev/reference/performance/understanding-the-query-execution-plan.md)
* [EXPLAIN ANALYZE](dev/reference/sql/statements/explain-analyze.md)
* [ANALYZE TABLE](dev/reference/sql/statements/analyze-table.md)
* [TRACE](dev/reference/sql/statements/trace.md)
