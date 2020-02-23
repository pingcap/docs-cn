---
title: 数值类型
category: reference
---

# 数值类型

TiDB 支持 MySQL 所有的数值类型，按照精度可以分为:

+ [整数类型（精确值)](#整数类型)
+ [浮点类型（近似值)](#浮点类型)
+ [定点类型（精确值)](#定点类型)

## 整数类型

TiDB 支持 MySQL 所有的整数类型，包括 `INTEGER`/`INT`、`TINYINT`、`SMALLINT`、`MEDIUMINT` 以及 `BIGINT`，完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/numeric-type-overview.html)文档。

字段说明：

| 语法元素 | 说明 |
| ---- | --------|
| M | 类型显示宽度，可选 |
| UNSIGNED | 无符号数，如果不加这个标识，则为有符号数 |
| ZEROFILL | 补零标识，如果有这个标识，TiDB 会自动给类型增加 UNSIGNED 标识，但是没有做补零的操作 |

### 类型定义

#### `BIT` 类型

比特值类型。M 表示比特位的长度，取值范围从1到64，其默认值是1。

{{< copyable "sql" >}}

```sql
BIT[(M)]
```

#### `BOOLEAN` 类型

布尔类型，别名为 `BOOL`，和 `TINYINT(1)` 等价。零值被认为是 `False`，非零值认为是 `True`。在 TiDB 内部，`True` 存储为 `1`，`False` 存储为 `0`。

{{< copyable "sql" >}}

```sql
BOOLEAN
```

#### `TINYINT` 类型

`TINYINT` 类型。有符号数的范围是 `[-128, 127]`。无符号数的范围是 `[0, 255]`。

{{< copyable "sql" >}}

```sql
TINYINT[(M)] [UNSIGNED] [ZEROFILL]
```

#### `SMALLINT` 类型

`SMALLINT` 类型。有符号数的范围是 `[-32768, 32767]`。无符号数的范围是 `[0, 65535]`。

{{< copyable "sql" >}}

```sql
SMALLINT[(M)] [UNSIGNED] [ZEROFILL]
```

#### `MEDIUMINT` 类型

`MEDIUMINT` 类型。有符号数的范围是 `[-8388608, 8388607]`。无符号数的范围是 `[0, 16777215]`。

{{< copyable "sql" >}}

```sql
MEDIUMINT[(M)] [UNSIGNED] [ZEROFILL]
```

### `INTEGER` 类型

`INTEGER` 类型，别名 `INT`。有符号数的范围是 `[-2147483648, 2147483647]`。无符号数的范围是 `[0, 4294967295]`。

{{< copyable "sql" >}}

```sql
INT[(M)] [UNSIGNED] [ZEROFILL]
```

或者：

{{< copyable "sql" >}}

```sql
INTEGER[(M)] [UNSIGNED] [ZEROFILL]
```

### `BIGINT` 类型

`BIGINT` 类型。有符号数的范围是 `[-9223372036854775808, 9223372036854775807]`。无符号数的范围是 `[0, 18446744073709551615]`。

{{< copyable "sql" >}}

```sql
BIGINT[(M)] [UNSIGNED] [ZEROFILL]
>
```

### 存储空间以及取值范围

每种类型对存储空间的需求以及最大/最小值如下表所示:

| 类型        | 存储空间 | 最小值(有符号/无符号) | 最大值(有符号/无符号) |
| ----------- |----------|-----------------------| --------------------- |
| `TINYINT`   | 1        | -128 / 0              | 127 / 255             |
| `SMALLINT`  | 2        | -32768 / 0            | 32767 / 65535         |
| `MEDIUMINT` | 3        | -8388608 / 0          | 8388607 / 16777215    |
| `INT`       | 4        | -2147483648 / 0       | 2147483647 / 4294967295 |
| `BIGINT`    | 8        | -9223372036854775808 / 0 | 9223372036854775807 / 18446744073709551615 |

## 浮点类型

