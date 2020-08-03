---
title: COLLATION_CHARACTER_SET_APPLICABILITY
summary: Learn the `COLLATION_CHARACTER_SET_APPLICABILITY` information_schema table.
---

# COLLATION_CHARACTER_SET_APPLICABILITY

The `COLLATION_CHARACTER_SET_APPLICABILITY` table maps collations to the applicable character set name. Similar to the `COLLATIONS` table, it is included only for compatibility with MySQL.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC collation_character_set_applicability;
```

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | NO   |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | NO   |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM collation_character_set_applicability WHERE character_set_name='utf8mb4';
```

```sql
+----------------+--------------------+
| COLLATION_NAME | CHARACTER_SET_NAME |
+----------------+--------------------+
| utf8mb4_bin    | utf8mb4            |
+----------------+--------------------+
1 row in set (0.00 sec)
```

The description of columns in the `COLLATION_CHARACTER_SET_APPLICABILITY` table is as follows:

* `COLLATION_NAME`: The name of the collation.
* `CHARACTER_SET_NAME`: The name of the character set which the collation belongs to.
