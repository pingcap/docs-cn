---
title: Periodically Delete Data Using TTL (Time to Live)
summary: Time to live (TTL) is a feature that allows you to manage TiDB data lifetime at the row level. In this document, you can learn how to use TTL to automatically expire and delete old data.
---

# Periodically Delete Expired Data Using TTL (Time to Live)

Time to live (TTL) is a feature that allows you to manage TiDB data lifetime at the row level. For a table with the TTL attribute, TiDB automatically checks data lifetime and deletes expired data at the row level. This feature can effectively save storage space and enhance performance in some scenarios.

The following are some common scenarios for TTL:

* Regularly delete verification codes and short URLs.
* Regularly delete unnecessary historical orders.
* Automatically delete intermediate results of calculations.

TTL is designed to help users clean up unnecessary data periodically and in a timely manner without affecting the online read and write workloads. TTL concurrently dispatches different jobs to different TiDB nodes to delete data in parallel in the unit of table. TTL does not guarantee that all expired data is deleted immediately, which means that even if some data is expired, the client might still read that data some time after the expiration time until that data is deleted by the background TTL job.

> **Warning:**
>
> This is an experimental feature. It is not recommended that you use it in a production environment.
> TTL is not available for [TiDB Cloud Serverless Tier](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier-beta).

## Syntax

You can configure the TTL attribute of a table using the [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) or [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) statement.

### Create a table with a TTL attribute

- Create a table with a TTL attribute:

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

    The preceding example creates a table `t1` and specifies `created_at` as the TTL timestamp column, which indicates the creation time of the data. The example also sets the longest time that a row is allowed to live in the table to 3 months through `INTERVAL 3 MONTH`. Data that lives longer than this value will be deleted later.

- Set the `TTL_ENABLE` attribute to enable or disable the feature of cleaning up expired data:

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF';
    ```

    If `TTL_ENABLE` is set to `OFF`, even if other TTL options are set, TiDB does not automatically clean up expired data in this table. For a table with the TTL attribute, `TTL_ENABLE` is `ON` by default.

- To be compatible with MySQL, you can set a TTL attribute using a comment:

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) /*T![ttl] TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF'*/;
    ```

    In TiDB, using the table TTL attribute or using comments to configure TTL is equivalent. In MySQL, the comment is ignored and an ordinary table is created.

### Modify the TTL attribute of a table

- Modify the TTL attribute of a table:

    ```sql
    ALTER TABLE t1 TTL = `created_at` + INTERVAL 1 MONTH;
    ```

    You can use the preceding statement to modify a table with an existing TTL attribute or to add a TTL attribute to a table without a TTL attribute.

- Modify the value of `TTL_ENABLE` for a table with the TTL attribute:

    ```sql
    ALTER TABLE t1 TTL_ENABLE = 'OFF';
    ```

- To remove all TTL attributes of a table:

    ```sql
    ALTER TABLE t1 REMOVE TTL;
    ```

### TTL and the default values of data types

You can use TTL together with [default values of the data types](/data-type-default-values.md). The following are two common usage examples:

* Use `DEFAULT CURRENT_TIMESTAMP` to specify the default value of a column as the current creation time and use this column as the TTL timestamp column. Records that were created 3 months ago are expired:

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

* Specify the default value of a column as the creation time or the latest update time and use this column as the TTL timestamp column. Records that have not been updated for 3 months are expired:

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

### TTL and generated columns

You can use TTL together with [generated columns](/generated-columns.md) (experimental feature) to configure complex expiration rules. For example:

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

The preceding statement uses the `expire_at` column as the TTL timestamp column and sets the expiration time according to the message type. If the message is an image, it expires in 5 days. Otherwise, it expires in 30 days.

You can use TTL together with the [JSON type](/data-type-json.md). For example:

```sql
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_info JSON,
    created_at DATE AS (JSON_EXTRACT(order_info, '$.created_at')) VIRTUAL
) TTL = `created_at` + INTERVAL 3 month;
```

## TTL job

For each table with a TTL attribute, TiDB internally schedules a background job to clean up expired data. You can customize the execution period of these jobs by setting the `TTL_JOB_INTERVAL` attribute for the table. The following example sets the background cleanup jobs for the table `orders` to run once every 24 hours:

```sql
ALTER TABLE orders TTL_JOB_INTERVAL = '24h';
```

`TTL_JOB_INTERVAL` is set to `1h` by default.

To disable the execution of TTL jobs, in addition to setting the `TTL_ENABLE='OFF'` table option, you can also disable the execution of TTL jobs in the entire cluster by setting the [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650) global variable:

```sql
SET @@global.tidb_ttl_job_enable = OFF;
```

In some scenarios, you might want to allow TTL jobs to run only in a certain time window. In this case, you can set the [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650) and [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650) global variables to specify the time window. For example:

```sql
SET @@global.tidb_ttl_job_schedule_window_start_time = '01:00 +0000';
SET @@global.tidb_ttl_job_schedule_window_end_time = '05:00 +0000';
```

The preceding statement allows TTL jobs to be scheduled only between 1:00 and 5:00 UTC. By default, the time window is set to `00:00 +0000` to `23:59 +0000`, which allows the jobs to be scheduled at any time.

## Monitoring metrics and charts

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is only applicable to on-premises TiDB. Currently, TiDB Cloud does not provide TTL metrics.

</CustomContent>

TiDB collects runtime information about TTL periodically and provides visualized charts of these metrics in Grafana. You can see these metrics in the TiDB -> TTL panel in Grafana.

<CustomContent platform="tidb">

For details of the metrics, see the TTL section in [TiDB Monitoring Metrics](/grafana-tidb-dashboard.md).

</CustomContent>

## Compatibility with TiDB tools

As an experimental feature, the TTL feature is not compatible with data import and export tools, including BR, TiDB Lightning, and TiCDC.

## Limitations

Currently, the TTL feature has the following limitations:

* The TTL attribute cannot be set on temporary tables, including local temporary tables and global temporary tables.
* A table with the TTL attribute does not support being referenced by other tables as the primary table in a foreign key constraint.
* It is not guaranteed that all expired data is deleted immediately. The time when expired data is deleted depends on the scheduling interval and scheduling window of the background cleanup job.
* Currently, a single table can only run a cleanup job on a single TiDB node at a given time. This might cause performance bottlenecks in some scenarios (for example, when the table is extremely large). This issue will be optimized in future releases.
