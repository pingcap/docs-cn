---
title: 从小数据量 MySQL 迁移数据到 TiDB
summary: 介绍如何从小数据量 MySQL 迁移数据到 TiDB。
aliases: ['/zh/tidb/dev/usage-scenario-incremental-migration/']
---

# 从小数据量 MySQL 迁移数据到 TiDB

本文档介绍如何使用 TiDB DM （以下简称 DM）以全量+增量的模式数据到 TiDB。本文所称“小数据量”通常指 TiB 级别以下。

一般而言，受到表结构索引数目等信息、硬件以及网络环境影响，迁移速率在 30～50GB/h 不等。使用 TiDB DM 迁移的流程如下图所示。

![dm](/media/dm/migrate-with-dm.png)

## 前提条件

- [使用 TiUP 安装 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)
- [DM 所需上下游数据库权限](/dm/dm-worker-intro.md)

## 第 1 步：创建数据源

首先，新建 `source1.yaml` 文件, 写入以下内容：

{{< copyable "" >}}

```yaml
# 唯一命名，不可重复。
source-id: "mysql-01"

# DM-worker 是否使用全局事务标识符 (GTID) 拉取 binlog。使用前提是上游 MySQL 已开启 GTID 模式。若上游存在主从自动切换，则必须使用 GTID 模式。
enable-gtid: true

from:
  host: "${host}"         # 例如：172.16.10.81
  user: "root"
  password: "${password}" # 支持但不推荐使用明文密码，建议使用 dmctl encrypt 对明文密码进行加密后使用
  port: 3306
```

其次，在终端中执行下面的命令后，使用 `tiup dmctl` 将数据源配置加载到 DM 集群中:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

该命令中的参数描述如下：

|参数           |描述|
|-              |-|
|`--master-addr`  |`dmctl` 要连接的集群的任意 DM-master 节点的 {advertise-addr}，例如：172.16.10.71:8261|
|`operate-source create` |向 DM 集群加载数据源|

## 第 2 步：创建迁移任务

新建 `task1.yaml` 文件, 写入以下内容：

{{< copyable "" >}}

```yaml
# 任务名，多个同时运行的任务不能重名。
name: "test"
# 任务模式，可设为
# full：只进行全量数据迁移
# incremental： binlog 实时同步
# all： 全量 + binlog 迁移
task-mode: "all"
# 下游 TiDB 配置信息。
target-database:
  host: "${host}"                   # 例如：172.16.10.83
  port: 4000
  user: "root"
  password: "${password}"           # 支持但不推荐使用明文密码，建议使用 dmctl encrypt 对明文密码进行加密后使用

# 当前数据迁移任务需要的全部上游 MySQL 实例配置。
mysql-instances:
-
  # 上游实例或者复制组 ID。
  source-id: "mysql-01"
  # 需要迁移的库名或表名的黑白名单的配置项名称，用于引用全局的黑白名单配置，全局配置见下面的 `block-allow-list` 的配置。
  block-allow-list: "listA"


# 黑白名单全局配置，各实例通过配置项名引用。
block-allow-list:
  listA:                              # 名称
    do-tables:                        # 需要迁移的上游表的白名单。
    - db-name: "test_db"              # 需要迁移的表的库名。
      tbl-name: "test_table"          # 需要迁移的表的名称。

```

以上内容为执行迁移的最小任务配置。关于任务的更多配置项，可以参考 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)。

## 第 3 步：启动任务

在你启动数据迁移任务之前，建议使用 `check-task` 命令检查配置是否符合 DM 的配置要求，以避免后期报错。

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

使用 `tiup dmctl` 执行以下命令启动数据迁移任务。

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

该命令中的参数描述如下：

|参数|描述|
|-|-|
|`--master-addr`|`dmctl` 要连接的集群的任意 DM-master 节点的 {advertise-addr}，例如： 172.16.10.71:8261|
|`start-task`|参数用于启动数据迁移任务|

如果任务启动失败，可根据返回结果的提示进行配置变更后执行 start-task task.yaml 命令重新启动任务。遇到问题请参考[故障及处理方法](/dm/dm-error-handling.md) 以及[常见问题](/dm/dm-faq.md)。

## 第 4 步：查看任务状态

如需了解 DM 集群中是否存在正在运行的迁移任务及任务状态等信息，可使用 `tiup dmctl` 执行 `query-status` 命令进行查询：

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

关于查询结果的详细解读，请参考[查询状态](/dm/dm-query-status.md)。

## 第 5 步：监控任务与查看日志（可选）

要查看迁移任务的历史状态以及更多的内部运行指标，可参考以下步骤。

如果使用 TiUP 部署 DM 集群时，正确部署了 Prometheus、Alertmanager 与 Grafana，则使用部署时填写的 IP 及端口进入 Grafana，选择 DM 的 Dashboard 查看 DM 相关监控项。

DM 在运行过程中，DM-worker, DM-master 及 dmctl 都会通过日志输出相关信息。各组件的日志目录如下：

- DM-master 日志目录：通过 DM-master 进程参数 `--log-file`设置。如果使用 TiUP 部署 DM，则日志目录默认位于 `/dm-deploy/dm-master-8261/log/`。
- DM-worker 日志目录：通过 DM-worker 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录默认位于 `/dm-deploy/dm-worker-8262/log/`。

## 探索更多

- [暂停数据迁移任务](/dm/dm-pause-task.md)
- [恢复数据迁移任务](/dm/dm-resume-task.md)
- [停止数据迁移任务](/dm/dm-stop-task.md)
- [导出和导入集群的数据源和任务配置](/dm/dm-export-import-config.md)
- [处理出错的 DDL 语句](/dm/handle-failed-ddl-statements.md)
