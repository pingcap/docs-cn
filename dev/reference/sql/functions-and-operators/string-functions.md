---
title: 字符串函数
category: reference
---

# 字符串函数

TiDB 支持使用 MySQL 5.7 中提供的大部分[字符串函数](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html)。

## 支持的函数

| 函数名   | 功能描述          |
|:----------|:-----------------------|
| [`ASCII()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ascii)  | 返回最左字符的数值       |
| [`BIN()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_bin)      | 返回一个数的二进制值的字符串表示   |
| [`BIT_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_bit-length)  | 返回字符串的位长度 |
| [`CHAR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_char)    | 返回由整数的代码值所给出的字符组成的字符串  |
| [`CHAR_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_char-length)  | 返回字符串的字符长度  |
| [`CHARACTER_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_character-length)   | 与 `CHAR_LENGTH()` 功能相同   |
| [`CONCAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_concat)      | 返回连接的字符串  |
| [`CONCAT_WS()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_concat-ws)   | 返回由分隔符连接的字符串   |
| [`ELT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_elt)  | 返回指定位置的字符串  |
| [`EXPORT_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_export-set)  | 返回一个字符串，其中值位中设置的每个位，可以得到一个 on 字符串，而每个未设置的位，可以得到一个 off 字符串  |
| [`FIELD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_field)  | 返回参数在后续参数中出现的第一个位置  |
| [`FIND_IN_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_find-in-set)  | 返回第一个参数在第二个参数中出现的位置 |
| [`FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_format)      | 返回指定小数位数格式的数字      |
| [`FROM_BASE64()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_from-base64)  | 解码 base-64 表示的字符串，并返回结果 |
| [`HEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_hex)  | 返回一个十进制数或字符串值的 16 进制表示  |
| [`INSERT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_insert)  | 在指定位置插入一个子字符串，最多不超过指定字符数  |
| [`INSTR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_instr)  | 返回第一次出现的子字符串的索引  |
| [`LCASE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lcase)  | 与 `LOWER()` 功能相同  |
| [`LEFT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_left)  | 返回最左侧指定长度的字符  |
| [`LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_length)  | 返回字符串长度，单位为字节 |
| [`LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like)  | 进行简单模式匹配  |
| [`LOCATE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_locate)  | 返回第一次出现的子字符串的位置 |
| [`LOWER()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lower)  | 返回全小写的参数  |
| [`LPAD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lpad)  | 返回字符串参数，左侧添加指定字符串 |
| [`LTRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ltrim)  | 去掉前缀空格 |
| [`MAKE_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_make-set)  | 返回一组用逗号分隔的字符串，这些字符串的位数与给定的 bits 参数对应  |
| [`MID()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_mid) | 返回一个以指定位置开始的子字符串   |
| [`NOT LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like) | 否定简单模式匹配    |
| [`NOT REGEXP`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_not-regexp)   | `REGEXP` 的否定形式  |
| [`OCT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_oct)    | 返回一个数值的八进制表示，形式为字符串  |
| [`OCTET_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_octet-length)   | 与 `LENGTH()` 功能相同   |
| [`ORD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ord)    | 返回该参数最左侧字符的字符编码   |
| [`POSITION()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_position)  | 与 `LOCATE()` 功能相同   |
| [`QUOTE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_quote)   | 使参数逃逸，为了在 SQL 语句中使用   |
| [`REGEXP`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)  | 使用正则表达式匹配模式  |
| [`REPEAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_repeat)   | 以指定次数重复一个字符串    |
| [`REPLACE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_replace)  | 替换所有出现的指定字符串   |
| [`REVERSE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_reverse)   | 反转字符串里的所有字符  |
| [`RIGHT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_right)    | 返回指定数量的最右侧的字符        |
| [`RLIKE`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)    | 与 `REGEXP` 功能相同 |
| [`RPAD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_rpad)  | 以指定次数添加字符串  |
| [`RTRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_rtrim)    | 去掉后缀空格  |
| [`SPACE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_space)   | 返回指定数量的空格，形式为字符串 |
| [`STRCMP()`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#function_strcmp) | 比较两个字符串  |
| [`SUBSTR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substr)      | 返回指定的子字符串 |
| [`SUBSTRING()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substring)  | 返回指定的子字符串   |
| [`SUBSTRING_INDEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substring-index)  | 从一个字符串中返回指定出现次数的定界符之前的子字符串  |
| [`TO_BASE64()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_to-base64)  | 返回转化为 base-64 表示的字符串参数   |
| [`TRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_trim)   | 去掉前缀和后缀空格 |
| [`UCASE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ucase)       | 与 `UPPER()` 功能相同   |
| [`UNHEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_unhex)  | 返回一个数的十六进制表示，形式为字符串 |
| [`UPPER()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_upper)   | 参数转换为大写形式  |

## 不支持的函数

* `LOAD_FILE()`
* `MATCH`
* `SOUNDEX()`
* `SOUNDS LIKE`
* `WEIGHT_STRING()`
