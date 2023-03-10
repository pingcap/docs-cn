---
title: PARTITIONS
summary: Learn the `PARTITIONS` INFORMATION_SCHEMA table.
---

# PARTITIONS

The `PARTITIONS` table provides information about partitioned tables.

```sql
USE INFORMATION_SCHEMA;
DESC partitions;
```

The output is as follows:

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
| PARTITION_EXPRESSION          | longtext     | YES  |      | NULL    |       |
| SUBPARTITION_EXPRESSION       | longtext     | YES  |      | NULL    |       |
| PARTITION_DESCRIPTION         | longtext     | YES  |      | NULL    |       |
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
| TIDB_PARTITION_ID             | bigint(21)   | YES  |      | NULL    |       |
| TIDB_PLACEMENT_POLICY_NAME    | varchar(64)  | YES  |      | NULL    |       |
+-------------------------------+--------------+------+------+---------+-------+
27 rows in set (0.00 sec)
```

```sql
CREATE TABLE test.t1 (id INT NOT NULL PRIMARY KEY) PARTITION BY HASH (id) PARTITIONS 2;
SELECT * FROM PARTITIONS WHERE table_schema='test' AND table_name='t1'\G
```

The output is as follows:

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
                  CREATE_TIME: 2022-12-14 06:09:33
                  UPDATE_TIME: NULL
                   CHECK_TIME: NULL
                     CHECKSUM: NULL
            PARTITION_COMMENT:
                    NODEGROUP: NULL
              TABLESPACE_NAME: NULL
            TIDB_PARTITION_ID: 89
   TIDB_PLACEMENT_POLICY_NAME: NULL
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
                  CREATE_TIME: 2022-12-14 06:09:33
                  UPDATE_TIME: NULL
                   CHECK_TIME: NULL
                     CHECKSUM: NULL
            PARTITION_COMMENT:
                    NODEGROUP: NULL
              TABLESPACE_NAME: NULL
            TIDB_PARTITION_ID: 90
   TIDB_PLACEMENT_POLICY_NAME: NULL
2 rows in set (0.00 sec)
```
