---
title: IMPORT INTO 和 TiDB Lightning 对比
summary: 了解 `IMPORT INTO` 和 TiDB Lightning 的差异。
---

# IMPORT INTO 和 TiDB Lightning 对比

许多用户反馈 [TiDB Lightning](/tidb-lightning/tidb-lightning-configuration.md) 的部署、配置、维护比较复杂，特别是在处理大数据量[并行导入](/tidb-lightning/tidb-lightning-distributed-import.md)的场景中。

针对此问题，TiDB 逐渐将 TiDB Lightning 的一些功能整合到 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 语句中。你可以直接通过执行 `IMPORT INTO` 导入数据，从而提升导入数据的效率。此外，`IMPORT INTO` 支持某些 TiDB Lightning 不支持的功能，例如自动分布式任务调度和 [TiDB 全局排序](/tidb-global-sort.md)。

`IMPORT INTO` 在 v7.2.0 中引入，在 v7.5.0 成为正式功能 (Generally Available, GA)，并会在未来版本中继续完善优化。一旦 `IMPORT INTO` 能够完全取代 TiDB Lightning，TiDB Lightning 将会被废弃。到时候会在 TiDB Release Notes 和文档中提前发布相关通知。

## `IMPORT INTO` 和 TiDB Lightning 对比

以下章节介绍了 `IMPORT INTO` 和 TiDB Lightning 在多个维度的差异。

### 部署成本

#### `IMPORT INTO`

`IMPORT INTO` 无需单独部署。你可以直接在 TiDB 节点上执行，从而省去了不必要的部署工作。

#### TiDB Lightning

相比之下，TiDB Lightning 需要进行[单独部署](/tidb-lightning/deploy-tidb-lightning.md)。

### 资源使用

#### `IMPORT INTO`

