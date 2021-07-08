---
title: MODIFY COLUMN | TiDB SQL Statement Reference
summary: An overview of the usage of MODIFY COLUMN for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-modify-column/','/docs/dev/reference/sql/statements/modify-column/']
---

# MODIFY COLUMN

The `ALTER TABLE.. MODIFY COLUMN` statement modifies a column on an existing table. The modification can include changing the data type and attributes. To rename at the same time, use the [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) statement instead.

Since v5.1.0, TiDB has supported changes of data types for Reorg data, including but not limited to:

- Changing `VARCHAR` to `BIGINT`
- Modifying the `DECIMAL` precision
- Compressing the length of `VARCHAR(10)` to `VARCHAR(5)`

## Synopsis

```ebnf+diagram
AlterTableStmt ::=
    'ALTER' IgnoreOptional 'TABLE' TableName ( AlterTableSpecListOpt AlterTablePartitionOpt | 'ANALYZE' 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList )? AnalyzeOptionListOpt )

AlterTableSpec ::=
    TableOptionList
|   'SET' 'TIFLASH' 'REPLICA' LengthNum LocationLabelList
|   'CONVERT' 'TO' CharsetKw ( CharsetName | 'DEFAULT' ) OptCollate
|   'ADD' ( ColumnKeywordOpt IfNotExists ( ColumnDef ColumnPosition | '(' TableElementList ')' ) | Constraint | 'PARTITION' IfNotExists NoWriteToBinLogAliasOpt ( PartitionDefinitionListOpt | 'PARTITIONS' NUM ) )
|   ( ( 'CHECK' | 'TRUNCATE' ) 'PARTITION' | ( 'OPTIMIZE' | 'REPAIR' | 'REBUILD' ) 'PARTITION' NoWriteToBinLogAliasOpt ) AllOrPartitionNameList
|   'COALESCE' 'PARTITION' NoWriteToBinLogAliasOpt NUM
|   'DROP' ( ColumnKeywordOpt IfExists ColumnName RestrictOrCascadeOpt | 'PRIMARY' 'KEY' | 'PARTITION' IfExists PartitionNameList | ( KeyOrIndex IfExists | 'CHECK' ) Identifier | 'FOREIGN' 'KEY' IfExists Symbol )
|   'EXCHANGE' 'PARTITION' Identifier 'WITH' 'TABLE' TableName WithValidationOpt
|   ( 'IMPORT' | 'DISCARD' ) ( 'PARTITION' AllOrPartitionNameList )? 'TABLESPACE'
|   'REORGANIZE' 'PARTITION' NoWriteToBinLogAliasOpt ReorganizePartitionRuleOpt
|   'ORDER' 'BY' AlterOrderItem ( ',' AlterOrderItem )*
|   ( 'DISABLE' | 'ENABLE' ) 'KEYS'
|   ( 'MODIFY' ColumnKeywordOpt IfExists | 'CHANGE' ColumnKeywordOpt IfExists ColumnName ) ColumnDef ColumnPosition
|   'ALTER' ( ColumnKeywordOpt ColumnName ( 'SET' 'DEFAULT' ( SignedLiteral | '(' Expression ')' ) | 'DROP' 'DEFAULT' ) | 'CHECK' Identifier EnforcedOrNot | 'INDEX' Identifier IndexInvisible )
|   'RENAME' ( ( 'COLUMN' | KeyOrIndex ) Identifier 'TO' Identifier | ( 'TO' | '='? | 'AS' ) TableName )
|   LockClause
|   AlgorithmClause
|   'FORCE'
|   ( 'WITH' | 'WITHOUT' ) 'VALIDATION'
|   'SECONDARY_LOAD'
|   'SECONDARY_UNLOAD'

ColumnKeywordOpt ::= 'COLUMN'?

ColumnDef ::=
    ColumnName ( Type | 'SERIAL' ) ColumnOptionListOpt

ColumnPosition ::=
    ( 'FIRST' | 'AFTER' ColumnName )?
```

## Examples

### Meta-Only Change

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
SHOW CREATE TABLE t1\G;
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

### Reorg-Data Change

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
SHOW CREATE TABLE t1\G;
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

> **Note:**
>
> - TiDB returns an error when the changed data type conflicts with an existing data row. In the above example, TiDB returns the following error:
>
>    ```
>    alter table t1 modify column col1 varchar(4);
>    ERROR 1406 (22001): Data Too Long, field len 4, data len 5
>    ```
>
> - Due to the compatibility with the Async Commit feature, the DDL statement waits for a period of time (about 2.5s) before starting to process into Reorg Data.
>
>    ```
>    Query OK, 0 rows affected (2.52 sec)
>    ```

## MySQL compatibility

* Does not support modifying multiple columns using a single `ALTER TABLE` statement. For example:

    ```sql
    ALTER TABLE t1 MODIFY col1 BIGINT, MODIFY id BIGINT NOT NULL;
    ERROR 1105 (HY000): Unsupported multi schema change
    ```

* Does not support modifying the Reorg-Data types on the primary key columns but supports modifying the Meta-Only types. For example:

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: column has primary key flag
    ```

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a bigint;
    Query OK, 0 rows affected (0.01 sec)
    ```

* Does not support modifying the column types on generated columns. For example:

    ```sql
    CREATE TABLE t (a INT, b INT as (a+1));
    ALTER TABLE t MODIFY COLUMN b VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: column is generated
    ```

* Does not support modifying the column types on the partitioned tables. For example:

    ```sql
    CREATE TABLE t (c1 INT, c2 INT, c3 INT) partition by range columns(c1) ( partition p0 values less than (10), partition p1 values less than (maxvalue));
    ALTER TABLE t MODIFY COLUMN c1 DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: table is partition table
    ```

* Does not support modifying some data types (for example, some TIME types, Bit, Set, Enum, JSON) are not supported due to some compatibility issues of the `cast` function's behavior between TiDB and MySQL.

    ```sql
    CREATE TABLE t (a DECIMAL(13, 7));
    ALTER TABLE t MODIFY COLUMN a DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: change from original type decimal(13,7) to datetime is currently unsupported yet
    ```

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
* [CHANGE COLUMN](/sql-statements/sql-statement-change-column.md)
