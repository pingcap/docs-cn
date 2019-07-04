---
title: Introduction to Statistics
summary: Learn how the statistics collect table-level and column-level information.
category: reference
aliases: ['/docs/sql/statistics/']
---

# Introduction to Statistics

Based on the statistics, the TiDB optimizer chooses the most efficient query execution plan. The statistics collect table-level and column-level information.

- The statistics of a table include the total number of rows and the number of updated rows.
- The statistics of a column include the number of different values, the number of `NULL`, the histogram, and the Count-Min Sketch of the column.

## Collect statistics

### Manual collection

You can run the `ANALYZE` statement to collect statistics.

#### Full collection

> **Note:**
>
> The execution time of `ANALYZE TABLE` in TiDB is longer than that in MySQL or InnoDB. In InnoDB, only a small number of pages are sampled, while in TiDB a comprehensive set of statistics is completely rebuilt. Scripts that were written for MySQL may naively expect `ANALYZE TABLE` will be a short-lived operation.
>
> For quicker analysis, you can set `tidb_enable_fast_analyze` to `1` to enable the Quick Analysis feature. The default value for this parameter is `0`.
>
> After Quick Analysis is enabled, TiDB randomly samples approximately 10,000 rows of data to build statistics. Therefore, in the case of uneven data distribution or a relatively small amount of data, the accuracy of statistical information is relatively poor. It might lead to poor execution plans, such as choosing the wrong index. If the execution time of the normal `ANALYZE` statement is acceptable, it is recommended to disable the Quick Analysis feature.

You can perform full collection using the following syntax.

+ To collect statistics of all the tables in `TableNameList`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableNameList [WITH NUM BUCKETS]
    ```

  `WITH NUM BUCKETS` specifies the maximum number of buckets in the generated histogram.

+ To collect statistics of the index columns on all `IndexNameList`s in `TableName`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS]
    ```

  The statement collects statistics of all index columns when `IndexNameList` is empty.

+ To collect statistics of partition in all `PartitionNameList`s in `TableName`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS]
    ```

+ To collect statistics of index columns for the partitions in all `PartitionNameList`s in `TableName`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [IndexNameList] [WITH NUM BUCKETS]
    ```

#### Incremental collection

To improve the speed of analysis after full collection, incremental collection could be used to analyze the newly added sections in monotonically non-decreasing columns such as time columns.

> **Note:**
>
> + Currently, the incremental collection is only provided for index.
> + When using the incremental collection, you must ensure that only `INSERT` operations exist on the table, and that the newly inserted value on the index column is monotonically non-decreasing. Otherwise, the statistical information might be inaccurate, affecting the TiDB optimizer to select an appropriate execution plan.

You can perform incremental collection using the following syntax.

+ To incrementally collect statistics for index columns in all `IndexNameLists` in `TableName`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE INCREMENTAL TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS]
    ```

+ To incrementally collect statistics of index columns for partitions in all `PartitionNameLists` in `TableName`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE INCREMENTAL TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS]
    ```

### Automatic update

For the `INSERT`, `DELETE`, or `UPDATE` statements, TiDB automatically updates the number of rows and updated rows. TiDB persists this information regularly and the update cycle is 5 * `stats-lease`. The default value of `stats-lease` is `3s`. If you specify the value as `0`, it does not update automatically.

Three system variables related to automatic update of statistics are as follows:

|  System Variable | Default Value | Description |
|---|---|---|
| `tidb_auto_analyze_ratio`| 0.5 | The threshold value of automatic update |
| `tidb_auto_analyze_start_time` | `00:00 +0000` | The start time in a day when TiDB can perform automatic update |
| `tidb_auto_analyze_end_time`   | `23:59 +0000` | The end time in a day when TiDB can perform automatic update |

When the ratio of the number of modified rows to the total number of rows of `tbl` in a table is greater than `tidb_auto_analyze_ratio`, and the current time is between `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time`, TiDB executes the `ANALYZE TABLE tbl` statement in the background to automatically update the statistics of this table.

When the query is executed, TiDB collects feedback with the probability of `feedback-probability` and uses it to update the histogram and Count-Min Sketch. You can modify the value of `feedback-probability` in the configuration file. The default value is `0.0`.

### Control `ANALYZE` concurrency

When you run the `ANALYZE` statement, you can adjust the concurrency using the following parameters, to control its effect on the system.

#### `tidb_build_stats_concurrency`

Currently, when you run the `ANALYZE` statement, the task is divided into multiple small tasks. Each task only works on one column or index. You can use the `tidb_build_stats_concurrency` parameter to control the number of simultaneous tasks. The default value is `4`.

#### `tidb_distsql_scan_concurrency`

