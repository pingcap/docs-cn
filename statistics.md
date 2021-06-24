---
title: Introduction to Statistics
summary: Learn how the statistics collect table-level and column-level information.
aliases: ['/docs/dev/statistics/','/docs/dev/reference/performance/statistics/']
---

# Introduction to Statistics

TiDB uses statistics to decide [which index to choose](/choose-index.md). The `tidb_analyze_version` variable controls the statistics collected by TiDB. Currently, two versions of statistics are supported: `tidb_analyze_version = 1` and `tidb_analyze_version = 2`. In versions before v5.1.0, the default value of this variable is `1`. In v5.1.0, the default value of this variable is `2`, which serves as an experimental feature. These two versions include different information in TiDB:

| Information | Version 1 | Version 2|
| --- | --- | ---|
| The total number of rows in the table | √ | √ |
| Column Count-Min Sketch | √ | × |
| Index Count-Min Sketch | √ | × |
| Column Top-N | √ | √ (Maintenance methods and precision are improved) |
| Index Top-N | √ (Insufficient maintenance precision might cause inaccuracy) | √ (Maintenance methods and precision are improved) |
| Column histogram | √ | √ (The histogram does not include Top-N values.) |
| Index histogram | √ | √ (The histogram buckets record the number of different values in each bucket, and the histogram does not include Top-N values.) |
| The number of `NULL`s in the column | √ | √ |
| The number of `NULL`s in the index | √ | √ |
| The average length of columns | √ | √ |
| The average length of indexes | √ | √ |

Compared to Version 1, Version 2 statistics avoids the potential inaccuracy caused by hash collision when the data volume is huge. It also maintains the estimate precision in most scenarios.

This document briefly introduces the histogram, Count-Min Sketch, and Top-N, and details the collection and maintenance of statistics.

## Histogram

A histogram is an approximate representation of the distribution of data. It divides the entire range of values into a series of buckets, and uses simple data to describe each bucket, such as the number of values ​​falling in the bucket. In TiDB, an equal-depth histogram is created for the specific columns of each table. The equal-depth histogram can be used to estimate the interval query.

Here "equal-depth" means that the number of values ​​falling into each bucket is as equal as possible. For example, for a given set {1.6, 1.9, 1.9, 2.0, 2.4, 2.6, 2.7, 2.7, 2.8, 2.9, 3.4, 3.5}, you want to generate 4 buckets. The equal-depth histogram is as follows. It contains four buckets [1.6, 1.9], [2.0, 2.6], [2.7, 2.8], [2.9, 3.5]. The bucket depth is 3.

![Equal-depth Histogram Example](/media/statistics-1.png)

