---
title: USER_PRIVILEGES
summary: 了解 `USER_PRIVILEGES` information_schema 表。
---

# USER_PRIVILEGES

`USER_PRIVILEGES` 表提供全局权限的信息。这些信息来自 `mysql.user` 系统表：

```sql
USE INFORMATION_SCHEMA;
DESC USER_PRIVILEGES;
```

输出结果如下：

```sql
+----------------+--------------+------+------+---------+-------+
| Field          | Type         | Null | Key  | Default | Extra |
+----------------+--------------+------+------+---------+-------+
| GRANTEE        | varchar(81)  | YES  |      | NULL    |       |
| TABLE_CATALOG  | varchar(512) | YES  |      | NULL    |       |
| PRIVILEGE_TYPE | varchar(64)  | YES  |      | NULL    |       |
| IS_GRANTABLE   | varchar(3)   | YES  |      | NULL    |       |
+----------------+--------------+------+------+---------+-------+
4 rows in set (0.00 sec)
```

查看 `USER_PRIVILEGES` 表中的信息：

```sql
SELECT * FROM USER_PRIVILEGES;
```

输出结果如下：

<CustomContent platform="tidb">

```sql
+------------+---------------+-------------------------+--------------+
| GRANTEE    | TABLE_CATALOG | PRIVILEGE_TYPE          | IS_GRANTABLE |
+------------+---------------+-------------------------+--------------+
| 'root'@'%' | def           | SELECT                  | YES          |
| 'root'@'%' | def           | INSERT                  | YES          |
| 'root'@'%' | def           | UPDATE                  | YES          |
| 'root'@'%' | def           | DELETE                  | YES          |
| 'root'@'%' | def           | CREATE                  | YES          |
| 'root'@'%' | def           | DROP                    | YES          |
| 'root'@'%' | def           | PROCESS                 | YES          |
| 'root'@'%' | def           | REFERENCES              | YES          |
| 'root'@'%' | def           | ALTER                   | YES          |
| 'root'@'%' | def           | SHOW DATABASES          | YES          |
| 'root'@'%' | def           | SUPER                   | YES          |
| 'root'@'%' | def           | EXECUTE                 | YES          |
| 'root'@'%' | def           | INDEX                   | YES          |
| 'root'@'%' | def           | CREATE USER             | YES          |
| 'root'@'%' | def           | CREATE TABLESPACE       | YES          |
| 'root'@'%' | def           | TRIGGER                 | YES          |
| 'root'@'%' | def           | CREATE VIEW             | YES          |
| 'root'@'%' | def           | SHOW VIEW               | YES          |
| 'root'@'%' | def           | CREATE ROLE             | YES          |
| 'root'@'%' | def           | DROP ROLE               | YES          |
| 'root'@'%' | def           | CREATE TEMPORARY TABLES | YES          |
| 'root'@'%' | def           | LOCK TABLES             | YES          |
| 'root'@'%' | def           | CREATE ROUTINE          | YES          |
| 'root'@'%' | def           | ALTER ROUTINE           | YES          |
| 'root'@'%' | def           | EVENT                   | YES          |
| 'root'@'%' | def           | SHUTDOWN                | YES          |
| 'root'@'%' | def           | RELOAD                  | YES          |
| 'root'@'%' | def           | FILE                    | YES          |
| 'root'@'%' | def           | CONFIG                  | YES          |
| 'root'@'%' | def           | REPLICATION CLIENT      | YES          |
| 'root'@'%' | def           | REPLICATION SLAVE       | YES          |
+------------+---------------+-------------------------+--------------+
31 rows in set (0.00 sec)
```

</CustomContent>

<CustomContent platform="tidb-cloud">

<!--与 TiDB 自托管版本相比，TiDB Cloud 中的 root 用户没有 SHUTDOWN 和 CONFIG 权限。-->

```sql
+------------+---------------+-------------------------+--------------+
| GRANTEE    | TABLE_CATALOG | PRIVILEGE_TYPE          | IS_GRANTABLE |
+------------+---------------+-------------------------+--------------+
| 'root'@'%' | def           | SELECT                  | YES          |
| 'root'@'%' | def           | INSERT                  | YES          |
| 'root'@'%' | def           | UPDATE                  | YES          |
| 'root'@'%' | def           | DELETE                  | YES          |
| 'root'@'%' | def           | CREATE                  | YES          |
| 'root'@'%' | def           | DROP                    | YES          |
| 'root'@'%' | def           | PROCESS                 | YES          |
| 'root'@'%' | def           | REFERENCES              | YES          |
| 'root'@'%' | def           | ALTER                   | YES          |
| 'root'@'%' | def           | SHOW DATABASES          | YES          |
| 'root'@'%' | def           | SUPER                   | YES          |
| 'root'@'%' | def           | EXECUTE                 | YES          |
| 'root'@'%' | def           | INDEX                   | YES          |
| 'root'@'%' | def           | CREATE USER             | YES          |
| 'root'@'%' | def           | CREATE TABLESPACE       | YES          |
| 'root'@'%' | def           | TRIGGER                 | YES          |
| 'root'@'%' | def           | CREATE VIEW             | YES          |
| 'root'@'%' | def           | SHOW VIEW               | YES          |
| 'root'@'%' | def           | CREATE ROLE             | YES          |
| 'root'@'%' | def           | DROP ROLE               | YES          |
| 'root'@'%' | def           | CREATE TEMPORARY TABLES | YES          |
| 'root'@'%' | def           | LOCK TABLES             | YES          |
| 'root'@'%' | def           | CREATE ROUTINE          | YES          |
| 'root'@'%' | def           | ALTER ROUTINE           | YES          |
| 'root'@'%' | def           | EVENT                   | YES          |
| 'root'@'%' | def           | RELOAD                  | YES          |
| 'root'@'%' | def           | FILE                    | YES          |
| 'root'@'%' | def           | REPLICATION CLIENT      | YES          |
| 'root'@'%' | def           | REPLICATION SLAVE       | YES          |
+------------+---------------+-------------------------+--------------+
29 rows in set (0.00 sec)
```

</CustomContent>

`USER_PRIVILEGES` 表中的字段说明如下：

* `GRANTEE`：被授予权限的用户名，格式为 `'user_name'@'host_name'`。
* `TABLE_CATALOG`：表所属的目录名称。此值始终为 `def`。
* `PRIVILEGE_TYPE`：要授予的权限类型。每行仅显示一种权限类型。
* `IS_GRANTABLE`：如果你具有 `GRANT OPTION` 权限，则值为 `YES`；否则，值为 `NO`。

## 另请参阅

- [`SHOW GRANTS`](/sql-statements/sql-statement-show-grants.md)
