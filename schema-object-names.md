---
title: Schema Object Names
category: reference
---

# Schema Object Names

在 TiDB 中，包括 database，table，index，column，alias 等等都被认为是 identifier (标识符，之后阐述用英文).

在 TiDB 中，identifier可以被反引号 (\`) 包裹，为了阐述方便，我们叫这种情况为 `被引用`。identifier 也可以不被 \` 包裹。但是如果一个 identifier 存在一个特殊符号或者是一个保留关键字，那么你必须要 `引用` 它。

{{< copyable "sql" >}}

```sql
SELECT * FROM `table` WHERE `table`.id = 20;
```

如果`ANSI_QUOTES` sql mode 被设置了，那么我们认为被双引号 `"` 包裹的字符串为 identifier。

{{< copyable "sql" >}}

```sql
CREATE TABLE "test" (a varchar(10));
```

```
ERROR 1105 (HY000): line 0 column 19 near " (a varchar(10))" (total length 35)
```

{{< copyable "sql" >}}

```sql
SET SESSION sql_mode='ANSI_QUOTES';
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE TABLE "test" (a varchar(10));
```

```
Query OK, 0 rows affected (0.09 sec)
```

如果你需要在被引用的 identifier 中使用反引号这个字符，那你需要重复两次，例如你需要创建一个表为 a`b：

{{< copyable "sql" >}}

```sql
CREATE TABLE `a``b` (a int);
```

在 select 语句中，alias 语句可以用 identifier 或者字符串：

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

更多[细节](https://dev.mysql.com/doc/refman/5.7/en/identifiers.html)

## Identifier Qualifiers

Object Names (对象名字) 可以被限定也可以不用。例如你可以在创建表的时候不指定 database names：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (i int);
```

但是如果你之前没有设定过默认的数据库，会报 `ERROR 1046 (3D000): No database selected` 错误。当然你也可以指定数据库限定名：

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t (i int);
```

对于 `.` 左右两端可以出现空格，`table_name.col_name` 等于 `table_name . col_name`。

如果你要引用这个 identifier，那么请使用：

```
`table_name`.`col_name`
```

而不是：

```
`table_name.col_name`
```

更多[细节](https://dev.mysql.com/doc/refman/5.7/en/identifier-qualifiers.html)
