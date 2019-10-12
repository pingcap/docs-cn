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

## Examples

```sql
test> create table t (id int key,name varchar(50), index (name));
Query OK, 0 rows affected
```

After a table is created, the table data is stored in a newly split Region by default. In this initial phase, all row data and index data of the table are written into this Region.

```sql
test> show table t regions;
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
| REGION_ID | START_KEY | END_Key | LEADER_ID | LEADER_STORE_ID | PEERS     | SCATTERING |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
| 5         | t_43_     |         | 8         | 2               | 8, 14, 93 | 0          |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
1 row in set
```

In the above example, `t_43_` is the value of `START_KEY` row. In this value, `t` is the table prefix and `43` is the table ID. The value of `END_KEY` row is empty (""), which means that it is an infinite value.

Use the `SPLIT TABLE REGION` statement to split row data into five Regions.

```sql
test> split table t between (0) and (100000) regions 5;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 5                  | 1.0                  |
+--------------------+----------------------+
1 row in set
```

```sql
test> show table t regions;
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+
| 98        | t_43_r       | t_43_r_20000 | 100       | 4               | 100, 101, 102 | 0          |
| 103       | t_43_r_20000 | t_43_r_40000 | 108       | 5               | 104, 108, 107 | 0          |
| 109       | t_43_r_40000 | t_43_r_60000 | 110       | 1               | 110, 111, 112 | 0          |
| 113       | t_43_r_60000 | t_43_r_80000 | 117       | 6               | 116, 117, 118 | 0          |
| 2         | t_43_r_80000 |              | 3         | 1               | 3, 91, 92     | 0          |
| 68        | t_43_        | t_43_r       | 90        | 6               | 69, 90, 97    | 0          |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+
6 rows in set
```

In the above example:

* Table t corresponds to six Regions. In these Regions, `98`, `103`, `109`, `113`, and `2` store the row data. `68` stores the index data.
* For `START_KEY` and `END_KEY` of Region `98`, `t_43` indicates the table prefix and ID. `_r` is the prefix of the record data in table t. `_i` is the prefix of the index data.
* In Region `98`, `START_KEY` and `END_KEY` mean that record data in the range of `[-inf, 20000)` is stored. In similar way, the ranges of data storage in Regions (`103`, `109`, `113`, `2`) can also be calculated.
* Region `68` stores the index data. The start key of table t's index data is `t_43_i`, which is in the range of Region `68`.

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

Now table t corresponds to seven Regions. Five of them (`98`, `103`, `109`, `113`, `2`) store the record data of table t and another two (`125`, `68`) store the index data `name`.

```sql
test> show table t regions;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
| 98        | t_43_r                      | t_43_r_20000                | 100       | 4               | 100, 101, 102 | 0          |
| 103       | t_43_r_20000                | t_43_r_40000                | 108       | 5               | 104, 108, 107 | 0          |
| 109       | t_43_r_40000                | t_43_r_60000                | 110       | 1               | 110, 111, 112 | 0          |
| 113       | t_43_r_60000                | t_43_r_80000                | 117       | 6               | 116, 117, 118 | 0          |
| 2         | t_43_r_80000                |                             | 3         | 1               | 3, 91, 92     | 0          |
| 125       | t_43_i_1_                   | t_43_i_1_016d80000000000000 | 127       | 6               | 127, 128, 129 | 0          |
| 68        | t_43_i_1_016d80000000000000 | t_43_r                      | 90        | 6               | 69, 90, 97    | 0          |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
7 rows in set
```

To check the Region that corresponds to table t in store 1, use the `WHERE` clause:

```sql
test> show table t regions where leader_store_id =1;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
| 109       | t_43_r_40000                | t_43_r_60000                | 110       | 1               | 110, 111, 112 | 0          |
| 2         | t_43_r_80000                |                             | 3         | 1               | 3, 91, 92     | 0          |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
2 rows in set
```

## See also

* [SPLIT REGION](/v2.1/reference/sql/statements/split-region.md)
* [CREATE TABLE](/v2.1/reference/sql/statements/create-table.md)
