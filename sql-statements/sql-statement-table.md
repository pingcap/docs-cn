---
title: TABLE | TiDB SQL 语句参考
summary: TiDB 数据库中 TABLE 的使用概述。
---

# TABLE

当不需要聚合或复杂过滤时，可以使用 `TABLE` 语句代替 `SELECT * FROM`。

## 语法图

```ebnf+diagram
TableStmt ::=
    "TABLE" Table ( "ORDER BY" Column )? ( "LIMIT" NUM )?
```

## 示例

创建表 `t1`：

```sql
CREATE TABLE t1(id INT PRIMARY KEY);
```

向 `t1` 插入一些数据：

```sql
INSERT INTO t1 VALUES (1),(2),(3);
```

查看表 `t1` 中的数据：

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

查询 `t1` 并按 `id` 字段降序排序：

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

查询 `t1` 中的第一条记录：

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

`TABLE` 语句在 MySQL 8.0.19 中引入。

## 另请参阅

- [`SELECT`](/sql-statements/sql-statement-select.md)
- [MySQL 中的 `TABLE` 语句](https://dev.mysql.com/doc/refman/8.0/en/table.html)
