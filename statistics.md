---
title: 统计信息简介
aliases: ['/docs-cn/dev/statistics/','/docs-cn/dev/reference/performance/statistics/']
---

# 统计信息简介

TiDB 使用统计信息来决定[索引的选择](/choose-index.md)。变量 `tidb_analyze_version` 用于控制所收集到的统计信息。目前 TiDB 中支持两种统计信息：`tidb_analyze_version = 1` 以及 `tidb_analyze_version = 2`。在 v5.1.0 以前的版本中，该变量的默认值为 `1`。在 v5.1.0 中，该变量的默认值为 `2`，作为实验特性启用。两种版本中，TiDB 维护的统计信息如下：

| 信息 | Version 1 | Version 2|
| --- | --- | ---|
| 表的总行数 | √ | √ |
| 列的 Count-Min Sketch | √ | × |
| 索引的 Count-Min Sketch | √ | × |
| 列的 Top-N | √ | √（改善了维护方式和精度） |
| 索引的 Top-N | √（维护精度不足，会产生较大误差） | √（改善了维护方式和精度） |
| 列的直方图 | √ | √（直方图中不包含 Top-N 中出现的值） |
| 索引的直方图 | √ | √（直方图的桶中记录了各自的不同值的个数，且直方图不包含 Top-N 中出现的值） |
| 列的 NULL 值个数 | √ | √ |
| 索引的 NULL 值个数 | √ | √ |
| 列的平均长度 | √ | √ |
| 索引的平均长度 | √ | √ |

Version 2 的统计信息避免了 Version 1 中因为哈希冲突导致的在较大的数据量中可能产生的较大误差，并保持了大多数场景中的估算精度。

本文接下来将简单介绍其中出现的直方图和 Count-Min Sketch 以及 Top-N 这些数据结构，以及详细介绍统计信息的收集和维护。

## 直方图简介

直方图是一种对数据分布情况进行描述的工具，它会按照数据的值大小进行分桶，并用一些简单的数据来描述每个桶，比如落在桶里的值的个数。在 TiDB 中，会对每个表具体的列构建一个等深直方图，区间查询的估算便是借助该直方图来进行。

等深直方图，就是让落入每个桶里的值数量尽量相等。举个例子，比方说对于给定的集合 {1.6, 1.9, 1.9, 2.0, 2.4, 2.6, 2.7, 2.7, 2.8, 2.9, 3.4, 3.5}，并且生成 4 个桶，那么最终的等深直方图就会如下图所示，包含四个桶 [1.6, 1.9]，[2.0, 2.6]，[2.7, 2.8]，[2.9, 3.5]，其桶深均为 3。

![等深直方图示例](/media/statistics-1.png)

