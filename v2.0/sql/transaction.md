---
title: Transactions
summary: Learn how to use the distributed transaction statements.
category: user guide
---

# Transactions

TiDB supports distributed transactions. The statements that relate to transactions include the `Autocommit` variable, `START TRANSACTION`/`BEGIN`, `COMMIT` and `ROLLBACK`.

## Autocommit

Syntax:

```sql
SET autocommit = {0 | 1}
```

If you set the value of `autocommit` to 1, the status of the current Session is autocommit. If you set the value of `autocommit` to 0, the status of the current Session is non-autocommit. The value of `autocommit` is 1 by default.       

In the autocommit status, the updates are automatically committed to the database after you run each statement. Otherwise, the updates are only committed when you run the `COMMIT` or `BEGIN` statement.

`autocommit` is also a System Variable. You can update the current Session or the Global value using the following variable assignment statement:

```sql
SET @@SESSION.autocommit = {0 | 1};
SET @@GLOBAL.autocommit = {0 | 1};
```   

## START TRANSACTION, BEGIN

Syntax:

```sql
BEGIN;

START TRANSACTION;

START TRANSACTION WITH CONSISTENT SNAPSHOT;
```

The three statements above are all statements that transactions start with, through which you can explicitly start a new transaction. If at this time, the current Session is in the process of a transaction, a new transaction is started after the current transaction is committed.

## COMMIT

Syntax:

```sql
COMMIT;
```

This statement is used to commit the current transaction, including all the updates between `BEGIN` and `COMMIT`.

## ROLLBACK

Syntax:

```sql
ROLLBACK;
```

This statement is used to roll back the current transaction and cancels all the updates between `BEGIN` and `COMMIT`.

## Explicit and implicit transaction

TiDB supports explicit transactions (`BEGIN/COMMIT`) and implicit transactions (`SET autocommit = 1`).

If you set the value of `autocommit` to 1 and start a new transaction through `BEGIN`, the autocommit is disabled before `COMMIT`/`ROLLBACK` which makes the transaction becomes explicit.

For DDL statements, the transaction is committed automatically and does not support rollback. If you run the DDL statement while the current Session is in the process of a transaction, the DDL statement is run after the current transaction is committed.

## Transaction isolation level

TiDB uses `SNAPSHOT ISOLATION` by default. You can set the isolation level of the current Session to `READ COMMITTED` using the following statement:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```
