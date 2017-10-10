---
title: 数据库管理语句
category: user guide
---

TiDB 可以通过一些语句对数据库进行管理，包括设置权限、修改系统变量、查询数据库状态。

## 权限管理

参考[权限管理文档](privilege.md)。

## `SET` 语句

`SET` 语句有多种作用和形式：

### 设置变量值

```sql
SET variable_assignment [, variable_assignment] ...

variable_assignment:
      user_var_name = expr
    | param_name = expr
    | local_var_name = expr
    | [GLOBAL | SESSION]
        system_var_name = expr
    | [@@global. | @@session. | @@]
        system_var_name = expr
```

这种语法可以设置 TiDB 的变量值，包括系统变量以及用户定义变量。对于用户自定义变量，都是会话范围的变量；对于系统变量，通过 `@@global.` 或者是 `GLOBAL` 设置的变量为全局范围变量，否则为会话范围变量。

### `SET CHARACTER` 语句和 `SET NAMES`

```sql
SET {CHARACTER SET | CHARSET}
    {'charset_name' | DEFAULT}

SET NAMES {'charset_name'
    [COLLATE 'collation_name'] | DEFAULT}
```

这个语句设置这三个会话范围的系统变量：`character_set_client`，`character_set_results`，`character_set_connection` 设置为给定的字符集。目前 `character_set_connection` 变量的值和 MySQL 有所区别，MySQL 将其设置为 `character_set_database` 的值。

### 设置密码

```sql
SET PASSWORD [FOR user] = password_option

password_option: {
    'auth_string'
  | PASSWORD('auth_string')
}
```

设置用户密码，具体信息参考[权限管理](privilege.md)。

### 设置隔离级别
```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```
设置事务隔离级别，具体信息参考[事务语句](transaction.md#事务隔离级别)。