---
title: PARTITIONS
summary: 了解 information_schema 表 `PARTITIONS`。
---

# PARTITIONS

`PARTITIONS` 表提供有关分区表的信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC partitions;
```

```sql
+-------------------------------+--------------+------+------+---------+-------+
| Field                         | Type         | Null | Key  | Default | Extra |
+-------------------------------+--------------+------+------+---------+-------+
| TABLE_CATALOG                 | varchar(512) | YES  |      | NULL    |       |
| TABLE_SCHEMA                  | varchar(64)  | YES  |      | NULL    |       |
| TABLE_NAME                    | varchar(64)  | YES  |      | NULL    |       |
| PARTITION_NAME                | varchar(64)  | YES  |      | NULL    |       |
| SUBPARTITION_NAME             | varchar(64)  | YES  |      | NULL    |       |
| PARTITION_ORDINAL_POSITION    | bigint(21)   | YES  |      | NULL    |       |
| SUBPARTITION_ORDINAL_POSITION | bigint(21)   | YES  |      | NULL    |       |
| PARTITION_METHOD              | varchar(18)  | YES  |      | NULL    |       |
| SUBPARTITION_METHOD           | varchar(12)  | YES  |      | NULL    |       |
| PARTITION_EXPRESSION          | longblob     | YES  |      | NULL    |       |
| SUBPARTITION_EXPRESSION       | longblob     | YES  |      | NULL    |       |
| PARTITION_DESCRIPTION         | longblob     | YES  |      | NULL    |       |
| TABLE_ROWS                    | bigint(21)   | YES  |      | NULL    |       |
| AVG_ROW_LENGTH                | bigint(21)   | YES  |      | NULL    |       |
| DATA_LENGTH                   | bigint(21)   | YES  |      | NULL    |       |
| MAX_DATA_LENGTH               | bigint(21)   | YES  |      | NULL    |       |
| INDEX_LENGTH                  | bigint(21)   | YES  |      | NULL    |       |
| DATA_FREE                     | bigint(21)   | YES  |      | NULL    |       |
| CREATE_TIME                   | datetime     | YES  |      | NULL    |       |
| UPDATE_TIME                   | datetime     | YES  |      | NULL    |       |
| CHECK_TIME                    | datetime     | YES  |      | NULL    |       |
| CHECKSUM                      | bigint(21)   | YES  |      | NULL    |       |
| PARTITION_COMMENT             | varchar(80)  | YES  |      | NULL    |       |
| NODEGROUP                     | varchar(12)  | YES  |      | NULL    |       |
| TABLESPACE_NAME               | varchar(64)  | YES  |      | NULL    |       |
+-------------------------------+--------------+------+------+---------+-------+
25 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t1 (id INT NOT NULL PRIMARY KEY) PARTITION BY HASH (id) PARTITIONS 2;
SELECT * FROM partitions WHERE table_schema='test' AND table_name='t1'\G
```

```sql
*************************** 1. row ***************************
                TABLE_CATALOG: def
                 TABLE_SCHEMA: test
                   TABLE_NAME: t1
               PARTITION_NAME: p0
            SUBPARTITION_NAME: NULL
   PARTITION_ORDINAL_POSITION: 1
SUBPARTITION_ORDINAL_POSITION: NULL
             PARTITION_METHOD: HASH
          SUBPARTITION_METHOD: NULL
         PARTITION_EXPRESSION: `id`
      SUBPARTITION_EXPRESSION: NULL
        PARTITION_DESCRIPTION: 
                   TABLE_ROWS: 0
               AVG_ROW_LENGTH: 0
                  DATA_LENGTH: 0
              MAX_DATA_LENGTH: 0
                 INDEX_LENGTH: 0
                    DATA_FREE: 0
                  CREATE_TIME: 2020-07-06 16:35:28
                  UPDATE_TIME: NULL
                   CHECK_TIME: NULL
                     CHECKSUM: NULL
            PARTITION_COMMENT: 
                    NODEGROUP: NULL
              TABLESPACE_NAME: NULL
*************************** 2. row ***************************
                TABLE_CATALOG: def
                 TABLE_SCHEMA: test
                   TABLE_NAME: t1
               PARTITION_NAME: p1
            SUBPARTITION_NAME: NULL
   PARTITION_ORDINAL_POSITION: 2
SUBPARTITION_ORDINAL_POSITION: NULL
             PARTITION_METHOD: HASH
          SUBPARTITION_METHOD: NULL
         PARTITION_EXPRESSION: `id`
      SUBPARTITION_EXPRESSION: NULL
        PARTITION_DESCRIPTION: 
                   TABLE_ROWS: 0
               AVG_ROW_LENGTH: 0
                  DATA_LENGTH: 0
              MAX_DATA_LENGTH: 0
                 INDEX_LENGTH: 0
                    DATA_FREE: 0
                  CREATE_TIME: 2020-07-06 16:35:28
                  UPDATE_TIME: NULL
                   CHECK_TIME: NULL
                     CHECKSUM: NULL
            PARTITION_COMMENT: 
                    NODEGROUP: NULL
              TABLESPACE_NAME: NULL
2 rows in set (0.00 sec)
```
