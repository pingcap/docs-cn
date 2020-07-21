---
title: TABLES
summary: Learn the `TABLES` information_schema table.
---

# TABLES

The `TABLES` table provides information about tables in databases:

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tables;
```

```
+---------------------------+---------------+------+------+----------+-------+
| Field                     | Type          | Null | Key  | Default  | Extra |
+---------------------------+---------------+------+------+----------+-------+
| TABLE_CATALOG             | varchar(512)  | YES  |      | NULL     |       |
| TABLE_SCHEMA              | varchar(64)   | YES  |      | NULL     |       |
| TABLE_NAME                | varchar(64)   | YES  |      | NULL     |       |
| TABLE_TYPE                | varchar(64)   | YES  |      | NULL     |       |
| ENGINE                    | varchar(64)   | YES  |      | NULL     |       |
| VERSION                   | bigint(21)    | YES  |      | NULL     |       |
| ROW_FORMAT                | varchar(10)   | YES  |      | NULL     |       |
| TABLE_ROWS                | bigint(21)    | YES  |      | NULL     |       |
| AVG_ROW_LENGTH            | bigint(21)    | YES  |      | NULL     |       |
| DATA_LENGTH               | bigint(21)    | YES  |      | NULL     |       |
| MAX_DATA_LENGTH           | bigint(21)    | YES  |      | NULL     |       |
| INDEX_LENGTH              | bigint(21)    | YES  |      | NULL     |       |
| DATA_FREE                 | bigint(21)    | YES  |      | NULL     |       |
| AUTO_INCREMENT            | bigint(21)    | YES  |      | NULL     |       |
| CREATE_TIME               | datetime      | YES  |      | NULL     |       |
| UPDATE_TIME               | datetime      | YES  |      | NULL     |       |
| CHECK_TIME                | datetime      | YES  |      | NULL     |       |
| TABLE_COLLATION           | varchar(32)   | NO   |      | utf8_bin |       |
| CHECKSUM                  | bigint(21)    | YES  |      | NULL     |       |
| CREATE_OPTIONS            | varchar(255)  | YES  |      | NULL     |       |
| TABLE_COMMENT             | varchar(2048) | YES  |      | NULL     |       |
| TIDB_TABLE_ID             | bigint(21)    | YES  |      | NULL     |       |
| TIDB_ROW_ID_SHARDING_INFO | varchar(255)  | YES  |      | NULL     |       |
+---------------------------+---------------+------+------+----------+-------+
23 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM tables WHERE table_schema='mysql' AND table_name='user'\G
```

```
*************************** 1. row ***************************
            TABLE_CATALOG: def
             TABLE_SCHEMA: mysql
               TABLE_NAME: user
               TABLE_TYPE: BASE TABLE
                   ENGINE: InnoDB
                  VERSION: 10
               ROW_FORMAT: Compact
               TABLE_ROWS: 0
           AVG_ROW_LENGTH: 0
              DATA_LENGTH: 0
          MAX_DATA_LENGTH: 0
             INDEX_LENGTH: 0
                DATA_FREE: 0
           AUTO_INCREMENT: NULL
              CREATE_TIME: 2020-07-05 09:25:51
              UPDATE_TIME: NULL
               CHECK_TIME: NULL
          TABLE_COLLATION: utf8mb4_bin
                 CHECKSUM: NULL
           CREATE_OPTIONS: 
            TABLE_COMMENT: 
            TIDB_TABLE_ID: 5
TIDB_ROW_ID_SHARDING_INFO: NULL
1 row in set (0.00 sec)
```

The following statements are equivalent:

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

The description of columns in the `TABLES` table is as follows:

* `TABLE_CATALOG`: The name of the catalog which the table belongs to. The value is always `def`.
* `TABLE_SCHEMA`: The name of the schema which the table belongs to.
* `TABLE_NAME`: The name of the table.
* `TABLE_TYPE`: The type of the table.
* `ENGINE`: The type of the storage engine. The value is currently `InnoDB`.
* `VERSION`: Version. The value is `10` by default.
* `ROW_FORMAT`: The row format. The value is currently `Compact`.
* `TABLE_ROWS`: The number of rows in the table in statistics.
* `AVG_ROW_LENGTH`: The average row length of the table. `AVG_ROW_LENGTH` = `DATA_LENGTH` / `TABLE_ROWS`.
* `DATA_LENGTH`: Data length. `DATA_LENGTH` = `TABLE_ROWS` \* the sum of storage lengths of the columns in the tuple. The replicas of TiKV are not taken into account.
* `MAX_DATA_LENGTH`: The maximum data length. The value is currently `0`, which means the data length has no upper limit.
* `INDEX_LENGTH`: The index length. `INDEX_LENGTH` = `TABLE_ROWS` \* the sum of lengths of the columns in the index tuple. The replicas of TiKV are not taken into account.
* `DATA_FREE`: Data fragment. The value is currently `0`.
* `AUTO_INCREMENT`: The current step of the auto- increment primary key.
* `CREATE_TIME`: The time at which the table is created.
* `UPDATE_TIME`: The time at which the table is updated.
* `CHECK_TIME`: The time at which the table is checked.
* `TABLE_COLLATION`: The collation of strings in the table.
* `CHECKSUM`: Checksum.
* `CREATE_OPTIONS`: Creates options.
* `TABLE_COMMENT`: The comments and notes of the table.

Most of the information in the table is the same as MySQL. Only two columns are newly defined by TiDB:

* `TIDB_TABLE_ID`: to indicate the internal ID of a table. This ID is unique in a TiDB cluster.
* `TIDDB_ROW_ID_SHARDING_INFO`: to indicate the sharding type of a table. The possible values are as follows:
    - `"NOT_SHARDED"`: the table is not sharded.
    - `"NOT_SHARDED(PK_IS_HANDLE)"`: the table that defines an integer Primary Key as its row id is not sharded.
    - `"PK_AUTO_RANDOM_BITS={bit_number}"`: the table that defines an integer Primary Key as its row id is sharded because the Primary Key is assigned with `AUTO_RANDOM` attribute.
    - `"SHARD_BITS={bit_number}"`: the table is sharded using `SHARD_ROW_ID_BITS={bit_number}`.
    - NULL: the table is a system table or view, and thus cannot be sharded.
