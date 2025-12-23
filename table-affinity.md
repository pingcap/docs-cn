---
title: 表级数据亲和性
summary: 通过表或分区的亲和性约束，控制 Region 的副本分布并查看调度状态。
---

# 表级数据亲和性 <span class="version-mark">实验特性，自 v8.5.5 起提供</span>

> **警告：**
>
> 该功能为实验特性，不建议在生产环境中使用。行为和接口可能在未来版本变更或移除。如遇问题，请在 GitHub 提交 [issue](https://github.com/pingcap/tidb/issues) 反馈。

表级数据亲和性用于将表或分区的 Region 归为同一亲和性分组，并让 PD 将这些 Region 的 Leader、Voter 优先调度到指定的 Store 上，减少跨节点分散带来的延迟。亲和性信息由 PD 维护，TiDB 通过 `AFFINITY` 表选项声明亲和性级别。

## 前置条件

- 集群版本：TiDB/PD/TiKV 均需为 v8.5.5 及以上的相互兼容版本。
- 在 PD 侧开启调度：将 `schedule.affinity-schedule-limit` 设置为大于 0，否则亲和性调度不会生效。示例：

  ```bash
  pd-ctl config set schedule.affinity-schedule-limit 4
  ```

- 可选：根据需要设置 `schedule.max-affinity-merge-region-size`（MiB），控制亲和性 Region 的合并阈值，设置为 `0` 表示关闭亲和性场景下的自动合并。

## 支持的亲和性级别

- 非分区表：`AFFINITY='table'`。
- 分区表：`AFFINITY='partition'`，每个分区会生成独立的亲和性分组。
- 取消亲和性：设置为 `AFFINITY=''` 或 `AFFINITY='none'`。
- 不支持在临时表、视图上开启亲和性。

## 基本用法

1. **创建或修改表时声明亲和性**

   ```sql
   CREATE TABLE t1 (a INT) AFFINITY = 'table';

   CREATE TABLE tp1 (a INT)
     AFFINITY = 'partition'
     PARTITION BY HASH(a) PARTITIONS 4;

   ALTER TABLE t1 AFFINITY = 'table';     -- 开启
   ALTER TABLE t1 AFFINITY = '';          -- 关闭
   ```

   开启后，TiDB 会在 PD 中为表或分区自动创建亲和性分组，并向 PD 维护对应的 key range。

2. **查看调度状态**

   - `SHOW AFFINITY;` 展示当前已开启亲和性的表或分区及其在 PD 中记录的目标副本分布。`STATUS` 含义：
     - `Pending`：PD 尚未开始进行亲和性调度（比如未确定 Leader/Voter）。
     - `Preparing`：正在调度 Region 以满足亲和性要求。
     - `Stable`：所有 Region 已达到目标分布。
   - INFORMATION_SCHEMA 也会暴露亲和性信息：
     - `TABLES.TIDB_AFFINITY`：表级亲和性。
     - `PARTITIONS.TIDB_AFFINITY`：分区级亲和性。

## 调度行为与内部机制

- **自动分裂拦截**：当 Region 属于亲和性分组，- 亲和性生效时，Region 默认不进行自动分裂（除非大小或 key 数超过阈值），避免产生过多 Region 影响亲和性效果。手工 `ADMIN SPLIT` 不受此限制。
- **降级与过期**：若分组目标的 Leader/Voter 所在 Store 不可用（如节点 down 、磁盘不足等），PD 会将分组标记为降级。若 10 分钟内未恢复，将自动过期并允许常规调度；此时亲和性调度暂停，`SHOW AFFINITY` 的状态会回到 `Pending`。恢复后可重新更新分组的 Leader/Voter 以重新启用亲和性。

## 限制与注意事项

- 开启亲和性后，**不支持修改分区方案**（如新增/删除/重组/交换分区）。如需调整分区，请先移除亲和性。
- 临时表、视图不支持亲和性。
- **数据量较大时需注意磁盘空间**：开启亲和性后，PD 会将表或分区的 Region 调度到指定的少数 Store 上。如果表数据量较大，可能导致这些 Store 的磁盘占用显著增加，需提前评估磁盘容量并做好监控。
- 亲和性调度依赖 PD 调度参数：
  - `schedule.affinity-schedule-limit` 默认 0（关闭）。需显式配置后，PD 才会为亲和性分组创建调度任务。
  - `schedule.max-affinity-merge-region-size` 为亲和性 Region 的合并阈值；设置为 0 关闭亲和性合并。
- 亲和性生效时，小于阈值的 Region 默认不进行自动分裂，手工 `ADMIN SPLIT` 仍可执行。
- 不支持 Learner 副本的亲和性调度：如果表配置了包含 Learner 副本的放置规则（比如 TiFlash），亲和性调度不会对 Learner 副本生效，但不影响现有 Learner 副本的分布。
- 当目标 Store 处于不可用、被驱逐 Leader、或与放置规则冲突时，PD 会将分组标记为降级或过期，亲和性调度暂停。恢复后可通过 `SHOW AFFINITY` 观察状态，必要时重新更新分组的 Leader/Voter。

## 相关语句与配置

- `CREATE TABLE` / `ALTER TABLE` 的 `AFFINITY` 选项。
- `SHOW AFFINITY` 语句。
- PD 调度参数：`schedule.affinity-schedule-limit`、`schedule.max-affinity-merge-region-size`。
