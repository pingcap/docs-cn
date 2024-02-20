---
title: String Functions
summary: Learn about the string functions in TiDB.
aliases: ['/docs/dev/functions-and-operators/string-functions/','/docs/dev/reference/sql/functions-and-operators/string-functions/']
---

# String Functions

TiDB supports most of the [string functions](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html) available in MySQL 5.7, some of the [string functions](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html) available in MySQL 8.0, and some of the [functions](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlqr/SQL-Functions.html#GUID-93EC62F8-415D-4A7E-B050-5D5B2C127009) available in Oracle 21.

<CustomContent platform="tidb">

For comparisons between functions and syntax of Oracle and TiDB, see [Comparisons between Functions and Syntax of Oracle and TiDB](/oracle-functions-to-tidb.md).

</CustomContent>

## Supported functions

### [`ASCII()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ascii)

The `ASCII(str)` function is used to get the ASCII value of the leftmost character in the given argument. The argument can be either a string or a number.

- If the argument is not empty, the function returns the ASCII value of the leftmost character.
- If the argument is an empty string, the function returns `0`.
- If the argument is `NULL`, the function returns `NULL`.

> **Note:**
>
> `ASCII(str)` only works for characters represented using 8 bits of binary digits (one byte).

Examples:

```sql
SELECT ASCII('A');

+------------+
| ASCII('A') |
+------------+
|         65 |
+------------+
```

```sql
SELECT ASCII('TiDB');

+---------------+
| ASCII('TiDB') |
+---------------+
|            84 |
+---------------+
```

```sql
SELECT ASCII(23);

+-----------+
| ASCII(23) |
+-----------+
|        50 |
+-----------+
```

### [`BIN()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bin)

The `BIN()` function is used to convert the given argument into a string representation of its binary value. The argument can be either a string or a number.

- If the argument is a positive number, the function returns a string representation of its binary value.
- If the argument is a negative number, the function converts the absolute value of the argument to its binary representation, inverts each bit of the binary value (changing `0` to `1` and `1` to `0`), and then adds `1` to the inverted value.
- If the argument is a string containing only digits, the function returns the result according to those digits. For example, the results for `"123"` and `123` are the same.
- If the argument is a string and its first character is not a digit (such as `"q123"`), the function returns `0`.
- If the argument is a string that consists of digits and non-digits, the function returns the result according to the consecutive digits at the beginning of the argument. For example, the results for `"123q123"` and `123` are the same.
- If the argument is `NULL`, the function returns `NULL`.

Examples:

```sql
SELECT BIN(123);

+----------+
| BIN(123) |
+----------+
| 1111011  |
+----------+
```

```sql
SELECT BIN(-7);

+------------------------------------------------------------------+
| BIN(-7)                                                          |
+------------------------------------------------------------------+
| 1111111111111111111111111111111111111111111111111111111111111001 |
+------------------------------------------------------------------+
```

```sql
SELECT BIN("123q123");

+----------------+
| BIN("123q123") |
+----------------+
| 1111011        |
+----------------+
```

Return a string containing binary representation of a number.

### [`BIT_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bit-length)

The `BIT_LENGTH()` function is used to return the length of a given argument in bits.

Examples:

```sql
SELECT BIT_LENGTH("TiDB");

+--------------------+
| BIT_LENGTH("TiDB") |
+--------------------+
|                 32 |
+--------------------+
```

8 bits per character x 4 characters = 32 bits

```sql
SELECT BIT_LENGTH("PingCAP 123");

+---------------------------+
| BIT_LENGTH("PingCAP 123") |
+---------------------------+
|                        88 |
+---------------------------+
```

8 bits per character (space is counted because it is a non-alphanumeric character) x 11 characters = 88 bits

```sql
SELECT CustomerName, BIT_LENGTH(CustomerName) AS BitLengthOfName FROM Customers;

+--------------------+-----------------+
| CustomerName       | BitLengthOfName |
+--------------------+-----------------+
| Albert Einstein    |             120 |
| Robert Oppenheimer |             144 |
+--------------------+-----------------+
```

> **Note:**
>
> The preceding example operates under the assumption that there is a database with a table named `Customers` and a column inside the table named `CustomerName`.

### [`CHAR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char)

The `CHAR()` function is used to get the corresponding character of a specific ASCII value. It performs the opposite operation of `ASCII()`, which returns the ASCII value of a specific character.

Examples:

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

The `CHAR()` function can also be used to get the corresponding character of ASCII values that extend beyond the standard ASCII range (`0` - `127`).

```sql
/*For extended ASCII: */

SELECT CHAR(128);

+------------+
|  CHAR(128) |
+------------+
|       0x80 |
+------------+
```

The `CHAR()` function can also get the corresponding character value of a unicode value.

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

The `CHAR_LENGTH()` function is used to get the total number of characters in a given argument as an integer.

Examples:

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

> **Note:**
>
> The preceding example operates under the assumption that there is a database with a table named `Customers` and a column inside the table named `CustomerName`.

### [`CHARACTER_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_character-length)

The `CHARACTER_LENGTH()` function is the same as the `CHAR_LENGTH()` function. Both functions can be used synonymously because they generate the same output.

## [`CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat)

The `CONCAT()` function concatenates one or more arguments into a single string.

Syntax:

```sql
CONCAT(str1,str2,...)
```

`str1, str2, ...` is a list of arguments to be concatenated. Each argument can be a string or a number.

Example:

```sql
SELECT CONCAT('TiDB', ' ', 'Server', '-', 1, TRUE);
```

Output:

```sql
+---------------------------------------------+
| CONCAT('TiDB', ' ', 'Server', '-', 1, TRUE) |
+---------------------------------------------+
| TiDB Server-11                              |
+---------------------------------------------+
```

If any of the arguments is `NULL`, `CONCAT()` returns `NULL`.

Example:

```sql
SELECT CONCAT('TiDB', NULL, 'Server');
```

Output:

```sql
+--------------------------------+
| CONCAT('TiDB', NULL, 'Server') |
+--------------------------------+
| NULL                           |
+--------------------------------+
```

In addition to the `CONCAT()` function, you can concatenate strings by placing them adjacent to each other as in the following example. Note that this method does not support numeric types.

```sql
SELECT 'Ti' 'DB' ' ' 'Server';
```

Output:

```sql
+-------------+
| Ti          |
+-------------+
| TiDB Server |
+-------------+
```

### [`CONCAT_WS()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat-ws)

The `CONCAT_WS()` function is a form of [`CONCAT()`](#concat) with a separator, which returns a string concatenated by the specified separator.

Syntax:

```sql
CONCAT_WS(separator,str1,str2,...)
```

- `separator`: the first argument is the separator, which concatenates the remaining arguments that are not `NULL`.
- `str1, str2, ...`: a list of arguments to be concatenated. Each argument can be a string or a number.

Example:

```sql
SELECT CONCAT_WS(',', 'TiDB Server', 'TiKV', 'PD');
```

Output:

```sql
+---------------------------------------------+
| CONCAT_WS(',', 'TiDB Server', 'TiKV', 'PD') |
+---------------------------------------------+
| TiDB Server,TiKV,PD                         |
+---------------------------------------------+
```

- If the separator is an empty string, `CONCAT_WS()` is equivalent to `CONCAT()` and returns the concatenated string of the remaining arguments.

    Example:

    ```sql
    SELECT CONCAT_WS('', 'TiDB Server', 'TiKV', 'PD');
    ```

    Output:

    ```sql
    +--------------------------------------------+
    | CONCAT_WS('', 'TiDB Server', 'TiKV', 'PD') |
    +--------------------------------------------+
    | TiDB ServerTiKVPD                          |
    +--------------------------------------------+
    ```

- If the separator is `NULL`, `CONCAT_WS()` returns `NULL`.

    Example:

    ```sql
    SELECT CONCAT_WS(NULL, 'TiDB Server', 'TiKV', 'PD');
    ```

    Output:

    ```sql
    +----------------------------------------------+
    | CONCAT_WS(NULL, 'TiDB Server', 'TiKV', 'PD') |
    +----------------------------------------------+
    | NULL                                         |
    +----------------------------------------------+
    ```

- If only one of the arguments to be concatenated is not `NULL`, `CONCAT_WS()` returns that argument.

    Example:

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', NULL);
    ```

    Output:

    ```sql
    +-------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', NULL) |
    +-------------------------------------+
    | TiDB Server                         |
    +-------------------------------------+
    ```

- If there are `NULL` arguments to be concatenated, `CONCAT_WS()` skips these `NULL` arguments.

    Example:

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', NULL, 'PD');
    ```

    Output:

    ```sql
    +-------------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', NULL, 'PD') |
    +-------------------------------------------+
    | TiDB Server,PD                            |
    +-------------------------------------------+
    ```

- If there are empty strings to be concatenated, `CONCAT_WS()` does not skip empty strings.

    Example:

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', '', 'PD');
    ```

    Output:

    ```sql
    +-----------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', '', 'PD') |
    +-----------------------------------------+
    | TiDB Server,,PD                         |
    +-----------------------------------------+
    ```

### [`ELT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_elt)

Return string at index number.

### [`EXPORT_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_export-set)

Return a string such that for every bit set in the value bits, you get an on string and for every unset bit, you get an off string.

### [`FIELD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_field)

Return the index (position)of the first argument in the subsequent arguments.

### [`FIND_IN_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_find-in-set)

Return the index position of the first argument within the second argument.

### [`FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_format)

The `FORMAT(X,D[,locale])` function is used to format the number `X` to a format similar to `"#,###,###. ##"`, rounded to `D` decimal places, and return the result as a string.

Arguments:

- `X`: the number to be formatted. It can be a direct numeric value, a numeric string, or a number in scientific notation.
- `D`: the number of decimal places for the returned value. The function rounds the number `X` to `D` decimal places. If `D` is greater than the actual number of decimal places in `X`, the result is padded with zeros to the corresponding length.
- `[locale]`: specifies a locale setting to be used for grouping between decimal points, thousands separators, and separators for resultant numbers. A valid locale value is the same as the valid value of the [`lc_time_names`](https://dev.mysql.com/doc/refman/8.3/en/server-system-variables.html#sysvar_lc_time_names) system variable. If not specified or the region setting is `NULL`, the `'en_US'` region setting is used by default. This argument is optional.

Behaviors:

- If the first argument is a string and contains only numbers, the function returns a result based on that numeric value. For example, `FORMAT('12.34', 1)` and `FORMAT(12.34, 1)` return the same result.
- If the first argument is a number represented in scientific notation (using `E/e`), the function returns the result based on that number. For example, `FORMAT('1E2', 3)` returns `100.000`.
- If the first argument is a string starting with non-numeric characters, the function returns zero and a warning `(Code 1292)`. For example, `FORMAT('q12.36', 5)` returns `0.00000`, but also includes a warning `Warning (Code 1292): Truncated incorrect DOUBLE value: 'q12.36'`.
- If the first argument is a string mixing numbers and non-numbers, the function returns a result based on the consecutive numeric part at the beginning of the argument, and also includes a warning `(Code 1292)`. For example, `FORMAT('12.36q56.78', 1)` returns the same numeric result as `FORMAT('12.36', 1)`, but includes a warning `Warning (Code 1292): Truncated incorrect DOUBLE value: '12.36q56.78'`.
- If the second argument is zero or a negative number, the function truncates the decimal part and returns an integer.
- If any of the arguments is `NULL`, the function returns `NULL`.

Examples:

The following examples show how to format the number 12.36 to different decimal places:

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
mysql> SELECT FORMAT(12.36, 2);
+------------------+
| FORMAT(12.36, 2) |
+------------------+
| 12.36            |
+------------------+
```

### [`FROM_BASE64()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_from-base64)

The `FROM_BASE64()` function is used to decode a [Base64](https://datatracker.ietf.org/doc/html/rfc4648) encoded string and return the decoded result in its hexadecimal form.

- This function accepts a single argument, that is, the Base64 encoded string to be decoded.
- If the argument is `NULL` or not a valid Base64 encoded string, the `FROM_BASE64()` function returns `NULL`.

Examples:

The following example shows how to decode the Base64 encoded string `'SGVsbG8gVGlEQg=='`. This string is the result of encoding `'Hello TiDB'`, using the [`TO_BASE64()`](#to_base64) function.

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

The following example shows how to decode the Base64 encoded number `MTIzNDU2`. This string is the result of encoding `123456`, which can be done using the [`TO_BASE64()`](#to_base64) function.

```sql
mysql> SELECT FROM_BASE64('MTIzNDU2');
+--------------------------------------------------+
| FROM_BASE64('MTIzNDU2')                          |
+--------------------------------------------------+
| 0x313233343536                                   |
+--------------------------------------------------+
```

### [`HEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_hex)

The `HEX()` function is used to convert the given argument into a string representation of its hexadecimal value. The argument can be either a string or a number.

- If the argument is a string, `HEX(str)` returns a hexadecimal string representation of `str`. The function converts each byte of each character in `str` into two hexadecimal digits. For example, the character `a` in a UTF-8 or ASCII character set is represented as a binary value of `00111101`, or `61` in hexadecimal notation.
- If the argument is a number, `HEX(n)` returns a hexadecimal string representation of `n`. The function treats the argument `n` as a `BIGINT` number, equivalent to using `CONV(n, 10, 16)`.
- If the argument is `NULL`, the function returns `NULL`.

Examples:

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

The `INSERT(str, pos, len, newstr)` function is used to replace a substring in `str` (that starts at position `pos` and is `len` characters long) with the string `newstr`. This function is multibyte safe.

- If `pos` exceeds the length of `str`, the function returns the original string `str` without modification.
- If `len` exceeds the remaining length of `str` from position `pos`, the function replaces the rest of the string from position `pos`.
- If any argument is `NULL`, the function returns `NULL`.

Examples:

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
SELECT INSERT('He likes tenis', 10, 100, '🍣');
+-------------------------------------------+
| INSERT('He likes tenis', 10, 100, '🍣')     |
+-------------------------------------------+
| He likes 🍣                                 |
+-------------------------------------------+
```

```sql
SELECT INSERT('あああああああ', 2, 3, 'いいい');
+----------------------------------------------------+
| INSERT('あああああああ', 2, 3, 'いいい')           |
+----------------------------------------------------+
| あいいいあああ                                     |
+----------------------------------------------------+
```

```sql
SELECT INSERT('あああああああ', 2, 3, 'xx');
+---------------------------------------------+
| INSERT('あああああああ', 2, 3, 'xx')        |
+---------------------------------------------+
| あxxあああ                                  |
+---------------------------------------------+
```

### [`INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_instr)

The `INSTR(str, substr)` function is used to get the position of the first occurrence of `substr` in `str`. Each argument can be either a string or a number. This function is the same as the two-argument version of [`LOCATE(substr, str)`](#locate), but with the order of the arguments reversed.

> **Note:**
>
> The case sensitivity of `INSTR(str, substr)` is determined by the [collations](/character-set-and-collation.md) used in TiDB. Binary collations (with the suffix `_bin`) are case-sensitive, while general collations (with the suffix `_general_ci` or `_ai_ci`, and) are case-insensitive.

- If either argument is a number, the function treats the number as a string.
- If `substr` is not in `str`, the function returns `0`. Otherwise, it returns the position of the first occurrence of `substr` in `str`.
- If either argument is `NULL`, the function returns `NULL`.

Examples:

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

The `LCASE(str)` function is a synonym for [`LOWER(str)`](#lower), which returns the lowercase of the given argument. 

### [`LEFT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_left)

The `LEFT()` function returns a specified number of characters from the left side of a string.

Syntax:

```sql
LEFT(`str`, `len`)
```

- `str`: the original string to extract characters. If `str` contains a multibyte character, the function counts it as a single code point. 
- `len`: the length of characters to be returned. 
    - If `len` is equal to or less than 0, the function returns an empty string.
    - If `len` is equal to or greater than the length of `str`, the function returns the original `str`. 
- If any argument is `NULL`, the function returns `NULL`.

Examples:

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

The `LENGTH()` function returns the length of a string in bytes.

`LENGTH()` counts a multibyte character as multiple bytes while `CHAR_LENGTH()` counts a multibyte character as a single code point.

If the argument is `NULL`, the function returns `NULL`.

Examples:

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

The `LIKE` operator is used for simple string matching. The expression `expr LIKE pat [ESCAPE 'escape_char']` returns `1` (`TRUE`) or `0` (`FALSE`). If either `expr` or `pat` is `NULL`, the result is `NULL`.

You can use the following two wildcard parameters with `LIKE`:

- `%` matches any number of characters, including zero characters.
- `_` matches exactly one character.

The following examples use the `utf8mb4_bin` collation:

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

The default escape character is `\`:

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

To specify a different escape character, such as `*`, you can use the `ESCAPE` clause:

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

You can use the `LIKE` operator to match a numeric value:

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

To specify a collation explicitly, such as `utf8mb4_unicode_ci`, you can use `COLLATE`:

```sql
SELECT '🍣🍺Sushi🍣🍺' COLLATE utf8mb4_unicode_ci LIKE '%SUSHI%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

### [`LOCATE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_locate)

The `LOCATE(substr, str[, pos])` function is used to get the position of the first occurrence of a specified substring `substr` in a string `str`. The `pos` argument is optional and specifies the starting position for the search.

- If the substring `substr` is not present in `str`, the function returns `0`.
- If any argument is `NULL`, the function returns `NULL`.
- This function is multibyte safe and performs a case-sensitive search only if at least one argument is a binary string.

The following examples use the `utf8mb4_bin` collation:

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
SELECT LOCATE('い', 'たいでぃーびー');
+----------------------------------------+
| LOCATE('い', 'たいでぃーびー')         |
+----------------------------------------+
|                                      2 |
+----------------------------------------+
```

```sql
SELECT LOCATE('い', 'たいでぃーびー', 3);
+-------------------------------------------+
| LOCATE('い', 'たいでぃーびー', 3)         |
+-------------------------------------------+
|                                         0 |
+-------------------------------------------+
```

The following examples use the `utf8mb4_unicode_ci` collation:

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
SELECT LOCATE('い', 'たいでぃーびー', 3);
+-------------------------------------------+
| LOCATE('い', 'たいでぃーびー', 3)         |
+-------------------------------------------+
|                                         4 |
+-------------------------------------------+
```

```sql
SELECT LOCATE('🍺', '🍣🍣🍣🍺🍺');
+----------------------------------------+
| LOCATE('🍺', '🍣🍣🍣🍺🍺')            |
+----------------------------------------+
|                                      1 |
+----------------------------------------+
```

The following multibyte and binary string examples use the `utf8mb4_bin` collation:

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

The `LOWER(str)` function is used to convert all characters in the given argument `str` to lowercase. The argument can be either a string or a number.

- If the argument is a string, the function returns the string in lowercase.
- If the argument is a number, the function returns the number without leading zeros.
- If the argument is `NULL`, the function returns `NULL`.

Examples:

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

Return the string argument, left-padded with the specified string.

### [`LTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ltrim)

Remove leading spaces.

### [`MAKE_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_make-set)

Return a set of comma-separated strings that have the corresponding bit in bits set.

### [`MID()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_mid)

Return a substring starting from the specified position.

### [`NOT LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like)

Negation of simple pattern matching.

### [`NOT REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp)

Negation of `REGEXP`.

### [`OCT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_oct)

Return a string containing octal representation of a number.

### [`OCTET_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_octet-length)

Synonym for `LENGTH()`.

### [`ORD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ord)

Return character code for leftmost character of the argument.

### [`POSITION()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_position)

Synonym for `LOCATE()`.

### [`QUOTE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_quote)

Escape the argument for use in an SQL statement.

### [`REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)

Pattern matching using regular expressions.

### [`REGEXP_INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-instr)

Return the starting index of the substring that matches the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)).

### [`REGEXP_LIKE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-like)

Whether the string matches the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)).

### [`REGEXP_REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-replace)

Replace substrings that match the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)).

