---
title: 字符集和排序规则
summary: 了解 TiDB 支持的字符集和排序规则。
---

# 字符集和排序规则

本文介绍 TiDB 支持的字符集和排序规则。

## 概念

字符集是一组符号和编码的集合。TiDB 的默认字符集是 `utf8mb4`，这与 MySQL 8.0 及更高版本的默认字符集相匹配。

排序规则是一组用于比较字符集中字符的规则，以及字符的排序顺序。例如在二进制排序规则中，`A` 和 `a` 不会被视为相等：

{{< copyable "sql" >}}

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_bin;
SELECT 'A' = 'a';
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
SELECT 'A' = 'a';
```

```sql
SELECT 'A' = 'a';
```

```sql
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

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT 'A' = 'a';
```

```sql
+-----------+
| 'A' = 'a' |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
```

## TiDB 支持的字符集和排序规则

目前，TiDB 支持以下字符集：

{{< copyable "sql" >}}

```sql
SHOW CHARACTER SET;
```

```sql
+---------+-------------------------------------+-------------------+--------+
| Charset | Description                         | Default collation | Maxlen |
+---------+-------------------------------------+-------------------+--------+
| ascii   | US ASCII                            | ascii_bin         |      1 |
| binary  | binary                              | binary            |      1 |
| gbk     | Chinese Internal Code Specification | gbk_chinese_ci    |      2 |
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

```sql
+--------------------+---------+------+---------+----------+---------+
| Collation          | Charset | Id   | Default | Compiled | Sortlen |
+--------------------+---------+------+---------+----------+---------+
| ascii_bin          | ascii   |   65 | Yes     | Yes      |       1 |
| binary             | binary  |   63 | Yes     | Yes      |       1 |
| gbk_bin            | gbk     |   87 |         | Yes      |       1 |
| gbk_chinese_ci     | gbk     |   28 | Yes     | Yes      |       1 |
| latin1_bin         | latin1  |   47 | Yes     | Yes      |       1 |
| utf8_bin           | utf8    |   83 | Yes     | Yes      |       1 |
| utf8_general_ci    | utf8    |   33 |         | Yes      |       1 |
| utf8_unicode_ci    | utf8    |  192 |         | Yes      |       1 |
| utf8mb4_0900_ai_ci | utf8mb4 |  255 |         | Yes      |       1 |
| utf8mb4_0900_bin   | utf8mb4 |  309 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 |  224 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
13 rows in set (0.00 sec)
```

