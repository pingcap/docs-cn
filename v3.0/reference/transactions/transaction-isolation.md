---
title: TiDB Transaction Isolation Levels
summary: Learn about the transaction isolation levels in TiDB.
category: reference
aliases: ['/docs/sql/transaction-isolation/']
---

# TiDB Transaction Isolation Levels

Transaction isolation is one of the foundations of database transaction processing. Isolation is the I in the acronym ACID (Atomicity, Consistency, Isolation, Durability), which represents the isolation property of database transactions.

The SQL-92 standard defines four levels of transaction isolation: Read Uncommitted, Read Committed, Repeatable Read, and Serializable. See the following table for details:

| Isolation Level  | Dirty Write   | Dirty Read | Fuzzy Read     | Phantom |
| :----------- | :------------ | :------------- | :----------| :-------- |
| READ UNCOMMITTED | Not Possible | Possible     | Possible     | Possible     |
| READ COMMITTED   | Not Possible | Not possible | Possible     | Possible     |
| REPEATABLE READ  | Not Possible | Not possible | Not possible | Possible     |
| SERIALIZABLE     | Not Possible | Not possible | Not possible | Not possible |

TiDB implements Snapshot Isolation consistency, which it advertises as `REPEATABLE-READ` for compatibility with MySQL. This differs from the [ANSI Repeatable Read isolation level](#difference-between-tidb-and-ansi-repeatable-read) and the [MySQL Repeatable Read level](#difference-between-tidb-and-mysql-repeatable-read).

> **Note:**
>
> In the default configuration of TiDB v3.0, the automatic transaction retry is disabled. For how this feature influences the isolation level and how to enable it, see [automatic retry and transactional anomalies caused by automatic retry](#automatic-retry-and-transactional-anomalies-caused-by-automatic-retry).

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
                                |               commit; -- the transaction commit fails and rolls back
```

### Difference between TiDB and ANSI Repeatable Read

The Repeatable Read isolation level in TiDB differs from ANSI Repeatable Read isolation level, though they sharing the same name. According to the standard described in the [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf) paper, TiDB implements the Snapshot Isolation (SI) level. This isolation level does not allow strict phantoms (A3) but allows broad phantoms (P3) and write skews. In contrast, the ANSI Repeatable Read isolation level allows phantom reads but does not allow write skews.

### Difference between TiDB and MySQL Repeatable Read

The Repeatable Read isolation level in TiDB differs from that in MySQL. The MySQL Repeatable Read isolation level does not check whether the current version is visible when updating, which means it can continue to update even if the row has been updated after the transaction starts. In contrast, if the row has been updated after the transaction starts, the TiDB transaction is rolled back and retried. Transaction Retries in TiDB might fail, leading to a final failure of the transaction, while in MySQL the updating transaction can be successful.

The MySQL Repeatable Read isolation level is not the snapshot isolation level. The consistency of MySQL Repeatable Read isolation level is weaker than both the snapshot isolation level and TiDB Repeatable Read isolation level.

## Automatic retry and transactional anomalies caused by automatic retry

By default TiDB will not retry transactions because this might lead to lost updates and damaged Snapshot Isolation. If your application can tolerate lost updates, and does not require Snapshot Isolation consistency, you can enable **this feature** by setting `tidb_disable_txn_auto_retry = off`. This has the benefit of fewer `COMMIT` statements generating errors. The value of `tidb_retry_limit` cannot be `0`. Otherwise, the automatic retry is also disabled.

When automatic retry is enabled, conflicts in an explicit transaction might lead to unexpected result.

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

To disable the automatic retry of explicit transactions, configure `tidb_disable_txn_auto_retry = on`:

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_disable_txn_auto_retry = on;
```

Changing the variable `tidb_disable_txn_auto_retry` does not affect the implicit single statement with `autocommit = 1`, because the automatic retry of this statement does not cause anomalies like update loss and does not break the isolation of a transaction.

After the automatic retry of explicit transactions is disabled, if a transaction conflict occurs, the `commit` statement returns an error that includes the `try again later` string. The application layer uses this string to judge whether the error can be retried.

If the application layer logic is included in the process of transaction execution, it is recommended to add the retry of explicit transactions at the application layer and disable automatic retry.

The `tidb_retry_limit` variable determines the maximum number of transaction retries. The default value is 10. When this variable is set to 0, none of the transactions automatically retries, including the implicit single statement transactions that are automatically committed. This is the way to completely disable the automatic retry mechanism in TiDB. If you are more concerned with the latency of transaction execution than transaction isolation, you can set it to 0. Then all conflicting transactions report failures to the application layer in the fastest way.
