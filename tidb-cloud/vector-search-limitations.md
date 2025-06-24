---
title: 向量搜索限制
summary: 了解 TiDB 向量搜索的限制。
---

# 向量搜索限制

本文介绍 TiDB 向量搜索的已知限制。

> **注意**
>
> TiDB 向量搜索仅适用于 TiDB Self-Managed（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

## 向量数据类型限制

- 每个[向量](/tidb-cloud/vector-search-data-types.md)最多支持 16383 维。
- 向量数据类型不能存储 `NaN`、`Infinity` 或 `-Infinity` 值。
- 向量数据类型不能存储双精度浮点数。如果你在向量列中插入或存储双精度浮点数，TiDB 会将它们转换为单精度浮点数。
- 向量列不能用于主键、唯一索引或分区键。要加速向量搜索性能，请使用[向量搜索索引](/tidb-cloud/vector-search-index.md)。
- 一个表可以有多个向量列。但是，[单个表中的列总数有限制](/tidb-limitations.md#limitations-on-a-single-table)。
- 目前，TiDB 不支持删除带有向量索引的向量列。要删除这样的列，请先删除向量索引，然后再删除向量列。
- 目前，TiDB 不支持将向量列修改为其他数据类型，如 `JSON` 和 `VARCHAR`。

## 向量索引限制

- 向量索引用于向量搜索。它不能加速其他查询，如范围查询或相等查询。因此，不能在非向量列上或多个向量列上创建向量索引。
- 一个表可以有多个向量索引。但是，[单个表中的索引总数有限制](/tidb-limitations.md#limitations-on-a-single-table)。
- 仅当使用不同的距离函数时，才允许在同一列上创建多个向量索引。
- 目前，向量索引的距离函数仅支持 `VEC_COSINE_DISTANCE()` 和 `VEC_L2_DISTANCE()`。
- 目前，TiDB 不支持删除带有向量索引的向量列。要删除这样的列，请先删除向量索引，然后再删除向量列。
- 目前，TiDB 不支持将向量索引设置为[不可见](/sql-statements/sql-statement-alter-index.md)。

## 与 TiDB 工具的兼容性

- TiDB Cloud 控制台中的数据迁移功能不支持将 MySQL 9.0 向量数据类型迁移或复制到 TiDB Cloud。

## 反馈

我们重视你的反馈，随时为你提供帮助：

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)
