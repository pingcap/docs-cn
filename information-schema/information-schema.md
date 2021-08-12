---
title: Information Schema
summary: TiDB implements the ANSI-standard information_schema for viewing system metadata.
aliases: ['/docs/dev/system-tables/system-table-information-schema/','/docs/dev/reference/system-databases/information-schema/','/tidb/dev/system-table-information-schema/']
---

# Information Schema

Information Schema provides an ANSI-standard way of viewing system metadata. TiDB also provides a number of custom `INFORMATION_SCHEMA` tables, in addition to the tables included for MySQL compatibility.

Many `INFORMATION_SCHEMA` tables have a corresponding `SHOW` command. The benefit of querying `INFORMATION_SCHEMA` is that it is possible to join between tables.

## Tables for MySQL compatibility

| Table Name                                                                              | Description                 |
|-----------------------------------------------------------------------------------------|-----------------------------|
| [`CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)            | Provides a list of character sets the server supports. |
| [`COLLATIONS`](/information-schema/information-schema-collations.md)                    | Provides a list of collations that the server supports. |
| [`COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md) | Explains which collations apply to which character sets. |
| [`COLUMNS`](/information-schema/information-schema-columns.md)                          | Provides a list of columns for all tables. |
| `COLUMN_PRIVILEGES`                                                                     | Not implemented by TiDB. Returns zero rows. |
| `COLUMN_STATISTICS`                                                                     | Not implemented by TiDB. Returns zero rows. |
| [`ENGINES`](/information-schema/information-schema-engines.md)                          | Provides a list of supported storage engines. |
| `EVENTS`                                                                                | Not implemented by TiDB. Returns zero rows. |
| `FILES`                                                                                 | Not implemented by TiDB. Returns zero rows. |
| `GLOBAL_STATUS`                                                                         | Not implemented by TiDB. Returns zero rows. |
| `GLOBAL_VARIABLES`                                                                      | Not implemented by TiDB. Returns zero rows. |
| [`KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)        | Describes the key constraints of the columns, such as the primary key constraint. |
| `OPTIMIZER_TRACE`                                                                       | Not implemented by TiDB. Returns zero rows. |
| `PARAMETERS`                                                                            | Not implemented by TiDB. Returns zero rows. |
| [`PARTITIONS`](/information-schema/information-schema-partitions.md)                    | Provides a list of table partitions. |
| `PLUGINS`                                                                               | Not implemented by TiDB. Returns zero rows. |
| [`PROCESSLIST`](/information-schema/information-schema-processlist.md)                  | Provides similar information to the command `SHOW PROCESSLIST`. |
| `PROFILING`                                                                             | Not implemented by TiDB. Returns zero rows. |
| `REFERENTIAL_CONSTRAINTS`                                                               | Provides information on `FOREIGN KEY` constraints. |
| `ROUTINES`                                                                              | Not implemented by TiDB. Returns zero rows. |
| [`SCHEMATA`](/information-schema/information-schema-schemata.md)                        | Provides similar information to `SHOW DATABASES`. |
| `SCHEMA_PRIVILEGES`                                                                     | Not implemented by TiDB. Returns zero rows. |
| `SESSION_STATUS`                                                                        | Not implemented by TiDB. Returns zero rows. |
| [`SESSION_VARIABLES`](/information-schema/information-schema-session-variables.md)      | Provides similar functionality to the command `SHOW SESSION VARIABLES` |
| [`STATISTICS`](/information-schema/information-schema-statistics.md)                    | Provides information on table indexes. |
| [`TABLES`](/information-schema/information-schema-tables.md)                            | Provides a list of tables that the current user has visibility of. Similar to `SHOW TABLES`. |
| `TABLESPACES`                                                                           | Not implemented by TiDB. Returns zero rows. |
| [`TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)      | Provides information on primary keys, unique indexes and foreign keys. |
| `TABLE_PRIVILEGES`                                                                      | Not implemented by TiDB. Returns zero rows. |
| `TRIGGERS`                                                                              | Not implemented by TiDB. Returns zero rows. |
| [`USER_PRIVILEGES`](/information-schema/information-schema-user-privileges.md)          | Summarizes the privileges associated with the current user. |
| [`VIEWS`](/information-schema/information-schema-views.md)                              | Provides a list of views that the current user has visibility of. Similar to running `SHOW FULL TABLES WHERE table_type = 'VIEW'` |

## Tables that are TiDB extensions

