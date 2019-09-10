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
-- 默认新建表后会单独切分出一个 Region 来存放该表的数据，开始时行数据和索引数据都会写到这个 Region。
test> show table t regions;
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
| REGION_ID | START_KEY | END_Key | LEADER_ID | LEADER_STORE_ID | PEERS     | SCATTERING |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
| 5         | t_43_     |         | 8         | 2               | 8, 14, 93 | 0          |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
-- 上面 START_KEY 列的值 t_43_ 中，t 是表数据的前缀，43 是表 t 的 table ID。
-- END_KEY 列的值为空（""）表示无穷大。
1 row in set
-- 用 `SPLIT TABLE REGION` 语法切分行数据的 Region，下面语法把表 t 的行数据切分成 5 个 Region。
test> split table t between (0) and (100000) regions 5;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 5                  | 1.0                  |
+--------------------+----------------------+
1 row in set
-- 表 t 现在一共有 6 个 Region，其中 98、103、109、113、2 用来存行数据，Region 68 用来存索引数据。
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
-- Region 98 的 START_KEY 和 END_KEY 中，t_43 是表数据前缀和 table ID，_r 是表 t record 数据的前缀，索引数据的前缀是 _i，
-- 所以 Region 98 的 START_KEY 和 END_KEY 表示用来存储 [-inf, 20000) 之前的 record 数据。其他 Region (103, 109, 113, 2) 的存储范围依次类推。
-- Region 68 用来存储索引数据存储。表 t 索引数据的起始 key 是 t_43_i，处于 Region 68 的存储范围内。

-- 用 `SPLIT TABLE REGION` 语法切分索引数据的 Region，下面语法把表 t 的索引 name 数据在 [a,z] 范围内切分成 2 个 Region。
test> split table t index name between ("a") and ("z") regions 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 2                  | 1.0                  |
+--------------------+----------------------+
1 row in set
-- 现在表 t 一共有 7 个 Region，其中 5 个 Region (98, 103, 109, 113, 2) 用来存表 t 的 record 数据，另外 2 个 Region (125, 68) 用来存 name 索引的数据。
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

## 另请参阅

* [SPLIT REGION](/v2.1/reference/sql/statements/split-region.md)
* [CREATE TABLE](/v2.1/reference/sql/statements/create-table.md)
