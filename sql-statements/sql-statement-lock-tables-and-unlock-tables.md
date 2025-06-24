---
title: LOCK TABLES 和 UNLOCK TABLES
summary: TiDB 数据库中 LOCK TABLES 和 UNLOCK TABLES 的使用概览。
---

# LOCK TABLES 和 UNLOCK TABLES

> **警告：**
>
> `LOCK TABLES` 和 `UNLOCK TABLES` 在当前版本中是实验性功能。不建议在生产环境中使用。

TiDB 允许客户端会话获取表锁，以便与其他会话协作访问表，或阻止其他会话修改表。一个会话只能为自己获取或释放锁。一个会话不能为另一个会话获取锁或释放另一个会话持有的锁。

`LOCK TABLES` 为当前客户端会话获取表锁。如果你对要锁定的每个对象都具有 `LOCK TABLES` 和 `SELECT` 权限，则可以为普通表获取表锁。

`UNLOCK TABLES` 显式释放当前会话持有的任何表锁。`LOCK TABLES` 在获取新锁之前会隐式释放当前会话持有的所有表锁。

表锁可以防止其他会话进行读取或写入。持有 `WRITE` 锁的会话可以执行表级操作，如 `DROP TABLE` 或 `TRUNCATE TABLE`。

> **注意：**
>
> 表锁功能默认是禁用的。
>
> - 对于 TiDB Self-Managed，要启用表锁功能，你需要在所有 TiDB 实例的配置文件中将 [`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400) 设置为 `true`。
> - 对于 TiDB Cloud Dedicated，要启用表锁功能，你需要联系 [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) 将 [`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400) 设置为 `true`。
> - 对于 TiDB Cloud Serverless，不支持将 [`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400) 设置为 `true`。

## 语法图

```ebnf+diagram
LockTablesDef
         ::= 'LOCK' ( 'TABLES' | 'TABLE' ) TableName LockType ( ',' TableName LockType)*


UnlockTablesDef
         ::= 'UNLOCK' 'TABLES'

LockType
         ::= 'READ' ('LOCAL')?
           | 'WRITE' ('LOCAL')?
```

## 获取表锁

你可以使用 `LOCK TABLES` 语句在当前会话中获取表锁。可以使用以下锁类型：

`READ` 锁：

- 持有此锁的会话可以读取表，但不能写入。
- 多个会话可以同时从同一个表获取 `READ` 锁。
- 其他会话无需显式获取 `READ` 锁即可读取表。

`READ LOCAL` 锁仅用于与 MySQL 语法兼容，不支持此功能。

`WRITE` 锁：

- 持有此锁的会话可以读取和写入表。
- 只有持有此锁的会话可以访问表。在锁释放之前，其他会话都不能访问它。

`WRITE LOCAL` 锁：

- 持有此锁的会话可以读取和写入表。
- 只有持有此锁的会话可以访问表。其他会话可以读取表，但不能写入。

如果 `LOCK TABLES` 语句需要的锁被另一个会话持有，`LOCK TABLES` 语句必须等待，并且在执行此语句时会返回错误，例如：

```sql
> LOCK TABLES t1 READ;
ERROR 8020 (HY000): Table 't1' was locked in WRITE by server: f4799bcb-cad7-4285-8a6d-23d3555173f1_session: 2199023255959
```

上述错误消息表示，TiDB `f4799bcb-cad7-4285-8a6d-23d3555173f1` 中 ID 为 `2199023255959` 的会话已经在表 `t1` 上持有 `WRITE` 锁。因此，当前会话无法在表 `t1` 上获取 `READ` 锁。

你不能在单个 `LOCK TABLES` 语句中多次获取相同的表锁。

```sql
> LOCK TABLES t WRITE, t READ;
ERROR 1066 (42000): Not unique table/alias: 't'
```

## 释放表锁

当会话持有的表锁被释放时，它们都会同时被释放。会话可以显式或隐式地释放其锁。

- 会话可以使用 `UNLOCK TABLES` 显式释放其锁。
- 如果已经持有锁的会话发出 `LOCK TABLES` 语句以获取锁，则在获取新锁之前会隐式释放其现有锁。

如果客户端会话的连接终止（无论是正常还是异常终止），TiDB 会隐式释放该会话持有的所有表锁。如果客户端重新连接，锁将不再有效。因此，不建议在客户端启用自动重连。如果启用自动重连，客户端在重连发生时不会收到通知，所有表锁或当前事务都会丢失。相反，如果禁用自动重连，当连接断开时，下一条语句执行时会发生错误。客户端可以检测到错误并采取适当的操作，如重新获取锁或重做事务。

## 表锁限制和条件

你可以安全地使用 `KILL` 终止持有表锁的会话。

你不能在以下数据库中的表上获取表锁：

- `INFORMATION_SCHEMA`
- `PERFORMANCE_SCHEMA`
- `METRICS_SCHEMA`
- `mysql`

## MySQL 兼容性

### 表锁获取

- 在 TiDB 中，如果会话 A 已经持有表锁，当会话 B 尝试写入表时会返回错误。在 MySQL 中，会话 B 的写入请求会被阻塞，直到会话 A 释放表锁，其他会话的锁定表请求会被阻塞，直到当前会话释放 `WRITE` 锁。
- 在 TiDB 中，如果 `LOCK TABLES` 语句需要的锁被另一个会话持有，`LOCK TABLES` 语句必须等待，并且在执行此语句时会返回错误。在 MySQL 中，此语句会被阻塞，直到获取锁。
- 在 TiDB 中，`LOCK TABLES` 语句在整个集群中生效。在 MySQL 中，此语句仅在当前 MySQL 服务器中生效，且与 NDB 集群不兼容。

### 表锁释放

当在 TiDB 会话中显式启动事务时（例如，使用 `BEGIN` 语句），TiDB 不会隐式释放会话持有的表锁；但 MySQL 会。
