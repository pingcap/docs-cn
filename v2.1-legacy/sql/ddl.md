---
title: Data Definition Statements
summary: Learn how to use DDL (Data Definition Language) in TiDB.
category: user guide
---

# Data Definition Statements

DDL (Data Definition Language) is used to define the database structure or schema, and to manage the database and statements of various objects in the database.

Currently, TiDB has implemented concurrent execution of the `ADD INDEX` operation and the `GENERAL` operation (namely the non-`ADD INDEX` DDL operation) across different tables. In this case, two workers process the `ADD INDEX` operation and a `GENERAL` operation respectively. When the operation requests are on the same table, workers execute these operations in the order of receiving the DDL operation requests. This feature is to guarantee the `ADD INDEX` operation (its execution time is longer than that of other operations in TiDB) does not block other DDL operations.

## CREATE DATABASE syntax

```sql
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
    [create_specification] ...

create_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```

The `CREATE DATABASE` statement is used to create a database, and to specify the default properties of the database, such as the default character set and validation rules. `CREATE SCHEMA` is a synonym for `CREATE DATABASE`.

If you create an existing database and does not specify `IF NOT EXISTS`, an error is displayed.

The `create_specification` option is used to specify the specific `CHARACTER SET` and `COLLATE` in the database. Currently, the option is only supported in syntax.

## DROP DATABASE syntax

```sql
DROP {DATABASE | SCHEMA} [IF EXISTS] db_name
```

The `DROP DATABASE` statement is used to delete the specified database and its tables.

The `IF EXISTS` statement is used to prevent an error if the database does not exist.

## CREATE TABLE syntax

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

The `CREATE TABLE` statement is used to create a table. Currently, it does not support temporary tables, `CHECK` constraints, or importing data from other tables while creating tables. It supports some of the `Partition_options` in syntax.

- When you create an existing table and if you specify `IF NOT EXIST`, it does not report an error. Otherwise, it reports an error.
- Use `LIKE` to create an empty table based on the definition of another table including its column and index properties.
- The `FULLTEXT` and `FOREIGN KEY` in `create_definition` are currently only supported in syntax.
- For the `data_type`, see [Data Types](../sql/datatype.md).
- The `[ASC | DESC]` in `index_col_name` is currently only supported in syntax.
- The `index_type` is currently only supported in syntax.
- The `KEY_BLOCK_SIZE` in `index_option` is currently only supported in syntax.
- The `table_option` currently only supports `AUTO_INCREMENT`, `CHARACTER SET` and `COMMENT`, while the others are only supported in syntax. The clauses are separated by a comma `,`. See the following table for details:
  
    | Parameters | Description | Example |
    | ---------- | ---------- | ------- |
    | `AUTO_INCREMENT` | The initial value of the increment field | `AUTO_INCREMENT` = 5 |
    | `CHARACTER SET` | To specify the string code for the table; currently only support UTF8MB4 | `CHARACTER SET` =  'utf8mb4' |
    | `COMMENT` | The comment information | `COMMENT` = 'comment info' |
  
### AUTO_INCREMENT description

The TiDB automatic increment ID (`AUTO_INCREMENT` ID) only guarantees automatic increment and uniqueness and does not guarantee continuous allocation. Currently, TiDB adopts bulk allocation. If you insert data into multiple TiDB servers at the same time, the allocated automatic increment ID is not continuous.

You can specify the `AUTO_INCREMENT` for integer fields. A table only supports one field with the `AUTO_INCREMENT` property.

## DROP TABLE syntax

```sql
DROP TABLE [IF EXISTS]
    tbl_name [, tbl_name] ...
    [RESTRICT | CASCADE]
```

You can delete multiple tables at the same time. The tables are separated by a comma `,`.

If you delete a table that does not exist and does not specify the use of `IF EXISTS`, an error is displayed.

The RESTRICT and CASCADE keywords do nothing. They are permitted to make porting easier from other database systems.

## TRUNCATE TABLE syntax

```sql
TRUNCATE [TABLE] tbl_name
```

The `TRUNCATE TABLE` statement is used to clear all the data in the specified table but keeps the table structure.

This operation is similar to deleting all the data of a specified table, but it is much faster and is not affected by the number of rows in the table.

> **Note:**
>
> If you use the `TRUNCATE TABLE` statement, the value of `AUTO_INCREMENT` in the original table is reset to its starting value.

## RENAME TABLE syntax

```sql
RENAME TABLE
    tbl_name TO new_tbl_name
```

