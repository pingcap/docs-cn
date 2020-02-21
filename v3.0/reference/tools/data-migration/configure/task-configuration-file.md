---
title: Data Migration Task Configuration File
summary: This document introduces the task configuration file of Data Migration.
category: reference
---

# Data Migration Task Configuration File

This document introduces the basic task configuration file of Data Migration --
[`task_basic.yaml`](https://github.com/pingcap/dm/blob/master/dm/master/task_advanced.yaml), including [global configuration](#global-configuration) and [instance configuration](#instance-configuration).

DM also implements [an advanced task configuration file](/v3.0/reference/tools/data-migration/configure/task-configuration-file-full.md) which provides greater flexibility and more control over DM.

For the feature and configuration of each configuration item, see [Data replication features](/v3.0/reference/tools/data-migration/features/overview.md).

## Important concepts

For description of important concepts including `source-id` and the DM-worker ID, see [Important concepts](/v3.0/reference/tools/data-migration/configure/overview.md#important-concepts).

## Task configuration file template (basic)

The following is a task configuration file template which allows you to perform basic data replication tasks.

```yaml
---

# ----------- Global configuration -----------
## ********** Basic configuration ************

```yaml
name: test                      # The name of the task. Should be globally unique.
task-mode: all                  # The task mode. Can be set to `full`/`incremental`/`all`.

target-database:                # Configuration of the downstream database instance.
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""                  # The dmctl encryption is needed when the password is not empty.

## ******** Feature configuration set **********
# The filter rule set of the black white list of the matched table of the upstream database instance.
black-white-list:
  bw-rule-1:             # # The name of the black and white lists filtering rule of the table matching the upstream database instance.
    do-dbs: ["all_mode"] # white list of upstream tables needs to be replicated
# ----------- Instance configuration -----------
mysql-instances:
  # The ID of the upstream instance or replication group ID. It can be configured by referring to the `source-id` in the `dm-master.toml` file.
  - source-id: "mysql-replica-01"
    black-white-list:  "bw-rule-1"
        mydumper-thread: 4             # The number of threads that Mydumper uses for dumping data, new in v1.0.2 and later versions
        loader-thread: 16              # The number of threads that Loader uses for loading data, new in v1.0.2 and later versions
        syncer-thread: 16              # The number of threads that Syncer uses for replicating incremental data, new in v1.0.2 and later versions
  - source-id: "mysql-replica-02"
    black-white-list:  "bw-rule-1"
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

- Description: the task mode that can be used to specify the data replication task to be executed.
- Value: string (`full`, `incremental`, or `all`).
    - `full` only makes a full backup of the upstream database and then imports the full data to the downstream database.
    - `incremental`: Only replicates the incremental data of the upstream database to the downstream database using the binlog. You can set the `meta` configuration item of the instance configuration to specify the starting position of incremental replication.
    - `all`: `full` + `incremental`. Makes a full backup of the upstream database, imports the full data to the downstream database, and then uses the binlog to make an incremental replication to the downstream database starting from the exported position during the full backup process (binlog position).

### Feature configuration set

For basic applications, you only need to modify the black and white lists filtering rule. Refer to the comments about `black-white-list` in the [template](#task-configuration-file-template-basic) or [Black & white table lists](/v3.0/reference/tools/data-migration/features/overview.md#black--white-table-lists) to see more details.

## Instance configuration

This part defines the subtask of data replication. DM supports replicating data from one or multiple MySQL instances to the same instance.

For more details, refer to the comments about `mysql-instances` in the [template](#task-configuration-file-template-basic).
