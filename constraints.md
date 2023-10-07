---
title: 约束
---

# 约束

TiDB 支持的约束与 MySQL 的基本相同。

## 非空约束

TiDB 支持的非空约束规则与 MySQL 支持的一致。例如：

```sql
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 age INT NOT NULL,
 last_login TIMESTAMP
);
```

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,123,NOW());
```

```
Query OK, 1 row affected (0.02 sec)
```

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,NULL,NOW());
```

```
ERROR 1048 (23000): Column 'age' cannot be null
```

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

TiDB 会解析并忽略 `CHECK` 约束。该行为与 MySQL 5.7 仅为语法兼容，实际上并不支持。 

示例如下：

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

唯一约束是指唯一索引和主键列中所有的非空值都是唯一的。

### 乐观事务

在 TiDB 的乐观事务中，默认会对唯一约束进行[惰性检查](/transaction-overview.md#惰性检查)。通过在事务提交时再进行批量检查，TiDB 能够减少网络开销、提升性能。例如：

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');
```

乐观事务模式下且 `tidb_constraint_check_in_place=OFF`：

```sql
BEGIN OPTIMISTIC;
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

```
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
INSERT INTO users (username) VALUES ('steve'),('elizabeth');
```

```
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

```sql
COMMIT;
```

```
ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'
```

在以上乐观事务的示例中，唯一约束的检查推迟到事务提交时才进行。由于 `bill` 值已经存在，这一行为导致了重复键错误。

你可通过设置 [`tidb_constraint_check_in_place`](/system-variables.md#tidb_constraint_check_in_place) 为 `ON` 停用此行为（该变量仅适用于乐观事务，悲观事务需通过 `tidb_constraint_check_in_place_pessimistic` 设置）。当 `tidb_constraint_check_in_place` 设置为 `ON` 时，TiDB 会在执行语句时就对唯一约束进行检查。例如：

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');
```

```sql
SET tidb_constraint_check_in_place = ON;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
BEGIN OPTIMISTIC;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

```
ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'
```

第一条 `INSERT` 语句导致了重复键错误。这会造成额外的网络通信开销，并可能降低插入操作的吞吐量。

### 悲观事务

在 TiDB 的悲观事务中，默认在执行任何一条需要插入或更新唯一索引的 SQL 语句时都会进行唯一约束检查：

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');

BEGIN PESSIMISTIC;
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

```
ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'
```

对于悲观事务，你可以设置变量 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) 为 `OFF` 来推迟唯一约束检查，到下一次对该唯一索引项加锁时或事务提交时再进行检查，同时也跳过对该悲观锁加锁，以获得更好的性能。此时需要注意：

- 由于推迟了唯一约束检查，TiDB 可能会读取到不满足唯一约束的结果，执行 `COMMIT` 语句时可能返回 `Duplicate entry` 错误。返回该错误时，TiDB 会回滚当前事务。

    下面这个例子跳过了对 `bill` 的加锁，因此 TiDB 可能读到不满足唯一性约束的结果：

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    SELECT * FROM users FOR UPDATE;
    ```

    TiDB 读到了不满足唯一性约束的结果：有两个 `bill`。

    ```sql
    +----+----------+
    | id | username |
    +----+----------+
    | 1  | dave     |
    | 2  | sarah    |
    | 3  | bill     |
    | 7  | jane     |
    | 8  | chris    |
    | 9  | bill     |
    +----+----------+
    ```

    此时，如果提交事务，TiDB 将进行唯一约束检查，报出 `Duplicate entry` 错误并回滚事务。

    ```sql
    COMMIT;
    ```

    ```
    ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'
    ```

- 关闭该变量时，如果在事务中写入数据，执行 `COMMIT` 语句可能会返回 `Write conflict` 错误。返回该错误时，TiDB 会回滚当前事务。

    在下面这个例子中，当有并发事务写入时，跳过悲观锁导致事务提交时报出 `Write conflict` 错误并回滚。

    ```sql
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(60) NOT NULL,
    UNIQUE KEY (username)
    );

    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    ```

    然后另一个会话中写入了 `bill`：

    ```sql
    INSERT INTO users (username) VALUES ('bill'); -- Query OK, 1 row affected
    ```

    在第一个会话中提交时，TiDB 会报出 `Write conflict` 错误。

    ```sql
    COMMIT;
    ```

    ```
    ERROR 9007 (HY000): Write conflict, txnStartTS=435688780611190794, conflictStartTS=435688783311536129, conflictCommitTS=435688783311536130, key={tableID=74, indexID=1, indexValues={bill, }} primary={tableID=74, indexID=1, indexValues={bill, }}, reason=LazyUniquenessCheck [try again later]
    ```

- 关闭该变量时，如果多个悲观事务之间存在写冲突，悲观锁可能会在其它悲观事务提交时被强制回滚，因此产生 `PessimisticLockNotFound` 错误。发生该错误时，说明该业务不适合推迟悲观事务的唯一约束检查，应考虑调整业务避免冲突，或在发生错误后重试事务。

- 关闭该变量会导致悲观事务中可能报出错误 `8147: LazyUniquenessCheckFailure`。

    > **注意：**
    >
    > 返回 8147 错误时当前事务回滚。

    下面的例子在 INSERT 语句执行时跳过了一次加锁后，在 DELETE 语句执行时对该唯一索引加锁并检查，即会在该语句报错：

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    DELETE FROM users where username = 'bill';
    ```

    ```
    ERROR 8147 (23000): transaction aborted because lazy uniqueness check is enabled and an error occurred: [kv:1062]Duplicate entry 'bill' for key 'users.username'
    ```

- 关闭该变量时，`1062 Duplicate entry` 报错不一定是当前执行的 SQL 语句所发生的错误。因此，在一个事务操作多个表，且这些表有同名索引时，请注意 `1062` 报错信息中提示的是哪个表的哪个索引发生了错误。

## 主键约束

与 MySQL 行为一样，主键约束包含了唯一约束，即创建了主键约束相当于拥有了唯一约束。此外，TiDB 其他的主键约束规则也与 MySQL 相似。例如：

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

```
Query OK, 0 rows affected (0.12 sec)
```

```sql
CREATE TABLE t2 (a INT NULL PRIMARY KEY);
```

```
ERROR 1171 (42000): All parts of a PRIMARY KEY must be NOT NULL; if you need NULL in a key, use UNIQUE instead
```

```sql
CREATE TABLE t3 (a INT NOT NULL PRIMARY KEY, b INT NOT NULL PRIMARY KEY);
```

```
ERROR 1068 (42000): Multiple primary key defined
```

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

```sql
CREATE TABLE t5 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b) CLUSTERED);
ALTER TABLE t5 DROP PRIMARY KEY;
```

```
ERROR 8200 (HY000): Unsupported drop primary key when the table is using clustered index
```

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

TiDB 也支持使用 `ALTER TABLE` 命令来删除外键 (`DROP FOREIGN KEY`) 和添加外键 (`ADD FOREIGN KEY`)：

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
