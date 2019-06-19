---
title: Information Schema
category: reference
aliases: ['/docs-cn/sql/information-schema/']
---

# Information Schema

为了和 MySQL 保持兼容，TiDB 支持很多 `INFORMATION\_SCHEMA` 表，其中有不少表都支持相应的 `SHOW` 命令。查询 `INFORMATION_SCHEMA` 表也为表的连接操作提供了可能。

## CHARACTER\_SETS Table

 `CHARACTER_SETS` 表提供[字符集](/dev/reference/sql/character-set.md)相关的信息。TiDB 默认支持并且只支持 utf8mb4。为与 MySQL 保持一致，表中也包含了其他字符集。

```sql
mysql> SELECT * FROM character_sets;
+--------------------+----------------------+---------------+--------+
| CHARACTER_SET_NAME | DEFAULT_COLLATE_NAME | DESCRIPTION   | MAXLEN |
+--------------------+----------------------+---------------+--------+
| utf8               | utf8_bin             | UTF-8 Unicode |      3 |
| utf8mb4            | utf8mb4_bin          | UTF-8 Unicode |      4 |
| ascii              | ascii_bin            | US ASCII      |      1 |
| latin1             | latin1_bin           | Latin1        |      1 |
| binary             | binary               | binary        |      1 |
+--------------------+----------------------+---------------+--------+
5 rows in set (0.00 sec)
```

## COLLATIONS Table

 `COLLATIONS` 表提供了 `CHARACTER_SETS` 表中字符集对应的排序规则列表。TiDB 当前仅支持二进制排序规则，包含该表仅为兼容 MySQL。

```sql
mysql> SELECT * FROM collations WHERE character_set_name='utf8mb4';
+------------------------+--------------------+------+------------+-------------+---------+
| COLLATION_NAME         | CHARACTER_SET_NAME | ID   | IS_DEFAULT | IS_COMPILED | SORTLEN |
+------------------------+--------------------+------+------------+-------------+---------+
| utf8mb4_general_ci     | utf8mb4            |   45 | Yes        | Yes         |       1 |
| utf8mb4_bin            | utf8mb4            |   46 |            | Yes         |       1 |
| utf8mb4_unicode_ci     | utf8mb4            |  224 |            | Yes         |       1 |
| utf8mb4_icelandic_ci   | utf8mb4            |  225 |            | Yes         |       1 |
| utf8mb4_latvian_ci     | utf8mb4            |  226 |            | Yes         |       1 |
| utf8mb4_romanian_ci    | utf8mb4            |  227 |            | Yes         |       1 |
| utf8mb4_slovenian_ci   | utf8mb4            |  228 |            | Yes         |       1 |
| utf8mb4_polish_ci      | utf8mb4            |  229 |            | Yes         |       1 |
| utf8mb4_estonian_ci    | utf8mb4            |  230 |            | Yes         |       1 |
| utf8mb4_spanish_ci     | utf8mb4            |  231 |            | Yes         |       1 |
| utf8mb4_swedish_ci     | utf8mb4            |  232 |            | Yes         |       1 |
| utf8mb4_turkish_ci     | utf8mb4            |  233 |            | Yes         |       1 |
| utf8mb4_czech_ci       | utf8mb4            |  234 |            | Yes         |       1 |
| utf8mb4_danish_ci      | utf8mb4            |  235 |            | Yes         |       1 |
| utf8mb4_lithuanian_ci  | utf8mb4            |  236 |            | Yes         |       1 |
| utf8mb4_slovak_ci      | utf8mb4            |  237 |            | Yes         |       1 |
| utf8mb4_spanish2_ci    | utf8mb4            |  238 |            | Yes         |       1 |
| utf8mb4_roman_ci       | utf8mb4            |  239 |            | Yes         |       1 |
| utf8mb4_persian_ci     | utf8mb4            |  240 |            | Yes         |       1 |
| utf8mb4_esperanto_ci   | utf8mb4            |  241 |            | Yes         |       1 |
| utf8mb4_hungarian_ci   | utf8mb4            |  242 |            | Yes         |       1 |
| utf8mb4_sinhala_ci     | utf8mb4            |  243 |            | Yes         |       1 |
| utf8mb4_german2_ci     | utf8mb4            |  244 |            | Yes         |       1 |
| utf8mb4_croatian_ci    | utf8mb4            |  245 |            | Yes         |       1 |
| utf8mb4_unicode_520_ci | utf8mb4            |  246 |            | Yes         |       1 |
| utf8mb4_vietnamese_ci  | utf8mb4            |  247 |            | Yes         |       1 |
+------------------------+--------------------+------+------------+-------------+---------+
26 rows in set (0.00 sec)
```