TiDB 支持 MySQL 所有的浮点类型，包括 `FLOAT`、`DOUBLE`，完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/floating-point-types.html)文档。

字段说明：

| 语法元素 | 说明                            |
| -------- | ------------------------------- |
| M        | 小数总位数 |
| D        | 小数点后位数 |
| UNSIGNED | 无符号数，如果不加这个标识，则为有符号数 |
| ZEROFILL | 补零标识，如果有这个标识，TiDB 会自动给类型增加 UNSIGNED 标识 |

### 类型定义

#### `FLOAT` 类型

单精度浮点数。允许的值范围为 -2^128 ~ +2^128，也即 -3.402823466E+38 到 -1.175494351E-38、0 和 1.175494351E-38 到 3.402823466E+38。这些是基于 IEEE 标准的理论限制。实际的范围根据硬件或操作系统的不同可能稍微小些。

`FLOAT(p)` 类型中，`p` 表示精度（以位数表示）。只使用该值来确定是否结果列的数据类型为 `FLOAT` 或 `DOUBLE`。如果 `p` 为从 0 到 24，数据类型变为没有 M 或 D 值的 `FLOAT`。如果 `p` 为从 25 到 53，数据类型变为没有 M 或 D 值的 `DOUBLE`。结果列范围与本节前面描述的单精度 `FLOAT` 或双精度 `DOUBLE` 数据类型相同。

{{< copyable "sql" >}}

```sql
FLOAT[(M,D)] [UNSIGNED] [ZEROFILL]
FLOAT(p) [UNSIGNED] [ZEROFILL]
```

> **警告：**
>
> 与在 MySQL 中一样，`FLOAT` 数据类型存储近似值。对于货币之类的精确值，建议使用 `DECIMAL` 类型。

#### `DOUBLE` 类型

双精度浮点数，别名为 `DOUBLE PRECISION`。允许的值范围为：-2^1024 ~ +2^1024，也即是 -1.7976931348623157E+308 到 -2.2250738585072014E-308、0 和 2.2250738585072014E-308 到 1.7976931348623157E+308。这些是基于 IEEE 标准的理论限制。实际的范围根据硬件或操作系统的不同可能稍微小些。

{{< copyable "sql" >}}

```sql
DOUBLE[(M,D)] [UNSIGNED] [ZEROFILL]
DOUBLE PRECISION [(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED] [ZEROFILL]
```

> **警告：**
>
> 与在 MySQL 中一样，`DOUBLE` 数据类型存储近似值。对于货币之类的精确值，建议使用 `DECIMAL` 类型。

### 存储空间

每种类型对存储空间的需求如下表所示:

| 类型        | 存储空间 |
| ----------- |----------|
| `FLOAT`     | 4        |
| `FLOAT(p)`  | 如果 0 <= p <= 24 为 4 个字节, 如果 25 <= p <= 53 为 8 个字节|
| `DOUBLE`    | 8        |

## 定点类型

TiDB 支持 MySQL 所有的定点类型，包括 `DECIMAL`、`NUMERIC`，完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/fixed-point-types.html)文档。

字段说明：

| 语法元素 | 说明                            |
| -------- | ------------------------------- |
| M        | 小数总位数 |
| D        | 小数点后位数 |
| UNSIGNED | 无符号数，如果不加这个标识，则为有符号数 |
| ZEROFILL | 补零标识，如果有这个标识，TiDB 会自动给类型增加 UNSIGNED 标识 |

### 类型定义

#### `DECIMAL` 类型

定点数，别名为 `NUMERIC`。M 是小数位数（精度）的总数，D 是小数点（标度）后面的位数。小数点和 `-`（负数）符号不包括在 M 中。如果 D 是 0，则值没有小数点或分数部分。如果 D 被省略，默认是 0。如果 M 被省略，默认是 10。

{{< copyable "sql" >}}

```sql
DECIMAL[(M[,D])] [UNSIGNED] [ZEROFILL]
NUMERIC[(M[,D])] [UNSIGNED] [ZEROFILL]
```