| Table Name                                                                              | Description |
|-----------------------------------------------------------------------------------------|-------------|
| [`ANALYZE_STATUS`](/information-schema/information-schema-analyze-status.md)            | Provides information about tasks to collect statistics. |
| [`CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md)  | Provides a summary of errors and warnings generated by client requests and returned to clients. |
| [`CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md)  | Provides a summary of errors and warnings generated by clients. |
| [`CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md)   | Provides a summary of errors and warnings generated by clients. |
| [`CLUSTER_CONFIG`](/information-schema/information-schema-cluster-config.md)            | Provides details about configuration settings for the entire TiDB cluster. |
| `CLUSTER_DEADLOCKS` | Provides a cluster-level view of the `DEADLOCKS` table. |
| [`CLUSTER_HARDWARE`](/information-schema/information-schema-cluster-info.md)            | Provides details on the underlying physical hardware discovered on each TiDB component. |
| [`CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)                | Provides details on the current cluster topology. |
| [`CLUSTER_LOAD`](/information-schema/information-schema-cluster-load.md)                | Provides current load information for TiDB servers in the cluster. |
| [`CLUSTER_LOG`](/information-schema/information-schema-cluster-log.md)                  | Provides a log for the entire TiDB cluster |
| `CLUSTER_PROCESSLIST`                                                                   | Provides a cluster-level view of the `PROCESSLIST` table. |
| `CLUSTER_SLOW_QUERY`                                                                    | Provides a cluster-level view of the `SLOW_QUERY` table. |
| `CLUSTER_STATEMENTS_SUMMARY`                                                            | Provides a cluster-level view of the `STATEMENTS_SUMMARY` table. |
| `CLUSTER_STATEMENTS_SUMMARY_HISTORY`                                                    | Provides a cluster-level view of the `STATEMENTS_SUMMARY_HISTORY` table. |
| `CLUSTER_TIDB_TRX` | Provides a cluster-level view of the `TIDB_TRX` table. |
| [`CLUSTER_SYSTEMINFO`](/information-schema/information-schema-cluster-systeminfo.md)    | Provides details about kernel parameter configuration for servers in the cluster. |
| [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md) | Provides the lock-waiting information on the TiKV server. |
| [`DDL_JOBS`](/information-schema/information-schema-ddl-jobs.md)                        | Provides similar output to `ADMIN SHOW DDL JOBS` |
| [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md) | Provides the information of several deadlock errors that have recently occurred. |
| [`INSPECTION_RESULT`](/information-schema/information-schema-inspection-result.md)      | Triggers internal diagnostics checks. |
| [`INSPECTION_RULES`](/information-schema/information-schema-inspection-rules.md)        | A list of internal diagnostic checks performed. |
| [`INSPECTION_SUMMARY`](/information-schema/information-schema-inspection-summary.md)    | A summarized report of important monitoring metrics. |
| [`METRICS_SUMMARY`](/information-schema/information-schema-metrics-summary.md)          | A summary of metrics extracted from Prometheus. |
| `METRICS_SUMMARY_BY_LABEL`                                                              | See `METRICS_SUMMARY` table. |
| [`METRICS_TABLES`](/information-schema/information-schema-metrics-tables.md)            | Provides the PromQL definitions for tables in `METRICS_SCHEMA`. |
| [`SEQUENCES`](/information-schema/information-schema-sequences.md)                      | The TiDB implementation of sequences is based on MariaDB. |
| [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)                    | Provides information on slow queries on the current TiDB server. |
| [`STATEMENTS_SUMMARY`](/statement-summary-tables.md)                                    | Similar to performance_schema statement summary in MySQL. |
| [`STATEMENTS_SUMMARY_HISTORY`](/statement-summary-tables.md)                            | Similar to performance_schema statement summary history in MySQL. |
| [`TABLE_STORAGE_STATS`](/information-schema/information-schema-table-storage-stats.md)  | Provides details about table sizes in storage. |
| [`TIDB_HOT_REGIONS`](/information-schema/information-schema-tidb-hot-regions.md)        | Provides statistics about which regions are hot. |
| [`TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)                | Provides index information about TiDB tables. |
| [`TIDB_SERVERS_INFO`](/information-schema/information-schema-tidb-servers-info.md)      | Provides a list of TiDB servers (namely, tidb-server component) |
| [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) | Provides the information of the transactions that are being executed on the TiDB node. |
| [`TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)          | Provides details about TiFlash replicas. |
| [`TIKV_REGION_PEERS`](/information-schema/information-schema-tikv-region-peers.md)      | Provides details about where regions are stored. |
| [`TIKV_REGION_STATUS`](/information-schema/information-schema-tikv-region-status.md)    | Provides statistics about regions. |
| [`TIKV_STORE_STATUS`](/information-schema/information-schema-tikv-store-status.md)      | Provides basic information about TiKV servers. |
