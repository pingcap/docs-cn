---
title: Information Schema
aliases: ['/docs-cn/dev/reference/system-databases/information-schema/','/docs-cn/dev/reference/system-databases/information-schema/','/docs-cn/dev/system-tables/system-table-information-schema/','/zh/tidb/dev/system-table-information-schema/']
---

# Information Schema

Information Schema 提供了一种查看系统元数据的 ANSI 标准方法。除了包含与 MySQL 兼容的表外，TiDB 还提供了许多自定义的 `INFORMATION_SCHEMA` 表。

许多 `INFORMATION_SCHEMA` 表都有相应的 `SHOW` 命令。查询 `INFORMATION_SCHEMA` 的好处是可以在表之间进行 `join` 操作。

## 与 MySQL 兼容的表

| 表名                                                                                                                       | 描述                                                                              |
| -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [`CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)                                               | 提供 TiDB 支持的字符集列表。                                                      |
| [`COLLATIONS`](/information-schema/information-schema-collations.md)                                                       | 提供 TiDB 支持的排序规则列表。                                                    |
| [`COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md) | 说明哪些排序规则适用于哪些字符集。                                                |
| [`COLUMNS`](/information-schema/information-schema-columns.md)                                                             | 提供所有表中列的列表。                                                            |
| `COLUMN_PRIVILEGES`                                                                                                        | TiDB 未实现，返回零行。                                                           |
| `COLUMN_STATISTICS`                                                                                                        | TiDB 未实现，返回零行。                                                           |
| [`ENGINES`](/information-schema/information-schema-engines.md)                                                             | 提供支持的存储引擎列表。                                                          |
| `EVENTS`                                                                                                                   | TiDB 未实现，返回零行。                                                           |
| `FILES`                                                                                                                    | TiDB 未实现，返回零行。                                                           |
| `GLOBAL_STATUS`                                                                                                            | TiDB 未实现，返回零行。                                                           |
| `GLOBAL_VARIABLES`                                                                                                         | TiDB 未实现，返回零行。                                                           |
| [`KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)                                           | 描述列的键约束，例如主键约束。                                                    |
| `OPTIMIZER_TRACE`                                                                                                          | TiDB 未实现，返回零行。                                                           |
| `PARAMETERS`                                                                                                               | TiDB 未实现，返回零行。                                                           |
| [`PARTITIONS`](/information-schema/information-schema-partitions.md)                                                       | 提供表分区的列表。                                                                |
| `PLUGINS`                                                                                                                  | TiDB 未实现，返回零行。                                                           |
| [`PROCESSLIST`](/information-schema/information-schema-processlist.md)                                                     | 提供与 `SHOW PROCESSLIST` 命令类似的信息。                                        |
| `PROFILING`                                                                                                                | TiDB 未实现，返回零行。                                                           |
| `REFERENTIAL_CONSTRAINTS`                                                                                                  | 提供有关 `FOREIGN KEY` 约束的信息。                                                          |
| `ROUTINES`                                                                                                                 | TiDB 未实现，返回零行。                                                           |
| [`SCHEMATA`](/information-schema/information-schema-schemata.md)                                                           | 提供与 `SHOW DATABASES` 命令类似的信息。                                          |
| `SCHEMA_PRIVILEGES`                                                                                                        | TiDB 未实现，返回零行。                                                           |
| `SESSION_STATUS`                                                                                                           | TiDB 未实现，返回零行。                                                           |
| [`SESSION_VARIABLES`](/information-schema/information-schema-session-variables.md)                                         | 提供与 `SHOW SESSION VARIABLES` 命令类似的功能。                                  |
| [`STATISTICS`](/information-schema/information-schema-statistics.md)                                                       | 提供有关表索引的信息。                                                            |
| [`TABLES`](/information-schema/information-schema-tables.md)                                                               | 提供当前用户可见的表的列表。 类似于 `SHOW TABLES`。                               |
| `TABLESPACES`                                                                                                              | TiDB 未实现，返回零行。                                                           |
| [`TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)                                         | 提供有关主键、唯一索引和外键的信息。                                              |
| `TABLE_PRIVILEGES`                                                                                                         | TiDB 未实现，返回零行。                                                           |
| `TRIGGERS`                                                                                                                 | TiDB 未实现，返回零行。                                                           |
| [`USER_PRIVILEGES`](/information-schema/information-schema-user-privileges.md)                                             | 汇总与当前用户相关的权限。                                                        |
| [`VIEWS`](/information-schema/information-schema-views.md)                                                                 | 提供当前用户可见的视图列表。类似于 `SHOW FULL TABLES WHERE table_type = 'VIEW'`。 |

## TiDB 中的扩展表

