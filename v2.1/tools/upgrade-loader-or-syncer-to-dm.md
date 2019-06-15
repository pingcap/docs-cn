---
title: Upgrade Loader or Syncer to Data Migration
summary: This document introduces how to upgrade Loader or Syncer to Data Migration. 
category: tools
---

# Upgrade Loader or Syncer to Data Migration

This document introduces how to upgrade Loader or Syncer to DM (Data Migration).

## Upgrade Loader to Data Migration

Loader is a tool used to load the full data that is dumped from [mydumper](../tools/mydumper.md) to TiDB.

When the `task-mode` of the task DM executes is `full`, DM automatically uses `dumper` to dump data and then uses `loader` to load the data.

To upgrade Loader to DM, perform the following steps:

1. [Deploy the DM cluster](../tools/data-migration-deployment.md).
2. Refer to [Loader configuration change](#loader-configuration-change) and generate the corresponding task configuration file.
3. [Use dmctl to start the task](../tools/data-migration-manage-task.md#create-the-data-replication-task).

### Loader Configuration change 

Loader uses the TOML file to define the process-related operation parameters and replication task parameters; DM uses the YAML file to define task configuration file parameters.

Taking the configuration options in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md) as examples, the corresponding relationship of task configuration options between Loader and DM is as follows:

| Configuration in Loader | Corresponding configuration in DM |
| ---------------------- | --------------------------------- |
| `pool-size` | `pool-size` of `loader` |
| `dir` | `dir` of `loader` |
| `db` | `target-database` |
| `alternative-db` | Deprecated |
| `source-db` | Deprecated |
| `route-rules` | `route-rules` |
| `pattern-schema` | `schema-pattern` |
| `pattern-table` | `table-pattern` |
| `do-db` | `do-dbs` of `black-white-list`. The filtering feature of databases has been refactored. For detailed configuration, see `do-dbs` in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md). |
| `do-table` | `do-tables` of `black-white-list`. The filtering feature of tables has been refactored. For detailed configuration, see `do-tables` in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md). |
| `ignore-db` | `ignore-dbs` of `black-white-list`. The filtering feature of databases has been refactored. For detailed configuration, see `ignore-dbs` in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md). |
| `ignore-table` | `ignore-tables` of `black-white-list`. The filtering feature of tables has been refactored. For detailed configuration, see `ignore-tables` in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md). |
| `rm-checkpoint` | Deprecated. A configuration option with a similar feature is `remove-meta`. |

Taking the configuration options in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md) as examples, the corresponding relationship of task configuration options between mydumper and DM is as follows:

| Configuration in mydumper | Corresponding configuration in DM |
| ---------------------- | --------------------------------- |
| `host` | No corresponding option. Configured when DM-worker is deployed. |
| `port` | No corresponding option. Configured when DM-worker is deployed. |
| `user` | No corresponding option. Configured when DM-worker is deployed. |
| `password` | No corresponding option. Configured when DM-worker is deployed. |
| `threads` | `threads` of `mydumper` |
| `chunk-filesize` | `chunk-filesize` of `mydumper` |
| `skip-tz-utc` | `skip-tz-utc` of `mydumper` |

Other options are specified using `extra-args` of `mydumper`. Their usage in DM is the same as that in mydumper.

## Upgrade Syncer to Data Migration

Syncer is a tool used to import data incrementally. The task Syncer executes is corresponding to the replication task with `incremental` `task-mode` in DM. The `syncer` processing unit feature of dm-worker in DM is corresponding to the Syncer feature.

To upgrade Syncer to DM, perform the following steps:

1. [Deploy the DM cluster](../tools/data-migration-deployment.md).
2. Refer to [Syncer configuration change](#syncer-configuration-change) and generate the corresponding task configuration file.
3. [Use dmctl to start the task](../tools/data-migration-manage-task.md#create-the-data-replication-task).

### Syncer Configuration change

Syncer uses the TOML file to define the process-related operation parameters and replication task parameters; DM uses the YAML file to define task configuration file parameters.

Taking the configuration options in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md) as examples, the corresponding relationship of task configuration options between Syncer and DM is as follows:

| Configuration in Syncer | Corresponding configuration in DM |
| ---------------------- | --------------------------------- |
| `server-id` | Transferred to `dm-worker.toml` |
| `flavor` | Transferred to `dm-worker.toml` |
| `enable-gtid` | Transferred to `dm-worker.toml` |
| `auto-fix-gtid` | Transferred to `dm-worker.toml` |
| `meta` | `meta` of `mysql-instances`. `binlog-name`/`binlog-pos` of `meta` in Syncer corresponds to that of `mysql-instances`. |
| `persistent-dir` | Deprecated |
| `worker-count` | `worker-count` of `syncer` |
| `batch` | `batch` of `syncer` |
| `max-retry` | `max-retry` of `syncer` |
| `do-db` | `do-dbs` of `black-white-list`. The filtering feature of databases has been refactored. For detailed configuration, see `do-dbs` in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md). |
| `do-table` | `do-tables` of `black-white-list`. The filtering feature of tables has been refactored. For detailed configuration, see `do-tables` in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md). |
| `ignore-db` | `ingore-dbs` of `black-white-list`. The filtering feature of databases has been refactored. For detailed configuration, see `ignore-dbs` in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md). |
| `ignore-table` | `ignore-tables` of `black-white-list`. The filtering feature of tables has been refactored. For detailed configuration, see `ignore-tables` in [Data Migration Task Configuration File](../tools/dm-task-configuration-file-intro.md). |
| `skip-ddls` | Deprecated. Use `filters`. |
| `skip-sqls` | Deprecated. Use `filters`. |
| `skip-events` | Deprecated. Use `filters`. |
| `skip-dmls` | Deprecated. Use `filters`. |
| `route-rules` | `route-rules`|
| `pattern-schema` | `schema-pattern` |
| `pattern-table` | `table-pattern` |
| `from` | `config` of `mysql-instances`. Keep it consistent with the upstream MySQL information during the DM-worker deployment. |
| `to` | `target-database` |
| `disable-detect` | `disable-detect` of `syncer` |
| `safe-mode` | `safe-mode` of `syncer` |
| `stop-on-ddl` | Deprecated |
| `execute-ddl-timeout` | Deprecated |
| `execute-dml-timeout` | Deprecated |
