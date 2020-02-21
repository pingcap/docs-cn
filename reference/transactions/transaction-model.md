---
title: Transaction Model
summary: Learn TiDB's transaction model and its differences with MySQL.
category: reference
---

# Transaction Model

TiDB implements an optimistic transaction model. Unlike MySQL, which uses row-level locking to avoid write conflict, in TiDB, the write conflict is checked only in the `commit` process during the execution of the statements like `Update`, `Insert`, `Delete`, and so on.

Similarly, statements such as `SELECT .. FOR UPDATE` do not work in the same way as in MySQL. Therefore, it is important to check the returned results of `commit` statements, because even if there is no error in execution, there might be errors during the `COMMIT` process.

> **Note:**
>
> Experimental support for [pessimistic locking](/reference/transactions/transaction-pessimistic.md) is now available. When enabled, TiDB will behave behave similar to the InnoDB storage engine.

## Transaction restrictions

Due to the distributed, 2-phase commit requirement of TiDB, large transactions that modify data can be particularly problematic. TiDB intentionally sets some limits on transaction sizes to reduce this impact:

* A transaction is limited to 5000 SQL statements (by default)
* Each Key-Value entry is no more than 6MB
* The total size of Key-Value entries is no more than 100MB

### Best practices

Because each transaction in TiDB requires two round trips to the PD leader, small transactions might have higher latencies in TiDB than MySQL. As a hypothetical example, the following query could be improved by moving from `autocommit` to using an explicit transaction:

The original version with `autocommit`:

{{< copyable "sql" >}}

```sql
UPDATE my_table SET a='new_value' WHERE id = 1;
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;
```

The improved version:

{{< copyable "sql" >}}

```sql
START TRANSACTION;
UPDATE my_table SET a='new_value' WHERE id = 1;
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;
COMMIT;
```

> **Note:**
>
> The distributed resources in TiDB might not be fully used in the single-threaded workloads, so the performance of TiDB is lower than that of a single-instance deployment of MySQL. This difference is similar to the case of transactions with higher latency in TiDB.

### SELECT .. FOR UPDATE

Due to optimistic locking, `SELECT .. FOR UPDATE` statements do not block other sessions from modifying data. Instead, the `SELECT .. FOR UPDATE` statement will cause the transaction to fail if rows have been modified by another transaction. Similarly, the `SELECT .. FOR UPDATE` statement disables any transaction retry.
