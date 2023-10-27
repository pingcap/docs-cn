---
title: TiDB Lightning 并行导入
summary: 本文档介绍了 TiDB Lightning 并行导入的概念、使用场景和使用方法。
---

# TiDB Lightning 并行导入

TiDB Lightning 的[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md) 从 v5.3.0 版本开始支持单表或多表数据的并行导入。通过支持同步启动多个实例，并行导入不同的单表或多表的不同数据，使 TiDB Lightning 具备水平扩展的能力，可大大降低导入大量数据所需的时间。

在技术实现上，TiDB Lightning 通过在目标 TiDB 中记录各个实例以及每个导入表导入数据的元信息，协调不同实例的 Row ID 分配范围、全局 Checksum 的记录和 TiKV 及 PD 的配置变更与恢复。

TiDB Lightning 并行导入可以用于以下场景：

- 并行导入分库分表的数据。在该场景中，来自上游多个数据库实例中的多个表，分别由不同的 TiDB Lightning 实例并行导入到下游 TiDB 数据库中。
- 并行导入单表的数据。在该场景中，存放在某个目录中或云存储（如 Amazon S3）中的多个单表文件，分别由不同的 TiDB Lightning 实例并行导入到下游 TiDB 数据库中。该功能为 v5.3.0 版本引入的新功能。

> **注意：**
>
> - 并行导入只支持初始化 TiDB 的空表，不支持导入数据到已有业务写入的数据表，否则可能会导致数据不一致的情况。
>
> - 并行导入一般用于物理导入模式，需要设置 `parallel-import = true`。
>
> - 并行导入一般用于物理导入模式；虽然也能用于逻辑导入模式，但是一般不会带来明显的性能提升。

## 使用说明

使用 TiDB Lightning 并行导入需要设置 `parallel-import = true`。TiDB Lightning 在启动时，会在下游 TiDB 中注册元信息，并自动检测是否有其他实例向目标集群导入数据。如果有，则自动进入并行导入模式。

但是在并行导入时，需要注意以下情况：

- 解决主键或者唯一索引的冲突
- 导入性能优化

### 解决主键或者唯一索引的冲突

在使用[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)并行导入时，需要确保多个 TiDB Lightning 的数据源之间，以及它们和 TiDB 的目标表中的数据没有主键或者唯一索引的冲突，并且导入的目标表不能有其他应用进行数据写入。否则，TiDB Lightning 将无法保证导入结果的正确性，并且导入完成后相关的数据表将处于数据索引不一致的状态。

### 导入性能优化

由于 TiDB Lightning 需要将生成的 Key-Value 数据上传到对应 Region 的每一个副本所在的 TiKV 节点，其导入速度受目标集群规模的限制。在通常情况下，建议确保目标 TiDB 集群中的 TiKV 实例数量与 TiDB Lightning 的实例数量大于 n:1 (n 为 Region 的副本数量)。同时，在使用 TiDB Lightning 并行导入模式时，为达到最优性能，建议进行如下限制：

- 每个 TiDB Lightning 部署在单独的机器上面。TiDB Lightning 默认会消耗所有的 CPU 资源，在单台机器上面部署多个实例并不能提升性能。
- 每个 TiDB Lightning 实例导入的源文件总大小不超过 5 TiB
- TiDB Lightning 实例的总数量不超过 10 个

在使用 TiDB Lightning 并行导入分库分表数据的时候，请根据数据量大小选择使用的 TiDB Lightning 实例数量。

- 如果 MySQL 数据量小于 2 TiB，可以使用 1 个 TiDB Lightning 实例进行并行导入
- 如果 MySQL 数据量超过 2 TiB，并且 MySQL 实例总数小于 10 个，建议每个 MySQL 实例对应 1 个 TiDB Lightning 实例，而且并行 TiDB Lightning 实例数量不要超过 10 个
- 如果 MySQL 数据量超过 2 TiB，并且 MySQL 实例总数超过 10 个，建议这些 MySQL 实例导出的数据平均分配 5 到 10 个 TiDB Lightning 实例进行导入

接下来，本文档将以两个并行导入的示例，详细介绍了不同场景下并行导入的操作步骤：

- 示例 1：使用 Dumpling + TiDB Lightning 并行导入分库分表数据至 TiDB
- 示例 2：使用 TiDB Lightning 并行导入单表数据

### 使用限制

TiDB Lightning 在运行时，需要独占部分资源，因此如果需要在单台机器上面部署多个 TiDB Lightning 实例(不建议生产环境使用)或多台机器共享磁盘存储时，需要注意如下使用限制：

- 每个 TiDB Lightning 实例的 tikv-importer.sorted-kv-dir 必须设置为不同的路径。多个实例共享相同的路径会导致非预期的行为，可能导致导入失败或数据出错。
- 每个 TiDB Lightning 的 checkpoint 需要分开存储。checkpoint 的详细配置见 [TiDB Lightning 断点续传](/tidb-lightning/tidb-lightning-checkpoints.md)。
    - 如果设置 checkpoint.driver = "file"（默认值），需要确保每个实例设置的 checkpoint 的路径不同。
    - 如果设置 checkpoint.driver = "mysql"，需要为每个实例设置不同的 schema。
