---
title: 字符集和排序规则
summary: TiDB 支持的字符集包括 ascii、binary、gbk、latin1、utf8 和 utf8mb4。排序规则包括 ascii_bin、binary、gbk_bin、gbk_chinese_ci、latin1_bin、utf8_bin、utf8_general_ci、utf8_unicode_ci、utf8mb4_0900_ai_ci、utf8mb4_0900_bin、utf8mb4_bin、utf8mb4_general_ci 和 utf8mb4_unicode_ci。TiDB 强烈建议使用 utf8mb4 字符集，因为它支持更多字符。在 TiDB 中，默认的排序规则受到客户端的连接排序规则设置的影响。如果客户端使用 utf8mb4_0900_ai_ci 作为连接排序规则，TiDB 将遵循客户端的配置。TiDB 还支持新的排序规则框架，用于在语义上支持不同的排序规则。
---

# 字符集和排序规则

本文介绍了 TiDB 中支持的字符集和排序规则。

## 字符集和排序规则的概念

字符集 (character set) 是符号与编码的集合。TiDB 中的默认字符集是 `utf8mb4`，与 MySQL 8.0 及更高版本中的默认字符集匹配。

排序规则 (collation) 是在字符集中比较字符以及字符排序顺序的规则。例如，在二进制排序规则中，比较 `A` 和 `a` 的结果是不一样的：

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_bin;
SELECT 'A' = 'a';
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
SELECT 'A' = 'a';
```

```sql
SELECT 'A' = 'a';
```

```
+-----------+
| 'A' = 'a' |
+-----------+
|         0 |
+-----------+
1 row in set (0.00 sec)
```

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT 'A' = 'a';
```

```
+-----------+
| 'A' = 'a' |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
```

以下示例展示了不同 Unicode 排序规则如何比较德语中的 `ß` 和 `ss`。可以看到，只有较为严格的 Unicode 排序规则会将它们视为等价，从而返回 `1`（表示 TRUE）。

```sql
SELECT
  'ss' COLLATE utf8mb4_general_ci = 'ß',
  'ss' COLLATE utf8mb4_unicode_ci = 'ß',
  'ss' COLLATE utf8mb4_0900_ai_ci = 'ß',
  'ss' COLLATE utf8mb4_0900_bin = 'ß'
\G
```

```
*************************** 1. row ***************************
'ss' COLLATE utf8mb4_general_ci = 'ß': 0
'ss' COLLATE utf8mb4_unicode_ci = 'ß': 1
'ss' COLLATE utf8mb4_0900_ai_ci = 'ß': 1
  'ss' COLLATE utf8mb4_0900_bin = 'ß': 0
1 row in set (0.01 sec)
```

### 字符集和排序规则的命名

一个字符集可以有多种排序规则。排序规则的命名格式为 `<character_set>_<collation_properties>`。例如，`utf8mb4` 字符集有一个名为 `utf8mb4_bin` 的排序规则，它是 `utf8mb4` 字符集的二进制排序规则。排序规则名称中可以包含多个属性 (collation properties)，以 `_` 进行分隔。

下表介绍了字符集和排序规则的后缀和含义。

| 后缀 | 含义 |
|---|---|
| `_bin` | 二进制排序规则 |
| `_ci` | 不区分大小写 |
| `_ai_ci` | 不区分重音和大小写 |
| `_0900_bin` | Unicode UCA 9.0.0，二进制排序规则 |
| `_unicode_ci` | （较旧的）Unicode UCA 排序规则，不区分大小写 |
| `_general_ci` | 较宽松的 Unicode 排序规则，不区分大小写 |

## 支持的字符集和排序规则

目前 TiDB 支持以下字符集：

```sql
SHOW CHARACTER SET;
```

