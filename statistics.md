---
title: 统计信息简介
aliases: ['/docs-cn/dev/statistics/','/docs-cn/dev/reference/performance/statistics/']
---

# 统计信息简介

TiDB 使用统计信息来决定[索引的选择](/choose-index.md)。变量 `tidb_analyze_version` 用于控制所收集到的统计信息。目前 TiDB 中支持两种统计信息：`tidb_analyze_version = 1` 以及 `tidb_analyze_version = 2`。在 v5.3.0 及之后的版本中，该变量的默认值为 `2`，作为实验特性启用。如果从 v5.3.0 之前版本的集群升级至 v5.3.0 及之后的版本，`tidb_analyze_version` 的默认值不发生变化。

> **注意：**
>
> 当 `tidb_analyze_version = 2` 时，如果执行 ANALYZE 语句后发生 OOM，请设置全局变量 `tidb_analyze_version = 1`，然后进行以下操作之一：
>
> - 如果 ANALYZE 语句是手动执行的，请手动 analyze 每张需要的表：
>
>   {{< copyable "sql" >}}
>
>   ```sql
>   select distinct(concat('ANALYZE ',table_schema, '.', table_name,';')) from information_schema.tables, mysql.stats_histograms where stats_ver = 2 and table_id = tidb_table_id ;
>    ```
>
> - 如果 ANALYZE 语句是开启了自动 analyze 后 TiDB 自动执行的，请使用以下 SQL 语句生成 DROP STATS 的语句并执行：
>
>   {{< copyable "sql" >}}
>
>   ```sql
>   select distinct(concat('DROP STATS ',table_schema, '.', table_name,';')) from information_schema.tables, mysql.stats_histograms where stats_ver = 2 and table_id = tidb_table_id ;
>   ```

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

##### 收集部分列的统计信息

执行 SQL 语句时，优化器在大多数情况下只会用到部分列（例如， `WHERE`、`JOIN`、`ORDER BY`、`GROUP BY` 子句中出现的列）的统计信息，这些被用到的列称为 `PREDICATE COLUMNS`。

如果一个表有很多列，收集所有列的统计信息会有较大的开销。为了降低开销，你可以只收集指定列或者 `PREDICATE COLUMNS` 的统计信息供优化器使用。

> **注意：**
>
> 收集部分列的统计信息的功能仅适用于 `tidb_analyze_version = 2` 的情况。

- 如果要收集指定列的统计信息，请使用以下语法：

    {{< copyable "sql" >}}

    ```sql
    ANALYZE TABLE TableName COLUMNS ColumnNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    其中，`ColumnNameList` 表示指定列的名称列表。如果需要指定多列，请使用用逗号 `,` 分隔列名。例如, `ANALYZE table t columns a, b`。该语法除了收集指定表中指定列的统计信息，将同时收集该表中索引列的统计信息以及所有索引的统计信息。

    > **注意：**
    >
    > 该语法为全量收集。例如，在使用该语法收集了 a 列和 b 列的统计信息之后，如果还想要增加收集 c 列的统计信息，需要在语法中同时指定这三列 `ANALYZE table t columns a, b, c`，而不是只指定新增的那一列 `ANALYZE TABLE t COLUMNS c`。

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

##### 收集索引的统计信息

如果要收集 TableName 中 IndexNameList 里所有索引的统计信息，请使用以下语法：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

当 IndexNameList 为空时，该语法将收集 TableName 中所有索引的统计信息。

> **注意：**
>
> 为了保证前后统计信息的一致性，当设置 `tidb_analyze_version=2` 时，该语句也会收集整个表的统计信息（包括所有列和所有索引的统计信息）而不限于索引的统计信息。

##### 收集分区的统计信息

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
ANALYZE INCREMENTAL TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

增量收集 TableName 中所有的 PartitionNameList 中分区的索引列统计信息：

{{< copyable "sql" >}}

```sql
ANALYZE INCREMENTAL TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
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

