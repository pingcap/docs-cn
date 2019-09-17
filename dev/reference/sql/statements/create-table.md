---
title: CREATE TABLE
summary: TiDB 数据库中 CREATE TABLE 的使用概况
category: reference
---

# CREATE TABLE

`CREATE TABLE` 语句用于在当前所选数据库中创建新表。另可参阅单独的 `CREATE TABLE LIKE` 文档。

## 语法图

**CreateTableStmt:**

![CreateTableStmt](/media/sqlgram/CreateTableStmt.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**TableElementListOpt:**

![TableElementListOpt](/media/sqlgram/TableElementListOpt.png)

**TableElement:**

![TableElement](/media/sqlgram/TableElement.png)

**PartitionOpt:**

![PartitionOpt](/media/sqlgram/PartitionOpt.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram/ColumnDef.png)

**ColumnName:**

![ColumnName](/media/sqlgram/ColumnName.png)

**Type:**

![Type](/media/sqlgram/Type.png)

**ColumnOptionListOpt:**

![ColumnOptionListOpt](/media/sqlgram/ColumnOptionListOpt.png)

**TableOptionListOpt:**

![TableOptionListOpt](/media/sqlgram/TableOptionListOpt.png)

## 语法说明

`CREATE TABLE` 用于创建一个表。目前不支持临时表，不支持 `CHECK` 约束，不支持创建表的同时从其它表导入数据功能。在语法上也支持一些 `Partition_options`，但是并不完全，就不做列举了。

以下是 `CREATE TABLE` 相关的语法说明：

```sql
CREATE TABLE [IF NOT EXISTS] tbl_name
    (create_definition,...)
    [table_options]
```

使用 `IF NOT EXIST` 时，即使创建的表已经存在，也不会报错，如果不指定时，则报错。

```sql
CREATE TABLE [IF NOT EXISTS] tbl_name
    { LIKE old_tbl_name | (LIKE old_tbl_name) }
```

使用 `LIKE` 基于一个表的定义创建一个空表，包括这个表中的列属性和索引属性。

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

`create_definition` 中 `FULLTEXT` 和 `FOREIGN KEY` 目前只是语法上支持。

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

`data_type` 请参考[数据类型](/dev/reference/sql/data-types/overview.md)章节。

```sql
index_col_name:
    col_name [(length)] [ASC | DESC]
```

`index_col_name` 中 `[ASC | DESC]` 目前只是语法上支持。

```sql
index_type:
    USING {BTREE | HASH}
```

`index_type` 目前只是语法上支持。

```sql
index_option:
    KEY_BLOCK_SIZE [=] value
  | index_type
  | COMMENT 'string'
```

`index_option` 中 `KEY_BLOCK_SIZE` 目前只是语法上支持。

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

`table_option` 目前支持的只有 `AUTO_INCREMENT`、`SHARD_ROW_ID_BITS`（详情介绍请参考 [TiDB 专用系统变量和语法](/dev/reference/configuration/tidb-server/tidb-specific-variables.md#shard_row_id_bits)）、`PRE_SPLIT_REGIONS`、`CHARACTER SET`、`COLLATE` 和 `COMMENT`，其它只是语法上支持。具体内容参考下表，各个子句之间用逗号隔开。

| 参数           |含义                                  |举例                      |
|----------------|--------------------------------------|----------------------------|
|`AUTO_INCREMENT`|自增字段初始值                        |`AUTO_INCREMENT` = 5|
|`SHARD_ROW_ID_BITS`|用来设置隐式 _tidb_rowid 的分片数量的 bit 位数 |`SHARD_ROW_ID_BITS` = 4|
|`PRE_SPLIT_REGIONS`|用来在建表时预先均匀切分 `2^(PRE_SPLIT_REGIONS)` 个 Region |`PRE_SPLIT_REGIONS` = 4|
|`CHARACTER SET` |指定该表所使用的字符集                | `CHARACTER SET` = 'utf8mb4'|
|`COLLATE`       |指定该表所使用的字符集排序规则        | `COLLATE` = 'utf8mb4_bin'|
|`COMMENT`       |注释信息                              | `COMMENT` = 'comment info'|

`split-table` 配置项默认情况下会开启，在此配置项开启时，建表操作会为每个表建立单独的 Region。

## 示例

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

## MySQL 兼容性

* TiDB 不支持 `CREATE TEMPORARY TABLE` 语法。
* 支持除空间类型以外的所有数据类型。
* 不支持 `FULLTEXT`，`HASH` 和 `SPATIAL` 索引。
* `KEY_BLOCK_SIZE` 和 `ENGINE` 属性可被解析，但会被忽略。
* `index_col_name` 属性支持 length 选项，最大长度限制为 3072 字节。此长度限制不会更改，具体取决于存储引擎和建表时使用的字符集。
* `index_col_name` 属性支持 `ASC` 和 `DESC` 的索引排序选项。
* `COMMENT` 属性最多支持 1024 个字符，不支持 `WITH PARSER` 选项。
* TiDB 在单个表中最多支持 512 列。InnoDB 中相应的数量限制为 1017，MySQL 中的硬限制为 4096。

## 另请参阅

* [DROP TABLE](/dev/reference/sql/statements/drop-table.md)
* [CREATE TABLE LIKE](/dev/reference/sql/statements/create-table-like.md)
* [SHOW CREATE TABLE](/dev/reference/sql/statements/show-create-table.md)
