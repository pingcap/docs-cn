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
    * 对于上述类型，既支持带等值条件的连接，也支持不带等值条件的连接（即 Cartesian Join）；在计算 Cartesian Join 时，只会使用 Broadcast 算法，而不会使用 Shuffle Hash Join 算法
* Window：当前支持下推的窗口函数包括：row_number()、rank()、dense_rank()、lead() 和 lag()

在 TiDB 中，算子之间会呈现树型组织结构。一个算子能下推到 TiFlash 的前提条件，是该算子的所有子算子都能下推到 TiFlash。因为大部分算子都包含有表达式计算，当且仅当一个算子所包含的所有表达式均支持下推到 TiFlash 时，该算子才有可能下推给 TiFlash。

## 支持下推的表达式

* 数学函数：`+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32, greatest(int/real), least(int/real)`
* 逻辑函数：`and, or, not, case when, if, ifnull, isnull, in, like, coalesce, is`
* 位运算：`bitand, bitor, bigneg, bitxor`
* 字符串函数：`substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp, regexp, regexp_like, regexp_instr, regexp_substr, regexp_replace`
* 日期函数：`date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add/adddate(datetime, int), date_add/adddate(string, int), date_add/adddate(string, real), date_sub/subdate(datetime, int), date_sub/subdate(string, int), date_sub/subdate(string, real), quarter, dayname, dayofmonth, dayofweek, dayofyear, last_day, monthname, to_seconds, to_days, from_days, weekofyear`
* JSON 函数：`json_length, ->, ->>, json_extract`
* 转换函数：`cast(int as double), cast(int as decimal), cast(int as string), cast(int as time), cast(double as int), cast(double as decimal), cast(double as string), cast(double as time), cast(string as int), cast(string as double), cast(string as decimal), cast(string as time), cast(decimal as int), cast(decimal as string), cast(decimal as time), cast(time as int), cast(time as decimal), cast(time as string), cast(time as real)`
* 聚合函数：`min, max, sum, count, avg, approx_count_distinct, group_concat`
* 其他函数：`inetntoa, inetaton, inet6ntoa, inet6aton`

## 下推限制

* 所有包含 Bit、Set 和 Geometry 类型的表达式均不能下推到 TiFlash
* date_add、date_sub、adddate 和 subdate 中的 interval 类型只支持如下几种，如使用了其他类型的 interval，TiFlash 会在运行时报错。
    * DAY
    * WEEK
    * MONTH
    * YEAR
    * HOUR
    * MINUTE
    * SECOND

如查询遇到不支持的下推计算，则需要依赖 TiDB 完成剩余计算，可能会很大程度影响 TiFlash 加速效果。对于暂不支持的算子/表达式，将会在后续版本中陆续支持。

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

在该查询中，算子 Limit 被下推到 TiFlash 对数据进行过滤，减少了网络传输数据量，进而减少网络传输开销。

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

在该查询中，表达式 `id + a` 被下推到 TiFlash，从而能提前进行计算，减少网络传输数据量，进而减少网络传输开销，提升整体计算性能。

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
