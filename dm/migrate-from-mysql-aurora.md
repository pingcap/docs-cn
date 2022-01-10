---
title: 从兼容 MySQL 的数据库迁移数据——以 Amazon Aurora MySQL 为例
summary: 使用 DM 从 MySQL/Amazon Aurora MySQL 迁移数据。
aliases: ['/docs-cn/tidb-data-migration/dev/migrate-from-mysql-aurora/']
---

# 从兼容 MySQL 的数据库迁移数据——以 Amazon Aurora MySQL 为例

本文以 [Amazon Aurora MySQL](https://aws.amazon.com/cn/rds/aurora/details/mysql-details/) 为例介绍如何使用 DM 从 MySQL 兼容的数据库迁移数据到 TiDB。

示例使用的 Aurora 集群信息如下：

| 集群 | 终端节点 | 端口 | 角色 | 版本 |
|:-------- |:--- | :--- | :--- |:---|
| Aurora-1 | test-dm-2-0.cluster-czrtqco96yc6.us-east-2.rds.amazonaws.com | 3306 | 写入器 | Aurora (MySQL)-5.7.12 |
| Aurora-1 | test-dm-2-0.cluster-ro-czrtqco96yc6.us-east-2.rds.amazonaws.com | 3306 | 读取器 | Aurora (MySQL)-5.7.12 |
| Aurora-2 | test-dm-2-0-2.cluster-czrtqco96yc6.us-east-2.rds.amazonaws.com | 3306 | 写入器 | Aurora (MySQL)-5.7.12 |
| Aurora-2 | test-dm-2-0-2.cluster-ro-czrtqco96yc6.us-east-2.rds.amazonaws.com | 3306 | 读取器 | Aurora (MySQL)-5.7.12 |

Aurora 集群数据与迁移计划如下：

| 集群 | 数据库 | 表 | 是否迁移 |
|:---- |:---- | :--- | :--- |
| Aurora-1 | migrate_me | t1 | 是 |
| Aurora-1 | ignore_me | ignore_table | 否 |
| Aurora-2 | migrate_me | t2 | 是 |
| Aurora-2 | ignore_me | ignore_table | 否 |

迁移使用的 Aurora 集群用户如下：

| 集群 | 用户 | 密码 |
|:---- |:---- | :--- |
| Aurora-1 | root | 12345678 |
| Aurora-2 | root | 12345678 |

示例使用的 TiDB 集群信息如下。该集群使用 [TiDB Cloud](https://tidbcloud.com/) 服务一键部署：

| 节点 | 端口 | 版本 |
|:--- | :--- | :--- |
| tidb.6657c286.23110bc6.us-east-1.prod.aws.tidbcloud.com | 4000 | v4.0.2 |

迁移使用的 TiDB 集群用户如下：

| 用户 | 密码 |
|:---- | :--- |
| root | 87654321 |

预期迁移后，TiDB 集群中存在表``` `migrate_me`.`t1` ```与``` `migrate_me`.`t2` ```，其中数据与 Aurora 集群一致。

> **注意：**
>
> 本次迁移不涉及合库合表，如需使用合库合表，参见 [DM 合库合表场景](/dm/scenarios.md#合库合表场景)。

## 第 1 步：数据迁移前置条件

为了保证迁移成功，在开始迁移之前需要进行前置条件的检查。本文在此列出了需要的检查以及与 DM、Aurora 组件相关的解决方案。

### DM 部署节点

DM 作为数据迁移的核心，需要正常连接上游 Aurora 集群与下游 TiDB 集群，因此通过 MySQL client 等方式检查部署 DM 的节点是否能连通上下游。除此以外，关于 DM 节点数目、软硬件等要求，参见 [DM 集群软硬件环境需求](/dm/dm-hardware-and-software-requirements.md)。

### Aurora

DM 在增量复制阶段依赖 `ROW` 格式的 binlog，参见[为 Aurora 实例启用 binlog](https://aws.amazon.com/cn/premiumsupport/knowledge-center/enable-binary-logging-aurora/) 进行配置。

如果 Aurora 已开启了 GTID，则可以基于 GTID 进行数据迁移。GTID 的启用方式参见[为 Aurora 集群启用 GTID 支持](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/AuroraUserGuide/mysql-replication-gtid.html#mysql-replication-gtid.configuring-aurora)。基于 GTID 进行数据迁移，需要将第 3 步数据源配置文件中的 `enable-gtid` 设置为 `true`。

> **注意：**
>
> + 基于 GTID 进行数据迁移需要 MySQL 5.7 (Aurora 2.04) 或更高版本。
> + 除上述 Aurora 特有配置以外，上游数据库需满足迁移 MySQL 的其他要求，例如表结构、字符集、权限等，参见[上游 MySQL 实例检查内容](/dm/dm-precheck.md#检查内容)。

## 第 2 步：部署 DM 集群

DM 可以通过多种方式进行部署，目前推荐使用 TiUP 部署 DM 集群。具体部署方法，参见[使用 TiUP 部署 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)。示例有两个数据源，因此需要至少部署两个 DM-worker 节点。

部署完成后，需要记录任意一台 DM-master 节点的 IP 和服务端口（默认为 `8261`），以供 `dmctl` 连接。本示例使用 `127.0.0.1:8261`。通过 TiUP 使用 `dmctl` 检查 DM 状态：

> **注意：**
>
> 使用其他方式部署 DM 可以用类似的方式调用 `dmctl`，参见 [dmctl 简介](/dm/dmctl-introduction.md)。

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 list-member
```

返回值中的 `master` 与 `worker` 与部署数目一致：

```bash
{
    "result": true,
    "msg": "",
    "members": [
        {
            "leader": {
                ...
            }
        },
        {
            "master": {
                "msg": "",
                "masters": [
                    ...
                ]
            }
        },
        {
            "worker": {
                "msg": "",
                "workers": [
                    ...
                ]
            }
        }
    ]
}
```

## 第 3 步：配置数据源

> **注意：**
>
> DM 所使用的配置文件支持明文或密文数据库密码，推荐使用密文数据库密码确保安全。如何获得密文数据库密码，参见[使用 dmctl 加密数据库密码](/dm/dm-manage-source.md#加密数据库密码)。

根据示例信息保存如下的数据源配置文件，其中 `source-id` 的值将在第 4 步配置任务时被引用。

文件 `source1.yaml`：

```yaml
# Aurora-1
source-id: "aurora-replica-01"

# 基于 GTID 进行数据迁移时，需要将该项设置为 true
enable-gtid: false

from:
  host: "test-dm-2-0.cluster-czrtqco96yc6.us-east-2.rds.amazonaws.com"
  user: "root"
  password: "12345678"
  port: 3306
```

文件 `source2.yaml`：

```yaml
# Aurora-2
source-id: "aurora-replica-02"

enable-gtid: false

from:
  host: "test-dm-2-0-2.cluster-czrtqco96yc6.us-east-2.rds.amazonaws.com"
  user: "root"
  password: "12345678"
  port: 3306
```

参见[使用 DM 迁移数据：创建数据源](/dm/migrate-data-using-dm.md#第-3-步创建数据源)，通过 TiUP 使用 `dmctl` 添加两个数据源。

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 operate-source create dm-test/source1.yaml
tiup dmctl --master-addr 127.0.0.1:8261 operate-source create dm-test/source2.yaml
```

添加数据源成功时，每个数据源的返回信息中包含了一个与之绑定的 DM-worker。

```bash
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "aurora-replica-01",
            "worker": "one-dm-worker-ID"
        }
    ]
}
```

## 第 4 步：配置任务

> **注意：**
>
> 由于 Aurora 不支持 FTWRL，仅使用全量模式导出数据时需要暂停写入，参见 [AWS 官网说明](https://aws.amazon.com/cn/premiumsupport/knowledge-center/mysqldump-error-rds-mysql-mariadb/)。在示例的全量+增量模式下，DM 将自动启用 [`safe mode`](/dm/dm-glossary.md#safe-mode) 解决这一问题。在其他模式下如需保证数据一致，参见 [AWS 官网说明](https://aws.amazon.com/cn/premiumsupport/knowledge-center/mysqldump-error-rds-mysql-mariadb/)操作。

本示例选择迁移 Aurora 已有数据并将新增数据实时迁移给 TiDB，即**全量+增量**模式。根据上文的 TiDB 集群信息、已添加的 `source-id`、要迁移的表，保存如下任务配置文件 `task.yaml`：

```yaml
# 任务名，多个同时运行的任务不能重名
name: "test"
# 全量+增量 (all) 迁移模式
task-mode: "all"
# 下游 TiDB 配置信息
target-database:
  host: "tidb.6657c286.23110bc6.us-east-1.prod.aws.tidbcloud.com"
  port: 4000
  user: "root"
  password: "87654321"

# 当前数据迁移任务需要的全部上游 MySQL 实例配置
mysql-instances:
- source-id: "aurora-replica-01"
  # 需要迁移的库名或表名的黑白名单的配置项名称，用于引用全局的黑白名单配置，全局配置见下面的 `block-allow-list` 的配置
  block-allow-list: "global"
  mydumper-config-name: "global"

- source-id: "aurora-replica-02"
  block-allow-list: "global"
  mydumper-config-name: "global"

# 黑白名单配置
block-allow-list:
  global:                             # 被上文 block-allow-list: "global" 引用
    do-dbs: ["migrate_me"]            # 需要迁移的上游数据库白名单。白名单以外的库表不会被迁移

# Dump 单元配置
mydumpers:
  global:                             # 被上文 mydumper-config-name: "global" 引用
    extra-args: "--consistency none"  # Aurora 不支持 FTWRL，配置此项以绕过
```

## 第 5 步：启动任务

通过 TiUP 使用 `dmctl` 启动任务。

> **注意：**
>
> 目前通过 TiUP 使用 `dmctl` 时，需要使用 `task.yaml` 绝对路径。TiUP 将会在后续更新中正确支持相对路径。

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 start-task /absolute/path/to/task.yaml --remove-meta
```

启动成功时的返回信息是：

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "aurora-replica-01",
            "worker": "one-dm-worker-ID"
        },
        {
            "result": true,
            "msg": "",
            "source": "aurora-replica-02",
            "worker": "another-dm-worker-ID"
        }
    ]
}
```

如果返回信息中有 `source db replication privilege checker`、`source db dump privilege checker` 错误，请检查 `errorMsg` 字段是否存在不能识别的权限。例如：

```
line 1 column 287 near \"INVOKE LAMBDA ON *.* TO...
```

以上返回信息说明 `INVOKE LAMBDA` 权限导致报错。如果该权限是 Aurora 特有的，请在配置文件中添加如下内容跳过检查。DM 会在版本更新中增强对 Aurora 权限的自动处理。

```
ignore-checking-items: ["replication_privilege","dump_privilege"]
```

## 第 6 步：查询任务并验证数据

通过 TiUP 使用 `dmctl` 查询正在运行的迁移任务及任务状态等信息。

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 query-status
```

任务正常运行的返回信息是：

```
{
    "result": true,
    "msg": "",
    "tasks": [
        {
            "taskName": "test",
            "taskStatus": "Running",
            "sources": [
                "aurora-replica-01",
                "aurora-replica-02"
            ]
        }
    ]
}
```

用户也可以在下游查询数据，在 Aurora 中修改数据并验证到 TiDB 的数据复制。
