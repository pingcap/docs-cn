---
title: Schema Object Names
summary: Learn about schema object names in TiDB SQL statements.
aliases: ['/docs/dev/schema-object-names/','/docs/dev/reference/sql/language-structure/schema-object-names/']
---

# Schema Object Names

<!-- markdownlint-disable MD038 -->

This document introduces schema object names in TiDB SQL statements.

Schema object names are used to name all schema objects in TiDB, including database, table, index, column, and alias. You can quote these objects using identifiers in SQL statements.

You can use backticks to enclose the identifier. For example, `SELECT * FROM t` can also be written as `` SELECT * FROM `t` ``. But if the identifier includes one or more special characters or is a reserved keyword, it must be enclosed in backticks to quote the schema object it represents.

{{< copyable "sql" >}}

```sql
SELECT * FROM `table` WHERE `table`.id = 20;
```

If you set `ANSI_QUOTES` in SQL MODE, TiDB will recognize the string enclosed in double quotation marks `"` as an identifier.

{{< copyable "sql" >}}

```sql
CREATE TABLE "test" (a varchar(10));
```

```sql
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 19 near ""test" (a varchar(10))" 
```

{{< copyable "sql" >}}

```sql
SET SESSION sql_mode='ANSI_QUOTES';
```

```sql
Query OK, 0 rows affected (0.000 sec)
```

{{< copyable "sql" >}}

```sql
CREATE TABLE "test" (a varchar(10));
```

```sql
Query OK, 0 rows affected (0.012 sec)
```

If you want to use the backtick character in the quoted identifier, repeat the backtick twice. For example, to create a table a`b:

{{< copyable "sql" >}}

```sql
CREATE TABLE `a``b` (a int);
```

In a `SELECT` statement, you can use an identifier or a string to specify an alias:

{{< copyable "sql" >}}

```sql
SELECT 1 AS `identifier`, 2 AS 'string';
```

```sql
+------------+--------+
| identifier | string |
+------------+--------+
|          1 |      2 |
+------------+--------+
1 row in set (0.00 sec)
```

For more information, see [MySQL Schema Object Names](https://dev.mysql.com/doc/refman/8.0/en/identifiers.html).

## Identifier qualifiers

Object names can be unqualified or qualified. For example, the following statement creates a table without a qualified name:

{{< copyable "sql" >}}

```sql
CREATE TABLE t (i int);
```

If you have not used the `USE` statement or the connection parameter to configure the database, the `ERROR 1046 (3D000): No database selected` error is displayed. At this time, you can specify the database qualified name:

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t (i int);
```

White spaces can exist around `.`. `table_name.col_name` and `table_name . col_name` are equivalent.

To quote this identifier, use:

{{< copyable "sql" >}}

```sql
`table_name`.`col_name`
```

Instead of:

```sql
`table_name.col_name`
```

For more information, see [MySQL Identifier Qualifiers](https://dev.mysql.com/doc/refman/8.0/en/identifier-qualifiers.html).
