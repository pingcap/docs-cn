---
title: TiFlash 支持的下推计算
summary: 了解 TiFlash 支持的下推计算。
---

# TiFlash 支持的下推计算

本文介绍 TiFlash 支持的下推计算。

## 下推算子

TiFlash 支持下推以下算子：

* TableScan：读取表中的数据。
* Selection：过滤数据。
* HashAgg：基于[哈希聚合](/explain-aggregation.md#hash-aggregation)算法执行数据聚合。
* StreamAgg：基于[流式聚合](/explain-aggregation.md#stream-aggregation)算法执行数据聚合。StreamAgg 仅支持不带 `GROUP BY` 条件的聚合。
* TopN：执行 TopN 计算。
* Limit：执行 limit 计算。
* Project：执行投影计算。
* HashJoin：使用[哈希连接](/explain-joins.md#hash-join)算法执行连接计算，但有以下条件：
    * 该算子仅在 [MPP 模式](/tiflash/use-tiflash-mpp-mode.md)下可以下推。
    * 支持的连接类型包括 Inner Join、Left Join、Semi Join、Anti Semi Join、Left Semi Join 和 Anti Left Semi Join。
    * 上述连接类型支持等值连接和非等值连接（笛卡尔积连接或空感知半连接）。在计算笛卡尔积连接或空感知半连接时，使用广播算法而不是 Shuffle Hash Join 算法。
* [窗口函数](/functions-and-operators/window-functions.md)：目前 TiFlash 支持 `ROW_NUMBER()`、`RANK()`、`DENSE_RANK()`、`LEAD()`、`LAG()`、`FIRST_VALUE()` 和 `LAST_VALUE()`。

在 TiDB 中，算子以树状结构组织。要将算子下推到 TiFlash，必须满足以下所有前提条件：

+ 其所有子算子都可以下推到 TiFlash。
+ 如果算子包含表达式（大多数算子都包含表达式），则该算子的所有表达式都可以下推到 TiFlash。

## 下推表达式

TiFlash 支持以下下推表达式：

| 表达式类型 | 运算符和函数 |
| :-------------- | :------------------------------------- |
| [数值函数和运算符](/functions-and-operators/numeric-functions-and-operators.md) | `+`、`-`、`/`、`*`、`%`、`>=`、`<=`、`=`、`!=`、`<`、`>`、`ROUND()`、`ABS()`、`FLOOR(int)`、`CEIL(int)`、`CEILING(int)`、`SQRT()`、`LOG()`、`LOG2()`、`LOG10()`、`LN()`、`EXP()`、`POW()`、`POWER()`、`SIGN()`、`RADIANS()`、`DEGREES()`、`CONV()`、`CRC32()`、`GREATEST(int/real)`、`LEAST(int/real)` |
| [逻辑函数](/functions-and-operators/control-flow-functions.md)和[运算符](/functions-and-operators/operators.md) | `AND`、`OR`、`NOT`、`CASE WHEN`、`IF()`、`IFNULL()`、`ISNULL()`、`IN`、`LIKE`、`ILIKE`、`COALESCE`、`IS` |
| [位运算](/functions-and-operators/bit-functions-and-operators.md) | `&`（按位与）、<code>\|</code>（按位或）、`~`（按位取反）、`^`（按位异或） |
| [字符串函数](/functions-and-operators/string-functions.md) | `SUBSTR()`、`CHAR_LENGTH()`、`REPLACE()`、`CONCAT()`、`CONCAT_WS()`、`LEFT()`、`RIGHT()`、`ASCII()`、`LENGTH()`、`TRIM()`、`LTRIM()`、`RTRIM()`、`POSITION()`、`FORMAT()`、`LOWER()`、`UCASE()`、`UPPER()`、`SUBSTRING_INDEX()`、`LPAD()`、`RPAD()`、`STRCMP()` |
| [正则表达式函数和运算符](/functions-and-operators/string-functions.md) | `REGEXP`、`REGEXP_LIKE()`、`REGEXP_INSTR()`、`REGEXP_SUBSTR()`、`REGEXP_REPLACE()`、`RLIKE` |
| [日期函数](/functions-and-operators/date-and-time-functions.md) | `DATE_FORMAT()`、`TIMESTAMPDIFF()`、`FROM_UNIXTIME()`、`UNIX_TIMESTAMP(int)`、`UNIX_TIMESTAMP(decimal)`、`STR_TO_DATE(date)`、`STR_TO_DATE(datetime)`、`DATEDIFF()`、`YEAR()`、`MONTH()`、`DAY()`、`EXTRACT(datetime)`、`DATE()`、`HOUR()`、`MICROSECOND()`、`MINUTE()`、`SECOND()`、`SYSDATE()`、`DATE_ADD/ADDDATE(datetime, int)`、`DATE_ADD/ADDDATE(string, int/real)`、`DATE_SUB/SUBDATE(datetime, int)`、`DATE_SUB/SUBDATE(string, int/real)`、`QUARTER()`、`DAYNAME()`、`DAYOFMONTH()`、`DAYOFWEEK()`、`DAYOFYEAR()`、`LAST_DAY()`、`MONTHNAME()`、`TO_SECONDS()`、`TO_DAYS()`、`FROM_DAYS()`、`WEEKOFYEAR()` |
| [JSON 函数](/functions-and-operators/json-functions.md) | `JSON_LENGTH()`、`->`、`->>`、`JSON_EXTRACT()`、`JSON_ARRAY()`、`JSON_DEPTH()`、`JSON_VALID()`、`JSON_KEYS()`、`JSON_CONTAINS_PATH()`、`JSON_UNQUOTE()` |
| [类型转换函数](/functions-and-operators/cast-functions-and-operators.md) | `CAST(int AS DOUBLE)、CAST(int AS DECIMAL)`、`CAST(int AS STRING)`、`CAST(int AS TIME)`、`CAST(double AS INT)`、`CAST(double AS DECIMAL)`、`CAST(double AS STRING)`、`CAST(double AS TIME)`、`CAST(string AS INT)`、`CAST(string AS DOUBLE)、CAST(string AS DECIMAL)`、`CAST(string AS TIME)`、`CAST(decimal AS INT)`、`CAST(decimal AS STRING)`、`CAST(decimal AS TIME)`、`CAST(decimal AS DOUBLE)`、`CAST(time AS INT)`、`CAST(time AS DECIMAL)`、`CAST(time AS STRING)`、`CAST(time AS REAL)`、`CAST(json AS JSON)`、`CAST(json AS STRING)`、`CAST(int AS JSON)`、`CAST(real AS JSON)`、`CAST(decimal AS JSON)`、`CAST(string AS JSON)`、`CAST(time AS JSON)`、`CAST(duration AS JSON)` |
| [聚合函数](/functions-and-operators/aggregate-group-by-functions.md) | `MIN()`、`MAX()`、`SUM()`、`COUNT()`、`AVG()`、`APPROX_COUNT_DISTINCT()`、`GROUP_CONCAT()` |
| [其他函数](/functions-and-operators/miscellaneous-functions.md) | `INET_NTOA()`、`INET_ATON()`、`INET6_NTOA()`、`INET6_ATON()` |

## 限制

* 包含 Bit、Set 和 Geometry 类型的表达式不能下推到 TiFlash。

* `DATE_ADD()`、`DATE_SUB()`、`ADDDATE()` 和 `SUBDATE()` 函数仅支持以下间隔类型。如果使用其他间隔类型，TiFlash 会报错。

    * DAY
    * WEEK
    * MONTH
    * YEAR
    * HOUR
    * MINUTE
    * SECOND

如果查询遇到不支持的下推计算，TiDB 需要完成剩余的计算，这可能会大大影响 TiFlash 的加速效果。当前不支持的算子和表达式可能会在未来版本中得到支持。

像 `MAX()` 这样的函数在作为聚合函数时支持下推，但作为窗口函数时不支持下推。

## 示例

本节提供一些将算子和表达式下推到 TiFlash 的示例。

### 示例 1：将算子下推到 TiFlash

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

在上述示例中，`Limit` 算子被下推到 TiFlash 进行数据过滤，这有助于减少需要通过网络传输的数据量，从而减少网络开销。这可以从 `Limit_15` 算子所在行的 `task` 列值为 `mpp[tiflash]` 看出。

### 示例 2：将表达式下推到 TiFlash

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

在上述示例中，表达式 `id + a` 被提前下推到 TiFlash 进行计算。这有助于减少需要通过网络传输的数据量，从而减少网络传输开销并提高整体计算性能。这可以从 `operator` 列值包含 `plus(test.t.id, test.t.a)` 的行中 `task` 列值为 `mpp[tiflash]` 看出。

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

上述示例仅在 TiFlash 上执行 `TableFullScan`。其他函数在 `root` 上计算和过滤，未下推到 TiFlash。

你可以通过运行以下命令来识别无法下推到 TiFlash 的算子和表达式：

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

上述示例中的表达式无法完全下推到 TiFlash，因为函数 `Time` 和 `Cast` 无法下推到 TiFlash。

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

在此输出中，你可以看到 `Window` 操作在 `task` 列中的值为 `mpp[tiflash]`，表明 `ROW_NUMBER() OVER (PARTITION BY id > 10)` 操作可以下推到 TiFlash。

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

在此输出中，你可以看到 `Window` 操作在 `task` 列中的值为 `root`，表明 `MAX(id) OVER (PARTITION BY id > 10)` 操作无法下推到 TiFlash。这是因为 `MAX()` 仅在作为聚合函数时支持下推，而作为窗口函数时不支持下推。
