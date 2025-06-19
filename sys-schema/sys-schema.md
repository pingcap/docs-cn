---
title: sys Schema
summary: 了解 `sys` schema 中的系统表。
---

# `sys` Schema

从 v8.0.0 开始，TiDB 提供了 `sys` schema。你可以使用 `sys` schema 中的视图来了解 TiDB 系统表、[`INFORMATION_SCHEMA`](/information-schema/information-schema.md) 和 [`PERFORMANCE SCHEMA`](/performance-schema/performance-schema.md) 中的数据。

## MySQL 兼容性表

| 表名                                                                                       | 描述                                               |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)                                  | 记录自 TiDB 上次启动以来未被使用过的索引。 |
