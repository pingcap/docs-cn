---
title: COLUMNS
summary: 了解 `COLUMNS` INFORMATION_SCHEMA 表。
---

# COLUMNS

`COLUMNS` 表提供了关于表中列的详细信息。

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
| COLLATION_NAME          | varchar(32)   | YES  |      | NULL    |       |
| COLUMN_TYPE              | text          | YES  |      | NULL    |       |
| COLUMN_KEY               | varchar(3)    | YES  |      | NULL    |       |
| EXTRA                    | varchar(30)   | YES  |      | NULL    |       |
| PRIVILEGES               | varchar(80)   | YES  |      | NULL    |       |
| COLUMN_COMMENT           | varchar(1024) | YES  |      | NULL    |       |
| GENERATION_EXPRESSION    | text          | NO   |      | NULL    |       |
+--------------------------+---------------+------+------+---------+-------+
21 rows in set (0.00 sec)
```

创建表 `test.t1` 并查询 `COLUMNS` 表中的信息：

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

`COLUMNS` 表中各列的描述如下：

* `TABLE_CATALOG`：包含该列的表所属的目录名称。该值始终为 `def`。
* `TABLE_SCHEMA`：包含该列的表所在的数据库（schema）名称。
* `TABLE_NAME`：包含该列的表名。
* `COLUMN_NAME`：列名。
* `ORDINAL_POSITION`：该列在表中的位置。
* `COLUMN_DEFAULT`：列的默认值。如果显式默认值为 `NULL`，或者列定义中不包含 `default` 子句，则该值为 `NULL`。
* `IS_NULLABLE`：该列是否可为空。如果该列可以存储 NULL 值，则该值为 `YES`；否则为 `NO`。
* `DATA_TYPE`：列中数据的类型。
* `CHARACTER_MAXIMUM_LENGTH`：对于字符串列，表示最大字符长度。
* `CHARACTER_OCTET_LENGTH`：对于字符串列，表示最大字节长度。
* `NUMERIC_PRECISION`：数字类型列的数值精度。
* `NUMERIC_SCALE`：数字类型列的数值小数位数。
* `DATETIME_PRECISION`：对于时间类型列，表示小数秒精度。
* `CHARACTER_SET_NAME`：字符串列的字符集名称。
* `COLLATION_NAME`：字符串列的排序规则名称。
* `COLUMN_TYPE`：列类型。
* `COLUMN_KEY`：该列是否被索引。该字段可能有以下值：
    * 空：该列未被索引，或该列被索引但是是多列非唯一索引中的第二列。
    * `PRI`：该列是主键或多个主键之一。
    * `UNI`：该列是唯一索引的第一列。
    * `MUL`：该列是非唯一索引的第一列，其中给定值允许出现多次。
* `EXTRA`：给定列的任何附加信息。
* `PRIVILEGES`：当前用户对该列拥有的权限。目前在 TiDB 中该值是固定的，始终为 `select,insert,update,references`。
* `COLUMN_COMMENT`：列定义中包含的注释。
* `GENERATION_EXPRESSION`：对于生成列，该值显示用于计算列值的表达式。对于非生成列，该值为空。

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
