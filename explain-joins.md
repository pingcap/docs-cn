---
title: 用 EXPLAIN 查看 JOIN 查询的执行计划
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 用 EXPLAIN 查看 JOIN 查询的执行计划

SQL 查询中可能会使用 JOIN 进行表连接，可以通过 `EXPLAIN` 语句来查看 JOIN 查询的执行计划。本文提供多个示例，以帮助用户理解表连接查询是如何执行的。

在 TiDB 中，SQL 优化器需要确定数据表的连接顺序，且要判断对于某条特定的 SQL 语句，哪一种 Join 算法最为高效。

本文档使用的示例数据如下:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id BIGINT NOT NULL PRIMARY KEY auto_increment, pad1 BLOB, pad2 BLOB, pad3 BLOB, int_col INT NOT NULL DEFAULT 0);
CREATE TABLE t2 (id BIGINT NOT NULL PRIMARY KEY auto_increment, t1_id BIGINT NOT NULL, pad1 BLOB, pad2 BLOB, pad3 BLOB, INDEX(t1_id));
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM dual;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
UPDATE t1 SET int_col = 1 WHERE pad1 = (SELECT pad1 FROM t1 ORDER BY RAND() LIMIT 1);
SELECT SLEEP(1);
ANALYZE TABLE t1, t2;
```

## Index Join

如果预计需要连接的行数较少（一般小于 1 万行），推荐使用 Index Join 算法。这个算法与 MySQL 主要使用的 Join 算法类似。在下表的示例中，`TableReader_28(Build)` 算子首先读取表 `t1`，然后根据在 `t1` 中匹配到的每行数据，依次探查表 `t2` 中的数据：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id;
```

```sql
+---------------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------+
| id                              | estRows   | task      | access object                | operator info                                                                  |
+---------------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------+
| IndexJoin_10                    | 180000.00 | root      |                              | inner join, inner:IndexLookUp_9, outer key:test.t1.id, inner key:test.t2.t1_id |
| ├─TableReader_28(Build)         | 142020.00 | root      |                              | data:TableFullScan_27                                                          |
| │ └─TableFullScan_27            | 142020.00 | cop[tikv] | table:t1                     | keep order:false                                                               |
| └─IndexLookUp_9(Probe)          | 1.27      | root      |                              |                                                                                |
|   ├─IndexRangeScan_7(Build)     | 1.27      | cop[tikv] | table:t2, index:t1_id(t1_id) | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false            |
|   └─TableRowIDScan_8(Probe)     | 1.27      | cop[tikv] | table:t2                     | keep order:false                                                               |
+---------------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

Index Join 算法对内存消耗较小，但如果需要执行大量探查操作，运行速度可能会慢于其他 Join 算法。以下面这条查询语句为例：

```sql
SELECT * FROM t1 INNER JOIN t2 ON t1.id=t2.t1_id WHERE t1.pad1 = 'value' and t2.pad1='value';
```

在 Inner Join 操作中，TiDB 会先执行 Join Reorder 算法，所以不能确定会先读取 `t1` 还是 `t2`。假设 TiDB 先读取了 `t1` 来构建 Build 端，那么 TiDB 会在探查 `t2` 前先根据谓词 `t1.col = 'value'` 筛选数据，但接下来每次探查 `t2` 时都要应用谓词 `t2.col='value'`。所以对于这条语句，Index Join 算法可能不如其他 Join 算法高效。

但如果 Build 端的数据量比 Probe 端小，且 Probe 端的数据已预先建立了索引，那么这种情况下 Index Join 算法效率更高。在下面这段查询语句中，因为 Index Join 比 Hash Join 效率低，所以 SQL 优化器选择了 Hash Join 算法：

{{< copyable "sql" >}}

```sql
-- 删除已有索引
ALTER TABLE t2 DROP INDEX t1_id;