> **警告：**
>
> TiDB 错误地将 latin1 视为 utf8 的子集。当存储 latin1 和 utf8 编码不同的字符时，这可能会导致意外行为。强烈建议使用 utf8mb4 字符集。更多详情请参见 [TiDB #18955](https://github.com/pingcap/tidb/issues/18955)。

> **注意：**
>
> TiDB 中的默认排序规则（带有 `_bin` 后缀的二进制排序规则）与 [MySQL 中的默认排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-charsets.html)（通常是带有 `_general_ci` 或 `_ai_ci` 后缀的通用排序规则）不同。当指定显式字符集但依赖隐式默认排序规则时，这可能会导致不兼容的行为。
>
> 然而，TiDB 中的默认排序规则也会受到客户端[连接排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)设置的影响。例如，MySQL 8.x 客户端默认将 `utf8mb4_0900_ai_ci` 作为 `utf8mb4` 字符集的连接排序规则。
>
> - 在 TiDB v7.4.0 之前，如果客户端使用 `utf8mb4_0900_ai_ci` 作为[连接排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)，由于 TiDB 不支持 `utf8mb4_0900_ai_ci` 排序规则，TiDB 会回退使用 TiDB 服务器默认排序规则 `utf8mb4_bin`。
> - 从 v7.4.0 开始，如果客户端使用 `utf8mb4_0900_ai_ci` 作为[连接排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)，TiDB 会遵循客户端的配置使用 `utf8mb4_0900_ai_ci` 作为默认排序规则。
你可以使用以下语句查看对应字符集的排序规则（在[新的排序规则框架](#新的排序规则框架)下）：

{{< copyable "sql" >}}

```sql
SHOW COLLATION WHERE Charset = 'utf8mb4';
```

```sql
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

关于 TiDB 对 GBK 字符集的支持详情，请参见 [GBK](/character-set-gbk.md)。

## TiDB 中的 `utf8` 和 `utf8mb4`

在 MySQL 中，字符集 `utf8` 最多只能存储三个字节。这足以存储基本多语言平面（BMP）中的字符，但不足以存储表情符号等字符。为此，建议使用字符集 `utf8mb4`。

默认情况下，TiDB 也将字符集 `utf8` 限制为最多三个字节，以确保在 TiDB 中创建的数据仍然可以安全地在 MySQL 中恢复。你可以通过将系统变量 [`tidb_check_mb4_value_in_utf8`](/system-variables.md#tidb_check_mb4_value_in_utf8) 的值更改为 `OFF` 来禁用此限制。

以下示例演示了在将 4 字节表情符号字符插入表时的默认行为。对于 `utf8` 字符集，`INSERT` 语句失败，但对于 `utf8mb4` 则成功：

```sql
CREATE TABLE utf8_test (
     c char(1) NOT NULL
    ) CHARACTER SET utf8;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

```sql
CREATE TABLE utf8m4_test (
     c char(1) NOT NULL
    ) CHARACTER SET utf8mb4;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

```sql
INSERT INTO utf8_test VALUES ('😉');
```

```sql
ERROR 1366 (HY000): incorrect utf8 value f09f9889(😉) for column c
```

```sql
INSERT INTO utf8m4_test VALUES ('😉');
```

```sql
Query OK, 1 row affected (0.02 sec)
```

```sql
SELECT char_length(c), length(c), c FROM utf8_test;
```

```sql
Empty set (0.01 sec)
```

```sql
SELECT char_length(c), length(c), c FROM utf8m4_test;
```

```sql
+----------------+-----------+------+
| char_length(c) | length(c) | c    |
+----------------+-----------+------+
|              1 |         4 | 😉     |
+----------------+-----------+------+
1 row in set (0.00 sec)
```
## 不同层次的字符集和排序规则

字符集和排序规则可以在不同层次设置。

### 数据库字符集和排序规则

每个数据库都有一个字符集和一个排序规则。你可以使用以下语句指定数据库字符集和排序规则：

```sql
CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

ALTER DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]
```

这里的 `DATABASE` 可以替换为 `SCHEMA`。

不同的数据库可以使用不同的字符集和排序规则。使用 `character_set_database` 和 `collation_database` 可以查看当前数据库的字符集和排序规则：

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

你也可以在 `INFORMATION_SCHEMA` 中查看这两个值：

{{< copyable "sql" >}}

```sql
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```
### 表字符集和排序规则

你可以使用以下语句指定表的字符集和排序规则：

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

如果未指定表字符集和排序规则，则使用数据库字符集和排序规则作为其默认值。如果你只指定字符集为 `utf8mb4` 而不指定排序规则，则排序规则由系统变量 [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-new-in-v740) 的值决定。

### 列字符集和排序规则

你可以使用以下语句指定列的字符集和排序规则：

```sql
col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]
```

如果未指定列字符集和排序规则，则使用表字符集和排序规则作为其默认值。如果你只指定字符集为 `utf8mb4` 而不指定排序规则，则排序规则由系统变量 [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-new-in-v740) 的值决定。

### 字符串字符集和排序规则

每个字符串对应一个字符集和一个排序规则。当你使用字符串时，可以使用以下选项：

{{< copyable "sql" >}}

```sql
[_charset_name]'string' [COLLATE collation_name]
```

示例：

{{< copyable "sql" >}}

```sql
SELECT 'string';
SELECT _utf8mb4'string';
SELECT _utf8mb4'string' COLLATE utf8mb4_general_ci;
```

规则：

+ 规则 1：如果指定了 `CHARACTER SET charset_name` 和 `COLLATE collation_name`，则直接使用 `charset_name` 字符集和 `collation_name` 排序规则。
+ 规则 2：如果指定了 `CHARACTER SET charset_name` 但未指定 `COLLATE collation_name`，则使用 `charset_name` 字符集及其默认排序规则。
+ 规则 3：如果既未指定 `CHARACTER SET charset_name` 也未指定 `COLLATE collation_name`，则使用由系统变量 `character_set_connection` 和 `collation_connection` 给出的字符集和排序规则。
### 客户端连接字符集和排序规则

+ 服务器字符集和排序规则是 `character_set_server` 和 `collation_server` 系统变量的值。

+ 默认数据库的字符集和排序规则是 `character_set_database` 和 `collation_database` 系统变量的值。

你可以使用 `character_set_connection` 和 `collation_connection` 为每个连接指定字符集和排序规则。`character_set_client` 变量用于设置客户端字符集。

在返回结果之前，`character_set_results` 系统变量指示服务器向客户端返回查询结果的字符集，包括结果的元数据。

你可以使用以下语句设置与客户端相关的字符集和排序规则：

+ `SET NAMES 'charset_name' [COLLATE 'collation_name']`

    `SET NAMES` 表示客户端将使用什么字符集向服务器发送 SQL 语句。`SET NAMES utf8mb4` 表示客户端的所有请求都使用 utf8mb4，服务器的结果也是如此。

    `SET NAMES 'charset_name'` 语句等同于以下语句组合：

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE` 是可选的，如果不存在，则使用 `charset_name` 的默认排序规则来设置 `collation_connection`。

