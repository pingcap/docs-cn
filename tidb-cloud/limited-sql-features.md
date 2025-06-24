---
title: TiDB Cloud 上的受限 SQL 功能
summary: 了解 TiDB Cloud 上的受限 SQL 功能。
---

# TiDB Cloud 上的受限 SQL 功能

TiDB Cloud 可以支持几乎所有 TiDB 支持的工作负载，但在 TiDB 自托管版本和 TiDB Cloud Dedicated/Serverless 版本之间存在一些功能差异。本文描述了 TiDB Cloud 上的 SQL 功能限制。我们正在不断填补 TiDB 自托管版本和 TiDB Cloud Dedicated/Serverless 版本之间的功能差距。如果你需要这些差距中的功能或能力，请[联系我们](/tidb-cloud/tidb-cloud-support.md)提出功能请求。

## 语句

### 放置和范围管理

| 语句 | TiDB Cloud Dedicated | TiDB Cloud Serverless |
|:-|:-|:-|
| `ALTER PLACEMENT POLICY` | 支持 | 不支持 [^1] |
| `CREATE PLACEMENT POLICY` | 支持 | 不支持 [^1] |
| `DROP PLACEMENT POLICY` | 支持 | 不支持 [^1] |
| `SHOW CREATE PLACEMENT POLICY` | 支持 | 不支持 [^1] |
| `SHOW PLACEMENT` | 支持 | 不支持 [^1] |
| `SHOW PLACEMENT FOR` | 支持 | 不支持 [^1] |
| `SHOW PLACEMENT LABELS` | 支持 | 不支持 [^1] |
| `SHOW TABLE REGIONS` | 支持 | 不支持 [^1] |
| `SPLIT REGION` | 支持 | 不支持 [^1] |

### 资源组

| 语句 | TiDB Cloud Dedicated | TiDB Cloud Serverless |
|:-|:-|:-|
| `ALTER RESOURCE GROUP` | 支持 | 不支持 [^2] |
| `CALIBRATE RESOURCE` | 不支持 | 不支持 [^2] |
| `CREATE RESOURCE GROUP` | 支持 | 不支持 [^2] |
| `DROP RESOURCE GROUP` | 支持 | 不支持 [^2] |
| `SET RESOURCE GROUP` | 支持 | 不支持 [^2] |
| `SHOW CREATE RESOURCE GROUP` | 支持 | 不支持 [^2] |

### 其他

| 语句 | TiDB Cloud Dedicated | TiDB Cloud Serverless |
|:-|:-|:-|
| `BACKUP` | 支持 | 不支持 [^3] |
| `SHOW BACKUPS` | 支持 | 不支持 [^3] |
| `RESTORE` | 支持 | 不支持 [^3] |
| `SHOW RESTORES` | 支持 | 不支持 [^3] |
| `ADMIN RESET TELEMETRY_ID` | 支持 | TiDB Cloud Serverless 不支持遥测。 |
| `ADMIN SHOW TELEMETRY` | 不支持 [^4] | 不支持 [^4] |
| `ADMIN SHOW SLOW` | 支持 | 不支持 [^5] |
| `ADMIN PLUGINS ENABLE` | 支持 | 不支持 [^8] |
| `ADMIN PLUGINS DISABLE` | 支持 | 不支持 [^8] |
| `ALTER INSTANCE RELOAD TLS` | 支持 | TiDB Cloud Serverless 自动刷新 TLS 证书。 |
| `LOAD DATA INFILE` | 支持 `LOAD DATA LOCAL INFILE` 和从 Amazon S3 或 Google Cloud Storage 导入的 `LOAD DATA INFILE` | 仅支持 `LOAD DATA LOCAL INFILE` |
| `CHANGE DRAINER` | 不支持 [^7] | 不支持 [^7] |
| `CHANGE PUMP` | 不支持 [^7] | 不支持 [^7] |
| `FLASHBACK CLUSTER` | 支持 | 不支持 [^3] |
| `LOAD STATS` | 支持 | 不支持 |
| `SELECT ... INTO OUTFILE` | 不支持 [^4] | 不支持 [^4] |
| `SET CONFIG` | 不支持 [^4] | 不支持 [^4] |
| `SHOW CONFIG` | 不支持 [^4] | 不支持 [^4] |
| `SHOW DRAINER STATUS` | 不支持 [^7] | 不支持 [^7] |
| `SHOW PLUGINS` | 支持 | 不支持 [^8] |
| `SHOW PUMP STATUS` | 不支持 [^7] | 不支持 [^7] |
| `SHUTDOWN` | 不支持 [^4] | 不支持 [^4] |
| `PLAN REPLAYER` | 支持 | 以不同方式支持[^11] |

