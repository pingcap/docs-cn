---
title: Bit-value Literals
category: user guide
---

# Bit-value Literals

位值字面值用 `b` 或者 `0b` 做前缀，后接以 0 跟 1 组成的二进制数字。其中 `0b` 是区分大小写的，`0B` 是会报错的。

合法的 Bit-value：

* b'01'
* B'01'
* 0b01


非法的 Bit-value：

* b'2' (2 不是二进制数值, 必须为 0 或 1)
* 0B01 (0B 必须是小写 0b)

默认情况，位值字面值是一个二进制字符串。

Bit-value 是作为二进制返回的，所以输出到 MySQL Client 可能会显示不出来，如果要转换为可打印的字符，可以使用内建函数 `BIN()` 或者 `HEX()`：

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
