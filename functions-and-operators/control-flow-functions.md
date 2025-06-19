---
title: 流程控制函数
summary: 了解流程控制函数。
---

# 流程控制函数

TiDB 支持 MySQL 8.0 中提供的所有[流程控制函数](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html)。

| 名称                                                                                            | 描述                       |
|:--------------------------------------------------------------------------------------------------|:----------------------------------|
| [`CASE`](#case)       | Case 运算符                     |
| [`IF()`](#if)         | If/else 结构                 |
| [`IFNULL()`](#ifnull) | Null if/else 结构            |
| [`NULLIF()`](#nullif) | 如果 expr1 = expr2，则返回 `NULL`      |

## CASE

[`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case) 运算符使你能够执行条件逻辑并根据指定条件自定义查询结果。

语法：

```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ...
    ELSE default_result
END
```

示例：

```sql
WITH RECURSIVE d AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM d WHERE n<10)
SELECT n, CASE WHEN n MOD 2 THEN "odd" ELSE "even" END FROM d;
```

```
+----+----------------------------------------------+
| n  | CASE WHEN n MOD 2 THEN "odd" ELSE "even" END |
+----+----------------------------------------------+
|  1 | odd                                          |
|  2 | even                                         |
|  3 | odd                                          |
|  4 | even                                         |
|  5 | odd                                          |
|  6 | even                                         |
|  7 | odd                                          |
|  8 | even                                         |
|  9 | odd                                          |
| 10 | even                                         |
+----+----------------------------------------------+
10 rows in set (0.00 sec)
```

## IF()

[`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if) 函数使你能够根据值或表达式是否为真来执行不同的操作。

语法：

```sql
IF(condition, value_if_true, value_if_false)
```

示例：

```sql
WITH RECURSIVE d AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM d WHERE n<10)
SELECT n, IF(n MOD 2, "odd", "even") FROM d;
```

```
+----+----------------------------+
| n  | IF(n MOD 2, "odd", "even") |
+----+----------------------------+
|  1 | odd                        |
|  2 | even                       |
|  3 | odd                        |
|  4 | even                       |
|  5 | odd                        |
|  6 | even                       |
|  7 | odd                        |
|  8 | even                       |
|  9 | odd                        |
| 10 | even                       |
+----+----------------------------+
10 rows in set (0.00 sec)
```

## IFNULL()

[`IFNULL(expr1,expr2)`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) 函数用于处理查询中的 NULL 值。如果 `expr1` 不为 `NULL`，则返回 `expr1`；否则返回 `expr2`。

示例：

```sql
WITH data AS (SELECT NULL AS x UNION ALL SELECT 1 )
SELECT x, IFNULL(x,'x has no value') FROM data;
```

```
+------+----------------------------+
| x    | IFNULL(x,'x has no value') |
+------+----------------------------+
| NULL | x has no value             |
|    1 | 1                          |
+------+----------------------------+
2 rows in set (0.0006 sec)
```

## NULLIF()

[`NULLIF(expr1,expr2)`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) 函数在两个参数相同或第一个参数为 `NULL` 时返回 `NULL`。否则，返回第一个参数。

示例：

```sql
WITH RECURSIVE d AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM d WHERE n<10)
SELECT n, NULLIF(n+n, n+2) FROM d;
```

```
+----+------------------+
| n  | NULLIF(n+n, n+2) |
+----+------------------+
|  1 |                2 |
|  2 |             NULL |
|  3 |                6 |
|  4 |                8 |
|  5 |               10 |
|  6 |               12 |
|  7 |               14 |
|  8 |               16 |
|  9 |               18 |
| 10 |               20 |
+----+------------------+
10 rows in set (0.00 sec)
```

在此示例中，当 `n` 等于 `2` 时，`n+n` 和 `n+2` 都等于 `4`，使两个参数相同，导致函数返回 `NULL`。
