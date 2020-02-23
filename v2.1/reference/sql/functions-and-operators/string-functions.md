---
title: 字符串函数
category: reference
---

# 字符串函数

| 函数名   | 功能描述          |
|:----------|:-----------------------|
| [`ASCII()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ascii)  | 返回最左字符的数值       |
| [`CHAR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_char)    | 返回由整数的代码值所给出的字符组成的字符串    |
| [`BIN()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_bin)      | 返回一个数的二进制值的字符串表示   |
| [`HEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_hex)      | 返回十进制值或字符串值的十六进制表示                                                                          |
| [`OCT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_oct)      | 返回一个数的八进制值的字符串表示                                                                               |
| [`UNHEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_unhex)       | 返回 HEX 表示的数字所代表的字符串                                                                                 |
| [`TO_BASE64()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_to-base64)                 | 返回转换为 BASE64 的字符串参数                                                                                         |
| [`FROM_BASE64()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_from-base64)             | 解码为 BASE64 的字符串并返回结果                                                                                              |
| [`LOWER()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lower)                         | 返回小写字母的字符                                                                                                          |
| [`LCASE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lcase)                         | 与 `LOWER()` 功能相同                                                                                                                       |
| [`UPPER()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_upper)                         | 返回大写字母的字符                                                                                                                     |
| [`UCASE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ucase)                         | 与 `UPPER()` 功能相同                                                                                                                       |
| [`LPAD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lpad)                           | 返回左边由指定字符串填充的字符串参数                                                                         |
| [`RPAD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_rpad)                           | 返回右边由指定字符串填充的字符串参数                                                                                               |
| [`TRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_trim)                           | 删除字符串的前缀和后缀                                                                                                        |
| [`LTRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ltrim)                         | 删除前面的空格字符                                                                                                             |
| [`RTRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_rtrim)                         | 删除结尾的空格字符                                                                                                                    |
| [`BIT_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_bit-length)               | 返回字符串的位长度                                                                                                        |
| [`CHAR_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_char-length)             | 返回字符串的字符长度                                                                                                   |
| [`CHARACTER_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_character-length)   | 与 `CHAR_LENGTH()` 功能相同                                                                                                                 |
| [`LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_length)                       | 返回字符串的字节长度                                                                                                    |
| [`OCTET_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_octet-length)           | 与 `LENGTH()` 功能相同                                                                                                                      |
| [`INSERT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_insert)                       | 在指定位置插入一个子字符串，直到指定的字符数                                                     |
| [`REPLACE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_replace)                     | 替换指定的字符串                                                                                                 |
| [`SUBSTR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substr)                       | 返回指定的子字符串                                                                                                         |
| [`SUBSTRING()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substring)                 | 返回指定的子字符串                                                                                                         |
| [`SUBSTRING_INDEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substring-index)     | 返回最终定界符左边或右边的子字符串                                              |
| [`MID()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_mid)                         | 返回从指定位置开始的子字符串                                                                                   |
| [`LEFT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_left)                           | 返回指定的最左字符                                                                                     |
| [`RIGHT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_right)                         | 返回指定的最右字符                                                                                       |
| [`INSTR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_instr)                         | 返回子字符串的第一个出现位置                                                                                      |
| [`LOCATE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_locate)                       | 返回子字符串的第一个出现位置，与 `INSTR()` 的参数位置相反                                                                                   |
| [`POSITION()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_position)                   | 与 `LOCATE()` 功能相同                                                                                                                      |
| [`REPEAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_repeat)                       | 返回重复指定次数的字符串                                                                                             |
| [`CONCAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_concat)                       | 返回连接的字符串                                                                                                                |
| [`CONCAT_WS()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_concat-ws)                 | 返回由分隔符连接的字符串                                                                                                         |
| [`REVERSE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_reverse)                     | 返回和字符顺序相反的字符串                                                                                                        |
| [`SPACE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_space)                       | 返回指定数目的空格组成的字符串                                                                                          |
| [`FIELD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_field)                         | 返回参数在后续参数中出现的第一个位置                                                             |
| [`ELT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_elt)                             | 返回指定位置的字符串                                                                                                             |
| [`EXPORT_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_export-set)               | 返回一个字符串，其中值位中设置的每个位，可以得到一个 on 字符串，而每个未设置的位，可以得到一个 off 字符串        |
| [`MAKE_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_make-set)                   | 返回一组逗号分隔的字符串，由位集合中具有相应位的字符串组成                                                    |
| [`FIND_IN_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_find-in-set)             | 返回第一个参数在第二个参数中出现的位置                                                                |
| [`FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_format)                       | 返回指定小数位数格式的数字                                                                           |
| [`ORD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ord)                             | 返回参数中最左字符的字符代码                                                                              |
| [`QUOTE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_quote)                         | 引用一个字符串，返回一个在 SQL 语句中可用作正确转义的数据值的结果                                                                                           |

## 字符串比较函数

| 函数名                                                                                                              | 功能描述                                                                                                                               |
|:------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|
| [`LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like)                  | 进行简单模式匹配                                                                                                                   |
| [`NOT LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like)          | 否定简单模式匹配                                                                                                       |
| [`STRCMP()`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#function_strcmp)            | 比较两个字符串                                                                                                                       |

## 正则表达式

| 表达式名                                                                                                              | 功能描述                                                                                                                               |
|:------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|
| [`REGEXP`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)                                   | 使用正则表达式进行模式匹配                                                                                                |
| [`RLIKE`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)                                    | 与 `REGEXP` 功能相同                                                                                                                        |
| [`NOT REGEXP`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_not-regexp)                           | 否定 `REGEXP`                                                                                                                        |