| 表名                                                                                    | 描述                                                           |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [`ANALYZE_STATUS`](/information-schema/information-schema-analyze-status.md)            | 提供有关收集统计信息的任务的信息。                             |
| [`CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md) | 汇总由客户端请求生成并返回给客户端的错误和警告。               |
| [`CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md) | 汇总由客户端产生的错误和警告。                                 |
| [`CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md)   | 汇总由客户端产生的错误和警告。                                 |
| [`CLUSTER_CONFIG`](/information-schema/information-schema-cluster-config.md)            | 提供有关整个 TiDB 集群的配置设置的详细信息。                   |
| `CLUSTER_DEADLOCKS`                                                                     | 提供 `DEADLOCKS` 表的集群级别的视图。                          |
| [`CLUSTER_HARDWARE`](/information-schema/information-schema-cluster-info.md)            | 提供在每个 TiDB 组件上发现的底层物理硬件的详细信息。           |
| [`CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)                | 提供当前集群拓扑的详细信息。                                   |
| [`CLUSTER_LOAD`](/information-schema/information-schema-cluster-load.md)                | 提供集群中 TiDB 服务器的当前负载信息。                         |
| [`CLUSTER_LOG`](/information-schema/information-schema-cluster-log.md)                  | 提供整个 TiDB 集群的日志。                                     |
| `CLUSTER_PROCESSLIST`                                                                   | 提供 `PROCESSLIST` 表的集群级别的视图。                        |
| `CLUSTER_SLOW_QUERY`                                                                    | 提供 `SLOW_QUERY` 表的集群级别的视图。                         |
| `CLUSTER_STATEMENTS_SUMMARY`                                                            | 提供 `STATEMENTS_SUMMARY` 表的集群级别的视图。                 |
| `CLUSTER_STATEMENTS_SUMMARY_HISTORY`                                                    | 提供 `STATEMENTS_SUMMARY_HISTORY` 表的集群级别的视图。         |
| `CLUSTER_TIDB_TRX`                                                                      | 提供 `TIDB_TRX` 表的集群级别的视图。                           |
| [`CLUSTER_SYSTEMINFO`](/information-schema/information-schema-cluster-systeminfo.md)    | 提供集群中服务器的内核参数配置的详细信息。                     |
| [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)          | 提供 TiKV 服务器上的等锁信息。                                 |
| [`DDL_JOBS`](/information-schema/information-schema-ddl-jobs.md)                        | 提供与 `ADMIN SHOW DDL JOBS` 类似的输出。                      |
| [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)                      | 提供 TiDB 节点上最近发生的数次死锁错误的信息。                 |
| [`INSPECTION_RESULT`](/information-schema/information-schema-inspection-result.md)      | 触发内部诊断检查。                                             |
| [`INSPECTION_RULES`](/information-schema/information-schema-inspection-rules.md)        | 进行的内部诊断检查的列表。                                     |
| [`INSPECTION_SUMMARY`](/information-schema/information-schema-inspection-summary.md)    | 重要监视指标的摘要报告。                                       |
| [`METRICS_SUMMARY`](/information-schema/information-schema-metrics-summary.md)          | 从 Prometheus 获取的指标的摘要。                               |
| `METRICS_SUMMARY_BY_LABEL`                                                              | 参见 `METRICS_SUMMARY` 表。                                    |
| [`METRICS_TABLES`](/information-schema/information-schema-metrics-tables.md)            | 为 `METRICS_SCHEMA` 中的表提供 PromQL 定义。                   |
| [`SEQUENCES`](/information-schema/information-schema-sequences.md)                      | 描述了基于 MariaDB 实现的 TiDB 序列。                          |
| [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)                    | 提供当前 TiDB 服务器上慢查询的信息。                           |
| [`STATEMENTS_SUMMARY`](/statement-summary-tables.md)                                    | 类似于 MySQL 中的 performance_schema 语句摘要。                |
| [`STATEMENTS_SUMMARY_HISTORY`](/statement-summary-tables.md)                            | 类似于 MySQL 中的 performance_schema 语句摘要历史。            |
| [`TABLE_STORAGE_STATS`](/information-schema/information-schema-table-storage-stats.md)  | 提供存储的表的大小的详细信息。                                 |
| [`TIDB_HOT_REGIONS`](/information-schema/information-schema-tidb-hot-regions.md)        | 提供有关哪些 Region 访问次数最多的统计信息。                   |
| [`TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)                | 提供有关 TiDB 表的索引信息。                                   |
| [`TIDB_SERVERS_INFO`](/information-schema/information-schema-tidb-servers-info.md)      | 提供 TiDB 服务器的列表                                         |
| [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)                        | 提供 TiDB 节点上正在执行的事务的信息。                         |
| [`TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)          | 提供有关 TiFlash 副本的详细信息。                              |
| [`TIKV_REGION_PEERS`](/information-schema/information-schema-tikv-region-peers.md)      | 提供 Region 存储位置的详细信息。                               |
| [`TIKV_REGION_STATUS`](/information-schema/information-schema-tikv-region-status.md)    | 提供 Region 的统计信息。                                       |
| [`TIKV_STORE_STATUS`](/information-schema/information-schema-tikv-store-status.md)      | 提供 TiKV 服务器的基本信息。                                   |