+ `SET CHARACTER SET 'charset_name'`

    类似于 `SET NAMES`，`SET NAMES 'charset_name'` 语句等同于以下语句组合：

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection=@@character_set_database;
    SET collation_connection = @@collation_database;
    ```

## 字符集和排序规则的选择优先级

字符串 > 列 > 表 > 数据库 > 服务器

## 选择字符集和排序规则的一般规则

+ 规则 1：如果指定了 `CHARACTER SET charset_name` 和 `COLLATE collation_name`，则直接使用 `charset_name` 字符集和 `collation_name` 排序规则。
+ 规则 2：如果指定了 `CHARACTER SET charset_name` 但未指定 `COLLATE collation_name`，则使用 `charset_name` 字符集及其默认排序规则。
+ 规则 3：如果既未指定 `CHARACTER SET charset_name` 也未指定 `COLLATE collation_name`，则使用优化级别更高的字符集和排序规则。

## 字符有效性检查

如果指定的字符集是 `utf8` 或 `utf8mb4`，TiDB 仅支持有效的 `utf8` 字符。对于无效字符，TiDB 会报告 `incorrect utf8 value` 错误。TiDB 中的这种字符有效性检查与 MySQL 8.0 兼容，但与 MySQL 5.7 或更早版本不兼容。

要禁用此错误报告，请使用 `set @@tidb_skip_utf8_check=1;` 跳过字符检查。

> **注意：**
>
> 如果跳过字符检查，TiDB 可能无法检测到应用程序写入的非法 UTF-8 字符，在执行 `ANALYZE` 时可能会导致解码错误，并引入其他未知的编码问题。如果你的应用程序无法保证写入字符串的有效性，不建议跳过字符检查。
## 排序规则支持框架

<CustomContent platform="tidb">

排序规则的语法支持和语义支持受 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 配置项的影响。语法支持和语义支持是不同的。前者表示 TiDB 可以解析和设置排序规则。后者表示 TiDB 可以在比较字符串时正确使用排序规则。

</CustomContent>

<CustomContent platform="tidb-cloud">

排序规则的语法支持和语义支持是不同的。前者表示 TiDB 可以解析和设置排序规则。后者表示 TiDB 可以在比较字符串时正确使用排序规则。

</CustomContent>

在 v4.0 之前，TiDB 仅提供[旧的排序规则框架](#旧的排序规则框架)。在这个框架中，TiDB 支持语法解析大多数 MySQL 排序规则，但在语义上将所有排序规则视为二进制排序规则。

从 v4.0 开始，TiDB 支持[新的排序规则框架](#新的排序规则框架)。在这个框架中，TiDB 语义解析不同的排序规则，并在比较字符串时严格遵循排序规则。

### 旧的排序规则框架

在 v4.0 之前，你可以在 TiDB 中指定大多数 MySQL 排序规则，这些排序规则按照默认排序规则处理，这意味着字节顺序决定字符顺序。与 MySQL 不同，TiDB 不处理字符的尾随空格，这导致以下行为差异：

{{< copyable "sql" >}}

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
```

```sql
Query OK, 0 rows affected
```

```sql
INSERT INTO t VALUES ('A');
```

```sql
Query OK, 1 row affected
```

```sql
INSERT INTO t VALUES ('a');
```

```sql
Query OK, 1 row affected
```

在 TiDB 中，上述语句成功执行。在 MySQL 中，由于 `utf8mb4_general_ci` 不区分大小写，会报告 `Duplicate entry 'a'` 错误。

```sql
INSERT INTO t1 VALUES ('a ');
```

```sql
Query OK, 1 row affected
```

