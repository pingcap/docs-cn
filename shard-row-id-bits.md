---
title: SHARD_ROW_ID_BITS
summary: Learn the SHARD_ROW_ID_BITS attribute.
---

# SHARD_ROW_ID_BITS

This document introduces the `SHARD_ROW_ID_BITS` table attribute, which is used to set the number of bits of the shards after the implicit `_tidb_rowid` is sharded.

## Concept

For the tables with a non-clustered primary key or no primary key, TiDB uses an implicit auto-increment row ID. When a large number of `INSERT` operations are performed, the data is written into a single Region, causing a write hot spot.

To mitigate the hot spot issue, you can configure `SHARD_ROW_ID_BITS`. The row IDs are scattered and the data are written into multiple different Regions.

- `SHARD_ROW_ID_BITS = 4` indicates 16 shards
- `SHARD_ROW_ID_BITS = 6` indicates 64 shards
- `SHARD_ROW_ID_BITS = 0` indicates the default 1 shard

<CustomContent platform="tidb">

For details on the usage, see [the Troubleshoot Hotspot Issues guide](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots).

</CustomContent>

<CustomContent platform="tidb-cloud">

For details on the usage, see [the Troubleshoot Hotspot Issues guide](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#use-shard_row_id_bits-to-process-hotspots).

</CustomContent>

## Examples

```sql
CREATE TABLE t (
    id INT PRIMARY KEY NONCLUSTERED
) SHARD_ROW_ID_BITS = 4;
```

```sql
ALTER TABLE t SHARD_ROW_ID_BITS = 4;
```
