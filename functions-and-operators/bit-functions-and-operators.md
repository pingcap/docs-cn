---
title: 位函数和操作符
summary: TiDB 支持 MySQL 5.7 中的所有位函数和操作符，包括BIT_COUNT()、&、~、|、^、<<和>>。BIT_COUNT() 返回参数二进制表示中为 1 的个数，& 表示位与，~ 表示按位取反，| 表示位或，^ 表示位亦或，<< 表示左移，>> 表示右移。
---

# 位函数和操作符

TiDB 支持使用 MySQL 5.7 中提供的所有[位函数和操作符](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html)。

**位函数和操作符表**

| 函数和操作符名 | 功能描述 |
| -------------- | ------------------------------------- |
| [`BIT_COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#function_bit-count) | 返回参数二进制表示中为 1 的个数 |
| [&](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-and) | 位与 |
| [~](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-invert) | 按位取反 |
| [\|](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-or) | 位或 |
| [^](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-xor) | 位亦或 |
| [<<](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_left-shift) | 左移 |
| [>>](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_right-shift) | 右移 |
