---
title: TiDB 系统数据库
category: user guide
---

# TiDB 系统数据库

TiDB 的系统数据库跟 MySQL 类似，里面包含一些服务器运行时需要的信息。

### 权限系统表

这些系统表里面包含了用户账户以及相应的授权信息：

* `user` 用户账户，全局权限，以及其它一些非权限的列
* `db` 数据库级别的权限
* `tables_priv` 表级的权限
* `columns_priv` 列级的权限

### 服务端帮助信息系统表

* `help_topic` 目前为空

### 统计信息相关系统表

* `stats_buckets` 统计信息的桶
* `stats_histograms` 统计信息的直方图
* `stats_meta` 表的元信息，比如总行数和修改数

### GC Worker 相关系统表

* `gc_delete_range` 

### 其它系统表

* `GLOBAL_VARIABLES` 全局系统变量表
* `tidb` 用于 TiDB 在 bootstrap 的时候记录相关版本信息

## INFORMATION\_SCHEMA 里面的表

INFORMATION\_SCHEMA 库里面的表主要是为了兼容 MySQL 而存在，有些第三方软件会查询里面的信息。在目前 TiDB 的实现中，里面大部分只是一些空表。

### CHARACTER\_SETS Table

提供字符集相关的信息，其实数据是假的。TiDB 默认支持并且只支持 utf8mb4 。

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

同上。

### COLLATION\_CHARACTER\_SET\_APPLICABILITY Table

空表。

### COLUMNS Table

COLUMNS 表提供了关于所有表的列的信息。这张表里面的信息不准确，推荐使用 SHOW 语句查询：

```sql
SHOW COLUMNS FROM table_name [FROM db_name] [LIKE 'wild']
```

### COLUMN\_PRIVILEGES Table

空表。

### ENGINES Table

ENGINES 表提供了关于存储引擎的信息。从和 MySQL 兼容性上考虑，TiDB `show engines` 的结果展示成了 InnoDB。

### EVENTS Table

空表。

### FILES Table

空表。

### GLOBAL\_STATUS Table

空表。

### GLOBAL\_VARIABLES Table

空表。

### KEY\_COLUMN\_USAGE Table

KEY\_COLUMN\_USAGE 这张表描述了关于列的 key 的约束，比如是否是主键列。

### OPTIMIZER\_TRACE Table

空表。

### PARAMETERS Table

空表。

### PARTITIONS Table

空表。

### PLUGINS Table

空表。

### PROFILING Table

空表。

### REFERENTIAL\_CONSTRAINTS Table

空表。

### ROUTINES Table

空表。

### SCHEMATA Table

SCHEMATA 表提供了关于数据库的信息。表中的内容和 SHOW DATABASES 基本等价。

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

空表。

### SESSION\_STATUS Table

空表。

### SESSION\_VARIABLES Table

SESSION\_VARIABLES 表提供了关于 session 变量的信息。表中的数据跟 SHOW SESSION VARIABLES 类似。

### STATISTICS Table

统计信息的表。

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

下列操作是等价的。

```sql
SELECT * FROM INFORMATION_SCHEMA.STATISTICS
  WHERE table_name = 'tbl_name'
  AND table_schema = 'db_name'

SHOW INDEX
  FROM tbl_name
  FROM db_name
```

### TABLES Table

TABLES 表提供了数据库里面关于表的信息。

以下操作是等价的：

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

### TABLESPACES Table

空表。

### TABLE\_CONSTRAINTS Table

TABLE\_CONSTRAINTS 记录了表的约束信息。其中：

* `CONSTRAINT_TYPE` 的取值可以是 UNIQUE, PRIMARY KEY, 或者 FOREIGN KEY。
* UNIQUE 和 PRIMARY KEY 信息跟 SHOW INDEX 看到的是一样的。

### TABLE\_PRIVILEGES Table

空表。

### TRIGGERS Table

空表。

### USER\_PRIVILEGES Table

USER\_PRIVILEGES 表提供了关于全局权限的信息。这张表的内容是根据 mysql.user 表生成的。

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

空表。TiDB 暂不支持视图。