- 每个 TiDB Lightning 的 log 文件应该设置为不同的路径。共享同一个 log 文件将不利于日志的查询和排查问题。
- 如果开启 [Web 界面](/tidb-lightning/tidb-lightning-web-interface.md) 或 Debug API，需要为每个实例的 `lightning.status-addr` 设置不同地址，否则，TiDB Lightning 进程会由于端口冲突无法启动。

## 示例 1：使用 Dumpling + TiDB Lightning 并行导入分库分表数据至 TiDB

在本示例中，假设上游为包含 10 个分表的 MySQL 集群，总共大小为 10 TiB。使用 5 个 TiDB Lightning 实例并行导入，每个实例导入 2 TiB 数据，预计可以将总导入时间（不包含 Dumpling 导出的耗时）由约 40 小时降至约 10 小时。

假设上游的库名为 `my_db`，每个分表的名字为 `my_table_01` ~ `my_table_10`，需要合并导入至下游的 `my_db.my_table` 表中。下面介绍具体的操作步骤。

### 第 1 步：使用 Dumpling 导出数据

在部署 TiDB Lightning 的 5 个节点上面分别导出两个分表的数据：

- 如果两个分表位于同一个 MySQL 实例中，可以直接使用 Dumpling 的 `--filter` 参数一次性导出。此时在使用 TiDB Lightning 导入时，指定 `data-source-dir` 为 Dumpling 数据导出的目录即可；
- 如果两个分表的数据分布在不同的 MySQL 节点上，则需要使用 Dumpling 分别导出，两次导出数据需要放置在同一父目录下<b>不同子目录里</b>，然后在使用 TiDB Lightning 导入时，`data-source-dir` 指定为此父级目录。

使用 Dumpling 导出数据的步骤，请参考 [Dumpling](/dumpling-overview.md)。

### 第 2 步：配置 TiDB Lightning 的数据源

创建 `tidb-lightning.toml` 配置文件，并加入如下内容：

```
[lightning]
status-addr = ":8289"

[mydumper]
# 设置为 Dumpling 导出数据的路径，如果 Dumpling 执行了多次并分属不同的目录，请将多次导出的数据置放在相同的父目录下并指定此父目录即可。
data-source-dir = "/path/to/source-dir"

[tikv-importer]
# 是否允许向已存在数据的表导入数据。默认值为 false。
# 当使用并行导入模式时，由于多个 TiDB Lightning 实例同时导入一张表，因此此开关必须设置为 true。
parallel-import = true
# "local"：物理导入模式，默认使用。适用于 TB 级以上大数据量，但导入期间下游 TiDB 无法对外提供服务。
# "tidb"：逻辑导入模式。TB 级以下数据量也可以采用，下游 TiDB 可正常提供服务。
backend = "local"

# 设置本地排序数据的路径
sorted-kv-dir = "/path/to/sorted-dir"
```

如果数据源存放在 Amazon S3 或 GCS 等外部存储中，需要额外的连接配置，你可以为这类配置指定参数。如下例子假设数据源存放在 Amazon S3 中：

```
./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
    -d 's3://my-bucket/sql-backup'
```

更多参数设置，请参考[外部存储服务的 URI 格式](/external-storage-uri.md)。

### 第 3 步：开启 TiDB Lightning 进行数据导入

在使用 TiDB Lightning 并行导入时，对每个 TiDB Lightning 节点机器配置的需求与非并行导入模式相同，每个 TiDB Lightning 节点需要消耗相同的资源，建议部署在不同的机器上。详细的部署步骤，请参考 [TiDB Lightning 部署与执行](/tidb-lightning/deploy-tidb-lightning.md)

依次在每台机器上面运行 TiDB Lightning。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

