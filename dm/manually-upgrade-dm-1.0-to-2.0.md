---
title: TiDB Data Migration 1.0.x 到 2.0+ 手动升级
summary: 了解如何从 TiDB Data Migration 1.0.x 手动升级到 2.0+。
---

# TiDB Data Migration 1.0.x 到 2.0+ 手动升级

本文档主要介绍如何手动从 DM v1.0.x 升级到 v2.0+，主要思路为利用 v1.0.x 时的全局 checkpoint 信息在 v2.0+ 集群中启动一个新的增量数据复制任务。

> **注意：**
>
> - DM 当前不支持在数据迁移任务处于全量导出或全量导入过程中从 v1.0.x 升级到 v2.0+。
> - 由于 DM 各组件间用于交互的 gRPC 协议进行了较大变更，因此需确保升级前后 DM 集群各组件（包括 dmctl）使用相同的版本。
> - 由于 DM 集群的元数据存储（如 checkpoint、shard DDL lock 状态及 online DDL 元信息等）发生了较大变更，升级到 v2.0+ 后无法自动复用 v1.0.x 的元数据，因此在执行升级操作前需要确保：
>     - 所有数据迁移任务不处于 shard DDL 协调过程中。
>     - 所有数据迁移任务不处于 online DDL 协调过程中。

下面是手动升级的具体步骤。

## 第 1 步：准备 v2.0+ 的配置文件

准备的 v2.0+ 的配置文件包括上游数据库的配置文件以及数据迁移任务的配置文件。

### 上游数据库配置文件

在 v2.0+ 中将[上游数据库 source 相关的配置](/dm/dm-source-configuration-file.md)从 DM-worker 的进程配置中独立了出来，因此需要根据 [v1.0.x 的 DM-worker 配置](/dm/dm-worker-configuration-file.md)拆分得到 source 配置。

> **注意：**
>
> 当前从 v1.0.x 升级到 v2.0+ 时，如在 source 配置中启用了 `enable-gtid`，则后续需要通过解析 binlog 或 relay log 文件获取 binlog position 对应的 GTID sets。

#### 从 DM-Ansible 部署的 v1.0.x 升级

如果 v1.0.x 是使用 DM-Ansible 部署的，且假设在 `inventory.ini` 中有如下 `dm_worker_servers` 配置：

```ini
[dm_master_servers]
dm_worker1 ansible_host=172.16.10.72 server_id=101 source_id="mysql-replica-01" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
dm_worker2 ansible_host=172.16.10.73 server_id=102 source_id="mysql-replica-02" mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

则可以转换得到如下两个 source 配置文件：

```yaml
# 原 dm_worker1 对应的 source 配置，如命名为 source1.yaml
server-id: 101                                   # 对应原 `server_id`
source-id: "mysql-replica-01"                    # 对应原 `source_id`
from:
  host: "172.16.10.81"                           # 对应原 `mysql_host`
  port: 3306                                     # 对应原 `mysql_port`
  user: "root"                                   # 对应原 `mysql_user`
  password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="   # 对应原 `mysql_password`
```

```yaml
# 原 dm_worker2 对应的 source 配置，如命名为 source2.yaml
server-id: 102                                   # 对应原 `server_id`
source-id: "mysql-replica-02"                    # 对应原 `source_id`
from:
  host: "172.16.10.82"                           # 对应原 `mysql_host`
  port: 3306                                     # 对应原 `mysql_port`
  user: "root"                                   # 对应原 `mysql_user`
  password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="   # 对应原 `mysql_password`
```

#### 从 Binary 部署的 v1.0.x 升级

如果 v1.0.x 是使用 Binary 部署的，且对应的 DM-worker 配置如下：

```toml
log-level = "info"
log-file = "dm-worker.log"
worker-addr = ":8262"

server-id = 101
source-id = "mysql-replica-01"
flavor = "mysql"

[from]
host = "172.16.10.81"
user = "root"
password = "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="
port = 3306
```

则可转换得到如下的一个 source 配置文件：

```yaml
server-id: 101                                   # 对应原 `server-id`
source-id: "mysql-replica-01"                    # 对应原 `source-id`
flavor: "mysql"                                  # 对应原 `flavor`
from:
  host: "172.16.10.81"                           # 对应原 `from.host`
  port: 3306                                     # 对应原 `from.port`
  user: "root"                                   # 对应原 `from.user`
  password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="   # 对应原 `from.password`