For details about the parameter that determines the upper limit to the number of histogram buckets, refer to [Manual Collection](#manual-collection). When the number of buckets is larger, the accuracy of the histogram is higher; however, higher accuracy is at the cost of the usage of memory resources. You can adjust this number appropriately according to the actual scenario.

## Count-Min Sketch

Count-Min Sketch is a hash structure. When an equivalence query contains `a = 1` or `IN` query (for example, `a in (1, 2, 3)`), TiDB uses this data structure for estimation.

A hash collision might occur since Count-Min Sketch is a hash structure. In the `EXPLAIN` statement, if the estimate of the equivalent query deviates greatly from the actual value, it can be considered that a larger value and a smaller value have been hashed together. In this case, you can take one of the following ways to avoid the hash collision:

- Modify the `WITH NUM TOPN` parameter. TiDB stores the high-frequency (top x) data separately, with the other data stored in Count-Min Sketch. Therefore, to prevent a larger value and a smaller value from being hashed together, you can increase the value of `WITH NUM TOPN`. In TiDB, its default value is 20. The maximum value is 1024. For more information about this parameter, see [Full Collection](#full-collection).
- Modify two parameters `WITH NUM CMSKETCH DEPTH` and `WITH NUM CMSKETCH WIDTH`. Both affect the number of hash buckets and the collision probability. You can increase the values of the two parameters appropriately according to the actual scenario to reduce the probability of hash collision, but at the cost of higher memory usage of statistics. In TiDB, the default value of `WITH NUM CMSKETCH DEPTH` is 5, and the default value of `WITH NUM CMSKETCH WIDTH` is 2048. For more information about the two parameters, see [Full Collection](#full-collection).

## Top-N values

Top-N values are values with the top N occurrences in a column or index. TiDB records the values and occurences of Top-N values.

## Collect statistics

### Manual collection

You can run the `ANALYZE` statement to collect statistics.

> **Note:**
>
> The execution time of `ANALYZE TABLE` in TiDB is longer than that in MySQL or InnoDB. In InnoDB, only a small number of pages are sampled, while in TiDB a comprehensive set of statistics is completely rebuilt. Scripts that were written for MySQL may naively expect `ANALYZE TABLE` will be a short-lived operation.
>
> For quicker analysis, you can set `tidb_enable_fast_analyze` to `1` to enable the Quick Analysis feature. The default value for this parameter is `0`.
>
> After Quick Analysis is enabled, TiDB randomly samples approximately 10,000 rows of data to build statistics. Therefore, in the case of uneven data distribution or a relatively small amount of data, the accuracy of statistical information is relatively poor. It might lead to poor execution plans, such as choosing the wrong index. If the execution time of the normal `ANALYZE` statement is acceptable, it is recommended to disable the Quick Analysis feature.
>
> `tidb_enable_fast_analyze` is an experimental feature, which currently **does not match exactly** with the statistical information of `tidb_analyze_version=2`. Therefore, you need to set the value of `tidb_analyze_version` to `1` when `tidb_enable_fast_analyze` is enabled.

#### Full collection

You can perform full collection using the following syntax.

+ To collect statistics of all the tables in `TableNameList`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
    ```

+ `WITH NUM BUCKETS` specifies the maximum number of buckets in the generated histogram.
+ `WITH NUM TOPN` specifies the maximum number of the generated `TOPN`s.
+ `WITH NUM CMSKETCH DEPTH` specifies the depth of the CM Sketch.
+ `WITH NUM CMSKETCH WIDTH` specifies the width of the CM Sketch.
+ `WITH NUM SAMPLES` specifies the number of samples.

+ To collect statistics of the index columns on all `IndexNameList`s in `TableName`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
    ```

  The statement collects statistics of all index columns when `IndexNameList` is empty.

+ To collect statistics of partition in all `PartitionNameList`s in `TableName`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
    ```

+ To collect statistics of index columns for the partitions in all `PartitionNameList`s in `TableName`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
    ```

> **Note:**
>
> To ensure that the statistical information before and after the collection is consistent, when you set `tidb_analyze_version=2`, `ANALYZE TABLE TableName INDEX` will also collect statistics of the whole table instead of the given index.

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
    ANALYZE INCREMENTAL TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
    ```

+ To incrementally collect statistics of index columns for partitions in all `PartitionNameLists` in `TableName`:

    {{< copyable "sql" >}}

    ```sql
    ANALYZE INCREMENTAL TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
    ```

### Automatic update

For the `INSERT`, `DELETE`, or `UPDATE` statements, TiDB automatically updates the number of rows and updated rows. TiDB persists this information regularly and the update cycle is 20 * `stats-lease`. The default value of `stats-lease` is `3s`. If you specify the value as `0`, it does not update automatically.

Three system variables related to automatic update of statistics are as follows:

|  System Variable | Default Value | Description |
|---|---|---|
| `tidb_auto_analyze_ratio`| 0.5 | The threshold value of automatic update |
| `tidb_auto_analyze_start_time` | `00:00 +0000` | The start time in a day when TiDB can perform automatic update |
| `tidb_auto_analyze_end_time`   | `23:59 +0000` | The end time in a day when TiDB can perform automatic update |

When the ratio of the number of modified rows to the total number of rows of `tbl` in a table is greater than `tidb_auto_analyze_ratio`, and the current time is between `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time`, TiDB executes the `ANALYZE TABLE tbl` statement in the background to automatically update the statistics of this table.

Before v5.0, when the query is executed, TiDB collects feedback with the probability of `feedback-probability` and uses it to update the histogram and Count-Min Sketch. **In v5.0, this feature is disabled by default, and it is not recommended to enable this feature.**

### Control `ANALYZE` concurrency

When you run the `ANALYZE` statement, you can adjust the concurrency using the following parameters, to control its effect on the system.

#### `tidb_build_stats_concurrency`

Currently, when you run the `ANALYZE` statement, the task is divided into multiple small tasks. Each task only works on one column or index. You can use the `tidb_build_stats_concurrency` parameter to control the number of simultaneous tasks. The default value is `4`.

#### `tidb_distsql_scan_concurrency`

When you analyze regular columns, you can use the `tidb_distsql_scan_concurrency` parameter to control the number of Region to be read at one time. The default value is `15`.

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

The syntax of `ShowLikeOrWhereOpt` is as follows:

{{< copyable "sql" >}}

```sql
SHOW STATS_META [ShowLikeOrWhere]
```

Currently, the `SHOW STATS_META` statement returns the following 6 columns:

| Syntax Element | Description  |
| :-------- | :------------- |
| `db_name`  |  The database name    |
| `table_name` | The table name |
| `partition_name`| The partition name |
| `update_time` | The time of the update |
| `modify_count` | The number of modified rows |
| `row_count` | The total number of rows |

> **Note:**
>
> When TiDB automatically updates the total number of rows and the number of modified rows according to DML statements, `update_time` is also updated. Therefore, `update_time` does not necessarily indicate the last time when the `ANALYZE` statement is executed.

### Health state of tables

You can use the `SHOW STATS_HEALTHY` statement to check the health state of tables and roughly estimate the accuracy of the statistics. When `modify_count` >= `row_count`, the health state is 0; when `modify_count` < `row_count`, the health state is (1 - `modify_count`/`row_count`) * 100.

The synopsis of `SHOW STATS_HEALTHY` is:

![ShowStatsHealthy](/media/sqlgram/ShowStatsHealthy.png)

and the synopsis of the `ShowLikeOrWhereOpt` part is:

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

Currently, the `SHOW STATS_HEALTHY` statement returns the following 4 columns:

| Syntax Element | Description  |
| :-------- | :------------- |
| `db_name`  | The database name    |
| `table_name` | The table name |
| `partition_name` | The partition name |
| `healthy` | The health state of tables |

### Metadata of columns

You can use the `SHOW STATS_HISTOGRAMS` statement to view the number of different values and the number of `NULL` in all the columns.

Syntax as follows:

{{< copyable "sql" >}}

```sql
SHOW STATS_HISTOGRAMS [ShowLikeOrWhere]
```

This statement returns the number of different values and the number of `NULL` in all the columns. You can use `ShowLikeOrWhere` to filter the information you need.

Currently, the `SHOW STATS_HISTOGRAMS` statement returns the following 10 columns:

| Syntax Element | Description    |
| :-------- | :------------- |
| `db_name`  |  The database name    |
| `table_name` | The table name |
| `partition_name` | The partition name |
| `column_name` | The column name (when `is_index` is `0`) or the index name (when `is_index` is `1`) |
| `is_index` | Whether it is an index column or not |
| `update_time` | The time of the update |
| `distinct_count` | The number of different values |
| `null_count` | The number of `NULL` |
| `avg_col_size` | The average length of columns |
| correlation | The Pearson correlation coefficient of the column and the integer primary key, which indicates the degree of association between the two columns|

### Buckets of histogram

You can use the `SHOW STATS_BUCKETS` statement to view each bucket of the histogram.

The syntax is as follows:

{{< copyable "sql" >}}

```sql
SHOW STATS_BUCKETS [ShowLikeOrWhere]
```

The diagram is as follows:

![SHOW STATS_BUCKETS](/media/sqlgram/SHOW_STATS_BUCKETS.png)

This statement returns information about all the buckets. You can use `ShowLikeOrWhere` to filter the information you need.

Currently, the `SHOW STATS_BUCKETS` statement returns the following 11 columns:

| Syntax Element | Description   |
| :-------- | :------------- |
| `db_name`  |  The database name    |
| `table_name` | The table name |
| `partition_name` | The partition name |
| `column_name` | The column name (when `is_index` is `0`) or the index name (when `is_index` is `1`) |
| `is_index` | Whether it is an index column or not |
| `bucket_id` | The ID of a bucket |
| `count` | The number of all the values that falls on the bucket and the previous buckets |
| `repeats` | The occurrence number of the maximum value |
| `lower_bound` | The minimum value |
| `upper_bound` | The maximum value |
| `ndv` | The number of different values in the bucket. When `tidb_analyze_version` = `1`, `ndv` is always `0`, which has no actual meaning. |

### Top-N information

You can use the `SHOW STATS_TOPN` statement to view the Top-N information currently collected by TiDB.

The syntax is as follows:

{{< copyable "sql" >}}

```sql
SHOW STATS_TOPN [ShowLikeOrWhere];
```

Currently, the `SHOW STATS_TOPN` statement returns the following 7 columns:

| Syntax Element | Description |
| ---- | ----|
| `db_name` | The database name |
| `table_name` | The table name |
| `partition_name` | The partition name |
| `column_name` | The column name (when `is_index` is `0`) or the index name (when `is_index` is `1`) |
| `is_index` | Whether it is an index column or not |
| `value` | The value of this column |
| `count` | How many times the value appears |

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

## See also

* [DROP STATS](/sql-statements/sql-statement-drop-stats.md)
