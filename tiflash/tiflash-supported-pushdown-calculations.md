---
title: TiFlash 支持的计算下推
summary: 了解 TiFlash 支持的计算下推。
---

# TiFlash 支持的计算下推

本文档介绍 TiFlash 支持的计算下推。

## 支持下推的算子

TiFlash 支持部分算子的下推，支持的算子如下：

* TableScan：该算子从表中读取数据
* Selection：该算子对数据进行过滤
* HashAgg：该算子基于 [Hash Aggregation](/explain-aggregation.md#hash-aggregation) 算法对数据进行聚合运算
* StreamAgg：该算子基于 [Stream Aggregation](/explain-aggregation.md#stream-aggregation) 算法对数据进行聚合运算。StreamAgg 仅支持不带 `GROUP BY` 条件的列。
* TopN：该算子对数据求 TopN 运算
* Limit：该算子对数据进行 limit 运算
* Project：该算子对数据进行投影运算
* HashJoin：该算子基于 [Hash Join](/explain-joins.md#hash-join) 算法对数据进行连接运算：
    * 只有在 [MPP 模式](/tiflash/use-tiflash-mpp-mode.md)下才能被下推
    * 支持的 Join 类型包括 Inner Join、Left Join、Semi Join、Anti Semi Join、Left Semi Join、Anti Left Semi Join
    * 对于上述类型，既支持带等值条件的连接，也支持不带等值条件的连接（即 Cartesian Join 或者 Null-aware Semi Join）；在计算 Cartesian Join 或者 Null-aware Semi Join 时，只会使用 Broadcast 算法，而不会使用 Shuffle Hash Join 算法
* Window：当前支持下推的函数包括[窗口函数](/functions-and-operators/window-functions.md) `ROW_NUMBER()`、`RANK()`、`DENSE_RANK()`、`LEAD()`、`LAG()`、`FIRST_VALUE()`、`LAST_VALUE()` 和[聚合函数](https://docs.pingcap.com/zh/tidb/dev/aggregate-group-by-functions/) `MIN()`、`MAX()`、`AVG()`、`COUNT()`、`SUM()`。

在 TiDB 中，算子之间会呈现树型组织结构。一个算子能下推到 TiFlash 的前提条件，是该算子的所有子算子都能下推到 TiFlash。因为大部分算子都包含有表达式计算，当且仅当一个算子所包含的所有表达式均支持下推到 TiFlash 时，该算子才有可能下推给 TiFlash。

## 支持下推的表达式

| 表达式类型 | 运算 |
| :-------------- | :------------------------------------- |
| [数学函数](/functions-and-operators/numeric-functions-and-operators.md) | `+`, `-`, `/`, `*`, `%`, `>=`, `<=`, `=`, `!=`, `<`, `>`, `ROUND()`, `ABS()`, `FLOOR(int)`, `CEIL(int)`, `CEILING(int)`, `SQRT()`, `LOG()`, `LOG2()`, `LOG10()`, `LN()`, `EXP()`, `POW()`, `POWER()`, `SIGN()`, `RADIANS()`, `DEGREES()`, `CONV()`, `CRC32()`, `GREATEST(int/real)`, `LEAST(int/real)` |
| [逻辑函数](/functions-and-operators/control-flow-functions.md)和[算子](/functions-and-operators/operators.md) | `AND`, `OR`, `NOT`, `CASE WHEN`, `IF()`, `IFNULL()`, `ISNULL()`, `IN`, `LIKE`, `ILIKE`, `COALESCE`, `IS` |
| [位运算](/functions-and-operators/bit-functions-and-operators.md) | `&` (bitand), <code>\|</code> (bitor), `~` (bitneg), `^` (bitxor) |
| [字符串函数](/functions-and-operators/string-functions.md) | `SUBSTR()`, `CHAR_LENGTH()`, `REPLACE()`, `CONCAT()`, `CONCAT_WS()`, `LEFT()`, `RIGHT()`, `ASCII()`, `LENGTH()`, `TRIM()`, `LTRIM()`, `RTRIM()`, `POSITION()`, `FORMAT()`, `LOWER()`, `UCASE()`, `UPPER()`, `SUBSTRING_INDEX()`, `LPAD()`, `RPAD()`, `STRCMP()` |
| [正则函数和算子](/functions-and-operators/string-functions.md) | `REGEXP`, `REGEXP_LIKE()`, `REGEXP_INSTR()`, `REGEXP_SUBSTR()`, `REGEXP_REPLACE()`, `RLIKE` |
| [日期函数](/functions-and-operators/date-and-time-functions.md) | `DATE_FORMAT()`, `TIMESTAMPDIFF()`, `FROM_UNIXTIME()`, `UNIX_TIMESTAMP(int)`, `UNIX_TIMESTAMP(decimal)`, `STR_TO_DATE(date)`, `STR_TO_DATE(datetime)`, `DATEDIFF()`, `YEAR()`, `MONTH()`, `DAY()`, `EXTRACT(datetime)`, `DATE()`, `HOUR()`, `MICROSECOND()`, `MINUTE()`, `SECOND()`, `SYSDATE()`, `DATE_ADD/ADDDATE(datetime, int)`, `DATE_ADD/ADDDATE(string, int/real)`, `DATE_SUB/SUBDATE(datetime, int)`, `DATE_SUB/SUBDATE(string, int/real)`, `QUARTER()`, `DAYNAME()`, `DAYOFMONTH()`, `DAYOFWEEK()`, `DAYOFYEAR()`, `LAST_DAY()`, `MONTHNAME()`, `TO_SECONDS()`, `TO_DAYS()`, `FROM_DAYS()`, `WEEKOFYEAR()` |
| [JSON 函数](/functions-and-operators/json-functions.md) | `JSON_LENGTH()`, `->`, `->>`, `JSON_EXTRACT()`, `JSON_ARRAY()`, `JSON_DEPTH()`, `JSON_VALID()`, `JSON_KEYS()`, `JSON_CONTAINS_PATH()`, `JSON_UNQUOTE()` |
| [向量函数](/vector-search/vector-search-functions-and-operators.md) | `VEC_L2_DISTANCE`, `VEC_COSINE_DISTANCE`, `VEC_NEGATIVE_INNER_PRODUCT`, `VEC_L1_DISTANCE`, `VEC_DIMS`, `VEC_L2_NORM`, `VEC_AS_TEXT` |
| [转换函数](/functions-and-operators/cast-functions-and-operators.md) | `CAST(int AS DOUBLE), CAST(int AS DECIMAL)`, `CAST(int AS STRING)`, `CAST(int AS TIME)`, `CAST(double AS INT)`, `CAST(double AS DECIMAL)`, `CAST(double AS STRING)`, `CAST(double AS TIME)`, `CAST(string AS INT)`, `CAST(string AS DOUBLE), CAST(string AS DECIMAL)`, `CAST(string AS TIME)`, `CAST(decimal AS INT)`, `CAST(decimal AS STRING)`, `CAST(decimal AS TIME)`, `CAST(decimal AS DOUBLE)`, `CAST(time AS INT)`, `CAST(time AS DECIMAL)`, `CAST(time AS STRING)`, `CAST(time AS REAL)`, `CAST(json AS JSON)`, `CAST(json AS STRING)`, `CAST(int AS JSON)`, `CAST(real AS JSON)`, `CAST(decimal AS JSON)`, `CAST(string AS JSON)`, `CAST(time AS JSON)`, `CAST(duration AS JSON)` |
| [聚合函数](/functions-and-operators/aggregate-group-by-functions.md) | `MIN()`, `MAX()`, `SUM()`, `COUNT()`, `AVG()`, `APPROX_COUNT_DISTINCT()`, `GROUP_CONCAT()` |
| [其他函数](/functions-and-operators/miscellaneous-functions.md) | `INET_NTOA()`, `INET_ATON()`, `INET6_NTOA()`, `INET6_ATON()` |

## 下推限制

* 所有包含 Bit、Set 和 Geometry 类型的表达式均不能下推到 TiFlash
* `DATE_ADD()`、`DATE_SUB()`、`ADDDATE()` 以及 `SUBDATE()` 中的 interval 类型只支持如下几种，如使用了其他类型的 interval，TiFlash 会在运行时报错。
    * DAY
    * WEEK
    * MONTH
    * YEAR
    * HOUR
    * MINUTE
    * SECOND

如查询遇到不支持的下推计算，则需要依赖 TiDB 完成剩余计算，可能会很大程度影响 TiFlash 加速效果。对于暂不支持的算子/表达式，将会在后续版本中陆续支持。

类似 `MAX()` 这样的函数在聚合算子中支持下推，但是在窗口函数算子中还不支持下推。

## 示例

以下通过一些例子对下推算子和表达式到 TiFlash 进行说明。

### 示例 1：下推算子到 TiFlash 存储

```sql
CREATE TABLE t(id INT PRIMARY KEY, a INT);
ALTER TABLE t SET TIFLASH REPLICA 1;

EXPLAIN SELECT * FROM t LIMIT 3;

+------------------------------+---------+--------------+---------------+--------------------------------+
| id                           | estRows | task         | access object | operator info                  |
+------------------------------+---------+--------------+---------------+--------------------------------+
| Limit_9                      | 3.00    | root         |               | offset:0, count:3              |
| └─TableReader_17             | 3.00    | root         |               | data:ExchangeSender_16         |
|   └─ExchangeSender_16        | 3.00    | mpp[tiflash] |               | ExchangeType: PassThrough      |
|     └─Limit_15               | 3.00    | mpp[tiflash] |               | offset:0, count:3              |
|       └─TableFullScan_14     | 3.00    | mpp[tiflash] | table:t       | keep order:false, stats:pseudo |
+------------------------------+---------+--------------+---------------+--------------------------------+
5 rows in set (0.18 sec)
```

在该查询中，算子 Limit 被下推到 TiFlash 对数据进行过滤，减少了网络传输数据量，进而减少网络传输开销。具体可查看以上示例中 `Limit_15` 算子的 `task` 列，其值为 `mpp[tiflash]`，表示该算子被下推到 TiFlash。

### 示例 2：下推表达式到 TiFlash 存储

```sql
CREATE TABLE t(id INT PRIMARY KEY, a INT);
ALTER TABLE t SET TIFLASH REPLICA 1;
INSERT INTO t(id,a) VALUES (1,2),(2,4),(11,2),(12,4),(13,4),(14,7);

EXPLAIN SELECT MAX(id + a) FROM t GROUP BY a;

+------------------------------------+---------+--------------+---------------+---------------------------------------------------------------------------+
| id                                 | estRows | task         | access object | operator info                                                             |
+------------------------------------+---------+--------------+---------------+---------------------------------------------------------------------------+
| TableReader_45                     | 4.80    | root         |               | data:ExchangeSender_44                                                    |
| └─ExchangeSender_44                | 4.80    | mpp[tiflash] |               | ExchangeType: PassThrough                                                 |
|   └─Projection_39                  | 4.80    | mpp[tiflash] |               | Column#3                                                                  |
|     └─HashAgg_37                   | 4.80    | mpp[tiflash] |               | group by:Column#9, funcs:max(Column#8)->Column#3                          |
|       └─Projection_46              | 6.00    | mpp[tiflash] |               | plus(test.t.id, test.t.a)->Column#8, test.t.a                             |
|         └─ExchangeReceiver_23      | 6.00    | mpp[tiflash] |               |                                                                           |
|           └─ExchangeSender_22      | 6.00    | mpp[tiflash] |               | ExchangeType: HashPartition, Hash Cols: [name: test.t.a, collate: binary] |
|             └─TableFullScan_21     | 6.00    | mpp[tiflash] | table:t       | keep order:false, stats:pseudo                                            |
+------------------------------------+---------+--------------+---------------+---------------------------------------------------------------------------+
8 rows in set (0.18 sec)

```

在该查询中，表达式 `id + a` 被下推到 TiFlash，从而能提前进行计算，减少网络传输数据量，进而减少网络传输开销，提升整体计算性能。具体可查看以上示例中 `operator` 列为 `plus(test.t.id, test.t.a)` 的行的 `task` 列，其值为 `mpp[tiflash]`，表示该表达式被下推到 TiFlash。

### 示例 3：下推限制

```sql
CREATE TABLE t(id INT PRIMARY KEY, a INT);
ALTER TABLE t SET TIFLASH REPLICA 1;
INSERT INTO t(id,a) VALUES (1,2),(2,4),(11,2),(12,4),(13,4),(14,7);

EXPLAIN SELECT id FROM t WHERE TIME(now()+ a) < '12:00:00';

+-----------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------+
| id                          | estRows | task         | access object | operator info                                                                                    |
+-----------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------+
| Projection_4                | 4.80    | root         |               | test.t.id                                                                                        |
| └─Selection_6               | 4.80    | root         |               | lt(cast(time(cast(plus(20230110083056, test.t.a), var_string(20))), var_string(10)), "12:00:00") |
|   └─TableReader_11          | 6.00    | root         |               | data:ExchangeSender_10                                                                           |
|     └─ExchangeSender_10     | 6.00    | mpp[tiflash] |               | ExchangeType: PassThrough                                                                        |
|       └─TableFullScan_9     | 6.00    | mpp[tiflash] | table:t       | keep order:false, stats:pseudo                                                                   |
+-----------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------+
5 rows in set, 3 warnings (0.20 sec)
```

分析执行计划可以发现，该查询在执行时只在 TiFlash 中进行了 TableFullScan，其他的函数计算和过滤均在 `root` 进行，并未下推至 TiFlash。

执行以下命令，可以查找不能下推的算子和表达式。

```sql
SHOW WARNINGS;

+---------+------+------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                            |
+---------+------+------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | Scalar function 'time'(signature: Time, return type: time) is not supported to push down to storage layer now.                     |
| Warning | 1105 | Scalar function 'cast'(signature: CastDurationAsString, return type: var_string(10)) is not supported to push down to tiflash now. |
| Warning | 1105 | Scalar function 'cast'(signature: CastDurationAsString, return type: var_string(10)) is not supported to push down to tiflash now. |
+---------+------+------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.18 sec)
```

可以看出，该查询的表达式无法完全下推至 TiFlash，因为 `Time` 函数和 `Cast` 函数无法下推至 TiFlash。

### 示例 4：窗口函数

```sql
CREATE TABLE t(id INT PRIMARY KEY, c1 VARCHAR(100));
ALTER TABLE t SET TIFLASH REPLICA 1;
INSERT INTO t VALUES(1,"foo"),(2,"bar"),(3,"bar foo"),(10,"foo"),(20,"bar"),(30,"bar foo");

EXPLAIN SELECT id, ROW_NUMBER() OVER (PARTITION BY id > 10) FROM t;
+----------------------------------+----------+--------------+---------------+---------------------------------------------------------------------------------------------------------------+
| id                               | estRows  | task         | access object | operator info                                                                                                 |
+----------------------------------+----------+--------------+---------------+---------------------------------------------------------------------------------------------------------------+
| TableReader_30                   | 10000.00 | root         |               | MppVersion: 1, data:ExchangeSender_29                                                                         |
| └─ExchangeSender_29              | 10000.00 | mpp[tiflash] |               | ExchangeType: PassThrough                                                                                     |
|   └─Projection_7                 | 10000.00 | mpp[tiflash] |               | test.t.id, Column#5, stream_count: 4                                                                          |
|     └─Window_28                  | 10000.00 | mpp[tiflash] |               | row_number()->Column#5 over(partition by Column#4 rows between current row and current row), stream_count: 4  |
|       └─Sort_14                  | 10000.00 | mpp[tiflash] |               | Column#4, stream_count: 4                                                                                     |
|         └─ExchangeReceiver_13    | 10000.00 | mpp[tiflash] |               | stream_count: 4                                                                                               |
|           └─ExchangeSender_12    | 10000.00 | mpp[tiflash] |               | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: Column#4, collate: binary], stream_count: 4 |
|             └─Projection_10      | 10000.00 | mpp[tiflash] |               | test.t.id, gt(test.t.id, 10)->Column#4                                                                        |
|               └─TableFullScan_11 | 10000.00 | mpp[tiflash] | table:t       | keep order:false, stats:pseudo                                                                                |
+----------------------------------+----------+--------------+---------------+---------------------------------------------------------------------------------------------------------------+
9 rows in set (0.0073 sec)
```

可以看到，`Window` 操作在 `task` 列中有一个 `mpp[tiflash]` 的值，表示 `ROW_NUMBER() OVER (PARTITION BY id > 10)` 操作能够被下推至 TiFlash。

```sql
CREATE TABLE t(id INT PRIMARY KEY, c1 VARCHAR(100));
ALTER TABLE t SET TIFLASH REPLICA 1;
INSERT INTO t VALUES(1,"foo"),(2,"bar"),(3,"bar foo"),(10,"foo"),(20,"bar"),(30,"bar foo");

EXPLAIN SELECT id, MAX(id) OVER (PARTITION BY id > 10) FROM t;
+-----------------------------+----------+-----------+---------------+------------------------------------------------------------+
| id                          | estRows  | task      | access object | operator info                                              |
+-----------------------------+----------+-----------+---------------+------------------------------------------------------------+
| Projection_6                | 10000.00 | root      |               | test.t1.id, Column#5                                       |
| └─Shuffle_14                | 10000.00 | root      |               | execution info: concurrency:5, data sources:[Projection_8] |
|   └─Window_7                | 10000.00 | root      |               | max(test.t1.id)->Column#5 over(partition by Column#4)      |
|     └─Sort_13               | 10000.00 | root      |               | Column#4                                                   |
|       └─Projection_8        | 10000.00 | root      |               | test.t1.id, gt(test.t1.id, 10)->Column#4                   |
|         └─TableReader_10    | 10000.00 | root      |               | data:TableFullScan_9                                       |
|           └─TableFullScan_9 | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                             |
+-----------------------------+----------+-----------+---------------+------------------------------------------------------------+
7 rows in set (0.0010 sec)
```

可以看到，`Window` 操作在 `task` 列中有一个 `root` 的值，表示 `MAX(id) OVER (PARTITION BY id > 10)` 操作不能被下推至 TiFlash。这是因为，`MAX()` 只支持作为聚合函数下推，而不支持作为窗口函数下推。
