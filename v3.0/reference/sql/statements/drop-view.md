---
title: DROP VIEW
summary: TiDB 数据库中 DROP VIEW 的使用概况。
category: reference
---

# DROP VIEW

`DROP VIEW` 语句用于从当前所选定的数据库中删除视图对象。视图所引用的基表不受影响。

## 语法图

**DropViewStmt:**

![DropViewStmt](/media/sqlgram/DropViewStmt.png)

**TableNameList:**

![TableNameList](/media/sqlgram/TableNameList.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

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
INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
CREATE VIEW v1 AS SELECT * FROM t1 WHERE c1 > 2;
```

```
Query OK, 0 rows affected (0.11 sec)
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
|  4 |  4 |
|  5 |  5 |
+----+----+
5 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM v1;
```

```
+----+----+
| id | c1 |
+----+----+
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
3 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DROP VIEW v1;
```

```
Query OK, 0 rows affected (0.23 sec)
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
|  4 |  4 |
|  5 |  5 |
+----+----+
5 rows in set (0.00 sec)
```

## MySQL 兼容性

`DROP VIEW` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/v3.0/report-issue.md)。

## See also

* [DROP TABLE](/v3.0/reference/sql/statements/drop-table.md)
* [CREATE VIEW](/v3.0/reference/sql/statements/create-view.md)
