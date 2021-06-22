---
title: DEADLOCKS
summary: Learn the `DEADLOCKS` information_schema table.
---

# DEADLOCKS

The `DEADLOCKS` table shows the information of the several deadlock errors that have occurred recently on the current TiDB node.

> **Warning:**
>
> Currently, this is an experimental feature. The definition and behavior of the table structure might have major changes in future releases.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC deadlocks;
```

```sql
+--------------------+---------------------+------+------+---------+-------+
| Field              | Type                | Null | Key  | Default | Extra |
+--------------------+---------------------+------+------+---------+-------+
| DEADLOCK_ID        | bigint(21)          | NO   |      | NULL    |       |
| OCCUR_TIME         | timestamp(6)        | YES  |      | NULL    |       |
| RETRYABLE          | tinyint(1)          | NO   |      | NULL    |       |
| TRY_LOCK_TRX_ID    | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_SQL_DIGEST | varchar(64)         | YES  |      | NULL    |       |
| KEY                | text                | YES  |      | NULL    |       |
| TRX_HOLDING_LOCK   | bigint(21) unsigned | NO   |      | NULL    |       |
+--------------------+---------------------+------+------+---------+-------+
```

The `DEADLOCKS` table uses multiple rows to show the same deadlock event, and each row displays the information about one of the transactions involved in the deadlock event. If the TiDB node records multiple deadlock errors, each error is distinguished using the `DEADLOCK_ID` column. The same `DEADLOCK_ID` indicates the same deadlock event. Note that `DEADLOCK_ID` **does not guarantee global uniqueness and will not be persisted**. It only shows the same deadlock event in the same result set.

The meaning of each column field in the `DEADLOCKS` table is as follows:

* `DEADLOCK_ID`: The ID of the deadlock event. When multiple deadlock errors exist in the table, you can use this column to distinguish rows that belong to different deadlock errors.
* `OCCUR_TIME`: The time when the deadlock error occurs.
* `RETRYABLE`: Whether the deadlock error can be retried. Currently, TiDB does not support collecting the information of the retryable deadlock error, so the value of this field is always `0`. For the description of retryable deadlock errors, see the [Retryable deadlock errors](#retryable-deadlock-errors) section.
* `TRY_LOCK_TRX_ID`: The ID of the transaction that tries to acquire lock. This ID is also the `start_ts` of the transaction.
* `CURRENT_SQL_DIGEST`: The digest of the SQL statement currently being executed in the lock-acquiring transaction.
* `KEY`: The blocked key that the transaction tries to lock. The value of this field is displayed in the form of hexadecimal string.
* `TRX_HOLDING_LOCK`: The ID of the transaction that currently holds the lock on the key and causes blocking. This ID is also the `start_ts` of the transaction.

To adjust the maximum number of deadlock events that can be recorded in the `DEADLOCKS` table, adjust the [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity) configuration in the TiDB configuration file. By default, the information of the recent 10 deadlock events is recorded in the table.

## Example 1

Assume that the table definition and the initial data are as follows:

{{< copyable "sql" >}}

```sql
create table t (id int primary key, v int);
insert into t values (1, 10), (2, 20);
```

Execute the two transactions in the following order:

| Transaction 1                               | Transaction 2                               | Description                 |
|--------------------------------------|--------------------------------------|----------------------|
| `update t set v = 11 where id = 1;`  |                                      |                      |
|                                      | `update t set v = 21 where id = 2;`  |                      |
| `update t set v = 12 where id = 2;`  |                                      | Transaction 1 gets blocked.          |
|                                      | `update t set v = 22 where id = 1;`  | Transaction 2 reports a deadlock error.  |

Next, transaction 2 reports a deadlock error. At this time, query the `DEADLOCKS` table:

{{< copyable "sql" >}}

```sql
select * from information_schema.deadlocks;
```

The expected output is as follows:

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+----------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | KEY                                    | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+----------------------------------------+--------------------+
|           1 | 2021-06-04 08:22:38.765699 |         0 | 425405959304904707 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | 7480000000000000385F728000000000000002 | 425405959304904708 |
|           1 | 2021-06-04 08:22:38.765699 |         0 | 425405959304904708 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | 7480000000000000385F728000000000000001 | 425405959304904707 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+----------------------------------------+--------------------+
```

Two rows of data are generated in the `DEADLOCKS` table. The `DEADLOCK_ID` field of both rows is `1`, which means that the information in both rows belongs to the same deadlock error. The first row shows that the transaction of the ID `425405959304904707` is blocked on the key of `"7480000000000000385F728000000000000002"` by the transaction of the ID `"425405959304904708"`. The second row shows that the transaction of the ID `"425405959304904708"` is blocked on the key of `"7480000000000000385F728000000000000001"` by the transaction of the ID `425405959304904707`, which constitutes mutual blocking and forms a deadlock.

## Example 2

