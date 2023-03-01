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
* [Window functions](/functions-and-operators/window-functions.md): Currently, TiFlash supports `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LEAD()`, and `LAG()`.

In TiDB, operators are organized in a tree structure. For an operator to be pushed down to TiFlash, all of the following prerequisites must be met:

+ All of its child operators can be pushed down to TiFlash.
+ If an operator contains expressions (most of the operators contain expressions), all expressions of the operator can be pushed down to TiFlash.

## Push-down expressions

TiFlash supports the following push-down expressions:

| Expression Type | Operations |
| :-------------- | :------------------------------------- |
| [Numeric functions and operators](/functions-and-operators/numeric-functions-and-operators.md) | `+`, `-`, `/`, `*`, `%`, `>=`, `<=`, `=`, `!=`, `<`, `>`, `ROUND()`, `ABS()`, `FLOOR(int)`, `CEIL(int)`, `CEILING(int)`, `SQRT()`, `LOG()`, `LOG2()`, `LOG10()`, `LN()`, `EXP()`, `POW()`, `SIGN()`, `RADIANS()`, `DEGREES()`, `CONV()`, `CRC32()`, `GREATEST(int/real)`, `LEAST(int/real)` |
| [Logical functions](/functions-and-operators/control-flow-functions.md) and [operators](/functions-and-operators/operators.md) | `AND`, `OR`, `NOT`, `CASE WHEN`, `IF()`, `IFNULL()`, `ISNULL()`, `IN`, `LIKE`, `COALESCE`, `IS` |
| [Bitwise operations](/functions-and-operators/bit-functions-and-operators.md) | `&` (bitand), `\|` (bitor), `~` (bitneg), `^` (bitxor) |
| [String functions](/functions-and-operators/string-functions.md) | `SUBSTR()`, `CHAR_LENGTH()`, `REPLACE()`, `CONCAT()`, `CONCAT_WS()`, `LEFT()`, `RIGHT()`, `ASCII()`, `LENGTH()`, `TRIM()`, `LTRIM()`, `RTRIM()`, `POSITION()`, `FORMAT()`, `LOWER()`, `UCASE()`, `UPPER()`, `SUBSTRING_INDEX()`, `LPAD()`, `RPAD()`, `STRCMP()` |
| [Regular expression functions and operators](/functions-and-operators/string-functions.md) | `REGEXP`, `REGEXP_LIKE()`, `REGEXP_INSTR()`, `REGEXP_SUBSTR()`, `REGEXP_REPLACE()` |
| [Date functions](/functions-and-operators/date-and-time-functions.md) | `DATE_FORMAT()`, `TIMESTAMPDIFF()`, `FROM_UNIXTIME()`, `UNIX_TIMESTAMP(int)`, `UNIX_TIMESTAMP(decimal)`, `STR_TO_DATE(date)`, `STR_TO_DATE(datetime)`, `DATEDIFF()`, `YEAR()`, `MONTH()`, `DAY()`, `EXTRACT(datetime)`, `DATE()`, `HOUR()`, `MICROSECOND()`, `MINUTE()`, `SECOND()`, `SYSDATE()`, `DATE_ADD/ADDDATE(datetime, int)`, `DATE_ADD/ADDDATE(string, int/real)`, `DATE_SUB/SUBDATE(datetime, int)`, `DATE_SUB/SUBDATE(string, int/real)`, `QUARTER()`, `DAYNAME()`, `DAYOFMONTH()`, `DAYOFWEEK()`, `DAYOFYEAR()`, `LAST_DAY()`, `MONTHNAME()`, `TO_SECONDS()`, `TO_DAYS()`, `FROM_DAYS()`, `WEEKOFYEAR()`
| [JSON function](/functions-and-operators/json-functions.md) | `JSON_LENGTH()`, `->`, `->>`, `JSON_EXTRACT()` |
| [Conversion functions](/functions-and-operators/cast-functions-and-operators.md) | `CAST(int AS DOUBLE), CAST(int AS DECIMAL)`, `CAST(int AS STRING)`, `CAST(int AS TIME)`, `CAST(double AS INT)`, `CAST(double AS DECIMAL)`, `CAST(double AS STRING)`, `CAST(double AS TIME)`, `CAST(string AS INT)`, `CAST(string AS DOUBLE), CAST(string AS DECIMAL)`, `CAST(string AS TIME)`, `CAST(decimal AS INT)`, `CAST(decimal AS STRING)`, `CAST(decimal AS TIME)`, `CAST(time AS INT)`, `CAST(time AS DECIMAL)`, `CAST(time AS STRING)`, `CAST(time AS REAL)` |
| [Aggregate functions](/functions-and-operators/aggregate-group-by-functions.md) | `MIN()`, `MAX()`, `SUM()`, `COUNT()`, `AVG()`, `APPROX_COUNT_DISTINCT()`, `GROUP_CONCAT()` |
| [Miscellaneous functions](/functions-and-operators/miscellaneous-functions.md) | `INET_NTOA()`, `INET_ATON()`, `INET6_NTOA()`, `INET6_ATON()` |

## Restrictions

* Expressions that contain the Bit, Set, and Geometry types cannot be pushed down to TiFlash.

* The `DATE_ADD()`, `DATE_SUB()`, `ADDDATE()`, and `SUBDATE()` functions support the following interval types only. If other interval types are used, TiFlash reports errors.

    * DAY
    * WEEK
    * MONTH
    * YEAR
    * HOUR
    * MINUTE
    * SECOND

If a query encounters unsupported push-down calculations, TiDB needs to complete the remaining calculations, which might greatly affect the TiFlash acceleration effect. The currently unsupported operators and expressions might be supported in future versions.

Functions like `MAX()` are supported for push-down when used as aggregate functions, but not as window functions.

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

In the preceding example, the operator `Limit` is pushed down to TiFlash for filtering data, which helps reduce the amount of data to be transferred over the network and reduce the network overhead. This is indicated by the `mpp[tiflash]` value of the `task` column on the row of the `Limit_15` operator.

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

In the preceding example, the expression `id + a` is pushed down to TiFlash for calculation in advance. This helps reduce the amount of data to be transferred over the network, thus reducing the network transmission overhead and improving the overall calculation performance. This is indicated by the `mpp[tiflash]` value in the `task` column of the row where the `operator` column has the `plus(test.t.id, test.t.a)` value.

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

### Example 4: Window functions

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

In this output, you can see that the `Window` operation has a value of `mpp[tiflash]` in the `task` column, indicating that the `ROW_NUMBER() OVER (PARTITION BY id > 10)` operation can be pushed down to TiFlash.

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

In this output, you can see that the `Window` operation has a value of `root` in the `task` column, indicating that the `MAX(id) OVER (PARTITION BY id > 10)` operation cannot be pushed down to TiFlash. This is because `MAX()` is only supported for push-down as an aggregate function and not as a window function.
