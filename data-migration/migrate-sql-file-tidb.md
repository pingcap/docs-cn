---
title: 从 SQL 文件迁移数据到 TiDB
summary: 介绍如何从 SQL 文件迁移数据到 TiDB。
---

# 从 SQL 文件迁移数据到 TiDB

本文介绍如何使用 TiDB Lightning 从 MySQL SQL 文件迁移数据到 TiDB。关于如何生成 MySQL SQL 文件，请参考 Dumpling 文档中的[导出为 SQL 文件](https://docs.pingcap.com/zh/tidb/stable/dumpling-overview#%E5%AF%BC%E5%87%BA%E4%B8%BA-sql-%E6%96%87%E4%BB%B6)。

## 前提条件

- [使用 TiUP 安装 TiDB Lightning](/migration-tools.md)
- [Lightning 所需下游数据库权限](/tidb-lightning/tidb-lightning-faq.md#tidb-lightning-对下游数据库的账号权限要求是怎样的)

## 第 1 步. 准备 SQL 文件

将所有 SQL 文件放到统一目录下，例如`/data/my_datasource/`, Lighting 将递归地寻找该目录下及其子目录内的所有`.sql`文件。

## 第 2 步. 定义目标表结构

CSV 文件自身未包含表结构信息。要导入 TiDB，就必须为其提供表结构。可以通过以下任一方法实现：

1. 编写包含 DDL 语句的 SQL 文件。

- 文件名格式为`${db_name}-schema-create.sql`,其内容需包含 CREATE DATABASE 语句；
- 文件名格式为`${db_name}.${table_name}-schema.sql`,其内容需包含 CREATE TABLE 语句。

之后需要在导入过程中将`tidb-lightning.toml`中设置。

```toml
[mydumper] 
no-schema = false # 通过 Lightning 在下游创建库和表，此项设为 false。
```

2. 手动在下游 TiDB 建库和表。之后需要在导入过程中将`tidb-lightning.toml`中设置。

```toml
[mydumper] 
no-schema = true # 若已经在下游创建好库和表，此项设为 true 表示不进行 schema 创建
```

## 第 3 步. 编写配置文件

新建文件 `tidb-lightning.toml`，包含以下内容：

{{< copyable "" >}}

```toml
[lightning]
# 日志
level = "info"
file = "tidb-lightning.log"

[tikv-importer]
# "local"：默认使用该模式，适用于 TB 级以上大数据量，但导入期间下游 TiDB 无法对外提供服务。
# "tidb"：TB 级以下数据量也可以采用`tidb`后端模式，下游 TiDB 可正常提供服务。 关于后端模式更多信息请参阅：https://docs.pingcap.com/tidb/stable/tidb-lightning-backends
backend = "local"
# 设置排序的键值对的临时存放地址，目标路径需要是一个空目录，至少需要数据源最大单表的空间
sorted-kv-dir = "${sorted-kv-dir}"

[mydumper]
# 源数据目录。支持本地路径例如`/data/my_datasource/`或 S3 路径例如：`s3://bucket-name/data-path`
data-source-dir = "${my_datasource}"

# 不创建表库，当在 #Step 2 手动完成下游表结构创建时此项设为 true，否则为 false
no-schema = true

# 目标集群的信息
host = "${ip}"
port = 4000
user = "root"
password = "${password}"
# 表结构信息在从 TiDB 的“状态端口”获取。
status-port = ${port}       # 例如：10080
# 集群 pd 的地址
pd-addr = "${ip}:${port}"   # 例如 172.16.31.3:2379。当 backend = "local" 时 status-port 和 pd-addr 必须正确填写，否则导入将出现异常。
```

关于配置文件更多信息，可参阅：[TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

## 第 4 步. 执行导入

运行 `tidb-lightning`。如果直接在命令行中启动程序，可能会因为 `SIGHUP` 信号而退出，建议配合`nohup`或`screen`等工具，如：

{{< copyable "shell-regular" >}}

```shell
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

导入完毕后，TiDB Lightning 会自动退出。若导入成功，日志 tidb-lightning.log 的最后一行会显示 `tidb lightning exit`。

如果出错，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。