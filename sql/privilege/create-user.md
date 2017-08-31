---
title: Create User 语句
category: user guide
---

# 语法
```sql
CREATE USER [IF NOT EXISTS]
    user [auth_spec] [, user [auth_spec]] ...

user:
    参见[用户账号名](user-account-name.md)。

auth_spec: {
    IDENTIFIED BY 'auth_string'
  | IDENTIFIED BY PASSWORD 'hash_string'
}
```

* IDENTIFIED BY 'auth_string'

设置登录密码，auth_string 将会被 TiDB 经过加密存储在 mysql.user 表中。

* IDENTIFIED BY PASSWORD 'hash_string'

设置登录密码，hash_string 将会被 TiDB 经过加密存储在 mysql.user 表中。目前这个行为和 MySQL 不一致，会在接下来的版本中修改为和 MySQL 一致的行为。