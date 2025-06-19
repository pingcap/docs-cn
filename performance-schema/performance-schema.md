---
title: Performance Schema
summary: TiDB 实现了用于查看系统元数据的 performance_schema。
---

# Performance Schema

TiDB 实现了 performance schema 表以保持与 MySQL 的兼容性。

## MySQL 兼容性表

| 表名                                                                                       | 描述                                               |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| `events_stages_current`                                                                          |                                                           |
| `events_stages_history`                                                                          |                                                           |
| `events_stages_history_long`                                                                     |                                                           |
| `events_statements_current`                                                                      |                                                           |
| `events_statements_history`                                                                      |                                                           |
| `events_statements_history_long`                                                                 |                                                           |
| `events_statements_summary_by_digest`                                                            |                                                           |
| `events_transactions_current`                                                                    |                                                           |
| `events_transactions_history`                                                                    |                                                           |
| `events_transactions_history_long`                                                               |                                                           |
| `global_status`                                                                                  |                                                           |
| `prepared_statements_instances`                                                                  |                                                           |
| [`session_connect_attrs`](/performance-schema/performance-schema-session-connect-attrs.md)       | 提供会话的连接属性。              |
| `session_status`                                                                                 |                                                           |
| `session_variables`                                                                              |                                                           |
| `setup_actors`                                                                                   |                                                           |
| `setup_consumers`                                                                                |                                                           |
| `setup_instruments`                                                                              |                                                           |
| `setup_objects`                                                                                  |                                                           |

## TiDB 扩展表

| 表名                                                                                       | 描述                                               |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| `pd_profile_allocs`                                                                              |                                                           |
| `pd_profile_block`                                                                               |                                                           |
| `pd_profile_cpu`                                                                                 |                                                           |
| `pd_profile_goroutines`                                                                          |                                                           |
| `pd_profile_memory`                                                                              |                                                           |
| `pd_profile_mutex`                                                                               |                                                           |
| `tidb_profile_allocs`                                                                            |                                                           |
| `tidb_profile_block`                                                                             |                                                           |
| `tidb_profile_cpu`                                                                               |                                                           |
| `tidb_profile_goroutines`                                                                        |                                                           |
| `tidb_profile_memory`                                                                            |                                                           |
| `tidb_profile_mutex`                                                                             |                                                           |
| `tikv_profile_cpu`                                                                               |                                                           |
