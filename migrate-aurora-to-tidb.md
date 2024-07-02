---
title: 从 Amazon Aurora 迁移数据到 TiDB
summary: 介绍如何使用快照从 Amazon Aurora 迁移数据到 TiDB。
---

# 从 Amazon Aurora 迁移数据到 TiDB

本文档介绍如何从 Amazon Aurora 迁移数据到 TiDB，迁移过程采用 [DB snapshot](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html)，可以节约大量的空间和时间成本。整个迁移包含两个过程：

- 使用 TiDB Lightning 导入全量数据到 TiDB
- 使用 DM 持续增量同步到 TiDB（可选）

## 前提条件

- [安装 Dumpling 和 TiDB Lightning](/migration-tools.md)。如果你要在目标端手动创建相应的表，则无需安装 Dumpling。
- [获取 Dumpling 所需上游数据库权限](/dumpling-overview.md#需要的权限)。
- [获取 TiDB Lightning 所需下游数据库权限](/tidb-lightning/tidb-lightning-faq.md#tidb-lightning-对下游数据库的账号权限要求是怎样的)。

## 导入全量数据到 TiDB

### 第 1 步：导出和导入 schema 文件

如果你已经提前手动在目标库创建好了相应的表，则可以跳过本节内容。

#### 1.1 导出 schema 文件

因为 Amazon Aurora 生成的快照文件并不包含建表语句文件，所以你需要使用 Dumpling 自行导出 schema 并使用 TiDB Lightning 在下游创建 schema。

运行以下命令时，建议使用 `--filter` 参数仅导出所需表的 schema。命令中所用参数描述，请参考 [Dumpling 主要选项表](/dumpling-overview.md#dumpling-主要选项表)。

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
tiup dumpling --host ${host} --port 3306 --user root --password ${password} --filter 'my_db1.table[12],mydb.*' --consistency none --no-data --output 's3://my-bucket/schema-backup'
```

记录上面命令中导出的 schema 的 URI，例如 's3://my-bucket/schema-backup'，后续导入 schema 时要用到。

为了获取 Amazon S3 的访问权限，可以将该 Amazon S3 的 Secret Access Key 和 Access Key 作为环境变量传入 Dumpling 或 TiDB Lightning。另外，Dumpling 或 TiDB Lightning 也可以通过 `~/.aws/credentials` 读取凭证文件。使用凭证文件可以让这台机器上所有的 Dumpling 或 TiDB Lightning 任务无需再次传入相关 Secret Access Key 和 Access Key。

#### 1.2 编写用于导入 schema 文件的 TiDB Lightning 配置文件

新建 `tidb-lightning-schema.toml` 文件，将以下内容复制到文件中并替换对应的内容。

```toml
[tidb]

# 目标 TiDB 集群信息。
host = ${host}
port = ${port}
user = "${user_name}"
password = "${password}"
status-port = ${status-port}  # TiDB 的“状态端口”，通常为 10080
pd-addr = "${ip}:${port}"     # 集群 PD 的地址，port 通常为 2379

[tikv-importer]
# 采用默认的物理导入模式 ("local")。注意该模式在导入期间下游 TiDB 无法对外提供服务。
# 关于后端模式更多信息，请参阅：https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-overview
backend = "local"

# 设置排序的键值对的临时存放地址，目标路径必须是一个空目录，目录空间须大于待导入数据集的大小。
# 建议设为与 `data-source-dir` 不同的磁盘目录并使用闪存介质，独占 IO 会获得更好的导入性能。
sorted-kv-dir = "${path}"

[mydumper]
# 设置从 Amazon Aurora 导出的 schema 文件的地址
data-source-dir = "s3://my-bucket/schema-backup"
```

如果需要在 TiDB 开启 TLS，请参考 [TiDB Lightning 配置参数](/tidb-lightning/tidb-lightning-configuration.md)。

#### 1.3 导入 schema 文件

使用 TiDB Lightning 导入 schema 到下游的 TiDB。

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_access_key}
nohup tiup tidb-lightning -config tidb-lightning-schema.toml > nohup.out 2>&1 &
```

### 第 2 步：导出和导入 Amazon Aurora 快照文件

本节介绍如何导出和导入 Amazon Aurora 快照文件。

#### 2.1 导出 Amazon Aurora 快照文件到 Amazon S3

1. 获取 Amazon Aurora binlog 的名称及位置以便于后续的增量迁移。在 Amazon Aurora 上，执行 `SHOW MASTER STATUS` 并记录当前 binlog 位置：

    ```sql
    SHOW MASTER STATUS;
    ```

    你将得到类似以下的输出，请记录 binlog 名称和位置，供后续步骤使用：

    ```
    +----------------------------+----------+--------------+------------------+-------------------+
    | File                       | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
    +----------------------------+----------+--------------+------------------+-------------------+
    | mysql-bin-changelog.018128 |    52806 |              |                  |                   |
    +----------------------------+----------+--------------+------------------+-------------------+
    1 row in set (0.012 sec)
    ```

2. 导出 Amazon Aurora 快照文件。具体方式请参考 Amazon Aurora 的官方文档：[Exporting DB snapshot data to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html)。请注意，执行 `SHOW MASTER STATUS` 命令和导出 Amazon Aurora 快照文件的时间间隔建议不要超过 5 分钟，否则记录的 binlog 位置过旧可能导致增量同步时产生数据冲突。

#### 2.2 编写用于导入快照文件的 TiDB Lightning 配置文件

新建 `tidb-lightning-data.toml` 文件，将以下内容复制到文件中并替换对应的内容。

```toml
[tidb]

# 目标 TiDB 集群信息。
host = ${host}
port = ${port}
user = "${user_name}"
password = "${password}"
status-port = ${status-port}  # TiDB 的“状态端口”，通常为 10080
pd-addr = "${ip}:${port}"     # 集群 PD 的地址，port 通常为 2379

[tikv-importer]
# 采用默认的物理导入模式 ("local")。注意该模式在导入期间下游 TiDB 无法对外提供服务。
# 关于后端模式更多信息请参阅：https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-overview
backend = "local"

# 设置排序的键值对的临时存放地址，目标路径必须是一个空目录，目录空间须大于待导入数据集的大小。
# 建议设为与 `data-source-dir` 不同的磁盘目录并使用闪存介质，独占 IO 会获得更好的导入性能。
sorted-kv-dir = "${path}"

[mydumper]
# 设置从 Amazon Aurora 导出的快照文件的地址
data-source-dir = "s3://my-bucket/sql-backup"

[[mydumper.files]]
# 解析 parquet 文件所需的表达式
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

如果需要在 TiDB 开启 TLS，请参考 [TiDB Lightning 配置参数](/tidb-lightning/tidb-lightning-configuration.md)。

#### 2.3 导入全量数据到 TiDB

1. 使用 TiDB Lightning 导入 Aurora Snapshot 的数据到 TiDB。 

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_access_key}
    nohup tiup tidb-lightning -config tidb-lightning-data.toml > nohup.out 2>&1 &
    ```

2. 导入开始后，可以采用以下任意方式查看进度：

    - 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
    - 通过监控面板查看进度，请参考 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。
    - 通过 Web 页面查看进度，请参考 [Web 界面](/tidb-lightning/tidb-lightning-web-interface.md)。

3. 导入完毕后，TiDB Lightning 会自动退出。查看 `tidb-lightning.log` 日志末尾是否有 `the whole procedure completed` 信息，如果有，表示导入成功。如果没有，则表示导入遇到了问题，可根据日志中的 error 提示解决遇到的问题。

> **注意：**
>
> 无论导入成功与否，最后一行都会显示 `tidb lightning exit`。它只是表示 TiDB Lightning 正常退出，不代表任务完成。

如果导入过程中遇到问题，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。

## 持续增量同步数据到 TiDB（可选）

### 前提条件

- [安装 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)
- [获取 DM 所需上下游数据库权限](/dm/dm-worker-intro.md)

### 第 1 步：创建数据源

1. 新建 `source1.yaml` 文件，写入以下内容：

    ```yaml
    # 唯一命名，不可重复。
    source-id: "mysql-01"

    # DM-worker 是否使用全局事务标识符 (GTID) 拉取 binlog。使用前提是上游 MySQL 已开启 GTID 模式。若上游存在主从自动切换，则必须使用 GTID 模式。
    enable-gtid: false

    from:
      host: "${host}"         # 例如：172.16.10.81
      user: "root"
      password: "${password}" # 支持但不推荐使用明文密码，建议使用 dmctl encrypt 对明文密码进行加密后使用
      port: 3306
    ```

2. 在终端中执行下面的命令，使用 `tiup dmctl` 将数据源配置加载到 DM 集群中:

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    该命令中的参数描述如下：

    | 参数           | 描述 |
    | -              | - |
    | `--master-addr` | dmctl 要连接的集群的任意 DM-master 节点的 `{advertise-addr}`，例如：172.16.10.71:8261 |
    | `operate-source create` |向 DM 集群加载数据源 |

### 第 2 步：创建迁移任务

新建 `task1.yaml` 文件，写入以下内容：

{{< copyable "" >}}

```yaml
# 任务名，多个同时运行的任务不能重名。
name: "test"
# 任务模式，可设为
# full：只进行全量数据迁移
# incremental： binlog 实时同步
# all： 全量 + binlog 迁移
task-mode: "incremental"
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
#    syncer-config-name: "global"        # syncer 配置的名称
    meta:                               # `task-mode` 为 `incremental` 且下游数据库的 `checkpoint` 不存在时 binlog 迁移开始的位置; 如果 checkpoint 存在，则以 `checkpoint` 为准。如果 `meta` 项和下游数据库的 `checkpoint` 都不存在，则从上游当前最新的 binlog 位置开始迁移。
      binlog-name: "mysql-bin.000004"   # “Step 1. 导出 Amazon Aurora 快照文件到 Amazon S3” 中记录的日志位置，当上游存在主从切换时，必须使用 gtid。
      binlog-pos: 109227
      # binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

# 【可选配置】 如果增量数据迁移需要重复迁移已经在全量数据迁移中完成迁移的数据，则需要开启 safe mode 避免增量数据迁移报错。
   ##  该场景多见于以下情况：全量迁移的数据不属于数据源的一个一致性快照，随后从一个早于全量迁移数据之前的位置开始同步增量数据。
   # syncers:            # sync 处理单元的运行配置参数。
   #  global:           # 配置名称。
   #    safe-mode: true # 设置为 true，会将来自数据源的 INSERT 改写为 REPLACE，将 UPDATE 改写为 DELETE 与 REPLACE，从而保证在表结构中存在主键或唯一索引的条件下迁移数据时可以重复导入 DML。在启动或恢复增量复制任务的前 1 分钟内 TiDB DM 会自动启动 safe mode。
```

以上内容为执行迁移的最小任务配置。关于任务的更多配置项，可以参考 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)

### 第 3 步：启动任务

在你启动数据迁移任务之前，建议使用 `check-task` 命令检查配置是否符合 DM 的配置要求，以降低后期报错的概率：

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

使用 `tiup dmctl` 执行以下命令启动数据迁移任务。

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

该命令中的参数描述如下：

|参数|描述|
|-|-|
|`--master-addr`|dmctl 要连接的集群的任意 DM-master 节点的 `{advertise-addr}`，例如：172.16.10.71:8261|
|`start-task`|命令用于创建数据迁移任务|

如果任务启动失败，可根据返回结果的提示进行配置变更后，再次执行上述命令，重新启动任务。遇到问题请参考[故障及处理方法](/dm/dm-error-handling.md)以及[常见问题](/dm/dm-faq.md)。

### 第 4 步：查看任务状态

如需了解 DM 集群中是否存在正在运行的迁移任务及任务状态等信息，可使用 `tiup dmctl` 执行 `query-status` 命令进行查询：

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

关于查询结果的详细解读，请参考[查询状态](/dm/dm-query-status.md)。

### 第 5 步：监控任务与查看日志

要查看迁移任务的历史状态以及更多的内部运行指标，可参考以下步骤。

如果使用 TiUP 部署 DM 集群时，正确部署了 Prometheus、Alertmanager 与 Grafana，则使用部署时填写的 IP 及端口进入 Grafana，选择 DM 的 dashboard 查看 DM 相关监控项。

DM 在运行过程中，DM-worker、DM-master 及 dmctl 都会通过日志输出相关信息。各组件的日志目录如下：

- DM-master 日志目录：通过 DM-master 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录默认位于 `/dm-deploy/dm-master-8261/log/`。
- DM-worker 日志目录：通过 DM-worker 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录默认位于 `/dm-deploy/dm-worker-8262/log/`。

## 探索更多

- [暂停数据迁移任务](/dm/dm-pause-task.md)
- [恢复数据迁移任务](/dm/dm-resume-task.md)
- [停止数据迁移任务](/dm/dm-stop-task.md)
- [导出和导入集群的数据源和任务配置](/dm/dm-export-import-config.md)
- [处理出错的 DDL 语句](/dm/handle-failed-ddl-statements.md)
