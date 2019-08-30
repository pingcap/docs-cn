---
title: UPDATE
summary: TiDB 数据库中 UPDATE 的使用概况。
category: reference
---

# UPDATE

`UPDATE` 语句用于修改指定表中的数据。

## 语法图

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

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
+----+----+
3 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
UPDATE t1 SET c1=5 WHERE c1=3;
```

```
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  5 |
+----+----+
3 rows in set (0.00 sec)
```

## MySQL 兼容性

`UPDATE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/report-issue.md)。

## 另请参阅

* [INSERT](/reference/sql/statements/insert.md)
* [SELECT](/reference/sql/statements/select.md)
* [DELETE](/reference/sql/statements/delete.md)
* [REPLACE](/reference/sql/statements/replace.md)
