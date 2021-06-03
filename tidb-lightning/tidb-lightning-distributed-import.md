---
title: TiDB Lightning 分布式导入
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-distributed-import/','/docs-cn/dev/reference/tools/tidb-lightning/distributed-import/']
---

# TiDB Lightning 分布式导入

从 v5.1.0 版本开始，TiDB Lightning Local Backend 增加如下功能的支持:

- 增量导入。支持导入新数据至已存在数据的表
- 分布式并行导入。支持同时启动多个 TiDB Lightning 导入数据至单个表中

> **注意：**
>
> 在使用 Local-Backend 增量导入或分布式导入时，都需要确保多个 TiDB Lightning 的数据源直接以及他们和 TiDB 的目标表中的数据没有主键或者唯一索引的冲突。否则，TiDB Lightning 将无法保证导入结果的正确性，并且导入完成后相关的数据表将处于数据索引不一致的状态。

## 增量导入

TiDB Lightning 会自动调整 ID 分配器的基准值以确保为设置 AUTO_INCREMENT 等类型的字段分配的值不会重复。同时，在开始导入之前，如果 TiDB Lightning 发现目标表中包含数据，则会首先执行一次 Checksum, 确保最终 Checksum 结果的正确性。

TiDB Lightning 总是会会检测目标表中是否包含数据，如果包含，则会自动切换至增量导入模式，因此无须执行任何操作即可使用此功能。

## 分布式并行导入

TiDB Lightning 分布式导入功能通过支持同步启动多个实例并行导入不同的单表或多表的不同数据，使 TiDB Lightning 具备水平扩展的能力，可大大降低导入的大量数据所需的时间。

TiDB Lightning 通过在目标 TiDB 中记录各个实例以及每个导入表的元信息，以协调不同实例的 Row ID 分配范围、全局 Checksum 的记录和 TiKV及PD 的配置变更与恢复。

### 使用说明

并行导入无须额外的配置，TiDB Lightning 在启动时会在下游 TiDB 中注册元信息，并自动检测是否有其他的实例向目标集群导入数据，如果存在则自动进入并行导入模式，无须做任何手动配置。

### 配置优化

TiDB Lightning 分布式并行的水平扩展性能受每个实例的导入速度和目标集群规模的限制。在通常情况下，建议至少确保目标 TiDB 集群中的 TiKV 实例数量与 TiDB Lightning 的实例数量大于 n:1 (n 为 Region 的副本数量)，以达到最佳的导入性能。

同时如果存在需要使用多个 TiDB Lightning 并行导入的单个表的数据，请调整如何配置：
```
[tikv-importer]
# 如果有多个 TiDB Lightning 导入相同的表，则按比例增大此设置。例如，需要启动 5 个示例导入相同表的数据，则设置为 480MiB 
region-split-size = '96MiB'
```

# 使用场景

## 使用 Dumpling + Lightning 合并导入分库分表数据至 TiDB

假设上游为包含 10 个分表的 MySQL 集群，总共大小为 10TB。使用 5 * TiDB Lightning 并行导入，每个实例导入 2TB 数据，预计可以将总导入时间(不包含 dumpling 导出的耗时) 由约 40 小时降至约 10 小时。

假设上游的库名为 `my_db`, 每个分表的名字为 `my_table_01` ~ `my_table_10`, 需要合并导入至下游的 `my_db.my_table` 表中。 具体的操作步骤如下：

### 第 1 步：使用 dumpling 导出数据

使用 Dumpling 导出数据的步骤具体请参考 [Dumpling](/dumpling-overview.md) 文档。

> **注意：**
>
> 如果需要导出的多个分表属于同一个上游 MySQL 集群，可以直接使用 dumpling 的 -f 参数一次导出多个分表的结果。如果多个分表分布在不同的集群，可以使用 dumpling 分两次导出，并将两次导出的结果放置在相同的父目录下即可。

### 第 2 步：配置 TiDB Lightning 的数据源

创建 tidb-lightning.toml 配置文件，并加入如下内容：

```
[lightning]
status-addr = ":8289"

[mydumper]
# 设置为 dumpling 导出数据的路径，如果dumpling 执行了多次并分属不同的目录，请将多次导出的数据置放在相同的父目录下并指定此父目录即可
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

### 第 3 步：开启 TiDB Lightning 进行数据导入

依次在每台机器上面运行 TiDB Lightning。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

```
# !/bin/bash
nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
```

导入开始后，可以采用以下两种方式查看进度：

- 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
- 通过监控面板查看进度，具体参见 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。

等待所有的 TiDB Lightning 运行结束，则整个导入完成。

## 使用多个 TiDB Lightning 并行导入单表的数据

如果源数据存放于 Amazon S3 等分布式存储中(见 [TiDB Lightning 支持的远端存储](/br/backup-and-restore-storages.md)) ，也可以使用多个 TiDB Lighting 导入不同的文件以加速整体的导入。

假设通过 dumpling 导出的源文件存放在 Amazon S3 云存储中，数据文件为 `my_db.my_table.00001.sql` ~ `my_db.my_table.10000.sql` 共计 10000 个 SQL 文件。如果希望使用两个 TiDB Lightning 实例加速导入，则可以在配置文件中增加如下设置：

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
