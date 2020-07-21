---
title: KEY_COLUMN_USAGE
summary: Learn the `KEY_COLUMN_USAGE` information_schema table.
---

# KEY_COLUMN_USAGE

The `KEY_COLUMN_USAGE` table describes the key constraints of the columns, such as the primary key constraint.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC key_column_usage;
```

```
+-------------------------------+--------------+------+------+---------+-------+
| Field                         | Type         | Null | Key  | Default | Extra |
+-------------------------------+--------------+------+------+---------+-------+
| CONSTRAINT_CATALOG            | varchar(512) | NO   |      | NULL    |       |
| CONSTRAINT_SCHEMA             | varchar(64)  | NO   |      | NULL    |       |
| CONSTRAINT_NAME               | varchar(64)  | NO   |      | NULL    |       |
| TABLE_CATALOG                 | varchar(512) | NO   |      | NULL    |       |
| TABLE_SCHEMA                  | varchar(64)  | NO   |      | NULL    |       |
| TABLE_NAME                    | varchar(64)  | NO   |      | NULL    |       |
| COLUMN_NAME                   | varchar(64)  | NO   |      | NULL    |       |
| ORDINAL_POSITION              | bigint(10)   | NO   |      | NULL    |       |
| POSITION_IN_UNIQUE_CONSTRAINT | bigint(10)   | YES  |      | NULL    |       |
| REFERENCED_TABLE_SCHEMA       | varchar(64)  | YES  |      | NULL    |       |
| REFERENCED_TABLE_NAME         | varchar(64)  | YES  |      | NULL    |       |
| REFERENCED_COLUMN_NAME        | varchar(64)  | YES  |      | NULL    |       |
+-------------------------------+--------------+------+------+---------+-------+
12 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM key_column_usage WHERE table_schema='mysql' and table_name='user';
```

```
*************************** 1. row ***************************
           CONSTRAINT_CATALOG: def
            CONSTRAINT_SCHEMA: mysql
              CONSTRAINT_NAME: PRIMARY
                TABLE_CATALOG: def
                 TABLE_SCHEMA: mysql
                   TABLE_NAME: user
                  COLUMN_NAME: Host
             ORDINAL_POSITION: 1
POSITION_IN_UNIQUE_CONSTRAINT: NULL
      REFERENCED_TABLE_SCHEMA: NULL
        REFERENCED_TABLE_NAME: NULL
       REFERENCED_COLUMN_NAME: NULL
*************************** 2. row ***************************
           CONSTRAINT_CATALOG: def
            CONSTRAINT_SCHEMA: mysql
              CONSTRAINT_NAME: PRIMARY
                TABLE_CATALOG: def
                 TABLE_SCHEMA: mysql
                   TABLE_NAME: user
                  COLUMN_NAME: User
             ORDINAL_POSITION: 2
POSITION_IN_UNIQUE_CONSTRAINT: NULL
      REFERENCED_TABLE_SCHEMA: NULL
        REFERENCED_TABLE_NAME: NULL
       REFERENCED_COLUMN_NAME: NULL
2 rows in set (0.00 sec)
```

The description of columns in the `KEY_COLUMN_USAGE` table is as follows:

* `CONSTRAINT_CATALOG`: The name of the catalog to which the constraint belongs. The value is always `def`.
* `CONSTRAINT_SCHEMA`: The name of the schema to which the constraint belongs.
* `CONSTRAINT_NAME`: The name of the constraint.
* `TABLE_CATALOG`: The name of the catalog to which the table belongs. The value is always `def`.
* `TABLE_SCHEMA`: The name of the schema to which the table belongs.
* `TABLE_NAME`: The name of the table with constraints.
* `COLUMN_NAME`: The name of the column with constraints.
* `ORDINAL_POSITION`: The position of the column in the constraint, rather than in the table. The position number starts from `1`.
* `POSITION_IN_UNIQUE_CONSTRAINT`: The unique constraint and the primary key constraint are empty. For foreign key constraints, this column is the position of the referenced table's key.
* `REFERENCED_TABLE_SCHEMA`: The name of the schema referenced by the constraint. Currently in TiDB, the value of this column in all constraints is `nil`, except for the foreign key constraint.
* `REFERENCED_TABLE_NAME`: The name of the table referenced by the constraint. Currently in TiDB, the value of this column in all constraints is `nil`, except for the foreign key constraint.
* `REFERENCED_COLUMN_NAME`: The name of the column referenced by the constraint. Currently in TiDB, the value of this column in all constraints is `nil`, except for the foreign key constraint.
