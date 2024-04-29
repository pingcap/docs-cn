---
title: 位函数和操作符
---

# 位函数和操作符

TiDB 支持使用 MySQL 8.0 中提供的所有[位函数和操作符](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html)。

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

## MySQL 兼容性

在处理位函数和操作符时，MySQL 8.0 与之前版本的 MySQL 之间存在一些差异。TiDB 旨在遵循 MySQL 8.0 的行为。

## 已知问题

在以下情况中，TiDB 中的查询结果与 MySQL 5.7 相同，但与 MySQL 8.0 不同。

- 二进制参数的位操作。更多信息，请参考 [#30637](https://github.com/pingcap/tidb/issues/30637)。
- `BIT_COUNT()` 函数的结果。更多信息，请参考 [#44621](https://github.com/pingcap/tidb/issues/44621)。