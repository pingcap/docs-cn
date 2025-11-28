---
title: 与 MySQL 安全特性差异
aliases: ['/docs-cn/dev/security-compatibility-with-mysql/','/docs-cn/dev/reference/security/compatibility/']
summary: TiDB 支持与 MySQL 5.7 类似的安全特性，同时也支持 MySQL 8.0 的部分安全特性。然而，在实现上存在一些差异，包括不支持列级别权限设置和部分权限属性。此外，TiDB 的密码过期策略和密码复杂度策略与 MySQL 存在一些差异。另外，TiDB 支持多种身份验证方式，包括 TLS 证书和 JWT。
---

# 与 MySQL 安全特性差异

TiDB 支持与 MySQL 5.7 类似的安全特性，同时 TiDB 还支持 MySQL 8.0 的部分安全特性。TiDB 的安全特性在实现上与 MySQL 存在差异。

## 不支持的安全功能特性

- 不支持列级别权限设置。
- 不支持权限属性 `max_questions`、`max_updated`。
- 不支持密码修改验证策略，修改密码时需要验证当前密码。
- 不支持双密码策略。
- 不支持随机密码生成策略。
- 不支持多因素身份验证。

## 与 MySQL 有差异的安全特性详细说明

### 密码过期策略

针对密码过期策略功能，TiDB 与 MySQL 的比较如下：

- MySQL 5.7 和 8.0 支持密码过期策略管理功能。
- TiDB 从 v6.5.0 起支持密码过期策略管理功能。

TiDB 的密码过期策略功能与 MySQL 保持一致，但是在密码过期处理机制上存在以下差异：

