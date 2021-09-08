---
title: TiDB Transaction Isolation Levels
summary: Learn about the transaction isolation levels in TiDB.
aliases: ['/docs/dev/transaction-isolation-levels/','/docs/dev/reference/transactions/transaction-isolation/']
---

# TiDB Transaction Isolation Levels

Transaction isolation is one of the foundations of database transaction processing. Isolation is one of the four key properties of a transaction (commonly referred as [ACID](/glossary.md#acid)).

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
> In TiDB v3.0, the automatic retry of transactions is disabled by default. It is not recommended to enable the automatic retry because it might **break the transaction isolation level**. Refer to [Transaction Retry](/optimistic-transaction.md#automatic-retry) for details.
>
> Starting from TiDB [v3.0.8](/releases/release-3.0.8.md#tidb), newly created TiDB clusters use the [pessimistic transaction model](/pessimistic-transaction.md) by default. The current read (`for update` read) is **non-repeatable read**. Refer to [pessimistic transaction mode](/pessimistic-transaction.md) for details.

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

Starting from TiDB [v4.0.0-beta](/releases/release-4.0.0-beta.md#tidb), TiDB supports the Read Committed isolation level. 

For historical reasons, the Read Committed isolation level of current mainstream databases is essentially the [Consistent Read isolation level defined by Oracle](https://docs.oracle.com/cd/B19306_01/server.102/b14220/consist.htm). In order to adapt to this situation, the Read Committed isolation level in TiDB pessimistic transactions is also a consistent read behavior in essence.

> **Note:**
>
> The Read Committed isolation level only takes effect in the [pessimistic transaction mode](/pessimistic-transaction.md). In the [optimistic transaction mode](/optimistic-transaction.md), setting the transaction isolation level to `Read Committed` does not take effect and transactions still use the Repeatable Read isolation level.

## Difference between TiDB and MySQL Read Committed

The MySQL Read Committed isolation level is in line with the Consistent Read features in most cases. There are also exceptions, such as [semi-consistent read](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html). This special behavior is not supported in TiDB.
