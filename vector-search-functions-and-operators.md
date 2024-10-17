---
title: 向量函数和操作符
summary: 本文介绍 TiDB 的向量相关函数和操作。
---

# 向量函数和操作符

本文介绍 TiDB 支持的向量函数和操作符。

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 向量函数

TiDB 为[向量数据类型](/vector-search-data-types.md)引入了以下向量函数：

**向量距离函数：**

| 函数名              |              描述          |
| --------------------------------------------------------- | ----------------------------------------------------------- |
| [`VEC_L2_DISTANCE`](#vec_l2_distance)             | 计算两个向量之间的 L2 距离 (欧氏距离)  |
| [`VEC_COSINE_DISTANCE`](#vec_cosine_distance)     | 计算两个向量之间的余弦距离               |
| [`VEC_NEGATIVE_INNER_PRODUCT`](#vec_negative_inner_product) | 计算两个向量内积的负数 |
| [`VEC_L1_DISTANCE`](#vec_l1_distance)             | 计算两个向量之间的 L1 距离 (曼哈顿距离)  |

**其他向量函数：**

| 函数名                   | 描述                                         |
| ------------------------------- | --------------------------------------------------- |
| [`VEC_DIMS`](#vec_dims)           | 计算向量的维度                   |
| [`VEC_L2_NORM`](#vec_l2_norm)     | 计算向量的 L2 范数 (欧氏规范) |
| [`VEC_FROM_TEXT`](#vec_from_text) | 将字符串类型转换为向量类型                  |
| [`VEC_AS_TEXT`](#vec_as_text)     | 将向量类型转换为字符串类型                     |

## 扩展的内置函数和运算符

TiDB 扩展了以下内置函数和运算符的功能，使其额外支持了[向量数据类型](/vector-search-data-types.md)。

**算术运算符：**

| 运算符                                    | 描述                              |
| :-------------------------------------------------------------------------------------- | :--------------------------------------- |
| [`+`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)  | 向量以元素为单位进行加法运算符    |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus) | 向量以元素为单位进行减法运算符 |

关于向量运算工作原理的更多信息，请参阅[向量数据类型的运算](/vector-search-data-types.md#运算)。

**聚合函数 (GROUP BY)：**

| 函数名                                   | 描述                                      |
| :--------------------------------- | :----------------------------------------------- |
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                  | 返回行数     |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct) | 返回不同值的行数 |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                      | 返回最大值                         |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                      | 返回最小值                  |

**比较函数与操作符：**

| 名称                                      | 描述                                           |
| ------------------------------------- | ----------------------------------------------------- |
| [`BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between)         | 检查值是否在某个取值范围内     |
| [`COALESCE()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce)                 | 获得第一个非 `NULL` 参数                    |
| [`=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal)                    | 相等比较符                       |
| [`<=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to)             | 安全的 `NULL` 相等比较符                           |
| [`>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than)         | 大于运算符                                 |
| [`>=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal)            | 大于或等于运算符                        |
| [`GREATEST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest)                 | 返回最大参数                           |
| [`IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in)                             | 检查值是否在一组数值之内       |
| [`IS NULL`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null)                     | 判断是否为 `NULL` 值                                       |
| [`ISNULL()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull)                     | 判断参数是否为 `NULL`                     |
| [`LEAST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least)                       | 返回最小参数                          |
| [`<`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than)                         | 小于运算符                                    |
| [`<=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal)               | 小于或等于运算符                           |
| [`NOT BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 检查值是否不在某个取值范围内 |
| [`!=`, `<>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal)                  | 不等运算符                                    |
| [`NOT IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in)                     | 检查值是否不在一组数值之内   |

关于如何比较向量的更多信息，请参阅[向量数据类型的比较](/vector-search-data-types.md#比较)。

**控制流程函数：**

| 函数名                                           | 描述                  |
| :--------------------------------------------- | :--------------------------- |
| [`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)       | Case 操作符                |
| [`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if)         | 构建 If/else            |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) | 构建 Null if/else       |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) | 如果 expr1 = expr2，返回 `NULL` |

**转换函数：**

| 函数名                                    | 描述                    |
| :----------------------------- | :----------------------------- |
| [`CAST()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast)       | 将值转换为字符串或向量类型 |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) | 将值转换为字符串类型 |

关于如何使用 `CAST()` 的更多信息，请参阅[向量数据类型的转换](/vector-search-data-types.md#类型转换-cast)。

## 使用示例

### VEC_L2_DISTANCE

```sql
VEC_L2_DISTANCE(vector1, vector2)
```

计算两个向量之间的 [L2 距离](https://zh.wikipedia.org/wiki/%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E8%B7%9D%E7%A6%BB) (欧式距离)，使用的公式为：

$DISTANCE(p,q)=\sqrt {\sum \limits _{i=1}^{n}{(p_{i}-q_{i})^{2}}}$

参与计算的两个向量的维度必须相同。当两个向量的维度不同时，TiDB 将返回错误信息。

示例：

```sql
[tidb]> SELECT VEC_L2_DISTANCE('[0,3]', '[4,0]');
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

计算两个向量之间的[余弦 (cosine)](https://zh.wikipedia.org/wiki/%E4%BD%99%E5%BC%A6%E7%9B%B8%E4%BC%BC%E6%80%A7) 距离，使用的公式为：

$DISTANCE(p,q)=1.0 - {\frac {\sum \limits _{i=1}^{n}{p_{i}q_{i}}}{{\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}}\cdot {\sqrt {\sum \limits _{i=1}^{n}{q_{i}^{2}}}}}}$

参与计算的两个向量的维度必须相同。当两个向量的维度不同时，TiDB 将返回错误信息。

示例：

```sql
[tidb]> SELECT VEC_COSINE_DISTANCE('[1, 1]', '[-1, -1]');
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

计算两个向量之间[内积](https://zh.wikipedia.org/wiki/%E7%82%B9%E7%A7%AF)的负值，使用的公式为：

$DISTANCE(p,q)=- INNER\_PROD(p,q)=-\sum \limits _{i=1}^{n}{p_{i}q_{i}}$

参与计算的两个向量的维度必须相同。当两个向量的维度不同时，TiDB 将返回错误信息。

示例：

```sql
[tidb]> SELECT VEC_NEGATIVE_INNER_PRODUCT('[1,2]', '[3,4]');
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

计算两个向量之间的 [L1 距离](https://zh.wikipedia.org/wiki/%E6%9B%BC%E5%93%88%E9%A0%93%E8%B7%9D%E9%9B%A2) (曼哈顿距离)，使用的公式为：

$DISTANCE(p,q)=\sum \limits _{i=1}^{n}{|p_{i}-q_{i}|}$

参与计算的两个向量的维度必须相同。当两个向量的维度不同时，TiDB 将返回错误信息。

示例：

```sql
[tidb]> SELECT VEC_L1_DISTANCE('[0,0]', '[3,4]');
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

示例：

```sql
[tidb]> SELECT VEC_DIMS('[1,2,3]');
+---------------------+
| VEC_DIMS('[1,2,3]') |
+---------------------+
|                   3 |
+---------------------+

[tidb]> SELECT VEC_DIMS('[]');
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

计算向量的 [L2 范数](https://zh.wikipedia.org/wiki/%E8%8C%83%E6%95%B0)（欧几里得范数），使用的公式为：

$NORM(p)=\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}$

示例：

```sql
[tidb]> SELECT VEC_L2_NORM('[3,4]');
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

将字符串类型转换为向量类型。

示例：

```sql
[tidb]> SELECT VEC_FROM_TEXT('[1,2]') + VEC_FROM_TEXT('[3,4]');
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

将向量类型转换为字符串类型。

示例：

```sql
[tidb]> SELECT VEC_AS_TEXT('[1.000,   2.5]');
+-------------------------------+
| VEC_AS_TEXT('[1.000,   2.5]') |
+-------------------------------+
| [1,2.5]                       |
+-------------------------------+
```

## MySQL 兼容性

向量函数、有关向量的内置函数和向量数据类型运算符只在 TiDB 中支持，MySQL 不支持。

## 另请参阅

- [向量数据类型](/vector-search-data-types.md)