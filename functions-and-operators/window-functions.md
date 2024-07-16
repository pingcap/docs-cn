---
title: 窗口函数
aliases: ['/docs-cn/dev/functions-and-operators/window-functions/','/docs-cn/dev/reference/sql/functions-and-operators/window-functions/']
summary: TiDB 中的窗口函数与 MySQL 8.0 基本一致。可以将 `tidb_enable_window_function` 设置为 `0` 来解决升级后无法解析语法的问题。TiDB 支持除 `GROUP_CONCAT()` 和 `APPROX_PERCENTILE()` 以外的所有 `GROUP BY` 聚合函数。其他支持的窗口函数包括 `CUME_DIST()`、`DENSE_RANK()`、`FIRST_VALUE()`、`LAG()`、`LAST_VALUE()`、`LEAD()`、`NTH_VALUE()`、`NTILE()`、`PERCENT_RANK()`、`RANK()` 和 `ROW_NUMBER()`。这些函数可以下推到 TiFlash。
---

# 窗口函数

TiDB 中窗口函数的使用方法与 MySQL 8.0 基本一致，详情可参见 [MySQL 窗口函数](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html)。由于窗口函数会使用一些保留关键字，可能导致原先可以正常执行的 SQL 语句在升级 TiDB 后无法被解析语法，此时可以将 [`tidb_enable_window_function`](/system-variables.md#tidb_enable_window_function) 设置为 `0`，该参数的默认值为 `1`。

你可以使用 [`tidb_enable_pipelined_window_function`](/system-variables.md#tidb_enable_pipelined_window_function) 系统变量禁用窗口函数的流水线执行算法。

另一个影响窗口功能的系统变量是 [`windowing_use_high_precision`](/system-variables.md#windowing_use_high_precision)。你可以使用该变量关闭高精度模式。

[本页](/tiflash/tiflash-supported-pushdown-calculations.md)列出的窗口函数可以下推到 TiFlash。

TiDB 支持除 `GROUP_CONCAT()` 和 `APPROX_PERCENTILE()` 以外的所有 [`GROUP BY` 聚合函数](/functions-and-operators/aggregate-group-by-functions.md)。此外，TiDB 支持的其他窗口函数如下：

| 函数名 | 功能描述 |
| :-------------- | :------------------------------------- |
| [`CUME_DIST()`](#cume_dist)      | 返回一组值中的累积分布 |
| [`DENSE_RANK()`](#dense_rank)    | 返回分区中当前行的排名，并且排名是连续的|
| [`FIRST_VALUE()`](#first_value)  | 当前窗口中第一行的表达式值 |
| [`LAG()`](#lag)                  | 分区中当前行前面第 N 行的表达式值|
| [`LAST_VALUE()`](#last_value)    | 当前窗口中最后一行的表达式值 |
| [`LEAD()`](#lead)                | 分区中当前行后面第 N 行的表达式值 |
| [`NTH_VALUE()`](#nth_value)      | 当前窗口中第 N 行的表达式值 |
| [`NTILE()`](#ntile)              | 将分区划分为 N 桶，为分区中的每一行分配桶号 |
| [`PERCENT_RANK()`](#percent_rank)| 返回分区中小于当前行的百分比 |
| [`RANK()`](#rank)                | 返回分区中当前行的排名，排名可能不连续 |
| [`ROW_NUMBER()`](#row_number)    | 返回分区中当前行的编号 |

## [`CUME_DIST()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_cume-dist)

`CUME_DIST()` 计算累积距离。请注意，窗口定义应使用 `ORDER BY`，否则将无法返回预期值。

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

`DENSE_RANK()`函数类似于 [`RANK()`](#rank)，但不会在出现并列时留下任何间隙。

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

`FIRST_VALUE(expr)` 返回数组中的第一个值。

下面的示例使用了两个不同的窗口定义：

1. `PARTITION BY n MOD 2 ORDER BY n` 的结果是两个数组：`1, 3` 和`2, 4`。因此，返回值要么是 1，要么是 2，因为它们是这两组的第一个值。
2. `PARTITION BY n <= 2 ORDER BY n` 会产生两个组：`1, 2` 和`3, 4` 因此，根据它所属的数组，会返回 1 或 3。

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

函数 `LAG(expr [, num [, default]])` 返回落后于当前值 `num` 的值。如果没有当前值，则返回 `default`，默认为 `NULL'。

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

函数 `LEAD(expr [, num [,default]])` 返回窗口中的前导值。它的前导值为 `num`，默认为 `1`。如果没有前导值，则返回 `default`。默认为 `NULL`。

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

函数 `NTH_VALUE(expr, n)` 返回窗口的第 n 个值。

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

`NTILE(n)` 函数将窗口分成 `n` 组，并返回数组的编号。

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

`PERCENT_RANK()` 函数返回一个介于 0 和 1 之间的数字，表示值小于当前窗口值的行的百分比。

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

`RANK()` 函数类似于 [`DENSE_RANK()`](#dense_rank)，但会在出现并列时留出空隙。这意味着它提供的是绝对排名。例如，等级为 7 意味着有 6 个等级更低。

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

`ROW_NUMBER()` 返回结果集的行号。

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
