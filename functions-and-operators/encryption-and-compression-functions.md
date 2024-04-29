---
title: 加密和压缩函数
---

# 加密和压缩函数

TiDB 支持使用 MySQL 8.0 中提供的大部分[加密和压缩函数](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html)。

## 支持的函数

| 函数名      | 功能描述      |
|:-----------|:----------------------------|
| [`MD5()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_md5)                                                             | 计算字符串的 MD5 校验和        |
| [`PASSWORD()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_password)                                | 计算并返回密码字符串          |
| [`RANDOM_BYTES()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_random-bytes)                                           | 返回随机字节向量                       |
| [`SHA1()`, `SHA()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha1)                                                    | 计算 SHA-1 160 位校验和               |
| [`SHA2()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha2)                                                           | 计算 SHA-2 校验和                       |
| [`SM3()`](https://zh.m.wikipedia.org/zh-hans/SM3)                                                           | 计算 SM3 校验和（MySQL 中暂不支持该函数）           |
| [`AES_DECRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-decrypt)                                             | 使用 AES 解密                             |
| [`AES_ENCRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-encrypt)                                             | 使用 AES 加密                                 |
| [`COMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_compress)                                                   | 返回经过压缩的二进制字符串                |
| [`UNCOMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompress)                                               | 解压缩字符串                   |
| [`UNCOMPRESSED_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompressed-length)                             | 返回字符串解压后的长度  |
| [`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_validate-password-strength)               | 确定密码强度            |

## 相关系统变量

* [`block_encryption_mode`](/system-variables.md#block_encryption_mode) 变量设置 `AES_ENCRYPT()` 和 `AES_DECRYPT()` 所使用的加密模式。

* [`validate_password.*`](/system-variables.md) 变量影响 `VALIDATE_PASSWORD_STRENGTH()` 函数的行为。

## 不支持的函数

* `DES_DECRYPT()`、`DES_ENCRYPT()`、`OLD_PASSWORD()` 和 `ENCRYPT()`：这些函数在 MySQL 5.7 中被废弃，并且已在 MySQL 8.0 中移除。
* 只在 MySQL 企业版中支持的函数。见 [Issue #2632](https://github.com/pingcap/tidb/issues/2632)。

## MySQL 兼容性

* TiDB 不支持 `STATEMENT_DIGEST()` 和 `STATEMENT_DIGEST_TEXT()` 函数。
