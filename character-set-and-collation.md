---
title: 字符集和排序规则
aliases: ['/docs-cn/dev/character-set-and-collation/','/docs-cn/dev/reference/sql/characterset-and-collation/','/docs-cn/dev/reference/sql/character-set/']
---

# 字符集和排序规则

本文介绍了 TiDB 中支持的字符集和排序规则。

## 字符集和排序规则的概念

字符集 (character set) 是符号与编码的集合。TiDB 中的默认字符集是 utf8mb4，与 MySQL 8.0 及更高版本中的默认字符集匹配。

排序规则 (collation) 是在字符集中比较字符以及字符排序顺序的规则。例如，在二进制排序规则中，比较“A”和“a”的结果是不一样的：

{{< copyable "sql" >}}

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_bin;
SELECT 'A' = 'a';
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
SELECT 'A' = 'a';
```

```sql
mysql> SELECT 'A' = 'a';
+-----------+
| 'A' = 'a' |
+-----------+
|         0 |
+-----------+
1 row in set (0.00 sec)

mysql> SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT 'A' = 'a';
+-----------+
| 'A' = 'a' |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
```

TiDB 默认使用二进制排序规则。这一点与 MySQL 不同，MySQL 默认使用不区分大小写的排序规则。

## 支持的字符集和排序规则

目前 TiDB 支持以下字符集：

{{< copyable "sql" >}}

```sql
SHOW CHARACTER SET;
```

```sql
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

TiDB 支持以下排序规则：

```sql
mysql> show collation;
+------------------------------+---------+------+---------+----------+---------+
| Collation                    | Charset | Id   | Default | Compiled | Sortlen |
+------------------------------+---------+------+---------+----------+---------+
| ascii_bin                    | ascii   |   65 | Yes     | Yes      |       1 |
| binary                       | binary  |   63 | Yes     | Yes      |       1 |
| latin1_bin                   | latin1  |   47 | Yes     | Yes      |       1 |
| utf8_bin                     | utf8    |   83 | Yes     | Yes      |       1 |
| utf8_general_ci              | utf8    |   33 |         | Yes      |       1 |
| utf8_unicode_ci              | utf8    |  192 |         | Yes      |       1 |
| utf8mb4_bin                  | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci           | utf8mb4 |   45 |         | Yes      |       1 |
| utf8mb4_unicode_ci           | utf8mb4 |  224 |         | Yes      |       1 |
| utf8mb4_zh_pinyin_tidb_as_cs | utf8mb4 | 2048 |         | Yes      |       1 |
+------------------------------+---------+------+---------+----------+---------+
10 rows in set (0.20 sec)
```

