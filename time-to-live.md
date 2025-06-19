---
title: 使用 TTL（生存时间）定期删除数据
summary: 生存时间（TTL）是一个允许您在行级别管理 TiDB 数据生命周期的功能。在本文档中，您可以了解如何使用 TTL 自动使数据过期并删除旧数据。
---

# 使用 TTL（生存时间）定期删除过期数据

生存时间（TTL）是一个允许您在行级别管理 TiDB 数据生命周期的功能。对于具有 TTL 属性的表，TiDB 会自动检查数据生命周期并在行级别删除过期数据。此功能在某些场景下可以有效节省存储空间并提升性能。

以下是 TTL 的一些常见使用场景：

* 定期删除验证码和短链接。
* 定期删除不必要的历史订单。
* 自动删除计算的中间结果。

TTL 的设计目的是帮助用户定期及时清理不必要的数据，而不影响在线读写工作负载。TTL 以表为单位，将不同的任务并发分派到不同的 TiDB 节点上并行删除数据。TTL 不保证所有过期数据都会立即被删除，这意味着即使某些数据已过期，客户端在过期时间之后的一段时间内仍可能读取到这些数据，直到后台 TTL 任务删除这些数据。

## 语法

您可以使用 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 或 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) 语句配置表的 TTL 属性。

### 创建具有 TTL 属性的表

- 创建具有 TTL 属性的表：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

    上述示例创建了一个表 `t1` 并指定 `created_at` 作为 TTL 时间戳列，该列表示数据的创建时间。示例还通过 `INTERVAL 3 MONTH` 设置了一行数据在表中允许存在的最长时间为 3 个月。超过此值的数据将在之后被删除。

- 设置 `TTL_ENABLE` 属性以启用或禁用清理过期数据的功能：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF';
    ```

    如果 `TTL_ENABLE` 设置为 `OFF`，即使设置了其他 TTL 选项，TiDB 也不会自动清理此表中的过期数据。对于具有 TTL 属性的表，`TTL_ENABLE` 默认为 `ON`。

- 为了与 MySQL 兼容，您可以使用注释设置 TTL 属性：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) /*T![ttl] TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF'*/;
    ```

    在 TiDB 中，使用表 TTL 属性或使用注释配置 TTL 是等效的。在 MySQL 中，注释会被忽略，并创建一个普通表。

### 修改表的 TTL 属性

- 修改表的 TTL 属性：

    ```sql
    ALTER TABLE t1 TTL = `created_at` + INTERVAL 1 MONTH;
    ```

    您可以使用上述语句修改已有 TTL 属性的表，或为没有 TTL 属性的表添加 TTL 属性。

- 修改具有 TTL 属性的表的 `TTL_ENABLE` 值：

    ```sql
    ALTER TABLE t1 TTL_ENABLE = 'OFF';
    ```

- 移除表的所有 TTL 属性：

    ```sql
    ALTER TABLE t1 REMOVE TTL;
    ```

### TTL 和数据类型的默认值

您可以将 TTL 与[数据类型的默认值](/data-type-default-values.md)一起使用。以下是两个常见的使用示例：

* 使用 `DEFAULT CURRENT_TIMESTAMP` 将列的默认值指定为当前创建时间，并使用此列作为 TTL 时间戳列。3 个月前创建的记录将过期：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

* 将列的默认值指定为创建时间或最新更新时间，并使用此列作为 TTL 时间戳列。3 个月未更新的记录将过期：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

### TTL 和生成列

您可以将 TTL 与[生成列](/generated-columns.md)一起使用来配置复杂的过期规则。例如：

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

上述语句使用 `expire_at` 列作为 TTL 时间戳列，并根据消息类型设置过期时间。如果消息是图片，则 5 天后过期。否则，30 天后过期。

您可以将 TTL 与 [JSON 类型](/data-type-json.md)一起使用。例如：

```sql
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_info JSON,
    created_at DATE AS (JSON_EXTRACT(order_info, '$.created_at')) VIRTUAL
) TTL = `created_at` + INTERVAL 3 month;
```

## TTL 任务