在[手动收集统计信息](#手动收集)一节中有控制直方图桶数量上限的参数。当桶数量越多，直方图的估算精度就越高，不过也会同时增大统计信息的内存使用，可以视具体情况来做调整。

## Count-Min Sketch

Count-Min Sketch 是一种哈希结构，当查询中出现诸如 `a = 1` 或者 `IN` 查询（如 `a in (1, 2, 3)`）这样的等值查询时，TiDB 便会使用这个数据结构来进行估算。

由于 Count-Min Sketch 是一个哈希结构，就有出现哈希碰撞的可能。当在 `EXPLAIN` 语句中发现等值查询的估算偏离实际值较大时，就可以认为是一个比较大的值和一个比较小的值被哈希到了一起。这时有以下两种手段来避免这个情况：

- 修改[手动收集统计信息](#手动收集)中提到的 `WITH NUM TOPN` 参数。TiDB 会将出现频率前 x 大的数据单独储存，之后的数据再储存到 Count-Min Sketch 中。因此可以调大这个值来避免一个比较大的值和一个比较小的值被哈希到一起。在 TiDB 中，这个参数的默认值是 20，最大可以设置为 1024。
- 修改[统计信息的收集-手动收集](#手动收集)中提到的 `WITH NUM CMSKETCH DEPTH` 和 `WITH NUM CMSKETCH WIDTH` 两个参数，这两个参数会影响哈希的桶数和碰撞概率，可是适当调大来减少冲突概率，同时它会影响统计信息的内存使用，可以视具体情况来调整。在 TiDB 中，`DEPTH` 的默认值是 5，`WIDTH` 的默认值是 2048。

## Top-N values

Top-N 即是这个列或者这个索引中，出现次数前 n 的值。TiDB 会记录前 n 个值的具体的值以及出现次数。

## 统计信息的收集

### 手动收集

可以通过执行 `ANALYZE` 语句来收集统计信息。

> **注意：**
>
> 在 TiDB 中执行 `ANALYZE TABLE` 语句比在 MySQL 或 InnoDB 中耗时更长。InnoDB 采样的只是少量页面，但 TiDB 会完全重构一系列统计信息。适用于 MySQL 的脚本会误以为执行 `ANALYZE TABLE` 耗时较短。
>
> 如需更快的分析速度，可将 `tidb_enable_fast_analyze` 设置为 `1` 来打开快速分析功能。该参数的默认值为 `0`。
>
> 快速分析功能开启后，TiDB 会随机采样约 10000 行的数据来构建统计信息。因此在数据分布不均匀或者数据量比较少的情况下，统计信息的准确度会比较差。可能导致执行计划不优，比如选错索引。如果可以接受普通 `ANALYZE` 语句的执行时间，则推荐关闭快速分析功能。
>
> `tidb_enable_fast_analyze` 为实验性功能，目前与 `tidb_analyze_version=2` 的统计信息**不完全匹配**。因此开启 `tidb_enable_fast_analyze` 时需要将 `tidb_analyze_version` 的值设置为 `1`。

#### 全量收集

可以通过以下几种语法进行全量收集。

收集 TableNameList 中所有表的统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
```

- `WITH NUM BUCKETS` 用于指定生成直方图的桶数量上限。
- `WITH NUM TOPN` 用于指定生成 TOPN 数目的上限。
- `WITH NUM CMSKETCH DEPTH` 用于指定 CM Sketch 的长。
- `WITH NUM CMSKETCH WIDTH` 用于指定 CM Sketch 的宽。
- `WITH NUM SAMPLES` 用于指定采样的数目。

收集 TableName 中所有的 IndexNameList 中的索引列的统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
```

IndexNameList 为空时会收集所有索引列的统计信息。

收集 TableName 中所有的 PartitionNameList 中分区的统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
```

收集 TableName 中所有的 PartitionNameList 中分区的索引列统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
```

> **注意：**
>
> 为了保证前后统计信息的一致性，在设置 `tidb_analyze_version=2` 时，`ANALYZE TABLE TableName INDEX` 也会收集整个表而不是所给索引的统计信息。

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
ANALYZE INCREMENTAL TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
```

增量收集 TableName 中所有的 PartitionNameList 中分区的索引列统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE INCREMENTAL TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH|SAMPLES];
```

### 自动更新

在发生增加，删除以及修改语句时，TiDB 会自动更新表的总行数以及修改的行数。这些信息会定期持久化下来，更新的周期是 20 * `stats-lease`，`stats-lease` 的默认值是 3s，如果将其指定为 0，那么将不会自动更新。

和统计信息自动更新相关的三个系统变量如下：

|  系统变量名 | 默认值 | 功能 |
|---|---|---|
| `tidb_auto_analyze_ratio`| 0.5 | 自动更新阈值 |
| `tidb_auto_analyze_start_time` | `00:00 +0000` | 一天中能够进行自动更新的开始时间 |
| `tidb_auto_analyze_end_time`   | `23:59 +0000` | 一天中能够进行自动更新的结束时间 |

当某个表 `tbl` 的修改行数与总行数的比值大于 `tidb_auto_analyze_ratio`，并且当前时间在 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 之间时，TiDB 会在后台执行 `ANALYZE TABLE tbl` 语句自动更新这个表的统计信息。

在 v5.0 版本之前，执行查询语句时，TiDB 会以 [`feedback-probability`](/tidb-configuration-file.md#feedback-probability) 的概率收集反馈信息，并将其用于更新直方图和 Count-Min Sketch。**对于 v5.0 版本，该功能默认关闭，暂不建议开启此功能。**

### 控制 ANALYZE 并发度

执行 ANALYZE 语句的时候，你可以通过一些参数来调整并发度，以控制对系统的影响。

#### tidb_build_stats_concurrency

目前 ANALYZE 执行的时候会被切分成一个个小的任务，每个任务只负责某一个列或者索引。`tidb_build_stats_concurrency` 可以控制同时执行的任务的数量，其默认值是 4。

#### tidb_distsql_scan_concurrency

在执行分析普通列任务的时候，`tidb_distsql_scan_concurrency` 可以用于控制一次读取的 Region 数量，其默认值是 15。

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

其中，`ShowLikeOrWhereOpt` 部分的语法图为：

```sql
SHOW STATS_META [ShowLikeOrWhere];
```

目前 `SHOW STATS_META` 会输出 6 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| partition_name| 分区名 |
| update_time | 更新时间 |
| modify_count | 修改的行数 |
| row_count | 总行数 |

> **注意：**
>
> 在 TiDB 根据 DML 语句自动更新总行数以及修改的行数时，`update_time` 也会被更新，因此并不能认为 `update_time` 是最近一次发生 Analyze 的时间。

### 表的健康度信息

通过 `SHOW STATS_HEALTHY` 可以查看表的统计信息健康度，并粗略估计表上统计信息的准确度。当 `modify_count` >= `row_count` 时，健康度为 0；当 `modify_count` < `row_count` 时，健康度为 (1 - `modify_count`/`row_count`) * 100。

`SHOW STATS_HEALTHY` 的语法图为：

![ShowStatsHealthy](/media/sqlgram/ShowStatsHealthy.png)

其中，`ShowLikeOrWhereOpt` 部分的语法图为：

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

目前，`SHOW STATS_HEALTHY` 会输出 4 列，具体如下：

| 语法元素 | 说明            |
| :-------- | :------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| partition_name| 分区名 |
| healthy | 健康度 |

### 列的元信息

你可以通过 `SHOW STATS_HISTOGRAMS` 来查看列的不同值数量以及 NULL 数量等信息。

语法如下：

{{< copyable "sql" >}}

```sql
SHOW STATS_HISTOGRAMS [ShowLikeOrWhere];
```

该语句会输出所有列的不同值数量以及 NULL 数量等信息，你可以通过 ShowLikeOrWhere 来筛选需要的信息。

目前 `SHOW STATS_HISTOGRAMS` 会输出 10 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| partition_name | 分区名 |
| column_name | 根据 is_index 来变化：is_index 为 0 时是列名，为 1 时是索引名 |
| is_index | 是否是索引列 |
| update_time | 更新时间 |
| distinct_count | 不同值数量 |
| null_count | NULL 的数量 |
| avg_col_size | 列平均长度 |
| correlation | 该列与整型主键的皮尔逊系数，表示两列之间的关联程度 |

### 直方图桶的信息

你可以通过 `SHOW STATS_BUCKETS` 来查看直方图每个桶的信息。

语法如下：

{{< copyable "sql" >}}

```sql
SHOW STATS_BUCKETS [ShowLikeOrWhere];
```

语法图：

**SHOW STATS_BUCKETS:**

![SHOW STATS_BUCKETS](/media/sqlgram/SHOW_STATS_BUCKETS.png)

该语句会输出所有桶的信息，你可以通过 ShowLikeOrWhere 来筛选需要的信息。

目前 `SHOW STATS_BUCKETS` 会输出 11 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| partition_name | 分区名 |
| column_name | 根据 is_index 来变化：is_index 为 0 时是列名，为 1 时是索引名 |
| is_index | 是否是索引列 |
| bucket_id | 桶的编号 |
| count | 所有落在这个桶及之前桶中值的数量 |
| repeats | 最大值出现的次数 |
| lower_bound | 最小值 |
| upper_bound | 最大值 |
| ndv | 当前桶内不同值的个数。当 `tidb_analyze_version` = 1 时，该值恒为 0，没有实际意义。 |

### Top-N 信息

你可以通过 `SHOW STATS_TOPN` 来查看当前 TiDB 中收集的 Top-N 值的信息。

语法如下：

{{< copyable "sql" >}}

```sql
SHOW STATS_TOPN [ShowLikeOrWhere];
```

目前 `SHOW STATS_TOPN` 会输出 7 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| partition_name | 分区名 |
| column_name | 根据 is_index 来变化：is_index 为 0 时是列名，为 1 时是索引名 |
| is_index | 是否是索引列 |
| value | 该列的值 |
| count | 该值出现的次数 |

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

## 另请参阅

* [DROP STATS](/sql-statements/sql-statement-drop-stats.md)
