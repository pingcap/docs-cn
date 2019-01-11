---
title: 操作符
category: user guide
---

# 操作符

| 操作符名 | 功能描述 |
| ------- | -------------------------------- |
| [`AND`, &&](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_and) | 逻辑与 |
| [`=`](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-equal) | 赋值 (可用于 [`SET`](https://dev.mysql.com/doc/refman/5.7/en/set-variable.html) 语句中, 或用于 [`UPDATE`](https://dev.mysql.com/doc/refman/5.7/en/update.html) 语句的 `SET` 中 ) |
| [`:=`](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-value) | 赋值 |
| [`BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_between) | 判断值满足范围 |
| [`BINARY`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#operator_binary) | 将一个字符串转换为一个二进制字符串 |
| [&](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-and) | 位与 |
| [~](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-invert) | 位非 |
| [`\|`](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-or) | 位或 |
| [`^`](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-xor) | 按位异或 |
| [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case) | case 操作符 |
| [`DIV`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_div) | 整数除 |
| [`/`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_divide) | 除法 |
| [`=`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal) | 相等比较 |
| [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to) | 空值安全型相等比较 |
| [`>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than) | 大于 |
| [`>=`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than-or-equal) | 大于或等于 |
| [`IS`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is) | 判断一个值是否等于一个布尔值 |
| [`IS NOT`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not) | 判断一个值是否不等于一个布尔值 |
| [`IS NOT NULL`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not-null) | 非空判断 |
| [`IS NULL`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-null) | 空值判断 |
| [`<<`](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_left-shift) | 左移 |
| [`<`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than) | 小于 |
| [`<=`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than-or-equal) | 小于或等于 |
| [`LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like) | 简单模式匹配 |
| [`-`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_minus) | 减 |
| [`%`, `MOD`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_mod) | 求余 |
| [`NOT`, `!`](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_not) | 取反 |
| [`NOT BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-between) | 判断值是否不在范围内 |
| [`!=`, `<>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal) | 不等于 |
| [`NOT LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like) | 不符合简单模式匹配 |
| [`NOT REGEXP`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_not-regexp) | 不符合正则表达式模式匹配 |
| [`\|\|`, `OR`](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_or) | 逻辑或 |
| [`+`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_plus) | 加 |
| [`REGEXP`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp) | 使用正则表达式进行模式匹配 |
| [`>>`](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_right-shift) | 右移 |
| [`RLIKE`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp) | REGEXP 同义词 |
| [`*`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_times) | 乘 |
| [`-`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_unary-minus) | 取反符号 |
| [`XOR`](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_xor) | 逻辑亦或 |

## 操作符优先级

操作符优先级显示在以下列表中，从最高优先级到最低优先级。同一行显示的操作符具有相同的优先级。

```sql
INTERVAL
BINARY
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

详情参见 [这里](https://dev.mysql.com/doc/refman/5.7/en/operator-precedence.html).

## 比较方法和操作符

| 操作符名 | 功能描述 |
| ------- | -------------------------------- |
| [`BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_between) | 判断值是否在范围内 |
| [`COALESCE()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) | 返回第一个非空值 |
| [`=`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal) | 相等比较 |
| [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to) | 空值安全型相等比较 |
| [`>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than) | 大于 |
| [`>=`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than-or-equal) | 大于或等于 |
| [`GREATEST()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_greatest) | 返回最大值 |
| [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in) | 判断值是否在一个值的集合内 |
| [`INTERVAL()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_interval) | 返回一个小于第一个参数的参数的下标 |
| [`IS`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is) | 判断是否等于一个布尔值 |
| [`IS NOT`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not) | 判断是否不等于一个布尔值 |
| [`IS NOT NULL`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not-null) | 非空判断 |
| [`IS NULL`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-null) | 空值判断 |
| [`ISNULL()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_isnull) | 判断参数是否为空 |
| [`LEAST()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_least) | 返回最小值 |
| [`<`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than) | 小于 |
| [`<=`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than-or-equal) | 小于或等于 |
| [`LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like) | 简单模式匹配 |
| [`NOT BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-between) | 判断值是否不在范围内 |
| [`!=`, `<>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal) | 不等于 |
| [`NOT IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_not-in) | 判断值是否不在一个值的集合内 |
| [`NOT LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like) | 不满足简单模式匹配 |
| [`STRCMP()`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#function_strcmp) | 比较两个字符串 |

详情参见 [这里](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html).

## 逻辑操作符

| 操作符名 | 功能描述 |
| ------- | -------------------------------- |
| [`AND`, &&](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_and) | 逻辑与 |
| [`NOT`, `!`](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_not) | 逻辑非 |
| [`\|\|`, `OR`](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_or) | 逻辑或 |
| [`XOR`](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_xor) | 逻辑亦或 |

详情参见 [这里](https://dev.mysql.com/doc/refman/5.7/en/group-by-handling.html).

## 赋值操作符

| 操作符名 | 功能描述 |
| ------- | -------------------------------- |
| [`=`](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-equal) | 赋值 (可用于 [`SET`](https://dev.mysql.com/doc/refman/5.7/en/set-variable.html) 语句中, 或用于 [`UPDATE`](https://dev.mysql.com/doc/refman/5.7/en/update.html) 语句的 `SET` 中 ) |
| [`:=`](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-value) | 赋值 |

详情参见 [这里](https://dev.mysql.com/doc/refman/5.7/en/group-by-functional-dependence.html).
