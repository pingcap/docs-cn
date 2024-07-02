---
title: 提升 TiDB 建表性能
summary: 介绍 TiDB 加速建表中的概念、原理、实现和影响。
---

# 提升 TiDB 建表性能

TiDB v7.6.0 引入了系统变量 [`tidb_ddl_version`](https://docs.pingcap.com/zh/tidb/v7.6/system-variables#tidb_ddl_version-从-v760-版本开始引入) 实现支持加速建表，可提升大批量建表的速度。从 v8.0.0 开始，该系统变量更名为 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)。

在 TiDB 中，对元数据对象的更改采用的是 online DDL 算法（即在线异步变更算法）。所有的 DDL Job 会提交到 `mysql.tidb_ddl_job` 表里，由 owner 节点拉取 DDL Job，执行完 online DDL 算法中的各个阶段后，将该 DDL Job 标记为已完成，移入 `mysql.tidb_ddl_history` 表中。因此 DDL 只能在 owner 节点执行，无法线性拓展。

然而，对于某些 DDL 而言，并不需要严格按照 online DDL 算法执行。如 `CREATE TABLE` 语句，Job 只有 `none` 和 `public` 两个状态，因此可以简化 DDL 的运行流程，使得建表语句可以在非 owner 节点执行，从而实现加速建表。

> **警告：**
>
> TiDB 加速建表目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 与 TiDB 工具的兼容性

- [TiCDC](/ticdc/ticdc-overview.md) 暂不支持同步通过 TiDB 加速创建的表。

## 限制

TiDB 加速建表目前仅适用于 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 语句，且该建表语句不带任何外键约束。

## 使用方法

你可以通过设置系统变量 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入) 的值来开启或关闭加速建表的功能。

要开启该功能，将该变量的值设置为 `ON`：

```sql
SET GLOBAL tidb_enable_fast_create_table = ON;
```

要关闭该功能，将该变量的值设置为 `OFF`：

```sql
SET GLOBAL tidb_enable_fast_create_table = OFF;
```

## 实现原理

TiDB 加速建表的实现步骤如下：

1. 创建 `CREATE TABLE` Job。

    通过解析 `CREATE TABLE` 语句生成相应的 DDL Job。

2. 执行 `CREATE TABLE` Job。

    由接收该 `CREATE TABLE` 语句的 TiDB 节点直接执行建表语句，将表结构持久化到 TiKV 中。同时，将 `CREATE TABLE` Job 标记为已完成，插入到 `mysql.tidb_ddl_history` 表中。

3. 同步表信息。

    TiDB 通知其他节点同步该新建的表结构。
