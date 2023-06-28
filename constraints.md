---
title: Constraints
summary: Learn how SQL Constraints apply to TiDB.
aliases: ['/docs/dev/constraints/','/docs/dev/reference/sql/constraints/']
---

# Constraints

TiDB supports almost the same constraints as MySQL.

## NOT NULL

NOT NULL constraints supported by TiDB are the same as those supported by MySQL.

For example:

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

* The first `INSERT` statement succeeds because it is possible to assign `NULL` to the `AUTO_INCREMENT` column. TiDB generates sequence numbers automatically.
* The second `INSERT` statement fails because the `age` column is defined as `NOT NULL`.
* The third `INSERT` statement succeeds because the `last_login` column is not explicitly defined as `NOT NULL`. NULL values ​​are allowed by default.

## CHECK

> **Note:**
>
> The `CHECK` constraint feature is disabled by default. To enable it, you need to set the [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720) variable to `ON`.

A `CHECK` constraint restricts the values of a column in a table to meet your specified conditions. When the `CHECK` constraint is added to a table, TiDB checks whether the constraint is satisfied during the insertion or updates of data into the table. If the constraint is not met, an error is returned.

The syntax for the `CHECK` constraint in TiDB is the same as that in MySQL:

```sql
[CONSTRAINT [symbol]] CHECK (expr) [[NOT] ENFORCED]
```

Syntax explanation:

- `[]`: the content within `[]` is optional.
- `CONSTRAINT [symbol]`: specifies the name of the `CHECK` constraint.
- `CHECK (expr)`: specifies the constraint condition, where `expr` needs to be a boolean expression. For each row in the table, the calculation result of this expression must be one of `TRUE`, `FALSE`, or `UNKNOWN` (for `NULL` values). If the calculation result is `FALSE` for a row, it indicates that the constraint is violated.
- `[NOT] ENFORCED`: specifies whether to implement the constraint check. You can use it to enable or disable a `CHECK` constraint.

### Add `CHECK` constraints

