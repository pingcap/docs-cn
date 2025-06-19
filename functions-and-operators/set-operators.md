---
title: 集合运算
summary: 了解 TiDB 支持的集合运算。
---

# 集合运算

TiDB 支持使用 UNION、EXCEPT 和 INTERSECT 运算符进行三种集合运算。集合的最小单位是 [`SELECT` 语句](/sql-statements/sql-statement-select.md)。

## UNION 运算符

在数学中，两个集合 A 和 B 的并集由 A 或 B 中的所有元素组成。例如：

```sql
SELECT 1 UNION SELECT 2;
+---+
| 1 |
+---+
| 2 |
| 1 |
+---+
2 rows in set (0.00 sec)
```

TiDB 同时支持 `UNION DISTINCT` 和 `UNION ALL` 运算符。`UNION DISTINCT` 从结果集中删除重复记录，而 `UNION ALL` 保留所有记录，包括重复项。在 TiDB 中默认使用 `UNION DISTINCT`。

```sql
CREATE TABLE t1 (a int);
CREATE TABLE t2 (a int);
INSERT INTO t1 VALUES (1),(2);
INSERT INTO t2 VALUES (1),(3);
```

以下分别是 `UNION DISTINCT` 和 `UNION ALL` 查询的示例：

```sql
SELECT * FROM t1 UNION DISTINCT SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
+---+
3 rows in set (0.00 sec)

SELECT * FROM t1 UNION ALL SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 1 |
| 3 |
+---+
4 rows in set (0.00 sec)
```

## EXCEPT 运算符

如果 A 和 B 是两个集合，EXCEPT 返回 A 和 B 的差集，即在 A 中但不在 B 中的元素组成的集合。

```sql
SELECT * FROM t1 EXCEPT SELECT * FROM t2;
+---+
| a |
+---+
| 2 |
+---+
1 rows in set (0.00 sec)
```

目前尚不支持 `EXCEPT ALL` 运算符。

## INTERSECT 运算符

在数学中，两个集合 A 和 B 的交集由同时在 A 和 B 中的所有元素组成，不包含其他元素。

```sql
SELECT * FROM t1 INTERSECT SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

目前尚不支持 `INTERSECT ALL` 运算符。INTERSECT 运算符的优先级高于 EXCEPT 和 UNION 运算符。

```sql
SELECT * FROM t1 UNION ALL SELECT * FROM t1 INTERSECT SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
| 1 |
| 2 |
+---+
3 rows in set (0.00 sec)
```

## 括号

TiDB 支持使用括号来指定集合运算的优先级。括号中的表达式会首先被处理。

```sql
(SELECT * FROM t1 UNION ALL SELECT * FROM t1) INTERSECT SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

## 使用 `ORDER BY` 和 `LIMIT`

TiDB 支持在集合运算的整个结果上使用 `ORDER BY` 或 `LIMIT` 子句。这两个子句必须位于整个语句的末尾。

```sql
(SELECT * FROM t1 UNION ALL SELECT * FROM t1 INTERSECT SELECT * FROM t2) ORDER BY a LIMIT 2;
+---+
| a |
+---+
| 1 |
| 1 |
+---+
2 rows in set (0.00 sec)
```
