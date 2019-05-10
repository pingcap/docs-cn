---
title: TiDB Transaction Isolation Levels
summary: Learn about the transaction isolation levels in TiDB.
category: reference
aliases: ['/docs/sql/transaction-isolation/']
---

# TiDB Transaction Isolation Levels

Transaction isolation is one of the foundations of database transaction processing. Isolation is the I in the acronym ACID (Atomicity, Consistency, Isolation, Durability), which represents the isolation property of database transactions.

The SQL-92 standard defines four levels of transaction isolation: Read Uncommitted, Read Committed, Repeatable Read and Serializable. See the following table for details:

| Isolation Level  | Dirty Read   | Nonrepeatable Read | Phantom Read          | Serialization Anomaly |
| ---------------- | ------------ | ------------------ | --------------------- | --------------------- |
| Read Uncommitted | Possible     | Possible           | Possible              | Possible              |
| Read Committed   | Not possible | Possible           | Possible              | Possible              |
| Repeatable Read  | Not possible | Not possible       | Not possible in  TiDB | Possible              |
| Serializable     | Not possible | Not possible       | Not possible          | Not possible          |

TiDB implements Snapshot Isolation consistency, which it advertises as `REPEATABLE-READ` for compatibility with MySQL. This differs from the [ANSI Repeatable Read isolation level](#difference-between-tidb-and-ansi-repeatable-read) and the [MySQL Repeatable Read level](#difference-between-tidb-and-mysql-repeatable-read).

> **Note:**
>
> In the default configuration, transactions may exhibit lost updates due to automatic retries. See the sections [Transactional anomalies caused by automatic retries](#transactional-anomalies-caused-by-automatic-retries) and [Transaction Retry](#transaction-retry) for additional context on this feature and how to disable it.

TiDB uses the [Percolator transaction model](https://research.google.com/pubs/pub36726.html). A global read timestamp is obtained when the transaction is started, and a global commit timestamp is obtained when the transaction is committed. The execution order of transactions is confirmed based on the timestamps. To know more about the implementation of TiDB transaction model, see [MVCC in TiKV](https://pingcap.com/blog/2016-11-17-mvcc-in-tikv/).

## Repeatable Read

The Repeatable Read isolation level only sees data committed before the transaction begins, and it never sees either uncommitted data or changes committed during transaction execution by concurrent transactions. However, the transaction statement does see the effects of previous updates executed within its own transaction, even though they are not yet committed.

For transactions running on different nodes, the start and commit order depends on the order that the timestamp is obtained from PD.

Transactions of the Repeatable Read isolation level cannot concurrently update a same row. When committing, if the transaction finds that the row has been updated by another transaction after it starts, then the transaction rolls back and retries automatically. For example:

```
create table t1(id int);
insert into t1 values(0);

start transaction;              |               start transaction;
select * from t1;               |               select * from t1;
update t1 set id=id+1;          |               update t1 set id=id+1;
commit;                         |
                                |               commit; -- roll back and retry atutomatically
```

### Difference between TiDB and ANSI Repeatable Read

The Repeatable Read isolation level in TiDB differs from ANSI Repeatable Read isolation level, though they sharing the same name. According to the standard described in the [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf) paper, TiDB implements the snapshot isolation level, and it does not allow phantom reads but allows write skews. In contrast, the ANSI Repeatable Read isolation level allows phantom reads but does not allow write skews.

### Difference between TiDB and MySQL Repeatable Read

The Repeatable Read isolation level in TiDB differs from that in MySQL. The MySQL Repeatable Read isolation level does not check whether the current version is visible when updating, which means it can continue to update even if the row has been updated after the transaction starts. In contrast, if the row has been updated after the transaction starts, the TiDB transaction is rolled back and retried. Transaction Retries in TiDB might fail, leading to a final failure of the transaction, while in MySQL the updating transaction can be successful.

The MySQL Repeatable Read isolation level is not the snapshot isolation level. The consistency of MySQL Repeatable Read isolation level is weaker than both the snapshot isolation level and TiDB Repeatable Read isolation level.

## Transaction retry

Transactions that fail may automatically be retried by TiDB, which may lead to lost updates. This feature can be disabled by setting `tidb_retry_limit = 0`.

```
[performance]
...
# The maximum number of retries when commit a transaction.
retry-limit = 10
```

## Transactional anomalies caused by automatic retries

Because TiDB automatically retries transactions [by default](#transaction-retry), the final result might not be as expected if the transactions created by the explicit `BEGIN` statement automatically retry after meeting a conflict.

Example 1:

| Session1 | Session2 |
| ---------------- | ------------ |
| `begin;` | `begin;` |
| `select balance from t where id = 1;` | `update t set balance = balance -100 where id = 1;` |
|  | `update t set balance = balance -100 where id = 2;` |
| // the subsequent logic depends on the result of `select` | `commit;` |
| `if balance > 100 {` | |
| `update t set balance = balance + 100 where id = 2;` | |
| `}` | |
| `commit;` // automatic retry | |

Example 2:

| Session1 | Session2   |
| ---------------- | ------------ |
| `begin;` | `begin;` |
| `update t set balance = balance - 100  where id = 1;` | `delete from t where id = 1;` |
|  | `commit;` |
| // the subsequent logic depends on the result of `affected_rows` | |
| `if affected_rows > 0 {` | |
| `update t set balance = balance + 100 where id = 2;` | |
| `}` | |
| `commit;` // automatic retry | |

Under the automatic retry mechanism of TiDB, all the executed statements for the first time are re-executed again. Whether the subsequent statements are to be executed or not depends on the results of the previous statements, automatic retry can violate snapshot isolation, causing lost updates.

To disable the automatic retry of explicit transactions, configure the `tidb_retry_limit` variable:

```sql
SET GLOBAL tidb_retry_limit = 0;
```

Changing the variable `tidb_disable_txn_auto_retry` does not affect the implicit single statement with `auto_commit = 1`, since this type of statement still automatically retries.

After the automatic retry of explicit transactions is disabled, if a transaction conflict occurs, the `commit` statement returns an error that includes the `try again later` string. The application layer uses this string to judge whether the error can be retried.

If the application layer logic is included in the process of transaction execution, it is recommended to add the retry of explicit transactions at the application layer and disable automatic retry.

## Statement rollback

If you execute a statement within a transaction, the statement does not take effect when an error occurs.

```
begin;
insert into test values (1);
insert into tset values (2);  // This statement does not take effect because "test" is misspelled as "tset".
insert into test values (3);
commit;
```

In the above example, the second `insert` statement fails, while the other two `insert` statements (1 & 3) can be successfully committed.

```
begin;
insert into test values (1);
insert into tset values (2);  // This statement does not take effect because "test" is misspelled as "tset".
insert into test values (3);
rollback;
```

In the above example, the second `insert` statement fails, and this transaction does not insert any data into the database because `rollback` is called.
