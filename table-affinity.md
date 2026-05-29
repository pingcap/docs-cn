---
title: 表级数据亲和性
summary: 通过为表或分区配置亲和性约束，控制 Region 副本的分布并查看调度状态。
---

# 表级数据亲和性 <span class="version-mark">从 v8.5.5 和 v9.0.0 开始引入</span>

> **警告：**
>
> 该功能为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

表级数据亲和性是 PD 在表级别上的数据分布调度机制，用于控制同一个表或分区中 Region 的 Leader 和 Voter 副本在 TiKV 集群中的分布。

开启 PD 数据亲和性调度，并将表的 `AFFINITY` 选项设置为 `table` 或 `partition` 后，PD 会将同一张表或同一个分区的 Region 归入同一个亲和性分组，并在调度过程中优先将这些 Region 的 Leader 和 Voter 副本放置到相同的少数 TiKV 节点上，从而减少查询过程中跨节点访问带来的网络延迟，提升查询性能。

## 使用限制

使用表级数据亲和性前，请注意以下限制：

- 在 [PD 微服务模式](/pd-microservices.md)下，该功能不会生效。
- [临时表](/temporary-tables.md)和[视图](/views.md)不支持配置数据亲和性。
- 为[分区表](/partitioned-table.md)配置数据亲和性后，**不支持修改该表的分区方案**，包括新增、删除、重组或交换分区。如需调整分区配置，请先移除该表的亲和性设置。
- **数据量较大时需提前评估磁盘容量**：开启数据亲和性后，PD 会优先将表或分区的 Region 调度到相同的少数 TiKV 节点上。对于数据量较大的表或分区，可能导致这些节点的磁盘使用率显著升高。建议提前评估磁盘容量并做好监控。
- 数据亲和性调度仅影响 Leader 和 Voter 副本的分布。如果表有 Learner 副本（如 TiFlash），Learner 副本的分布不受亲和性配置影响。

## 前提条件

PD 亲和性调度特性默认关闭。在设置表或分区的亲和性前，请开启并配置该特性。

1. 将 PD 配置项 [`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-从-v855-和-v900-版本开始引入) 设置为大于 `0` 的值，以开启 PD 的亲和性调度。

    例如，执行以下命令将该配置项设置为 `4`，表示允许 PD 最多同时执行 4 个亲和性调度任务：

    ```bash
    pd-ctl config set schedule.affinity-schedule-limit 4
    ```

2. （可选）根据需要设置 PD 配置项 [`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-从-v855-和-v900-版本开始引入)（默认值为 `256`，单位为 MiB），用于控制属于同一亲和性分组中相邻的小 Region 自动合并的阈值。设置为 `0` 表示关闭亲和性分组中相邻的小 Region 的自动合并。

## 使用方法

本节介绍如何配置表或分区的亲和性，以及如何查看亲和性调度状态。

### 配置表或分区的亲和性

你可以通过 `CREATE TABLE` 或 `ALTER TABLE` 语句中的 `AFFINITY` 选项配置表或分区的亲和性。

| 亲和性等级 | 适用范围 | 效果 |
|---|---|---|
| `AFFINITY='table'` | 非分区表 | 开启该表的亲和性，PD 会为此表的所有 Region 创建一个亲和性分组。 |
| `AFFINITY='partition'` | 分区表 | 开启该表中每个分区的亲和性，PD 会为此表的**每个分区**对应的 Region 分别创建独立的亲和性分组。例如，当表包含 4 个分区时，PD 将为该表创建 4 个相互独立的亲和性分组。 |
| `AFFINITY=''` 或 `AFFINITY='none'` | 已设置 `AFFINITY='table'` 或 `AFFINITY='partition'` 的表 | 关闭该表或分区的亲和性。设置后，PD 会删除对应表或分区的亲和性分组，表或分区的 Region 将不再受到亲和性调度约束。TiKV 上 Region 的自动分裂将在最长 10 分钟内恢复为默认状态。 |

**示例**：

创建非分区表时开启该表的亲和性：

```sql
CREATE TABLE t1 (a INT) AFFINITY = 'table';
```

创建分区表时开启该表中每个分区的亲和性：

```sql
CREATE TABLE tp1 (a INT)
  AFFINITY = 'partition'
  PARTITION BY HASH(a) PARTITIONS 4;
```

为现有非分区表开启亲和性：

```sql
CREATE TABLE t2 (a INT);
ALTER TABLE t2 AFFINITY = 'table';
```

关闭表的亲和性：

```sql
ALTER TABLE t1 AFFINITY = '';
```

### 查看亲和性

可以通过以下方式查看表或分区的亲和性信息：

- 执行 [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md) 语句，在 `Status` 列查看已开启亲和性的表或分区及其调度状态。`Status` 列的值含义如下：

    - `Pending`：PD 尚未对该表或分区进行亲和性调度，比如未确定 Leader 或 Voter 时。
    - `Preparing`：PD 正在调度 Region 以满足亲和性要求。
    - `Stable`：所有 Region 已达到目标分布。

- 查询 [`INFORMATION_SCHEMA.TABLES`](/information-schema/information-schema-tables.md) 表的 `TIDB_AFFINITY` 列查看表的亲和性等级。
- 查询 [`INFORMATION_SCHEMA.PARTITIONS`](/information-schema/information-schema-partitions.md) 表的 `TIDB_AFFINITY` 列查看分区的亲和性等级。

## 注意事项

- **Region 的自动分裂**：当 Region 属于某个亲和性分组且亲和性生效时，Region 默认不会自动分裂，以避免产生过多 Region 影响亲和性效果。只有当 Region 大小超过 [`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-从-v855-和-v900-版本开始引入) 值的四倍时，才会触发自动分裂。需要注意的是，非 TiKV 或 PD 自动触发的 Region 分裂（例如手动执行的 [`SPLIT TABLE`](/sql-statements/sql-statement-split-region.md)）不受此限制。

- **降级与过期机制**：如果亲和性分组中目标 Leader 或 Voter 所在的 TiKV 节点处于不可用状态（例如节点宕机或磁盘空间不足）、Leader 被驱逐，或与现有放置规则发生冲突时，PD 会将该亲和性分组标记为降级状态。在降级期间，对应表或分区的亲和性调度将暂停。

    - 若相关节点在 10 分钟内恢复正常，PD 会继续按照原有亲和性设置进行调度。
    - 若超过 10 分钟仍未恢复，该亲和性分组将被标记为过期。此时 PD 会先恢复常规调度行为（[`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md) 的状态会回到 `Pending`），然后自动更新亲和性分组中的 Leader 和 Voter，以重新启用亲和性调度。

## 相关语句与配置

- [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 和 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) 的 `AFFINITY` 选项
- [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md)
- PD 配置项：[`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-从-v855-和-v900-版本开始引入) 和 [`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-从-v855-和-v900-版本开始引入)