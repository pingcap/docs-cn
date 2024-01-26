---
title: TiDB DDL V2 加速建表
summary: 介绍 TiDB DDL V2 加速建表中的概念、原理、实现和影响。
---

# TiDB DDL V2 加速建表

从 v7.6.0 开始，TiDB DDL 新版本 V2 实现支持加速建表，可提升大批量建表的速度。

在 TiDB 中，对元数据对象的更改采用的是 online DDL 算法（即在线异步变更算法）。所有的 DDL Job 会提交到 `mysql.tidb_ddl_job` 表里，由 owner 节点拉取 DDL Job，执行完 online DDL 算法中的各个阶段后，将该 DDL Job 标记为已完成，移入 `mysql.tidb_ddl_history` 表中。因此 DDL 只能在 owner 节点执行，无法线性拓展。

然而，对于某些 DDL 而言，并不需要严格按照 online DDL 算法执行。如 `CREATE TABLE` 语句，Job 只有 `none` 和 `public` 两个状态，因此可以简化 DDL 的运行流程，使得建表语句可以在非 owner 节点执行，从而实现加速建表。

> **警告：**
>
> TiDB DDL V2 目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 与 TiDB 工具的兼容性

- [TiCDC](/ticdc/ticdc-overview.md) 暂不支持同步通过 TiDB DDL V2 创建的表。

## 限制

TiDB DDL V2 目前仅适用于 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 语句，且该建表语句不带任何外键约束。

## 使用方法

你可以通过设置系统变量 [`tidb_ddl_version`](/system-variables.md#tidb_ddl_version-从-v760-版本开始引入) 的值来开启或关闭 TiDB DDL V2 功能。

要开启该功能，将该变量的值设置为 `2`：

```sql
SET GLOBAL tidb_ddl_version = 2;
```

要关闭该功能，将该变量的值设置为 `1`：

```sql
SET GLOBAL tidb_ddl_version = 1;
```

## 实现原理

TiDB DDL V2 加速建表的实现步骤如下：

1. 创建 `CREATE TABLE` Job。

    此步骤和 V1 版本实现相同，通过解析 `CREATE TABLE` 语句生成相应的 DDL Job。

2. 执行 `CREATE TABLE` Job。

    与 V1 版本将 Job 插入 `mysql.tidb_ddl_job` 表中不同，V2 版本由接收该 `CREATE TABLE` 语句的 TiDB 节点直接执行建表语句，将表结构持久化到 TiKV 中。同时，将 `CREATE TABLE` Job 标记为已完成，插入到 `mysql.tidb_ddl_history` 表中。

3. 同步表信息。

    TiDB 通知其他节点同步该新建的表结构。