### [`REGEXP_SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-substr)

Return the substring that matches the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)).

### [`REPEAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_repeat)

Repeat a string the specified number of times.

### [`REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_replace)

Replace occurrences of a specified string.

### [`REVERSE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_reverse)

Reverse the characters in a string.

### [`RIGHT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_right)

Return the specified rightmost number of characters.

### [`RLIKE`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)

Synonym for `REGEXP`.

### [`RPAD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rpad)

Append string the specified number of times.

### [`RTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rtrim)

Remove trailing spaces.

### [`SPACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_space)

Return a string of the specified number of spaces.

### [`STRCMP()`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp)

Compare two strings.

### [`SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substr)

Return the substring as specified.

### [`SUBSTRING()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring)

Return the substring as specified.

### [`SUBSTRING_INDEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring-index)

The `SUBSTRING_INDEX()` function is used to extract a substring from a string based on a specified delimiter and count. This function is particularly useful when dealing with data separated by a specific delimiter, such as parsing CSV data or processing log files.

Syntax:

```sql
SUBSTRING_INDEX(str, delim, count)
```

- `str`: specifies the string to be processed.
- `delim`: specifies the delimiter in the string, which is case-sensitive.
- `count`: specifies the number of occurrences of the delimiter.
    - If `count` is a positive number, the function returns the substring before the `count` occurrences (counting from the left of the string) of the delimiter.
    - If `count` is a negative number, the function returns the substring after the `count` occurrences (counting from the right of the string) of the delimiter.
    - If `count` is `0`, the function returns an empty string.