EXPLAIN ANALYZE SELECT /*+ INL_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
```

```sql
Query OK, 0 rows affected (0.29 sec)

+-----------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+-----------------------+------+
| id                          | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                    | operator info                                                                  | memory                | disk |
+-----------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+-----------------------+------+
| IndexJoin_13                | 90000.00 | 20000   | root      |               | time:613.19955ms, loops:21, inner:{total:42.494047ms, concurrency:5, task:12, construct:33.149671ms, fetch:9.322956ms, build:8.66µs}, probe:32.435355ms                                                                                                                                           | inner join, inner:TableReader_9, outer key:test.t2.t1_id, inner key:test.t1.id | 269.63341903686523 MB | N/A  |
| ├─TableReader_19(Build)     | 90000.00 | 90000   | root      |               | time:586.613252ms, loops:95, cop_task: {num: 3, max: 205.893949ms, min: 185.051354ms, avg: 194.878702ms, p95: 205.893949ms, max_proc_keys: 31715, p95_proc_keys: 31715, tot_proc: 332ms, tot_wait: 4ms, rpc_num: 4, rpc_time: 584.907774ms, copr_cache_hit_ratio: 0.00}, backoff{regionMiss: 2ms} | data:TableFullScan_18                                                          | 182.624906539917 MB   | N/A  |
| │ └─TableFullScan_18        | 90000.00 | 90000   | cop[tikv] | table:t2      | time:0ns, loops:0, tikv_task:{proc max:72ms, min:64ms, p80:72ms, p95:72ms, iters:102, tasks:3}                                                                                                                                                                                                    | keep order:false                                                               | N/A                   | N/A  |
| └─TableReader_9(Probe)      | 0.00     | 5       | root      |               | time:8.432051ms, loops:14, cop_task: {num: 14, max: 629.805µs, min: 226.129µs, avg: 420.979µs, p95: 629.805µs, max_proc_keys: 4, p95_proc_keys: 4, rpc_num: 15, rpc_time: 5.953229ms, copr_cache_hit_ratio: 0.00}                                                                                 | data:Selection_8                                                               | N/A                   | N/A  |
|   └─Selection_8             | 0.00     | 5       | cop[tikv] |               | time:0ns, loops:0, tikv_task:{proc max:0s, min:0s, p80:0s, p95:0s, iters:14, tasks:14}                                                                                                                                                                                                            | eq(test.t1.int_col, 1)                                                         | N/A                   | N/A  |
|     └─TableRangeScan_7      | 1.00     | 25      | cop[tikv] | table:t1      | time:0ns, loops:0, tikv_task:{proc max:0s, min:0s, p80:0s, p95:0s, iters:14, tasks:14}                                                                                                                                                                                                            | range: decided by [test.t2.t1_id], keep order:false                            | N/A                   | N/A  |
+-----------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+-----------------------+------+
6 rows in set (0.61 sec)

+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                          | operator info                                     | memory                | disk    |
+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| HashJoin_19                  | 90000.00 | 20000   | root      |               | time:406.098528ms, loops:22, build_hash_table:{total:148.574644ms, fetch:146.843636ms, build:1.731008ms}, probe:{concurrency:5, total:2.026547436s, max:406.039309ms, probe:205.337813ms, fetch:1.821209623s}                                           | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 30.00731658935547 MB  | 0 Bytes |
| ├─TableReader_22(Build)      | 71.01    | 10000   | root      |               | time:147.072725ms, loops:12, cop_task: {num: 3, max: 145.847743ms, min: 50.932527ms, avg: 113.009029ms, p95: 145.847743ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 284ms, rpc_num: 3, rpc_time: 338.950488ms, copr_cache_hit_ratio: 0.00} | data:Selection_21                                 | 29.679713249206543 MB | N/A     |
| │ └─Selection_21             | 71.01    | 10000   | cop[tikv] |               | time:0ns, loops:0, tikv_task:{proc max:132ms, min:48ms, p80:132ms, p95:132ms, iters:83, tasks:3}                                                                                                                                                        | eq(test.t1.int_col, 1)                            | N/A                   | N/A     |
| │   └─TableFullScan_20       | 71010.00 | 71010   | cop[tikv] | table:t1      | time:0ns, loops:0, tikv_task:{proc max:128ms, min:48ms, p80:128ms, p95:128ms, iters:83, tasks:3}                                                                                                                                                        | keep order:false                                  | N/A                   | N/A     |
| └─TableReader_24(Probe)      | 90000.00 | 90000   | root      |               | time:365.918504ms, loops:91, cop_task: {num: 3, max: 398.62145ms, min: 338.460345ms, avg: 358.732721ms, p95: 398.62145ms, max_proc_keys: 31715, p95_proc_keys: 31715, tot_proc: 536ms, rpc_num: 3, rpc_time: 1.076128895s, copr_cache_hit_ratio: 0.00}  | data:TableFullScan_23                             | 182.62489891052246 MB | N/A     |
|   └─TableFullScan_23         | 90000.00 | 90000   | cop[tikv] | table:t2      | time:0ns, loops:0, tikv_task:{proc max:100ms, min:40ms, p80:100ms, p95:100ms, iters:102, tasks:3}                                                                                                                                                       | keep order:false                                  | N/A                   | N/A     |
+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
6 rows in set (0.41 sec)

+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                           | operator info                                     | memory                | disk    |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| HashJoin_20                  | 90000.00 | 20000   | root      |               | time:441.897092ms, loops:21, build_hash_table:{total:138.600864ms, fetch:136.353899ms, build:2.246965ms}, probe:{concurrency:5, total:2.207403854s, max:441.850032ms, probe:148.01937ms, fetch:2.059384484s}                                             | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 30.00731658935547 MB  | 0 Bytes |
| ├─TableReader_25(Build)      | 71.01    | 10000   | root      |               | time:138.081807ms, loops:12, cop_task: {num: 3, max: 134.702901ms, min: 53.356202ms, avg: 93.372186ms, p95: 134.702901ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 236ms, rpc_num: 3, rpc_time: 280.017658ms, copr_cache_hit_ratio: 0.00}   | data:Selection_24                                 | 29.680171966552734 MB | N/A     |
| │ └─Selection_24             | 71.01    | 10000   | cop[tikv] |               | time:0ns, loops:0, tikv_task:{proc max:80ms, min:52ms, p80:80ms, p95:80ms, iters:83, tasks:3}                                                                                                                                                            | eq(test.t1.int_col, 1)                            | N/A                   | N/A     |
| │   └─TableFullScan_23       | 71010.00 | 71010   | cop[tikv] | table:t1      | time:0ns, loops:0, tikv_task:{proc max:80ms, min:52ms, p80:80ms, p95:80ms, iters:83, tasks:3}                                                                                                                                                            | keep order:false                                  | N/A                   | N/A     |
| └─TableReader_22(Probe)      | 90000.00 | 90000   | root      |               | time:413.560548ms, loops:91, cop_task: {num: 3, max: 432.938474ms, min: 231.263355ms, avg: 365.710741ms, p95: 432.938474ms, max_proc_keys: 31715, p95_proc_keys: 31715, tot_proc: 488ms, rpc_num: 3, rpc_time: 1.097021983s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_21                             | 182.62489891052246 MB | N/A     |
|   └─TableFullScan_21         | 90000.00 | 90000   | cop[tikv] | table:t2      | time:0ns, loops:0, tikv_task:{proc max:80ms, min:80ms, p80:80ms, p95:80ms, iters:102, tasks:3}                                                                                                                                                           | keep order:false                                  | N/A                   | N/A     |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
6 rows in set (0.44 sec)
```

在上面所示的 Index Join 操作中，`t1.int_col` 一列的索引被删除了。如果加上这个索引，操作执行速度可以从 `0.61 秒` 提高到 `0.14 秒`，如下表所示：

```sql
-- 重新添加索引
ALTER TABLE t2 ADD INDEX (t1_id);

EXPLAIN ANALYZE SELECT /*+ INL_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
```

```sql
Query OK, 0 rows affected (3.65 sec)

+---------------------------------+----------+---------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+-----------------------+------+
| id                              | estRows  | actRows | task      | access object                | execution info                                                                                                                                                                                                                                                           | operator info                                                                   | memory                | disk |
+---------------------------------+----------+---------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+-----------------------+------+
| IndexJoin_11                    | 90000.00 | 0       | root      |                              | time:136.876686ms, loops:1, inner:{total:114.948158ms, concurrency:5, task:7, construct:5.329114ms, fetch:109.610054ms, build:2.38µs}, probe:1.699799ms                                                                                                                  | inner join, inner:IndexLookUp_10, outer key:test.t1.id, inner key:test.t2.t1_id | 29.864535331726074 MB | N/A  |
| ├─TableReader_32(Build)         | 10000.00 | 10000   | root      |                              | time:95.755212ms, loops:12, cop_task: {num: 3, max: 95.652443ms, min: 30.758712ms, avg: 57.545129ms, p95: 95.652443ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 124ms, rpc_num: 3, rpc_time: 172.528417ms, copr_cache_hit_ratio: 0.00}                      | data:Selection_31                                                               | 29.679298400878906 MB | N/A  |
| │ └─Selection_31                | 10000.00 | 10000   | cop[tikv] |                              | time:0ns, loops:0, tikv_task:{proc max:44ms, min:28ms, p80:44ms, p95:44ms, iters:84, tasks:3}                                                                                                                                                                            | eq(test.t1.int_col, 1)                                                          | N/A                   | N/A  |
| │   └─TableFullScan_30          | 71010.00 | 71010   | cop[tikv] | table:t1                     | time:0ns, loops:0, tikv_task:{proc max:44ms, min:28ms, p80:44ms, p95:44ms, iters:84, tasks:3}                                                                                                                                                                            | keep order:false                                                                | N/A                   | N/A  |
| └─IndexLookUp_10(Probe)         | 9.00     | 0       | root      |                              | time:103.93801ms, loops:7                                                                                                                                                                                                                                                |                                                                                 | 2.1787109375 KB       | N/A  |
|   ├─IndexRangeScan_8(Build)     | 9.00     | 0       | cop[tikv] | table:t2, index:t1_id(t1_id) | time:0s, loops:0, cop_task: {num: 7, max: 23.969244ms, min: 12.003682ms, avg: 14.659066ms, p95: 23.969244ms, tot_proc: 100ms, rpc_num: 7, rpc_time: 102.435966ms, copr_cache_hit_ratio: 0.00}, tikv_task:{proc max:24ms, min:12ms, p80:16ms, p95:24ms, iters:7, tasks:7} | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false             | N/A                   | N/A  |
|   └─TableRowIDScan_9(Probe)     | 9.00     | 0       | cop[tikv] | table:t2                     | time:0ns, loops:0                                                                                                                                                                                                                                                        | keep order:false                                                                | N/A                   | N/A  |
+---------------------------------+----------+---------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+-----------------------+------+
7 rows in set (0.14 sec)

+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                         | operator info                                     | memory                | disk    |
+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| HashJoin_31                  | 90000.00 | 0       | root      |               | time:402.263795ms, loops:1, build_hash_table:{total:128.467151ms, fetch:126.871282ms, build:1.595869ms}, probe:{concurrency:5, total:2.010969815s, max:402.212295ms, probe:8.924769ms, fetch:2.002045046s}                                             | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 29.689788818359375 MB | 0 Bytes |
| ├─TableReader_34(Build)      | 10000.00 | 10000   | root      |               | time:126.765972ms, loops:11, cop_task: {num: 3, max: 126.721293ms, min: 54.375481ms, avg: 84.518849ms, p95: 126.721293ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 208ms, rpc_num: 3, rpc_time: 253.478218ms, copr_cache_hit_ratio: 0.00} | data:Selection_33                                 | 29.679292678833008 MB | N/A     |
| │ └─Selection_33             | 10000.00 | 10000   | cop[tikv] |               | time:0ns, loops:0, tikv_task:{proc max:72ms, min:56ms, p80:72ms, p95:72ms, iters:84, tasks:3}                                                                                                                                                          | eq(test.t1.int_col, 1)                            | N/A                   | N/A     |
| │   └─TableFullScan_32       | 71010.00 | 71010   | cop[tikv] | table:t1      | time:0ns, loops:0, tikv_task:{proc max:72ms, min:56ms, p80:72ms, p95:72ms, iters:84, tasks:3}                                                                                                                                                          | keep order:false                                  | N/A                   | N/A     |
| └─TableReader_36(Probe)      | 90000.00 | 90000   | root      |               | time:400.447175ms, loops:90, cop_task: {num: 3, max: 400.838264ms, min: 309.474053ms, avg: 341.01943ms, p95: 400.838264ms, max_proc_keys: 31719, p95_proc_keys: 31719, tot_proc: 528ms, rpc_num: 3, rpc_time: 1.02298055s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_35                             | 182.62786674499512 MB | N/A     |
|   └─TableFullScan_35         | 90000.00 | 90000   | cop[tikv] | table:t2      | time:0ns, loops:0, tikv_task:{proc max:108ms, min:72ms, p80:108ms, p95:108ms, iters:102, tasks:3}                                                                                                                                                      | keep order:false                                  | N/A                   | N/A     |
+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
6 rows in set (0.40 sec)

+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                          | operator info                                     | memory                | disk    |
+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| HashJoin_32                  | 90000.00 | 0       | root      |               | time:356.282882ms, loops:1, build_hash_table:{total:154.187155ms, fetch:151.259305ms, build:2.92785ms}, probe:{concurrency:5, total:1.781087041s, max:356.238312ms, probe:7.406146ms, fetch:1.773680895s}                                               | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 29.689788818359375 MB | 0 Bytes |
| ├─TableReader_41(Build)      | 10000.00 | 10000   | root      |               | time:151.190175ms, loops:11, cop_task: {num: 3, max: 151.055697ms, min: 56.214348ms, avg: 96.70463ms, p95: 151.055697ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 240ms, rpc_num: 3, rpc_time: 290.019942ms, copr_cache_hit_ratio: 0.00}   | data:Selection_40                                 | 29.679292678833008 MB | N/A     |
| │ └─Selection_40             | 10000.00 | 10000   | cop[tikv] |               | time:0ns, loops:0, tikv_task:{proc max:80ms, min:56ms, p80:80ms, p95:80ms, iters:84, tasks:3}                                                                                                                                                           | eq(test.t1.int_col, 1)                            | N/A                   | N/A     |
| │   └─TableFullScan_39       | 71010.00 | 71010   | cop[tikv] | table:t1      | time:0ns, loops:0, tikv_task:{proc max:80ms, min:56ms, p80:80ms, p95:80ms, iters:84, tasks:3}                                                                                                                                                           | keep order:false                                  | N/A                   | N/A     |
| └─TableReader_43(Probe)      | 90000.00 | 90000   | root      |               | time:354.68523ms, loops:90, cop_task: {num: 3, max: 354.313475ms, min: 328.460762ms, avg: 345.530558ms, p95: 354.313475ms, max_proc_keys: 31719, p95_proc_keys: 31719, tot_proc: 508ms, rpc_num: 3, rpc_time: 1.036492374s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_42                             | 182.62786102294922 MB | N/A     |
|   └─TableFullScan_42         | 90000.00 | 90000   | cop[tikv] | table:t2      | time:0ns, loops:0, tikv_task:{proc max:84ms, min:64ms, p80:84ms, p95:84ms, iters:102, tasks:3}                                                                                                                                                          | keep order:false                                  | N/A                   | N/A     |
+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
6 rows in set (0.36 sec)
```

> **注意：**
>
> 在上方示例中，SQL 优化器之所以选择了性能较差的 Hash Join 算法，而不是 Index Join 算法，原因在于查询优化是一个 [NP 完全问题](https://zh.wikipedia.org/wiki/NP%E5%AE%8C%E5%85%A8)，可能会选择不太理想的计划。如果需要频繁调用这个查询，建议通过[执行计划管理](/sql-plan-management.md)的方式将 Hint 与 SQL 语句绑定，这样要比在发送给 TiDB 的 SQL 语句中插入 Hint 更容易管理。

### Index Join 相关算法

如果使用 Hint [`INL_JOIN`](/optimizer-hints.md#inl_joint1_name--tl_name-) 进行 Index Join 操作，TiDB 会在连接外表之前创建一个中间结果的 Hash Table。TiDB 同样也支持使用 Hint [`INL_HASH_JOIN`](/optimizer-hints.md#inl_hash_join) 在外表上建 Hash Table。以上所述的 Index Join 相关算法都由 SQL 优化器自动选择。

### 配置

Index Join 算法的性能受以下系统变量影响：

* [`tidb_index_join_batch_size`](/system-variables.md#tidb_index_join_batch_size)（默认值：`25000`）- `index lookup join` 操作的 batch 大小。
* [`tidb_index_lookup_join_concurrency`](/system-variables.md#tidb_index_lookup_join_concurrency)（默认值：`4`）- 可以并发执行的 index lookup 任务数。

## Hash Join

在 Hash Join 操作中，TiDB 首先读取 Build 端的数据并将其缓存在 Hash Table 中，然后再读取 Probe 端的数据，使用 Probe 端的数据来探查 Hash Table 以获得所需行。与 Index Join 算法相比，Hash Join 要消耗更多内存，但如果需要连接的行数很多，运行速度会比 Index Join 快。TiDB 中的 Hash Join 算子是多线程的，并且可以并发执行。

下面是一个 Hash Join 示例：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+-----------+-----------+---------------+------------------------------------------------+
| id                          | estRows   | task      | access object | operator info                                  |
+-----------------------------+-----------+-----------+---------------+------------------------------------------------+
| HashJoin_27                 | 142020.00 | root      |               | inner join, equal:[eq(test.t1.id, test.t2.id)] |
| ├─TableReader_29(Build)     | 142020.00 | root      |               | data:TableFullScan_28                          |
| │ └─TableFullScan_28        | 142020.00 | cop[tikv] | table:t1      | keep order:false                               |
| └─TableReader_31(Probe)     | 180000.00 | root      |               | data:TableFullScan_30                          |
|   └─TableFullScan_30        | 180000.00 | cop[tikv] | table:t2      | keep order:false                               |
+-----------------------------+-----------+-----------+---------------+------------------------------------------------+
5 rows in set (0.00 sec)
```

TiDB 会按照以下顺序执行 `HashJoin_27` 算子：

1. 将 Build 端数据缓存在内存中。
2. 根据缓存数据在 Build 端构造一个 Hash Table。
3. 读取 Probe 端的数据。
4. 使用 Probe 端的数据来探查 Hash Table。
5. 将符合条件的结果返回给用户。

`EXPLAIN` 返回结果中的 `operator info` 一列记录了 `HashJoin_27` 的其他信息，包括该查询是 Inner Join 还是 Outer Join 以及 Join 的条件是什么等。在上面给出的示例中，该查询为 Inner Join，Join 条件是 `equal:[eq(test.t1.id, test.t2.id)]`，与查询语句中的 `WHERE t1.id = t2.id` 部分对应。下面例子中其他几个 Join 算子的 operator info 和此处类似。

### 运行数据

如果在执行操作时，内存使用超过了 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 规定的值（默认为 1GB），且 `oom-use-tmp-storage` 的值为 `true` （默认为 `true`），那么 TiDB 会尝试使用临时存储，在磁盘上创建 Hash Join 的 Build 端。`EXPLAIN ANALYZE` 返回结果中的 `execution info` 一栏记录了有关内存使用情况等运行数据。下面的例子展示了 `tidb_mem_quota_query` 的值分别设为 1GB（默认）及 500MB 时，`EXPLAIN ANALYZE` 的返回结果（当内存配额设为 500MB 时，磁盘用作临时存储区）：

```sql
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
SET tidb_mem_quota_query=500 * 1024 * 1024;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+---------+
| id                          | estRows   | actRows | task      | access object | execution info                                                                                                                                                                                                                                           | operator info                                  | memory                | disk    |
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+---------+
| HashJoin_27                 | 142020.00 | 71010   | root      |               | time:647.508572ms, loops:72, build_hash_table:{total:579.254415ms, fetch:566.91012ms, build:12.344295ms}, probe:{concurrency:5, total:3.23315006s, max:647.520113ms, probe:330.884716ms, fetch:2.902265344s}                                             | inner join, equal:[eq(test.t1.id, test.t2.id)] | 209.61642456054688 MB | 0 Bytes |
| ├─TableReader_29(Build)     | 142020.00 | 71010   | root      |               | time:567.088247ms, loops:72, cop_task: {num: 2, max: 569.809411ms, min: 369.67451ms, avg: 469.74196ms, p95: 569.809411ms, max_proc_keys: 39245, p95_proc_keys: 39245, tot_proc: 400ms, rpc_num: 2, rpc_time: 939.447231ms, copr_cache_hit_ratio: 0.00}   | data:TableFullScan_28                          | 210.2100534439087 MB  | N/A     |
| │ └─TableFullScan_28        | 142020.00 | 71010   | cop[tikv] | table:t1      | proc max:64ms, min:48ms, p80:64ms, p95:64ms, iters:79, tasks:2                                                                                                                                                                                           | keep order:false                               | N/A                   | N/A     |
| └─TableReader_31(Probe)     | 180000.00 | 90000   | root      |               | time:337.233636ms, loops:91, cop_task: {num: 3, max: 569.790741ms, min: 332.758911ms, avg: 421.543165ms, p95: 569.790741ms, max_proc_keys: 31719, p95_proc_keys: 31719, tot_proc: 500ms, rpc_num: 3, rpc_time: 1.264570696s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_30                          | 267.1126985549927 MB  | N/A     |
|   └─TableFullScan_30        | 180000.00 | 90000   | cop[tikv] | table:t2      | proc max:84ms, min:72ms, p80:84ms, p95:84ms, iters:102, tasks:3                                                                                                                                                                                          | keep order:false                               | N/A                   | N/A     |
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+---------+
5 rows in set (0.65 sec)

Query OK, 0 rows affected (0.00 sec)

+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+----------------------+
| id                          | estRows   | actRows | task      | access object | execution info                                                                                                                                                                                                                                           | operator info                                  | memory                | disk                 |
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+----------------------+
| HashJoin_27                 | 142020.00 | 71010   | root      |               | time:963.983353ms, loops:72, build_hash_table:{total:775.961447ms, fetch:503.789677ms, build:272.17177ms}, probe:{concurrency:5, total:4.805454793s, max:963.973133ms, probe:922.156835ms, fetch:3.883297958s}                                           | inner join, equal:[eq(test.t1.id, test.t2.id)] | 93.53974533081055 MB  | 210.7459259033203 MB |
| ├─TableReader_29(Build)     | 142020.00 | 71010   | root      |               | time:504.062018ms, loops:72, cop_task: {num: 2, max: 509.276857ms, min: 402.66386ms, avg: 455.970358ms, p95: 509.276857ms, max_proc_keys: 39245, p95_proc_keys: 39245, tot_proc: 384ms, rpc_num: 2, rpc_time: 911.893237ms, copr_cache_hit_ratio: 0.00}  | data:TableFullScan_28                          | 210.20934200286865 MB | N/A                  |
| │ └─TableFullScan_28        | 142020.00 | 71010   | cop[tikv] | table:t1      | proc max:88ms, min:72ms, p80:88ms, p95:88ms, iters:79, tasks:2                                                                                                                                                                                           | keep order:false                               | N/A                   | N/A                  |
| └─TableReader_31(Probe)     | 180000.00 | 90000   | root      |               | time:363.058382ms, loops:91, cop_task: {num: 3, max: 412.659191ms, min: 358.489688ms, avg: 391.463008ms, p95: 412.659191ms, max_proc_keys: 31719, p95_proc_keys: 31719, tot_proc: 484ms, rpc_num: 3, rpc_time: 1.174326746s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_30                          | 267.11340618133545 MB | N/A                  |
|   └─TableFullScan_30        | 180000.00 | 90000   | cop[tikv] | table:t2      | proc max:92ms, min:64ms, p80:92ms, p95:92ms, iters:102, tasks:3                                                                                                                                                                                          | keep order:false                               | N/A                   | N/A                  |
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+----------------------+
5 rows in set (0.98 sec)
```

### 配置

Hash Join 算法的性能受以下系统变量影响：

* [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)（默认值：1GB）- 如果某条查询的内存消耗超出了配额，TiDB 会尝试将 Hash Join 的 Build 端移到磁盘上以节省内存。
* [`tidb_hash_join_concurrency`](/system-variables.md#tidb_hash_join_concurrency)（默认值：`5`）- 可以并发执行的 Hash Join 任务数量。

## Merge Join

Merge Join 是一种特殊的 Join 算法。当两个关联表要 Join 的字段需要按排好的顺序读取时，适用 Merge Join 算法。由于 Build 端和 Probe 端的数据都会读取，这种算法的 Join 操作是流式的，类似“拉链式合并”的高效版。Merge Join 占用的内存要远低于 Hash Join，但 Merge Join 不能并发执行。

下面是一个使用 Merge Join 的例子：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+-----------+-----------+---------------+-------------------------------------------------------+
| id                          | estRows   | task      | access object | operator info                                         |
+-----------------------------+-----------+-----------+---------------+-------------------------------------------------------+
| MergeJoin_7                 | 142020.00 | root      |               | inner join, left key:test.t1.id, right key:test.t2.id |
| ├─TableReader_12(Build)     | 180000.00 | root      |               | data:TableFullScan_11                                 |
| │ └─TableFullScan_11        | 180000.00 | cop[tikv] | table:t2      | keep order:true                                       |
| └─TableReader_10(Probe)     | 142020.00 | root      |               | data:TableFullScan_9                                  |
|   └─TableFullScan_9         | 142020.00 | cop[tikv] | table:t1      | keep order:true                                       |
+-----------------------------+-----------+-----------+---------------+-------------------------------------------------------+
5 rows in set (0.00 sec)
```

TiDB 会按照以下顺序执行 Merge Join 算子：

1. 从 Build 端把一个 Join Group 的数据全部读取到内存中。
2. 读取 Probe 端的数据。
3. 将 Probe 端的每行数据与 Build 端的一个完整 Join Group 比较，依次查看是否匹配（除了满足等值条件以外，还有其他非等值条件，这里的“匹配”主要是指查看是否满足非等值条件）。Join Group 指的是所有 Join Key 上值相同的数据。

## 其他类型查询的执行计划

+ [MPP 模式查询的执行计划](/explain-mpp.md)
+ [索引查询的执行计划](/explain-indexes.md)
+ [子查询的执行计划](/explain-subqueries.md)
+ [聚合查询的执行计划](/explain-aggregation.md)
+ [视图查询的执行计划](/explain-views.md)
+ [分区查询的执行计划](/explain-partitions.md)
+ [开启 IndexMerge 查询的执行计划](/explain-index-merge.md)
