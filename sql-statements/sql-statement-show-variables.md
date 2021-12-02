---
title: SHOW [GLOBAL|SESSION] VARIABLES
summary: TiDB 数据库中 SHOW [GLOBAL|SESSION] VARIABLES 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-variables/','/docs-cn/dev/reference/sql/statements/show-variables/']
---

# SHOW [GLOBAL|SESSION] VARIABLES

`SHOW [GLOBAL|SESSION] VARIABLES` 语句用于显示 `GLOBAL` 或 `SESSION` 范围的变量列表。如果未指定范围，则应用默认范围 `SESSION`。

## 语法图

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

**GlobalScope:**

![GlobalScope](/media/sqlgram/GlobalScope.png)

## 示例

查看 TiDB 定义的专用系统变量，关于这些变量的含义参见[系统变量和语法](/system-variables.md)。

{{< copyable "sql" >}}

```sql
SHOW GLOBAL VARIABLES LIKE 'tidb%';
```

```sql
+-------------------------------------+---------------------+
| Variable_name                       | Value               |
+-------------------------------------+---------------------+
| tidb_allow_batch_cop                | 0                   |
| tidb_allow_remove_auto_inc          | 0                   |
| tidb_auto_analyze_end_time          | 23:59 +0000         |
| tidb_auto_analyze_ratio             | 0.5                 |
| tidb_auto_analyze_start_time        | 00:00 +0000         |
| tidb_backoff_lock_fast              | 100                 |
| tidb_backoff_weight                 | 2                   |
| tidb_batch_commit                   | 0                   |
| tidb_batch_delete                   | 0                   |
| tidb_batch_insert                   | 0                   |
| tidb_build_stats_concurrency        | 4                   |
| tidb_capture_plan_baselines         | off                 |
| tidb_check_mb4_value_in_utf8        | 1                   |
| tidb_checksum_table_concurrency     | 4                   |
| tidb_config                         |                     |
| tidb_constraint_check_in_place      | 0                   |
| tidb_current_ts                     | 0                   |
| tidb_ddl_error_count_limit          | 512                 |
| tidb_ddl_reorg_batch_size           | 256                 |
| tidb_ddl_reorg_priority             | PRIORITY_LOW        |
| tidb_ddl_reorg_worker_cnt           | 4                   |
| tidb_disable_txn_auto_retry         | 1                   |
| tidb_distsql_scan_concurrency       | 15                  |
| tidb_dml_batch_size                 | 20000               |
| tidb_enable_cascades_planner        | 0                   |
| tidb_enable_chunk_rpc               | 1                   |
| tidb_enable_collect_execution_info  | 1                   |
| tidb_enable_fast_analyze            | 0                   |
| tidb_enable_index_merge             | 0                   |
| tidb_enable_noop_functions          | 0                   |
| tidb_enable_radix_join              | 0                   |
| tidb_enable_slow_log                | 1                   |
| tidb_enable_stmt_summary            | 1                   |
| tidb_enable_table_partition          | on                  |
| tidb_enable_vectorized_expression   | 1                   |
| tidb_enable_window_function         | 1                   |
| tidb_evolve_plan_baselines          | off                 |
| tidb_evolve_plan_task_end_time      | 23:59 +0000         |
| tidb_evolve_plan_task_max_time      | 600                 |
| tidb_evolve_plan_task_start_time    | 00:00 +0000         |
| tidb_expensive_query_time_threshold | 60                  |
| tidb_force_priority                 | NO_PRIORITY         |
| tidb_general_log                    | 0                   |
| tidb_hash_join_concurrency          | 5                   |
| tidb_hashagg_final_concurrency      | 4                   |
| tidb_hashagg_partial_concurrency    | 4                   |
| tidb_index_join_batch_size          | 25000               |
| tidb_index_lookup_concurrency       | 4                   |
| tidb_index_lookup_join_concurrency  | 4                   |
| tidb_index_lookup_size              | 20000               |
| tidb_index_serial_scan_concurrency  | 1                   |
| tidb_init_chunk_size                | 32                  |
| tidb_isolation_read_engines         | tikv, tiflash, tidb |
| tidb_low_resolution_tso             | 0                   |
| tidb_max_chunk_size                 | 1024                |
| tidb_max_delta_schema_count         | 1024                |
| tidb_mem_quota_hashjoin             | 34359738368         |
| tidb_mem_quota_indexlookupjoin      | 34359738368         |
| tidb_mem_quota_indexlookupreader    | 34359738368         |
| tidb_mem_quota_mergejoin            | 34359738368         |
| tidb_mem_quota_nestedloopapply      | 34359738368         |
| tidb_mem_quota_query                | 1073741824          |
| tidb_mem_quota_sort                 | 34359738368         |
| tidb_mem_quota_topn                 | 34359738368         |
| tidb_metric_query_range_duration    | 60                  |
| tidb_metric_query_step              | 60                  |
| tidb_opt_agg_push_down              | 0                   |
| tidb_opt_concurrency_factor         | 3                   |
| tidb_opt_copcpu_factor              | 3                   |
| tidb_opt_correlation_exp_factor     | 1                   |
| tidb_opt_correlation_threshold      | 0.9                 |
| tidb_opt_cpu_factor                 | 3                   |
| tidb_opt_desc_factor                | 3                   |
| tidb_opt_disk_factor                | 1.5                 |
| tidb_opt_distinct_agg_push_down     | 0                   |
| tidb_opt_insubq_to_join_and_agg     | 1                   |
| tidb_opt_join_reorder_threshold     | 0                   |
| tidb_opt_memory_factor              | 0.001               |
| tidb_opt_network_factor             | 1                   |
| tidb_opt_scan_factor                | 1.5                 |
| tidb_opt_seek_factor                | 20                  |
| tidb_opt_write_row_id               | 0                   |
| tidb_optimizer_selectivity_level    | 0                   |
| tidb_pprof_sql_cpu                  | 0                   |
| tidb_projection_concurrency         | 4                   |
| tidb_query_log_max_len              | 4096                |
| tidb_record_plan_in_slow_log        | 1                   |
| tidb_replica_read                   | leader              |
| tidb_retry_limit                    | 10                  |
| tidb_row_format_version             | 2                   |
| tidb_scatter_region                 | 0                   |
| tidb_skip_isolation_level_check     | 0                   |
| tidb_skip_utf8_check                | 0                   |
| tidb_slow_log_threshold             | 300                 |
| tidb_slow_query_file                | tidb-slow.log       |
| tidb_snapshot                       |                     |
| tidb_stmt_summary_history_size      | 24                  |
| tidb_stmt_summary_internal_query    | 0                   |
| tidb_stmt_summary_max_sql_length    | 4096                |
| tidb_stmt_summary_max_stmt_count    | 3000                |
| tidb_stmt_summary_refresh_interval  | 1800                |
| tidb_store_limit                    | 0                   |
| tidb_txn_mode                       |                     |
| tidb_use_plan_baselines             | on                  |
| tidb_wait_split_region_finish       | 1                   |
| tidb_wait_split_region_timeout      | 300                 |
| tidb_window_concurrency             | 4                   |
+-------------------------------------+---------------------+
108 rows in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SHOW GLOBAL VARIABLES LIKE 'time_zone%';
```

```
+---------------+--------+
| Variable_name | Value  |
+---------------+--------+
| time_zone     | SYSTEM |
+---------------+--------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SHOW [GLOBAL|SESSION] VARIABLES` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [`SET [GLOBAL|SESSION]`](/sql-statements/sql-statement-set-variable.md)
