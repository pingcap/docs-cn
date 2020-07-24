---
title: Security Compatibility with MySQL
summary: Learn TiDB's security compatibilities with MySQL.
aliases: ['/docs/dev/security-compatibility-with-mysql/','/docs/dev/reference/security/compatibility/']
---

# Security Compatibility with MySQL

TiDB supports similar security functionality to MySQL 5.7, with the following exceptions:

- Only the `mysql_native_password` password-based and certificate-based authentication is supported
    - In MySQL 8.0, `mysql_native_password` is [no longer the default/preferred plugin](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.html#upgrade-caching-sha2-password). To connect to TiDB using a MySQL client from MySQL 8.0, you must explicitly specify `default-auth=mysql_native_password`.
- External authentication (such as with LDAP) is not currently supported
- Column level permissions are not supported
- Password expiry, as well as password last-changed tracking and password lifetime are not supported [#9709](https://github.com/pingcap/tidb/issues/9709)
- The permission attributes `max_questions`, `max_updated`, `max_connections`, `max_user_connections` are not supported
- Password validation is not currently supported [#9741](https://github.com/pingcap/tidb/issues/9741)