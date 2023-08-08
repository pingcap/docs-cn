---
title: TRACE
summary: TiDB 数据库中 TRACE 的使用概况。
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
trace format='json' select * from mysql.user;
```

可将 JSON 格式的跟踪文件粘贴到跟踪查看器中。查看器可通过 TiDB 状态端口访问：

![TiDB Trace Viewer-1](/media/trace-paste.png)

![TiDB Trace Viewer-2](/media/trace-view.png)

## MySQL 兼容性

`TRACE` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
