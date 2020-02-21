---
title: Operators
summary: Learn about the operators precedence, comparison functions and operators, logical operators, and assignment operators.
category: reference
---

# Operators

This document describes the operators precedence, comparison functions and operators, logical operators, and assignment operators.

- [Operator precedence](#operator-precedence)
- [Comparison functions and operators](#comparison-functions-and-operators)
- [Logical operators](#logical-operators)
- [Assignment operators](#assignment-operators)

| Name | Description |
| ---------------------------------------- | ---------------------------------------- |
| [AND, &&](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_and) | Logical AND |
| [=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-equal) | Assign a value (as part of a [`SET`](https://dev.mysql.com/doc/refman/5.7/en/set-variable.html) statement, or as part of the `SET` clause in an [`UPDATE`](https://dev.mysql.com/doc/refman/5.7/en/update.html) statement) |
| [:=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-value) | Assign a value |
| [BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_between) | Check whether a value is within a range of values |
| [BINARY](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#operator_binary) | Cast a string to a binary string |
| [&](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-and) | Bitwise AND |
| [~](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-invert) | Bitwise inversion |
| [\|](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-or) | Bitwise OR |
| [^](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-xor) | Bitwise XOR |
| [CASE](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case) | Case operator |
| [DIV](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_div) | Integer division |
| [/](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_divide) | Division operator |
| [=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal) | Equal operator |
| [<=>](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to) | NULL-safe equal to operator |
| [>](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than) | Greater than operator |
| [>=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than-or-equal) | Greater than or equal operator |
| [IS](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is) | Test a value against a boolean |
| [IS NOT](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not) | Test a value against a boolean |
| [IS NOT NULL](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not-null) | NOT NULL value test |
| [IS NULL](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-null) | NULL value test |
| [->](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path) | Return value from JSON column after evaluating path; equivalent to `JSON_EXTRACT()` |
| [->>](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path) | Return value from JSON column after evaluating path and unquoting the result; equivalent to `JSON_UNQUOTE(JSON_EXTRACT())` |
| [<<](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_left-shift) | Left shift |
| [<](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than) | Less than operator |
| [<=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than-or-equal) | Less than or equal operator |
| [LIKE](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like) | Simple pattern matching |
| [-](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_minus) | Minus operator |
| [%, MOD](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_mod) | Modulo operator |
| [NOT, !](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_not) | Negates value |
| [NOT BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-between) | Check whether a value is not within a range of values |
| [!=, <>](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal) | Not equal operator |
| [NOT LIKE](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like) | Negation of simple pattern matching |
| [NOT REGEXP](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_not-regexp) | Negation of REGEXP |
| [\|\|, OR](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_or) | Logical OR |
| [+](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_plus) | Addition operator |
| [REGEXP](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp) | Pattern matching using regular expressions |
| [>>](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_right-shift) | Right shift |
| [RLIKE](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp) | Synonym for REGEXP |
| [SOUNDS LIKE](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#operator_sounds-like) | Compare sounds |
| [*](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_times) | Multiplication operator |
| [-](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_unary-minus) | Change the sign of the argument |
| [XOR](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_xor) | Logical XOR |

## Operator precedence

Operator precedences are shown in the following list, from highest precedence to the lowest. Operators that are shown together on a line have the same precedence.

```sql
INTERVAL
BINARY, COLLATE
!
- (unary minus), ~ (unary bit inversion)
^
*, /, DIV, %, MOD
-, +
<<, >>
&
|
= (comparison), <=>, >=, >, <=, <, <>, !=, IS, LIKE, REGEXP, IN
BETWEEN, CASE, WHEN, THEN, ELSE
NOT
AND, &&
XOR
OR, ||
= (assignment), :=
```

For details, see [Operator Precedence](https://dev.mysql.com/doc/refman/5.7/en/operator-precedence.html).

## Comparison functions and operators

| Name | Description |
| ---------------------------------------- | ---------------------------------------- |
| [BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_between) | Check whether a value is within a range of values |
| [COALESCE()](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) | Return the first non-NULL argument |
| [=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal) | Equal operator |
| [<=>](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to) | NULL-safe equal to operator |
| [>](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than) | Greater than operator |
| [>=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than-or-equal) | Greater than or equal operator |
| [GREATEST()](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_greatest) | Return the largest argument |
| [IN()](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in) | Check whether a value is within a set of values |
| [INTERVAL()](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_interval) | Return the index of the argument that is less than the first argument |
| [IS](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is) | Test a value against a boolean |
| [IS NOT](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not) | Test a value against a boolean |
| [IS NOT NULL](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not-null) | NOT NULL value test |
| [IS NULL](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-null) | NULL value test |
| [ISNULL()](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_isnull) | Test whether the argument is NULL |
| [LEAST()](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_least) | Return the smallest argument |
| [<](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than) | Less than operator |
| [<=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than-or-equal) | Less than or equal operator |
| [LIKE](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like) | Simple pattern matching |
| [NOT BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-between) | Check whether a value is not within a range of values |
| [!=, <>](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal) | Not equal operator |
| [NOT IN()](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_not-in) | Check whether a value is not within a set of values |
| [NOT LIKE](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like) | Negation of simple pattern matching |
| [STRCMP()](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#function_strcmp) | Compare two strings |

For details, see [Comparison Functions and Operators](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html).

## Logical operators

| Name | Description |
| ---------------------------------------- | ------------- |
| [AND, &&](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_and) | Logical AND |
| [NOT, !](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_not) | Negates value |
| [\|\|, OR](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_or) | Logical OR |
| [XOR](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_xor) | Logical XOR |

For details, see [MySQL Handling of GROUP BY](https://dev.mysql.com/doc/refman/5.7/en/group-by-handling.html).

## Assignment operators

| Name | Description |
| ---------------------------------------- | ---------------------------------------- |
| [=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-equal) | Assign a value (as part of a [`SET`](https://dev.mysql.com/doc/refman/5.7/en/set-variable.html) statement, or as part of the `SET` clause in an [`UPDATE`](https://dev.mysql.com/doc/refman/5.7/en/update.html) statement) |
| [:=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-value) | Assign a value |

For details, see [Detection of Functional Dependence](https://dev.mysql.com/doc/refman/5.7/en/group-by-functional-dependence.html).
