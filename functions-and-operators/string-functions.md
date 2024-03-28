---
title: 字符串函数
aliases: ['/docs-cn/dev/functions-and-operators/string-functions/','/docs-cn/dev/reference/sql/functions-and-operators/string-functions/','/docs-cn/dev/sql/string-functions/']
---

# 字符串函数

TiDB 支持使用大部分 MySQL 5.7 中提供的[字符串函数](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html)、一部分 MySQL 8.0 中提供的[字符串函数](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html)和一部分 Oracle 21 所提供的[函数](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlqr/SQL-Functions.html#GUID-93EC62F8-415D-4A7E-B050-5D5B2C127009)。

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

`CHAR()` 函数用于获取指定 ASCII 值的对应字符。该函数执行的操作与 `ASCII()` 相反，`ASCII()` 用于返回指定字符的 ASCII 值。

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
SELECT CustomerName, CHAR_LENGTH(CustomerName) AS LenghtOfName FROM Customers;

+--------------------+--------------+
| CustomerName       | LenghtOfName |
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

返回指定位置的字符串

### [`EXPORT_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_export-set)

返回一个字符串，其中值位中设置的每个位，可以得到一个 on 字符串，而每个未设置的位，可以得到一个 off 字符串

### [`FIELD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_field)

返回参数在后续参数中出现的第一个位置

### [`FIND_IN_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_find-in-set)

返回第一个参数在第二个参数中出现的位置

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

返回字符串参数，左侧添加指定字符串

### [`LTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ltrim)

去掉前缀空格

### [`MAKE_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_make-set)

返回一组用逗号分隔的字符串，这些字符串的位数与给定的 bits 参数对应

### [`MID()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_mid)

返回一个以指定位置开始的子字符串

### [`NOT LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like)

否定简单模式匹配

### [`NOT REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp)

`REGEXP` 的否定形式

### [`OCT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_oct)

返回一个数值的八进制表示，形式为字符串

### [`OCTET_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_octet-length)

与 `LENGTH()` 功能相同

### [`ORD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ord)

返回该参数最左侧字符的字符编码

### [`POSITION()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_position)

与 `LOCATE()` 功能相同

### [`QUOTE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_quote)

使参数逃逸，为了在 SQL 语句中使用

### [`REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)

使用正则表达式匹配模式

### [`REGEXP_INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-instr)

返回满足正则的子字符串的第一个索引位置（与 MySQL 不完全兼容，具体请参考[正则函数与 MySQL 的兼容性](#正则函数与-mysql-的兼容性)）

### [`REGEXP_LIKE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-like)

判断字符串是否满足正则表达式（与 MySQL 不完全兼容，具体请参考[正则函数与 MySQL 的兼容性](#正则函数与-mysql-的兼容性)）

### [`REGEXP_REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-replace)

替换满足正则表达式的子字符串（与 MySQL 不完全兼容，具体请参考[正则函数与 MySQL 的兼容性](#正则函数与-mysql-的兼容性)）

### [`REGEXP_SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-substr)

返回满足正则表达式的子字符串（与 MySQL 不完全兼容，具体请参考[正则函数与 MySQL 的兼容性](#正则函数与-mysql-的兼容性)）

### [`REPEAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_repeat)

以指定次数重复一个字符串

### [`REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_replace)

替换所有出现的指定字符串

### [`REVERSE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_reverse)

反转字符串里的所有字符

### [`RIGHT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_right)

返回指定数量的最右侧的字符

### [`RLIKE`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)

与 `REGEXP` 功能相同

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
