---
title: TABLE_CONSTRAINTS
summary: 了解 `TABLE_CONSTRAINTS` information_schema 表。
---

# TABLE_CONSTRAINTS

`TABLE_CONSTRAINTS` 表描述了哪些表具有[约束](/constraints.md)。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC table_constraints;
```

```sql
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

```sql
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

`TABLE_CONSTRAINTS` 表中的字段说明如下：

* `CONSTRAINT_CATALOG`：约束所属的目录名称。该值始终为 `def`。
* `CONSTRAINT_SCHEMA`：约束所属的数据库名称。
* `CONSTRAINT_NAME`：约束的名称。
* `TABLE_NAME`：表的名称。
* `CONSTRAINT_TYPE`：约束的类型。值可以是 `UNIQUE`、`PRIMARY KEY` 或 `FOREIGN KEY`。`UNIQUE` 和 `PRIMARY KEY` 信息类似于 `SHOW INDEX` 语句的执行结果。
