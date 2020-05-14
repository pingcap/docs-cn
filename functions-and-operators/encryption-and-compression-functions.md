---
title: 加密和压缩函数
category: reference
---

# 加密和压缩函数

| 函数名      | 功能描述      |
|:-----------|:----------------------------|
| [`MD5()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_md5)                                                             | 计算字符串的 MD5 校验和        |
| [`PASSWORD()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_password)                                | 计算并返回密码字符串          |
| [`RANDOM_BYTES()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_random-bytes)                                           | 返回随机字节向量                       |
| [`SHA1()`, `SHA()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha1)                                                    | 计算 SHA-1 160 位校验和               |
| [`SHA2()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha2)                                                           | 计算 SHA-2 校验和                       |
| [`AES_DECRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-decrypt)                                             | 使用 AES 解密                             |
| [`AES_ENCRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-encrypt)                                             | 使用 AES 加密                                 |
| [`COMPRESS()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_compress)                                                   | 返回经过压缩的二进制字符串                |
| [`UNCOMPRESS()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompress)                                               | 解压缩字符串                   |
| [`UNCOMPRESSED_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompressed-length)                             | 返回字符串解压后的长度  |
| [`CREATE_ASYMMETRIC_PRIV_KEY()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-asymmetric-priv-key)    | 创建私钥                              |
| [`CREATE_ASYMMETRIC_PUB_KEY()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-asymmetric-pub-key)      | 创建公钥                                 |
| [`CREATE_DH_PARAMETERS()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-dh-parameters)                | 创建 DH 共享密钥                        |
| [`CREATE_DIGEST()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-digest)                              | 从字符串创建摘要                      |
| [`ASYMMETRIC_DECRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-decrypt)                    | 使用公钥或私钥解密密文    |
| [`ASYMMETRIC_DERIVE()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-derive)                    | 从非对称密钥导出对称密钥        |
| [`ASYMMETRIC_ENCRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-encrypt)                    | 使用公钥或私钥加密明文   |
| [`ASYMMETRIC_SIGN()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-sign)                          | 从摘要创建签名                    |
| [`ASYMMETRIC_VERIFY()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-verify)                      | 验证签名字符串是否匹配摘要字符串             |
