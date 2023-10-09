---
title: UPDATE
summary: TiDB 数据库中 UPDATE 的使用概况。
---

# UPDATE

`UPDATE` 语句用于修改指定表中的数据。

## 语法图

**UpdateStmt:**

![UpdateStmt](/media/sqlgram/UpdateStmt.png)

**PriorityOpt:**

![PriorityOpt](/media/sqlgram/PriorityOpt.png)

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
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
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

在计算表达式中的列时，TiDB 总使用原始的值。例如：

```sql
CREATE TABLE t (a int, b int);
INSERT INTO t VALUES (1,2);
UPDATE t SET a = a+1,b=a;
```

在 MySQL 中，`b` 列的值会被更新成 2，因为 `b` 列被设置为与 `a` 列相同，而 `a`（最初是 1）在同一条语句中被更新成了 2。

TiDB 遵守标准的 SQL 行为，这里将 `b` 列值更新成 1。

## 另请参阅

* [INSERT](/sql-statements/sql-statement-insert.md)
* [SELECT](/sql-statements/sql-statement-select.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)
