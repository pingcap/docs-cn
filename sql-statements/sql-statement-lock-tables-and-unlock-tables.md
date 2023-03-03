---
title: LOCK TABLES 和 UNLOCK TABLES
summary: TiDB 数据库中 LOCK TABLES 和 UNLOCK TABLES 的使用概况。
---

# LOCK TABLES 和 UNLOCK TABLES

客户端会话可以使用 `LOCK TABLES` 语句获取表锁，以便和其他会话合作访问表，或者防止其他会话修改表。会话只能为自己获取或释放锁。一个会话无法获取另一个会话的锁或释放另一个会话持有的锁。

`LOCK TABLES` 可以为当前的客户端会话获取表锁。你可以获取普通表的表锁，但你必须拥有锁定对象的 `LOCK TABLES` 和 `SELECT ` 权限。

`UNLOCK TABLES` 显式释放当前会话持有的任何表锁。`LOCK TABLES` 在获取新锁之前会隐式释放当前会话持有的所有表锁。

表锁可以防止其他会话的读取或写入。持有 WRITE 锁的会话可以执行表级操作，例如 `DROP TABLE` 或 `TRUNCATE TABLE`。对于持有读锁的会话，不允许执行 `DROP TABLE` 或 `TRUNCATE TABLE` 操作。

> **警告：**
>
> LOCK TABLES 和 UNLOCK TABLES 目前为实验特性，不建议在生产环境中使用。

## 语法图

```ebnf+diagram
LockTablesDef
         ::= 'LOCK' 'TABLES' TableName LockType ( ',' TableName LockType)*


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
  - 只有持有 `WRITE` 锁的会话才能访问该表。在释放锁之前，没有其他会话可以访问它。
  - 其他会话对该表的锁请求会被阻塞直到当前会话释放 `WRITE` 锁。

`WRITE LOCAL` 锁：

  - 持有 `WRITE LOCAL` 锁的会话可以读取和写入表。
  - 只有持有 `WRITE LOCAL` 锁的会话才能写入该表，但其他会话依然可以读取该表的数据。

如果 LOCK TABLES 语句想要获取的表锁被其他会话持有且必须等待锁释放时，则 `LOCK TABLES` 语句会执行报错，例如：

```sql
> lock table t1 read;
ERROR 8020 (HY000): Table 't1' was locked in WRITE by server: f4799bcb-cad7-4285-8a6d-23d3555173f1_session: 2199023255959
```

上面的错误信息说明在 TiDB `f4799bcb-cad7-4285-8a6d-23d3555173f1` 上的会话 `2199023255959` 持有表 `t1` 的 `WRITE` 锁，所以当前会话无法获取表 `t1` 的 `READ` 锁。

不能在单个 `LOCK TABLES` 语句中多次获取同一个表的锁。

```sql
> LOCK TABLE t WRITE, t READ;
(1066, "Not unique table/alias: 't'")
```

## 释放表锁

释放会话持有的表锁时，它们将同时释放。会话可以显式释放其锁，也可以在某些情况下隐式释放锁。

- 会话可以使用 `UNLOCK TABLES` 语句显式释放其持有的所有锁。
