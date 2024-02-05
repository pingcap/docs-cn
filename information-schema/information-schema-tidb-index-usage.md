---
title: TIDB_INDEX_USAGE
summary: 了解 information_schema 表 `TIDB_INDEX_USAGE`。
---

# TIDB_INDEX_USAGE

`TIDB_INDEX_USAGE` 记录了当前节点所有 Index 的访问统计信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tidb_index_usage;
```

```sql
+--------------------------+-------------+------+------+---------+-------+
| Field                    | Type        | Null | Key  | Default | Extra |
+--------------------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA             | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME               | varchar(64) | YES  |      | NULL    |       |
| INDEX_NAME               | varchar(64) | YES  |      | NULL    |       |
| QUERY_TOTAL              | bigint(21)  | YES  |      | NULL    |       |
| KV_REQ_TOTAL             | bigint(21)  | YES  |      | NULL    |       |
| ROWS_ACCESS_TOTAL        | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0      | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0_1    | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_1_10   | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_10_20  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_20_50  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_50_100 | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_100    | bigint(21)  | YES  |      | NULL    |       |
| LAST_ACCESS_TIME         | datetime    | YES  |      | NULL    |       |
+--------------------------+-------------+------+------+---------+-------+
14 rows in set (0.00 sec)
```

`TIDB_INDEX_USAGE` 表中列的含义如下：

* `TABLE_SCHEMA`：索引所在表的所属数据库的名称。
* `TABLE_NAME`：索引所在表的名称。
* `INDEX_NAME`：索引的名称
* `QUERY_TOTAL`：访问该索引的语句总数。
* `KV_REQ_TOTAL`：访问该索引时产生的 KV 请求总数。
* `ROWS_ACCESS_TOTAL`：访问该索引时扫描的总行数。
* `PERCENTAGE_ACCESS_0`：访问行数占表总行数比例为 0 的次数。
* `PERCENTAGE_ACCESS_0_1`：访问行数占总行数比例为 0 到 1% 的次数。
* `PERCENTAGE_ACCESS_1_10`：访问行数占总行数比例为 1% 到 10% 的次数。
* `PERCENTAGE_ACCESS_10_20`：访问行数占总行数比例为 10% 到 20% 的次数。
* `PERCENTAGE_ACCESS_20_50`：访问行数占总行数比例为 20% 到 50% 的次数。
* `PERCENTAGE_ACCESS_50_100`：访问行数占总行数比例为 50% 到 100% 的次数。
* `PERCENTAGE_ACCESS_100`：访问行数占总行数比例为 100% 的次数。
* `LAST_ACCESS_TIME`：最后一次访问该索引的时间。

# 限制

- `TIDB_INDEX_USAGE` 表中的数据可能有至多 5 分钟的延迟。
- 在 TiDB 重启后，`TIDB_INDEX_USAGE` 表中的数据会被清空。
