---
title: DATA_LOCK_WAITS
summary: Learn the `DATA_LOCK_WAITS` information_schema table.
---

# DATA_LOCK_WAITS

The `DATA_LOCK_WAITS` table shows the ongoing pessimistic locks waiting on all TiKV nodes in the cluster.

> **Warning:**
>
> Currently, this is an experimental feature. The definition and behavior of the table structure might have major changes in future releases.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC data_lock_waits;
```

```sql
+------------------------+---------------------+------+------+---------+-------+
| Field                  | Type                | Null | Key  | Default | Extra |
+------------------------+---------------------+------+------+---------+-------+
| KEY                    | varchar(64)         | NO   |      | NULL    |       |
| TRX_ID                 | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_HOLDING_TRX_ID | bigint(21) unsigned | NO   |      | NULL    |       |
| SQL_DIGEST             | varchar(64)         | YES  |      | NULL    |       |
+------------------------+---------------------+------+------+---------+-------+
```

The meaning of each column field in the `DATA_LOCK_WAITS` table is as follows:

* `KEY`: The KEY that is waiting for the lock and displayed in the form of hexadecimal string.
* `TRX_ID`: The ID of the transaction that is waiting for the lock. This ID is also the `start_ts` of the transaction.
* `CURRENT_HOLDING_TRX_ID`: The ID of the transaction that currently holds the lock. This ID is also the `start_ts` of the transaction.
* `SQL_DIGEST`: The digest of the SQL statement that is currently blocked in the lock-waiting transaction.

> **Warning:**
>
> * The information in this table is obtained in real time from all TiKV nodes during the query. Currently, even if the `WHERE` condition is added, TiDB might still collect information from all TiKV nodes. If the cluster is large and the load is high, querying this table might cause a potential risk of performance jitter. Therefore, use this table according to your actual situation.
> * The information from different TiKV nodes is NOT guaranteed to be the snapshot at the same point in time.

## Example

{{< copyable "sql" >}}

```sql
select * from information_schema.data_lock_waits\G
```

```sql
*************************** 1. row ***************************
                   KEY: 7480000000000000355f728000000000000002
                TRX_ID: 425405024158875649
CURRENT_HOLDING_TRX_ID: 425405016242126849
            SQL_DIGEST: f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb22
2 rows in set (0.01 sec)
```

The above query result shows that the transaction of the ID `425405024158875649` was trying to obtain the pessimistic lock on the key `7480000000000000355f728000000000000002` when the statement with digest `"f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb22"` was being executed, but the lock on this key was held by the transaction of the ID `425405016242126849`.

## SQL Digest

The `DATA_LOCK_WAITS` table records the SQL digest but not the original SQL statement.

SQL digest is the hash value of the normalized SQL statement. To find the original SQL statement corresponding to the SQL digest, perform one of the following operations:

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