## COLLATION\_CHARACTER\_SET\_APPLICABILITY Table

`COLLATION_CHARACTER_SET_APPLICABILITY` 表将排序规则映射至适用的字符集名称。和 `COLLATIONS` 表一样，包含此表也是为了兼容 MySQL。

```sql
mysql> SELECT * FROM collation_character_set_applicability WHERE character_set_name='utf8mb4';
+------------------------+--------------------+
| COLLATION_NAME         | CHARACTER_SET_NAME |
+------------------------+--------------------+
| utf8mb4_general_ci     | utf8mb4            |
| utf8mb4_bin            | utf8mb4            |
| utf8mb4_unicode_ci     | utf8mb4            |
| utf8mb4_icelandic_ci   | utf8mb4            |
| utf8mb4_latvian_ci     | utf8mb4            |
| utf8mb4_romanian_ci    | utf8mb4            |
| utf8mb4_slovenian_ci   | utf8mb4            |
| utf8mb4_polish_ci      | utf8mb4            |
| utf8mb4_estonian_ci    | utf8mb4            |
| utf8mb4_spanish_ci     | utf8mb4            |
| utf8mb4_swedish_ci     | utf8mb4            |
| utf8mb4_turkish_ci     | utf8mb4            |
| utf8mb4_czech_ci       | utf8mb4            |
| utf8mb4_danish_ci      | utf8mb4            |
| utf8mb4_lithuanian_ci  | utf8mb4            |
| utf8mb4_slovak_ci      | utf8mb4            |
| utf8mb4_spanish2_ci    | utf8mb4            |
| utf8mb4_roman_ci       | utf8mb4            |
| utf8mb4_persian_ci     | utf8mb4            |
| utf8mb4_esperanto_ci   | utf8mb4            |
| utf8mb4_hungarian_ci   | utf8mb4            |
| utf8mb4_sinhala_ci     | utf8mb4            |
| utf8mb4_german2_ci     | utf8mb4            |
| utf8mb4_croatian_ci    | utf8mb4            |
| utf8mb4_unicode_520_ci | utf8mb4            |
| utf8mb4_vietnamese_ci  | utf8mb4            |
+------------------------+--------------------+
26 rows in set (0.00 sec)
```

## COLUMNS Table

COLUMNS 表提供了表的所有列的信息。

```sql
mysql> CREATE TABLE test.t1 (a int);
1 row in set (0.01 sec)
mysql> SELECT * FROM information_schema.columns WHERE table_schema='test' AND TABLE_NAME='t1'\G
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
1 row in set (0.01 sec)
```

对应的 `SHOW` 语句如下：

```sql
mysql> SHOW COLUMNS FROM t1 FROM test;
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)
```

## ENGINES Table

`ENGINES` 表提供了关于存储引擎的信息。从和 MySQL 兼容性上考虑，TiDB 会一直将 InnoDB 描述为唯一支持的引擎。

```sql
mysql> SELECT * FROM engines\G
*************************** 1. row ***************************
      ENGINE: InnoDB
     SUPPORT: DEFAULT
     COMMENT: Supports transactions, row-level locking, and foreign keys
TRANSACTIONS: YES
          XA: YES
  SAVEPOINTS: YES
1 row in set (0.00 sec)
```

