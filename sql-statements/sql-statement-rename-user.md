---
title: RENAME USER
summary: TiDB 数据库中 RENAME USER 的使用概况。
---

# RENAME USER

`RENAME USER` 语句用于对已有用户进行重命名。

## 语法图

```ebnf+diagram
RenameUserStmt ::=
    'RENAME' 'USER' UserToUser ( ',' UserToUser )*

UserToUser ::=
    Username 'TO' Username

Username ::=
    StringName ('@' StringName | singleAtIdentifier)? | 'CURRENT_USER' OptionalBraces
```

## 示例

```sql
CREATE USER 'newuser' IDENTIFIED BY 'mypassword';
```

```
Query OK, 1 row affected (0.02 sec)
```

```sql
SHOW GRANTS FOR 'newuser';
```

```
+-------------------------------------+
| Grants for newuser@%                |
+-------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%' |
+-------------------------------------+
1 row in set (0.00 sec)
```

```sql
RENAME USER 'newuser' TO 'testuser';
```

```
Query OK, 0 rows affected (0.08 sec)
```

```sql
SHOW GRANTS FOR 'testuser';
```

```
+--------------------------------------+
| Grants for testuser@%                |
+--------------------------------------+
| GRANT USAGE ON *.* TO 'testuser'@'%' |
+--------------------------------------+
1 row in set (0.00 sec)
```

```sql
SHOW GRANTS FOR 'newuser';
```

```
ERROR 1141 (42000): There is no such grant defined for user 'newuser' on host '%'
```

## MySQL 兼容性

`RENAME USER` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [CREATE USER](/sql-statements/sql-statement-create-user.md)
* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)
* [DROP USER](/sql-statements/sql-statement-drop-user.md)
