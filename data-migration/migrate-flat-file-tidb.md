---
title: 从 CSV 文件迁移数据到 TiDB
summary: 介绍如何从 CSV 等文件迁移数据到 TiDB。
---

# 从 CSV 文件迁移数据到 TiDB

TiDB Lightning 支持读取 CSV 格式的文件，以及其他定界符格式如 TSV（制表符分隔值）。日常我们称之为“平面文件”类型的数据导入，也可以参考本文档进行。以下将以 CSV 文件为例展示如何导入。

## 前提条件

- [使用 TiUP 安装 TiDB Lightning](/migration-tools.md)
- [Lightning 所需下游数据库权限](/tidb-lightning/tidb-lightning-faq.md#tidb-lightning-对下游数据库的账号权限要求是怎样的)

## 第 1 步. 准备 CSV 文件

将所有要导入的 CSV 文件放在同一目录下，若要 Lighting 识别所有 CSV 文件，文件名必须满足以下格式：

- 包含整张表数据的 CSV 文件需命名为`${db_name}.${table_name}.csv`
- 如果一个表分布于多个 CSV 文件，这些 CSV 文件命名需加上文件编号的后缀，如 `${db_name}.${table_name}.003.csv`。数字部分不需要连续但必须递增，并用零填充为同样长度。

## 第 2 步. 创建目标表结构

CSV 文件自身未包含表结构信息。要导入 TiDB，就必须为其提供表结构。可以通过以下任一方法实现：

1. 首先编写包含 DDL 语句的 SQL 文件。

- 文件名格式为`${db_name}-schema-create.sql`,其内容需包含 CREATE DATABASE 语句；
- 文件名格式为`${db_name}.${table_name}-schema.sql`,其内容需包含 CREATE TABLE 语句。

之后需要在导入过程中将`tidb-lightning.toml`中设置。

```toml
[mydumper] 
no-schema = false # 通过 Lightning 在下游创建库和表，此项设为 false。
```

2. 手动在下游 TiDB 建库和表。之后需要在导入过程中在`tidb-lightning.toml`中进行设置。

```toml
[mydumper] 
no-schema = true # 若已经在下游创建好库和表，此项设为 true 表示不进行 schema 创建
```

## 第 3 步. 编写配置文件

新建文件 `tidb-lightning.toml`，包含以下内容：

{{< copyable "shell-regular" >}}

```toml
[lightning]
# 日志
level = "info"
file = "tidb-lightning.log"

[tikv-importer]
# "local"：默认使用该模式，适用于 TB 级以上大数据量，但导入期间下游 TiDB 无法对外提供服务。
# "tidb"：TB 级以下数据量也可以采用`tidb`后端模式，下游 TiDB 可正常提供服务。 关于后端模式更多信息请参阅：https://docs.pingcap.com/tidb/stable/tidb-lightning-backends
# 更多配置
backend = "local"
# 设置排序的键值对的临时存放地址，目标路径需要是一个空目录，至少需要数据源最大单表的空间
sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

[mydumper]
# 源数据目录。
data-source-dir = "/data/my_datasource/"

# 设置是否需要创建表库
# 若需要 Lightning 创建库表，则设为 false
# 若已手动完成下游表结构创建，则设为 true
no-schema = true

# 定义 CSV 格式
[mydumper.csv]
# 字段分隔符，必须为 ASCII 字符。不建议源文件使用默认的“,”简单分隔符，推荐“|+|”等非常见字符组合
separator = ','
# 引用定界符，可以为 ASCII 字符或空字符。
delimiter = '"'
# CSV 文件是否包含表头。
# 如果为 true，首行将会被跳过。
header = true
# CSV 是否包含 NULL。
# 如果为 true，CSV 文件的任何列都不能解析为 NULL。
not-null = false
# 如果 `not-null` 为 false（即 CSV 可以包含 NULL），
# 为以下值的字段将会被解析为 NULL。
null = '\N'
# 是否解析字段内的反斜线转义符。
backslash-escape = true
# 是否移除以分隔符结束的行。
trim-last-separator = false

# 目标集群的信息
host = "${ip}"
port = 4000
user = "root"
password = "${password}"
# 表结构信息在从 TiDB 的“状态端口”获取。
status-port = ${port} # 例如：10080
# 集群 pd 的地址
pd-addr = "${ip}:${port}" # 例如 172.16.31.3:2379。当 backend = "local" 时 status-port 和 pd-addr 必须正确填写，否则导入将出现异常。
```

关于配置文件更多信息，可参阅：[TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md)。

## 第 4 步. 以更快的速度导入（可选）

导入文件的大小统一约为 256 MiB 时，TiDB Lightning 可达到最佳工作状态。如果导入单个 CSV 大文件，TiDB Lightning 只能使用一个线程来处理，这会降低导入速度。

要解决此问题，可先将 CSV 文件分割为多个文件。对于通用格式的 CSV 文件，在没有读取整个文件的情况下无法快速确定行的开始和结束位置。因此，默认情况下 TiDB Lightning 不会自动分割 CSV 文件。但如果你确定待导入的 CSV 文件符合特定的限制要求，则可以启用`strict-format`模式。启用后，TiDB Lightning 会将单个 CSV 大文件分割为单个大小为 256 MiB 的多个文件块进行并行处理。

> **注意：**
>
> 如果 CSV 文件不是严格格式但 `strict-format` 被误设为 `true`，跨多行的单个完整字段会被分割成两部分，导致解析失败，甚至不报错地导入已损坏的数据。

严格格式的 CSV 文件中，每个字段仅占一行，即必须满足以下条件之一：

- delimiter 为空；
- 每个字段不包含 CR (\r）或 LF（\n）。

如果您确认满足条件，可按如下配置开启`strict-format`模式以加快导入速度。

```toml
[mydumper]
strict-format = true
```

## 第 5 步. 执行导入

运行 `tidb-lightning`。如果直接在命令行中启动程序，可能会因为 `SIGHUP` 信号而退出，建议配合`nohup`或`screen`等工具，如：

{{< copyable "shell-regular" >}}

```shell
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

导入完毕后，TiDB Lightning 会自动退出。若导入成功，日志 tidb-lightning.log 的最后一行会显示 `tidb lightning exit`。

如果出错，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。

## 其他格式的文件

以上以 CSV 文件举例完整导入过程，若数据源为其他格式，除文件名仍必须以`.csv`结尾外，配置文件`tidb-lightning.toml`的`[mydumper.csv]`格式定义同样需要做相应修改。常见的格式举例：

**TSV**

```
# 格式示例
# ID    Region    Count
# 1     East      32
# 2     South     NULL
# 3     West      10
# 4     North     39

# 格式配置
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
trim-last-separator = false
```

**TPC-H DBGEN**

```
# 格式示例
# 1|East|32|
# 2|South|0|
# 3|West|10|
# 4|North|39|

# 格式配置
[mydumper.csv]
separator = '|'
delimiter = ''
header = false
not-null = true
backslash-escape = false
trim-last-separator = true
```

## 探索更多

- [关于 mydumper.csv 内字段定义](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)