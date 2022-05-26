---
title: KILL [TIDB]
summary: TiDB 数据库中 KILL [TIDB] 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-kill/','/docs-cn/dev/reference/sql/statements/kill/']
---

# KILL [TIDB]

`KILL TIDB` 语句用于终止 TiDB 中的连接。

## 语法图

```ebnf+diagram
KillStmt ::= KillOrKillTiDB ( 'CONNECTION' | 'QUERY' )? NUM

KillOrKillTiDB ::= 'KILL' 'TIDB'?
```

## 示例

{{< copyable "sql" >}}

```sql
SHOW PROCESSLIST;
```

```
+------+------+-----------+------+---------+------+-------+------------------+
| Id   | User | Host      | db   | Command | Time | State | Info             |
+------+------+-----------+------+---------+------+-------+------------------+
|    1 | root | 127.0.0.1 | test | Query   |    0 | 2     | SHOW PROCESSLIST |
|    2 | root | 127.0.0.1 |      | Sleep   |    4 | 2     |                  |
+------+------+-----------+------+---------+------+-------+------------------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
KILL TIDB 2;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

* 按照设计，`KILL` 语句默认与 MySQL 不兼容。负载均衡器后面通常放有多个 TiDB 服务器，这种默认不兼容有助于防止在错误的 TiDB 服务器上终止连接。
* 请**不要**在配置文件里设置 [`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query)，**除非**你确定客户端将始终连接到同一个 TiDB 节点。这是因为当你在默认的 MySQL 客户端按下 <kbd>ctrl</kbd>+<kbd>c</kbd> 时，客户端会开启一个新连接，并在这个新连接中执行 `KILL` 语句。此时，如果客户端和 TiDB 中间有代理，新连接可能会被路由到其他的 TiDB 节点，从而错误地终止其他会话。
* `KILL TIDB` 语句是 TiDB 的扩展语法，其功能与 MySQL 命令 `KILL [CONNECTION|QUERY]` 和 MySQL 命令行 <kbd>ctrl</kbd>+<kbd>c</kbd> 相同。在同一个 TiDB 节点上，你可以安全地使用 `KILL TIDB` 语句。
* TiDB 从 v6.1.0 起引入 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-从-v610-版本开始引入) 配置项，默认值为 `true`。当 `enable-global-kill` 为 `true` 时，`KILL` 语句和 `KILL TIDB` 语句均能跨节点终止查询或连接，无需担心错误地终止其他查询或连接。当你使用客户端连接到任何一个 TiDB 节点执行 `KILL` 语句或 `KILL TIDB` 语句时，该语句会被转发给对应的 TiDB 节点。当客户端和 TiDB 中间有代理时，`KILL` 语句或 `KILL TIDB` 语句也会被转发给对应的 TiDB 节点执行。目前暂时不支持在 `enable-global-kill` 为 `true` 时用 MySQL 命令行 <kbd>ctrl</kbd>+<kbd>c</kbd> 终止查询或连接。

## 另请参阅

* [SHOW \[FULL\] PROCESSLIST](/sql-statements/sql-statement-show-processlist.md)
* [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)