在 TiDB v5.0 之前，执行查询语句时，TiDB 会以 [`feedback-probability`](/tidb-configuration-file.md#feedback-probability) 的概率收集反馈信息，并将其用于更新直方图和 Count-Min Sketch。**从 v5.0 起，该功能默认关闭，暂不建议开启此功能。**

从 TiDB v6.0 起，TiDB 支持通过 `KILL` 语句终止正在后台运行的 `ANALYZE` 任务。如果发现正在后台运行的 `ANALYZE` 任务消耗大量资源影响业务，你可以通过以下步骤终止该 `ANALYZE` 任务：

1. 执行以下 SQL 语句获得正在执行后台 `ANALYZE` 任务的 TiDB 实例地址和任务 `ID`：

    {{< copyable "sql" >}}

    ```sql
    SELECT ci.instance as instance, cp.id as id FROM information_schema.cluster_info ci, information_schema.cluster_processlist cp WHERE ci.status_address = cp.instance and ci.type = 'tidb' and cp.info like 'analyze table %' and cp.user = '' and cp.host = '';
    ```

    如果输出结果为空，说明后台没有正在执行的 `ANALYZE` 任务。

2. 使用客户端连接到执行后台 `ANALYZE` 任务的 TiDB 实例，然后执行以下 `KILL` 语句：

    {{< copyable "sql" >}}

    ```sql
    KILL TIDB ${id};
    ```

    `${id}` 为上一步中查询得到的后台 `ANALYZE` 任务的 `ID`。

    > **注意：**
    >
    > 只有当使用客户端连接到执行后台 `ANALYZE` 任务的 TiDB 实例时，执行 `KILL` 语句才能终止后台的 `ANALYZE` 任务。如果使用客户端连接到其他 TiDB 实例，或者客户端和 TiDB 中间有代理，`KILL` 语句不能终止后台的 `ANALYZE` 任务。更多信息，请参考 [`KILL [TIDB]`](/sql-statements/sql-statement-kill.md)。

### 控制 ANALYZE 并发度

执行 ANALYZE 语句的时候，你可以通过一些参数来调整并发度，以控制对系统的影响。

#### tidb_build_stats_concurrency

目前 ANALYZE 执行的时候会被切分成一个个小的任务，每个任务只负责某一个列或者索引。`tidb_build_stats_concurrency` 可以控制同时执行的任务的数量，其默认值是 4。

#### tidb_distsql_scan_concurrency

在执行分析普通列任务的时候，`tidb_distsql_scan_concurrency` 可以用于控制一次读取的 Region 数量，其默认值是 15。

#### tidb_index_serial_scan_concurrency

在执行分析索引列任务的时候，`tidb_index_serial_scan_concurrency` 可以用于控制一次读取的 Region 数量，其默认值是 1。

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

多次手动执行 `ANALYZE` 语句并指定持久化配置项时，TiDB 会使用最新一次 `ANALYZE` 指定的配置项覆盖上一次记录的持久化配置。

#### 关闭 ANALYZE 配置持久化功能

要关闭 `ANALYZE` 配置持久化功能，请设置系统变量 `tidb_persist_analyze_options` 为 `OFF`。由于 `ANALYZE` 配置持久化功能在 `tidb_analyze_version = 1` 的情况下不适用，因此设置 `tidb_analyze_version = 1` 同样会达到关闭配置持久化的效果。

关闭 `ANALYZE` 配置持久化功能后，已持久化的配置记录不会被清除。因此，当再次开启该功能时，TiDB 会继续使用之前记录的持久化配置收集统计信息。

> **注意：**
>
> 当再次开启 `ANALYZE` 配置持久化功能时，如果之前记录的持久化配置项已经不适用当前的数据，请手动执行 `ANALYZE` 语句并指定新的持久化配置项。

### 查看 ANALYZE 状态

在执行 `ANALYZE` 时，可以通过 SQL 语句来查看当前 `ANALYZE` 的状态。

语法如下：

{{< copyable "sql" >}}

```sql
SHOW ANALYZE STATUS [ShowLikeOrWhere];
```

该语句会输出 `ANALYZE` 的状态，可以通过使用 `ShowLikeOrWhere` 来筛选需要的信息。

目前 `SHOW ANALYZE STATUS` 会输出 7 列，具体如下：

| 列名 | 说明            |
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

`SHOW STATS_HEALTHY` 的语法图为：

![ShowStatsHealthy](/media/sqlgram/ShowStatsHealthy.png)

其中，`ShowLikeOrWhereOpt` 部分的语法图为：

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

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

语法如下：

{{< copyable "sql" >}}

```sql
DROP STATS TableName;
```

该语句会删除 TableName 中所有的统计信息。

## 统计信息的加载

默认情况下，列的统计信息占用空间大小不同，TiDB 对统计信息的加载方式也会不同。

- 对于 count、distinctCount、nullCount 等占用空间较小的统计信息，只要有数据更新，TiDB 就会自动将对应的统计信息加载进内存供 SQL 优化阶段使用。
- 对于直方图、TopN、CMSketch 等占用空间较大的统计信息，为了确保 SQL 执行的性能，TiDB 会按需进行异步加载。例如，对于直方图，只有当某条 SQL 语句的优化阶段使用到了某列的直方图统计信息时，TiDB 才会将该列的直方图信息加载到内存。按需异步加载的优势是统计信息加载不会影响到 SQL 执行的性能，但在 SQL 优化时有可能使用不完整的统计信息。

从 v5.4.0 开始，TiDB 引入了统计信息同步加载的特性，支持执行当前 SQL 语句时将直方图、TopN、CMSketch 等占用空间较大的统计信息同步加载到内存，提高该 SQL 语句优化时统计信息的完整性。

> **警告：**
>
> 统计信息同步加载目前为实验性特性，不建议在生产环境中使用。

统计信息同步加载特性默认关闭。要开启该特性，请将系统变量 `tidb_stats_load_sync_wait` 的值设置为 SQL 优化等待加载列的完整统计信息的超时时间（单位为毫秒）。该变量默认值为 0，代表未开启。

开启该特性后，你可以进一步配置该特性：

- 通过修改系统变量 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-从-v540-版本开始引入) 的值控制 SQL 优化等待超时后的行为。该变量默认值为 `OFF`，代表超时后 SQL 执行失败。当设置该变量为 `ON` 时，整个 SQL 优化过程不会使用任何列上的直方图、TopN 或 CMSketch，而是退回使用 pseudo 的统计信息。
- 通过修改 TiDB 配置项 [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-从-v540-版本开始引入) 的值控制统计信息同步加载可以并发处理的最大列数。该配置项的默认值为 `5`。
- 通过修改 TiDB 配置项 [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-从-v540-版本开始引入) 的值设置统计信息同步加载最多可以缓存多少列的请求。该配置项的默认值为 `1000`。

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
