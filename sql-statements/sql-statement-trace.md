---
title: TRACE | TiDB SQL Statement Reference
summary: An overview of the usage of TRACE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-trace/','/docs/dev/reference/sql/statements/trace/']
---

# TRACE

The `TRACE` statement provides detailed information about query execution. It is intended to be viewed through a Graphical interface exposed by the TiDB server's status port.

## Synopsis

**TraceStmt:**

![TraceStmt](/media/sqlgram/TraceStmt.png)

**TraceableStmt:**

![TraceableStmt](/media/sqlgram/TraceableStmt.png)

## Examples

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

The JSON formatted trace can be pasted into the trace viewer, which is accessed via the TiDB status port:

![TiDB Trace Viewer-1](/media/trace-paste.png)

![TiDB Trace Viewer-2](/media/trace-view.png)

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
