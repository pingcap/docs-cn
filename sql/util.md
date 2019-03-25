---
title: Utility Statements
summary: Learn how to use the utility statements, including the `DESCRIBE`, `EXPLAIN`, and `USE` statements.
category: user guide
---

# Utility Statements

This document describes the utility statements, including the `DESCRIBE`, `EXPLAIN`, and `USE` statements.

## `DESCRIBE` statement

The `DESCRIBE` and `EXPLAIN` statements are synonyms, which can also be abbreviated as `DESC`. See the usage of the `EXPLAIN` statement.

## `EXPLAIN` statement

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

For more information about the `EXPLAIN` statement, see [Understand the Query Execution Plan](../sql/understanding-the-query-execution-plan.md).

In addition to the MySQL standard result format, TiDB also supports DotGraph and you need to specify `FORMAT = "dot"` as in the following example:

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

If the `dot` program (in the `graphviz` package) is installed on your computer, you can generate a PNG file using the following method:

```bash
dot xx.dot -T png -O

The xx.dot is the result returned by the above statement.
```

If the `dot` program is not installed on your computer, copy the result to [this website](http://www.webgraphviz.com/) to get a tree diagram:

![Explain Dot](../media/explain_dot.png)

## `USE` statement

```sql
USE db_name
```

The `USE` statement is used to switch the default database. If the table in this SQL statement does not correspond to an explicitly specified database, then the default database is used.

## `TRACE` statement

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

When the `format` is `json`, the output is some `json` text. If the text is too long, they are split into multiple lines.

A visualization of the `json` output can be accessed via the `tidb-server` status and metrics port (default: `:10080`). Here is a demo:

```sql
mysql> trace format='json' select * from  t\G;
*************************** 1. row ***************************
operation: [{"ID":{"Trace":"22a6ccdaf58481ea","Span":"4f29711d1db208b4","Parent":"64aa858bd66f5c65"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5nZXRUeG5GdXR1cmU="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDQ5NDc1MTgrMDg6MDA="},{"Key":"Span.End","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDQ5NTI1MDYrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":[{"ID":{"Trace":"22a6ccdaf58481ea","Span":"5a1f3a948a72ff6f","Parent":"64aa858bd66f5c65"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5QYXJzZVNRTA=="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDUwMTc3MzgrMDg6MDA="},{"Key":"Span.End","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDUwNTczNzQrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"22a6ccdaf58481ea","Span":"1252ea914624eff1","Parent":"64aa858bd66f5c65"},"Annotations":[{"Key":"Name","Value":"ZXhlY3V0b3IuQ29tcGlsZQ=="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDUxMTc3NzQrMDg6MDA="},{"Key":"Span.End","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDUzNzMwNjIrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"22a6ccdaf58481ea","Span":"1a32f23071104f0d","Parent":"64aa858bd66f5c65"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5Db21taXRUeG4="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDU1NzIyMTkrMDg6MDA="},{"Key":"Span.End","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDU1ODY4MDIrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"22a6ccdaf58481ea","Span":"1a253a1a7e9513ca","Parent":"64aa858bd66f5c65"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5ydW5TdG10"},{"Key":"_schema:name","Value":null},{"Key":"Msg","Value":"eyJzcWwiOiJzZWxlY3QgKiBmcm9tICB0In0="},{"Key":"Time","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDU0MTkxOCswODowMA=="},{"Key":"_schema:log","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDU0MTMxMTcrMDg6MDA="},{"Key":"Span.End","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDU2MjE1MjgrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"22a6ccdaf58481ea","Span":"0db4399b79ba58c5","Parent":"64aa858bd66f5c65"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5FeGVjdXRl"},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDQ5NDI4MSswODowMA=="},{"Key":"Span.End","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDU2OTcwMzcrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"22a6ccdaf58481ea","Span":"5fb58dc2f1f6273a","Parent":"64aa858bd66f5c65"},"Annotations":[{"Key":"Name","Value":"dGFibGVSZWFkZXIuTmV4dA=="},{"Key":"_schema:name","Value":null},{"Key":"Span.End","Value":"MjAxOS0wMy0yMFQxNjoxMDo1NC4xODIxODMxODIrMDg6MDA="},{"Key":"Span.Start","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDU3NTM5ODYrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"22a6ccdaf58481ea","Span":"4c4ceeeeba9bb2eb","Parent":"64aa858bd66f5c65"},"Annotations":[{"Key":"Name","Value":"cmVjb3JkU2V0Lk5leHQ="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wMy0yMFQxNjoxMDo1My4yNDU3NDc0NjMrMDg6MDA="},{"Key":"Span.End","Value":"MjAxOS0wMy0yMFQxNjoxMDo1NC4xODIyMDUyNTUrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null}]}]
1 row in set (0.93 sec)
```

Open the "trace viewer" page, fill the `json` output.

![TiDB Trace Viewer-1](../media/tidb-trace-viewer.png)

![TiDB Trace Viewer-2](../media/tidb-trace-viewer-2.png)
