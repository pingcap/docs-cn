---
title: Schema Object Names
summary: Learn about the schema object names (identifiers) in TiDB.
category: reference
---

# Schema Object Names

Some objects names in TiDB, including database, table, index, column, alias, etc., are known as identifiers.

In TiDB, you can quote or unquote an identifier. If an identifier contains special characters or is a reserved word, you must quote it whenever you refer to it. To quote, use the backtick (\`) to wrap the identifier. For example:

```sql
mysql> SELECT * FROM `table` WHERE `table`.id = 20;
```

If the `ANSI_QUOTES` SQL mode is enabled, you can also quote identifiers within double quotation marks("):

```sql
mysql> CREATE TABLE "test" (a varchar(10));
ERROR 1105 (HY000): line 0 column 19 near " (a varchar(10))" (total length 35)

mysql> SET SESSION sql_mode='ANSI_QUOTES';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE TABLE "test" (a varchar(10));
Query OK, 0 rows affected (0.09 sec)
```

The quote characters can be included within an identifier. Double the character if the character to be included within the identifier is the same as that used to quote the identifier itself. For example, the following statement creates a table named a\`b:

```sql
mysql> CREATE TABLE `a``b` (a int);
```

In a `SELECT` statement, a quoted column alias can be specified using an identifier or a string quoting characters:

```sql
mysql> SELECT 1 AS `identifier`, 2 AS 'string';
+------------+--------+
| identifier | string |
+------------+--------+
|          1 |      2 |
+------------+--------+
1 row in set (0.00 sec)
```

For more information, see [MySQL Schema Object Names](https://dev.mysql.com/doc/refman/5.7/en/identifiers.html).

## Identifier qualifiers

Object names can be unqualified or qualified. For example, the following statement creates a table using the unqualified name `t`:

```sql
CREATE TABLE t (i int);
```

If there is no default database, the `ERROR 1046 (3D000): No database selected` is displayed. You can also use the qualified name `test.t`:

```sql
CREATE TABLE test.t (i int);
```

The qualifier character is a separate token and need not be contiguous with the associated identifiers. For example, there can be white spaces around `.`, and `table_name.col_name` and `table_name . col_name` are equivalent.

To quote this identifier, use:

```sql
`table_name`.`col_name`
```

Instead of

```sql
`table_name.col_name`
```

For more information, see [MySQL Identifier Qualifiers](https://dev.mysql.com/doc/refman/5.7/en/identifier-qualifiers.html).
