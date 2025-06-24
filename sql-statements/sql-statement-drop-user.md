---
title: DROP USER | TiDB SQL 语句参考
summary: TiDB 数据库中 DROP USER 的使用概览。
---

# DROP USER

该语句从 TiDB 系统数据库中删除用户。可以使用可选关键字 `IF EXISTS` 来在用户不存在时静默错误。该语句需要 `CREATE USER` 权限。

## 语法图

```ebnf+diagram
DropUserStmt ::=
    'DROP' 'USER' ( 'IF' 'EXISTS' )? UsernameList

Username ::=
    StringName ('@' StringName | singleAtIdentifier)? | 'CURRENT_USER' OptionalBraces
```

## 示例

```sql
mysql> DROP USER idontexist;
ERROR 1396 (HY000): Operation DROP USER failed for idontexist@%

mysql> DROP USER IF EXISTS 'idontexist';
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE USER 'newuser' IDENTIFIED BY 'mypassword';
Query OK, 1 row affected (0.02 sec)

mysql> GRANT ALL ON test.* TO 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------------------+
| Grants for newuser@%                            |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'             |
| GRANT ALL PRIVILEGES ON test.* TO 'newuser'@'%' |
+-------------------------------------------------+
2 rows in set (0.00 sec)

mysql> REVOKE ALL ON test.* FROM 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------+
| Grants for newuser@%                |
+-------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%' |
+-------------------------------------+
1 row in set (0.00 sec)

mysql> DROP USER 'newuser';
Query OK, 0 rows affected (0.14 sec)

mysql> SHOW GRANTS FOR 'newuser';
ERROR 1141 (42000): There is no such grant defined for user 'newuser' on host '%'
```

## MySQL 兼容性

* 在 TiDB 中，使用 `IF EXISTS` 删除不存在的用户不会产生警告。[问题 #10196](https://github.com/pingcap/tidb/issues/10196)。

## 另请参阅

* [CREATE USER](/sql-statements/sql-statement-create-user.md)
* [ALTER USER](/sql-statements/sql-statement-alter-user.md)
* [SHOW CREATE USER](/sql-statements/sql-statement-show-create-user.md)

<CustomContent platform="tidb">

* [权限管理](/privilege-management.md)

</CustomContent>
