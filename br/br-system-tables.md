---
title: 快照恢复时无法恢复的系统表
summary: 列出快照恢复时无法恢复的系统表
---

# 快照恢复时无法恢复的系统表

在使用快照备份来备份集群时，BR 会将系统表备份为库名带 `__TiDB_BR_Temporary_` 前缀的表，例如表 `mysql.user` 将会被备份为 `__TiDB_BR_Temporary_mysql.user`. 因此在进行快照恢复时会首先恢复一系列库名带 `__TiDB_BR_Temporary_` 前缀的系统表，避免与恢复集群现有的系统表中的数据冲突。当 BR 开始恢复系统表时，会通过 `REPLACE INTO` 的 SQL 将数据从库名带 `__TiDB_BR_Temporary_` 前缀的表写入到对应的系统表中。

下面列出了快照恢复无法通过上述方式进行恢复的系统表。

* `mysql`
    * `advisory_locks` 
    * `analyze_jobs`
    * `analyze_options`
    * `capture_plan_baselines_blacklist`
    * `column_stats_usage`
    * `dist_framework_meta`
    * `gc_delete_range`
    * `gc_delete_range_done`
    * `global_variables`
    * `help_topic`
    * `index_advisor_results`
    * `plan_replayer_status`
    * `plan_replayer_task`
    * `request_unit_by_group`
    * `stats_buckets`
    * `stats_extended`
	* `stats_feedback`
	* `stats_fm_sketch`
	* `stats_histograms`
	* `stats_history`
	* `stats_meta`
	* `stats_meta_history`
	* `stats_table_locked`
	* `stats_top_n`
    * `table_cache_meta`
    * `tidb`
    * `tidb_background_subtask`
    * `tidb_background_subtask_history`
    * `tidb_ddl_history`
    * `tidb_ddl_job`
    * `tidb_ddl_notifier`
    * `tidb_ddl_reorg`
    * `tidb_global_task`
    * `tidb_global_task_history`
    * `tidb_import_jobs`
    * `tidb_mdl_info`
    * `tidb_mdl_view`
    * `tidb_pitr_id_map`
    * `tidb_runaway_queries`
    * `tidb_runaway_watch`
    * `tidb_runaway_watch_done`
    * `tidb_timers`
    * `tidb_ttl_job_history`
    * `tidb_ttl_table_status`
    * `tidb_ttl_task`

* `sys`
    * `schema_unused_indexes`
