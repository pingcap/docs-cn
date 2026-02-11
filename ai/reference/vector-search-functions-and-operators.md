---
title: 向量函数与运算符
summary: 了解可用于向量数据类型的函数与运算符。
aliases: ['/zh/tidb/stable/vector-search-functions-and-operators/','/zh/tidb/dev/vector-search-functions-and-operators/','/zh/tidbcloud/vector-search-functions-and-operators/']
---

# 向量函数与运算符

本文档列出了可用于向量数据类型的函数与运算符。

> **注意：**
>
> - 向量函数与运算符目前为 Beta 版本，可能会在未提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量数据类型及这些向量函数适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

## 向量函数

以下函数专为 [向量数据类型](/ai/reference/vector-search-data-types.md) 设计。

**向量距离函数：**

| 函数名                                               | 描述                                                      | [向量索引](/ai/reference/vector-search-index.md)支持 |
| ---------------------------------------------------- | --------------------------------------------------------- |---------------------------|
| [`VEC_L2_DISTANCE`](#vec_l2_distance)                | 计算两个向量之间的 L2 距离（欧氏距离）                    | 是                       |
| [`VEC_COSINE_DISTANCE`](#vec_cosine_distance)        | 计算两个向量之间的余弦距离                                | 是                       |
| [`VEC_NEGATIVE_INNER_PRODUCT`](#vec_negative_inner_product) | 计算两个向量内积的相反数                                 | 否                       |
| [`VEC_L1_DISTANCE`](#vec_l1_distance)                | 计算两个向量之间的 L1 距离（曼哈顿距离）                  | 否                       |

**其他向量函数：**

| 函数名                        | 描述                                         |
| ----------------------------- | -------------------------------------------- |
| [`VEC_DIMS`](#vec_dims)           | 返回向量的维度                              |
| [`VEC_L2_NORM`](#vec_l2_norm)     | 计算向量的 L2 范数（欧氏范数）              |
| [`VEC_FROM_TEXT`](#vec_from_text) | 将字符串转换为向量                          |
| [`VEC_AS_TEXT`](#vec_as_text)     | 将向量转换为字符串                          |

## 扩展内置函数与运算符

以下内置函数与运算符已扩展以支持对 [向量数据类型](/ai/reference/vector-search-data-types.md) 的操作。

**算术运算符：**

| 名称                                                                                   | 描述                              |
| :------------------------------------------------------------------------------------- | :------------------------------- |
| [`+`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)  | 向量按元素加法运算符              |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus) | 向量按元素减法运算符              |

关于向量算术运算的更多信息，参见 [向量数据类型 | 算术运算](/ai/reference/vector-search-data-types.md#arithmetic)。

**聚合（GROUP BY）函数：**

| 名称                              | 描述                                      |
| :----------------------- | :---------------------------------------- |
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                  | 返回结果行数                             |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct) | 返回不同值的数量                         |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                      | 返回最大值                               |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                      | 返回最小值                               |

**比较函数与运算符：**

| 名称                                  | 描述                                           |
| ---------------------------------------- | ---------------------------------------------- |
| [`BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between)         | 检查值是否在某个范围内                        |
| [`COALESCE()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce)                 | 返回第一个非空值参数                          |
| [`=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal)                             | 等于运算符                                    |
| [`<=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to)                        | NULL 安全等于运算符                           |
| [`>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than)                      | 大于运算符                                    |
| [`>=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal)            | 大于等于运算符                                |
| [`GREATEST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest)                 | 返回最大参数                                  |
| [`IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in)                             | 检查值是否在某个集合中                        |
| [`IS NULL`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null)                     | 测试值是否为 `NULL`                           |
| [`ISNULL()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull)                     | 测试参数是否为 `NULL`                         |
| [`LEAST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least)                       | 返回最小参数                                  |
| [`<`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than)                         | 小于运算符                                    |
| [`<=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal)               | 小于等于运算符                                |
| [`NOT BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 检查值是否不在某个范围内                      |
| [`!=`, `<>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal)                  | 不等于运算符                                  |
| [`NOT IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in)                     | 检查值是否不在某个集合中                      |

关于向量比较的更多信息，参见 [向量数据类型 | 比较](/ai/reference/vector-search-data-types.md#comparison)。

**流程控制函数：**

| 名称                                                                                              | 描述                  |
| :------------------------------------------------------------------------------------------------ | :-------------------- |
| [`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)       | CASE 运算符           |
| [`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if)         | if/else 结构          |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) | null if/else 结构     |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) | 如果 expr1 = expr2 则返回 `NULL` |

**类型转换函数：**

| 名称                                                                                        | 描述                        |
| :------------------------------------------------------------------------------------------ | :-------------------------- |
| [`CAST()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast)       | 将值转换为字符串或向量      |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) | 将值转换为字符串            |

关于如何使用 `CAST()` 的更多信息，参见 [向量数据类型 | 类型转换](/ai/reference/vector-search-data-types.md#cast)。

## 完整参考

### VEC_L2_DISTANCE

```sql
VEC_L2_DISTANCE(vector1, vector2)
```

使用以下公式计算两个向量之间的 [L2 距离](https://en.wikipedia.org/wiki/Euclidean_distance)（欧氏距离）：

$DISTANCE(p,q)=\sqrt {\sum \limits _{i=1}^{n}{(p_{i}-q_{i})^{2}}}$

两个向量必须具有相同的维度，否则会返回错误。

示例：

```sql
SELECT VEC_L2_DISTANCE('[0, 3]', '[4, 0]');
```

```
+-------------------------------------+
| VEC_L2_DISTANCE('[0, 3]', '[4, 0]') |
+-------------------------------------+
|                                   5 |
+-------------------------------------+
```

### VEC_COSINE_DISTANCE

```sql
VEC_COSINE_DISTANCE(vector1, vector2)
```

使用以下公式计算两个向量之间的 [余弦距离](https://en.wikipedia.org/wiki/Cosine_similarity)：

$DISTANCE(p,q)=1.0 - {\frac {\sum \limits _{i=1}^{n}{p_{i}q_{i}}}{{\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}}\cdot {\sqrt {\sum \limits _{i=1}^{n}{q_{i}^{2}}}}}}$

两个向量必须具有相同的维度，否则会返回错误。

对于来自 OpenAI 的 embedding，[推荐](https://help.openai.com/en/articles/6824809-embeddings-faq)使用此函数。

示例：

```sql
SELECT VEC_COSINE_DISTANCE('[1, 1]', '[-1, -1]');
```

```
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

使用以下公式，通过计算两个向量 [内积](https://en.wikipedia.org/wiki/Dot_product) 的相反数来计算距离：

$DISTANCE(p,q)=- INNER\_PROD(p,q)=-\sum \limits _{i=1}^{n}{p_{i}q_{i}}$

两个向量必须具有相同的维度，否则会返回错误。

示例：

```sql
SELECT VEC_NEGATIVE_INNER_PRODUCT('[1, 2]', '[3, 4]');
```

```
+------------------------------------------------+
| VEC_NEGATIVE_INNER_PRODUCT('[1, 2]', '[3, 4]') |
+------------------------------------------------+
|                                            -11 |
+------------------------------------------------+
```

### VEC_L1_DISTANCE

```sql
VEC_L1_DISTANCE(vector1, vector2)
```

使用以下公式计算两个向量之间的 [L1 距离](https://en.wikipedia.org/wiki/Taxicab_geometry)（曼哈顿距离）：

$DISTANCE(p,q)=\sum \limits _{i=1}^{n}{|p_{i}-q_{i}|}$

两个向量必须具有相同的维度，否则会返回错误。

示例：

```sql
SELECT VEC_L1_DISTANCE('[0, 0]', '[3, 4]');
```

```
+-------------------------------------+
| VEC_L1_DISTANCE('[0, 0]', '[3, 4]') |
+-------------------------------------+
|                                   7 |
+-------------------------------------+
```

### VEC_DIMS

```sql
VEC_DIMS(vector)
```

返回向量的维度。

示例：

```sql
SELECT VEC_DIMS('[1, 2, 3]');
```

```
+-----------------------+
| VEC_DIMS('[1, 2, 3]') |
+-----------------------+
|                     3 |
+-----------------------+
```

```sql
SELECT VEC_DIMS('[]');
```

```
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

使用以下公式计算向量的 [L2 范数](https://en.wikipedia.org/wiki/Norm_(mathematics))（欧氏范数）：

$NORM(p)=\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}$

示例：

```sql
SELECT VEC_L2_NORM('[3, 4]');
```

```
+-----------------------+
| VEC_L2_NORM('[3, 4]') |
+-----------------------+
|                     5 |
+-----------------------+
```

### VEC_FROM_TEXT

```sql
VEC_FROM_TEXT(string)
```

将字符串转换为向量。在许多场景下，此转换会被隐式执行，例如向 `VECTOR` 数据类型的列插入数据时。然而，在某些不支持隐式转换的表达式中（如向量的算术运算），你需要显式调用此函数。

示例：

```sql
SELECT VEC_FROM_TEXT('[1, 2]') + VEC_FROM_TEXT('[3, 4]');
```

```
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
SELECT VEC_AS_TEXT('[1.000, 2.5]');
```

```
+-----------------------------+
| VEC_AS_TEXT('[1.000, 2.5]') |
+-----------------------------+
| [1,2.5]                     |
+-----------------------------+
```

## MySQL 兼容性

向量函数以及内置函数和运算符在向量数据类型上的扩展用法为 TiDB 特有，MySQL 不支持。

## 另请参阅

- [向量数据类型](/ai/reference/vector-search-data-types.md)
