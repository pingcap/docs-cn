---
title: mysql.user
summary: 了解 `mysql` 系统表 `user`。
---

# `mysql.user`

`mysql.user` 表提供用户账户及其权限的信息。

使用以下 SQL 语句查看 `mysql.user` 表的结构：

```sql
DESC mysql.user;
```

输出结果如下：

```
+------------------------+----------------------+------+------+-------------------+-------+
| Field                  | Type                 | Null | Key  | Default           | Extra |
+------------------------+----------------------+------+------+-------------------+-------+
| Host                   | char(255)            | NO   | PRI  | NULL              |       |
| User                   | char(32)             | NO   | PRI  | NULL              |       |
| authentication_string  | text                 | YES  |      | NULL              |       |
| plugin                 | char(64)             | YES  |      | NULL              |       |
| Select_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Insert_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Update_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Delete_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Create_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Drop_priv              | enum('N','Y')        | NO   |      | N                 |       |
| Process_priv           | enum('N','Y')        | NO   |      | N                 |       |
| Grant_priv             | enum('N','Y')        | NO   |      | N                 |       |
| References_priv        | enum('N','Y')        | NO   |      | N                 |       |
| Alter_priv             | enum('N','Y')        | NO   |      | N                 |       |
| Show_db_priv           | enum('N','Y')        | NO   |      | N                 |       |
| Super_priv             | enum('N','Y')        | NO   |      | N                 |       |
| Create_tmp_table_priv  | enum('N','Y')        | NO   |      | N                 |       |
| Lock_tables_priv       | enum('N','Y')        | NO   |      | N                 |       |
| Execute_priv           | enum('N','Y')        | NO   |      | N                 |       |
| Create_view_priv       | enum('N','Y')        | NO   |      | N                 |       |
| Show_view_priv         | enum('N','Y')        | NO   |      | N                 |       |
| Create_routine_priv    | enum('N','Y')        | NO   |      | N                 |       |
| Alter_routine_priv     | enum('N','Y')        | NO   |      | N                 |       |
| Index_priv             | enum('N','Y')        | NO   |      | N                 |       |
| Create_user_priv       | enum('N','Y')        | NO   |      | N                 |       |
| Event_priv             | enum('N','Y')        | NO   |      | N                 |       |
| Repl_slave_priv        | enum('N','Y')        | NO   |      | N                 |       |
| Repl_client_priv       | enum('N','Y')        | NO   |      | N                 |       |
| Trigger_priv           | enum('N','Y')        | NO   |      | N                 |       |
| Create_role_priv       | enum('N','Y')        | NO   |      | N                 |       |
| Drop_role_priv         | enum('N','Y')        | NO   |      | N                 |       |
| Account_locked         | enum('N','Y')        | NO   |      | N                 |       |
| Shutdown_priv          | enum('N','Y')        | NO   |      | N                 |       |
| Reload_priv            | enum('N','Y')        | NO   |      | N                 |       |
| FILE_priv              | enum('N','Y')        | NO   |      | N                 |       |
| Config_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Create_Tablespace_Priv | enum('N','Y')        | NO   |      | N                 |       |
| Password_reuse_history | smallint(5) unsigned | YES  |      | NULL              |       |
| Password_reuse_time    | smallint(5) unsigned | YES  |      | NULL              |       |
| User_attributes        | json                 | YES  |      | NULL              |       |
| Token_issuer           | varchar(255)         | YES  |      | NULL              |       |
| Password_expired       | enum('N','Y')        | NO   |      | N                 |       |
| Password_last_changed  | timestamp            | YES  |      | CURRENT_TIMESTAMP |       |
| Password_lifetime      | smallint(5) unsigned | YES  |      | NULL              |       |
+------------------------+----------------------+------+------+-------------------+-------+
44 rows in set (0.00 sec)
```

`mysql.user` 表包含多个字段，可分为三组：

* 账户相关字段：
    * `Host`：指定 TiDB 用户账户的主机名。
    * `User`：指定 TiDB 用户账户的用户名。
* 权限相关字段：

    以 `_priv` 或 `_Priv` 结尾的字段定义授予用户账户的权限。例如，`Select_priv` 表示用户账户具有全局 `Select` 权限。更多信息，请参考 [TiDB 各操作需要的权限](/privilege-management.md#tidb-各操作需要的权限)。

* 安全相关字段：
    * `authentication_string` 和 `plugin`：`authentication_string` 存储用户账户的凭证。凭证根据 `plugin` 字段指定的认证插件进行验证。
    * `Account_locked`：表示用户账户是否被锁定。
    * `Password_reuse_history` 和 `Password_reuse_time`：用于[密码重用策略](/password-management.md#密码重用策略)。
    * `User_attributes`：提供用户账户注释和用户账户属性信息。
    * `Token_issuer`：用于 [`tidb_auth_token`](/security-compatibility-with-mysql.md#tidb_auth_token) 认证插件。
    * `Password_expired`、`Password_last_changed` 和 `Password_lifetime`：用于[密码过期策略](/password-management.md#密码过期策略)。

虽然 TiDB `mysql.user` 表中的大多数字段也存在于 MySQL `mysql.user` 表中，但 `Token_issuer` 字段是 TiDB 特有的。