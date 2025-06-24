---
title: mysql 系统库
summary: 了解 TiDB 系统表。
---

# `mysql` 系统库

`mysql` 系统库包含 TiDB 的系统表。其设计类似于 MySQL 中的 `mysql` 系统库，可以直接编辑如 `mysql.user` 等表。它还包含了一些 MySQL 的扩展表。

> **注意：**
>
> 在大多数情况下，不建议使用 `INSERT`、`UPDATE` 或 `DELETE` 直接修改系统表的内容。相反，应使用 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)、[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)、[`DROP USER`](/sql-statements/sql-statement-drop-user.md)、[`GRANT`](/sql-statements/sql-statement-grant-privileges.md)、[`REVOKE`](/sql-statements/sql-statement-revoke-privileges.md) 和 [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md) 等语句来管理用户和权限。如果必须直接修改系统表，请使用 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md) 使更改生效。

## 授权系统表

这些系统表包含用户账户及其权限的授权信息：

- [`user`](/mysql-schema/mysql-schema-user.md)：用户账户、全局权限和其他非权限列
- `db`：数据库级别权限
- `tables_priv`：表级别权限
- `columns_priv`：列级别权限
- `password_history`：密码修改历史
- `default_roles`：用户的默认角色
- `global_grants`：动态权限
- `global_priv`：基于证书的认证信息
- `role_edges`：角色之间的关系

## 集群状态系统表

* `tidb` 表包含一些 TiDB 的全局信息：

    * `bootstrapped`：TiDB 集群是否已初始化。注意该值为只读，不可修改。
    * `tidb_server_version`：TiDB 初始化时的版本信息。注意该值为只读，不可修改。
    * `system_tz`：TiDB 的系统时区。
    * `new_collation_enabled`：TiDB 是否启用了[新的排序规则框架](/character-set-and-collation.md#new-framework-for-collations)。注意该值为只读，不可修改。

## 服务器端帮助系统表

目前，`help_topic` 为空。

## 统计信息系统表

- `stats_buckets`：统计信息的桶
- `stats_histograms`：统计信息的直方图
- `stats_top_n`：统计信息的 TopN
- `stats_meta`：表的元信息，如总行数和更新行数
- `stats_extended`：扩展统计信息，如列之间的顺序相关性
- `stats_feedback`：统计信息的查询反馈
- `stats_fm_sketch`：统计信息列直方图的 FMSketch 分布
- `stats_table_locked`：锁定统计信息的相关信息
- `stats_meta_history`：历史统计信息中的元信息
- `stats_history`：历史统计信息中的其他信息
- `analyze_options`：每个表的默认 `analyze` 选项
- `column_stats_usage`：列统计信息的使用情况
- `analyze_jobs`：正在进行的统计信息收集任务和最近 7 天的历史任务记录

## 执行计划相关系统表

- `bind_info`：执行计划的绑定信息
- `capture_plan_baselines_blacklist`：执行计划自动绑定的黑名单

## PLAN REPLAYER 相关系统表

- `plan_replayer_status`：用户注册的 [`PLAN REPLAYER CAPTURE`](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#use-plan-replayer-capture) 任务
- `plan_replayer_task`：[`PLAN REPLAYER CAPTURE`](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#use-plan-replayer-capture) 任务的结果

## GC worker 系统表

> **注意：**
>
> GC worker 系统表仅适用于 TiDB 自托管版本，在 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/) 上不可用。

- `gc_delete_range`：待删除的 KV 范围
- `gc_delete_range_done`：已删除的 KV 范围

## 缓存表相关系统表

- `table_cache_meta` 存储缓存表的元数据。

## TTL 相关系统表

* `tidb_ttl_table_status`：所有 TTL 表的已执行 TTL 任务和正在进行的 TTL 任务
* `tidb_ttl_task`：当前正在进行的 TTL 子任务
* `tidb_ttl_job_history`：最近 90 天的 TTL 任务执行历史

## 失控查询相关系统表

* `tidb_runaway_queries`：过去 7 天内所有已识别的失控查询的历史记录
* `tidb_runaway_watch`：失控查询的监视列表
* `tidb_runaway_watch_done`：已删除或过期的失控查询监视列表

## 元数据锁相关系统表

* `tidb_mdl_view`：元数据锁的视图。可用于查看当前被阻塞的 DDL 语句信息
* `tidb_mdl_info`：TiDB 内部用于跨节点同步元数据锁

## DDL 语句相关系统表

* `tidb_ddl_history`：DDL 语句的历史记录
* `tidb_ddl_job`：TiDB 当前正在执行的 DDL 语句的元数据
* `tidb_ddl_reorg`：TiDB 当前正在执行的物理 DDL 语句（如添加索引）的元数据

## TiDB 分布式执行框架 (DXF) 相关系统表

* `dist_framework_meta`：分布式执行框架 (DXF) 任务调度器的元数据
* `tidb_global_task`：当前 DXF 任务的元数据
* `tidb_global_task_history`：历史 DXF 任务的元数据，包括成功和失败的任务
* `tidb_background_subtask`：当前 DXF 子任务的元数据
* `tidb_background_subtask_history`：历史 DXF 子任务的元数据

## 资源控制相关系统表

* `request_unit_by_group`：所有资源组消耗的资源单位 (RUs) 的历史记录

## 其他系统表

<CustomContent platform="tidb">

> **注意：**
>
> `tidb`、`expr_pushdown_blacklist`、`opt_rule_blacklist`、`table_cache_meta`、`tidb_import_jobs` 和 `tidb_timers` 系统表仅适用于 TiDB 自托管版本，在 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/) 上不可用。

- `GLOBAL_VARIABLES`：全局系统变量表
- `expr_pushdown_blacklist`：表达式下推的黑名单
- `opt_rule_blacklist`：逻辑优化规则的黑名单
- `tidb_import_jobs`：[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 的作业信息
- `tidb_timers`：内部定时器的元数据
- `advisory_locks`：与[锁定函数](/functions-and-operators/locking-functions.md)相关的信息

</CustomContent>

<CustomContent platform="tidb-cloud">

- `GLOBAL_VARIABLES`：全局系统变量表

</CustomContent>