In TiDB, you can add a `CHECK` constraint to a table using either the [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) or the [`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md) statement.

- Example of adding a `CHECK` constraint using the `CREATE TABLE` statement:

    ```sql
    CREATE TABLE t(a INT CHECK(a > 10) NOT ENFORCED, b INT, c INT, CONSTRAINT c1 CHECK (b > c));
    ```

- Example of adding a `CHECK` constraint using the `ALTER TABLE` statement:

    ```sql
    ALTER TABLE t ADD CONSTRAINT CHECK (1 < c);
    ```

When adding or enabling a `CHECK` constraint, TiDB checks the existing data in the table. If any data violates the constraint, the operation of adding the `CHECK` constraint will fail and return an error.

When adding a `CHECK` constraint, you can either specify a constraint name or leave the name unspecified. If no constraint name is specified, TiDB automatically generates a constraint name in the `<tableName>_chk_<1, 2, 3...>` format.

### View `CHECK` constraints

You can view the constraint information in a table using the [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) statement. For example:

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

### Delete `CHECK` constraints

When deleting a `CHECK` constraint, you need to specify the name of the constraint to be deleted. For example:

```sql
ALTER TABLE t DROP CONSTRAINT t_chk_1;
```

### Enable or disable `CHECK` constraints

When [adding a `CHECK` constraint](#add-check-constraints) to a table, you can specify whether TiDB needs to implement the constraint check during data insertion or updates.

- If `NOT ENFORCED` is specified, TiDB does not check the constraint conditions during data insertion or updates.
- If `NOT ENFORCED` is not specified or `ENFORCED` is specified, TiDB checks the constraint conditions during data insertion or updates.

In addition to specifying `[NOT] ENFORCED` when adding the constraint, you can also enable or disable a `CHECK` constraint using the `ALTER TABLE` statement. For example:

```sql
ALTER TABLE t ALTER CONSTRAINT c1 NOT ENFORCED;
```

### MySQL compatibility

- It is not supported to add a `CHECK` constraint while adding a column (for example, `ALTER TABLE t ADD COLUMN a CHECK(a > 0)`). In this case, only the column is added successfully, and TiDB ignores the `CHECK` constraint without reporting any error.
- It is not supported to use `ALTER TABLE t CHANGE a b int CHECK(b > 0)` to add a `CHECK` constraint. When this statement is executed, TiDB reports an error.

## UNIQUE KEY

Unique constraints mean that all non-null values in a unique index and a primary key column are unique.

### Optimistic transactions

By default, for optimistic transactions, TiDB checks unique constraints [lazily](/transaction-overview.md#lazy-check-of-constraints) in the execution phase and strictly in the commit phase, which helps reduce network overhead and improve performance.

For example:

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');
```

With optimistic locking and `tidb_constraint_check_in_place=OFF`:

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

In the preceding optimistic example, the unique check was deferred until the transaction is committed. This resulted in a duplicate key error, because the value `bill` was already present.

You can disable this behavior by setting [`tidb_constraint_check_in_place`](/system-variables.md#tidb_constraint_check_in_place) to `ON`. When `tidb_constraint_check_in_place=ON`, the unique constraint is checked when a statement is executed. Note that this variable is only applicable to optimistic transactions. For pessimistic transactions, you can control this behavior using the [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) variable.

For example:

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

The first `INSERT` statement caused a duplicate key error. This causes additional network communication overhead and may reduce the throughput of insert operations.

### Pessimistic transactions

In pessimistic transactions, by default, TiDB checks `UNIQUE` constraints when a SQL statement that requires inserting or updating unique indexes is executed.

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

To achieve better performance of pessimistic transactions, you can set the [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) variable to `OFF`, which allows TiDB to defer the unique constraint check of a unique index (to the next time when this index requires a lock or to the time when the transaction is committed) and skip the corresponding pessimistic lock. When using this variable, pay attention to the following:

- Due to the deferred unique constraint check, TiDB might read results that do not meet the unique constraints and return a `Duplicate entry` error when you commit a pessimistic transaction. When this error occurs, TiDB rolls back the current transaction.

    The following example skips the lock to `bill`, so TiDB might get results that do not satisfy the uniqueness constraints.

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    SELECT * FROM users FOR UPDATE;
    ```

   As in the following example output, the query results of TiDB contain two `bills`, which does not satisfy the uniqueness constraints.

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

    At this time, if the transaction is committed, TiDB will perform a unique constraint check, report a `Duplicate entry` error, and roll back the transaction.

    ```sql
    COMMIT;
    ```

    ```
    ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'
    ```

- When this variable is disabled, committing a pessimistic transaction that needs to write data might return a `Write conflict` error. When this error occurs, TiDB rolls back the current transaction.

    As in the following example, if two concurrent transactions need to insert data to the same table, skipping the pessimistic lock causes TiDB to return a `Write conflict` error when you commit a transaction. And the transaction will be rolled back.

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

    At the same time, another session inserts `bill` to the same table.

    ```sql
    INSERT INTO users (username) VALUES ('bill'); -- Query OK, 1 row affected
    ```

    Then, when you commit the transaction in the first session, TiDB reports a `Write conflict` error.

    ```sql
    COMMIT;
    ```

    ```
    ERROR 9007 (HY000): Write conflict, txnStartTS=435688780611190794, conflictStartTS=435688783311536129, conflictCommitTS=435688783311536130, key={tableID=74, indexID=1, indexValues={bill, }} primary={tableID=74, indexID=1, indexValues={bill, }}, reason=LazyUniquenessCheck [try again later]
    ```

- When this variable is disabled, if there is a write conflict among multiple pessimistic transactions, the pessimistic lock might be forced to roll back when other pessimistic transactions are committed, thus resulting in a `Pessimistic lock not found` error. When this error occurs, it means that deferring the unique constraint check of the pessimistic transaction is not suitable for your application scenario. In this case, consider adjusting the application logic to avoid the conflict or retrying the transaction after an error occurs.

- When this variable is disabled, executing a DML statement in a pessimistic transaction might return an error `8147: LazyUniquenessCheckFailure`.

    > **Note:**
    >
    > When the `8147` error occurs, TiDB rolls back the current transaction.

    As in the following example, at the execution of the `INSERT` statement, TiDB skips a lock. Then, at the execution of the `DELETE` statement, TiDB locks the unique index and checks the unique constraints, so you will see an error is reported at the `DELETE` statement.

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    DELETE FROM users where username = 'bill';
    ```

    ```
    ERROR 8147 (23000): transaction aborted because lazy uniqueness check is enabled and an error occurred: [kv:1062]Duplicate entry 'bill' for key 'users.username'
    ```

- When this variable is disabled, the `1062 Duplicate entry` error might be not from the current SQL statement. Therefore, when a transaction operates on multiple tables that have indexes with the same name, you need to check the `1062` error message to find which index the error is actually from.

## PRIMARY KEY

Like MySQL, primary key constraints contain unique constraints, that is, creating a primary key constraint is equivalent to having a unique constraint. In addition, other primary key constraints of TiDB are also similar to those of MySQL.

For example:

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

* Table `t2` failed to be created, because column `a` is defined as the primary key and does not allow NULL values.
* Table `t3` failed to be created, because a table can only have one primary key.
* Table `t4` was created successfully, because even though there can be only one primary key, TiDB supports defining multiple columns as the composite primary key.

In addition to the rules above, TiDB currently only supports adding and deleting the primary keys of the `NONCLUSTERED` type. For example:

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

For more details about the primary key of the `CLUSTERED` type, refer to [clustered index](/clustered-indexes.md).

## FOREIGN KEY

> **Note:**
>
> Starting from v6.6.0, TiDB supports the [FOREIGN KEY constraints](/foreign-key.md) feature. Before v6.6.0, TiDB supports creating and deleting foreign key constraints, but the constraints are not actually effective. After upgrading TiDB to v6.6.0, you can delete the invalid foreign key and create a new one to make the foreign key constraints effective.

TiDB supports creating `FOREIGN KEY` constraints in DDL commands.

For example:

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

TiDB also supports the syntax to `DROP FOREIGN KEY` and `ADD FOREIGN KEY` via the `ALTER TABLE` command.

```sql
ALTER TABLE orders DROP FOREIGN KEY fk_user_id;
ALTER TABLE orders ADD FOREIGN KEY fk_user_id (user_id) REFERENCES users(id);
```
