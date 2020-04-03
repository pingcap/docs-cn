---
title: 字符集支持
category: reference
---

# 字符集支持

名词解释，下面的阐述中会交错使用中文或者英文，请互相对照：

* Character Set：字符集
* Collation：排序规则

collation 的语法支持和语义支持受到配置项 new_collation_enable 的影响，这里我们区分语法支持和语义支持，语法支持是指 TiDB 能够解析和设置 collation，语义支持是指 TiDB 能够在字符串比较时正确地使用 collation。如果new_collation_enable = true, 则只能设置和使用语义支持的 collation。如果 new_collation_enable = false，则能设置语法支持的 collation，语义上所有的 collation 都当成 binary collation。

目前 `TiDB` 支持以下字符集：

{{< copyable "sql" >}}

```sql
SHOW CHARACTER SET;
```

```
+---------|---------------|-------------------|--------+
| Charset | Description   | Default collation | Maxlen |
+---------|---------------|-------------------|--------+
| utf8    | UTF-8 Unicode | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode | utf8mb4_bin       |      4 |
| ascii   | US ASCII      | ascii_bin         |      1 |
| latin1  | Latin1        | latin1_bin        |      1 |
| binary  | binary        | binary            |      1 |
+---------|---------------|-------------------|--------+
5 rows in set (0.00 sec)
```

> **注意：**
>
> - 每种字符集都对应一个默认的 Collation，当前有且仅有一个。

对于字符集来说，至少会有一个 Collation（排序规则）与之对应。利用以下的语句可以查看字符集对应的排序规则（以下是 new_collation_enable = true 情况下的结果）：

{{< copyable "sql" >}}

```sql
SHOW COLLATION WHERE Charset = 'utf8mb4';
```

```
+--------------------+---------+------+---------+----------+---------+
| Collation          | Charset | Id   | Default | Compiled | Sortlen |
+--------------------+---------+------+---------+----------+---------+
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
2 rows in set (0.00 sec)
```


每一个字符集，都有一个默认的 Collation，例如 `utf8mb4` 的默认 Collation 就为 `utf8mb4_bin`。


## 集群 Character Set 和 Collation

暂不支持

## 数据库 Character Set 和 Collation

每个数据库都有相应的 Character Set 和 Collation，数据库的 Character Set 和 Collation 可以通过以下语句来设置：

```sql
CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

ALTER DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]
```

在这里 `DATABASE` 可以跟 `SCHEMA` 互换使用。

不同的数据库之间可以使用不一样的字符集和排序规则。

通过系统变量 `character_set_database` 和 `collation_database` 可以查看到当前数据库的字符集以及排序规则：

{{< copyable "sql" >}}

```sql
create schema test1 character set utf8mb4 COLLATE uft8mb4_general_ci;
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
use test1;
```

```
Database changed
```

{{< copyable "sql" >}}

```sql
SELECT @@character_set_database, @@collation_database;
```

```
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| utf8mb4                  | uft8mb4_general_ci   |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
create schema test2 character set latin1 COLLATE latin1_bin;
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
use test2;
```

```
Database changed
```

{{< copyable "sql" >}}

```sql
SELECT @@character_set_database, @@collation_database;
```

```
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| latin1                   | latin1_bin           |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

在 INFORMATION_SCHEMA 中也可以查看到这两个值：

{{< copyable "sql" >}}

```sql
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```

## 表的 Character Set 和 Collation

表的 Character Set 和 Collation 可以通过以下语句来设置：

```sql
CREATE TABLE tbl_name (column_list)
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]]

