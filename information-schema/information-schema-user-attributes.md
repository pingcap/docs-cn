---
title: USER_ATTRIBUTES
summary: 了解 `USER_ATTRIBUTES` INFORMATION_SCHEMA 表。
---

# USER_ATTRIBUTES

`USER_PRIVILEGES` 表提供了用户注释和用户属性的相关信息。这些信息来自 `mysql.user` 系统表。

```sql
USE information_schema;
DESC user_attributes;
```

```sql
+-----------+--------------+------+------+---------+-------+
| Field     | Type         | Null | Key  | Default | Extra |
+-----------+--------------+------+------+---------+-------+
| USER      | varchar(32)  | NO   |      | NULL    |       |
| HOST      | varchar(255) | NO   |      | NULL    |       |
| ATTRIBUTE | longtext     | YES  |      | NULL    |       |
+-----------+--------------+------+------+---------+-------+
3 rows in set (0.00 sec)
```

`USER_ATTRIBUTES` 表中的字段说明如下：

* `USER`：用户名。
* `HOST`：用户可以从哪个主机连接到 TiDB。如果该字段的值为 `％`，表示用户可以从任何主机连接到 TiDB。
* `ATTRIBUTE`：用户的注释和属性，通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句设置。

以下是一个示例：

```sql
CREATE USER testuser1 COMMENT 'This user is created only for test';
CREATE USER testuser2 ATTRIBUTE '{"email": "user@pingcap.com"}';
SELECT * FROM information_schema.user_attributes;
```

```sql
+-----------+------+---------------------------------------------------+
| USER      | HOST | ATTRIBUTE                                         |
+-----------+------+---------------------------------------------------+
| root      | %    | NULL                                              |
| testuser1 | %    | {"comment": "This user is created only for test"} |
| testuser2 | %    | {"email": "user@pingcap.com"}                     |
+-----------+------+---------------------------------------------------+
3 rows in set (0.00 sec)
```
