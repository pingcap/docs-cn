---
title: Literal Values
summary: Learn how to use various literal values.
category: reference
aliases: ['/docs/sql/literal-values/']
---

# Literal Values

This document describes String literals, Numeric literals, NULL values, Hexadecimal literals, Date and time literals, Boolean literals, and Bit-value literals.

## String literals

A string is a sequence of bytes or characters, enclosed within either single quote `'` or double quote `"` characters. For example:

```
'example string'
"example string"
```

Quoted strings placed next to each other are concatenated to a single string. The following lines are equivalent:

```
'a string'
'a' ' ' 'string'
"a" ' ' "string"
```

If the `ANSI_QUOTES` SQL MODE is enabled, string literals can be quoted only within single quotation marks because a string quoted within double quotation marks is interpreted as an identifier.

A binary string is a string of bytes. Each binary string has a character set and collation named `binary`. A non-binary string is a string of characters. It has a character set other than `binary` and a collation that is compatible with the character set.

For both types of strings, comparisons are based on the numeric values of the string unit. For binary strings, the unit is the byte. For non-binary strings, the unit is the character and some character sets support multibyte characters.

A string literal may have an optional `character set introducer` and `COLLATE clause`, to designate it as a string that uses a specific character set and collation. TiDB only supports this in syntax, but does not process it.

```
[_charset_name]'string' [COLLATE collation_name]
```

For example:

```
SELECT _latin1'string';
SELECT _binary'string';
SELECT _utf8'string' COLLATE utf8_bin;
```

You can use N'literal' (or n'literal') to create a string in the national character set. The following statements are equivalent:

```
SELECT N'some text';
SELECT n'some text';
SELECT _utf8'some text';
```

Escape characters:

