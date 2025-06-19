---
title: SHARD_ROW_ID_BITS
summary: 了解 SHARD_ROW_ID_BITS 属性。
---

# SHARD_ROW_ID_BITS

本文档介绍 `SHARD_ROW_ID_BITS` 表属性，该属性用于设置隐式 `_tidb_rowid` 分片后的分片位数。

## 概念

对于非聚簇主键或没有主键的表，TiDB 使用隐式自增行 ID。当执行大量 `INSERT` 操作时，数据会写入单个 Region，导致写入热点。

为了缓解热点问题，您可以配置 `SHARD_ROW_ID_BITS`。行 ID 会被打散，数据会写入多个不同的 Region。

- `SHARD_ROW_ID_BITS = 4` 表示 16 个分片
- `SHARD_ROW_ID_BITS = 6` 表示 64 个分片
- `SHARD_ROW_ID_BITS = 0` 表示默认 1 个分片

<CustomContent platform="tidb">

有关使用详情，请参阅[热点问题处理指南](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)。

</CustomContent>

<CustomContent platform="tidb-cloud">

有关使用详情，请参阅[热点问题处理指南](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#use-shard_row_id_bits-to-process-hotspots)。

</CustomContent>

## 示例

```sql
CREATE TABLE t (
    id INT PRIMARY KEY NONCLUSTERED
) SHARD_ROW_ID_BITS = 4;
```

```sql
ALTER TABLE t SHARD_ROW_ID_BITS = 4;
```
