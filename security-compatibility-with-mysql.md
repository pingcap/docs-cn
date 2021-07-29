---
title: Security Compatibility with MySQL
summary: Learn TiDB's security compatibilities with MySQL.
aliases: ['/docs/dev/security-compatibility-with-mysql/','/docs/dev/reference/security/compatibility/']
---

# Security Compatibility with MySQL

TiDB supports similar security functionality to MySQL 5.7, with the following exceptions:

- Column level permissions are not supported
- Password expiry, as well as password last-changed tracking and password lifetime are not supported [#9709](https://github.com/pingcap/tidb/issues/9709)
- The permission attributes `max_questions`, `max_updated`, `max_connections`, `max_user_connections` are not supported
- Password validation is not currently supported [#9741](https://github.com/pingcap/tidb/issues/9741)

## Authentication plugin status

TiDB supports multiple authentication methods. These methods can be specified on a per user basis using [`CREATE USER`](/sql-statements/sql-statement-create-user.md) and [`ALTER USER`](/sql-statements/sql-statement-create-user.md). These methods are compatible with the authentication methods of MySQL with the same names.

You can use one of the following supported authentication methods in the table. To specify a default method that the server advertises when the client-server connection is being established, set the [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) variable.

The support for TLS authentication is configured differently. For detailed information, see [Enable TLS between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md).

| Authentication Method    | Supported        |
| :------------------------| :--------------- |
| `mysql_native_password`  | Yes              |
| `sha256_password`        | No               |
| `caching_sha2_password`  | Yes, since 5.2.0 |
| `auth_socket`            | No               |
| [TLS Certificates]       | Yes              |
| LDAP                     | No               |
| PAM                      | No               |
| ed25519 (MariaDB)        | No               |
| GSSAPI (MariaDB)         | No               |

[TLS Certificates]: /enable-tls-between-clients-and-servers.md
