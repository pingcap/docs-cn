---
title: 统计信息简介
category: reference
aliases: ['/docs-cn/sql/statistics/']
---

# 统计信息简介

TiDB 优化器会根据统计信息来选择最优的执行计划。统计信息收集了表级别和列级别的信息，表的统计信息包括总行数和修改的行数。列的统计信息包括不同值的数量、NULL 的数量、直方图、以及该列的 Count-Min Sketch 信息。

## 统计信息的收集

### 手动收集

可以通过执行 `ANALYZE` 语句来收集统计信息。

#### 全量收集

> **注意：**
>
> 在 TiDB 中执行 `ANALYZE TABLE` 语句比在 MySQL 或 InnoDB 中耗时更长。InnoDB 采样的只是少量页面，但 TiDB 会完全重构一系列统计信息。适用于 MySQL 的脚本会误以为执行 `ANALYZE TABLE` 耗时较短。
>
> 如需更快的分析速度，可将 `tidb_enable_fast_analyze` 设置为 `1` 来打开快速分析功能。该参数的默认值为 `0`。
>
> 快速分析功能开启后，TiDB 会随机采样约 10000 行的数据来构建统计信息。因此在数据分布不均匀或者数据量比较少的情况下，统计信息的准确度会比较差。可能导致执行计划不优，比如选错索引。如果可以接受普通 `ANALYZE` 语句的执行时间，则推荐关闭快速分析功能。

可以通过以下几种语法进行全量收集。

收集 TableNameList 中所有表的统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableNameList [WITH NUM BUCKETS];
```

WITH NUM BUCKETS 可以用来指定生成直方图的桶数量上限。

收集 TableName 中所有的 IndexNameList 中的索引列的统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS];
```

IndexNameList 为空时会收集所有索引列的统计信息。

收集 TableName 中所有的 PartitionNameList 中分区的统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS];
```

收集 TableName 中所有的 PartitionNameList 中分区的索引列统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableName PARTITION PartitionNameList [IndexNameList] [WITH NUM BUCKETS];
```

#### 增量收集

对于类似时间列这样的单调不减列，在进行全量收集后，可以使用增量收集来单独分析新增的部分，以提高分析的速度。

> **注意：**
>
> 1. 目前只有索引提供了增量收集的功能
> 2. 使用增量收集时，必须保证表上只有插入操作，且应用方需要保证索引列上新插入的值是单调不减的，否则会导致统计信息不准，影响 TiDB 优化器选择合适的执行计划

可以通过以下几种语法进行增量收集。

增量收集 TableName 中所有的 IndexNameList 中的索引列的统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE INCREMENTAL TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS];
```

增量收集 TableName 中所有的 PartitionNameList 中分区的索引列统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE INCREMENTAL TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS];
```

### 自动更新

在发生增加，删除以及修改语句时，TiDB 会自动更新表的总行数以及修改的行数。这些信息会定期持久化下来，
更新的周期是 5 * `stats-lease`，`stats-lease` 的默认值是 3s，如果将其指定为 0，那么将不会自动更新。

和统计信息自动更新相关的三个系统变量如下：

|  系统变量名 | 默认值 | 功能 |
|---|---|---|
| `tidb_auto_analyze_ratio`| 0.5 | 自动更新阈值 |
| `tidb_auto_analyze_start_time` | `00:00 +0000` | 一天中能够进行自动更新的开始时间 |
| `tidb_auto_analyze_end_time`   | `23:59 +0000` | 一天中能够进行自动更新的结束时间 |

当某个表 `tbl` 的修改行数与总行数的比值大于 `tidb_auto_analyze_ratio`，并且当前时间在 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 之间时，TiDB 会在后台执行 `ANALYZE TABLE tbl` 语句自动更新这个表的统计信息。

在查询语句执行时，TiDB 会以 `feedback-probability` 的概率收集反馈信息，并将其用于更新直方图和 Count-Min Sketch。`feedback-probability` 可通过配置文件修改，其默认值是 `0.0`。

### 控制 ANALYZE 并发度

执行 ANALYZE 语句的时候，你可以通过一些参数来调整并发度，以控制对系统的影响。

#### tidb_build_stats_concurrency

目前 ANALYZE 执行的时候会被切分成一个个小的任务，每个任务只负责某一个列或者索引。`tidb_build_stats_concurrency` 可以控制同时执行的任务的数量，其默认值是 4。

#### tidb_distsql_scan_concurrency

在执行分析普通列任务的时候，`tidb_distsql_scan_concurrency` 可以用于控制一次读取的 Region 数量，其默认值是 10。

