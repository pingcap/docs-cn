---
title: KILL
summary: TiDB 数据库中 KILL 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-kill/','/docs-cn/dev/reference/sql/statements/kill/']
---

# KILL

`KILL` 语句可以终止当前 TiDB 集群中任意一个 TiDB 实例中的某个连接。

## 语法图

```ebnf+diagram
KillStmt ::= 'KILL' 'TIDB'? ( 'CONNECTION' | 'QUERY' )? CONNECTION_ID
```

## 示例

查询当前集群中所有活跃查询，并终止其中某一个连接：

{{< copyable "sql" >}}

```sql
SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST;
```

```
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
| ID                  | USER | INSTANCE        | INFO                                                                        |
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
| 8306449708033769879 | root | 127.0.0.1:10082 | select sleep(30), 'foo'                                                     |
| 5857102839209263511 | root | 127.0.0.1:10080 | select sleep(50)                                                            |
| 5857102839209263513 | root | 127.0.0.1:10080 | SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST |
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
```

{{< copyable "sql" >}}

```sql
KILL 5857102839209263511;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

- MySQL 的 `KILL` 语句仅能终止当前连接的 MySQL 实例上的连接，TiDB 的 `KILL` 语句能终止整个集群中任意一个 TiDB 实例上的连接。
- 暂时不支持使用 MySQL 命令行 <kbd>ctrl</kbd>+<kbd>c</kbd> 终止查询或连接。

## 行为变更说明

TiDB 从 v6.1.0 起新增 Global Kill 功能（由 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-从-v610-版本开始引入) 配置项控制，默认启用）。启用 Global Kill 功能时，`KILL` 语句和 `KILL TIDB` 语句均能跨节点终止查询或连接，且无需担心错误地终止其他查询或连接。当你使用客户端连接到任何一个 TiDB 节点执行 `KILL` 语句或 `KILL TIDB` 语句时，该语句会被转发给对应的 TiDB 节点。当客户端和 TiDB 中间有代理时，`KILL` 及 `KILL TIDB` 语句也会被转发给对应的 TiDB 节点执行。

对于 TiDB v6.1.0 之前的版本，或未启用 Global Kill 功能时：

- `KILL` 语句与 MySQL 不兼容，负载均衡器后面通常放有多个 TiDB 服务器，这种不兼容有助于防止在错误的 TiDB 服务器上终止连接。你需要显式地增加 `TIDB` 后缀，通过执行 `KILL TIDB` 语句来终止当前连接的 TiDB 实例上的其他连接。
- **强烈不建议**在配置文件里设置 [`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query)，**除非**你确定客户端将始终连接到同一个 TiDB 节点。这是因为当你在默认的 MySQL 客户端按下 <kbd>ctrl</kbd>+<kbd>c</kbd> 时，客户端会开启一个新连接，并在这个新连接中执行 `KILL` 语句。此时，如果客户端和 TiDB 中间有代理，新连接可能会被路由到其他的 TiDB 节点，从而错误地终止其他会话。
- `KILL TIDB` 语句是 TiDB 的扩展语法，其功能与 MySQL 命令 `KILL [CONNECTION|QUERY]` 和 MySQL 命令行 <kbd>ctrl</kbd>+<kbd>c</kbd> 相同。在同一个 TiDB 节点上，你可以安全地使用 `KILL TIDB` 语句。

## 另请参阅

- [SHOW \[FULL\] PROCESSLIST](/sql-statements/sql-statement-show-processlist.md)
- [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)