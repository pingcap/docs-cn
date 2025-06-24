---
title: 向量数据类型
summary: 了解 TiDB 中的向量数据类型。
---

# 向量数据类型

向量是一个浮点数序列，例如 `[0.3, 0.5, -0.1, ...]`。TiDB 提供了向量数据类型，专门针对在 AI 应用中广泛使用的向量嵌入进行了存储和查询优化。

目前提供以下向量数据类型：

- `VECTOR`：任意维度的单精度浮点数序列。
- `VECTOR(D)`：固定维度 `D` 的单精度浮点数序列。

使用向量数据类型相比使用 [`JSON`](/data-type-json.md) 类型有以下优势：

- 支持向量索引：你可以构建[向量搜索索引](/tidb-cloud/vector-search-index.md)来加速向量搜索。
- 维度限制：你可以指定维度以禁止插入不同维度的向量。
- 优化的存储格式：向量数据类型针对处理向量数据进行了优化，与 `JSON` 类型相比提供更好的空间效率和性能。

> **注意**
>
> TiDB 向量搜索仅适用于 TiDB 自建集群（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

## 语法

你可以使用以下语法的字符串来表示向量值：

```sql
'[<float>, <float>, ...]'
```

示例：

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR(3)
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]');

INSERT INTO vector_table VALUES (2, NULL);
```

插入语法无效的向量值将导致错误：

```sql
[tidb]> INSERT INTO vector_table VALUES (3, '[5, ]');
ERROR 1105 (HY000): Invalid vector text: [5, ]
```

在以下示例中，由于在创建表时为 `embedding` 列强制指定了维度 `3`，插入不同维度的向量将导致错误：

```sql
[tidb]> INSERT INTO vector_table VALUES (4, '[0.3, 0.5]');
ERROR 1105 (HY000): vector has 2 dimensions, does not fit VECTOR(3)
```

有关向量数据类型的可用函数和运算符，请参见[向量函数和运算符](/tidb-cloud/vector-search-functions-and-operators.md)。

有关构建和使用向量搜索索引的更多信息，请参见[向量搜索索引](/tidb-cloud/vector-search-index.md)。

## 存储不同维度的向量

你可以通过省略 `VECTOR` 类型的维度参数，在同一列中存储不同维度的向量：

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]'); -- 3 维向量，正确
INSERT INTO vector_table VALUES (2, '[0.3, 0.5]');       -- 2 维向量，正确
```

但是请注意，你不能为此列构建[向量搜索索引](/tidb-cloud/vector-search-index.md)，因为向量距离只能在相同维度的向量之间计算。

## 比较

你可以使用[比较运算符](/functions-and-operators/operators.md)（如 `=`、`!=`、`<`、`>`、`<=` 和 `>=`）来比较向量数据类型。有关向量数据类型的完整比较运算符和函数列表，请参见[向量函数和运算符](/tidb-cloud/vector-search-functions-and-operators.md)。

向量数据类型按元素进行数值比较。例如：

- `[1] < [12]`
- `[1,2,3] < [1,2,5]`
- `[1,2,3] = [1,2,3]`
- `[2,2,3] > [1,2,3]`

不同维度的向量使用字典序比较，规则如下：

- 两个向量从开始按元素逐个比较，每个元素进行数值比较。
- 第一个不匹配的元素决定哪个向量在字典序上_小于_或_大于_另一个。
- 如果一个向量是另一个向量的前缀，则较短的向量在字典序上_小于_另一个。例如，`[1,2,3] < [1,2,3,0]`。
- 长度相同且元素相同的向量在字典序上_相等_。
- 空向量在字典序上_小于_任何非空向量。例如，`[] < [1]`。
- 两个空向量在字典序上_相等_。

在比较向量常量时，考虑执行从字符串到向量的[显式转换](#转换)，以避免基于字符串值的比较：

```sql
-- 因为给定的是字符串，TiDB 正在比较字符串：
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- 显式转换为向量以按向量比较：
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

## 算术运算

向量数据类型支持算术运算 `+`（加法）和 `-`（减法）。但是，不支持不同维度向量之间的算术运算，这将导致错误。

示例：

```sql
[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]');
+---------------------------------------------+
| VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]') |
+---------------------------------------------+
| [9]                                         |
+---------------------------------------------+
1 row in set (0.01 sec)

