---
title: mysql Schema
summary: 了解 TiDB 系统表。
---

# `mysql` Schema

`mysql` 库里存储的是 TiDB 系统表。该设计类似于 MySQL 中的 `mysql` 库，其中 `mysql.user` 之类的表可以直接编辑。该库还包含许多 MySQL 的扩展表。

## 权限系统表

这些系统表里面包含了用户账户以及相应的授权信息：

* `user` 用户账户，全局权限，以及其它一些非权限的列
* `db` 数据库级别的权限
* `tables_priv` 表级的权限
* `columns_priv` 列级的权限
* `password_history` 记录密码更改历史
* `default_roles` 默认启用的角色
* `global_grants` 动态权限
* `global_priv` 基于证书的认证信息
* `role_edges` 角色之间的关系信息

## 集群状态系统表

* `tidb` 用于记录 TiDB 的一些全局信息

    * `bootstrapped` 用于记录 TiDB 集群是否已完成初始化，注意该值为只读，不可修改。
    * `tidb_server_version` 用于记录 TiDB 在初始化时的版本信息，注意该值为只读，不可修改。
    * `system_tz` 用于记录 TiDB 的系统时区
    * `new_collation_enabled` 用于记录 TiDB 是否开启了[新排序规则框架](/character-set-and-collation.md#新框架下的排序规则支持)，注意该值为只读，不可修改。

## 服务端帮助信息系统表

* `help_topic` 目前为空

## 统计信息相关系统表

* `stats_buckets` 统计信息的桶
* `stats_histograms` 统计信息的直方图
* `stats_top_n` 统计信息的 TopN
* `stats_meta` 表的元信息，比如总行数和修改数
* `stats_extended` 扩展统计信息，比如列之间的顺序相关性
* `stats_feedback` 统计信息的查询反馈
* `stats_fm_sketch` 统计信息列的直方图 FMSketch 分布
* `analyze_options` 各个表默认的 `analyze` 参数
* `column_stats_usage` 列统计信息的使用情况
* `analyze_jobs` 正在执行的统计信息收集任务以及过去 7 天内的历史任务记录

## 执行计划相关系统表

* `bind_info` 执行计划的绑定信息
* `capture_plan_baselines_blacklist` 关于自动绑定执行计划对象的黑名单

## GC Worker 相关系统表

* `gc_delete_range` 需要被 GC worker 定期删除的 KV 范围段
* `gc_delete_range_done` 已经被删除的 KV 范围段

## 缓存表使用的系统表

* `table_cache_meta` 存储了缓存表的元信息

## TTL 相关系统表

* `tidb_ttl_table_status` 所有 TTL 表的上一次执行与正在执行的 TTL 任务
* `tidb_ttl_task` 正在执行的 TTL 子任务
* `tidb_ttl_job_history` 过去 90 天内 TTL 任务的执行历史

## Runaway Queries 相关系统表

* `tidb_runaway_queries` 过去 7 天内所有识别到的 Runaway Queries 的历史记录
* `tidb_runaway_watch` Runaway Queries 的监控列表 (Watch List)
* `tidb_runaway_watch_done` 被删除或者过期的 Runaway Queries 的监控列表

## 元数据锁相关系统表

* `tidb_mdl_view` 元数据锁的视图，可以用于查看当前阻塞的 DDL 的相关信息
* `tidb_mdl_info` TiDB 内部用于同步各节点的元数据锁的相关信息

## DDL 相关系统表

* `tidb_ddl_history` 记录了 DDL 语句的历史记录
* `tidb_ddl_job` TiDB 内部存放的正在执行的 DDL 的元数据，用于执行 DDL
* `tidb_ddl_reorg` TiDB 内部存放的正在执行的物理 DDL（例如加索引）的元数据，用于执行物理 DDL

## 分布式执行框架相关系统表

* `dist_framework_meta` 存放分布式执行框架任务调度的元信息
* `tidb_global_task` 存放当前分布式框架正在执行的任务元信息
* `tidb_global_task_history` 存放分布式执行框架完成（成功或者失败）的任务元信息
* `tidb_background_subtask` 存放当前正在执行的分布式执行框架任务的子任务元信息
* `tidb_background_subtask_history` 存放历史的分布式执行框架任务的子任务元信息

## 资源管控相关系统表

* `request_unit_by_group` 存放资源组 RU 消耗统计的历史记录

## 其它系统表

* `GLOBAL_VARIABLES` 全局系统变量表
* `expr_pushdown_blacklist` 表达式下推的黑名单
* `opt_rule_blacklist` 逻辑优化规则的黑名单
* `tidb_import_jobs` 记录 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 任务信息
* `tidb_timers` 存储了内部定时器的相关元信息
