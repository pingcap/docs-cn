---
title: Create a Data Migration Task
summary: Learn how to create a data migration task in TiDB Data Migration.
---

# Create a Data Migration Task

You can use the `start-task` command to create a data migration task. When the data migration task is started, DM [prechecks privileges and configurations](/dm/dm-precheck.md).

{{< copyable "" >}}

```bash
help start-task
```

```
Starts a task as defined in the configuration file

Usage:
  dmctl start-task [-s source ...] [--remove-meta] <config-file> [flags]

Flags:
  -h, --help                help for start-task
      --remove-meta         whether to remove task's meta data
      --start-time string   specify the start time of binlog replication, e.g. '2021-10-21 00:01:00' or 2021-10-21T00:01:00

Global Flags:
      --config string        Path to config file.
      --master-addr string   Master API server address, this parameter is required when interacting with the dm-master
      --rpc-timeout string   RPC timeout, default is 10m. (default "10m")
  -s, --source strings       MySQL Source ID.
      --ssl-ca string        Path of file that contains list of trusted SSL CAs for connection.
      --ssl-cert string      Path of file that contains X509 certificate in PEM format for connection.
      --ssl-key string       Path of file that contains X509 key in PEM format for connection.
  -V, --version              Prints version and exit.
```

## Usage example

{{< copyable "" >}}

```bash
start-task [ -s "mysql-replica-01"] ./task.yaml
```

## Flags description

- `-s`: (Optional) Specifies the MySQL source to execute `task.yaml`. If it is set, the command only starts the subtasks of the specified task on the MySQL source.
- `config-file`: (Required) Specifies the file path of `task.yaml`.
- `remove-meta`: (Optional) Specifies whether to remove the task's previous metadata when starting the task.
- `start-time`: (Optional) Specifies the start time of binlog replication.
    - Format: `'2021-10-21 00:01:00'` or `2021-10-21T00:01:00`.
    - For incremental tasks, you can specify a rough starting point for the task using this flag. This flag takes precedence over the binlog position in the task configuration file and the binlog position in the downstream checkpoint.
    - When the task already has a checkpoint, if you start the task using this flag, DM automatically enables safe mode until the replication passes the checkpoint. This is to avoid the data duplication error caused by resetting the task to an earlier position.
        - When you reset the task to an earlier position, if the table schema at that time point is different from the downstream at the current time point, the task might report an error.
        - When you reset the task to a later position, note that the skipped binlog might have dirty data left in the downstream.
    - When you specify an earlier start time, DM starts migration from the earliest binlog position available.
    - When you specify a later start time, DM reports an error: `start-time {input-time} is too late, no binlog location matches it`.

## Returned results

{{< copyable "" >}}

```bash
start-task task.yaml
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        }
    ]
}
```