> **警告：**
>
> TiDB 会错误地将 `latin1` 视为 `utf8` 的子集。当用户存储不同于 `latin1` 和 `utf8` 编码的字符时，可能会导致意外情况出现。因此强烈建议使用 `utf8mb4` 字符集。详情参阅 [TiDB #18955](https://github.com/pingcap/tidb/issues/18955)。

> **注意：**
>
> TiDB 中的默认排序规则（后缀为 `_bin` 的二进制排序规则）与 [MySQL 中的默认排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-charsets.html)不同，后者通常是一般排序规则，后缀为 `_general_ci`。当用户指定了显式字符集，但依赖于待选的隐式默认排序规则时，这个差异可能导致兼容性问题。

利用以下的语句可以查看字符集对应的排序规则（以下是[新的排序规则框架](#新框架下的排序规则支持)）下的结果：

{{< copyable "sql" >}}

```sql
SHOW COLLATION WHERE Charset = 'utf8mb4';
```

```sql
+--------------------+---------+------+---------+----------+---------+
| Collation          | Charset | Id   | Default | Compiled | Sortlen |
+--------------------+---------+------+---------+----------+---------+
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 |  224 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
3 rows in set (0.00 sec)
```

## TiDB 中的 `utf8` 和 `utf8mb4`

MySQL 限制字符集 `utf8` 为最多 3 个字节。这足以存储在基本多语言平面 (BMP) 中的字符，但不足以存储表情符号等字符。因此，建议改用字符集`utf8mb4`。

默认情况下，TiDB 同样限制字符集 `utf8` 为最多 3 个字节，以确保 TiDB 中创建的数据可以在 MySQL 中顺利恢复。你可以禁用此功能，方法是在 TiDB 配置文件中将 `check-mb4-value-in-utf8` 的值更改为 `FALSE`。

以下示例演示了在表中插入 4 字节的表情符号字符时的默认行为。`utf8` 字符集下 `INSERT` 语句不能执行，`utf8mb4` 字符集下可以执行 `INSERT` 语句：

```sql
mysql> CREATE TABLE utf8_test (
    ->  c char(1) NOT NULL
    -> ) CHARACTER SET utf8;
Query OK, 0 rows affected (0.09 sec)

mysql> CREATE TABLE utf8m4_test (
    ->  c char(1) NOT NULL
    -> ) CHARACTER SET utf8mb4;
Query OK, 0 rows affected (0.09 sec)

mysql> INSERT INTO utf8_test VALUES ('😉');
ERROR 1366 (HY000): incorrect utf8 value f09f9889(😉) for column c
mysql> INSERT INTO utf8m4_test VALUES ('😉');
Query OK, 1 row affected (0.02 sec)

mysql> SELECT char_length(c), length(c), c FROM utf8_test;
Empty set (0.01 sec)

mysql> SELECT char_length(c), length(c), c FROM utf8m4_test;
+----------------+-----------+------+
| char_length(c) | length(c) | c    |
+----------------+-----------+------+
|              1 |         4 | 😉     |
+----------------+-----------+------+
1 row in set (0.00 sec)
```

## 不同范围的字符集和排序规则

字符集和排序规则可以在设置在不同的层次。

### 数据库的字符集和排序规则

每个数据库都有相应的字符集和排序规则。数据库的字符集和排序规则可以通过以下语句来设置：

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
CREATE SCHEMA test1 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
USE test1;
```

```sql
Database changed
```

{{< copyable "sql" >}}

```sql
SELECT @@character_set_database, @@collation_database;
```

```sql
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| utf8mb4                  | utf8mb4_general_ci   |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE SCHEMA test2 CHARACTER SET latin1 COLLATE latin1_bin;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
USE test2;
```

```sql
Database changed
```

{{< copyable "sql" >}}

```sql
SELECT @@character_set_database, @@collation_database;
```

```sql
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

### 表的字符集和排序规则

表的字符集和排序规则可以通过以下语句来设置：

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

```sql
Query OK, 0 rows affected (0.08 sec)
```

如果表的字符集和排序规则没有设置，那么数据库的字符集和排序规则就作为其默认值。

### 列的字符集和排序规则

列的字符集和排序规则的语法如下：

```sql
col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]
```

如果列的字符集和排序规则没有设置，那么表的字符集和排序规则就作为其默认值。

### 字符串的字符集和排序规则

每一个字符串都对应一个字符集和一个排序规则，在使用字符串时指此选项可选，如下：

```sql
[_charset_name]'string' [COLLATE collation_name]
```

示例如下：

{{< copyable "sql" >}}

```sql
SELECT 'string';
SELECT _utf8mb4'string';
SELECT _utf8mb4'string' COLLATE utf8mb4_general_ci;
```

规则如下：

* 规则 1：如果指定了 `CHARACTER SET charset_name` 和 `COLLATE collation_name`，则直接使用 `charset_name`  字符集和 `collation_name` 排序规则。
* 规则 2：如果指定了 `CHARACTER SET charset_name` 且未指定 `COLLATE collation_name`，则使用 `charset_name` 字符集和 `charset_name` 对应的默认排序规则。
* 规则 3：如果 `CHARACTER SET charset_name` 和 `COLLATE collation_name` 都未指定，则使用 `character_set_connection` 和 `collation_connection` 系统变量给出的字符集和排序规则。

### 客户端连接的字符集和排序规则

* 服务器的字符集和排序规则可以通过系统变量 `character_set_server` 和 `collation_server` 获取。
* 数据库的字符集和排序规则可以通过环境变量 `character_set_database` 和 `collation_database` 获取。

对于每一个客户端的连接，也有相应的变量表示字符集和排序规则：`character_set_connection` 和 `collation_connection`。

`character_set_client` 代表客户端的字符集。在返回结果前，服务端会把结果根据 `character_set_results` 转换成对应的字符集，包括结果的元信息等。

可以用以下的语句来影响这些跟客户端相关的字符集变量：

* `SET NAMES 'charset_name' [COLLATE 'collation_name']`

    `SET NAMES` 用来设定客户端会在之后的请求中使用的字符集。`SET NAMES utf8mb4` 表示客户端会在接下来的请求中，都使用 utf8mb4 字符集。服务端也会在之后返回结果的时候使用 utf8mb4 字符集。`SET NAMES 'charset_name'` 语句其实等于下面语句的组合：

    {{< copyable "sql" >}}

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE` 是可选的，如果没有提供，将会用 `charset_name` 对应的默认排序规则设置 `collation_connection`。

* `SET CHARACTER SET 'charset_name'`

    跟 `SET NAMES` 类似，等价于下面语句的组合：

    {{< copyable "sql" >}}

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET charset_connection = @@charset_database;
    SET collation_connection = @@collation_database;
    ```

## 服务器、数据库、表、列、字符串的字符集和排序规则的优先级

优先级从高到低排列顺序为：

字符串 > 列 > 表 > 数据库 > 服务器

## 字符集和排序规则的通用选择规则

* 规则 1：如果指定了 `CHARACTER SET charset_name` 和 `COLLATE collation_name`，则直接使用 `charset_name` 字符集和 `collation_name` 排序规则。
* 规则 2：如果指定了 `CHARACTER SET charset_name` 且未指定 `COLLATE collation_name`，则使用 `charset_name` 字符集和 `charset_name` 对应的默认排序规则。
* 规则 3：如果 `CHARACTER SET charset_name` 和 `COLLATE collation_name` 都未指定，则使用更高优先级的字符集和排序规则。

## 字符合法性检查

当指定的字符集为 utf8 或 utf8mb4 时，TiDB 仅支持合法的 utf8 字符。对于不合法的字符，会报错：`incorrect utf8 value`。该字符合法性检查与 MySQL 8.0 兼容，与 MySQL 5.7 及以下版本不兼容。

如果不希望报错，可以通过 `set @@tidb_skip_utf8_check=1;` 跳过字符检查。

## 排序规则支持

排序规则的语法支持和语义支持受到配置项 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 的影响。这里语法支持和语义支持有所区别。语法支持是指 TiDB 能够解析和设置排序规则；而语义支持是指 TiDB 能够在比较字符串时正确地使用排序规则。

在 4.0 版本之前，TiDB 只提供了旧的排序规则框架，能够在语法上支持的绝大部分 MySQL 排序规则，但语义上所有的排序规则都当成二进制排序规则。

4.0 版本中，TiDB 增加了新的排序规则框架用于在语义上支持不同的排序规则，保证字符串比较时严格遵循对应的排序规则，详情请见下文。

### 旧框架下的排序规则支持

在 4.0 版本之前，TiDB 中可以指定大部分 MySQL 中的排序规则，并把这些排序规则按照默认排序规则处理，即以编码字节序为字符定序。和 MySQL 不同的是，TiDB 在比较字符前按照排序规则的 PADDING 属性将字符末尾的空格删除，因此会造成以下的行为区别：

{{< copyable "sql" >}}

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
Query OK, 0 rows affected
INSERT INTO t VALUES ('A');
Query OK, 1 row affected
INSERT INTO t VALUES ('a');
Query OK, 1 row affected # TiDB 会执行成功，而在 MySQL 中，则由于 utf8mb4_general_ci 大小写不敏感，报错 Duplicate entry 'a'。
INSERT INTO t VALUES ('a ');
Query OK, 1 row affected # TiDB 会执行成功，而在 MySQL 中，则由于补齐空格比较，报错 Duplicate entry 'a '。
```

### 新框架下的排序规则支持

TiDB 4.0 新增了完整的排序规则支持框架，从语义上支持了排序规则，并新增了配置开关 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)，在集群初次初始化时决定是否启用新排序规则框架。在该配置开关打开之后初始化集群，可以通过 `mysql`.`tidb` 表中的 `new_collation_enabled` 变量确认是否启用新排序规则框架：

{{< copyable "sql" >}}

```sql
SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME='new_collation_enabled';
```

```sql
+----------------+
| VARIABLE_VALUE |
+----------------+
| True           |
+----------------+
1 row in set (0.00 sec)
```

在新的排序规则框架下，TiDB 能够支持 `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_unicode_ci` 和 `utf8mb4_unicode_ci` 这几种排序规则，与 MySQL 兼容。

使用 `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_unicode_ci` 和 `utf8mb4_unicode_ci` 中任一种时，字符串之间的比较是大小写不敏感 (case-insensitive) 和口音不敏感 (accent-insensitive) 的。同时，TiDB 还修正了排序规则的 `PADDING` 行为：

{{< copyable "sql" >}}

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
Query OK, 0 rows affected (0.00 sec)
INSERT INTO t VALUES ('A');
Query OK, 1 row affected (0.00 sec)
INSERT INTO t VALUES ('a');
ERROR 1062 (23000): Duplicate entry 'a' for key 'PRIMARY' # TiDB 兼容了 MySQL 的 case insensitive collation。
INSERT INTO t VALUES ('a ');
ERROR 1062 (23000): Duplicate entry 'a ' for key 'PRIMARY' # TiDB 修正了 `PADDING` 行为，与 MySQL 兼容。
```

> **注意：**
>
> TiDB 中 padding 的实现方式与 MySQL 的不同。在 MySQL 中，padding 是通过补齐空格实现的。而在 TiDB 中 padding 是通过裁剪掉末尾的空格来实现的。两种做法在绝大多数情况下是一致的，唯一的例外是字符串尾部包含小于空格 (0x20) 的字符时，例如 `'a' < 'a\t'` 在 TiDB 中的结果为 `1`，而在 MySQL 中，其等价于 `'a ' < 'a\t'`，结果为 `0`。

## 表达式中排序规则的 Coercibility 值

如果一个表达式涉及多个不同排序规则的子表达式时，需要对计算时用的排序规则进行推断，规则如下：

+ 显式 `COLLATE` 子句的 coercibility 值为 `0`。
+ 如果两个字符串的排序规则不兼容，这两个字符串 `concat` 结果的 coercibility 值为 `1`。
+ 列或者 `CAST()`、`CONVERT()` 和 `BINARY()` 的排序规则的 coercibility 值为 `2`。
+ 系统常量（`USER()` 或者 `VERSION()` 返回的字符串）的 coercibility 值为 `3`。
+ 常量的 coercibility 值为 `4`。
+ 数字或者中间变量的 coercibility 值为 `5`。
+ `NULL` 或者由 `NULL` 派生出的表达式的 coercibility 值为 `6`。

在推断排序规则时，TiDB 优先使用 coercibility 值较低的表达式的排序规则。如果 coercibility 值相同，则按以下优先级确定排序规则：

binary > utf8mb4_bin > (utf8mb4_general_ci = utf8mb4_unicode_ci) > utf8_bin > (utf8_general_ci = utf8_unicode_ci) > latin1_bin > ascii_bin

以下情况 TiDB 无法推断排序规则并报错：

- 如果两个子表达式的排序规则不相同，而且表达式的 coercibility 值都为 `0`。
- 如果两个子表达式的排序规则不兼容，而且表达式的返回类型为 `String` 类。

## `COLLATE` 子句

TiDB 支持使用 `COLLATE` 子句来指定一个表达式的排序规则，该表达式的 coercibility 值为 `0`，具有最高的优先级。示例如下：

{{< copyable "sql" >}}

```sql
SELECT 'a' = _utf8mb4 'A' collate utf8mb4_general_ci;
```

```sql
+-----------------------------------------------+
| 'a' = _utf8mb4 'A' collate utf8mb4_general_ci |
+-----------------------------------------------+
|                                             1 |
+-----------------------------------------------+
1 row in set (0.00 sec)
```

更多细节，参考 [Connection Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-connection.html)。
