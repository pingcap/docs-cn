---
title: CHECK_CONSTRAINTS
summary: Learn the `CHECK_CONSTRAINTS` INFORMATION_SCHEMA table.
---

# CHECK\_CONSTRAINTS

The `CHECK_CONSTRAINTS` table provides information about [`CHECK` constraints](/constraints.md#check) on tables.

```sql
USE INFORMATION_SCHEMA;
DESC CHECK_CONSTRAINTS;
```

The output is as follows:

```sql
+--------------------+-------------+------+-----+---------+-------+
| Field              | Type        | Null | Key | Default | Extra |
+--------------------+-------------+------+-----+---------+-------+
| CONSTRAINT_CATALOG | varchar(64) | NO   |     | NULL    |       |
| CONSTRAINT_SCHEMA  | varchar(64) | NO   |     | NULL    |       |
| CONSTRAINT_NAME    | varchar(64) | NO   |     | NULL    |       |
| CHECK_CLAUSE       | longtext    | NO   |     | NULL    |       |
+--------------------+-------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```

The following example adds a `CHECK` constraint using the `CREATE TABLE` statement:

```sql
CREATE TABLE test.t1 (id INT PRIMARY KEY, CHECK (id%2 = 0));
SELECT * FROM CHECK_CONSTRAINTS\G
```

The output is as follows:

```sql
*************************** 1. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: test
   CONSTRAINT_NAME: t1_chk_1
      CHECK_CLAUSE: (`id` % 2 = 0)
1 row in set (0.00 sec)
```

Fields in the `CHECK_CONSTRAINTS` table are described as follows:

* `CONSTRAINT_CATALOG`: The catalog of the constraint, which is always `def`.
* `CONSTRAINT_SCHEMA`: The schema of the constraint.
* `CONSTRAINT_NAME`: The name of the constraint.
* `CHECK_CLAUSE`: The clause of the check constraint.
