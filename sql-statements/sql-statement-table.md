---
title: TABLE
summary: TiDB 数据库中 TABLE 语句的使用概况。
---

# TABLE

当不需要聚合或复杂的过滤操作时，可以用 `TABLE` 语句代替 `SELECT * FROM`。

## 语法图

```ebnf+diagram
TableStmt ::=
    "TABLE" Table ( "ORDER BY" Column )? ( "LIMIT" NUM )?
```

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1(id INT PRIMARY KEY);
```

```sql
Query OK, 0 rows affected (0.31 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 VALUES (1),(2),(3);
```

```sql
Query OK, 3 rows affected (0.06 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
TABLE t1;
```

```sql
+----+
| id |
+----+
|  1 |
|  2 |
|  3 |
+----+
3 rows in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
TABLE t1 ORDER BY id DESC;
```

```sql
+----+
| id |
+----+
|  3 |
|  2 |
|  1 |
+----+
3 rows in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
TABLE t1 LIMIT 1;
```

```sql
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.01 sec)
```

## MySQL 兼容性

`TABLE` 语句是从 MySQL 8.0.19 开始引入的。

## 另请参阅

- [SELECT](/sql-statements/sql-statement-select.md)
- [TABLE statements in MySQL](https://dev.mysql.com/doc/refman/8.0/en/table.html)
