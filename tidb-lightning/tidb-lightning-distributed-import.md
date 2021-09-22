---
title: TiDB Lightning 分布式并行导入
---

# TiDB Lightning 分布式并行导入

TiDB Lightning 的 Local 后端模式从 v5.1.0 版本开始支持单表的并行导入模式，即同时启动多个 TiDB Lightning 导入数据至单个表中。

TiDB Lightning 并行导入功能通过支持同步启动多个实例并行导入不同的单表或多表的不同数据，使 TiDB Lightning 具备水平扩展的能力，可大大降低导入大量数据所需的时间。

TiDB Lightning 通过在目标 TiDB 中记录各个实例以及每个导入表的元信息，以协调不同实例的 Row ID 分配范围、全局 Checksum 的记录和 TiKV 及 PD 的配置变更与恢复。

> **注意：**
>
> 在使用 Local 后端模式并行导入时，需要确保多个 TiDB Lightning 的数据源之间，以及它们和 TiDB 的目标表中的数据没有主键或者唯一索引的冲突，并且导入的目标表不能有其他应用进行数据写入，否则，TiDB Lightning 将无法保证导入结果的正确性，并且导入完成后相关的数据表将处于数据索引不一致的状态。

## 使用说明

使用 TiDB Lightning 进行并行导入无须额外配置。TiDB Lightning 在启动时会在下游 TiDB 中注册元信息，并自动检测是否有其他的实例向目标集群导入数据，如果存在则自动进入并行导入模式。

## 配置优化

TiDB Lightning 分布式并行的水平扩展性能受每个实例的导入速度和目标集群规模的限制。在通常情况下，建议至少确保目标 TiDB 集群中的 TiKV 实例数量与 TiDB Lightning 的实例数量大于 n:1 (n 为 Region 的副本数量)，以达到最佳的导入性能。

TiDB Lightning 在默认配置下会按照 96 MiB 的大小划分 Region 的大小，但是在并行导入的时候，由于不同的 TiDB Lightning 实例划分的 Region 范围不同，会导致产生大量不足 96 MiB 的 Region，大幅影响导入的性能。为了缓解此问题，建议在并行导入的时候，将此参数调大至 `n * 96 MiB`（n 为最大并行导入单表的 lightning 实例数量）。

```
[tikv-importer]
#  Region 分裂的大小，默认为 96MiB，如果有 5 个 TiDB-Lightning 实例并行导入，则建议调整为 5 * 96MiB = 480MiB
region-split-size = '480MiB'
```

## 使用示例

### 使用 Dumpling + Lightning 合并导入分库分表数据至 TiDB

假设上游为包含 10 个分表的 MySQL 集群，总共大小为 10TB。使用 5 个 TiDB Lightning 实例并行导入，每个实例导入 2 TB 数据，预计可以将总导入时间（不包含 Dumpling 导出的耗时)）由约 40 小时降至约 10 小时。

假设上游的库名为 `my_db`，每个分表的名字为 `my_table_01` ~ `my_table_10`，需要合并导入至下游的 `my_db.my_table` 表中。 具体的操作步骤如下：

#### 第 1 步：使用 Dumpling 导出数据

使用 Dumpling 导出数据的步骤具体请参考 [Dumpling](/dumpling-overview.md) 文档。

> **注意：**
>
> 如果需要导出的多个分表属于同一个上游 MySQL 实例，可以直接使用 Dumpling 的 `-f` 参数一次导出多个分表的结果。如果多个分表分布在不同的 MySQL 实例，可以使用 Dumpling 分两次导出，并将两次导出的结果放置在相同的父目录下即可。

#### 第 2 步：配置 TiDB Lightning 的数据源

创建 `tidb-lightning.toml` 配置文件，并加入如下内容：

```
[lightning]
status-addr = ":8289"

[mydumper]
# 设置为 Dumpling 导出数据的路径，如果 Dumpling 执行了多次并分属不同的目录，请将多次导出的数据置放在相同的父目录下并指定此父目录即可
data-source-dir = "/path/to/source-dir"

[tikv-importer]
# 使用 local 后端
backend = "local"

# 设置本地排序数据的路径
sorted-kv-dir = "/path/to/sorted-dir"

# 调整 region 的大小
region-split-size = '480MiB'

# 设置分库分表合并规则
[[routes]]
schema-pattern = "my_db"
table-pattern = "my_table_*"
target-schema = "my_db"
target-table = "my_table"
``` 

#### 第 3 步：开启 TiDB Lightning 进行数据导入

依次在每台机器上面运行 TiDB Lightning。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

```
# !/bin/bash
nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
```

导入开始后，可以采用以下两种方式查看进度：

- 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
- 通过监控面板查看进度，具体参见 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。

等待所有的 TiDB Lightning 运行结束，则整个导入完成。

### 使用多个 TiDB Lightning 并行导入单表的数据

如果源数据存放于 Amazon S3 等分布式存储中(见 [TiDB Lightning 支持的远端存储](/br/backup-and-restore-storages.md)) ，也可以使用多个 TiDB Lighting 导入不同的文件以加速整体的导入。

假设通过 Dumpling 导出的源文件存放在 Amazon S3 云存储中，数据文件为 `my_db.my_table.00001.sql` ~ `my_db.my_table.10000.sql` 共计 10000 个 SQL 文件。如果希望使用两个 TiDB Lightning 实例加速导入，则可以在配置文件中增加如下设置：

```
[[mydumper.files]]
# db schema 文件
pattern = '(?i)^(?:[^/]*/)my_db-schema-create\.sql'
schema = "my_db"
type = "schema-schema"

[[mydumper.files]]
# table schema 文件
pattern = '(?i)^(?:[^/]*/)my_db\.my_table-schema\.sql'
schema = "my_db"
table = "my_table"
type = "table-schema"

[[mydumper.files]]
# 只导入 00001~05000 这些数据文件并忽略其他文件
pattern = '(?i)^(?:[^/]*/)my_db\.my_table\.(0[0-4][0-9][0-9][0-9]|05000)\.sql'
schema = "my_db"
table = "my_table"
type = "sql"

```

然后另外一个 Lightning 的配置修改为只导入 `05001 ~ 10000` 这些数据文件即可。