## KEY\_COLUMN\_USAGE Table

`KEY_COLUMN_USAGE` 表描述了列的键约束，比如主键约束。

```sql
mysql> SELECT * FROM key_column_usage WHERE table_schema='mysql' and table_name='user'\G
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

## SCHEMATA Table

SCHEMATA 表提供了关于数据库的信息。表中的数据与 `SHOW DATABASES` 语句的执行结果等价。

```sql
mysql> SELECT * FROM schemata; 
+--------------+--------------------+----------------------------+------------------------+----------+ 
| CATALOG_NAME | SCHEMA_NAME        | DEFAULT_CHARACTER_SET_NAME | DEFAULT_COLLATION_NAME | SQL_PATH | 
+--------------+--------------------+----------------------------+------------------------+----------+ 
| def          | INFORMATION_SCHEMA | utf8mb4                    | utf8mb4_bin            | NULL     | 
| def          | mynewdb            | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | mysql              | utf8mb4                    | utf8mb4_bin            | NULL     | 
| def          | PERFORMANCE_SCHEMA | utf8mb4                    | utf8mb4_bin            | NULL     | 
| def          | test               | utf8mb4                    | utf8mb4_bin            | NULL     | 
+--------------+--------------------+----------------------------+------------------------+----------+ 
5 rows in set (0.00 sec)
```

## SESSION\_VARIABLES Table

`SESSION\_VARIABLES` 表提供了关于 session 变量的信息。表中的数据跟 `SHOW SESSION VARIABLES` 语句执行结果类似。

```sql
mysql> SELECT * FROM session_variables LIMIT 10;
+----------------------------------+----------------------+
| VARIABLE_NAME                    | VARIABLE_VALUE       |
+----------------------------------+----------------------+
| max_write_lock_count             | 18446744073709551615 |
| server_id_bits                   | 32                   |
| net_read_timeout                 | 30                   |
| innodb_online_alter_log_max_size | 134217728            |
| innodb_optimize_fulltext_only    | OFF                  |
| max_join_size                    | 18446744073709551615 |
| innodb_read_io_threads           | 4                    |
| session_track_gtids              | OFF                  |
| have_ssl                         | DISABLED             |
| max_binlog_cache_size            | 18446744073709547520 |
+----------------------------------+----------------------+
10 rows in set (0.00 sec)
```

## STATISTICS Table

 `STATISTICS` 表提供了关于表索引的信息。

```sql
mysql> desc statistics;
+---------------|---------------------|------|------|---------|-------+
| Field         | Type                | Null | Key  | Default | Extra |
+---------------|---------------------|------|------|---------|-------+
| TABLE_CATALOG | varchar(512)        | YES  |      | NULL    |       |
| TABLE_SCHEMA  | varchar(64)         | YES  |      | NULL    |       |
| TABLE_NAME    | varchar(64)         | YES  |      | NULL    |       |
| NON_UNIQUE    | varchar(1)          | YES  |      | NULL    |       |
| INDEX_SCHEMA  | varchar(64)         | YES  |      | NULL    |       |
| INDEX_NAME    | varchar(64)         | YES  |      | NULL    |       |
| SEQ_IN_INDEX  | bigint(2) UNSIGNED  | YES  |      | NULL    |       |
| COLUMN_NAME   | varchar(21)         | YES  |      | NULL    |       |
| COLLATION     | varchar(1)          | YES  |      | NULL    |       |
| CARDINALITY   | bigint(21) UNSIGNED | YES  |      | NULL    |       |
| SUB_PART      | bigint(3) UNSIGNED  | YES  |      | NULL    |       |
| PACKED        | varchar(10)         | YES  |      | NULL    |       |
| NULLABLE      | varchar(3)          | YES  |      | NULL    |       |
| INDEX_TYPE    | varchar(16)         | YES  |      | NULL    |       |
| COMMENT       | varchar(16)         | YES  |      | NULL    |       |
| INDEX_COMMENT | varchar(1024)       | YES  |      | NULL    |       |
+---------------|---------------------|------|------|---------|-------+
```

下列语句是等价的：

```sql
SELECT * FROM INFORMATION_SCHEMA.STATISTICS
  WHERE table_name = 'tbl_name'
  AND table_schema = 'db_name'

