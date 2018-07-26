---
title: Prepared SQL Statement Syntax
summary: Use Prepared statements to reduce the load of statement parsing and query optimization, and improve execution efficiency.
category: user guide
---

# Prepared SQL Statement Syntax

TiDB supports server-side Prepared statements, which can reduce the load of statement parsing and query optimization and improve execution efficiency. You can use Prepared statements in two ways: application programs and SQL statements.

## Use application programs

Most MySQL Drivers support Prepared statements, such as [MySQL Connector/C](https://dev.mysql.com/doc/connector-c/en/). You can call the Prepared statement API directly through the Binary protocol.

## Use SQL statements

You can also implement Prepared statements using `PREPARE`, `EXECUTE` and `DEALLOCATE PREPARE`. This approach is not as efficient as the application programs, but you do not need to write a program.

### `PREPARE` statement

```sql
PREPARE stmt_name FROM preparable_stmt
```

The `PREPARE` statement preprocesses `preparable_stmt` (syntax parsing, semantic check and query optimization) and names the result as `stmt_name`. The following operations can refer to it using `stmt_name`. Processed statements can be executed using the `EXECUTE` statement or released using the `DEALLOCATE PREPARE` statement.

### `EXECUTE` statement

```sql
EXECUTE stmt_name [USING @var_name [, @var_name] ...]
```

The `EXECUTE` statement executes the prepared statements named as `stmt_name`. If parameters exist in the prepared statements, use the User Variable list in the `USING` clause to assign values to parameters.

### `DEALLOCATE PREPARE` statement

```sql
{DEALLOCATE | DROP} PREPARE stmt_name
```

The `DEALLOCATE PREPARE` statement is used to delete the result of the prepared statements returned by `PREPARE`.

For more information, see [MySQL Prepared Statement Syntax](https://dev.mysql.com/doc/refman/5.7/en/sql-syntax-prepared-statements.html).
