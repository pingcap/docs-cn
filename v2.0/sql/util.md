---
title: 实用工具语句
category: user guide
---

## `DESCRIBE` 语句

`DESCRIBE` 和 `EXPLAIN` 是同义词，另外还可以缩写为 `DESC`。请参考 `EXPLAIN` 语句的用法。

## `EXPLAIN` 语句

```sql
{EXPLAIN | DESCRIBE | DESC}
    tbl_name [col_name]

{EXPLAIN | DESCRIBE | DESC}
    [explain_type]
    explainable_stmt

explain_type:
    FORMAT = format_name

format_name:
    "DOT"

explainable_stmt: {
    SELECT statement
  | DELETE statement
  | INSERT statement
  | REPLACE statement
  | UPDATE statement
}
```

`EXPLAIN` 语句详细信息参考[理解 TiDB 执行计划](understanding-the-query-execution-plan.md)章节。

除了 MySQL 标准的结果格式之外，TiDB 还支持输出 DotGraph 结果，这时需要指定 `FORMAT = "dot"`，示例如下：

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

如果电脑上安装了 `dot` 程序 (包含在 graphviz 软件包中)，可以通过如下方式生成 PNG 文件：

```bash
dot xx.dot -T png -O

这里的 xx.dot 是上面的语句返回结果。
```

如果没有安装 `dot`，可以将结果拷贝到[这个网站](http://www.webgraphviz.com/)，可以得到一个树状图：

![Explain Dot](../media/explain_dot.png)

## `USE` 语句

```sql
USE db_name
```

切换需要使用的 Database 的时候，如果 SQL 语句中的表没有显式指定的 Database，即默认使用当前选定的 Database。
