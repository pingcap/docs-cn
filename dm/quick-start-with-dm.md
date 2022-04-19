---
title: TiDB Data Migration 快速上手试用
summary: 了解如何快速上手部署试用 TiDB Data Migration 工具。
---

# TiDB Data Migration 快速上手指南

本文介绍如何快速体验使用数据迁移工具 [TiDB Data Migration](https://github.com/pingcap/dm) (DM) 从 MySQL 迁移数据到 TiDB。

如需在生产环境中部署 DM，请参考以下文档：

- [使用 TiUP 部署 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)
- [创建数据源](/dm/quick-start-create-source.md)
- [创建数据迁移任务](/dm/quick-start-create-task)

## 使用样例

在本地部署的 DM 集群组件和访问的 MySQL 和 TiDB 节点的信息如下：

| 实例        | 服务器地址   | 端口使用 |
| :---------- | :----------- | :----------- |
| DM-master  | 127.0.0.1 | 8261, 8291（内部端口） |
| DM-worker  | 127.0.0.1 | 8262 |
| MySQL-3306 | 127.0.0.1 | 3306 |
| TiDB       | 127.0.0.1 | 4000 |

## 使用 binary 包部署 DM

### 准备 DM binary 包

首先需要下载 DM 最新的 binary 或者手动编译。

#### 第一种方式：下载最新 DM binary 包

{{< copyable "shell-regular" >}}

```bash
wget http://download.pingcap.org/dm-nightly-linux-amd64.tar.gz
tar -xzvf dm-nightly-linux-amd64.tar.gz
cd dm-nightly-linux-amd64
```

#### 第二种方式：编译最新 DM binary 包

{{< copyable "shell-regular" >}}

```bash
git clone https://github.com/pingcap/dm.git
cd dm
make
```

### 部署 DM-master

执行如下命令启动 DM-master：

{{< copyable "shell-regular" >}}

```bash
nohup bin/dm-master --master-addr='127.0.0.1:8261' --log-file=/tmp/dm-master.log --name="master1" >> /tmp/dm-master.log 2>&1 &
```

### 部署 DM-worker

执行如下命令启动 DM-worker：

{{< copyable "shell-regular" >}}

```bash
nohup bin/dm-worker --worker-addr='127.0.0.1:8262' --log-file=/tmp/dm-worker.log --join='127.0.0.1:8261' --name="worker1" >> /tmp/dm-worker.log 2>&1 &
```

### 检查 DM 集群部署是否正常

{{< copyable "shell-regular" >}}

```bash
bin/dmctl --master-addr=127.0.0.1:8261 list-member
```

一个正常 DM 集群的范例返回结果如下所示：

```bash
{
    "result": true,
    "msg": "",
    "members": [
        {
            "leader": {
                "msg": "",
                "name": "master1",
                "addr": "127.0.0.1:8261"
            }
        },
        {
            "master": {
                "msg": "",
                "masters": [
                    {
                        "name": "master1",
                        "memberID": "11007177379717700053",
                        "alive": true,
                        "peerURLs": [
                            "http://127.0.0.1:8291"
                        ],
                        "clientURLs": [
                            "http://127.0.0.1:8261"
                        ]
                    }
                ]
            }
        },
        {
            "worker": {
                "msg": "",
                "workers": [
                    {
                        "name": "worker1",
                        "addr": "127.0.0.1:8262",
                        "stage": "free",
                        "source": ""
                    }
                ]
            }
        }
    ]
}
```

## 从 MySQL 同步数据到 TiDB

### 准备数据

使用 DM 之前，先准备好数据，向 MySQL-3306 写入示例数据。

{{< copyable "sql" >}}

```sql
drop database if exists `testdm`;
create database `testdm`;
use `testdm`;
create table t1 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
insert into t1 (id, uid, name) values (1, 10001, 'Gabriel García Márquez'), (2, 10002, 'Cien años de soledad');
insert into t2 (id, uid, name) values (3, 20001, 'José Arcadio Buendía'), (4, 20002, 'Úrsula Iguarán'), (5, 20003, 'José Arcadio');
```

### 加载数据源 MySQL 配置

运行数据迁移任务前，需要加载数据源的配置，也就是 MySQL 的相关设置，到 DM。

#### 对数据源 MySQL 访问密码进行加密

> **注意：**
>
> + 如果数据源没有设置密码，则可以跳过该步骤。
> + 自 v2.0 起，DM 可以使用明文密码配置数据源的访问密码信息。

为了安全，可配置及使用加密后的 MySQL 访问密码，以密码为 "123456" 为例：

{{< copyable "shell-regular" >}}

```bash
./bin/dmctl --encrypt "123456"
```

```
fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg=
```

记录该加密后的密码，用于下面新建 MySQL 数据源。

#### 编写数据源 MySQL 配置

把以下配置文件内容写入到 `mysql-source-conf.yaml` 中。

MySQL1 的配置文件：

```yaml
# MySQL Configuration.

source-id: "mysql-replica-01"

from:
  host: "127.0.0.1"
  user: "root"
  password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
  port: 3306
```

#### 加载数据源 MySQL 配置

在终端中执行下面的命令，使用 dmctl 将 MySQL 的数据源配置加载到 DM 集群中：

{{< copyable "shell-regular" >}}

```bash
./bin/dmctl --master-addr=127.0.0.1:8261 operate-source create mysql-source-conf.yaml
```

结果如下：

```bash
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

这样就成功将 MySQL-3306 数据源添加到了 DM 集群。

### 创建数据迁移任务

在导入[准备数据](#准备数据)后，进行以下操作将 MySQL 的 `testdm`.`t1` 和 `testdm`.`t2` 两张表迁移到 TiDB。

1. 创建任务的配置文件 `testdm-task.yaml`：

    {{< copyable "" >}}

    ```yaml
    ---
    name: testdm
    task-mode: all

    target-database:
      host: "127.0.0.1"
      port: 4000
      user: "root"
      password: "" # 如果密码不为空，则推荐使用经过 dmctl 加密的密文

    mysql-instances:
      - source-id: "mysql-replica-01"
        block-allow-list:  "ba-rule1"

    block-allow-list:
      ba-rule1:
        do-dbs: ["testdm"]
    ```

2. 使用 dmctl 创建任务：

    {{< copyable "shell-regular" >}}

    ```bash
    ./bin/dmctl --master-addr 127.0.0.1:8261 start-task testdm-task.yaml
    ```

    结果如下：

    ```bash
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

这样就成功创建了一个将 MySQL-3306 数据迁移到 TiDB 的任务。

### 查看迁移任务状态

在创建迁移任务之后，可以用 `dmtcl query-status` 来查看任务的状态。

{{< copyable "shell-regular" >}}

```bash
./bin/dmctl --master-addr 127.0.0.1:8261 query-status
```

结果如下：

```bash
{
    "result": true,
    "msg": "",
    "tasks": [
        {
            "taskName": "testdm",
            "taskStatus": "Running",
            "sources": [
                "mysql-replica-01"
            ]
        }
    ]
}
```