在 TiDB 中，上述语句成功执行。在 MySQL 中，由于在填充空格后进行比较，会返回 `Duplicate entry 'a '` 错误。

### 新的排序规则框架

从 TiDB v4.0 开始，引入了一个完整的排序规则框架。

<CustomContent platform="tidb">

这个新框架支持语义解析排序规则，并引入了 `new_collations_enabled_on_first_bootstrap` 配置项来决定在集群首次初始化时是否启用新框架。要启用新框架，请将 `new_collations_enabled_on_first_bootstrap` 设置为 `true`。详情请参见 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)。

对于已经初始化的 TiDB 集群，你可以通过 `mysql.tidb` 表中的 `new_collation_enabled` 变量检查新排序规则是否启用：

> **注意：**
>
> 如果 `mysql.tidb` 表的查询结果与 `new_collations_enabled_on_first_bootstrap` 的值不同，则 `mysql.tidb` 表的结果为实际值。

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

</CustomContent>

<CustomContent platform="tidb-cloud">

这个新框架支持语义解析排序规则。TiDB 在集群首次初始化时默认启用新框架。

</CustomContent>

在新框架下，TiDB 支持 `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_unicode_ci`、`utf8mb4_unicode_ci`、`utf8mb4_0900_bin`、`utf8mb4_0900_ai_ci`、`gbk_chinese_ci` 和 `gbk_bin` 排序规则，这与 MySQL 兼容。

当使用 `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_unicode_ci`、`utf8mb4_unicode_ci`、`utf8mb4_0900_ai_ci` 和 `gbk_chinese_ci` 其中之一时，字符串比较不区分大小写和重音。同时，TiDB 还纠正了排序规则的 `PADDING` 行为：

{{< copyable "sql" >}}

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO t VALUES ('A');
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
INSERT INTO t VALUES ('a');
```

```sql
ERROR 1062 (23000): Duplicate entry 'a' for key 't.PRIMARY' -- TiDB 与 MySQL 的不区分大小写排序规则兼容。
```

```sql
INSERT INTO t VALUES ('a ');
```

```sql
ERROR 1062 (23000): Duplicate entry 'a ' for key 't.PRIMARY' -- TiDB 修改了 `PADDING` 行为以与 MySQL 兼容。
```

> **注意：**
>
> TiDB 中的填充实现与 MySQL 不同。在 MySQL 中，填充是通过填充空格实现的。在 TiDB 中，填充是通过切掉末尾的空格实现的。这两种方法在大多数情况下是相同的。唯一的例外是当字符串末尾包含小于空格 (0x20) 的字符时。例如，在 TiDB 中 `'a' < 'a\t'` 的结果是 `1`，但在 MySQL 中，`'a' < 'a\t'` 等同于 `'a ' < 'a\t'`，结果是 `0`。
## 表达式中排序规则的强制性值

如果一个表达式涉及多个具有不同排序规则的子句，你需要推断计算中使用的排序规则。规则如下：

+ 显式 `COLLATE` 子句的强制性值为 `0`。
+ 如果两个字符串的排序规则不兼容，则具有不同排序规则的两个字符串的连接的强制性值为 `1`。
+ 列、`CAST()`、`CONVERT()` 或 `BINARY()` 的排序规则的强制性值为 `2`。
+ 系统常量（由 `USER()` 或 `VERSION()` 返回的字符串）的强制性值为 `3`。
+ 常量的强制性值为 `4`。
+ 数字或中间变量的强制性值为 `5`。
+ `NULL` 或从 `NULL` 派生的表达式的强制性值为 `6`。

在推断排序规则时，TiDB 倾向于使用强制性值较低的表达式的排序规则。如果两个子句的强制性值相同，则根据以下优先级确定排序规则：

binary > utf8mb4_bin > (utf8mb4_general_ci = utf8mb4_unicode_ci) > utf8_bin > (utf8_general_ci = utf8_unicode_ci) > latin1_bin > ascii_bin

在以下情况下，TiDB 无法推断排序规则并报错：

- 如果两个子句的排序规则不同且两个子句的强制性值都为 `0`。
- 如果两个子句的排序规则不兼容且表达式的返回类型为 `String`。

## `COLLATE` 子句

TiDB 支持使用 `COLLATE` 子句指定表达式的排序规则。此表达式的强制性值为 `0`，具有最高优先级。请看以下示例：

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

更多详情，请参见[连接字符集和排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html)。