```

### 数据迁移任务配置文件

对于[数据迁移任务配置向导](/dm/dm-task-configuration-guide.md)，v2.0+ 基本与 v1.0.x 保持兼容，可直接复制 v1.0.x 的配置。

## 第 2 步：部署 v2.0+ 集群

> **注意：**
>
> 如果已有其他可用的 v2.0+ 集群，可跳过此步。

[使用 TiUP](/dm/deploy-a-dm-cluster-using-tiup.md) 按所需要节点数部署新的 v2.0+ 集群。

## 第 3 步：下线 v1.0.x 集群

如果原 v1.0.x 集群是使用 DM-Ansible 部署的，则[使用 DM-Ansible 下线 v1.0.x 集群](https://docs.pingcap.com/zh/tidb-data-migration/v1.0/cluster-operations#下线集群)。

如果原 v1.0.x 集群是使用 Binary 部署，则直接停止 DM-worker 与 DM-master 进程。

## 第 4 步：升级数据迁移任务

1. 使用 [`operate-source`](/dm/dm-manage-source.md#数据源操作) 命令将[准备 v2.0+ 的配置文件](#第-1-步准备-v20-的配置文件)中得到的上游数据库 source 配置加载到 v2.0+ 集群中。

2. 在下游 TiDB 中，从 v1.0.x 的数据复制任务对应的增量 checkpoint 表中获取对应的全局 checkpoint 信息。

    - 假设 v1.0.x 的数据迁移配置中未额外指定 `meta-schema`（或指定其值为默认的`dm_meta`），且对应的任务名为 `task_v1`，则对应的 checkpoint 信息在下游 TiDB 的 ``` `dm_meta`.`task_v1_syncer_checkpoint` ``` 表中。
    - 使用以下 SQL 语句分别获取该数据迁移任务对应的所有上游数据库 source 的全局 checkpoint 信息。

        ```sql
        > SELECT `id`, `binlog_name`, `binlog_pos` FROM `dm_meta`.`task_v1_syncer_checkpoint` WHERE `is_global`=1;
        +------------------+-------------------------+------------+
        | id               | binlog_name             | binlog_pos |
        +------------------+-------------------------+------------+
        | mysql-replica-01 | mysql-bin|000001.000123 | 15847      |
        | mysql-replica-02 | mysql-bin|000001.000456 | 10485      |
        +------------------+-------------------------+------------+
        ```

3. 更新 v1.0.x 的数据迁移任务配置文件以启动新的 v2.0+ 数据迁移任务。

    - 如 v1.0.x 的数据迁移任务配置文件为 `task_v1.yaml`，则将其复制一份为 `task_v2.yaml`。
    - 对 `task_v2.yaml` 进行以下修改：
        - 将 `name` 修改为一个新的、不存在的名称，如 `task_v2`
        - 将 `task-mode` 修改为 `incremental`
        - 根据 step.2 中获取的全局 checkpoint 信息，为各 source 设置增量复制的起始点，如：

            ```yaml
            mysql-instances:
              - source-id: "mysql-replica-01"        # 对应 checkpoint 信息所属的 `id`
                meta:
                  binlog-name: "mysql-bin.000123"    # 对应 checkpoint 信息中的 `binlog_name`，但不包含 `|000001` 部分
                  binlog-pos: 15847                  # 对应 checkpoint 信息中的 `binlog_pos`

              - source-id: "mysql-replica-02"
                meta:
                  binlog-name: "mysql-bin.000456"
                  binlog-pos: 10485
            ```

            > **注意：**
            >
            > 如在 source 配置中启动了 `enable-gtid`，当前需要通过解析 binlog 或 relay log 文件获取 binlog position 对应的 GTID sets 并在 `meta` 中设置为 `binlog-gtid`。

4. 使用 [`start-task`](/dm/dm-create-task.md) 命令以 v2.0+ 的数据迁移任务配置文件启动升级后的数据迁移任务。

5. 使用 [`query-status`](/dm/dm-query-status.md) 命令确认数据迁移任务是否运行正常。

如果数据迁移任务运行正常，则表明 DM 升级到 v2.0+ 的操作成功。
