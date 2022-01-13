---
title: SHOW [FULL] PROCESSLIST
summary: TiDB 数据库中 SHOW [FULL] PROCESSLIST 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-processlist/','/docs-cn/dev/reference/sql/statements/show-processlist/']
---

# SHOW [FULL] PROCESSLIST

`SHOW [FULL] PROCESSLIST` 语句列出连接到相同 TiDB 服务器的当前会话。`Info` 列包含查询文本，除非指定可选关键字 `FULL`，否则文本会被截断。

## 语法图

**ShowProcesslistStmt:**

![ShowProcesslistStmt](/media/sqlgram/ShowProcesslistStmt.png)

**OptFull:**

![OptFull](/media/sqlgram/OptFull.png)

## 示例

{{< copyable "sql" >}}

```sql
SHOW PROCESSLIST;
```

```
+------+------+-----------------+------+---------+------+------------+------------------+
| Id   | User | Host            | db   | Command | Time | State      | Info             |
+------+------+-----------------+------+---------+------+------------+------------------+
|    5 | root | 127.0.0.1:45970 | test | Query   |    0 | autocommit | SHOW PROCESSLIST |
+------+------+-----------------+------+---------+------+------------+------------------+
1 rows in set (0.00 sec)
```

## MySQL 兼容性

* TiDB 中的 `State` 列是非描述性的。在 TiDB 中，将状态表示为单个值更复杂，因为查询是并行执行的，而且每个 Go 线程在任一时刻都有不同的状态。

## 另请参阅

* [KILL \[TIDB\]](/sql-statements/sql-statement-kill.md)
