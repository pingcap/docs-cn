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

在发生增加，删除以及修改语句时，TiDB 会自动更新表的总行数以及修改的行数。这些信息会定期持久化下来，更新的周期可以由 `statsLease` 参数指定，
更新的周期是 5 * `statsLease`, `statsLease` 的默认值是 3s，如果将其指定为 0，那么将不会自动更新。

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
