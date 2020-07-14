---
title: DROP SEQUENCE
summary: An overview of the usage of DROP SEQUENCE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-drop-sequence/','/docs/dev/reference/sql/statements/drop-sequence/']
---

# DROP SEQUENCE

The `DROP SEQUENCE` statement drops the sequence object in TiDB.

## Synopsis

**DropSequenceStmt:**

![DropSequenceStmt](/media/sqlgram/DropSequenceStmt.png)

**IfExists:**

![IfExists](/media/sqlgram/IfExists.png)

**TableNameList:**

![TableNameList](/media/sqlgram/TableNameList.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

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

Currently, sequence object is not supported by MySQL.

## See also

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
