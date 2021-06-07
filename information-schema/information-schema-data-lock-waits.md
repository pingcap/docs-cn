---
title: DATA_LOCK_WAITS
summary: 了解 information_schema 表 `DATA_LOCK_WAITS`。
---

# DATA_LOCK_WAITS

`DATA_LOCK_WAITS` 表展示了集群中的所有 TiKV 节点上当前正在发生的悲观锁等锁的情况。

> **警告：**
>
> 该功能目前为实验性功能，表结构的定义和行为将来可能有较大改动。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC data_lock_waits;
```

```
+------------------------+---------------------+------+------+---------+-------+
| Field                  | Type                | Null | Key  | Default | Extra |
+------------------------+---------------------+------+------+---------+-------+
| KEY                    | varchar(64)         | NO   |      | NULL    |       |
| TRX_ID                 | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_HOLDING_TRX_ID | bigint(21) unsigned | NO   |      | NULL    |       |
| SQL_DIGEST             | varchar(64)         | YES  |      | NULL    |       |
+------------------------+---------------------+------+------+---------+-------+
```

`DATA_LOCK_WAITS` 表的各列的含义如下：

* `KEY`：正在发生等锁的 KEY，以十六进制编码的形式显示。
* `TRX_ID`：正在等锁的事务的事务 ID，即 start ts。
* `CURRENT_HOLDING_TRX_ID`：当前持有锁的事务的事务 ID，即 start ts。
* `SQL_DIGEST`：当前正在等锁的事务被阻塞的 SQL 语句的 Digest。

需要注意：

* 该表中的信息在查询时实时地从所有 TiKV 节点中获取。目前即使设置了 WHERE 查询条件，也无法避免对所有 TiKV 节点都进行信息收集。
* 来自不同 TiKV 节点的信息不保证是同一时间点的快照。

## 示例

{{< copyable "sql" >}}

```sql
select * from information_schema.data_lock_waits\G
```

```
*************************** 1. row ***************************                          
                   KEY: 7480000000000000355f728000000000000002                          
                TRX_ID: 425405024158875649                                              
CURRENT_HOLDING_TRX_ID: 425405016242126849                                              
            SQL_DIGEST: f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb22
2 rows in set (0.01 sec)                                                                
```

上述结果显示，事务 ID 为 `425405024158875649` 的事务在执行 Digest 为 `"f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb22"` 的语句的过程中，试图在 `"7480000000000000355f728000000000000002"` 这个 key 上获取悲观锁，但是该 key 目前被事务 ID 为 `425405016242126849` 的事务持有。

## SQL Digest

`DATA_LOCK_WAITS` 表中会记录 SQL Digest，并不记录 SQL 原文。

SQL Digest 是 SQL 归一化之后的哈希值。对于最近一段时间内执行过的语句，可以从 `STATEMENTS_SUMMARY` 或 `STATEMENTS_SUMMARY_HISTORY` 中根据 Digest 查找到对应的归一化 SQL 的原文：

{{< copyable "sql" >}}

```sql
select digest, digest_text from information_schema.statements_summary where digest = "f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb2";
```

```
+------------------------------------------------------------------+---------------------------------------+
| digest                                                           | digest_text                           |
+------------------------------------------------------------------+---------------------------------------+
| f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb2 | update `t` set `v` = ? where `id` = ? |
+------------------------------------------------------------------+---------------------------------------+
```

关于 SQL Digest 和 `STATEMENTS_SUMMARY`、`STATEMENTS_SUMMARY_HISTORY` 表的详细说明请参阅 [Statement Summary Tables](/statement-summary-tables)。