## 函数和运算符

| 函数和运算符 | TiDB Cloud Dedicated | TiDB Cloud Serverless |
|:-|:-|:-|
| `SLEEP` | 无限制 | [`SLEEP()` 函数](https://docs.pingcap.com/tidbcloud/miscellaneous-functions)有限制，最大睡眠时间为 300 秒。|

## 系统表

| 数据库 | 表 | TiDB Cloud Dedicated | TiDB Cloud Serverless |
|:-|:-|:-|:-|
| `information_schema` | `ATTRIBUTES` | 支持 | 不支持 [^1] |
| `information_schema` | `CLUSTER_CONFIG` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `CLUSTER_HARDWARE` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `CLUSTER_INFO` | 支持 | 不支持 [^1] |
| `information_schema` | `CLUSTER_LOAD` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `CLUSTER_LOG` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `CLUSTER_SLOW_QUERY` | 支持 | 不支持 [^5] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY` | 支持 | 不支持 [^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_EVICTED` | 支持 | 不支持 [^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_HISTORY` | 支持 | 不支持 [^6] |
| `information_schema` | `CLUSTER_SYSTEMINFO` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `INSPECTION_RESULT` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `INSPECTION_RULES` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `INSPECTION_SUMMARY` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `METRICS_SUMMARY` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `METRICS_SUMMARY_BY_LABEL` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `METRICS_TABLES` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `PLACEMENT_POLICIES` | 支持 | 不支持 [^1] |
| `information_schema` | `RESOURCE_GROUPS` | 支持 | 不支持 [^2] |
| `information_schema` | `SLOW_QUERY` | 支持 | 不支持 [^5] |
| `information_schema` | `STATEMENTS_SUMMARY` | 支持 | 不支持 [^6] |
| `information_schema` | `STATEMENTS_SUMMARY_EVICTED` | 支持 | 不支持 [^6] |
| `information_schema` | `STATEMENTS_SUMMARY_HISTORY` | 支持 | 不支持 [^6] |
| `information_schema` | `TIDB_HOT_REGIONS` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `TIDB_HOT_REGIONS_HISTORY` | 支持 | 不支持 [^1] |
| `information_schema` | `TIDB_SERVERS_INFO` | 支持 | 不支持 [^1] |
| `information_schema` | `TIKV_REGION_PEERS` | 支持 | 不支持 [^1] |
| `information_schema` | `TIKV_REGION_STATUS` | 支持 | 不支持 [^1] |
| `information_schema` | `TIKV_STORE_STATUS` | 支持 | 不支持 [^1] |
| `performance_schema` | `pd_profile_allocs` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `pd_profile_block` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `pd_profile_cpu` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `pd_profile_goroutines` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `pd_profile_memory` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `pd_profile_mutex` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_allocs` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_block` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_cpu` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_goroutines` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_memory` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_mutex` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tikv_profile_cpu` | 不支持 [^4] | 不支持 [^4] |
| `mysql` | `expr_pushdown_blacklist` | 不支持 [^4] | 不支持 [^4] |
| `mysql` | `gc_delete_range` | 不支持 [^4] | 不支持 [^4] |
| `mysql` | `gc_delete_range_done` | 不支持 [^4] | 不支持 [^4] |
| `mysql` | `opt_rule_blacklist` | 不支持 [^4] | 不支持 [^4] |
| `mysql` | `tidb` | 不支持 [^4] | 不支持 [^4] |

## 系统变量

| 变量 | TiDB Cloud Dedicated | TiDB Cloud Serverless |
|:-|:-|:-|
| `datadir` | 无限制 | 不支持 [^1] |
| `interactive_timeout` | 无限制 | 只读 [^10] |
| `max_allowed_packet` | 无限制 | 只读 [^10] |
| `plugin_dir` | 无限制 | 不支持 [^8] |
| `plugin_load` | 无限制 | 不支持 [^8] |
| `require_secure_transport` | 不支持 [^12] | 只读 [^10] |
| `skip_name_resolve` | 无限制 | 只读 [^10] |
| `sql_log_bin` | 无限制 | 只读 [^10] |
| `tidb_cdc_write_source` | 无限制 | 只读 [^10] |
| `tidb_check_mb4_value_in_utf8` | 不支持 [^4] | 不支持 [^4] |
| `tidb_config` | 不支持 [^4] | 不支持 [^4] |
| `tidb_ddl_disk_quota` | 无限制 | 只读 [^10] |
| `tidb_ddl_enable_fast_reorg` | 无限制 | 只读 [^10] |
| `tidb_ddl_error_count_limit` | 无限制 | 只读 [^10] |
| `tidb_ddl_flashback_concurrency` | 无限制 | 只读 [^10] |
| `tidb_ddl_reorg_batch_size` | 无限制 | 只读 [^10] |
| `tidb_ddl_reorg_priority` | 无限制 | 只读 [^10] |
| `tidb_ddl_reorg_worker_cnt` | 无限制 | 只读 [^10] |
| `tidb_enable_1pc` | 无限制 | 只读 [^10] |
| `tidb_enable_async_commit` | 无限制 | 只读 [^10] |
| `tidb_enable_auto_analyze` | 无限制 | 只读 [^10] |
| `tidb_enable_collect_execution_info` | 不支持 [^4] | 不支持 [^4] |
| `tidb_enable_ddl` | 无限制 | 只读 [^10] |
| `tidb_enable_gc_aware_memory_track` | 无限制 | 只读 [^10] |
| `tidb_enable_gogc_tuner` | 无限制 | 只读 [^10] |
| `tidb_enable_local_txn` | 无限制 | 只读 [^10] |
| `tidb_enable_resource_control` | 无限制 | 只读 [^10] |
| `tidb_enable_slow_log` | 不支持 [^4] | 不支持 [^4] |
| `tidb_enable_stmt_summary` | 无限制 | 只读 [^10] |
| `tidb_enable_telemetry` | 不支持 [^4] | 不支持 [^4] |
| `tidb_enable_top_sql` | 无限制 | 只读 [^10] |
| `tidb_enable_tso_follower_proxy` | 无限制 | 只读 [^10] |
| `tidb_expensive_query_time_threshold` | 不支持 [^4] | 不支持 [^4] |
| `tidb_force_priority` | 不支持 [^4] | 不支持 [^4] |
| `tidb_gc_concurrency` | 无限制 | 只读 [^10] |
| `tidb_gc_enable` | 无限制 | 只读 [^10] |
| `tidb_gc_max_wait_time` | 无限制 | 只读 [^10] |
| `tidb_gc_run_interval` | 无限制 | 只读 [^10] |
| `tidb_gc_scan_lock_mode` | 无限制 | 只读 [^10] |
| `tidb_general_log` | 不支持 [^4] | 不支持 [^4] |
| `tidb_generate_binary_plan` | 无限制 | 只读 [^10] |
| `tidb_gogc_tuner_threshold` | 无限制 | 只读 [^10] |
| `tidb_guarantee_linearizability` | 无限制 | 只读 [^10] |
| `tidb_isolation_read_engines` | 无限制 | 只读 [^10] |
| `tidb_log_file_max_days` | 无限制 | 只读 [^10] |
| `tidb_memory_usage_alarm_ratio` | 不支持 [^4] | 不支持 [^4] |
| `tidb_metric_query_range_duration` | 不支持 [^4] | 不支持 [^4] |
| `tidb_metric_query_step` | 不支持 [^4] | 不支持 [^4] |
| `tidb_opt_write_row_id` | 不支持 [^4] | 不支持 [^4] |
| `tidb_placement_mode` | 无限制 | 只读 [^10] |
| `tidb_pprof_sql_cpu` | 不支持 [^4] | 不支持 [^4] |
| `tidb_record_plan_in_slow_log` | 不支持 [^4] | 不支持 [^4] |
| `tidb_redact_log` | 不支持 [^4] | 不支持 [^4] |
| `tidb_restricted_read_only` | 不支持 [^4] | 不支持 [^4] |
| `tidb_row_format_version` | 不支持 [^4] | 不支持 [^4] |
| `tidb_scatter_region` | 无限制 | 只读 [^10] |
| `tidb_server_memory_limit` | 无限制 | 只读 [^10] |
| `tidb_server_memory_limit_gc_trigger` | 无限制 | 只读 [^10] |
| `tidb_server_memory_limit_sess_min_size` | 无限制 | 只读 [^10] |
| `tidb_simplified_metrics` | 无限制 | 只读 [^10] |
| `tidb_slow_query_file` | 不支持 [^4] | 不支持 [^4] |
| `tidb_slow_log_threshold` | 不支持 [^4] | 不支持 [^4] |
| `tidb_slow_txn_log_threshold` | 不支持 [^4] | 不支持 [^4] |
| `tidb_stats_load_sync_wait` | 无限制 | 只读 [^10] |
| `tidb_stmt_summary_history_size` | 无限制 | 只读 [^10] |
| `tidb_stmt_summary_internal_query` | 无限制 | 只读 [^10] |
| `tidb_stmt_summary_max_sql_length` | 无限制 | 只读 [^10] |
| `tidb_stmt_summary_max_stmt_count` | 无限制 | 只读 [^10] |
| `tidb_stmt_summary_refresh_interval` | 无限制 | 只读 [^10] |
| `tidb_sysproc_scan_concurrency` | 无限制 | 只读 [^10] |
| `tidb_top_sql_max_meta_count` | 不支持 [^4] | 不支持 [^4] |
| `tidb_top_sql_max_time_series_count` | 不支持 [^4] | 不支持 [^4] |
| `tidb_tso_client_batch_max_wait_time` | 无限制 | 只读 [^10] |
| `tidb_ttl_delete_batch_size` | 无限制 | 只读 [^10] |
| `tidb_ttl_delete_rate_limit` | 无限制 | 只读 [^10] |
| `tidb_ttl_delete_worker_count` | 无限制 | 只读 [^10] |
| `tidb_ttl_job_schedule_window_end_time` | 无限制 | 只读 [^10] |
| `tidb_ttl_job_schedule_window_start_time` | 无限制 | 只读 [^10] |
| `tidb_ttl_running_tasks` | 无限制 | 只读 [^10] |
| `tidb_ttl_scan_batch_size` | 无限制 | 只读 [^10] |
| `tidb_ttl_scan_worker_count` | 无限制 | 只读 [^10] |
| `tidb_txn_mode` | 无限制 | 只读 [^10] |
| `tidb_wait_split_region_finish` | 无限制 | 只读 [^10] |
| `tidb_wait_split_region_timeout` | 无限制 | 只读 [^10] |
| `txn_scope` | 无限制 | 只读 [^10] |
| `validate_password.enable` | 无限制 | 始终启用 [^9] |
| `validate_password.length` | 无限制 | 至少 `8` [^9] |
| `validate_password.mixed_case_count` | 无限制 | 至少 `1` [^9] |
| `validate_password.number_count` | 无限制 | 至少 `1` [^9] |
| `validate_password.policy` | 无限制 | 只能是 `MEDIUM` 或 `STRONG` [^9] |
| `validate_password.special_char_count` | 无限制 | 至少 `1` [^9] |
| `wait_timeout` | 无限制 | 只读 [^10] |

[^1]: TiDB Cloud Serverless 不支持配置数据放置。

[^2]: TiDB Cloud Serverless 不支持配置资源组。

[^3]: 要在 TiDB Cloud Serverless 上执行[备份和恢复](/tidb-cloud/backup-and-restore-serverless.md)操作，你可以使用 TiDB Cloud 控制台。

[^4]: 该功能在[安全增强模式（SEM）](/system-variables.md#tidb_enable_enhanced_security)下不可用。

[^5]: 要在 TiDB Cloud Serverless 上跟踪[慢查询](/tidb-cloud/tune-performance.md#slow-query)，你可以使用 TiDB Cloud 控制台。

[^6]: 要在 TiDB Cloud Serverless 上执行[语句分析](/tidb-cloud/tune-performance.md#statement-analysis)，你可以使用 TiDB Cloud 控制台。

[^7]: TiDB Cloud 不支持 Drainer 和 Pump。

[^8]: TiDB Cloud Serverless 不支持插件。

[^9]: TiDB Cloud Serverless 强制执行强密码策略。

[^10]: 该变量在 TiDB Cloud Serverless 上为只读。

[^11]: TiDB Cloud Serverless 不支持像[示例](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#examples-of-exporting-cluster-information)中那样通过 `${tidb-server-status-port}` 下载由 `PLAN REPLAYER` 导出的文件。相反，TiDB Cloud Serverless 会生成一个[预签名 URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)供你下载文件。请注意，此 URL 在生成后 10 小时内有效。

[^12]: 不支持。为 TiDB Cloud Dedicated 集群启用 `require_secure_transport` 将导致 SQL 客户端连接失败。
