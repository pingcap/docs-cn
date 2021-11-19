---
title: SHARD_ROW_ID_BITS
summary: 介绍 TiDB 的 `SHARD_ROW_ID_BITS` 表属性。
---

# SHARD_ROW_ID_BITS

本文介绍表属性 `SHARD_ROW_ID_BITS`，它用来设置隐式 `_tidb_rowid` 分片数量的 bit 位数。

## 基本概念

对于非整数主键或没有主键的表，TiDB 会使用一个隐式的自增 rowid。大量执行 `INSERT` 插入语句时会把数据集中写入单个 Region，造成写入热点。

通过设置 `SHARD_ROW_ID_BITS`，可以把 rowid 打散写入多个不同的 Region，缓解写入热点问题。但是设置的过大会造成 RPC 请求数放大，增加 CPU 和网络开销。

- `SHARD_ROW_ID_BITS = 4` 表示 16 个分片
- `SHARD_ROW_ID_BITS = 6` 表示 64 个分片
- `SHARD_ROW_ID_BITS = 0` 表示默认值 1 个分片

## 语句示例

- `CREATE TABLE`: `CREATE TABLE t (c int) SHARD_ROW_ID_BITS = 4;`
- `ALTER TABLE`: `ALTER TABLE t SHARD_ROW_ID_BITS = 4;`
