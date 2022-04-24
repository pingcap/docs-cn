---
title: 通过快照迁移 Amazon Aurora 到 TiDB
summary: 介绍如何使用快照从 Amazon Aurora 迁移数据到 TiDB。
aliases: ['/zh/tidb/dev/migrate-from-aurora-using-lightning/','/docs-cn/dev/migrate-from-aurora-mysql-database/','/docs-cn/dev/how-to/migrate/from-mysql-aurora/','/docs-cn/dev/how-to/migrate/from-aurora/','/zh/tidb/dev/migrate-from-aurora-mysql-database/','/zh/tidb/dev/migrate-from-mysql-aurora']
---

# 通过快照迁移 Amazon Aurora 到 TiDB

本文档介绍如何从 Amazon Aurora 迁移数据到 TiDB，迁移过程采用 [DB snapshot](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html)，具有以下特征：

- 操作较为复杂，需要使用 Dumpling/Lightning/DM 三种迁移工具。
- 创建新快照的过程对在线业务有影响。
- 节约全量数据导入过程的时间和空间消耗。
- 全量导入性能较好
- 适用于大数据量迁移

整个迁移包含两个过程：

- 使用 Lightning 导入全量数据到 TiDB
- 使用 DM 持续增量同步到 TiDB（可选）

## 前提条件

