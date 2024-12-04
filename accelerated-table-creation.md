---
title: 提升 TiDB 建表性能
summary: 介绍 TiDB 加速建表中的概念、原理、实现和影响。
aliases: ['/zh/tidb/dev/ddl-v2/']
---

# 提升 TiDB 建表性能

TiDB v7.6.0 引入了系统变量 [`tidb_ddl_version`](https://docs.pingcap.com/zh/tidb/v7.6/system-variables#tidb_ddl_version-从-v760-版本开始引入) 实现支持加速建表，可提升大批量建表的速度。从 v8.0.0 开始，该系统变量更名为 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)。

通过 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入) 系统变量开启加速建表后，同时提交到同一个 TiDB 节点的相同 schema 的建表语句会被合并为批量建表语句，以提高建表性能。因此为了提高建表性能，需要尽量连接相同的 TiDB 节点并发创建同一个 schema 下的表，并适当提高并发度。

合并后的批量建表语句在同一个事务内执行，如果其中一个语句失败，所有语句都会失败。

## 与 TiDB 工具的兼容性

- 在 TiDB v8.3.0 之前的版本中，[TiCDC](/ticdc/ticdc-overview.md) 不支持同步通过 TiDB 加速创建的表。从 v8.3.0 开始，TiCDC 可以正常同步这类表。

## 限制

TiDB 加速建表目前仅适用于 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 语句，且该建表语句不带任何外键约束。

## 使用方法

你可以通过设置系统变量 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入) 的值来开启或关闭加速建表的功能。

从 TiDB v8.5.0 开始，新创建的集群默认开启 TiDB 加速建表功能，即 `tidb_enable_fast_create_table` 默认值为 `ON`。如果从 v8.4.0 及之前版本的集群升级至 v8.5.0 及之后的版本，`tidb_enable_fast_create_table` 的默认值不发生变化。

要开启该功能，将该变量的值设置为 `ON`：

```sql
SET GLOBAL tidb_enable_fast_create_table = ON;
```

要关闭该功能，将该变量的值设置为 `OFF`：

```sql
SET GLOBAL tidb_enable_fast_create_table = OFF;
```
