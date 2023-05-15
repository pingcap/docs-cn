---
title: Cast Functions and Operators
summary: Learn about the cast functions and operators.
aliases: ['/docs/dev/functions-and-operators/cast-functions-and-operators/','/docs/dev/reference/sql/functions-and-operators/cast-functions-and-operators/']
---

# Cast Functions and Operators

Cast functions and operators enable conversion of values from one data type to another. TiDB supports all of the [cast functions and operators](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html) available in MySQL 5.7.

## List of cast functions and operators

| Name                                     | Description                      |
| ---------------------------------------- | -------------------------------- |
| [`BINARY`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#operator_binary) | Cast a string to a binary string |
| [`CAST()`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#function_cast) | Cast a value as a certain type   |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#function_convert) | Cast a value as a certain type   |

> **Note:**
>
> TiDB and MySQL display inconsistent results for `SELECT CAST(MeN AS CHAR)` (or its equivalent form `SELECT CONVERT(MeM, CHAR)`), where `MeN` represents a double-precision floating-point number in scientific notation. MySQL displays the complete numeric value when `-15 <= N <= 14` and the scientific notation when `N < -15` or `N > 14`. However, TiDB always displays the complete numeric value. For example, MySQL displays the result of `SELECT CAST(3.1415e15 AS CHAR)` as `3.1415e15`, while TiDB displays the result as `3141500000000000`.
