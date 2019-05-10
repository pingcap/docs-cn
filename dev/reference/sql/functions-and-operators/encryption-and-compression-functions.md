---
title: Encryption and Compression Functions
summary: Learn about the encryption and compression functions.
category: reference
aliases: ['/docs/sql/encryption-and-compression-functions/']
---

# Encryption and Compression Functions

| Name                                                                                                                                               | Description                                       |
|:------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------|
| [`MD5()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_md5)                                                             | Calculate MD5 checksum                            |
| [`PASSWORD()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_password)                                | Calculate and return a password string            |
| [`RANDOM_BYTES()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_random-bytes)                                           | Return a random byte vector                       |
| [`SHA1(), SHA()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha1)                                                    | Calculate an SHA-1 160-bit checksum               |
| [`SHA2()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha2)                                                           | Calculate an SHA-2 checksum                       |
| [`AES_DECRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-decrypt)                                             | Decrypt using AES                                 |
| [`AES_ENCRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-encrypt)                                             | Encrypt using AES                                 |
| [`COMPRESS()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_compress)                                                   | Return result as a binary string                  |
| [`UNCOMPRESS()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompress)                                               | Uncompress a string compressed                    |
| [`UNCOMPRESSED_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompressed-length)                             | Return the length of a string before compression  |
| [`CREATE_ASYMMETRIC_PRIV_KEY()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-asymmetric-priv-key)    | Create private key                                |
| [`CREATE_ASYMMETRIC_PUB_KEY()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-asymmetric-pub-key)      | Create public key                                 |
| [`CREATE_DH_PARAMETERS()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-dh-parameters)                | Generate shared DH secret                         |
| [`CREATE_DIGEST()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-digest)                              | Generate digest from string                       |
| [`ASYMMETRIC_DECRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-decrypt)                    | Decrypt ciphertext using private or public key    |
| [`ASYMMETRIC_DERIVE()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-derive)                    | Derive symmetric key from asymmetric keys         |
| [`ASYMMETRIC_ENCRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-encrypt)                    | Encrypt cleartext using private or public key     |
| [`ASYMMETRIC_SIGN()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-sign)                          | Generate signature from digest                    |
| [`ASYMMETRIC_VERIFY()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-verify)                      | Verify that signature matches digest              |
