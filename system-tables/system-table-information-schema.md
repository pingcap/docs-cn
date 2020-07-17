---
title: Information Schema
summary: Learn how to use Information Schema in TiDB.
aliases: ['/docs/dev/system-tables/system-table-information-schema/','/docs/dev/reference/system-databases/information-schema/']
---

# Information Schema

As part of MySQL compatibility, TiDB supports a number of `INFORMATION_SCHEMA` tables. Many of these tables also have a corresponding `SHOW` command. The benefit of querying `INFORMATION_SCHEMA` is that it is possible to join between tables.

## Fully Supported Information Schema Tables

### ANALYZE_STATUS table

The `ANALYZE_STATUS` table provides information about the running tasks that collect statistics and a limited number of history tasks.

{{< copyable "sql" >}}

```sql
select * from `ANALYZE_STATUS`;
```

```sql
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| TABLE_SCHEMA | TABLE_NAME | PARTITION_NAME | JOB_INFO          | PROCESSED_ROWS | START_TIME          | STATE    |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| test         | t          |                | analyze index idx | 2              | 2019-06-21 19:51:14 | finished |
| test         | t          |                | analyze columns   | 2              | 2019-06-21 19:51:14 | finished |
| test         | t1         | p0             | analyze columns   | 0              | 2019-06-21 19:51:15 | finished |
| test         | t1         | p3             | analyze columns   | 0              | 2019-06-21 19:51:15 | finished |
| test         | t1         | p1             | analyze columns   | 0              | 2019-06-21 19:51:15 | finished |
| test         | t1         | p2             | analyze columns   | 1              | 2019-06-21 19:51:15 | finished |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
6 rows in set
```

### CHARACTER_SETS table

The `CHARACTER_SETS` table provides information about [character sets](/character-set-and-collation.md). Currently, TiDB only supports some of the character sets.

{{< copyable "sql" >}}

```sql
SELECT * FROM character_sets;
```

```sql
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

### COLLATIONS table

The `COLLATIONS` table provides a list of collations that correspond to character sets in the `CHARACTER_SETS` table.  Currently this table is included only for compatibility with MySQL, as TiDB only supports binary collation:

{{< copyable "sql" >}}

```sql
SELECT * FROM collations WHERE character_set_name='utf8mb4';
```

```sql
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

### COLLATION_CHARACTER_SET_APPLICABILITY table

The `COLLATION_CHARACTER_SET_APPLICABILITY` table maps collations to the applicable character set name.  Similar to the `COLLATIONS` table, it is included only for compatibility with MySQL:

{{< copyable "sql" >}}

```sql
SELECT * FROM collation_character_set_applicability WHERE character_set_name='utf8mb4';
```

```sql
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

### COLUMNS table

The `COLUMNS` table provides detailed information about columns in tables:

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t1 (a int);
```

```sql
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.columns WHERE table_schema='test' AND TABLE_NAME='t1';
```

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
1 row in set (0.01 sec)
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

{{< copyable "sql" >}}

```sql
SHOW COLUMNS FROM t1 FROM test;
```

```sql
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)
```

### ENGINES table

The `ENGINES` table provides information about storage engines. For compatibility, TiDB will always describe InnoDB as the only supported engine. In addition, other column values in the `ENGINES` table are also fixed values.

{{< copyable "sql" >}}

```sql
SELECT * FROM engines;
```

```sql
*************************** 1. row ***************************
      ENGINE: InnoDB
     SUPPORT: DEFAULT
     COMMENT: Supports transactions, row-level locking, and foreign keys
TRANSACTIONS: YES
          XA: YES
  SAVEPOINTS: YES
1 row in set (0.00 sec)
```

The description of columns in the `ENGINES` table is as follows:

* `ENGINES`: The name of the storage engine.
* `SUPPORT`: The level of support that the server has on the storage engine. In TiDB, the value is always `DEFAULT`.
* `COMMENT`: The brief comment on the storage engine.
* `TRANSACTIONS`：Whether the storage engine supports transactions.
* `XA`: Whether the storage engine supports XA transactions.
* `SAVEPOINTS`: Whether the storage engine supports `savepoints`.

### KEY_COLUMN_USAGE table

The `KEY_COLUMN_USAGE` table describes the key constraints of the columns, such as the primary key constraint:

{{< copyable "sql" >}}

```sql
SELECT * FROM key_column_usage WHERE table_schema='mysql' and table_name='user';
```

