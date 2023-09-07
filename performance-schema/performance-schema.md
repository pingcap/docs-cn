---
title: Performance Schema
summary: TiDB implements the performance_schema for viewing system metadata.
---

# Performance Schema

TiDB implements performance schema tables for MySQL compatibility.

## Tables for MySQL compatibility

| Table Name                                                                                       | Description                                               |
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
| [`session_connect_attrs`](/performance-schema/performance-schema-session-connect-attrs.md)       | Provides connection attributes for sessions.              |
| `session_status`                                                                                 |                                                           |
| `session_variables`                                                                              |                                                           |
| `setup_actors`                                                                                   |                                                           |
| `setup_consumers`                                                                                |                                                           |
| `setup_instruments`                                                                              |                                                           |
| `setup_objects`                                                                                  |                                                           |

## Tables that are TiDB extensions

| Table Name                                                                                       | Description                                               |
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
