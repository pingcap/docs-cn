---
title: UPDATE | TiDB SQL Statement Reference 
summary: An overview of the usage of UPDATE for the TiDB database.
category: reference
---

# UPDATE

The `UPDATE` statement is used to modify data in a specified table.

## Synopsis

**UpdateStmt:**

![UpdateStmt](/media/sqlgram/UpdateStmt.png)

**TableRef:**

![TableRef](/media/sqlgram/TableRef.png)

**TableRefs:**

![TableRefs](/media/sqlgram/TableRefs.png)

**AssignmentList:**

![AssignmentList](/media/sqlgram/AssignmentList.png)

**WhereClauseOptional:**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1), (2), (3);
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
+----+----+
3 rows in set (0.00 sec)

mysql> UPDATE t1 SET c1=5 WHERE c1=3;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  5 |
+----+----+
3 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [INSERT](/reference/sql/statements/insert.md)
* [SELECT](/reference/sql/statements/select.md)
* [DELETE](/reference/sql/statements/delete.md)
* [REPLACE](/reference/sql/statements/replace.md)
