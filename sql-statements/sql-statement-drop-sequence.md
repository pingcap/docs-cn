---
title: DROP SEQUENCE
summary: An overview of the usage of DROP SEQUENCE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-drop-sequence/','/docs/dev/reference/sql/statements/drop-sequence/']
---

# DROP SEQUENCE

The `DROP SEQUENCE` statement drops the sequence object in TiDB.

## Synopsis

```ebnf+diagram
DropSequenceStmt ::=
    'DROP' 'SEQUENCE' IfExists TableNameList

IfExists ::= ( 'IF' 'EXISTS' )?

TableNameList ::=
    TableName ( ',' TableName )*

TableName ::=
    Identifier ('.' Identifier)?
```

## Examples

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

## MySQL compatibility

This statement is a TiDB extension. The implementation is modeled on sequences available in MariaDB.

## See also

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
