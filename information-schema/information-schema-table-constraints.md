---
title: TABLE_CONSTRAINTS
summary: Learn the `TABLE_CONSTRAINTS` information_schema table.
---

# TABLE_CONSTRAINTS

The `TABLE_CONSTRAINTS` table describes which tables have constraints.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC table_constraints;
```

```
+--------------------+--------------+------+------+---------+-------+
| Field              | Type         | Null | Key  | Default | Extra |
+--------------------+--------------+------+------+---------+-------+
| CONSTRAINT_CATALOG | varchar(512) | YES  |      | NULL    |       |
| CONSTRAINT_SCHEMA  | varchar(64)  | YES  |      | NULL    |       |
| CONSTRAINT_NAME    | varchar(64)  | YES  |      | NULL    |       |
| TABLE_SCHEMA       | varchar(64)  | YES  |      | NULL    |       |
| TABLE_NAME         | varchar(64)  | YES  |      | NULL    |       |
| CONSTRAINT_TYPE    | varchar(64)  | YES  |      | NULL    |       |
+--------------------+--------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM table_constraints WHERE constraint_type='UNIQUE';
```

```
+--------------------+--------------------+-------------------------+--------------------+-------------------------------------+-----------------+
| CONSTRAINT_CATALOG | CONSTRAINT_SCHEMA  | CONSTRAINT_NAME         | TABLE_SCHEMA       | TABLE_NAME                          | CONSTRAINT_TYPE |
+--------------------+--------------------+-------------------------+--------------------+-------------------------------------+-----------------+
| def                | mysql              | name                    | mysql              | help_topic                          | UNIQUE          |
| def                | mysql              | tbl                     | mysql              | stats_meta                          | UNIQUE          |
| def                | mysql              | tbl                     | mysql              | stats_histograms                    | UNIQUE          |
| def                | mysql              | tbl                     | mysql              | stats_buckets                       | UNIQUE          |
| def                | mysql              | delete_range_index      | mysql              | gc_delete_range                     | UNIQUE          |
| def                | mysql              | delete_range_done_index | mysql              | gc_delete_range_done                | UNIQUE          |
| def                | PERFORMANCE_SCHEMA | SCHEMA_NAME             | PERFORMANCE_SCHEMA | events_statements_summary_by_digest | UNIQUE          |
+--------------------+--------------------+-------------------------+--------------------+-------------------------------------+-----------------+
7 rows in set (0.01 sec)
```

- The `CONSTRAINT_TYPE` value can be `UNIQUE`, `PRIMARY KEY`, or `FOREIGN KEY`.
- The `UNIQUE` and `PRIMARY KEY` information is similar to the result of the `SHOW INDEX` statement.