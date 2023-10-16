---
title: Limited SQL Features on TiDB Cloud
summary: Learn about the limited SQL features on TiDB Cloud.
---

# Limited SQL features on TiDB Cloud

TiDB Cloud works with almost all workloads that TiDB supports, but there are some feature differences between TiDB Self-Hosted and TiDB Dedicated/Serverless. This document describes the limitations of SQL features on TiDB Cloud. We are constantly filling in the feature gaps between TiDB Self-Hosted and TiDB Dedicated/Serverless. If you require these features or capabilities in the gap, [contact us](/tidb-cloud/tidb-cloud-support.md) for a feature request.

## Statements

### Placement and range management

| Statement | TiDB Dedicated | TiDB Serverless |
|:-|:-|:-|
| `ALTER PLACEMENT POLICY` | Supported | Not supported [^1] |
| `CREATE PLACEMENT POLICY` | Supported | Not supported [^1] |
| `DROP PLACEMENT POLICY` | Supported | Not supported [^1] |
| `SHOW CREATE PLACEMENT POLICY` | Supported | Not supported [^1] |
| `SHOW PLACEMENT` | Supported | Not supported [^1] |
| `SHOW PLACEMENT FOR` | Supported | Not supported [^1] |
| `SHOW PLACEMENT LABELS` | Supported | Not supported [^1] |
| `SHOW TABLE REGIONS` | Supported | Not supported [^1] |
| `SPLIT REGION` | Supported | Not supported [^1] |

### Resource groups

| Statement | TiDB Dedicated | TiDB Serverless |
|:-|:-|:-|
| `ALTER RESOURCE GROUP` | Supported | Not supported [^2] |
| `CALIBRATE RESOURCE` | Not supported | Not supported [^2] |
| `CREATE RESOURCE GROUP` | Supported | Not supported [^2] |
| `DROP RESOURCE GROUP` | Supported | Not supported [^2] |
| `SET RESOURCE GROUP` | Supported | Not supported [^2] |
| `SHOW CREATE RESOURCE GROUP` | Supported | Not supported [^2] |

### Others

| Statement | TiDB Dedicated | TiDB Serverless |
|:-|:-|:-|
| `BACKUP` | Supported | Not supported [^3] |
| `SHOW BACKUPS` | Supported | Not supported [^3] |
| `RESTORE` | Supported | Not supported [^3] |
| `SHOW RESTORES` | Supported | Not supported [^3] |
| `ADMIN RESET TELEMETRY_ID` | Supported | Telemetry is not supported on TiDB Serverless. |
| `ADMIN SHOW TELEMETRY` | Not supported [^4] | Not supported [^4] |
| `ADMIN SHOW SLOW` | Supported | Not supported [^5] |
| `ADMIN PLUGINS ENABLE` | Supported | Not supported [^8] |
| `ADMIN PLUGINS DISABLE` | Supported | Not supported [^8] |
| `ALTER INSTANCE RELOAD TLS` | Supported | TiDB Serverless automatically refreshes the TLS certificate. |
| `LOAD DATA INFILE` | Only supports `LOAD DATA LOCAL INFILE` | Only supports `LOAD DATA LOCAL INFILE` |
| `CHANGE DRAINER` | Not supported [^7] | Not supported [^7] |
| `CHANGE PUMP` | Not supported [^7] | Not supported [^7] |
| `FLASHBACK CLUSTER TO TIMESTAMP` | Supported | Not supported [^3] |
| `LOAD STATS` | Supported | Not supported |
| `SELECT ... INTO OUTFILE` | Not supported [^4] | Not supported [^4] |
| `SET CONFIG` | Not supported [^4] | Not supported [^4] |
| `SHOW CONFIG` | Not supported [^4] | Not supported [^4] |
| `SHOW DRAINER STATUS` | Not supported [^7] | Not supported [^7] |
| `SHOW PLUGINS` | Supported | Not supported [^8] |
| `SHOW PUMP STATUS` | Not supported [^7] | Not supported [^7] |
| `SHUTDOWN` | Not supported [^4] | Not supported [^4] |
| `CREATE TABLE ... AUTO_ID_CACHE` | Supported | Not supported [^12] |

## Functions and operators

