---
title: TIDB_INDEX_USAGE
summary: 了解 `TIDB_INDEX_USAGE` INFORMATION_SCHEMA 表。
---

# TIDB_INDEX_USAGE

<CustomContent platform="tidb">

从 v8.0.0 开始，TiDB 提供了 `TIDB_INDEX_USAGE` 表。你可以使用 `TIDB_INDEX_USAGE` 获取当前 TiDB 节点上所有索引的使用统计信息。默认情况下，TiDB 在执行 SQL 语句时会收集这些索引使用统计信息。你可以通过关闭 [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info) 配置项或 [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) 系统变量来禁用此功能。

</CustomContent>

<CustomContent platform="tidb-cloud">

从 v8.0.0 开始，TiDB 提供了 `TIDB_INDEX_USAGE` 表。你可以使用 `TIDB_INDEX_USAGE` 获取当前 TiDB 节点上所有索引的使用统计信息。默认情况下，TiDB 在执行 SQL 语句时会收集这些索引使用统计信息。你可以通过关闭 [`instance.tidb_enable_collect_execution_info`](https://docs.pingcap.com/tidb/v8.0/tidb-configuration-file#tidb_enable_collect_execution_info) 配置项或 [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) 系统变量来禁用此功能。

</CustomContent>

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

`TIDB_INDEX_USAGE` 表中的列说明如下：

* `TABLE_SCHEMA`：包含索引的表所属的数据库名称。
* `TABLE_NAME`：包含索引的表名。
* `INDEX_NAME`：索引名称。
* `QUERY_TOTAL`：访问该索引的语句总数。
* `KV_REQ_TOTAL`：访问该索引时生成的 KV 请求总数。
* `ROWS_ACCESS_TOTAL`：访问该索引时扫描的行数总和。
* `PERCENTAGE_ACCESS_0`：行访问比例（访问的行数占表总行数的百分比）为 0 的次数。
* `PERCENTAGE_ACCESS_0_1`：行访问比例在 0% 到 1% 之间的次数。
* `PERCENTAGE_ACCESS_1_10`：行访问比例在 1% 到 10% 之间的次数。
* `PERCENTAGE_ACCESS_10_20`：行访问比例在 10% 到 20% 之间的次数。
* `PERCENTAGE_ACCESS_20_50`：行访问比例在 20% 到 50% 之间的次数。
* `PERCENTAGE_ACCESS_50_100`：行访问比例在 50% 到 100% 之间的次数。
* `PERCENTAGE_ACCESS_100`：行访问比例为 100% 的次数。
* `LAST_ACCESS_TIME`：最近一次访问该索引的时间。

## CLUSTER_TIDB_INDEX_USAGE

`TIDB_INDEX_USAGE` 表仅提供单个 TiDB 节点上所有索引的使用统计信息。要获取集群中所有 TiDB 节点的索引使用统计信息，你需要查询 `CLUSTER_TIDB_INDEX_USAGE` 表。

与 `TIDB_INDEX_USAGE` 表相比，`CLUSTER_TIDB_INDEX_USAGE` 表的查询结果多了一个 `INSTANCE` 字段。该字段显示集群中每个节点的 IP 地址和端口，帮助你区分不同节点的统计信息。

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

## 限制

- `TIDB_INDEX_USAGE` 表中的数据可能会有最多 5 分钟的延迟。
- TiDB 重启后，`TIDB_INDEX_USAGE` 表中的数据会被清空。
- TiDB 只有在表有有效的统计信息时才会记录该表的索引使用情况。

## 更多信息

- [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)
