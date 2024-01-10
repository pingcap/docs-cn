---
title: KEYWORDS
summary: Learn the `KEYWORDS` INFORMATION_SCHEMA table.
---

# KEYWORDS

Starting from v7.6.0, TiDB provides the `KEYWORDS` table. You can use this table to get information about [keywords](/keywords.md) in TiDB.

```sql
USE INFORMATION_SCHEMA;
DESC keywords;
```

The output is as follows:

```
+----------+--------------+------+------+---------+-------+
| Field    | Type         | Null | Key  | Default | Extra |
+----------+--------------+------+------+---------+-------+
| WORD     | varchar(128) | YES  |      | NULL    |       |
| RESERVED | int(11)      | YES  |      | NULL    |       |
+----------+--------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

Field description:

- `WORD`: The keyword.
- `RESERVED`: Whether the keyword is reserved.

The following statement queries the information about `ADD` and `USER` keywords:

```sql
SELECT * FROM INFORMATION_SCHEMA.KEYWORDS WHERE WORD IN ('ADD','USER');
```

From the output, you can see that `ADD` is a reserved keyword and `USER` is a non-reserved keyword.

```
+------+----------+
| WORD | RESERVED |
+------+----------+
| ADD  |        1 |
| USER |        0 |
+------+----------+
2 rows in set (0.00 sec)
```
