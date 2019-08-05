---
title: Information Schema
summary: Learn how to use Information Schema in TiDB.
category: reference
---

# Information Schema

As part of MySQL compatibility, TiDB supports a number of `INFORMATION_SCHEMA` tables. Many of these tables also have a corresponding `SHOW` command. The benefit of querying `INFORMATION_SCHEMA` is that it is possible to join between tables.

## Fully Supported Information Schema Tables

### CHARACTER\_SETS table

The `CHARACTER_SETS` table provides information about [character sets](/reference/sql/character-set.md). The default character set in TiDB is `utf8mb4`. Additional character sets in this table are included for compatibility with MySQL:

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

### COLLATIONS table

The `COLLATIONS` table provides a list of collations that correspond to character sets in the `CHARACTER_SETS` table.  Currently this table is included only for compatibility with MySQL, as TiDB only supports binary collation:

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

### COLLATION\_CHARACTER\_SET\_APPLICABILITY table

The `COLLATION_CHARACTER_SET_APPLICABILITY` table maps collations to the applicable character set name.  Similar to the `COLLATIONS` table, it is included only for compatibility with MySQL:

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

### COLUMNS table

The `COLUMNS` table provides detailed information about columns in tables:

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

The corresponding `SHOW` statement is as follows:

```sql
mysql> SHOW COLUMNS FROM t1 FROM test;
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)
```

### ENGINES table

The `ENGINES` table provides information about storage engines. For compatibility, TiDB will always describe InnoDB as the only supported engine:

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

### KEY\_COLUMN\_USAGE table

The `KEY_COLUMN_USAGE` table describes the key constraints of the columns, such as the primary key constraint:

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

### SCHEMATA table

The `SCHEMATA` table provides information about databases. The table data is equivalent to the result of the `SHOW DATABASES` statement:

```sql
mysql> select * from SCHEMATA\G
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

### SESSION\_VARIABLES table

The `SESSION_VARIABLES` table provides information about session variables. The table data is similar to the result of the `SHOW SESSION VARIABLES` statement:

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

### STATISTICS table

The `STATISTICS` table provides information about table indexes:

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

The following statements are equivalent:

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

### TABLE\_CONSTRAINTS table

The `TABLE_CONSTRAINTS` table describes which tables have constraints:

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

- The `CONSTRAINT_TYPE` value can be `UNIQUE`, `PRIMARY KEY`, or `FOREIGN KEY`.
- The `UNIQUE` and `PRIMARY KEY` information is similar to the result of the `SHOW INDEX` statement.

### USER\_PRIVILEGES table

The `USER_PRIVILEGES` table provides information about global privileges. This information comes from the `mysql.user` system table:

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

### VIEWS table

The `VIEWS` table provides information about SQL views:

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
