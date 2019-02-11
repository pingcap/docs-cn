---
title: 实用工具语句
category: user guide
---

# 实用工具语句

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

`EXPLAIN` 语句详细信息参考[理解 TiDB 执行计划](../sql/understanding-the-query-execution-plan.md)章节。

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

切换默认 Database，当 SQL 语句中的表没有显示指定 Database 时，即使用默认 Database。

## `TRACE` 语句

```sql
TRACE [FORMAT = format_name] traceable_stmt

format_name:
    "json" | "row"

traceable_stmt: {
    SELECT statement
  | DELETE statement
  | INSERT statement
  | REPLACE statement
  | UPDATE statement
}
```

```sql
mysql> trace format = 'row' select * from mysql.user;
+---------------------------|-----------------|------------+
| operation                 | startTS         | duration   |
+---------------------------|-----------------|------------+
| session.getTxnFuture      | 19:54:35.310841 | 4.255µs    |
|   ├─session.Execute       | 19:54:35.310837 | 928.349µs  |
|   ├─session.ParseSQL      | 19:54:35.310906 | 35.379µs   |
|   ├─executor.Compile      | 19:54:35.310972 | 420.688µs  |
|   ├─session.runStmt       | 19:54:35.311427 | 222.431µs  |
|   ├─session.CommitTxn     | 19:54:35.311601 | 14.696µs   |
|   ├─recordSet.Next        | 19:54:35.311828 | 419.797µs  |
|   ├─tableReader.Next      | 19:54:35.311834 | 379.932µs  |
|   ├─recordSet.Next        | 19:54:35.312310 | 26.831µs   |
|   └─tableReader.Next      | 19:54:35.312314 | 2.84µs     |
+---------------------------|-----------------|------------+
10 rows in set (0.00 sec)
```

当 format 为 json 时，输出是一段 json 格式的内容。如果长度过大，则输出会被换行。

输出的 json 内容可以在集成的 Web UI 里面查看，效果如下：

![](https://user-images.githubusercontent.com/1420062/48955365-8b82dc80-ef88-11e8-9ecb-22d0bcf565c3.gif)