ALTER TABLE tbl_name
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]
```

例如：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1(a int) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```
Query OK, 0 rows affected (0.08 sec)
```

如果表的字符集和排序规则没有设置，那么数据库的字符集和排序规则就作为其默认值。

## 列的 Character Set 和 Collation

列的 Character Set 和 Collation 的语法如下：

```sql
col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]
```

如果列的字符集和排序规则没有设置，那么表的字符集和排序规则就作为其默认值。

## 字符串 Character Sets 和 Collation

每一字符串字符文字有一个字符集和一个比较排序规则，在使用字符串时指，此选项可选，如下：

```sql
[_charset_name]'string' [COLLATE collation_name]
```

示例，如下：

{{< copyable "sql" >}}

```sql
SELECT 'string';
SELECT _utf8mb4'string';
SELECT _utf8mb4'string' COLLATE utf8mb4_general_ci;
```

规则，如下：

* 规则1： 指定 CHARACTER SET charset_name 和 COLLATE collation_name，则直接使用 CHARACTER SET charset_name 和COLLATE collation_name。
* 规则2:    指定 CHARACTER SET charset_name 且未指定 COLLATE collation_name，则使用 CHARACTER SET charset_name 和 CHARACTER SET charset_name 默认的排序比较规则。
* 规则3:   CHARACTER SET charset_name 和 COLLATE collation_name 都未指定，则使用 character_set_connection 和 collation_connection 系统变量给出的字符集和比较排序规则。

## 客户端连接的 Character Sets 和 Collations

* 服务器的字符集和排序规则可以通过系统变量 `character_set_server` 和 `collation_server` 获取。
* 数据库的字符集和排序规则可以通过环境变量 `character_set_database` 和 `collation_database` 获取。

对于每一个客户端的连接，也有相应的变量表示字符集和排序规则：`character_set_connection` 和 `collation_connection`。

`character_set_client` 代表客户端的字符集。在返回结果前，服务端会把结果根据 `character_set_results` 转换成对应的字符集。包括结果的元信息等。

可以用以下的语句来影响这些跟客户端相关的字符集变量：

* `SET NAMES 'charset_name' [COLLATE 'collation_name']`

`SET NAMES` 用来设定客户端会在之后的请求中使用的字符集。`SET NAMES utf8mb4` 表示客户端会在接下来的请求中，都使用 utf8mb4 字符集。服务端也会在之后返回结果的时候使用 utf8mb4 字符集。
`SET NAMES 'charset_name'` 语句其实等于下面语句的组合：

{{< copyable "sql" >}}

```sql
SET character_set_client = charset_name;
SET character_set_results = charset_name;
SET character_set_connection = charset_name;
```

`COLLATE` 是可选的，如果没有提供，将会用 charset_name 默认的 Collation。

* `SET CHARACTER SET 'charset_name'`

跟 `SET NAMES` 类似，等价于下面语句的组合：

{{< copyable "sql" >}}

```sql
SET character_set_client = charset_name;
SET character_set_results = charset_name;
SET collation_connection = @@collation_database;
```

## 集群，服务器，数据库，表，列，字符串 Character Sets 和 Collation 优化级

字符串 > 列 > 表 > 数据库 > 服务器 > 集群

## Character Sets 和 Collation 通用选择规则

* 规则1： 指定 CHARACTER SET charset_name 和 COLLATE collation_name，则直接使用 CHARACTER SET charset_name 和COLLATE collation_name。
* 规则2:    指定 CHARACTER SET charset_name 且未指定 COLLATE collation_name，则使用 CHARACTER SET charset_name 和 CHARACTER SET charset_name 默认的排序比较规则。
* 规则3:   CHARACTER SET charset_name 和 COLLATE collation_name 都未指定，则使用更高优化级给出的字符集和排序比较规则。

## 字符合法性检查

当指定的字符集为 utf8 或 utf8mb4 时，TiDB 仅支持合法的 utf8 字符。对于不合法的字符，会报错：`incorrect utf8 value`。该字符合法性检查与 MySQL 8.0 兼容，与 MySQL 5.7 及以下版本不兼容。

如果不希望报错，可以通过 `set @@tidb_skip_utf8_check=1;` 跳过字符检查。

更多细节，参考 [Connection Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-connection.html)。

