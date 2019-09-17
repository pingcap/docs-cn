---
title: CREATE TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE TABLE for the TiDB database.
category: reference
---

# CREATE TABLE

This statement creates a new table in the currently selected database. See also `CREATE TABLE LIKE`, which is documented separately.

## Synopsis

**CreateTableStmt:**

![CreateTableStmt](/media/sqlgram-v2.1/CreateTableStmt.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram-v2.1/IfNotExists.png)

**TableName:**

![TableName](/media/sqlgram-v2.1/TableName.png)

**TableElementListOpt:**

![TableElementListOpt](/media/sqlgram-v2.1/TableElementListOpt.png)

**TableElement:**

![TableElement](/media/sqlgram-v2.1/TableElement.png)

**PartitionOpt:**

![PartitionOpt](/media/sqlgram-v2.1/PartitionOpt.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram-v2.1/ColumnDef.png)

**ColumnName:**

![ColumnName](/media/sqlgram-v2.1/ColumnName.png)

**Type:**

![Type](/media/sqlgram-v2.1/Type.png)

**ColumnOptionListOpt:**

![ColumnOptionListOpt](/media/sqlgram-v2.1/ColumnOptionListOpt.png)

**TableOptionListOpt:**

![TableOptionListOpt](/media/sqlgram-v2.1/TableOptionListOpt.png)

## Syntax

The `CREATE TABLE` statement is used to create a table. Currently, it does not support temporary tables, `CHECK` constraints, or importing data from other tables while creating tables. It supports some of the `Partition_options` in syntax.

Here are some options about the `CREATE TABLE` syntax:

```sql
CREATE TABLE [IF NOT EXISTS] tbl_name
    (create_definition,...)
    [table_options]
```

When you create an existing table, if you specify `IF NOT EXIST`, it does not report an error. Otherwise, it reports an error.

```sql
CREATE TABLE [IF NOT EXISTS] tbl_name
    { LIKE old_tbl_name | (LIKE old_tbl_name) }
```

Use `LIKE` to create an empty table based on the definition of another table including its column and index properties.

```sql
create_definition:
    col_name column_definition
  | [CONSTRAINT [symbol]] PRIMARY KEY [index_type] (index_col_name,...)
      [index_option] ...
  | {INDEX|KEY} [index_name] [index_type] (index_col_name,...)
      [index_option] ...
  | [CONSTRAINT [symbol]] UNIQUE [INDEX|KEY]
      [index_name] [index_type] (index_col_name,...)
      [index_option] ...
  | {FULLTEXT} [INDEX|KEY] [index_name] (index_col_name,...)
      [index_option] ...
  | [CONSTRAINT [symbol]] FOREIGN KEY
      [index_name] (index_col_name,...) reference_definition
```

The `FULLTEXT` and `FOREIGN KEY` in `create_definition` are currently only supported in syntax.

```sql
column_definition:
    data_type [NOT NULL | NULL] [DEFAULT default_value]
      [AUTO_INCREMENT] [UNIQUE [KEY] | [PRIMARY] KEY]
      [COMMENT 'string']
      [reference_definition]
  | data_type [GENERATED ALWAYS] AS (expression)
      [VIRTUAL | STORED] [UNIQUE [KEY]] [COMMENT comment]
      [NOT NULL | NULL] [[PRIMARY] KEY]

data_type:
    BIT[(length)]
  | TINYINT[(length)] [UNSIGNED] [ZEROFILL]
  | SMALLINT[(length)] [UNSIGNED] [ZEROFILL]
  | MEDIUMINT[(length)] [UNSIGNED] [ZEROFILL]
  | INT[(length)] [UNSIGNED] [ZEROFILL]
  | INTEGER[(length)] [UNSIGNED] [ZEROFILL]
  | BIGINT[(length)] [UNSIGNED] [ZEROFILL]
  | REAL[(length,decimals)] [UNSIGNED] [ZEROFILL]
  | DOUBLE[(length,decimals)] [UNSIGNED] [ZEROFILL]
  | FLOAT[(length,decimals)] [UNSIGNED] [ZEROFILL]
  | DECIMAL[(length[,decimals])] [UNSIGNED] [ZEROFILL]
  | NUMERIC[(length[,decimals])] [UNSIGNED] [ZEROFILL]
  | DATE
  | TIME[(fsp)]
  | TIMESTAMP[(fsp)]
  | DATETIME[(fsp)]
  | YEAR
  | CHAR[(length)] [BINARY]
      [CHARACTER SET charset_name] [COLLATE collation_name]
  | VARCHAR(length) [BINARY]
      [CHARACTER SET charset_name] [COLLATE collation_name]
  | BINARY[(length)]
  | VARBINARY(length)
  | TINYBLOB
  | BLOB
  | MEDIUMBLOB
  | LONGBLOB
  | TINYTEXT [BINARY]
      [CHARACTER SET charset_name] [COLLATE collation_name]
  | TEXT [BINARY]
      [CHARACTER SET charset_name] [COLLATE collation_name]
  | MEDIUMTEXT [BINARY]
      [CHARACTER SET charset_name] [COLLATE collation_name]
  | LONGTEXT [BINARY]
      [CHARACTER SET charset_name] [COLLATE collation_name]
  | ENUM(value1,value2,value3,...)
      [CHARACTER SET charset_name] [COLLATE collation_name]
  | SET(value1,value2,value3,...)
      [CHARACTER SET charset_name] [COLLATE collation_name]
  | JSON
```

