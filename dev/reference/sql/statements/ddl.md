---
title: 数据定义语言
category: reference
aliases: ['/docs-cn/sql/ddl/']
---

# 数据定义语言

DDL（Data Definition Language）用于定义和管理数据库以及数据库中各种对象的语句。

目前 TiDB 实现了 `ADD INDEX` 操作和 `GENERAL` 操作（除了 `ADD INDEX` 以外的 DDL 操作）在表间的并行。即在不同表之间，`ADD INDEX` 操作和 `GENERAL` 操作可以并行执行。也可以认为目前有两个 worker 分别处理 `ADD INDEX` 操作和 `GENERAL` 操作，当处理的请求是同一个表内的操作时，按接受到 DDL 请求的先后顺序来执行。该功能是为了初步且稳定地解决 `ADD INDEX` 操作（当前 TiDB 中只有 `ADD INDEX` 操作的执行时间会比较久）可能阻塞其他 DDL 操作的问题。

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

`create_specification` 选项用于指定数据库具体的 `CHARACTER SET` 和 `COLLATE`。目前这个选项只是语法支持。

## DROP DATABASE 语法

```sql
DROP {DATABASE | SCHEMA} [IF EXISTS] db_name
```

`DROP DATABASE` 用于删除指定数据库以及它其中的所用表格。

`IF EXISTS` 用于防止当数据库不存在时发生错误。

## CREATE TABLE 语法

```sql
CREATE TABLE [IF NOT EXISTS] tbl_name
    (create_definition,...)
    [table_options]

CREATE TABLE [IF NOT EXISTS] tbl_name
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

* `data_type` 请参考[数据类型](/dev/reference/sql/data-types.md)章节。

* `index_col_name` 中 `[ASC | DESC]` 目前只是语法上支持。

* `index_type` 目前只是语法上支持。

* `index_option` 中 `KEY_BLOCK_SIZE` 目前只是语法上支持。

* `table_option` 目前支持的只有 `AUTO_INCREMENT`，`CHARACTER SET` 和 `COMMENT`，其它只是语法上支持。具体内容参考下表，各个子句之间用逗号隔开。

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
DROP TABLE [IF EXISTS]
    tbl_name [, tbl_name] ...
    [RESTRICT | CASCADE]
```

可以同时删除多个表，表之间用 `,` 隔开。

当删除不存在的表时且不指定使用 `IF EXISTS` 时会报错。

关键字 RESTRICT 和 CASCADE 没有实际效果。其作用是与其他数据库兼容。

## TRUNCATE TABLE 语法

```sql
TRUNCATE [TABLE] tbl_name
```

`TRUNCATE TABLE` 用于清除指定表中所有数据，但是保留表结构。

此操作于删除指定表全表数据的操作类似，但是操作的执行速度会远快于删除全表的速度，且不受表内数据行数影响。

> **注意：**
>
> 使用此语句后，原先表内的 `AUTO_INCREMENT` 的值不会记录，会被重新计数。

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

## ALTER TABLE 语法

