---
title: 使用 TTL (Time to Live) 定期删除过期数据
summary: Time to Live (TTL) 提供了行级别的生命周期控制策略。本篇文档介绍如何通过 TTL (Time to Live) 来管理表数据的生命周期。
---

# 使用 TTL (Time to Live) 定期删除过期数据

Time to Live (TTL) 提供了行级别的生命周期控制策略。通过为表设置 TTL 属性，TiDB 可以周期性地自动检查并清理表中的过期数据。此功能在一些场景可以有效节省存储空间、提升性能。

TTL 常见的使用场景：

* 定期删除验证码、短网址记录
* 定期删除不需要的历史订单
* 自动删除计算的中间结果

TTL 设计的目标是在不影响在线读写负载的前提下，帮助用户周期性且及时地清理不需要的数据。TTL 会以表为单位，并发地分发不同的任务到不同的 TiDB Server 节点上，进行并行删除处理。TTL 并不保证所有过期数据立即被删除，也就是说即使数据过期了，客户端仍然有可能在这之后的一段时间内读到过期的数据，直到其真正的被后台处理任务删除。

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。
> TTL 无法在 [Serverless Tier clusters](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier-beta) 上使用。

## 语法

你可以通过 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 或 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) 语句来配置表的 TTL 功能。

### 创建具有 TTL 属性的表

- 创建一个具有 TTL 属性的表：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

    上面的例子创建了一张表 `t1`，并指定了 `created_at` 为 TTL 的时间列，表示数据的创建时间。同时，它还通过 `INTERVAL 3 MONTH` 设置了表中行的最长存活时间为 3 个月。超过了此时长的过期数据会在之后被删除。

- 设置 `TTL_ENABLE` 属性来开启或关闭清理过期数据的功能：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF';
    ```

    如果 `TTL_ENABLE` 被设置成了 `OFF`，则即使设置了其他 TTL 选项，当前表也不会自动清理过期数据。对于一个设置了 TTL 属性的表，`TTL_ENABLE` 在缺省条件下默认为 `ON`。

- 为了与 MySQL 兼容，你也可以使用注释语法来设置 TTL：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) /*T![ttl] TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF'*/;
    ```

    在 TiDB 环境中，使用表的 TTL 属性和注释语法来配置 TTL 是等价的。在 MySQL 环境中，会自动忽略注释中的内容，并创建普通的表。

### 修改表的 TTL 属性

- 修改表的 TTL 属性：

    ```sql
    ALTER TABLE t1 TTL = `created_at` + INTERVAL 1 MONTH;
    ```

    上面的语句既支持修改已配置 TTL 属性的表，也支持为一张非 TTL 的表添加 TTL 属性。

- 单独修改 TTL 表的 `TTL_ENABLE` 值：

    ```sql
    ALTER TABLE t1 TTL_ENABLE = 'OFF';
    ```

- 清除一张表的所有 TTL 属性：

    ```sql
    ALTER TABLE t1 REMOVE TTL;
    ```

### TTL 和数据类型的默认值

TTL 可以和[数据类型的默认值](/data-type-default-values.md)一起使用。以下是两种常见的用法示例：

* 使用 `DEFAULT CURRENT_TIMESTAMP` 来指定某一列的默认值为该行的创建时间，并用这一列作为 TTL 的时间列，创建时间超过 3 个月的数据将被标记为过期：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

* 指定某一列的默认值为该行的创建时间或更新时间，并用这一列作为 TTL 的时间列，创建时间或更新时间超过 3 个月的数据将被标记为过期：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

### TTL 和生成列

TTL 可以和[生成列](/generated-columns.md)（实验特性）一起使用，用来表达更加复杂的过期规则。例如：

```sql
CREATE TABLE message (
    id int PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image bool,
    expire_at TIMESTAMP AS (IF(image,
            created_at + INTERVAL 5 DAY,
            created_at + INTERVAL 30 DAY
    ))
) TTL = `expire_at` + INTERVAL 0 DAY;
```

上述语句的消息以 `expire_at` 列来作为过期时间，并按照消息类型来设定。如果是图片，则 5 天后过期，不然就 30 天后过期。

TTL 还可以和 [JSON 类型](/data-type-json.md) 一起使用。例如：

```sql
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_info JSON,
    created_at DATE AS (JSON_EXTRACT(order_info, '$.created_at')) VIRTUAL
) TTL = `created_at` + INTERVAL 3 month;
```

## TTL 任务

对于每张设置了 TTL 属性的表，TiDB 内部会定期调度后台任务来清理过期的数据。你可以通过设置全局变量 [`tidb_ttl_job_run_interval`](/system-variables.md#tidb_ttl_job_run_interval-从-v650-版本开始引入) 来自定义任务的执行周期，比如通过下面的语句将后台清理任务设置为每 24 小时执行一次：

```sql
SET @@global.tidb_ttl_job_run_interval = '24h';
```

如果想禁止 TTL 任务的执行，除了可以设置表属性 `TTL_ENABLE='OFF'` 外，也可以通过设置全局变量 `tidb_ttl_job_enable` 关闭整个集群的 TTL 任务的执行。

```sql
SET @@global.tidb_ttl_job_enable = OFF;
```

在某些场景下，你可能希望只允许在每天的某个时间段内调度后台的 TTL 任务，此时可以设置全局变量 [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-从-v650-版本开始引入) 和 [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-从-v650-版本开始引入) 来指定时间窗口，比如：

```sql
SET @@global.tidb_ttl_job_schedule_window_start_time = '01:00 +0000';
SET @@global.tidb_ttl_job_schedule_window_end_time = '05:00 +0000';
```

上述语句只允许在 UTC 时间的凌晨 1 点到 5 点调度 TTL 任务。默认情况下的时间窗口设置为 `00:00 +0000` 到 `23:59 +0000`，即允许所有时段的任务调度。

## 监控与图表

TiDB 会定时采集 TTL 的运行时信息，并在 Grafana 中提供了相关指标的可视化图表。你可以在 TiDB -> TTL 的面板下看到这些信息。指标详情见 [TiDB 重要监控指标详解](/grafana-tidb-dashboard.md) 中的 `TTL` 部分。

## 工具兼容性

作为实验特性，TTL 特性暂时不兼容包括 BR、TiDB Lightning、TiCDC 在内的数据导入导出以及同步工具。

## 使用限制

目前，TTL 特性具有以下限制:

* 不允许在临时表上设置 TTL 属性，包括本地临时表和全局临时表。
* 具有 TTL 属性的表不支持作为外键约束的主表被其他表引用。
* 不保证所有过期数据立即被删除，过期数据被删除的时间取决于后台清理任务的调度周期和调度窗口。
* 目前单个表的清理任务同时只能在同一个 TiDB Server 节点运行，这在某些场景下（比如表特别大的情况）可能会产生性能瓶颈。此问题会在后续版本中优化。
