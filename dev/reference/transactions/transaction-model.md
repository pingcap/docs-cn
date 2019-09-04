---
title: Transaction Model
summary: Learn TiDB's transaction model and its differences with MySQL.
category: reference
---

# Transaction Model

TiDB defaults to an optimistic transaction model. This means that unlike MySQL where statements may block waiting to acquire row-locks, TiDB will allow modifications to occur and detect the conflict at the transaction attempts to commit.

Similarly, statements such as `SELECT .. FOR UPDATE` do not work in the same way as in MySQL.

> **Note:**
>
> Experimental support for [pessimistic locking](/dev/reference/transactions/transaction-pessimistic.md) is now available. When enabled, TiDB will behave behave similar to the InnoDB storage engine.

## Differences from MySQL

### Transaction retry

While the transaction retry is not enabled by default, TiDB can automatically retry failed transactions when `tidb_disable_txn_auto_retry = off`. This feature is disabled by default because retry might lead to lost updates.

### Large transactions

Due to the distributed, 2-phase commit requirement of TiDB, large transactions that modify data can be particularly problematic. TiDB intentionally sets some limits on transaction sizes to reduce this impact:

* A transaction is limited to 5000 SQL statements (by default)
* Each Key-Value entry is no more than 6MB
* The total number of Key-Value entries is no more than 300,000
* The total size of Key-Value entries is no more than 100MB

### Small transactions

Since each transaction in TiDB requires two round trips to the PD leader, small transactions may have higher latencies in TiDB than MySQL. As a hypothetical example, the following query could be improved by moving from `auto_commit` to using an explicit transaction:

```sql
# original version with auto_commit
UPDATE my_table SET a='new_value' WHERE id = 1;
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;

# improved version
START TRANSACTION;
UPDATE my_table SET a='new_value' WHERE id = 1;
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;
COMMIT;
```

### SELECT .. FOR UPDATE

Due to optimistic locking, `SELECT .. FOR UPDATE` statements do not block other sessions from modifying data. Instead, the `SELECT .. FOR UPDATE` statement will cause the transaction to fail if rows have been modified by another transaction. Similarly, the `SELECT .. FOR UPDATE` statement disables any transaction retry.

### Single-threaded or latency-sensitive workloads

Due to its distributed nature, workloads that are single-threaded or latency-sensitive may perform worse in TiDB when compared to a single-instance deployment of MySQL. This difference is similar to the case of small transactions being potentially slower in TiDB.

### Load data

+ Syntax:

    ```
    LOAD DATA LOCAL INFILE 'file_name' INTO TABLE table_name
        {FIELDS | COLUMNS} TERMINATED BY 'string' ENCLOSED BY 'char' ESCAPED BY 'char'
        LINES STARTING BY 'string' TERMINATED BY 'string'
        IGNORE n LINES
        (col_name ...);
    ```

    Currently, the supported `ESCAPED BY` characters are: `/\/\`.

+ Transaction

    When TiDB executes the `LOAD DATA` operation, a record with 20,000 rows of data is seen as a transaction for persistent storage by default. If one `LOAD DATA` operation inserts more than 20,000 rows, it is divided into multiple transactions to commit. If an error occurs in one transaction, this transaction in process is not committed. However, transactions before that are committed successfully. In this case, a part of the `LOAD DATA` operation is successfully inserted, and the rest of the data insertion fails. But MySQL treats a `LOAD DATA` operation as one transaction, one error leads to the failure of the entire `LOAD DATA` operation.

    > **Warning:**
    >
    > The `LOAD DATA` operation in TiDB by default splits transactions and commits them in batches. However, this operation is at the expense of breaking the atomicity and isolation of the transaction. When performing this operation, you must ensure that there are **no other** ongoing operations on the table. When an error occurs, **manual intervention is required to check the consistency and integrity of the data**. Therefore, it is not recommended to set this variable in a production environment.
