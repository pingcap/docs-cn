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
* `schema_index_usage` 索引的使用情况
* `analyze_jobs` 正在执行的统计信息收集任务以及过去 7 天内的历史任务记录
* `load_data_jobs` 正在执行或历史执行的 `LOAD DATA` 任务

## 执行计划相关系统表

* `bind_info` 执行计划的绑定信息
* `capture_plan_baselines_blacklist` 关于自动绑定执行计划对象的黑名单

## GC Worker 相关系统表

* `gc_delete_range` 需要被 GC worker 定期删除的 KV 范围段
* `gc_delete_range_done` 已经被删除的 KV 范围段

## 缓存表使用的系统表

* `table_cache_meta` 存储了缓存表的元信息

## TTL 相关系统表

* `mysql.tidb_ttl_table_status` 所有 TTL 表的上一次执行与正在执行的 TTL 任务
* `mysql.tidb_ttl_task` 正在执行的 TTL 子任务
* `mysql.tidb_ttl_job_history` 过去 90 天内 TTL 任务的执行历史

## 其它系统表

* `GLOBAL_VARIABLES` 全局系统变量表
* `tidb` 用于 TiDB 在 bootstrap 的时候记录相关版本信息
* `expr_pushdown_blacklist` 表达式下推的黑名单
* `opt_rule_blacklist` 逻辑优化规则的黑名单
* `table_cache_meta` 缓存表的信息
