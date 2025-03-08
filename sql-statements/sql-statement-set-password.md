---
title: SET PASSWORD
summary: TiDB 数据库中 SET PASSWORD 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-set-password/','/docs-cn/dev/reference/sql/statements/set-password/']
---

# SET PASSWORD

`SET PASSWORD` 语句用于更改 TiDB 系统数据库中的用户密码。

> **注意：**
>
> 建议使用 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句更改密码，如下所示：
>
> ```sql
> ALTER USER myuser IDENTIFIED BY 'mypassword';
> ```

## 语法图

```ebnf+diagram
SetPasswordStmt ::=
    "SET" "PASSWORD" ( "FOR" Username )? "=" stringLit
```

## 示例

```sql
SET PASSWORD='test';
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
CREATE USER 'newuser' IDENTIFIED BY 'test';
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
SHOW CREATE USER 'newuser';
```

```
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SET PASSWORD FOR 'newuser' = 'test';
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
SHOW CREATE USER 'newuser';
```

```
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SET PASSWORD` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [CREATE USER](/sql-statements/sql-statement-create-user.md)
* [Privilege Management](/privilege-management.md)
