---
title: Transaction Model
summary: Learn TiDB's transaction model and its differences with MySQL.
category: reference
aliases: ['/docs/sql/transaction-model/']
---

# Transaction Model

TiDB implements an optimistic transaction model. Unlike MySQL, which uses row-level locking to avoid write conflict, in TiDB, the write conflict is checked only in the `commit` process during the execution of the statements like `Update`, `Insert`, `Delete`, and so on.

Similarly, functions such as `GET_LOCK()` and `RELEASE_LOCK()` and statements such as `SELECT .. FOR UPDATE` do not work in the same way as in MySQL.

**Note:**
>
> On the business side, remember to check the returned results of `commit` because even there is no error in the execution, there might be errors in the `commit` process.

## Differences from MySQL

### Transaction retry

By default, transactions that fail may automatically be retried by TiDB, which may lead to lost updates. This feature can be disabled by setting `tidb_retry_limit = 0`.

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

    When TiDB is in the execution of loading data, by default, a record with 20,000 rows of data is seen as a transaction for persistent storage. If a load data operation inserts more than 20,000 rows, it will be divided into multiple transactions to commit. If an error occurs in one transaction, this transaction in process will not be committed. However, transactions before that are committed successfully. In this case, a part of the load data operation is successfully inserted, and the rest of the data insertion fails. But MySQL treats a load data operation as a transaction, one error leads to the failure of the entire load data operation.
