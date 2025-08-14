---
title: SHARD_ROW_ID_BITS
summary: 介绍 TiDB 的 `SHARD_ROW_ID_BITS` 表属性。
---

# SHARD_ROW_ID_BITS

本文介绍表属性 `SHARD_ROW_ID_BITS`，它用来设置隐式 `_tidb_rowid` 分片数量的 bit 位数。

## 基本概念

对于非[聚簇索引](/clustered-indexes.md)主键或没有主键的表，TiDB 会使用一个隐式的自增 rowid。大量执行 `INSERT` 插入语句时会把数据集中写入单个 Region，造成写入热点。

通过设置 `SHARD_ROW_ID_BITS`，可以把 rowid 打散写入多个不同的 Region，缓解写入热点问题。

- `SHARD_ROW_ID_BITS = 4` 表示 16 个分片
- `SHARD_ROW_ID_BITS = 6` 表示 64 个分片
- `SHARD_ROW_ID_BITS = 0` 表示默认值 1 个分片

设置 `SHARD_ROW_ID_BITS = S` 时，`_tidb_rowid` 的具体结构如下：

| 符号位 | 分片位 | 自增位       |
|--------|--------|--------------|
| 1 bit | `S` bits | `63-S` bits |

- 自增位的值保存在 TiKV 中，由 TiDB 按顺序分配，每次分配后值会自增 1。自增位确保了 `_tidb_rowid` 列的值全局唯一。当自增位的值耗尽后（即达到最大值时），再次自动分配时会报 `Failed to read auto-increment value from storage engine` 错误。
- 关于 `_tidb_rowid` 取值范围：最终生成值包含的最大位数 = 分片位 + 自增位，最大值为 `(2^63)-1`。

> **注意：**
>
> 分片位长度 (`S`) 的选取：
>
> - 由于 `_tidb_rowid` 总位数为 64 位，分片位的数量会影响自增位的数量：当分片位数增加时，自增位数会减少，反之亦然。因此，你需要权衡“自动分配值的随机性”以及“可用自增空间”。
> - 最佳实践是将分片位设置为 `log(2, x)`，其中 `x` 为当前集群中 TiKV 节点的数量。例如，如果一个 TiDB 集群中存在 16 个 TiKV 节点，分片位推荐设置为 `log(2, 16)`，即 `4`。在所有 Region 被均匀调度到各个 TiKV 节点后，此时大批量写入操作的负载可被均匀分布到不同 TiKV 节点，以实现资源最大化利用。

关于 `SHARD_ROW_ID_BITS` 的更多使用信息，可参考[使用 SHARD_ROW_ID_BITS 处理热点表](/troubleshoot-hot-spot-issues.md#使用-shard_row_id_bits-处理热点表)。

## 语句示例

```sql
CREATE TABLE t (
    id INT PRIMARY KEY NONCLUSTERED
) SHARD_ROW_ID_BITS = 4;
```

```sql
ALTER TABLE t SHARD_ROW_ID_BITS = 4;
```
