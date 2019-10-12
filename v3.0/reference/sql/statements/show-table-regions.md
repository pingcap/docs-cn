---
title: SHOW TABLE REGIONS
summary: Learn how to use SHOW TABLE REGIONS in TiDB.
category: reference
---

# SHOW TABLE REGIONS

The `SHOW TABLE REGIONS` statement is used to show the Region information of a table in TiDB.

## Synopsis

```sql
SHOW TABLE [table_name] REGIONS [WhereClauseOptional];
SHOW TABLE [table_name] INDEX [index_name] REGIONS [WhereClauseOptional];
```

Executing `SHOW TABLE REGIONS` returns the following columns:

* `REGION_ID`: The Region ID.
* `START_KEY`: The start key of the Region.
* `END_KEY`: The end key of the Region.
* `LEADER_ID`: The Leader ID of the Region.
* `LEADER_STORE_ID`: The ID of the store (TiKV) where the Region leader is located.
* `PEERS`: The IDs of all Region replicas.
* `SCATTERING`: Whether the Region is being scheduled. `1` means true.
* `WRITTEN_BYTES`: The estimated amount of data written into the Region within one heartbeat cycle. The unit is byte.
* `READ_BYTES`: The estimated amount of data read from the Region within one heartbeat cycle. The unit is byte.
* `APPROXIMATE_SIZE(MB)`: The estimated amount of data in the Region. The unit is megabytes (MB).
* `APPROXIMATE_KEYS`: The estimated number of Keys in the Region.

> **Note:**
>
> The values of `WRITTEN_BYTES`, `READ_BYTES`, `APPROXIMATE_SIZE(MB)`, `APPROXIMATE_KEYS` are not accurate data. They are estimated data from PD based on the heartbeat information that PD receives from the Region.

## Examples

```sql
test> create table t (id int key,name varchar(50), index (name));
Query OK, 0 rows affected
```

After a table is created, the table data is stored in a newly split Region by default. In this initial phase, all row data and index data of the table are written into this Region.

```sql
test> show table t regions;
+-----------+-----------+---------+-----------+-----------------+-----------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS     | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+---------------+------------+----------------------+------------------+
| 3         | t_43_     |         | 73        | 9               | 5, 73, 93 | 0          | 35            | 0          | 1                    | 0                |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+---------------+------------+----------------------+------------------+
1 row in set
```

In the above result, `t_43_` is the value of `START_KEY` row. In this value, `t` is the table prefix and `43` is the table ID. The value of `END_KEY` row is empty (""), which means that it is an infinite value.

Use the `SPLIT TABLE REGION` statement to split row data into five Regions.

```sql
test> split table t between (0) and (100000) regions 5;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 5                  | 1.0                  |
+--------------------+----------------------+
```

In the above example:

* `TOTAL_SPLIT_REGION` indicates the number of newly split Regions. In this example, the number is 5.
* `SCATTER_FINISH_RATIO` indicates the rate at which the newly split Regions are successfully scattered. `1.0` means that all Regions are scattered.

```sql
test> show table t regions;
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
| 102       | t_43_r       | t_43_r_20000 | 118       | 7               | 105, 118, 119 | 0          | 0             | 0          | 1                    | 0                |
| 106       | t_43_r_20000 | t_43_r_40000 | 120       | 7               | 107, 108, 120 | 0          | 23            | 0          | 1                    | 0                |
| 110       | t_43_r_40000 | t_43_r_60000 | 112       | 9               | 112, 113, 121 | 0          | 0             | 0          | 1                    | 0                |
| 114       | t_43_r_60000 | t_43_r_80000 | 122       | 7               | 115, 122, 123 | 0          | 35            | 0          | 1                    | 0                |
| 3         | t_43_r_80000 |              | 93        | 8               | 5, 73, 93     | 0          | 0             | 0          | 1                    | 0                |
| 98        | t_43_        | t_43_r       | 99        | 1               | 99, 100, 101  | 0          | 0             | 0          | 1                    | 0                |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
6 rows in set
```

In the above example:

* Table t corresponds to six Regions. In these Regions, `102`, `106`, `110`, `114`, and `3` store the row data and `98` stores the index data.
* For `START_KEY` and `END_KEY` of Region `102`, `t_43` indicates the table prefix and ID. `_r` is the prefix of the record data in table t. `_i` is the prefix of the index data.
* In Region `102`, `START_KEY` and `END_KEY` mean that record data in the range of `[-inf, 20000)` is stored. In similar way, the ranges of data storage in Regions (`103`, `109`, `113`, `2`) can also be calculated.
* Region `98` stores the index data. The start key of table t's index data is `t_43_i`, which is in the range of Region `98`.

To check the Region that corresponds to table t in store 1, use the `WHERE` clause:

```sql
test> show table t regions where leader_store_id =1;
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS        | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+
| 98        | t_43_     | t_43_r  | 99        | 1               | 99, 100, 101 | 0          | 0             | 0          | 1                    | 0                |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+
```

Use `SPLIT TABLE REGION` to split the index data into Regions. In the following example, the index data `name` of table t is split into two Regions in the range of `[a,z]`.

```sql
test> split table t index name between ("a") and ("z") regions 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 2                  | 1.0                  |
+--------------------+----------------------+
1 row in set
```

Now table t corresponds to seven Regions. Five of them (`102`, `106`, `110`, `114`, `3`) store the record data of table t and another two (`135`, `98`) store the index data `name`.

```sql
test> show table t regions;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
| 102       | t_43_r                      | t_43_r_20000                | 118       | 7               | 105, 118, 119 | 0          | 0             | 0          | 1                    | 0                |
| 106       | t_43_r_20000                | t_43_r_40000                | 120       | 7               | 108, 120, 126 | 0          | 0             | 0          | 1                    | 0                |
| 110       | t_43_r_40000                | t_43_r_60000                | 112       | 9               | 112, 113, 121 | 0          | 0             | 0          | 1                    | 0                |
| 114       | t_43_r_60000                | t_43_r_80000                | 122       | 7               | 115, 122, 123 | 0          | 35            | 0          | 1                    | 0                |
| 3         | t_43_r_80000                |                             | 93        | 8               | 73, 93, 128   | 0          | 0             | 0          | 1                    | 0                |
| 135       | t_43_i_1_                   | t_43_i_1_016d80000000000000 | 139       | 2               | 138, 139, 140 | 0          | 35            | 0          | 1                    | 0                |
| 98        | t_43_i_1_016d80000000000000 | t_43_r                      | 99        | 1               | 99, 100, 101  | 0          | 0             | 0          | 1                    | 0                |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
7 rows in set
```

## See also

* [SPLIT REGION](/v3.0/reference/sql/statements/split-region.md)
* [CREATE TABLE](/v3.0/reference/sql/statements/create-table.md)
