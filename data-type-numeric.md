---
title: Numeric Types
summary: Learn about numeric data types supported in TiDB.
aliases: ['/docs/dev/data-type-numeric/','/docs/dev/reference/sql/data-types/numeric/']
---

# Numeric Types

TiDB supports all the MySQL numeric types, including:

+ [Integer Types](#integer-types) (Exact Value)
+ [Floating-Point Types](#floating-point-types) (Approximate Value)
+ [Fixed-Point Types](#fixed-point-types) (Exact Value)

## Integer types

TiDB supports all the MySQL integer types, including `INTEGER`/`INT`, `TINYINT`, `SMALLINT`, `MEDIUMINT`, and `BIGINT`. For more information, see [Integer Data Type Syntax in MySQL](https://dev.mysql.com/doc/refman/5.7/en/integer-types.html).

The following table summarizes field descriptions:

| Syntax Element | Description |
| -------- | ------------------------------- |
| M | the display width of the type. Optional. |
| UNSIGNED | UNSIGNED. If omitted, it is SIGNED. |
| ZEROFILL | If you specify ZEROFILL for a numeric column, TiDB automatically adds the UNSIGNED attribute to the column. |

The following table summarizes the required storage and range for integer types supported by TiDB:

| Data Type | Storage Required (bytes) | Minimum Value (signed/unsigned) | Maximum value (signed/unsigned) |
| ------- | -------- | ----------- | ------------ |
| `TINYINT` | 1 | -128 / 0 | 127 / 255 |
| `SMALLINT` | 2 | -32768 / 0 | 32767 / 65535 |
| `MEDIUMINT` | 3 | -8388608 / 0 | 8388607 / 16777215 |
| `INT` | 4 | -2147483648 / 0 | 2147483647 / 4294967295 |
| `BIGINT` | 8 | -9223372036854775808 / 0 | 9223372036854775807 / 18446744073709551615 |

### `BIT` type

The BIT data type. A type of BIT(M) enables the storage of M-bit values. M can range from 1 to 64, with the default value of 1:

```sql
BIT[(M)]
```

### `BOOLEAN` type

The `BOOLEAN` type and its alias `BOOL` are equivalent to `TINYINT(1)`. If the value is `0`, it is considered as `False`; otherwise, it is considered `True`. As in MySQL, `True` is `1` and `False` is `0`:

```sql
BOOLEAN
```

### `TINYINT` type

The `TINYINT` data type stores signed values of range [-128, 127] and unsigned values of range [0, 255]:

```sql
TINYINT[(M)] [UNSIGNED] [ZEROFILL]
```

### `SMALLINT` type

The `SMALLINT` data type stores signed values of range [-32768, 32767], and unsigned values of range [0, 65535]:

```sql
SMALLINT[(M)] [UNSIGNED] [ZEROFILL]
```

### `MEDIUMINT` type

The `MEDIUMINT` data type stores signed values of range [-8388608, 8388607], and unsigned values of range [0, 16777215]:

```sql
MEDIUMINT[(M)] [UNSIGNED] [ZEROFILL]
```

### `INTEGER` type

The `INTEGER` type and its alias `INT` stores signed values of range [-2147483648, 2147483647], and unsigned values of range [0, 4294967295]:

```sql
INT[(M)] [UNSIGNED] [ZEROFILL]
```

You can also use another form:

```sql
INTEGER[(M)] [UNSIGNED] [ZEROFILL]
```

### `BIGINT` type

The `BIGINT` data type stores signed values of range [-9223372036854775808, 9223372036854775807], and unsigned values of range [0, 18446744073709551615]:

```sql
BIGINT[(M)] [UNSIGNED] [ZEROFILL]
```

## Floating-point types

TiDB supports all the MySQL floating-point types, including `FLOAT`, and `DOUBLE`. For more information, see [Floating-Point Types (Approximate Value) - FLOAT, DOUBLE in MySQL](https://dev.mysql.com/doc/refman/5.7/en/floating-point-types.html).

The following table summarizes field descriptions:

| Syntax Element | Description |
| -------- | ------------------------------- |
| M | the total number of digits |
| D | the number of digits following the decimal point |
| UNSIGNED | UNSIGNED. If omitted, it is SIGNED. |
| ZEROFILL | If you specify ZEROFILL for a numeric column, TiDB automatically adds the UNSIGNED attribute to the column. |

The following table summarizes the required storage for floating-point types supported by TiDB:

| Data Type | Storage Required (bytes)|
| ----------- |----------|
| `FLOAT` | 4 |
| `FLOAT(p)` | If 0 <= p <= 24, it is 4; if 25 <= p <= 53, it is 8|
| `DOUBLE` | 8 |

### `FLOAT` type

The `FLOAT` type stores a single-precision floating-point number. Permissible values are -3.402823466E+38 to -1.175494351E-38, 0, and 1.175494351E-38 to 3.402823466E+38. These are the theoretical limits, based on the IEEE standard. The actual range might be slightly smaller depending on your hardware or operating system.

`FLOAT(p)` can be used to represent the required precision in bits. TiDB uses this value only to determine whether to use `FLOAT` or `DOUBLE` for the resulting data type. If p is from 0 to 24, the data type becomes FLOAT with no M or D values. If p is from 25 to 53, the data type becomes `DOUBLE` with no M or D values. The range of the resulting column is the same as for the single-precision `FLOAT` or double-precision `DOUBLE` data type.

```sql
FLOAT[(M,D)] [UNSIGNED] [ZEROFILL]
FLOAT(p) [UNSIGNED] [ZEROFILL]
```

> **Note:**
>
> As in MySQL, the `FLOAT` data type stores approximate values. For values such as currency, it is recommended to use the `DECIMAL` type instead.
> In TiDB, the default precision of the `FLOAT` data type is 8 bits, but in MySQL, the default precision is 6 bits. For example, assuming that you insert `123456789` and `1.23456789` into columns of the `FLOAT` type in both TiDB and MySQL, when you query the corresponding values in MySQL, you get `123457000` and `1.23457`, while in TiDB, you get `123456790` and `1.2345679`.

### `DOUBLE` type

The `DOUBLE` type, and its alias `DOUBLE PRECISION` stores a double-precision floating-point number. Permissible values are -1.7976931348623157E+308 to -2.2250738585072014E-308, 0, and 2.2250738585072014E-308 to 1.7976931348623157E+308. These are the theoretical limits, based on the IEEE standard. The actual range might be slightly smaller depending on your hardware or operating system.

```sql
DOUBLE[(M,D)] [UNSIGNED] [ZEROFILL]
DOUBLE PRECISION [(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED] [ZEROFILL]
```

> **Warning:**
>
> As in MySQL, the `DOUBLE` data type stores approximate values. For values such as currency, it is recommended to use the `DECIMAL` type instead.

## Fixed-point types

TiDB supports all the MySQL floating-point types, including DECIMAL, and NUMERIC. For more information, [Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC in MySQL](https://dev.mysql.com/doc/refman/5.7/en/fixed-point-types.html).

The meaning of the fields:

| Syntax Element | Description |
| -------- | ------------------------------- |
| M | the total number of digits |
| D | the number of digits after the decimal point |
| UNSIGNED | UNSIGNED. If omitted, it is SIGNED. |
| ZEROFILL | If you specify ZEROFILL for a numeric column, TiDB automatically adds the UNSIGNED attribute to the column. |

### `DECIMAL` type

`DECIMAL` and its alias `NUMERIC` stores a packed "exact" fixed-point number. M is the total number of digits (the precision), and D is the number of digits after the decimal point (the scale). The decimal point and (for negative numbers) the - sign are not counted in M. If D is 0, values have no decimal point or fractional part. The maximum number of digits (M) for DECIMAL is 65. The maximum number of supported decimals (D) is 30. If D is omitted, the default is 0. If M is omitted, the default is 10.

```sql
DECIMAL[(M[,D])] [UNSIGNED] [ZEROFILL]
NUMERIC[(M[,D])] [UNSIGNED] [ZEROFILL]
```
