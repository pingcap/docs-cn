---
title: 从 Amazon Aurora 迁移数据到 TiDB
summary: 介绍如何使用快照从 Amazon Aurora 迁移数据到 TiDB。
aliases: ['/zh/tidb/dev/migrate-from-aurora-using-lightning/','/docs-cn/dev/migrate-from-aurora-mysql-database/','/docs-cn/dev/how-to/migrate/from-mysql-aurora/','/docs-cn/dev/how-to/migrate/from-aurora/','/zh/tidb/dev/migrate-from-aurora-mysql-database/','/zh/tidb/dev/migrate-from-mysql-aurora','/zh/tidb/stable/migrate-from-aurora-using-lightning/']
---

# 从 Amazon Aurora 迁移数据到 TiDB

本文档介绍如何从 Amazon Aurora 迁移数据到 TiDB，迁移过程采用 [DB snapshot](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html)，可以节约大量的空间和时间成本。整个迁移包含两个过程：

- 使用 TiDB Lightning 导入全量数据到 TiDB
- 使用 DM 持续增量同步到 TiDB（可选）

## 前提条件

- [安装 Dumpling 和 TiDB Lightning](/migration-tools.md)。如果你要在目标端手动创建相应的表，则无需安装 Dumpling。
- [获取 Dumpling 所需上游数据库权限](/dumpling-overview.md#需要的权限)。
- [获取 TiDB Lightning 所需下游数据库权限](/tidb-lightning/tidb-lightning-faq.md#tidb-lightning-对下游数据库的账号权限要求是怎样的)。
- 如果你想使用 DM 同步增量数据，请在创建迁移快照前为 Aurora 集群启用 binary logging，并设置 `binlog_format=ROW` 和 `binlog_row_image=FULL`。对于 Aurora MySQL 3，还需要设置 `binlog_transaction_compression=OFF`。请保留所需 binlog，直到 DM 追平上游。详情参见 [Setting up binary log replication for Aurora MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Replication.MySQL.SettingUp.html) 和 [DM precheck](/dm/dm-precheck.md)。

## 导入全量数据到 TiDB

### 第 1 步：导出和导入 schema 文件

如果你已经提前手动在目标库创建好了相应的表，则可以跳过本节内容。

在导出 schema 之前，请先创建或选定你将在[第 2.1 步](#21-导出-amazon-aurora-快照文件到-amazon-s3)中使用的快照；如果你计划使用 DM，请先完成该节中的 binlog 配置。schema 必须与该快照一致。如果快照创建后源端的 schema 发生了变化，请按第 2.1 步所述将该快照恢复到临时集群，再将该集群作为下文中的 Dumpling 数据源（`${host}`）。在 schema 导出完成前，请保持恢复出的 schema 不变。如果你在 TiDB 中手动创建表，也要确保表定义与所选快照一致。

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
host = "${host}"
port = "${port}"
user = "${user_name}"
password = "${password}"
status-port = "${status-port}"  # TiDB 的“状态端口”，通常为 10080
pd-addr = "${ip}:${port}"       # 集群 PD 的地址，port 通常为 2379

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

1. 如果你计划使用 DM 进行增量同步，请在创建快照前完成[前提条件](#前提条件)中的 binlog 配置。请使用自定义 DB cluster parameter group，并按需重启 writer instance 以使配置生效。详情参见 [Configuring Aurora MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_LogAccess.MySQL.BinaryFormat.html)。

    如果你计划在 DM 中设置 `enable-gtid: true`，还需要在创建快照前在原始源端启用 GTID 模式。设置方法请参见 [Enabling GTID-based replication for an Aurora MySQL cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/mysql-replication-gtid.configuring-aurora.html)。

    请设置一个 binlog 保留时间，覆盖从创建快照到 DM 追平上游的整个期间，包括快照导出、TiDB Lightning 导入以及用于应对延迟的额外裕量。以下示例将保留时间设置为 144 小时（6 天），并显示配置结果以供验证。请根据迁移耗时以及你的 Aurora 版本支持的上限调整该值：

    ```sql
    CALL mysql.rds_set_configuration('binlog retention hours', 144);
    CALL mysql.rds_show_configuration;
    ```

    如果你只需要全量数据迁移，则可以跳过此步骤。

2. 创建或选定要导出的 Aurora DB cluster snapshot。如果你计划使用 DM，请获取与该快照对应的 binlog 文件名和位置：将该快照恢复到一个临时 Aurora 集群，并使用与源集群相同的 parameter group；然后在恢复后的 writer instance 的 **Recent Events** 中找到 `Binlog position from crash recovery is <binlog-file-name> <binlog-position>` 消息。详细步骤请参见 [Setting up binary log replication for Aurora MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Replication.MySQL.SettingUp.html)。请记录这些值，供 DM 任务使用；DM 任务仍需连接到原始源端 Aurora 集群。只有在记录好该位置并完成第 1 步中所需的 schema 导出后，才能删除这个临时集群。

    对于增量同步，创建快照时必须已经启用了所需的 binlog 配置。在原始源端上，使用 `SHOW BINARY LOGS;` 确认所需的 binlog 文件仍然可用，并从该位置开始保留全部 binlog，直到 DM 处理完成。如果现有快照不满足这些条件，请在完成本节步骤 1 中的 binlog 配置后重新创建快照。每当你选择不同的快照时，都要确认[第 1 步](#第-1-步导出和导入-schema-文件)中准备的 schema 与该快照一致。如果不一致，请从新快照恢复出的临时集群重新导出 schema，并在导入快照数据前更新目标表定义。不要使用 `SHOW MASTER STATUS` 返回的当前位点代替快照位点，否则可能导致部分变更被重复回放或被跳过。

    如果源集群启用了 enhanced binlog（`aurora_enhanced_binlog=1`），且运行的是早于 3.14.0 的 Aurora MySQL 3 版本，那么在存在回滚事务时，快照恢复得到的 binlog 坐标可能不正确。在使用此流程前，请先将源集群升级到 3.14.0 或更高版本，并重新创建快照。详情参见 [Aurora MySQL 3.14.0 release notes](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraMySQLReleaseNotes/AuroraMySQL.Updates.3140.html)。

3. 将步骤 2 中选定的快照导出到 Amazon S3。详细步骤请参见 [Exporting DB cluster snapshot data to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-export-snapshot.html)。无论导出任务何时启动，导出的数据都以该快照对应的时间点为准。

#### 2.2 编写用于导入快照文件的 TiDB Lightning 配置文件

新建 `tidb-lightning-data.toml` 文件，将以下内容复制到文件中并替换对应的内容。

```toml
[tidb]

# 目标 TiDB 集群信息。
host = "${host}"
port = "${port}"
user = "${user_name}"
password = "${password}"
status-port = "${status-port}"  # TiDB 的“状态端口”，通常为 10080
pd-addr = "${ip}:${port}"       # 集群 PD 的地址，port 通常为 2379

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
# 解析 Parquet 文件所需的表达式
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

新建 `task1.yaml` 文件。请将 `meta.binlog-name` 和 `meta.binlog-pos` 设置为你在[第 2.1 步](#21-导出-amazon-aurora-快照文件到-amazon-s3)中记录的、与快照对齐的值，并将 DM 配置为从原始源端 Aurora 集群读取数据。

如果你设置了 `enable-gtid: true`，还需要将 `meta.binlog-gtid` 设置为与所记录快照位点对应的 GTID 集。要获取该 GTID 集，请使用 [`mysqlbinlog`](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html) 从记录到的源 binlog 文件开头开始读取，并指定 `--stop-position=<binlog-position>`。然后，将该文件中的 `Previous_gtids` 集与该位置之前已提交事务的 GTID 合并。不要直接使用源端当前的 `gtid_executed` 值，因为它可能包含快照创建之后的事务。配置要求请参见 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)。

迁移任务配置如下：

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
      binlog-name: "mysql-bin-changelog.018128" # 仅为示例值。请替换为所选快照对应的 binlog 文件名；当上游存在主从切换时，必须使用 GTID。
      binlog-pos: 52806 # 仅为示例值。请替换为所选快照对应的 binlog 位置。
      # binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

# 【可选配置】 如果增量数据同步需要重复同步已经在全量数据迁移中完成迁移的数据，则需要开启 safe mode，避免增量数据同步报错。
   ##  该场景多见于以下情况：全量迁移的数据不属于数据源的一个一致性快照，随后从一个早于全量迁移数据之前的位置开始同步增量数据。
   # syncers:            # sync 处理单元的运行配置参数。
   #  global:           # 配置名称。
   #    safe-mode: true # 设置为 true，会将来自数据源的 INSERT 改写为 REPLACE，将 UPDATE 改写为 DELETE 与 REPLACE，从而保证在表结构中存在主键或唯一索引的条件下迁移数据时可以重复导入 DML。在启动或恢复增量同步任务的前 1 分钟内 TiDB DM 会自动启动 safe mode。
```

以上内容为执行迁移的最小任务配置。关于任务的更多配置项，可以参考 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)

### 第 3 步：启动任务

在你启动数据迁移任务之前，建议使用 `check-task` 命令检查配置是否符合 DM 的配置要求，以降低后期报错的概率：

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task1.yaml
```

使用 `tiup dmctl` 执行以下命令启动数据迁移任务。

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task1.yaml
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
