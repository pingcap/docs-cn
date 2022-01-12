---
title: 创建数据迁移任务
summary: 了解 TiDB Data Migration 如何创建数据迁移任务。
aliases: ['/docs-cn/tidb-data-migration/dev/create-task/']
---

# 创建数据迁移任务

`start-task` 命令用于创建数据迁移任务。当数据迁移任务启动时，DM 将[自动对相应权限和配置进行前置检查](/dm/dm-precheck.md)。

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

## 命令用法示例

{{< copyable "" >}}

```bash
start-task [ -s "mysql-replica-01"] ./task.yaml
```

## 参数解释

+ `-s`：
    - 可选
    - 指定在特定的一个 MySQL 源上执行 `task.yaml`
    - 如果设置，则只启动指定任务在该 MySQL 源上的子任务
+ `config-file`：
    - 必选
    - 指定 `task.yaml` 的文件路径
+ `remove-meta`:
    - 可选
    - 如果设置，则在启动指定任务时会移除该任务之前存在的 metadata

## 返回结果示例

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
