---
title: 统计信息简介
aliases: ['/docs-cn/dev/statistics/','/docs-cn/dev/reference/performance/statistics/']
---

# 统计信息简介

TiDB 使用统计信息来决定[索引的选择](/choose-index.md)。

## 统计信息版本

变量 `tidb_analyze_version` 用于控制所收集到的统计信息。目前 TiDB 中支持两种统计信息：`tidb_analyze_version = 1` 以及 `tidb_analyze_version = 2`。在 v5.3.0 及之后的版本中，该变量的默认值为 `2`。如果从 v5.3.0 之前版本的集群升级至 v5.3.0 及之后的版本，`tidb_analyze_version` 的默认值不发生变化。

Version 2 的统计信息避免了 Version 1 中因为哈希冲突导致的在较大的数据量中可能产生的较大误差，并保持了大多数场景中的估算精度。

两种版本中，TiDB 维护的统计信息如下：

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

当 `tidb_analyze_version = 2` 时，如果执行 ANALYZE 语句后发生 OOM，需要设置全局变量 `tidb_analyze_version = 1`，回退到 Version 1，然后根据情况进行以下操作：

- 如果 ANALYZE 语句是手动执行的，你需要手动 ANALYZE 每张需要的表：

    ```sql
    SELECT DISTINCT(CONCAT('ANALYZE TABLE ', table_schema, '.', table_name, ';')) FROM information_schema.tables, mysql.stats_histograms WHERE stats_ver = 2 AND table_id = tidb_table_id;
    ```

- 如果 ANALYZE 语句是开启了自动 ANALYZE 后 TiDB 自动执行的，使用以下 SQL 语句生成 DROP STATS 的语句并执行：

    ```sql
    SELECT DISTINCT(CONCAT('DROP STATS ', table_schema, '.', table_name, ';')) FROM information_schema.tables, mysql.stats_histograms WHERE stats_ver = 2 AND table_id = tidb_table_id;
    ```

- 如果上一条语句返回结果太长，不方便复制粘贴，可以将结果导出到临时文件后，再执行:

    ```sql
    SELECT DISTINCT... INTO outfile '/tmp/sql.txt';
    mysql -h ${TiDB_IP} -u user -P ${TIDB_PORT} ... < '/tmp/sql.txt';
    ```

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

目前 TiDB 收集统计信息为全量收集，通过 `ANALYZE TABLE` 语句来实现。

