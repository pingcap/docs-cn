---
title: KILL
summary: TiDB 数据库中 KILL 的使用概述。
---

# KILL

`KILL` 语句用于终止当前 TiDB 集群中任何 TiDB 实例的连接。从 TiDB v6.2.0 开始，你还可以使用 `KILL` 语句终止正在进行的 DDL 作业。

## 语法概要

```ebnf+diagram
KillStmt ::= 'KILL' 'TIDB'? ( 'CONNECTION' | 'QUERY' )? CONNECTION_ID
```

## 示例

以下示例展示如何获取当前集群中所有活跃查询并终止其中任意一个。

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

- MySQL 的 `KILL` 语句只能终止当前连接的 MySQL 实例中的连接，而 TiDB 的 `KILL` 语句可以终止整个集群中任何 TiDB 实例的连接。
- 在 v7.2.0 及更早版本中，不支持使用 MySQL 命令行的 <kbd>Control+C</kbd> 来终止 TiDB 中的查询或连接。

## 行为变更说明

<CustomContent platform="tidb">

从 v7.3.0 开始，TiDB 支持生成 32 位连接 ID，默认启用，由配置项 [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730) 控制。当 Global Kill 功能和 32 位连接 ID 都启用时，TiDB 生成 32 位连接 ID，你可以在 MySQL 命令行中使用 <kbd>Control+C</kbd> 终止查询或连接。

> **警告：**
>
> 当集群中 TiDB 实例数量超过 2048 个或单个 TiDB 实例并发连接数超过 1048576 时，32 位连接 ID 空间不足，会自动升级为 64 位连接 ID。升级过程中，现有业务和已建立的连接不受影响。但是，后续新建的连接将无法在 MySQL 命令行中使用 <kbd>Control+C</kbd> 终止。

从 v6.1.0 开始，TiDB 支持 Global Kill 功能，默认启用，由配置项 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) 控制。

</CustomContent>

<CustomContent platform="tidb-cloud">

从 v7.3.0 开始，TiDB 支持生成 32 位连接 ID，默认启用。当 Global Kill 功能和 32 位连接 ID 都启用时，你可以在 MySQL 命令行中使用 <kbd>Control+C</kbd> 终止查询或连接。

从 v6.1.0 开始，TiDB 支持 Global Kill 功能，默认启用。

</CustomContent>

当启用 Global Kill 功能时，`KILL` 和 `KILL TIDB` 语句都可以跨实例终止查询或连接，因此你无需担心错误终止查询或连接。当你使用客户端连接到任何 TiDB 实例并执行 `KILL` 或 `KILL TIDB` 语句时，该语句将被转发到目标 TiDB 实例。如果客户端和 TiDB 集群之间有代理，`KILL` 和 `KILL TIDB` 语句也会被转发到目标 TiDB 实例执行。

如果未启用 Global Kill 功能或你使用的 TiDB 版本早于 v6.1.0，请注意以下事项：

- 默认情况下，`KILL` 与 MySQL 不兼容。这有助于防止连接被错误的 TiDB 服务器终止，因为通常会在负载均衡器后面放置多个 TiDB 服务器。要终止当前连接的 TiDB 实例上的其他连接，你需要通过执行 `KILL TIDB` 语句显式添加 `TIDB` 后缀。

<CustomContent platform="tidb">

- **强烈不建议**在配置文件中设置 [`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query)，除非你确定客户端将始终连接到同一个 TiDB 实例。这是因为在默认 MySQL 客户端中按 <kbd>Control+C</kbd> 会打开一个新连接来执行 `KILL`。如果客户端和 TiDB 集群之间有代理，新连接可能会被路由到不同的 TiDB 实例，这可能会错误地终止不同的会话。

</CustomContent>

- `KILL TIDB` 语句是 TiDB 的扩展。此语句的功能类似于 MySQL 的 `KILL [CONNECTION|QUERY]` 命令和 MySQL 命令行的 <kbd>Control+C</kbd>。在同一个 TiDB 实例上使用 `KILL TIDB` 是安全的。

## 另请参阅

* [SHOW \[FULL\] PROCESSLIST](/sql-statements/sql-statement-show-processlist.md)
* [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)