The `RENAME TABLE` statement is used to rename a table. 

This statement is equivalent to the following `ALTER TABLE` statement:

```sql
ALTER TABLE old_table RENAME new_table;
```

## ALTER TABLE syntax

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

The `ALTER TABLE` statement is used to update the structure of an existing table, such as updating the table or table properties, adding or deleting columns, creating or deleting indexes, updating columns or column properties. The descriptions of several field types are as follows:

- For `index_col_name`, `index_type`, and `index_option`, see [CREATE INDEX Syntax](#create-index-syntax).
- Currently, the `table_option` supports `AUTO_INCREMENT` and `COMMENT`, while the others are only supported in syntax.

The support for specific operation types is as follows:

- `ADD/DROP INDEX/COLUMN`: currently, does not support the creation or deletion of multiple indexes or columns at the same time
- `ADD/DROP PRIMARY KEY`: currently not supported
- `DROP COLUMN`: currently does not support the deletion of columns that are primary key columns or index columns
- `ADD COLUMN`: currently, does not support setting the newly added column as the primary key or unique index at the same time, and does not support setting the column property to `AUTO_INCREMENT`
- `CHANGE/MODIFY COLUMN`: currently supports some of the syntaxes, and the details are as follows:
  - In updating data types, the `CHANGE/MODIFY COLUMN` only supports updates between integer types, updates between string types, and updates between Blob types. You can only extend the length of the original type. The column properties of `unsigned`/`charset`/`collate` cannot be changed. The specific supported types are classified as follows:
      - Integer types: `TinyInt`, `SmallInt`, `MediumInt`, `Int`, `BigInt`
      - String types: `Char`, `Varchar`, `Text`, `TinyText`, `MediumText`, `LongText`
      - Blob types: `Blob`, `TinyBlob`, `MediumBlob`, `LongBlob`
  - In updating type definition, the `CHANGE/MODIFY COLUMN` supports `default value`, `comment`, `null`, `not null` and `OnUpdate`.
  - The `CHANGE/MODIFY COLUMN` does not support the update of `enum` type column.
- `LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}`: is currently only supported in syntax    

## CREATE INDEX syntax

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

The `CREATE INDEX` statement is used to create the index for an existing table. In function, `CREATE INDEX` corresponds to the index creation of `ALTER TABLE`. Similar to MySQL, the `CREATE INDEX` cannot create a primary key index.

### Difference from MySQL

- The `CREATE INDEX` supports the `UNIQUE` index and does not support `FULLTEXT` and `SPATIAL` indexes.
- The `index_col_name` supports the length option with a maximum length limit of 3072 bytes. The length limit does not change depending on the storage engine, and character set used when building the table. This is because TiDB does not use storage engines like InnoDB and MyISAM, and only provides syntax compatibility with MySQL for the storage engine options when creating tables. Similarly, TiDB uses the utf8mb4 character set, and only provides syntax compatibility with MySQL for the character set options when creating tables. For more information, see [Compatibility with MySQL](../sql/mysql-compatibility.md).
- The `index_col_name` supports the index sorting options of `ASC` and `DESC`. The behavior of sorting options is similar to MySQL, and only syntax parsing is supported. All the internal indexes are stored in ascending order. For more information, see [CREATE INDEX Syntax](https://dev.mysql.com/doc/refman/5.7/en/create-index.html).
- The `index_option` supports `KEY_BLOCK_SIZE`, `index_type` and `COMMENT`. The `COMMENT` supports a maximum of 1024 characters and does not support the `WITH PARSER` option.
- The `index_type` supports `BTREE` and `HASH` only in MySQL syntax, which means the index type is independent of the storage engine option in the creating table statement. For example, in MySQL, when you use `CREATE INDEX` on a table using InnoDB, it only supports the `BTREE` index, while TiDB supports both `BTREE` and `HASH` indexes.
- TiDB supports `algorithm_option` and `lock_option` only in MySQL syntax.
- TiDB supports at most 512 columns in a single table. The corresponding number limit in InnoDB is 1017, and the hard limit in MySQL is 4096. For more details, see [Limits on Table Column Count and Row Size](https://dev.mysql.com/doc/refman/5.7/en/column-count-limit.html).

## DROP INDEX syntax

```sql
DROP INDEX index_name ON tbl_name
```

The `DROP INDEX` statement is used to delete a table index. Currently, it does not support deleting the primary key index.

## ADMIN statement

You can use the `ADMIN` statement to view the information related to DDL job. For details, see [here](../sql/admin.md#admin-statement).