- MySQL 5.7 和 8.0 在密码过期后是否将客户端的连接限制为“沙盒模式”，由客户端和服务端设置的组合确定。
- TiDB 在密码过期后是否将客户端的连接限制为“沙盒模式”，仅由 TiDB 配置文件中的 `[security]` 部分的 [`disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-从-v650-版本开始引入) 选项确定。

### 密码复杂度策略

针对密码复杂度策略功能，TiDB 与 MySQL 的比较如下：

- MySQL 5.7 以 validate_password 插件的形式实现了密码复杂度策略管理功能。
- MySQL 8.0 重新以 validate_password 组件的形式实现了密码复杂度策略管理功能。
- TiDB 从 v6.5.0 起内置实现了密码复杂度策略管理功能。

因此，功能实现上存在以下差异：

- 密码复杂度策略功能如何启用：

    + MySQL 5.7 以 validate_password 插件的形式实现，需要进行插件的安装以启用密码复杂度策略管理。
    + MySQL 8.0 以 validate_password 组件的形式实现，需要进行组件的安装以启用密码复杂度策略管理。
    + TiDB 内置实现了密码复杂度策略管理，支持通过系统变量 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 启用密码复杂度策略管理。

- 密码字典功能：

    + MySQL 5.7 通过变量 `validate_password_dictionary_file` 指定一个文件路径，在文件中写入密码中不允许包含的单词。
    + MySQL 8.0 通过变量 `validate_password.dictionary_file` 指定一个文件路径，在文件中写入密码中不允许包含的单词。
    + TiDB 通过变量 [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-从-v650-版本开始引入) 指定一个字符串，在该字符串中写入密码中不允许包含的单词。

### 密码连续错误限制登录策略

针对密码连续错误限制登录策略功能，TiDB 与 MySQL 的比较如下：

- MySQL 5.7 不支持密码连续错误限制登录策略管理功能。
- MySQL 8.0 支持密码连续错误限制登录策略管理功能。
- TiDB 从 v6.5.0 起支持密码连续错误限制登录策略管理功能。

因为用户的失败尝试次数和锁定状态需要做到全局一致，而 TiDB 是分布式数据库，不能像 MySQL 在服务端的内存中记录失败尝试次数和锁定状态，所以实现机制存在以下差异：

- 用户未被自动锁定，失败尝试次数的计数重置场景：

    + MySQL 8.0：

        - 服务器重启时，所有用户失败尝试次数的计数都会被重置。
        - 执行 `FLUSH PRIVILEGES` 时，所有用户失败尝试次数的计数都会被重置。
        - 对该用户执行 `ALTER USER ... ACCOUNT UNLOCK` 解锁命令时。
        - 该用户登录成功时。

    + TiDB：

        - 对该用户执行 `ALTER USER ... ACCOUNT UNLOCK` 解锁命令时。
        - 该用户登录成功时。

- 账户被自动锁定后的解锁场景：

    + MySQL 8.0：

        - 服务器重启时，所有用户的自动锁定标识都会被重置。
        - 执行 `FLUSH PRIVILEGES` 时，所有用户的自动锁定标识都会被重置。
        - 该用户锁定时间结束，这种情况下，用户的自动锁定标识将在下次登录尝试时重置。
        - 对该用户执行 `ALTER USER ... ACCOUNT UNLOCK` 解锁命令时。

    + TiDB：

        - 该用户锁定时间结束，这种情况下，用户的自动锁定标识将在下次登录尝试时重置。
        - 对该用户执行 `ALTER USER ... ACCOUNT UNLOCK` 解锁命令时。

### 密码重用策略

针对密码重用策略功能，TiDB 与 MySQL 的比较如下：

- MySQL 5.7 不支持密码重用策略管理功能。
- MySQL 8.0 支持密码重用策略管理功能。
- TiDB 从 v6.5.0 起支持密码重用策略管理功能。

TiDB 的密码重用策略功能与 MySQL 一致，在实现密码重用策略时都增加了系统表 `mysql.password_history`，但 TiDB 与 MySQL 在删除 `mysql.user` 系统表中不存在的用户时存在以下差异：

- 场景：没有正确创建用户（例如： `user01` ），而通过 `INSERT INTO mysql.password_history VALUES (...)` 命令直接向 `mysql.password_history` 系统表中添加一条 `user01` 的记录，此时系统表 `mysql.user` 中没有 `user01` 的记录。对该用户执行 `DROP USER` 操作时，TiDB 和 MySQL 状态不一致。
- 差异点：

    + MySQL：执行 `DROP USER user01` 时，在 `mysql.user` 和 `mysql.password_history` 系统表中匹配 `user01`，若在两个系统表或其中一个系统表中匹配成功，则 `DROP USER` 操作可以正常执行，不会报错。
    + TiDB：执行 `DROP USER user01` 时，只在 `mysql.user` 系统表中匹配 `user01`，若没有匹配成功，则 `DROP USER` 操作执行失败，返回报错。此时如果需要成功执行 `DROP USER user01` 操作，删除 `mysql.password_history` 中 `user01` 的记录，请使用 `DROP USER IF EXISTS user01`。

## 可用的身份验证插件

TiDB 支持多种身份验证方式。通过使用 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 语句和 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句，即可创建新用户或更改 TiDB 权限系统内的已有用户。TiDB 身份验证方式与 MySQL 兼容，其名称与 MySQL 保持一致。

TiDB 目前支持的身份验证方式可在以下的表格中查找到。服务器和客户端建立连接时，如要指定服务器对外通告的默认验证方式，可通过 [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) 变量进行设置。`tidb_sm3_password` 为仅在 TiDB 支持的 SM3 身份验证方式，使用该方式登录的用户需要使用 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)。`tidb_auth_token` 用于 TiDB Cloud 内部的基于 JSON Web Token (JWT) 的认证，用户通过配置也可以用于自托管环境。

针对 TLS 身份验证，TiDB 目前采用不同的配置方案。具体情况请参见[为 TiDB 客户端服务端间通信开启加密传输](/enable-tls-between-clients-and-servers.md)。

| 身份验证方式    | 支持        |
| :------------------------| :--------------- |
| `mysql_native_password`  | 是              |
| `sha256_password`        | 否               |
| `caching_sha2_password`  | 是（5.2.0 版本起） |
| `auth_socket`            | 是（5.3.0 版本起） |
| `tidb_sm3_password`      | 是（6.3.0 版本起） |
| `tidb_auth_token`        | 是（6.4.0 版本起） |
| `authentication_ldap_sasl`   | 是（7.1.0 版本起） |
| `authentication_ldap_simple` | 是（7.1.0 版本起） |
| TLS 证书       | 是              |
| LDAP                     | 是（7.1.0 版本起） |
| PAM                      | 否               |
| ed25519 (MariaDB)        | 否               |
| GSSAPI (MariaDB)         | 否               |
| FIDO                     | 否               |

### `tidb_auth_token`

`tidb_auth_token` 是一种基于 [JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519) 的无密码认证方式。在 v6.4.0 中，`tidb_auth_token` 仅用于 TiDB Cloud 内部的用户认证，从 v6.5.0 起，你也可以将 `tidb_auth_token` 配置为 TiDB 自托管环境中用户的认证方式。不同于 `mysql_native_password`、`caching_sha2_password` 等使用密码的认证方式，`tidb_auth_token` 认证方式在创建用户时无需设置并保存自定义密码，在用户登录时只需使用一个签发的 token，从而简化用户的认证过程并提升安全性。

#### JWT

JWT 由 Header、Payload 和 Signature 三部分组成。这三部分分别通过 base64 编码后，使用点号（`.`）拼接成一个字符串，以便在客户端和服务器之间传输。

Header 描述 JWT 的元数据，包含 3 个属性：

* `alg`：表示签名使用的算法，默认为 `RS256`。
* `typ`：表示 token 的类型，为 `JWT`。
* `kid`：表示用于生成 token 签名的 key ID。

Header 示例：

```json
{
  "alg": "RS256",
  "kid": "the-key-id-0",
  "typ": "JWT"
}
```

Payload 是 JWT 的主体部分，用于保存用户的信息。Payload 中的每个字段称为一个 claim（声明）。TiDB 用户认证要求提供的声明如下：

* `iss`：如果[创建用户](/sql-statements/sql-statement-create-user.md)时未指定 `TOKEN_ISSUER` 或者将其设置为了空字符串，则可以不包含该声明；否则 `iss` 应该与 `TOKEN_ISSUER` 设置值相同。
* `sub`：TiDB 中要求该值与待认证的用户名相同。
* `iat`：发布 token 的时间戳。TiDB 中要求该值不得晚于认证时的时间，也不得早于认证前 15 分钟。
* `exp`：token 到期的时间戳。如果 token 在认证时已经过期，则认证失败。
* `email`：邮件地址。创建用户时可以通过 `ATTRIBUTE '{"email": "xxxx@pingcap.com"}'` 指定 email 信息。如果创建用户时未指定 email 信息，则该声明应设置为空字符串；否则该声明应该与创建用户时的设置值相同。

Payload 示例：

```json
{
  "email": "user@pingcap.com",
  "exp": 1703305494,
  "iat": 1703304594,
  "iss": "issuer-abc",
  "sub": "user@pingcap.com"
}
```

Signature 用于对 Header 和 Payload 这两部分数据进行签名。

> **警告：**
>
> - Header 与 Payload 使用 base64 进行编码的过程是可逆的，请勿在 Payload 中携带敏感数据。
> - `tidb_auth_token` 认证方式要求客户端支持 [`mysql_clear_password`](https://dev.mysql.com/doc/refman/8.0/en/cleartext-pluggable-authentication.html) 插件，并将 token 以明文的方式发送至 TiDB，因此请[为 TiDB 开启加密传输](/enable-tls-between-clients-and-servers.md)后再使用 `tidb_auth_token` 进行认证。

#### 使用方法

配置并使用 `tidb_auth_token` 作为 TiDB 自托管环境中用户的认证方式，有以下几个步骤：

1. 在 TiDB 配置文件中设置 [`auth-token-jwks`](/tidb-configuration-file.md#auth-token-jwks-从-v640-版本开始引入) 和 [`auth-token-refresh-interval`](/tidb-configuration-file.md#auth-token-refresh-interval-从-v640-版本开始引入)。

    例如，可以通过下列命令获取示例 JWKS：

    ```bash
    wget https://raw.githubusercontent.com/CbcWestwolf/generate_jwt/master/JWKS.json
    ```

    然后在 TiDB 的配置文件 `config.toml` 中配置上述 JWKS 文件的路径：

    ```toml
    [security]
    auth-token-jwks = "JWKS.json"
    ```

2. 启动 `tidb-server`，并定期更新保存 JWKS 至 `auth-token-jwks` 指定的路径。

3. 创建使用 `tidb_auth_token` 认证的用户，并根据需要通过 `REQUIRE TOKEN_ISSUER` 和 `ATTRIBUTE '{"email": "xxxx@pingcap.com"}` 指定 `iss` 与 `email` 信息。

    例如，创建一个使用 `tidb_auth_token` 认证的用户 `user@pingcap.com`：

    ```sql
    CREATE USER 'user@pingcap.com' IDENTIFIED WITH 'tidb_auth_token' REQUIRE TOKEN_ISSUER 'issuer-abc' ATTRIBUTE '{"email": "user@pingcap.com"}';
    ```

4. 生成并签发用于认证的 token，通过 mysql 客户端的 `mysql_clear_text` 插件进行认证。

    通过 `go install github.com/cbcwestwolf/generate_jwt` 安装 JWT 生成工具。该工具仅用于生成测试 `tidb_auth_token` 的 JWT。例如：

    ```text
    generate_jwt --kid "the-key-id-0" --sub "user@pingcap.com" --email "user@pingcap.com" --iss "issuer-abc"
    ```

    打印公钥和 token 形式如下：

    ```text
    -----BEGIN PUBLIC KEY-----
    MIIBCgKCAQEAq8G5n9XBidxmBMVJKLOBsmdOHrCqGf17y9+VUXingwDUZxRp2Xbu
    LZLbJtLgcln1lC0L9BsogrWf7+pDhAzWovO6Ai4Aybu00tJ2u0g4j1aLiDdsy0gy
    vSb5FBoL08jFIH7t/JzMt4JpF487AjzvITwZZcnsrB9a9sdn2E5B/aZmpDGi2+Is
    f5osnlw0zvveTwiMo9ba416VIzjntAVEvqMFHK7vyHqXbfqUPAyhjLO+iee99Tg5
    AlGfjo1s6FjeML4xX7sAMGEy8FVBWNfpRU7ryTWoSn2adzyA/FVmtBvJNQBCMrrA
    hXDTMJ5FNi8zHhvzyBKHU0kBTS1UNUbP9wIDAQAB
    -----END PUBLIC KEY-----

    eyJhbGciOiJSUzI1NiIsImtpZCI6InRoZS1rZXktaWQtMCIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXJAcGluZ2NhcC5jb20iLCJleHAiOjE3MDMzMDU0OTQsImlhdCI6MTcwMzMwNDU5NCwiaXNzIjoiaXNzdWVyLWFiYyIsInN1YiI6InVzZXJAcGluZ2NhcC5jb20ifQ.T4QPh2hTB5on5xCuvtWiZiDTuuKvckggNHtNaovm1F4RvwUv15GyOqj9yMstE-wSoV5eLEcPC2HgE6eN1C6yH_f4CU-A6n3dm9F1w-oLbjts7aYCl8OHycVYnq609fNnb8JLsQAmd1Zn9C0JW899-WSOQtvjLqVSPe9prH-cWaBVDQXzUJKxwywQzk9v-Z1Njt9H3Rn9vvwwJEEPI16VnaNK38I7YG-1LN4fAG9jZ6Zwvz7vb_s4TW7xccFf3dIhWTEwOQ5jDPCeYkwraRXU8NC6DPF_duSrYJc7d7Nu9Z2cr-E4i1Rt_IiRTuIIzzKlcQGg7jd9AGEfGe_SowsA-w
    ```

    复制上面最后一行的 token 用于登录：

    ```Shell
    mycli -h 127.0.0.1 -P 4000 -u 'user@pingcap.com' -p '<the-token-generated>'
    ```

    注意这里使用的 mysql 客户端必须支持 `mysql_clear_password` 插件。[mycli](https://www.mycli.net/) 默认开启这一插件，如果使用 [mysql 命令行客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)则需要 `--enable-cleartext-plugin` 选项来开启这个插件：

    ```Shell
    mysql -h 127.0.0.1 -P 4000 -u 'user@pingcap.com' -p'<the-token-generated>' --enable-cleartext-plugin
    ```

    如果在生成 token 的时候指定了错误的 `--sub`（比如 `--sub "wronguser@pingcap.com"`），则无法使用该 token 进行认证。

可以使用 [jwt.io](https://jwt.io/) 提供的 debugger 对 token 进行编解码。