> **注意：**
>
> - 在 TiDB 中执行 `ANALYZE TABLE` 语句比在 MySQL 或 InnoDB 中耗时更长。InnoDB 采样的只是少量页面，但 TiDB 会完全重构一系列统计信息。适用于 MySQL 的脚本会误以为执行 `ANALYZE TABLE` 耗时较短。
> - 从 v7.5.0 开始，统计信息[快速分析 (`tidb_enable_fast_analyze`)](/system-variables.md#tidb_enable_fast_analyze) 和[增量收集](https://docs.pingcap.com/zh/tidb/v7.4/statistics#增量收集)废弃。

可以通过以下几种语法进行全量收集。

收集 TableNameList 中所有表的统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

- `WITH NUM BUCKETS` 用于指定生成直方图的桶数量上限。
- `WITH NUM TOPN` 用于指定生成 TOPN 数目的上限。
- `WITH NUM CMSKETCH DEPTH` 用于指定 CM Sketch 的长。
- `WITH NUM CMSKETCH WIDTH` 用于指定 CM Sketch 的宽。
- `WITH NUM SAMPLES` 用于指定采样的数目。
- `WITH FLOAT_NUM SAMPLERATE` 用于指定采样率。

`WITH NUM SAMPLES` 与 `WITH FLOAT_NUM SAMPLERATE` 这两种设置对应了两种不同的收集采样的算法。

- `WITH NUM SAMPLES` 指定了采样集的大小，在 TiDB 中是以蓄水池采样的方式实现。当表较大时，不推荐使用这种方式收集统计信息。因为蓄水池采样中间结果集会产生一定的冗余结果，会对内存等资源造成额外的压力。
- `WITH FLOAT_NUM SAMPLERATE` 是在 v5.3.0 中引入的采样方式，指定的采样率的大小，是取值范围 `(0, 1]` 的参数。在 TiDB 中是以伯努利采样的方式实现，更适合对较大的表进行采样，在收集效率和资源使用上更有优势。

在 v5.3.0 之前 TiDB 采用蓄水池采样的方式收集统计信息。自 v5.3.0 版本起，TiDB Version 2 的统计信息默认会选取伯努利采样的方式收集统计信息。若要重新使用蓄水池采样的方式采样，可以使用 `WITH NUM SAMPLES` 语句。

> **注意：**
>
> 目前采样率基于自适应算法进行计算。当你通过 [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) 可以观察到一个表的行数时，可通过这个行数去计算采集 10 万行所对应的采样率。如果你观察不到这个值，可通过 [`TABLE_STORAGE_STATS`](/information-schema/information-schema-table-storage-stats.md) 表的 `TABLE_KEYS` 列作为另一个参考来计算采样率。
>
> 通常情况下，`STATS_META` 相对 `TABLE_KEYS` 更可信，但是通过 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 等方式导入数据结束后，`STATS_META` 结果是 `0`。为了处理这个情况，你可以在 `STATS_META` 的结果远小于 `TABLE_KEYS` 的结果时，使用 `TABLE_KEYS` 计算采样率。

#### 收集部分列的统计信息

执行 SQL 语句时，优化器在大多数情况下只会用到部分列（例如，`WHERE`、`JOIN`、`ORDER BY`、`GROUP BY` 子句中出现的列）的统计信息，这些被用到的列称为 `PREDICATE COLUMNS`。

如果一个表有很多列，收集所有列的统计信息会有较大的开销。为了降低开销，你可以只收集指定列或者 `PREDICATE COLUMNS` 的统计信息供优化器使用。

> **注意：**
>
> - 收集部分列的统计信息的功能仅适用于 [`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-从-v510-版本开始引入) 的情况。
> - TiDB v7.2.0 引入了系统变量 [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-从-v720-版本开始引入)，该变量可以控制在执行 `ANALYZE` 命令收集统计信息时，跳过哪些类型的列的统计信息收集。该变量仅适用于 `tidb_analyze_version = 2` 的情况。

- 如果要收集指定列的统计信息，请使用以下语法：

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName COLUMNS ColumnNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    其中，`ColumnNameList` 表示指定列的名称列表。如果需要指定多列，请使用用逗号 `,` 分隔列名。例如, `ANALYZE table t columns a, b`。该语法除了收集指定表中指定列的统计信息，将同时收集该表中索引列的统计信息以及所有索引的统计信息。

    > **注意：**
    >
    > 该语法为全量收集。例如，在使用该语法收集了 a 列和 b 列的统计信息之后，如果还想要增加收集 c 列的统计信息，需要在语法中同时指定这三列 `ANALYZE TABLE t columns a, b, c`，而不是只指定新增的那一列 `ANALYZE TABLE t COLUMNS c`。

- 如果要收集 `PREDICATE COLUMNS` 的统计信息，请进行以下操作：

    > **警告：**
    >
    > 收集 `PREDICATE COLUMNS` 的统计信息目前为实验特性，不建议在生产环境中使用。

    1. 设置系统变量 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-从-v540-版本开始引入) 的值为 `ON` 开启 TiDB 对 `PREDICATE COLUMNS` 的收集。

        开启后，TiDB 将每隔 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease) 时间将 `PREDICATE COLUMNS` 信息写入系统表 `mysql.column_stats_usage`。

    2. 在业务的查询模式稳定以后，使用以下语法收集 `PREDICATE COLUMNS` 的统计信息。

        {{< copyable "sql" >}}

        ```sql
        ANALYZE TABLE TableName PREDICATE COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
        ```

        该语法除了收集指定表中 `PREDICATE COLUMNS` 的统计信息，将同时收集该表中索引列的统计信息以及所有索引的统计信息。

        > **注意：**
        >
        > - 如果系统表 `mysql.column_stats_usage` 中没有关于该表的`PREDICATE COLUMNS` 记录，执行以上语句会收集该表中所有列的统计信息以及所有索引的统计信息。
        > - 使用该语法收集统计信息后，当执行一种新的类型的 SQL 查询时，优化器可能会暂时使用旧的或者 pseudo 的列统计信息，然后在下一次收集统计信息的时候收集该列的统计信息。

- 如果要收集所有列的统计信息以及所有索引的统计信息，可以使用以下语法：

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName ALL COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

如果要持久化 `ANALYZE` 语句中列的配置（包括 `COLUMNS ColumnNameList`、`PREDICATE COLUMNS`、`ALL COLUMNS`），请设置系统变量 `tidb_persist_analyze_options` 的值设置为 `ON` 以开启 [ANALYZE 配置持久化](/statistics.md#analyze-配置持久化)特性。开启 ANALYZE 配置持久化特性后：

- 当 TiDB 自动收集统计信息或者你手动执行 `ANALYZE` 语句收集统计信息但未指定列的配置时，TiDB 会继续沿用之前持久化的配置。
- 当多次手动执行 `ANALYZE` 语句并指定列的配置时，TiDB 会使用最新一次 `ANALYZE` 指定的配置项覆盖上一次记录的持久化配置。

如果你想查看一个表中哪些列是 `PREDICATE COLUMNS`，哪些列的统计信息已经被收集，可以使用以下语法：

{{< copyable "sql" >}}

```sql
SHOW COLUMN_STATS_USAGE [ShowLikeOrWhere];
```

`SHOW COLUMN_STATS_USAGE` 会输出 6 列，具体如下：

| 列名 | 说明            |
| -------- | ------------- |
| Db_name  |  数据库名    |
| Table_name | 表名 |
| Partition_name | 分区名 |
| Column_name | 列名 |
| Last_used_at | 该列统计信息在最近一次查询优化中被用到的时间 |
| Last_analyzed_at | 该列统计信息最近一次被收集的时间 |

在以下示例中，执行 `ANALYZE TABLE t PREDICATE COLUMNS;` 后，TiDB 将收集 `b`，`c`，`d` 列的统计信息，其中 `b` 列是 `PREDICATE COLUMN`，`c` 列和 `d` 列是索引列。

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_column_tracking = ON;
Query OK, 0 rows affected (0.00 sec)

CREATE TABLE t (a INT, b INT, c INT, d INT, INDEX idx_c_d(c, d));
Query OK, 0 rows affected (0.00 sec)

-- 在此查询中优化器用到了 b 列的统计信息。
SELECT * FROM t WHERE b > 1;
Empty set (0.00 sec)

-- 等待一段时间（100 * stats-lease）后，TiDB 将收集的 `PREDICATE COLUMNS` 写入 mysql.column_stats_usage。
-- 指定 `last_used_at IS NOT NULL` 表示显示 TiDB 收集到的 `PREDICATE COLUMNS`。
SHOW COLUMN_STATS_USAGE WHERE db_name = 'test' AND table_name = 't' AND last_used_at IS NOT NULL;
+---------+------------+----------------+-------------+---------------------+------------------+
| Db_name | Table_name | Partition_name | Column_name | Last_used_at        | Last_analyzed_at |
+---------+------------+----------------+-------------+---------------------+------------------+
| test    | t          |                | b           | 2022-01-05 17:21:33 | NULL             |
+---------+------------+----------------+-------------+---------------------+------------------+
1 row in set (0.00 sec)

ANALYZE TABLE t PREDICATE COLUMNS;
Query OK, 0 rows affected, 1 warning (0.03 sec)

-- 指定 `last_analyzed_at IS NOT NULL` 表示显示收集过统计信息的列。
SHOW COLUMN_STATS_USAGE WHERE db_name = 'test' AND table_name = 't' AND last_analyzed_at IS NOT NULL;
+---------+------------+----------------+-------------+---------------------+---------------------+
| Db_name | Table_name | Partition_name | Column_name | Last_used_at        | Last_analyzed_at    |
+---------+------------+----------------+-------------+---------------------+---------------------+
| test    | t          |                | b           | 2022-01-05 17:21:33 | 2022-01-05 17:23:06 |
| test    | t          |                | c           | NULL                | 2022-01-05 17:23:06 |
| test    | t          |                | d           | NULL                | 2022-01-05 17:23:06 |
+---------+------------+----------------+-------------+---------------------+---------------------+
3 rows in set (0.00 sec)
```

#### 收集索引的统计信息

如果要收集 TableName 中 IndexNameList 里所有索引的统计信息，请使用以下语法：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

当 IndexNameList 为空时，该语法将收集 TableName 中所有索引的统计信息。

> **注意：**
>
> 为了保证前后统计信息的一致性，当设置 `tidb_analyze_version=2` 时，该语句也会收集整个表的统计信息（包括所有列和所有索引的统计信息）而不限于索引的统计信息。

#### 收集分区的统计信息

- 如果要收集 TableName 中所有的 PartitionNameList 中分区的统计信息，请使用以下语法：

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

- 如果要收集 TableName 中所有的 PartitionNameList 中分区的索引统计信息，请使用以下语法：

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

- 当收集分区的统计信息时，如果只[收集部分列的统计信息](/statistics.md#收集部分列的统计信息)，请使用以下语法：

    > **警告：**
    >
    > 收集 `PREDICATE COLUMNS` 的统计信息目前为实验特性，不建议在生产环境中使用。

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [COLUMNS ColumnNameList|PREDICATE COLUMNS|ALL COLUMNS] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

#### 动态裁剪模式下的分区表统计信息

分区表在开启[动态裁剪模式](/partitioned-table.md#动态裁剪模式)的情况下，TiDB 将收集表级别的汇总统计信息，以下称 GlobalStats。 目前 GlobalStats 由分区统计信息合并汇总得到。在动态裁剪模式开启的情况下，任一分区上的统计信息更新都会触发 GlobalStats 的更新。

> **注意：**
>
> - 当触发 GlobalStats 更新时，如果 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-从-v730-版本开始引入) 关闭：
>
>     - 若某些分区上缺少统计信息（比如新增的未 analyze 过的分区），会停止生成 GlobalStats，并通过 warning 信息提示用户缺少分区的统计信息。
>     - 若某些列的统计信息合并过程中，缺少某些分区在该列上的统计信息（在不同分区上 analyze 时指定了不同的列），会停止生成 GlobalStats，并通过 warning 信息提示用户缺少列在分区上的统计信息。
>
> - 当触发 GlobalStats 更新时，如果 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-从-v730-版本开始引入) 开启：
>
>     如果某些分区缺失全部或者部分列的统计信息，TiDB 生成 GlobalStats 时会跳过缺失的分区统计信息，不影响 GlobalStats 生成。
>
> - 在动态裁剪模式开启的情况下，分区和表的 ANALYZE 配置需要保持一致，因此 ANALYZE TABLE TableName PARTITION PartitionNameList 命令后指定的 COLUMNS 配置和 WITH 后指定的 OPTIONS 配置将被忽略，并会通过 warning 信息提示用户。

### 自动更新

在发生增加，删除以及修改语句时，TiDB 会自动更新表的总行数以及修改的行数。这些信息会定期持久化下来，更新的周期为 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)。`stats-lease` 配置项的默认值是 3s，如果将其指定为 0，那么统计信息将不会自动更新。

#### 相关系统变量

|  系统变量名 | 默认值 | 功能 |
|---|---|---|
| [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) | 0.5 | 自动更新阈值 |
| [`tidb_auto_analyze_start_time`](/system-variables.md#tidb_auto_analyze_start_time) | `00:00 +0000` | 一天中能够进行自动更新的开始时间 |
| [`tidb_auto_analyze_end_time`](/system-variables.md#tidb_auto_analyze_end_time) | `23:59 +0000` | 一天中能够进行自动更新的结束时间 |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-从-v640-版本开始引入)   | `1` | TiDB 自动 analyze 分区表（即自动更新分区表的统计信息）时，每次同时 analyze 分区的个数 |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) | `ON` | 是否启用优先队列来调度自动收集统计信息的任务。开启该变量后，TiDB 会优先收集那些更有收集价值的表，例如新创建的索引、发生分区变更的分区表等。同时，TiDB 也会优先处理那些健康度较低的表，将它们安排在队列的前端。 |

当某个表 `tbl` 的修改行数与总行数的比值大于 `tidb_auto_analyze_ratio`，并且当前时间在 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 之间时，TiDB 会在后台执行 `ANALYZE TABLE tbl` 语句自动更新这个表的统计信息。

为了避免小表因为少量数据修改而频繁触发自动更新，当表的行数小于 1000 时，TiDB 不会触发对此表的自动更新。你可以通过 `SHOW STATS_META` 来查看表的行数情况。

#### 关闭自动更新

如果发现自动更新统计信息消耗过多的资源，影响在线业务，可以通过系统变量 [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-从-v610-版本开始引入) 关闭自动更新。

#### 终止后台的 `ANALYZE` 任务

从 TiDB v6.0 起，TiDB 支持通过 `KILL` 语句终止正在后台运行的 `ANALYZE` 任务。如果发现正在后台运行的 `ANALYZE` 任务消耗大量资源影响业务，你可以通过以下步骤终止该 `ANALYZE` 任务：

1. 执行以下 SQL 语句：

    {{< copyable "sql" >}}

    ```sql
    SHOW ANALYZE STATUS
    ```

    查看 `instance` 列和 `process_id` 列获得正在执行后台 `ANALYZE` 任务的 TiDB 实例地址和任务 `ID`。

2. 终止正在后台运行的 `ANALYZE` 任务。

   - 如果 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-从-v610-版本开始引入) 的值为 `true` (默认为 `true`），你可以直接执行 `KILL TIDB ${id};` 语句。其中，${id} 为上一步中查询得到的后台 `ANALYZE` 任务的 `ID`。
   - 如果 `enable-global-kill` 的值为 `false`，你需要先使用客户端连接到执行后台 `ANALYZE` 任务的 TiDB 实例，然后再执行 `KILL TIDB ${id};` 语句。如果使用客户端连接到其他 TiDB 实例，或者客户端和 TiDB 中间有代理，`KILL` 语句不能终止后台的 `ANALYZE` 任务。

关于 `KILL` 语句的更多信息，请参考 [`KILL [TIDB]`](/sql-statements/sql-statement-kill.md)。

### 控制 ANALYZE 并发度

执行 ANALYZE 语句的时候，你可以通过一些系统变量来调整并发度，以控制对系统的影响。

相关系统变量的关系如下图所示：

![analyze_concurrency](/media/analyze_concurrency.png)

`tidb_build_stats_concurrency`、`tidb_build_sampling_stats_concurrency` 和 `tidb_analyze_partition_concurrency` 为上下游关系。实际的总并发为：`tidb_build_stats_concurrency`* (`tidb_build_sampling_stats_concurrency` + `tidb_analyze_partition_concurrency`) 。所以在变更这些参数的时候，需要同时考虑这三个参数的值。建议按 `tidb_analyze_partition_concurrency`、`tidb_build_sampling_stats_concurrency`、`tidb_build_stats_concurrency` 的顺序逐个调节，并观察对系统的影响。这三个参数的值越大，对系统的资源开销就越大。

#### `tidb_build_stats_concurrency`

`ANALYZE` 在执行时会被切分成一个个小任务，每个任务只负责某一个列或者索引的统计信息收集。[`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency) 用于控制可以同时执行的小任务的数量，其默认值是 `2`。TiDB v7.4.0 及其之前版本默认值为 `4`。

#### `tidb_build_sampling_stats_concurrency`

在执行 `ANALYZE` 普通列任务的时候，[`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-从-v750-版本开始引入) 可以用于控制执行采样任务的并发数量，其默认值是 `2`。

#### `tidb_analyze_partition_concurrency`

在执行 `ANALYZE` 的时候，[`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency) 可以用于控制对分区表统计信息进行读写的并发度，其默认值是 `2`。TiDB v7.4.0 及其之前版本默认值为 `1`。

#### `tidb_distsql_scan_concurrency`

在执行分析普通列任务的时候，[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 可以用于控制一次读取的 Region 数量，其默认值是 15。修改该变量值会影响查询性能，请谨慎调整。

#### `tidb_index_serial_scan_concurrency`

在执行分析索引列任务的时候，[`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency) 可以用于控制一次读取的 Region 数量，其默认值是 1。修改该变量值会影响查询性能，请谨慎调整。

### ANALYZE 配置持久化

从 v5.4.0 起，TiDB 支持 `ANALYZE` 配置持久化功能，方便后续收集统计信息时沿用已有配置项。

TiDB 支持持久化的配置项包括：

| 配置项 | 对应的 ANALYZE 语法 |
| --- | --- |
| 直方图桶数 | WITH NUM BUCKETS |
| TopN 个数 | WITH NUM TOPN |
| 采样数 | WITH NUM SAMPLES |
| 采样率 | WITH FLOATNUM SAMPLERATE |
| ANALYZE 的列的类型 | AnalyzeColumnOption ::= ( 'ALL COLUMNS' \| 'PREDICATE COLUMNS' \| 'COLUMNS' ColumnNameList ) |
| ANALYZE 的列 | ColumnNameList ::= Identifier ( ',' Identifier )* |

#### 开启 ANALYZE 配置持久化功能

`ANALYZE` 配置持久化功能默认开启（系统变量 `tidb_analyze_version` 为默认值 `2`，`tidb_persist_analyze_options` 为默认值 `ON`），用于记录手动执行 `ANALYZE` 语句时指定的持久化配置项。记录后，当 TiDB 下一次自动更新统计信息或者你手动收集统计信息但未指定配置项时，TiDB 会按照记录的配置项收集统计信息。

要查询用于自动分析操作的特定表上持久化的配置，可以使用以下 SQL 语句：

```sql
SELECT sample_num, sample_rate, buckets, topn, column_choice, column_ids FROM mysql.analyze_options opt JOIN information_schema.tables tbl ON opt.table_id = tbl.tidb_table_id WHERE tbl.table_schema = '{db_name}' AND tbl.table_name = '{table_name}';
```

TiDB 将使用最新 `ANALYZE` 语句指定的配置覆盖先前记录的持久配置。例如，如果你运行 `ANALYZE TABLE t WITH 200 TOPN;` ，它将在 `ANALYZE` 语句中设置前 200 个值。随后，执行 `ANALYZE TABLE t WITH 0.1 SAMPLERATE;` 将为自动 `ANALYZE` 语句同时设置前 200 个值和 0.1 的采样率，类似于 `ANALYZE TABLE t WITH 200 TOPN, 0.1 SAMPLERATE;` 。

#### 关闭 ANALYZE 配置持久化功能

要关闭 `ANALYZE` 配置持久化功能，请设置系统变量 `tidb_persist_analyze_options` 为 `OFF`。由于 `ANALYZE` 配置持久化功能在 `tidb_analyze_version = 1` 的情况下不适用，因此设置 `tidb_analyze_version = 1` 同样会达到关闭配置持久化的效果。

关闭 `ANALYZE` 配置持久化功能后，已持久化的配置记录不会被清除。因此，当再次开启该功能时，TiDB 会继续使用之前记录的持久化配置收集统计信息。

> **注意：**
>
> 当再次开启 `ANALYZE` 配置持久化功能时，如果之前记录的持久化配置项已经不适用当前的数据，请手动执行 `ANALYZE` 语句并指定新的持久化配置项。

#### 分区表的 ANALYZE 配置持久化功能

在静态裁剪模式下 ANALYZE 分区表时，配置持久化遵守：

- ANALYZE TABLE 时会持久化表级别的配置和实际被 ANALYZE 的所有分区的配置
- 分区的统计信息会继承使用表级别的持久化配置
- ANALYZE TABLE ... PARTITION ... WITH ... 所指定的分区配置只持久化到分区级别，不会影响表级别的持久化配置
- 当 ANALYZE 语句指定了配置，且同时存在持久化配置时，按照语句 > 分区 > 表的优先级继承和重写配置信息

在[动态裁剪模式](/partitioned-table.md#动态裁剪模式)下 ANALYZE 分区表时，配置持久化遵守：

- ANALYZE TABLE 时只持久化表级别的配置
- 分区的统计信息会继承使用表级别的持久化配置
- GlobalStats 会使用表级别的持久化配置
- ANALYZE TABLE ... PARTITION ... WITH ... 所指定的分区配置会被忽略，且不会被持久化

### 统计信息收集的内存限制

> **警告：**
>
> 目前限制 ANALYZE 的内存使用量为实验特性，在生产环境中使用时可能存在内存统计有误差的情况。

TiDB 从 v6.1.0 开始引入了统计信息收集的内存限制，你可以通过 [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-从-v610-版本开始引入) 变量来控制 TiDB 更新统计信息时的最大总内存占用。

要合理地配置 `tidb_mem_quota_analyze` 值，你需要考虑集群的数据。在使用默认采样率的情况下，主要考虑列的数量、列上的值的大小，以及 TiDB 的内存配置。你可参考以下建议来配置变量的最大值和最小值：

> **注意：**
>
> 以下配置建议仅供参考，实际配置需要在真实场景中测试确定。

- 最小值：需要大于 TiDB 从集群上列最多的表收集统计信息时使用的最大内存。一个粗略的参考信息是，在测试集上，20 列的表在默认配置下，统计信息收集的最大内存使用约为 800 MiB；160 列的表在默认配置下，统计信息收集的最大内存使用约为 5 GiB。
- 最大值：需要小于集群在不进行统计信息收集时的内存空余量。

### 查看 ANALYZE 状态

在执行 `ANALYZE` 时，可以通过 SQL 语句来查看当前 `ANALYZE` 的状态。

语法如下：

{{< copyable "sql" >}}

```sql
SHOW ANALYZE STATUS [ShowLikeOrWhere];
```

该语句会输出 `ANALYZE` 的状态，可以通过使用 `ShowLikeOrWhere` 来筛选需要的信息。

目前 `SHOW ANALYZE STATUS` 会输出 11 列，具体如下：

| 列名 | 说明            |
| -------- | ------------- |
| table_schema  |  数据库名    |
| table_name | 表名 |
| partition_name| 分区名 |
| job_info | 任务具体信息。如果分析索引，该信息会包含索引名。当 `tidb_analyze_version =2` 时，该信息会包含采样率等配置项。 |
| processed_rows | 已经分析的行数 |
| start_time | 任务开始执行的时间 |
| end_time | 任务结束执行的时间 |
| state | 任务状态，包括 pending（等待）、running（正在执行）、finished（执行成功）和 failed（执行失败）|
| fail_reason | 任务失败的原因。如果执行成功则为 `NULL`。 |
| instance | 执行任务的 TiDB 实例 |
| process_id | 执行任务的 process ID |

从 TiDB v6.1.0 起，执行 `SHOW ANALYZE STATUS` 语句将显示集群级别的任务，且 TiDB 重启后仍能看到重启之前的任务记录。在 TiDB v6.1.0 之前，执行 `SHOW ANALYZE STATUS` 语句仅显示实例级别的任务，且 TiDB 重启后任务记录会被清空。

`SHOW ANALYZE STATUS` 仅显示最近的任务记录。从 TiDB v6.1 起，你可以通过系统表 `mysql.analyze_jobs` 查看过去 7 天内的历史记录。

当设置了 [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-从-v610-版本开始引入) 且 TiDB 后台的统计信息自动更新任务的内存占用超过了这个阈值时，自动更新任务会重试。失败的任务和重试的任务都可以在 `SHOW ANALYZE STATUS` 的结果中查看。

当 [`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-从-v610-版本开始引入) 大于 0 时，如果后台统计信息自动更新任务的执行时间超过这个阈值，该任务会被终止。

```sql
mysql> SHOW ANALYZE STATUS [ShowLikeOrWhere];
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| Table_schema | Table_name | Partition_name | Job_info                                                                                  | Processed_rows | Start_time          | End_time            | State    | Fail_reason                                                                   |
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| test         | sbtest1    |                | retry auto analyze table all columns with 100 topn, 0.055 samplerate                      |        2000000 | 2022-05-07 16:41:09 | 2022-05-07 16:41:20 | finished | NULL                                                                          |
| test         | sbtest1    |                | auto analyze table all columns with 100 topn, 0.5 samplerate                              |              0 | 2022-05-07 16:40:50 | 2022-05-07 16:41:09 | failed   | analyze panic due to memory quota exceeds, please try with smaller samplerate |
```

## 统计信息的查看

你可以通过一些语句来查看统计信息的状态。

### 表的元信息

你可以通过 `SHOW STATS_META` 来查看表的总行数以及修改的行数等信息。

语法如下：

{{< copyable "sql" >}}

```sql
SHOW STATS_META [ShowLikeOrWhere];
```

其中，`ShowLikeOrWhereOpt` 部分的语法图为：

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

目前 `SHOW STATS_META` 会输出 6 列，具体如下：

| 列名 | 说明            |
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

语法如下：

{{< copyable "sql" >}}

```sql
SHOW STATS_HEALTHY [ShowLikeOrWhere];
```

`SHOW STATS_HEALTHY` 的语法图为：

![ShowStatsHealthy](/media/sqlgram/ShowStatsHealthy.png)

目前，`SHOW STATS_HEALTHY` 会输出 4 列，具体如下：

| 列名 | 说明            |
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

| 列名 | 说明            |
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

| 列名 | 说明            |
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

| 列名 | 说明            |
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

{{< copyable "sql" >}}

```sql
DROP STATS TableName;
```

该语句会删除 TableName 中所有的统计信息，如果是分区表，包括所有分区的统计信息和分区动态裁剪模式下生成的 GlobalStats。

{{< copyable "sql" >}}

```sql
DROP STATS TableName PARTITION PartitionNameList;
```

该语句只删除 PartitionNameList 中对应的分区的统计信息。

{{< copyable "sql" >}}

```sql
DROP STATS TableName GLOBAL;
```

该语句只删除该表在分区动态裁剪模式下生成的 GlobalStats。

## 统计信息的加载

默认情况下，列的统计信息占用空间大小不同，TiDB 对统计信息的加载方式也会不同。

- 对于 count、distinctCount、nullCount 等占用空间较小的统计信息，只要有数据更新，TiDB 就会自动将对应的统计信息加载进内存供 SQL 优化阶段使用。
- 对于直方图、TopN、CMSketch 等占用空间较大的统计信息，为了确保 SQL 执行的性能，TiDB 会按需进行异步加载。例如，对于直方图，只有当某条 SQL 语句的优化阶段使用到了某列的直方图统计信息时，TiDB 才会将该列的直方图信息加载到内存。按需异步加载的优势是统计信息加载不会影响到 SQL 执行的性能，但在 SQL 优化时有可能使用不完整的统计信息。

从 v5.4.0 开始，TiDB 引入了统计信息同步加载的特性，支持执行当前 SQL 语句时将直方图、TopN、CMSketch 等占用空间较大的统计信息同步加载到内存，提高该 SQL 语句优化时统计信息的完整性。

要开启该特性，请将系统变量 [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-从-v540-版本开始引入) 的值设置为 SQL 优化等待加载列的完整统计信息的超时时间（单位为毫秒）。该变量默认值为 100，代表开启统计信息同步加载。

开启该特性后，你可以进一步配置该特性：

- 通过修改系统变量 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-从-v540-版本开始引入) 的值控制 SQL 优化等待超时后的行为。该变量默认值为 `ON`，代表超时后 SQL 优化过程不会使用任何列上的直方图、TopN 或 CMSketch。当设置该变量为 `OFF` 时，代表超时后 SQL 执行失败。
- 通过修改 TiDB 配置项 [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-从-v540-版本开始引入) 的值控制统计信息同步加载可以并发处理的最大列数。该配置项的默认值为 `5`。
- 通过修改 TiDB 配置项 [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-从-v540-版本开始引入) 的值设置统计信息同步加载最多可以缓存多少列的请求。该配置项的默认值为 `1000`。

在 TiDB 启动阶段，初始统计信息加载完成之前执行的 SQL 可能有不合理的执行计划，从而影响性能。为了避免这种情况，从 v7.1.0 开始，TiDB 引入了配置项 [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入)。你可以控制 TiDB 启动时是否在统计信息初始化完成后再对外提供服务。该配置项从 v7.2.0 起默认开启。

从 v7.1.0 开始，TiDB 引入了配置参数 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-从-v710-版本开始引入) 用于控制是否开启轻量级的统计信息初始化。

- 当 `lite-init-stats` 为 `true` 时，统计信息初始化时列和索引的直方图、TopN、Count-Min Sketch 均不会加载到内存中。
- 当 `lite-init-stats` 为 `false` 时，统计信息初始化时索引和主键的直方图、TopN、Count-Min Sketch 会被加载到内存中，非主键列的直方图、TopN、Count-Min Sketch 不会加载到内存中。当优化器需要某一索引或者列的直方图、TopN、Count-Min Sketch 时，这些统计信息会被同步或异步加载到内存中。

`lite-init-stats` 默认值为 `true`，即开启轻量级的统计信息初始化。将 `lite-init-stats` 设置为 `true` 可以加速统计信息初始化，避免加载不必要的统计信息，从而降低 TiDB 的内存使用。

## 统计信息的导入导出

### 导出统计信息

统计信息的导出接口如下。

+ 通过以下接口可以获取数据库 `${db_name}` 中的表 `${table_name}` 的 JSON 格式的统计信息：

    {{< copyable "" >}}

    ```
    http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}
    ```

    示例如下：

    {{< copyable "" >}}

    ```
    curl -s http://127.0.0.1:10080/stats/dump/test/t1 -o /tmp/t1.json
    ```

+ 通过以下接口可以获取数据库 `${db_name}` 中的表 `${table_name}` 在指定时间上的 JSON 格式统计信息。指定的时间应在 GC SafePoint 之后。

    {{< copyable "" >}}

    ```
    http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyyMMddHHmmss}
    ```

### 导入统计信息

> **注意：**
>
> 启动 MySQL 客户端时，请使用 `--local-infile=1` 参数。

导入的统计信息一般是通过统计信息导出接口得到的 json 文件。

语法如下：

{{< copyable "sql" >}}

```sql
LOAD STATS 'file_name';
```

`file_name` 为要导入的统计信息的文件名。

## 锁定统计信息

从 v6.5.0 开始，TiDB 引入了锁定统计信息的特性。当一张表或一个分区的统计信息被锁定以后，该表或分区的统计信息将无法被修改，也无法对该表进行 `ANALYZE` 操作。用例如下：

创建表 `t`，插入一些数据，在未锁定表 `t` 的统计信息的情况下成功执行 `ANALYZE` 语句。

```sql
mysql> CREATE TABLE t(a INT, b INT);
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO t VALUES (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.02 sec)

mysql> SHOW WARNINGS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                                                                               |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "Row count in stats_meta is much smaller compared with the row count got by PD, use min(1, 15000/4) as the sample-rate=1" |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

锁定表 `t` 的统计信息，执行 `ANALYZE` 语句，warning 提示跳过对表 `t` 的 `ANALYZE`。

```sql
mysql> LOCK STATS t;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW STATS_LOCKED;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          |                | locked |
+---------+------------+----------------+--------+
1 row in set (0.01 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 2 warnings (0.00 sec)

mysql> SHOW WARNINGS;
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                 |
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "use min(1, 110000/8) as the sample-rate=1" |
| Warning | 1105 | skip analyze locked table: test.t                                                                                                       |
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

解锁表 `t` 的统计信息，成功执行 `ANALYZE` 语句。

```sql
mysql> UNLOCK STATS t;
Query OK, 0 rows affected (0.01 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.03 sec)

mysql> SHOW WARNINGS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                 |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "use min(1, 110000/8) as the sample-rate=1" |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

另外，你也可以通过 `LOCK STATS` 语句锁定分区的统计信息。用例如下：

创建分区表 `t`，插入一些数据，在未锁定分区 `p1` 的统计信息的情况下成功执行 `ANALYZE` 语句。

```sql
mysql> CREATE TABLE t(a INT, b INT) PARTITION BY RANGE (a) (PARTITION p0 VALUES LESS THAN (10), PARTITION p1 VALUES LESS THAN (20), PARTITION p2 VALUES LESS THAN (30));
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO t VALUES (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 6 warning (0.02 sec)

mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                                                                                              |
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p0, reason to use this rate is "Row count in stats_meta is much smaller compared with the row count got by PD, use min(1, 15000/4) as the sample-rate=1" |
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1"                                                                 |
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p2, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1"                                                                 |
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
6 rows in set (0.01 sec)
```

锁定分区 `p1` 的统计信息，执行 `ANALYZE` 语句，warning 提示跳过对分区 `p1` 的 `ANALYZE`。

```sql
mysql> LOCK STATS t PARTITION p1;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW STATS_LOCKED;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          | p1             | locked |
+---------+------------+----------------+--------+
1 row in set (0.00 sec)

mysql> ANALYZE TABLE t PARTITION p1;
Query OK, 0 rows affected, 2 warnings (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                              |
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1" |
| Warning | 1105 | skip analyze locked table: test.t partition (p1)                                                                                                                     |
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

解锁分区 `p1` 的统计信息，成功执行 `ANALYZE` 语句。

```sql
mysql> UNLOCK STATS t PARTITION p1;
Query OK, 0 rows affected (0.00 sec)

mysql> ANALYZE TABLE t PARTITION p1;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                              |
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1" |
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### 锁定统计信息的行为说明

* 如果统计信息在分区表上锁定，那么该分区表上所有分区的统计信息就都保持锁定。
* 如果表或者分区被 truncate，该表或分区上的统计信息锁定将会被解除。

具体行为参见下面表格：

|                            | 删除整张表 | Truncate 整张表                                                | Truncate 某个分区                                              | 创建一个新分区 | 删除某个分区                                 | Reorganize 某个分区                          | 交换某个分区             |
|----------------------------|------------|----------------------------------------------------------------|----------------------------------------------------------------|----------------|----------------------------------------------|----------------------------------------------|--------------------------|
| 非分区表被锁定             | 锁定失效   | 锁定失效，因为 TiDB 删除了旧表，所以锁定信息也一起被删除       | /                                                              | /              | /                                            | /                                            | /                        |
| 分区表并且整张表被锁定     | 锁定失效   | 锁定失效，因为 TiDB 删除了旧表，所以锁定信息也一起被删除       | 旧的分区锁定信息失效，自动锁定新的分区                         | 自动锁定新分区 | 被删除的分区锁定信息被清理，整张表锁继续生效 | 被删除的分区锁定信息被清理，新分区被自动锁定 | 锁定信息被转移到被交换表，新分区被自动锁定 |
| 分区表并且只锁定了某些分区 | 锁定失效   | 锁定失效，因为 TiDB 删除了旧的分区表，所以锁定信息也一起被删除 | 锁定失效，因为 TiDB 删除了旧的分区表，所以锁定信息也一起被删除 | /              | 被删除的分区锁定信息被清理                   | 被删除的分区锁定信息被清理                   | 锁定信息被转移到被交换表 |

## 另请参阅

* [LOAD STATS](/sql-statements/sql-statement-load-stats.md)
* [DROP STATS](/sql-statements/sql-statement-drop-stats.md)
* [LOCK STATS](/sql-statements/sql-statement-lock-stats.md)
* [UNLOCK STATS](/sql-statements/sql-statement-unlock-stats.md)
* [SHOW STATS_LOCKED](/sql-statements/sql-statement-show-stats-locked.md)
