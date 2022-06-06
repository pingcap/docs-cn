---
title: 恢复数据迁移任务
summary: 了解 TiDB Data Migration 如何恢复数据迁移任务。
---

# 恢复数据迁移任务

`resume-task` 命令用于恢复处于 `Paused` 状态的数据迁移任务，通常用于在人为处理完造成迁移任务暂停的故障后手动恢复迁移任务。

{{< copyable "" >}}

```bash
help resume-task
```

```
resume a specified paused task

Usage:
 dmctl resume-task [-s source ...] <task-name | task-file> [flags]

Flags:
 -h, --help   help for resume-task

Global Flags:
 -s, --source strings   MySQL Source ID
```

## 命令用法示例

{{< copyable "" >}}

```bash
resume-task [-s "mysql-replica-01"] task-name
```

## 参数解释

- `-s`：
    - 可选
    - 指定在特定的一个 MySQL 源上恢复数据迁移任务的子任务
    - 如果设置，则只恢复该任务在指定 MySQL 源上的子任务
- `task-name | task-file`：
    - 必选
    - 指定任务名称或任务文件路径

## 返回结果示例

{{< copyable "" >}}

```bash
resume-task test
```

```
{
    "op": "Resume",
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
