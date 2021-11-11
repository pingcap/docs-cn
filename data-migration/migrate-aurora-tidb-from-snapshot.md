---
title: 从 Aurora 迁移数据到 TiDB
summary: 介绍如何使用快照从 Aurora 迁移数据到 TiDB。
---

# 从 Aurora 迁移数据到 TiDB

本文档介绍通过 Aurora 迁移数据到 TiDB，采用[DB snapshot](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html) 导入可以节约大量的空间和时间成本。迁移过程包含两个过程：

- 使用 Lightning 导入全量数据到 TiDB
- 使用 DM 持续增量数据到 TiDB（可选）

## 前提条件

- [使用 TiUP 安装 Dumpling 和 Lightning](/migration-tools.md)
- [使用 TiUP 安装 DM 集群](https://docs.pingcap.com/zh/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup)
- [DM 所需上下游数据库权限](https://docs.pingcap.com/zh/tidb-data-migration/stable/dm-worker-intro)
- [Lightning 所需下游数据库权限](/tidb-lightning/tidb-lightning-faq.md#tidb-lightning-对下游数据库的账号权限要求是怎样的)

## 使用 Lightning 导入全量数据到 TiDB

### Step 1. 导出 Aurora 快照文件到 Amazon S3

导出 Aurora 快照文件的具体方式，请参考 Aurora 的官方文档：[Exporting DB snapshot data to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html).

### Step 2. 使用 Dumpling 导出 schema

因为 Aurora 生成的快照文件并不包含建表语句文件，所以您需要使用 Dumpling 自行导出 schema 并使用 Lightning 在下游创建。或者跳过此步骤以手动方式在下游自行创建。

{{< copyable "shell-regular" >}}

```shell
tiup dumpling --host ${host} --port 3306 --user root --password ${password} --no-data --output ./schema --filter "mydb.*"
```

命令中所用参数描述如下，如需更多信息可参考：[Dumpling overview](/dumpling-overview.md).

|参数               |说明|
|-                  |-|
|-u or --user       |MySQL 数据库的用户|
|-p or --password   |MySQL 数据库的用户密码|
|-P or --port       |MySQL 数据库的端口|
|-h or --host       |MySQL 数据库的 IP 地址|
|-t or --thread     |导出的线程数|
|-o or --output     |存储导出文件的目录，支持本地文件路径或[外部存储 URL 格式](/br/backup-and-restore-storages.md)|
|-r or --row        |单个文件的最大行数|
|-F                 |指定单个文件的最大大小，单位为 MiB|
|-B 或 --database   |导出指定数据库|
|-d 或 --no-data    |不导出数据，仅导出 schema|

### Step 3. 编写 Lightning 配置文件 

根据一下内容创建`tidb-lighting.toml` 配置文件:

{{< copyable "shell-regular" >}}

```shell
vim tidb-lighting.toml
```

{{< copyable "" >}}

```toml
[tidb]

# 目标 TiDB 集群信息.
host = ${host}                # 例如：172.16.32.1
port = ${port}                # 例如：4000
user = "${user_name}"         # 例如："root"
password = "${password}"      # 例如："rootroot"
status-port = ${status-port}  # 表架构信息在从 TiDB 的“状态端口”获取例如：10080
pd-addr = "${ip}:${port}"     # 集群 PD 的地址，Lighting 通过 PD 获取部分信息，例如 172.16.31.3:2379。当 backend = "local" 时 status-port 和 pd-addr 必须正确填写，否则导入将出现异常。

[tikv-importer]
# 默认使用 local 后端以获取最好的性能，但导入期间下游 TiDB 无法对外提供服务。
# 也可以考虑使用 tidb 后端，性能与 DM 近似，但导入期间下游 TiDB 可以正常提供服务。
# 关于后端模式的更多信息请参考： https://docs.pingcap.com/tidb/stable/tidb-lightning-backends
backend = "local"

# 设置排序的键值对的临时存放地址，目标路径需要是一个空目录,至少需要数据源最大单表的空间
sorted-kv-dir = "${path}"

[mydumper]
# 快照文件的地址
data-source-dir = "${s3_path}"  # eg: s3://bucket-name/data-path

[[mydumper.files]]
# 解析 parquet 文件所需的表达式
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

如果需要在 TiDB 开启 TLS ，请参考： [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md)

### Step 4. Create table schemas in TiDB

使用 Lightning 在下游 TiDB 建表:

{{< copyable "shell-regular" >}}

```shell
tiup tidb-lightning -config tidb-lightning.toml -d ./schema -no-schema=false
```

### Step 5. Import data into TiDB using TiDB Lightning

运行 `tidb-lightning`。如果直接在命令行中启动程序，可能会因为 `SIGHUP` 信号而退出，建议配合`nohup`或`screen`等工具，如：

{{< copyable "shell-regular" >}}

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
nohup tiup tidb-lightning -config tidb-lightning.toml -no-schema=true > nohup.out &
```

导入开始后，可以采用以下任意方式查看进度：

- 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
- 通过监控面板查看进度，请参见 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。

导入完毕后，TiDB Lightning 会自动退出。查看日志的最后 5 行中会有 `the whole procedure completed`，则表示导入成功。

> **注意：**
>
> 无论导入成功与否，最后一行都会显示 `tidb lightning exit`。它只是表示 TiDB Lightning  正常退出，不代表任务完成。

如果导入过程中遇到问题，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。
