---
title: DDL
category: user guide
---

# 数据定义语言
DDL（Data Definition Language）用于定义和管理数据库以及数据库中各种对象的语句。

+ [CREATE DATABASE 语法](#create-database-语法)
+ [DROP DATABASE 语法](#drop-database-语法)
+ CREATE TABLE 语法
+ [DROP TABLE 语法](#drop-table-语法)
+ [TRUNCATE TABLE 语法](#truncate-table-语法)
+ [RENAME TABLE 语法](#rename-table-语法)
+ ALTER TABLE 语法
+ CREATE INDEX 语法
+ [DROP INDEX 语法](#drop-index-语法)

## CREATE DATABASE 语法

```sql
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
    [create_specification] ...

create_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```

`CREATE DATABASE` 用于创建数据库，并可以指定数据库的默认属性（如数据库默认字符集,校验规则。`CREATE SCHEMA` 跟 `CREATE DATABASE` 操作效果一样。
  
当创建已存在的数据库且不指定使用 `IF NOT EXISTS` 时会报错。

`create_specification` 选项用于指定数据库具体的 `CHARACTER` 和 `COLLATE`。目前这个选项只是语法支持。

## DROP DATABASE 语法

```sql
DROP {DATABASE | SCHEMA} [IF EXISTS] db_name
```

`DROP DATABASE` 用于删除指定数据库以及它其中的所用表格。

`IF EXISTS` 用于防止当数据库不存在时发生错误。

## CREATE TABLE 语法

```sql
CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name
    (create_definition,...)
    [table_options]

CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name
    { LIKE old_tbl_name | (LIKE old_tbl_name) }

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

index_col_name:
    col_name [(length)] [ASC | DESC]

index_type:
    USING {BTREE | HASH}

index_option:
    KEY_BLOCK_SIZE [=] value
  | index_type
  | COMMENT 'string'

reference_definition:
    REFERENCES tbl_name (index_col_name,...)
      [MATCH FULL | MATCH PARTIAL | MATCH SIMPLE]
      [ON DELETE reference_option]
      [ON UPDATE reference_option]

reference_option:
    RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT

table_options:
    table_option [[,] table_option] ...

table_option:
    AUTO_INCREMENT [=] value
  | AVG_ROW_LENGTH [=] value
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

`CREATE TABLE` 用于创建一个表。目前不支持临时表，不支持 `CHECK` 约束，不支持创建表的同时从其它表导入数据功能。
在语法上也支持一些 `Partition_options`，但是并不完全，就不做列举了。

* 使用 `IF NOT EXIST` 时，即使创建的表已经存在，也不会报错，如果不指定时，则报错。

* 使用 `LIKE` 基于一个表的定义创建一个空表，包括这个表中的列属性和索引属性。

* `create_definition` 中 `FULLTEXT` 和 `FOREIGN KEY` 目前只是语法上支持

* `data_type` 请参考[数据类型](datatype.md)章节。

* `index_col_name` 中 `[ASC | DESC]` 目前只是语法上支持。

* `index_type` 目前只是语法上支持。

* `index_option` 中 `KEY_BLOCK_SIZE` 目前只是语法上支持。

* `table_option` 目前支持的只有 `AUTO_INCREMENT`，`COMMENT` 和 `CHARACTER SET`，其它只是语法上支持。具体内容参考下表，各个子句j间用逗号隔开。

| 参数           |含义                                  |举例                        |
|----------------|--------------------------------------|----------------------------|
|`AUTO_INCREMENT`|自增字段初始值                        |`AUTO_INCREMENT` = 5|
|`CHARACTER SET` |指定该表的字符串编码。目前支持 UTF8MB4| `CHARACTER SET` =  'utf8mb4'|
|`COMMENT`       |注释信息                              | `COMMENT` = 'comment info' |

### AUTO_INCREMENT 说明
TiDB 的自增 ID (`AUTO_INCREMENT` ID) 只保证自增且唯一，并不保证连续分配。TiDB 目前采用批量分配的方式，所以如果在多台 TiDB 上同时插入数据，分配的自增 ID 会不连续。

允许给整型类型的字段指定 `AUTO_INCREMENT`，且一个表只允许一个属性为 `AUTO_INCREMENT` 的字段。

## DROP TABLE 语法

```sql
DROP [TEMPORARY] TABLE [IF EXISTS]
    tbl_name [, tbl_name] ...
```

可以同时删除多个表，表之间用 `,` 隔开。

当删除不存在的表时且不指定使用 `IF EXISTS` 时会报错。

## TRUNCATE TABLE 语法

```sql
TRUNCATE [TABLE] tbl_name
```

`TRUNCATE TABLE` 用于清除指定表中所有数据，但是保留表结构。

此操作于删除指定表全表数据的操作类似，但是操作的执行速度会远快于删除全表的速度，且不受表内数据行数影响。

注意：使用此语句后，原先表内的 `AUTO_INCREMENT` 的值不会记录，会被重新计数。

## RENAME TABLE 语法

```sql
RENAME TABLE
    tbl_name TO new_tbl_name
```

`RENAME TABLE` 用于对一个表进行重命名。

这个语句等价于如下的 `ALTER TABLE` 语句：
```sql
ALTER TABLE old_table RENAME new_table;
```

## DROP INDEX 语法

```sql
DROP INDEX index_name ON tbl_name
```

`DROP INDEX` 用于删除表上的一个索引，目前暂不支持删除主键索引。
