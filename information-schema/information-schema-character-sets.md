---
title: CHARACTER_SETS
summary: Learn the `CHARACTER_SETS` information_schema table.
---

# CHARACTER_SETS

The `CHARACTER_SETS` table provides information about [character sets](/character-set-and-collation.md). Currently, TiDB only supports some of the character sets.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC character_sets;
```

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

{{< copyable "sql" >}}

```sql
SELECT * FROM `character_sets`;
```

```
+--------------------+----------------------+---------------+--------+
| CHARACTER_SET_NAME | DEFAULT_COLLATE_NAME | DESCRIPTION   | MAXLEN |
+--------------------+----------------------+---------------+--------+
| utf8               | utf8_bin             | UTF-8 Unicode |      3 |
| utf8mb4            | utf8mb4_bin          | UTF-8 Unicode |      4 |
| ascii              | ascii_bin            | US ASCII      |      1 |
| latin1             | latin1_bin           | Latin1        |      1 |
| binary             | binary               | binary        |      1 |
+--------------------+----------------------+---------------+--------+
5 rows in set (0.00 sec)
```

The description of columns in the `CHARACTER_SETS` table is as follows:

* `CHARACTER_SET_NAME`: The name of the character set.
* `DEFAULT_COLLATE_NAME` The default collation name of the character set.
* `DESCRIPTION` The description of the character set.
* `MAXLEN` The maximum length required to store a character in this character set.
