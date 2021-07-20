---
title: User-Defined Variables
summary: Learn how to use user-defined variables.
aliases: ['/docs/dev/user-defined-variables/','/docs/dev/reference/sql/language-structure/user-defined-variables/']
---

# User-Defined Variables

This document describes the concept of user-defined variables in TiDB and the methods to set and read the user-defined variables.

> **Warning:**
>
> User-defined variables are still an experimental feature. It is **NOT** recommended that you use them in the production environment.

The format of the user-defined variables is `@var_name`. The characters that compose `var_name` can be any characters that can compose an identifier, including the numbers `0-9`, the letters `a-zA-Z`, the underscore `_`, the dollar sign `$`, and the UTF-8 characters. In addition, it also includes the English period `.`. The user-defined variables are case-insensitive.

The user-defined variables are session-specific, which means a user variable defined by one client connection cannot be seen or used by other client connections.

## Set the user-defined variables

You can use the `SET` statement to set a user-defined variable, and the syntax is `SET @var_name = expr [, @var_name = expr] ...;`. For example:

{{< copyable "sql" >}}

```sql
SET @favorite_db = 'TiDB';
```

{{< copyable "sql" >}}

```sql
SET @a = 'a', @b = 'b', @c = 'c';
```

For the assignment operator, you can also use `:=`. For example:

{{< copyable "sql" >}}

```sql
SET @favorite_db := 'TiDB';
```

The content to the right of the assignment operator can be any valid expression. For example:

{{< copyable "sql" >}}

```sql
SET @c = @a + @b;
```

{{< copyable "sql" >}}

```sql
set @c = b'1000001' + b'1000001';
```

## Read the user-defined variables

To read a user-defined variable, you can use the `SELECT` statement to query:

{{< copyable "sql" >}}

```sql
SELECT @a1, @a2, @a3
```

```
+------+------+------+
| @a1  | @a2  | @a3  |
+------+------+------+
|    1 |    2 |    4 |
+------+------+------+
```

You can also assign values in the `SELECT` statement:

```sql
SELECT @a1, @a2, @a3, @a4 := @a1+@a2+@a3;
```

```
+------+------+------+--------------------+
| @a1  | @a2  | @a3  | @a4 := @a1+@a2+@a3 |
+------+------+------+--------------------+
|    1 |    2 |    4 |                  7 |
+------+------+------+--------------------+
```

Before the variable `@a4` is modified or the connection is closed, its value is always `7`.

If a hexadecimal literal or binary literal is used when setting the user-defined variable, TiDB will treat it as a binary string. If you want to set it to a number, you can manually add the `CAST` conversion, or use the numeric operator in the expression:

{{< copyable "sql" >}}

```sql
SET @v1 = b'1000001';
SET @v2 = b'1000001'+0;
SET @v3 = CAST(b'1000001' AS UNSIGNED);
```

{{< copyable "sql" >}}

```sql
SELECT @v1, @v2, @v3;
```

```
+------+------+------+
| @v1  | @v2  | @v3  |
+------+------+------+
| A    | 65   | 65   |
+------+------+------+
```

If you refer to a user-defined variable that has not been initialized, it has a value of NULL and a type of string.

{{< copyable "sql" >}}

```sql
SELECT @not_exist;
```

```
+------------+
| @not_exist |
+------------+
| NULL       |
+------------+
```

In addition to using the `SELECT` statement to read the user-defined variables, another common usage is the `PREPARE` statement. For example:

{{< copyable "sql" >}}

```sql
SET @s = 'SELECT SQRT(POW(?,2) + POW(?,2)) AS hypotenuse';
PREPARE stmt FROM @s;
SET @a = 6;
SET @b = 8;
EXECUTE stmt USING @a, @b;
```

```
+------------+
| hypotenuse |
+------------+
|         10 |
+------------+
```

The contents of the user-defined variables are not recognized as identifiers in the SQL statements. For example:

{{< copyable "sql" >}}

```sql
SELECT * from t;
```

```
+---+
| a |
+---+
| 1 |
+---+
```

{{< copyable "sql" >}}

```sql
SET @col = "`a`";
SELECT @col FROM t;
```

```
+------+
| @col |
+------+
| `a`  |
+------+
```

## MySQL compatibility

Except for `SELECT ... INTO <variable>`, the syntax supported in MySQL and TiDB is identical.

For more information, see [User-Defined Variables in MySQL](https://dev.mysql.com/doc/refman/5.7/en/user-variables.html).
