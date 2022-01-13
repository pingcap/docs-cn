---
title: 暂停数据迁移任务
summary: 了解 TiDB Data Migration 如何暂停数据迁移任务。
aliases: ['/docs-cn/tidb-data-migration/dev/pause-task/']
---

# 暂停数据迁移任务

`pause-task` 命令用于暂停数据迁移任务。

> **注意：**
>
> 有关 `pause-task` 与 `stop-task` 的区别如下：
>
> - 使用 `pause-task` 仅暂停迁移任务的执行，但仍然会在内存中保留任务的状态信息等，且可通过 `query-status` 进行查询；使用 `stop-task` 会停止迁移任务的执行，并移除内存中与该任务相关的信息，且不可再通过 `query-status` 进行查询，但不会移除已经写入到下游数据库中的数据以及其中的 checkpoint 等 `dm_meta` 信息。
> - 使用 `pause-task` 暂停迁移任务期间，由于任务本身仍然存在，因此不能再启动同名的新任务，且会阻止对该任务所需 relay log 的清理；使用 `stop-task` 停止任务后，由于任务不再存在，因此可以再启动同名的新任务，且不会阻止对 relay log 的清理。
> - `pause-task` 一般用于临时暂停迁移任务以排查问题等；`stop-task` 一般用于永久删除迁移任务或通过与 `start-task` 配合以更新配置信息。

{{< copyable "" >}}

```bash
help pause-task
```

```
pause a specified running task

Usage:
 dmctl pause-task [-s source ...] <task-name | task-file> [flags]

Flags:
 -h, --help   help for pause-task

Global Flags:
 -s, --source strings   MySQL Source ID
```

## 命令用法示例

{{< copyable "" >}}

```bash
pause-task [-s "mysql-replica-01"] task-name
```

## 参数解释

- `-s`：
    - 可选
    - 指定在特定的一个 MySQL 源上暂停数据迁移任务的子任务
    - 如果设置，则只暂停该任务在指定 MySQL 源上的子任务
- `task-name| task-file`：
    - 必选
    - 指定任务名称或任务文件路径

## 返回结果示例

{{< copyable "" >}}

```bash
pause-task test
```

```
{
    "op": "Pause",
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
