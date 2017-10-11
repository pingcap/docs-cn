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

## `SHOW` 语句

TiDB 支持部分 `SHOW` 语句，用于查看 Database/Table/Column 信息，或者是数据库内部的状态。已经支持的语句：

```sql
# 已支持，且和 MySQL 行为一致
SHOW CHARACTER SET [like_or_where]
SHOW COLLATION [like_or_where]
SHOW [FULL] COLUMNS FROM tbl_name [FROM db_name] [like_or_where]
SHOW CREATE DATABASE db_name
SHOW CREATE TABLE tbl_name
SHOW DATABASES [like_or_where]
SHOW GRANTS FOR user
SHOW INDEX FROM tbl_name [FROM db_name]
SHOW PRIVILEGES
SHOW [FULL] PROCESSLIST
SHOW [GLOBAL | SESSION] STATUS [like_or_where]
SHOW TABLE STATUS [FROM db_name] [like_or_where]
SHOW [FULL] TABLES [FROM db_name] [like_or_where]
SHOW [GLOBAL | SESSION] VARIABLES [like_or_where]
SHOW WARNINGS

# 已支持，但是返回空结果，目的是提升兼容性
SHOW ENGINE engine_name {STATUS | MUTEX}
SHOW [STORAGE] ENGINES
SHOW PLUGINS
SHOW PROCEDURE STATUS [like_or_where]
SHOW TRIGGERS [FROM db_name] [like_or_where]
SHOW EVENTS
SHOW FUNCTION STATUS [like_or_where]

# TiDB 特有语句，用于查看统计信息，具体信息请参考[统计信息](https://github.com/pingcap/docs-cn/blob/master/sql/statistics.md#统计信息的查看)
SHOW STATS_META [like_or_where]
SHOW STATS_HISTOGRAMS [like_or_where]
SHOW STATS_BUCKETS [like_or_where]


like_or_where:
    LIKE 'pattern'
  | WHERE expr
```

## `ADMIN` 语句

该语句是 TiDB 扩展语法，用于查看 TiDB 自身的状态。

```sql
ADMIN SHOW DDL
ADMIN SHOW DDL JOBS
```

* `ADMIN SHOW DDL`

用于查看当前正在执行的 DDL 作业。

* `ADMIN SHOW DDL JOBS`

用于查看当前 DDL 作业队列中的前十条结果以及已执行完成的 DDL 作业队列中的最近十条结果。