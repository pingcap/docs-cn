---
title: Security Compatibility with MySQL
summary: Learn TiDB's security compatibilities with MySQL.
category: reference
aliases: ['/docs/sql/security-compatibility/']
---

# Security Compatibility with MySQL

TiDB supports similar security functionality to MySQL 5.7, with the following exceptions:

- Only the `mysql_native_password` authentication scheme is supported
- External authentication (such as with LDAP) is not currently supported
- Column level permissions are not supported
- Using certificates for authentication is not supported [#9708](https://github.com/pingcap/tidb/issues/9708)
- Password expiry, as well as password last-changed tracking and password lifetime are not supported [#9709](https://github.com/pingcap/tidb/issues/9709)
- The permission attributes `max_questions`, `max_updated`, `max_connections`, `max_user_connections` are not supported
- Password validation is not currently supported [#9741](https://github.com/pingcap/tidb/issues/9741)
- Transparent Data Encryption (TDE) is not currently supported
