---
title: Explain Statements That Use Joins
summary: Learn about the execution plan information returned by the EXPLAIN statement in TiDB.
---

# Explain Statements That Use Joins

In TiDB, the SQL Optimizer needs to decide in which order tables should be joined and what is the most efficient join algorithm for a particular SQL statement. The examples in this document are based on the following sample data:

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

If the number of estimated rows that need to be joined is small (typically less than 10000 rows), it is preferable to use the index join method. This method of join works similar to the primary method of join used in MySQL. In the following example, the operator `├─TableReader_29(Build)` first reads the table `t1`. For each row that matches, TiDB will probe the table `t2`:

> **Note:**
>
> In the returned execution plan, for all probe-side child nodes of `IndexJoin` and `Apply` operators, the meaning of `estRows` since v6.4.0 is different from that before v6.4.0. For more details, see [TiDB Query Execution Plan Overview](/explain-overview.md#understand-explain-output).

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id;
```

```sql
+---------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                              | estRows  | task      | access object                | operator info                                                                                                             |
+---------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_11                    | 90000.00 | root      |                              | inner join, inner:IndexLookUp_10, outer key:test.t1.id, inner key:test.t2.t1_id, equal cond:eq(test.t1.id, test.t2.t1_id) |
| ├─TableReader_29(Build)         | 71010.00 | root      |                              | data:TableFullScan_28                                                                                                     |
| │ └─TableFullScan_28            | 71010.00 | cop[tikv] | table:t1                     | keep order:false                                                                                                          |
| └─IndexLookUp_10(Probe)         | 90000.00 | root      |                              |                                                                                                                           |
|   ├─IndexRangeScan_8(Build)     | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false                                                       |
|   └─TableRowIDScan_9(Probe)     | 90000.00 | cop[tikv] | table:t2                     | keep order:false                                                                                                          |
+---------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
```

Index join is efficient in memory usage, but might be slower to execute than other join methods when a large number of probe operations are required. Consider also the following query:

```sql
SELECT * FROM t1 INNER JOIN t2 ON t1.id=t2.t1_id WHERE t1.pad1 = 'value' and t2.pad1='value';
```

In an inner join operation, TiDB implements join reordering and might access either `t1` or `t2` first. Assume that TiDB selects `t1` as the first table to apply the `build` step, and then TiDB is able to filter on the predicate `t1.col = 'value'` before probing the table `t2`. The filter for the predicate `t2.col='value'` will be applied on each probe of table `t2`, which might be less efficient than other join methods.

Index join is effective if the build side is small and the probe side is pre-indexed and large. Consider the following query where an index join performs worse than a hash join and is not chosen by the SQL Optimizer:

{{< copyable "sql" >}}

```sql
-- DROP previously added index
ALTER TABLE t2 DROP INDEX t1_id;

EXPLAIN ANALYZE SELECT /*+ INL_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
```

```sql
+-----------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+---------+------+
| id                          | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                                           | operator info                                                                                                             | memory  | disk |
+-----------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+---------+------+
| IndexJoin_14                | 90000.00 | 0       | root      |               | time:330.2ms, loops:1, inner:{total:72.2ms, concurrency:5, task:12, construct:58.6ms, fetch:13.5ms, build:2.12µs}, probe:26.1ms                                                                                                                                                                                          | inner join, inner:TableReader_10, outer key:test.t2.t1_id, inner key:test.t1.id, equal cond:eq(test.t2.t1_id, test.t1.id) | 88.5 MB | N/A  |
| ├─TableReader_20(Build)     | 90000.00 | 90000   | root      |               | time:307.2ms, loops:96, cop_task: {num: 24, max: 130.6ms, min: 170.9µs, avg: 33.5ms, p95: 105ms, max_proc_keys: 10687, p95_proc_keys: 9184, tot_proc: 472ms, rpc_num: 24, rpc_time: 802.4ms, copr_cache_hit_ratio: 0.62, distsql_concurrency: 15}                                                                        | data:TableFullScan_19                                                                                                     | 58.6 MB | N/A  |
| │ └─TableFullScan_19        | 90000.00 | 90000   | cop[tikv] | table:t2      | tikv_task:{proc max:34ms, min:0s, avg: 15.3ms, p80:24ms, p95:30ms, iters:181, tasks:24}, scan_detail: {total_process_keys: 69744, total_process_keys_size: 217533936, total_keys: 69753, get_snapshot_time: 701.6µs, rocksdb: {delete_skipped_count: 97368, key_skipped_count: 236847, block: {cache_hit_count: 3509}}}  | keep order:false                                                                                                          | N/A     | N/A  |
| └─TableReader_10(Probe)     | 12617.92 | 0       | root      |               | time:11.9ms, loops:12, cop_task: {num: 42, max: 848.8µs, min: 199µs, avg: 451.8µs, p95: 846.2µs, max_proc_keys: 7, p95_proc_keys: 5, rpc_num: 42, rpc_time: 18.3ms, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}                                                                                                 | data:Selection_9                                                                                                          | N/A     | N/A  |
|   └─Selection_9             | 12617.92 | 0       | cop[tikv] |               | tikv_task:{proc max:0s, min:0s, avg: 0s, p80:0s, p95:0s, iters:42, tasks:42}, scan_detail: {total_process_keys: 56, total_process_keys_size: 174608, total_keys: 77, get_snapshot_time: 727.7µs, rocksdb: {block: {cache_hit_count: 154}}}                                                                               | eq(test.t1.int_col, 1)                                                                                                    | N/A     | N/A  |
|     └─TableRangeScan_8      | 90000.00 | 56      | cop[tikv] | table:t1      | tikv_task:{proc max:0s, min:0s, avg: 0s, p80:0s, p95:0s, iters:42, tasks:42}                                                                                                                                                                                                                                             | range: decided by [test.t2.t1_id], keep order:false                                                                       | N/A     | N/A  |
+-----------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+---------+------+

+------------------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                                         | operator info                                     | memory  | disk    |
+------------------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| HashJoin_20                  | 90000.00 | 0       | root      |               | time:313.6ms, loops:1, build_hash_table:{total:24.6ms, fetch:21.2ms, build:3.32ms}, probe:{concurrency:5, total:1.57s, max:313.5ms, probe:18.9ms, fetch:1.55s}                                                                                                                                                         | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 32.0 MB | 0 Bytes |
| ├─TableReader_23(Build)      | 9955.54  | 10000   | root      |               | time:23.6ms, loops:12, cop_task: {num: 11, max: 504.6µs, min: 203.7µs, avg: 377.4µs, p95: 504.6µs, rpc_num: 11, rpc_time: 3.92ms, copr_cache_hit_ratio: 1.00, distsql_concurrency: 15}                                                                                                                                 | data:Selection_22                                 | 14.9 MB | N/A     |
| │ └─Selection_22             | 9955.54  | 10000   | cop[tikv] |               | tikv_task:{proc max:104ms, min:3ms, avg: 24.4ms, p80:33ms, p95:104ms, iters:113, tasks:11}, scan_detail: {get_snapshot_time: 241.4µs, rocksdb: {block: {}}}                                                                                                                                                            | eq(test.t1.int_col, 1)                            | N/A     | N/A     |
| │   └─TableFullScan_21       | 71010.00 | 71010   | cop[tikv] | table:t1      | tikv_task:{proc max:101ms, min:3ms, avg: 23.8ms, p80:33ms, p95:101ms, iters:113, tasks:11}                                                                                                                                                                                                                             | keep order:false                                  | N/A     | N/A     |
| └─TableReader_25(Probe)      | 90000.00 | 90000   | root      |               | time:293.7ms, loops:91, cop_task: {num: 24, max: 105.7ms, min: 210.9µs, avg: 31.4ms, p95: 103.8ms, max_proc_keys: 10687, p95_proc_keys: 9184, tot_proc: 407ms, rpc_num: 24, rpc_time: 752.2ms, copr_cache_hit_ratio: 0.62, distsql_concurrency: 15}                                                                    | data:TableFullScan_24                             | 58.6 MB | N/A     |
|   └─TableFullScan_24         | 90000.00 | 90000   | cop[tikv] | table:t2      | tikv_task:{proc max:31ms, min:0s, avg: 13ms, p80:19ms, p95:26ms, iters:181, tasks:24}, scan_detail: {total_process_keys: 69744, total_process_keys_size: 217533936, total_keys: 69753, get_snapshot_time: 637.2µs, rocksdb: {delete_skipped_count: 97368, key_skipped_count: 236847, block: {cache_hit_count: 3509}}}  | keep order:false                                  | N/A     | N/A     |
+------------------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+

+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                                           | operator info                                     | memory  | disk    |
+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| HashJoin_21                  | 90000.00 | 0       | root      |               | time:331.7ms, loops:1, build_hash_table:{total:32.7ms, fetch:26ms, build:6.73ms}, probe:{concurrency:5, total:1.66s, max:331.3ms, probe:16ms, fetch:1.64s}                                                                                                                                                               | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 32.3 MB | 0 Bytes |
| ├─TableReader_26(Build)      | 9955.54  | 10000   | root      |               | time:30.4ms, loops:13, cop_task: {num: 11, max: 1.87ms, min: 844.7µs, avg: 1.29ms, p95: 1.87ms, rpc_num: 11, rpc_time: 13.5ms, copr_cache_hit_ratio: 1.00, distsql_concurrency: 15}                                                                                                                                      | data:Selection_25                                 | 12.2 MB | N/A     |
| │ └─Selection_25             | 9955.54  | 10000   | cop[tikv] |               | tikv_task:{proc max:104ms, min:3ms, avg: 24.4ms, p80:33ms, p95:104ms, iters:113, tasks:11}, scan_detail: {get_snapshot_time: 521µs, rocksdb: {block: {}}}                                                                                                                                                                | eq(test.t1.int_col, 1)                            | N/A     | N/A     |
| │   └─TableFullScan_24       | 71010.00 | 71010   | cop[tikv] | table:t1      | tikv_task:{proc max:101ms, min:3ms, avg: 23.8ms, p80:33ms, p95:101ms, iters:113, tasks:11}                                                                                                                                                                                                                               | keep order:false                                  | N/A     | N/A     |
| └─TableReader_23(Probe)      | 90000.00 | 90000   | root      |               | time:308.6ms, loops:91, cop_task: {num: 24, max: 123.3ms, min: 518.9µs, avg: 32.4ms, p95: 113.4ms, max_proc_keys: 10687, p95_proc_keys: 9184, tot_proc: 499ms, rpc_num: 24, rpc_time: 776ms, copr_cache_hit_ratio: 0.62, distsql_concurrency: 15}                                                                        | data:TableFullScan_22                             | 58.6 MB | N/A     |
|   └─TableFullScan_22         | 90000.00 | 90000   | cop[tikv] | table:t2      | tikv_task:{proc max:44ms, min:0s, avg: 16.8ms, p80:27ms, p95:40ms, iters:181, tasks:24}, scan_detail: {total_process_keys: 69744, total_process_keys_size: 217533936, total_keys: 69753, get_snapshot_time: 955.4µs, rocksdb: {delete_skipped_count: 97368, key_skipped_count: 236847, block: {cache_hit_count: 3509}}}  | keep order:false                                  | N/A     | N/A     |
+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
```

In the above example, the index join operation is missing an index on `t1.int_col`. Once this index is added, the performance of the operation improves from `0.3 sec` to `0.06 sec`, as the following result shows:

```sql
-- Re-add index
ALTER TABLE t2 ADD INDEX (t1_id);

EXPLAIN ANALYZE SELECT /*+ INL_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
```

```sql
+----------------------------------+----------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+-----------+------+
| id                               | estRows  | actRows | task      | access object                | execution info                                                                                                                                                                                                                                                                                                                                                                               | operator info                                                                                                             | memory    | disk |
+----------------------------------+----------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+-----------+------+
| IndexJoin_12                     | 90000.00 | 0       | root      |                              | time:65.6ms, loops:1, inner:{total:129.7ms, concurrency:5, task:7, construct:7.13ms, fetch:122.5ms, build:16.4µs}, probe:2.54ms                                                                                                                                                                                                                                                              | inner join, inner:IndexLookUp_11, outer key:test.t1.id, inner key:test.t2.t1_id, equal cond:eq(test.t1.id, test.t2.t1_id) | 28.7 MB   | N/A  |
| ├─TableReader_33(Build)          | 9955.54  | 10000   | root      |                              | time:15.4ms, loops:16, cop_task: {num: 11, max: 1.52ms, min: 211.5µs, avg: 416.8µs, p95: 1.52ms, rpc_num: 11, rpc_time: 4.36ms, copr_cache_hit_ratio: 1.00, distsql_concurrency: 15}                                                                                                                                                                                                         | data:Selection_32                                                                                                         | 13.9 MB   | N/A  |
| │ └─Selection_32                 | 9955.54  | 10000   | cop[tikv] |                              | tikv_task:{proc max:104ms, min:3ms, avg: 24.4ms, p80:33ms, p95:104ms, iters:113, tasks:11}, scan_detail: {get_snapshot_time: 185µs, rocksdb: {block: {}}}                                                                                                                                                                                                                                    | eq(test.t1.int_col, 1)                                                                                                    | N/A       | N/A  |
| │   └─TableFullScan_31           | 71010.00 | 71010   | cop[tikv] | table:t1                     | tikv_task:{proc max:101ms, min:3ms, avg: 23.8ms, p80:33ms, p95:101ms, iters:113, tasks:11}                                                                                                                                                                                                                                                                                                   | keep order:false                                                                                                          | N/A       | N/A  |
| └─IndexLookUp_11(Probe)          | 90000.00 | 0       | root      |                              | time:115.6ms, loops:7                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                           | 555 Bytes | N/A  |
|   ├─IndexRangeScan_9(Build)      | 90000.00 | 0       | cop[tikv] | table:t2, index:t1_id(t1_id) | time:114.3ms, loops:7, cop_task: {num: 7, max: 42ms, min: 1.3ms, avg: 16.2ms, p95: 42ms, tot_proc: 71ms, rpc_num: 7, rpc_time: 113.2ms, copr_cache_hit_ratio: 0.29, distsql_concurrency: 15}, tikv_task:{proc max:37ms, min:0s, avg: 11.3ms, p80:20ms, p95:37ms, iters:7, tasks:7}, scan_detail: {total_keys: 9296, get_snapshot_time: 141.9µs, rocksdb: {block: {cache_hit_count: 18592}}}  | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false                                                       | N/A       | N/A  |
|   └─TableRowIDScan_10(Probe)     | 90000.00 | 0       | cop[tikv] | table:t2                     |                                                                                                                                                                                                                                                                                                                                                                                              | keep order:false                                                                                                          | N/A       | N/A  |
+----------------------------------+----------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+-----------+------+

+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                                             | operator info                                     | memory  | disk    |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| HashJoin_32                  | 90000.00 | 0       | root      |               | time:320.2ms, loops:1, build_hash_table:{total:19.3ms, fetch:16.8ms, build:2.52ms}, probe:{concurrency:5, total:1.6s, max:320.1ms, probe:16.1ms, fetch:1.58s}                                                                                                                                                              | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 32.0 MB | 0 Bytes |
| ├─TableReader_35(Build)      | 9955.54  | 10000   | root      |               | time:18.6ms, loops:12, cop_task: {num: 11, max: 713.8µs, min: 197.3µs, avg: 368.5µs, p95: 713.8µs, rpc_num: 11, rpc_time: 3.83ms, copr_cache_hit_ratio: 1.00, distsql_concurrency: 15}                                                                                                                                     | data:Selection_34                                 | 14.9 MB | N/A     |
| │ └─Selection_34             | 9955.54  | 10000   | cop[tikv] |               | tikv_task:{proc max:104ms, min:3ms, avg: 24.4ms, p80:33ms, p95:104ms, iters:113, tasks:11}, scan_detail: {get_snapshot_time: 178.9µs, rocksdb: {block: {}}}                                                                                                                                                                | eq(test.t1.int_col, 1)                            | N/A     | N/A     |
| │   └─TableFullScan_33       | 71010.00 | 71010   | cop[tikv] | table:t1      | tikv_task:{proc max:101ms, min:3ms, avg: 23.8ms, p80:33ms, p95:101ms, iters:113, tasks:11}                                                                                                                                                                                                                                 | keep order:false                                  | N/A     | N/A     |
| └─TableReader_37(Probe)      | 90000.00 | 90000   | root      |               | time:304.4ms, loops:91, cop_task: {num: 24, max: 114ms, min: 251.1µs, avg: 33.1ms, p95: 110.4ms, max_proc_keys: 10687, p95_proc_keys: 9184, tot_proc: 492ms, rpc_num: 24, rpc_time: 793ms, copr_cache_hit_ratio: 0.62, distsql_concurrency: 15}                                                                            | data:TableFullScan_36                             | 58.6 MB | N/A     |
|   └─TableFullScan_36         | 90000.00 | 90000   | cop[tikv] | table:t2      | tikv_task:{proc max:38ms, min:3ms, avg: 14.1ms, p80:23ms, p95:35ms, iters:181, tasks:24}, scan_detail: {total_process_keys: 69744, total_process_keys_size: 217533936, total_keys: 139497, get_snapshot_time: 577.2µs, rocksdb: {delete_skipped_count: 44208, key_skipped_count: 253431, block: {cache_hit_count: 3527}}}  | keep order:false                                  | N/A     | N/A     |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+

+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                                             | operator info                                     | memory  | disk    |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| HashJoin_33                  | 90000.00 | 0       | root      |               | time:306.3ms, loops:1, build_hash_table:{total:20.5ms, fetch:17.1ms, build:3.45ms}, probe:{concurrency:5, total:1.53s, max:305.9ms, probe:17.1ms, fetch:1.51s}                                                                                                                                                             | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 32.0 MB | 0 Bytes |
| ├─TableReader_42(Build)      | 9955.54  | 10000   | root      |               | time:19.6ms, loops:12, cop_task: {num: 11, max: 1.07ms, min: 246.1µs, avg: 600µs, p95: 1.07ms, rpc_num: 11, rpc_time: 6.17ms, copr_cache_hit_ratio: 1.00, distsql_concurrency: 15}                                                                                                                                         | data:Selection_41                                 | 19.7 MB | N/A     |
| │ └─Selection_41             | 9955.54  | 10000   | cop[tikv] |               | tikv_task:{proc max:104ms, min:3ms, avg: 24.4ms, p80:33ms, p95:104ms, iters:113, tasks:11}, scan_detail: {get_snapshot_time: 282.9µs, rocksdb: {block: {}}}                                                                                                                                                                | eq(test.t1.int_col, 1)                            | N/A     | N/A     |
| │   └─TableFullScan_40       | 71010.00 | 71010   | cop[tikv] | table:t1      | tikv_task:{proc max:101ms, min:3ms, avg: 23.8ms, p80:33ms, p95:101ms, iters:113, tasks:11}                                                                                                                                                                                                                                 | keep order:false                                  | N/A     | N/A     |
| └─TableReader_44(Probe)      | 90000.00 | 90000   | root      |               | time:289.2ms, loops:91, cop_task: {num: 24, max: 108.2ms, min: 252.8µs, avg: 31.3ms, p95: 106.1ms, max_proc_keys: 10687, p95_proc_keys: 9184, tot_proc: 445ms, rpc_num: 24, rpc_time: 750.4ms, copr_cache_hit_ratio: 0.62, distsql_concurrency: 15}                                                                        | data:TableFullScan_43                             | 58.6 MB | N/A     |
|   └─TableFullScan_43         | 90000.00 | 90000   | cop[tikv] | table:t2      | tikv_task:{proc max:31ms, min:3ms, avg: 13.3ms, p80:24ms, p95:30ms, iters:181, tasks:24}, scan_detail: {total_process_keys: 69744, total_process_keys_size: 217533936, total_keys: 139497, get_snapshot_time: 730.2µs, rocksdb: {delete_skipped_count: 44208, key_skipped_count: 253431, block: {cache_hit_count: 3527}}}  | keep order:false                                  | N/A     | N/A     |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
```

> **Note:**
>
> In the above example, the SQL Optimizer selects the hash join plan which performs worse than the index join. Query optimization is an [NP-complete problem](https://en.wikipedia.org/wiki/NP-completeness), and less-than-optimal plans might be chosen. If this is a frequent query, it is recommended to use [SQL Plan Management](/sql-plan-management.md) to bind a hint to a query, which can be easier to manage than inserting hints into queries that your application sends to TiDB.

### Variations of Index Join

An index join operation using the hint [`INL_JOIN`](/optimizer-hints.md#inl_joint1_name--tl_name-) creates a hash table of the intermediate results before joining on the outer table. TiDB also supports creating a hash table on the outer table using the hint [`INL_HASH_JOIN`](/optimizer-hints.md#inl_hash_join). Each of these variations of index join is automatically selected by the SQL Optimizer.

### Configuration

Index join performance is influenced by the following system variables:

- [`tidb_index_join_batch_size`](/system-variables.md#tidb_index_join_batch_size) (default value: `25000`) - the batch size of `index lookup join` operations.
- [`tidb_index_lookup_join_concurrency`](/system-variables.md#tidb_index_lookup_join_concurrency) (default value: `4`) - the number of concurrent index lookup tasks.

## Hash Join

In a hash join operation, TiDB reads and caches the data on the `Build` side of the join in a hash table, and then reads the data on the `Probe` side of the join, probing the hash table to access required rows. Hash joins require more memory to execute than index joins but execute much faster when there are a lot of rows that need to be joined. The hash join operator is multi-threaded in TiDB and executes in parallel.

An example of hash join is as follows:

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

For the execution process of `HashJoin_27`, TiDB performs the following operations in order:

1. Cache the data of the `Build` side in memory.
2. Construct a Hash Table on the `Build` side based on the cached data.
3. Read the data at the `Probe` side.
4. Use the data of the `Probe` side to probe the Hash Table.
5. Return qualified data to the user.

The `operator info` column in the `EXPLAIN` result table also records other information about `HashJoin_27`, including whether the query is Inner Join or Outer Join, and what are the conditions of Join. In the above example, the query is an Inner Join, where the Join condition `equal:[eq(test.t1.id, test.t2.id)]` partly corresponds with the query condition `WHERE t1.id = t2.id`. The operator info of the other Join operators in the following examples is similar to this one.

### Runtime Statistics

If [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) (default value: 1 GB) is exceeded, and the [`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom) value is `ON` (default), TiDB will attempt to use temporary storage, and might create the `Build` operator (used as part of the hash join) on disk. Runtime statistics such as memory usage are recorded in the `execution info` of the `EXPLAIN ANALYZE` result table. The following example shows the output of `EXPLAIN ANALYZE` with a 1 GB (default) and a 500 MB quota for `tidb_mem_quota_query`. At 500 MB, disk is used for temporary storage:

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

### Configuration

Hash join performance is influenced by the following system variables:

- [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) (default value: 1GB) - if the memory quota for a query is exceeded, TiDB will attempt to spill the `Build` operator of a hash join to disk to save memory.
- [`tidb_hash_join_concurrency`](/system-variables.md#tidb_hash_join_concurrency) (default value: `5`) - the number of concurrent hash join tasks.

### Related optimizations

TiDB provides the Runtime Filter feature, which optimizes the performance of hash join and greatly improves its execution speed. For specific optimization usage, see [Runtime Filter](/runtime-filter.md).

## Merge Join

Merge join is a special sort of join that applies when both sides of the join are read in sorted order. It can be described as similar to an _efficient zipper merge_: as data is read on both the `Build` and the `Probe` sides of the join, the join operation works like a streaming operation. Merge joins require far less memory than hash join but do not execute in parallel.

The following is an example:

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

For the execution process of the merge join operator, TiDB performs the following operations:

1. Read all the data of a Join Group from the `Build` side into the memory.
2. Read the data of the `Probe` side.
3. Compare whether each row of data on the `Probe` side matches a complete Join Group on the `Build` side. Apart from equivalent conditions, there are non-equivalent conditions. Here "match" mainly refers to checking whether non-equivalent conditions are met. Join Group refers to the data with the same value among all Join Keys.
