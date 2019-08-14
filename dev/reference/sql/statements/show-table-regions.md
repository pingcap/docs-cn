---
title: SHOW TABLE REGIONS
summary: 了解如何使用 TiDB 数据库中的 SHOW TABLE REGIONS。
category: reference
---

# SHOW TABLE REGIONS

`SHOW TABLE REGIONS` 语句用于显示 TiDB 中某个表的 Region 信息。

## 语法图

```sql
index_name
SHOW TABLE [table_name] REGIONS;

SHOW TABLE [table_name] INDEX [index_name] REGIONS;
```

`SHOW TABLE REGIONS` 会返回如下列：

* `REGION_ID`：Region 的 ID。
* `START_KEY`：Region 的 Start key。
* `END_KEY`：Region 的 End key。
* `LEADER_ID`：Region 的 Leader ID。
* `LEADER_STORE_ID`：Region leader 所在的 store (TiKV) ID。
* `PEERS`：Region 所有副本的 ID。
* `SCATTERING`：Region 是否正在打散或调度中。

## 示例

```sql
test> create table t (id int key,name varchar(50), index (name));
Query OK, 0 rows affected
-- 默认新建表后会单独 split 出一个 Region 来存放该表的数据，开始时行数据和索引数据都会写到这个 Region。
test> show table t regions;
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
| REGION_ID | START_KEY | END_Key | LEADER_ID | LEADER_STORE_ID | PEERS     | SCATTERING |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
| 5         | t_43_     |         | 8         | 2               | 8, 14, 93 | 0          |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
1 row in set
-- 用 `SPLIT TABLE REGION` 语法切分行数据的 Region，下面语法把表 t 的行数据切分成 5 个 Region。
test> split table t between (0) and (100000) regions 5;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 4                  | 1.0                  |
+--------------------+----------------------+
1 row in set
test> show table t regions;
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+
| REGION_ID | START_KEY    | END_Key      | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+
| 94        | t_43_        | t_43_r_20000 | 95        | 2               | 95, 96, 97    | 0          |
| 98        | t_43_r_20000 | t_43_r_40000 | 101       | 4               | 101, 103, 102 | 0          |
| 104       | t_43_r_40000 | t_43_r_60000 | 108       | 3               | 105, 106, 108 | 0          |
| 109       | t_43_r_60000 | t_43_r_80000 | 111       | 13              | 111, 112, 113 | 0          |
| 5         | t_43_r_80000 |              | 8         | 2               | 8, 14, 93     | 0          |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+
5 rows in set
-- 用 `SPLIT TABLE REGION` 语法切分索引数据的 Region，下面语法把表 t 的索引 name 数据在 [a,z] 范围内切分成 2 个 Region。
test> split table t index name between ("a") and ("z") regions 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 2                  | 1.0                  |
+--------------------+----------------------+
1 row in set
-- 现在表 t 一共有 6 个 Region，其中 ID 是 94 的 Region 既会写入 [-inf,20000) 的行数据，也会写入索引 [l,+inf] 的 name 索引数据。
test> show table t regions;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
| REGION_ID | START_KEY                   | END_Key                     | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
| 94        | t_43_i_1_016d80000000000000 | t_43_r_20000                | 95        | 2               | 95, 96, 97    | 0          |
| 98        | t_43_r_20000                | t_43_r_40000                | 101       | 4               | 101, 103, 102 | 0          |
| 104       | t_43_r_40000                | t_43_r_60000                | 108       | 3               | 105, 106, 108 | 0          |
| 109       | t_43_r_60000                | t_43_r_80000                | 111       | 13              | 111, 112, 113 | 0          |
| 5         | t_43_r_80000                |                             | 8         | 2               | 8, 14, 93     | 0          |
| 122       | t_43_i_1_                   | t_43_i_1_016d80000000000000 | 125       | 4               | 123, 124, 125 | 0          |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
6 rows in set
```

## 另请参阅

* [SPLIT REGIONS](/reference/sql/statements/split-regions.md)
* [CREATE TABLE](/reference/sql/statements/create-table.md)
