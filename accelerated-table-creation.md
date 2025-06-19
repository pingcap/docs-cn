---
title: TiDB 加速表创建
aliases: ['/tidb/stable/ddl-v2/']
summary: 了解 TiDB 中创建表的性能优化的概念、原理和实现细节。
---

# TiDB 加速表创建

TiDB v7.6.0 引入了系统变量 [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_enable_fast_create_table-new-in-v800) 以支持加速表创建，提高批量创建表的效率。从 v8.0.0 开始，该系统变量被重命名为 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)。

TiDB 使用在线异步 schema 变更算法来更改元数据。所有 DDL 任务都提交到 `mysql.tidb_ddl_job` 表中，由 owner 节点拉取 DDL 任务执行。在执行完在线 DDL 算法的每个阶段后，DDL 任务被标记为完成并移动到 `mysql.tidb_ddl_history` 表中。因此，DDL 语句只能在 owner 节点上执行，无法线性扩展。

然而，对于某些 DDL 语句，不需要严格遵循在线 DDL 算法。例如，`CREATE TABLE` 语句的任务只有 `none` 和 `public` 两个状态。因此，TiDB 可以简化 DDL 的执行过程，在非 owner 节点上执行 `CREATE TABLE` 语句以加速表创建。

> **警告：**
>
> 该功能目前是实验性功能，不建议在生产环境中使用。该功能可能会在没有事先通知的情况下发生变更或被移除。如果发现 bug，请通过在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues) 来反馈。

## 与 TiDB 工具的兼容性

- [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) 不支持复制通过 `tidb_enable_fast_create_table` 创建的表。

## 限制

目前，表创建性能优化仅支持 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 语句，且该语句不能包含任何外键约束。

## 使用 `tidb_enable_fast_create_table` 加速表创建

你可以通过指定系统变量 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) 的值来启用或禁用表创建性能优化。

要启用表创建性能优化，将该变量的值设置为 `ON`：

```sql
SET GLOBAL tidb_enable_fast_create_table = ON;
```

要禁用表创建性能优化，将该变量的值设置为 `OFF`：

```sql
SET GLOBAL tidb_enable_fast_create_table = OFF;
```

## 实现原理

表创建性能优化的详细实现原理如下：

1. 创建 `CREATE TABLE` 任务。

   通过解析 `CREATE TABLE` 语句生成相应的 DDL 任务。

2. 执行 `CREATE TABLE` 任务。

   接收 `CREATE TABLE` 语句的 TiDB 节点直接执行该语句，然后将表结构持久化到 TiKV。同时，将 `CREATE TABLE` 任务标记为完成并插入到 `mysql.tidb_ddl_history` 表中。

3. 同步表信息。

   TiDB 通知其他节点同步新创建的表结构。