SHOW INDEX
  FROM tbl_name
  FROM db_name
```

## TABLES Table

`TABLES` 表提供了数据库里面关于表的信息。

```sql
mysql> SELECT * FROM tables WHERE table_schema='mysql' AND table_name='user'\G
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
 AUTO_INCREMENT: 0
    CREATE_TIME: 2019-03-29 09:17:27
    UPDATE_TIME: NULL
     CHECK_TIME: NULL
TABLE_COLLATION: utf8mb4_bin
       CHECKSUM: NULL
 CREATE_OPTIONS: 
  TABLE_COMMENT: 
  TIDB_TABLE_ID: 5
1 row in set (0.00 sec)
```

以下操作是等价的：

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

## TABLE\_CONSTRAINTS Table

`TABLE\_CONSTRAINTS` 表记录了表的约束信息。

```sql
mysql> SELECT * FROM table_constraints WHERE constraint_type='UNIQUE'\G
*************************** 1. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: name
      TABLE_SCHEMA: mysql
        TABLE_NAME: help_topic
   CONSTRAINT_TYPE: UNIQUE
*************************** 2. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: tbl
      TABLE_SCHEMA: mysql
        TABLE_NAME: stats_meta
   CONSTRAINT_TYPE: UNIQUE
*************************** 3. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: tbl
      TABLE_SCHEMA: mysql
        TABLE_NAME: stats_histograms
   CONSTRAINT_TYPE: UNIQUE
*************************** 4. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: tbl
      TABLE_SCHEMA: mysql
        TABLE_NAME: stats_buckets
   CONSTRAINT_TYPE: UNIQUE
*************************** 5. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: delete_range_index
      TABLE_SCHEMA: mysql
        TABLE_NAME: gc_delete_range
   CONSTRAINT_TYPE: UNIQUE
*************************** 6. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: delete_range_done_index
      TABLE_SCHEMA: mysql
        TABLE_NAME: gc_delete_range_done
   CONSTRAINT_TYPE: UNIQUE
6 rows in set (0.00 sec)
```

其中：

* `CONSTRAINT_TYPE` 的取值可以是 `UNIQUE`，`PRIMARY KEY`，或者 `FOREIGN KEY`。
* `UNIQUE` 和 `PRIMARY KEY` 信息与 `SHOW INDEX` 语句的执行结果类似。

## USER\_PRIVILEGES Table

USER\_PRIVILEGES 表提供了关于全局权限的信息。该表的数据根据 `mysql.user` 系统表生成。

```sql
mysql> desc USER_PRIVILEGES;
+----------------|--------------|------|------|---------|-------+
| Field          | Type         | Null | Key  | Default | Extra |
+----------------|--------------|------|------|---------|-------+
| GRANTEE        | varchar(81)  | YES  |      | NULL    |       |
| TABLE_CATALOG  | varchar(512) | YES  |      | NULL    |       |
| PRIVILEGE_TYPE | varchar(64)  | YES  |      | NULL    |       |
| IS_GRANTABLE   | varchar(3)   | YES  |      | NULL    |       |
+----------------|--------------|------|------|---------|-------+
4 rows in set (0.00 sec)
```

## VIEWS Table

`VIEWS` 表提供了关于 SQL 视图的信息。

```
mysql> create view test.v1 as select 1;
Query OK, 0 rows affected (0.00 sec)
mysql> select * from views\G
*************************** 1. row ***************************
       TABLE_CATALOG: def
        TABLE_SCHEMA: test
          TABLE_NAME: v1
     VIEW_DEFINITION: select 1
        CHECK_OPTION: CASCADED
        IS_UPDATABLE: NO
             DEFINER: root@127.0.0.1
       SECURITY_TYPE: DEFINER
