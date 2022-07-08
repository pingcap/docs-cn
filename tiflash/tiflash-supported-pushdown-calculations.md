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
* Window functions: Currently, TiFlash supports row_number(), rank(), and dense_rank().

In TiDB, operators are organized in a tree structure. For an operator to be pushed down to TiFlash, all of the following prerequisites must be met:

+ All of its child operators can be pushed down to TiFlash.
+ If an operator contains expressions (most of the operators contain expressions), all expressions of the operator can be pushed down to TiFlash.

## Push-down expressions

TiFlash supports the following push-down expressions:

* Mathematical functions: `+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32, greatest(int/real), least(int/real)`
* Logical functions: `and, or, not, case when, if, ifnull, isnull, in, like, coalesce, is`
* Bitwise operations: `bitand, bitor, bigneg, bitxor`
* String functions: `substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp, regexp`
* Date functions: `date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add, date_sub, adddate, subdate, quarter, dayname, dayofmonth, dayofweek, dayofyear, last_day, monthname, to_seconds, to_days, from_days, weekofyear`
* JSON function: `json_length`
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
