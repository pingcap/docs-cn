---
title: Split Region
summary: TiDB 数据库中 Split Region 的使用概览。
---

# Split Region

在 TiDB 中创建的每个新表默认会分配一个 [Region](/tidb-storage.md#region) 来存储该表的数据。这个默认行为由 TiDB 配置文件中的 `split-table` 控制。当该 Region 中的数据超过默认的 Region 大小限制时，该 Region 会开始分裂成两个。

在上述情况下，由于开始时只有一个 Region，所有写请求都会发生在该 Region 所在的 TiKV 上。如果对新创建的表有大量写入，就会造成热点问题。

为了解决上述场景中的热点问题，TiDB 引入了预分裂功能，可以根据指定的参数为某个表预先分裂多个 Region，并将这些 Region 分散到各个 TiKV 节点上。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 语法图

```ebnf+diagram
SplitRegionStmt ::=
    "SPLIT" SplitSyntaxOption "TABLE" TableName PartitionNameList? ("INDEX" IndexName)? SplitOption

SplitSyntaxOption ::=
    ("REGION" "FOR")? "PARTITION"?

TableName ::=
    (SchemaName ".")? Identifier

PartitionNameList ::=
    "PARTITION" "(" PartitionName ("," PartitionName)* ")"

SplitOption ::=
    ("BETWEEN" RowValue "AND" RowValue "REGIONS" NUM
|   "BY" RowValue ("," RowValue)* )

RowValue ::=
    "(" ValuesOpt ")"
```

## Split Region 的使用

Split Region 语法有两种类型：

- 均匀切分的语法：

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

    `BETWEEN lower_value AND upper_value REGIONS region_num` 定义了上界、下界和 Region 数量。然后当前的 Region 会在上下界之间被均匀地分裂成指定数量（由 `region_num` 指定）的 Region。

- 不均匀切分的语法：

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

    `BY value_list…` 手动指定一系列点，基于这些点对当前 Region 进行分裂。这适用于数据分布不均匀的场景。

以下示例显示了 `SPLIT` 语句的结果：

```sql
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 4                  | 1.0                  |
+--------------------+----------------------+
```

* `TOTAL_SPLIT_REGION`：新分裂的 Region 数量。
* `SCATTER_FINISH_RATIO`：新分裂 Region 的分散完成率。`1.0` 表示所有 Region 都已分散。`0.5` 表示只有一半的 Region 已分散，其余正在分散中。

> **注意：**
>
> 以下两个会话变量可能会影响 `SPLIT` 语句的行为：
>
> - `tidb_wait_split_region_finish`：分散 Region 可能需要一段时间。这个时间取决于 PD 调度和 TiKV 负载。此变量用于控制执行 `SPLIT REGION` 语句时是否等待所有 Region 分散完成后才向客户端返回结果。如果其值设置为 `1`（默认值），TiDB 仅在分散完成后返回结果。如果其值设置为 `0`，TiDB 会不考虑分散状态直接返回结果。
> - `tidb_wait_split_region_timeout`：此变量用于设置 `SPLIT REGION` 语句的执行超时时间，单位为秒。默认值为 300s。如果 `split` 操作在此时间内未完成，TiDB 会返回超时错误。

### 切分表 Region

每个表中行数据的 key 由 `table_id` 和 `row_id` 编码而成。格式如下：

```go
t[table_id]_r[row_id]
```

例如，当 `table_id` 为 22，`row_id` 为 11 时：

```go
t22_r11
```

同一个表中的行数据具有相同的 `table_id`，但每一行都有其唯一的 `row_id`，可以用于 Region 切分。

#### 均匀切分

因为 `row_id` 是整数，可以根据指定的 `lower_value`、`upper_value` 和 `region_num` 计算出要切分的 key 的值。TiDB 首先计算步长值（`step = (upper_value - lower_value)/region_num`）。然后在 `lower_value` 和 `upper_value` 之间按每个"步长"均匀切分，生成 `region_num` 指定数量的 Region。

例如，如果你想为表 t 在 key 范围 `minInt64`~`maxInt64` 之间均匀切分出 16 个 Region，可以使用以下语句：

```sql
SPLIT TABLE t BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

此语句将表 t 在 minInt64 和 maxInt64 之间切分成 16 个 Region。如果给定的主键范围小于指定范围，例如 0~1000000000，你可以使用 0 和 1000000000 分别代替 minInt64 和 maxInt64 来切分 Region。

```sql
SPLIT TABLE t BETWEEN (0) AND (1000000000) REGIONS 16;
```

#### 不均匀切分

如果已知数据分布不均匀，想要在 key 范围 -inf ~ 10000、10000 ~ 90000 和 90000 ~ +inf 分别切分一个 Region，可以通过设置固定点来实现，如下所示：

```sql
SPLIT TABLE t BY (10000), (90000);
```

### 切分索引 Region

表中索引数据的 key 由 `table_id`、`index_id` 和索引列的值编码而成。格式如下：

```go
t[table_id]_i[index_id][index_value]
```

例如，当 `table_id` 为 22，`index_id` 为 5，`index_value` 为 abc 时：

```go
t22_i5abc
```

同一个表中同一个索引的数据具有相同的 `table_id` 和 `index_id`。要切分索引 Region，需要根据 `index_value` 进行切分。

#### 均匀切分

索引的均匀切分方式与数据的均匀切分方式相同。但是计算步长值更复杂，因为 `index_value` 可能不是整数。

首先将 `upper` 和 `lower` 的值编码成字节数组。在移除 `lower` 和 `upper` 字节数组的最长公共前缀后，将 `lower` 和 `upper` 的前 8 个字节转换为 uint64 格式。然后计算 `step = (upper - lower)/num`。之后，将计算出的步长编码成字节数组，并将其附加到 `lower` 和 `upper` 字节数组的最长公共前缀后面用于索引切分。以下是一个示例：

如果 `idx` 索引的列是整数类型，你可以使用以下 SQL 语句切分索引数据：

```sql
SPLIT TABLE t INDEX idx BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

此语句将表 t 中的索引 idx 从 `minInt64` 到 `maxInt64` 切分成 16 个 Region。

如果索引 idx1 的列是 varchar 类型，你想按前缀字母切分索引数据：

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("z") REGIONS 25;
```

此语句将索引 idx1 从 a~z 切分成 25 个 Region。Region 1 的范围是 `[minIndexValue, b)`；Region 2 的范围是 `[b, c)`；... Region 25 的范围是 `[y, minIndexValue]`。对于 `idx` 索引，前缀为 `a` 的数据写入 Region 1，前缀为 `b` 的数据写入 Region 2。

在上述切分方法中，前缀为 `y` 和 `z` 的数据都会写入 Region 25，因为上界不是 `z`，而是 `{`（ASCII 中 `z` 的下一个字符）。因此，更准确的切分方法如下：

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("{") REGIONS 26;
```

此语句将表 `t` 的索引 idx1 从 a~`{` 切分成 26 个 Region。Region 1 的范围是 `[minIndexValue, b)`；Region 2 的范围是 `[b, c)`；... Region 25 的范围是 `[y, z)`，Region 26 的范围是 `[z, maxIndexValue)`。

如果索引 `idx2` 的列是时间类型（如 timestamp/datetime），你想按年份切分索引 Region：

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

此语句将表 `t` 中的索引 `idx2` 从 `2010-01-01 00:00:00` 到 `2020-01-01 00:00:00` 切分成 10 个 Region。Region 1 的范围是 `[minIndexValue, 2011-01-01 00:00:00)`；Region 2 的范围是 `[2011-01-01 00:00:00, 2012-01-01 00:00:00)`。

如果你想按天切分索引 Region，参考以下示例：

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2020-06-01 00:00:00") AND ("2020-07-01 00:00:00") REGIONS 30;
```

此语句将表 `t` 中索引 `idx2` 的 2020 年 6 月的数据切分成 30 个 Region，每个 Region 代表 1 天。

其他类型索引列的 Region 切分方法类似。

对于联合索引的数据 Region 切分，唯一的区别是你可以指定多个列值。

例如，索引 `idx3 (a, b)` 包含 2 列，列 `a` 是 timestamp 类型，列 `b` 是 int 类型。如果你只想根据列 `a` 进行时间范围切分，可以使用单列时间索引的 SQL 语句。在这种情况下，不要在 `lower_value` 和 `upper_velue` 中指定列 `b` 的值。

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

在相同的时间范围内，如果你想根据列 b 再进行一次切分。只需在切分时指定列 b 的值即可。

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00", "a") AND ("2010-01-01 00:00:00", "z") REGIONS 10;
```

此语句根据列 b 的值在 a~z 范围内切分 10 个 Region，列 a 的时间前缀相同。如果为列 a 指定的值不同，则可能不会使用列 b 的值。

如果表的主键是[非聚簇索引](/clustered-indexes.md)，在切分 Region 时需要使用反引号 ``` ` ``` 来转义 `PRIMARY` 关键字。例如：

```sql
SPLIT TABLE t INDEX `PRIMARY` BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

#### 不均匀切分

索引数据也可以通过指定索引值来切分。

例如，有 `idx4 (a,b)`，列 `a` 是 varchar 类型，列 `b` 是 timestamp 类型。

```sql
SPLIT TABLE t1 INDEX idx4 BY ("a", "2000-01-01 00:00:01"), ("b", "2019-04-17 14:26:19"), ("c", "");
```

此语句指定 3 个值来切分 4 个 Region。每个 Region 的范围如下：

```
region1  [ minIndexValue               , ("a", "2000-01-01 00:00:01"))
region2  [("a", "2000-01-01 00:00:01") , ("b", "2019-04-17 14:26:19"))
region3  [("b", "2019-04-17 14:26:19") , ("c", "")                   )
region4  [("c", "")                    , maxIndexValue               )
```

### 切分分区表的 Region

切分分区表的 Region 与切分普通表的 Region 相同。唯一的区别是对每个分区执行相同的切分操作。

+ 均匀切分的语法：

    ```sql
    SPLIT [PARTITION] TABLE t [PARTITION] [(partition_name_list...)] [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

+ 不均匀切分的语法：

    ```sql
    SPLIT [PARTITION] TABLE table_name [PARTITION (partition_name_list...)] [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

#### 切分分区表 Region 的示例

1. 创建一个分区表 `t`。假设你想创建一个分成两个分区的 Hash 表。示例语句如下：

    ```sql
    CREATE TABLE t (a INT, b INT, INDEX idx(a)) PARTITION BY HASH(a) PARTITIONS 2;
    ```

    创建表 `t` 后，为每个分区切分一个 Region。使用 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) 语法查看此表的 Region：

    ```sql
    SHOW TABLE t REGIONS;
    ```

    ```sql
    +-----------+-----------+---------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS            | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
    +-----------+-----------+---------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | 1978      | t_1400_   | t_1401_ | 1979      | 4               | 1979, 1980, 1981 | 0          | 0             | 0          | 1                    | 0                |
    | 6         | t_1401_   |         | 17        | 4               | 17, 18, 21       | 0          | 223           | 0          | 1                    | 0                |
    +-----------+-----------+---------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    ```

2. 使用 `SPLIT` 语法为每个分区切分一个 Region。假设你想将每个分区中 `[0,10000]` 范围内的数据切分成四个 Region。示例语句如下：

    ```sql
    split partition table t between (0) and (10000) regions 4;
    ```

    在上述语句中，`0` 和 `10000` 分别表示你想要分散的热点数据对应的上下界 `row_id`。

    > **注意：**
    >
    > 此示例仅适用于热点数据均匀分布的场景。如果热点数据在指定数据范围内分布不均匀，请参考[切分分区表的 Region](#切分分区表的-region) 中的不均匀切分语法。

3. 再次使用 `SHOW TABLE REGIONS` 语法查看此表的 Region。你可以看到此表现在有十个 Region，每个分区有五个 Region，其中四个是行数据，一个是索引数据。

    ```sql
    SHOW TABLE t REGIONS;
    ```

    ```sql
    +-----------+---------------+---------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | REGION_ID | START_KEY     | END_KEY       | LEADER_ID | LEADER_STORE_ID | PEERS            | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
    +-----------+---------------+---------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | 1998      | t_1400_r      | t_1400_r_2500 | 2001      | 5               | 2000, 2001, 2015 | 0          | 132           | 0          | 1                    | 0                |
    | 2006      | t_1400_r_2500 | t_1400_r_5000 | 2016      | 1               | 2007, 2016, 2017 | 0          | 35            | 0          | 1                    | 0                |
    | 2010      | t_1400_r_5000 | t_1400_r_7500 | 2012      | 2               | 2011, 2012, 2013 | 0          | 35            | 0          | 1                    | 0                |
    | 1978      | t_1400_r_7500 | t_1401_       | 1979      | 4               | 1979, 1980, 1981 | 0          | 621           | 0          | 1                    | 0                |
    | 1982      | t_1400_       | t_1400_r      | 2014      | 3               | 1983, 1984, 2014 | 0          | 35            | 0          | 1                    | 0                |
    | 1990      | t_1401_r      | t_1401_r_2500 | 1992      | 2               | 1991, 1992, 2020 | 0          | 120           | 0          | 1                    | 0                |
    | 1994      | t_1401_r_2500 | t_1401_r_5000 | 1997      | 5               | 1996, 1997, 2021 | 0          | 129           | 0          | 1                    | 0                |
    | 2002      | t_1401_r_5000 | t_1401_r_7500 | 2003      | 4               | 2003, 2023, 2022 | 0          | 141           | 0          | 1                    | 0                |
    | 6         | t_1401_r_7500 |               | 17        | 4               | 17, 18, 21       | 0          | 601           | 0          | 1                    | 0                |
    | 1986      | t_1401_       | t_1401_r      | 1989      | 5               | 1989, 2018, 2019 | 0          | 123           | 0          | 1                    | 0                |
    +-----------+---------------+---------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    ```

4. 你也可以为每个分区的索引切分 Region。例如，你可以将 `idx` 索引的 `[1000,10000]` 范围切分成两个 Region。示例语句如下：

    ```sql
    SPLIT PARTITION TABLE t INDEX idx BETWEEN (1000) AND (10000) REGIONS 2;
    ```

#### 切分单个分区的示例

你可以指定要切分的分区。

1. 创建一个分区表。假设你想创建一个分成三个分区的 Range 分区表。示例语句如下：

    ```sql
    CREATE TABLE t ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
        PARTITION p1 VALUES LESS THAN (10000),
        PARTITION p2 VALUES LESS THAN (20000),
        PARTITION p3 VALUES LESS THAN (MAXVALUE) );
    ```

2. 假设你想将 `p1` 分区中 `[0,10000]` 范围的数据切分成两个 Region。示例语句如下：

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p1) BETWEEN (0) AND (10000) REGIONS 2;
    ```

3. 假设你想将 `p2` 分区中 `[10000,20000]` 范围的数据切分成两个 Region。示例语句如下：

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p2) BETWEEN (10000) AND (20000) REGIONS 2;
    ```

4. 你可以使用 `SHOW TABLE REGIONS` 语法查看此表的 Region：

    ```sql
    SHOW TABLE t REGIONS;
    ```

    ```sql
    +-----------+----------------+----------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | REGION_ID | START_KEY      | END_KEY        | LEADER_ID | LEADER_STORE_ID | PEERS            | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
    +-----------+----------------+----------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | 2040      | t_1406_        | t_1406_r_5000  | 2045      | 3               | 2043, 2045, 2044 | 0          | 0             | 0          | 1                    | 0                |
    | 2032      | t_1406_r_5000  | t_1407_        | 2033      | 4               | 2033, 2034, 2035 | 0          | 0             | 0          | 1                    | 0                |
    | 2046      | t_1407_        | t_1407_r_15000 | 2048      | 2               | 2047, 2048, 2050 | 0          | 35            | 0          | 1                    | 0                |
    | 2036      | t_1407_r_15000 | t_1408_        | 2037      | 4               | 2037, 2038, 2039 | 0          | 0             | 0          | 1                    | 0                |
    | 6         | t_1408_        |                | 17        | 4               | 17, 18, 21       | 0          | 214           | 0          | 1                    | 0                |
    +-----------+----------------+----------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    ```

5. 假设你想将 `p1` 和 `p2` 分区的 `idx` 索引的 `[0,20000]` 范围切分成两个 Region。示例语句如下：

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p1,p2) INDEX idx BETWEEN (0) AND (20000) REGIONS 2;
    ```

## pre_split_regions

在创建具有 `AUTO_RANDOM` 或 `SHARD_ROW_ID_BITS` 属性的表时，如果你希望在表创建后立即将表均匀预分裂成多个 Region，也可以指定 `PRE_SPLIT_REGIONS` 选项。表的预分裂 Region 数量为 `2^(PRE_SPLIT_REGIONS)`。

> **注意：**
>
> `PRE_SPLIT_REGIONS` 的值必须小于或等于 `SHARD_ROW_ID_BITS` 或 `AUTO_RANDOM` 的值。

`tidb_scatter_region` 全局变量会影响 `PRE_SPLIT_REGIONS` 的行为。此变量控制在表创建后是否等待 Region 预分裂和分散完成后再返回结果。如果在创建表后有密集写入，你需要将此变量的值设置为 `1`，这样 TiDB 会等到所有 Region 分裂和分散完成后才向客户端返回结果。否则，TiDB 会在分散完成之前写入数据，这会对写入性能产生显著影响。

### pre_split_regions 示例

```sql
CREATE TABLE t (a INT, b INT, INDEX idx1(a)) SHARD_ROW_ID_BITS = 4 PRE_SPLIT_REGIONS=2;
```

创建表后，此语句为表 t 分裂 `4 + 1` 个 Region。`4 (2^2)` 个 Region 用于保存表行数据，1 个 Region 用于保存 `idx1` 的索引数据。

这 4 个表 Region 的范围如下：

```
region1:   [ -inf      ,  1<<61 )
region2:   [ 1<<61     ,  2<<61 )
region3:   [ 2<<61     ,  3<<61 )
region4:   [ 3<<61     ,  +inf  )
```

<CustomContent platform="tidb">

> **注意：**
>
> Split Region 语句分裂的 Region 受 PD 中的 [Region 合并](/best-practices/pd-scheduling-best-practices.md#region-merge)调度器控制。为了避免 PD 在新分裂的 Region 后很快就重新合并，你需要使用[表属性](/table-attributes.md)或[动态修改](/pd-control.md)与 Region 合并功能相关的配置项。

</CustomContent>

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [SHOW TABLE REGIONS](/sql-statements/sql-statement-show-table-regions.md)
* 会话变量：[`tidb_scatter_region`](/system-variables.md#tidb_scatter_region)、[`tidb_wait_split_region_finish`](/system-variables.md#tidb_wait_split_region_finish) 和 [`tidb_wait_split_region_timeout`](/system-variables.md#tidb_wait_split_region_timeout)。
