---
title: Character Set and Collation
summary: Learn about the supported character sets and collations in TiDB.
aliases: ['/docs/dev/character-set-and-collation/','/docs/dev/reference/sql/characterset-and-collation/','/docs/dev/reference/sql/character-set/']
---

# Character Set and Collation

This document introduces the character sets and collations supported by TiDB.

## Concepts

A character set is a set of symbols and encodings. The default character set in TiDB is utf8mb4, which matches the default in MySQL 8.0 and above.

A collation is a set of rules for comparing characters in a character set, and the sorting order of characters. For example in a binary collation `A` and `a` do not compare as equal:

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

TiDB defaults to using a binary collation. This differs from MySQL, which uses a case-insensitive collation by default.

## Character sets and collations supported by TiDB

Currently, TiDB supports the following character sets:

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
| gbk     | Chinese Internal Code Specification | gbk_bin           |      2 |
| latin1  | Latin1                              | latin1_bin        |      1 |
| utf8    | UTF-8 Unicode                       | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode                       | utf8mb4_bin       |      4 |
+---------+-------------------------------------+-------------------+--------+
6 rows in set (0.00 sec)
```

TiDB supports the following collations:

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
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 |  224 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
11 rows in set (0.00 sec)
```

> **Warning:**
>
> TiDB incorrectly treats latin1 as a subset of utf8. This can lead to unexpected behaviors when you store characters that differ between latin1 and utf8 encodings. It is strongly recommended to the utf8mb4 character set. See [TiDB #18955](https://github.com/pingcap/tidb/issues/18955) for more details.

> **Note:**
>
> The default collations in TiDB (binary collations, with the suffix `_bin`) are different than [the default collations in MySQL](https://dev.mysql.com/doc/refman/8.0/en/charset-charsets.html) (typically general collations, with the suffix `_general_ci`). This can cause incompatible behavior when specifying an explicit character set but relying on the implicit default collation to be chosen.

You can use the following statement to view the collations (under the [new framework for collations](#new-framework-for-collations)) that corresponds to the character set.

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

For details about the TiDB support of the GBK character set, see [GBK](/character-set-gbk.md).

## `utf8` and `utf8mb4` in TiDB

In MySQL, the character set `utf8` is limited to a maximum of three bytes. This is sufficient to store characters in the Basic Multilingual Plane (BMP), but not enough to store characters such as emojis. For this, it is recommended to use the character set `utf8mb4` instead.

By default, TiDB also limits the character set `utf8` to a maximum of three bytes to ensure that data created in TiDB can still safely be restored in MySQL. You can disable it by changing the value of the system variable [`tidb_check_mb4_value_in_utf8`](/system-variables.md#tidb_check_mb4_value_in_utf8) to `OFF`.

The following demonstrates the default behavior when inserting a 4-byte emoji character into a table. The `INSERT` statement fails for the `utf8` character set, but succeeds for `utf8mb4`:

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

## Character set and collation in different layers

The character set and collation can be set at different layers.

### Database character set and collation

Each database has a character set and a collation. You can use the following statements to specify the database character set and collation:

```sql
CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

ALTER DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]
```

`DATABASE` can be replaced with `SCHEMA` here.

Different databases can use different character sets and collations. Use the `character_set_database` and `collation_database` to see the character set and collation of the current database:

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

You can also see the two values in `INFORMATION_SCHEMA`:

{{< copyable "sql" >}}

```sql
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```

### Table character set and collation

You can use the following statement to specify the character set and collation for tables:

```sql
CREATE TABLE tbl_name (column_list)
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]]

ALTER TABLE tbl_name
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]
```

For example:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1(a int) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

If the table character set and collation are not specified, the database character set and collation are used as their default values.

### Column character set and collation

You can use the following statement to specify the character set and collation for columns:

```sql
col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]
```

If the column character set and collation are not specified, the table character set and collation are used as their default values.

### String character sets and collation

Each string corresponds to a character set and a collation. When you use a string, this option is available:

{{< copyable "sql" >}}

```sql
[_charset_name]'string' [COLLATE collation_name]
```

Example:

{{< copyable "sql" >}}

```sql
SELECT 'string';
SELECT _utf8mb4'string';
SELECT _utf8mb4'string' COLLATE utf8mb4_general_ci;
```

Rules:

+ Rule 1: If you specify `CHARACTER SET charset_name` and `COLLATE collation_name`, then the `charset_name` character set and the `collation_name` collation are used directly.
+ Rule 2: If you specify `CHARACTER SET charset_name` but do not specify `COLLATE collation_name`, the `charset_name` character set and the default collation of `charset_name` are used.
+ Rule 3: If you specify neither `CHARACTER SET charset_name` nor `COLLATE collation_name`, the character set and collation given by the system variables `character_set_connection` and `collation_connection` are used.

### Client connection character set and collation

+ The server character set and collation are the values of the `character_set_server` and `collation_server` system variables.

+ The character set and collation of the default database are the values of the `character_set_database` and `collation_database` system variables.

You can use `character_set_connection` and `collation_connection` to specify the character set and collation for each connection. The `character_set_client` variable is to set the client character set.

Before returning the result, the `character_set_results` system variable indicates the character set in which the server returns query results to the client, including the metadata of the result.

You can use the following statement to set the character set and collation that is related to the client:

+ `SET NAMES 'charset_name' [COLLATE 'collation_name']`

    `SET NAMES` indicates what character set the client will use to send SQL statements to the server. `SET NAMES utf8mb4` indicates that all the requests from the client use utf8mb4, as well as the results from the server.

    The `SET NAMES 'charset_name'` statement is equivalent to the following statement combination:

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE` is optional, if absent, the default collation of the `charset_name` is used to set the `collation_connection`.

+ `SET CHARACTER SET 'charset_name'`

    Similar to `SET NAMES`, the `SET NAMES 'charset_name'` statement is equivalent to the following statement combination:

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET charset_connection = @@charset_database;
    SET collation_connection = @@collation_database;
    ```

## Selection priorities of character sets and collations

String > Column > Table > Database > Server

## General rules on selecting character sets and collation

+ Rule 1: If you specify `CHARACTER SET charset_name` and `COLLATE collation_name`, then the `charset_name` character set and the `collation_name` collation are used directly.
+ Rule 2: If you specify `CHARACTER SET charset_name` and do not specify `COLLATE collation_name`, then the `charset_name` character set and the default collation of `charset_name` are used.
+ Rule 3: If you specify neither `CHARACTER SET charset_name` nor `COLLATE collation_name`, the character set and collation with higher optimization levels are used.

## Validity check of characters

If the specified character set is `utf8` or `utf8mb4`, TiDB only supports the valid `utf8` characters. For invalid characters, TiDB reports the `incorrect utf8 value` error. This validity check of characters in TiDB is compatible with MySQL 8.0 but incompatible with MySQL 5.7 or earlier versions.

To disable this error reporting, use `set @@tidb_skip_utf8_check=1;` to skip the character check.

> **Note:**
>
> If the character check is skipped, TiDB might fail to detect illegal UTF-8 characters written by the application, cause decoding errors when `ANALYZE` is executed, and introduce other unknown encoding issues. If your application cannot guarantee the validity of the written string, it is not recommended to skip the character check.

## Collation support framework

<CustomContent platform="tidb">

The syntax support and semantic support for the collation are influenced by the [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) configuration item. The syntax support and semantic support are different. The former indicates that TiDB can parse and set collations. The latter indicates that TiDB can correctly use collations when comparing strings.

</CustomContent>

Before v4.0, TiDB provides only the [old framework for collations](#old-framework-for-collations). In this framework, TiDB supports syntactically parsing most of the MySQL collations but semantically takes all collations as binary collations.

Since v4.0, TiDB supports a [new framework for collations](#new-framework-for-collations). In this framework, TiDB semantically parses different collations and strictly follows the collations when comparing strings.

### Old framework for collations

Before v4.0, you can specify most of the MySQL collations in TiDB, and these collations are processed according to the default collations, which means that the byte order determines the character order. Different from MySQL, TiDB does not handle the trailing spaces of a character, which causes the following behavior differences:

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

In TiDB, the preceding statement is successfully executed. In MySQL, because `utf8mb4_general_ci` is case-insensitive, the `Duplicate entry 'a'` error is reported.

```sql
INSERT INTO t1 VALUES ('a ');
```

```sql
Query OK, 1 row affected
```

In TiDB, the preceding statement is successfully executed. In MySQL, because comparison is performed after the spaces are filled in, the `Duplicate entry 'a '` error is returned.

### New framework for collations

Since TiDB v4.0, a complete framework for collations is introduced.

<CustomContent platform="tidb">

This new framework supports semantically parsing collations and introduces the `new_collations_enabled_on_first_bootstrap` configuration item to decide whether to enable the new framework when a cluster is first initialized. To enable the new framework, set `new_collations_enabled_on_first_bootstrap` to `true`. For details, see [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap). If you initialize the cluster after the configuration item is enabled, you can check whether the new collation is enabled through the `new_collation_enabled` variable in the `mysql`.`tidb` table:

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

</CustomContent>

<CustomContent platform="tidb-cloud">

This new framework supports semantically parsing collations. TiDB enables the new framework by default when a cluster is first initialized.

</CustomContent>

Under the new framework, TiDB supports the `utf8_general_ci`, `utf8mb4_general_ci`, `utf8_unicode_ci`, `utf8mb4_unicode_ci`, `gbk_chinese_ci`, and `gbk_bin` collations, which is compatible with MySQL.

When one of `utf8_general_ci`, `utf8mb4_general_ci`, `utf8_unicode_ci`, `utf8mb4_unicode_ci`, and `gbk_chinese_ci` is used, the string comparison is case-insensitive and accent-insensitive. At the same time, TiDB also corrects the collation's `PADDING` behavior:

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
ERROR 1062 (23000): Duplicate entry 'a' for key 't.PRIMARY' # TiDB is compatible with the case-insensitive collation of MySQL.
```

```sql
INSERT INTO t VALUES ('a ');
```

```sql
ERROR 1062 (23000): Duplicate entry 'a ' for key 't.PRIMARY' # TiDB modifies the `PADDING` behavior to be compatible with MySQL.
```

> **Note:**
>
> The implementation of padding in TiDB is different from that in MySQL. In MySQL, padding is implemented by filling in spaces. In TiDB, padding is implemented by cutting out the spaces at the end. The two approaches are the same in most cases. The only exception is when the end of the string contains characters that are less than spaces (0x20). For example, the result of `'a' < 'a\t'` in TiDB is `1`, but in MySQL, `'a' < 'a\t'` is equivalent to `'a ' < 'a\t'`, and the result is `0`.

## Coercibility values of collations in expressions

If an expression involves multiple clauses of different collations, you need to infer the collation used in the calculation. The rules are as follows:

+ The coercibility value of the explicit `COLLATE` clause is `0`.
+ If the collations of two strings are incompatible, the coercibility value of the concatenation of two strings with different collations is `1`.
+ The collation of the column, `CAST()`, `CONVERT()`, or `BINARY()` has a coercibility value of `2`.
+ The system constant (the string returned by `USER ()` or `VERSION ()`) has a coercibility value of `3`.
+ The coercibility value of constants is `4`.
+ The coercibility value of numbers or intermediate variables is `5`.
+ `NULL` or expressions derived from `NULL` has a coercibility value of `6`.

When inferring collations, TiDB prefers using the collation of expressions with lower coercibility values. If the coercibility values of two clauses are the same, the collation is determined according to the following priority:

binary > utf8mb4_bin > (utf8mb4_general_ci = utf8mb4_unicode_ci) > utf8_bin > (utf8_general_ci = utf8_unicode_ci) > latin1_bin > ascii_bin

TiDB cannot infer the collation and reports an error in the following situations:

- If the collations of two clauses are different and the coercibility value of both clauses is `0`.
- If the collations of two clauses are incompatible and the returned type of expression is `String`.

## `COLLATE` clause

TiDB supports using the `COLLATE` clause to specify the collation of an expression. The coercibility value of this expression is `0`, which has the highest priority. See the following example:

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

For more details, see [Connection Character Sets and Collations](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html).
