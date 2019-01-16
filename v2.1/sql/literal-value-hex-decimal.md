---
title: 十六进制字面值
category: user guide
---

# 十六进制字面值

十六进制字面值是有 `X` 和 `0x` 前缀的字符串，后接表示十六进制的数字。注意 `0x` 是大小写敏感的，不能表示为 `0X`。

例:

```
X'ac12'
X'12AC'
x'ac12'
x'12AC'
0xac12
0x12AC
```

以下是不合法的十六进制字面值：

```
X'1z' (z 不是合法的十六进制值)
0X12AC (0X 必须用小写的 0x)
```

对于使用 `X'val'` 格式的十六进制字面值，`val` 必须要有一个数字，可以在前面补一个 0 来避免语法错误。

```sql
mysql> select X'aff';
ERROR 1105 (HY000): line 0 column 13 near ""hex literal: invalid hexadecimal format, must even numbers, but 3 (total length 13)
mysql> select X'0aff';
+---------+
| X'0aff' |
+---------+
|
       |
+---------+
1 row in set (0.00 sec)
```

默认情况，十六进制字面值是一个二进制字符串。

如果需要将一个字符串或者数字转换为十六进制字面值，可以使用内建函数 `HEX()`：

```sql
mysql> SELECT HEX('TiDB');
+-------------+
| HEX('TiDB') |
+-------------+
| 54694442    |
+-------------+
1 row in set (0.01 sec)

mysql> SELECT X'54694442';
+-------------+
| X'54694442' |
+-------------+
| TiDB        |
+-------------+
1 row in set (0.00 sec)
```
