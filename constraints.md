---
title: 约束
summary: 了解 SQL 约束如何应用于 TiDB。
---

# 约束

TiDB 支持几乎与 MySQL 相同的约束。

## NOT NULL

TiDB 支持的 NOT NULL 约束与 MySQL 支持的相同。

例如：

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

* 第一个 `INSERT` 语句成功，因为可以将 `NULL` 分配给 `AUTO_INCREMENT` 列。TiDB 会自动生成序列号。
* 第二个 `INSERT` 语句失败，因为 `age` 列被定义为 `NOT NULL`。
* 第三个 `INSERT` 语句成功，因为 `last_login` 列没有显式定义为 `NOT NULL`。默认允许 NULL 值。

## CHECK

> **注意：**
>
> `CHECK` 约束功能默认是禁用的。要启用它，你需要将 [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720) 变量设置为 `ON`。

`CHECK` 约束限制表中列的值必须满足你指定的条件。当向表中插入或更新数据时，TiDB 会检查是否满足约束条件。如果不满足约束条件，则会返回错误。

TiDB 中的 `CHECK` 约束语法与 MySQL 相同：

```sql
[CONSTRAINT [symbol]] CHECK (expr) [[NOT] ENFORCED]
```

语法说明：

- `[]`：`[]` 中的内容是可选的。
- `CONSTRAINT [symbol]`：指定 `CHECK` 约束的名称。
- `CHECK (expr)`：指定约束条件，其中 `expr` 需要是一个布尔表达式。对于表中的每一行，该表达式的计算结果必须是 `TRUE`、`FALSE` 或 `UNKNOWN`（对于 `NULL` 值）中的一个。如果某一行的计算结果为 `FALSE`，表示违反了约束。
- `[NOT] ENFORCED`：指定是否执行约束检查。你可以用它来启用或禁用 `CHECK` 约束。

### 添加 `CHECK` 约束

