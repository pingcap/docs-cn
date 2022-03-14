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
+ `start-time`:
    - 可选
    - 对于增量任务，可以通过该参数大致指定任务起始位点，无需在任务配置文件中指定 binlog 位置。当该任务存在 checkpoint 时，通过这种方式启动任务会自动开启 safemode 直到同步过 checkpoint，以避免重置任务到更早位置时遇到数据重复的报错
    - 格式为 `'2021-10-21 00:01:00'` 或 `2021-10-21T00:01:00`
    - 指定了过早的时间时，会从最早的 binlog 开始同步
    - 指定了过晚的时间时，会报错 `start-time {input-time} is too late, no binlog location matches it`

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
