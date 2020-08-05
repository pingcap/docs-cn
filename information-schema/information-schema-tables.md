---
title: TABLES
summary: 了解 information_schema 表 `TABLES`。
---

# TABLES

`TABLES` 表提供了数据库里关于表的信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tables;
```

```sql
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

```sql
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

下列语句是等价的：

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

`TABLES` 表各列字段含义如下：

* `TABLE_CATALOG`：表所属的目录的名称。该值始终为 `def`。
* `TABLE_SCHEMA`：表所属数据库的名称。
* `TABLE_NAME`：表的名称。
* `TABLE_TYPE`：表的类型。
* `ENGINE`：存储引擎类型。该值暂为 ‘InnoDB’。
* `VERSION`：版本，默认值为 10。
* `ROW_FORMAT`：行格式。该值暂为 ‘Compact’。
* `TABLE_ROWS`：统计信息中该表所存的行数。
* `AVG_ROW_LENGTH`：该表中所存数据的平均行长度。平均行长度 = DATA_LENGTH / 统计信息中的行数。
* `DATA_LENGTH`：数据长度。数据长度 = 统计信息中的行数 × 元组各列存储长度和，这里尚未考虑 TiKV 的副本数。
* `MAX_DATA_LENGTH`：最大数据长度。该值暂为 0，表示没有最大数据长度的限制。
* `INDEX_LENGTH`：索引长度。索引长度 = 统计信息中的行数 × 索引元组各列长度和，这里尚未考虑 TiKV 的副本数。
* `DATA_FREE`：空间碎片。该值暂为 0。
* `AUTO_INCREMENT`：该表中自增主键自动增量的当前值。
* `CREATE_TIME`：该表的创建时间。
* `UPDATE_TIME`：该表的更新时间。
* `CHECK_TIME`：该表的检查时间。
* `TABLE_COLLATION`：该表的字符校验编码集。
* `CHECKSUM`：校验和。
* `CREATE_OPTIONS`：创建选项。
* `TABLE_COMMENT`：表的注释、备注。

表中的信息大部分定义自 MySQL，只有两列是 TiDB 新增的：

* `TIDB_TABLE_ID`：标识表的内部 ID，该 ID 在一个 TiDB 集群内部唯一。
* `TIDB_ROW_ID_SHARDING_INFO`：标识表的 Sharding 类型，可能的值为：
    - `"NOT_SHARDED"`：表未被 Shard。
    - `"NOT_SHARDED(PK_IS_HANDLE)"`：一个定义了整型主键的表未被 Shard。
    - `"PK_AUTO_RANDOM_BITS={bit_number}"`：一个定义了整型主键的表由于定义了 `AUTO_RANDOM` 而被 Shard。
    - `"SHARD_BITS={bit_number}"`：表使用 `SHARD_ROW_ID_BITS={bit_number}` 进行了 Shard。
    - NULL：表属于系统表或 View，无法被 Shard。
