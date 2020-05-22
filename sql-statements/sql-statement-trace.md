---
title: TRACE
summary: TiDB 数据库中 TRACE 的使用概况。
category: reference
aliases: ['/docs-cn/dev/reference/sql/statements/trace/']
---

# TRACE

`TRACE` 语句用于提供查询执行的详细信息，可通过 TiDB 服务器状态端口所公开的图形界面进行查看。

## 语法图

**TraceStmt:**

![TraceStmt](/media/sqlgram/TraceStmt.png)

**TraceableStmt:**

![TraceableStmt](/media/sqlgram/TraceableStmt.png)

## 示例

{{< copyable "sql" >}}

```sql
trace format='row' select * from mysql.user;
```

```
+--------------------------------------------+-----------------+------------+
| operation                                  | startTS         | duration   |
+--------------------------------------------+-----------------+------------+
| trace                                      | 17:03:31.938237 | 886.086µs  |
|   ├─session.Execute                        | 17:03:31.938247 | 507.812µs  |
|   │ ├─session.ParseSQL                     | 17:03:31.938254 | 22.504µs   |
|   │ ├─executor.Compile                     | 17:03:31.938321 | 278.931µs  |
|   │ │ └─session.getTxnFuture               | 17:03:31.938337 | 1.515µs    |
|   │ └─session.runStmt                      | 17:03:31.938613 | 109.578µs  |
|   │   ├─TableReaderExecutor.Open           | 17:03:31.938645 | 50.657µs   |
|   │   │ └─distsql.Select                   | 17:03:31.938666 | 21.066µs   |
|   │   │   └─RPCClient.SendRequest          | 17:03:31.938799 | 158.411µs  |
|   │   └─session.CommitTxn                  | 17:03:31.938705 | 12.06µs    |
|   │     └─session.doCommitWitRetry         | 17:03:31.938709 | 2.437µs    |
|   ├─*executor.TableReaderExecutor.Next     | 17:03:31.938781 | 224.327µs  |
|   └─*executor.TableReaderExecutor.Next     | 17:03:31.939019 | 6.266µs    |
+--------------------------------------------+-----------------+------------+
13 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
TRACE FORMAT='json' SELECT * FROM t1 WHERE id = 2;
```

```
operation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| [{"ID":{"Trace":"7f88549f606d5b72","Span":"0118ce7c10f368a0","Parent":"0000000000000000"},"Annotations":[{"Key":"Name","Value":"dHJhY2U="},{"Key":"_schema:name","Value":null},{"Key":"Msg","Value":"ZXhlY3V0ZSBkb25lLCBSZXR1cm5Sb3c6IDEsIE1vZGlmeVJvdzogMA=="},{"Key":"Time","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAxNzIrMDg6MDA="},{"Key":"_schema:log","Value":null},{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45Mjk5MDMrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAyMjM0MTMrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":[{"ID":{"Trace":"7f88549f606d5b72","Span":"1ce4df477db99315","Parent":"0118ce7c10f368a0"},"Annotations":[{"Key":"Name","Value":"KmV4ZWN1dG9yLlBvaW50R2V0RXhlY3V0b3IuTmV4dA=="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAwNTgrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAxNTU4MDIrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":[{"ID":{"Trace":"7f88549f606d5b72","Span":"2fad4bbd33b0e2fa","Parent":"1ce4df477db99315"},"Annotations":[{"Key":"Name","Value":"dGlrdlNuYXBzaG90LmdldA=="},{"Key":"_schema:name","Value":null},{"Key":"Msg","Value":"c2VuZCBHZXQgcmVxdWVzdCB0byByZWdpb24gNCBhdCBzdG9yZTE="},{"Key":"Time","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAwNzUrMDg6MDA="},{"Key":"_schema:log","Value":null},{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAwNjIrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAxNDQ5MTYrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":[{"ID":{"Trace":"7f88549f606d5b72","Span":"2ce7346e52341d99","Parent":"2fad4bbd33b0e2fa"},"Annotations":[{"Key":"Name","Value":"UlBDQ2xpZW50LlNlbmRSZXF1ZXN0"},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAwNzcrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAxMzYyNDErMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null}]}]},{"ID":{"Trace":"7f88549f606d5b72","Span":"0c78c3f1f83de3ed","Parent":"0118ce7c10f368a0"},"Annotations":[{"Key":"Name","Value":"KmV4ZWN1dG9yLlBvaW50R2V0RXhlY3V0b3IuTmV4dA=="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAxNjUrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAxNjU4MjUrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"7f88549f606d5b72","Span":"755fa921d354d231","Parent":"0118ce7c10f368a0"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5FeGVjdXRl"},{"Key":"_schema:name","Value":null},{"Key":"Msg","Value":"ZXhlY3V0ZTogU0VMRUNUICogRlJPTSB0MSBXSEVSRSBpZCA9IDI="},{"Key":"Time","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45Mjk5MTIrMDg6MDA="},{"Key":"_schema:log","Value":null},{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45Mjk5MDcrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAwNDM1NzErMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":[{"ID":{"Trace":"7f88549f606d5b72","Span":"606f9966437f529f","Parent":"755fa921d354d231"},"Annotations":[{"Key":"Name","Value":"ZXhlY3V0b3IuQ29tcGlsZQ=="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45Mjk5NTUrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45Mjk5NzU4MTgrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"7f88549f606d5b72","Span":"1b92d023e89e99c4","Parent":"755fa921d354d231"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5ydW5TdG10"},{"Key":"_schema:name","Value":null},{"Key":"Msg","Value":"eyJzcWwiOiJTRUxFQ1QgKiBGUk9NIHQxIFdIRVJFIGlkID0gMiJ9"},{"Key":"Time","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45Mjk5OSswODowMA=="},{"Key":"_schema:log","Value":null},{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45Mjk5ODgrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAwMjQyMDcrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":[{"ID":{"Trace":"7f88549f606d5b72","Span":"6a61f7ffdcbad0c4","Parent":"1b92d023e89e99c4"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5Db21taXRUeG4="},{"Key":"_schema:name","Value":null |
| },{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAwMDYrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAwMTg1MDIrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":[{"ID":{"Trace":"7f88549f606d5b72","Span":"52f0c4a81d7fe604","Parent":"6a61f7ffdcbad0c4"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5kb0NvbW1pdFdpdFJldHJ5"},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAwMDkrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45MzAwMTE1OSswODowMA=="},{"Key":"_schema:Timespan","Value":null}],"Sub":null}]}]},{"ID":{"Trace":"7f88549f606d5b72","Span":"66367e8aa80ff69b","Parent":"755fa921d354d231"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5QYXJzZVNRTA=="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45Mjk5MTQrMDg6MDA="},{"Key":"Span.End","Value":"MjAyMC0wNS0yMlQxNzowNzoxNi45Mjk5MzA1NjkrMDg6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null}]}]}]           |
1 row in set (0.00 sec)
```

可将 JSON 格式的跟踪文件粘贴到跟踪查看器中。查看器可通过 TiDB 状态端口访问：

![TiDB Trace Viewer-1](/media/trace-paste.png)

![TiDB Trace Viewer-2](/media/trace-view.png)

## MySQL 兼容性

`TRACE` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
