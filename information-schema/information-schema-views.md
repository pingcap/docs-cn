---
title: VIEWS
summary: Learn the `VIEWS` INFORMATION_SCHEMA table.
---

# VIEWS

The `VIEWS` table provides information about SQL views.

```sql
USE INFORMATION_SCHEMA;
DESC VIEWS;
```

The output is as follows:

```sql
+----------------------+--------------+------+------+---------+-------+
| Field                | Type         | Null | Key  | Default | Extra |
+----------------------+--------------+------+------+---------+-------+
| TABLE_CATALOG        | varchar(512) | NO   |      | NULL    |       |
| TABLE_SCHEMA         | varchar(64)  | NO   |      | NULL    |       |
| TABLE_NAME           | varchar(64)  | NO   |      | NULL    |       |
| VIEW_DEFINITION      | longtext     | NO   |      | NULL    |       |
| CHECK_OPTION         | varchar(8)   | NO   |      | NULL    |       |
| IS_UPDATABLE         | varchar(3)   | NO   |      | NULL    |       |
| DEFINER              | varchar(77)  | NO   |      | NULL    |       |
| SECURITY_TYPE        | varchar(7)   | NO   |      | NULL    |       |
| CHARACTER_SET_CLIENT | varchar(32)  | NO   |      | NULL    |       |
| COLLATION_CONNECTION | varchar(32)  | NO   |      | NULL    |       |
+----------------------+--------------+------+------+---------+-------+
10 rows in set (0.00 sec)
```

Create a view and query the `VIEWS` table:

```sql
CREATE VIEW test.v1 AS SELECT 1;
SELECT * FROM VIEWS\G
```

The output is as follows:

```sql
*************************** 1. row ***************************
       TABLE_CATALOG: def
        TABLE_SCHEMA: test
          TABLE_NAME: v1
     VIEW_DEFINITION: SELECT 1
        CHECK_OPTION: CASCADED
        IS_UPDATABLE: NO
             DEFINER: root@127.0.0.1
       SECURITY_TYPE: DEFINER
CHARACTER_SET_CLIENT: utf8mb4
COLLATION_CONNECTION: utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```

Fields in the `VIEWS` table are described as follows:

* `TABLE_CATALOG`: The name of the catalog to which the view belongs. This value is always `def`.
* `TABLE_SCHEMA`: The name of the schema to which the view belongs.
* `TABLE_NAME`: The view name.
* `VIEW_DEFINITION`: The definition of view, which is made by the `SELECT` statement when the view is created.
* `CHECK_OPTION`: The `CHECK_OPTION` value. The value options are `NONE`, `CASCADE`, and `LOCAL`.
* `IS_UPDATABLE`: Whether `UPDATE`/`INSERT`/`DELETE` is applicable to the view. In TiDB, the value is always `NO`.
* `DEFINER`: The name of the user who creates the view, which is in the format of `'user_name'@'host_name'`.
* `SECURITY_TYPE`: The value of `SQL SECURITY`. The value options are `DEFINER` and `INVOKER`.
* `CHARACTER_SET_CLIENT`: The value of the `character_set_client` session variable when the view is created.
* `COLLATION_CONNECTION`: The value of the `collation_connection` session variable when the view is created.