```
+---------+-------------------------------------+-------------------+--------+
| Charset | Description                         | Default collation | Maxlen |
+---------+-------------------------------------+-------------------+--------+
| ascii   | US ASCII                            | ascii_bin         |      1 |
| binary  | binary                              | binary            |      1 |
| gbk     | Chinese Internal Code Specification | gbk_bin           |      2 |
| latin1  | Latin1                              | latin1_bin        |      1 |
| utf8    | UTF-8 Unicode                       | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode                       | utf8mb4_bin       |      4 |
+---------+-------------------------------------+-------------------+--------+
6 rows in set (0.00 sec)
```

TiDB 支持以下排序规则：

```sql
SHOW COLLATION;
```

```
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 | PAD SPACE     |
| binary             | binary  |  63 | Yes     | Yes      |       1 | NO PAD        |
| gbk_bin            | gbk     |  87 |         | Yes      |       1 | PAD SPACE     |
| gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 | PAD SPACE     |
| latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_general_ci    | utf8    |  33 |         | Yes      |       1 | PAD SPACE     |
| utf8_unicode_ci    | utf8    | 192 |         | Yes      |       8 | PAD SPACE     |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
13 rows in set (0.00 sec)
```

> **警告：**
>
> TiDB 会错误地将 `latin1` 视为 `utf8` 的子集。当用户存储不同于 `latin1` 和 `utf8` 编码的字符时，可能会导致意外情况出现。因此强烈建议使用 `utf8mb4` 字符集。详情参阅 [TiDB #18955](https://github.com/pingcap/tidb/issues/18955)。

> **注意：**
>
> TiDB 中的默认排序规则（后缀为 `_bin` 的二进制排序规则）与 [MySQL 中的默认排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-charsets.html)不同，后者通常是一般排序规则，后缀为 `_general_ci` 或 `_ai_ci`。当用户指定了显式字符集，但依赖于待选的隐式默认排序规则时，这个差异可能导致兼容性问题。
> 在 TiDB 中，默认的排序规则也受到客户端的[连接排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)设置的影响。例如，MySQL 8.x 客户端默认使用 `utf8mb4_0900_ai_ci` 作为 `utf8mb4` 字符集的连接排序规则。
>
> - 在 TiDB v7.4.0 之前，如果客户端使用 `utf8mb4_0900_ai_ci` 作为[连接排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)，因为 TiDB 不支持 `utf8mb4_0900_ai_ci` 排序规则，TiDB 将回退到使用 TiDB 服务器默认的排序规则 `utf8mb4_bin`。
> - 从 v7.4.0 开始，如果客户端使用 `utf8mb4_0900_ai_ci` 作为[连接排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)，TiDB 将遵循客户端的配置，使用 `utf8mb4_0900_ai_ci` 作为默认排序规则。

利用以下的语句可以查看字符集对应的排序规则（以下是[新的排序规则框架](#新框架下的排序规则支持)）下的结果：

```sql
SHOW COLLATION WHERE Charset = 'utf8mb4';
```

```
+--------------------+---------+------+---------+----------+---------+
| Collation          | Charset | Id   | Default | Compiled | Sortlen |
+--------------------+---------+------+---------+----------+---------+
| utf8mb4_0900_ai_ci | utf8mb4 |  255 |         | Yes      |       1 |
| utf8mb4_0900_bin   | utf8mb4 |  309 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 |  224 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
5 rows in set (0.00 sec)
```

TiDB 对 GBK 字符集的支持详情见 [GBK](/character-set-gbk.md)。

## TiDB 中的 `utf8` 和 `utf8mb4`

MySQL 限制字符集 `utf8` 为最多 3 个字节。这足以存储在基本多语言平面 (Basic Multilingual Plane, BMP) 中的字符，但不足以存储表情符号 (emoji) 等字符。对于新安装的系统，建议使用 `utf8mb4` 字符集，并逐步迁移停止使用 `utf8`。

在 MySQL 和 TiDB 中，`utf8` 和 `utf8mb3` 是同一字符集的别名。

默认情况下，TiDB 也将 `utf8` 字符集限制为最多 3 个字节，以确保在 TiDB 中创建的数据仍能安全地恢复到 MySQL 中。尽管你可以通过将系统变量 [`tidb_check_mb4_value_in_utf8`](/system-variables.md#tidb_check_mb4_value_in_utf8) 的值更改为 `OFF` 来禁用此限制，但建议使用 `utf8mb4` 以获得完整的 Unicode 支持和更好的兼容性。

以下示例演示了在表中插入 4 字节的表情符号字符（emoji 字符）时的默认行为。`utf8` 字符集下 `INSERT` 语句不能执行，`utf8mb4` 字符集下可以执行 `INSERT` 语句：

```sql
CREATE TABLE utf8_test (
     c char(1) NOT NULL
    ) CHARACTER SET utf8;
```

```
Query OK, 0 rows affected (0.09 sec)
```

```sql
CREATE TABLE utf8m4_test (
     c char(1) NOT NULL
    ) CHARACTER SET utf8mb4;
```

```
Query OK, 0 rows affected (0.09 sec)
```

```sql
INSERT INTO utf8_test VALUES ('😉');
```

```
ERROR 1366 (HY000): incorrect utf8 value f09f9889(😉) for column c
```

```sql
INSERT INTO utf8m4_test VALUES ('😉');
```

```
Query OK, 1 row affected (0.02 sec)
```

```sql
SELECT char_length(c), length(c), c FROM utf8_test;
```

```
Empty set (0.01 sec)
```

```sql
SELECT char_length(c), length(c), c FROM utf8m4_test;
```

```
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

```sql
CREATE SCHEMA test1 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```
Query OK, 0 rows affected (0.09 sec)
```

```sql
USE test1;
```

```sql
Database changed
```

```sql
SELECT @@character_set_database, @@collation_database;
```

```
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| utf8mb4                  | utf8mb4_general_ci   |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

```sql
CREATE SCHEMA test2 CHARACTER SET latin1 COLLATE latin1_bin;
```

```
Query OK, 0 rows affected (0.09 sec)
```

```sql
USE test2;
```

```
Database changed
```

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

```sql
CREATE TABLE t1(a int) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```
Query OK, 0 rows affected (0.08 sec)
```

如果表的字符集和排序规则没有设置，那么数据库的字符集和排序规则就作为其默认值。在仅指定字符集为 `utf8mb4`，但未设置排序规则时，排序规则为变量 [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-从-v740-版本开始引入) 指定的值。

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

如果列的字符集和排序规则没有设置，那么表的字符集和排序规则就作为其默认值。在仅指定字符集为 `utf8mb4`，但未设置排序规则时，排序规则为变量 [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-从-v740-版本开始引入) 指定的值。

### 字符串的字符集和排序规则

每一个字符串都对应一个字符集和一个排序规则，在使用字符串时指此选项可选，如下：

```sql
[_charset_name]'string' [COLLATE collation_name]
```

示例如下：

```sql
SELECT 'string';
SELECT _utf8mb4'string';
SELECT _utf8mb4'string' COLLATE utf8mb4_general_ci;
```

规则如下：

* 规则 1：如果指定了 `CHARACTER SET charset_name` 和 `COLLATE collation_name`，则直接使用 `charset_name` 字符集和 `collation_name` 排序规则。
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

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE` 是可选的，如果没有提供，将会用 `charset_name` 对应的默认排序规则设置 `collation_connection`。

* `SET CHARACTER SET 'charset_name'`

    跟 `SET NAMES` 类似，等价于下面语句的组合：

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection=@@character_set_database;
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

> **注意：**
>
> 跳过字符检查可能会使 TiDB 检测不到应用写入的非法 UTF-8 字符，进一步导致执行 `ANALYZE` 时解码错误，以及引入其他未知的编码问题。如果应用不能保证写入字符串的合法性，不建议跳过该检查。

## 排序规则支持

排序规则的语法支持和语义支持受到配置项 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 的影响。这里语法支持和语义支持有所区别。语法支持是指 TiDB 能够解析和设置排序规则；而语义支持是指 TiDB 能够在比较字符串时正确地使用排序规则。

在 4.0 版本之前，TiDB 只提供了旧的排序规则框架，能够在语法上支持的绝大部分 MySQL 排序规则，但语义上所有的排序规则都当成二进制排序规则。

4.0 版本中，TiDB 增加了新的排序规则框架用于在语义上支持不同的排序规则，保证字符串比较时严格遵循对应的排序规则，详情请见下文。

### 旧框架下的排序规则支持

在 4.0 版本之前，TiDB 中可以指定大部分 MySQL 中的排序规则，并把这些排序规则按照默认排序规则处理，即以编码字节序为字符定序。和 MySQL 不同的是，TiDB 不会处理字符末尾的空格，因此会造成以下的行为区别：

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
```

```
Query OK, 0 rows affected
```

```sql
INSERT INTO t VALUES ('A');
```

```
Query OK, 1 row affected
```

```sql
INSERT INTO t VALUES ('a');
```

```
Query OK, 1 row affected
```

以上语句，在 TiDB 会执行成功，而在 MySQL 中，由于 `utf8mb4_general_ci` 大小写不敏感，报错 `Duplicate entry 'a'`。

```sql
INSERT INTO t VALUES ('a ');
```

```
Query OK, 1 row affected
```

以上语句，在 TiDB 会执行成功，而在 MySQL 中，由于补齐空格比较，报错 `Duplicate entry 'a '`。

### 新框架下的排序规则支持

TiDB 4.0 新增了完整的排序规则支持框架，从语义上支持了排序规则，并新增了配置开关 `new_collations_enabled_on_first_bootstrap`，在集群初次初始化时决定是否启用新排序规则框架。如需启用新排序规则框架，可将 `new_collations_enabled_on_first_bootstrap` 的值设为 `true`，详情参见 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)。

对于一个已经初始化完成的 TiDB 集群，可以通过 `mysql.tidb` 表中的 `new_collation_enabled` 变量确认是否启用了新排序规则框架。

> **注意：**
>
> 当 `mysql.tidb` 表查询结果和 `new_collations_enabled_on_first_bootstrap` 的值不同时，以 `mysql.tidb` 表的结果为准。

```sql
SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME='new_collation_enabled';
```

```
+----------------+
| VARIABLE_VALUE |
+----------------+
| True           |
+----------------+
1 row in set (0.00 sec)
```

在新的排序规则框架下，TiDB 能够支持 `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_unicode_ci`、`utf8mb4_unicode_ci`、`utf8mb4_0900_bin`、`utf8mb4_0900_ai_ci`、`gbk_chinese_ci` 和 `gbk_bin` 这几种排序规则，与 MySQL 兼容。

使用 `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_unicode_ci`、`utf8mb4_unicode_ci`、`utf8mb4_0900_ai_ci` 和 `gbk_chinese_ci` 中任一种时，字符串之间的比较是大小写不敏感 (case-insensitive) 和口音不敏感 (accent-insensitive) 的。同时，TiDB 还修正了排序规则的 `PADDING` 行为：

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO t VALUES ('A');
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
INSERT INTO t VALUES ('a');
```

```
ERROR 1062 (23000): Duplicate entry 'a' for key 't.PRIMARY'
```

TiDB 兼容了 MySQL 的 case insensitive collation。

```sql
INSERT INTO t VALUES ('a ');
```

```
ERROR 1062 (23000): Duplicate entry 'a ' for key 't.PRIMARY'
```

TiDB 修正了 `PADDING` 行为，与 MySQL 兼容。

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

```sql
SELECT 'a' = _utf8mb4 'A' collate utf8mb4_general_ci;
```

```
+-----------------------------------------------+
| 'a' = _utf8mb4 'A' collate utf8mb4_general_ci |
+-----------------------------------------------+
|                                             1 |
+-----------------------------------------------+
1 row in set (0.00 sec)
```

更多细节，参考 [Connection Character Sets and Collations](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html)。
