---
title: TTL 支持
summary: 介绍如何通过 SQL 来管理表数据的生命周期
---

# TTL 支持

TTL 提供了行级别的生命周期控制策略。在 TiDB 中，设置了 TTL 属性的表会根据配置自动删除过期的数据来防止存储空间的无限增长。此功能在一些场景很有用，比如：定期删除验证码记录等。

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

## 语法

你可以通过 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 或 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) 语句来配置表的 TTL 功能。

### 创建具有 TTL 属性的表

可以通过以下语句创建一个具有 TTL 属性的表：

```sql
CREATE TABLE t1 (
    id int PRIMARY KEY,
    created_at TIMESTAMP
) TTL = `created_at` + INTERVAL 3 MONTH;
```

上面的例子创建了一张表 `t1`， 并指定了 `created_at` 为 TTL 的时间列，表示数据的创建时间。同时，它还通过 `INTERVAL 3 MONTH` 设置了表中行的最长存活时间为 3 个月。超过了此时长的过期数据会在之后被删除。

在创建表的时候，你也可以额外设置 `TTL_ENABLE` 属性来开启或关闭清理过期数据的功能，比如：

```sql
CREATE TABLE t1 (
    id int PRIMARY KEY,
    created_at TIMESTAMP
) TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF';
```

如果 `TTL_ENABLE` 被设置成了 `OFF`，则即使设置了其他 TTL 选项，当前表也不会自动清理过期数据。在缺省条件下，`TTL_ENABLE` 被默认设置为 `ON`。

为了与 MySQL 兼容，TTL 也支持注释语法，比如对于上述语句也可以写作：

```sql
CREATE TABLE t1 (
    id int PRIMARY KEY,
    created_at TIMESTAMP
) /*T![ttl] TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF'*/;
```

在 TiDB 环境下，上述两个语句等价。在 Mysql 环境中，会自动忽略注释中的内容，并创建普通的表。

### 修改表的 TTL 属性

支持通过 ALTER 语句修改表的 TTL 属性。比如：

```sql
ALTER TABLE t1 TTL = `created_at` + INTERVAL 1 MONTH;
```

上面的语句即支持修改已有的 TTL 属性的表，也支持将一张非 TTL 的表设置为具有 TTL 属性的表。

对于 TTL 表，也可以单独修改 `TTL_ENABLE` 的值：

```sql
ALTER TABLE t1 TTL_ENABLE = 'OFF';
```

如果想清除一张表的所有 TTL 属性，则可以执行：

```
ALTER TABLE t1 REMOVE TTL;
```

## TTL 任务

对于每张设置了 TTL 属性的表，TiDB 内部会定期调度后台任务来清理过期的数据。你可以通过设置全局变量 [`tidb_ttl_job_run_interval`](/system-variables.md#tidb_ttl_job_run_interval-从-v650-版本开始引入) 来自定义任务的执行周期，比如下面的例子里后台清理任务被设置为每 24 小时执行一次：

```
SET @@global.tidb_ttl_job_run_interval = '24h';
```

如果想禁止 TTL 任务的执行，除了可以设置表属性 `TTL_ENABLE='OFF'` 外，也可以通过设置全局变量 `tidb_ttl_job_enable` 关闭整个集群的 TTL 任务的执行。 

```
SET @@global.tidb_ttl_job_enable = OFF;
```

在某些场景下，我们可能希望只允许在某个时间窗口内调度后台的 TTL 任务，此时可以设置全局变量 `tidb_ttl_job_schedule_window_start_time` 和 `tidb_ttl_job_schedule_window_end_time` 来指定时间窗口，比如：

```
SET @@global.tidb_ttl_job_schedule_window_start_time = '01:00 +0000';
SET @@global.tidb_ttl_job_schedule_window_end_time = '05:00 +0000';
```

则只允许 UTC 时间的凌晨 1 点到 5 点调度 TTL 任务。默认情况下的时间窗口设置为 `00:00 +0000` 到 `23:59 +0000`，即允许所有时段的任务调度。

## 工具兼容性

作为实验特性，暂时不兼容包括 BR, Lightning, TiCDC 在内的数据导入导出以及同步工具。

## 使用限制

目前，TTL 特性具有以下限制:

* 不允许在临时表上设置 TTL 属性，包括本地临时表和全局临时表。
* 具有 TTL 属性的表不支持作为外键约束的主表被其他表引用。
* 不保证所有过期数据立即被删除，过期数据被删除的时间取决于后台清理任务的调度周期和调度窗口。
* 目前单个表的清理任务同时只能在一个 TiDB 节点运行，这在某些场景下（比如表特别大的情况）可能会产生性能瓶颈。此问题会在后续版本中优化。
