---
title: TRACE | TiDB SQL Statement Reference 
summary: An overview of the usage of TRACE for the TiDB database.
category: reference
---

# TRACE

The `TRACE` statement provides detailed information about query execution. It is intended to be viewed through a Graphical interface exposed by the TiDB server's status port.

## Synopsis

**TraceStmt:**

![TraceStmt](/media/sqlgram/TraceStmt.png)

**TraceableStmt:**

![TraceableStmt](/media/sqlgram/TraceableStmt.png)


## Examples

```sql
mysql> trace format='row' select * from mysql.user;
+---------------------------+-----------------+------------+
| operation                 | startTS         | duration   |
+---------------------------+-----------------+------------+
| session.getTxnFuture      | 10:33:34.647148 | 3.847µs    |
|   ├─session.Execute       | 10:33:34.647146 | 536.233µs  |
|   ├─session.ParseSQL      | 10:33:34.647182 | 19.868µs   |
|   ├─executor.Compile      | 10:33:34.647219 | 295.688µs  |
|   ├─session.runStmt       | 10:33:34.647533 | 116.229µs  |
|   ├─session.CommitTxn     | 10:33:34.647631 | 5.44µs     |
|   ├─recordSet.Next        | 10:33:34.647707 | 833.103µs  |
|   ├─tableReader.Next      | 10:33:34.647709 | 806.783µs  |
|   ├─recordSet.Next        | 10:33:34.648572 | 19.367µs   |
|   └─tableReader.Next      | 10:33:34.648575 | 1.783µs    |
+---------------------------+-----------------+------------+
10 rows in set (0.00 sec)

mysql> CREATE TABLE t1 (id int not null primary key auto_increment);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> TRACE FORMAT='json' SELECT * FROM t1 WHERE id = 2\G
*************************** 1. row ***************************
operation: [{"ID":{"Trace":"60d20d005593de87","Span":"44e5b309242ffe2f","Parent":"79d146dac9a29a7e"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5nZXRUeG5GdXR1cmU="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE2MTQ3ODYtMDY6MDA="},{"Key":"Span.End","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE2MjA0MDYtMDY6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":[{"ID":{"Trace":"60d20d005593de87","Span":"4dbf8f2ca373b4b0","Parent":"79d146dac9a29a7e"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5QYXJzZVNRTA=="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE2NjE1MTQtMDY6MDA="},{"Key":"Span.End","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE3MDYxNjgtMDY6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"60d20d005593de87","Span":"6b6d6916df809604","Parent":"79d146dac9a29a7e"},"Annotations":[{"Key":"Name","Value":"ZXhlY3V0b3IuQ29tcGlsZQ=="},{"Key":"_schema:name","Value":null},{"Key":"Span.End","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE3NTcyODUtMDY6MDA="},{"Key":"Span.Start","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE3MzE0MjYtMDY6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"60d20d005593de87","Span":"3f1bcdd402a72911","Parent":"79d146dac9a29a7e"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5Db21taXRUeG4="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE3OTgyNjItMDY6MDA="},{"Key":"Span.End","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE4MDU1NzYtMDY6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"60d20d005593de87","Span":"58c1f7d66dc5afbc","Parent":"79d146dac9a29a7e"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5ydW5TdG10"},{"Key":"_schema:name","Value":null},{"Key":"Msg","Value":"eyJzcWwiOiJTRUxFQ1QgKiBGUk9NIHQxIFdIRVJFIGlkID0gMiJ9"},{"Key":"Time","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE3ODA1NjgtMDY6MDA="},{"Key":"_schema:log","Value":null},{"Key":"Span.End","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE4MTk5MzMtMDY6MDA="},{"Key":"Span.Start","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE3NzcyNDItMDY6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"60d20d005593de87","Span":"6bd8cc440fb31ed7","Parent":"79d146dac9a29a7e"},"Annotations":[{"Key":"Name","Value":"c2Vzc2lvbi5FeGVjdXRl"},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE2MTEwODktMDY6MDA="},{"Key":"Span.End","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE4NTU0My0wNjowMA=="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"60d20d005593de87","Span":"61d0b809f6cc018b","Parent":"79d146dac9a29a7e"},"Annotations":[{"Key":"Name","Value":"cmVjb3JkU2V0Lk5leHQ="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDE4NzQ1NTYtMDY6MDA="},{"Key":"Span.End","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDIyOTg4NjYtMDY6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null},{"ID":{"Trace":"60d20d005593de87","Span":"2bd2c3d47ccb1133","Parent":"79d146dac9a29a7e"},"Annotations":[{"Key":"Name","Value":"cmVjb3JkU2V0Lk5leHQ="},{"Key":"_schema:name","Value":null},{"Key":"Span.Start","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDIzMjY0ODgtMDY6MDA="},{"Key":"Span.End","Value":"MjAxOS0wNC0xN1QxMDozOToxMC45NDIzMjkwMDMtMDY6MDA="},{"Key":"_schema:Timespan","Value":null}],"Sub":null}]}]
1 row in set (0.00 sec)
```

The JSON formatted trace can be pasted into the trace viewer, which is accessed via the TiDB status port:

![TiDB Trace Viewer-1](/media/trace-paste.png)

![TiDB Trace Viewer-2](/media/trace-view.png)


## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [EXPLAIN ANALYZE](/dev/reference/sql/statements/explain-analyze.md)
