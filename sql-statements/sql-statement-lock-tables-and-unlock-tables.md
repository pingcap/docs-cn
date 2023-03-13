---
title: LOCK TABLES 和 UNLOCK TABLES
summary: TiDB 数据库中 LOCK TABLES 和 UNLOCK TABLES 的使用概况。
---

# LOCK TABLES 和 UNLOCK TABLES

> **警告：**
>
> `LOCK TABLES` 和 `UNLOCK TABLES` 目前为实验特性，不建议在生产环境中使用。

客户端会话可以使用 `LOCK TABLES` 语句获取表锁，以便和其他会话合作访问表，或者防止其他会话修改表。会话只能为自己获取或释放锁。一个会话无法为另一个会话获取表锁或释放另一个会话持有的表锁。

`LOCK TABLES` 可以为当前客户端会话获取表锁。你可以获取普通表的表锁，但你必须拥有锁定对象的 `LOCK TABLES` 和 `SELECT` 权限。

`UNLOCK TABLES` 显式释放当前会话持有的所有表锁。`LOCK TABLES` 在获取新锁之前会隐式释放当前会话持有的所有表锁。

表锁可以防止其他会话的读取或写入。持有 `WRITE` 锁的会话可以执行表级操作，例如 `DROP TABLE` 或 `TRUNCATE TABLE`。

> **警告：**
>
> 开启表锁功能需要在所有 TiDB 实例的配置文件中设置 [`enable-table-lock`](/tidb-configuration-file.md#enable-table-lock-从-v400-版本开始引入) 为 `true`。

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

你可以在会话中使用 `LOCK TABLES` 语句获取表锁。表锁有以下类型：

`READ` 锁：

- 持有 `READ` 锁的会话可以读表，但不能写入。
- 多个会话可以同时获取同一个表的 `READ` 锁。
- 其他会话可以在不显式获取 `READ` 锁的情况下读表。

`READ LOCAL` 锁只是语法兼容 MySQL，实际上并不支持。

`WRITE` 锁：

- 持有 `WRITE` 锁的会话可以读取和写入表。
- 只有持有 `WRITE` 锁的会话才能访问该表。在释放锁之前，其他会话不能读取或写入该表。

`WRITE LOCAL` 锁：

- 持有 `WRITE LOCAL` 锁的会话可以读取和写入表。
- 只有持有 `WRITE LOCAL` 锁的会话才能写入该表，但其他会话依然可以读取该表的数据。

如果 `LOCK TABLES` 语句想要获取的表锁被其他会话持有且必须等待锁释放时，则 `LOCK TABLES` 语句会执行报错，例如：

```sql
> LOCK TABLES t1 read;
ERROR 8020 (HY000): Table 't1' was locked in WRITE by server: f4799bcb-cad7-4285-8a6d-23d3555173f1_session: 2199023255959
```

以上错误信息表明，在 TiDB `f4799bcb-cad7-4285-8a6d-23d3555173f1` 中，ID 为 `2199023255959` 的会话已经持有表 `t1` 的 `WRITE` 锁，所以，当前会话无法获取表 `t1` 的 `READ` 锁。

不能在单个 `LOCK TABLES` 语句中多次获取同一个表的锁。

```sql
> LOCK TABLES t WRITE, t READ;
ERROR 1066 (42000): Not unique table/alias: 't'
```

## 释放表锁

释放会话持有的表锁时，将同时释放该会话所有持有的表锁。会话可以显式或隐式释放表锁：

- 会话可以使用 `UNLOCK TABLES` 语句显式释放其持有的所有表锁。
- 当会话使用 `LOCK TABLES` 语句来获取表锁，而且同时已经持有其他表锁时，则在获取新表锁之前，将隐式释放其已经持有的所有表锁。

当客户端会话的连接终止（无论是正常还是异常），TiDB 都会隐式释放会话持有的所有表锁。如果客户端重新连接，锁将不再有效。因此，通常不建议在客户端使用自动重新连接，因为在开启自动重新连接时，如果发生重新连接，任何表锁或当前事务都将丢失，而且不会通知客户端。禁用自动重新连接后，如果连接断开，则客户端会话发出的下一条语句将会收到报错信息。客户端可以检测到错误并采取适当的操作，例如重新获取锁或重做事务。

## 表锁的使用限制和条件

你可以安全地使用 `KILL` 语句终止已经持有表锁的会话。

不支持获取以下数据库中表的表锁：

- `INFORMATION_SCHEMA`
- `PERFORMANCE_SCHEMA`
- `METRICS_SCHEMA` 
- `mysql`

## 和 MySQL 的兼容性

### 获取表锁

- 在 TiDB 中，如果会话 A 已经持有了一个表的表锁，另一个会话 B 对该表写入时会报错；但 MySQL 会阻塞会话 B 对该表的写入，直到会话 A 释放该表锁。其他会话对该表的锁请求会被阻塞直到当前会话释放 `WRITE` 锁。
- 在 TiDB 中，如果 `LOCK TABLES` 语句想要获取的表锁被其他会话持有且必须等待锁释放时，`LOCK TABLES` 语句会执行报错；但 MySQL 会阻塞 `LOCK TABLES` 语句的执行，直到成功获取想要的表锁。
- 在 TiDB 中，使用 `LOCK TABLES` 语句获取表锁的作用域是整个集群；但 MySQL 中表锁的作用域是单个 MySQL 服务器，与 NDB 群集不兼容。

### 释放表锁

在 TiDB 的会话中显示开启一个事务时（例如使用 `BEGIN` 语句），TiDB 不会隐式释放当前会话已经持有的表锁；但 MySQL 会隐式释放当前会话已经持有的表锁。
