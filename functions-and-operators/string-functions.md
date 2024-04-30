---
title: 字符串函数
aliases: ['/docs-cn/dev/functions-and-operators/string-functions/','/docs-cn/dev/reference/sql/functions-and-operators/string-functions/','/docs-cn/dev/sql/string-functions/']
summary: TiDB 支持 MySQL 8.0 中提供的大部分字符串函数以及 Oracle 21 中提供的部分函数。
---

# 字符串函数

TiDB 支持使用 MySQL 8.0 中提供的大部分[字符串函数](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html)以及 Oracle 21 中提供的部分[函数](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlqr/SQL-Functions.html#GUID-93EC62F8-415D-4A7E-B050-5D5B2C127009)。

关于 Oracle 函数和 TiDB 函数的对照关系，请参考 [Oracle 与 TiDB 函数和语法差异对照](/oracle-functions-to-tidb.md)。

## 支持的函数

### [`ASCII()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ascii)

`ASCII()` 函数用于获取输入的参数中最左字符的 ASCII 值。该参数可以为字符串或数字。

- 如果输入参数不为空，该函数返回参数中最左字符的 ASCII 值。
- 如果输入参数为空字符串，该函数返回 `0`。
- 如果输入参数为 `NULL`，该函数返回 `NULL`。

> **注意：**
>
> `ASCII()` 只能处理那些用 8 个二进制数字（即单个字节）来表示的字符。

查询示例：

```sql
SELECT ASCII('A'), ASCII('TiDB'), ASCII(23);
```

返回结果：

```sql
+------------+---------------+-----------+
| ASCII('A') | ASCII('TiDB') | ASCII(23) |
+------------+---------------+-----------+
|         65 |            84 |        50 |
+------------+---------------+-----------+
```

### [`BIN()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bin)

`BIN()` 函数用于将输入的参数转换为其二进制值的字符串表示形式。该参数可以为字符串或数字。

- 如果输入参数为正数，该函数返回该参数的二进制值的字符串表示形式。
- 如果输入参数为负数，该函数会将该参数的绝对值转换为其二进制值，然后对二进制值的每位取反（`0` 变为 `1`，`1` 变为 `0`），最后加上 `1`。
- 如果输入参数为字符串，且该字符串中只包含数字，该函数将按照该数字返回结果。例如，`"123"` 与 `123` 的返回结果相同。
- 如果输入参数为字符串，且该字符串第一个字符不是数字（如 `"q123"`），该函数返回 `0`。
- 如果输入参数为字符串，且该字符串由数字和非数字组成，该函数将按照该参数中最前面连续的数字返回结果。例如，`'123q123'` 与 `123` 的返回结果相同，但 `BIN('123q123')` 会产生一个 `Truncated incorrect INTEGER value: '123q123'` 的警告。
- 如果输入参数为 `NULL`，该函数返回 `NULL`。

查询示例 1：

```sql
SELECT BIN(123), BIN('123q123');
```

返回结果 1：

```sql
+----------+----------------+
| BIN(123) | BIN('123q123') |
+----------+----------------+
| 1111011  | 1111011        |
+----------+----------------+
```

查询示例 2：

```sql
SELECT BIN(-7);
```

返回结果 2：

```sql
+------------------------------------------------------------------+
| BIN(-7)                                                          |
+------------------------------------------------------------------+
| 1111111111111111111111111111111111111111111111111111111111111001 |
+------------------------------------------------------------------+
```

### [`BIT_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bit-length)

`BIT_LENGTH()` 函数用于返回输入参数的长度，单位为 bit。

示例：

```sql
SELECT BIT_LENGTH("TiDB");

+--------------------+
| BIT_LENGTH("TiDB") |
+--------------------+
|                 32 |
+--------------------+
```

每个字符 8 位 x 4 个字符 = 32 位

```sql
SELECT BIT_LENGTH("PingCAP 123");

+---------------------------+
| BIT_LENGTH("PingCAP 123") |
+---------------------------+
|                        88 |
+---------------------------+
```

每个字符 8 位（空格也会被计算在内，因为它是非字母数字字符） x 11 个字符 = 88 位

```sql
SELECT CustomerName, BIT_LENGTH(CustomerName) AS BitLengthOfName FROM Customers;

+--------------------+-----------------+
| CustomerName       | BitLengthOfName |
+--------------------+-----------------+
| Albert Einstein    |             120 |
| Robert Oppenheimer |             144 |
+--------------------+-----------------+
```

> **注意：**
>
> 上面这个示例假设数据库中存在一个名为 `Customers` 的表，表中有一个名为 `CustomerName` 的列。

### [`CHAR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char)

`CHAR()` 函数用于获取指定 ASCII 值的对应字符。该函数执行的操作与 `ASCII()` 相反，`ASCII()` 用于返回指定字符的 ASCII 值。如果提供了多个参数，`CHAR()` 函数将作用于所有参数并将它们的结果拼接在一起返回。

示例：

```sql
SELECT CHAR(65);

+------------+
|  CHAR(65)  |
+------------+
|          A |
+------------+
```

```sql
SELECT CHAR(84);

+------------+
|  CHAR(84)  |
+------------+
|          T |
+------------+
```

`CHAR()` 函数还可用于获取超出标准 ASCII 范围（`0` - `127`）的 ASCII 值的对应字符。

```sql
/*For extended ASCII: */

SELECT CHAR(128);

+------------+
|  CHAR(128) |
+------------+
|       0x80 |
+------------+
```

`CHAR()` 函数还可用于获取 Unicode 值的对应字符。

```sql
/* For Unicode: */

--skip-binary-as-hex

SELECT CHAR(50089);

+--------------+
|  CHAR(50089) |
+--------------+
|            é |
+--------------+
```

```sql
SELECT CHAR(65,66,67);
```

```
+----------------+
| CHAR(65,66,67) |
+----------------+
| ABC            |
+----------------+
1 row in set (0.00 sec)
```

### [`CHAR_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char-length)

`CHAR_LENGTH()` 函数用于获取输入参数中字符的总数。

示例：

```sql
SELECT CHAR_LENGTH("TiDB") AS LengthOfString;

+----------------+
| LengthOfString |
+----------------+
|              4 |
+----------------+
```

```sql
SELECT CustomerName, CHAR_LENGTH(CustomerName) AS LengthOfName FROM Customers;

+--------------------+--------------+
| CustomerName       | LengthOfName |
+--------------------+--------------+
| Albert Einstein    |           15 |
| Robert Oppenheimer |           18 |
+--------------------+--------------+
```

> **注意：**
>
> 上面这个示例假设数据库中存在一个名为 `Customers` 的表，表中有一个名为 `CustomerName` 的列。

### [`CHARACTER_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_character-length)

`CHARACTER_LENGTH()` 函数与 `CHAR_LENGTH()` 函数功能相同，返回结果相同，可以互换使用。

### [`CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat)

`CONCAT()` 函数用于将输入的参数连接成一个字符串。

语法：

```sql
CONCAT(str1,str2,...)
```

`str1, str2, ...` 为要连接的参数。该参数可以是字符串或数字。

查询示例：

```sql
SELECT CONCAT('TiDB', ' ', 'Server', '-', 1, TRUE);
```

返回结果：

```sql
+---------------------------------------------+
| CONCAT('TiDB', ' ', 'Server', '-', 1, TRUE) |
+---------------------------------------------+
| TiDB Server-11                              |
+---------------------------------------------+
```

如果任一参数的值为 `NULL`， 则 `CONCAT()` 返回 `NULL`。

查询示例：

```sql
SELECT CONCAT('TiDB', NULL, 'Server');
```

返回结果：

```sql
+--------------------------------+
| CONCAT('TiDB', NULL, 'Server') |
+--------------------------------+
| NULL                           |
+--------------------------------+
```

除了使用 `CONCAT()` 函数外，你也可以通过字符串彼此相邻的方式获取拼接字符串，但是该方式不支持数字类型。例如：

```sql
SELECT 'Ti' 'DB' ' ' 'Server';
```

返回结果：

```sql
+-------------+
| Ti          |
+-------------+
| TiDB Server |
+-------------+
```

### [`CONCAT_WS()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat-ws)

`CONCAT_WS()` 函数是一种带分隔符的 [`CONCAT()`](#concat)，返回由分隔符连接的字符串。

语法：

```sql
CONCAT_WS(separator,str1,str2,...)
```

- `separator`：第一个参数为分隔符，用于连接其余的不为 `NULL` 的参数。
- `str1, str2, ...`：要连接的参数。该参数可以为字符串或数字。

查询示例：

```sql
SELECT CONCAT_WS(',', 'TiDB Server', 'TiKV', 'PD');
```

返回结果：

```sql
+---------------------------------------------+
| CONCAT_WS(',', 'TiDB Server', 'TiKV', 'PD') |
+---------------------------------------------+
| TiDB Server,TiKV,PD                         |
+---------------------------------------------+
```

- 如果分隔符为空，则 `CONCAT_WS()` 等效于 `CONCAT()`，返回其余参数连接后的字符串。

    查询示例：

    ```sql
    SELECT CONCAT_WS('', 'TiDB Server', 'TiKV', 'PD');
    ```

    返回结果：

    ```sql
    +--------------------------------------------+
    | CONCAT_WS('', 'TiDB Server', 'TiKV', 'PD') |
    +--------------------------------------------+
    | TiDB ServerTiKVPD                          |
    +--------------------------------------------+
    ```

- 如果分隔符为 `NULL`，则 `CONCAT_WS()`返回 `NULL`。

    查询示例：

    ```sql
    SELECT CONCAT_WS(NULL, 'TiDB Server', 'TiKV', 'PD');
    ```

    返回结果：

    ```sql
    +----------------------------------------------+
    | CONCAT_WS(NULL, 'TiDB Server', 'TiKV', 'PD') |
    +----------------------------------------------+
    | NULL                                         |
    +----------------------------------------------+
    ```

- 如果用于连接的参数中只有一个不为 `NULL`，则 `CONCAT_WS()` 返回此参数。

    查询示例：

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', NULL);
    ```

    返回结果：

    ```sql
    +-------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', NULL) |
    +-------------------------------------+
    | TiDB Server                         |
    +-------------------------------------+
    ```

- 如果用于连接的参数中有 `NULL`，`CONCAT_WS()`会忽略 `NULL`。

    查询示例：

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', NULL, 'PD');
    ```

    返回结果：

    ```sql
    +-------------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', NULL, 'PD') |
    +-------------------------------------------+
    | TiDB Server,PD                            |
    +-------------------------------------------+
    ```

- 如果用于连接的参数中有空字符串，`CONCAT_WS()` 不会忽略该字符串。

    查询示例：

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', '', 'PD');
    ```

    返回结果：

    ```sql
    +-----------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', '', 'PD') |
    +-----------------------------------------+
    | TiDB Server,,PD                         |
    +-----------------------------------------+
    ```

### [`ELT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_elt)

`ELT()` 函数返回索引号对应的元素。

```sql
SELECT ELT(3, 'This', 'is', 'TiDB');
```

```sql
+------------------------------+
| ELT(3, 'This', 'is', 'TiDB') |
+------------------------------+
| TiDB                         |
+------------------------------+
1 row in set (0.00 sec)
```

在以上示例中，该函数返回第三个元素，即 `'TiDB'`。

### [`EXPORT_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_export-set)

`EXPORT_SET()` 函数返回一个由指定数量 (`number_of_bits`) 的 `on`/`off` 值组成的字符串，各个值之间可以用 `separator` 分隔（可选）。这些值将基于输入的 `bits` 参数中的相应 bit 是否为 `1` 而确定，其中第一个值对应于 `bits` 中的最右边（即最低）的 bit。

语法：

```sql
EXPORT_SET(bits, on, off, [separator[, number_of_bits]])
```

- `bits`：一个代表 bits 值的整数。
- `on`：如果对应的 bit 为 `1`，则返回该字符串。
- `off`：如果对应的 bit 为 `0`，则返回该字符串。
- `separator`（可选）：输出字符串中的分隔符。
- `number_of_bits`（可选）：要处理的位数。如果未设置，则默认使用 `64`（最大位数），这意味着 `bits` 将被视为一个无符号 64 位整数。

示例：

在以下示例中，`number_of_bits` 设置为 `5`，因此该函数返回由 `|` 分隔的 5 个值。`'101'` 里的 bit 值只有三位，所以其他位被视为未设置。因此，将 `number_of_bits` 设置为 `101` 或设置为 `00101` 的返回结果相同。

```sql
SELECT EXPORT_SET(b'101',"ON",'off','|',5);
```

```sql
+-------------------------------------+
| EXPORT_SET(b'101',"ON",'off','|',5) |
+-------------------------------------+
| ON|off|ON|off|off                   |
+-------------------------------------+
1 row in set (0.00 sec)
```

在以下示例中，`bits` 设置为 `00001111`，`on` 设置为 `x`，`off` 设置为 `_`。这使函数在这些 `0` 位上返回 `____`，在这些 `1` 位上返回 `xxxx`。因此，从右到左处理 `00001111` 中的位时，该函数返回 `xxxx____`。

```sql
SELECT EXPORT_SET(b'00001111', 'x', '_', '', 8);
```

```sql
+------------------------------------------+
| EXPORT_SET(b'00001111', 'x', '_', '', 8) |
+------------------------------------------+
| xxxx____                                 |
+------------------------------------------+
1 row in set (0.00 sec)
```

在以下示例中，`bits` 设置为 `00001111`，`on` 设置为 `x`，`off` 设置为 `_`。这使函数在每个 `1` 位上返回 `x`，在每个 `0` 位上返回 `_`。因此，从右到左处理 `01010101` 中的位时，该函数返回 `x_x_x_x_`。

```sql
SELECT EXPORT_SET(b'01010101', 'x', '_', '', 8);
```

```sql
+------------------------------------------+
| EXPORT_SET(b'01010101', 'x', '_', '', 8) |
+------------------------------------------+
| x_x_x_x_                                 |
+------------------------------------------+
1 row in set (0.00 sec)
```

### [`FIELD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_field)

返回参数在后续参数中出现的第一个位置

在以下示例中，`FIELD()` 的第一个参数是 `needle`，它与后续列表中的第二个参数匹配，因此函数返回 `2`。

```sql
SELECT FIELD('needle', 'A', 'needle', 'in', 'a', 'haystack');
+-------------------------------------------------------+
| FIELD('needle', 'A', 'needle', 'in', 'a', 'haystack') |
+-------------------------------------------------------+
|                                                     2 |
+-------------------------------------------------------+
1 row in set (0.00 sec)
```

### [`FIND_IN_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_find-in-set)

返回第一个参数在第二个参数中出现的位置

该函数通常与 [`SET`](/data-type-string.md#set-类型) 数据类型一起使用。

在以下示例中，`Go` 是集合 `COBOL,BASIC,Rust,Go,Java,Fortran` 中的第四个元素，因此函数返回 `4`。

```sql
SELECT FIND_IN_SET('Go', 'COBOL,BASIC,Rust,Go,Java,Fortran');
+-------------------------------------------------------+
| FIND_IN_SET('Go', 'COBOL,BASIC,Rust,Go,Java,Fortran') |
+-------------------------------------------------------+
|                                                     4 |
+-------------------------------------------------------+
1 row in set (0.00 sec)
```

### [`FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_format)

`FORMAT(X,D[,locale])` 函数用于将数字 `X` 格式化为类似于 `“#,###,###.##”` 的格式，四舍五入保留 `D` 位小数，并将结果作为字符串返回。

参数：

- `X`：要格式化的数字。可以是直接的数字值、数字字符串、或科学记数法格式的数字。
- `D`：指定返回值的小数位数。该函数根据 `D` 对 `X` 进行四舍五入。如果 `D` 大于 `X` 的实际小数位数，则会在结果中填充相应长度的零。
- `[locale]`：指定一个区域设置，用于结果中数字的小数点、千位分隔符和分隔符之间的分组。合法的区域设置值与 [`lc_time_names`](https://dev.mysql.com/doc/refman/8.3/en/server-system-variables.html#sysvar_lc_time_names) 系统变量的合法值相同。如果未指定或者设置为 `NULL`，则默认使用 `'en_US'` 区域设置。该参数可选。

行为细节：

- 如果输入的第一个参数为字符串，且该字符串中只包含数字时，该函数将按照该数字返回结果。例如，`FORMAT('12.36', 1)` 与 `FORMAT(12.36, 1)` 的返回结果相同。
- 如果输入的第一个参数为科学计数法（`E/e`）表示的数字时，该函数将按照该数字返回结果。例如，`FORMAT('1E2', 3)`），函数返回 `100.000`。
- 如果输入的第一个参数为非数字开头的字符串时，该函数除了返回零值外，还返回一个警告 `(Code 1292)`。例如，`FORMAT('q12.36', 5)` 函数返回 `0.00000`，还会包含一个警告 `Warning (Code 1292): Truncated incorrect DOUBLE value: 'q12.36'`。
- 如果输入的第一个参数为数字和非数字混合的字符串时，该函数将基于该参数中开头连续的数字部分返回结果，还返回一个警告 `(Code 1292)`。例如，`FORMAT('12.36q56.78', 1)` 与 `FORMAT('12.36', 1)` 的返回的数字结果相同，但 `FORMAT('12.36q56.78', 1)` 还会包含一个警告 `Warning (Code 1292): Truncated incorrect DOUBLE value: '12.36q56.78'`。
- 如果输入的第二个参数为零或负数，该函数将四舍五入小数部分并返回整数。
- 如果输入的任意参数为 `NULL`，函数将返回 `NULL`。

示例：

格式化数字 12.36 到不同的小数位数：

```sql
mysql> SELECT FORMAT(12.36, 1);
+------------------+
| FORMAT(12.36, 1) |
+------------------+
| 12.4             |
+------------------+
```

```sql
mysql> SELECT FORMAT(12.36, 5);
+------------------+
| FORMAT(12.36, 5) |
+------------------+
| 12.36000         |
+------------------+
```

```sql
mysql> SELECT FORMAT(1234.56, 1, 'en_US');
+-----------------------------+
| FORMAT(1234.56, 1, 'en_US') |
+-----------------------------+
| 1,234.6                     |
+-----------------------------+
```

### [`FROM_BASE64()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_from-base64)

`FROM_BASE64(str)` 函数用于对 [Base64](https://datatracker.ietf.org/doc/html/rfc4648) 编码的字符串进行解码，并将解码结果以十六进制字符串的形式返回。

- 此函数接受一个单一参数，即需要解码的 Base64 编码字符串。
- 如果输入参数为 `NULL` 或无效的 Base64 编码字符串，`FROM_BASE64()` 函数将返回 `NULL`。

示例：

以下示例解码 Base64 编码的字符串 `'SGVsbG8gVGlEQg=='`，该字符串是 `'Hello TiDB'` 经过 [`TO_BASE64()`](#to_base64) 函数编码的结果。

```sql
mysql> SELECT TO_BASE64('Hello TiDB');
+-------------------------+
| TO_BASE64('Hello TiDB') |
+-------------------------+
| SGVsbG8gVGlEQg==        |
+-------------------------+

mysql> SELECT FROM_BASE64('SGVsbG8gVGlEQg==');
+------------------------------------------------------------------+
| FROM_BASE64('SGVsbG8gVGlEQg==')                                  |
+------------------------------------------------------------------+
| 0x48656C6C6F2054694442                                           |
+------------------------------------------------------------------+
```

```sql
mysql> SELECT CONVERT(FROM_BASE64('SGVsbG8gVGlEQg==') USING utf8mb4);
+--------------------------------------------------------+
| CONVERT(FROM_BASE64('SGVsbG8gVGlEQg==') USING utf8mb4) |
+--------------------------------------------------------+
| Hello TiDB                                             |
+--------------------------------------------------------+
```

以下示例解码 Base64 编码的数字 `MTIzNDU2`，该字符串是 `123456` 经过 [`TO_BASE64()`](#to_base64) 函数编码的结果。

```sql
mysql> SELECT FROM_BASE64('MTIzNDU2');
+--------------------------------------------------+
| FROM_BASE64('MTIzNDU2')                          |
+--------------------------------------------------+
| 0x313233343536                                   |
+--------------------------------------------------+
```

### [`HEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_hex)

`HEX()` 函数用于将输入的参数转换为其十六进制值的字符串表示形式。该参数可以为字符串或数字。

- 如果输入参数为字符串，`HEX(str)` 返回 `str` 的十六进制字符串表示。该函数将 `str` 中每个字符的每个字节转换为两个十六进制数字。例如，在 UTF-8 或 ASCII 字符集中，字符 `a` 的二进制表示为 `00111101`，十六进制表示为 `61`。
- 如果输入参数为数字，`HEX(n)` 返回 `n` 的十六进制字符串表示。该函数将参数 `n` 视为 `BIGINT` 数字，相当于 `CONV(n, 10, 16)`。
- 如果输入参数为 `NULL`，该函数返回 `NULL`。

示例：

```sql
SELECT X'616263', HEX('abc'), UNHEX(HEX('abc')), 0x616263;
+-----------+------------+-------------------+----------+
| X'616263' | HEX('abc') | UNHEX(HEX('abc')) | 0x616263 |
+-----------+------------+-------------------+----------+
| abc       | 616263     | abc               | abc      |
+-----------+------------+-------------------+----------+
```

```sql
SELECT X'F09F8DA3', HEX('🍣'), UNHEX(HEX('🍣')), 0xF09F8DA3;
+-------------+-------------+--------------------+------------+
| X'F09F8DA3' | HEX('🍣')     | UNHEX(HEX('🍣'))     | 0xF09F8DA3 |
+-------------+-------------+--------------------+------------+
| 🍣            | F09F8DA3    | 🍣                   | 🍣           |
+-------------+-------------+--------------------+------------+
```

```sql
SELECT HEX(255), CONV(HEX(255), 16, 10);
+----------+------------------------+
| HEX(255) | CONV(HEX(255), 16, 10) |
+----------+------------------------+
| FF       | 255                    |
+----------+------------------------+
```

```sql
SELECT HEX(NULL);
+-----------+
| HEX(NULL) |
+-----------+
| NULL      |
+-----------+
```

### [`INSERT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_insert)

`INSERT(str, pos, len, newstr)` 函数用于将字符串 `str` 中的一个子字符串（从位置 `pos` 开始，长度为 `len`）替换为字符串 `newstr`。该函数是多字节安全的。

- 如果 `pos` 超过了 `str` 的长度，函数返回原始字符串 `str` 而不做修改。
- 如果 `len` 超过了从位置 `pos` 开始的 `str` 的剩余长度，函数将从位置 `pos` 开始替换字符串的其余部分。
- 如果任一参数为 `NULL`，该函数返回 `NULL`。

示例：

```sql
SELECT INSERT('He likes tennis', 4, 5, 'plays');
+------------------------------------------+
| INSERT('He likes tennis', 4, 5, 'plays') |
+------------------------------------------+
| He plays tennis                          |
+------------------------------------------+
```

```sql
SELECT INSERT('He likes tennis', -1, 5, 'plays');
+-------------------------------------------+
| INSERT('He likes tennis', -1, 5, 'plays') |
+-------------------------------------------+
| He likes tennis                           |
+-------------------------------------------+
```

```sql
SELECT INSERT('He likes tennis', 4, 100, 'plays');
+--------------------------------------------+
| INSERT('He likes tennis', 4, 100, 'plays') |
+--------------------------------------------+
| He plays                                   |
+--------------------------------------------+
```

```sql
SELECT INSERT('He likes tennis', 10, 100, '🍣');
+-------------------------------------------+
| INSERT('He likes tennis', 10, 100, '🍣')     |
+-------------------------------------------+
| He likes 🍣                                 |
+-------------------------------------------+
```

```sql
SELECT INSERT('PingCAP 数据库', 1, 7, 'TiDB');
+-------------------------------------------+
| INSERT('PingCAP 数据库', 1, 7, 'TiDB')    |
+-------------------------------------------+
| TiDB 数据库                               |
+-------------------------------------------+
```

### [`INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_instr)

`INSTR(str, substr)` 函数用于获取子字符串 `substr` 在字符串 `str` 中第一次出现的位置。`substr` 和 `str` 均可以为字符串或数字。该函数与 [`LOCATE(substr, str)`](#locate) 函数的两参数版本功能相同，但参数顺序相反。

> **注意：**
>
> `INSTR(str, substr)` 函数是否区分大小取决于 TiDB 所使用的[排序规则](/character-set-and-collation.md)。二进制排序规则（以 `_bin` 为后缀）区分大小写，而通用排序规则（以 `_general_ci` 或 `_ai_ci` 为后缀）不区分大小写。

- 如果任一输入参数为数字，该函数将数字视为字符串处理。
- 如果 `substr` 不在 `str` 中，函数返回 `0`。否则，返回 `substr` 在 `str` 中第一次出现的位置。
- 如果任一参数为 `NULL`，该函数返回 `NULL`。

示例：

```sql
SELECT INSTR("pingcap.com", "tidb");
+------------------------------+
| INSTR("pingcap.com", "tidb") |
+------------------------------+
|                            0 |
+------------------------------+
```

```sql
SELECT INSTR("pingcap.com/tidb", "tidb");
+-----------------------------------+
| INSTR("pingcap.com/tidb", "tidb") |
+-----------------------------------+
|                                13 |
+-----------------------------------+
```

```sql
SELECT INSTR("pingcap.com/tidb" COLLATE utf8mb4_bin, "TiDB");
+-------------------------------------------------------+
| INSTR("pingcap.com/tidb" COLLATE utf8mb4_bin, "TiDB") |
+-------------------------------------------------------+
|                                                     0 |
+-------------------------------------------------------+
```

```sql
SELECT INSTR("pingcap.com/tidb" COLLATE utf8mb4_general_ci, "TiDB");
+--------------------------------------------------------------+
| INSTR("pingcap.com/tidb" COLLATE utf8mb4_general_ci, "TiDB") |
+--------------------------------------------------------------+
|                                                           13 |
+--------------------------------------------------------------+
```

```sql
SELECT INSTR(0123, "12");
+-------------------+
| INSTR(0123, "12") |
+-------------------+
|                 1 |
+-------------------+
```

### [`LCASE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lcase)

`LCASE(str)`函数与 [`LOWER(str)`](#lower) 函数功能相同，都是返回输入参数的小写形式。

### [`LEFT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_left)

`LEFT()` 函数用于返回字符串左侧指定数量的字符。

语法：

```sql
LEFT(`str`, `len`)
```

- `str`：要提取字符的原始字符串。如果 `str` 包含一个多字节字符，该函数将其视为一个字符。
- `len`：要返回的字符长度。
    - 如果 `len` 小于或等于 0，该函数返回空字符串。
    - 如果 `len` 大于或等于 `str` 的长度，该函数将返回原始的 `str`。
- 如果任何参数为 `NULL`，该函数返回 `NULL`。

示例：

```sql
SELECT LEFT('ABCED', 3);
+------------------+
| LEFT('ABCED', 3) |
+------------------+
| ABC              |
+------------------+

SELECT LEFT('ABCED', 6);
+------------------+
| LEFT('ABCED', 6) |
+------------------+
| ABCED            |
+------------------+
```

```sql
SELECT LEFT('ABCED', 0);
+------------------+
| LEFT('ABCED', 0) |
+------------------+
|                  |
+------------------+

SELECT LEFT('ABCED', -1);
+-------------------+
| LEFT('ABCED', -1) |
+-------------------+
|                   |
+-------------------+
```

```sql
SELECT LEFT('🍣ABC', 3);
+--------------------+
| LEFT('🍣ABC', 3)     |
+--------------------+
| 🍣AB                 |
+--------------------+
```

```sql
SELECT LEFT('ABC', NULL);
+-------------------+
| LEFT('ABC', NULL) |
+-------------------+
| NULL              |
+-------------------+

SELECT LEFT(NULL, 3);
+------------------------------+
| LEFT(NULL, 3)                |
+------------------------------+
| NULL                         |
+------------------------------+
```

### [`LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_length)

`LENGTH()` 函数用于返回字符串的字节长度。`LENGTH()` 将单个多字节字符视为多个字节，而 `CHAR_LENGTH()` 将单个多字节字符视为单个字符。

如果输入参数为 `NULL`，该函数将返回 `NULL`。

示例：

```sql
SELECT LENGTH('ABC');
+---------------+
| LENGTH('ABC') |
+---------------+
|             3 |
+---------------+

SELECT LENGTH('🍣ABC');
+-------------------+
| LENGTH('🍣ABC')     |
+-------------------+
|                 7 |
+-------------------+

SELECT CHAR_LENGTH('🍣ABC');
+------------------------+
| CHAR_LENGTH('🍣ABC')     |
+------------------------+
|                      4 |
+------------------------+
```

```sql
SELECT LENGTH(NULL);
+--------------+
| LENGTH(NULL) |
+--------------+
|         NULL |
+--------------+
```

### [`LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like)

`LIKE` 用于进行简单字符串匹配。表达式 `expr LIKE pat [ESCAPE 'escape_char']` 返回 `1` (`TRUE`) 或 `0` (`FALSE`)。如果 `expr` 或 `pat` 中任一个为 `NULL`，结果为 `NULL`。

你可以在 `LIKE` 中使用以下两个通配符：

- `%` 匹配任意数量的字符，包括零个字符。
- `_` 精确匹配一个字符。

以下示例使用 `utf8mb4_bin` 排序规则：

```sql
SET collation_connection='utf8mb4_bin';
SHOW VARIABLES LIKE 'collation_connection';
+----------------------+-------------+
| Variable_name        | Value       |
+----------------------+-------------+
| collation_connection | utf8mb4_bin |
+----------------------+-------------+
```

```sql
SELECT NULL LIKE '%' as result;
+--------+
| result |
+--------+
|   NULL |
+--------+
```

```sql
SELECT 'sushi!!!' LIKE 'sushi_' AS result;
+--------+
| result |
+--------+
|      0 |
+--------+
```

```sql
SELECT '🍣🍺sushi🍣🍺' LIKE '%sushi%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

```sql
SELECT '🍣🍺sushi🍣🍺' LIKE '%SUSHI%' AS result;
+--------+
| result |
+--------+
|      0 |
+--------+
```

```sql
SELECT '🍣🍺sushi🍣🍺' LIKE '%🍣%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

默认的转义字符是 `\`：

```sql
SELECT 'sushi!!!' LIKE 'sushi\_' AS result;
+--------+
| result |
+--------+
|      0 |
+--------+
```

```sql
SELECT 'sushi_' LIKE 'sushi\_' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

你可以使用 `ESCAPE` 子句指定一个不同的转义字符，例如 `*`：

```sql
SELECT 'sushi_' LIKE 'sushi*_' ESCAPE '*' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

```sql
SELECT 'sushi!' LIKE 'sushi*_' ESCAPE '*' AS result;
+--------+
| result |
+--------+
|      0 |
+--------+
```

你可以使用 `LIKE` 匹配一个数字：

```sql
SELECT 10 LIKE '1%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

```sql
SELECT 10000 LIKE '12%' AS result;
+--------+
| result |
+--------+
|      0 |
+--------+
```

你可以使用 `COLLATE` 显式指定一个排序规则，例如 `utf8mb4_unicode_ci`：

```sql
SELECT '🍣🍺Sushi🍣🍺' COLLATE utf8mb4_unicode_ci LIKE '%SUSHI%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

### [`LOCATE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_locate)

`LOCATE(substr, str[, pos])` 函数用于返回子字符串 `substr` 在字符串 `str` 中第一次出现的位置。`pos` 参数是可选的，用于指定查找的起始位置。

- 如果子字符串 `substr` 不在字符串 `str` 中，该函数返回 `0`。
- 如果任一参数为 `NULL`，该函数返回 `NULL`。
- 该函数是多字节安全的，并且只有当至少一个参数是二进制字符串时，才执行区分大小写的查找。

以下示例使用 `utf8mb4_bin` 排序规则：

```sql
SET collation_connection='utf8mb4_bin';
SHOW VARIABLES LIKE 'collation_connection';
+----------------------+-------------+
| Variable_name        | Value       |
+----------------------+-------------+
| collation_connection | utf8mb4_bin |
+----------------------+-------------+
```

```sql
SELECT LOCATE('bar', 'foobarbar');
+----------------------------+
| LOCATE('bar', 'foobarbar') |
+----------------------------+
|                          4 |
+----------------------------+
```

```sql
SELECT LOCATE('baz', 'foobarbar');
+----------------------------+
| LOCATE('baz', 'foobarbar') |
+----------------------------+
|                          0 |
+----------------------------+
```

```sql
SELECT LOCATE('bar', 'fooBARBAR');
+----------------------------+
| LOCATE('bar', 'fooBARBAR') |
+----------------------------+
|                          0 |
+----------------------------+
```

```sql
SELECT LOCATE('bar', 'foobarBAR', 100);
+---------------------------------+
| LOCATE('bar', 'foobarBAR', 100) |
+---------------------------------+
|                               0 |
+---------------------------------+
```

```sql
SELECT LOCATE('bar', 'foobarbar', 5);
+-------------------------------+
| LOCATE('bar', 'foobarbar', 5) |
+-------------------------------+
|                             7 |
+-------------------------------+
```

```sql
SELECT LOCATE('bar', NULL);
+---------------------+
| LOCATE('bar', NULL) |
+---------------------+
|                NULL |
+---------------------+
```

```sql
SELECT LOCATE('DB', 'TiDB tidb 数据库');
+-------------------------------------+
| LOCATE('DB', 'TiDB tidb 数据库')    |
+-------------------------------------+
|                                   3 |
+-------------------------------------+
```

```sql
SELECT LOCATE('DB', 'TiDB tidb 数据库', 4);
+----------------------------------------+
| LOCATE('DB', 'TiDB tidb 数据库', 4)    |
+----------------------------------------+
|                                      0 |
+----------------------------------------+
```

以下示例使用 `utf8mb4_unicode_ci` 排序规则：

```sql
SET collation_connection='utf8mb4_unicode_ci';
SHOW VARIABLES LIKE 'collation_connection';
+----------------------+--------------------+
| Variable_name        | Value              |
+----------------------+--------------------+
| collation_connection | utf8mb4_unicode_ci |
+----------------------+--------------------+
```

```sql
SELECT LOCATE('DB', 'TiDB tidb 数据库', 4);
+----------------------------------------+
| LOCATE('DB', 'TiDB tidb 数据库', 4)    |
+----------------------------------------+
|                                      8 |
+----------------------------------------+
```

```sql
SELECT LOCATE('🍺', '🍣🍣🍣🍺🍺');
+----------------------------------------+
| LOCATE('🍺', '🍣🍣🍣🍺🍺')            |
+----------------------------------------+
|                                      1 |
+----------------------------------------+
```

以下多字节和二进制字符串示例使用 `utf8mb4_bin` 排序规则：

```sql
SET collation_connection='utf8mb4_bin';
SHOW VARIABLES LIKE 'collation_connection';
+----------------------+-------------+
| Variable_name        | Value       |
+----------------------+-------------+
| collation_connection | utf8mb4_bin |
+----------------------+-------------+
```

```sql
SELECT LOCATE('🍺', '🍣🍣🍣🍺🍺');
+----------------------------------------+
| LOCATE('🍺', '🍣🍣🍣🍺🍺')                         |
+----------------------------------------+
|                                      4 |
+----------------------------------------+
```

```sql
SELECT LOCATE('b', _binary'aBcde');
+-----------------------------+
| LOCATE('b', _binary'aBcde') |
+-----------------------------+
|                           0 |
+-----------------------------+
```

```sql
SELECT LOCATE('B', _binary'aBcde');
+-----------------------------+
| LOCATE('B', _binary'aBcde') |
+-----------------------------+
|                           2 |
+-----------------------------+
```

```sql
SELECT LOCATE(_binary'b', 'aBcde');
+-----------------------------+
| LOCATE(_binary'b', 'aBcde') |
+-----------------------------+
|                           0 |
+-----------------------------+
```

```sql
SELECT LOCATE(_binary'B', 'aBcde');
+-----------------------------+
| LOCATE(_binary'B', 'aBcde') |
+-----------------------------+
|                           2 |
+-----------------------------+
```

### [`LOWER()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lower)

`LOWER(str)` 函数用于将输入的参数 `str` 中的所有字符转换为小写。该参数可以为字符串或数字。

- 如果输入参数为字符串，该函数返回字符串的小写形式。
- 如果输入参数为数字，该函数将会去掉该数字中的前导零。
- 如果输入参数为 `NULL`，该函数返回 `NULL`。

示例：

```sql
SELECT LOWER("TiDB");

+---------------+
| LOWER("TiDB") |
+---------------+
| tidb          |
+---------------+
```

```sql
SELECT LOWER(-012);

+-------------+
| LOWER(-012) |
+-------------+
| -12         |
+-------------+
```

### [`LPAD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lpad)

`LPAD(str, len, padstr)` 函数返回字符串参数，左侧填充指定字符串 `padstr`，直到字符串长度达到 `len` 个字符。

- 如果 `len` 小于字符串 `str` 的长度，函数将字符串 `str` 截断到长度 `len`。
- 如果 `len` 为负数，函数返回 `NULL`。
- 如果任一参数为 `NULL`，该函数返回 `NULL`。

示例：

```sql
SELECT LPAD('TiDB',8,'>');
+--------------------+
| LPAD('TiDB',8,'>') |
+--------------------+
| >>>>TiDB           |
+--------------------+
1 row in set (0.00 sec)
```

```sql
SELECT LPAD('TiDB',2,'>');
+--------------------+
| LPAD('TiDB',2,'>') |
+--------------------+
| Ti                 |
+--------------------+
1 row in set (0.00 sec)
```

```sql
SELECT LPAD('TiDB',-2,'>');
+---------------------+
| LPAD('TiDB',-2,'>') |
+---------------------+
| NULL                |
+---------------------+
1 row in set (0.00 sec)
```

### [`LTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ltrim)

`LTRIM()` 函数用于删除给定的字符串中的前导空格（即字符串开头的连续空格）。

如果输入的参数为 `NULL`，该函数将返回 `NULL`。

> **注意：**
>
> 该函数只去掉空格字符（U+0020），不去掉其他类似空格的字符，如制表符（U+0009）或非分隔符（U+00A0）。

示例：

在以下示例中，`LTRIM()` 函数删除了 `'    hello'` 中的前导空格，并返回 `hello`。

```sql
SELECT LTRIM('    hello');
```

```
+--------------------+
| LTRIM('    hello') |
+--------------------+
| hello              |
+--------------------+
1 row in set (0.00 sec)
```

在以下示例中，[`CONCAT()`](#concat) 用于将 `LTRIM('    hello')` 的结果用 `«` 和 `»` 包裹起来。通过这种格式，可以更容易地看到所有前导空格都被删除了。

```sql
SELECT CONCAT('«',LTRIM('    hello'),'»');
```

```
+------------------------------------+
| CONCAT('«',LTRIM('    hello'),'»') |
+------------------------------------+
| «hello»                            |
+------------------------------------+
1 row in set (0.00 sec)
```

### [`MAKE_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_make-set)

`MAKE_SET()` 函数根据输入的 `bits` 参数中相应的 bit 是否为 `1` 返回一组由逗号分隔的字符串。

语法：

```sql
MAKE_SET(bits, str1, str2, ...)
```

- `bits`：控制其后的字符串参数中的哪些参数会包含到输出结果中。如果 `bits` 为 `NULL`，该函数将返回 `NULL`。
- `str1, str2, ...`：字符串参数列表。每个字符串与 `bits` 参数中从右到左的一个 bit 依次对应。`str1` 对应于 `bits` 中从右起的第一个 bit，`str2` 对应于从右起的第二个 bit，依此类推。如果相应的 bit 为 `1`，则该字符串将包含在输出结果中；否则，将不包含在输出结果中。

示例：

在以下示例中，因为 `bits` 参数中的所有 bit 都为 `0`，该函数将不会在结果中包含 `bits` 后的任何字符串参数，因此返回空字符串。

```sql
SELECT MAKE_SET(b'000','foo','bar','baz');
```

```
+------------------------------------+
| MAKE_SET(b'000','foo','bar','baz') |
+------------------------------------+
|                                    |
+------------------------------------+
1 row in set (0.00 sec)
```

在以下示例中，因为只有从右起的第一个 bit 为 `1`，该函数只返回第一个字符串 `foo`。

```sql
SELECT MAKE_SET(b'001','foo','bar','baz');
```

```
+------------------------------------+
| MAKE_SET(b'001','foo','bar','baz') |
+------------------------------------+
| foo                                |
+------------------------------------+
1 row in set (0.00 sec)
```

在以下示例中，因为只有从右起的第二个 bit 为 `1`，该函数只返回第二个字符串 `bar`。

```sql
SELECT MAKE_SET(b'010','foo','bar','baz');
```

```
+------------------------------------+
| MAKE_SET(b'010','foo','bar','baz') |
+------------------------------------+
| bar                                |
+------------------------------------+
1 row in set (0.00 sec)
```

在以下示例中，因为只有从右起的第三个 bit 为 `1`，该函数只返回第三个字符串 `baz`。

```sql
SELECT MAKE_SET(b'100','foo','bar','baz');
```

```
+------------------------------------+
| MAKE_SET(b'100','foo','bar','baz') |
+------------------------------------+
| baz                                |
+------------------------------------+
1 row in set (0.00 sec)
```

在以下示例中，因为所有 bit 都为 `1`，该函数将返回全部的三个字符串，并以逗号分隔。

```sql
SELECT MAKE_SET(b'111','foo','bar','baz');
```

```
+------------------------------------+
| MAKE_SET(b'111','foo','bar','baz') |
+------------------------------------+
| foo,bar,baz                        |
+------------------------------------+
1 row in set (0.0002 sec)
```

### [`MID()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_mid)

`MID(str,pos,len)` 函数返回从指定的 `pos` 位置开始的长度为 `len` 的子字符串。

如果任一参数为 `NULL`，该函数将返回 `NULL`。

TiDB 不支持该函数的两参数版本。更多信息，请参见 [#52420](https://github.com/pingcap/tidb/issues/52420)。

示例：

在以下示例中，`MID()` 返回给定的字符串中从第二个字符 (`b`) 开始的长度为 `3` 个字符的的子字符串。

```sql
SELECT MID('abcdef',2,3);
```

```
+-------------------+
| MID('abcdef',2,3) |
+-------------------+
| bcd               |
+-------------------+
1 row in set (0.00 sec)
```

### [`NOT LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like)

否定简单模式匹配。

该函数的功能与 [`LIKE`](#like) 函数相反。

示例：

在以下示例中，因为 `aaa` 匹配 `a%` 模式，`NOT LIKE` 返回 `0`（代表结果为 False）。

```sql
SELECT 'aaa' LIKE 'a%', 'aaa' NOT LIKE 'a%';
```

```
+-----------------+---------------------+
| 'aaa' LIKE 'a%' | 'aaa' NOT LIKE 'a%' |
+-----------------+---------------------+
|               1 |                   0 |
+-----------------+---------------------+
1 row in set (0.00 sec)
```

在以下示例中，因为 `aaa` 与 `b%` 模式不匹配，`NOT LIKE` 返回 `1`（代表结果为 True）。

```sql
SELECT 'aaa' LIKE 'b%', 'aaa' NOT LIKE 'b%';
```

```
+-----------------+---------------------+
| 'aaa' LIKE 'b%' | 'aaa' NOT LIKE 'b%' |
+-----------------+---------------------+
|               0 |                   1 |
+-----------------+---------------------+
1 row in set (0.00 sec)
```

### [`NOT REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp)

[`REGEXP`](#regexp) 的否定形式

### [`OCT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_oct)

`OCT()` 函数用于返回一个数值的[八进制](https://zh.wikipedia.org/wiki/八进制)表示，形式为字符串。

示例：

以下示例使用[递归的公共表表达式 (CTE)](/develop/dev-guide-use-common-table-expression.md#递归的-cte) 生成从 0 到 20 的数字序列，然后使用 `OCT()` 函数将每个数字转换为其八进制表示。从 0 到 7 的十进制数在八进制中有相同的表示，从 8 到 15 的十进制数对应从 10 到 17 的八进制数。

```sql
WITH RECURSIVE nr(n) AS (
    SELECT 0 AS n
    UNION ALL
    SELECT n+1 FROM nr WHERE n<20
)
SELECT n, OCT(n) FROM nr;
```

```
+------+--------+
| n    | OCT(n) |
+------+--------+
|    0 | 0      |
|    1 | 1      |
|    2 | 2      |
|    3 | 3      |
|    4 | 4      |
|    5 | 5      |
|    6 | 6      |
|    7 | 7      |
|    8 | 10     |
|    9 | 11     |
|   10 | 12     |
|   11 | 13     |
|   12 | 14     |
|   13 | 15     |
|   14 | 16     |
|   15 | 17     |
|   16 | 20     |
|   17 | 21     |
|   18 | 22     |
|   19 | 23     |
|   20 | 24     |
+------+--------+
20 rows in set (0.00 sec)
```

### [`OCTET_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_octet-length)

与 [`LENGTH()`](#length) 功能相同

### [`ORD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ord)

返回给定的参数中最左侧字符的字符编码。

该函数的功能类似于 [`CHAR()`](#char)，但处理方式相反。

示例：

以 `a` 和 `A` 为例，`ORD()` 返回 `a` 的字符代码 `97` 和 `A` 的字符代码 `65`。

```sql
SELECT ORD('a'), ORD('A');
```

```
+----------+----------+
| ORD('a') | ORD('A') |
+----------+----------+
|       97 |       65 |
+----------+----------+
1 row in set (0.00 sec)
```

如果将从 `ORD()` 获得的字符代码作为 `CHAR()` 函数的输入，即可获取原始字符。请注意，以下输出的格式可能会根据你的 MySQL 客户端是否启用了 `binary-as-hex` 选项而有所不同。

```sql
SELECT CHAR(97), CHAR(65);
```

```
+----------+----------+
| CHAR(97) | CHAR(65) |
+----------+----------+
| a        | A        |
+----------+----------+
1 row in set (0.01 sec)
```

以下示例展示了 `ORD()` 如何处理多字节字符。`101` 和 `0x65` 都是 `e` 字符的 UTF-8 编码值，但格式不同。`50091` 和 `0xC3AB` 也表示的是相同的值，但对应 `ë` 字符。

```sql
SELECT ORD('e'), ORD('ë'), HEX('e'), HEX('ë');
```

```
+----------+-----------+----------+-----------+
| ORD('e') | ORD('ë')  | HEX('e') | HEX('ë')  |
+----------+-----------+----------+-----------+
|      101 |     50091 | 65       | C3AB      |
+----------+-----------+----------+-----------+
1 row in set (0.00 sec)
```

### [`POSITION()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_position)

与 [`LOCATE()`](#locate) 功能相同

### [`QUOTE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_quote)

`QUOTE()` 函数用于转义字符串，使其可以在 SQL 语句中使用。

如果输入参数为 `NULL`，该函数返回 `NULL`。

示例：

为了直接显示查询结果，而不是以十六进制编码的形式展示，你需要使用 [`--skip-binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex) 选项启动 MySQL 客户端。

以下示例显示了 ASCII NULL 字符被转义为 `\0`，单引号字符 `'` 被转义为 `\'`：

```sql
SELECT QUOTE(0x002774657374);
```

```
+-----------------------+
| QUOTE(0x002774657374) |
+-----------------------+
| '\0\'test'            |
+-----------------------+
1 row in set (0.00 sec)
```

### [`REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)

使用正则表达式匹配模式

示例：

下面示例使用了两个正则表达式来匹配一些字符串。

```sql
WITH vals AS (
    SELECT 'TiDB' AS v 
    UNION ALL
    SELECT 'Titanium'
    UNION ALL
    SELECT 'Tungsten'
    UNION ALL
    SELECT 'Rust'
)
SELECT 
    v,
    v REGEXP '^Ti' AS 'starts with "Ti"',
    v REGEXP '^.{4}$' AS 'Length is 4 characters'
FROM
    vals;
```

```
+----------+------------------+------------------------+
| v        | starts with "Ti" | Length is 4 characters |
+----------+------------------+------------------------+
| TiDB     |                1 |                      1 |
| Titanium |                1 |                      0 |
| Tungsten |                0 |                      0 |
| Rust     |                0 |                      1 |
+----------+------------------+------------------------+
4 rows in set (0.00 sec)
```

`REGEXP` 并不限于只在 `SELECT` 子句中使用。例如，`REGEXP` 还可以用于查询的 `WHERE` 子句中。

```sql
SELECT
    v
FROM (
        SELECT 'TiDB' AS v
    ) AS vals
WHERE
    v REGEXP 'DB$';
```

```
+------+
| v    |
+------+
| TiDB |
+------+
1 row in set (0.01 sec)
```

### [`REGEXP_INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-instr)

返回满足正则的子字符串的第一个索引位置（与 MySQL 不完全兼容，具体请参考[正则函数与 MySQL 的兼容性](#正则函数与-mysql-的兼容性)）

`REGEXP_INSTR(str, regexp, [start, [match, [ret, [match_type]]]])` 函数返回正则表达式（`regexp`）匹配字符串（`str`）的位置。

如果 `str` 或 `regexp` 为 `NULL`，则该函数返回 `NULL`。

示例：

下面示例展示了 `^.b.$` 匹配 `abc` 的情况。

```sql
SELECT REGEXP_INSTR('abc','^.b.$');
```

```
+-----------------------------+
| REGEXP_INSTR('abc','^.b.$') |
+-----------------------------+
|                           1 |
+-----------------------------+
1 row in set (0.00 sec)
```

下面示例展示了使用第三个参数来从字符串的指定位置起查找匹配值的情况。

```sql
SELECT REGEXP_INSTR('abcabc','a');
```

```
+----------------------------+
| REGEXP_INSTR('abcabc','a') |
+----------------------------+
|                          1 |
+----------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT REGEXP_INSTR('abcabc','a',2);
```

```
+------------------------------+
| REGEXP_INSTR('abcabc','a',2) |
+------------------------------+
|                            4 |
+------------------------------+
1 row in set (0.00 sec)
```

下面示例展示了使用第四个参数来查找第二个匹配值的情况。

```sql
SELECT REGEXP_INSTR('abcabc','a',1,2);
```

```
+--------------------------------+
| REGEXP_INSTR('abcabc','a',1,2) |
+--------------------------------+
|                              4 |
+--------------------------------+
1 row in set (0.00 sec)
```

下面示例展示了使用第五个参数来返回匹配值后面的那个值的位置，而不是返回匹配值的位置。

```sql
SELECT REGEXP_INSTR('abcabc','a',1,1,1);
```

```
+----------------------------------+
| REGEXP_INSTR('abcabc','a',1,1,1) |
+----------------------------------+
|                                2 |
+----------------------------------+
1 row in set (0.00 sec)
```

下面示例展示了使用第六个参数来添加 `i` 标志以获得不区分大小写的匹配。有关正则表达式 `match_type` 的更多详细信息，请参阅 [`match_type` 兼容性](#匹配模式-match_type-兼容性)。

```sql
SELECT REGEXP_INSTR('abcabc','A',1,1,0,'');
```

```
+-------------------------------------+
| REGEXP_INSTR('abcabc','A',1,1,0,'') |
+-------------------------------------+
|                                   0 |
+-------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT REGEXP_INSTR('abcabc','A',1,1,0,'i');
```

```
+--------------------------------------+
| REGEXP_INSTR('abcabc','A',1,1,0,'i') |
+--------------------------------------+
|                                    1 |
+--------------------------------------+
1 row in set (0.00 sec)
```

除了 `match_type`，[排序规则](/character-set-and-collation.md) 也会影响匹配。在下面的示例中，使用了区分大小写和不区分大小写的排序规则来展示这种影响。

```sql
SELECT REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_general_ci);
```

```
+-------------------------------------------------------+
| REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_general_ci) |
+-------------------------------------------------------+
|                                                     1 |
+-------------------------------------------------------+
1 row in set (0.01 sec)
```

```sql
SELECT REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_bin);
```

```
+------------------------------------------------+
| REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_bin) |
+------------------------------------------------+
|                                              0 |
+------------------------------------------------+
1 row in set (0.00 sec)
```

### [`REGEXP_LIKE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-like)

判断字符串是否满足正则表达式（与 MySQL 不完全兼容，具体请参考[正则函数与 MySQL 的兼容性](#正则函数与-mysql-的兼容性)）

`REGEXP_LIKE(str, regex, [match_type])` 函数用于判断正则表达式是否匹配字符串。可选的 `match_type` 参数可以用于更改匹配行为。

示例：

下面示例展示了 `^a` 匹配 `abc` 的情况。

```sql
SELECT REGEXP_LIKE('abc','^a');
```

```
+-------------------------+
| REGEXP_LIKE('abc','^a') |
+-------------------------+
|                       1 |
+-------------------------+
1 row in set (0.00 sec)
```

下面示例展示了 `^A` 不匹配 `abc` 的情况。

```sql
SELECT REGEXP_LIKE('abc','^A');
```

```
+-------------------------+
| REGEXP_LIKE('abc','^A') |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.00 sec)
```

下面示例展示了 `^A` 匹配 `abc` 的情况，因为 `i` 标志启用了不区分大小写的匹配，所以能够匹配上。关于正则表达式 `match_type` 的更多详细信息，请参阅 [`match_type` 兼容性](#匹配模式-match_type-兼容性)。

```sql
SELECT REGEXP_LIKE('abc','^A','i');
```

```
+-----------------------------+
| REGEXP_LIKE('abc','^A','i') |
+-----------------------------+
|                           1 |
+-----------------------------+
1 row in set (0.00 sec)
```

### [`REGEXP_REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-replace)

替换满足正则表达式的子字符串（与 MySQL 不完全兼容，具体请参考[正则函数与 MySQL 的兼容性](#正则函数与-mysql-的兼容性)）

`REGEXP_REPLACE(str, regexp, replace, [start, [match, [match_type]]])` 函数可以用于基于正则表达式替换字符串。

示例：

下面的示例中，两个 `o` 被替换为 `i`。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o{2}', 'i');
```

```
+--------------------------------------+
| REGEXP_REPLACE('TooDB', 'o{2}', 'i') |
+--------------------------------------+
| TiDB                                 |
+--------------------------------------+
1 row in set (0.00 sec)
```

下面示例从第三个字符开始匹配，导致正则表达式不匹配，不进行任何替换。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o{2}', 'i',3);
```

```
+----------------------------------------+
| REGEXP_REPLACE('TooDB', 'o{2}', 'i',3) |
+----------------------------------------+
| TooDB                                  |
+----------------------------------------+
1 row in set (0.00 sec)
```

下面示例中，第五个参数用于设置替换第一个或第二个匹配的值。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o', 'i',1,1);
```

```
+---------------------------------------+
| REGEXP_REPLACE('TooDB', 'o', 'i',1,1) |
+---------------------------------------+
| TioDB                                 |
+---------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT REGEXP_REPLACE('TooDB', 'o', 'i',1,2);
```

```
+---------------------------------------+
| REGEXP_REPLACE('TooDB', 'o', 'i',1,2) |
+---------------------------------------+
| ToiDB                                 |
+---------------------------------------+
1 row in set (0.00 sec)
```

下面示例中，第六个参数用于设置 `match_type` 为不区分大小写的匹配。更多关于正则表达式 `match_type` 的详细信息，请参阅 [`match_type` 兼容性](#匹配模式-match_type-兼容性)。

```sql
SELECT REGEXP_REPLACE('TooDB', 'O{2}','i',1,1);
```

```
+-----------------------------------------+
| REGEXP_REPLACE('TooDB', 'O{2}','i',1,1) |
+-----------------------------------------+
| TooDB                                   |
+-----------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT REGEXP_REPLACE('TooDB', 'O{2}','i',1,1,'i');
```

```
+---------------------------------------------+
| REGEXP_REPLACE('TooDB', 'O{2}','i',1,1,'i') |
+---------------------------------------------+
| TiDB                                        |
+---------------------------------------------+
1 row in set (0.00 sec)
```

### [`REGEXP_SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-substr)

返回满足正则表达式的子字符串（与 MySQL 不完全兼容，具体请参考[正则函数与 MySQL 的兼容性](#正则函数与-mysql-的兼容性)）

`REGEXP_SUBSTR(str, regexp, [start, [match, [match_type]]])` 函数用于基于正则表达式获取子字符串。

下面示例使用 `Ti.{2}` 正则表达式从 `This is TiDB` 字符串中获取 `TiDB` 子字符串。

```sql
SELECT REGEXP_SUBSTR('This is TiDB','Ti.{2}');
```

```
+----------------------------------------+
| REGEXP_SUBSTR('This is TiDB','Ti.{2}') |
+----------------------------------------+
| TiDB                                   |
+----------------------------------------+
1 row in set (0.00 sec)
```

### [`REPEAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_repeat)

`REPEAT()` 函数用于以指定次数重复一个字符串。

示例：

以下示例使用[递归的公共表表达式 (CTE)](/develop/dev-guide-use-common-table-expression.md#递归的-cte) 生成从 1 到 20 的数字序列，并使用 `REPEAT()` 函数重复对应次数的 `x` 字符串：

```sql
WITH RECURSIVE nr(n) AS (
    SELECT 1 AS n 
    UNION ALL 
    SELECT n+1 FROM nr WHERE n<20
)
SELECT n, REPEAT('x',n) FROM nr;
```

```
+------+----------------------+
| n    | REPEAT('x',n)        |
+------+----------------------+
|    1 | x                    |
|    2 | xx                   |
|    3 | xxx                  |
|    4 | xxxx                 |
|    5 | xxxxx                |
|    6 | xxxxxx               |
|    7 | xxxxxxx              |
|    8 | xxxxxxxx             |
|    9 | xxxxxxxxx            |
|   10 | xxxxxxxxxx           |
|   11 | xxxxxxxxxxx          |
|   12 | xxxxxxxxxxxx         |
|   13 | xxxxxxxxxxxxx        |
|   14 | xxxxxxxxxxxxxx       |
|   15 | xxxxxxxxxxxxxxx      |
|   16 | xxxxxxxxxxxxxxxx     |
|   17 | xxxxxxxxxxxxxxxxx    |
|   18 | xxxxxxxxxxxxxxxxxx   |
|   19 | xxxxxxxxxxxxxxxxxxx  |
|   20 | xxxxxxxxxxxxxxxxxxxx |
+------+----------------------+
20 rows in set (0.01 sec)
```

以下示例演示了 `REPEAT()` 可以处理包含多个字符的字符串：

```sql
SELECT REPEAT('ha',3);
```

```
+----------------+
| REPEAT('ha',3) |
+----------------+
| hahaha         |
+----------------+
1 row in set (0.00 sec)
```

### [`REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_replace)

替换所有出现的指定字符串

### [`REVERSE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_reverse)

反转字符串里的所有字符

### [`RIGHT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_right)

返回指定数量的最右侧的字符

### [`RLIKE`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)

与 [`REGEXP`](#regexp) 功能相同

### [`RPAD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rpad)

以指定次数添加字符串

### [`RTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rtrim)

去掉后缀空格

### [`SPACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_space)

返回指定数量的空格，形式为字符串

### [`STRCMP()`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp)

比较两个字符串

### [`SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substr)

返回指定的子字符串

### [`SUBSTRING()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring)

返回指定的子字符串

### [`SUBSTRING_INDEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring-index)

`SUBSTRING_INDEX()` 函数用于按照指定的分隔符和次数从字符串中提取子字符串。该函数在处理以特定分隔符分隔的数据时特别有用，例如解析 CSV 数据或处理日志文件。

语法：

```sql
SUBSTRING_INDEX(str, delim, count)
```

- `str`：要处理的字符串。
- `delim`：指定字符串中的分隔符，大小写敏感。
- `count`：指定分隔符出现的次数。
    - 如果 `count` 为正数，该函数返回从字符串左边开始的第 `count` 个分隔符之前的子字符串。
    - 如果 `count` 为负数，该函数返回从字符串右边开始的第 `count` 个分隔符之后的子字符串。
    - 如果 `count` 为 `0`，该函数返回一个空字符串。

查询示例 1：

```sql
SELECT SUBSTRING_INDEX('www.tidbcloud.com', '.', 2);
```

返回结果 1：

```sql
+-----------------------------------------+
| SUBSTRING_INDEX('www.tidbcloud.com', '.', 2) |
+-----------------------------------------+
| www.tidbcloud                                |
+-----------------------------------------+
```

查询示例 2：

```sql
SELECT SUBSTRING_INDEX('www.tidbcloud.com', '.', -1);
```

返回结果 2：

```sql
+------------------------------------------+
| SUBSTRING_INDEX('www.tidbcloud.com', '.', -1) |
+------------------------------------------+
| com                                      |
+------------------------------------------+
```

### [`TO_BASE64()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_to-base64)

`TO_BASE64()` 函数用于将输入的参数转换为 base-64 编码形式的字符串，并按照当前连接的字符集和排序规则返回结果。base-64 编码的字符串可以使用 [`FROM_BASE64()`](#from_base64) 函数进行解码。

语法：

```sql
TO_BASE64(str)
```

- 如果输入参数不是字符串，该函数会将其转换为字符串后再进行 base-64 编码。
- 如果输入参数为 `NULL`，该函数返回 `NULL`。

查询示例 1：

```sql
SELECT TO_BASE64('abc');
```

返回结果 1：

```sql
+------------------+
| TO_BASE64('abc') |
+------------------+
| YWJj             |
+------------------+
```

查询示例 2：

```sql
SELECT TO_BASE64(6);
```

返回结果 2：

```sql
+--------------+
| TO_BASE64(6) |
+--------------+
| Ng==         |
+--------------+
```

### [`TRANSLATE()`](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/TRANSLATE.html#GUID-80F85ACB-092C-4CC7-91F6-B3A585E3A690)

将字符串中出现的所有指定字符替换为其它字符。这个函数不会像 Oracle 一样将空字符串视为`NULL`

### [`TRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_trim)

去掉前缀和后缀空格

### [`UCASE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ucase)

`UCASE()` 函数将字符串转换为大写字母，此函数等价于 `UPPER()` 函数。

> **注意：**
>
> 当字符串为 null 时，则返回 `NULL`。

查询示例：

```sql
SELECT UCASE('bigdata') AS result_upper, UCASE(null) AS result_null;
```

返回结果：

```sql
+--------------+-------------+
| result_upper | result_null |
+--------------+-------------+
| BIGDATA      | NULL        |
+--------------+-------------+
```

### [`UNHEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_unhex)

`UNHEX()` 函数执行 `HEX()` 函数的逆运算，将参数中的每对字符视为十六进制数字，并将其转换为该数字表示的字符，返回值为二进制字符串。

> **注意：**
>
> 传入的字符串必须是合法的十六进制数值，包含 `0~9`、`A~F`、`a~f`，如果为 `NULL` 或超出该范围，则返回 `NULL`。

查询示例：

```sql
SELECT UNHEX('54694442');
```

返回结果：

```sql
+--------------------------------------+
| UNHEX('54694442')                    |
+--------------------------------------+
| 0x54694442                           |
+--------------------------------------+
```

### [`UPPER()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_upper)

`UPPER()` 函数将字符串转换为大写字母，此函数等价于 `UCASE()` 函数。

> **注意：**
>
> 当字符串为 null 时，则返回 `NULL`。

查询示例：

```sql
SELECT UPPER('bigdata') AS result_upper, UPPER(null) AS result_null;
```

返回结果：

```sql
+--------------+-------------+
| result_upper | result_null |
+--------------+-------------+
| BIGDATA      | NULL        |
+--------------+-------------+
```

### [`WEIGHT_STRING()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_weight-string)

`WEIGHT_STRING()` 函数返回字符串的权重（二进制字符），主要用于多字符集场景下的排序和比较操作。如果参数为 `NULL`，则返回 `NULL`。语法示例如下：

```sql
WEIGHT_STRING(str [AS {CHAR|BINARY}(N)])
```

* `str`：字符串表达式。如果是非二进制字符串，例如 CHAR、VARCHAR 或 TEXT 值，则返回值包含该字符串的排序规则权重；如果是二进制字符串，例如 BINARY、VARBINARY 或 BLOB 值，则返回值与输入相同。
* `AS {CHAR|BINARY}(N)`：可选参数，用于指定输出结果的类型和长度。`CHAR` 表示字符数据类型，而 `BINARY` 表示二进制数据类型；`N` 指定输出的长度，取值为大于等于 1 的整数。

> **注意：**
>
> 当 `N` 小于字符串长度时，字符串将被截断；当 `N` 超过字符串长度时，`CHAR` 类型将用空格来填充以达到指定长度，`BINARY` 类型将以 `0x00` 来填充以达到指定长度。

查询示例：

```sql
SET NAMES 'utf8mb4';
SELECT HEX(WEIGHT_STRING('ab' AS CHAR(3))) AS char_result, HEX(WEIGHT_STRING('ab' AS BINARY(3))) AS binary_result;
```

返回结果：

```sql
+-------------+---------------+
| char_result | binary_result |
+-------------+---------------+
| 6162        | 616200        |
+-------------+---------------+
```

## 不支持的函数

* `LOAD_FILE()`
* `MATCH()`
* `SOUNDEX()`

## 正则函数与 MySQL 的兼容性

本节介绍 TiDB 中正则函数 `REGEXP_INSTR()`、`REGEXP_LIKE()`、`REGEXP_REPLACE()`、`REGEXP_SUBSTR()` 与 MySQL 的兼容情况。

### 语法兼容性

MySQL 的实现使用的是 [ICU](https://github.com/unicode-org/icu) (International Components for Unicode) 库，TiDB 的实现使用的是 [RE2](https://github.com/google/re2) 库，两个库之间的语法差异可以查阅 [ICU 文档](https://unicode-org.github.io/icu/userguide/)和 [RE2 文档](https://github.com/google/re2/wiki/Syntax)。

### 匹配模式 `match_type` 兼容性

TiDB 与 MySQL 在 `match_type` 上的差异：

- TiDB 中 `match_type` 可选值为：`"c"`、`"i"`、`"m"`、`"s"`。MySQL 中 `match_type` 可选值为：`"c"`、`"i"`、`"m"`、`"n"`、`"u"`。
- TiDB 中 `"s"` 对应 MySQL 中的 `"n"`，即 `.` 字符匹配行结束符。

    例如：MySQL 中 `SELECT REGEXP_LIKE(a, b, "n") FROM t1;` 在 TiDB 中需要修改为 `SELECT REGEXP_LIKE(a, b, "s") FROM t1;`。

- TiDB 不支持 `match_type` 为 `"u"`。

| `match_type` | MySQL | TiDB | 描述                                   |
|:------------:|-------|------|----------------------------------------|
| c            | Yes   | Yes  | 大小写敏感匹配                          |
| i            | Yes   | Yes  | 大小写不敏感匹配                        |
| m            | Yes   | Yes  | 匹配多行文本的模式                        |
| s            | No    | Yes  | 匹配新行，和 MySQL 中的 `n` 相同        |
| n            | Yes   | No   | 匹配新行，和 TiDB 中的 `s` 相同         |
| u            | Yes   | No   | UNIX&trade 换行符           |

### 数据类型兼容性

TiDB 与 MySQL 在二进制字符串 (binary string) 数据类型上的差异：

- MySQL 8.0.22 及以上版本中正则函数不支持二进制字符串，具体信息可查看 [MySQL 文档](https://dev.mysql.com/doc/refman/8.0/en/regexp.html)。但在实际使用过程中，如果所有参数或者返回值的数据类型都是二进制字符串，则正则函数可以正常使用，否则报错。
- TiDB 目前完全禁止使用二进制字符串，无论什么情况都会报错。

### 其它兼容性

- TiDB 与 MySQL 在替换空字符串上存在差异，下面以 `REGEXP_REPLACE("", "^$", "123")` 为例：

    - MySQL 不会对空串进行替换，其结果为 `""`。
    - TiDB 会对空串进行替换，其结果为 `"123"`。

- TiDB 与 MySQL 在捕获组的关键字上存在差异。MySQL 的捕获组关键字为`$`，而 TiDB 的捕获组关键字为`\\`。此外，TiDB 只支持编号为 `0` 到 `9` 的捕获组。

    例如，以下 SQL 语句在 TiDB 中的返回结果为 `ab`。

    ```sql
    SELECT REGEXP_REPLACE('abcd','(.*)(.{2})$','\\1') AS s;
    ```

### 已知问题

- [GitHub Issue #37981](https://github.com/pingcap/tidb/issues/37981)