CHARACTER_SET_CLIENT: utf8
COLLATION_CONNECTION: utf8_general_ci
1 row in set (0.00 sec)
```

## TIDB\_INDEXES

`TIDB_INDEXES` 表提供了 TiDB 中索引的一些信息。

```sql
mysql> show create table tidb_indexes\G
*************************** 1. row ***************************
       Table: TIDB_INDEXES
Create Table: CREATE TABLE `TIDB_INDEXES` (
  `TABLE_SCHEMA` varchar(64) DEFAULT NULL,
  `TABLE_NAME` varchar(64) DEFAULT NULL,
  `NON_UNIQUE` bigint(21) unsigned DEFAULT NULL,
  `KEY_NAME` varchar(64) DEFAULT NULL,
  `SEQ_IN_INDEX` bigint(21) unsigned DEFAULT NULL,
  `COLUMN_NAME` varchar(64) DEFAULT NULL,
  `SUB_PART` bigint(21) unsigned DEFAULT NULL,
  `INDEX_COMMENT` varchar(2048) DEFAULT NULL,
  `INDEX_ID` bigint(21) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

其中 `INDEX_ID` 是 TiDB 为每个索引分配的唯一 ID，这个 ID 也可以在其他系统表和 API 中获取。有了 `INDEX_ID` 后，可以和这个表做一些关联查询来获得更加有用的信息。
如，我们在 [SLOW_QUERY 表](#SLOW\_QUERY)中得到了某条 SQL 涉及的 `TABLE_ID` 以及 `INDEX_ID`，这时我们可以通过如下的 SQL 来获取索引的信息：

```sql
select
   tidb_indexes.*
from
   tidb_indexes,
   tables
where
   tidb_indexes.table_schema = tables.table_schema
   and tidb_indexes.table_name = tidb_indexes.table_name
   and tables.tidb_table_id = ?
   and index_id = ?
```

## TIDB\_HOT\_REGIONS Table

`TIDB_HOT_REGIONS` 表提供了当前 TiKV 中热点 region 的信息。

```sql
mysql> show create table tidb_hot_regions\G
*************************** 1. row ***************************
       Table: TIDB_HOT_REGIONS
Create Table: CREATE TABLE `TIDB_HOT_REGIONS` (
  `TABLE_ID` bigint(21) unsigned DEFAULT NULL,
  `INDEX_ID` bigint(21) unsigned DEFAULT NULL,
  `DB_NAME` varchar(64) DEFAULT NULL,
  `TABLE_NAME` varchar(64) DEFAULT NULL,
  `INDEX_NAME` varchar(64) DEFAULT NULL,
  `TYPE` varchar(64) DEFAULT NULL,
  `MAX_HOT_DEGREE` bigint(21) unsigned DEFAULT NULL,
  `REGION_COUNT` bigint(21) unsigned DEFAULT NULL,
  `FLOW_BYTES` bigint(21) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

其中，`TABLE_ID`, `INDEX_ID` 是 TiDB 为每个表和索引生成的 ID。
`TYPE` 是热点的类型，值可以是 `READ`, `WRITE` 两者之一。

## TIKV\_STORE\_STATUS

`TIKV_STORE_STATUS` 表通过 PD 的 API，展示了 TiKV 节点的一些基本信息。

```sql
mysql> show create table tikv_store_status\G
*************************** 1. row ***************************
       Table: TIKV_STORE_STATUS
Create Table: CREATE TABLE `TIKV_STORE_STATUS` (
  `STORE_ID` bigint(21) unsigned DEFAULT NULL,
  `ADDRESS` varchar(64) DEFAULT NULL,
  `STORE_STATE` bigint(21) unsigned DEFAULT NULL,
  `STORE_STATE_NAME` varchar(64) DEFAULT NULL,
  `LABEL` json unsigned DEFAULT NULL,
  `VERSION` varchar(64) DEFAULT NULL,
  `CAPACITY` varchar(64) DEFAULT NULL,
  `AVAILABLE` varchar(64) DEFAULT NULL,
  `LEADER_COUNT` bigint(21) unsigned DEFAULT NULL,
  `LEADER_WEIGHT` bigint(21) unsigned DEFAULT NULL,
  `LEADER_SCORE` bigint(21) unsigned DEFAULT NULL,
  `LEADER_SIZE` bigint(21) unsigned DEFAULT NULL,
  `REGION_COUNT` bigint(21) unsigned DEFAULT NULL,
  `REGION_WEIGHT` bigint(21) unsigned DEFAULT NULL,
  `REGION_SCORE` bigint(21) unsigned DEFAULT NULL,
  `REGION_SIZE` bigint(21) unsigned DEFAULT NULL,
  `START_TS` datetime unsigned DEFAULT NULL,
  `LAST_HEARTBEAT_TS` datetime unsigned DEFAULT NULL,
  `UPTIME` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.01 sec)
```

## TIKV\_REGION\_STATUS

`TIKV_REGION_STATUS` 表通过 PD 的 API，展示 TiKV 中 Region 的一些基础信息。

```sql
mysql> show create table tikv_region_status\G
*************************** 1. row ***************************
       Table: TIKV_REGION_STATUS
Create Table: CREATE TABLE `TIKV_REGION_STATUS` (
  `REGION_ID` bigint(21) unsigned DEFAULT NULL,
  `START_KEY` text DEFAULT NULL,
  `END_KEY` text DEFAULT NULL,
  `EPOCH_CONF_VER` bigint(21) unsigned DEFAULT NULL,
  `EPOCH_VERSION` bigint(21) unsigned DEFAULT NULL,
  `WRITTEN_BYTES` bigint(21) unsigned DEFAULT NULL,
  `READ_BYTES` bigint(21) unsigned DEFAULT NULL,
  `APPROXIMATE_SIZE` bigint(21) unsigned DEFAULT NULL,
  `APPROXIMATE_KEYS` bigint(21) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

通过在列 `EPOCH_CONF_VER`, `WRITTEN_BYTES`, `READ_BYTES` 等列上做 `ORDER BY X LIMIT Y` 操作，可以实现 PD-CTL 中 `top confver`, `top read`, `top write` 等操作。如要找写入量最大的 3 个 region，可以用如下的 SQL 实现：

```
select * from tikv_region_status order by written_bytes desc limit 3;
```

## TIKV\_REGION\_PEERS

`TIKV_REGION_PEERS` 通过 PD 的 API，展示了 TikV 中 单个 Region 节点的一些详细信息。诸如是否是 learner，是否是 leader 等。

```sql
mysql> show create table tikv_region_peers\G
*************************** 1. row ***************************
       Table: TIKV_REGION_PEERS
Create Table: CREATE TABLE `TIKV_REGION_PEERS` (
  `REGION_ID` bigint(21) unsigned DEFAULT NULL,
  `PEER_ID` bigint(21) unsigned DEFAULT NULL,
  `STORE_ID` bigint(21) unsigned DEFAULT NULL,
  `IS_LEARNER` tinyint(1) unsigned DEFAULT NULL,
  `IS_LEADER` tinyint(1) unsigned DEFAULT NULL,
  `STATUS` varchar(10) DEFAULT NULL,
  `DOWN_SECONDS` bigint(21) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

如，我们想要知道 `WRITTEN_BYTES` 最高的三个 region 分别在哪些 TiKV 上，可以通过如下的 SQL 实现：

```sql
select
   address,
   tikv.address,
   region.region_id,
from
   tikv_store_status tikv,
   tikv_region_peers peer,
   (
      select
         *
      from
         tikv_region_status region
      order by
         written_bytes desc limit 3
   )
   region
where
   region.region_id = peer.region_id
   and peer.is_leader = 1
   and peer.store_id = tikv.region_id
```

## ANALYZE\_STATUS

`ANALYZE_STATUS` 表展示了当前集群 `ANALYZE` 命令的执行情况。

```sql
mysql> show create table analyze_status\G
*************************** 1. row ***************************
       Table: ANALYZE_STATUS
Create Table: CREATE TABLE `ANALYZE_STATUS` (
  `TABLE_SCHEMA` varchar(64) DEFAULT NULL,
  `TABLE_NAME` varchar(64) DEFAULT NULL,
  `PARTITION_NAME` varchar(64) DEFAULT NULL,
  `JOB_INFO` varchar(64) DEFAULT NULL,
  `PROCESSED_ROWS` bigint(20) unsigned DEFAULT NULL,
  `START_TIME` datetime unsigned DEFAULT NULL,
  `STATE` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

其中 STATE 列表明了一个具体的 analyze 任务的执行情况，可能有如下四个值 `pending`, `running`, `finished`, `failed`。

## SLOW\_QUERY

`SLOW_QUERY` 表是映射了慢查询日志的表。其列名均和慢查询日志中的字段名一一对应。具体信息可以查看[慢查询日志](../../how-to/maintain/identify-slow-queries.md)

```sql
mysql> show create table slow_query\G
*************************** 1. row ***************************
       Table: SLOW_QUERY
Create Table: CREATE TABLE `SLOW_QUERY` (
  `Time` timestamp unsigned NULL DEFAULT NULL,
  `Txn_start_ts` bigint(20) unsigned DEFAULT NULL,
  `User` varchar(64) DEFAULT NULL,
  `Host` varchar(64) DEFAULT NULL,
  `Conn_ID` bigint(20) unsigned DEFAULT NULL,
  `Query_time` double unsigned DEFAULT NULL,
  `Process_time` double unsigned DEFAULT NULL,
  `Wait_time` double unsigned DEFAULT NULL,
  `Backoff_time` double unsigned DEFAULT NULL,
  `Request_count` bigint(20) unsigned DEFAULT NULL,
  `Total_keys` bigint(20) unsigned DEFAULT NULL,
  `Process_keys` bigint(20) unsigned DEFAULT NULL,
  `DB` varchar(64) DEFAULT NULL,
  `Index_ids` varchar(100) DEFAULT NULL,
  `Is_internal` tinyint(1) unsigned DEFAULT NULL,
  `Digest` varchar(64) DEFAULT NULL,
  `Stats` varchar(512) DEFAULT NULL,
  `Cop_proc_avg` double unsigned DEFAULT NULL,
  `Cop_proc_p90` double unsigned DEFAULT NULL,
  `Cop_proc_max` double unsigned DEFAULT NULL,
  `Cop_proc_addr` varchar(64) DEFAULT NULL,
  `Cop_wait_avg` double unsigned DEFAULT NULL,
  `Cop_wait_p90` double unsigned DEFAULT NULL,
  `Cop_wait_max` double unsigned DEFAULT NULL,
  `Cop_wait_addr` varchar(64) DEFAULT NULL,
  `Mem_max` bigint(20) unsigned DEFAULT NULL,
  `Query` varchar(4096) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

## 不支持的 Information Schema 表

TiDB 包含以下 `INFORMATION_SCHEMA` 表，但仅会返回空行：

* `COLUMN_PRIVILEGES`
* `EVENTS`
* `FILES`
* `GLOBAL_STATUS`
* `GLOBAL_VARIABLES`
* `OPTIMIZER_TRACE`
* `PARAMETERS`
* `PARTITIONS`
* `PLUGINS`
* `PROFILING`
* `REFERENTIAL_CONSTRAINTS`
* `ROUTINES`
* `SCHEMA_PRIVILEGES`
* `SESSION_STATUS`
* `TABLESPACES`
* `TABLE_PRIVILEGES`
* `TRIGGERS`
