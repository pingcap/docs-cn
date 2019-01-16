---
title: The TiDB System Database
summary: Learn tables contained in the TiDB System Database.
category: user guide
---

# The TiDB System Database

The TiDB System Database is similar to MySQL, which contains tables that store information required by the server when it runs.

## Grant system tables

These system tables contain grant information about user accounts and their privileges:

- `user`: user accounts, global privileges, and other non-privilege columns
- `db`: database-level privileges
- `tables_priv`: table-level privileges
- `columns_priv`: column-level privileges

## Server-side help system tables

Currently, the `help_topic` is NULL.

## Statistics system tables

- `stats_buckets`: the buckets of statistics
- `stats_histograms`: the histograms of statistics
- `stats_meta`: the meta information of tables, such as the total number of rows and updated rows

## GC worker system tables

- `gc_delete_range`: to record the data to be deleted

## Miscellaneous system tables

- `GLOBAL_VARIABLES`: global system variable table
- `tidb`: to record the version information when TiDB executes `bootstrap`

## INFORMATION\_SCHEMA tables

To be compatible with MySQL, TiDB supports INFORMATION\_SCHEMA tables. Some third-party software queries information in these tables. Currently, most INFORMATION\_SCHEMA tables in TiDB are NULL.

### CHARACTER\_SETS table

The CHARACTER\_SETS table provides information about [character sets](../sql/character-set-support.md). The default character set in TiDB is `utf8`, which behaves similar to `utf8mb4` in MySQL. Additional character sets in this table are included for compatibility with MySQL:

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

The COLLATIONS table provides a list of collations that correspond to character sets in the CHARACTER\_SETS table.  Currently this table is included only for compatibility with MySQL, as TiDB only supports binary collation.

### COLLATION\_CHARACTER\_SET\_APPLICABILITY table

This table maps collations to the applicable character set name.  Similar to the collations table, it is included only for compatibility with MySQL.

### COLUMNS table

The COLUMNS table provides information about columns in tables. The information in this table is not accurate. To query information, it is recommended to use the `SHOW` statement:

```sql
SHOW COLUMNS FROM table_name [FROM db_name] [LIKE 'wild']
```

### COLUMN\_PRIVILEGES table

NULL.

### ENGINES table

The ENGINES table provides information about storage engines. For compatibility, TiDB will always describe InnoDB as the only supported engine.

### EVENTS table

NULL.

### FILES table

NULL.

### GLOBAL\_STATUS table

NULL.

### GLOBAL\_VARIABLES table

NULL.

### KEY\_COLUMN\_USAGE table

The KEY_COLUMN_USAGE table describes the key constraints of the columns, such as the primary key constraint.

### OPTIMIZER\_TRACE table

NULL.

### PARAMETERS table

NULL.

### PARTITIONS table

NULL.

### PLUGINS table

NULL.

### PROFILING table

NULL.

### REFERENTIAL\_CONSTRAINTS table

NULL.

### ROUTINES table

NULL.

### SCHEMATA table

The SCHEMATA table provides information about databases. The table data is equivalent to the result of the `SHOW DATABASES` statement.

```sql
mysql> select * from SCHEMATA;
+--------------|--------------------|----------------------------|------------------------|----------+
| CATALOG_NAME | SCHEMA_NAME        | DEFAULT_CHARACTER_SET_NAME | DEFAULT_COLLATION_NAME | SQL_PATH |
+--------------|--------------------|----------------------------|------------------------|----------+
| def          | INFORMATION_SCHEMA | utf8                       | utf8_bin               | NULL     |
| def          | mysql              | utf8                       | utf8_bin               | NULL     |
| def          | PERFORMANCE_SCHEMA | utf8                       | utf8_bin               | NULL     |
| def          | test               | utf8                       | utf8_bin               | NULL     |
+--------------|--------------------|----------------------------|------------------------|----------+
4 rows in set (0.00 sec)
```

### SCHEMA\_PRIVILEGES table

NULL.

### SESSION\_STATUS table

NULL.

### SESSION\_VARIABLES table

The SESSION\_VARIABLES table provides information about session variables. The table data is similar to the result of the `SHOW SESSION VARIABLES` statement.

### STATISTICS table

The STATISTICS table provides information about table indexes.

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

The TABLES table provides information about tables in databases.

The following statements are equivalent:

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

### TABLESPACES table

NULL.

### TABLE\_CONSTRAINTS table

The TABLE_CONSTRAINTS table describes which tables have constraints.

- The `CONSTRAINT_TYPE` value can be UNIQUE, PRIMARY KEY, or FOREIGN KEY.
- The UNIQUE and PRIMARY KEY information is similar to the result of the `SHOW INDEX` statement.

### TABLE\_PRIVILEGES table

NULL.

### TRIGGERS table

NULL.

### USER\_PRIVILEGES table

The USER_PRIVILEGES table provides information about global privileges. This information comes from the mysql.user grant table.

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

NULL. Currently, TiDB does not support views. 
