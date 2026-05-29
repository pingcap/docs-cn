---
title: 加密和压缩函数
aliases: ['/docs-cn/dev/functions-and-operators/encryption-and-compression-functions/','/docs-cn/dev/reference/sql/functions-and-operators/encryption-and-compression-functions/']
summary: TiDB 支持 MySQL 8.0 中提供的大部分加密和压缩函数。
---

# 加密和压缩函数

TiDB 支持使用 MySQL 8.0 中提供的大部分[加密和压缩函数](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html)。

## 支持的函数

| 函数名                                                           | 功能描述              |
|:--------------------------------------------------------------|:------------------|
| [`AES_DECRYPT()`](#aes_decrypt)                               | 使用 AES 解密         |
| [`AES_ENCRYPT()`](#aes_encrypt)                               | 使用 AES 加密         |
| [`COMPRESS()`](#compress)                                     | 返回压缩后的二进制字符串      |
| [`MD5()`](#md5)                                               | 计算字符串的 MD5 校验和    |
| [`PASSWORD()`](#password)                                     | 计算并返回密码字符串        |
| [`RANDOM_BYTES()`](#random_bytes)                             | 返回随机字节向量          |
| [`SHA()`](#sha)                                               | 计算 SHA-1 160 位校验和 |
| [`SHA1()`](#sha1)                                             | 计算 SHA-1 160 位校验和 |
| [`SHA2()`](#sha2)                                             | 计算 SHA-2 校验和      |
| [`SM3()`](#sm3)                                               | 计算 SM3 校验和        |
| [`UNCOMPRESS()`](#uncompress)                                 | 解压缩字符串            |
| [`UNCOMPRESSED_LENGTH()`](#uncompressed_length)               | 返回字符串压缩前的长度       |
| [`VALIDATE_PASSWORD_STRENGTH()`](#validate_password_strength) | 计算密码强度            |

### `AES_DECRYPT()`

`AES_DECRYPT(data, key [,iv])` 函数使用相同的 `key` 解密之前由 [`AES_ENCRYPT()`](#aes_encrypt) 函数加密的 `data`。

你可以使用系统变量 [`block_encryption_mode`](/system-variables.md#block_encryption_mode) 选择[高级加密标准 (AES)](https://zh.wikipedia.org/wiki/高级加密标准) 加密模式。

对于需要初始化向量的加密模式，使用 `iv` 参数设置。默认值为 `NULL`。

```sql
SELECT AES_DECRYPT(0x28409970815CD536428876175F1A4923, 'secret');
```

```
+----------------------------------------------------------------------------------------------------------------------+
| AES_DECRYPT(0x28409970815CD536428876175F1A4923, 'secret')                                                            |
+----------------------------------------------------------------------------------------------------------------------+
| 0x616263                                                                                                             |
+----------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### `AES_ENCRYPT()`

`AES_ENCRYPT(data, key [,iv])` 函数使用[高级加密标准 (AES)](https://zh.wikipedia.org/wiki/高级加密标准) 算法和 `key` 加密 `data`。

你可以使用系统变量 [`block_encryption_mode`](/system-variables.md#block_encryption_mode) 选择 AES 加密模式。

对于需要初始化向量的加密模式，使用 `iv` 参数设置。默认值为 `NULL`。

```sql
SELECT AES_ENCRYPT(0x616263,'secret');
```

```
+----------------------------------------------------------------+
| AES_ENCRYPT(0x616263,'secret')                                 |
+----------------------------------------------------------------+
| 0x28409970815CD536428876175F1A4923                             |
+----------------------------------------------------------------+
1 row in set (0.00 sec)
```

### `COMPRESS()`

`COMPRESS(expr)` 函数返回输入参数 `expr` 的压缩版本。

- 如果输入参数为 `NULL`，该函数返回 `NULL`。
- 如果输入参数为空字符串，该函数返回零长度值。

对于非零长度输入参数，函数返回具有以下结构的二进制字符串：

- 字节 0 到 3：未压缩长度
- 字节 4 到结尾：zlib 压缩数据

```sql
SELECT COMPRESS(0x414243);
```

```
+------------------------------------------+
| COMPRESS(0x414243)                       |
+------------------------------------------+
| 0x03000000789C72747206040000FFFF018D00C7 |
+------------------------------------------+
1 row in set (0.00 sec)
```

在此输出中，`0x03000000` 表示未压缩长度 (3)，`0x789C72747206040000FFFF018D00C7` 是 zlib 压缩数据。

使用 Python 在 TiDB 外部解码的示例：

```python
import codecs
import zlib

data = codecs.decode('03000000789C72747206040000FFFF018D00C7','hex')
print(int.from_bytes(data[:4], byteorder='little'))  # 3
print(zlib.decompress(data[4:]))  # b'ABC'
```

对于短字符串，`COMPRESS()` 可能返回比输入更多的字节。以下示例显示 100 个 `a` 字符的字符串压缩为 19 字节。

```sql
WITH x AS (SELECT REPEAT('a',100) 'a')
SELECT LENGTH(a),LENGTH(COMPRESS(a)) FROM x;
```

```
+-----------+---------------------+
| LENGTH(a) | LENGTH(COMPRESS(a)) |
+-----------+---------------------+
|       100 |                  19 |
+-----------+---------------------+
1 row in set (0.00 sec)
```

### `MD5()`

`MD5(expr)` 函数为给定参数 `expr` 计算 128 位 [MD5](https://zh.wikipedia.org/wiki/MD5) 哈希值。

```sql
SELECT MD5('abc');
```

```
+----------------------------------+
| MD5('abc')                       |
+----------------------------------+
| 900150983cd24fb0d6963f7d28e17f72 |
+----------------------------------+
1 row in set (0.00 sec)
```

### `PASSWORD()`

> **警告：**
>
> `PASSWORD()` 函数在 MySQL 5.7 中已弃用，在 MySQL 8.0 中已删除，在 TiDB 中也已弃用。不建议使用此函数。

`PASSWORD(str)` 函数计算可用于 `mysql_native_password` 认证方法的密码哈希。

```sql
SELECT PASSWORD('secret');
```

```
+-------------------------------------------+
| PASSWORD('secret')                        |
+-------------------------------------------+
| *14E65567ABDB5135D0CFD9A70B3032C179A49EE7 |
+-------------------------------------------+
1 row in set, 1 warning (0.00 sec)

Warning (Code 1681): PASSWORD is deprecated and will be removed in a future release.
```

### `RANDOM_BYTES()`

`RANDOM_BYTES(n)` 函数返回 `n` 个随机字节。

```sql
SELECT RANDOM_BYTES(3);
```

```
+----------------------------------+
| RANDOM_BYTES(3)                  |
+----------------------------------+
| 0x1DBC0D                         |
+----------------------------------+
1 row in set (0.00 sec)
```

### `SHA()`

`SHA()` 函数是 [`SHA1`](#sha1) 的别名。

### `SHA1()`

`SHA1(expr)` 函数为给定参数 `expr` 计算 160 位 [SHA-1](https://zh.wikipedia.org/wiki/SHA-1) 哈希值。

```sql
SELECT SHA1('abc');
```

```
+------------------------------------------+
| SHA1('abc')                              |
+------------------------------------------+
| a9993e364706816aba3e25717850c26c9cd0d89d |
+------------------------------------------+
1 row in set (0.00 sec)
```

### `SHA2()`

`SHA2(str, n)` 函数使用 [SHA-2](https://zh.wikipedia.org/wiki/SHA-2) 系列中的算法计算哈希值。参数 `n` 用于选择算法。如果任一参数为 `NULL` 或 `n` 指定的算法未知或不受支持，`SHA2()` 返回 `NULL`。

以下列出支持的算法：

| n   | 算法      |
|-----|---------|
| 0   | SHA-256 |
| 224 | SHA-224 |
| 256 | SHA-256 |
| 384 | SHA-384 |
| 512 | SHA-512 |

```sql
SELECT SHA2('abc',224);
```

```
+----------------------------------------------------------+
| SHA2('abc',224)                                          |
+----------------------------------------------------------+
| 23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7 |
+----------------------------------------------------------+
1 row in set (0.00 sec)
```

### `SM3()`

> **注意：**
>
> `SM3()` 函数是 TiDB 扩展，未在 MySQL 中实现。

`SM3(str)` 函数为给定参数 `str` 计算 256 位 [ShangMi 3 (SM3)](https://zh.wikipedia.org/wiki/SM3) 哈希值。

```sql
SELECT SM3('abc');
```

```
+------------------------------------------------------------------+
| SM3('abc')                                                       |
+------------------------------------------------------------------+
| 66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0 |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### `UNCOMPRESS()`

`UNCOMPRESS(data)` 函数解压缩使用 [`COMPRESS()`](#compress) 函数压缩的数据。

```sql
SELECT UNCOMPRESS(0x03000000789C72747206040000FFFF018D00C7);
```

```
+------------------------------------------------------------------------------------------------------------+
| UNCOMPRESS(0x03000000789C72747206040000FFFF018D00C7)                                                       |
+------------------------------------------------------------------------------------------------------------+
| 0x414243                                                                                                   |
+------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### `UNCOMPRESSED_LENGTH()`

`UNCOMPRESSED_LENGTH(data)` 函数返回压缩数据的前 4 个字节，即字符串在使用 [`COMPRESS()`](#compress) 函数压缩之前的长度。

```sql
SELECT UNCOMPRESSED_LENGTH(0x03000000789C72747206040000FFFF018D00C7);
```

```
+---------------------------------------------------------------+
| UNCOMPRESSED_LENGTH(0x03000000789C72747206040000FFFF018D00C7) |
+---------------------------------------------------------------+
|                                                             3 |
+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

### `VALIDATE_PASSWORD_STRENGTH()`

`VALIDATE_PASSWORD_STRENGTH(str)` 函数用作 [TiDB 密码管理](/password-management.md)的一部分，它计算密码的强度并返回一个 0 到 100 之间的整数值。

[`validate_password.*`](/system-variables.md) 系统变量影响 `VALIDATE_PASSWORD_STRENGTH()` 函数的行为。

示例：

- 要启用密码复杂度检查，将系统变量 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 设置为 `ON`：

    ```sql
    SET GLOBAL validate_password.enable=ON;
    ```

- 查看密码验证相关的系统变量：

    ```sql
    SHOW VARIABLES LIKE 'validate_password.%';
    ```

    ```
    +--------------------------------------+--------+
    | Variable_name                        | Value  |
    +--------------------------------------+--------+
    | validate_password.check_user_name    | ON     |
    | validate_password.dictionary         |        |
    | validate_password.enable             | ON     |
    | validate_password.length             | 8      |
    | validate_password.mixed_case_count   | 1      |
    | validate_password.number_count       | 1      |
    | validate_password.policy             | MEDIUM |
    | validate_password.special_char_count | 1      |
    +--------------------------------------+--------+
    8 rows in set (0.01 sec)
    ```

- 检查空字符串的密码强度，返回 `0`：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('');
    ```

    ```
    +--------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('') |
    +--------------------------------+
    |                              0 |
    +--------------------------------+
    1 row in set (0.00 sec)
    ```

- 检查短字符串 `abcdef` 的密码强度，返回 `25`：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('abcdef');
    ```

    ```
    +--------------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('abcdef') |
    +--------------------------------------+
    |                                   25 |
    +--------------------------------------+
    1 row in set (0.00 sec)
    ```

- 检查较长字符串 `abcdefghi` 的密码强度，返回 `50`。此字符串长于 [`validate_password.length`](/system-variables.md#validate_passwordlength-从-v650-版本开始引入) 的默认值：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('abcdefghi');
    ```

    ```
    +-----------------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('abcdefghi') |
    +-----------------------------------------+
    |                                      50 |
    +-----------------------------------------+
    1 row in set (0.00 sec)
    ```

- 向字符串添加大写字符不会提高密码强度：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi');
    ```

    ```
    +-----------------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('Abcdefghi') |
    +-----------------------------------------+
    |                                      50 |
    +-----------------------------------------+
    1 row in set (0.01 sec)
    ```

- 向字符串添加数字也不会提高密码强度：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi123');
    ```

    ```
    +--------------------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('Abcdefghi123') |
    +--------------------------------------------+
    |                                         50 |
    +--------------------------------------------+
    1 row in set (0.00 sec)
    ```

- 最后，向字符串添加特殊字符将密码强度提高到 `100`，表示密码强度很高：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi123%$#');
    ```

    ```
    +-----------------------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('Abcdefghi123%$#') |
    +-----------------------------------------------+
    |                                           100 |
    +-----------------------------------------------+
    1 row in set (0.00 sec)
    ```

## 不支持的函数

* TiDB 不支持只在 MySQL 企业版中支持的函数。见 [Issue #2632](https://github.com/pingcap/tidb/issues/2632)。

## MySQL 兼容性

* TiDB 不支持 `STATEMENT_DIGEST()` 和 `STATEMENT_DIGEST_TEXT()` 函数。
* TiDB 不支持 MySQL 8.0.30 中为 [`AES_ENCRYPT()`](#aes_encrypt) 和 [`AES_DECRYPT`](#aes_decrypt) 新增的 `kdf_name`、`salt` 和 `iterations` 参数。
* MySQL 未实现 [`SM3()`](#sm3) 函数。