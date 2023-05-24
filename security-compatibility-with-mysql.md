---
title: Security Compatibility with MySQL
summary: Learn TiDB's security compatibilities with MySQL.
aliases: ['/docs/dev/security-compatibility-with-mysql/','/docs/dev/reference/security/compatibility/']
---

# Security Compatibility with MySQL

TiDB supports security features similar to MySQL 5.7, and also supports some security features of MySQL 8.0. The security features of TiDB are different from MySQL in implementation.

## Unsupported security features

- Column level permissions.
- These permission attributes: `max_questions`, `max_updated`, and `max_user_connections`.
- Password verification policy, which requires you to verify the current password when you change it.
- Dual password policy.
- Random password generation.
- Multi-factor authentication.

## Differences with MySQL

### Password expiration policy

The password expiration policies of TiDB and MySQL have the following differences:

- MySQL supports password expiration policy in v5.7 and v8.0.
- TiDB supports password expiration policy starting from v6.5.0.

The expiration mechanism of TiDB is different from MySQL in the following aspects:

- In MySQL v5.7 and v8.0, the configuration of the client and the server combined together determines whether to enable "sandbox mode" for the client connection.
- In TiDB, the [`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) configuration item alone determines whether to enable "sandbox mode" for the client connection.

### Password complexity policy

The password complexity policies of TiDB and MySQL have the following differences:

- MySQL v5.7 implements the password complexity policy by using the `validate_password` plugin.
- MySQL v8.0 re-implements the password complexity policy by using the `validate_password` component.
- TiDB introduces a built-in password complexity management feature starting from v6.5.0.

The feature implementation has the following differences:

- Enable the feature:

    - In MySQL v5.7, the feature is implemented by using the `validate_password` plugin. You can enable the feature by installing the plugin.
    - In MySQL v8.0, the feature is implemented by using the `validate_password` component. You can enable the feature by installing the component.
    - For TiDB, this feature is built-in. You can enable the feature using the system variable [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650).

- Dictionary check:

    - In MySQL v5.7, you can specify a file path using the `validate_password_dictionary_file` variable. The file contains a list of words that are not allowed to exist in passwords.
    - In MySQL v8.0, you can specify a file path using the `validate_password.dictionary_file` variable. The file contains a list of words that are not allowed to exist in passwords.
    - In TiDB, you can specify a string using the [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-new-in-v650) system variable. The string contains a list of words that are not allowed to exist in passwords.

### Password failure tracking

The password failure tracking policies of TiDB and MySQL have the following differences:

- MySQL v5.7 does not support password failure tracking.
- MySQL v8.0 supports password failure tracking.
- TiDB supports password failure tracking starting from v6.5.0.

Because the number of failed attempts and lock status of accounts need to be globally consistent, and as a distributed database, TiDB cannot record the number of failed attempts and lock status in the server memory like MySQL, so the implementation mechanisms are different between TiDB and MySQL.

- For users that are not locked automatically, the count of failed attempts is reset in the following scenarios:

    + MySQL 8.0:

        - When the server is restarted, the count of failed attempts for all accounts is reset.
        - When `FLUSH PRIVILEGES` is executed, the count of failed attempts for all accounts is reset.
        - When you run `ALTER USER ... ACCOUNT UNLOCK` to unlock an account, the count is reset.
        - When an account logs in successfully, the count is reset.

    + TiDB:

        - When you run `ALTER USER ... ACCOUNT UNLOCK` to unlock an account, the count is reset.
        - When an account logs in successfully, the count is reset.

- For users that are locked automatically, the count of failed attempts is reset in the following scenarios:

    + MySQL 8.0:

        - When the server is restarted, the temporary locking for all accounts is reset.
        - When `FLUSH PRIVILEGES` is executed, the temporary locking for all accounts is reset.
        - If the lock time of an account ends, the temporary locking for the account is reset on the next login attempt.
        - When you run `ALTER USER ... ACCOUNT UNLOCK` to unlock an account, the temporary locking for the account is reset.

    + TiDB:

        - If the lock time of an account ends, the temporary locking for the account is reset on the next login attempt.
        - When you run `ALTER USER ... ACCOUNT UNLOCK` to unlock an account, the temporary locking for the account is reset.

### Password reuse policy

The password reuse policies of TiDB and MySQL have the following differences:

- MySQL v5.7 does not support password reuse management.
- MySQL v8.0 supports password reuse management.
- TiDB supports password reuse management starting from v6.5.0.

The implementation mechanisms are consistent between TiDB and MySQL. Both use the `mysql.password_history` system table to implement the password reuse management feature. However, when deleting a user that does not exist in the `mysql.user` system table, TiDB and MySQL have different behaviors:

- Scenario: A user (`user01`) is not created in a normal way; instead, it is created by using the `INSERT INTO mysql.password_history VALUES (...)` statement to append a record of `user01` to the `mysql.password_history` system table. In such cases, because the record of `user01` does not exist in the `mysql.user` system table, when you run `DROP USER` on `user01`, TiDB and MySQL have different behaviors.

    - MySQL: When you run `DROP USER user01`, MySQL tries to find `user01` in `mysql.user` and `mysql.password_history`. If either system table contains `user01`, the `DROP USER` statement is executed successfully and no error is reported.
    - TiDB: When you run `DROP USER user01`, TiDB tries to find `user01` only in `mysql.user`. If no related record is found, the `DROP USER` statement fails and an error is reported. If you want to execute the statement successfully and delete the `user01` record from `mysql.password_history`, use `DROP USER IF EXISTS user01` instead.

## Authentication plugin status

TiDB supports multiple authentication methods. These methods can be specified on a per user basis using [`CREATE USER`](/sql-statements/sql-statement-create-user.md) and [`ALTER USER`](/sql-statements/sql-statement-create-user.md). These methods are compatible with the authentication methods of MySQL with the same names.

You can use one of the following supported authentication methods in the table. To specify a default method that the server advertises when the client-server connection is being established, set the [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) variable. `tidb_sm3_password` is the SM3 authentication method only supported in TiDB. Therefore, to authenticate using this method, you must connect to TiDB using [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3). `tidb_auth_token` is a JSON Web Token (JWT) based authentication method used only in TiDB Cloud.

<CustomContent platform="tidb">

The support for TLS authentication is configured differently. For detailed information, see [Enable TLS between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

The support for TLS authentication is configured differently. For detailed information, see [Enable TLS between TiDB Clients and Servers](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers).

</CustomContent>

| Authentication Method        | Supported        |
| :----------------------------| :--------------- |
| `mysql_native_password`      | Yes              |
| `sha256_password`            | No               |
| `caching_sha2_password`      | Yes, since 5.2.0 |
| `auth_socket`                | Yes, since 5.3.0 |
| `tidb_sm3_password`          | Yes, since 6.3.0 |
| `tidb_auth_token`            | Yes, since 6.4.0 |
| `authentication_ldap_sasl`   | Yes, since 7.1.0 |
| `authentication_ldap_simple` | Yes, since 7.1.0 |
| TLS Certificates             | Yes              |
| LDAP                         | Yes, since 7.1.0 |
| PAM                          | No               |
| ed25519 (MariaDB)            | No               |
| GSSAPI (MariaDB)             | No               |
| FIDO                         | No               |
