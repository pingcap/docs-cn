---
title: SHOW [FULL] PROCESSLIST | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW [FULL] PROCESSLIST 的使用概览。
---

# SHOW [FULL] PROCESSLIST

此语句列出连接到同一 TiDB 服务器的当前会话。`Info` 列包含查询文本，除非指定可选关键字 `FULL`，否则该文本将被截断。

## 语法

```ebnf+diagram
ShowProcesslistStmt ::=
    "SHOW" "FULL"? "PROCESSLIST"
```

## 示例

```sql
mysql> SHOW PROCESSLIST;
+------+------+-----------------+------+---------+------+------------+------------------+
| Id   | User | Host            | db   | Command | Time | State      | Info             |
+------+------+-----------------+------+---------+------+------------+------------------+
|    5 | root | 127.0.0.1:45970 | test | Query   |    0 | autocommit | SHOW PROCESSLIST |
+------+------+-----------------+------+---------+------+------------+------------------+
1 rows in set (0.00 sec)
```

## MySQL 兼容性

* TiDB 中的 `State` 列是非描述性的。在 TiDB 中将状态表示为单个值更复杂，因为查询是并行执行的，每个 goroutine 在任何时候都会有不同的状态。

## 另请参阅

* [KILL \[TIDB\]](/sql-statements/sql-statement-kill.md)
* [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)
