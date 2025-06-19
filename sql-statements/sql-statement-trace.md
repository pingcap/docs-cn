---
title: TRACE | TiDB SQL 语句参考
summary: TiDB 数据库中 TRACE 的使用概述。
---

# TRACE

`TRACE` 语句提供查询执行的详细信息。它旨在通过 TiDB 服务器状态端口暴露的图形界面进行查看。

## 语法

```ebnf+diagram
TraceStmt ::=
    "TRACE" ( "FORMAT" "=" stringLit )? TracableStmt

TracableStmt ::=
    ( SelectStmt | DeleteFromStmt | UpdateStmt | InsertIntoStmt | ReplaceIntoStmt | UnionStmt | LoadDataStmt | BeginTransactionStmt | CommitStmt | RollbackStmt | SetStmt )
```

| 格式 | 描述 |
|--------|------------------------------------|
| row    | 以树形格式输出 |
| json   | 以 JSON 格式结构化输出 |
| log    | 基于日志的输出 |

## 示例

### Row

```sql
TRACE FORMAT='row' SELECT * FROM mysql.user;
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

### JSON

```sql
TRACE FORMAT='json' SELECT * FROM mysql.user;
```

JSON 格式的跟踪信息可以粘贴到跟踪查看器中，该查看器可通过 TiDB 状态端口访问：

![TiDB Trace Viewer-1](/media/trace-paste.png)

![TiDB Trace Viewer-2](/media/trace-view.png)

### Log

```sql
TRACE FORMAT='log' SELECT * FROM mysql.user;
```

```
+----------------------------+--------------------------------------------------------+------+------------------------------------+
| time                       | event                                                  | tags | spanName                           |
+----------------------------+--------------------------------------------------------+------+------------------------------------+
| 2024-04-08 08:41:47.358734 | --- start span trace ----                              |      | trace                              |
| 2024-04-08 08:41:47.358737 | --- start span session.ExecuteStmt ----                |      | session.ExecuteStmt                |
| 2024-04-08 08:41:47.358746 | --- start span executor.Compile ----                   |      | executor.Compile                   |
| 2024-04-08 08:41:47.358984 | --- start span session.runStmt ----                    |      | session.runStmt                    |
| 2024-04-08 08:41:47.359035 | --- start span TableReaderExecutor.Open ----           |      | TableReaderExecutor.Open           |
| 2024-04-08 08:41:47.359047 | --- start span distsql.Select ----                     |      | distsql.Select                     |
| 2024-04-08 08:41:47.359073 | --- start span *executor.TableReaderExecutor.Next ---- |      | *executor.TableReaderExecutor.Next |
| 2024-04-08 08:41:47.359077 | table scan table: user, range: [[-inf,+inf]]           |      | *executor.TableReaderExecutor.Next |
| 2024-04-08 08:41:47.359094 | --- start span regionRequest.SendReqCtx ----           |      | regionRequest.SendReqCtx           |
| 2024-04-08 08:41:47.359098 | send Cop request to region 16 at store1                |      | regionRequest.SendReqCtx           |
| 2024-04-08 08:41:47.359237 | --- start span *executor.TableReaderExecutor.Next ---- |      | *executor.TableReaderExecutor.Next |
| 2024-04-08 08:41:47.359240 | table scan table: user, range: [[-inf,+inf]]           |      | *executor.TableReaderExecutor.Next |
| 2024-04-08 08:41:47.359242 | execute done, ReturnRow: 1, ModifyRow: 0               |      | trace                              |
| 2024-04-08 08:41:47.359252 | execute done, modify row: 0                            |      | trace                              |
+----------------------------+--------------------------------------------------------+------+------------------------------------+
14 rows in set (0.0008 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