For the `data_type`, see [Data Types](/v2.1/reference/sql/data-types/overview.md).

```sql
index_col_name:
    col_name [(length)] [ASC | DESC]
```

The `[ASC | DESC]` in `index_col_name` is currently only supported in syntax.

```sql
index_type:
    USING {BTREE | HASH}
```

The `index_type` is currently only supported in syntax.

```sql
index_option:
    KEY_BLOCK_SIZE [=] value
  | index_type
  | COMMENT 'string'
```

The `KEY_BLOCK_SIZE` in `index_option` is currently only supported in syntax.

```sql
reference_definition:
    REFERENCES tbl_name (index_col_name,...)
      [MATCH FULL | MATCH PARTIAL | MATCH SIMPLE]
      [ON DELETE reference_option]
      [ON UPDATE reference_option]

reference_option:
    RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT
```

```sql
table_options:
    table_option [[,] table_option] ...

table_option:
    AUTO_INCREMENT [=] value
  | AVG_ROW_LENGTH [=] value
  | SHARD_ROW_ID_BITS [=] value
  | PRE_SPLIT_REGIONS [=] value
  | [DEFAULT] CHARACTER SET [=] charset_name
  | CHECKSUM [=] {0 | 1}
  | [DEFAULT] COLLATE [=] collation_name
  | COMMENT [=] 'string'
  | COMPRESSION [=] {'ZLIB'|'LZ4'|'NONE'}
  | CONNECTION [=] 'connect_string'
  | DELAY_KEY_WRITE [=] {0 | 1}
  | ENGINE [=] engine_name
  | KEY_BLOCK_SIZE [=] value
  | MAX_ROWS [=] value
  | MIN_ROWS [=] value
  | ROW_FORMAT [=] {DEFAULT|DYNAMIC|FIXED|COMPRESSED|REDUNDANT|COMPACT}
  | STATS_PERSISTENT [=] {DEFAULT|0|1}
```

The `table_option` currently only supports `AUTO_INCREMENT`, `SHARD_ROW_ID_BITS` (see [TiDB Specific System Variables](/v2.1/reference/configuration/tidb-server/tidb-specific-variables.md#shard_row_id_bits) for details), `PRE_SPLIT_REGIONS`, `CHARACTER SET`, `COLLATE`, and `COMMENT`, while the others are only supported in syntax. The clauses are separated by a comma `,`. See the following table for details:

| Parameters | Description | Example |
| ---------- | ---------- | ------- |
| `AUTO_INCREMENT` | The initial value of the increment field | `AUTO_INCREMENT` = 5 |
| `SHARD_ROW_ID_BITS` | To set the number of bits for the implicit `_tidb_rowid` shards |`SHARD_ROW_ID_BITS` = 4|
| `PRE_SPLIT_REGIONS` | To pre-split 2^(PRE_SPLIT_REGIONS-1) Regions when creating a table |`PRE_SPLIT_REGIONS` = 4|
| `CHARACTER SET` | To specify the string code for the table; currently only support UTF8MB4 | `CHARACTER SET` =  'utf8mb4' |
| `COMMENT` | The comment information | `COMMENT` = 'comment info' |

> **Note:**
>
> In TiDB 2.1 versions, the three features `SHARD_ROW_ID_BITS`, `PRE_SPLIT_REGIONS` and `COLLATE` are supported starting from the 2.1.13 version (including 2.1.13).

## Examples

```sql
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.11 sec)

mysql> CREATE TABLE t2 LIKE t1;
Query OK, 0 rows affected (0.10 sec)

mysql> DESC t1;
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t1;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.00 sec)
```

## MySQL compatibility

* TiDB does not support the syntax `CREATE TEMPORARY TABLE`.
* All of the data types except spatial types are supported.
* `FULLTEXT`, `HASH` and `SPATIAL` indexes are not supported.
* The `KEY_BLOCK_SIZE` and `ENGINE` attributes are parsed but ignored.
* The `index_col_name` attribute supports the length option with a maximum length limit of 3072 bytes. The length limit does not change depending on the storage engine, and character set used when building the table.
* The `index_col_name` attribute supports the index sorting options of `ASC` and `DESC`
* The `COMMENT` attribute supports a maximum of 1024 characters and does not support the `WITH PARSER` option.
* TiDB supports at most 512 columns in a single table. The corresponding number limit in InnoDB is 1017, and the hard limit in MySQL is 4096.

## See also

* [DROP TABLE](/v2.1/reference/sql/statements/drop-table.md)
* [CREATE TABLE LIKE](/v2.1/reference/sql/statements/create-table-like.md)
* [SHOW CREATE TABLE](/v2.1/reference/sql/statements/show-create-table.md)
