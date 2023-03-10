---
title: COLUMNS
summary: Learn the `COLUMNS` INFORMATION_SCHEMA table.
---

# COLUMNS

The `COLUMNS` table provides detailed information about columns in tables.

```sql
USE INFORMATION_SCHEMA;
DESC COLUMNS;
```

The output is as follows:

```sql
+--------------------------+---------------+------+------+---------+-------+
| Field                    | Type          | Null | Key  | Default | Extra |
+--------------------------+---------------+------+------+---------+-------+
| TABLE_CATALOG            | varchar(512)  | YES  |      | NULL    |       |
| TABLE_SCHEMA             | varchar(64)   | YES  |      | NULL    |       |
| TABLE_NAME               | varchar(64)   | YES  |      | NULL    |       |
| COLUMN_NAME              | varchar(64)   | YES  |      | NULL    |       |
| ORDINAL_POSITION         | bigint(64)    | YES  |      | NULL    |       |
| COLUMN_DEFAULT           | text          | YES  |      | NULL    |       |
| IS_NULLABLE              | varchar(3)    | YES  |      | NULL    |       |
| DATA_TYPE                | varchar(64)   | YES  |      | NULL    |       |
| CHARACTER_MAXIMUM_LENGTH | bigint(21)    | YES  |      | NULL    |       |
| CHARACTER_OCTET_LENGTH   | bigint(21)    | YES  |      | NULL    |       |
| NUMERIC_PRECISION        | bigint(21)    | YES  |      | NULL    |       |
| NUMERIC_SCALE            | bigint(21)    | YES  |      | NULL    |       |
| DATETIME_PRECISION       | bigint(21)    | YES  |      | NULL    |       |
| CHARACTER_SET_NAME       | varchar(32)   | YES  |      | NULL    |       |
| COLLATION_NAME           | varchar(32)   | YES  |      | NULL    |       |
| COLUMN_TYPE              | text          | YES  |      | NULL    |       |
| COLUMN_KEY               | varchar(3)    | YES  |      | NULL    |       |
| EXTRA                    | varchar(30)   | YES  |      | NULL    |       |
| PRIVILEGES               | varchar(80)   | YES  |      | NULL    |       |
| COLUMN_COMMENT           | varchar(1024) | YES  |      | NULL    |       |
| GENERATION_EXPRESSION    | text          | NO   |      | NULL    |       |
+--------------------------+---------------+------+------+---------+-------+
21 rows in set (0.00 sec)
```

Create a table `test.t1` and query the information in the `COLUMNS` table:

```sql
CREATE TABLE test.t1 (a int);
SELECT * FROM COLUMNS WHERE table_schema='test' AND TABLE_NAME='t1'\G
```

输出结果如下：

```sql
*************************** 1. row ***************************
           TABLE_CATALOG: def
            TABLE_SCHEMA: test
              TABLE_NAME: t1
             COLUMN_NAME: a
        ORDINAL_POSITION: 1
          COLUMN_DEFAULT: NULL
             IS_NULLABLE: YES
               DATA_TYPE: int
CHARACTER_MAXIMUM_LENGTH: NULL
  CHARACTER_OCTET_LENGTH: NULL
       NUMERIC_PRECISION: 11
           NUMERIC_SCALE: 0
      DATETIME_PRECISION: NULL
      CHARACTER_SET_NAME: NULL
          COLLATION_NAME: NULL
             COLUMN_TYPE: int(11)
              COLUMN_KEY:
                   EXTRA:
              PRIVILEGES: select,insert,update,references
          COLUMN_COMMENT:
   GENERATION_EXPRESSION:
1 row in set (0.02 sec)
```

The description of columns in the `COLUMNS` table is as follows:

* `TABLE_CATALOG`: The name of the catalog to which the table with the column belongs. The value is always `def`.
* `TABLE_SCHEMA`: The name of the schema in which the table with the column is located.
* `TABLE_NAME`: The name of the table with the column.
* `COLUMN_NAME`: The name of the column.
* `ORDINAL_POSITION`: The position of the column in the table.
* `COLUMN_DEFAULT`: The default value of the column. If the explicit default value is `NULL`, or if the column definition does not include the `default` clause, this value is `NULL`.
* `IS_NULLABLE`: Whether the column is nullable. If the column can store null values, this value is `YES`; otherwise, it is `NO`.
* `DATA_TYPE`: The type of data in the column.
* `CHARACTER_MAXIMUM_LENGTH`: For string columns, the maximum length in characters.
* `CHARACTER_OCTET_LENGTH`: For string columns, the maximum length in bytes.
* `NUMERIC_PRECISION`: The numeric precision of a number-type column.
* `NUMERIC_SCALE`: The numeric scale of a number-type column.
* `DATETIME_PRECISION`: For time-type columns, the fractional seconds precision.
* `CHARACTER_SET_NAME`: The name of the character set of a string column.
* `COLLATION_NAME`: The name of the collation of a string column.
* `COLUMN_TYPE`: The column type.
* `COLUMN_KEY`: Whether this column is indexed. This field might have the following values:
    * Empty: This column is not indexed, or this column is indexed and is the second column in a multi-column non-unique index.
    * `PRI`: This column is the primary key or one of multiple primary keys.
    * `UNI`: This column is the first column of the unique index.
    * `MUL`: The column is the first column of a non-unique index, in which a given value is allowed to occur for multiple times.
* `EXTRA`: Any additional information of the given column.
* `PRIVILEGES`: The privilege that the current user has on this column. Currently, this value is fixed in TiDB, and is always `select,insert,update,references`.
* `COLUMN_COMMENT`: Comments contained in the column definition.
* `GENERATION_EXPRESSION`: For generated columns, this value displays the expression used to calculate the column value. For non-generated columns, the value is empty.

The corresponding `SHOW` statement is as follows:

```sql
SHOW COLUMNS FROM t1 FROM test;
```

The output is as follows:

```sql
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)
```