---
title: Data Migration Task Configuration File
summary: This document introduces the task configuration file of Data Migration.
aliases: ['/docs/tidb-data-migration/dev/task-configuration-file/']
---

# Data Migration Task Configuration File

This document introduces the basic task configuration file of Data Migration (DM), including [global configuration](#global-configuration) and [instance configuration](#instance-configuration).

DM also implements [an advanced task configuration file](/dm/task-configuration-file-full.md) which provides greater flexibility and more control over DM.

For the feature and configuration of each configuration item, see [Data migration features](/dm/dm-key-features.md).

## Important concepts

For description of important concepts including `source-id` and the DM-worker ID, see [Important concepts](/dm/dm-config-overview.md#important-concepts).

## Task configuration file template (basic)

The following is a task configuration file template which allows you to perform basic data migration tasks.

```yaml
---

# ----------- Global configuration -----------
## ********** Basic configuration ************
name: test                      # The name of the task. Should be globally unique.
task-mode: all                  # The task mode. Can be set to `full`/`incremental`/`all`.

target-database:                # Configuration of the downstream database instance.
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""                  # It is recommended to use password encrypted with dmctl if the password is not empty.

## ******** Feature configuration set **********
# The filter rule set of the block allow list of the matched table of the upstream database instance.
block-allow-list:        # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  bw-rule-1:             # The name of the block and allow lists filtering rule of the table matching the upstream database instance.
    do-dbs: ["all_mode"] # Allow list of upstream tables needs to be migrated.
# ----------- Instance configuration -----------
mysql-instances:
  # The ID of the upstream instance or migration group. It can be configured by referring to the `source-id` in the `dm-master.toml` file.
  - source-id: "mysql-replica-01"
    block-allow-list:  "bw-rule-1"
    mydumper-thread: 4             # The number of threads that the dump processing unit uses for dumping data.
    loader-thread: 16              # The number of threads that the load processing unit uses for loading data. When multiple instances are migrating data to TiDB at the same time, reduce the value according to the load.
    syncer-thread: 16              # The number of threads that the sync processing unit uses for replicating incremental data. When multiple instances are migrating data to TiDB at the same time, reduce the value according to the load.

  - source-id: "mysql-replica-02"
    block-allow-list:  "bw-rule-1" # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
    mydumper-thread: 4
    loader-thread: 16
    syncer-thread: 16
```

## Configuration order

1. Edit the [global configuration](#global-configuration).
2. Edit the [instance configuration](#instance-configuration) based on the global configuration.

## Global configuration

### Basic configuration

Refer to the comments in the [template](#task-configuration-file-template-basic) to see more details. Specific instruction about `task-mode` are as follows:

- Description: the task mode that can be used to specify the data migration task to be executed.
- Value: string (`full`, `incremental`, or `all`).
    - `full` only makes a full backup of the upstream database and then imports the full data to the downstream database.
    - `incremental`: Only replicates the incremental data of the upstream database to the downstream database using the binlog. You can set the `meta` configuration item of the instance configuration to specify the starting position of incremental replication.
    - `all`: `full` + `incremental`. Makes a full backup of the upstream database, imports the full data to the downstream database, and then uses the binlog to make an incremental replication to the downstream database starting from the exported position during the full backup process (binlog position).

> **Note:**
>
> DM uses dumpling to execute full backups. During the full backup process, [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock) is used to temporarily interrupt the DML and DDL operations of the replica database, to ensure the consistency of the backup connections, and to record the binlog position (POS) information for incremental replications. The lock is released after all backup connections start transactions.
>
> It is recommended to perform full backups during off-peak hours or on the MySQL replica database.

### Feature configuration set

For basic applications, you only need to modify the block and allow lists filtering rule. Refer to the comments about `block-allow-list` in the [template](#task-configuration-file-template-basic) or [Block & allow table lists](/dm/dm-key-features.md#block-and-allow-table-lists) to see more details.

## Instance configuration

This part defines the subtask of data migration. DM supports migrating data from one or multiple MySQL instances to the same instance.

For more details, refer to the comments about `mysql-instances` in the [template](#task-configuration-file-template-basic).

## Modify the task configuration

It is recommended to update the modified configuration to the DM cluster by executing the `stop-task` and `start-task` commands, since the DM cluster persists the task configuration. If the task configuration file is modified directly, without restarting the task, the configuration changes does not take effect. In this case, the DM cluster still reads the previous task configuration when the DM cluster is restarted.

To illustrate how to modify the task configuration, the following is an example of modifying `timezone`:

1. Modify the task configuration file and set `timezone` to `Asia/Shanghai`.

2. Stop the task by executing the `stop-task` command:

    {{< copyable "" >}}

    ```bash
    stop-task <task-name | task-file>
    ```

3. Start the task by executing the `start-task` command:

    {{< copyable "" >}}

    ```bash
    start-task <config-file>
    ```

4. In DM v6.0 and later versions, you can check whether the configuration takes effect by executing the `config` command:

    {{< copyable "" >}}

    ```bash
    get-config task <task-name>
    ```
