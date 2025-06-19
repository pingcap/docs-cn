---
title: SCHEMATA
summary: 了解 `SCHEMATA` information_schema 表。
---

# SCHEMATA

`SCHEMATA` 表提供了数据库的相关信息。该表的数据等同于 [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md) 语句的结果。

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

`SCHEMATA` 表中的字段说明如下：

* `CATALOG_NAME`：数据库所属的目录。
* `SCHEMA_NAME`：数据库名称。
* `DEFAULT_CHARACTER_SET_NAME`：数据库的默认字符集。
* `DEFAULT_COLLATION_NAME`：数据库的默认排序规则。
* `SQL_PATH`：该项的值始终为 `NULL`。
