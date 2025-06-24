---
title: DROP SEQUENCE
summary: TiDB 数据库中 DROP SEQUENCE 的使用概述。
---

# DROP SEQUENCE

`DROP SEQUENCE` 语句用于在 TiDB 中删除序列对象。

## 语法图

```ebnf+diagram
DropSequenceStmt ::=
    'DROP' 'SEQUENCE' IfExists TableNameList

IfExists ::= ( 'IF' 'EXISTS' )?

TableNameList ::=
    TableName ( ',' TableName )*

TableName ::=
    Identifier ('.' Identifier)?
```

## 示例

{{< copyable "sql" >}}

```sql
DROP SEQUENCE seq;
```

```
Query OK, 0 rows affected (0.10 sec)
```

{{< copyable "sql" >}}

```sql
DROP SEQUENCE seq, seq2;
```

```
Query OK, 0 rows affected (0.03 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。其实现参考了 MariaDB 中可用的序列。

## 另请参阅

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [ALTER SEQUENCE](/sql-statements/sql-statement-alter-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
