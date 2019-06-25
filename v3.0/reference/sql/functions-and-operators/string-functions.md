---
title: String Functions
summary: Learn about the string functions in TiDB.
category: reference
aliases: ['/docs/sql/string-functions/']
---

# String Functions

TiDB supports most of the [string functions](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html) available in MySQL 5.7.

## Supported functions

| Name                                                                                                              | Description                                                                                                                               |
|:------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|
| [`ASCII()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ascii)                         | Return numeric value of left-most character                                                                                               |
| [`BIN()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_bin)                             | Return a string containing binary representation of a number                                                                              |
| [`BIT_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_bit-length)               | Return length of argument in bits                                                                                                         |
| [`CHAR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_char)                           | Return the character for each integer passed                                                                                              |
| [`CHAR_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_char-length)             | Return number of characters in argument                                                                                                   |
| [`CHARACTER_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_character-length)   | Synonym for `CHAR_LENGTH()`                                                                                                               |
| [`CONCAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_concat)                       | Return concatenated string                                                                                                                |
| [`CONCAT_WS()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_concat-ws)                 | Return concatenate with separator                                                                                                         |
| [`ELT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_elt)                             | Return string at index number                                                                                                             |
| [`EXPORT_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_export-set)               | Return a string such that for every bit set in the value bits, you get an on string and for every unset bit, you get an off string        |
| [`FIELD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_field)                         | Return the index (position) of the first argument in the subsequent arguments                                                             |
| [`FIND_IN_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_find-in-set)             | Return the index position of the first argument within the second argument                                                                |
| [`FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_format)                       | Return a number formatted to specified number of decimal places                                                                           |
| [`FROM_BASE64()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_from-base64)             | Decode to a base-64 string and return result                                                                                              |
| [`HEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_hex)                             | Return a hexadecimal representation of a decimal or string value                                                                          |
| [`INSERT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_insert)                       | Insert a substring at the specified position up to the specified number of characters                                                     |
| [`INSTR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_instr)                         | Return the index of the first occurrence of substring                                                                                     |
| [`LCASE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lcase)                         | Synonym for `LOWER()`                                                                                                                     |
| [`LEFT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_left)                           | Return the leftmost number of characters as specified                                                                                     |
| [`LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_length)                       | Return the length of a string in bytes                                                                                                    |
| [`LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like)                  | Simple pattern matching                                                                                                                   |
| [`LOCATE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_locate)                       | Return the position of the first occurrence of substring                                                                                  |
| [`LOWER()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lower)                         | Return the argument in lowercase                                                                                                          |
| [`LPAD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lpad)                           | Return the string argument, left-padded with the specified string                                                                         |
| [`LTRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ltrim)                         | Remove leading spaces                                                                                                                     |
| [`MAKE_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_make-set)                   | Return a set of comma-separated strings that have the corresponding bit in bits set                                                       |
| [`MID()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_mid)                             | Return a substring starting from the specified position                                                                                   |
| [`NOT LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like)          | Negation of simple pattern matching                                                                                                       |
| [`NOT REGEXP`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_not-regexp)                           | Negation of `REGEXP`                                                                                                                      |
| [`OCT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_oct)                             | Return a string containing octal representation of a number                                                                               |
| [`OCTET_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_octet-length)           | Synonym for `LENGTH()`                                                                                                                    |
| [`ORD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ord)                             | Return character code for leftmost character of the argument                                                                              |
| [`POSITION()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_position)                   | Synonym for `LOCATE()`                                                                                                                    |
| [`QUOTE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_quote)                         | Escape the argument for use in an SQL statement                                                                                           |
| [`REGEXP`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)                                   | Pattern matching using regular expressions                                                                                                |
| [`REPEAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_repeat)                       | Repeat a string the specified number of times                                                                                             |
| [`REPLACE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_replace)                     | Replace occurrences of a specified string                                                                                                 |
| [`REVERSE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_reverse)                     | Reverse the characters in a string                                                                                                        |
| [`RIGHT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_right)                         | Return the specified rightmost number of characters                                                                                       |
| [`RLIKE`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)                                    | Synonym for `REGEXP`                                                                                                                      |
| [`RPAD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_rpad)                           | Append string the specified number of times                                                                                               |
| [`RTRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_rtrim)                         | Remove trailing spaces                                                                                                                    |
| [`SPACE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_space)                         | Return a string of the specified number of spaces                                                                                         |
| [`STRCMP()`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#function_strcmp)            | Compare two strings                                                                                                                       |
| [`SUBSTR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substr)                       | Return the substring as specified                                                                                                         |
| [`SUBSTRING()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substring)                 | Return the substring as specified                                                                                                         |
| [`SUBSTRING_INDEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substring-index)     | Return a substring from a string before the specified number of occurrences of the delimiter                                              |
| [`TO_BASE64()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_to-base64)                 | Return the argument converted to a base-64 string                                                                                         |
| [`TRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_trim)                           | Remove leading and trailing spaces                                                                                                        |
| [`UCASE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ucase)                         | Synonym for `UPPER()`                                                                                                                     |
| [`UNHEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_unhex)                         | Return a string containing hex representation of a number                                                                                 |
| [`UPPER()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_upper)                         | Convert to uppercase                                                                                                                      |

## Unsupported functions

* `LOAD_FILE()`
* `MATCH`
* `SOUNDEX()`
* `SOUNDS LIKE`
* `WEIGHT_STRING()`