#### tidb_index_serial_scan_concurrency

在执行分析索引列任务的时候，`tidb_index_serial_scan_concurrency` 可以用于控制一次读取的 Region 数量，其默认值是 1。

### 查看 ANALYZE 状态

在执行 `ANALYZE` 时，可以通过 SQL 语句来查看当前 `ANALYZE` 的状态。

语法如下：

{{< copyable "sql" >}}

```sql
SHOW ANALYZE STATUS [ShowLikeOrWhere];
```

该语句会输出 `ANALYZE` 的状态，可以通过使用 `ShowLikeOrWhere` 来筛选需要的信息。

目前 `SHOW ANALYZE STATUS` 会输出 7 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| table_schema  |  数据库名    |
| table_name | 表名 |
| partition_name| 分区名 |
| job_info | 任务具体信息。如果分析索引则会包含索引名 |
| row_count | 已经分析的行数 |
| start_time | 任务开始执行的时间 |
| state | 任务状态，包括 pending（等待）、running（正在执行）、finished（执行成功）和 failed（执行失败）|

## 统计信息的查看

你可以通过一些语句来查看统计信息的状态。

### 表的元信息

你可以通过 `SHOW STATS_META` 来查看表的总行数以及修改的行数等信息。

语法如下：

{{< copyable "sql" >}}

```sql
SHOW STATS_META [ShowLikeOrWhere];
```

该语句会输出所有表的总行数以及修改行数等信息，你可以通过 ShowLikeOrWhere 来筛选需要的信息。

目前 `SHOW STATS_META` 会输出 6 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| partition_name| 分区名 |
| update_time | 更新时间 |
| modify_count | 修改的行数 |
| row_count | 总行数 |

### 列的元信息

你可以通过 `SHOW STATS_HISTOGRAMS` 来查看列的不同值数量以及 NULL 数量等信息。

语法如下：

{{< copyable "sql" >}}

```sql
SHOW STATS_HISTOGRAMS [ShowLikeOrWhere];
```

该语句会输出所有列的不同值数量以及 NULL 数量等信息，你可以通过 ShowLikeOrWhere 来筛选需要的信息。

目前 `SHOW STATS_HISTOGRAMS` 会输出 8 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| partition_name | 分区名 |
| column_name | 列名 |
| is_index | 是否是索引列 |
| update_time | 更新时间 |
| distinct_count | 不同值数量 |
| null_count | NULL 的数量 |
| avg_col_size | 列平均长度 |

### 直方图桶的信息

你可以通过 `SHOW STATS_BUCKETS` 来查看直方图每个桶的信息。

语法如下：

{{< copyable "sql" >}}

```sql
SHOW STATS_BUCKETS [ShowLikeOrWhere];
```

该语句会输出所有桶的信息，你可以通过 ShowLikeOrWhere 来筛选需要的信息。

目前 `SHOW STATS_BUCKETS` 会输出 10 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| partition_name | 分区名 |
| column_name | 列名 |
| is_index | 是否是索引列 |
| bucket_id | 桶的编号 |
| count | 所有落在这个桶及之前桶中值的数量 |
| repeats | 最大值出现的次数 |
| lower_bound | 最小值 |
| upper_bound | 最大值 |

## 删除统计信息

可以通过执行 `DROP STATS` 语句来删除统计信息。

语法如下：

{{< copyable "sql" >}}

```sql
DROP STATS TableName;
```

该语句会删除 TableName 中所有的统计信息。

## 统计信息的导入导出

### 导出统计信息

统计信息的导出接口如下。

通过以下接口可以获取数据库 `${db_name}` 中的表 `${table_name}` 的 json 格式的统计信息：

{{< copyable "" >}}

```
http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}
```

通过以下接口可以获取数据库 `${db_name}` 中的表 `${table_name}` 在指定时间上的 json 格式统计信息。指定的时间应在 GC SafePoint 之后。

{{< copyable "" >}}

```
http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyyMMddHHmmss}
```

通过以下接口可以获取数据库 `${db_name}` 中的表 `${table_name}` 在指定时间上的 json 格式统计信息。指定的时间应在 GC SafePoint 之后。

{{< copyable "" >}}

```
http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyy-MM-dd HH:mm:ss}
```

### 导入统计信息

导入的统计信息一般是通过统计信息导出接口得到的 json 文件。

语法如下：

{{< copyable "sql" >}}

```sql
LOAD STATS 'file_name';
```

`file_name` 为要导入的统计信息的文件名。
