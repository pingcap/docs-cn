---
title: DEADLOCKS
summary: Learn the `DEADLOCKS` INFORMATION_SCHEMA table.
---

# DEADLOCKS

The `DEADLOCKS` table shows the information of the several deadlock errors that have occurred recently on the current TiDB node.

```sql
USE INFORMATION_SCHEMA;
DESC deadlocks;
```

Thhe output is as follows:

```sql
+-------------------------+---------------------+------+------+---------+-------+
| Field                   | Type                | Null | Key  | Default | Extra |
+-------------------------+---------------------+------+------+---------+-------+
| DEADLOCK_ID             | bigint(21)          | NO   |      | NULL    |       |
| OCCUR_TIME              | timestamp(6)        | YES  |      | NULL    |       |
| RETRYABLE               | tinyint(1)          | NO   |      | NULL    |       |
| TRY_LOCK_TRX_ID         | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)         | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                | YES  |      | NULL    |       |
| KEY                     | text                | YES  |      | NULL    |       |
| KEY_INFO                | text                | YES  |      | NULL    |       |
| TRX_HOLDING_LOCK        | bigint(21) unsigned | NO   |      | NULL    |       |
+-------------------------+---------------------+------+------+---------+-------+
```

The `DEADLOCKS` table uses multiple rows to show the same deadlock event, and each row displays the information about one of the transactions involved in the deadlock event. If the TiDB node records multiple deadlock errors, each error is distinguished using the `DEADLOCK_ID` column. The same `DEADLOCK_ID` indicates the same deadlock event. Note that `DEADLOCK_ID` **does not guarantee global uniqueness and will not be persisted**. It only shows the same deadlock event in the same result set.

The meaning of each column field in the `DEADLOCKS` table is as follows:

