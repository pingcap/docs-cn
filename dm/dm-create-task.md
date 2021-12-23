---
title: Create a Data Migration Task
summary: Learn how to create a data migration task in TiDB Data Migration.
aliases: ['/tidb-data-migration/dev/create-task/']
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
  -h, --help          Help for start-task
      --remove-meta   Whether to remove task's metadata
Global Flags:
  -s, --source strings   MySQL Source ID
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