Assume that you query the `DEADLOCKS` table and get the following result:

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+----------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | KEY                                    | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+----------------------------------------+--------------------+
|           1 | 2021-06-04 08:22:38.765699 |         0 | 425405959304904707 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | 7480000000000000385F728000000000000002 | 425405959304904708 |
|           1 | 2021-06-04 08:22:38.765699 |         0 | 425405959304904708 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | 7480000000000000385F728000000000000001 | 425405959304904707 |
|           2 | 2021-06-04 08:22:56.795410 |         0 | 425405961664462853 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | 7480000000000000385F728000000000000002 | 425405961664462854 |
|           2 | 2021-06-04 08:22:56.795410 |         0 | 425405961664462854 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | 7480000000000000385F728000000000000003 | 425405961664462855 |
|           2 | 2021-06-04 08:22:56.795410 |         0 | 425405961664462855 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | 7480000000000000385F728000000000000001 | 425405961664462853 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+----------------------------------------+--------------------+
```

The `DEADLOCK_ID` column in the above query result shows that the first two rows together represent the information of a deadlock error, and the two transactions that wait for each other form the deadlock. The next three rows together represent another deadlock information, and the three transactions that wait in a cycle form the deadlock.

## Retryable deadlock errors

> **Note:**
>
> Currently, TiDB does not support collecting retryable deadlock errors in the `DEADLOCKS` table.

When transaction A is blocked by a lock already held by transaction B, and transaction B is directly or indirectly blocked by the lock held by the current transaction A, a deadlock error will occur. In this deadlock, there might be two cases:

+ Case 1: Transaction B might be (directly or indirectly) blocked by a lock generated by a statement that has been executed after transaction A starts and before transaction A gets blocked.
+ Case 2: Transaction B might also be blocked by the statement currently being executed in transaction A.

In case 1, TiDB will report a deadlock error to the client of transaction A and terminate the transaction.

In case 2, the statement currently being executed in transaction A will be automatically retried in TiDB. For example, suppose that transaction A executes the following statement:

{{< copyable "sql" >}}

```sql
update t set v = v + 1 where id = 1 or id = 2;
```

Transaction B executes the following two statements successively.

{{< copyable "sql" >}}

```sql
update t set v = 4 where id = 2;
update t set v = 2 where id = 1;
```

Then if transaction A locks the two rows with `id = 1` and `id = 2`, and the two transactions run in the following sequence:

1. Transaction A locks the row with `id = 1`.
2. Transaction B executes the first statement and locks the row with `id = 2`.
3. Transaction B executes the second statement and tries to lock the row with `id = 1`, which is blocked by transaction A.
4. Transaction A tries to lock the row with `id = 2` and is blocked by transaction B, which forms a deadlock.

For this case, because the statement of transaction A that blocks other transactions is also the statement currently being executed, the pessimistic lock on the current statement can be resolved (so that transaction B can continue to run), and the current statement can be retried. TiDB uses the key hash internally to determine whether this is the case.

When a retryable deadlock occurs, the internal automatic retry will not cause a transaction error, so it is transparent to the client. However, if this situation occurs frequently, the performance might be affected. When this occurs, you can see `single statement deadlock, retry statement` in the TiDB log.

## CLUSTER_DEADLOCKS

The `CLUSTER_DEADLOCKS` table returns information about the recent deadlock errors on each TiDB node in the entire cluster, which is the information of the `DEADLOCKS` table on each node combined together. `CLUSTER_DEADLOCKS` also contains an additional `INSTANCE` column to display the IP address and port of the node to distinguish between different TiDB nodes.

Note that, because `DEADLOCK_ID` does not guarantee global uniqueness, in the query result of the `CLUSTER_DEADLOCKS` table, you need to use the `INSTANCE` and `DEADLOCK_ID` together to distinguish the information of different deadlock errors in the result set.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC cluster_deadlocks;
```

```sql
+--------------------+---------------------+------+------+---------+-------+
| Field              | Type                | Null | Key  | Default | Extra |
+--------------------+---------------------+------+------+---------+-------+
| INSTANCE           | varchar(64)         | YES  |      | NULL    |       |
| DEADLOCK_ID        | bigint(21)          | NO   |      | NULL    |       |
| OCCUR_TIME         | timestamp(6)        | YES  |      | NULL    |       |
| RETRYABLE          | tinyint(1)          | NO   |      | NULL    |       |
| TRY_LOCK_TRX_ID    | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_SQL_DIGEST | varchar(64)         | YES  |      | NULL    |       |
| KEY                | text                | YES  |      | NULL    |       |
| TRX_HOLDING_LOCK   | bigint(21) unsigned | NO   |      | NULL    |       |
+--------------------+---------------------+------+------+---------+-------+
```

## SQL Digest

The `DEADLOCKS` table records the SQL digest but not the original SQL statement.

SQL digest is the hash value after the SQL normalization. To find the original SQL statement corresponding to the SQL digest, perform one of the following operations:

- For the statements executed on the current TiDB node in the recent period of time, you can find the corresponding original SQL statement in the `STATEMENTS_SUMMARY` or `STATEMENTS_SUMMARY_HISTORY` table according to the SQL digest.
- For the statements executed on all TiDB nodes in the entire cluster in the recent period of time, you can find the corresponding SQL statement in the `CLUSTER_STATEMENTS_SUMMARY` or `CLUSTER_STATEMENTS_SUMMARY_HISTORY` table according to the SQL digest.

{{< copyable "sql" >}}

```sql
select digest, digest_text from information_schema.statements_summary where digest = "f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb2";
```

```sql
+------------------------------------------------------------------+---------------------------------------+
| digest                                                           | digest_text                           |
+------------------------------------------------------------------+---------------------------------------+
| f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb2 | update `t` set `v` = ? where `id` = ? |
+------------------------------------------------------------------+---------------------------------------+
```

For detailed description of SQL digest, `STATEMENTS_SUMMARY`, `STATEMENTS_SUMMARY_HISTORY`, `CLUSTER_STATEMENTS_SUMMARY`, and `CLUSTER_STATEMENTS_SUMMARY_HISTORY` tables, see [Statement Summary Tables](/statement-summary-tables.md).
