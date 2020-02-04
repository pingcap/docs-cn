---
title: TRUNCATE
summary: TiDB 数据库中 TRUNCATE 的使用概况。
category: reference
---

# TRUNCATE

`TRUNCATE` 语句以非事务方式从表中删除所有数据。可认为 `TRUNCATE` 语句同 `DROP TABLE` + `CREATE TABLE` 组合在语义上相同，定义与 `DROP TABLE` 语句相同。

`TRUNCATE TABLE tableName` 和 `TRUNCATE tableName` 均为有效语法。

## 语法图

**TruncateTableStmt:**

![TruncateTableStmt](/media/sqlgram/TruncateTableStmt.png)

**OptTable:**

![OptTable](/media/sqlgram/OptTable.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.01 sec)
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
TRUNCATE t1;
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
Empty set (0.00 sec)
```

{{< copyable "sql" >}}

```sqlS
INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
TRUNCATE TABLE t1;
```

```
Query OK, 0 rows affected (0.11 sec)
```

## MySQL 兼容性

`TRUNCATE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/dev/report-issue.md)。

## 另请参阅

* [DROP TABLE](/dev/reference/sql/statements/drop-table.md)
* [DELETE](/dev/reference/sql/statements/delete.md)
* [CREATE TABLE](/dev/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/dev/reference/sql/statements/show-create-table.md)
