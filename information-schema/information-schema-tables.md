---
title: TABLES
summary: 了解 `TABLES` information_schema 表。
---

# TABLES

`TABLES` 表提供了数据库中表的相关信息：

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

以下语句是等价的：

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

`TABLES` 表中各列的描述如下：

* `TABLE_CATALOG`：表所属的目录名称。该值始终为 `def`。
* `TABLE_SCHEMA`：表所属的数据库名称。
* `TABLE_NAME`：表的名称。
* `TABLE_TYPE`：表的类型。
* `ENGINE`：存储引擎的类型。当前值为 `InnoDB`。
* `VERSION`：版本号。默认值为 `10`。
* `ROW_FORMAT`：行格式。当前值为 `Compact`。
* `TABLE_ROWS`：统计信息中的表行数。
* `AVG_ROW_LENGTH`：表的平均行长度。`AVG_ROW_LENGTH` = `DATA_LENGTH` / `TABLE_ROWS`。
* `DATA_LENGTH`：数据长度。`DATA_LENGTH` = `TABLE_ROWS` \* 元组中列的存储长度之和。不考虑 TiKV 的副本。
* `MAX_DATA_LENGTH`：最大数据长度。当前值为 `0`，表示数据长度没有上限。
* `INDEX_LENGTH`：索引长度。`INDEX_LENGTH` = `TABLE_ROWS` \* 索引元组中列的长度之和。不考虑 TiKV 的副本。
* `DATA_FREE`：数据碎片。当前值为 `0`。
* `AUTO_INCREMENT`：自增主键的当前步长。
* `CREATE_TIME`：表的创建时间。
* `UPDATE_TIME`：表的更新时间。
* `CHECK_TIME`：表的检查时间。
* `TABLE_COLLATION`：表中字符串的排序规则。
* `CHECKSUM`：校验和。
* `CREATE_OPTIONS`：创建选项。
* `TABLE_COMMENT`：表的注释和备注。

表中的大部分信息与 MySQL 相同。只有两列是 TiDB 新定义的：

* `TIDB_TABLE_ID`：表示表的内部 ID。此 ID 在 TiDB 集群中是唯一的。
* `TIDB_ROW_ID_SHARDING_INFO`：表示表的分片类型。可能的值如下：
    - `"NOT_SHARDED"`：表未分片。
    - `"NOT_SHARDED(PK_IS_HANDLE)"`：将整数主键定义为其行 ID 的表未分片。
    - `"PK_AUTO_RANDOM_BITS={bit_number}"`：将整数主键定义为其行 ID 的表已分片，因为主键被赋予了 `AUTO_RANDOM` 属性。
    - `"SHARD_BITS={bit_number}"`：使用 `SHARD_ROW_ID_BITS={bit_number}` 对表进行分片。
    - NULL：表是系统表或视图，因此无法分片。
