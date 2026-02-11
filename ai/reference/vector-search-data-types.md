---
title: 向量数据类型
summary: 了解 TiDB 中的向量数据类型。
aliases: ['/zh/tidb/stable/vector-search-data-types/','/zh/tidb/dev/vector-search-data-types/','/zh/tidbcloud/vector-search-data-types/']
---

# 向量数据类型

向量是一组浮点数序列，例如 `[0.3, 0.5, -0.1, ...]`。TiDB 提供了向量数据类型，专门针对高效存储和查询在 AI 应用中广泛使用的向量嵌入进行了优化。

> **注意：**
>
> - 向量数据类型目前为 Beta 版本，可能会在未提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量数据类型适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

目前支持以下向量数据类型：

- `VECTOR`：任意维度的单精度浮点数序列。
- `VECTOR(D)`：固定维度 `D` 的单精度浮点数序列。

与使用 [`JSON`](/data-type-json.md) 类型相比，使用向量数据类型具有以下优势：

- 支持向量索引：你可以构建 [向量搜索索引](/ai/reference/vector-search-index.md) 来加速向量搜索。
- 维度约束：你可以指定维度，禁止插入不同维度的向量。
- 优化的存储格式：向量数据类型针对向量数据进行了优化，空间效率和性能优于 `JSON` 类型。

## 语法

你可以使用如下语法的字符串来表示一个向量值：

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

插入语法不合法的向量值会报错：

```sql
[tidb]> INSERT INTO vector_table VALUES (3, '[5, ]');
ERROR 1105 (HY000): Invalid vector text: [5, ]
```

在下例中，由于在建表时为 `embedding` 列指定了维度 `3`，插入不同维度的向量会报错：

```sql
[tidb]> INSERT INTO vector_table VALUES (4, '[0.3, 0.5]');
ERROR 1105 (HY000): vector has 2 dimensions, does not fit VECTOR(3)
```

关于向量数据类型可用的函数和运算符，参见 [向量函数与运算符](/ai/reference/vector-search-functions-and-operators.md)。

关于如何构建和使用向量搜索索引，参见 [向量搜索索引](/ai/reference/vector-search-index.md)。

## 存储不同维度的向量

你可以通过在 `VECTOR` 类型中省略维度参数，在同一列中存储不同维度的向量：

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]'); -- 3 维向量，OK
INSERT INTO vector_table VALUES (2, '[0.3, 0.5]');       -- 2 维向量，OK
```

但需要注意的是，你无法为该列构建 [向量搜索索引](/ai/reference/vector-search-index.md)，因为只有相同维度的向量之间才能计算向量距离。

## 比较

你可以使用 [比较运算符](/functions-and-operators/operators.md)（如 `=`, `!=`, `<`, `>`, `<=`, `>=`）对向量数据类型进行比较。关于向量数据类型的完整比较运算符和函数列表，参见 [向量函数与运算符](/ai/reference/vector-search-functions-and-operators.md)。

向量数据类型按元素逐一进行数值比较。例如：

- `[1] < [12]`
- `[1,2,3] < [1,2,5]`
- `[1,2,3] = [1,2,3]`
- `[2,2,3] > [1,2,3]`

对于不同维度的两个向量，采用字典序比较，规则如下：

- 两个向量从头开始逐元素比较，每个元素按数值比较。
- 第一个不相等的元素决定哪个向量在字典序上 _更小_ 或 _更大_。
- 如果一个向量是另一个向量的前缀，则较短的向量在字典序上 _更小_。例如，`[1,2,3] < [1,2,3,0]`。
- 长度相同且元素完全相同的两个向量在字典序上 _相等_。
- 空向量在字典序上 _小于_ 任何非空向量。例如，`[] < [1]`。
- 两个空向量在字典序上 _相等_。

在比较向量常量时，建议进行 [显式类型转换](#cast)，将字符串转换为向量，以避免基于字符串值的比较：

```sql
-- 由于传入的是字符串，TiDB 按字符串比较：
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- 显式转换为向量后按向量比较：
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

