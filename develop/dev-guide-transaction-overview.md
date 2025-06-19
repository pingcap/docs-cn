---
title: 事务概述
summary: TiDB 事务的简要介绍。
---

# 事务概述

TiDB 支持完整的分布式事务，提供[乐观事务](/optimistic-transaction.md)和[悲观事务](/pessimistic-transaction.md)（在 TiDB 3.0 中引入）。本文主要介绍事务语句、乐观事务和悲观事务、事务隔离级别，以及乐观事务中的应用端重试和错误处理。

## 常用语句

本章介绍如何在 TiDB 中使用事务。以下示例演示了一个简单事务的过程：

Bob 想要转账 $20 给 Alice。这个事务包括两个操作：

- Bob 的账户减少 $20。
- Alice 的账户增加 $20。

事务可以确保上述两个操作都执行成功或都失败。

使用 [bookshop](/develop/dev-guide-bookshop-schema-design.md) 数据库中的 `users` 表插入一些示例数据：

```sql
INSERT INTO users (id, nickname, balance)
  VALUES (2, 'Bob', 200);
INSERT INTO users (id, nickname, balance)
  VALUES (1, 'Alice', 100);
```

运行以下事务并解释每个语句的含义：

```sql
BEGIN;
  UPDATE users SET balance = balance - 20 WHERE nickname = 'Bob';
  UPDATE users SET balance = balance + 20 WHERE nickname= 'Alice';
COMMIT;
```

上述事务执行成功后，表应该如下所示：

```
+----+--------------+---------+
| id | account_name | balance |
+----+--------------+---------+
|  1 | Alice        |  120.00 |
|  2 | Bob          |  180.00 |
+----+--------------+---------+

```

### 开始事务

要显式开始一个新事务，你可以使用 `BEGIN` 或 `START TRANSACTION`。

```sql
BEGIN;
```

```sql
START TRANSACTION;
```

TiDB 的默认事务模式是悲观事务。你也可以显式指定[乐观事务模式](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)：

```sql
BEGIN OPTIMISTIC;
```

启用[悲观事务模式](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)：

```sql
BEGIN PESSIMISTIC;
```

如果在执行上述语句时当前会话正处于事务中，TiDB 会先提交当前事务，然后开始一个新事务。

### 提交事务

你可以使用 `COMMIT` 语句提交 TiDB 在当前事务中所做的所有修改。

```sql
COMMIT;
```

在启用乐观事务之前，请确保你的应用程序可以正确处理 `COMMIT` 语句可能返回的错误。如果你不确定你的应用程序将如何处理，建议使用悲观事务模式。

### 回滚事务

你可以使用 `ROLLBACK` 语句回滚当前事务的修改。

```sql
ROLLBACK;
```

在前面的转账示例中，如果你回滚整个事务，Alice 和 Bob 的余额将保持不变，当前事务的所有修改都被取消。

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

如果客户端连接停止或关闭，事务也会自动回滚。

## 事务隔离级别

事务隔离级别是数据库事务处理的基础。**ACID** 中的 "I"（隔离性）指的是事务的隔离性。

SQL-92 标准定义了四个隔离级别：

- 读未提交（`READ UNCOMMITTED`）
- 读已提交（`READ COMMITTED`）
- 可重复读（`REPEATABLE READ`）
- 可串行化（`SERIALIZABLE`）

详细信息请参见下表：

| 隔离级别 | 脏写 | 脏读 | 不可重复读 | 幻读 |
| ---------------- | ------------ | ------------ | ------------ | ------------ |
| READ UNCOMMITTED | 不可能 | 可能 | 可能 | 可能 |
| READ COMMITTED   | 不可能 | 不可能 | 可能 | 可能 |
| REPEATABLE READ  | 不可能 | 不可能 | 不可能 | 可能 |
| SERIALIZABLE     | 不可能 | 不可能 | 不可能 | 不可能 |

TiDB 支持以下隔离级别：`READ COMMITTED` 和 `REPEATABLE READ`：

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

TiDB 实现了快照隔离（SI）级别的一致性，为了与 MySQL 保持一致，也称为"可重复读"。这个隔离级别与 [ANSI 可重复读隔离级别](/transaction-isolation-levels.md#difference-between-tidb-and-ansi-repeatable-read)和 [MySQL 可重复读隔离级别](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read)不同。更多详细信息，请参见 [TiDB 事务隔离级别](/transaction-isolation-levels.md)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
