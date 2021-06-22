---
title: 约束
---

# 约束

TiDB 支持的约束与 MySQL 的基本相同。

## 非空约束

TiDB 支持的非空约束规则与 MySQL 支持的一致。例如：

{{< copyable "sql" >}}

```sql
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 age INT NOT NULL,
 last_login TIMESTAMP
);
```

{{< copyable "sql" >}}

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,123,NOW());
```

```
Query OK, 1 row affected (0.02 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,NULL,NOW());
```

```
ERROR 1048 (23000): Column 'age' cannot be null
```

{{< copyable "sql" >}}

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,123,NULL);
```

```
Query OK, 1 row affected (0.03 sec)
```

* 第一条 `INSERT` 语句成功，因为对于定义为 `AUTO_INCREMENT` 的列，允许 `NULL` 作为其特殊值。TiDB 将为其分配下一个自动值。

* 第二条 `INSERT` 语句失败，因为 `age` 列被定义为 `NOT NULL`。

* 第三条 `INSERT` 语句成功，因为 `last_login` 列没有被明确地指定为 `NOT NULL`。默认允许 `NULL` 值。

## `CHECK` 约束

TiDB 会解析并忽略 `CHECK` 约束。该行为与 MySQL 5.7 的相兼容。

示例如下：

{{< copyable "sql" >}}

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username),
 CONSTRAINT min_username_length CHECK (CHARACTER_LENGTH(username) >=4)
);
INSERT INTO users (username) VALUES ('a');
SELECT * FROM users;
```

## 唯一约束

在 TiDB 的乐观事务中，默认会对唯一约束进行[惰性检查](/transaction-overview.md#惰性检查)。通过在事务提交时再进行批量检查，TiDB 能够减少网络开销、提升性能。例如：

{{< copyable "sql" >}}

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');
```

默认的悲观事务模式下：

{{< copyable "sql" >}}

```sql
BEGIN;
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

```
ERROR 1062 (23000): Duplicate entry 'bill' for key 'username'
```

乐观事务模式下且 `tidb_constraint_check_in_place=0`：

{{< copyable "sql" >}}

```sql
BEGIN OPTIMISTIC;
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

```
Query OK, 0 rows affected (0.00 sec)
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
INSERT INTO users (username) VALUES ('steve'),('elizabeth');
```

```
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
COMMIT;
```

```
ERROR 1062 (23000): Duplicate entry 'bill' for key 'username'
```

在乐观事务的示例中，唯一约束的检查推迟到事务提交时才进行。由于 `bill` 值已经存在，这一行为导致了重复键错误。

你可通过设置 `tidb_constraint_check_in_place` 为 `1` 停用此行为（该变量设置对悲观事务无效，悲观事务始终在语句执行时检查约束）。当 `tidb_constraint_check_in_place` 设置为 `1` 时，则会在执行语句时就对唯一约束进行检查。例如：

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');
```

{{< copyable "sql" >}}

```sql
SET tidb_constraint_check_in_place = 1;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
BEGIN OPTIMISTIC;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

```
ERROR 1062 (23000): Duplicate entry 'bill' for key 'username'
..
```

第一条 `INSERT` 语句导致了重复键错误。这会造成额外的网络通信开销，并可能降低插入操作的吞吐量。

## 主键约束

与 MySQL 行为一样，主键约束包含了唯一约束，即创建了主键约束相当于拥有了唯一约束。此外，TiDB 其他的主键约束规则也与 MySQL 相似。例如：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

```
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```sql
CREATE TABLE t2 (a INT NULL PRIMARY KEY);
```

```
ERROR 1171 (42000): All parts of a PRIMARY KEY must be NOT NULL; if you need NULL in a key, use UNIQUE instead
```

{{< copyable "sql" >}}

```sql
CREATE TABLE t3 (a INT NOT NULL PRIMARY KEY, b INT NOT NULL PRIMARY KEY);
```

```
ERROR 1068 (42000): Multiple primary key defined
```

{{< copyable "sql" >}}

```sql
CREATE TABLE t4 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b));
```

```
Query OK, 0 rows affected (0.10 sec)
```

分析：

* 表 `t2` 创建失败，因为定义为主键的列 `a` 不能允许 `NULL` 值。
* 表 `t3` 创建失败，因为一张表只能有一个主键。
* 表 `t4` 创建成功，因为虽然只能有一个主键，但 TiDB 支持定义一个多列组合作为复合主键。

除上述规则外，TiDB 目前仅支持对 `NONCLUSTERED` 的主键进行添加和删除操作。例如：

{{< copyable "sql" >}}

```sql
CREATE TABLE t5 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b) CLUSTERED);
ALTER TABLE t5 DROP PRIMARY KEY;
```

```
ERROR 8200 (HY000): Unsupported drop primary key when the table is using clustered index
```

{{< copyable "sql" >}}

```sql
CREATE TABLE t5 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b) NONCLUSTERED);
ALTER TABLE t5 DROP PRIMARY KEY;
```

```
Query OK, 0 rows affected (0.10 sec)
```

要了解关于 `CLUSTERED` 主键的详细信息，请参考[聚簇索引](/clustered-indexes.md)。

## 外键约束

> **注意：**
>
> TiDB 仅部分支持外键约束功能。

TiDB 支持创建外键约束。例如：

```sql
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 doc JSON
);
CREATE TABLE orders (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 user_id INT NOT NULL,
 doc JSON,
 FOREIGN KEY fk_user_id (user_id) REFERENCES users(id)
);
```

{{< copyable "sql" >}}

```sql
SELECT table_name, column_name, constraint_name, referenced_table_name, referenced_column_name
FROM information_schema.key_column_usage WHERE table_name IN ('users', 'orders');
```

```
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

{{< copyable "sql" >}}

```sql
ALTER TABLE orders DROP FOREIGN KEY fk_user_id;
ALTER TABLE orders ADD FOREIGN KEY fk_user_id (user_id) REFERENCES users(id);
```

### 注意

* TiDB 支持外键是为了在将其他数据库迁移到 TiDB 时，不会因为此语法报错。但是，TiDB 不会在 DML 语句中对外键进行约束检查。例如，即使 `users` 表中不存在 `id=123` 的记录，下列事务也能提交成功：

    ```
    START TRANSACTION;
    INSERT INTO orders (user_id, doc) VALUES (123, NULL);
    COMMIT;
    ```
