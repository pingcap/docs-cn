---
title: 字面值
category: user guide
---

# 字面值

## String Literals

String Literals 是一个 bytes 或者 characters 的序列，两端被单引号 `'` 或者双引号 `"` 包围，例如：

```
'example string'
"example string"
```

如果字符串是连续的，会被合并为一个独立的 string。以下表示是一样的：

```
'a string'
'a' ' ' 'string'
"a" ' ' "string"
```

如果 `ANSI_QUOTES` SQL MODE 开启了，那么只有单引号内的会被认为是 String Literals，对于双引号内的字符串，会被认为是一个 identifier。

binary string 是一串 bytes 组成的字符串，每一个 binary string 有一个叫做 `binary` 的 character set 和 collation。一个非二进制的字符串是一个由字符组成的字符串，它有除 `binary` 外的 character set和与之兼容的 collation。

对于两种字符串类型，比较都是基于每个字符的数值。对于 binary string 而言，比较单元就是字节，对于非二进制的字符串，那么单元就是字符，而有的字符集支持多字节字符。

一个 String Literal 可以拥有一个可选的 `character set introducer` 和 `COLLATE clause`，可以用来指派特定的字符集跟 collation（TiDB 对此只是做了语法上的兼容，并不实质做处理)。

```
[_charset_name]'string' [COLLATE collation_name]
```

例如：

```
SELECT _latin1'string';
SELECT _binary'string';
SELECT _utf8'string' COLLATE utf8_bin;
```

你可以使用 N'literal' 或者 n'literal' 来创建使用 national character set 的字符串，下列语句是一样的：

```
SELECT N'some text';
SELECT n'some text';
SELECT _utf8'some text';
```

转义字符：

- \\0: ASCII NUL (X'00') 字符
- \\': 单引号
- \\": 双引号
- \\b: 退格符号
- \\n: 换行符
- \\r: 回车符
- \\t: tab 符（制表符）
- \\z: ASCII 26 (Ctrl + Z)
- \\\: 反斜杠 \\
- \\%: \%
- \\_: \_

如果要在 string literal 中使用 `'` 或者 `"`，有以下几种办法：

* 在 `'` 引用的字符串中，可以用 `''` 来表示单引号。
* 在 `"` 引用的字符串中，可以用 `""` 来表示双引号。
* 前面接转义符`\`。
* 在 `'` 中表示 `"` 或者在 `"` 中表示 `'` 都不需要特别的处理。

更多[细节](https://dev.mysql.com/doc/refman/5.7/en/string-literals.html)。

## Numeric Literals

数值字面值包括 integer 跟 Decimal 类型跟浮点数字面值。

integer 可以包括 `.` 作为小数点分隔，数字前可以有 `-` 或者 `+` 来表示正数或者负数。

精确数值字面值可以表示为如下格式：`1, .2, 3.4, -5, -6.78, +9.10`.

科学记数法也是被允许的，表示为如下格式：`1.2E3, 1.2E-3, -1.2E3, -1.2E-3`。

更多[细节](https://dev.mysql.com/doc/refman/5.7/en/number-literals.html)。

## NULL Values

`NULL` 代表数据为空，它是大小写不敏感的，与 `\N`(大小写敏感) 同义。

需要注意的是 `NULL` 跟 `0` 并不一样，跟空字符串 `''` 也不一样。

## Hexadecimal Literals

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

```
mysql> select X'aff';
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

```
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

## Date and Time Literals

Date 跟 Time 字面值有几种格式，例如用字符串表示，或者直接用数字表示。在 TiDB 里面，当 TiDB 期望一个 Date 的时候，它会把 `'2017-08-24'`， `'20170824'`，`20170824` 当做是 Date。

TiDB 的 Date 值有以下几种格式：

* `'YYYY-MM-DD'` 或者 `'YY-MM-DD'`，这里的 `-` 分隔符并不是严格的，可以是任意的标点符号。比如 `'2017-08-24'`，`'2017&08&24'`， `'2012@12^31'` 都是一样的。唯一需要特别对待的是 '.' 号，它被当做是小数点，用于分隔整数和小数部分。
 Date 和 Time 部分可以被 'T' 分隔，它的作用跟空格符是一样的，例如 `2017-8-24 10:42:00` 跟 `2017-8-24T10:42:00` 是一样的。
* `'YYYYMMDDHHMMSS'` 或者 `'YYMMDDHHMMSS'`，例如 `'20170824104520'` 和 `'170824104520'` 被当做是 `'2017-08-24 10:45:20'`，但是如果你提供了一个超过范围的值，例如`'170824304520'`，那这就不是一个有效的 Date 字面值。
* `YYYYMMDDHHMMSS` 或者 `YYMMDDHHMMSS` 注意这里没有单引号或者双引号，是一个数字。例如 `20170824104520`表示为 `'2017-08-24 10:45:20'`。

DATETIME 或者 TIMESTAMP 值可以接一个小数部分，用来表示微秒（精度最多到小数点后 6 位），用小数点 `.` 分隔。

Dates 如果 year 部分只有两个数字，这是有歧义的（推荐使用四个数字的格式），TiDB 会尝试用以下的规则来解释：

* year 值如果在 `70-99` 范围，那么被转换成 `1970-1999`。
* year 值如果在 `00-69` 范围，那么被转换成 `2000-2069`。

对于小于 10 的 month 或者 day 值，`'2017-8-4'` 跟 `'2017-08-04'` 是一样的。对于 Time 也是一样，比如 `'2017-08-24 1:2:3'` 跟 `'2017-08-24 01:02:03'`是一样的。

在需要 Date 或者 Time 的语境下, 对于数值，TiDB 会根据数值的长度来选定指定的格式：

* 6 个数字，会被解释为 `YYMMDD`。
* 12 个数字，会被解释为 `YYMMDDHHMMSS`。
* 8 个数字，会解释为 `YYYYMMDD`。
* 14 个数字，会被解释为 `YYYYMMDDHHMMSS`。

对于 Time 类型，TiDB 用以下格式来表示：

* `'D HH:MM:SS'`，或者 `'HH:MM:SS'`，`'HH:MM'`，`'D HH:MM'`，`'D HH'`，`'SS'`，这里的 D 表示 days，合法的范围是 `0-34`。
* 数值 `HHMMSS`，例如 `231010` 被解释为`'23:10:10'`。
* 数值 `SS`，`MMSS`，`HHMMSS` 都是可以被当做 Time。

Time 类型的小数点也是 `.`，精度最多小数点后 6 位。

更多[细节](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-literals.html)。

## Boolean Literals

常量 `TRUE` 和 `FALSE` 等于 1 和 0，它是大小写不敏感的。

```
mysql> SELECT TRUE, true, tRuE, FALSE, FaLsE, false;
+------+------+------+-------+-------+-------+
| TRUE | true | tRuE | FALSE | FaLsE | false |
+------+------+------+-------+-------+-------+
|    1 |    1 |    1 |     0 |     0 |     0 |
+------+------+------+-------+-------+-------+
1 row in set (0.00 sec)
```

## Bit-Value Literals

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
