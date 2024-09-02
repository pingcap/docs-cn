---
title: 向量数据类型
summary: 本文介绍 TiDB 的向量数据类型。
---

# 向量数据类型(Vector)

TiDB 提供的矢量数据类型专门针对AI向量嵌入用例进行了优化。通过使用向量数据类型，可以高效地存储和查询浮点数序列，例如 `[0.3, 0.5, -0.1, ...]`.

目前可用的向量数据类型如下：

- `VECTOR`: 单精度浮点数序列。每一行的维度可以不同。
- `VECTOR(D)`: 具有固定维度 `D` 的单精度浮点数序列。

与存储在`JSON`列中相比，向量数据类型具有这些优势：

- 支持向量索引。 可以通过构建[向量搜索索引]()加速查询。
- 指定维度。可以指定一个维度，禁止插入不同维度的向量。
- 优化存储格式。向量数据类型的存储空间效率甚至比`JSON`数据类型更高。

## Value syntax

向量值包含任意数量的浮点数，可以使用以下语法中的字符串来表示向量值：

```sql
'[<float>, <float>, ...]'
```

例如:

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

在上例中，`embedding`列的维度为 3，因此插入不同维度的向量会导致错误：

```sql
[tidb]> INSERT INTO vector_table VALUES (4, '[0.3, 0.5]');
ERROR 1105 (HY000): vector has 2 dimensions, does not fit VECTOR(3)
```

有关向量数据类型的可用函数和操作，参阅[向量函数与操作](/vector-search-functions-and-operators.md)

有关向量搜索索引的信息，参阅[向量搜索索引](/vector-search-index.md)

## 不同维度的向量

通过省略 `VECTOR` 类型中的维度参数，可以在同一列中存储不同维度的向量：

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]'); -- 3 dimensions vector, OK
INSERT INTO vector_table VALUES (2, '[0.3, 0.5]');       -- 2 dimensions vector, OK
```

但是，我们不能为此列构建[向量搜索索引](/vector-search-index.md)，因为向量距离只能在具有相同维度的向量之间计算。

## 对比

我们可以使用[比较运算符](/vector-search-functions-and-operators.md)来比较两个向量，如：`=`, `!=`, `<`, `>`, `<=`, and `>=`。有关向量数据类型的比较运算符和函数的完整列表，参阅[向量函数与操作](/vector-search-functions-and-operators.md)。

向量数据类型以元素为单位进行比较，例如：

- `[1] < [12]`
- `[1,2,3] < [1,2,5]`
- `[1,2,3] = [1,2,3]`
- `[2,2,3] > [1,2,3]`

不同维度的向量采用字典序比较，具有一下特性：

- 两个矢量逐个元素进行比较，每个元素都以数值形式进行比较。
- 第一个不匹配的元素决定哪一个向量在字典序上 _less_ 或 _greater_。
- 如果一个向量是另一个向量的前缀，那么较短的向量为 _less_ 。
- 长度相同、元素相同的两个向量为 _equal_ 。
- 空向量是小于任何非空向量。
- 两个空向量为 _equal_ 。

例如:

- `[] < [1]`
- `[1,2,3] < [1,2,3,0]`

在比较向量常量时，需要考虑执行从字符串到向量的 [显式转换](#cast)，以避免基于字符串值的比较：

```sql
-- Because string is given, TiDB is comparing strings:
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- Cast to vector explicitly to compare by vectors:
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

## 运算

向量数据类型支持以元素为单位的算术运算 `+` 和 `-` 。但是，在不同维度的向量之间执行算术运算会导致错误。

例如:

```sql
[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]');
+---------------------------------------------+
| VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]') |
+---------------------------------------------+
| [9]                                         |
+---------------------------------------------+
1 row in set (0.01 sec)

mysql> SELECT VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]');
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

### 向量与字符串之间的转换

向量和字符串之间进行转换，可以使用以下函数：

- `CAST(... AS VECTOR)`: String ⇒ Vector
- `CAST(... AS CHAR)`: Vector ⇒ String
- `VEC_FROM_TEXT`: String ⇒ Vector
- `VEC_AS_TEXT`: Vector ⇒ String

在调用接收向量数据类型的函数时，存在隐式转换：

```sql
-- There is an implicit cast here, since VEC_DIMS only accepts VECTOR arguments:
[tidb]> SELECT VEC_DIMS('[0.3, 0.5, -0.1]');
+------------------------------+
| VEC_DIMS('[0.3, 0.5, -0.1]') |
+------------------------------+
|                            3 |
+------------------------------+
1 row in set (0.01 sec)

-- Cast explicitly using VEC_FROM_TEXT:
[tidb]> SELECT VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]'));
+---------------------------------------------+
| VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]')) |
+---------------------------------------------+
|                                           3 |
+---------------------------------------------+
1 row in set (0.01 sec)

-- Cast explicitly using CAST(... AS VECTOR):
[tidb]> SELECT VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR));
+----------------------------------------------+
| VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR)) |
+----------------------------------------------+
|                                            3 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

当运算符或函数接受多种数据类型时，请使用显式转换。例如，在比较中，使用显式转换来比较向量数值而不是字符串数值：

```sql
-- Because string is given, TiDB is comparing strings:
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- Cast to vector explicitly to compare by vectors:
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

要显式地将向量转换为字符串表示，请使用`VEC_AS_TEXT()`函数：

```sql
-- String representation is normalized:
[tidb]> SELECT VEC_AS_TEXT('[0.3,     0.5,  -0.1]');
+--------------------------------------+
| VEC_AS_TEXT('[0.3,     0.5,  -0.1]') |
+--------------------------------------+
| [0.3,0.5,-0.1]                       |
+--------------------------------------+
1 row in set (0.01 sec)
```

有关其他转换函数，请参阅 [向量函数和操作](/vector-search-functions-and-operators.md)。

### 向量与其他数据类型之间的转换

目前无法直接在向量和其他数据类型（如 `JSON`）之间进行转换。您需要使用字符串作为中间类型。

## 约束

- 支持的最大向量维数为 16383。
- 不能在向量数据类型中存储 `NaN`、`Infinity` 或 `Infinity` 值。
- 目前，向量数据类型不能存储双精度浮点数。未来版本将支持这一功能。

有关其他限制，请参阅[向量搜索限制](/vector-search-limitations.md)。

## MySQL兼容性

向量数据类型只在 TiDB 中支持，MySQL 不支持。

## 其他信息

- [向量函数和操作](/tidb-cloud/vector-search-functions-and-operators.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)