---
title: COLLATION_CHARACTER_SET_APPLICABILITY
summary: Learn the `COLLATION_CHARACTER_SET_APPLICABILITY` INFORMATION_SCHEMA table.
---

# COLLATION_CHARACTER_SET_APPLICABILITY

The `COLLATION_CHARACTER_SET_APPLICABILITY` table maps collations to the applicable character set name. Similar to the `COLLATIONS` table, it is included only for compatibility with MySQL.

```sql
USE INFORMATION_SCHEMA;
DESC COLLATION_CHARACTER_SET_APPLICABILITY;
```

The output is as follows:

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | NO   |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | NO   |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

View the collation mapping for the `utf8mb4` character set in the `COLLATION_CHARACTER_SET_APPLICABILITY` table:

```sql
SELECT * FROM COLLATION_CHARACTER_SET_APPLICABILITY WHERE character_set_name='utf8mb4';
```

The output is as follows:

```sql
+--------------------+--------------------+
| COLLATION_NAME     | CHARACTER_SET_NAME |
+--------------------+--------------------+
| utf8mb4_bin        | utf8mb4            |
| utf8mb4_general_ci | utf8mb4            |
| utf8mb4_unicode_ci | utf8mb4            |
+--------------------+--------------------+
3 rows in set (0.00 sec)
```

The description of columns in the `COLLATION_CHARACTER_SET_APPLICABILITY` table is as follows:

* `COLLATION_NAME`: The name of the collation.
* `CHARACTER_SET_NAME`: The name of the character set which the collation belongs to.
