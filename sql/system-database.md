---
title: The TiDB System Database
category: user guide
---

# The TiDB System Database

The TiDB System Database is similar to MySQL, which contains tables that store information required by the server when it runs.

## Grant System Tables

These system tables contain grant information about user accounts and their privileges:

- `user`: user accounts, global privileges, and other non-privilege columns
- `db`: database-level privileges
- `tables_priv`: table-level privileges
- `columns_priv`: column-level privileges

## Server-Side Help System Tables

Currently, the `help_topic` is NULL.

## Statistics System Tables

- `stats_buckets`: the buckets of statistics
- `stats_histograms`: the histograms of statistics
- `stats_meta`: the meta information of tables, such as the total number of rows and updated rows

## GC Worker System Tables

- `gc_delete_range`: to record the data to be deleted

## Miscellaneous System Tables

- `GLOBAL_VARIABLES`: global system variable table
- `tidb`: to record the version information when TiDB executes `bootstrap`

## INFORMATION\_SCHEMA Tables

To be compatible with MySQL, TiDB supports INFORMATION\_SCHEMA tables. Some third-party software queries information in these tables. Currently, most INFORMATION\_SCHEMA tables in TiDB are NULL.

### CHARACTER\_SETS Table

The CHARACTER\_SETS table provides information about character sets. But it contains dummy data. By default, TiDB only supports utf8mb4.

```sql
mysql> select * from CHARACTER_SETS;
+--------------------|----------------------|-----------------------|--------+
| CHARACTER_SET_NAME | DEFAULT_COLLATE_NAME | DESCRIPTION           | MAXLEN |
+--------------------|----------------------|-----------------------|--------+
| ascii              | ascii_general_ci     | US ASCII              |      1 |
| binary             | binary               | Binary pseudo charset |      1 |
| latin1             | latin1_swedish_ci    | cp1252 West European  |      1 |
| utf8               | utf8_general_ci      | UTF-8 Unicode         |      3 |
| utf8mb4            | utf8mb4_general_ci   | UTF-8 Unicode         |      4 |
+--------------------|----------------------|-----------------------|--------+
5 rows in set (0.00 sec)
```

### COLLATIONS Table

The COLLATIONS table is similar to the CHARACTER\_SETS table.

### COLLATION\_CHARACTER\_SET\_APPLICABILITY Table

NULL.

### COLUMNS Table

The COLUMNS table provides information about columns in tables. The information in this table is not accurate. To query information, it is recommended to use the `SHOW` statement:

```sql
SHOW COLUMNS FROM table_name [FROM db_name] [LIKE 'wild']
```

### COLUMNS\_PRIVILEGE Table

NULL.

### ENGINES Table

The ENGINES table provides information about storage engines. But it contains dummy data only. In the production environment, use the TiKV engine for TiDB.

### EVENTS Table

NULL.

### FILES Table

NULL.

### GLOBAL\_STATUS Table

NULL.

### GLOBAL\_VARIABLES Table

NULL.

### KEY\_COLUMN\_USAGE Table

The KEY_COLUMN_USAGE table describes the key constraints of the columns, such as the primary key constraint.

### OPTIMIZER\_TRACE Table

NULL.

### PARAMETERS Table

NULL.

### PARTITIONS Table

NULL.

### PLUGINS Table

NULL.

### PROFILING Table

NULL.

### REFERENTIAL\_CONSTRAINTS Table

NULL.

### ROUTINES Table

NULL.

### SCHEMATA Table

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

### SCHEMA\_PRIVILEGES Table

NULL.

### SESSION\_STATUS Table

NULL.

### SESSION\_VARIABLES Table

The SESSION\_VARIABLES table provides information about session variables. The table data is similar to the result of the `SHOW SESSION VARIABLES` statement.

### STATISTICS Table

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

### TABLES Table

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

### TABLESPACES Table

NULL.

### TABLE\_CONSTRAINTS Table

The TABLE_CONSTRAINTS table describes which tables have constraints.

- The `CONSTRAINT_TYPE` value can be UNIQUE, PRIMARY KEY, or FOREIGN KEY.
- The UNIQUE and PRIMARY KEY information is similar to the result of the `SHOW INDEX` statement.

### TABLE\_PRIVILEGES Table

NULL.

### TRIGGERS Table

NULL.

### USER\_PRIVILEGES Table

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

### VIEWS Table

NULL. Currently, TiDB does not support views. 
