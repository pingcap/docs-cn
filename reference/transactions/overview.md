---
title: Transactions
summary: Learn how to use the distributed transaction statements.
category: reference
---

# Transactions

TiDB supports complete distributed transactions. This document introduces transaction-related statements, explicit and implicit transactions, isolation levels, and laziness checks for transactions.

The common variables include `autocommit`, [`tidb_disable_txn_auto_retry`](/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_disable_txn_auto_retry), and [`tidb_retry_limit`](/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_retry_limit).

## Common syntax

### `BEGIN`, `START TRANSACTION` and `START TRANSACTION WITH CONSISTENT SNAPSHOT`

Syntax:

{{< copyable "sql" >}}

```sql
BEGIN;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION WITH CONSISTENT SNAPSHOT;
```

All of the above three statements are used to start a transaction with the same effect. You can explicitly start a new transaction by executing one of these statements. If the current session is in the process of a transaction when one of these statements is executed, TiDB automatically commits the current transaction before starting a new transaction.

### `COMMIT`

Syntax:

{{< copyable "sql" >}}

```sql
COMMIT;
```

You can use this statement to commit the current transaction, including all updates between `[BEGIN|START TRANSACTION]` and `COMMIT`.

### `ROLLBACK`

Syntax:

{{< copyable "sql" >}}

```sql
ROLLBACK;
```

You can use this statement to roll back the current transaction and cancels all updates between `[BEGIN | START TRANSACTION]` and `ROLLBACK`.

## Autocommit

Syntax:

{{< copyable "sql" >}}

```sql
SET autocommit = {0 | 1}
```

If you set the value of `autocommit` to `1`, the status of the current session is autocommit. If you set the value of `autocommit` to `0`, the status of the current session is non-autocommit. The value of `autocommit` is `1` by default.

When autocommit is enabled, statements are automatically committed immediately following their execution. When autocommit is disabled, statements are only committed when you execute the `COMMIT` statement.

> **Note:**
>
> Some statements are committed implicitly. For example, executing `[BEGIN|START TRANSACTION]` implicitly commits the last transaction and starts a new transaction. This behavior is required for MySQL compatibility. Refer to [implicit commit](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) for more details.

`autocommit` is also a system variable. You can update the current session or the Global value using the following variable assignment statement:

{{< copyable "sql" >}}

```sql
SET @@SESSION.autocommit = {0 | 1};
```

{{< copyable "sql" >}}

```sql
SET @@GLOBAL.autocommit = {0 | 1};
```

## Explicit and implicit transaction

TiDB supports explicit transactions (`[BEGIN|START TRANSACTION]` and `COMMIT`) and implicit transactions (`SET autocommit = 1`).

If you set the value of `autocommit` to `1` and start a new transaction through the `[BEGIN|START TRANSACTION]` statement, the autocommit is disabled before `COMMIT` or `ROLLBACK` which makes the transaction becomes explicit.

For DDL statements, the transaction is committed automatically and does not support rollback. If you run the DDL statement while the current session is in the process of a transaction, the DDL statement is executed after the current transaction is committed.

## Transaction isolation level

TiDB **only supports** `SNAPSHOT ISOLATION`. You can set the isolation level of the current session to `READ COMMITTED` using the following statement. However, TiDB is only compatible with the `READ COMMITTED` isolation level in syntax and transactions are still executed at the `SNAPSHOT ISOLATION` level.

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## Lazy check of constraints

**Lazy check** means that by default TiDB will not check [primary key](/reference/sql/constraints.md#primary-key) or [unique constraints](/reference/sql/constraints.md#unique) when an `INSERT` statement is executed, but instead checks when the transaction is committed. In TiDB, the lazy check is performed for values written by ordinary `INSERT` statements.

For example:

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
INSERT INTO t1 VALUES (1);
START TRANSACTION;
INSERT INTO t1 VALUES (1); -- MySQL returns an error; TiDB returns success.
INSERT INTO t1 VALUES (2);
COMMIT; -- It is successfully committed in MySQL; TiDB returns an error and the transaction rolls back.
SELECT * FROM t1; -- MySQL returns 1 2; TiDB returns 1.
```

The lazy check is important because if you perform a unique constraint check on every `INSERT` statement in a transaction, it can cause high network overhead. A batch check when the transaction is committed can greatly improve performance.

> **Note:**
>
> This optimization does not take effect for `INSERT IGNORE` and `INSERT ON DUPLICATE KEY UPDATE`, only for normal `INSERT` statements. The behavior can also be disabled by setting `tidb_constraint_check_in_place=TRUE`.

## Statement rollback

If you execute a statement within a transaction, the statement does not take effect when an error occurs.

```sql
begin;
insert into test values (1);
insert into tset values (2);  // This statement does not take effect because "test" is misspelled as "tset".
insert into test values (3);
commit;
```

In the above example, the second `insert` statement fails, while the other two `insert` statements (1 & 3) can be successfully committed.

```sql
begin;
insert into test values (1);
insert into tset values (2);  // This statement does not take effect because "test" is misspelled as "tset".
insert into test values (3);
rollback;
```

In the above example, the second `insert` statement fails, and this transaction does not insert any data into the database because `rollback` is called.
