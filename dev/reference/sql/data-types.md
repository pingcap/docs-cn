---
title: TiDB Data Type
summary: Learn about the data types supported in TiDB.
category: reference
aliases: ['/docs/sql/datatype/']
---

# TiDB Data Type

TiDB supports all the data types in MySQL except the Spatial type, including numeric type, string type, date & time type, and JSON type.

The definition of the data type is: `T(M[, D])`. In this format:

- `T` indicates the specific data type.
- `M` indicates the maximum display width for integer types. For floating-point and fixed-point types, `M` is the total number of digits that can be stored (the precision). For string types, `M` is the maximum length. The maximum permissible value of M depends on the data type.
- `D` applies to floating-point and fixed-point types and indicates the number of digits following the decimal point (the scale).
- `fsp` applies to the TIME, DATETIME, and TIMESTAMP types and represents the fractional seconds precision. The `fsp` value, if given, must be in the range 0 to 6. A value of 0 signifies that there is no fractional part. If omitted, the default precision is 0.

## Numeric types

### Overview

TiDB supports all the MySQL numeric types, including:

+ Integer Types (Exact Value)
+ Floating-Point Types (Approximate Value)
+ Fixed-Point Types (Exact Value)

### Integer types (exact value)

TiDB supports all the MySQL integer types, including INTEGER/INT, TINYINT, SMALLINT, MEDIUMINT, and BIGINT. For more information, see [Numeric Type Overview in MySQL](https://dev.mysql.com/doc/refman/5.7/en/numeric-type-overview.html).

#### Type definition

Syntax:

```sql
BIT[(M)]
> The BIT data type. A type of BIT(M) enables storage of M-bit values. M can range from 1 to 64.

TINYINT[(M)] [UNSIGNED] [ZEROFILL]
> The TINYINT data type. The value range for signed: [-128, 127] and the range for unsigned is [0, 255].

BOOL, BOOLEAN
> BOOLEAN and is equivalent to TINYINT(1). If the value is "0", it is considered as False; otherwise, it is considered True. In TiDB, True is "1" and False is "0".


SMALLINT[(M)] [UNSIGNED] [ZEROFILL]
> SMALLINT. The signed range is: [-32768, 32767], and the unsigned range is [0, 65535].

MEDIUMINT[(M)] [UNSIGNED] [ZEROFILL]
> MEDIUMINT. The signed range is: [-8388608, 8388607], and the unsigned range is [0, 16777215].

INT[(M)] [UNSIGNED] [ZEROFILL]
> INT. The signed range is: [-2147483648, 2147483647], and the unsigned range is [0, 4294967295].

INTEGER[(M)] [UNSIGNED] [ZEROFILL]
> Same as INT.

BIGINT[(M)] [UNSIGNED] [ZEROFILL]
> BIGINT. The signed range is: [-9223372036854775808, 9223372036854775807], and the unsigned range is [0, 18446744073709551615].
```

The meaning of the fields:

| Syntax Element | Description |
| -------- | ------------------------------- |
| M | the display width of the type. Optional. |
| UNSIGNED | UNSIGNED. If omitted, it is SIGNED. |
| ZEROFILL | If you specify ZEROFILL for a numeric column, TiDB automatically adds the UNSIGNED attribute to the column. |

#### Storage and range

See the following for the requirements of the storage and minimum value/maximim value of each data type:

| Type | Storage Required (bytes) | Minimum Value (Signed/Unsigned) | Maximum Value (Signed/Unsigned) |
| ----------- |----------|-----------------------| --------------------- |
| `TINYINT` | 1 | -128 / 0 | 127 / 255 |
| `SMALLINT` | 2 | -32768 / 0 | 32767 / 65535 |
| `MEDIUMINT` | 3 | -8388608 / 0 | 8388607 / 16777215 |
| `INT` | 4 | -2147483648 / 0 | 2147483647 / 4294967295 |
| `BIGINT` | 8 | -9223372036854775808 / 0 | 9223372036854775807 / 18446744073709551615 |

### Floating-point types (approximate value)

TiDB supports all the MySQL floating-point types, including FLOAT, and DOUBLE. For more information, [Floating-Point Types (Approximate Value) - FLOAT, DOUBLE in MySQL](https://dev.mysql.com/doc/refman/5.7/en/floating-point-types.html).

#### Type definition

Syntax:

```sql
FLOAT[(M,D)] [UNSIGNED] [ZEROFILL]
> A small (single-precision) floating-point number. Permissible values are -3.402823466E+38 to -1.175494351E-38, 0, and 1.175494351E-38 to 3.402823466E+38. These are the theoretical limits, based on the IEEE standard. The actual range might be slightly smaller depending on your hardware or operating system.

DOUBLE[(M,D)] [UNSIGNED] [ZEROFILL]
> A normal-size (double-precision) floating-point number. Permissible values are -1.7976931348623157E+308 to -2.2250738585072014E-308, 0, and 2.2250738585072014E-308 to 1.7976931348623157E+308. These are the theoretical limits, based on the IEEE standard. The actual range might be slightly smaller depending on your hardware or operating system.
 
DOUBLE PRECISION [(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED] [ZEROFILL]
> Synonym for DOUBLE.

FLOAT(p) [UNSIGNED] [ZEROFILL]
> A floating-point number. p represents the precision in bits, but TiDB uses this value only to determine whether to use FLOAT or DOUBLE for the resulting data type. If p is from 0 to 24, the data type becomes FLOAT with no M or D values. If p is from 25 to 53, the data type becomes DOUBLE with no M or D values. The range of the resulting column is the same as for the single-precision FLOAT or double-precision DOUBLE data types described earlier in this section.
```

The meaning of the fields:

| Syntax Element | Description |
| -------- | ------------------------------- |
| M | the total number of digits |
| D | the number of digits following the decimal point |
| UNSIGNED | UNSIGNED. If omitted, it is SIGNED. |
| ZEROFILL | If you specify ZEROFILL for a numeric column, TiDB automatically adds the UNSIGNED attribute to the column. |

#### Storage

See the following for the requirements of the storage:

| Data Type | Storage Required (bytes)|
| ----------- |----------|
| `FLOAT` | 4 |
| `FLOAT(p)` | If 0 <= p <= 24, it is 4; if 25 <= p <= 53, it is 8|
| `DOUBLE` | 8 |


### Fixed-point types (exact value)

TiDB supports all the MySQL floating-point types, including DECIMAL, and NUMERIC. For more information, [Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC in MySQL](https://dev.mysql.com/doc/refman/5.7/en/fixed-point-types.html).

#### Type definition

Syntax

```sql
DECIMAL[(M[,D])] [UNSIGNED] [ZEROFILL]
> A packed “exact” fixed-point number. M is the total number of digits (the precision), and D is the number of digits after the decimal point (the scale). The decimal point and (for negative numbers) the - sign are not counted in M. If D is 0, values have no decimal point or fractional part. The maximum number of digits (M) for DECIMAL is 65. The maximum number of supported decimals (D) is 30. If D is omitted, the default is 0. If M is omitted, the default is 10.

NUMERIC[(M[,D])] [UNSIGNED] [ZEROFILL]
> Synonym for DECIMAL.
```

The meaning of the fields:

| Syntax Element | Description |
| -------- | ------------------------------- |
| M | the total number of digits |
| D | the number of digits after the decimal point |
| UNSIGNED | UNSIGNED. If omitted, it is SIGNED. |
| ZEROFILL | If you specify ZEROFILL for a numeric column, TiDB automatically adds the UNSIGNED attribute to the column. |

## Date and time types

### Overview

TiDB supports all the MySQL floating-point types, including DATE, DATETIME, TIMESTAMP, TIME, and YEAR. For more information, [Date and Time Types in MySQL](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-types.html).

#### Type definition

Syntax:

```sql
DATE
> A date. The supported range is '1000-01-01' to '9999-12-31'. TiDB displays DATE values in 'YYYY-MM-DD' format.

DATETIME[(fsp)]
> A date and time combination. The supported range is '1000-01-01 00:00:00.000000' to '9999-12-31 23:59:59.999999'. TiDB displays DATETIME values in 'YYYY-MM-DD HH:MM:SS[.fraction]' format, but permits assignment of values to DATETIME columns using either strings or numbers.
An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0.

TIMESTAMP[(fsp)]
> A timestamp. The range is '1970-01-01 00:00:01.000000' to '2038-01-19 03:14:07.999999'.
An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0.
An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0.

TIME[(fsp)]
> A time. The range is '-838:59:59.000000' to '838:59:59.000000'. TiDB displays TIME values in 'HH:MM:SS[.fraction]' format.
An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0.

YEAR[(4)]
> A year in four-digit format. Values display as 1901 to 2155, and 0000.

```

## String types

### Overview

TiDB supports all the MySQL string types, including CHAR, VARCHAR, BINARY, VARBINARY, BLOB, TEXT, ENUM, and SET. For more information, [String Types in MySQL](https://dev.mysql.com/doc/refman/5.7/en/string-types.html).

#### Type definition

Syntax:

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
> A fixed-length string. If stored as CHAR, it is right-padded with spaces to the specified length. M represents the column length in characters. The range of M is 0 to 255.

[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
> A variable-length string. M represents the maximum column length in characters. The range of M is 0 to 65,535. The effective maximum length of a VARCHAR is subject to the maximum row size (65,535 bytes, which is shared among all columns) and the character set used.

BINARY(M)
> The BINARY type is similar to the CHAR type, but stores binary byte strings rather than nonbinary character strings.

VARBINARY(M)
> The VARBINARY type is similar to the VARCHAR type, but stores binary byte strings rather than nonbinary character strings.

BLOB[(M)]
> A BLOB column with a maximum length of 65,535 bytes. M represents the maximum column length.

TINYBLOB
> A BLOB column with a maximum length of 255 bytes.

MEDIUMBLOB
> A BLOB column with a maximum length of 16,777,215 bytes.

LONGBLOB
> A BLOB column with a maximum length of 4,294,967,295 bytes.

TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
> A TEXT column. M represents the maximum column length ranging from 0 to 65,535. The maximum length of TEXT is based on the size of the longest row and the character set.

TINYTEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
> A TEXT column with a maximum length of 255 characters.

MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
> A TEXT column with a maximum length of 16,777,215 characters.

LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
> A TEXT column with a maximum length of 4,294,967,295 characters.

ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]
> An enumeration. A string object that can have only one value, chosen from the list of values 'value1', 'value2', ..., NULL or the special '' error value.

SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]
> A set. A string object that can have zero or more values, each of which must be chosen from the list of values 'value1', 'value2', ...
```

## JSON types

TiDB supports the JSON (JavaScript Object Notation) data type.
The JSON type can store semi-structured data like JSON documents. The JSON data type provides the following advantages over storing JSON-format strings in a string column:

- Use the Binary format for serialization. The internal format permits quick read access to JSON document elements.
- Automatic validation of the JSON documents stored in JSON columns.Only valid documents can be stored.

JSON columns, like columns of other binary types, are not indexed directly, but you can index the fields in the JSON document in the form of generated column:

```sql
CREATE TABLE city (
id INT PRIMARY KEY,
detail JSON,
population INT AS (JSON_EXTRACT(detail, '$.population')
);
INSERT INTO city VALUES (1, '{"name": "Beijing", "population": 100}');
SELECT id FROM city WHERE population >= 100;
```

For more information, see [JSON Functions](/dev/reference/sql/functions-and-operators/json-functions.md) and [Generated Columns](/dev/reference/sql/generated-columns.md).

## The ENUM data type

An ENUM is a string object with a value chosen from a list of permitted values that are enumerated explicitly in the column specification when the table is created. The syntax is:

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
ENUM('apple', 'orange', 'pear')
```

The value of the ENUM data type is stored as numbers. Each value is converted to a number according the definition order. In the previous example, each string is mapped to a number:

| Value | Number |
| ---- | ---- |
| NULL | NULL |
| '' | 0 |
| 'apple' | 1 |
| 'orange' | 2 |
| 'pear' | 3 |

For more information, see [the ENUM type in MySQL](https://dev.mysql.com/doc/refman/5.7/en/enum.html).

## The SET type

A SET is a string object that can have zero or more values, each of which must be chosen from a list of permitted values specified when the table is created. The syntax is:

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
SET('1', '2') NOT NULL
```
In the example, any of the following values can be valid:

```
''
'1'
'2'
'1,2'
```
In TiDB, the values of the SET type is internally converted to Int64. The existence of each element is represented using a binary: 0 or 1. For a column specified as `SET('a','b','c','d')`, the members have the following decimal and binary values.

| Member | Decimal Value | Binary Value |
| ---- | ---- | ------ |
| 'a' | 1 | 0001 |
| 'b' | 2 | 0010 |
| 'c' | 4 | 0100 |
| 'd' | 8 | 1000 |

In this case, for an element of `('a', 'c')`, it is 0101 in binary.

For more information, see [the SET type in MySQL](https://dev.mysql.com/doc/refman/5.7/en/set.html).

## Data type default values

The DEFAULT value clause in a data type specification indicates a default value for a column. The default value must be a constant and cannot be a function or an expression. But for the time type, you can specify the `NOW`, `CURRENT_TIMESTAMP`, `LOCALTIME`, and `LOCALTIMESTAMP` functions as the default for TIMESTAMP and DATETIME columns

The BLOB, TEXT, and JSON columns cannot be assigned a default value.

If a column definition includes no explicit DEFAULT value, TiDB determines the default value as follows:

- If the column can take NULL as a value, the column is defined with an explicit DEFAULT NULL clause.
- If the column cannot take NULL as the value, TiDB defines the column with no explicit DEFAULT clause.

For data entry into a NOT NULL column that has no explicit DEFAULT clause, if an INSERT or REPLACE statement includes no value for the column, TiDB handles the column according to the SQL mode in effect at the time:

- If strict SQL mode is enabled, an error occurs for transactional tables, and the statement is rolled back. For nontransactional tables, an error occurs.
- If strict mode is not enabled, TiDB sets the column to the implicit default value for the column data type.

Implicit defaults are defined as follows:

- For numeric types, the default is 0. If declared with the AUTO_INCREMENT attribute, the default is the next value in the sequence.
- For date and time types other than TIMESTAMP, the default is the appropriate “zero” value for the type. For TIMESTAMP, the default value is the current date and time.
- For string types other than ENUM, the default value is the empty string. For ENUM, the default is the first enumeration value.
