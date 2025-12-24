---
title: SLOW_QUERY
summary: 了解 INFORMATION_SCHEMA 表 `SLOW_QUERY`。
---

# SLOW_QUERY

`SLOW_QUERY` 表中提供了当前节点的慢查询相关的信息，其内容通过解析当前节点的 TiDB [慢查询日志](/tidb-configuration-file.md#slow-query-file)而来，列名和慢日志中的字段名是一一对应。关于如何使用该表调查和改善慢查询，请参考[慢查询日志文档](/identify-slow-queries.md)。

```sql
USE INFORMATION_SCHEMA;
DESC slow_query;
```

输出结果示例如下：

```sql
+--------------------------------------------+-----------------+------+------+---------+-------+
| Field                                      | Type            | Null | Key  | Default | Extra |
+--------------------------------------------+-----------------+------+------+---------+-------+
| Time                                       | timestamp(6)    | NO   | PRI  | NULL    |       |
| Txn_start_ts                               | bigint unsigned | YES  |      | NULL    |       |
| User                                       | varchar(64)     | YES  |      | NULL    |       |
| Host                                       | varchar(64)     | YES  |      | NULL    |       |
| Conn_ID                                    | bigint unsigned | YES  |      | NULL    |       |
| Session_alias                              | varchar(64)     | YES  |      | NULL    |       |
| Exec_retry_count                           | bigint unsigned | YES  |      | NULL    |       |
| Exec_retry_time                            | double          | YES  |      | NULL    |       |
| Query_time                                 | double          | YES  |      | NULL    |       |
| Parse_time                                 | double          | YES  |      | NULL    |       |
| Compile_time                               | double          | YES  |      | NULL    |       |
| Rewrite_time                               | double          | YES  |      | NULL    |       |
| Preproc_subqueries                         | bigint unsigned | YES  |      | NULL    |       |
| Preproc_subqueries_time                    | double          | YES  |      | NULL    |       |
| Optimize_time                              | double          | YES  |      | NULL    |       |
| Wait_TS                                    | double          | YES  |      | NULL    |       |
| Prewrite_time                              | double          | YES  |      | NULL    |       |
| Wait_prewrite_binlog_time                  | double          | YES  |      | NULL    |       |
| Commit_time                                | double          | YES  |      | NULL    |       |
| Get_commit_ts_time                         | double          | YES  |      | NULL    |       |
| Commit_backoff_time                        | double          | YES  |      | NULL    |       |
| Backoff_types                              | varchar(64)     | YES  |      | NULL    |       |
| Resolve_lock_time                          | double          | YES  |      | NULL    |       |
| Local_latch_wait_time                      | double          | YES  |      | NULL    |       |
| Write_keys                                 | bigint          | YES  |      | NULL    |       |
| Write_size                                 | bigint          | YES  |      | NULL    |       |
| Prewrite_region                            | bigint          | YES  |      | NULL    |       |
| Txn_retry                                  | bigint          | YES  |      | NULL    |       |
| Cop_time                                   | double          | YES  |      | NULL    |       |
| Process_time                               | double          | YES  |      | NULL    |       |
| Wait_time                                  | double          | YES  |      | NULL    |       |
| Backoff_time                               | double          | YES  |      | NULL    |       |
| LockKeys_time                              | double          | YES  |      | NULL    |       |
| Request_count                              | bigint unsigned | YES  |      | NULL    |       |
| Total_keys                                 | bigint unsigned | YES  |      | NULL    |       |
| Process_keys                               | bigint unsigned | YES  |      | NULL    |       |
| Rocksdb_delete_skipped_count               | bigint unsigned | YES  |      | NULL    |       |
| Rocksdb_key_skipped_count                  | bigint unsigned | YES  |      | NULL    |       |
| Rocksdb_block_cache_hit_count              | bigint unsigned | YES  |      | NULL    |       |
| Rocksdb_block_read_count                   | bigint unsigned | YES  |      | NULL    |       |
| Rocksdb_block_read_byte                    | bigint unsigned | YES  |      | NULL    |       |
| DB                                         | varchar(64)     | YES  |      | NULL    |       |
| Index_names                                | varchar(100)    | YES  |      | NULL    |       |
| Is_internal                                | tinyint(1)      | YES  |      | NULL    |       |
| Digest                                     | varchar(64)     | YES  |      | NULL    |       |
| Stats                                      | varchar(512)    | YES  |      | NULL    |       |
| Cop_proc_avg                               | double          | YES  |      | NULL    |       |
| Cop_proc_p90                               | double          | YES  |      | NULL    |       |
| Cop_proc_max                               | double          | YES  |      | NULL    |       |
| Cop_proc_addr                              | varchar(64)     | YES  |      | NULL    |       |
| Cop_wait_avg                               | double          | YES  |      | NULL    |       |
| Cop_wait_p90                               | double          | YES  |      | NULL    |       |
| Cop_wait_max                               | double          | YES  |      | NULL    |       |
| Cop_wait_addr                              | varchar(64)     | YES  |      | NULL    |       |
| Mem_max                                    | bigint          | YES  |      | NULL    |       |
| Disk_max                                   | bigint          | YES  |      | NULL    |       |
| KV_total                                   | double          | YES  |      | NULL    |       |
| PD_total                                   | double          | YES  |      | NULL    |       |
| Backoff_total                              | double          | YES  |      | NULL    |       |
| Unpacked_bytes_sent_tikv_total             | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_received_tikv_total         | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_sent_tikv_cross_zone        | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_received_tikv_cross_zone    | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_sent_tiflash_total          | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_received_tiflash_total      | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_sent_tiflash_cross_zone     | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_received_tiflash_cross_zone | bigint          | YES  |      | NULL    |       |
| Write_sql_response_total                   | double          | YES  |      | NULL    |       |
| Result_rows                                | bigint          | YES  |      | NULL    |       |
| Warnings                                   | longtext        | YES  |      | NULL    |       |
| Backoff_Detail                             | varchar(4096)   | YES  |      | NULL    |       |
| Prepared                                   | tinyint(1)      | YES  |      | NULL    |       |
| Succ                                       | tinyint(1)      | YES  |      | NULL    |       |
| IsExplicitTxn                              | tinyint(1)      | YES  |      | NULL    |       |
| IsWriteCacheTable                          | tinyint(1)      | YES  |      | NULL    |       |
| Plan_from_cache                            | tinyint(1)      | YES  |      | NULL    |       |
| Plan_from_binding                          | tinyint(1)      | YES  |      | NULL    |       |
| Has_more_results                           | tinyint(1)      | YES  |      | NULL    |       |
| Resource_group                             | varchar(64)     | YES  |      | NULL    |       |
| Request_unit_read                          | double          | YES  |      | NULL    |       |
| Request_unit_write                         | double          | YES  |      | NULL    |       |
| Time_queued_by_rc                          | double          | YES  |      | NULL    |       |
| Tidb_cpu_time                              | double          | YES  |      | NULL    |       |
| Tikv_cpu_time                              | double          | YES  |      | NULL    |       |
| Plan                                       | longtext        | YES  |      | NULL    |       |
| Plan_digest                                | varchar(128)    | YES  |      | NULL    |       |
| Binary_plan                                | longtext        | YES  |      | NULL    |       |
| Prev_stmt                                  | longtext        | YES  |      | NULL    |       |
| Query                                      | longtext        | YES  |      | NULL    |       |
+--------------------------------------------+-----------------+------+------+---------+-------+
89 rows in set (0.00 sec)
```

`Query` 列的语句长度上限由系统变量 [`tidb_stmt_summary_max_sql_length`](/system-variables.md#tidb_stmt_summary_max_sql_length-从-v40-版本开始引入) 控制。

## CLUSTER_SLOW_QUERY table

`CLUSTER_SLOW_QUERY` 表中提供了集群所有节点的慢查询相关的信息，其内容通过解析 TiDB 慢查询日志而来，该表使用上和 `SLOW_QUERY` 表一样。`CLUSTER_SLOW_QUERY` 表结构上比 `SLOW_QUERY` 多一列 `INSTANCE`，表示该行慢查询信息来自的 TiDB 节点地址。关于如何使用该表调查和改善慢查询，请参考[慢查询日志文档](/identify-slow-queries.md)。

```sql
DESC CLUSTER_SLOW_QUERY;
```

输出结果示例如下：

```sql
+--------------------------------------------+-----------------+------+------+---------+-------+
| Field                                      | Type            | Null | Key  | Default | Extra |
+--------------------------------------------+-----------------+------+------+---------+-------+
| INSTANCE                                   | varchar(64)     | YES  |      | NULL    |       |
| Time                                       | timestamp(6)    | NO   | PRI  | NULL    |       |
| Txn_start_ts                               | bigint unsigned | YES  |      | NULL    |       |
| User                                       | varchar(64)     | YES  |      | NULL    |       |
| Host                                       | varchar(64)     | YES  |      | NULL    |       |
| Conn_ID                                    | bigint unsigned | YES  |      | NULL    |       |
| Session_alias                              | varchar(64)     | YES  |      | NULL    |       |
| Exec_retry_count                           | bigint unsigned | YES  |      | NULL    |       |
| Exec_retry_time                            | double          | YES  |      | NULL    |       |
| Query_time                                 | double          | YES  |      | NULL    |       |
| Parse_time                                 | double          | YES  |      | NULL    |       |
| Compile_time                               | double          | YES  |      | NULL    |       |
| Rewrite_time                               | double          | YES  |      | NULL    |       |
| Preproc_subqueries                         | bigint unsigned | YES  |      | NULL    |       |
| Preproc_subqueries_time                    | double          | YES  |      | NULL    |       |
| Optimize_time                              | double          | YES  |      | NULL    |       |
| Wait_TS                                    | double          | YES  |      | NULL    |       |
| Prewrite_time                              | double          | YES  |      | NULL    |       |
| Wait_prewrite_binlog_time                  | double          | YES  |      | NULL    |       |
| Commit_time                                | double          | YES  |      | NULL    |       |
| Get_commit_ts_time                         | double          | YES  |      | NULL    |       |
| Commit_backoff_time                        | double          | YES  |      | NULL    |       |
| Backoff_types                              | varchar(64)     | YES  |      | NULL    |       |
| Resolve_lock_time                          | double          | YES  |      | NULL    |       |
| Local_latch_wait_time                      | double          | YES  |      | NULL    |       |
| Write_keys                                 | bigint          | YES  |      | NULL    |       |
| Write_size                                 | bigint          | YES  |      | NULL    |       |
| Prewrite_region                            | bigint          | YES  |      | NULL    |       |
| Txn_retry                                  | bigint          | YES  |      | NULL    |       |
| Cop_time                                   | double          | YES  |      | NULL    |       |
| Process_time                               | double          | YES  |      | NULL    |       |
| Wait_time                                  | double          | YES  |      | NULL    |       |
| Backoff_time                               | double          | YES  |      | NULL    |       |
| LockKeys_time                              | double          | YES  |      | NULL    |       |
| Request_count                              | bigint unsigned | YES  |      | NULL    |       |
| Total_keys                                 | bigint unsigned | YES  |      | NULL    |       |
| Process_keys                               | bigint unsigned | YES  |      | NULL    |       |
| Rocksdb_delete_skipped_count               | bigint unsigned | YES  |      | NULL    |       |
| Rocksdb_key_skipped_count                  | bigint unsigned | YES  |      | NULL    |       |
| Rocksdb_block_cache_hit_count              | bigint unsigned | YES  |      | NULL    |       |
| Rocksdb_block_read_count                   | bigint unsigned | YES  |      | NULL    |       |
| Rocksdb_block_read_byte                    | bigint unsigned | YES  |      | NULL    |       |
| DB                                         | varchar(64)     | YES  |      | NULL    |       |
| Index_names                                | varchar(100)    | YES  |      | NULL    |       |
| Is_internal                                | tinyint(1)      | YES  |      | NULL    |       |
| Digest                                     | varchar(64)     | YES  |      | NULL    |       |
| Stats                                      | varchar(512)    | YES  |      | NULL    |       |
| Cop_proc_avg                               | double          | YES  |      | NULL    |       |
| Cop_proc_p90                               | double          | YES  |      | NULL    |       |
| Cop_proc_max                               | double          | YES  |      | NULL    |       |
| Cop_proc_addr                              | varchar(64)     | YES  |      | NULL    |       |
| Cop_wait_avg                               | double          | YES  |      | NULL    |       |
| Cop_wait_p90                               | double          | YES  |      | NULL    |       |
| Cop_wait_max                               | double          | YES  |      | NULL    |       |
| Cop_wait_addr                              | varchar(64)     | YES  |      | NULL    |       |
| Mem_max                                    | bigint          | YES  |      | NULL    |       |
| Disk_max                                   | bigint          | YES  |      | NULL    |       |
| KV_total                                   | double          | YES  |      | NULL    |       |
| PD_total                                   | double          | YES  |      | NULL    |       |
| Backoff_total                              | double          | YES  |      | NULL    |       |
| Unpacked_bytes_sent_tikv_total             | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_received_tikv_total         | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_sent_tikv_cross_zone        | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_received_tikv_cross_zone    | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_sent_tiflash_total          | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_received_tiflash_total      | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_sent_tiflash_cross_zone     | bigint          | YES  |      | NULL    |       |
| Unpacked_bytes_received_tiflash_cross_zone | bigint          | YES  |      | NULL    |       |
| Write_sql_response_total                   | double          | YES  |      | NULL    |       |
| Result_rows                                | bigint          | YES  |      | NULL    |       |
| Warnings                                   | longtext        | YES  |      | NULL    |       |
| Backoff_Detail                             | varchar(4096)   | YES  |      | NULL    |       |
| Prepared                                   | tinyint(1)      | YES  |      | NULL    |       |
| Succ                                       | tinyint(1)      | YES  |      | NULL    |       |
| IsExplicitTxn                              | tinyint(1)      | YES  |      | NULL    |       |
| IsWriteCacheTable                          | tinyint(1)      | YES  |      | NULL    |       |
| Plan_from_cache                            | tinyint(1)      | YES  |      | NULL    |       |
| Plan_from_binding                          | tinyint(1)      | YES  |      | NULL    |       |
| Has_more_results                           | tinyint(1)      | YES  |      | NULL    |       |
| Resource_group                             | varchar(64)     | YES  |      | NULL    |       |
| Request_unit_read                          | double          | YES  |      | NULL    |       |
| Request_unit_write                         | double          | YES  |      | NULL    |       |
| Time_queued_by_rc                          | double          | YES  |      | NULL    |       |
| Tidb_cpu_time                              | double          | YES  |      | NULL    |       |
| Tikv_cpu_time                              | double          | YES  |      | NULL    |       |
| Plan                                       | longtext        | YES  |      | NULL    |       |
| Plan_digest                                | varchar(128)    | YES  |      | NULL    |       |
| Binary_plan                                | longtext        | YES  |      | NULL    |       |
| Prev_stmt                                  | longtext        | YES  |      | NULL    |       |
| Query                                      | longtext        | YES  |      | NULL    |       |
+--------------------------------------------+-----------------+------+------+---------+-------+
90 rows in set (0.00 sec)
```

查询集群系统表时，TiDB 也会将相关计算下推给其他节点执行，而不是把所有节点的数据都取回来，可以查看执行计划，如下：

```sql
DESC SELECT COUNT(*) FROM CLUSTER_SLOW_QUERY WHERE user = 'u1';
```

输出结果示例如下：

```sql
+----------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| id                         | estRows  | task      | access object            | operator info                                        |
+----------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| StreamAgg_7                | 1.00     | root      |                          | funcs:count(1)->Column#75                            |
| └─TableReader_13           | 10.00    | root      |                          | data:Selection_12                                    |
|   └─Selection_12           | 10.00    | cop[tidb] |                          | eq(INFORMATION_SCHEMA.cluster_slow_query.user, "u1") |
|     └─TableFullScan_11     | 10000.00 | cop[tidb] | table:CLUSTER_SLOW_QUERY | keep order:false, stats:pseudo                       |
+----------------------------+----------+-----------+--------------------------+------------------------------------------------------+
4 rows in set (0.00 sec)
```

上面执行计划表示，会将 `user = u1` 条件下推给其他的 (`cop`) TiDB 节点执行，也会把聚合算子（即上面输出结果中的 `StreamAgg` 算子）下推。

目前由于没有对系统表收集统计信息，所以有时会导致某些聚合算子不能下推，导致执行较慢，用户可以通过手动指定聚合下推的 SQL HINT 来将聚合算子下推，示例如下：

```sql
SELECT /*+ AGG_TO_COP() */ COUNT(*) FROM CLUSTER_SLOW_QUERY GROUP BY user;
```

## 查看执行信息

通过对 `SLOW_QUERY` 表执行 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)，你可以获取数据库如何检索慢查询信息的详情。然而，如果对 `CLUSTER_SLOW_QUERY` 表执行 `EXPLAIN ANALYZE`，将无法获取这些信息。

示例：

```sql
EXPLAIN ANALYZE SELECT * FROM INFORMATION_SCHEMA.SLOW_QUERY LIMIT 1\G
```

```
*************************** 1. row ***************************
            id: Limit_7
       estRows: 1.00
       actRows: 1
          task: root
 access object:
execution info: time:3.46ms, loops:2, RU:0.000000
 operator info: offset:0, count:1
        memory: N/A
          disk: N/A
*************************** 2. row ***************************
            id: └─MemTableScan_10
       estRows: 10000.00
       actRows: 64
          task: root
 access object: table:SLOW_QUERY
execution info: time:3.45ms, loops:1, initialize: 55.5µs, read_file: 1.21ms, parse_log: {time:4.11ms, concurrency:15}, total_file: 1, read_file: 1, read_size: 4.06 MB
 operator info: only search in the current 'tidb-slow.log' file
        memory: 1.26 MB
          disk: N/A
2 rows in set (0.01 sec)
```

在输出中，查看 `execution info` 中的以下字段（为便于阅读，这些字段的格式已优化）：

```
initialize: 55.5µs,
read_file: 1.21ms,
parse_log: {
  time:4.11ms,
  concurrency:15
},
total_file: 1,
read_file: 1,
read_size: 4.06 MB
```

| 字段 | 描述 |
|---|---|
| `initialize` | 用于初始化的时间 |
| `read_file` | 用于读取慢日志文件的时间 |
| `parse_log.time` | 用于解析慢日志文件的时间 |
| `parse_log.concurrency` | 解析慢日志文件的并发度（由 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 控制） |
| `total_file` | 慢日志文件的总数 |
| `read_file` | 已读取的慢日志文件数 |
| `read_size` | 从日志文件中读取的字节数 |
