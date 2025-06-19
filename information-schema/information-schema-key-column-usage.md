---
title: KEY_COLUMN_USAGE
summary: 了解 `KEY_COLUMN_USAGE` information_schema 表。
---

# KEY_COLUMN_USAGE

`KEY_COLUMN_USAGE` 表描述了列的键约束，例如主键约束。

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

`KEY_COLUMN_USAGE` 表中各列的描述如下：

* `CONSTRAINT_CATALOG`：约束所属的目录名称。该值始终为 `def`。
* `CONSTRAINT_SCHEMA`：约束所属的数据库（schema）名称。
* `CONSTRAINT_NAME`：约束的名称。
* `TABLE_CATALOG`：表所属的目录名称。该值始终为 `def`。
* `TABLE_SCHEMA`：表所属的数据库（schema）名称。
* `TABLE_NAME`：具有约束的表名。
* `COLUMN_NAME`：具有约束的列名。
* `ORDINAL_POSITION`：列在约束中的位置，而不是在表中的位置。位置编号从 `1` 开始。
* `POSITION_IN_UNIQUE_CONSTRAINT`：唯一约束和主键约束为空。对于外键约束，此列是被引用表的键的位置。
* `REFERENCED_TABLE_SCHEMA`：约束引用的数据库（schema）名称。目前在 TiDB 中，除外键约束外，所有约束中该列的值都为 `nil`。
* `REFERENCED_TABLE_NAME`：约束引用的表名。目前在 TiDB 中，除外键约束外，所有约束中该列的值都为 `nil`。
* `REFERENCED_COLUMN_NAME`：约束引用的列名。目前在 TiDB 中，除外键约束外，所有约束中该列的值都为 `nil`。
