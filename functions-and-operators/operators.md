---
title: 运算符
summary: 了解运算符优先级、比较函数和运算符、逻辑运算符以及赋值运算符。
---

# 运算符

本文档描述运算符优先级、比较函数和运算符、逻辑运算符以及赋值运算符。

- [运算符优先级](#运算符优先级)
- [比较函数和运算符](#比较函数和运算符)
- [逻辑运算符](#逻辑运算符)
- [赋值运算符](#赋值运算符)

| 名称 | 描述 |
| ---------------------------------------- | ---------------------------------------- |
| [AND, &&](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_and) | 逻辑与 |
| [=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-equal) | 赋值（作为 [`SET`](https://dev.mysql.com/doc/refman/8.0/en/set-variable.html) 语句的一部分，或作为 [`UPDATE`](https://dev.mysql.com/doc/refman/8.0/en/update.html) 语句中 `SET` 子句的一部分） |
| [:=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-value) | 赋值 |
| [BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between) | 检查值是否在某个范围内 |
| [BINARY](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#operator_binary) | 将字符串转换为二进制字符串 |
| [&](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-and) | 按位与 |
| [~](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-invert) | 按位取反 |
| [\|](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-or) | 按位或 |
| [^](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-xor) | 按位异或 |
| [CASE](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case) | Case 运算符 |
| [DIV](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_div) | 整数除法 |
| [/](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_divide) | 除法运算符 |
| [=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal) | 等于运算符 |
| [`<=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to) | NULL 安全的等于运算符 |
| [>](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than) | 大于运算符 |
| [>=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal) | 大于等于运算符 |
| [IS](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is) | 测试值是否为布尔值 |
| [IS NOT](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not) | 测试值是否为布尔值 |
| [IS NOT NULL](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not-null) | 非 NULL 值测试 |
| [IS NULL](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null) | NULL 值测试 |
| [->](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path) | 在评估路径后从 JSON 列返回值；等同于 `JSON_EXTRACT()` |
| [->>](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path) | 在评估路径后从 JSON 列返回值并对结果去引号；等同于 `JSON_UNQUOTE(JSON_EXTRACT())` |
| [<<](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_left-shift) | 左移 |
| [<](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than) | 小于运算符 |
| [<=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal) | 小于等于运算符 |
| [LIKE](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like) | 简单模式匹配 |
| [ILIKE](https://www.postgresql.org/docs/current/functions-matching.html) | 不区分大小写的简单模式匹配（TiDB 支持，但 MySQL 不支持） |
| [-](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus) | 减法运算符 |
| [%, MOD](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_mod) | 取模运算符 |
| [NOT, !](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_not) | 取反值 |
| [NOT BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 检查值是否不在某个范围内 |
| [!=, `<>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal) | 不等于运算符 |
| [NOT LIKE](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like) | 简单模式匹配的否定 |
| [NOT REGEXP](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp) | REGEXP 的否定 |
| [\|\|, OR](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_or) | 逻辑或 |
| [+](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus) | 加法运算符 |
| [REGEXP](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp) | 使用正则表达式的模式匹配 |
| [>>](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_right-shift) | 右移 |
| [RLIKE](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp) | REGEXP 的同义词 |
| [*](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_times) | 乘法运算符 |
| [-](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_unary-minus) | 改变参数的符号 |
| [XOR](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_xor) | 逻辑异或 |

## 不支持的运算符

* [`SOUNDS LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#operator_sounds-like)

## 运算符优先级

以下列表显示了运算符的优先级，从最高优先级到最低优先级。同一行显示的运算符具有相同的优先级。

```sql
INTERVAL
BINARY, COLLATE
!
- (一元减号), ~ (一元按位取反)
^
*, /, DIV, %, MOD
-, +
<<, >>
&
|
= (比较), <=>, >=, >, <=, <, <>, !=, IS, LIKE, REGEXP, IN
BETWEEN, CASE, WHEN, THEN, ELSE
NOT
AND, &&
XOR
OR, ||
= (赋值), :=
```

详情请参见 [运算符优先级](https://dev.mysql.com/doc/refman/8.0/en/operator-precedence.html)。

## 比较函数和运算符

| 名称 | 描述 |
| ---------------------------------------- | ---------------------------------------- |
| [BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between) | 检查值是否在某个范围内 |
| [COALESCE()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce) | 返回第一个非 NULL 参数 |
| [=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal) | 等于运算符 |
| [`<=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to) | NULL 安全的等于运算符 |
| [>](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than) | 大于运算符 |
| [>=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal) | 大于等于运算符 |
| [GREATEST()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest) | 返回最大的参数 |
| [IN()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in) | 检查值是否在一组值中 |
| [INTERVAL()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_interval) | 返回小于第一个参数的参数的索引 |
| [IS](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is) | 测试值是否为布尔值 |
| [IS NOT](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not) | 测试值是否为布尔值 |
| [IS NOT NULL](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not-null) | 非 NULL 值测试 |
| [IS NULL](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null) | NULL 值测试 |
| [ISNULL()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull) | 测试参数是否为 NULL |
| [LEAST()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least) | 返回最小的参数 |
| [<](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than) | 小于运算符 |
| [<=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal) | 小于等于运算符 |
| [LIKE](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like) | 简单模式匹配 |
| [ILIKE](https://www.postgresql.org/docs/current/functions-matching.html) | 不区分大小写的简单模式匹配（TiDB 支持，但 MySQL 不支持） |
| [NOT BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 检查值是否不在某个范围内 |
| [!=, `<>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal) | 不等于运算符 |
| [NOT IN()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in) | 检查值是否不在一组值中 |
| [NOT LIKE](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like) | 简单模式匹配的否定 |
| [STRCMP()](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp) | 比较两个字符串 |

详情请参见 [比较函数和运算符](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html)。

## 逻辑运算符

| 名称 | 描述 |
| ---------------------------------------- | ------------- |
| [AND, &&](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_and) | 逻辑与 |
| [NOT, !](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_not) | 取反值 |
| [\|\|, OR](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_or) | 逻辑或 |
| [XOR](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_xor) | 逻辑异或 |

详情请参见 [MySQL 对 GROUP BY 的处理](https://dev.mysql.com/doc/refman/8.0/en/group-by-handling.html)。

## 赋值运算符

| 名称 | 描述 |
| ---------------------------------------- | ---------------------------------------- |
| [=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-equal) | 赋值（作为 [`SET`](https://dev.mysql.com/doc/refman/8.0/en/set-variable.html) 语句的一部分，或作为 [`UPDATE`](https://dev.mysql.com/doc/refman/8.0/en/update.html) 语句中 `SET` 子句的一部分） |
| [:=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-value) | 赋值 |

详情请参见 [函数依赖性检测](https://dev.mysql.com/doc/refman/8.0/en/group-by-functional-dependence.html)。

## MySQL 兼容性

* MySQL 不支持 `ILIKE` 运算符。