[tidb]> SELECT VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]');
+-----------------------------------------------------+
| VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]') |
+-----------------------------------------------------+
| [1,1,1]                                             |
+-----------------------------------------------------+
1 row in set (0.01 sec)

[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[1,2,3]');
ERROR 1105 (HY000): vectors have different dimensions: 1 and 3
```

## 转换

### 在向量 ⇔ 字符串之间转换

要在向量和字符串之间进行转换，使用以下函数：

- `CAST(... AS VECTOR)`：字符串 ⇒ 向量
- `CAST(... AS CHAR)`：向量 ⇒ 字符串
- `VEC_FROM_TEXT`：字符串 ⇒ 向量
- `VEC_AS_TEXT`：向量 ⇒ 字符串

为了提高可用性，如果你调用仅支持向量数据类型的函数（如向量相关距离函数），你也可以直接传入格式合规的字符串。在这种情况下，TiDB 会自动执行隐式转换。

```sql
-- VEC_DIMS 函数只接受 VECTOR 参数，所以你可以直接传入字符串进行隐式转换。
[tidb]> SELECT VEC_DIMS('[0.3, 0.5, -0.1]');
+------------------------------+
| VEC_DIMS('[0.3, 0.5, -0.1]') |
+------------------------------+
|                            3 |
+------------------------------+
1 row in set (0.01 sec)

-- 你也可以使用 VEC_FROM_TEXT 显式将字符串转换为向量，然后将向量传递给 VEC_DIMS 函数。
[tidb]> SELECT VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]'));
+---------------------------------------------+
| VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]')) |
+---------------------------------------------+
|                                           3 |
+---------------------------------------------+
1 row in set (0.01 sec)

-- 你也可以使用 CAST(... AS VECTOR) 显式转换：
[tidb]> SELECT VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR));
+----------------------------------------------+
| VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR)) |
+----------------------------------------------+
|                                            3 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

当使用接受多种数据类型的运算符或函数时，你需要在将字符串传递给该运算符或函数之前显式将字符串类型转换为向量类型，因为在这种情况下 TiDB 不执行隐式转换。例如，在执行比较操作之前，你需要显式将字符串转换为向量；否则，TiDB 会将它们作为字符串值而不是向量数值进行比较：

```sql
-- 因为给定的是字符串，TiDB 正在比较字符串：
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- 显式转换为向量以按向量比较：
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

你也可以显式将向量转换为其字符串表示。以使用 `VEC_AS_TEXT()` 函数为例：

```sql
-- 字符串首先被隐式转换为向量，然后向量被显式转换为字符串，因此返回规范格式的字符串：
[tidb]> SELECT VEC_AS_TEXT('[0.3,     0.5,  -0.1]');
+--------------------------------------+
| VEC_AS_TEXT('[0.3,     0.5,  -0.1]') |
+--------------------------------------+
| [0.3,0.5,-0.1]                       |
+--------------------------------------+
1 row in set (0.01 sec)
```

有关其他转换函数，请参见[向量函数和运算符](/tidb-cloud/vector-search-functions-and-operators.md)。

### 在向量 ⇔ 其他数据类型之间转换

目前，不支持向量与其他数据类型（如 `JSON`）之间的直接转换。要解决此限制，请在 SQL 语句中使用字符串作为中间数据类型进行转换。

请注意，使用 `ALTER TABLE ... MODIFY COLUMN ...` 无法将表中存储的向量数据类型列转换为其他数据类型。

## 限制

请参见[向量数据类型限制](/tidb-cloud/vector-search-limitations.md#vector-data-type-limitations)。

## MySQL 兼容性

向量数据类型是 TiDB 特有的，MySQL 不支持。

## 另请参阅

- [向量函数和运算符](/tidb-cloud/vector-search-functions-and-operators.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)
- [提高向量搜索性能](/tidb-cloud/vector-search-improve-performance.md)
