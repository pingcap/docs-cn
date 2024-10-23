---
title: ADD COLUMN
summary: TiDB 数据库中 ADD COLUMN 的使用概况。
---

# ADD COLUMN

`ALTER TABLE.. ADD COLUMN` 语句用于在已有表中添加列。在 TiDB 中，`ADD COLUMN` 为在线操作，不会阻塞表中的数据读写。

## 语法图

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AddColumnSpec ( ',' AddColumnSpec )*

TableName ::=
    Identifier ('.' Identifier)?

AddColumnSpec
         ::= 'ADD' 'COLUMN' 'IF NOT EXISTS'? ColumnName ColumnType ColumnOption+ ( 'FIRST' | 'AFTER' ColumnName )?

ColumnType
         ::= NumericType
           | StringType
           | DateAndTimeType
           | 'SERIAL'

ColumnOption
         ::= 'NOT'? 'NULL'
           | 'AUTO_INCREMENT'
           | 'PRIMARY'? 'KEY' ( 'CLUSTERED' | 'NONCLUSTERED' )? ( 'GLOBAL' | 'LOCAL' )?
           | 'UNIQUE' 'KEY'? ( 'GLOBAL' | 'LOCAL' )?
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
```

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 VALUES (NULL);
```

```
Query OK, 1 row affected (0.02 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 ADD COLUMN c1 INT NOT NULL;
```

```
Query OK, 0 rows affected (0.28 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
+----+----+
| id | c1 |
+----+----+
|  1 |  0 |
+----+----+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 ADD c2 INT NOT NULL AFTER c1;
```

```
Query OK, 0 rows affected (0.28 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
+----+----+----+
| id | c1 | c2 |
+----+----+----+
|  1 |  0 |  0 |
+----+----+----+
1 row in set (0.00 sec)
```

## MySQL 兼容性

* 不支持将新添加的列设为 `PRIMARY KEY`。
* 不支持将新添加的列设为 `AUTO_INCREMENT`。
* 对添加生成列有局限性，具体可参考：[生成列局限性](/generated-columns.md#生成列的局限性)。
* TiDB 对[分区表](/partitioned-table.md)进行了扩展，你可以在添加新列时通过将 `PRIMARY KEY` 或 `UNIQUE INDEX` 设置为 `GLOBAL` 来设置[全局索引](/partitioned-table.md#全局索引)。该扩展与 MySQL 不兼容。

## 另请参阅

* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