Example 1:

```sql
SELECT SUBSTRING_INDEX('www.tidbcloud.com', '.', 2);
```

Result 1:

```sql
+-----------------------------------------+
| SUBSTRING_INDEX('www.tidbcloud.com', '.', 2) |
+-----------------------------------------+
| www.tidbcloud                                |
+-----------------------------------------+
```

Example 2:

```sql
SELECT SUBSTRING_INDEX('www.tidbcloud.com', '.', -1);
```

Result 2:

```sql
+------------------------------------------+
| SUBSTRING_INDEX('www.tidbcloud.com', '.', -1) |
+------------------------------------------+
| com                                      |
+------------------------------------------+
```

### [`TO_BASE64()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_to-base64)

The `TO_BASE64()` function is used to convert the given argument to a string in the base-64 encoded form and return the result according to the character set and collation of the current connection. A base-64 encoded string can be decoded using the [`FROM_BASE64()`](#from_base64) function.

Syntax:

```sql
TO_BASE64(str)
```

- If the argument is not a string, the function converts it to a string before base-64 encoding.
- If the argument is `NULL`, the function returns `NULL`.

Example 1:

```sql
SELECT TO_BASE64('abc');
```

Result 1:

```sql
+------------------+
| TO_BASE64('abc') |
+------------------+
| YWJj             |
+------------------+
```

Example 2:

```sql
SELECT TO_BASE64(6);
```

Result 2:

```sql
+--------------+
| TO_BASE64(6) |
+--------------+
| Ng==         |
+--------------+
```

### [`TRANSLATE()`](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/TRANSLATE.html#GUID-80F85ACB-092C-4CC7-91F6-B3A585E3A690)

Replace all occurrences of characters by other characters in a string. It does not treat empty strings as `NULL` as Oracle does.

### [`TRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_trim)

Remove leading and trailing spaces.

### [`UCASE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ucase)

Synonym for `UPPER()`.

### [`UNHEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_unhex)

Return a string containing hex representation of a number.

### [`UPPER()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_upper)

Convert to uppercase.

### [`WEIGHT_STRING()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_weight-string)

Return the weight string for the input string.

## Unsupported functions

* `LOAD_FILE()`
* `MATCH()`
* `SOUNDEX()`

## Regular expression compatibility with MySQL

The following sections describe the regular expression compatibility with MySQL.

### Syntax compatibility

MySQL implements regular expression using International Components for Unicode (ICU), and TiDB uses RE2. To learn the syntax differences between the two libraries, you can refer to the [ICU documentation](https://unicode-org.github.io/icu/userguide/) and [RE2 Syntax](https://github.com/google/re2/wiki/Syntax).

### `match_type` compatibility

The value options of `match_type` between TiDB and MySQL are:

- Value options in TiDB are `"c"`, `"i"`, `"m"`, and `"s"`, and value options in MySQL are `"c"`, `"i"`, `"m"`, `"n"`, and `"u"`.
- The `"s"` in TiDB corresponds to `"n"` in MySQL. When `"s"` is set in TiDB, the `.` character also matches line terminators (`\n`).

    For example, the `SELECT REGEXP_LIKE(a, b, "n") FROM t1` in MySQL is the same as the `SELECT REGEXP_LIKE(a, b, "s") FROM t1` in TiDB.

- TiDB does not support `"u"`, which means Unix-only line endings in MySQL.

### Data type compatibility

The difference between TiDB and MySQL support for the binary string type:

- MySQL does not support binary strings in regular expression functions since 8.0.22. For more details, refer to [MySQL documentation](https://dev.mysql.com/doc/refman/8.0/en/regexp.html). But in practice, regular functions can work in MySQL when all parameters or return types are binary strings. Otherwise, an error will be reported.
- Currently, TiDB prohibits using binary strings and an error will be reported under any circumstances.

### Other compatibility

The difference between TiDB and MySQL support in replacing empty strings:

The following takes `REGEXP_REPLACE("", "^$", "123")` as an example:

- MySQL does not replace the empty string and returns `""` as the result.
- TiDB replaces the empty string and returns `"123"` as the result.
