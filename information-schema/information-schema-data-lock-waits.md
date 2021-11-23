---
title: DATA_LOCK_WAITS
summary: 了解 information_schema 表 `DATA_LOCK_WAITS`。
---

# DATA_LOCK_WAITS

`DATA_LOCK_WAITS` 表展示了集群中所有 TiKV 节点上当前正在发生的悲观锁等锁的情况。

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

`DATA_LOCK_WAITS` 表中各列的字段含义如下：

* `KEY`：正在发生等锁的 key，以十六进制编码的形式显示。
* `KEY_INFO`：对 `KEY` 进行解读得出的一些详细信息，见 [KEY_INFO](#key_info)。
* `TRX_ID`：正在等锁的事务 ID，即 `start_ts`。
* `CURRENT_HOLDING_TRX_ID`：当前持有锁的事务 ID，即 `start_ts`。
* `SQL_DIGEST`：当前正在等锁的事务中被阻塞的 SQL 语句的 Digest。
* `SQL_DIGEST_TEXT`：当前正在等锁的事务中被阻塞的 SQL 语句的归一化形式，即去除了参数和格式的 SQL 语句。与 `SQL_DIGEST` 对应。

> **警告：**
>
> * 仅拥有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户可以查询该表。
> * 目前该表仅能记录**悲观锁等锁**的情况，如果乐观事务（如 autocommit 的事务）被悲观锁阻塞，这一表中不会显示相应等锁信息。 
> * `DATA_LOCK_WAITS` 表中的信息是在查询时，从所有 TiKV 节点实时获取的。目前，即使加上了 `WHERE` 查询条件，也无法避免对所有 TiKV 节点都进行信息收集。如果集群规模很大、负载很高，查询该表有造成性能抖动的潜在风险，因此请根据实际情况使用。
> * 来自不同 TiKV 节点的信息不能保证是同一时间点的快照。
> * `SQL_DIGEST` 列中的信息（SQL Digest）为 SQL 语句进行归一化后计算得到的哈希值。`SQL_DIGEST_TEXT` 列中的信息为内部从 Statements Summary 系列表中查询得到，因而存在内部查询不到对应语句的可能性。关于 SQL Digest 和 Statements Summary 相关表的详细说明，请参阅[Statement Summary Tables](/statement-summary-tables.md)。

## `KEY_INFO`

`KEY_INFO` 列中展示了对 `KEY` 列中所给出的 key 的详细信息，以 JSON 格式给出。其包含的信息如下：

* `"db_id"`：该 key 所属的数据库（schema）的 ID。
* `"db_name"`：该 key 所属的数据库（schema）的名称。
* `"table_id"`：该 key 所属的表的 ID。
* `"table_name"`：该 key 所属的表的名称。
* `"partition_id"`：该 key 所在的分区（partition）的 ID。
* `"partition_name"`：该 key 所在的分区（partition）的名称。
* `"handle_type"`：该 row key （即储存一行数据的 key）的 handle 类型，其可能的值有：
    * `"int"`：handle 为 int 类型，即 handle 为 row ID
    * `"common"`：非 int64 类型的 handle，在启用 clustered index 时非 int 类型的主键会显示为此类型
    * `"unknown"`：当前暂不支持的 handle 类型
* `"handle_value"`：handle 的值。
* `"index_id"`：该 index key （即储存索引的 key）所属的 index ID。
* `"index_name"`：该 index key 所属的 index 名称。
* `"index_values"`：该 index key 中的 index value。

其中，不适用或当前无法查询到的信息会被省略。比如，row key 的信息中不会包含 `index_id`、`index_name` 和 `index_values`；index key 不会包含 `handle_type` 和 `handle_value`；非分区表不会显示 `partition_id` 和 `partition_name`；已经被删除掉的表中的 key 的信息无法获取 `table_name`、`db_id`、`db_name`、`index_name` 等 schema 信息，且无法区分是否为分区表。

> **注意：**
>
> 如果一个 key 来自一张启用了分区的表，而在查询时，由于某些原因（例如，其所属的表已经被删除）导致无法查询其所属的 schema 信息，则其所属的分区的 ID 可能会出现在 `table_id` 字段中。这是因为，TiDB 对不同分区的 key 的编码方式与对几张独立的表的 key 的编码方式一致，因而在缺失 schema 信息时无法确认该 key 属于一张未分区的表还是某张表的一个分区。

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

以上查询结果显示，ID 为 `426790594290122753` 的事务在执行 Digest 为 `"38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"`、形如 ``update `t` set `v` = `v` + ? where `id` = ?`` 的语句的过程中，试图在 `"7480000000000000355F728000000000000001"` 这个 key 上获取悲观锁，但是该 key 上的锁目前被 ID 为 `426790590082449409` 的事务持有。
