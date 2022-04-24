---
title: 通过只读副本迁移 Amazon Aurora 到 TiDB
summary: 介绍如何使用只读副本从 Amazon Aurora 迁移数据到 TiDB。
aliases: ['/zh/tidb/dev/migrate-from-aurora-using-lightning/','/docs-cn/dev/migrate-from-aurora-mysql-database/','/docs-cn/dev/how-to/migrate/from-mysql-aurora/','/docs-cn/dev/how-to/migrate/from-aurora/','/zh/tidb/dev/migrate-from-aurora-mysql-database/','/zh/tidb/dev/migrate-from-mysql-aurora']
---

# 通过只读副本迁移 Amazon Aurora 到 TiDB

本文档介绍如何从 Amazon Aurora 迁移数据到 TiDB，相比[通过快照迁移 Aurora 到 TiDB](/migrate-aurora-to-tidb.md),本文仅使用 DM 工具进行迁移，具有以下特征：

- 操作简单，仅需使用一种工具 DM。
- 从 Aurora 只读副本导出全量数据，对在线业务影响低。
- DM 所在环境需具备足以容纳全量数据的存储空间。
- 全量导入性能较低，适合 TB 级以下或对迁移时长要求不高的场景。
- 适合合库合表迁移的场景。

整个迁移包含两个过程：

- 为 Aurora 创建只读副本（可选）
- 使用 DM 迁移全量+增量到 TiDB

## 前提条件

- [安装 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)
- [获取 DM 所需上下游数据库权限](/dm/dm-worker-intro.md)

## 第 1 步： 创建数据源

1. 为了避免对当前业务产生影响，建议增加 Aurora 只读副本。参考步骤：[将 Aurora 副本添加到数据库集群](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/AuroraUserGuide/aurora-replicas-adding.html)

2. 新建`source1.yaml`文件, 写入以下内容：

    {{< copyable "" >}}

    ```yaml
    # 唯一命名，不可重复。
    source-id: "mysql-01"
    enable-relay: true        # 开启 relay log，避免全量迁移耗时过久，缺少 binlog 导致增量同步失败

    from:
      host: "${host}"         # 例如：只读副本的访问地址
      user: "${username}"
      password: "${password}" # 支持但不推荐使用明文密码，建议使用 dmctl encrypt 对明文密码进行加密后使用
      port: 3306
    ```

    如果需要将多个表库合并导入 TiDB，可参考[合库合表迁移到 TiDB](/migrate-small-mysql-shards-to-tidb.md)。

3. 在终端中执行下面的命令，使用 `tiup dmctl` 将数据源配置加载到 DM 集群中:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    该命令中的参数描述如下：

    |参数           |描述|
    |-              |-|
    |`--master-addr`  |dmctl 要连接的集群的任意 DM-master 节点的 {advertise-addr}，例如：172.16.10.71:8261|
    |`operate-source create`|向 DM 集群加载数据源|

## 第 2 步： 创建迁移任务

新建 `task1.yaml` 文件, 写入以下内容：

{{< copyable "" >}}

```yaml
# 任务名，多个同时运行的任务不能重名。
name: "test"
# 任务模式，可设为
# full：只进行全量数据迁移。Aurora 仅能通过快照的方式保证全量数据处于一致状态，因此在本文场景应仅使用 all 模式。
# incremental： binlog 持续同步
# all： 全量迁移 + binlog 持续同步
task-mode: "all"
# 下游 TiDB 配置信息。
target-database:
  host: "${host}"                   # 例如：172.16.10.83
  port: 4000
  user: "root"
  password: "${password}"           # 支持但不推荐使用明文密码，建议使用 dmctl encrypt 对明文密码进行加密后使用

# 黑白名单全局配置，各实例通过配置项名引用。
block-allow-list:                     # 如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list。
  listA:                              # 名称
    do-tables:                        # 需要迁移的上游表的白名单。
    - db-name: "test_db"              # 需要迁移的表的库名。
      tbl-name: "test_table"          # 需要迁移的表的名称。

# 配置数据源
mysql-instances:
  - source-id: "mysql-01"               # 数据源 ID，即 source1.yaml 中的 source-id
    block-allow-list: "listA"           # 引入上面黑白名单配置。
    mydumper-config-name: "configA"    # 引用上面的 syncers 增量数据配置。


mydumpers:                           # dump 处理单元的运行配置参数
  configA:                           # 配置名称
    threads: 4                       # dump 处理单元从上游数据库实例导出数据和 check-task 访问上游的线程数量，默认值为 4
    chunk-filesize: 64               # dump 处理单元生成的数据文件大小，默认值为 64，单位为 MB
    extra-args: "--consistency none" # Aurora 禁用了 ”super“ 权限，因此需要将 consistency 设为 none。如果 task-mode=all, DM 将在增量同步阶段自动启用 safe-mode 保持数据一致性。

```

以上内容为执行迁移的最小任务配置。关于任务的更多配置项，可以参考 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)

## 第 3 步： 启动任务

在你启动数据迁移任务之前，建议使用 `check-task` 命令检查配置是否符合 DM 的配置要求，以降低后期报错的概率：

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
|`--master-addr`|dmctl 要连接的集群的任意 DM-master 节点的 {advertise-addr}，例如： 172.16.10.71:8261|
|`start-task`|命令用于创建数据迁移任务|

如果任务启动失败，可根据返回结果的提示进行配置变更后，再次执行上述命令，重新启动任务。遇到问题请参考[故障及处理方法](/dm/dm-error-handling.md)以及[常见问题](/dm/dm-faq.md)。

## 第 4 步： 查看任务状态

如需了解 DM 集群中是否存在正在运行的迁移任务及任务状态等信息，可使用 `tiup dmctl` 执行 `query-status` 命令进行查询：

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

关于查询结果的详细解读，请参考[查询状态](/dm/dm-query-status.md)。

## 第 5 步： 监控任务与查看日志

要查看迁移任务的历史状态以及更多的内部运行指标，可参考以下步骤。

如果使用 TiUP 部署 DM 集群时，正确部署了 Prometheus、Alertmanager 与 Grafana，则使用部署时填写的 IP 及端口进入 Grafana，选择 DM 的 dashboard 查看 DM 相关监控项。

DM 在运行过程中，DM-worker, DM-master 及 dmctl 都会通过日志输出相关信息。各组件的日志目录如下：

- DM-master 日志目录：通过 DM-master 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录默认位于 `/dm-deploy/dm-master-8261/log/`。
- DM-worker 日志目录：通过 DM-worker 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录默认位于 `/dm-deploy/dm-worker-8262/log/`。

## 探索更多

- [合库合表迁移到 TiDB](/migrate-small-mysql-shards-to-tidb.md)
- [暂停数据迁移任务](/dm/dm-pause-task.md)
- [恢复数据迁移任务](/dm/dm-resume-task.md)
- [停止数据迁移任务](/dm/dm-stop-task.md)
- [导出和导入集群的数据源和任务配置](/dm/dm-export-import-config.md)
- [处理出错的 DDL 语句](/dm/handle-failed-ddl-statements.md)
