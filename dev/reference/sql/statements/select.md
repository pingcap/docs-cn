---
title: SELECT | TiDB SQL Statement Reference 
summary: An overview of the usage of SELECT for the TiDB database.
category: reference
---

# SELECT 

The `SELECT` statement is used to read data from TiDB.

## Synopsis

**SelectStmt:**

![SelectStmt](/media/sqlgram/SelectStmt.png)

**FromDual:**

![FromDual](/media/sqlgram/FromDual.png)

**WhereClauseOptional:**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

**SelectStmtOpts:**

![SelectStmtOpts](/media/sqlgram/SelectStmtOpts.png)

**SelectStmtFieldList:**

![SelectStmtFieldList](/media/sqlgram/SelectStmtFieldList.png)

**TableRefsClause:**

![TableRefsClause](/media/sqlgram/TableRefsClause.png)

**WhereClauseOptional:**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

**SelectStmtGroup:**

![SelectStmtGroup](/media/sqlgram/SelectStmtGroup.png)

**HavingClause:**

![HavingClause](/media/sqlgram/HavingClause.png)

**OrderByOptional:**

![OrderByOptional](/media/sqlgram/OrderByOptional.png)

**SelectStmtLimit:**

![SelectStmtLimit](/media/sqlgram/SelectStmtLimit.png)

**SelectLockOpt:**

![SelectLockOpt](/media/sqlgram/SelectLockOpt.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
5 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [INSERT](/dev/reference/sql/statements/insert.md)
* [DELETE](/dev/reference/sql/statements/delete.md)
* [UPDATE](/dev/reference/sql/statements/update.md)
* [REPLACE](/dev/reference/sql/statements/replace.md)
