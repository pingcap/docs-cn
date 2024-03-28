---
title: CHANGE COLUMN
summary: TiDB 数据库中 CHANGE COLUMN 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-change-column/','/docs-cn/dev/reference/sql/statements/change-column/']
---

# CHANGE COLUMN

`ALTER TABLE .. CHANGE COLUMN` 语句用于在已有表上更改列，包括对列进行重命名，和将数据改为兼容类型。

从 v5.1.0 版本起，TiDB 开始支持 Reorg 数据的类型变更，包括但不限于：

- 从 varchar 转换为 bigint
- decimal 精度修改
- 从 varchar(10) 到 varchar(5) 的长度压缩

## 语法图

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName ChangeColumnSpec ( ',' ChangeColumnSpec )*

ChangeColumnSpec
         ::= 'CHANGE' ColumnKeywordOpt 'IF EXISTS' ColumnName ColumnName ColumnType ColumnOption* ( 'FIRST' | 'AFTER' ColumnName )?

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

创建表 `t1` 并插入数据：

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
INSERT INTO t1 (col1) VALUES (1),(2),(3),(4),(5);
SELECT * FROM t1;
```

表 `t1` 的数据如下：

```sql
+----+------+
| id | col1 |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
|  4 |    4 |
|  5 |    5 |
+----+------+
5 rows in set (0.01 sec)
```

将表 `t1` 的列 `col1` 重命名为 `col2`：

```sql
ALTER TABLE t1 CHANGE col1 col2 INT;
SELECT * FROM t1;
```

表 `t1` 的数据如下：

```sql
+----+------+
| id | col2 |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
|  4 |    4 |
|  5 |    5 |
+----+------+
5 rows in set (0.01 sec)
```

将表 `t1` 的列 `col2` 重命名为 `col3`，并将列的类型从 `INT` 改为 `BIGINT`：

```sql
ALTER TABLE t1 CHANGE col2 col3 BIGINT, ALGORITHM=INSTANT;
SELECT * FROM t1;
```

表 `t1` 的数据如下：

```sql
+----+------+
| id | col3 |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
|  4 |    4 |
|  5 |    5 |
+----+------+
5 rows in set (0.00 sec)
```

下面语句将表 `t1` 的列 `col3` 重命名为 `col4`，并将主键 `id` 重命名为 `id2`：

```sql
ALTER TABLE t1 CHANGE col3 col4 BIGINT, CHANGE id id2 INT NOT NULL;
ERROR 8200 (HY000): Unsupported modify column: can't remove auto_increment without @@tidb_allow_remove_auto_inc enabled
```

由于 `id` 是自增列，所以不能直接将其重命名为 `id2`。需要先开启 [`tidb_allow_remove_auto_inc`](/system-variables.md#tidb_allow_remove_auto_inc-从-v2118-和-v304-版本开始引入)，然后再执行 `ALTER TABLE` 语句：

```sql
SET tidb_allow_remove_auto_inc = ON;
ALTER TABLE t1 CHANGE col3 col4 BIGINT, CHANGE id id2 INT NOT NULL;
SELECT * FROM t1;
```

表 `t1` 的数据如下：

```
+-----+------+
| id2 | col4 |
+-----+------+
|   1 |    1 |
|   2 |    2 |
|   3 |    3 |
|   4 |    4 |
|   5 |    5 |
+-----+------+
5 rows in set (0.00 sec)
```

## MySQL 兼容性

* 不支持主键列上 [Reorg-Data](/sql-statements/sql-statement-modify-column.md#reorg-data-change) 类型的变更。

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t CHANGE COLUMN a a VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: this column has primary key flag
    ```

* 不支持分区表上的列类型变更。

    ```sql
    CREATE TABLE t (c1 INT, c2 INT, c3 INT) partition by range columns(c1) ( partition p0 values less than (10), partition p1 values less than (maxvalue));
    ALTER TABLE t CHANGE COLUMN c1 c1 DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: table is partition table
    ```

* 不支持生成列上的列类型变更。

    ```sql
    CREATE TABLE t (a INT, b INT as (a+1));
    ALTER TABLE t CHANGE COLUMN b b VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: newCol IsGenerated false, oldCol IsGenerated true
    ```

* 不支持部分数据类型（例如，部分时间类型、Bit、Set、Enum、JSON 等）的变更，因为 TiDB 中 `CAST` 函数与 MySQL 的行为存在兼容性问题。

  ```sql
  CREATE TABLE t (a DECIMAL(13, 7));
  ALTER TABLE t CHANGE COLUMN a a DATETIME;
  ERROR 8200 (HY000): Unsupported modify column: [ddl:8200]Unsupported modify column: change from original type decimal(13,7) to datetime is currently unsupported yet
  ```

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
* [MODIFY COLUMN](/sql-statements/sql-statement-modify-column.md)
