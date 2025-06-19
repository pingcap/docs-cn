---
title: 窗口函数
summary: 本文档介绍 TiDB 支持的窗口函数。
---

# 窗口函数

TiDB 中窗口函数的用法与 MySQL 8.0 类似。详情请参见 [MySQL 窗口函数](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html)。

在 TiDB 中，你可以使用以下系统变量来控制窗口函数：

- [`tidb_enable_window_function`](/system-variables.md#tidb_enable_window_function)：由于窗口函数在解析器中保留了额外的[关键字](/keywords.md)，TiDB 提供此变量来禁用窗口函数。如果在升级 TiDB 后解析 SQL 语句时出现错误，请尝试将此变量设置为 `OFF`。
- [`tidb_enable_pipelined_window_function`](/system-variables.md#tidb_enable_pipelined_window_function)：你可以使用此变量来禁用窗口函数的流水线执行算法。
- [`windowing_use_high_precision`](/system-variables.md#windowing_use_high_precision)：你可以使用此变量来禁用窗口函数的高精度模式。

[此处列出的](/tiflash/tiflash-supported-pushdown-calculations.md)窗口函数可以下推到 TiFlash。

除了 `GROUP_CONCAT()` 和 `APPROX_PERCENTILE()` 外，TiDB 支持将所有 [`GROUP BY` 聚合函数](/functions-and-operators/aggregate-group-by-functions.md)用作窗口函数。此外，TiDB 还支持以下窗口函数：

| 函数名                     | 功能描述 |
| :-------------------------------- | :------------------------------------- |
| [`CUME_DIST()`](#cume_dist)       | 返回一组值中某个值的累积分布。 |
| [`DENSE_RANK()`](#dense_rank)     | 返回当前行在分区内的排名，排名是连续的（无间隔）。 |
| [`FIRST_VALUE()`](#first_value)   | 返回当前窗口中第一行的表达式值。 |
| [`LAG()`](#lag)                   | 返回分区内当前行前 N 行的表达式值。 |
| [`LAST_VALUE()`](#last_value)     | 返回当前窗口中最后一行的表达式值。 |
| [`LEAD()`](#lead)                 | 返回分区内当前行后 N 行的表达式值。 |
| [`NTH_VALUE()`](#nth_value)       | 返回当前窗口中第 N 行的表达式值。 |
| [`NTILE()`](#ntile)               | 将分区划分为 N 个桶，为分区中的每一行分配桶号，并返回当前行在分区内的桶号。 |
| [`PERCENT_RANK()`](#percent_rank) | 返回小于当前行值的分区值的百分比。 |
| [`RANK()`](#rank)                 | 返回当前行在分区内的排名。排名可能有间隔。 |
| [`ROW_NUMBER()`](#row_number)     | 返回分区中当前行的编号。 |

## [`CUME_DIST()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_cume-dist)

`CUME_DIST()` 计算一组值中某个值的累积分布。注意，你需要使用 `ORDER BY` 子句与 `CUME_DIST()` 一起使用来对值组进行排序。否则，此函数将不会返回预期的值。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT 1
    UNION
    SELECT
        n+2
    FROM
        cte
    WHERE
        n<6
)
SELECT
    *,
    CUME_DIST() OVER(ORDER BY n)
FROM
    cte;
```

```
+------+------------------------------+
| n    | CUME_DIST() OVER(ORDER BY n) |
+------+------------------------------+
|    1 |                         0.25 |
|    3 |                          0.5 |
|    5 |                         0.75 |
|    7 |                            1 |
+------+------------------------------+
4 rows in set (0.00 sec)
```

## [`DENSE_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_dense-rank)

`DENSE_RANK()` 函数返回当前行的排名。它类似于 [`RANK()`](#rank)，但在出现并列（共享相同值和排序条件的行）时不会留下间隔。

```sql
SELECT
    *,
    DENSE_RANK() OVER (ORDER BY n)
FROM (
    SELECT 5 AS 'n'
    UNION ALL
    SELECT 8
    UNION ALL
    SELECT 5
    UNION ALL
    SELECT 30
    UNION ALL
    SELECT 31
    UNION ALL
    SELECT 32) a;
```

```
+----+--------------------------------+
| n  | DENSE_RANK() OVER (ORDER BY n) |
+----+--------------------------------+
|  5 |                              1 |
|  5 |                              1 |
|  8 |                              2 |
| 30 |                              3 |
| 31 |                              4 |
| 32 |                              5 |
+----+--------------------------------+
6 rows in set (0.00 sec)
```

## [`FIRST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_first-value)

`FIRST_VALUE(expr)` 返回窗口中的第一个值。

以下示例使用了两种不同的窗口定义：

- `PARTITION BY n MOD 2 ORDER BY n` 将表 `a` 中的数据分为两组：`1, 3` 和 `2, 4`。因此它返回 `1` 或 `2`，因为这些是这些组的第一个值。
- `PARTITION BY n <= 2 ORDER BY n` 将表 `a` 中的数据分为两组：`1, 2` 和 `3, 4`。因此它返回 `1` 或 `3`，具体取决于 `n` 属于哪个组。

```sql
SELECT
    n,
    FIRST_VALUE(n) OVER (PARTITION BY n MOD 2 ORDER BY n),
    FIRST_VALUE(n) OVER (PARTITION BY n <= 2 ORDER BY n)
FROM (
    SELECT 1 AS 'n'
    UNION
    SELECT 2
    UNION
    SELECT 3
    UNION
    SELECT 4
) a
ORDER BY
    n;
```

```
+------+-------------------------------------------------------+------------------------------------------------------+
| n    | FIRST_VALUE(n) OVER (PARTITION BY n MOD 2 ORDER BY n) | FIRST_VALUE(n) OVER (PARTITION BY n <= 2 ORDER BY n) |
+------+-------------------------------------------------------+------------------------------------------------------+
|    1 |                                                     1 |                                                    1 |
|    2 |                                                     2 |                                                    1 |
|    3 |                                                     1 |                                                    3 |
|    4 |                                                     2 |                                                    3 |
+------+-------------------------------------------------------+------------------------------------------------------+
4 rows in set (0.00 sec)
```

## [`LAG()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lag)

`LAG(expr [, num [, default]])` 函数返回当前行前 `num` 行的 `expr` 值。如果该行不存在，则返回 `default`。默认情况下，当未指定时，`num` 为 `1`，`default` 为 `NULL`。

在以下示例中，由于未指定 `num`，`LAG(n)` 返回前一行的 `n` 值。当 `n` 为 1 时，由于前一行不存在且未指定 `default`，`LAG(1)` 返回 `NULL`。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT 1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    LAG(n) OVER ()
FROM
    cte;
```

```
+------+----------------+
| n    | LAG(n) OVER () |
+------+----------------+
|    1 |           NULL |
|    2 |              1 |
|    3 |              2 |
|    4 |              3 |
|    5 |              4 |
|    6 |              5 |
|    7 |              6 |
|    8 |              7 |
|    9 |              8 |
|   10 |              9 |
+------+----------------+
10 rows in set (0.01 sec)
```

## [`LAST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_last-value)

`LAST_VALUE()` 函数返回窗口中的最后一个值。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    LAST_VALUE(n) OVER (PARTITION BY n<=5)
FROM
    cte
ORDER BY
    n;
```

```
+------+----------------------------------------+
| n    | LAST_VALUE(n) OVER (PARTITION BY n<=5) |
+------+----------------------------------------+
|    1 |                                      5 |
|    2 |                                      5 |
|    3 |                                      5 |
|    4 |                                      5 |
|    5 |                                      5 |
|    6 |                                     10 |
|    7 |                                     10 |
|    8 |                                     10 |
|    9 |                                     10 |
|   10 |                                     10 |
+------+----------------------------------------+
10 rows in set (0.00 sec)
```

## [`LEAD()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lead)

`LEAD(expr [, num [,default]])` 函数返回当前行后 `num` 行的 `expr` 值。如果该行不存在，则返回 `default`。默认情况下，当未指定时，`num` 为 `1`，`default` 为 `NULL`。

在以下示例中，由于未指定 `num`，`LEAD(n)` 返回下一行的 `n` 值。当 `n` 为 10 时，由于下一行不存在且未指定 `default`，`LEAD(10)` 返回 `NULL`。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    LEAD(n) OVER ()
FROM
    cte;
```

```
+------+-----------------+
| n    | LEAD(n) OVER () |
+------+-----------------+
|    1 |               2 |
|    2 |               3 |
|    3 |               4 |
|    4 |               5 |
|    5 |               6 |
|    6 |               7 |
|    7 |               8 |
|    8 |               9 |
|    9 |              10 |
|   10 |            NULL |
+------+-----------------+
10 rows in set (0.00 sec)
```

## [`NTH_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_nth-value)

`NTH_VALUE(expr, n)` 函数返回窗口中的第 `n` 个值。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    FIRST_VALUE(n) OVER w AS 'First',
    NTH_VALUE(n, 2) OVER w AS 'Second',
    NTH_VALUE(n, 3) OVER w AS 'Third',
    LAST_VALUE(n) OVER w AS 'Last'
FROM
    cte
WINDOW
    w AS (PARTITION BY n<=5)
ORDER BY
    n;
```

```
+------+-------+--------+-------+------+
| n    | First | Second | Third | Last |
+------+-------+--------+-------+------+
|    1 |     1 |      2 |     3 |    5 |
|    2 |     1 |      2 |     3 |    5 |
|    3 |     1 |      2 |     3 |    5 |
|    4 |     1 |      2 |     3 |    5 |
|    5 |     1 |      2 |     3 |    5 |
|    6 |     6 |      7 |     8 |   10 |
|    7 |     6 |      7 |     8 |   10 |
|    8 |     6 |      7 |     8 |   10 |
|    9 |     6 |      7 |     8 |   10 |
|   10 |     6 |      7 |     8 |   10 |
+------+-------+--------+-------+------+
10 rows in set (0.00 sec)
```

## [`NTILE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_ntile)

`NTILE(n)` 函数将窗口分成 `n` 组，并返回每行所属的组号。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
    n<10
)
SELECT
    n,
    NTILE(5) OVER (),
    NTILE(2) OVER ()
FROM
    cte;
```

```
+------+------------------+------------------+
| n    | NTILE(5) OVER () | NTILE(2) OVER () |
+------+------------------+------------------+
|    1 |                1 |                1 |
|    2 |                1 |                1 |
|    3 |                2 |                1 |
|    4 |                2 |                1 |
|    5 |                3 |                1 |
|    6 |                3 |                2 |
|    7 |                4 |                2 |
|    8 |                4 |                2 |
|    9 |                5 |                2 |
|   10 |                5 |                2 |
+------+------------------+------------------+
10 rows in set (0.00 sec)
```

## [`PERCENT_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_percent-rank)

`PERCENT_RANK()` 函数返回一个介于 0 和 1 之间的数字，表示小于当前行值的行的百分比。

```sql
SELECT
    *,
    PERCENT_RANK() OVER (ORDER BY n),
    PERCENT_RANK() OVER (ORDER BY n DESC)
FROM (
    SELECT 5 AS 'n'
    UNION ALL
    SELECT 8
    UNION ALL
    SELECT 5
    UNION ALL
    SELECT 30
    UNION ALL
    SELECT 31
    UNION ALL
    SELECT 32) a;
```

```
+----+----------------------------------+---------------------------------------+
| n  | PERCENT_RANK() OVER (ORDER BY n) | PERCENT_RANK() OVER (ORDER BY n DESC) |
+----+----------------------------------+---------------------------------------+
|  5 |                                0 |                                   0.8 |
|  5 |                                0 |                                   0.8 |
|  8 |                              0.4 |                                   0.6 |
| 30 |                              0.6 |                                   0.4 |
| 31 |                              0.8 |                                   0.2 |
| 32 |                                1 |                                     0 |
+----+----------------------------------+---------------------------------------+
6 rows in set (0.00 sec)
```

## [`RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_rank)

`RANK()` 函数类似于 [`DENSE_RANK()`](#dense_rank)，但在出现并列（共享相同值和排序条件的行）时会留下间隔。这意味着它提供了一个绝对排名。例如，排名 7 意味着有 6 个排名较低的行。

```sql
SELECT
    *,
    RANK() OVER (ORDER BY n),
    DENSE_RANK() OVER (ORDER BY n)
FROM (
    SELECT 5 AS 'n'
    UNION ALL
    SELECT 8
    UNION ALL
    SELECT 5
    UNION ALL
    SELECT 30
    UNION ALL
    SELECT 31
    UNION ALL
    SELECT 32) a;
```

```
+----+--------------------------+--------------------------------+
| n  | RANK() OVER (ORDER BY n) | DENSE_RANK() OVER (ORDER BY n) |
+----+--------------------------+--------------------------------+
|  5 |                        1 |                              1 |
|  5 |                        1 |                              1 |
|  8 |                        3 |                              2 |
| 30 |                        4 |                              3 |
| 31 |                        5 |                              4 |
| 32 |                        6 |                              5 |
+----+--------------------------+--------------------------------+
6 rows in set (0.00 sec)
```

## [`ROW_NUMBER()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_row-number)

`ROW_NUMBER()` 返回结果集中当前行的行号。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+3
    FROM
        cte
    WHERE
        n<30
)
SELECT
    n,
    ROW_NUMBER() OVER ()
FROM
    cte;
```

```
+------+----------------------+
| n    | ROW_NUMBER() OVER () |
+------+----------------------+
|    1 |                    1 |
|    4 |                    2 |
|    7 |                    3 |
|   10 |                    4 |
|   13 |                    5 |
|   16 |                    6 |
|   19 |                    7 |
|   22 |                    8 |
|   25 |                    9 |
|   28 |                   10 |
|   31 |                   11 |
+------+----------------------+
11 rows in set (0.00 sec)
```
