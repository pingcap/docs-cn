---
title: DATA_LOCK_WAITS
summary: 了解 `DATA_LOCK_WAITS` information_schema 表。
---

# DATA_LOCK_WAITS

`DATA_LOCK_WAITS` 表显示集群中所有 TiKV 节点上正在进行的锁等待信息，包括悲观事务的锁等待信息和被阻塞的乐观事务的信息。

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

`DATA_LOCK_WAITS` 表中各列字段的含义如下：

* `KEY`：正在等待锁的键，以十六进制形式表示。
* `KEY_INFO`：`KEY` 的详细信息。参见 [KEY_INFO](#key_info) 部分。
* `TRX_ID`：等待锁的事务 ID。此 ID 也是事务的 `start_ts`。
* `CURRENT_HOLDING_TRX_ID`：当前持有锁的事务 ID。此 ID 也是事务的 `start_ts`。
* `SQL_DIGEST`：锁等待事务中当前被阻塞的 SQL 语句的摘要。
* `SQL_DIGEST_TEXT`：锁等待事务中当前被阻塞的规范化 SQL 语句（不含参数和格式的 SQL 语句）。它与 `SQL_DIGEST` 相对应。

> **警告：**
>
> * 只有具有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户才能查询此表。
> * 目前，对于乐观事务，`SQL_DIGEST` 和 `SQL_DIGEST_TEXT` 字段为 `null`（表示不可用）。作为解决方法，要找出导致阻塞的 SQL 语句，你可以将此表与 [`CLUSTER_TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) 联合查询，以获取乐观事务的所有 SQL 语句。
> * `DATA_LOCK_WAITS` 表中的信息是在查询期间从所有 TiKV 节点实时获取的。目前，即使查询有 `WHERE` 条件，信息收集仍会在所有 TiKV 节点上进行。如果你的集群较大且负载较高，查询此表可能会带来性能抖动的潜在风险。因此，请根据实际情况使用。
> * 来自不同 TiKV 节点的信息不保证是同一时间点的快照。
> * `SQL_DIGEST` 列中的信息（SQL 摘要）是从规范化 SQL 语句计算得出的哈希值。`SQL_DIGEST_TEXT` 列中的信息是从语句概要表内部查询的，因此可能找不到相应的语句。有关 SQL 摘要和语句概要表的详细说明，请参见[语句概要表](/statement-summary-tables.md)。

## `KEY_INFO`

`KEY_INFO` 列显示 `KEY` 列的详细信息。信息以 JSON 格式显示。各字段说明如下：

* `"db_id"`：键所属 schema 的 ID。
* `"db_name"`：键所属 schema 的名称。
* `"table_id"`：键所属表的 ID。
* `"table_name"`：键所属表的名称。
* `"partition_id"`：键所在分区的 ID。
* `"partition_name"`：键所在分区的名称。
* `"handle_type"`：行键（即存储一行数据的键）的句柄类型。可能的值如下：
    * `"int"`：句柄类型为 int，表示句柄是行 ID。
    * `"common"`：句柄类型不是 int64。这种类型在启用聚簇索引时的非整数主键中显示。
    * `"unknown"`：当前不支持的句柄类型。
* `"handle_value"`：句柄值。
* `"index_id"`：索引键（存储索引的键）所属的索引 ID。
* `"index_name"`：索引键所属的索引名称。
* `"index_values"`：索引键中的索引值。

在上述字段中，如果某个字段的信息不适用或当前不可用，则该字段在查询结果中会被省略。例如，行键信息不包含 `index_id`、`index_name` 和 `index_values`；索引键不包含 `handle_type` 和 `handle_value`；非分区表不显示 `partition_id` 和 `partition_name`；已删除表中的键信息无法获取 `table_name`、`db_id`、`db_name` 和 `index_name` 等 schema 信息，也无法区分该表是否为分区表。

> **注意：**
>
> 如果一个键来自启用了分区的表，并且在查询期间由于某些原因（例如，键所属的表已被删除）无法查询到该键所属的 schema 信息，则该键所属的分区的 ID 可能会出现在 `table_id` 字段中。这是因为 TiDB 对不同分区的键的编码方式与对几个独立表的键的编码方式相同。因此，当缺少 schema 信息时，TiDB 无法确认该键是属于非分区表还是属于某个表的一个分区。

## 示例

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

上述查询结果显示，ID 为 `426790594290122753` 的事务在执行摘要为 `"38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"` 且形式为 ``update `t` set `v` = `v` + ? where `id` = ?`` 的语句时，正在尝试获取键 `"7480000000000000355F728000000000000001"` 的悲观锁，但该键的锁被 ID 为 `426790590082449409` 的事务持有。