```shell
# !/bin/bash
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

在并行导入的场景下，TiDB Lightning 在启动任务之后，会自动进行下列检查：

- 检查本地盘空间（即 `sort-kv-dir` 配置）以及 TiKV 集群是否有足够空间导入数据，空间大小的详细说明参考 [TiDB Lightning 下游数据库所需空间](/tidb-lightning/tidb-lightning-requirements.md#目标数据库所需空间)和 [TiDB Lightning 运行时资源要求](/tidb-lightning/tidb-lightning-physical-import-mode.md#运行环境需求)。检查时会对数据源进行采样，通过采样结果预估索引大小占比。由于估算中考虑了索引，因此可能会出现尽管数据源大小低于本地盘可用空间，但依然无法通过检测的情况。
- 检查 TiKV 集群的 region 分布是否均匀，以及是否存在大量空 region，如果空 region 的数量大于 max(1000,  表的数量 * 3)，即大于 “1000” 和 “3 倍表数量”二者中的最大者，则无法执行导入。
- 检查数据源导入数据是否有序，并且根据检查结果自动调整 `mydumper.batch-size` 的大小。因此 `mydumper.batch-size` 配置不再对用户开放。

你也可以通过 `lightning.check-requirements` 配置来关闭检查，执行强制导入。更多详细检查内容，可以查看 [Lightning 执行前检查项](/tidb-lightning/tidb-lightning-prechecks.md)。

### 第 4 步：查看进度

开始导入后，可以通过以下任意方式查看进度：

- 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
- 通过监控面板查看进度。详情请参见 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。

等待所有的 TiDB Lightning 运行结束，则整个导入完成。

## 示例 2：使用 TiDB Lightning 并行导入单表数据

TiDB Lightning 也支持并行导入单表的数据。例如，将存放在 Amazon S3 中的多个单表文件，分别由不同的 TiDB Lightning 实例并行导入到下游 TiDB 数据库中。该方法可以加快整体导入速度。关于详细的参数配置，可以参考[外部存储服务的 URI 格式](/external-storage-uri.md)。

> **注意：**
>
> 在本地环境下，可以使用 Dumpling 的 `--filesize` 或 `--where` 参数，预先将单表的数据划分成不同的部分导出至多台机器的本地磁盘，此时依然可以使用并行导入功能，其配置与示例 1 相同。

假设通过 Dumpling 导出的源文件存放在 Amazon S3 云存储中，数据文件为 `my_db.my_table.00001.sql` ~ `my_db.my_table.10000.sql` 共计 10000 个 SQL 文件。如果希望使用 2 个 TiDB Lightning 实例加速导入，则需要在配置文件中增加如下设置：

```
[[mydumper.files]]
# db schema 文件
pattern = '(?i)^(?:[^/]*/)*my_db-schema-create\.sql'
schema = "my_db"
type = "schema-schema"

[[mydumper.files]]
# table schema 文件
pattern = '(?i)^(?:[^/]*/)*my_db\.my_table-schema\.sql'
schema = "my_db"
table = "my_table"
type = "table-schema"

[[mydumper.files]]
# 只导入 00001~05000 这些数据文件并忽略其他文件
pattern = '(?i)^(?:[^/]*/)*my_db\.my_table\.(0[0-4][0-9][0-9][0-9]|05000)\.sql'
schema = "my_db"
table = "my_table"
type = "sql"

[tikv-importer]
# 是否允许向已存在数据的表导入数据。默认值为 false。
# 当使用并行导入模式时，由于多个 TiDB Lightning 实例同时导入一张表，因此此开关必须设置为 true。
parallel-import = true
```

另外一个实例的配置修改为只导入 `05001 ~ 10000` 数据文件即可。

其他步骤请参考示例 1 中的相关步骤。

## 错误处理

### 部分 TiDB Lightning 节点异常终止

在并行导入过程中，如果一个或多个 TiDB Lightning 节点异常终止，需要首先根据日志中的报错明确异常退出的原因，然后根据错误类型做不同处理：

- 如果是正常退出，例如手动 Kill 或内存溢出被操作系统终止等，可以在适当调整配置后直接重启 TiDB Lightning，无须任何其他操作。

- 如果是不影响数据正确性的报错，例如网络超时，请按以下步骤解决：

    1. 在每一个失败的节点上，执行 [checkpoint-error-ignore](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-ignore) 命令，值设置为 `all`，以清除断点续传源数据中记录的错误。

    2. 重启这些异常的节点，从断点位置继续导入。

- 如果在日志中看到影响数据正确性的报错，如 checksum mismatched，表示源文件中有非法的数据，请按以下步骤解决：

    1. 在每一个 Lightning 节点（包括成功导入数据的节点）上执行 [checkpoint-error-destroy](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy) 命令，以清除失败的表中已导入的数据，并将这些表的 checkpoint 状态重置为 "not yet started"。

    2. 使用 [`filter`](/table-filter.md) 参数在所有 TiDB Lightning 节点（包括任务正常结束的节点）上重新配置和导入失败表的数据。重新配置任务时，不要将 checkpoint-error-destroy 命令放在每一个 Lightning 节点的启动脚本中，否则会删除多个并行导入任务使用的共享元数据，可能会导致数据导入过程出现问题。例如，如果启动了第二个 Lightning 导入任务，它将删除第一个数据导入任务写入的元数据，导致数据导入异常。

### 导入过程中报错 "Target table is calculating checksum. Please wait until the checksum is finished and try again"

在部分并行导入场景，如果表比较多或者一些表的数据量比较小，可能会出现当一个或多个任务开始处理某个表的时候，此表对应的其他任务已经完成，并开始数据一致性校验。此时，由于数据一致性校验不支持写入其他数据，对应的任务会返回 "Target table is calculating checksum. Please wait until the checksum is finished and try again" 错误。等校验任务完成，重启这些失败的任务，报错会消失，数据的正确性也不会受影响。
