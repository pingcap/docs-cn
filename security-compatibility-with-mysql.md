---
title: 与 MySQL 安全特性差异
aliases: ['/docs-cn/dev/security-compatibility-with-mysql/','/docs-cn/dev/reference/security/compatibility/']
---

# 与 MySQL 安全特性差异

除以下功能外，TiDB 支持与 MySQL 5.7 类似的安全特性。

- 不支持列级别权限设置。
- 不支持密码过期，最后一次密码变更记录以及密码生存期。[#9709](https://github.com/pingcap/tidb/issues/9709)
- 不支持权限属性 `max_questions`，`max_updated`，`max_connections` 以及 `max_user_connections`。
- 不支持密码验证。[#9741](https://github.com/pingcap/tidb/issues/9741)

## 可用的身份验证插件

TiDB 支持多种身份验证方式。通过使用 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 语句和 [`ALTER USER`](/sql-statements/sql-statement-create-user.md) 语句，即可创建新用户或更改 TiDB 权限系统内的已有用户。TiDB 身份验证方式与 MySQL 兼容，其名称与 MySQL 保持一致。

TiDB 目前支持的身份验证方式可在以下的表格中查找到。当把身份验证方式设定为默认方法时，服务端会显示当前服务端与客户端之间的连接状态。如需进行其操作，请设置 [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) 参数。

针对 TLS 身份验证，TiDB 目前采用不同的配置方案。具体情况请参见[为 TiDB 客户端服务端间通信开启加密传输](/enable-tls-between-clients-and-servers.md).

| 身份验证方式    | 支持        |
| :------------------------| :--------------- |
| `mysql_native_password`  | 是              |
| `sha256_password`        | 否               |
| `caching_sha2_password`  | 是（5.2.0 版本起） |
| `auth_socket`            | 否               |
| [TLS Certificates]       | 是              |
| LDAP                     | 否               |
| PAM                      | 否               |
| ed25519 (MariaDB)        | 否               |
| GSSAPI (MariaDB)         | 否               |

[TLS 证书]: /enable-tls-between-clients-and-servers.md