| Function and operator | TiDB Dedicated | TiDB Serverless |
|:-|:-|:-|
| `SLEEP` | No Limitation | The [`SLEEP()` function](https://docs.pingcap.com/tidbcloud/miscellaneous-functions) has a limitation wherein it can only support a maximum sleep time of 300 seconds.|

## System tables

| Database | Table | TiDB Dedicated | TiDB Serverless |
|:-|:-|:-|:-|
| `information_schema` | `ATTRIBUTES` | Supported | Not supported [^1] |
| `information_schema` | `CLUSTER_CONFIG` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `CLUSTER_HARDWARE` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `CLUSTER_INFO` | Supported | Not supported [^1] |
| `information_schema` | `CLUSTER_LOAD` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `CLUSTER_LOG` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `CLUSTER_SLOW_QUERY` | Supported | Not supported [^5] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY` | Supported | Not supported [^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_EVICTED` | Supported | Not supported [^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_HISTORY` | Supported | Not supported [^6] |
| `information_schema` | `CLUSTER_SYSTEMINFO` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `INSPECTION_RESULT` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `INSPECTION_RULES` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `INSPECTION_SUMMARY` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `METRICS_SUMMARY` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `METRICS_SUMMARY_BY_LABEL` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `METRICS_TABLES` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `PLACEMENT_POLICIES` | Supported | Not supported [^1] |
| `information_schema` | `RESOURCE_GROUPS` | Supported | Not supported [^2] |
| `information_schema` | `SLOW_QUERY` | Supported | Not supported [^5] |
| `information_schema` | `STATEMENTS_SUMMARY` | Supported | Not supported [^6] |
| `information_schema` | `STATEMENTS_SUMMARY_EVICTED` | Supported | Not supported [^6] |
| `information_schema` | `STATEMENTS_SUMMARY_HISTORY` | Supported | Not supported [^6] |
| `information_schema` | `TIDB_HOT_REGIONS` | Not supported [^4] | Not supported [^4] |
| `information_schema` | `TIDB_HOT_REGIONS_HISTORY` | Supported | Not supported [^1] |
| `information_schema` | `TIDB_SERVERS_INFO` | Supported | Not supported [^1] |
| `information_schema` | `TIFLASH_SEGMENTS` | Supported | Not supported [^1] |
| `information_schema` | `TIFLASH_TABLES` | Supported | Not supported [^1] |
| `information_schema` | `TIKV_REGION_PEERS` | Supported | Not supported [^1] |
| `information_schema` | `TIKV_REGION_STATUS` | Supported | Not supported [^1] |
| `information_schema` | `TIKV_STORE_STATUS` | Supported | Not supported [^1] |
| `performance_schema` | `pd_profile_allocs` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `pd_profile_block` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `pd_profile_cpu` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `pd_profile_goroutines` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `pd_profile_memory` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `pd_profile_mutex` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `tidb_profile_allocs` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `tidb_profile_block` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `tidb_profile_cpu` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `tidb_profile_goroutines` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `tidb_profile_memory` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `tidb_profile_mutex` | Not supported [^4] | Not supported [^4] |
| `performance_schema` | `tikv_profile_cpu` | Not supported [^4] | Not supported [^4] |
| `mysql` | `expr_pushdown_blacklist` | Not supported [^4] | Not supported [^4] |
| `mysql` | `gc_delete_range` | Not supported [^4] | Not supported [^4] |
| `mysql` | `gc_delete_range_done` | Not supported [^4] | Not supported [^4] |
| `mysql` | `opt_rule_blacklist` | Not supported [^4] | Not supported [^4] |
| `mysql` | `tidb` | Not supported [^4] | Not supported [^4] |
| `mysql` | `tidb_ttl_job_history` | Supported | Not supported [^9] |
| `mysql` | `tidb_ttl_table_status` | Supported | Not supported [^9] |
| `mysql` | `tidb_ttl_task` | Supported | Not supported [^9] |

## System variables

| Variable | TiDB Dedicated | TiDB Serverless |
|:-|:-|:-|
| `datadir` | No limitation | Not supported [^1] |
| `interactive_timeout` | No limitation | Read-only [^11] |
| `max_allowed_packet` | No limitation | Read-only [^11] |
| `plugin_dir` | No limitation | Not supported [^8] |
| `plugin_load` | No limitation | Not supported [^8] |
| `require_secure_transport` | Not supported [^13] | Read-only [^11] |
| `skip_name_resolve` | No limitation | Read-only [^11] |
| `sql_log_bin` | No limitation | Read-only [^11] |
| `tidb_cdc_write_source` | No limitation | Read-only [^11] |
| `tidb_check_mb4_value_in_utf8` | Not supported [^4] | Not supported [^4] |
| `tidb_config` | Not supported [^4] | Not supported [^4] |
| `tidb_ddl_disk_quota` | No limitation | Read-only [^11] |
| `tidb_ddl_enable_fast_reorg` | No limitation | Read-only [^11] |
| `tidb_ddl_error_count_limit` | No limitation | Read-only [^11] |
| `tidb_ddl_flashback_concurrency` | No limitation | Read-only [^11] |
| `tidb_ddl_reorg_batch_size` | No limitation | Read-only [^11] |
| `tidb_ddl_reorg_priority` | No limitation | Read-only [^11] |
| `tidb_ddl_reorg_worker_cnt` | No limitation | Read-only [^11] |
| `tidb_enable_1pc` | No limitation | Read-only [^11] |
| `tidb_enable_async_commit` | No limitation | Read-only [^11] |
| `tidb_enable_auto_analyze` | No limitation | Read-only [^11] |
| `tidb_enable_collect_execution_info` | Not supported [^4] | Not supported [^4] |
| `tidb_enable_ddl` | No limitation | Read-only [^11] |
| `tidb_enable_gc_aware_memory_track` | No limitation | Read-only [^11] |
| `tidb_enable_gogc_tuner` | No limitation | Read-only [^11] |
| `tidb_enable_local_txn` | No limitation | Read-only [^11] |
| `tidb_enable_resource_control` | No limitation | Read-only [^11] |
| `tidb_enable_slow_log` | Not supported [^4] | Not supported [^4] |
| `tidb_enable_stmt_summary` | No limitation | Read-only [^11] |
| `tidb_enable_telemetry` | Not supported [^4] | Not supported [^4] |
| `tidb_enable_top_sql` | No limitation | Read-only [^11] |
| `tidb_enable_tso_follower_proxy` | No limitation | Read-only [^11] |
| `tidb_expensive_query_time_threshold` | Not supported [^4] | Not supported [^4] |
| `tidb_force_priority` | Not supported [^4] | Not supported [^4] |
| `tidb_gc_concurrency` | No limitation | Read-only [^11] |
| `tidb_gc_enable` | No limitation | Read-only [^11] |
| `tidb_gc_life_time` | No limitation | Read-only [^11] |
| `tidb_gc_max_wait_time` | No limitation | Read-only [^11] |
| `tidb_gc_run_interval` | No limitation | Read-only [^11] |
| `tidb_gc_scan_lock_mode` | No limitation | Read-only [^11] |
| `tidb_general_log` | Not supported [^4] | Not supported [^4] |
| `tidb_generate_binary_plan` | No limitation | Read-only [^11] |
| `tidb_gogc_tuner_threshold` | No limitation | Read-only [^11] |
| `tidb_guarantee_linearizability` | No limitation | Read-only [^11] |
| `tidb_isolation_read_engines` | No limitation | Read-only [^11] |
| `tidb_log_file_max_days` | No limitation | Read-only [^11] |
| `tidb_memory_usage_alarm_ratio` | Not supported [^4] | Not supported [^4] |
| `tidb_metric_query_range_duration` | Not supported [^4] | Not supported [^4] |
| `tidb_metric_query_step` | Not supported [^4] | Not supported [^4] |
| `tidb_opt_write_row_id` | Not supported [^4] | Not supported [^4] |
| `tidb_placement_mode` | No limitation | Read-only [^11] |
| `tidb_pprof_sql_cpu` | Not supported [^4] | Not supported [^4] |
| `tidb_record_plan_in_slow_log` | Not supported [^4] | Not supported [^4] |
| `tidb_redact_log` | Not supported [^4] | Not supported [^4] |
| `tidb_restricted_read_only` | Not supported [^4] | Not supported [^4] |
| `tidb_row_format_version` | Not supported [^4] | Not supported [^4] |
| `tidb_scatter_region` | No limitation | Read-only [^11] |
| `tidb_server_memory_limit` | No limitation | Read-only [^11] |
| `tidb_server_memory_limit_gc_trigger` | No limitation | Read-only [^11] |
| `tidb_server_memory_limit_sess_min_size` | No limitation | Read-only [^11] |
| `tidb_simplified_metrics` | No limitation | Read-only [^11] |
| `tidb_slow_query_file` | Not supported [^4] | Not supported [^4] |
| `tidb_slow_log_threshold` | Not supported [^4] | Not supported [^4] |
| `tidb_slow_txn_log_threshold` | Not supported [^4] | Not supported [^4] |
| `tidb_stats_load_sync_wait` | No limitation | Read-only [^11] |
| `tidb_stmt_summary_history_size` | No limitation | Read-only [^11] |
| `tidb_stmt_summary_internal_query` | No limitation | Read-only [^11] |
| `tidb_stmt_summary_max_sql_length` | No limitation | Read-only [^11] |
| `tidb_stmt_summary_max_stmt_count` | No limitation | Read-only [^11] |
| `tidb_stmt_summary_refresh_interval` | No limitation | Read-only [^11] |
| `tidb_sysproc_scan_concurrency` | No limitation | Read-only [^11] |
| `tidb_top_sql_max_meta_count` | Not supported [^4] | Not supported [^4] |
| `tidb_top_sql_max_time_series_count` | Not supported [^4] | Not supported [^4] |
| `tidb_tso_client_batch_max_wait_time` | No limitation | Read-only [^11] |
| `tidb_ttl_delete_batch_size` | No limitation | Read-only [^9] |
| `tidb_ttl_delete_rate_limit` | No limitation | Read-only [^9] |
| `tidb_ttl_delete_worker_count` | No limitation | Read-only [^9] |
| `tidb_ttl_job_enable` | No limitation | Read-only [^9] |
| `tidb_ttl_job_schedule_window_end_time` | No limitation | Read-only [^9] |
| `tidb_ttl_job_schedule_window_start_time` | No limitation | Read-only [^9] |
| `tidb_ttl_running_tasks` | No limitation | Read-only [^9] |
| `tidb_ttl_scan_batch_size` | No limitation | Read-only [^9] |
| `tidb_ttl_scan_worker_count` | No limitation | Read-only [^9] |
| `tidb_txn_mode` | No limitation | Read-only [^11] |
| `tidb_wait_split_region_finish` | No limitation | Read-only [^11] |
| `tidb_wait_split_region_timeout` | No limitation | Read-only [^11] |
| `txn_scope` | No limitation | Read-only [^11] |
| `validate_password.enable` | No limitation | Always enabled [^10] |
| `validate_password.length` | No limitation | At least `8` [^10] |
| `validate_password.mixed_case_count` | No limitation | At least `1` [^10] |
| `validate_password.number_count` | No limitation | At least `1` [^10] |
| `validate_password.policy` | No limitation | Can only be `MEDIUM` or `STRONG` [^10] |
| `validate_password.special_char_count` | No limitation | At least `1` [^10] |
| `wait_timeout` | No limitation | Read-only [^11] |

[^1]: Configuring data placement is not supported on TiDB Serverless.

[^2]: Configuring resource groups is not supported on TiDB Serverless.

[^3]: To perform [Back up and Restore](/tidb-cloud/backup-and-restore-serverless.md) operations on TiDB Serverless, you can use the TiDB Cloud console instead. 

[^4]: The feature is unavailable in [Security Enhanced Mode (SEM)](/system-variables.md#tidb_enable_enhanced_security).

[^5]: To track [Slow Query](/tidb-cloud/tune-performance.md#slow-query) on TiDB Serverless, you can use the TiDB Cloud console instead.

[^6]: To perform [Statement Analysis](/tidb-cloud/tune-performance.md#statement-analysis) on TiDB Serverless, you can use the TiDB Cloud console instead.

[^7]: Drainer and Pump are not supported on TiDB Cloud.

[^8]: Plugin is not supported on TiDB Serverless.

[^9]: [Time to live (TTL)](/time-to-live.md) is currently unavailable on TiDB Serverless.

[^10]: TiDB Serverless enforces strong password policy.

[^11]: The variable is read-only on TiDB Serverless.

[^12]: Customizing cache size using [`AUTO_ID_CACHE`](/auto-increment.md#cache-size-control) is temporarily unavailable on TiDB Serverless.

[^13]: Not supported. Enabling `require_secure_transport` for TiDB Dedicated clusters will result in SQL client connection failures.