When you analyze regular columns, you can use the `tidb_distsql_scan_concurrency` parameter to control the number of Region to be read at one time. The default value is `10`.

#### `tidb_index_serial_scan_concurrency`

When you analyze index columns, you can use the `tidb_index_serial_scan_concurrency` parameter to control the number of Region to be read at one time. The default value is `1`.

### View `ANALYZE` state

When executing the `ANALYZE` statement, you can view the current state of `ANALYZE` using the following SQL statement:

{{< copyable "sql" >}}

```sql
SHOW ANALYZE STATUS [ShowLikeOrWhere]
```

This statement returns the state of `ANALYZE`. You can use `ShowLikeOrWhere` to filter the information you need.

Currently, the `SHOW ANALYZE STATUS` statement returns the following 7 columns:

| Syntax Element | Description            |
| :-------- | :------------- |
| table_schema  |  The database name    |
| table_name | The table name |
| partition_name| The partition name |
| job_info | The task information. The element includes index names when index analysis is performed. |
| row_count | The number of rows that have been analyzed |
| start_time | The time at which the task starts |
| state | The state of a task, including `pending`, `running`, `finished`, and `failed` |

## View statistics

You can view the statistics status using the following statements.

### Metadata of tables

You can use the `SHOW STATS_META` statement to view the total number of rows and the number of updated rows.

Syntax as follows:

{{< copyable "sql" >}}

```sql
SHOW STATS_META [ShowLikeOrWhere]
```

This statement returns the total number of all the rows in all the tables and the number of updated rows. You can use `ShowLikeOrWhere` to filter the information you need.

Currently, the `SHOW STATS_META` statement returns the following 6 columns:

| Syntax Element | Description  |
| :-------- | :------------- |
| `db_name`  |  The database name    |
| `table_name` | The table name |
| `partition_name`| The partition name |
| `update_time` | The the time of the update |
| `modify_count` | The number of modified rows |
| `row_count` | The total number of rows |

### Metadata of columns

You can use the `SHOW STATS_HISTOGRAMS` statement to view the number of different values and the number of `NULL` in all the columns.

Syntax as follows:

{{< copyable "sql" >}}

```sql
SHOW STATS_HISTOGRAMS [ShowLikeOrWhere]
```

This statement returns the number of different values and the number of `NULL` in all the columns. You can use `ShowLikeOrWhere` to filter the information you need.

Currently, the `SHOW STATS_HISTOGRAMS` statement returns the following 8 columns:

| Syntax Element | Description    |
| :-------- | :------------- |
| `db_name`  |  The database name    |
| `table_name` | The table name |
| `partition_name` | The partition name |
| `column_name` | The column name |
| `is_index` | Whether it is an index column or not |
| `update_time` | The time of the update |
| `distinct_count` | The number of different values |
| `null_count` | The number of `NULL` |
| `avg_col_size` | The average length of columns |

### Buckets of histogram

You can use the `SHOW STATS_BUCKETS` statement to view each bucket of the histogram.

Syntax as follows:

{{< copyable "sql" >}}

```sql
SHOW STATS_BUCKETS [ShowLikeOrWhere]
```

This statement returns information about all the buckets. You can use `ShowLikeOrWhere` to filter the information you need.

Currently, the `SHOW STATS_BUCKETS` statement returns the following 10 columns:

| Syntax Element | Description   |
| :-------- | :------------- |
| `db_name`  |  The database name    |
| `table_name` | The table name |
| `partition_name` | The partition name |
| `column_name` | The column name |
| `is_index` | Whether it is an index column or not |
| `bucket_id` | The the ID of a bucket |
| `count` | The number of all the values that falls on the bucket and the previous buckets |
| `repeats` | The occurrence number of the maximum value |
| `lower_bound` | The minimum value |
| `upper_bound` | The maximum value |

## Delete statistics

You can run the `DROP STATS` statement to delete statistics.

Syntax as follows:

{{< copyable "sql" >}}

```sql
DROP STATS TableName
```

The statement deletes statistics of all the tables in `TableName`.

## Import and export statistics

### Export statistics

The interface to export statistics is as follows:

+ To obtain the JSON format statistics of the `${table_name}` table in the `${db_name}` database:

    {{< copyable "" >}}

    ```
    http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}
    ```

+ To obtain the JSON format statistics of the `${table_name}` table in the `${db_name}` database at specific time:

    {{< copyable "" >}}

    ```
    http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyyMMddHHmmss}
    ```

### Import statistics

Generally, the imported statistics refer to the JSON file obtained using the export interface.

Syntax:

{{< copyable "sql" >}}

```
LOAD STATS 'file_name'
```

`file_name` is the file name of the statistics to be imported.