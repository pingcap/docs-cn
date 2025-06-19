---
title: Schema 对象名称
summary: 了解 TiDB SQL 语句中的 schema 对象名称。
---

# Schema 对象名称

<!-- markdownlint-disable MD038 -->

本文档介绍 TiDB SQL 语句中的 schema 对象名称。

Schema 对象名称用于命名 TiDB 中的所有 schema 对象，包括数据库、表、索引、列和别名。你可以在 SQL 语句中使用标识符来引用这些对象。

你可以使用反引号来包围标识符。例如，`SELECT * FROM t` 也可以写作 `` SELECT * FROM `t` ``。但是，如果标识符包含一个或多个特殊字符或是保留关键字，则必须用反引号包围以引用它所代表的 schema 对象。

{{< copyable "sql" >}}

```sql
SELECT * FROM `table` WHERE `table`.id = 20;
```

如果你在 SQL MODE 中设置了 `ANSI_QUOTES`，TiDB 将识别用双引号 `"` 包围的字符串作为标识符。

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

如果你想在引用的标识符中使用反引号字符，请重复反引号两次。例如，要创建一个名为 a`b 的表：

{{< copyable "sql" >}}

```sql
CREATE TABLE `a``b` (a int);
```

在 `SELECT` 语句中，你可以使用标识符或字符串来指定别名：

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

更多信息，请参见 [MySQL Schema Object Names](https://dev.mysql.com/doc/refman/8.0/en/identifiers.html)。

## 标识符限定符

对象名称可以是非限定的或限定的。例如，以下语句创建一个没有限定名称的表：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (i int);
```

如果你没有使用 `USE` 语句或连接参数来配置数据库，将显示 `ERROR 1046 (3D000): No database selected` 错误。此时，你可以指定数据库限定名称：

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t (i int);
```

`.` 周围可以存在空格。`table_name.col_name` 和 `table_name . col_name` 是等价的。

要引用此标识符，请使用：

{{< copyable "sql" >}}

```sql
`table_name`.`col_name`
```

而不是：

```sql
`table_name.col_name`
```

更多信息，请参见 [MySQL Identifier Qualifiers](https://dev.mysql.com/doc/refman/8.0/en/identifier-qualifiers.html)。
