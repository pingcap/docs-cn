---
title: DROP SEQUENCE
summary: An overview of the usage of DROP SEQUENCE for the TiDB database.
category: reference
---

# DROP SEQUENCE

The `DROP SEQUENCE` statement drops the sequence object in TiDB.

## Synopsis

**DropSequenceStmt:**

![DropSequenceStmt](/media/sqlgram/DropSequenceStmt.png)

**OptTemporary:**

![OptTemporary](/media/sqlgram/OptTemporary.png)

**IfExists:**

![IfExists](/media/sqlgram/IfExists.png)

**TableNameList:**

![TableNameList](/media/sqlgram/TableNameList.png)

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

Currently, MySQL does not have the sequence option. The TiDB sequence is borrowed from MariaDB. Except for the `SETVAL` function, all other functions have the same progressions with those functions of MariaDB.

## See also

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
