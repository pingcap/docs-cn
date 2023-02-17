---
title: EXPLAIN
summary: TiDB 数据库中 EXPLAIN 的使用概况。
aliases: ['/docs-cn/v3.0/sql-statements/sql-statement-explain/','/docs-cn/v3.0/reference/sql/statements/explain/','/docs-cn/sql/util/']
---

# EXPLAIN

`EXPLAIN` 语句仅用于显示查询的执行计划，而不执行查询。`EXPLAIN ANALYZE` 可执行查询，补充 `EXPLAIN` 语句。如果 `EXPLAIN` 的输出与预期结果不匹配，可考虑在查询的每个表上执行 `ANALYZE TABLE`。

语句 `DESC` 和 `DESCRIBE` 是 `EXPLAIN` 的别名。`EXPLAIN <tableName>` 的替代用法记录在 [`SHOW [FULL] COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md) 下。

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
EXPLAIN SELECT 1;
```

```
+-------------------+-------+------+---------------+
| id                | count | task | operator info |
+-------------------+-------+------+---------------+
| Projection_3      | 1.00  | root | 1             |
| └─TableDual_4     | 1.00  | root | rows:1        |
+-------------------+-------+------+---------------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.10 sec)
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
EXPLAIN SELECT * FROM t1 WHERE id = 1;
```

```
+-------------+-------+------+--------------------+
| id          | count | task | operator info      |
+-------------+-------+------+--------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 |
+-------------+-------+------+--------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DESC SELECT * FROM t1 WHERE id = 1;
```

```
+-------------+-------+------+--------------------+
| id          | count | task | operator info      |
+-------------+-------+------+--------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 |
+-------------+-------+------+--------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DESCRIBE SELECT * FROM t1 WHERE id = 1;
```

```
+-------------+-------+------+--------------------+
| id          | count | task | operator info      |
+-------------+-------+------+--------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 |
+-------------+-------+------+--------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN INSERT INTO t1 (c1) VALUES (4);
```

```
ERROR 1105 (HY000): Unsupported type *core.Insert
```

{{< copyable "sql" >}}

```sql
EXPLAIN UPDATE t1 SET c1=5 WHERE c1=3;
```

```
+---------------------+----------+------+-------------------------------------------------------------+
| id                  | count    | task | operator info                                               |
+---------------------+----------+------+-------------------------------------------------------------+
| TableReader_6       | 10.00    | root | data:Selection_5                                            |
| └─Selection_5       | 10.00    | cop  | eq(test.t1.c1, 3)                                           |
|   └─TableScan_4     | 10000.00 | cop  | table:t1, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+-------------------------------------------------------------+
3 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN DELETE FROM t1 WHERE c1=3;
```

```
+---------------------+----------+------+-------------------------------------------------------------+
| id                  | count    | task | operator info                                               |
+---------------------+----------+------+-------------------------------------------------------------+
| TableReader_6       | 10.00    | root | data:Selection_5                                            |
| └─Selection_5       | 10.00    | cop  | eq(test.t1.c1, 3)                                           |
|   └─TableScan_4     | 10000.00 | cop  | table:t1, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+-------------------------------------------------------------+
3 rows in set (0.00 sec)
```

如果未指定 `FORMAT`，或未指定 `FORMAT ="row"`，那么 `EXPLAIN` 语句将以表格格式输出结果。更多信息，可参阅 [Understand the Query Execution Plan](https://pingcap.com/docs/v3.0/reference/performance/understanding-the-query-execution-plan/)。

除 MySQL 标准结果格式外，TiDB 还支持 DotGraph。需按照下列所示指定 `FORMAT ="dot"`：

{{< copyable "sql" >}}

```sql
create table t(a bigint, b bigint);
desc format = "dot" select A.a, B.b from t A join t B on A.a > B.b where A.a < 10;
```

```+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
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

{{< copyable "shell-regular" >}}

```bash
dot xx.dot -T png -O
```

The `xx.dot` is the result returned by the above statement.

如果你的计算机上未安装 `dot` 程序，可将结果复制到 [本网站](http://www.webgraphviz.com/) 以获取树形图：

![Explain Dot](/media/explain_dot.png)

## MySQL 兼容性

* `EXPLAIN` 的格式和 TiDB 中潜在的执行计划都与 MySQL 有很大不同。
<<<<<<< HEAD
* TiDB 不像 MySQL 那样支持 `EXPLAIN FORMAT = JSON`。
* TiDB 目前不支持插入语句的 `EXPLAIN`。
=======
* TiDB 不支持 `FORMAT=JSON` 或 `FORMAT=TREE` 选项。
* TiDB 支持的 `FORMAT=tidb_json` 是对当前默认 `EXPLAIN` 格式的 JSON 编码，与 MySQL 的 `FORMAT=JSON` 结果的格式、字段信息都不同。

## `EXPLAIN FOR CONNECTION`

`EXPLAIN FOR CONNECTION` 用于获得一个连接中当前正在执行 SQL 的执行计划或者是最后执行 SQL 的执行计划，其输出格式与 `EXPLAIN` 完全一致。但 TiDB 中的实现与 MySQL 不同，除了输出格式之外，还有以下区别：

- 如果连接处于睡眠状态，MySQL 返回为空，而 TiDB 返回的是最后执行的查询计划。
- 如果获取当前会话连接的执行计划，MySQL 会报错，而 TiDB 会正常返回。
- MySQL 的文档中指出，MySQL 要求登录用户与被查询的连接相同，或者拥有 `PROCESS` 权限，而 TiDB 则要求登录用户与被查询的连接相同，或者拥有 `SUPER` 权限。
>>>>>>> e5cdb970e (explain for connection: fix the compatibility with MySQL (#13045))

## 另请参阅

* [Understanding the Query Execution Plan](/query-execution-plan.md)
* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
