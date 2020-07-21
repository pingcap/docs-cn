---
title: COLLATIONS
summary: Learn the `COLLATIONS` information_schema table.
---

# COLLATIONS

The `COLLATIONS` table provides a list of collations that correspond to character sets in the `CHARACTER_SETS` table. Currently, this table is included only for compatibility with MySQL.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC collations;
```

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | YES  |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | YES  |      | NULL    |       |
| ID                 | bigint(11)  | YES  |      | NULL    |       |
| IS_DEFAULT         | varchar(3)  | YES  |      | NULL    |       |
| IS_COMPILED        | varchar(3)  | YES  |      | NULL    |       |
| SORTLEN            | bigint(3)   | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM collations WHERE character_set_name='utf8mb4';
```

```
+----------------+--------------------+------+------------+-------------+---------+
| COLLATION_NAME | CHARACTER_SET_NAME | ID   | IS_DEFAULT | IS_COMPILED | SORTLEN |
+----------------+--------------------+------+------------+-------------+---------+
| utf8mb4_bin    | utf8mb4            |   46 | Yes        | Yes         |       1 |
+----------------+--------------------+------+------------+-------------+---------+
1 row in set (0.00 sec)
```
