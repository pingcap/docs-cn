---
title: TiDB Lightning 后端
summary: 了解使用 TiDB Lightning 导入数据时，如何选择不同的后端。
---

# TiDB Lightning 后端

TiDB Lightning 的[后端](/tidb-lightning/tidb-lightning-glossary.md#backend)决定 `tidb-lightning` 组件将如何把将数据导入到目标集群中。目前，TiDB Lightning 支持以下后端：

+ [Local-backend](#tidb-lightning-local-backend)
+ [Importer-backend](#tidb-lightning-importer-backend)
+ [TiDB-backend](#tidb-lightning-tidb-backend)

以上几种后端导入数据的区别如下：

* **Local-backend**：`tidb-lightning` 先将数据编码成键值对并排序存储在本地临时目录，然后将这些键值对以 SST 文件的形式上传到各个 TiKV 节点，然后由 TiKV 将这些 SST 文件 Ingest 到集群中。和 `Importer-backend` 原理相同，不过不依赖额外的 `tikv-importer` 组件。

* **Importer-backend**：`tidb-lightning` 先将 SQL 或 CSV 数据编码成键值对，由 `tikv-importer` 对写入的键值对进行排序，然后把这些键值对 Ingest 到 TiKV 节点中。

* **TiDB-backend**：`tidb-lightning` 先将数据编码成 `INSERT` 语句，然后直接在 TiDB 节点上运行这些 SQL 语句进行数据导入。

| 后端 | Local-backend | Importer-backend | TiDB-backend |
|:---|:---|:---|:---|
| 速度 | 快 (~500 GB/小时) | 快 (~400 GB/小时) | 慢 (~50 GB/小时) |
| 资源使用率 | 高 | 高 | 低 |
| 占用网络带宽 | 高 | 中  | 低 |
| 导入时是否满足 ACID | 否 | 否 | 是 |
| 目标表 | 必须为空 | 必须为空 | 可以不为空 |
| 额外组件 | 无 | `tikv-importer` | 无 |
| 支持 TiDB 集群版本 | >= v4.0.0 | 全部 | 全部 |
| 是否影响 TiDB 对外提供服务 | 是 | 是 | 否 |

## 如何选择后端模式

- 如果导入的目标集群为 v4.0 或以上版本，请优先考虑使用 Local-backend 模式。Local-backend 部署更简单并且性能也较其他两个模式更高
- 如果目标集群为 v3.x 或以下，建议使用 Importer-backend 模式
- 如果需要导入的集群为生产环境线上集群，或需要导入的表中已包含有数据，则最好使用 TiDB-backend 模式

## TiDB Lightning Local-backend

自 TiDB 4.0.3 版本起，TiDB Lightning 引入了 Local-backend 特性。该特性支持导入数据到 v4.0.0 以上的 TiDB 集群。

### 部署和配置 TiDB Lightning

TiDB Lightning Local-backend 模式的部署方法见 [TiDB Lightning 部署与执行](/tidb-lightning/deploy-tidb-lightning.md)。

## TiDB Lightning TiDB-backend

> **注意：**
>
> 从 TiDB v4.0 起，PingCAP 不再维护 [Loader](https://docs.pingcap.com/zh/tidb/v4.0/loader-overview) 工具。从 v5.0 起，不再提供 Loader 的文档。Loader 的功能已经完全被 TiDB Lightning 的 TiDB backend 功能取代，强烈建议切换到 TiDB Lightning。

### 部署和配置 TiDB Lightning

使用 TiDB-backend 时，你无需部署 `tikv-importer`。与[标准部署过程](/tidb-lightning/deploy-tidb-lightning.md)相比，部署 TiDB-backend 时有如下不同：

* 可以跳过所有涉及 `tikv-importer` 的步骤。
* 必须更改相应配置申明使用的是 TiDB-backend。

#### 硬件需求

使用 TiDB-backend 时， TiDB Lightning 的速度仅受限于 TiDB 执行 SQL 语句的速度。因此，即使是低配的机器也足够发挥出最佳性能。推荐的硬件配置如下：

* 16 逻辑核 CPU
* 足够储存整个数据源的 SSD 硬盘，读取速度越快越好
* 千兆网卡

#### 手动部署

手动部署时，你无需下载和配置 `tikv-importer`，TiDB Lightning 可[在此下载](/download-ecosystem-tools.md#tidb-lightning)。

在运行 `tidb-lightning` 之前，在配置文件中加上如下几行：

```toml
[tikv-importer]
backend = "tidb"
```

或者在用命令行启动 `tidb-lightning` 时，传入参数 `--backend tidb`。

#### 配置说明与示例

```toml
# tidb-lightning 任务配置

[lightning]
# 启动之前检查集群是否满足最低需求
check-requirements = true

# 每张表被切分成一个用于存储索引的“索引引擎”和若干存储行数据的“数据引擎”
# 这两项设置控制两种引擎文件的最大并发数
# 控制同时允许导入的最大表数量，对于 TiDB-backend，默认值为 CPU 数
index-concurrency = 40

# 控制同时允许导入的最大“数据引擎”数，默认值为 CPU 数，本配置应大于或等于 index-concurrency
table-concurrency = 40

# 执行 SQL 语句的并发数。默认与逻辑 CPU 的数量相同
# TiDB-backend 的瓶颈通常不在 CPU, 可以根据下游集群的实际负载调大此配置以优化写入速度
# 在调整此配置时，建议将 index-concurrency 和 table-concurrency 也调整成相同的值
region-concurrency = 40

# 日志相关的配置
# 输出日志级别
level = "info"

# 日志输出的文件。如果为空（默认），则会输出至 /tmp/lightning.log.{timestamp}；如果希望输出至系统标准输出，请设置为 "-"
# file = "tidb-lightning.log"

[checkpoint]
# 启用断点续传
# 导入数据时，TiDB Lightning 会记录当前表导入的进度
# 若 TiDB Lightning 或其他组件异常退出，在重启时也可以避免重复再导入已完成的数据
enable = true

# 存储断点的方式
#  - file（默认）：存放在本地文件系统（要求 v2.1.1 或以上）
#  - mysql：存放在兼容 MySQL 的数据库服务器
driver = "file"

# 存储断点的数据库名称
# 仅在 driver = "mysql" 时生效
# schema = "tidb_lightning_checkpoint"

# 断点的存放位置
#
# 若 driver = "file"，此参数为断点信息存放的文件路径
# 如果不设置该参数则默认为 `/tmp/CHECKPOINT_SCHEMA.pb`
#
# 若 driver = "mysql"，此参数为数据库连接参数 (DSN)，格式为“用户:密码@tcp(地址:端口)/”
# 默认会重用 [tidb] 设置目标数据库来存储断点
# 为避免加重目标集群的压力，建议另外使用一个兼容 MySQL 的数据库服务器
# dsn = "/tmp/tidb_lightning_checkpoint.pb"

# 导入成功后是否保留断点。默认为删除
# 保留断点可用于调试，但有可能泄漏数据源的元数据
# keep-after-success = false

[tikv-importer]
# 后端模式，对于 TiDB-backend 请设置为 “tidb”
backend = "tidb"

# 对于插入重复数据时执行的操作：
# - replace：新数据替代已有数据
# - ignore：保留已有数据，忽略新数据
# - error：中止导入并报错
# on-duplicate = "replace"

[mydumper]
# 设置文件读取的区块大小(默认为 64 KiB)，确保该值比数据源的最长字符串长。
# read-block-size = "64KiB" 

# （源数据文件）单个导入区块大小的最小值（默认为 100 GiB）。
# TiDB Lightning 根据该值将一张大表分割为多个数据引擎文件。
# batch-size = "100GiB"

# 本地源数据目录或外部存储 URL
data-source-dir = "/data/my_database"

# “严格”格式的导入数据可加快处理速度。
# strict-format = true 要求：
# 在 CSV 文件的所有记录中，每条数据记录的值不可包含字符换行符（U+000A 和 U+000D，即 \r 和 \n）
# 甚至被引号包裹的字符换行符都不可包含，即换行符只可用来分隔行。
# 导入数据源为严格格式时，TiDB Lightning 会快速定位大文件的分割位置进行并行处理。
# 但是如果输入数据为非严格格式，可能会将一条完整的数据分割成两部分，导致结果出错。
# 为保证数据安全而非追求处理速度，默认值为 false。
# strict-format = false

# 如果 strict-format = true，TiDB Lightning 会将 CSV 大文件分割为多个文件块进行并行处理。max-region-size 是分割后每个文件块的最大大小。
# max-region-size = "256MiB" # Byte（默认是 256 MiB）

# 只导入与该通配符规则相匹配的表，默认会过滤掉系统表。详情见表库过滤章节。
# filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

# 配置 CSV 文件的解析方式（如果源文件中不包含 CSV 文件可不设置此项）。
[mydumper.csv]
# 字段分隔符，应为单个 ASCII 字符。
separator = ','

# 引用定界符，可为单个 ASCII 字符或空字符串。
delimiter = '"'

# CSV 文件是否包含表头。
# 如果 header = true，将跳过首行。
header = true

# CSV 文件是否包含 NULL。
# 如果 not-null = true，CSV 所有列都不能解析为 NULL。
not-null = false

# 如果 not-null = false（即 CSV 可以包含 NULL），
# 为以下值的字段将会被解析为 NULL。
null = '\N'

# 是否对字段内“\“进行转义
backslash-escape = true

# 如果有行以分隔符结尾，删除尾部分隔符。
trim-last-separator = false

[tidb]
# 目标集群的信息。tidb-server 的地址，填一个即可。
host = "172.16.31.1"
port = 4000
user = "root"
password = ""

# 解析和执行 SQL 语句的默认 SQL 模式。
# sql-mode = "ONLY_FULL_GROUP_BY,NO_ENGINE_SUBSTITUTION"

# SQL 连接是否使用 TLS。可选值为：
#  * ""            - 如果填充了 [tidb.security] 部分，则强制使用 TLS（与 "cluster" 情况相同），否则与 "false" 情况相同
#  * "false"       - 禁用 TLS
#  * "cluster"     - 强制使用 TLS, 并使用 [tidb.security] 部分中指定的 CA 验证服务器的证书
#  * "skip-verify" - 强制使用 TLS, 但不验证服务器的证书（不安全！）
#  * "preferred"   - 与 "skip-verify" 相同，但是如果服务器不支持 TLS，则会退回到未加密的连接
tls = ""

# 指定证书和密钥用于 TLS 连接 MySQL。
# [tidb.security]

# CA 的公钥证书。设置为空字符串可禁用 SQL 的 TLS。
# ca-path = "/path/to/ca.pem"

# 该服务的公钥证书。默认为 `security.cert-path` 的副本
# cert-path = "/path/to/lightning.pem"

# 此服务的私钥。默认为 `security.key-path` 的副本
# key-path = "/path/to/lightning.key"

# 设置周期性后台操作。
# 支持的单位：h（时）、m（分）、s（秒）。
[cron]

# 在日志中打印导入进度的持续时间。
log-progress = "5m"
```

### 解决冲突

TiDB-backend 支持导入到已填充的表（非空表）。但是，新数据可能会与旧数据的唯一键冲突。你可以通过使用如下任务配置来控制遇到冲突时的默认行为：

```toml
[tikv-importer]
backend = "tidb"
on-duplicate = "replace" # 或者 “error”、“ignore”
```

| 设置 | 冲突时默认行为 | 对应 SQL 语句 |
|:---|:---|:---|
| replace | 新数据替代旧数据 | `REPLACE INTO ...` |
| ignore | 保留旧数据，忽略新数据 | `INSERT IGNORE INTO ...` |
| error | 中止导入 | `INSERT INTO ...` |

### 从 Loader 迁移到 TiDB Lightning TiDB-backend

当需要将数据导入到 TiDB 集群时，TiDB Lightning TiDB-backend 可以完全取代 [Loader](https://docs.pingcap.com/zh/tidb/v4.0/loader-overview)。下表说明了如何将 Loader 的配置迁移到 [TiDB Lightning 配置](/tidb-lightning/tidb-lightning-configuration.md)中：

<table>
<thead><tr><th>Loader</th><th>TiDB Lightning</th></tr></thead>
<tbody>
<tr><td>

```toml
# 日志级别
log-level = "info"
# 日志的输出目录
log-file = "loader.log"
# Prometheus
status-addr = ":8272"
# 线程数
pool-size = 16
```

</td><td>

```toml
[lightning]
# 日志级别
level = "info"
# 日志的输出目录。如果未指定该位置目录，默认为执行命令的所在目录。
file = "tidb-lightning.log"
# Prometheus
pprof-port = 8289
# 并发度 (最好使用默认设置)
#region-concurrency = 16
```

</td></tr>
<tr><td>

```toml
# 断点数据库名
checkpoint-schema = "tidb_loader"
```

</td><td>

```toml
[checkpoint]
# 断点存储
enable = true
schema = "tidb_lightning_checkpoint"
# 断点默认存储在本地的文件系统，这样更高效。但你也可以
# 选择将断点存储在目标数据库中，设置如下：
# driver = "mysql"
```

</td></tr>
<tr><td>

```toml
```

</td><td>

```toml
[tikv-importer]
# 使用 TiDB-backend
backend = "tidb"
```

</td></tr>
<tr><td>

```toml
# 数据源目录
dir = "/data/export/"
```

</td><td>

```toml
[mydumper]
# 数据源目录
data-source-dir = "/data/export"
```

</td></tr>

<tr><td>

```toml
[db]
# TiDB 连接参数
host = "127.0.0.1"
port = 4000
user = "root"
password = ""
#sql-mode = ""
```

</td><td>

```toml
[tidb]
# TiDB 连接参数
host = "127.0.0.1"
port = 4000
# 在 TiDB-backend 模式下，该参数为可选参数
# status-port = 10080
user = "root"
password = ""
#sql-mode = ""
```

</td></tr>
<tr><td>

```toml
# [[route-rules]]
# Table routes
# schema-pattern = "shard_db_*"
# table-pattern = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td><td>

```toml
# [[routes]]
# Table routes
# schema-pattern = "shard_db_*"
# table-pattern = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td></tr>
</tbody>
</table>

## TiDB Lightning Importer-backend

### 部署 Importer-backend

本节介绍 TiDB Lightning 使用 Importer 模式的部署方式：[手动部署](#手动部署-tidb-lightning)。

#### 硬件需求

`tidb-lightning` 和 `tikv-importer` 这两个组件皆为资源密集程序，建议各自单独部署。

为了优化效能，建议硬件配置如下：

- `tidb-lightning`

    - 32+ 逻辑核 CPU
    - 足够储存整个数据源的 SSD 硬盘，读取速度越快越好
    - 使用万兆网卡，带宽需 300 MB/s 以上
    - 运行过程默认会占满 CPU资源，因此建议将 `tidb-lightning` 部署到一台单独的机器上。条件不允许的情况下可以和其他组件（比如 `tidb-server`）部署在同一台机器上，然后通过配置 `region-concurrency` 限制 `tidb-lightning` 使用 CPU 资源。

- `tikv-importer`

    - 32+ 逻辑核 CPU
    - 40 GB+ 内存
    - 1 TB+ SSD 硬盘，IOPS 越高越好（要求 ≥8000）
        * 硬盘必须大于最大的 N 个表的大小总和，其中 `N` = `max(index-concurrency, table-concurrency)`。
    - 使用万兆网卡，带宽需 300 MB/s 以上
    - 运行过程中 CPU、I/O 和网络带宽资源都可能占满，建议单独部署。

如果机器充裕的话，可以部署多套 `tidb-lightning` + `tikv-importer`，然后将源数据以表为粒度进行切分，并发导入。

#### 手动部署 TiDB Lightning

##### 第 1 步：部署 TiDB 集群

在开始数据导入之前，需先部署一套要进行导入的 TiDB 集群 (版本要求 2.0.9 以上)，建议使用最新版。部署方法可参考 [使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。

##### 第 2 步：下载 TiDB Lightning 安装包

在[工具下载](/download-ecosystem-tools.md#tidb-lightning)页面下载 TiDB Lightning 安装包（需选择与 TiDB 集群相同的版本）。

##### 第 3 步：启动 `tikv-importer`

1. 从安装包上传 `bin/tikv-importer`。

2. 配置 `tikv-importer.toml`。

    ```toml
    # TiKV Importer 配置文件模版

    # 日志文件。
    log-file = "tikv-importer.log"
    # 日志等级：trace、debug、info、warn、error、off。
    log-level = "info"

    # 状态服务器的监听地址。
    status-server-address = "0.0.0.0:8286"

    [server]
    # tikv-importer 监听的地址，tidb-lightning 需要连到这个地址进行数据写入。
    addr = "0.0.0.0:8287"

    [metric]
    # 给 Prometheus 客户端的推送任务名称。
    job = "tikv-importer"
    # 给 Prometheus 客户端的推送间隔。
    interval = "15s"
    # Prometheus Pushgateway 地址。
    address = ""

    [import]
    # 存储引擎文档 (engine file) 的文件夹路径。
    import-dir = "/mnt/ssd/data.import/"
    ```

    上面仅列出了 `tikv-importer` 的基本配置。完整配置请参考[`tikv-importer` 配置说明](/tidb-lightning/tidb-lightning-configuration.md#tikv-importer)。

3. 运行 `tikv-importer`。

    {{< copyable "shell-regular" >}}

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

##### 第 4 步：启动 `tidb-lightning`

1. 从安装包上传 `bin/tidb-lightning` 及 `bin/tidb-lightning-ctl`。

2. 将数据源写入到同样的机器。

3. 配置 `tidb-lightning.toml`。对于没有出现在下述模版中的配置，TiDB Lightning 给出配置错误的提醒并退出。

    ```toml
    [lightning]

    # 转换数据的并发数，默认为逻辑 CPU 数量，不需要配置。
    # 混合部署的情况下可以配置为逻辑 CPU 的 75% 大小。
    # region-concurrency =

    # 日志
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # tikv-importer 的监听地址，需改成 tikv-importer 服务器的实际地址。
    addr = "172.16.31.10:8287"

    [mydumper]
    # 源数据目录。
    data-source-dir = "/data/my_database"

    [tidb]
    # 目标集群的信息。tidb-server 的监听地址，填一个即可。
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # 表架构信息在从 TiDB 的“状态端口”获取。
    status-port = 10080
    ```

    上面仅列出了 `tidb-lightning` 的基本配置信息。完整配置信息请参考[`tidb-lightning` 配置说明](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-全局配置)。

4. 运行 `tidb-lightning`。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

    {{< copyable "shell-regular" >}}

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```
