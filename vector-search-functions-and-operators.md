---
title: 向量函数和操作
summary: 本文介绍 TiDB 的向量相关函数和操作。
---

# 向量函数和操作


## 向量函数

[向量数据类型](/vector-search-data-types.md)具有以下函数：

**向量距离函数:**

| Function Name                                             | Description                                                      |
| --------------------------------------------------------- | ---------------------------------------------------------------- |
| [VEC_L2_DISTANCE](#vec_l2_distance)                       | Calculates L2 distance (Euclidean distance) between two vectors  |
| [VEC_COSINE_DISTANCE](#vec_cosine_distance)               | Calculates the cosine distance between two vectors               |
| [VEC_NEGATIVE_INNER_PRODUCT](#vec_negative_inner_product) | Calculates the negative of the inner product between two vectors |
| [VEC_L1_DISTANCE](#vec_l1_distance)                       | Calculates L1 distance (Manhattan distance) between two vectors  |

**其他向量函数:**

| Function Name                   | Description                                         |
| ------------------------------- | --------------------------------------------------- |
| [VEC_DIMS](#vec_dims)           | Returns the dimension of a vector                   |
| [VEC_L2_NORM](#vec_l2_norm)     | Calculates the L2 norm (Euclidean norm) of a vector |
| [VEC_FROM_TEXT](#vec_from_text) | Converts a string into a vector                     |
| [VEC_AS_TEXT](#vec_as_text)     | Converts a vector into a string                     |

## 扩展内置函数和运算符

扩展了以下内置函数和操作符，支持对[向量数据类型](/vector-search-data-types.md)进行操作。

**算术运算符:**

| Name                                                                                    | Description                              |
| :-------------------------------------------------------------------------------------- | :--------------------------------------- |
| [`+`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)  | Vector element-wise addition operator    |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus) | Vector element-wise subtraction operator |

有关向量运算工作原理的更多信息，请参阅 [向量数据类型 | 运算](/vector-search-data-types.md#运算)。

**聚合函数(GROUP BY):**

| Name                                                                                                          | Description                                      |
| :------------------------------------------------------------------------------------------------------------ | :----------------------------------------------- |
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                  | Return a count of the number of rows returned    |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct) | Return the count of a number of different values |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                      | Return the maximum value                         |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                      | Return the minimum value                         |

**比较函数与操作符:**

| Name                                                                                                                | Description                                           |
| ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| [`BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between)         | Check whether a value is within a range of values     |
| [`COALESCE()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce)                 | Return the first non-NULL argument                    |
| [`=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal)                             | Equal operator                                        |
| [`<=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to)                        | NULL-safe equal to operator                           |
| [`>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than)                      | Greater than operator                                 |
| [`>=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal)            | Greater than or equal operator                        |
| [`GREATEST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest)                 | Return the largest argument                           |
| [`IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in)                             | Check whether a value is within a set of values       |
| [`IS NULL`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null)                     | NULL value test                                       |
| [`ISNULL()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull)                     | Test whether the argument is NULL                     |
| [`LEAST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least)                       | Return the smallest argument                          |
| [`<`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than)                         | Less than operator                                    |
| [`<=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal)               | Less than or equal operator                           |
| [`NOT BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | Check whether a value is not within a range of values |
| [`!=`, `<>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal)                  | Not equal operator                                    |
| [`NOT IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in)                     | Check whether a value is not within a set of values   |

For more information about how vectors are compared, see [Vector Data Type | Comparison](/tidb-cloud/vector-search-data-types.md#comparison).

**控制流函数:**

| Name                                                                                              | Description                  |
| :------------------------------------------------------------------------------------------------ | :--------------------------- |
| [`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)       | Case operator                |
| [`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if)         | If/else construct            |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) | Null if/else construct       |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) | Return NULL if expr1 = expr2 |

**转换函数:**

| Name                                                                                        | Description                    |
| :------------------------------------------------------------------------------------------ | :----------------------------- |
| [`CAST()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast)       | Cast a value as a certain type |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) | Cast a value as a certain type |

有关如何使用 `CAST()` 的更多信息，请参阅 [向量数据类型 | 类型转换](/vector-search-data-types.md#类型转换)。

## 参考

### VEC_L2_DISTANCE

```sql
VEC_L2_DISTANCE(vector1, vector2)
```

使用以下公式计算两个向量之间的 L2 距离（欧氏距离）：

$DISTANCE(p,q)=\sqrt {\sum \limits _{i=1}^{n}{(p_{i}-q_{i})^{2}}}$

两个向量的维度必须相同。否则将返回错误信息。

例如:

```sql
[tidb]> select VEC_L2_DISTANCE('[0,3]', '[4,0]');
+-----------------------------------+
| VEC_L2_DISTANCE('[0,3]', '[4,0]') |
+-----------------------------------+
|                                 5 |
+-----------------------------------+
```

### VEC_COSINE_DISTANCE

```sql
VEC_COSINE_DISTANCE(vector1, vector2)
```

使用以下公式计算两个向量之间的余弦距离：

$DISTANCE(p,q)=1.0 - {\frac {\sum \limits _{i=1}^{n}{p_{i}q_{i}}}{{\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}}\cdot {\sqrt {\sum \limits _{i=1}^{n}{q_{i}^{2}}}}}}$

两个向量的维度必须相同。否则将返回错误信息。

例如:

```sql
[tidb]> select VEC_COSINE_DISTANCE('[1, 1]', '[-1, -1]');
+-------------------------------------------+
| VEC_COSINE_DISTANCE('[1, 1]', '[-1, -1]') |
+-------------------------------------------+
|                                         2 |
+-------------------------------------------+
```

### VEC_NEGATIVE_INNER_PRODUCT

```sql
VEC_NEGATIVE_INNER_PRODUCT(vector1, vector2)
```

利用两个向量间内积的负值计算距离，公式如下：

$DISTANCE(p,q)=- INNER\_PROD(p,q)=-\sum \limits _{i=1}^{n}{p_{i}q_{i}}$

两个向量的维度必须相同。否则将返回错误信息。

例如:

```sql
[tidb]> select VEC_NEGATIVE_INNER_PRODUCT('[1,2]', '[3,4]');
+----------------------------------------------+
| VEC_NEGATIVE_INNER_PRODUCT('[1,2]', '[3,4]') |
+----------------------------------------------+
|                                          -11 |
+----------------------------------------------+
```

### VEC_L1_DISTANCE

```sql
VEC_L1_DISTANCE(vector1, vector2)
```

使用以下公式计算两个向量之间的 L1 距离（曼哈顿距离）：

$DISTANCE(p,q)=\sum \limits _{i=1}^{n}{|p_{i}-q_{i}|}$

两个向量的维度必须相同。否则将返回错误信息。

例如:

```sql
[tidb]> select VEC_L1_DISTANCE('[0,0]', '[3,4]');
+-----------------------------------+
| VEC_L1_DISTANCE('[0,0]', '[3,4]') |
+-----------------------------------+
|                                 7 |
+-----------------------------------+
```

### VEC_DIMS

```sql
VEC_DIMS(vector)
```

返回向量的维度。

例如:

```sql
[tidb]> select VEC_DIMS('[1,2,3]');
+---------------------+
| VEC_DIMS('[1,2,3]') |
+---------------------+
|                   3 |
+---------------------+

[tidb]> select VEC_DIMS('[]');
+----------------+
| VEC_DIMS('[]') |
+----------------+
|              0 |
+----------------+
```

### VEC_L2_NORM

```sql
VEC_L2_NORM(vector)
```

使用以下公式计算向量的 L2 范数（欧几里得范数）：

$NORM(p)=\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}$

例如:

```sql
[tidb]> select VEC_L2_NORM('[3,4]');
+----------------------+
| VEC_L2_NORM('[3,4]') |
+----------------------+
|                    5 |
+----------------------+
```

### VEC_FROM_TEXT

```sql
VEC_FROM_TEXT(string)
```

将字符串转换为向量。

例如:

```sql
[tidb]> select VEC_FROM_TEXT('[1,2]') + VEC_FROM_TEXT('[3,4]');
+-------------------------------------------------+
| VEC_FROM_TEXT('[1,2]') + VEC_FROM_TEXT('[3,4]') |
+-------------------------------------------------+
| [4,6]                                           |
+-------------------------------------------------+
```

### VEC_AS_TEXT

```sql
VEC_AS_TEXT(vector)
```

将向量转换为字符串

例如:

```sql
[tidb]> select VEC_AS_TEXT('[1.000,   2.5]');
+-------------------------------+
| VEC_AS_TEXT('[1.000,   2.5]') |
+-------------------------------+
| [1,2.5]                       |
+-------------------------------+
```

## MySQL 兼容性

向量函数以及内置函数和向量数据类型运算符的扩展用法是 TiDB 特有的，MySQL 不支持。

## 参考

- [向量数据类型](/vector-search-data-types.md)