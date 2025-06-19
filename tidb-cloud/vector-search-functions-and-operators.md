---
title: 向量函数和运算符
summary: 了解向量数据类型可用的函数和运算符。
---

# 向量函数和运算符

本文档列出了向量数据类型可用的函数和运算符。

> **注意**
>
> TiDB 向量搜索功能仅适用于 TiDB 自管理版本（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。该功能不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

## 向量函数

以下函数专门为[向量数据类型](/tidb-cloud/vector-search-data-types.md)设计。

**向量距离函数：**

| 函数名                                                      | 描述                                |
| ----------------------------------------------------------- | ---------------------------------- |
| [`VEC_L2_DISTANCE`](#vec_l2_distance)                       | 计算两个向量之间的 L2 距离（欧几里得距离） |
| [`VEC_COSINE_DISTANCE`](#vec_cosine_distance)               | 计算两个向量之间的余弦距离              |
| [`VEC_NEGATIVE_INNER_PRODUCT`](#vec_negative_inner_product) | 计算两个向量之间内积的负值              |
| [`VEC_L1_DISTANCE`](#vec_l1_distance)                       | 计算两个向量之间的 L1 距离（曼哈顿距离） |

**其他向量函数：**

| 函数名                           | 描述                           |
| --------------------------------- | ----------------------------- |
| [`VEC_DIMS`](#vec_dims)           | 返回向量的维度                  |
| [`VEC_L2_NORM`](#vec_l2_norm)     | 计算向量的 L2 范数（欧几里得范数） |
| [`VEC_FROM_TEXT`](#vec_from_text) | 将字符串转换为向量               |
| [`VEC_AS_TEXT`](#vec_as_text)     | 将向量转换为字符串               |

## 扩展内置函数和运算符

以下内置函数和运算符已扩展以支持[向量数据类型](/tidb-cloud/vector-search-data-types.md)的操作。

**算术运算符：**

| 名称                                                                                    | 描述                    |
| :-------------------------------------------------------------------------------------- | :-------------------- |
| [`+`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)  | 向量元素逐个相加运算符      |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus) | 向量元素逐个相减运算符      |

有关向量算术运算的更多信息，请参见[向量数据类型 | 算术运算](/tidb-cloud/vector-search-data-types.md#arithmetic)。

**聚合（GROUP BY）函数：**

| 名称                                                                                                          | 描述                    |
| :------------------------------------------------------------------------------------------------------------ | :-------------------- |
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                  | 返回返回行数的计数        |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct) | 返回不同值的计数         |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                      | 返回最大值             |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                      | 返回最小值             |

**比较函数和运算符：**

| 名称                                                                                                                | 描述                         |
| ------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| [`BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between)         | 检查值是否在某个范围内          |
| [`COALESCE()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce)                 | 返回第一个非 NULL 参数         |
| [`=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal)                             | 等于运算符                    |
| [`<=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to)                        | NULL 安全的等于运算符          |
| [`>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than)                      | 大于运算符                    |
| [`>=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal)            | 大于等于运算符                |
| [`GREATEST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest)                 | 返回最大参数                  |
| [`IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in)                             | 检查值是否在一组值中           |
| [`IS NULL`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null)                     | 测试值是否为 `NULL`           |
| [`ISNULL()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull)                     | 测试参数是否为 `NULL`         |
| [`LEAST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least)                       | 返回最小参数                  |
| [`<`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than)                         | 小于运算符                    |
| [`<=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal)               | 小于等于运算符                |
| [`NOT BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 检查值是否不在某个范围内        |
| [`!=`, `<>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal)                  | 不等于运算符                  |
| [`NOT IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in)                     | 检查值是否不在一组值中         |

有关向量比较的更多信息，请参见[向量数据类型 | 比较](/tidb-cloud/vector-search-data-types.md#comparison)。

**流程控制函数：**

| 名称                                                                                              | 描述                         |
| :------------------------------------------------------------------------------------------------ | :-------------------------- |
| [`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)       | Case 运算符                  |
| [`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if)         | If/else 结构                |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) | Null if/else 结构           |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) | 如果 expr1 = expr2 则返回 NULL |

**类型转换函数：**

| 名称                                                                                        | 描述                      |
| :------------------------------------------------------------------------------------------ | :----------------------- |
| [`CAST()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast)       | 将值转换为字符串或向量       |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) | 将值转换为字符串           |

有关如何使用 `CAST()` 的更多信息，请参见[向量数据类型 | 类型转换](/tidb-cloud/vector-search-data-types.md#cast)。

## 完整参考

### VEC_L2_DISTANCE

```sql
VEC_L2_DISTANCE(vector1, vector2)
```

使用以下公式计算两个向量之间的 [L2 距离](https://en.wikipedia.org/wiki/Euclidean_distance)（欧几里得距离）：

$DISTANCE(p,q)=\sqrt {\sum \limits _{i=1}^{n}{(p_{i}-q_{i})^{2}}}$

两个向量必须具有相同的维度。否则，将返回错误。

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

使用以下公式计算两个向量之间的[余弦距离](https://en.wikipedia.org/wiki/Cosine_similarity)：

$DISTANCE(p,q)=1.0 - {\frac {\sum \limits _{i=1}^{n}{p_{i}q_{i}}}{{\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}}\cdot {\sqrt {\sum \limits _{i=1}^{n}{q_{i}^{2}}}}}}$

两个向量必须具有相同的维度。否则，将返回错误。

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

使用以下公式计算两个向量之间[内积](https://en.wikipedia.org/wiki/Dot_product)的负值作为距离：

$DISTANCE(p,q)=- INNER\_PROD(p,q)=-\sum \limits _{i=1}^{n}{p_{i}q_{i}}$

两个向量必须具有相同的维度。否则，将返回错误。

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

使用以下公式计算两个向量之间的 [L1 距离](https://en.wikipedia.org/wiki/Taxicab_geometry)（曼哈顿距离）：

$DISTANCE(p,q)=\sum \limits _{i=1}^{n}{|p_{i}-q_{i}|}$

两个向量必须具有相同的维度。否则，将返回错误。

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

使用以下公式计算向量的 [L2 范数](<https://en.wikipedia.org/wiki/Norm_(mathematics)>)（欧几里得范数）：

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

将字符串转换为向量。

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

将向量转换为字符串。

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

向量函数以及内置函数和运算符在向量数据类型上的扩展用法是 TiDB 特有的，MySQL 中不支持这些功能。

## 另请参阅

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