## 算术运算

向量数据类型支持 `+`（加法）和 `-`（减法）算术运算。但不同维度的向量之间不支持算术运算，否则会报错。

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

## 类型转换

### 向量 ⇔ 字符串 的类型转换

要在向量和字符串之间进行类型转换，可以使用以下函数：

- `CAST(... AS VECTOR)`：字符串 ⇒ 向量
- `CAST(... AS CHAR)`：向量 ⇒ 字符串
- `VEC_FROM_TEXT`：字符串 ⇒ 向量
- `VEC_AS_TEXT`：向量 ⇒ 字符串

为提升易用性，如果你调用的函数只支持向量数据类型（如向量相关性距离函数），也可以直接传入符合格式的字符串。此时 TiDB 会自动进行隐式类型转换。

```sql
-- VEC_DIMS 函数只接受 VECTOR 参数，因此可以直接传入字符串进行隐式转换。
[tidb]> SELECT VEC_DIMS('[0.3, 0.5, -0.1]');
+------------------------------+
| VEC_DIMS('[0.3, 0.5, -0.1]') |
+------------------------------+
|                            3 |
+------------------------------+
1 row in set (0.01 sec)

-- 你也可以先用 VEC_FROM_TEXT 显式将字符串转换为向量，再传递给 VEC_DIMS 函数。
[tidb]> SELECT VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]'));
+---------------------------------------------+
| VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]')) |
+---------------------------------------------+
|                                           3 |
+---------------------------------------------+
1 row in set (0.01 sec)

-- 也可以用 CAST(... AS VECTOR) 显式转换：
[tidb]> SELECT VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR));
+----------------------------------------------+
| VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR)) |
+----------------------------------------------+
|                                            3 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

当你使用接受多种数据类型的运算符或函数时，需要在将字符串传递给该运算符或函数前，显式将字符串类型转换为向量类型，因为此时 TiDB 不会进行隐式类型转换。例如，在进行比较运算前，需要显式将字符串转换为向量，否则 TiDB 会按字符串值进行比较，而不是按向量数值进行比较：

```sql
-- 由于传入的是字符串，TiDB 按字符串比较：
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- 显式转换为向量后按向量比较：
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

你也可以将向量显式转换为其字符串表示。例如，使用 `VEC_AS_TEXT()` 函数：

```sql
-- 字符串首先被隐式转换为向量，然后向量被显式转换为字符串，因此返回标准化格式的字符串：
[tidb]> SELECT VEC_AS_TEXT('[0.3,     0.5,  -0.1]');
+--------------------------------------+
| VEC_AS_TEXT('[0.3,     0.5,  -0.1]') |
+--------------------------------------+
| [0.3,0.5,-0.1]                       |
+--------------------------------------+
1 row in set (0.01 sec)
```

更多类型转换函数，参见 [向量函数与运算符](/ai/reference/vector-search-functions-and-operators.md)。

### 向量 ⇔ 其他数据类型的类型转换

目前不支持向量与其他数据类型（如 `JSON`）之间的直接类型转换。你可以在 SQL 语句中通过字符串作为中间类型进行转换来规避此限制。

需要注意的是，表中存储的向量数据类型列，无法通过 `ALTER TABLE ... MODIFY COLUMN ...` 转换为其他数据类型。

## 限制

关于向量数据类型的限制，参见 [向量搜索限制](/ai/reference/vector-search-limitations.md) 和 [向量索引限制](/ai/reference/vector-search-index.md#restrictions)。

## MySQL 兼容性

向量数据类型为 TiDB 特有，MySQL 不支持。

## 另请参阅

- [向量函数与运算符](/ai/reference/vector-search-functions-and-operators.md)
- [向量搜索索引](/ai/reference/vector-search-index.md)
- [提升向量搜索性能](/ai/reference/vector-search-improve-performance.md)
