---
title: SHOW TABLE REGIONS
summary: 了解如何使用 TiDB 数据库中的 SHOW TABLE REGIONS。
category: reference
---

# SHOW TABLE REGIONS

`SHOW TABLE REGIONS` 语句用于显示 TiDB 中某个表的 Region 信息。

## 语法图

```sql
SHOW TABLE [table_name] REGIONS [WhereClauseOptional];

SHOW TABLE [table_name] INDEX [index_name] REGIONS [WhereClauseOptional];
```

`SHOW TABLE REGIONS` 会返回如下列：

* `REGION_ID`：Region 的 ID。
* `START_KEY`：Region 的 Start key。
* `END_KEY`：Region 的 End key。
* `LEADER_ID`：Region 的 Leader ID。
* `LEADER_STORE_ID`：Region leader 所在的 store (TiKV) ID。
* `PEERS`：Region 所有副本的 ID。
* `SCATTERING`：Region 是否正在调度中。1 表示正在调度。
* `WRITTEN_BYTES`：估算的 Region 在 1 个心跳周期内的写入数据量大小，单位是 byte。
* `READ_BYTES`：估算的 Region 在 1 个心跳周期内的读数据量大小，单位是 byte。
* `APPROXIMATE_SIZE(MB)`：估算的 Region 的数据量大小，单位是 MB。
* `APPROXIMATE_KEYS`：估算的 Region 内 Key 的个数。

注意，`WRITTEN_BYTES`，`READ_BYTES`，`APPROXIMATE_SIZE(MB)`，`APPROXIMATE_KEYS` 的值是 PD 根据 Region 的心跳汇报信息统计，估算出来的数据，所以不是精确的数据。

## 示例

```sql
test> create table t (id int key,name varchar(50), index (name));
Query OK, 0 rows affected

-- 默认新建表后会单独 split 出一个 Region 来存放该表的数据，开始时行数据和索引数据都会写到这个 Region。
test> show table t regions;
+-----------+-----------+---------+-----------+-----------------+-----------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS     | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+---------------+------------+----------------------+------------------+
| 3         | t_43_     |         | 73        | 9               | 5, 73, 93 | 0          | 35            | 0          | 1                    | 0                |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+---------------+------------+----------------------+------------------+
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
-- TOTAL_SPLIT_REGION 表示新切的 region 数量，这是新切了 5 个 region.
-- SCATTER_FINISH_RATIO 表示新切的 region 的打散成功率，1.0 表示都已经打散了。

-- 表 t 现在一共有 6 个 Region，其中 102、106、110、114、3 用来存行数据，Region 98 用来存索引数据。
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

-- Region 102 的 START_KEY 和 END_KEY 中，t_43 是表数据前缀和 table ID，_r 是表 t record 数据的前缀，索引数据的前缀是 _i，
-- 所以 Region 102 的 START_KEY 和 END_KEY 表示用来存储 [-inf, 20000) 之前的 record 数据。其他 Region (103, 109, 113, 2) 的存储范围依次类推。
-- Region 98 用来存储索引数据存储。表 t 索引数据的起始 key 是 t_43_i，处于 Region 98 的存储范围内。
6 rows in set

-- 查看表 t 在 store 1 上的 region，用 where 条件过滤。
test> show table t regions where leader_store_id =1;
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS        | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+
| 98        | t_43_     | t_43_r  | 99        | 1               | 99, 100, 101 | 0          | 0             | 0          | 1                    | 0                |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+


-- 用 `SPLIT TABLE REGION` 语法切分索引数据的 Region，下面语法把表 t 的索引 name 数据在 [a,z] 范围内切分成 2 个 Region。
test> split table t index name between ("a") and ("z") regions 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 2                  | 1.0                  |
+--------------------+----------------------+
1 row in set

-- 现在表 t 一共有 7 个 Region，其中 5 个 Region (102, 106, 110, 114, 3) 用来存表 t 的 record 数据，另外 2 个 Region (135, 98) 用来存 name 索引的数据。
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

## 另请参阅

* [SPLIT REGION](dev/reference/sql/statements/split-region.md)
* [CREATE TABLE](dev/reference/sql/statements/create-table.md)
