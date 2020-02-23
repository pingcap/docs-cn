---
title: 统计信息简介
category: user guide
---

# 统计信息简介

TiDB 优化器会根据统计信息来选择最优的执行计划。统计信息收集了表级别和列级别的信息，表的统计信息包括总行数，以及修改的行数。列的统计信息包括不同值的数量，NULL 的数量，以及该列的直方图信息。

## 统计信息的收集

### 手动收集

你可以通过执行 `ANALYZE` 语句来收集统计信息。

语法：
```sql
ANALYZE TABLE TableNameList
> 该语句会收集 TableNameList 中所有表的统计信息。

ANALYZE TABLE TableName INDEX IndexNameList
> 该语句会收集 TableName 中所有的 IndexNameList 中的索引列的统计信息。
```

### 自动更新

在发生增加，删除以及修改语句时，TiDB 会自动更新表的总行数以及修改的行数。这些信息会定期持久化下来，
更新的周期是 5 * `stats-lease`, `stats-lease` 的默认值是 3s，如果将其指定为 0，那么将不会自动更新。

### 控制 ANALYZE 并发度

执行 ANALYZE 语句的时候，你可以通过一些参数来调整并发度，以控制对系统的影响。

#### tidb_build_stats_concurrency

目前 ANALYZE 执行的时候会被切分成一个个小的任务，每个任务只负责某一个列或者索引。`tidb_build_stats_concurrency` 可以控制同时执行的任务的数量，其默认值是 4。

#### tidb_distsql_scan_concurrency

在执行分析普通列任务的时候，`tidb_distsql_scan_concurrency` 可以用于控制一次读取的 Region 数量，其默认值是 10。

#### tidb_index_serial_scan_concurrency

在执行分析索引列任务的时候，`tidb_index_serial_scan_concurrency` 可以用于控制一次读取的 Region 数量，其默认值是 1。

## 统计信息的查看

你可以通过一些语句来查看统计信息的状态。

### 表的元信息

你可以通过 `SHOW STATS_META` 来查看表的总行数以及修改的行数等信息。

语法：
```sql
SHOW STATS_META [ShowLikeOrWhere]
> 该语句会输出所有表的总行数以及修改行数等信息，你可以通过使用 ShowLikeOrWhere 来筛选需要的信息。
```

目前 `SHOW STATS_META` 会输出 5 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| update_time | 更新时间 |
| modify_count | 修改的行数 |
| row_count | 总行数 |

### 列的元信息

你可以通过 `SHOW STATS_HISTOGRAMS` 来查看列的不同值数量以及 NULL 数量等信息。

语法：
```sql
SHOW STATS_HISTOGRAMS [ShowLikeOrWhere]
> 该语句会输出所有列的不同值数量以及 NULL 数量等信息，你可以通过使用 ShowLikeOrWhere 来筛选需要的信息。
```

目前 `SHOW STATS_HISTOGRAMS` 会输出 7 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| column_name | 列名 |
| is_index | 是否是索引列 |
| update_time | 更新时间 |
| distinct_count | 不同值数量 |
| null_count | NULL 的数量 |

### 直方图桶的信息

你可以通过 `SHOW STATS_BUCKETS` 来查看直方图每个桶的信息。

语法：
```sql
SHOW STATS_BUCKETS [ShowLikeOrWhere]
> 该语句会输出所有桶的信息，你可以通过使用 ShowLikeOrWhere 来筛选需要的信息。
```

目前 `SHOW STATS_BUCKETS` 会输出 9 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| column_name | 列名 |
| is_index | 是否是索引列 |
| bucket_id | 桶的编号 |
| count | 所有落在这个桶及之前桶中值的数量 |
| repeats | 最大值出现的次数 |
| lower_bound | 最小值 |
| upper_bound | 最大值 |

## 删除统计信息

可以通过执行 `DROP STATS` 语句来删除统计信息。

语法：
```sql
DROP STATS TableName
> 该语句会删除 TableName 中所有的统计信息。
```
