---
title: Transaction overview
summary: A brief introduction to transactions in TiDB.
---

# Transaction overview

TiDB supports complete distributed transactions, providing [optimistic transactions](/optimistic-transaction.md) and [pessimistic transactions](/pessimistic-transaction.md) (introduced in TiDB 3.0). This article mainly introduces transaction statements, optimistic transactions and pessimistic transactions, transaction isolation levels, and application-side retry and error handling in optimistic transactions.

## Common statements

This chapter introduces how to use transactions in TiDB. The following example demonstrates the process of a simple transaction:

Bob wants to transfer $20 to Alice. This transaction includes two operations:

- Bob's account is reduced by $20.
- Alice's account is increased by $20.

Transactions can ensure that both of the above operations are executed successfully or both fail.

Insert some sample data into the table using the `users` table in the [bookshop](/develop/dev-guide-bookshop-schema-design.md) database:

```sql
INSERT INTO users (id, nickname, balance)
  VALUES (2, 'Bob', 200);
INSERT INTO users (id, nickname, balance)
  VALUES (1, 'Alice', 100);
```

Run the following transactions and explain what each statement means:

```sql
BEGIN;
  UPDATE users SET balance = balance - 20 WHERE nickname = 'Bob';
  UPDATE users SET balance = balance + 20 WHERE nickname= 'Alice';
COMMIT;
```

After the above transaction is executed successfully, the table should look like this:

```
+----+--------------+---------+
| id | account_name | balance |
+----+--------------+---------+
|  1 | Alice        |  120.00 |
|  2 | Bob          |  180.00 |
+----+--------------+---------+

```

### Start a transaction

To explicitly start a new transaction, you can use either `BEGIN` or `START TRANSACTION`.

```sql
BEGIN;
```

```sql
START TRANSACTION;
```

The default transaction mode of TiDB is pessimistic. You can also explicitly specify the [optimistic transaction model](/develop/dev-guide-optimistic-and-pessimistic-transaction.md):

```sql
BEGIN OPTIMISTIC;
```

Enable the [pessimistic transaction mode](/develop/dev-guide-optimistic-and-pessimistic-transaction.md):

```sql
BEGIN PESSIMISTIC;
```

If the current session is in the middle of a transaction when the above statement is executed, TiDB commits the current transaction first, and then starts a new transaction.

### Commit a transaction

You can use the `COMMIT` statement to commit all modifications made by TiDB in the current transaction.

```sql
COMMIT;
```

Before enabling optimistic transactions, make sure that your application can properly handle errors that may be returned by a `COMMIT` statement. If you are not sure how your application will handle it, it is recommended to use the pessimistic transaction mode instead.

### Roll back a transaction

You can use the `ROLLBACK` statement to roll back modifications of the current transaction.

```sql
ROLLBACK;
```

In the previous transfer example, if you roll back the entire transaction, Alice's and Bob's balances will remain unchanged, and all modifications of the current transaction are canceled.

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

The transaction is also automatically rolled back if the client connection is stopped or closed.

## Transaction isolation levels

The transaction isolation levels are the basis of database transaction processing. The "I" (Isolation) in **ACID** refers to the isolation of the transactions.

The SQL-92 standard defines four isolation levels:

- read uncommitted (`READ UNCOMMITTED`)
- read committed (`READ COMMITTED`)
- repeatable read (`REPEATABLE READ`)
- serializable (`SERIALIZABLE`).

See the table below for details:

| Isolation Level  | Dirty Write  | Dirty Read   | Fuzzy Read   | Phantom      |
| ---------------- | ------------ | ------------ | ------------ | ------------ |
| READ UNCOMMITTED | Not Possible | Possible     | Possible     | Possible     |
| READ COMMITTED   | Not Possible | Not possible | Possible     | Possible     |
| REPEATABLE READ  | Not Possible | Not possible | Not possible | Possible     |
| SERIALIZABLE     | Not Possible | Not possible | Not possible | Not possible |

TiDB supports the following isolation levels: `READ COMMITTED` and `REPEATABLE READ`:

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

TiDB implements Snapshot Isolation (SI) level consistency, also known as "repeatable read" for consistency with MySQL. This isolation level is different from [ANSI Repeatable Read Isolation Level](/transaction-isolation-levels.md#difference-between-tidb-and-ansi-repeatable-read) and [MySQL Repeatable Read Isolation Level](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read). For more details, see [TiDB Transaction Isolation Levels](/transaction-isolation-levels.md).