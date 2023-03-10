---
title: CHARACTER_SETS
summary: Learn the `CHARACTER_SETS` INFORMATION_SCHEMA table.
---

# CHARACTER_SETS

The `CHARACTER_SETS` table provides information about [character sets](/character-set-and-collation.md). Currently, TiDB only supports some of the character sets.

```sql
USE INFORMATION_SCHEMA;
DESC CHARACTER_SETS;
```

The output is as follows:

```
+----------------------+-------------+------+------+---------+-------+
| Field                | Type        | Null | Key  | Default | Extra |
+----------------------+-------------+------+------+---------+-------+
| CHARACTER_SET_NAME   | varchar(32) | YES  |      | NULL    |       |
| DEFAULT_COLLATE_NAME | varchar(32) | YES  |      | NULL    |       |
| DESCRIPTION          | varchar(60) | YES  |      | NULL    |       |
| MAXLEN               | bigint(3)   | YES  |      | NULL    |       |
+----------------------+-------------+------+------+---------+-------+
4 rows in set (0.00 sec)
```

View the `CHARACTER_SETS` table:

```sql
SELECT * FROM `CHARACTER_SETS`;
```

The output is as follows:

```sql
+--------------------+----------------------+-------------------------------------+--------+
| CHARACTER_SET_NAME | DEFAULT_COLLATE_NAME | DESCRIPTION                         | MAXLEN |
+--------------------+----------------------+-------------------------------------+--------+
| ascii              | ascii_bin            | US ASCII                            |      1 |
| binary             | binary               | binary                              |      1 |
| gbk                | gbk_chinese_ci       | Chinese Internal Code Specification |      2 |
| latin1             | latin1_bin           | Latin1                              |      1 |
| utf8               | utf8_bin             | UTF-8 Unicode                       |      3 |
| utf8mb4            | utf8mb4_bin          | UTF-8 Unicode                       |      4 |
+--------------------+----------------------+-------------------------------------+--------+
6 rows in set (0.00 sec)
```

The description of columns in the `CHARACTER_SETS` table is as follows:

* `CHARACTER_SET_NAME`: The name of the character set.
* `DEFAULT_COLLATE_NAME` The default collation name of the character set.
* `DESCRIPTION` The description of the character set.
* `MAXLEN` The maximum length required to store a character in this character set.
