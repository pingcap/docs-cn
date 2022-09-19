---
title: SAVEPOINT | TiDB SQL Statement Reference
summary: An overview of the usage of SAVEPOINT for the TiDB database.
---

# SAVEPOINT

`SAVEPOINT` is a feature introduced in TiDB v6.2.0. The syntax is as follows:

```sql
SAVEPOINT identifier
ROLLBACK TO [SAVEPOINT] identifier
RELEASE SAVEPOINT identifier
```

> **Warning:**
>
> - You cannot use `SAVEPOINT` with TiDB Binlog enabled.
> - You cannot use `SAVEPOINT` in pessimistic transactions when [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) is disabled.

- `SAVEPOINT` is used to set a savepoint of a specified name in the current transaction. If a savepoint with the same name already exists, it will be deleted and a new savepoint with the same name will be set.

- `ROLLBACK TO SAVEPOINT` rolls back a transaction to the savepoint of a specified name and does not terminate the transaction. Data changes made to the table data after the savepoint will be reverted in the rollback, and all savepoints after the savepoint are deleted. In a pessimistic transaction, the locks held by the transaction are not rolled back. Instead, the locks will be released when the transaction ends.

    If the savepoint specified in the `ROLLBACK TO SAVEPOINT` statement does not exist, the statement returns the following error:

    ```
    ERROR 1305 (42000): SAVEPOINT identifier does not exist
    ```

- `RELEASE SAVEPOINT` statement removes the named savepoint and **all savepoints** after this savepoint from the current transaction, without committing or rolling back the current transaction. If the savepoint of the specified name does not exist, the following error is returned:

    ```
    ERROR 1305 (42000): SAVEPOINT identifier does not exist
    ```

    After the transaction is committed or rolled back, all savepoints in the transaction will be deleted.

## Examples

Create a table `t1`:

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

Start the current transaction:

```sql
BEGIN;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

Insert data into the table and set a savepoint `sp1`:

```sql
INSERT INTO t1 VALUES (1);
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
SAVEPOINT sp1;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

Insert data into the table again and set a savepoint `sp2`:

```sql
INSERT INTO t1 VALUES (2);
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
SAVEPOINT sp2;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

Release the savepoint `sp2`:

```sql
RELEASE SAVEPOINT sp2;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

Roll back to the savepoint `sp1`:

```sql
ROLLBACK TO SAVEPOINT sp1;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

Commit the transaction and query the table. Only the data inserted before `sp1` is returned.

```sql
COMMIT;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
SELECT * FROM t1;
```

```sql
+---+
| a |
+---+
| 1 |
+---+
1 row in set
```

## MySQL compatibility

When `ROLLBACK TO SAVEPOINT` is used to roll back a transaction to a specified savepoint, MySQL releases the locks held only after the specified savepoint, while in TiDB pessimistic transaction, TiDB does not immediately release the locks held after the specified savepoint. Instead, TiDB releases all locks when the transaction is committed or rolled back.

## See also

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [TiDB Optimistic Transaction Mode](/optimistic-transaction.md)
* [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md)
