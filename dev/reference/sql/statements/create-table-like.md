---
title: CREATE TABLE LIKE
summary: TiDB 数据库中 CREATE TABLE LIKE 的使用概况。
category: reference
---

# CREATE TABLE LIKE

`CREATE TABLE LIKE` 语句用于复制已有表的定义，但不复制任何数据。

## 语法图

**CreateTableStmt:**

![CreateTableStmt](/media/sqlgram/CreateTableStmt.png)

**LikeTableWithOrWithoutParen:**

![LikeTableWithOrWithoutParen](/media/sqlgram/LikeTableWithOrWithoutParen.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT NOT NULL);
```

```
Query OK, 0 rows affected (0.13 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE TABLE t2 LIKE t1;
```

```
Query OK, 0 rows affected (0.10 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t2;
```

```
Empty set (0.00 sec)
```

## MySQL 兼容性

`CREATE TABLE LIKE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/dev/report-issue.md)。

## 另请参阅

* [CREATE TABLE](/dev/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/dev/reference/sql/statements/show-create-table.md)
