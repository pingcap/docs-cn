---
title: DATA_LOCK_WAITS
summary: Learn the `DATA_LOCK_WAITS` information_schema table.
---

# DATA_LOCK_WAITS

The `DATA_LOCK_WAITS` table shows the ongoing pessimistic locks waiting on all TiKV nodes in the cluster.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC data_lock_waits;
```

```sql
+------------------------+---------------------+------+------+---------+-------+
| Field                  | Type                | Null | Key  | Default | Extra |
+------------------------+---------------------+------+------+---------+-------+
| KEY                    | text                | NO   |      | NULL    |       |
| KEY_INFO               | text                | YES  |      | NULL    |       |
| TRX_ID                 | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_HOLDING_TRX_ID | bigint(21) unsigned | NO   |      | NULL    |       |
| SQL_DIGEST             | varchar(64)         | YES  |      | NULL    |       |
| SQL_DIGEST_TEXT        | text                | YES  |      | NULL    |       |
+------------------------+---------------------+------+------+---------+-------+
```

The meaning of each column field in the `DATA_LOCK_WAITS` table is as follows:

* `KEY`: The key that is waiting for the lock and in the hexadecimal form.
* `KEY_INFO`: The detailed information of `KEY`. See the [KEY_INFO](#key_info) section.
* `TRX_ID`: The ID of the transaction that is waiting for the lock. This ID is also the `start_ts` of the transaction.
* `CURRENT_HOLDING_TRX_ID`: The ID of the transaction that currently holds the lock. This ID is also the `start_ts` of the transaction.
* `SQL_DIGEST`: The digest of the SQL statement that is currently blocked in the lock-waiting transaction.
* `SQL_DIGEST_TEXT`: The normalized SQL statement (the SQL statement without arguments and formats) that is currently blocked in the lock-waiting transaction. It corresponds to `SQL_DIGEST`.

> **Warning:**
>
> * Only the users with the [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) privilege can query this table.
> * The information in the `DATA_LOCK_WAITS` table is obtained in real time from all TiKV nodes during the query. Currently, even if a query has the `WHERE` condition, the information collection is still performed on all TiKV nodes. If your cluster is large and the load is high, querying this table might cause potential risk of performance jitter. Therefore, use it according to your actual situation.
> * Information from different TiKV nodes is NOT guaranteed to be snapshots of the same time.
> * The information (SQL digest) in the `SQL_DIGEST` column is the hash value calculated from the normalized SQL statement. The information in the `SQL_DIGEST_TEXT` column is internally queried from statements summary tables, so it is possible that the corresponding statement cannot be found internally. For the detailed description of SQL digests and the statements summary tables, see [Statement Summary Tables](/statement-summary-tables.md).

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

## Example

{{< copyable "sql" >}}

```sql
select * from information_schema.data_lock_waits\G
```

```sql
*************************** 1. row ***************************
                   KEY: 7480000000000000355F728000000000000001
              KEY_INFO: {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"}
                TRX_ID: 426790594290122753
CURRENT_HOLDING_TRX_ID: 426790590082449409
            SQL_DIGEST: 38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821
       SQL_DIGEST_TEXT: update `t` set `v` = `v` + ? where `id` = ?
1 row in set (0.01 sec)
```

The above query result shows that the transaction of the ID `426790594290122753` is trying to obtain the pessimistic lock on the key `"7480000000000000355F728000000000000001"` when executing a statement that has digest `"38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"` and  is in the form of ``update `t` set `v` = `v` + ? where `id` = ?``, but the lock on this key was held by the transaction of the ID `426790590082449409`.
