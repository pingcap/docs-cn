---
title: COLUMNS
summary: 了解 INFORMATION_SCHEMA 表 `COLUMNS`。
---

# COLUMNS

`COLUMNS` 表提供了表的所有列的信息。

```sql
USE INFORMATION_SCHEMA;
DESC COLUMNS;
```

输出结果如下：

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

创建表 `test.t1`，并查询 `COLUMNS` 表的信息：

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

`COLUMNS` 表中列的含义如下：

* `TABLE_CATALOG`：包含列的表所属的目录的名称。该值始终为 `def`。
* `TABLE_SCHEMA`：包含列的表所属的数据库的名称。
* `TABLE_NAME`：包含列的表的名称。
* `COLUMN_NAME`：列的名称。
* `ORDINAL_POSITION`：表中列的位置。
* `COLUMN_DEFAULT`：列的默认值。如果列的显式默认值为 `NULL`，或者列定义中不包含 `default` 子句，则此值为 `NULL`。
* `IS_NULLABLE`：列的可空性。如果列中可以存储空值，则该值为 `YES`，否则为 `NO`。
* `DATA_TYPE`：列的数据类型。
* `CHARACTER_MAXIMUM_LENGTH`：对于字符串列，以字符为单位的最大长度。
* `CHARACTER_OCTET_LENGTH`：对于字符串列，以字节为单位的最大长度。
* `NUMERIC_PRECISION`：对于数字列，为数字精度。
* `NUMERIC_SCALE`：对于数字列，为数字刻度。
* `DATETIME_PRECISION`：对于时间列，小数秒精度。
* `CHARACTER_SET_NAME`：对于字符串列，字符集名称。
* `COLLATION_NAME`：对于字符串列，排序规则名称。
* `COLUMN_TYPE`：列类型。
* `COLUMN_KEY`：该列是否被索引。具体显示如下：
    * 如果此值为空，则该列要么未被索引，要么被索引且是多列非唯一索引中的第二列。
    * 如果此值是 `PRI`，则该列是主键，或者是多列主键中的一列。
    * 如果此值是 `UNI`，则该列是唯一索引的第一列。
    * 如果此值是 `MUL`，则该列是非唯一索引的第一列，在该列中允许给定值的多次出现。
* `EXTRA`：关于给定列的任何附加信息。
* `PRIVILEGES`：当前用户对该列拥有的权限。目前在 TiDB 中，此值为定值，一直为 `select,insert,update,references`。
* `COLUMN_COMMENT`：列定义中包含的注释。
* `GENERATION_EXPRESSION`：对于生成的列，显示用于计算列值的表达式。对于未生成的列为空。

对应的 `SHOW` 语句如下：

```sql
SHOW COLUMNS FROM t1 FROM test;
```

输出结果如下：

```sql
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)
```

## 另请参阅

- [`SHOW COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md)