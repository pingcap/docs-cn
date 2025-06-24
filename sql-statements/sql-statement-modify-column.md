---
title: MODIFY COLUMN | TiDB SQL 语句参考
summary: TiDB 数据库中 MODIFY COLUMN 的使用概览。
---

# MODIFY COLUMN

`ALTER TABLE.. MODIFY COLUMN` 语句修改现有表上的列。修改可以包括更改数据类型和属性。如果同时需要重命名，请使用 [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) 语句。

从 v5.1.0 开始，TiDB 支持 Reorg 数据的数据类型更改，包括但不限于：

- 将 `VARCHAR` 更改为 `BIGINT`
- 修改 `DECIMAL` 精度
- 将 `VARCHAR(10)` 的长度压缩为 `VARCHAR(5)`

## 语法

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName ModifyColumnSpec ( ',' ModifyColumnSpec )*

ModifyColumnSpec
         ::= 'MODIFY' ColumnKeywordOpt 'IF EXISTS' ColumnName ColumnType ColumnOption* ( 'FIRST' | 'AFTER' ColumnName )?

ColumnType
         ::= NumericType
           | StringType
           | DateAndTimeType
           | 'SERIAL'

ColumnOption
         ::= 'NOT'? 'NULL'
           | 'AUTO_INCREMENT'
           | 'PRIMARY'? 'KEY' ( 'CLUSTERED' | 'NONCLUSTERED' )?
           | 'UNIQUE' 'KEY'?
           | 'DEFAULT' ( NowSymOptionFraction | SignedLiteral | NextValueForSequence )
           | 'SERIAL' 'DEFAULT' 'VALUE'
           | 'ON' 'UPDATE' NowSymOptionFraction
           | 'COMMENT' stringLit
           | ( 'CONSTRAINT' Identifier? )? 'CHECK' '(' Expression ')' ( 'NOT'? ( 'ENFORCED' | 'NULL' ) )?
           | 'GENERATED' 'ALWAYS' 'AS' '(' Expression ')' ( 'VIRTUAL' | 'STORED' )?
           | 'REFERENCES' TableName ( '(' IndexPartSpecificationList ')' )? Match? OnDeleteUpdateOpt
           | 'COLLATE' CollationName
           | 'COLUMN_FORMAT' ColumnFormat
           | 'STORAGE' StorageMedia
           | 'AUTO_RANDOM' ( '(' LengthNum ')' )?

ColumnName ::=
    Identifier ( '.' Identifier ( '.' Identifier )? )?
```

## 示例

### 仅元数据更改

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (col1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 MODIFY col1 BIGINT;
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE t1\G
```

```sql
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `col1` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001
1 row in set (0.00 sec)
```

### Reorg 数据更改

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (col1) VALUES (12345),(67890);
```

```
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 MODIFY col1 VARCHAR(5);
```

```
Query OK, 0 rows affected (2.52 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE t1\G
```

```sql
*************************** 1. row ***************************
       Table: t1
CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `col1` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001
1 row in set (0.00 sec)
```

> **注意：**
>
> - 当更改的数据类型与现有数据行冲突时，TiDB 会返回错误。在上面的示例中，TiDB 返回以下错误：
>
>    ```
>    alter table t1 modify column col1 varchar(4);
>    ERROR 1406 (22001): Data Too Long, field len 4, data len 5
>    ```
>
> - 由于与 Async Commit 功能的兼容性，DDL 语句在开始处理 Reorg 数据之前会等待一段时间（约 2.5 秒）。
>
>    ```
>    Query OK, 0 rows affected (2.52 sec)
>    ```

## MySQL 兼容性

* 不支持在主键列上修改 Reorg 数据类型，但支持修改仅元数据类型。例如：

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: column has primary key flag
    ```

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a INT(10) UNSIGNED;
    ERROR 8200 (HY000): Unsupported modify column: column has primary key flag
    ```

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a bigint;
    Query OK, 0 rows affected (0.01 sec)
    ```

* 不支持修改生成列的列类型。例如：

    ```sql
    CREATE TABLE t (a INT, b INT as (a+1));
    ALTER TABLE t MODIFY COLUMN b VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: column is generated
    ```

* 不支持修改分区表的列类型。例如：

    ```sql
    CREATE TABLE t (c1 INT, c2 INT, c3 INT) partition by range columns(c1) ( partition p0 values less than (10), partition p1 values less than (maxvalue));
    ALTER TABLE t MODIFY COLUMN c1 DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: table is partition table
    ```

* 由于 TiDB 和 MySQL 之间 `cast` 函数行为的一些兼容性问题，不支持从某些数据类型（例如某些 TIME 类型、BIT、SET、ENUM、JSON）转换为其他类型。

    ```sql
    CREATE TABLE t (a DECIMAL(13, 7));
    ALTER TABLE t MODIFY COLUMN a DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: change from original type decimal(13,7) to datetime is currently unsupported yet
    ```

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
* [CHANGE COLUMN](/sql-statements/sql-statement-change-column.md)
