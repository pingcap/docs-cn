---
title: mysql.user
summary: 了解 `mysql` 架构中的 `user` 表。
---

# `mysql.user`

`mysql.user` 表提供了用户账户及其权限的信息。

要查看 `mysql.user` 的结构，请使用以下 SQL 语句：

```sql
DESC mysql.user;
```

输出如下：

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

`mysql.user` 表包含多个字段，可以分为三类：

<CustomContent platform="tidb">

* 作用域：
    * `Host`：指定 TiDB 账户的主机名。
    * `User`：指定 TiDB 账户的用户名。
* 权限：

    以 `_priv` 或 `_Priv` 结尾的字段定义了授予用户账户的权限。例如，`Select_priv` 表示用户具有全局 `Select` 权限。更多信息，请参见[TiDB 操作所需权限](/privilege-management.md#privileges-required-for-tidb-operations)。

* 安全：
    * `authentication_string` 和 `plugin`：`authentication_string` 存储用户账户的凭据。凭据的解释基于 `plugin` 字段中指定的认证插件。
    * `Account_locked`：表示用户账户是否被锁定。
    * `Password_reuse_history` 和 `Password_reuse_time`：用于[密码重用策略](/password-management.md#password-reuse-policy)。
    * `User_attributes`：提供用户注释和用户属性信息。
    * `Token_issuer`：用于 [`tidb_auth_token`](/security-compatibility-with-mysql.md#tidb_auth_token) 认证插件。
    * `Password_expired`、`Password_last_changed` 和 `Password_lifetime`：用于[密码过期策略](/password-management.md#password-expiration-policy)。

</CustomContent>

<CustomContent platform="tidb-cloud">

* 作用域：
    * `Host`：指定 TiDB 账户的主机名。
    * `User`：指定 TiDB 账户的用户名。
* 权限：

    以 `_priv` 或 `_Priv` 结尾的字段定义了授予用户账户的权限。例如，`Select_priv` 表示用户具有全局 `Select` 权限。更多信息，请参见[TiDB 操作所需权限](https://docs.pingcap.com/tidb/stable/privilege-management#privileges-required-for-tidb-operations)。

* 安全：
    * `authentication_string` 和 `plugin`：`authentication_string` 存储用户账户的凭据。凭据的解释基于 `plugin` 字段中指定的认证插件。
    * `Account_locked`：表示用户账户是否被锁定。
    * `Password_reuse_history` 和 `Password_reuse_time`：用于[密码重用策略](https://docs.pingcap.com/tidb/stable/password-management#password-reuse-policy)。
    * `User_attributes`：提供用户注释和用户属性信息。
    * `Token_issuer`：用于 [`tidb_auth_token`](https://docs.pingcap.com/tidb/stable/security-compatibility-with-mysql#tidb_auth_token) 认证插件。
    * `Password_expired`、`Password_last_changed` 和 `Password_lifetime`：用于[密码过期策略](https://docs.pingcap.com/tidb/stable/password-management#password-expiration-policy)。

</CustomContent>

虽然 TiDB `mysql.user` 表中的大多数字段也存在于 MySQL `mysql.user` 表中，但 `Token_issuer` 字段是 TiDB 特有的。