- `\0`: An ASCII NUL (X'00') character
- `\'`: A single quote (') character
- `\"`: A double quote (")character
- `\b`: A backspace character
- `\n`: A newline (linefeed) character
- `\r`: A carriage return character
- `\t`: A tab character
- `\z`: ASCII 26 (Ctrl + Z)
- `\\`: A backslash `\` character
- `\%`: A `%` character
- `\_`: A `_` character

You can use the following ways to include quote characters within a string:

- A `'` inside a string quoted with `'` may be written as `''`.
- A `"` inside a string quoted with `"` may be written as `""`.
- Precede the quote character by an escape character `\`.
- A `'` inside a string quoted with `"` needs no special treatment, and a `"` inside a string quoted with `'` needs no special treatment either.

For more information, see [String Literals in MySQL](https://dev.mysql.com/doc/refman/5.7/en/string-literals.html).

## Numeric literals

Numeric literals include integer and DECIMAL literals and floating-point literals.

Integer may include `.` as a decimal separator. Numbers may be preceded by `-` or `+` to indicate a negative or positive value respectively.

Exact-value numeric literals can be represented as `1, .2, 3.4, -5, -6.78, +9.10`.

Numeric literals can also be represented in scientific notation, such as `1.2E3, 1.2E-3, -1.2E3, -1.2E-3`.

For more information, see [Numeric Literals in MySQL](https://dev.mysql.com/doc/refman/5.7/en/number-literals.html).

## NULL values

The `NULL` value means “no data”. NULL can be written in any letter case. A synonym is `\N` (case sensitive).

Be aware that the `NULL` value is different from values such as `0` for numeric types or the empty string `''` for string types.

## Hexadecimal literals

Hexadecimal literal values are written using `X'val'` or `0xval` notation, where `val` contains hexadecimal digits. A leading `0x` is case sensitive and cannot be written as `0X`.

Legal hexadecimal literals:

```
X'ac12'
X'12AC'
x'ac12'
x'12AC'
0xac12
0x12AC
```

Illegal hexadecimal literals:

```
X'1z' (z is not a hexadecimal legal digit)
0X12AC (0X must be written as 0x)
```

Hexadecimal literals written using `X'val'` notation must contain an even number of digits. To avoid the syntax error, pad the value with a leading zero:

```sql
mysql> select X'aff';
ERROR 1105 (HY000): line 0 column 13 near ""hex literal: invalid hexadecimal format, must even numbers, but 3 (total length 13)
mysql> select X'0aff';
+---------+
| X'0aff' |
+---------+
|
       |
+---------+
1 row in set (0.00 sec)
```

By default, a hexadecimal literal is a binary string.

To convert a string or a number to a string in hexadecimal format, use the `HEX()` function:

```sql
mysql> SELECT HEX('TiDB');
+-------------+
| HEX('TiDB') |
+-------------+
| 54694442    |
+-------------+
1 row in set (0.01 sec)

mysql> SELECT X'54694442';
+-------------+
| X'54694442' |
+-------------+
| TiDB        |
+-------------+
1 row in set (0.00 sec)
```

## Date and time literals

Date and time values can be represented in several formats, such as quoted strings or as numbers. When TiDB expects a date, it interprets any of `'2015-07-21'`, `'20150721'` and `20150721` as a date.

TiDB supports the following formats for date values:

- As a string in either `'YYYY-MM-DD'` or `'YY-MM-DD'` format. The `-` delimiter is "relaxed" in syntax. Any punctuation character may be used as the delimiter between date parts. For example, `'2017-08-24'`, `'2017&08&24'` and `'2012@12^31'` are equivalent. The only delimiter recognized is the `.` character, which is treated as a decimal point to separate the integer and fractional parts. The date and time parts can be separated by `T` other than a space. For example, `2017-8-24 10:42:00` and `2017-8-24T10:42:00` are equivalent.
- As a string with no delimiters in either `'YYYYMMDDHHMMSS'` or `'YYMMDDHHMMSS'` format. For example, `'20170824104520'` and `'170824104520'` are interpreted as `'2017-08-24 10:45:20'`. But `'170824304520'` is illegal because the hour part exceeds the legal range.
- As a number in either `YYYYMMDDHHMMSS` or `YYMMDDHHMMSS` format, without single quotation marks or double quotation marks. For example, `20170824104520` is interpreted as `'2017-08-24 10:45:20'`.

A DATETIME or TIMESTAMP value can include a trailing fractional seconds part in up to microseconds (6 digits) precision. The fractional part should always be separated from the rest of the time by a decimal point.

Dates containing two-digit year values are ambiguous. It is recommended to use the four-digit format. TiDB interprets two-digit year values using the following rules:

- Year values in the range of `70-99` are converted to `1970-1999`.
- Year values in the range of `00-69` are converted to `2000-2069`.

For values specified as strings that include date part delimiters, it is unnecessary to specify two digits for month or day values that are less than 10. `'2017-8-4'` is the same as `'2017-08-04'`. Similarly, for values specified as strings that include time part delimiters, it is unnecessary to specify two digits for hour, minute, or second values that are less than 10. `'2017-08-24 1:2:3'` is the same as `'2017-08-24 01:02:03'`.

In TiDB, the date or time values specified as numbers are interpreted according their length:

- 6 digits: `YYMMDD`
- 12 digits: `YYMMDDHHMMSS`
- 8 digits: `YYYYMMDD`
- 14 digits: `YYYYMMDDHHMMSS`

TiDB supports the following formats for time values:

- As a string in `'D HH:MM:SS'` format. You can also use one of the following “relaxed” syntaxes: `'HH:MM:SS'`, `'HH:MM'`, `'D HH:MM'`, `'D HH'`, or `'SS'`. Here D represents days and the legal value range is `0-34`.
- As a number in `'HHMMSS'` format. For example, `231010` is interpreted as `'23:10:10'`.
- A number in any of the `SS`, `MMSS` or `HHMMSS` format can be treated as time.

The time value can also include a trailing fractional part in up to 6 digits precision. The `.` character represents the decimal point.

For more information, see [Date and Time Literals in MySQL](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-literals.html).

## Boolean literals

The constants `TRUE` and `FALSE` evaluate to 1 and 0 respectively, which are not case sensitive.

```sql
mysql> SELECT TRUE, true, tRuE, FALSE, FaLsE, false;
+------+------+------+-------+-------+-------+
| TRUE | true | tRuE | FALSE | FaLsE | false |
+------+------+------+-------+-------+-------+
|    1 |    1 |    1 |     0 |     0 |     0 |
+------+------+------+-------+-------+-------+
1 row in set (0.00 sec)
```

## Bit-value literals

Bit-value literals are written using `b'val'` or `0bval` notation. The `val` is a binary value written using zeros and ones. A leading `0b` is case sensitive and cannot be written as `0B`.

Legal bit-value literals:

```
b'01'
B'01'
0b01
```

Illegal bit-value literals:

```
b'2' (2 is not a binary digit; it must be 0 or 1)
0B01 (0B must be written as 0b)
```

By default, a bit-value literal is a binary string.

Bit values are returned as binary values, which may not display well in the MySQL client. To convert a bit value to printable form, you can use a conversion function such as `BIN()` or `HEX()`.

```sql
CREATE TABLE t (b BIT(8));
INSERT INTO t SET b = b'00010011';
INSERT INTO t SET b = b'1110';
INSERT INTO t SET b = b'100101';

mysql> SELECT b+0, BIN(b), HEX(b) FROM t;
+------+--------+--------+
| b+0  | BIN(b) | HEX(b) |
+------+--------+--------+
|   19 | 10011  | 13     |
|   14 | 1110   | E      |
|   37 | 100101 | 25     |
+------+--------+--------+
3 rows in set (0.00 sec)
```
