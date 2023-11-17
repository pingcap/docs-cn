---
title: 与 MySQL 安全特性差异
---

# 与 MySQL 安全特性差异

TiDB 支持与 MySQL 5.7 类似的安全特性，同时 TiDB 还支持 MySQL 8.0 的部分安全特性。TiDB 的安全特性在实现上与 MySQL 存在差异。

## 不支持的安全功能特性

- 不支持列级别权限设置。
- 不支持权限属性 `max_questions`，`max_updated` 以及 `max_user_connections`。
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

TiDB 支持多种身份验证方式。通过使用 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 语句和 [`ALTER USER`](/sql-statements/sql-statement-create-user.md) 语句，即可创建新用户或更改 TiDB 权限系统内的已有用户。TiDB 身份验证方式与 MySQL 兼容，其名称与 MySQL 保持一致。

TiDB 目前支持的身份验证方式可在以下的表格中查找到。服务器和客户端建立连接时，如要指定服务器对外通告的默认验证方式，可通过 [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) 变量进行设置。`tidb_sm3_password` 为仅在 TiDB 支持的 SM3 身份验证方式，使用该方式登录的用户需要使用 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)。`tidb_auth_token` 为仅用于 TiDB Cloud 内部的基于 JSON Web Token (JWT) 的认证方式。

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
