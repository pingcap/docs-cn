---
title: USER_ATTRIBUTES
summary: Learn the `USER_ATTRIBUTES` INFORMATION_SCHEMA table.
---

# USER_ATTRIBUTES

The `USER_PRIVILEGES` table provides information about user comments and user attributes. This information comes from the `mysql.user` system table.

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

Fields in the `USER_ATTRIBUTES` table are described as follows:

* `USER`: The user name.
* `HOST`: The host from which the user can connect to TiDB. If the value of this field is `％`, it means that the user can connect to TiDB from any host.
* `ATTRIBUTE`: The comment and attribute of the user, which are set by the [`CREATE USER`](/sql-statements/sql-statement-create-user.md) or [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) statement.

The following is an example:

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