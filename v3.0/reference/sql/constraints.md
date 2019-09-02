---
title: 约束
category: reference
aliases: ['/docs-cn/sql/constraints/']
---

# 约束

TiDB 支持的基本约束与 MySQL 的基本相同，但有以下区别：

- 默认对唯一约束进行[惰性检查](v3.0/reference/transactions/overview.md#事务的惰性检查)。通过在事务提交时再进行批量检查，TiDB 能够减少网络开销、提升性能。您可通过设置 `tidb_constraint_check_in_place` 为 `TRUE` 改变此行为。

- TiDB 支持创建外键约束，但不会在 DML 语句中对外键进行约束（即外键约束不生效）。

## 外键约束

目前，TiDB 支持创建外键。例如：

```
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

TiDB 也支持使用 `ALTER TABLE` 命令来删除外键（`DROP FOREIGN KEY`）和添加外键（`ADD FOREIGN KEY`）：

```
ALTER TABLE orders DROP FOREIGN KEY fk_user_id;
ALTER TABLE orders ADD FOREIGN KEY fk_user_id (user_id) REFERENCES users(id);
```

然而，TiDB 不会在 DML 语句中对外键进行约束。例如，即使 `users` 表中不存在 `id=123` 的记录，下列事务也能提交成功：

```
START TRANSACTION;
INSERT INTO orders (user_id, doc) VALUES (123, NULL);
COMMIT;
```

## 非空约束

TiDB 支持的非空约束规则与 MySQL 支持的一致。例如：

```
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

* 第一条 `INSERT` 语句成功，因为对于定义为 `auto_increment` 的列，允许 `NULL` 作为其特殊值。TiDB 将为其分配下一个自动值。

* 第二条 `INSERT` 语句失败，因为 `age` 列被定义为 `NOT NULL`。

* 第三条 `INSERT` 语句成功，因为 `last_login` 列没有被明确地指定为 `NOT NULL`。默认允许 `NULL` 值。

## 主键约束

TiDB 支持的主键约束规则与 MySQL 支持的相似。例如：

```
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)
mysql> CREATE TABLE t2 (a INT NULL PRIMARY KEY);
ERROR 1171 (42000): All parts of a PRIMARY KEY must be NOT NULL; if you need NULL in a key, use UNIQUE instead
mysql> CREATE TABLE t3 (a INT NOT NULL PRIMARY KEY, b INT NOT NULL PRIMARY KEY);
ERROR 1068 (42000): Multiple primary key defined
mysql> CREATE TABLE t4 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b));
Query OK, 0 rows affected (0.10 sec)
```

* 表 `t2` 创建失败，因为定义为主键的列 `a` 不能允许 `NULL` 值。
* 表 `t3` 创建失败，因为一张表只能有一个主键。
* 表 `t4` 创建成功，因为虽然只能有一个主键，但 TiDB 支持定义一个多列组合作为复合主键。

除上述规则外，TiDB 还强加了另一个限制，即一旦一张表创建成功，其主键就不能再改变。

## 唯一约束

在 TiDB 中，默认会对唯一约束进行惰性检查。通过直到事务提交时才进行批量检查，TiDB 能够减少网络通信开销。例如：

```
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

* 第一条 `INSERT` 语句不会导致重复键错误，这同 MySQL 的规则一致。该检查将推迟到事务提交时才会进行。

如果将 `tidb_constraint_check_in_place` 更改为 `TRUE`，则会在执行语句时就对唯一约束进行检查。例如：

```
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

* 第一条 `INSERT` 语句导致了重复键错误。这会造成额外的网络通信开销，并可能降低插入操作的吞吐量。