* `DEADLOCK_ID`: The ID of the deadlock event. When multiple deadlock errors exist in the table, you can use this column to distinguish rows that belong to different deadlock errors.
* `OCCUR_TIME`: The time when the deadlock error occurs.
* `RETRYABLE`: Whether the deadlock error can be retried. For the description of retryable deadlock errors, see the [Retryable deadlock errors](#retryable-deadlock-errors) section.
* `TRY_LOCK_TRX_ID`: The ID of the transaction that tries to acquire lock. This ID is also the `start_ts` of the transaction.
* `CURRENT_SQL_DIGEST`: The digest of the SQL statement currently being executed in the lock-acquiring transaction.
* `CURRENT_SQL_DIGEST_TEXT`: The normalized form of the SQL statement that is currently being executed in the lock-acquiring transaction.
* `KEY`: The blocked key that the transaction tries to lock. The value of this field is displayed in the form of hexadecimal string.
* `KEY_INFO`: The detailed information of `KEY`. See the [`KEY_INFO`](#key_info) section.
* `TRX_HOLDING_LOCK`: The ID of the transaction that currently holds the lock on the key and causes blocking. This ID is also the `start_ts` of the transaction.

<CustomContent platform="tidb">

To adjust the maximum number of deadlock events that can be recorded in the `DEADLOCKS` table, adjust the [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity) configuration in the TiDB configuration file. By default, the information of the recent 10 deadlock events is recorded in the table.

</CustomContent>

<CustomContent platform="tidb-cloud">

The information of the recent 10 deadlock events is recorded in the `DEADLOCKS` table.

</CustomContent>

> **Warning:**
>
> * Only users with the [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) privilege can query this table.
> * The information (SQL digest) in the `CURRENT_SQL_DIGEST` column is the hash value calculated from the normalized SQL statement. The information in the `CURRENT_SQL_DIGEST_TEXT` column is internally queried from statements summary tables, so it is possible that the corresponding statement cannot be found internally. For the detailed description of SQL digests and the statements summary tables, see [Statement Summary Tables](/statement-summary-tables.md).

## `KEY_INFO`

The `KEY_INFO` column shows the detailed information of the `KEY` column. The information is shown in the JSON format. The description of each field is as follows:

* `"db_id"`: The ID of the schema to which the key belongs.
* `"db_name"`: The name of the schema to which the key belongs.
* `"table_id"`: The ID of the table to which the key belongs.
* `"table_name"`: The name of the table to which the key belongs.
* `"partition_id"`: The ID of the partition where the key is located.
* `"partition_name"`: The name of the partition where the key is located.
* `"handle_type"`: The handle type of the row key (that is, the key that stores a row of data). The possible values ​​are as follows:
    * `"int"`: The handle type is int, which means that the handle is the row ID.
    * `"common"`: The handle type is not int64. This type is shown in the non-int primary key when clustered index is enabled.
    * `"unknown"`: The handle type is currently not supported.
* `"handle_value"`: The handle value.
* `"index_id"`: The index ID to which the index key (the key that stores the index) belongs.
* `"index_name"`: The name of the index to which the index key belongs.
* `"index_values"`: The index value in the index key.

In the above fields, if the information of a field is not applicable or currently unavailable, the field is omitted in the query result. For example, the row key information does not contain `index_id`, `index_name`, and `index_values`; the index key does not contain `handle_type` and `handle_value`; non-partitioned tables do not display `partition_id` and `partition_name`; the key information in the deleted table cannot obtain schema information such as `table_name`, `db_id`, `db_name`, and `index_name`, and it is unable to distinguish whether the table is a partitioned table.

> **Note:**
>
> If a key comes from a table with partitioning enabled, and the information of the schema to which the key belongs cannot be queried due to some reasons (for example, the table to which the key belongs has been deleted) during the query, the ID of the partition to which the key belongs might be appear in the `table_id` field. This is because TiDB encodes the keys of different partitions in the same way as it encodes the keys of several independent tables. Therefore, when the schema information is missing, TiDB cannot confirm whether the key belongs to an unpartitioned table or to one partition of a table.

## Retryable deadlock errors

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is not applicable to TiDB Cloud.

</CustomContent>

<CustomContent platform="tidb">

> **Note:**
>
> The `DEADLOCKS` table does not collect the information of retryable deadlock errors by default. If you want the table to collect the retryable deadlock error information, you can adjust the value of [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable) in the TiDB configuration file.

</CustomContent>

When transaction A is blocked by a lock already held by transaction B, and transaction B is directly or indirectly blocked by the lock held by the current transaction A, a deadlock error will occur. In this deadlock, there might be two cases:

+ Case 1: Transaction B might be (directly or indirectly) blocked by a lock generated by a statement that has been executed after transaction A starts and before transaction A gets blocked.
+ Case 2: Transaction B might also be blocked by the statement currently being executed in transaction A.

In case 1, TiDB will report a deadlock error to the client of transaction A and terminate the transaction.

In case 2, the statement currently being executed in transaction A will be automatically retried in TiDB. For example, suppose that transaction A executes the following statement:

```sql
UPDATE t SET v = v + 1 WHERE id = 1 OR id = 2;
```

Transaction B executes the following two statements successively.

```sql
UPDATE t SET v = 4 WHERE id = 2;
UPDATE t SET v = 2 WHERE id = 1;
```

Then if transaction A locks the two rows with `id = 1` and `id = 2`, and the two transactions run in the following sequence:

1. Transaction A locks the row with `id = 1`.
2. Transaction B executes the first statement and locks the row with `id = 2`.
3. Transaction B executes the second statement and tries to lock the row with `id = 1`, which is blocked by transaction A.
4. Transaction A tries to lock the row with `id = 2` and is blocked by transaction B, which forms a deadlock.

For this case, because the statement of transaction A that blocks other transactions is also the statement currently being executed, the pessimistic lock on the current statement can be resolved (so that transaction B can continue to run), and the current statement can be retried. TiDB uses the key hash internally to determine whether this is the case.

When a retryable deadlock occurs, the internal automatic retry will not cause a transaction error, so it is transparent to the client. However, if this situation occurs frequently, the performance might be affected. When this occurs, you can see `single statement deadlock, retry statement` in the TiDB log.

## Example 1

Assume that the table definition and the initial data is as follows:

```sql
CREATE TABLE t (id int primary key, v int);
INSERT INTO t VALUES (1, 10), (2, 20);
```

Two transactions are executed in the following order:

| Transaction 1                               | Transaction 2                               | Description                 |
|--------------------------------------|--------------------------------------|----------------------|
| `UPDATE t SET v = 11 WHERE id = 1;`  |                                      |                      |
|                                      | `UPDATE t SET v = 21 WHERE id = 2;`  |                      |
| `UPDATE t SET v = 12 WHERE id = 2;`  |                                      | Transaction 1 gets blocked.          |
|                                      | `UPDATE t SET v = 22 WHERE id = 1;`  | Transaction 2 reports a deadlock error.  |

Next, transaction 2 reports a deadlock error. At this time, query the `DEADLOCKS` table:

```sql
SELECT * FROM INFORMATION_SCHEMA.DEADLOCKS;
```

The expected output is as follows:

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | CURRENT_SQL_DIGEST_TEXT                 | KEY                                    | KEY_INFO                                                                                           | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406216 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812829645406217 |
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406217 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812829645406216 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
```

Two rows of data are generated in the `DEADLOCKS` table. The `DEADLOCK_ID` field of both rows is `1`, which means that the information in both rows belongs to the same deadlock error. The first row shows that on the key of `"7480000000000000355F728000000000000002"`, the transaction of the ID `"426812829645406216"` is blocked by the transaction of the ID `"426812829645406217"`. The second row shows that on the key of `"7480000000000000355F728000000000000001"`, the transaction of the ID `"426812829645406217"` is blocked by the transaction of the ID `426812829645406216`, which constitutes mutual blocking and forms a deadlock.

## Example 2

Assume that you query the `DEADLOCKS` table and get the following result:

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | CURRENT_SQL_DIGEST_TEXT                 | KEY                                    | KEY_INFO                                                                                           | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406216 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812829645406217 |
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406217 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812829645406216 |
|           2 | 2021-08-05 11:09:21.252154 |         0 | 426812832017809412 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812832017809413 |
|           2 | 2021-08-05 11:09:21.252154 |         0 | 426812832017809413 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000003 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"3"} | 426812832017809414 |
|           2 | 2021-08-05 11:09:21.252154 |         0 | 426812832017809414 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812832017809412 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
```

The `DEADLOCK_ID` column in the preceding query result shows that the first two rows together represent the information of a deadlock error, and the two transactions that wait for each other form the deadlock. The next three rows together represent the information of another deadlock error, and the three transactions that wait in a cycle form the deadlock.

## CLUSTER_DEADLOCKS

The `CLUSTER_DEADLOCKS` table returns information about the recent deadlock errors on each TiDB node in the entire cluster, which is the combined information of the `DEADLOCKS` table on each node. `CLUSTER_DEADLOCKS` also includes an additional `INSTANCE` column to display the IP address and port of the node to distinguish between different TiDB nodes.

Note that, because `DEADLOCK_ID` does not guarantee global uniqueness, in the query result of the `CLUSTER_DEADLOCKS` table, you need to use the `INSTANCE` and `DEADLOCK_ID` together to distinguish the information of different deadlock errors in the result set.

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_DEADLOCKS;
```

The output is as follows:

```sql
+-------------------------+---------------------+------+------+---------+-------+
| Field                   | Type                | Null | Key  | Default | Extra |
+-------------------------+---------------------+------+------+---------+-------+
| INSTANCE                | varchar(64)         | YES  |      | NULL    |       |
| DEADLOCK_ID             | bigint(21)          | NO   |      | NULL    |       |
| OCCUR_TIME              | timestamp(6)        | YES  |      | NULL    |       |
| RETRYABLE               | tinyint(1)          | NO   |      | NULL    |       |
| TRY_LOCK_TRX_ID         | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)         | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                | YES  |      | NULL    |       |
| KEY                     | text                | YES  |      | NULL    |       |
| KEY_INFO                | text                | YES  |      | NULL    |       |
| TRX_HOLDING_LOCK        | bigint(21) unsigned | NO   |      | NULL    |       |
+-------------------------+---------------------+------+------+---------+-------+
```
