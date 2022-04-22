---
title: 从 SQL 文件迁移数据到 TiDB
summary: 介绍如何使用 TiDB Lightning 从 MySQL SQL 文件迁移数据到 TiDB。
aliases: ['/docs-cn/dev/migrate-from-mysql-mydumper-files/','/zh/tidb/dev/migrate-from-mysql-mydumper-files/','/zh/tidb/dev/migrate-from-mysql-dumpling-files/']
---

# 从 SQL 文件迁移数据到 TiDB

本文介绍如何使用 TiDB Lightning 从 MySQL SQL 文件迁移数据到 TiDB。关于如何生成 MySQL SQL 文件，请参考 Dumpling 文档中的[导出为 SQL 文件](/dumpling-overview.md#导出为-sql-文件)。

## 前提条件

- [使用 TiUP 安装 TiDB Lightning](/migration-tools.md)
- [Lightning 所需下游数据库权限](/tidb-lightning/tidb-lightning-faq.md#tidb-lightning-对下游数据库的账号权限要求是怎样的)

## 第 1 步：准备 SQL 文件

将所有 SQL 文件放到统一目录下，例如 `/data/my_datasource/` 或 `s3://my-bucket/sql-backup?region=us-west-2`。Lightning 将递归地寻找该目录下及其子目录内的所有 `.sql` 文件。

## 第 2 步：定义目标表结构

要导入 TiDB，就必须为 SQL 文件提供表结构。

如果使用 Dumpling 工具导出数据，则会自动导出表结构文件。此外，其他方式导出的数据可以通过以下任一方法创建表结构：

* **方法一**：使用 TiDB Lightning 创建表结构。

    编写包含 DDL 语句的 SQL 文件：

    - 文件名格式为 `${db_name}-schema-create.sql`，其内容需包含 `CREATE DATABASE` 语句。
    - 文件名格式为 `${db_name}.${table_name}-schema.sql`，其内容需包含 `CREATE TABLE` 语句。

* **方法二**：手动在下游 TiDB 建库和表。

## 第 3 步：编写配置文件

新建文件 `tidb-lightning.toml`，包含以下内容：

{{< copyable "" >}}

```toml
[lightning]
# 日志
level = "info"
file = "tidb-lightning.log"

[tikv-importer]
# "local"：默认使用该模式，适用于 TiB 级以上大数据量，但导入期间下游 TiDB 无法对外提供服务。
backend = "local"
# # "tidb"：TiB 级以下数据量也可以采用 `tidb` 后端模式，下游 TiDB 可正常提供服务。关于后端模式更多信息请参 https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-backends。
# 设置排序的键值对的临时存放地址，目标路径必须是一个空目录，目录空间须大于待导入数据集的大小。建议设为与 `data-source-dir` 不同的磁盘目录并使用闪存介质，独占 I/O 会获得更好的导入性能。
sorted-kv-dir = "${sorted-kv-dir}"

[mydumper]
# 源数据目录
data-source-dir = "${data-path}" # 本地或 S3 路径，例如：'s3://my-bucket/sql-backup?region=us-west-2'

[tidb]
# 目标集群的信息
host = ${host}                # 例如：172.16.32.1
port = ${port}                # 例如：4000
user = "${user_name}"         # 例如："root"
password = "${password}"      # 例如："rootroot"
status-port = ${status-port}  # 导入过程 Lightning 需要在从 TiDB 的“状态端口”获取表结构信息，例如：10080
pd-addr = "${ip}:${port}"     # 集群 PD 的地址，Lightning 通过 PD 获取部分信息，例如 172.16.31.3:2379。当 backend = "local" 时 status-port 和 pd-addr 必须正确填写，否则导入将出现异常。
```

关于配置文件更多信息，可参阅 [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md)。

## 第 4 步：执行导入

运行 `tidb-lightning`。如果直接在命令行中启动程序，可能会因为 `SIGHUP` 信号而退出，建议配合 `nohup` 或 `screen` 等工具。

若从 S3 导入，则需将有权限访问该 Amazon S3 后端存储的账号的 SecretKey 和 AccessKey 作为环境变量传入 Lightning 节点。

{{< copyable "shell-regular" >}}

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
```

同时，TiDB Lightning 还支持从 `~/.aws/credentials` 读取凭证文件。

导入开始后，可以采用以下任意方式查看进度：

- 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
- 通过监控面板查看进度，请参考 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。
- 通过 Web 页面查看进度，请参考 [Web 界面](/tidb-lightning/tidb-lightning-web-interface.md)。

导入完毕后，TiDB Lightning 会自动退出。查看日志的最后 5 行中会有 `the whole procedure completed`，则表示导入成功。

> **注意：**
>
> 无论导入成功与否，最后一行都会显示 `tidb lightning exit`。它只是表示 TiDB Lightning  正常退出，不代表任务完成。

如果导入过程中遇到问题，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。