- [安装 Dumpling 和 Lightning](/migration-tools.md)。
- [获取 Dumpling 所需 上游数据库权限](/dumpling-overview.md#需要的权限)。
- [获取 Lightning 所需下游数据库权限](/tidb-lightning/tidb-lightning-faq.md#tidb-lightning-对下游数据库的账号权限要求是怎样的)。

## 导入全量数据到 TiDB

### 第 1 步： 导出 Aurora 快照文件到 Amazon S3

1. 在 Aurora 上，执行以下命令，查询并记录当前 binlog 位置，且时间为 T1：

    ```sql
    mysql> SHOW MASTER STATUS;
    ```

    你将得到类似以下的输出，请记录 binlog 名称和位置，供后续步骤使用：

    ```
    +------------------+----------+--------------+------------------+-------------------+
    | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
    +------------------+----------+--------------+------------------+-------------------+
    | mysql-bin.000002 |    52806 |              |                  |                   |
    +------------------+----------+--------------+------------------+-------------------+
    1 row in set (0.012 sec)
    ```

2. 创建快照，此操作时间为 T2。
  
3. 导出 Aurora 快照文件到 S3。具体方式请参考 Aurora 的官方文档：[Exporting DB snapshot data to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html).

### 第 2 步： 导出 schema 文件

因为 Aurora 生成的快照文件并不包含建表语句文件，所以你需要使用 Dumpling 自行导出 schema 并使用 Lightning 在下游创建 schema。你也可以跳过此步骤，并以手动方式在下游自行创建 schema。

运行以下命令，建议使用 `--filter` 参数仅导出所需表的 schema：

{{< copyable "shell-regular" >}}

```shell
tiup dumpling --host ${host} --port 3306 --user root --password ${password} --filter 'my_db1.table[12]' --no-data --output 's3://my-bucket/schema-backup?region=us-west-2' --filter "mydb.*"
```

命令中所用参数描述如下。如需更多信息可参考 [Dumpling overview](/dumpling-overview.md)。

|参数               |说明|
|-                  |-|
|-u 或 --user       |Aurora MySQL 数据库的用户|
|-p 或 --password   |MySQL 数据库的用户密码|
|-P 或 --port       |MySQL 数据库的端口|
|-h 或 --host       |MySQL 数据库的 IP 地址|
|-t 或 --thread     |导出的线程数|
|-o 或 --output     |存储导出文件的目录，支持本地文件路径或[外部存储 URL 格式](/br/backup-and-restore-storages.md)|
|-r 或 --row        |单个文件的最大行数|
|-F                 |指定单个文件的最大大小，单位为 MiB, 建议值 256 MiB|
|-B 或 --database   |导出指定数据库|
|-T 或 --tables-list |导出指定数据表|
|-d 或 --no-data    |不导出数据，仅导出 schema|
|-f 或 --filter     |导出能匹配模式的表，不可用 -T 一起使用，语法可参考[table filter](/table-filter.md)|

### 第 3 步： 编写 Lightning 配置文件

根据以下内容创建`tidb-lightning.toml` 配置文件：

{{< copyable "shell-regular" >}}

```shell
vim tidb-lightning.toml
```

{{< copyable "" >}}

```toml
[tidb]

# 目标 TiDB 集群信息.
host = ${host}                # 例如：172.16.32.1
port = ${port}                # 例如：4000
user = "${user_name}"         # 例如："root"
password = "${password}"      # 例如："rootroot"
status-port = ${status-port}  # 表结构信息在从 TiDB 的“状态端口”获取例如：10080
pd-addr = "${ip}:${port}"     # 集群 PD 的地址，lightning 通过 PD 获取部分信息，例如 172.16.31.3:2379。当 backend = "local" 时 status-port 和 pd-addr 必须正确填写，否则导入将出现异常。

[tikv-importer]
# "local"：默认使用该模式，适用于 TB 级以上大数据量，但导入期间下游 TiDB 无法对外提供服务。
# "tidb"：TB 级以下数据量也可以采用`tidb`后端模式，下游 TiDB 可正常提供服务。 关于后端模式更多信息请参阅：https://docs.pingcap.com/tidb/stable/tidb-lightning-backends
backend = "local"

# 设置排序的键值对的临时存放地址，目标路径必须是一个空目录，目录空间须大于待导入数据集的大小，建议设为与 `data-source-dir` 不同的磁盘目录并使用闪存介质，独占 IO 会获得更好的导入性能。
sorted-kv-dir = "${path}"

[mydumper]
# 快照文件的地址
data-source-dir = "${s3_path}"  # eg: s3://my-bucket/sql-backup?region=us-west-2

[[mydumper.files]]
# 解析 parquet 文件所需的表达式
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

如果需要在 TiDB 开启 TLS ，请参考 [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md)。

### 第 4 步： 导入全量数据到 TiDB

1. 使用 Lightning 在下游 TiDB 建表:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup tidb-lightning -config tidb-lightning.toml -d 's3://my-bucket/schema-backup?region=us-west-2' -no-schema=false
    ```

2. 运行 `tidb-lightning`。如果直接在命令行中启动程序，可能会因为 `SIGHUP` 信号而退出，建议配合`nohup`或`screen`等工具，如：

    将有权限访问该 Amazon S3 后端存储的账号的 SecretKey 和 AccessKey 作为环境变量传入 Lightning 节点。同时还支持从 `~/.aws/credentials` 读取凭证文件。

    {{< copyable "shell-regular" >}}

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml -no-schema=true > nohup.out 2>&1 &
    ```

3. 导入开始后，可以采用以下任意方式查看进度：

   - 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
   - 通过监控面板查看进度，请参考 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。
   - 通过 Web 页面查看进度，请参考 [Web 界面](/tidb-lightning/tidb-lightning-web-interface.md)。

4. 导入完毕后，TiDB Lightning 会自动退出。查看日志的最后 5 行中会有 `the whole procedure completed`，则表示导入成功。

> **注意：**
>
> 无论导入成功与否，最后一行都会显示 `tidb lightning exit`。它只是表示 TiDB Lightning  正常退出，不代表任务完成。

如果导入过程中遇到问题，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。

## 持续增量同步数据到 TiDB（可选）

### 前提条件

- [安装 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)
- [获取 DM 所需上下游数据库权限](/dm/dm-worker-intro.md)

### 第 1 步： 创建数据源

1. 新建`source1.yaml`文件, 写入以下内容：

    {{< copyable "" >}}

    ```yaml
    # 唯一命名，不可重复。
    source-id: "mysql-01"

    from:
      host: "${host}"         # 例如：172.16.10.81
      user: "root"
      password: "${password}" # 支持但不推荐使用明文密码，建议使用 dmctl encrypt 对明文密码进行加密后使用
      port: 3306
    ```

2. 在终端中执行下面的命令，使用 `tiup dmctl` 将数据源配置加载到 DM 集群中:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    该命令中的参数描述如下：

    |参数           |描述|
    |-              |-|
    |`--master-addr`  |dmctl 要连接的集群的任意 DM-master 节点的 {advertise-addr}，例如：172.16.10.71:8261|
    |`operate-source create`|向 DM 集群加载数据源|

### 第 2 步： 创建迁移任务

新建 `task1.yaml` 文件, 写入以下内容：

{{< copyable "" >}}

```yaml
# 任务名，多个同时运行的任务不能重名。
name: "test"
# 任务模式，本场景下应使用 incremental 模式
# full：只进行全量数据迁移
# incremental： binlog 持续同步
# all： 全量迁移 + binlog 持续同步
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
    syncer-config-name: "configA"    # 引用上面的 syncers 增量数据配置。
    meta:                               # task-mode 为 incremental 且下游数据库的 checkpoint 不存在时 binlog 迁移开始的位置; 如果 checkpoint 存在，则以 checkpoint 为准。
      binlog-name: "mysql-bin.000002"   # “Step 1. 导出 Aurora 快照文件到 Amazon S3” 中记录的日志位置。
      binlog-pos: 52806

#【可选配置】 如果增量数据迁移需要重复迁移已经在全量数据迁移中完成迁移的数据，则需要开启 safe mode 避免增量数据迁移报错。
#  该场景多见于以下情况：全量迁移的数据不属于数据源的一个一致性快照，随后从一个早于全量迁移数据之前的位置开始同步增量数据。
syncers:            # sync 处理单元的运行配置参数。
  configA:           # 配置名称。
    safe-mode: true # 设置为 true，会将来自数据源的 INSERT 改写为 REPLACE，将 UPDATE 改写为 DELETE 与 REPLACE，从而保证在表结构中存在主键或唯一索引的条件下迁移数据时可以重复导入 DML。在启动或恢复增量复制任务的前 1 分钟内 TiDB DM 会自动启动 safe mode。

```

> **注意：**
>
> 由于 `SHOW MASTER STATUS`时（T1），与创建快照时（T2）存在时间差，增量同步可能出现数据冲突错误。因此前述任务配置中启用了 safe-mode，但 safe-mode 并不建议长期运行，待数据一致后可关闭 safe-mode.

以上内容为执行迁移的最小任务配置。关于任务的更多配置项，可以参考 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)

### 第 3 步： 启动任务

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

### 第 4 步： 查看任务状态

如需了解 DM 集群中是否存在正在运行的迁移任务及任务状态等信息，可使用 `tiup dmctl` 执行 `query-status` 命令进行查询：

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

关于查询结果的详细解读，请参考[查询状态](/dm/dm-query-status.md)。

### 第 5 步： 监控任务与查看日志

要查看迁移任务的历史状态以及更多的内部运行指标，可参考以下步骤。

如果使用 TiUP 部署 DM 集群时，正确部署了 Prometheus、Alertmanager 与 Grafana，则使用部署时填写的 IP 及端口进入 Grafana，选择 DM 的 dashboard 查看 DM 相关监控项。

DM 在运行过程中，DM-worker, DM-master 及 dmctl 都会通过日志输出相关信息。各组件的日志目录如下：

- DM-master 日志目录：通过 DM-master 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录默认位于 `/dm-deploy/dm-master-8261/log/`。
- DM-worker 日志目录：通过 DM-worker 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录默认位于 `/dm-deploy/dm-worker-8262/log/`。

## 探索更多

- [暂停数据迁移任务](/dm/dm-pause-task.md)
- [恢复数据迁移任务](/dm/dm-resume-task.md)
- [停止数据迁移任务](/dm/dm-stop-task.md)
- [导出和导入集群的数据源和任务配置](/dm/dm-export-import-config.md)
- [处理出错的 DDL 语句](/dm/handle-failed-ddl-statements.md)