在 TiDB 中，你可以使用 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 或 [`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md) 语句向表添加 `CHECK` 约束。

- 使用 `CREATE TABLE` 语句添加 `CHECK` 约束的示例：

    ```sql
    CREATE TABLE t(a INT CHECK(a > 10) NOT ENFORCED, b INT, c INT, CONSTRAINT c1 CHECK (b > c));
    ```

- 使用 `ALTER TABLE` 语句添加 `CHECK` 约束的示例：

    ```sql
    ALTER TABLE t ADD CONSTRAINT CHECK (1 < c);
    ```

添加或启用 `CHECK` 约束时，TiDB 会检查表中现有的数据。如果有任何数据违反约束，添加 `CHECK` 约束的操作将失败并返回错误。

添加 `CHECK` 约束时，你可以指定约束名称，也可以不指定。如果不指定约束名称，TiDB 会自动生成一个格式为 `<表名>_chk_<1, 2, 3...>` 的约束名称。

### 查看 `CHECK` 约束

你可以使用 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 语句查看表中的约束信息。例如：

```sql
SHOW CREATE TABLE t;
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                                                                                                     |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
CONSTRAINT `c1` CHECK ((`b` > `c`)),
CONSTRAINT `t_chk_1` CHECK ((`a` > 10)) /*!80016 NOT ENFORCED */,
CONSTRAINT `t_chk_2` CHECK ((1 < `c`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### 删除 `CHECK` 约束

删除 `CHECK` 约束时，需要指定要删除的约束名称。例如：

```sql
ALTER TABLE t DROP CONSTRAINT t_chk_1;
```

### 启用或禁用 `CHECK` 约束

在[添加 `CHECK` 约束](#添加-check-约束)到表时，你可以指定 TiDB 在插入或更新数据时是否需要执行约束检查。

- 如果指定了 `NOT ENFORCED`，TiDB 在插入或更新数据时不会检查约束条件。
- 如果未指定 `NOT ENFORCED` 或指定了 `ENFORCED`，TiDB 在插入或更新数据时会检查约束条件。

除了在添加约束时指定 `[NOT] ENFORCED`，你还可以使用 `ALTER TABLE` 语句启用或禁用 `CHECK` 约束。例如：

```sql
ALTER TABLE t ALTER CONSTRAINT c1 NOT ENFORCED;
```

### MySQL 兼容性

- 不支持在添加列时添加 `CHECK` 约束（例如，`ALTER TABLE t ADD COLUMN a CHECK(a > 0)`）。在这种情况下，只有列添加成功，TiDB 会忽略 `CHECK` 约束而不报错。
- 不支持使用 `ALTER TABLE t CHANGE a b int CHECK(b > 0)` 添加 `CHECK` 约束。执行此语句时，TiDB 会报错。

## UNIQUE KEY

唯一约束意味着唯一索引和主键列中的所有非空值都是唯一的。

### 乐观事务

默认情况下，对于乐观事务，TiDB 在执行阶段[延迟检查](/transaction-overview.md#延迟检查约束)唯一约束，在提交阶段严格检查，这有助于减少网络开销并提高性能。

例如：

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');
```

使用乐观锁并且 `tidb_constraint_check_in_place=OFF`：

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

在上述乐观示例中，唯一性检查被推迟到事务提交时。这导致了重复键错误，因为值 `bill` 已经存在。

你可以通过将 [`tidb_constraint_check_in_place`](/system-variables.md#tidb_constraint_check_in_place) 设置为 `ON` 来禁用此行为。当 `tidb_constraint_check_in_place=ON` 时，唯一约束在语句执行时检查。请注意，此变量仅适用于乐观事务。对于悲观事务，你可以使用 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) 变量来控制此行为。

例如：

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

第一个 `INSERT` 语句导致重复键错误。这会导致额外的网络通信开销，可能会降低插入操作的吞吐量。

### 悲观事务

在悲观事务中，默认情况下，TiDB 在执行需要插入或更新唯一索引的 SQL 语句时检查 `UNIQUE` 约束。

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

为了获得更好的悲观事务性能，你可以将 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) 变量设置为 `OFF`，这允许 TiDB 延迟唯一索引的唯一约束检查（到下次需要锁定该索引时或事务提交时）并跳过相应的悲观锁。使用此变量时，请注意以下几点：

- 由于延迟的唯一约束检查，TiDB 可能会读取到不满足唯一约束的结果，并在提交悲观事务时返回 `Duplicate entry` 错误。当出现此错误时，TiDB 会回滚当前事务。

    以下示例跳过对 `bill` 的锁定，因此 TiDB 可能会获取不满足唯一性约束的结果。

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    SELECT * FROM users FOR UPDATE;
    ```

    如下例所示，TiDB 的查询结果包含两个 `bill`，这不满足唯一性约束。

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

    此时，如果提交事务，TiDB 将执行唯一约束检查，报告 `Duplicate entry` 错误，并回滚事务。

    ```sql
    COMMIT;
    ```

    ```
    ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'
    ```

- 当此变量被禁用时，提交需要写入数据的悲观事务可能会返回 `Write conflict` 错误。当出现此错误时，TiDB 会回滚当前事务。

    如下例所示，如果两个并发事务需要向同一个表插入数据，跳过悲观锁会导致 TiDB 在提交事务时返回 `Write conflict` 错误。事务将被回滚。

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

    同时，另一个会话向同一个表插入 `bill`。

    ```sql
    INSERT INTO users (username) VALUES ('bill'); -- Query OK, 1 row affected
    ```

    然后，当你在第一个会话中提交事务时，TiDB 会报告 `Write conflict` 错误。

    ```sql
    COMMIT;
    ```

    ```
    ERROR 9007 (HY000): Write conflict, txnStartTS=435688780611190794, conflictStartTS=435688783311536129, conflictCommitTS=435688783311536130, key={tableID=74, indexID=1, indexValues={bill, }} primary={tableID=74, indexID=1, indexValues={bill, }}, reason=LazyUniquenessCheck [try again later]
    ```

- 当此变量被禁用时，如果多个悲观事务之间存在写冲突，当其他悲观事务提交时，悲观锁可能会被强制回滚，从而导致 `Pessimistic lock not found` 错误。当出现此错误时，这意味着延迟悲观事务的唯一约束检查不适合你的应用场景。在这种情况下，考虑调整应用逻辑以避免冲突，或在发生错误后重试事务。

- 当此变量被禁用时，在悲观事务中执行 DML 语句可能会返回错误 `8147: LazyUniquenessCheckFailure`。

    > **注意：**
    >
    > 当出现 `8147` 错误时，TiDB 会回滚当前事务。

    如下例所示，在执行 `INSERT` 语句时，TiDB 跳过了锁定。然后，在执行 `DELETE` 语句时，TiDB 锁定唯一索引并检查唯一约束，因此你会看到在 `DELETE` 语句处报告了一个错误。

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    DELETE FROM users where username = 'bill';
    ```

    ```
    ERROR 8147 (23000): transaction aborted because lazy uniqueness check is enabled and an error occurred: [kv:1062]Duplicate entry 'bill' for key 'users.username'
    ```

- 当此变量被禁用时，`1062 Duplicate entry` 错误可能不是来自当前 SQL 语句。因此，当事务操作多个具有相同名称索引的表时，你需要检查 `1062` 错误消息以找出错误实际来自哪个索引。

## PRIMARY KEY

与 MySQL 一样，主键约束包含唯一约束，即创建主键约束相当于具有唯一约束。此外，TiDB 的其他主键约束也与 MySQL 类似。

例如：

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

* 表 `t2` 创建失败，因为列 `a` 被定义为主键且不允许 NULL 值。
* 表 `t3` 创建失败，因为一个表只能有一个主键。
* 表 `t4` 创建成功，因为虽然只能有一个主键，但 TiDB 支持将多个列定义为复合主键。

除了上述规则外，TiDB 目前只支持添加和删除 `NONCLUSTERED` 类型的主键。例如：

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

有关 `CLUSTERED` 类型的主键的更多详细信息，请参考[聚簇索引](/clustered-indexes.md)。

## FOREIGN KEY

> **注意：**
>
> 从 v6.6.0 开始，TiDB 支持[外键约束](/foreign-key.md)作为实验性功能。在 v6.6.0 之前，TiDB 支持创建和删除外键约束，但约束实际上并不生效。将 TiDB 升级到 v6.6.0 后，你可以删除无效的外键并创建新的外键，以使外键约束生效。

TiDB 支持在 DDL 命令中创建 `FOREIGN KEY` 约束。

例如：

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

TiDB 还支持通过 `ALTER TABLE` 命令使用 `DROP FOREIGN KEY` 和 `ADD FOREIGN KEY` 语法。

```sql
ALTER TABLE orders DROP FOREIGN KEY fk_user_id;
ALTER TABLE orders ADD FOREIGN KEY fk_user_id (user_id) REFERENCES users(id);
```