```sql
ALTER TABLE tbl_name
    [alter_specification]

alter_specification:
    table_options
  | ADD [COLUMN] col_name column_definition
        [FIRST | AFTER col_name]
  | ADD [COLUMN] (col_name column_definition,...)
  | ADD {INDEX|KEY} [index_name]
        [index_type] (index_col_name,...) [index_option] ...
  | ADD [CONSTRAINT [symbol]] PRIMARY KEY
        [index_type] (index_col_name,...) [index_option] ...
  | ADD [CONSTRAINT [symbol]]
        UNIQUE [INDEX|KEY] [index_name]
        [index_type] (index_col_name,...) [index_option] ...
  | ADD FULLTEXT [INDEX|KEY] [index_name]
        (index_col_name,...) [index_option] ...
  | ADD [CONSTRAINT [symbol]]
        FOREIGN KEY [index_name] (index_col_name,...)
        reference_definition
  | ALTER [COLUMN] col_name {SET DEFAULT literal | DROP DEFAULT}
  | CHANGE [COLUMN] old_col_name new_col_name column_definition
        [FIRST|AFTER col_name]
  | {DISABLE|ENABLE} KEYS
  | DROP [COLUMN] col_name
  | DROP {INDEX|KEY} index_name
  | DROP PRIMARY KEY
  | DROP FOREIGN KEY fk_symbol
  | LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}
  | MODIFY [COLUMN] col_name column_definition
        [FIRST | AFTER col_name]
  | RENAME [TO|AS] new_tbl_name
  | {WITHOUT|WITH} VALIDATION

index_col_name:
    col_name [(length)] [ASC | DESC]

index_type:
    USING {BTREE | HASH}

index_option:
    KEY_BLOCK_SIZE [=] value
  | index_type
  | COMMENT 'string'

table_options:
    table_option [[,] table_option] ...

table_option:
    AVG_ROW_LENGTH [=] value
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

`ALTER TABLE` 用于修改已存在的表的结构，比如：修改表及表属性、新增或删除列、创建或删除索引、修改列及属性等。以下是几个字段类型的描述：

* `index_col_name`、`index_type` 和 `index_option` 可以参考 [CREATE INDEX 语法](#create-index-语法)。

* `table_option` 目前支持的修改类型为 `AUTO_INCREMENT` 和 `COMMENT`，其它的只是语法上支持。

下面介绍一下具体操作类型的支持情况。

* `ADD/DROP INDEX/COLUMN` 操作目前不支持同时创建或删除多个索引或列。

* `ADD/DROP PRIMARY KEY` 操作目前不支持。

* `DROP COLUMN` 操作目前不支持删除的列为主键列或索引列。

* `ADD COLUMN` 操作目前不支持同时将新添加的列设为主键或唯一索引，也不支持将此列设成 `AUTO_INCREMENT` 属性。

* `CHANGE/MODIFY COLUMN` 操作目前支持部分语法，细节如下：
    - 在修改类型方面，只支持整数类型之间修改，字符串类型之间修改和 Blob 类型之间的修改，且只能使原类型长度变长。此外，不能改变列的 `unsigned`/`charset`/`collate` 属性。这里的类型分类如下：
    - 具体支持的整型类型有：`TinyInt`，`SmallInt`，`MediumInt`，`Int`，`BigInt`。
    - 具体支持的字符串类型有：`Char`，`Varchar`，`Text`，`TinyText`，`MediumText`，`LongText`。
    - 具体支持的 Blob 类型有：`Blob`，`TinyBlob`，`MediumBlob`，`LongBlob`。
    - 在修改类型定义方面，支持的包括 `default value`，`comment`，`null`，`not null` 和 `OnUpdate`。
    - 不支持对 `enum` 类型的列进行修改

* `LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}` 目前只是语法支持。

## CREATE INDEX 语法

```sql
CREATE [UNIQUE] INDEX index_name
    [index_type]
    ON tbl_name (index_col_name,...)
    [index_option] ...

index_col_name:
    col_name [(length)] [ASC | DESC]

index_option:
    KEY_BLOCK_SIZE [=] value
  | index_type
  | COMMENT 'string'

index_type:
    USING {BTREE | HASH}
```

`CREATE INDEX` 语句的作用是为一个已经存在的表创建一个索引。在功能上，`CREATE INDEX` 对应于 `ALTER TABLE` 语句的创建索引功能。与 MySQL 一样 `CREATE INDEX` 不能创建主键索引。

### 与 MySQL 的差异

* 支持 `UNIQUE` 索引，不支持 `FULLTEXT` 和 `SPATIAL` 索引。

* `index_col_name` 支持长度选项，最大长度限制为3072字节，该长度限制不根据建表时使用的存储引擎、字符集而变。这是因为 TiDB 并非使用 Innodb 、 MyISAM 等存储引擎，因此，仅对建表时的存储引擎选项进行了 MySQL 语法上的兼容。对于字符集，TiDB 使用的是 utf8mb4 字符集，对于建表时的字符集选项同样仅有 MySQL 语法上的兼容。详见[与 MySQL 兼容性对比](/dev/reference/mysql-compatibility.md)章节。

* `index_col_name` 支持索引排序选项 `ASC` 和 `DESC`。 排序选项行为与 MySQL 一致，仅支持语法解析，内部所有索引都是以正序排列。详见 MySQL 的 [CREATE INDEX Syntax](https://dev.mysql.com/doc/refman/5.7/en/create-index.html) 章节。

* `index_option` 支持 `KEY_BLOCK_SIZE` 、`index_type` 和 `COMMENT` 。 `COMMENT` 允许最大1024个字符。不支持 `WITH PARSER` 选项。

* `index_type` 支持 `BTREE` 和 `HASH` ，但仅有 MySQL 语法上的支持，即索引类型与建表语句中的存储引擎选项无关。举例：在 MySQL 中，使用 Innodb 的表，在 `CREATE INDEX` 时只能使用 `BTREE` 索引，而在 TiDB 中既可以使用 `BTREE` 也可以使用 `HASH` 。

* MySQL 的 `algorithm_option` 和 `lock_option` 选项 TiDB 仅作语法支持。

* TiDB 单表最多支持 512 个列。InnoDB 的限制是 1017。MySQL 的硬限制是 4096。详见 MySQL 文档 [Limits on Table Column Count and Row Size](https://dev.mysql.com/doc/refman/5.7/en/column-count-limit.html)

## DROP INDEX 语法

```sql
DROP INDEX index_name ON tbl_name
```

`DROP INDEX` 用于删除表上的一个索引，目前暂不支持删除主键索引。

## ADMIN 语句

`ADMIN` 语句可以查看一些跟 DDL 任务相关的信息，具体可以看[这里](/dev/reference/sql/statements/admin.md)。
