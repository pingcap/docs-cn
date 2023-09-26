---
title: Encryption and Compression Functions
summary: Learn about the encryption and compression functions.
aliases: ['/docs/dev/functions-and-operators/encryption-and-compression-functions/','/docs/dev/reference/sql/functions-and-operators/encryption-and-compression-functions/']
---

# Encryption and Compression Functions

TiDB supports most of the [encryption and compression functions](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html) available in MySQL 5.7.

## Supported functions

| Name                                                                                                                                               | Description                                       |
|:------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------|
| [`MD5()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_md5)                                                             | Calculate MD5 checksum                            |
| [`PASSWORD()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_password)                                | Calculate and return a password string            |
| [`RANDOM_BYTES()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_random-bytes)                                           | Return a random byte vector                       |
| [`SHA1(), SHA()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha1)                                                    | Calculate an SHA-1 160-bit checksum               |
| [`SHA2()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha2)                                                           | Calculate an SHA-2 checksum                       |
| [`SM3()`](https://en.wikipedia.org/wiki/SM3_(hash_function))                                                    | Calculate an SM3 checksum (currently MySQL does not support this function)                      |
| [`AES_DECRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-decrypt)                                             | Decrypt using AES                                 |
| [`AES_ENCRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-encrypt)                                             | Encrypt using AES                                 |
| [`COMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_compress)                                                   | Return result as a binary string                  |
| [`UNCOMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompress)                                               | Uncompress a string compressed                    |
| [`UNCOMPRESSED_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompressed-length)                             | Return the length of a string before compression  |
| [`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_validate-password-strength) | Validate the password strength |

## Related system variables

The `block_encryption_mode` variable sets the encryption mode that is used for `AES_ENCRYPT()` and `AES_DECRYPT()`.

## Unsupported functions

* `DES_DECRYPT()`, `DES_ENCRYPT()`, `OLD_PASSWORD()`, `ENCRYPT()`: these functions were deprecated in MySQL 5.7 and removed in 8.0.
* Functions only available in MySQL Enterprise [Issue #2632](https://github.com/pingcap/tidb/issues/2632).
