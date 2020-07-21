---
title: SCHEMATA
summary: Learn the `SCHEMATA` information_schema table.
---

# SCHEMATA

The `SCHEMATA` table provides information about databases. The table data is equivalent to the result of the `SHOW DATABASES` statement.

{{< copyable "sql" >}}

```sql
USE information_schema;
desc SCHEMATA;
```

```
+----------------------------+--------------+------+------+---------+-------+
| Field                      | Type         | Null | Key  | Default | Extra |
+----------------------------+--------------+------+------+---------+-------+
| CATALOG_NAME               | varchar(512) | YES  |      | NULL    |       |
| SCHEMA_NAME                | varchar(64)  | YES  |      | NULL    |       |
| DEFAULT_CHARACTER_SET_NAME | varchar(64)  | YES  |      | NULL    |       |
| DEFAULT_COLLATION_NAME     | varchar(32)  | YES  |      | NULL    |       |
| SQL_PATH                   | varchar(512) | YES  |      | NULL    |       |
+----------------------------+--------------+------+------+---------+-------+
5 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM SCHEMATA;
```

```
+--------------+--------------------+----------------------------+------------------------+----------+
| CATALOG_NAME | SCHEMA_NAME        | DEFAULT_CHARACTER_SET_NAME | DEFAULT_COLLATION_NAME | SQL_PATH |
+--------------+--------------------+----------------------------+------------------------+----------+
| def          | INFORMATION_SCHEMA | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | METRICS_SCHEMA     | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | mysql              | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | PERFORMANCE_SCHEMA | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | test               | utf8mb4                    | utf8mb4_bin            | NULL     |
+--------------+--------------------+----------------------------+------------------------+----------+
5 rows in set (0.00 sec)
```
