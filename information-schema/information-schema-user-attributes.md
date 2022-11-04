---
title: USER_ATTRIBUTES
summary: 了解 INFORMATION_SCHEMA 表 `USER_ATTRIBUTES`。
---

# USER_ATTRIBUTES

`USER_ATTRIBUTES` 表提供了用户的注释和属性。该表的数据根据 `mysql.user` 系统表生成。

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

`USER_ATTRIBUTES` 表中列的含义如下：

* `USER`：用户名。
* `HOST`：用户可用于连接的主机。百分号（`％`）表示主机名不受限制。
* `ATTRIBUTE`：通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句设置的用户相关的注释和属性。

示例：

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
