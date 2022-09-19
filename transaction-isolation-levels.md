---
title: TiDB Transaction Isolation Levels
summary: Learn about the transaction isolation levels in TiDB.
aliases: ['/docs/dev/transaction-isolation-levels/','/docs/dev/reference/transactions/transaction-isolation/']
---

# TiDB Transaction Isolation Levels

<CustomContent platform="tidb">

Transaction isolation is one of the foundations of database transaction processing. Isolation is one of the four key properties of a transaction (commonly referred as [ACID](/glossary.md#acid)).

</CustomContent>

<CustomContent platform="tidb-cloud">

Transaction isolation is one of the foundations of database transaction processing. Isolation is one of the four key properties of a transaction (commonly referred as [ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)).

</CustomContent>

The SQL-92 standard defines four levels of transaction isolation: Read Uncommitted, Read Committed, Repeatable Read, and Serializable. See the following table for details:

| Isolation Level  | Dirty Write   | Dirty Read | Fuzzy Read     | Phantom |
| :----------- | :------------ | :------------- | :----------| :-------- |
| READ UNCOMMITTED | Not Possible | Possible     | Possible     | Possible     |
| READ COMMITTED   | Not Possible | Not possible | Possible     | Possible     |
| REPEATABLE READ  | Not Possible | Not possible | Not possible | Possible     |
| SERIALIZABLE     | Not Possible | Not possible | Not possible | Not possible |

TiDB implements Snapshot Isolation (SI) consistency, which it advertises as `REPEATABLE-READ` for compatibility with MySQL. This differs from the [ANSI Repeatable Read isolation level](#difference-between-tidb-and-ansi-repeatable-read) and the [MySQL Repeatable Read level](#difference-between-tidb-and-mysql-repeatable-read).

> **Note:**
>
> Starting from TiDB v3.0, the automatic retry of transactions is disabled by default. It is not recommended to enable the automatic retry because it might **break the transaction isolation level**. Refer to [Transaction Retry](/optimistic-transaction.md#automatic-retry) for details.
>
> Starting from TiDB v3.0.8, newly created TiDB clusters use the [pessimistic transaction mode](/pessimistic-transaction.md) by default. The current read (`for update` read) is **non-repeatable read**. Refer to [pessimistic transaction mode](/pessimistic-transaction.md) for details.

## Repeatable Read isolation level

The Repeatable Read isolation level only sees data committed before the transaction begins, and it never sees either uncommitted data or changes committed during transaction execution by concurrent transactions. However, the transaction statement does see the effects of previous updates executed within its own transaction, even though they are not yet committed.

For transactions running on different nodes, the start and commit order depends on the order that the timestamp is obtained from PD.

Transactions of the Repeatable Read isolation level cannot concurrently update a same row. When committing, if the transaction finds that the row has been updated by another transaction after it starts, then the transaction rolls back. For example:

```sql
create table t1(id int);
insert into t1 values(0);

start transaction;              |               start transaction;
select * from t1;               |               select * from t1;
update t1 set id=id+1;          |               update t1 set id=id+1; -- In pessimistic transactions, the `update` statement executed later waits for the lock until the transaction holding the lock commits or rolls back and releases the row lock.
commit;                         |
                                |               commit; -- The transaction commit fails and rolls back. Pessimistic transactions can commit successfully.
```

### Difference between TiDB and ANSI Repeatable Read

The Repeatable Read isolation level in TiDB differs from ANSI Repeatable Read isolation level, though they sharing the same name. According to the standard described in the [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf) paper, TiDB implements the Snapshot Isolation level. This isolation level does not allow strict phantoms (A3) but allows broad phantoms (P3) and write skews. In contrast, the ANSI Repeatable Read isolation level allows phantom reads but does not allow write skews.

### Difference between TiDB and MySQL Repeatable Read

The Repeatable Read isolation level in TiDB differs from that in MySQL. The MySQL Repeatable Read isolation level does not check whether the current version is visible when updating, which means it can continue to update even if the row has been updated after the transaction starts. In contrast, if the row has been updated after the transaction starts, the TiDB optimistic transaction is rolled back and retried. Transaction retries in TiDB's optimistic concurrency control might fail, leading to a final failure of the transaction, while in TiDB's pessimistic concurrency control and MySQL, the updating transaction can be successful.

## Read Committed isolation level

Starting from TiDB v4.0.0-beta, TiDB supports the Read Committed isolation level.

For historical reasons, the Read Committed isolation level of current mainstream databases is essentially the [Consistent Read isolation level defined by Oracle](https://docs.oracle.com/cd/B19306_01/server.102/b14220/consist.htm). In order to adapt to this situation, the Read Committed isolation level in TiDB pessimistic transactions is also a consistent read behavior in essence.

> **Note:**
>
> The Read Committed isolation level only takes effect in the [pessimistic transaction mode](/pessimistic-transaction.md). In the [optimistic transaction mode](/optimistic-transaction.md), setting the transaction isolation level to `Read Committed` does not take effect and transactions still use the Repeatable Read isolation level.

Starting from v6.0.0, TiDB supports using the [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) system variable to optimize the timestamp acquisition in scenarios where read-write conflicts are rare. After enabling this variable, TiDB will try to use the previous valid timestamp to read data when `SELECT` is executed. The initial value of this variable is the `start_ts` of the transaction.

- If TiDB does not encounter any data update during the read process, it returns the result to the client and the `SELECT` statement is successfully executed.
- If TiDB encounters data update during the read process:
    - If TiDB has not yet sent the result to the client, TiDB tries to acquire a new timestamp and retry this statement.
    - If TiDB has already sent partial data to the client, TiDB reports an error to the client. The amount of data sent to the client each time is controlled by `tidb_init_chunk_size` and `tidb_max_chunk_size`.

In scenarios where the `READ-COMMITTED` isolation level is used, the `SELECT` statements are many, and read-write conflicts are rare, enabling this variable can avoid the latency and cost of getting the global timestamp.

Since v6.3.0, TiDB supports optimizing the acquisition of timestamps by enabling the system variable [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630) in scenarios where point-write conflicts are few. After enabling this variable, during the execution of point-write statements, TiDB will try to use valid timestamps of the current transaction to read and lock data. TiDB will read data in the same way when [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) is enabled.

Currently, the applicable types of point-write statements include `UPDATE`, `DELETE`, and `SELECT ...... FOR UPDATE`. A point-write statement refers to a write statement that uses the primary key or unique key as a filter condition and the final execution operator contains `POINT-GET`. Currently, the three types of point-write statements have these in common: they first perform a point query based on the key value. If the key exists, they lock the key. If the key does not exist, they return an empty set.

- If the entire read process of a point-write statement does not encounter an updated data version, TiDB continues to use the timestamp of the current transaction to lock the data.
    - If a write conflict occurs due to an old timestamp during the lock acquisition process, TiDB retries the lock acquisition process by obtaining the latest global timestamp.
    - If no write conflicts or other errors occur during the lock acquisition process, the lock is acquired successfully.
- If an updated data version is encountered during the read process, TiDB tries to acquire a new timestamp and retries this statement.

In transactions with many point-write statements but a few point-write conflicts in the `READ-COMMITTED` isolation level, enabling this variable can avoid the latency and overhead of getting the global timestamp.

## Difference between TiDB and MySQL Read Committed

The MySQL Read Committed isolation level is in line with the Consistent Read features in most cases. There are also exceptions, such as [semi-consistent read](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html). This special behavior is not supported in TiDB.
