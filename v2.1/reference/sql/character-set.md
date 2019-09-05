---
title: 字符集支持
category: reference
---

# 字符集支持

名词解释，下面的阐述中会交错使用中文或者英文，请互相对照：

* Character Set：字符集
* Collation：排序规则

目前 `TiDB` 支持以下字符集：

```sql
mysql> SHOW CHARACTER SET;
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

对于字符集来说，至少会有一个 Collation（排序规则）与之对应。而大部分字符集实际上会有多个 Collation。利用以下的语句可以查看：

```sql
mysql> SHOW COLLATION WHERE Charset = 'latin1';
+-------------------|---------|------|---------|----------|---------+
| Collation         | Charset | Id   | Default | Compiled | Sortlen |
+-------------------|---------|------|---------|----------|---------+
| latin1_german1_ci | latin1  |    5 |         | Yes      |       1 |
| latin1_swedish_ci | latin1  |    8 | Yes     | Yes      |       1 |
| latin1_danish_ci  | latin1  |   15 |         | Yes      |       1 |
| latin1_german2_ci | latin1  |   31 |         | Yes      |       1 |
| latin1_bin        | latin1  |   47 |         | Yes      |       1 |
| latin1_general_ci | latin1  |   48 |         | Yes      |       1 |
| latin1_general_cs | latin1  |   49 |         | Yes      |       1 |
| latin1_spanish_ci | latin1  |   94 |         | Yes      |       1 |
+-------------------|---------|------|---------|----------|---------+
8 rows in set (0.00 sec)
```

`latin1` Collation（排序规则）分别有以下含义：

| Collation         | 含义                              |
|:------------------|:----------------------------------|
| latin1_bin        | latin1 编码的二进制表示           |
| latin1_danish_ci  | 丹麦语/挪威语，不区分大小写       |
| latin1_general_ci | 多种语言的 (西欧)，不区分大小写   |
| latin1_general_cs | 多种语言的 (ISO 西欧)，区分大小写 |
| latin1_german1_ci | 德国 DIN-1 (字典序)，不区分大小写 |
| latin1_german2_ci | 德国 DIN-2，不区分大小写          |
| latin1_spanish_ci | 现代西班牙语，不区分大小写        |
| latin1_swedish_ci | 瑞典语/芬兰语，不区分大小写       |

每一个字符集，都有一个默认的 Collation，例如 `utf8` 的默认 Collation 就为 `utf8_bin`。

> **注意：**
>
> `TiDB` 目前的 Collation 都是区分大小写的。

## Collation 命名规则

`TiDB` 的 Collation 遵循着如下的命名规则：

* Collation 的前缀是它相应的字符集，通常之后会跟着一个或者更多的后缀来表名其他的排序规则， 例如：utf8_general_ci 和 lation1_swedish_ci 是 utf8
 和 latin1 字符集的 Collation。但是 binary 字符集只有一个 Collation，就是 binary。
* 一个语言对应的 Collation 会包含语言的名字，例如 utf8_turkish_ci 和 utf8_hungarian_ci 是依据 Turkish(土耳其语) 和 Hungarian(匈牙利语) 的排序规则来排序。
* Collation 的后缀表示了 Collation 是否区分大小写和是否区分口音。下面的表展示了这些特性：

| 后缀 | 含义                             |
|:-----|:---------------------------------|
| \_ai | 口音不敏感（Accent insensitive） |
| \_as | 口音敏感 （Accent sensitive）  |
| \_ci | 大小写不敏感                     |
| \_cs | 大小写敏感                       |

> **注意：**
>
> 目前为止 TiDB 只支持部分以上提到的 Collation。

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

```sql
mysql> create schema test1 character set utf8 COLLATE uft8_general_ci;
Query OK, 0 rows affected (0.09 sec)

mysql> use test1;
Database changed
mysql> SELECT @@character_set_database, @@collation_database;
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| utf8                     | uft8_general_ci      |
+--------------------------|----------------------+
1 row in set (0.00 sec)

mysql> create schema test2 character set latin1 COLLATE latin1_general_ci;
Query OK, 0 rows affected (0.09 sec)

mysql> use test2;
Database changed
mysql> SELECT @@character_set_database, @@collation_database;
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| latin1                   | latin1_general_ci    |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

在 INFORMATION_SCHEMA 中也可以查看到这两个值：

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

```sql
mysql> CREATE TABLE t1(a int) CHARACTER SET utf8 COLLATE utf8_general_ci;
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

## 客户端连接的 Character Sets 和 Collations

* 服务器的字符集和排序规则可以通过系统变量 `character_set_server` 和 `collation_server` 获取。
* 数据库的字符集和排序规则可以通过环境变量 `character_set_database` 和 `collation_database` 获取。

对于每一个客户端的连接，也有相应的变量表示字符集和排序规则：`character_set_connection` 和 `collation_connection`。

`character_set_client` 代表客户端的字符集。在返回结果前，服务端会把结果根据 `character_set_results` 转换成对应的字符集。包括结果的元信息等。

可以用以下的语句来影响这些跟客户端相关的字符集变量：

* `SET NAMES 'charset_name' [COLLATE 'collation_name']`

`SET NAMES` 用来设定客户端会在之后的请求中使用的字符集。`SET NAMES utf8` 表示客户端会在接下来的请求中，都使用 utf8 字符集。服务端也会在之后返回结果的时候使用 utf8 字符集。
`SET NAMES 'charset_name'` 语句其实等于下面语句的组合：

```
SET character_set_client = charset_name;
SET character_set_results = charset_name;
SET character_set_connection = charset_name;

```

`COLLATE` 是可选的，如果没有提供，将会用 charset_name 默认的 Collation。

* `SET CHARACTER SET 'charset_name'`

跟 `SET NAMES` 类似，等价于下面语句的组合：

```
SET character_set_client = charset_name;
SET character_set_results = charset_name;
SET collation_connection = @@collation_database;

```

## 字符合法性检查

当指定的字符集为 utf8 或 utf8mb4 时，TiDB 仅支持合法的 utf8 字符。对于不合法的字符，会报错：`incorrect utf8 value`。该字符合法性检查与 MySQL 8.0 兼容，与 MySQL 5.7 及以下版本不兼容。

如果不希望报错，可以通过 `set @@tidb_skip_utf8_check=1;` 跳过字符检查。

更多细节，参考 [Connection Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-connection.html)。