对于每个具有 TTL 属性的表，TiDB 内部会调度一个后台任务来清理过期数据。您可以通过为表设置 `TTL_JOB_INTERVAL` 属性来自定义这些任务的执行周期。以下示例将表 `orders` 的后台清理任务设置为每 24 小时运行一次：

```sql
ALTER TABLE orders TTL_JOB_INTERVAL = '24h';
```

`TTL_JOB_INTERVAL` 默认设置为 `1h`。

在执行 TTL 任务时，TiDB 会将表分割成最多 64 个任务，以 Region 为最小单位。这些任务将被分布式执行。您可以通过设置系统变量 [`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-new-in-v700) 来限制整个集群中并发 TTL 任务的数量。但是，并非所有表的 TTL 任务都可以被分割成任务。有关哪些类型的表的 TTL 任务不能被分割成任务的更多详细信息，请参考[限制](#限制)部分。

要禁用 TTL 任务的执行，除了设置表选项 `TTL_ENABLE='OFF'` 外，您还可以通过设置 [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650) 全局变量来禁用整个集群中 TTL 任务的执行：

```sql
SET @@global.tidb_ttl_job_enable = OFF;
```

在某些场景下，您可能希望只允许 TTL 任务在特定时间窗口内运行。在这种情况下，您可以设置 [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650) 和 [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650) 全局变量来指定时间窗口。例如：

```sql
SET @@global.tidb_ttl_job_schedule_window_start_time = '01:00 +0000';
SET @@global.tidb_ttl_job_schedule_window_end_time = '05:00 +0000';
```

上述语句只允许在 UTC 时间 1:00 到 5:00 之间调度 TTL 任务。默认情况下，时间窗口设置为 `00:00 +0000` 到 `23:59 +0000`，允许在任何时间调度任务。

## 可观测性

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本节仅适用于 TiDB Self-Managed。目前，TiDB Cloud 不提供 TTL 指标。

</CustomContent>

TiDB 定期收集 TTL 的运行时信息，并在 Grafana 中提供这些指标的可视化图表。您可以在 Grafana 的 TiDB -> TTL 面板中查看这些指标。

<CustomContent platform="tidb">

有关指标的详细信息，请参见[TiDB 监控指标](/grafana-tidb-dashboard.md)中的 TTL 部分。

</CustomContent>

此外，TiDB 提供了三个表来获取有关 TTL 任务的更多信息：

+ `mysql.tidb_ttl_table_status` 表包含所有 TTL 表的先前执行的 TTL 任务和正在进行的 TTL 任务的信息

    ```sql
    TABLE mysql.tidb_ttl_table_status LIMIT 1\G
    ```

    ```
    *************************** 1. row ***************************
                          table_id: 85
                   parent_table_id: 85
                  table_statistics: NULL
                       last_job_id: 0b4a6d50-3041-4664-9516-5525ee6d9f90
               last_job_start_time: 2023-02-15 20:43:46
              last_job_finish_time: 2023-02-15 20:44:46
               last_job_ttl_expire: 2023-02-15 19:43:46
                  last_job_summary: {"total_rows":4369519,"success_rows":4369519,"error_rows":0,"total_scan_task":64,"scheduled_scan_task":64,"finished_scan_task":64}
                    current_job_id: NULL
              current_job_owner_id: NULL
            current_job_owner_addr: NULL
         current_job_owner_hb_time: NULL
            current_job_start_time: NULL
            current_job_ttl_expire: NULL
                 current_job_state: NULL
                current_job_status: NULL
    current_job_status_update_time: NULL
    1 row in set (0.040 sec)
    ```

    列 `table_id` 是分区表的 ID，`parent_table_id` 是表的 ID，与 [`information_schema.tables`](/information-schema/information-schema-tables.md) 中的 ID 对应。如果表不是分区表，这两个 ID 相同。

    列 `{last, current}_job_{start_time, finish_time, ttl_expire}` 分别描述了最后一次或当前执行的 TTL 任务的开始时间、结束时间和过期时间。`last_job_summary` 列描述了最后一次 TTL 任务的执行状态，包括总行数、成功行数和失败行数。

+ `mysql.tidb_ttl_task` 表包含正在进行的 TTL 子任务的信息。一个 TTL 任务被分割成许多子任务，此表记录当前正在执行的子任务。
+ `mysql.tidb_ttl_job_history` 表包含已执行的 TTL 任务的信息。TTL 任务历史记录保留 90 天。

    ```sql
    TABLE mysql.tidb_ttl_job_history LIMIT 1\G
    ```

    ```
    *************************** 1. row ***************************
               job_id: f221620c-ab84-4a28-9d24-b47ca2b5a301
             table_id: 85
      parent_table_id: 85
         table_schema: test_schema
           table_name: TestTable
       partition_name: NULL
          create_time: 2023-02-15 17:43:46
          finish_time: 2023-02-15 17:45:46
           ttl_expire: 2023-02-15 16:43:46
         summary_text: {"total_rows":9588419,"success_rows":9588419,"error_rows":0,"total_scan_task":63,"scheduled_scan_task":63,"finished_scan_task":63}
         expired_rows: 9588419
         deleted_rows: 9588419
    error_delete_rows: 0
               status: finished
    ```

    列 `table_id` 是分区表的 ID，`parent_table_id` 是表的 ID，与 `information_schema.tables` 中的 ID 对应。`table_schema`、`table_name` 和 `partition_name` 分别对应数据库、表名和分区名。`create_time`、`finish_time` 和 `ttl_expire` 表示 TTL 任务的创建时间、结束时间和过期时间。`expired_rows` 和 `deleted_rows` 表示过期行数和成功删除的行数。

## 与 TiDB 工具的兼容性

TTL 可以与其他 TiDB 迁移、备份和恢复工具一起使用。

| 工具名称 | 最低支持版本 | 说明 |
| --- | --- | --- |
| Backup & Restore (BR) | v6.6.0 | 使用 BR 恢复数据后，表的 `TTL_ENABLE` 属性将被设置为 `OFF`。这可以防止 TiDB 在备份和恢复后立即删除过期数据。您需要手动打开每个表的 `TTL_ENABLE` 属性以重新启用 TTL。 |
| TiDB Lightning | v6.6.0 | 使用 TiDB Lightning 导入数据后，导入表的 `TTL_ENABLE` 属性将被设置为 `OFF`。这可以防止 TiDB 在导入后立即删除过期数据。您需要手动打开每个表的 `TTL_ENABLE` 属性以重新启用 TTL。 |
| TiCDC | v7.0.0 | 下游的 `TTL_ENABLE` 属性将自动设置为 `OFF`。上游的 TTL 删除操作将同步到下游。因此，为了防止重复删除，下游表的 `TTL_ENABLE` 属性将被强制设置为 `OFF`。 |

## 与 SQL 的兼容性

| 功能名称 | 说明 |
| :-- | :---- |
| [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md) | `FLASHBACK TABLE` 将把表的 `TTL_ENABLE` 属性设置为 `OFF`。这可以防止 TiDB 在闪回后立即删除过期数据。您需要手动打开每个表的 `TTL_ENABLE` 属性以重新启用 TTL。 |
| [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) | `FLASHBACK DATABASE` 将把表的 `TTL_ENABLE` 属性设置为 `OFF`，且不会修改 `TTL_ENABLE` 属性。这可以防止 TiDB 在闪回后立即删除过期数据。您需要手动打开每个表的 `TTL_ENABLE` 属性以重新启用 TTL。 |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) | `FLASHBACK CLUSTER` 将把系统变量 [`TIDB_TTL_JOB_ENABLE`](/system-variables.md#tidb_ttl_job_enable-new-in-v650) 设置为 `OFF`，且不会更改 `TTL_ENABLE` 属性的值。 |

## 限制

目前，TTL 功能有以下限制：

* TTL 属性不能在临时表上设置，包括本地临时表和全局临时表。
* 具有 TTL 属性的表不支持在外键约束中被其他表作为主表引用。
* 不保证所有过期数据都会立即删除。过期数据被删除的时间取决于后台清理任务的调度间隔和调度窗口。
* 对于使用[聚簇索引](/clustered-indexes.md)的表，如果主键既不是整数类型也不是二进制字符串类型，则 TTL 任务无法被分割成多个任务。这将导致 TTL 任务在单个 TiDB 节点上顺序执行。如果表包含大量数据，TTL 任务的执行可能会变慢。

## 常见问题

<CustomContent platform="tidb">

- 如何判断删除速度是否足够快以保持数据大小相对稳定？

    在 [Grafana `TiDB` 面板](/grafana-tidb-dashboard.md)中，`TTL Insert Rows Per Hour` 面板记录了前一小时插入的总行数。相应的 `TTL Delete Rows Per Hour` 记录了前一小时 TTL 任务删除的总行数。如果 `TTL Insert Rows Per Hour` 长期高于 `TTL Delete Rows Per Hour`，则表示插入速率高于删除速率，总数据量将会增加。例如：

    ![insert fast example](/media/ttl/insert-fast.png)

    值得注意的是，由于 TTL 不保证过期行会立即被删除，而且当前插入的行将在未来的 TTL 任务中被删除，即使在短时间内 TTL 删除速度低于插入速度，也不一定意味着 TTL 速度太慢。您需要结合具体情况来考虑。

- 如何判断 TTL 任务的瓶颈是在扫描还是删除？

    查看 `TTL Scan Worker Time By Phase` 和 `TTL Delete Worker Time By Phase` 面板。如果扫描工作线程在 `dispatch` 阶段的时间占比较大，而删除工作线程很少处于 `idle` 阶段，则说明扫描工作线程在等待删除工作线程完成删除。如果此时集群资源仍然空闲，可以考虑增加 `tidb_ttl_delete_worker_count` 来增加删除工作线程的数量。例如：

    ![scan fast example](/media/ttl/scan-fast.png)

    相反，如果扫描工作线程很少处于 `dispatch` 阶段，而删除工作线程长时间处于 `idle` 阶段，则说明扫描工作线程相对较忙。例如：

    ![delete fast example](/media/ttl/delete-fast.png)

    TTL 任务中扫描和删除的比例与机器配置和数据分布有关，因此每个时刻的监控数据只能代表当时正在执行的 TTL 任务。您可以通过查看 `mysql.tidb_ttl_job_history` 表来确定某个时刻正在运行的是哪个 TTL 任务以及该任务对应的表。

- 如何合理配置 `tidb_ttl_scan_worker_count` 和 `tidb_ttl_delete_worker_count`？

    1. 参考"如何判断 TTL 任务的瓶颈是在扫描还是删除？"来考虑是否需要增加 `tidb_ttl_scan_worker_count` 或 `tidb_ttl_delete_worker_count` 的值。
    2. 如果 TiKV 节点数量较多，增加 `tidb_ttl_scan_worker_count` 的值可以使 TTL 任务的工作负载更加均衡。

   由于过多的 TTL 工作线程会造成较大压力，您需要结合评估 TiDB 的 CPU 水平以及 TiKV 的磁盘和 CPU 使用情况。根据不同的场景和需求（是否需要尽可能加快 TTL 速度，或者是否需要减少 TTL 对其他查询的影响），可以调整 `tidb_ttl_scan_worker_count` 和 `tidb_ttl_delete_worker_count` 的值来提高 TTL 扫描和删除的速度或减少 TTL 任务带来的性能影响。

</CustomContent>
<CustomContent platform="tidb-cloud">

- 如何合理配置 `tidb_ttl_scan_worker_count` 和 `tidb_ttl_delete_worker_count`？

   如果 TiKV 节点数量较多，增加 `tidb_ttl_scan_worker_count` 的值可以使 TTL 任务的工作负载更加均衡。

   但是过多的 TTL 工作线程会造成较大压力，您需要结合评估 TiDB 的 CPU 水平以及 TiKV 的磁盘和 CPU 使用情况。根据不同的场景和需求（是否需要尽可能加快 TTL 速度，或者是否需要减少 TTL 对其他查询的影响），可以调整 `tidb_ttl_scan_worker_count` 和 `tidb_ttl_delete_worker_count` 的值来提高 TTL 扫描和删除的速度或减少 TTL 任务带来的性能影响。

</CustomContent>
