---
title: EXPLAIN
summary: TiDB 数据库中 EXPLAIN 的使用概况。
---

# EXPLAIN

`EXPLAIN` 语句仅用于显示查询的执行计划，而不执行查询。`EXPLAIN ANALYZE` 可执行查询，补充 `EXPLAIN` 语句。如果 `EXPLAIN` 的输出与预期结果不匹配，可考虑在查询的每个表上执行 `ANALYZE TABLE`。

语句 `DESC` 和 `DESCRIBE` 是 `EXPLAIN` 的别名。`EXPLAIN <tableName>` 的替代用法记录在 [`SHOW [FULL] COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md) 下。

TiDB 支持 `EXPLAIN [options] FOR CONNECTION connection_id`，但与 MySQL 的 `EXPLAIN FOR` 有一些区别，请参见 [`EXPLAIN FOR CONNECTION`](#explain-for-connection)。

## 语法图

```ebnf+diagram
ExplainSym ::=
    'EXPLAIN'
|   'DESCRIBE'
|   'DESC'

ExplainStmt ::=
    ExplainSym ( TableName ColumnName? | 'ANALYZE'? ExplainableStmt | 'FOR' 'CONNECTION' NUM | 'FORMAT' '=' ( stringLit | ExplainFormatType ) ( 'FOR' 'CONNECTION' NUM | ExplainableStmt ) )

ExplainableStmt ::=
    SelectStmt
|   DeleteFromStmt
|   UpdateStmt
|   InsertIntoStmt
|   ReplaceIntoStmt
|   UnionStmt
```

## EXPLAIN 输出格式

> **注意：**
>
> 使用 MySQL 客户端连接到 TiDB 时，为避免输出结果在终端中换行，可先执行 `pager less -S` 命令。执行命令后，新的 `EXPLAIN` 的输出结果不再换行，可按右箭头 <kbd>→</kbd> 键水平滚动阅读输出结果。

目前 TiDB 的 `EXPLAIN` 会输出 5 列，分别是：`id`，`estRows`，`task`，`access object`，`operator info`。执行计划中每个算子都由这 5 列属性来描述，`EXPLAIN` 结果中每一行描述一个算子。每个属性的具体含义如下：

| 属性名          | 含义 |
|:----------------|:----------------------------------------------------------------------------------------------------------|
| id            | 算子的 ID，是算子在整个执行计划中唯一的标识。在 TiDB 2.1 中，ID 会格式化地显示算子的树状结构。数据从孩子结点流向父亲结点，每个算子的父亲结点有且仅有一个。|
| estRows       | 算子预计将会输出的数据条数，基于统计信息以及算子的执行逻辑估算而来。在 4.0 之前叫 count。 |
| task          | 算子属于的 task 种类。目前的执行计划分成为两种 task，一种叫 **root** task，在 tidb-server 上执行，一种叫 **cop** task，在 TiKV 或者 TiFlash 上并行执行。当前的执行计划在 task 级别的拓扑关系是一个 root task 后面可以跟许多 cop task，root task 使用 cop task 的输出结果作为输入。cop task 中执行的也即是 TiDB 下推到 TiKV 或者 TiFlash 上的任务，每个 cop task 分散在 TiKV 或者 TiFlash 集群中，由多个进程共同执行。 |
| access object | 算子所访问的数据项信息。包括表 `table`，表分区 `partition` 以及使用的索引 `index`（如果有）。只有直接访问数据的算子才拥有这些信息。 |
| operator info | 算子的其它信息。各个算子的 operator info 各有不同，可参考下面的示例解读。 |

## 示例

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT 1;
```

```
+-------------------+---------+------+---------------+---------------+
| id                | estRows | task | access object | operator info |
+-------------------+---------+------+---------------+---------------+
| Projection_3      | 1.00    | root |               | 1->Column#1   |
| └─TableDual_4     | 1.00    | root |               | rows:1        |
+-------------------+---------+------+---------------+---------------+
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
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1      |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DESC SELECT * FROM t1 WHERE id = 1;
```

```
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1      |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DESCRIBE SELECT * FROM t1 WHERE id = 1;
```

```
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1      |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN INSERT INTO t1 (c1) VALUES (4);
```

```
+----------+---------+------+---------------+---------------+
| id       | estRows | task | access object | operator info |
+----------+---------+------+---------------+---------------+
| Insert_1 | N/A     | root |               | N/A           |
+----------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN UPDATE t1 SET c1=5 WHERE c1=3;
```

```
+---------------------------+---------+-----------+---------------+--------------------------------+
| id                        | estRows | task      | access object | operator info                  |
+---------------------------+---------+-----------+---------------+--------------------------------+
| Update_4                  | N/A     | root      |               | N/A                            |
| └─TableReader_8           | 0.00    | root      |               | data:Selection_7               |
|   └─Selection_7           | 0.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|     └─TableFullScan_6     | 3.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+---------------------------+---------+-----------+---------------+--------------------------------+
4 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN DELETE FROM t1 WHERE c1=3;
```

```
+---------------------------+---------+-----------+---------------+--------------------------------+
| id                        | estRows | task      | access object | operator info                  |
+---------------------------+---------+-----------+---------------+--------------------------------+
| Delete_4                  | N/A     | root      |               | N/A                            |
| └─TableReader_8           | 0.00    | root      |               | data:Selection_7               |
|   └─Selection_7           | 0.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|     └─TableFullScan_6     | 3.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+---------------------------+---------+-----------+---------------+--------------------------------+
4 rows in set (0.01 sec)
```

如果未指定 `FORMAT`，或未指定 `FORMAT ="row"`，那么 `EXPLAIN` 语句将以表格格式输出结果。更多信息，可参阅 [Understand the Query Execution Plan](https://pingcap.com/docs/dev/reference/performance/understanding-the-query-execution-plan/)。

除 MySQL 标准结果格式外，TiDB 还支持 DotGraph。需按照下列所示指定 `FORMAT ="dot"`：

{{< copyable "sql" >}}

```sql
create table t(a bigint, b bigint);
desc format = "dot" select A.a, B.b from t A join t B on A.a > B.b where A.a < 10;
```

```
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| dot contents                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|
digraph Projection_8 {
subgraph cluster8{
node [style=filled, color=lightgrey]
color=black
label = "root"
"Projection_8" -> "HashJoin_9"
"HashJoin_9" -> "TableReader_13"
"HashJoin_9" -> "Selection_14"
"Selection_14" -> "TableReader_17"
}
subgraph cluster12{
node [style=filled, color=lightgrey]
color=black
label = "cop"
"Selection_12" -> "TableFullScan_11"
}
subgraph cluster16{
node [style=filled, color=lightgrey]
color=black
label = "cop"
"Selection_16" -> "TableFullScan_15"
}
"TableReader_13" -> "Selection_12"
"TableReader_17" -> "Selection_16"
}
 |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

如果你的计算机上安装了 `dot` 程序（在 `graphviz` 包中），可使用以下方法生成 PNG 文件：

{{< copyable "shell-regular" >}}

```bash
dot xx.dot -T png -O
```

The `xx.dot` is the result returned by the above statement.

如果你的计算机上未安装 `dot` 程序，可将结果复制到[本网站](http://www.webgraphviz.com/)以获取树形图：

![Explain Dot](/media/explain_dot.png)

## MySQL 兼容性

* `EXPLAIN` 的格式和 TiDB 中潜在的执行计划都与 MySQL 有很大不同。
* TiDB 不像 MySQL 那样支持 `EXPLAIN FORMAT = JSON`。
* TiDB 目前不支持插入语句的 `EXPLAIN`。

## `EXPLAIN FOR CONNECTION`

`EXPLAIN FOR CONNECTION` 用于获得一个连接中当前正在执行 SQL 的执行计划或者是最后执行 SQL 的执行计划，其输出格式与 `EXPLAIN` 完全一致。但 TiDB 中的实现与 MySQL 不同，除了输出格式之外，还有以下区别：

- MySQL 返回的是**正在执行**的查询计划，而 TiDB 返回的是**最后执行**的查询计划。
- MySQL 的文档中指出，MySQL 要求登录用户与被查询的连接相同，或者拥有 `PROCESS` 权限，而 TiDB 则要求登录用户与被查询的连接相同，或者拥有 `SUPER` 权限。

## 另请参阅

* [理解 TiDB 执行计划](/explain-overview.md)
* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
