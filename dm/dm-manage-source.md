---
title: 管理上游数据源
summary: 了解如何管理上游 MySQL 实例。
aliases: ['/docs-cn/tidb-data-migration/dev/manage-source/']
---

# 管理上游数据源配置

本文介绍了如何使用 [dmctl](/dm/dmctl-introduction.md) 组件来管理数据源配置，包括如何加密数据库密码，数据源操作，查看数据源配置，改变数据源与 DM-worker 的绑定关系。

## 加密数据库密码

在 DM 相关配置文件中，推荐使用经 dmctl 加密后的密码。对于同一个原始密码，每次加密后密码不同。

{{< copyable "shell-regular" >}}

```bash
./dmctl -encrypt 'abc!@#123'
```

```
MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=
```

## 数据源操作

`operate-source` 命令向 DM 集群加载、列出、移除数据源。

{{< copyable "" >}}

```bash
help operate-source
```

```
`create`/`update`/`stop`/`show` upstream MySQL/MariaDB source.

Usage:
  dmctl operate-source <operate-type> [config-file ...] [--print-sample-config] [flags]

Flags:
  -h, --help                  help for operate-source
  -p, --print-sample-config   print sample config file of source

Global Flags:
  -s, --source strings   MySQL Source ID
```

### 参数解释

+ `create`：创建一个或多个上游的数据库源。创建多个数据源失败时，会尝试回滚到执行命令之前的状态

+ `update`：更新一个上游的数据库源

+ `stop`：停止一个或多个上游的数据库源。停止多个数据源失败时，可能有部分数据源已成功停止

+ `show`：显示已添加的数据源以及对应的 DM-worker

+ `config-file`：
    - 指定 `source.yaml` 的文件路径
    - 可传递多个文件路径

+ `--print-sample-config`：打印示例配置文件。该参数会忽视其余参数

### 命令用法示例

使用 `operate-source` 命令创建数据源配置：

{{< copyable "" >}}

```bash
operate-source create ./source.yaml
```

其中 `source.yaml` 的配置参考[上游数据库配置文件介绍](/dm/dm-source-configuration-file.md)。

结果如下：

{{< copyable "" >}}

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "dm-worker-1"
        }
    ]
}
```

## 查看数据源配置

> **注意：**
>
> `config` 命令仅在 DM v6.02.0.1 及其以后版本支持, DM v2.0.1+ 可使用 `get-config` 命令。

如果知道 source-id，可以通过 `dmctl --master-addr <master-addr> config source <source-id>` 命令直接查看数据源配置。

{{< copyable "" >}}

```bash
config source mysql-replica-01
```

```
{
  "result": true,
  "msg": "",
  "cfg": "enable-gtid: false
    flavor: mysql
    source-id: mysql-replica-01
    from:
      host: 127.0.0.1
      port: 8407
      user: root
      password: '******'
}
```

如果不知道 source-id，可以先通过 `dmctl --master-addr <master-addr> operate-source show` 查看源数据库列表。

{{< copyable "" >}}

```bash
operate-source show
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "source is added but there is no free worker to bound",
            "source": "mysql-replica-02",
            "worker": ""
        },
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "dm-worker-1"
        }
    ]
}
```

## 改变数据源与 DM-worker 的绑定关系

`transfer-source` 用于改变数据源与 DM-worker 的绑定关系。

{{< copyable "" >}}

```bash
help transfer-source
```

```
Transfers a upstream MySQL/MariaDB source to a free worker.

Usage:
  dmctl transfer-source <source-id> <worker-id> [flags]

Flags:
  -h, --help   help for transfer-source

Global Flags:
  -s, --source strings   MySQL Source ID.
```

在改变绑定关系前，DM 会检查待解绑的 worker 是否正在运行同步任务，如果正在运行则需要先[暂停任务](/dm/dm-pause-task.md)，并在改变绑定关系后[恢复任务](/dm/dm-resume-task.md)。

### 命令用法示例

如果不清楚 DM-worker 的绑定关系，可以通过 `dmctl --master-addr <master-addr> list-member --worker` 查看。

{{< copyable "" >}}

```bash
list-member --worker
```

```
{
    "result": true,
    "msg": "",
    "members": [
        {
            "worker": {
                "msg": "",
                "workers": [
                    {
                        "name": "dm-worker-1",
                        "addr": "127.0.0.1:8262",
                        "stage": "bound",
                        "source": "mysql-replica-01"
                    },
                    {
                        "name": "dm-worker-2",
                        "addr": "127.0.0.1:8263",
                        "stage": "free",
                        "source": ""
                    }
                ]
            }
        }
    ]
}
```

在本示例中 `mysql-replica-01` 绑定到了 `dm-worker-1` 上。使用如下命令可以将该数据源绑定到 `dm-worker-2` 上

{{< copyable "" >}}

```bash
transfer-source mysql-replica-01 dm-worker-2
```

```
{
    "result": true,
    "msg": ""
}
```

再次通过 `dmctl --master-addr <master-addr> list-member --worker` 查看，检查命令已生效。

{{< copyable "" >}}

```bash
list-member --worker
```

```
{
    "result": true,
    "msg": "",
    "members": [
        {
            "worker": {
                "msg": "",
                "workers": [
                    {
                        "name": "dm-worker-1",
                        "addr": "127.0.0.1:8262",
                        "stage": "free",
                        "source": ""
                    },
                    {
                        "name": "dm-worker-2",
                        "addr": "127.0.0.1:8263",
                        "stage": "bound",
                        "source": "mysql-replica-01"
                    }
                ]
            }
        }
    ]
}
```
