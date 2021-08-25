---
title: SCHEMATA
summary: 了解 information_schema 表 `SCHEMATA`。
---

# SCHEMATA

`SCHEMATA` 表提供了关于数据库的信息。表中的数据与 `SHOW DATABASES` 语句的执行结果等价。

{{< copyable "sql" >}}

```sql
USE information_schema;
desc SCHEMATA;
```

```sql
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

```sql
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

`SCHEMATA` 表各列字段含义如下：

* CATALOG_NAME：数据库归属的目录名，该列值永远为 `def`。
* SCHEMA_NAME：数据库的名字。
* DEFAULT_CHARACTER_SET_NAME：数据库的默认字符集。
* DEFAULT_COLLATION_NAME：数据库的默认 collation。
* SQL_PATH：该项值永远为 `NULL`。
