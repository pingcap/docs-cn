---
title: REPLACE
summary: TiDB 数据库中 REPLACE 的使用概况。
category: reference
---

# REPLACE

从语义上看，`REPLACE` 语句是 `DELETE` 语句和 `INSERT` 语句的结合，可用于简化应用程序代码。

## 语法图

**ReplaceIntoStmt:**

![ReplaceIntoStmt](/media/sqlgram/ReplaceIntoStmt.png)

**PriorityOpt:**

![PriorityOpt](/media/sqlgram/PriorityOpt.png)

**IntoOpt:**

![IntoOpt](/media/sqlgram/IntoOpt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**InsertValues:**

![InsertValues](/media/sqlgram/InsertValues.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.12 sec)
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
REPLACE INTO t1 (id, c1) VALUES(3, 99);
```

```
Query OK, 2 rows affected (0.01 sec)
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
|  3 | 99 |
+----+----+
3 rows in set (0.00 sec)
```

## MySQL 兼容性

`REPLACE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/dev/report-issue.md)。

## 另请参阅

* [DELETE](/dev/reference/sql/statements/delete.md)
* [INSERT](/dev/reference/sql/statements/insert.md)
* [SELECT](/dev/reference/sql/statements/select.md)
* [UPDATE](/dev/reference/sql/statements/update.md)
