---
title: 与 MySQL 安全特性差异
aliases: ['/docs-cn/dev/security-compatibility-with-mysql/','/docs-cn/dev/reference/security/compatibility/']
---

# 与 MySQL 安全特性差异

除以下功能外，TiDB 支持与 MySQL 5.7 类似的安全特性。

- 仅支持 `mysql_native_password` 密码验证或证书验证登陆方案。
- 不支持外部身份验证方式（如 LDAP）。
- 不支持列级别权限设置。
- 不支持密码过期，最后一次密码变更记录以及密码生存期。[#9709](https://github.com/pingcap/tidb/issues/9709)
- 不支持权限属性 `max_questions`，`max_updated`，`max_connections` 以及 `max_user_connections`。
- 不支持密码验证。[#9741](https://github.com/pingcap/tidb/issues/9741)