```sql
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

The description of columns in the `KEY_COLUMN_USAGE` table is as follows:

* `CONSTRAINT_CATALOG`: The name of the catalog to which the constraint belongs. The value is always `def`.
* `CONSTRAINT_SCHEMA`: The name of the schema to which the constraint belongs.
* `CONSTRAINT_NAME`: The name of the constraint.
* `TABLE_CATALOG`: The name of the catalog to which the table belongs. The value is always `def`.
* `TABLE_SCHEMA`: The name of the schema to which the table belongs.
* `TABLE_NAME`: The name of the table with constraints.
* `COLUMN_NAME`: The name of the column with constraints.
* `ORDINAL_POSITION`: The position of the column in the constraint, rather than in the table. The position number starts from `1`.
* `POSITION_IN_UNIQUE_CONSTRAINT`: The unique constraint and the primary key constraint are empty. For foreign key constraints, this column is the position of the referenced table's key.
* `REFERENCED_TABLE_SCHEMA`: The name of the schema referenced by the constraint. Currently in TiDB, the value of this column in all constraints is `nil`, except for the foreign key constraint.
* `REFERENCED_TABLE_NAME`: The name of the table referenced by the constraint. Currently in TiDB, the value of this column in all constraints is `nil`, except for the foreign key constraint.
* `REFERENCED_COLUMN_NAME`: The name of the column referenced by the constraint. Currently in TiDB, the value of this column in all constraints is `nil`, except for the foreign key constraint.

### PROCESSLIST table

`PROCESSLIST`, just like `show processlist`, is used to view the requests that are being handled.

The `PROCESSLIST` table has a `MEM` column that `show processlist` does not have. `MEM` means the occupied memory of the requests being handled, and its unit is `byte`.

```sql
+----+------+------+--------------------+---------+------+-------+---------------------------+-----+
| ID | USER | HOST | DB                 | COMMAND | TIME | STATE | INFO                      | MEM |
+----+------+------+--------------------+---------+------+-------+---------------------------+-----+
| 1  | root | ::1  | INFORMATION_SCHEMA | Query   | 0    | 2     | select * from PROCESSLIST | 0   |
+----+------+------+--------------------+---------+------+-------+---------------------------+-----+
```

### SCHEMATA table

The `SCHEMATA` table provides information about databases. The table data is equivalent to the result of the `SHOW DATABASES` statement:

{{< copyable "sql" >}}

```sql
select * from SCHEMATA;
```

```sql
*************************** 1. row ***************************
              CATALOG_NAME: def
               SCHEMA_NAME: INFORMATION_SCHEMA
DEFAULT_CHARACTER_SET_NAME: utf8mb4
    DEFAULT_COLLATION_NAME: utf8mb4_bin
                  SQL_PATH: NULL
*************************** 2. row ***************************
              CATALOG_NAME: def
               SCHEMA_NAME: mysql
DEFAULT_CHARACTER_SET_NAME: utf8mb4
    DEFAULT_COLLATION_NAME: utf8mb4_bin
                  SQL_PATH: NULL
*************************** 3. row ***************************
              CATALOG_NAME: def
               SCHEMA_NAME: PERFORMANCE_SCHEMA
DEFAULT_CHARACTER_SET_NAME: utf8mb4
    DEFAULT_COLLATION_NAME: utf8mb4_bin
                  SQL_PATH: NULL
*************************** 4. row ***************************
              CATALOG_NAME: def
               SCHEMA_NAME: test
DEFAULT_CHARACTER_SET_NAME: utf8mb4
    DEFAULT_COLLATION_NAME: utf8mb4_bin
                  SQL_PATH: NULL
4 rows in set (0.00 sec)
```

## CLUSTER_PROCESSLIST

`CLUSTER_PROCESSLIST` is the cluster system table corresponding to `PROCESSLIST`. It is used to query the `PROCESSLIST` information of all TiDB nodes in the cluster. The table schema of `CLUSTER_PROCESSLIST` has one more column than `PROCESSLIST`, the `INSTANCE` column, which stores the address of the TiDB node this row of data is from.

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.cluster_processlist;
```

```sql
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
| INSTANCE        | ID  | USER | HOST     | DB   | COMMAND | TIME | STATE      | INFO                                                 | MEM | TxnStart                               |
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
| 10.0.1.22:10080 | 150 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077223) |
| 10.0.1.22:10080 | 138 | root | 10.0.1.1 | test | Query   | 0    | autocommit | SELECT * FROM information_schema.cluster_processlist | 0   | 05-28 03:54:21.230(416976223923077220) |
| 10.0.1.22:10080 | 151 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077224) |
| 10.0.1.21:10080 | 15  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077222) |
| 10.0.1.21:10080 | 14  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077225) |
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
```

