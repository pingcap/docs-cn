---
title: Push-down calculations Supported by TiFlash
summary: Learn the push-down calculations supported by TiFlash.
---

# Push-down Calculations Supported by TiFlash

This document introduces the push-down calculations supported by TiFlash.

## Push-down operators

TiFlash supports the push-down of the following operators:

* TableScan: Reads data from tables.
* Selection: Filters data.
* HashAgg: Performs data aggregation based on the [Hash Aggregation](/explain-aggregation.md#hash-aggregation) algorithm.
* StreamAgg: Performs data aggregation based on the [Stream Aggregation](/explain-aggregation.md#stream-aggregation) algorithm. SteamAgg only supports the aggregation without the `GROUP BY` condition.
* TopN: Performs the TopN calculation.
* Limit: Performs the limit calculation.
* Project: Performs the projection calculation.
* HashJoin: Performs the join calculation using the [Hash Join](/explain-joins.md#hash-join) algorithm, but with the following conditions:
    * The operator can be pushed down only in the [MPP mode](/tiflash/use-tiflash-mpp-mode.md).
    * Supported joins are Inner Join, Left Join, Semi Join, Anti Semi Join, Left Semi Join, and Anti Left Semi Join.
    * The preceding joins support both Equi Join and Non-Equi Join (Cartesian Join). When calculating Cartesian Join, the Broadcast algorithm, instead of the Shuffle Hash Join algorithm, is used.
* Window functions: Currently, TiFlash supports row_number(), rank(), dense_rank(), lead(), and lag()

In TiDB, operators are organized in a tree structure. For an operator to be pushed down to TiFlash, all of the following prerequisites must be met:

+ All of its child operators can be pushed down to TiFlash.
+ If an operator contains expressions (most of the operators contain expressions), all expressions of the operator can be pushed down to TiFlash.

## Push-down expressions

TiFlash supports the following push-down expressions:

* Mathematical functions: `+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32, greatest(int/real), least(int/real)`
* Logical functions: `and, or, not, case when, if, ifnull, isnull, in, like, coalesce, is`
* Bitwise operations: `bitand, bitor, bigneg, bitxor`
* String functions: `substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp, regexp, regexp_like, regexp_instr, regexp_substr, regexp_replace`
* Date functions: `date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add/adddate(datetime, int), date_add/adddate(string, int), date_add/adddate(string, real), date_sub/subdate(datetime, int), date_sub/subdate(string, int), date_sub/subdate(string, real), quarter, dayname, dayofmonth, dayofweek, dayofyear, last_day, monthname, to_seconds, to_days, from_days, weekofyear`
* JSON function: `json_length, ->, ->>, json_extract`
* Conversion functions: `cast(int as double), cast(int as decimal), cast(int as string), cast(int as time), cast(double as int), cast(double as decimal), cast(double as string), cast(double as time), cast(string as int), cast(string as double), cast(string as decimal), cast(string as time), cast(decimal as int), cast(decimal as string), cast(decimal as time), cast(time as int), cast(time as decimal), cast(time as string), cast(time as real)`
* Aggregate functions: `min, max, sum, count, avg, approx_count_distinct, group_concat`
* Miscellaneous functions: `inetntoa, inetaton, inet6ntoa, inet6aton`

## Restrictions

* Expressions that contain the Bit, Set, and Geometry types cannot be pushed down to TiFlash.

* The `date_add`, `date_sub`, `adddate`, and `subdate` functions support the following interval types only. If other interval types are used, TiFlash reports errors.

    * DAY
    * WEEK
    * MONTH
    * YEAR
    * HOUR
    * MINUTE
    * SECOND

If a query encounters unsupported push-down calculations, TiDB needs to complete the remaining calculations, which might greatly affect the TiFlash acceleration effect. The currently unsupported operators and expressions might be supported in future versions.

## Examples

This section provides some examples of pushing down operators and expressions to TiFlash.

### Example 1: Push operators down to TiFlash

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

In the preceding example, the operator `Limit` is pushed down to TiFlash for filtering data, which helps reduce the amount of data to be transferred over the network and reduce the network overhead.

### Example 2: Push expressions down to TiFlash

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

In the preceding example, the expression `id + a` is pushed down to TiFlash for calculation in advance. This helps reduce the amount of data to be transferred over the network, thus reducing the network transmission overhead and improving the overall calculation performance.

### Example 3: Restrictions for pushdown

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

The preceding example only performs `TableFullScan` on TiFlash. Other functions are calculated and filtered on `root` and are not pushed down to TiFlash.

You can identify the operators and expressions that cannot be pushed down to TiFlash by running the following command:

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

The expressions in the preceding example cannot be completely pushed down to TiFlash, because the functions `Time` and `Cast` cannot be pushed down to TiFlash.
