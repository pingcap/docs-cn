---
title: sys Schema
summary: 了解 TiDB `sys` 系统数据库。
---

# `sys` Schema

TiDB 从 v8.0.0 开始提供 `sys` Schema。你可以通过查看 `sys` 系统数据库中的表或视图理解 TiDB 的系统表、[`INFORMATION_SCHEMA`](/information-schema/information-schema.md) 表和 [`PERFORMANCE SCHEMA`](/performance-schema/performance-schema.md) 表内的数据。

## 与 MySQL 兼容的表

| 表名                                                                  | 描述                        |
|---------------------------------------------------------------------|---------------------------|
| [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) | 记录自 TiDB 上次启动以来未被使用的索引信息。 |