### SESSION_VARIABLES table

The `SESSION_VARIABLES` table provides information about session variables. The table data is similar to the result of the `SHOW SESSION VARIABLES` statement:

{{< copyable "sql" >}}

```sql
SELECT * FROM session_variables LIMIT 10;
```

```sql
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

## SLOW_QUERY table

The `SLOW_QUERY` table provides the slow query information of the current node, which is the parsing result of the TiDB slow log file. The column names in the table are corresponding to the field names in the slow log. For how to use this table to identify problematic statements and improve query performance, see [Slow Query Log Document](/identify-slow-queries.md).

{{< copyable "sql" >}}

```sql
desc information_schema.slow_query;
```

```sql
+---------------------------+---------------------+------+-----+---------+-------+
| Field                     | Type                | Null | Key | Default | Extra |
+---------------------------+---------------------+------+-----+---------+-------+
| Time                      | timestamp unsigned  | YES  |     | <null>  |       |
| Txn_start_ts              | bigint(20) unsigned | YES  |     | <null>  |       |
| User                      | varchar(64)         | YES  |     | <null>  |       |
| Host                      | varchar(64)         | YES  |     | <null>  |       |
| Conn_ID                   | bigint(20) unsigned | YES  |     | <null>  |       |
| Query_time                | double unsigned     | YES  |     | <null>  |       |
| Parse_time                | double unsigned     | YES  |     | <null>  |       |
| Compile_time              | double unsigned     | YES  |     | <null>  |       |
| Prewrite_time             | double unsigned     | YES  |     | <null>  |       |
| Wait_prewrite_binlog_time | double unsigned     | YES  |     | <null>  |       |
| Commit_time               | double unsigned     | YES  |     | <null>  |       |
| Get_commit_ts_time        | double unsigned     | YES  |     | <null>  |       |
| Commit_backoff_time       | double unsigned     | YES  |     | <null>  |       |
| Backoff_types             | varchar(64)         | YES  |     | <null>  |       |
| Resolve_lock_time         | double unsigned     | YES  |     | <null>  |       |
| Local_latch_wait_time     | double unsigned     | YES  |     | <null>  |       |
| Write_keys                | bigint(22) unsigned | YES  |     | <null>  |       |
| Write_size                | bigint(22) unsigned | YES  |     | <null>  |       |
| Prewrite_region           | bigint(22) unsigned | YES  |     | <null>  |       |
| Txn_retry                 | bigint(22) unsigned | YES  |     | <null>  |       |
| Process_time              | double unsigned     | YES  |     | <null>  |       |
| Wait_time                 | double unsigned     | YES  |     | <null>  |       |
| Backoff_time              | double unsigned     | YES  |     | <null>  |       |
| LockKeys_time             | double unsigned     | YES  |     | <null>  |       |
| Request_count             | bigint(20) unsigned | YES  |     | <null>  |       |
| Total_keys                | bigint(20) unsigned | YES  |     | <null>  |       |
| Process_keys              | bigint(20) unsigned | YES  |     | <null>  |       |
| DB                        | varchar(64)         | YES  |     | <null>  |       |
| Index_names               | varchar(100)        | YES  |     | <null>  |       |
| Is_internal               | tinyint(1) unsigned | YES  |     | <null>  |       |
| Digest                    | varchar(64)         | YES  |     | <null>  |       |
| Stats                     | varchar(512)        | YES  |     | <null>  |       |
| Cop_proc_avg              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_p90              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_max              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_addr             | varchar(64)         | YES  |     | <null>  |       |
| Cop_wait_avg              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_p90              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_max              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_addr             | varchar(64)         | YES  |     | <null>  |       |
| Mem_max                   | bigint(20) unsigned | YES  |     | <null>  |       |
| Succ                      | tinyint(1) unsigned | YES  |     | <null>  |       |
| Plan_from_cache           | tinyint(1)          | YES  |     | <null>  |       |
| Plan                      | longblob unsigned   | YES  |     | <null>  |       |
| Plan_digest               | varchar(128)        | YES  |     | <null>  |       |
| Prev_stmt                 | longblob unsigned   | YES  |     | <null>  |       |
| Query                     | longblob unsigned   | YES  |     | <null>  |       |
+---------------------------+---------------------+------+-----+---------+-------+
```

## CLUSTER_SLOW_QUERY table

The `CLUSTER_SLOW_QUERY` table provides the slow query information of all nodes in the cluster, which is the parsing result of the TiDB slow log files. You can use the `CLUSTER_SLOW_QUERY` table the way you do with [`SLOW_QUERY`](#slow_query-table). The table schema of the `CLUSTER_SLOW_QUERY` table differs from that of the `SLOW_QUERY` table in that an `INSTANCE` column is added to `CLUSTER_SLOW_QUERY`. The `INSTANCE` column represents the TiDB node address of the row information on the slow query. For how to use this table to identify problematic statements and improve query performance, see [Slow Query Log Document](/identify-slow-queries.md).

{{< copyable "sql" >}}

```sql
desc information_schema.cluster_slow_query;
```

```sql
+---------------------------+---------------------+------+-----+---------+-------+
| Field                     | Type                | Null | Key | Default | Extra |
+---------------------------+---------------------+------+-----+---------+-------+
| INSTANCE                  | varchar(64)         | YES  |     | <null>  |       |
| Time                      | timestamp unsigned  | YES  |     | <null>  |       |
| Txn_start_ts              | bigint(20) unsigned | YES  |     | <null>  |       |
| User                      | varchar(64)         | YES  |     | <null>  |       |
| Host                      | varchar(64)         | YES  |     | <null>  |       |
| Conn_ID                   | bigint(20) unsigned | YES  |     | <null>  |       |
| Query_time                | double unsigned     | YES  |     | <null>  |       |
| Parse_time                | double unsigned     | YES  |     | <null>  |       |
| Compile_time              | double unsigned     | YES  |     | <null>  |       |
| Prewrite_time             | double unsigned     | YES  |     | <null>  |       |
| Wait_prewrite_binlog_time | double unsigned     | YES  |     | <null>  |       |
| Commit_time               | double unsigned     | YES  |     | <null>  |       |
| Get_commit_ts_time        | double unsigned     | YES  |     | <null>  |       |
| Commit_backoff_time       | double unsigned     | YES  |     | <null>  |       |
| Backoff_types             | varchar(64)         | YES  |     | <null>  |       |
| Resolve_lock_time         | double unsigned     | YES  |     | <null>  |       |
| Local_latch_wait_time     | double unsigned     | YES  |     | <null>  |       |
| Write_keys                | bigint(22) unsigned | YES  |     | <null>  |       |
| Write_size                | bigint(22) unsigned | YES  |     | <null>  |       |
| Prewrite_region           | bigint(22) unsigned | YES  |     | <null>  |       |
| Txn_retry                 | bigint(22) unsigned | YES  |     | <null>  |       |
| Process_time              | double unsigned     | YES  |     | <null>  |       |
| Wait_time                 | double unsigned     | YES  |     | <null>  |       |
| Backoff_time              | double unsigned     | YES  |     | <null>  |       |
| LockKeys_time             | double unsigned     | YES  |     | <null>  |       |
| Request_count             | bigint(20) unsigned | YES  |     | <null>  |       |
| Total_keys                | bigint(20) unsigned | YES  |     | <null>  |       |
| Process_keys              | bigint(20) unsigned | YES  |     | <null>  |       |
| DB                        | varchar(64)         | YES  |     | <null>  |       |
| Index_names               | varchar(100)        | YES  |     | <null>  |       |
| Is_internal               | tinyint(1) unsigned | YES  |     | <null>  |       |
| Digest                    | varchar(64)         | YES  |     | <null>  |       |
| Stats                     | varchar(512)        | YES  |     | <null>  |       |
| Cop_proc_avg              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_p90              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_max              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_addr             | varchar(64)         | YES  |     | <null>  |       |
| Cop_wait_avg              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_p90              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_max              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_addr             | varchar(64)         | YES  |     | <null>  |       |
| Mem_max                   | bigint(20) unsigned | YES  |     | <null>  |       |
| Succ                      | tinyint(1) unsigned | YES  |     | <null>  |       |
| Plan_from_cache           | tinyint(1)          | YES  |     | <null>  |       |
| Plan                      | longblob unsigned   | YES  |     | <null>  |       |
| Plan_digest               | varchar(128)        | YES  |     | <null>  |       |
| Prev_stmt                 | longblob unsigned   | YES  |     | <null>  |       |
| Query                     | longblob unsigned   | YES  |     | <null>  |       |
+---------------------------+---------------------+------+-----+---------+-------+
```

When the cluster system table is queried, TiDB does not obtain data from all nodes, but pushes down the related calculation to other nodes. The execution plan is as follows:

{{< copyable "sql" >}}

```sql
desc select count(*) from information_schema.cluster_slow_query where user = 'u1';
```

```sql
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| id                       | estRows  | task      | access object            | operator info                                        |
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| StreamAgg_20             | 1.00     | root      |                          | funcs:count(Column#53)->Column#51                    |
| └─TableReader_21         | 1.00     | root      |                          | data:StreamAgg_9                                     |
|   └─StreamAgg_9          | 1.00     | cop[tidb] |                          | funcs:count(1)->Column#53                            |
|     └─Selection_19       | 10.00    | cop[tidb] |                          | eq(information_schema.cluster_slow_query.user, "u1") |
|       └─TableFullScan_18 | 10000.00 | cop[tidb] | table:CLUSTER_SLOW_QUERY | keep order:false, stats:pseudo                       |
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
```

In the above execution plan, the `user = u1` condition is pushed down to other (`cop`) TiDB nodes, and the aggregate operator is also pushed down (the `StreamAgg` operator in the graph).

Currently, because statistics of the system tables are not collected, sometimes some aggregation operators cannot be pushed down, which results in slow execution. In this case, you can manually specify the SQL HINT to push down the aggregation operators. For example:

{{< copyable "sql" >}}

```sql
select /*+ AGG_TO_COP() */ count(*) from information_schema.cluster_slow_query group by user;
```

### STATISTICS table

The `STATISTICS` table provides information about table indexes:

{{< copyable "sql" >}}

```sql
desc statistics;
```

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| TABLE_CATALOG | varchar(512)  | YES  |      | NULL    |       |
| TABLE_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| TABLE_NAME    | varchar(64)   | YES  |      | NULL    |       |
| NON_UNIQUE    | varchar(1)    | YES  |      | NULL    |       |
| INDEX_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| INDEX_NAME    | varchar(64)   | YES  |      | NULL    |       |
| SEQ_IN_INDEX  | bigint(2)     | YES  |      | NULL    |       |
| COLUMN_NAME   | varchar(21)   | YES  |      | NULL    |       |
| COLLATION     | varchar(1)    | YES  |      | NULL    |       |
| CARDINALITY   | bigint(21)    | YES  |      | NULL    |       |
| SUB_PART      | bigint(3)     | YES  |      | NULL    |       |
| PACKED        | varchar(10)   | YES  |      | NULL    |       |
| NULLABLE      | varchar(3)    | YES  |      | NULL    |       |
| INDEX_TYPE    | varchar(16)   | YES  |      | NULL    |       |
| COMMENT       | varchar(16)   | YES  |      | NULL    |       |
| INDEX_COMMENT | varchar(1024) | YES  |      | NULL    |       |
| IS_VISIBLE    | varchar(3)    | YES  |      | NULL    |       |
| Expression    | varchar(64)   | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
```

The following statements are equivalent:

```sql
SELECT * FROM INFORMATION_SCHEMA.STATISTICS
  WHERE table_name = 'tbl_name'
  AND table_schema = 'db_name'

SHOW INDEX
  FROM tbl_name
  FROM db_name
```

### TABLES table

The `TABLES` table provides information about tables in databases:

{{< copyable "sql" >}}

```sql
SELECT * FROM tables WHERE table_schema='mysql' AND table_name='user';
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
           AUTO_INCREMENT: 0
              CREATE_TIME: 2019-03-29 09:17:27
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

Most of the information in the table is the same as MySQL. Only two columns are newly defined by TiDB:

* `TIDB_TABLE_ID`: to indicate the internal ID of a table. This ID is unique in a TiDB cluster.
* `TIDDB_ROW_ID_SHARDING_INFO`: to indicate the sharding type of a table. The possible values are as follows:
    - `"NOT_SHARDED"`: the table is not sharded.
    - `"NOT_SHARDED(PK_IS_HANDLE)"`: the table that defines an integer Primary Key as its row id is not sharded.
    - `"PK_AUTO_RANDOM_BITS={bit_number}"`: the table that defines an integer Primary Key as its row id is sharded because the Primary Key is assigned with `AUTO_RANDOM` attribute.
    - `"SHARD_BITS={bit_number}"`: the table is sharded using `SHARD_ROW_ID_BITS={bit_number}`.
    - NULL: the table is a system table or view, and thus cannot be sharded.

### TABLE_CONSTRAINTS table

The `TABLE_CONSTRAINTS` table describes which tables have constraints:

{{< copyable "sql" >}}

```sql
SELECT * FROM table_constraints WHERE constraint_type='UNIQUE';
```

```sql
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

- The `CONSTRAINT_TYPE` value can be `UNIQUE`, `PRIMARY KEY`, or `FOREIGN KEY`.
- The `UNIQUE` and `PRIMARY KEY` information is similar to the result of the `SHOW INDEX` statement.

### TIDB_HOT_REGIONS table

The `TIDB_HOT_REGIONS` table provides information about hotspot Regions.

{{< copyable "sql" >}}

```sql
desc TIDB_HOT_REGIONS;
```

```sql
+----------------+---------------------+------+-----+---------+-------+
| Field          | Type                | Null | Key | Default | Extra |
+----------------+---------------------+------+-----+---------+-------+
| TABLE_ID       | bigint(21) unsigned | YES  |     | <null>  |       |
| INDEX_ID       | bigint(21) unsigned | YES  |     | <null>  |       |
| DB_NAME        | varchar(64)         | YES  |     | <null>  |       |
| TABLE_NAME     | varchar(64)         | YES  |     | <null>  |       |
| INDEX_NAME     | varchar(64)         | YES  |     | <null>  |       |
| TYPE           | varchar(64)         | YES  |     | <null>  |       |
| MAX_HOT_DEGREE | bigint(21) unsigned | YES  |     | <null>  |       |
| REGION_COUNT   | bigint(21) unsigned | YES  |     | <null>  |       |
| FLOW_BYTES     | bigint(21) unsigned | YES  |     | <null>  |       |
+----------------+---------------------+------+-----+---------+-------+
```

### TIDB_INDEXES table

The `TIDB_INDEXES` table provides the INDEX information of all tables.

{{< copyable "sql" >}}

```sql
desc TIDB_INDEXES;
```

```sql
+---------------+---------------------+------+-----+---------+-------+
| Field         | Type                | Null | Key | Default | Extra |
+---------------+---------------------+------+-----+---------+-------+
| TABLE_SCHEMA  | varchar(64)         | YES  |     | <null>  |       |
| TABLE_NAME    | varchar(64)         | YES  |     | <null>  |       |
| NON_UNIQUE    | bigint(21) unsigned | YES  |     | <null>  |       |
| KEY_NAME      | varchar(64)         | YES  |     | <null>  |       |
| SEQ_IN_INDEX  | bigint(21) unsigned | YES  |     | <null>  |       |
| COLUMN_NAME   | varchar(64)         | YES  |     | <null>  |       |
| SUB_PART      | bigint(21) unsigned | YES  |     | <null>  |       |
| INDEX_COMMENT | varchar(2048)       | YES  |     | <null>  |       |
| INDEX_ID      | bigint(21) unsigned | YES  |     | <null>  |       |
+---------------+---------------------+------+-----+---------+-------+
```

Fields in the `TIDB_INDEXES` table are described as follows:

* `TABLE_SCHEMA`: The name of the schema to which the index belongs.
* `TABLE_NAME`: The name of the table to which the index belongs.
* `NON_UNIQUE`: If the index is unique, the value is `0`; otherwise, the value is `1`.
* `KEY_NAME`: The index name. If the index is the primary key, the name is `PRIMARY`.
* `SEQ_IN_INDEX`: The sequential number of columns in the index, which starts from `1`.
* `COLUMN_NAME`: The name of the column where the index is located.
* `SUB_PART`: The prefix length of the index. If the the column is partly indexed, the `SUB_PART` value is the count of the indexed characters; otherwise, the value is `NULL`.
* `INDEX_COMMENT`: The comment of the index, which is made when the index is created.
* `INDEX_ID`: The index ID.

### TIKV_REGION_PEERS table

The `TIKV_REGION_PEERS` table provides the peer information of all Regions.

{{< copyable "sql" >}}

```sql
desc TIKV_REGION_PEERS;
```

```sql
+--------------+---------------------+------+-----+---------+-------+
| Field        | Type                | Null | Key | Default | Extra |
+--------------+---------------------+------+-----+---------+-------+
| REGION_ID    | bigint(21) unsigned | YES  |     | <null>  |       |
| PEER_ID      | bigint(21) unsigned | YES  |     | <null>  |       |
| STORE_ID     | bigint(21) unsigned | YES  |     | <null>  |       |
| IS_LEARNER   | tinyint(1) unsigned | YES  |     | <null>  |       |
| IS_LEADER    | tinyint(1) unsigned | YES  |     | <null>  |       |
| STATUS       | varchar(10)         | YES  |     | <null>  |       |
| DOWN_SECONDS | bigint(21) unsigned | YES  |     | <null>  |       |
+--------------+---------------------+------+-----+---------+-------+
```

### TIKV_REGION_STATUS table

The `TIKV_REGION_STATUS` table provides the status information of all Regions.

{{< copyable "sql" >}}

```sql
desc TIKV_REGION_STATUS;
```

```sql
+------------------+---------------------+------+-----+---------+-------+
| Field            | Type                | Null | Key | Default | Extra |
+------------------+---------------------+------+-----+---------+-------+
| REGION_ID        | bigint(21) unsigned | YES  |     | <null>  |       |
| START_KEY        | text                | YES  |     | <null>  |       |
| END_KEY          | text                | YES  |     | <null>  |       |
| EPOCH_CONF_VER   | bigint(21) unsigned | YES  |     | <null>  |       |
| EPOCH_VERSION    | bigint(21) unsigned | YES  |     | <null>  |       |
| WRITTEN_BYTES    | bigint(21) unsigned | YES  |     | <null>  |       |
| READ_BYTES       | bigint(21) unsigned | YES  |     | <null>  |       |
| APPROXIMATE_SIZE | bigint(21) unsigned | YES  |     | <null>  |       |
| APPROXIMATE_KEYS | bigint(21) unsigned | YES  |     | <null>  |       |
+------------------+---------------------+------+-----+---------+-------+
```

### TIKV_STORE_STATUS table

The `TIKV_STORE_STATUS` table provides the status information of all TiKV Stores.

{{< copyable "sql" >}}

```sql
desc TIKV_STORE_STATUS;
```

```sql
+-------------------+---------------------+------+-----+---------+-------+
| Field             | Type                | Null | Key | Default | Extra |
+-------------------+---------------------+------+-----+---------+-------+
| STORE_ID          | bigint(21) unsigned | YES  |     | <null>  |       |
| ADDRESS           | varchar(64)         | YES  |     | <null>  |       |
| STORE_STATE       | bigint(21) unsigned | YES  |     | <null>  |       |
| STORE_STATE_NAME  | varchar(64)         | YES  |     | <null>  |       |
| LABEL             | json unsigned       | YES  |     | <null>  |       |
| VERSION           | varchar(64)         | YES  |     | <null>  |       |
| CAPACITY          | varchar(64)         | YES  |     | <null>  |       |
| AVAILABLE         | varchar(64)         | YES  |     | <null>  |       |
| LEADER_COUNT      | bigint(21) unsigned | YES  |     | <null>  |       |
| LEADER_WEIGHT     | bigint(21) unsigned | YES  |     | <null>  |       |
| LEADER_SCORE      | bigint(21) unsigned | YES  |     | <null>  |       |
| LEADER_SIZE       | bigint(21) unsigned | YES  |     | <null>  |       |
| REGION_COUNT      | bigint(21) unsigned | YES  |     | <null>  |       |
| REGION_WEIGHT     | bigint(21) unsigned | YES  |     | <null>  |       |
| REGION_SCORE      | bigint(21) unsigned | YES  |     | <null>  |       |
| REGION_SIZE       | bigint(21) unsigned | YES  |     | <null>  |       |
| START_TS          | datetime unsigned   | YES  |     | <null>  |       |
| LAST_HEARTBEAT_TS | datetime unsigned   | YES  |     | <null>  |       |
| UPTIME            | varchar(64)         | YES  |     | <null>  |       |
+-------------------+---------------------+------+-----+---------+-------+
```

### USER_PRIVILEGES table

The `USER_PRIVILEGES` table provides information about global privileges. This information comes from the `mysql.user` system table:

{{< copyable "sql" >}}

```sql
desc USER_PRIVILEGES;
```

```sql
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

Fields in the `USER_PRIVILEGES` table are described as follows:

* `GRANTEE`: The name of the granted user, which is in the format of `'user_name'@'host_name'`.
* `TABLE_CATALOG`: The name of the catalog to which the table belongs. This value is always `def`.
* `PRIVILEGE_TYPE`: The privilege type to be granted. Only one privilege type is shown in each row.
* `IS_GRANTABLE`: If you have the `GRANT OPTION` privilege, the value is `YES`; otherwise, the value is `NO`.

### VIEWS table

The `VIEWS` table provides information about SQL views:

{{< copyable "sql" >}}

```sql
create view test.v1 as select 1;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
select * from views;
```

```sql
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

Fields in the `VIEWS` table are described as follows:

* `TABLE_CATALOG`: The name of the catalog to which the view belongs. This value is always `def`.
* `TABLE_SCHEMA`: The name of the schema to which the view belongs.
* `TABLE_NAME`: The view name.
* `VIEW_DEFINITION`: The definition of view, which is made by the `SELECT` statement when the view is created.
* `CHECK_OPTION`: The `CHECK_OPTION` value. The value options are `NONE`, `CASCADE`, and `LOCAL`.
* `IS_UPDATABLE`: Whether `UPDATE`/`INSERT`/`DELETE` is applicable to the view. In TiDB, the value is always `NO`.
* `DEFINER`: The name of the user who creates the view, which is in the format of `'user_name'@'host_name'`.
* `SECURITY_TYPE`: The value of `SQL SECURITY`. The value options are `DEFINER` and `INVOKER`.
* `CHARACTER_SET_CLIENT`: The value of the `character_set_client` session variable when the view is created.
* `COLLATION_CONNECTION`: The value of the `collation_connection` session variable when the view is created.

## TIDB\_INDEXES table

The `TIDB_INDEXES` table provides index-related information.

{{< copyable "sql" >}}

```sql
desc tidb_indexes\G
```

```sql
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

`INDEX_ID` is the unique ID that TiDB allocates for each index. It can be used to do a join operation with `INDEX_ID` obtained from another table or API.

For example, you can obtain `TABLE_ID` and `INDEX_ID` that are involved in some slow query in the [`SLOW_QUERY` table](#slow_query-table) and then obtain the specific index information using the following SQL statements:

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

## TIDB\_HOT\_REGIONS table

The `TIDB_HOT_REGIONS` table provides the hot Region information in the current TiKV instance.

{{< copyable "sql" >}}

```sql
desc tidb_hot_regions\G
```

```sql
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

- `TABLE_ID` and `INDEX_ID` are IDs generated for the corresponding table and index in TiDB.
- `TYPE` is the type for a hot Region. Its value can be `READ` or `WRITE`.

## TIKV\_STORE\_STATUS table

The `TIKV_STORE_STATUS` table shows some basic information of TiKV nodes via PD's API, like the ID allocated in the cluster, address and port, and status, capacity, and the number of Region leaders of the current node.

{{< copyable "sql" >}}

```sql
desc tikv_store_status\G
```

```sql
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

## TIKV\_REGION\_STATUS table

The `TIKV_REGION_STATUS` table shows some basic information of TiKV Regions via PD's API, like the Region ID, starting and ending key-values, and read and write traffic.

{{< copyable "sql" >}}

```sql
desc tikv_region_status\G
```

```sql
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

You can implement the `top confver`, `top read` and `top write` operations in pd-ctl via the `ORDER BY X LIMIT Y` operation on the `EPOCH_CONF_VER`, `WRITTEN_BYTES` and `READ_BYTES` columns.

You can query the top 3 Regions with the most write data using the following SQL statement:

```sql
select * from tikv_region_status order by written_bytes desc limit 3;
```

## TIKV\_REGION\_PEERS table

The `TIKV_REGION_PEERS` table shows detailed information of a single Region node in TiKV, like whether it is a learner or leader.

{{< copyable "sql" >}}

```sql
desc tikv_region_peers\G
```

```sql
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

For example, you can query the specific TiKV addresses for the top 3 Regions with the maximum value of `WRITTEN_BYTES` using the following SQL statement:

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

## ANALYZE\_STATUS table

The `ANALYZE_STATUS` table shows the execution status of the `ANALYZE` command in the current cluster.

{{< copyable "sql" >}}

```sql
desc analyze_status\G
```

```sql
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

The `STATE` column shows the execution status of a specific `ANALYZE` task. Its value can be `pending`, `running`,`finished` or `failed`.

## SLOW\_QUERY table

The `SLOW_QUERY` table maps slow query logs. Its column names and field names of slow query logs have an one-to-one corresponse relationship. For details, see [Identify Slow Queries](/identify-slow-queries.md#identify-slow-queries).

{{< copyable "sql" >}}

```sql
desc slow_query\G
```

```sql
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

## Unsupported Information Schema Tables

The following `INFORMATION_SCHEMA` tables are present in TiDB, but will always return zero rows:

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
