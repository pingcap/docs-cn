---
title: 从 Amazon Aurora MySQL 迁移数据
summary: 使用 DM 从 Amazon Aurora MySQL 迁移数据。
category: how-to
---

# 从 Amazon Aurora MySQL 迁移数据

本文介绍如何使用 DM 从 [Amazon Aurora MySQL](https://aws.amazon.com/cn/rds/aurora/details/mysql-details/) 迁移数据到 TiDB。

## 第 1 步：在 Aurora 集群中启用 binlog

假设有两个 Aurora 集群需要迁移数据到 TiDB，其集群信息如下，其中 Aurora-1 包含一个独立的读取器节点。

| 集群 | 终端节点 | 端口 | 角色 |
|:-------- |:--- | :--- | :--- |
| Aurora-1 | pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | 写入器 |
| Aurora-1 | pingcap-1-us-east-2a.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | 读取器 |
| Aurora-2 | pingcap-2.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | 写入器 |

DM 在增量同步阶段依赖 `ROW` 格式的 binlog，如果未启用 binlog 及设置正确的 binlog 格式，则不能正常使用 DM 进行数据同步，具体可参见[检查内容](v2.1/reference/tools/data-migration/precheck.md#检查内容)。

> **注意：**
>
> Aurora 读取器不能开启 binlog，因此不能作为 DM 数据迁移时的上游 master server。

如果需要基于 GTID 进行数据迁移，还需要为 Aurora 集群启用 GTID 支持。

> **注意：**
>
> 基于 GTID 的数据迁移需要 MySQL 5.7 (Aurora 2.04.1) 或更高版本。

### 为 Aurora 集群修改 binlog 相关参数

在 Aurora 集群中，binlog 相关参数是**集群参数组中的集群级参数**，有关如何为 Aurora 集群启用 binlog 支持，请参考[在复制主实例上启用二进制日志记录](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Replication.MySQL.html#AuroraMySQL.Replication.MySQL.EnableBinlog)。在使用 DM 进行数据迁移时，需要将 `binlog_format` 参数设置为 `ROW`。

如果需要基于 GTID 进行数据迁移，需要将 `gtid-mode` 与 `enforce_gtid_consistency` 均设置为 `ON`。有关如何为 Aurora 集群启用基于 GTID 的数据迁移支持，请参考 [Configuring GTID-Based Replication for an Aurora MySQL Cluster](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/AuroraUserGuide/mysql-replication-gtid.html#mysql-replication-gtid.configuring-aurora)。

> **注意：**
>
> 在 Aurora 管理后台中，`gtid_mode` 参数表示为 `gtid-mode`。

## 第 2 步：部署 DM 集群

目前推荐使用 DM-Ansible 部署 DM 集群，具体部署方法参照[使用 DM-Ansible 部署 DM 集群](v2.1/how-to/deploy/data-migration-with-ansible.md)。

> **注意：**
>
> - 在 DM 所有的配置文件中，数据库的密码要使用 dmctl 加密后的密文。如果数据库密码为空，则不需要加密。关于如何使用 dmctl 加密明文密码，参考[使用 dmctl 加密上游 MySQL 用户密码](v2.1/how-to/deploy/data-migration-with-ansible.md#使用-dmctl-加密上游-mysql-用户密码)。
> - 上下游数据库用户必须拥有相应的读写权限。

## 第 3 步：检查集群信息

使用 DM-Ansible 部署 DM 集群后，相关配置信息如下：

- DM 集群相关组件配置信息

    | 组件 | 主机 | 端口 |
    |:------|:---- |:---- |
    | dm_worker1 | 172.16.10.72 | 8262 |
    | dm_worker2 | 172.16.10.73 | 8262 |
    | dm_master | 172.16.10.71 | 8261 |

- 上下游数据库实例相关信息

    | 数据库实例 | 主机 | 端口 | 用户名 | 加密密码 |
    |:-------- |:--- | :--- | :--- | :--- |
    | 上游 Aurora-1 | pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | root | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | 上游 Aurora-2 | pingcap-2.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | root | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | 下游 TiDB | 172.16.10.83 | 4000 | root | |

- dm-master 进程配置文件 `{ansible deploy}/conf/dm-master.toml` 中的配置

    ```toml
    # Master 配置。

    [[deploy]]
    source-id = "mysql-replica-01"
    dm-worker = "172.16.10.72:8262"

    [[deploy]]
    source-id = "mysql-replica-02"
    dm-worker = "172.16.10.73:8262"
    ```

## 第 4 步：配置任务

假设需要将 Aurora-1 和 Aurora-2 实例的 `test_db` 库的 `test_table` 表以**全量+增量**的模式同步到下游 TiDB 的 `test_db` 库的 `test_table` 表。

复制并编辑 `{ansible deploy}/conf/task.yaml.example`，生成如下任务配置文件 `task.yaml`：

```yaml
# 任务名，多个同时运行的任务不能重名。
name: "test"
# 全量+增量 (all) 同步模式。
task-mode: "all"
# 下游 TiDB 配置信息。
target-database:
  host: "172.16.10.83"
  port: 4000
  user: "root"
  password: ""

# 当前数据同步任务需要的全部上游 MySQL 实例配置。
mysql-instances:
-
  # 上游实例或者复制组 ID，参考 `inventory.ini` 的 `source_id` 或者 `dm-master.toml` 的 `source-id 配置`。
  source-id: "mysql-replica-01"
  # 需要同步的库名或表名的黑白名单的配置项名称，用于引用全局的黑白名单配置，全局配置见下面的 `black-white-list` 的配置。
  black-white-list: "global"
  # Mydumper 的配置项名称，用于引用全局的 Mydumper 配置。
  mydumper-config-name: "global"

-
  source-id: "mysql-replica-02"
  black-white-list: "global"
  mydumper-config-name: "global"

# 黑白名单全局配置，各实例通过配置项名引用。
black-white-list:
  global:
    do-tables:                        # 需要同步的上游表的白名单。
    - db-name: "test_db"              # 需要同步的表的库名。
      tbl-name: "test_table"          # 需要同步的表的名称。

# Mydumper 全局配置，各实例通过配置项名引用。
mydumpers:
  global:
    extra-args: "-B test_db -T test_table"  # 只导出 `test_db` 库中的 `test_table` 表，可设置 Mydumper 的任何参数。
```

## 第 5 步：启动任务

1. 进入 dmctl 目录 `/home/tidb/dm-ansible/resources/bin/`

2. 执行以下命令启动 dmctl

    ```bash
    ./dmctl --master-addr 172.16.10.71:8261
    ```

3. 执行以下命令启动数据同步任务

    ```bash
    # `task.yaml` 是之前编辑的配置文件
    start-task ./task.yaml
    ```

    - 如果执行命令后的返回结果中不包含错误信息，则表明任务已经成功启动
    - 如果包含以下错误信息，则表明上游 Aurora 用户可能拥有 TiDB 不支持的权限类型

        ```json
        {
            "id": 4,
            "name": "source db dump privilege chcker",
            "desc": "check dump privileges of source DB",
            "state": "fail",
            "errorMsg": "line 1 column 285 near \"LOAD FROM S3, SELECT INTO S3 ON *.* TO 'root'@'%' WITH GRANT OPTION\" ...",
            "instruction": "",
            "extra": "address of db instance - pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com"
        },
        {
            "id": 5,
            "name": "source db replication privilege chcker",
            "desc": "check replication privileges of source DB",
            "state": "fail",
            "errorMsg": "line 1 column 285 near \"LOAD FROM S3, SELECT INTO S3 ON *.* TO 'root'@'%' WITH GRANT OPTION\" ...",
            "instruction": "",
            "extra": "address of db instance - pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com"
        }
        ```

        此时可以选择以下两种处理方法中的任意一种进行处理后，再使用 `start-task` 尝试重新启动任务：

        1. 为用于进行数据迁移的 Aurora 用户移除不被 TiDB 支持的不必要的权限
        2. 如果能确保 Aurora 用户拥有 DM 所需要的权限，可以在 `task.yaml` 配置文件中添加如下顶级配置项以跳过启用任务时的前置权限检查

            ```yaml
            ignore-checking-items: ["dump_privilege", "replication_privilege"]
            ```

## 第 6 步：查询任务

如需了解 DM 集群中是否存在正在运行的同步任务及任务状态等信息，可在 dmctl 内使用以下命令进行查询：

```bash
query-status
```

> **注意：**
>
> 如果查询命令的返回结果中包含以下错误信息，则表明在全量同步的 dump 阶段不能获得相应的 lock：
>
>   ```bash
>   Couldn't acquire global lock, snapshots will not be consistent: Access denied for user 'root'@'%' (using password: YES)
>   ```
>
> 此时如果能接受不使用 FTWL 来确保 dump 文件与 metadata 的一致或上游能暂时停止写入，可以通过为 `mydumpers` 下的 `extra-args` 添加 `--no-locks` 参数来进行绕过，具体方法为：
>
> 1. 使用 `stop-task` 停止当前由于不能正常 dump 而已经转为 paused 的任务
> 2. 将原 `task.yaml` 中的 `extra-args: "-B test_db -T test_table"` 更新为 `extra-args: "-B test_db -T test_table --no-locks"`
> 3. 使用 `start-task` 重新启动任务
