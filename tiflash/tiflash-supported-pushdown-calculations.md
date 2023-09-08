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
* Window：当前支持下推的窗口函数包括：row_number()、rank() 和 dense_rank()

在 TiDB 中，算子之间会呈现树型组织结构。一个算子能下推到 TiFlash 的前提条件，是该算子的所有子算子都能下推到 TiFlash。因为大部分算子都包含有表达式计算，当且仅当一个算子所包含的所有表达式均支持下推到 TiFlash 时，该算子才有可能下推给 TiFlash。

## 支持下推的表达式

* 数学函数：`+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32, greatest(int/real), least(int/real)`
* 逻辑函数：`and, or, not, case when, if, ifnull, isnull, in, like, coalesce, is`
* 位运算：`bitand, bitor, bigneg, bitxor`
* 字符串函数：`substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp, regexp`
* 日期函数：`date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add/adddate(datetime, int), date_add/adddate(string, int), date_add/adddate(string, real), date_sub/subdate(datetime, int), date_sub/subdate(string, int), date_sub/subdate(string, real), quarter, dayname, dayofmonth, dayofweek, dayofyear, last_day, monthname, to_seconds, to_days, from_days, weekofyear`
* JSON 函数：`json_length`
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
* 所有包含 [`ROWS` 或 `RANGE` 类型的 frame](https://dev.mysql.com/doc/refman/8.0/en/window-functions-frames.html) 的窗口函数均不支持下推到 TiFlash

如查询遇到不支持的下推计算，则需要依赖 TiDB 完成剩余计算，可能会很大程度影响 TiFlash 加速效果。对于暂不支持的算子/表达式，将会在后续版本中陆续支持。
