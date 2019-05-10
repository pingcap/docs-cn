---
title: Constraints
summary: Learn how SQL Constraints apply to TiDB.
category: reference
aliases: ['/docs/sql/constraints/'] 
---

# Constraints

## Overview

TiDB supports the same basic constraints supported in MySQL with the follwing exceptions:

- `PRIMARY KEY` and `UNIQUE` constraints are checked lazily by default. By batching checks until when the transaction commits, TiDB is able to reduce network communication. This behavior can be changed by setting `tidb_constraint_check_in_place` to `TRUE`.

- `FOREIGN KEY` constraints are not currently enforced by DML.

## Foreign Key

TiDB currently only supports `FOREIGN KEY` creation in DDL commands. For example:

```sql
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY auto_increment,
 doc JSON
);

CREATE TABLE orders (
 id INT NOT NULL PRIMARY KEY auto_increment,
 user_id INT NOT NULL,
 doc JSON,
 FOREIGN KEY fk_user_id (user_id) REFERENCES users(id)
);

mysql> SELECT table_name, column_name, constraint_name, referenced_table_name, referenced_column_name
FROM information_schema.key_column_usage WHERE table_name IN ('users', 'orders');
+------------+-------------+-----------------+-----------------------+------------------------+
| table_name | column_name | constraint_name | referenced_table_name | referenced_column_name |
+------------+-------------+-----------------+-----------------------+------------------------+
| users      | id          | PRIMARY         | NULL                  | NULL                   |
| orders     | id          | PRIMARY         | NULL                  | NULL                   |
| orders     | user_id     | fk_user_id      | users                 | id                     |
+------------+-------------+-----------------+-----------------------+------------------------+
3 rows in set (0.00 sec)
```

TiDB also supports the syntax to `DROP FOREIGN KEY` and `ADD FOREIGN KEY` via the `ALTER TABLE` command:

```sql
ALTER TABLE orders DROP FOREIGN KEY fk_user_id;
ALTER TABLE orders ADD FOREIGN KEY fk_user_id (user_id) REFERENCES users(id); 
```

Currently foreign keys are not enforced as part of DML operations. For example, in TiDB the following transaction commits successfully even though there is no `user_id` with `id=123`:

```sql
START TRANSACTION;
INSERT INTO orders (user_id, doc) VALUES (123, NULL);
COMMIT;
```

## Not Null

TiDB supports the `NOT NULL` constraint with identical semantics to MySQL. For example:

```sql
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY auto_increment,
 age INT NOT NULL,
 last_login TIMESTAMP
);

mysql> INSERT INTO users (id,age,last_login) VALUES (NULL,123,NOW());
Query OK, 1 row affected (0.02 sec)

mysql> INSERT INTO users (id,age,last_login) VALUES (NULL,NULL,NOW());
ERROR 1048 (23000): Column 'age' cannot be null

mysql> INSERT INTO users (id,age,last_login) VALUES (NULL,123,NULL);
Query OK, 1 row affected (0.03 sec)
```

* The first `INSERT` statement succeeded because `NULL` is permitted as a special value for columns defined as `auto_increment`. This results in the next auto-value being allocated.

* The second `INSERT` statement fails because the `age` column was defined as `NOT NULL`.

* The third `INSERT` statement succeeds because `last_login` did not explicitly specify the column as `NOT NULL`. The default behavior is to permit `NULL` values.

## Primary Key

In TiDB, `PRIMARY KEY` constraints are checked lazily by default. By batching checks until when the transaction commits, TiDB is able to reduce network communication. For example:

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.01 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1); -- does not error
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (2);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT; -- triggers an error
ERROR 1062 (23000): Duplicate entry '1' for key 'PRIMARY'
```

`PRIMARY KEY` constraints otherwise have similar behavior and restrictions to MySQL:

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> CREATE TABLE t2 (a INT NULL PRIMARY KEY);
ERROR 1171 (42000): All parts of a PRIMARY KEY must be NOT NULL; if you need NULL in a key, use UNIQUE instead

mysql> CREATE TABLE t3 (a INT NOT NULL PRIMARY KEY, b INT NOT NULL PRIMARY KEY);
ERROR 1068 (42000): Multiple primary key defined

mysql> CREATE TABLE t4 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b));
Query OK, 0 rows affected (0.10 sec)
```

* Table `t2` failed to be created because the column `a` permitted `NULL` values.
* Table `t3` failed because there can only be one `PRIMARY KEY` on a table.
* Table `t4` was successful, because even though there can only be one primary key, it may be defined as a composite of multiple columns.

In addition to these semantics, TiDB also imposes the restriction that once a table is created, the `PRIMARY KEY` can not be changed.

## Unique

In TiDB, `UNIQUE` constraints are checked lazily by default. By batching checks until when the transaction commits, TiDB is able to reduce network communication. For example:

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY auto_increment,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> INSERT INTO users (username) VALUES ('steve'),('elizabeth');
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0

mysql> COMMIT;
ERROR 1062 (23000): Duplicate entry 'bill' for key 'username'
```

* The first `INSERT` statement does not cause a duplicate key error, as it would in MySQL. This check is deferred until the `COMMIT` statement is executed.

By changing `tidb_constraint_check_in_place` to `TRUE`, `UNIQUE` constraints will be checked as statements are executed. For example:

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY auto_increment,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');

mysql> SET tidb_constraint_check_in_place = TRUE;
Query OK, 0 rows affected (0.00 sec)

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
ERROR 1062 (23000): Duplicate entry 'bill' for key 'username'

..
```

* The first `INSERT` statement causes a duplicate key error. This results in additional network communication, and will likely decrease insert throughput. 
