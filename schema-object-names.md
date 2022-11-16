---
title: Schema 对象名
summary: 本文介绍 TiDB SQL 语句中的模式对象名。
---

# Schema 对象名

<!-- markdownlint-disable MD038 -->

本文介绍 TiDB SQL 语句中的模式对象名。

模式对象名用于命名 TiDB 中所有的模式对象，包括 database、table、index、column、alias 等等。在 SQL 语句中，可以通过标识符 (identifier) 来引用这些对象。

标识符可以被反引号包裹，即 `SELECT * FROM t` 也可以写成 `` SELECT * FROM `t` ``。但如果标识符中存在至少一个特殊符号，或者它是一个保留关键字，那就必须使用反引号包裹来引用它所代表的模式对象。

{{< copyable "sql" >}}

```sql
SELECT * FROM `table` WHERE `table`.id = 20;
```

如果 SQL MODE 中设置了 `ANSI_QUOTES`，那么 TiDB 会将被双引号 `"` 包裹的字符串识别为 identifier。

```sql
MySQL [test]> CREATE TABLE "test" (a varchar(10));
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 19 near ""test" (a varchar(10))" 

MySQL [test]> SET SESSION sql_mode='ANSI_QUOTES';
Query OK, 0 rows affected (0.000 sec)

MySQL [test]> CREATE TABLE "test" (a varchar(10));
Query OK, 0 rows affected (0.012 sec)
```

如果要在被引用的标识符中使用反引号这个字符，则需要重复两次反引号，例如创建一个表 a`b：

{{< copyable "sql" >}}

```sql
CREATE TABLE `a``b` (a int);
```

在 select 语句中，alias 部分可以用标识符或者字符串：

{{< copyable "sql" >}}

```sql
SELECT 1 AS `identifier`, 2 AS 'string';
```

```
+------------+--------+
| identifier | string |
+------------+--------+
|          1 |      2 |
+------------+--------+
1 row in set (0.00 sec)
```

更多细节，请参考 [MySQL 文档](https://dev.mysql.com/doc/refman/5.7/en/identifiers.html)。

## Identifier Qualifiers

Object Names（对象名字）有时可以被限定或者省略。例如在创建表的时候可以省略数据库限定名：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (i int);
```

如果之前没有使用 `USE` 或者连接参数来设定数据库，会报 `ERROR 1046 (3D000): No database selected` 错误。此时可以指定数据库限定名：

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t (i int);
```

`.` 的左右两端可以出现空格，`table_name.col_name` 等于 `table_name . col_name`。

如果要引用这个模式对象，那么请使用：

```
`table_name`.`col_name`
```

而不是：

```
`table_name.col_name`
```

更多细节，请参考 [MySQL 文档](https://dev.mysql.com/doc/refman/5.7/en/identifier-qualifiers.html)。
