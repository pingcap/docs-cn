---
title: Performance Schema
summary: 了解 TiDB `performance_schema` 系统数据库。
---

# Performance Schema

TiDB 实现了兼容 MySQL 的 performance schema 表。

## 与 MySQL 兼容的表

| 表名| 描述 |
| --- | --- |
| `events_stages_current` |  |
| `events_stages_history`|  |
| `events_stages_history_long` |  |
| `events_statements_current` |  |
| `events_statements_history` |  |
| `events_statements_history_long` |  |
| `events_statements_summary_by_digest` |  |
| `events_transactions_current` |  |
| `events_transactions_history` |  |
| `events_transactions_history_long` |  |
| `global_status` |  |
| `prepared_statements_instances` |  |
| [`session_connect_attrs`](/performance-schema/performance-schema-session-connect-attrs.md) | 为会话提供连接属性。 |
| `session_status` |  |
| `session_variables` |  |
| `setup_actors`  |  |
| `setup_consumers`  |  |
| `setup_instruments`|  |
| `setup_objects` |  |

## TiDB 中的扩展表

| 表名 | 描述 |
| ------------------------- | ----------- |
| `pd_profile_allocs` | |
| `pd_profile_block`  | |
| `pd_profile_cpu` | |
| `pd_profile_goroutines`| |
| `pd_profile_memory` | |
| `pd_profile_mutex`  | |
| `tidb_profile_allocs`  | |
| `tidb_profile_block`| |
| `tidb_profile_cpu`  | |
| `tidb_profile_goroutines` | |
| `tidb_profile_memory`  | |
| `tidb_profile_mutex`| |
| `tikv_profile_cpu`  | |
