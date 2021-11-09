---
title: 从 TB 级以上 MySQL 迁移数据到 TiDB
summary: 介绍如何从 TB 级以上 MySQL 迁移数据到 TiDB。
---

# 从 TB 级以上 MySQL 迁移数据到 TiDB

通常数据量较低时，使用 DM 进行迁移较为简单，可直接完成全量+持续增量迁移工作。但当数据量较大时，DM 较低的数据导入速度(30~50 GiB/h)可能令整个迁移周期过长。

因此，本文档介绍使用 Dumpling 和 Lightning 进行全量数据迁移，其 local backend 模式导入速度可达 500 GiB/h。再使用 DM 完成增量数据迁移。

## 前提条件

- [使用 TiUP 安装 DM 集群](https://docs.pingcap.com/zh/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup)
- [使用 TiUP 安装 Dumpling 和 Lightning](/migration-tools.md)
- [Lightning 所需下游数据库权限](/tidb-lightning/tidb-lightning-faq.md#tidb-lightning-对下游数据库的账号权限要求是怎样的)
- [Dumpling 所需上游数据库权限](/dumpling-overview.md#从-tidbmysql-导出数据)

## 第 1 步. 使用 Dumpling 从 MySQL 导出全量数据

Dumpling 默认导出数据格式为 SQL 文件。也可以通过设置 --filetype sql 导出数据到 SQL 文件：

{{< copyable "shell-regular" >}}

```shell
tiup dumpling \
  -u root \
  -p ${password} \
  -P 4000 \
  -h 127.0.0.1 \
  --filetype sql \
  -t 8 \
  -o ${data-path} \
  -r 200000 \
  -F 256MiB
```

以上命令行中用到的参数描述如下。要了解更多 Dumpling 参数，请参考 [Dumpling 使用文档](/dumpling-overview.md)
|权限               |作用域|
|-                  |-|
|-u or --user       |MySQL 数据库的用户|
|-p or --password   |MySQL 数据库的用户密码|
|-P or --port       |MySQL 数据库的端口|
|-h or --host       |MySQL 数据库的 IP 地址|
|-t or --thread     |导出的线程数|
|-o or --output     |存储导出文件的目录，支持本地文件路径或[外部存储 URL 格式](/br/backup-and-restore-storages.md)|
|-r or --row        |单个文件的最大行数|
|-F                 |指定单个文件的最大大小，单位为 MiB|

请确保`${data-path}`拥有足够的空间。强烈建议使用`-F`参数以避免单表过大导致备份过程中断。

查看在`${data-path}`目录下的`metadata`文件，这是 Dumpling 自动生成的元信息文件，请记录其中的 binlog 位置信息，这将在第 3 步增量同步的时候使用

```
SHOW MASTER STATUS:
 Log: mysql-bin.000004
 Pos: 109227
 GTID:
```

## 第 2 步. 使用 Lightning 导入全量数据到 TiDB

编写配置文件`tidb-lightning.toml`：

{{< copyable "shell-regular" >}}

```toml
[lightning]
# 日志
level = "info"
file = "tidb-lightning.log"

[tikv-importer]
# 默认使用 local 后端以获取最好的性能，但导入期间下游 TiDB 无法对外提供服务。
# 也可以考虑使用 tidb 后端，性能与 DM 近似，但导入期间下游 TiDB 可以正常提供服务。
# 关于后端模式的更多信息请参考： https://docs.pingcap.com/tidb/stable/tidb-lightning-backends
backend = "local"
# 设置排序的键值对的临时存放地址，目标路径需要是一个空目录且空间充足。
sorted-kv-dir = "${sorted-kv-dir}"

[mydumper]
# 源数据目录，即第 1 步中 Dumpling 保存数据的路径。
data-source-dir = "${data-path}"

# 配置通配符规则，默认规则会过滤 mysql、sys、INFORMATION_SCHEMA、PERFORMANCE_SCHEMA、METRICS_SCHEMA、INSPECTION_SCHEMA 系统数据库下的所有表
# 若不配置该项，导入系统表时会出现“找不到 schema”的异常
filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

[tidb]
# 目标集群的信息
host = ${host}              # 例如：172.16.32.1
port = ${port}              # 例如：4000
user = "${user_name}"       # 例如："root"
password = "${password}"    # 例如："rootroot"
# 表架构信息在从 TiDB 的“状态端口”获取
status-port = ${status-port} # 例如：10080
# 集群 PD 的地址，Lighting 通过 PD 获取部分信息
pd-addr = "${ip}:${port}"   # 例如 172.16.31.3:2379。当 backend = "local" 时 status-port 和 pd-addr 必须正确填写，否则导入将出现异常。
```

关于更多 Lightning 的配置，请参考[TiDB Lightning 配置参数](/tidb-lightning/tidb-lightning-configuration.md)

运行 `tidb-lightning`。如果直接在命令行中启动程序，可能会因为 `SIGHUP` 信号而退出，建议配合`nohup`或`screen`等工具，如：

{{< copyable "shell-regular" >}}

```shell
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

导入完毕后，TiDB Lightning 会自动退出。若导入成功，日志 tidb-lightning.log 的最后一行会显示 `tidb lightning exit`。
如果出错，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。

## 第 3 步. 使用 DM 持续复制增量数据到 TiDB

新建`source1.yaml`文件, 写入以下内容：

{{< copyable "shell-regular" >}}

```yaml
# Configuration.
source-id: "mysql-01" # 唯一命令，不可重复
 
# DM-worker 是否使用全局事务标识符 (GTID) 拉取 binlog。使用前提是上游 MySQL 已开启 GTID 模式。若上游存在主从自动切换，则必须使用 GTID 模式。
enable-gtid: false

from:
  host: "${host}"           # 例如：172.16.10.81
  user: "root"
  password: "${password}"   # 支持但不推荐使用明文密码，建议使用 dmctl encrypt 对明文密码进行加密后使用
  port: 3306
```

在终端中执行下面的命令，使用`tiup dmctl`将数据源配置加载到 DM 集群中:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr 172.16.10.71:8261 operate-source create source1.yaml
```

该命令中的参数描述如下：
|参数           |描述|
|-              |-|
|--master-addr  |dmctl 要连接的集群的任意 DM-master 节点的 {advertise-addr}|
|operate-source create|向 DM 集群加载、列出、移除数据源|

编辑`task.yaml`，配置增量同步模式，以及每个数据源的同步起点：

{{< copyable "shell-regular" >}}

```yaml
   name: task-test              # 任务名称，需要全局唯一。
   task-mode: incremental       # 任务模式，设为 "incremental" 即只进行增量数据迁移。

   ## 配置下游 TiDB 数据库实例访问信息
   target-database:         # 下游数据库实例配置。
     host: "${host}"        # 例如：127.0.0.1
     port: 4000
     user: "root"
     password: "${password}"    # 推荐使用经过 dmctl 加密的密文。

   ##  使用黑白名单配置需要同步的表
   block-allow-list:            # 数据源数据库实例匹配的表的 block-allow-list 过滤规则集，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list。
     bw-rule-1:                 # 黑白名单配置项 ID。
       do-dbs: ["${db-name}"]   # 迁移哪些库。

   ## 【可选配置】 如果增量数据迁移需要重复迁移已经在全量数据迁移中完成迁移的数据，则需要开启 safe mode 避免增量数据迁移报错。
   ##  该场景多见于以下情况：全量迁移的数据不属于数据源的一个一致性快照，随后从一个早于全量迁移数据之前的位置开始同步增量数据。
   # syncers:            # sync 处理单元的运行配置参数。
   #  global:           # 配置名称。
   #    safe-mode: true # 设置为 true，会将来自数据源的 INSERT 改写为 REPLACE，将 UPDATE 改写为 DELETE 与 REPLACE，从而保证在表结构中存在主键或唯一索引的条件下迁移数据时可以重复导入 DML。在启动或恢复增量复制任务的前 1 分钟内 TiDB DM 会自动启动 safe mode。

   ## 配置数据源
   mysql-instances:
     - source-id: "mysql-01"         # 数据源 ID，即 source1.yaml 中的 source-id
       block-allow-list: "bw-rule-1" # 引入上面黑白名单配置。
#       syncer-config-name: "global"  # 引用上面的 syncers 增量数据配置。
       meta:                         # task-mode 为 incremental 且下游数据库的 checkpoint 不存在时 binlog 迁移开始的位置; 如果 checkpoint 存在，则以 checkpoint 为准。
         binlog-name: "mysql-bin.000004"  # 第 1 步中记录的日志位置，当上游存在主从切换时，必须使用 gtid。
         binlog-pos: 109227
         # binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

```

以上内容为执行迁移的最小任务配置。关于任务的更多配置项，可以参考[DM 任务完整配置文件介绍](https://docs.pingcap.com/zh/tidb-data-migration/stable/task-configuration-file-full)

在你启动数据迁移任务之前，建议使用`check-task`命令检查配置是否符合 DM 的配置要求，以降低后期报错的概率。

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr 172.16.10.71:8261 check-task task.yaml
```

使用 tiup dmctl 执行以下命令启动数据迁移任务。

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr 172.16.10.71:8261 start-task task.yaml
```

该命令中的参数描述如下：

|参数|描述|
|-|-|
|--master-addr|dmctl 要连接的集群的任意 DM-master 节点的 {advertise-addr}|
|start-task|命令用于创建数据迁移任务|

如果任务启动失败，可根据返回结果的提示进行配置变更后执行 start-task task.yaml 命令重新启动任务。遇到问题请参考 [故障及处理方法](https://docs.pingcap.com/zh/tidb-data-migration/stable/error-handling) 以及 [常见问题](https://docs.pingcap.com/zh/tidb-data-migration/stable/faq)

## 第 4 步. 查看任务状态

如需了解 DM 集群中是否存在正在运行的迁移任务及任务状态等信息，可使用`tiup dmctl`执行`query-status`命令进行查询：

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr 172.16.10.71:8261 query-status ${task-name}
```

关于查询结果的详细解读，请参考[查询状态](https://docs.pingcap.com/zh/tidb-data-migration/stable/query-status)

## 第 5 步. 监控任务与查看日志(可选)

要查看迁移任务的历史状态以及更多的内部运行指标，可参考以下步骤。
如果使用 TiUP 部署 DM 集群时，正确部署了 Prometheus、Alertmanager 与 Grafana，则使用部署时填写的 IP 及 端口进入 Grafana，选择 DM 的 dashboard 查看 DM 相关监控项。
DM 在运行过程中，DM-worker, DM-master 及 dmctl 都会通过日志输出相关信息。各组件的日志目录如下：

- DM-master 日志目录：通过 DM-master 进程参数`--log-file`设置。如果使用 TiUP 部署 DM，则日志目录默认位于`/dm-deploy/dm-master-8261/log/`。
- DM-worker 日志目录：通过 DM-worker 进程参数`--log-file`设置。如果使用 TiUP 部署 DM，则日志目录默认位于`/dm-deploy/dm-worker-8262/log/`。

## 探索更多

- [暂停数据迁移任务](https://docs.pingcap.com/zh/tidb-data-migration/stable/pause-task)
- [恢复数据迁移任务](https://docs.pingcap.com/zh/tidb-data-migration/stable/resume-task)
- [停止数据迁移任务](https://docs.pingcap.com/zh/tidb-data-migration/stable/stop-task)
- [导出和导入集群的数据源和任务配置](https://docs.pingcap.com/zh/tidb-data-migration/stable/export-import-config)
- [处理出错的 DDL 语句](https://docs.pingcap.com/zh/tidb-data-migration/stable/handle-failed-ddl-statements)