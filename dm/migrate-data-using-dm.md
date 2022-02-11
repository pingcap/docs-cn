---
title: 使用 DM 迁移数据
---

# 使用 DM 迁移数据

本文介绍如何使用 DM 工具迁移数据。

## 第 1 步：部署 DM 集群

推荐[使用 TiUP 部署 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)；也可以[使用 binary 部署 DM 集群](/dm/deploy-a-dm-cluster-using-binary.md)用于体验或测试。

> **注意：**
>
> - 在 DM 所有的配置文件中，对于数据库密码推荐使用 dmctl 加密后的密文。如果数据库密码为空，则不需要加密。关于如何使用 dmctl 加密明文密码，参考[使用 dmctl 加密数据库密码](/dm/dm-manage-source.md#加密数据库密码)。
> - 上下游数据库用户必须拥有相应的读写权限。

## 第 2 步：检查集群信息

使用 TiUP 部署 DM 集群后，相关配置信息如下：

- DM 集群相关组件配置信息

    | 组件 | 主机 | 端口 |
    |:------|:---- |:---- |
    | dm_worker1 | 172.16.10.72 | 8262 |
    | dm_worker2 | 172.16.10.73 | 8262 |
    | dm_master | 172.16.10.71 | 8261 |

- 上下游数据库实例相关信息

    | 数据库实例 | 主机 | 端口 | 用户名 | 加密密码 |
    |:-------- |:--- | :--- | :--- | :--- |
    | 上游 MySQL-1 | 172.16.10.81 | 3306 | root | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | 上游 MySQL-2 | 172.16.10.82 | 3306 | root | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | 下游 TiDB | 172.16.10.83 | 4000 | root | |

上游 MySQL 数据库实例用户所需权限参见[上游 MySQL 实例配置前置检查](/dm/dm-precheck.md)介绍。

## 第 3 步：创建数据源

1. 将 MySQL-1 的相关信息写入到 `conf/source1.yaml` 中：

    ```yaml
    # MySQL1 Configuration.

    source-id: "mysql-replica-01"

    # DM-worker 是否使用全局事务标识符 (GTID) 拉取 binlog。使用前提是在上游 MySQL 已开启 GTID 模式。
    enable-gtid: false

    from:
      host: "172.16.10.81"
      user: "root"
      password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="
      port: 3306
    ```

2. 在终端中执行下面的命令，使用 `tiup dmctl` 将 MySQL-1 的数据源配置加载到 DM 集群中：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup dmctl --master-addr 172.16.10.71:8261 operate-source create conf/source1.yaml
    ```

3. 对于 MySQL-2，修改配置文件中的相关信息，并执行相同的 dmctl 命令。

## 第 4 步：配置任务

假设需要将 MySQL-1 和 MySQL-2 实例的 `test_db` 库的 `test_table` 表以**全量+增量**的模式迁移到下游 TiDB 的 `test_db` 库的 `test_table` 表。

编辑任务配置文件 `task.yaml`：

```yaml
# 任务名，多个同时运行的任务不能重名。
name: "test"
# 全量+增量 (all) 迁移模式。
task-mode: "all"
# 下游 TiDB 配置信息。
target-database:
  host: "172.16.10.83"
  port: 4000
  user: "root"
  password: ""

# 当前数据迁移任务需要的全部上游 MySQL 实例配置。
mysql-instances:
-
  # 上游实例或者复制组 ID，参考 `inventory.ini` 的 `source_id` 或者 `dm-master.toml` 的 `source-id 配置`。
  source-id: "mysql-replica-01"
  # 需要迁移的库名或表名的黑白名单的配置项名称，用于引用全局的黑白名单配置，全局配置见下面的 `block-allow-list` 的配置。
  block-allow-list: "global"          # 如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list。
  # dump 处理单元的配置项名称，用于引用全局的 dump 处理单元配置。
  mydumper-config-name: "global"

-
  source-id: "mysql-replica-02"
  block-allow-list: "global"          # 如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list。
  mydumper-config-name: "global"

# 黑白名单全局配置，各实例通过配置项名引用。
block-allow-list:                     # 如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list。
  global:
    do-tables:                        # 需要迁移的上游表的白名单。
    - db-name: "test_db"              # 需要迁移的表的库名。
      tbl-name: "test_table"          # 需要迁移的表的名称。

# dump 处理单元全局配置，各实例通过配置项名引用。
mydumpers:
  global:
    extra-args: ""
```

## 第 5 步：启动任务

为了提前发现数据迁移任务的一些配置错误，DM 中增加了[前置检查](/dm/dm-precheck.md)功能：

- 启动数据迁移任务时，DM 自动检查相应的权限和配置。
- 也可使用 `check-task` 命令手动前置检查上游的 MySQL 实例配置是否符合 DM 的配置要求。

> **注意：**
>
> 第一次启动数据迁移任务时，必须确保上游数据库已配置。否则，启动任务时会报错。

使用 `tiup dmctl` 执行以下命令启动数据迁移任务。其中，`task.yaml` 是之前编辑的配置文件。

{{< copyable "" >}}

```bash
tiup dmctl --master-addr 172.16.10.71:8261 start-task ./task.yaml
```

- 如果执行该命令后返回的结果如下，则表明任务已成功启动。

    ```json
    {
        "result": true,
        "msg": "",
        "workers": [
            {
                "result": true,
                "worker": "172.16.10.72:8262",
                "msg": ""
            },
            {
                "result": true,
                "worker": "172.16.10.73:8262",
                "msg": ""
            }
        ]
    }
    ```

- 如果任务启动失败，可根据返回结果的提示进行配置变更后执行 `start-task task.yaml` 命令重新启动任务。

## 第 6 步：查询任务

如需了解 DM 集群中是否存在正在运行的迁移任务及任务状态等信息，可使用 `tiup dmctl` 执行以下命令进行查询：

{{< copyable "" >}}

```bash
tiup dmctl --master-addr 172.16.10.71:8261 query-status
```

## 第 7 步：停止任务

如果不再需要进行数据迁移，可以使用 `tiup dmctl` 执行以下命令停止迁移任务：

{{< copyable "" >}}

```bash
tiup dmctl --master-addr 172.16.10.71:8261 stop-task test
```

其中的 `test` 是 `task.yaml` 配置文件中 `name` 配置项设置的任务名。

## 第 8 步：监控任务与查看日志

如果使用 TiUP 部署 DM 集群时，正确部署了 Prometheus、Alertmanager 与 Grafana，且其地址均为 `172.16.10.71`。可在浏览器中打开 <http://172.16.10.71:9093> 进入 Alertmanager 查看 DM 告警信息；可在浏览器中打开 <http://172.16.10.71:3000> 进入 Grafana，选择 DM 的 dashboard 查看 DM 相关监控项。

DM 在运行过程中，DM-worker, DM-master 及 dmctl 都会通过日志输出相关信息。各组件的日志目录如下：

- DM-master 日志目录：通过 DM-master 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录位于 `{log_dir}`。
- DM-worker 日志目录：通过 DM-worker 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录位于 `{log_dir}`。
