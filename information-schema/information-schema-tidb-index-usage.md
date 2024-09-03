---
title: TIDB_INDEX_USAGE
summary: 了解 INFORMATION_SCHEMA 表 `TIDB_INDEX_USAGE`。
---

# TIDB_INDEX_USAGE

TiDB 从 v8.0.0 开始提供 `TIDB_INDEX_USAGE` 表，你可以使用该表查看当前 TiDB 节点中所有索引的访问统计信息。在 SQL 语句执行时，TiDB 默认维护访问索引有关的统计信息，可以通过修改配置项 [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info) 或者系统变量 [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) 将其关闭。

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_INDEX_USAGE;
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
* `INDEX_NAME`：索引的名称。
* `QUERY_TOTAL`：访问该索引的语句总数。
* `KV_REQ_TOTAL`：访问该索引时产生的 KV 请求总数。
* `ROWS_ACCESS_TOTAL`：访问该索引时扫描的总行数。
* `PERCENTAGE_ACCESS_0`：行访问比例（访问行数占表总行数的百分比）为 0 的次数。
* `PERCENTAGE_ACCESS_0_1`：行访问比例为 0 到 1% 的次数。
* `PERCENTAGE_ACCESS_1_10`：行访问比例为 1% 到 10% 的次数。
* `PERCENTAGE_ACCESS_10_20`：行访问比例为 10% 到 20% 的次数。
* `PERCENTAGE_ACCESS_20_50`：行访问比例为 20% 到 50% 的次数。
* `PERCENTAGE_ACCESS_50_100`：行访问比例为 50% 到 100% 的次数。
* `PERCENTAGE_ACCESS_100`：行访问比例为 100% 的次数。
* `LAST_ACCESS_TIME`：最近一次访问该索引的时间。

## CLUSTER_TIDB_INDEX_USAGE

`TIDB_INDEX_USAGE` 表仅提供单个 TiDB 节点中所有索引的访问统计信息。如果要查看整个集群上所有 TiDB 节点中索引的访问统计信息，需要查询 `CLUSTER_TIDB_INDEX_USAGE` 表。

与 `TIDB_INDEX_USAGE` 表的查询结果相比，`CLUSTER_TIDB_INDEX_USAGE` 表的查询结果额外包含了 `INSTANCE` 字段。`INSTANCE` 字段展示了集群中各节点的 IP 地址和端口，用于区分不同节点上的统计信息。

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_TIDB_INDEX_USAGE;
```

输出结果如下：

```sql
+--------------------------+-------------+------+------+---------+-------+
| Field                    | Type        | Null | Key  | Default | Extra |
+--------------------------+-------------+------+------+---------+-------+
| INSTANCE                 | varchar(64) | YES  |      | NULL    |       |
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
15 rows in set (0.00 sec)
```

## 使用限制

- `TIDB_INDEX_USAGE` 表中的数据可能存在最多 5 分钟的延迟。
- 在 TiDB 重启后，`TIDB_INDEX_USAGE` 表中的数据会被清空。

## 更多阅读

- [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)
