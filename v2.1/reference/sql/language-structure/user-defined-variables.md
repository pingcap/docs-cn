---
title: User-Defined Variables
summary: Learn how to use user-defined variables.
category: reference
---

# User-Defined Variables

The format of the user-defined variables is `@var_name`. `@var_name` consists of alphanumeric characters, `_`, and `$`. The user-defined variables are case-insensitive.

The user-defined variables are session specific, which means a user variable defined by one client cannot be seen or used by other clients.

You can use the `SET` statement to set a user variable:

```sql
SET @var_name = expr [, @var_name = expr] ...
```
or

```sql
SET @var_name := expr
```
For SET, you can use `=` or `:=` as the assignment operator.

For example:

```sql
mysql> SET @a1=1, @a2=2, @a3:=4;
mysql> SELECT @a1, @a2, @t3, @a4 := @a1+@a2+@a3;
+------+------+------+--------------------+
| @a1 | @a2 | @a3 | @a4 := @a1+@a2+@a3 |
+------+------+------+--------------------+
| 1 | 2 | 4 | 7 |
+------+------+------+--------------------+
```

Hexadecimal or bit values assigned to user variables are treated as binary strings in TiDB. To assign a hexadecimal or bit value as a number, use it in numeric context. For example, add `0` or use `CAST(... AS UNSIGNED)`:

```sql
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1 | @v2 | @v3 |
+------+------+------+
| A | 65 | 65 |
+------+------+------+
1 row in set (0.00 sec)

mysql> SET @v1 = b'1000001';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @v2 = b'1000001'+0;
Query OK, 0 rows affected (0.00 sec)

mysql> SET @v3 = CAST(b'1000001' AS UNSIGNED);
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1 | @v2 | @v3 |
+------+------+------+
| A | 65 | 65 |
+------+------+------+
1 row in set (0.00 sec)
```

If you refer to a user-defined variable that has not been initialized, it has a value of NULL and a type of string.

```sql
mysql> select @not_exist;
+------------+
| @not_exist |
+------------+
| NULL |
+------------+
1 row in set (0.00 sec)
```

The user-defined variables cannot be used as an identifier in the SQL statement. For example:

```sql
mysql> select * from t;
+------+
| a |
+------+
| 1 |
+------+
1 row in set (0.00 sec)

mysql> SET @col = "a";
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @col FROM t;
+------+
| @col |
+------+
| a |
+------+
1 row in set (0.00 sec)

mysql> SELECT `@col` FROM t;
ERROR 1054 (42S22): Unknown column '@col' in 'field list'

mysql> SET @col = "`a`";
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @col FROM t;
+------+
| @col |
+------+
| `a` |
+------+
1 row in set (0.01 sec)
```

An exception is that when you are constructing a string for use as a prepared statement to execute later:

```sql
mysql> PREPARE stmt FROM "SELECT @c FROM t";
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE stmt;
+------+
| @c |
+------+
| a |
+------+
1 row in set (0.01 sec)

mysql> DEALLOCATE PREPARE stmt;
Query OK, 0 rows affected (0.00 sec)
```

For more information, see [User-Defined Variables in MySQL](https://dev.mysql.com/doc/refman/5.7/en/user-variables.html).