`IMPORT INTO` 任务可以与其它业务负载共享 TiDB 节点的资源，或者错峰使用这些节点以充分利用资源。为实现以最优性能保持业务稳定运行，同时保证 `IMPORT INTO` 任务的性能和稳定性，你可以指定[特定的 TiDB 节点](/system-variables.md#tidb_service_scope-从-v740-版本开始引入)，专门用于使用 `IMPORT INTO` 导入数据。

当使用 [TiDB 全局排序](/tidb-global-sort.md)时，你无需加载太大的本地磁盘。TiDB 全局排序可以使用 Amazon S3 作为存储。一旦完成数据导入，存储在 Amazon S3 上用于全局排序的数据会自动删除，以节省存储成本。

#### TiDB Lightning

你需要单独的服务器部署和运行 TiDB Lightning。不执行数据导入任务时，这些资源处于闲置状态。在周期性的导入数据的场景中，闲置的时间会更长，造成资源浪费。

如果导入的数据量大，还需要准备较大的本地磁盘对导入的数据进行排序。

### 任务配置和集成

#### `IMPORT INTO`

你可以直接编写 SQL 语句来提交导入任务，方便调用和集成。

#### TiDB Lightning

相比之下，TiDB Lightning 需要你编写[配置文件](/tidb-lightning/tidb-lightning-configuration.md)，非常复杂，而且不便于第三方软件调用。

### 任务调度

#### `IMPORT INTO`

`IMPORT INTO` 支持分布式执行。例如，当你需要将 40 TiB 的源数据文件导入到一张目标表时，在提交了 SQL 语句之后，TiDB 会自动将导入任务拆分成多个子任务，然后调度不同的 TiDB 节点分布式执行这些子任务。

#### TiDB Lightning

相比之下，TiDB Lightning 的配置复杂、低效且容易出错。

假设你需要启动 10 个 TiDB Lightning 实例并行导入数据，那么你需要编写 10 个 TiDB Lightning 配置文件，并在每个配置文件中配置对应 TiDB Lightning 实例读取的源文件范围。例如，TiDB Lightning 实例 1 读取前 100 个文件，实例 2 读取接下来的 100 个文件，依此类推。

此外，你还需要为这 10 个 TiDB Lightning 实例配置共享元数据表和其他配置信息。配置相对复杂和繁琐。

### 全局排序与本地排序

#### `IMPORT INTO`

基于 TiDB 全局排序，`IMPORT INTO` 可以将几十 TiB 的源数据传输到多个 TiDB 节点，编码数据 KV 对和索引 KV 对，并传输到 Amazon S3 对这些 KV 对进行全局排序，然后写入到 TiKV。

由于这些 KV 对是全局排序过的，因此从各个 TiDB 节点导入到 TiKV 的数据不会重叠，可以直接将其写入到 RocksDB 中。这样就不需要 TiKV 执行 Compaction 操作，从而显着提升写入 TiKV 的性能和稳定性。

导入完成后，Amazon S3 上用于全局排序的数据将自动删除，节省存储成本。

#### TiDB Lightning

TiDB Lightning 仅支持本地排序。例如，对于几十 TiB 的源数据，如果 TiDB Lightning 没有配置大的本地磁盘，或者使用多个 TiDB Lightning 实例并行导入，则每个 TiDB Lightning 实例只会使用本地磁盘对待导入的数据进行排序。由于无法进行全局排序，多个 TiDB Lightning 实例导入到 TiKV 的数据之间会出现重叠，尤其是索引数据较多的场景，这将会触发 TiKV 进行 Compaction 操作。Compaction 操作非常消耗资源，会导致 TiKV 的写入性能和稳定性下降。

如果后续还要继续导入数据，你需要继续保留 TiDB Lightning 服务器以及该服务器上的磁盘，以供下次导入使用。与 `IMPORT INTO` 使用 Amazon S3 按需付费的方式相比，使用 TiDB Lightning 成本相对较高。

### 性能

目前，还没有 `IMPORT INTO` 和 TiDB Lightning 在同等测试环境下的性能测试对比结果。

使用 Amazon S3 作为全局排序的存储时，`IMPORT INTO` 性能测试结果如下：

| 源数据集                         | 节点配置                                       | 单个 TiDB 节点平均导入速度    |
|---------------------------------|----------------------------------------------|----------------------------|
| 40 TiB 数据（22.6 亿行，单行大小 19 KiB） | 10 个 TiDB (16C32G) 节点和 20 个 TiKV (16C27G) 节点  | 222 GiB/h        |
| 10 TiB 数据（5.65 亿行，单行大小 19 KiB） | 5 个 TiDB (16C32G) 节点和 10 个 TiKV (16C27G) 节点  | 307 GiB/h        |

### 高可用性

#### `IMPORT INTO`

当某个 TiDB 节点发生故障后，该节点上的任务会自动转移到其它 TiDB 节点上继续运行。

#### TiDB Lightning

TiDB Lightning 实例节点出现故障后，需要根据之前记录的检查点在新节点上手动恢复任务。

### 可扩展性

#### `IMPORT INTO`

由于使用全局排序，导入 TiKV 的数据不会重叠，与 TiDB Lightning 相比，具有更好的可扩展性。

#### TiDB Lightning

由于仅支持本地排序，添加 TiDB Lightning 实例时导入 TiKV 的数据可能会重叠，导致 TiKV 需要更多的压缩操作，与 `IMPORT INTO` 相比，可扩展性受到限制。

## `IMPORT INTO` 不支持的特性

目前，`IMPORT INTO` 还缺少一些特性，在部分场景无法替代 TiDB Lightning，例如：

- 逻辑导入

    在使用 `IMPORT INTO` 导入数据之前，目标表必须为空。如果需要将数据导入到已经包含数据的表中，建议使用 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) 或直接插入等方法。从 v8.0 起，TiDB 支持[批量 DML](/system-variables.md#tidb_dml_type-从-v800-版本开始引入) 来执行大型事务。

- 冲突数据处理

    `IMPORT INTO` 目前不支持冲突数据处理。在导入数据前，你需要正确定义表结构，且保证导入的数据不存在主键或唯一键冲突，否则可能会导致任务失败。

- 将数据导入多个目标表

    目前，一个 `IMPORT INTO` 语句仅允许导入数据到一个目标表。如果要将数据导入到多个目标表中，则需要提交多个 `IMPORT INTO` 语句。

在未来的版本中，`IMPORT INTO` 计划将支持这些功能，并对功能进行其他增强，例如允许在任务执行期间修改并发性以及调整写入 TiKV 的吞吐量，让你更方便地管理任务。

## 总结

与 TiDB Lightning 相比，`IMPORT INTO` 语句可以直接在 TiDB 节点上执行，支持自动化分布式任务调度和 [TiDB 全局排序](/tidb-global-sort.md)，在部署、资源利用率、任务配置便捷性、调用集成便捷性、高可用性和可扩展性等方面都有很大提升。建议在合适的场景下，使用 `IMPORT INTO` 代替 TiDB Lightning。
