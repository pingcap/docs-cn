---
title: 事务概览
summary: 简单介绍 TiDB 中的事务。
---

# 事务概览

TiDB 支持完整的分布式事务，提供[乐观事务](/optimistic-transaction.md)与[悲观事务](/pessimistic-transaction.md)（TiDB 3.0 中引入）两种事务模型。本文主要介绍涉及到事务的语句、乐观事务和悲观事务、事务的隔离级别，以及乐观事务应用端重试和错误处理。

## 通用语句

本章介绍在 TiDB 中如何使用事务。 将使用下面的示例来演示一个简单事务的控制流程：

Bob 要给 Alice 转账 20 元钱，当中至少包括两个操作：

- Bob 账户减少 20 元。
- Alice 账户增加 20 元。

事务可以确保以上两个操作要么都执行成功，要么都执行失败，不会出现钱平白消失或出现的情况。

使用 [bookshop](/develop/dev-guide-bookshop-schema-design.md) 数据库中的 `users` 表，在表中插入一些示例数据：

{{< copyable "sql" >}}

```sql
INSERT INTO users (id, nickname, balance)
  VALUES (2, 'Bob', 200);
INSERT INTO users (id, nickname, balance)
  VALUES (1, 'Alice', 100);
```

现在，运行以下事务并解释每个语句的含义：

{{< copyable "sql" >}}

```sql
BEGIN;
  UPDATE users SET balance = balance - 20 WHERE nickname = 'Bob';
  UPDATE users SET balance = balance + 20 WHERE nickname= 'Alice';
COMMIT;
```

上述事务成功后，表应如下所示：

```
+----+--------------+---------+
| id | account_name | balance |
+----+--------------+---------+
|  1 | Alice        |  120.00 |
|  2 | Bob          |  180.00 |
+----+--------------+---------+

```

### 开启事务

要显式地开启一个新事务，既可以使用 `BEGIN` 语句，也可以使用 `START TRANSACTION` 语句，两者效果相同。语法：

{{< copyable "sql" >}}

```sql
BEGIN;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION;
```

TiDB 的默认事务模式是悲观事务，你也可以明确指定开启[乐观事务](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)：

{{< copyable "sql" >}}

```sql
BEGIN OPTIMISTIC;
```

开启[悲观事务](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)：

{{< copyable "sql" >}}

```sql
BEGIN PESSIMISTIC;
```

如果执行以上语句时，当前 Session 正处于一个事务的中间过程，那么系统会先自动提交当前事务，再开启一个新的事务。

### 提交事务

`COMMIT` 语句用于提交 TiDB 在当前事务中进行的所有修改。语法：

{{< copyable "sql" >}}

```sql
COMMIT;
```

启用乐观事务前，请确保应用程序可正确处理 `COMMIT` 语句可能返回的错误。如果不确定应用程序将会如何处理，建议改为使用悲观事务。

### 回滚事务

`ROLLBACK` 语句用于回滚并撤销当前事务的所有修改。语法：

{{< copyable "sql" >}}

```sql
ROLLBACK;
```

回到之前转账示例，使用 `ROLLBACK` 回滚整个事务之后，Alice 和 Bob 的余额都未发生改变，当前事务的所有修改一起被取消。

{{< copyable "sql" >}}

```sql
TRUNCATE TABLE `users`;

INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (1, 'Alice', 100), (2, 'Bob', 200);

SELECT * FROM `users`;
+----+--------------+---------+
| id | nickname     | balance |
+----+--------------+---------+
|  1 | Alice        |  100.00 |
|  2 | Bob          |  200.00 |
+----+--------------+---------+

BEGIN;
  UPDATE `users` SET `balance` = `balance` - 20 WHERE `nickname`='Bob';
  UPDATE `users` SET `balance` = `balance` + 20 WHERE `nickname`='Alice';
ROLLBACK;

SELECT * FROM `users`;
+----+--------------+---------+
| id | nickname     | balance |
+----+--------------+---------+
|  1 | Alice        |  100.00 |
|  2 | Bob          |  200.00 |
+----+--------------+---------+
```

如果客户端连接中止或关闭，也会自动回滚该事务。

## 事务隔离级别

事务隔离级别是数据库事务处理的基础，**ACID** 中的 **“I”**，即 Isolation，指的就是事务的隔离性。

SQL-92 标准定义了 4 种隔离级别：读未提交 (`READ UNCOMMITTED`)、读已提交 (`READ COMMITTED`)、可重复读 (`REPEATABLE READ`)、串行化 (`SERIALIZABLE`)。详见下表：

| Isolation Level  | Dirty Write  | Dirty Read   | Fuzzy Read   | Phantom      |
| ---------------- | ------------ | ------------ | ------------ | ------------ |
| READ UNCOMMITTED | Not Possible | Possible     | Possible     | Possible     |
| READ COMMITTED   | Not Possible | Not possible | Possible     | Possible     |
| REPEATABLE READ  | Not Possible | Not possible | Not possible | Possible     |
| SERIALIZABLE     | Not Possible | Not possible | Not possible | Not possible |

TiDB 语法上支持设置 `READ COMMITTED` 和 `REPEATABLE READ` 两种隔离级别：

{{< copyable "sql" >}}

```sql
mysql> SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
ERROR 8048 (HY000): The isolation level 'READ-UNCOMMITTED' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
mysql> SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
Query OK, 0 rows affected (0.00 sec)

mysql> SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
Query OK, 0 rows affected (0.00 sec)

mysql> SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
ERROR 8048 (HY000): The isolation level 'SERIALIZABLE' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
```

TiDB 实现了快照隔离 (Snapshot Isolation, SI) 级别的一致性。为与 MySQL 保持一致，又称其为“可重复读”。该隔离级别不同于 [ANSI 可重复读隔离级别](/transaction-isolation-levels.md#与-ansi-可重复读隔离级别的区别) 和 [MySQL 可重复读隔离级别](/transaction-isolation-levels.md#与-mysql-可重复读隔离级别的区别)。更多细节请阅读 [TiDB 事务隔离级别](/transaction-isolation-levels.md)。
