---
title: SHOW [FULL] PROCESSLIST
summary: TiDB 数据库中 SHOW [FULL] PROCESSLIST 的使用概况。
---

# SHOW [FULL] PROCESSLIST

`SHOW [FULL] PROCESSLIST` 语句列出连接到相同 TiDB 服务器的当前会话。

## 语法图

```ebnf+diagram
ShowProcesslistStmt ::=
    "SHOW" "FULL"? "PROCESSLIST"
```

## 示例

```sql
SHOW PROCESSLIST;
```

```sql
+------+------+-----------------+------+---------+------+------------+------------------+
| Id   | User | Host            | db   | Command | Time | State      | Info             |
+------+------+-----------------+------+---------+------+------------+------------------+
|    5 | root | 127.0.0.1:45970 | test | Query   |    0 | autocommit | SHOW PROCESSLIST |
+------+------+-----------------+------+---------+------+------------+------------------+
1 rows in set (0.00 sec)
```

以上返回结果中的主要字段描述如下：

- `Command`：SQL 语句的类型，通常值为 `Query`。
- `Time`：SQL 语句开始执行的时间。
- `State`：SQL 语句的状态。常见的值是 `autocommit`，表示该 SQL 语句是自动提交的。`in transaction` 表示该 SQL 语句处于事务中。
- `Info`：表示具体的 SQL 文本。除非指定可选关键字 `FULL`，否则文本会被截断。

## MySQL 兼容性

* TiDB 中的 `State` 列是非描述性的。在 TiDB 中，将状态表示为单个值更复杂，因为查询是并行执行的，而且每个 Go 线程在任一时刻都有不同的状态。

## 另请参阅

* [KILL \[TIDB\]](/sql-statements/sql-statement-kill.md)
* [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)
