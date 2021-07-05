---
title: DATA_LOCK_WAITS
summary: 了解 information_schema 表 `DATA_LOCK_WAITS`。
---

# DATA_LOCK_WAITS

`DATA_LOCK_WAITS` 表展示了集群中所有 TiKV 节点上当前正在发生的悲观锁等锁的情况。

> **警告：**
>
> 该功能目前为实验性功能，表结构的定义和行为在未来版本中可能有较大改动。

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

`DATA_LOCK_WAITS` 表中各列的字段含义如下：

* `KEY`：正在发生等锁的 KEY，以十六进制编码的形式显示。
* `TRX_ID`：正在等锁的事务 ID，即 `start_ts`。
* `CURRENT_HOLDING_TRX_ID`：当前持有锁的事务 ID，即 `start_ts`。
* `SQL_DIGEST`：当前正在等锁的事务中被阻塞的 SQL 语句的 Digest。

> **警告：**
>
> * 该表中的信息是在查询时，从所有 TiKV 节点实时获取的。目前，即使加上了 `WHERE` 查询条件，也无法避免对所有 TiKV 节点都进行信息收集。如果集群规模很大、负载很高，查询该表有造成性能抖动的潜在风险，因此请根据实际情况使用。
> * 来自不同 TiKV 节点的信息不一定是同一时间点的快照。

## 示例

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

以上查询结果显示，ID 为 `425405024158875649` 的事务在执行 Digest 为 `"f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb22"` 的语句的过程中，试图在 `"7480000000000000355f728000000000000002"` 这个 key 上获取悲观锁，但是该 key 上的锁目前被 ID 为 `425405016242126849` 的事务持有。

## SQL Digest

`DATA_LOCK_WAITS` 表中会记录 SQL Digest，并不记录 SQL 原文。

SQL Digest 是 SQL 归一化之后的哈希值。如需查找 SQL Digest 对应的 SQL 原文，请进行以下操作之一：

- 对于当前 TiDB 节点在最近一段时间内执行过的语句，你可以从 `STATEMENTS_SUMMARY` 或 `STATEMENTS_SUMMARY_HISTORY` 中根据 SQL Digest 查找到对应的 SQL 原文。
- 对于整个集群所有 TiDB 节点在最近一段时间内执行过的语句，你可以从 `CLUSTER_STATEMENTS_SUMMARY` 或`CLUSTER_STATEMENTS_SUMMARY_HISTORY` 中根据 SQL Digest 查找到对应的 SQL 原文。

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

关于 SQL Digest 和 `STATEMENTS_SUMMARY`、`STATEMENTS_SUMMARY_HISTORY` 、`CLUSTER_STATEMENTS_SUMMARY`、`CLUSTER_STATEMENTS_SUMMARY_HISTORY` 表的详细说明，请参阅 [Statement Summary Tables](/statement-summary-tables.md)。
