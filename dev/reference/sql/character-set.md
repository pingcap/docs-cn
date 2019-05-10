---
title: Character Set Support
summary: Learn about the supported character sets in TiDB.
category: reference
aliases: ['/docs/sql/character-set-support/','/docs/sql/character-set-configuration/']
---

# Character Set Support

A character set is a set of symbols and encodings. A collation is a set of rules for comparing characters in a character set.

Currently, TiDB supports the following character sets:

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

> **Note:**
>
> In TiDB, utf8 is treated as utf8mb4.

Each character set has at least one collation. Most of the character sets have several collations. You can use the following statement to display the available character sets:

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

The `latin1` collations have the following meanings:

| Collation           | Meaning                                             |
|:--------------------|:----------------------------------------------------|
| `latin1_bin`        | Binary according to `latin1` encoding               |
| `latin1_danish_ci`  | Danish/Norwegian                                    |
| `latin1_general_ci` | Multilingual (Western European)                     |
| `latin1_general_cs` | Multilingual (ISO Western European), case sensitive |
| `latin1_german1_ci` | German DIN-1 (dictionary order)                     |
| `latin1_german2_ci` | German DIN-2 (phone book order)                     |
| `latin1_spanish_ci` | Modern Spanish                                      |
| `latin1_swedish_ci` | Swedish/Finnish                                     |

Each character set has a default collation. For example, the default collation for utf8 is `utf8_bin`.

> **Note:**
>
> The collations in TiDB are case sensitive.

## Collation naming conventions

The collation names in TiDB follow these conventions:

- The prefix of a collation is its corresponding character set, generally followed by one or more suffixes indicating other collation characteristic.  For example, `utf8_general_ci` and `latin1_swedish_ci` are collations for the utf8 and latin1 character sets, respectively. The `binary` character set has a single collation, also named `binary`, with no suffixes.
- A language-specific collation includes a language name. For example, `utf8_turkish_ci` and `utf8_hungarian_ci` sort characters for the utf8 character set using the rules of Turkish and Hungarian, respectively.
- Collation suffixes indicate whether a collation is case and accent sensitive, or binary. The following table shows the suffixes used to indicate these characteristics.

    | Suffix | Meaning            |
    |:-------|:-------------------|
    | \_ai   | Accent insensitive |
    | \_as   | Accent sensitive   |
    | \_ci   | Case insensitive   |
    | \_cs   | Case sensitive     |
    | \_bin  | Binary             |

> **Note:**
>
> Currently, TiDB only supports some of the collations in the above table.

## Database character set and collation

Each database has a character set and a collation. You can use the `CREATE DATABASE` statement to specify the database character set and collation:

```sql
CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]
```
Where `DATABASE` can be replaced with `SCHEMA`.

Different databases can use different character sets and collations. Use the `character_set_database` and  `collation_database` to see the character set and collation of the current database:

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

You can also see the two values in INFORMATION_SCHEMA:

```sql
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```

## Table character set and collation

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

```sql
mysql> CREATE TABLE t1(a int) CHARACTER SET utf8 COLLATE utf8_general_ci;
Query OK, 0 rows affected (0.08 sec)
```
The table character set and collation are used as the default values for column definitions if the column character set and collation are not specified in individual column definitions.

## Column character set and collation

See the following table for the character set and collation syntax for columns:

```sql
col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]
```

## Connection character sets and collations

- The server character set and collation are the values of the `character_set_server` and `collation_server` system variables.

- The character set and collation of the default database are the values of the `character_set_database` and `collation_database` system variables.
    You can use `character_set_connection` and `collation_connection` to specify the character set and collation for each connection.
    The `character_set_client` variable is to set the client character set. Before returning the result, the `character_set_results` system variable indicates the character set in which the server returns query results to the client, including the metadata of the result.

You can use the following statement to specify a particular collation that is related to the client:

- `SET NAMES 'charset_name' [COLLATE 'collation_name']`

    `SET NAMES` indicates what character set the client will use to send SQL statements to the server. `SET NAMES utf8` indicates that all the requests from the client use utf8, as well as the results from the server.

    The `SET NAMES 'charset_name'` statement is equivalent to the following statement combination:

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE` is optional, if absent, the default collation of the `charset_name` is used.

- `SET CHARACTER SET 'charset_name'`

    Similar to `SET NAMES`, the `SET NAMES 'charset_name'` statement is equivalent to the following statement combination:

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET collation_connection = @@collation_database;
    ```

For more information, see [Connection Character Sets and Collations in MySQL](https://dev.mysql.com/doc/refman/5.7/en/charset-connection.html).
