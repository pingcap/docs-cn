---
title: KEYWORDS
summary: 了解 INFORMATION_SCHEMA 表 `KEYWORDS`。
---

# KEYWORDS

TiDB 从 v7.6.0 开始提供 `KEYWORDS` 表，你可以使用该表查看 TiDB 中[关键字](/keywords.md)的信息。

```sql
USE INFORMATION_SCHEMA;
DESC keywords;
```

输出结果如下：

```
+----------+--------------+------+------+---------+-------+
| Field    | Type         | Null | Key  | Default | Extra |
+----------+--------------+------+------+---------+-------+
| WORD     | varchar(128) | YES  |      | NULL    |       |
| RESERVED | int(11)      | YES  |      | NULL    |       |
+----------+--------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

字段含义如下：

- `WORD`：关键字
- `RESERVED`：关键字是否为保留关键字

例如，你可以使用以下 SQL 语句查询 `ADD` 和 `USER` 关键字的信息：

```sql
SELECT * FROM INFORMATION_SCHEMA.KEYWORDS WHERE WORD IN ('ADD','USER');
```

输出结果显示 `ADD` 是一个保留关键字，`USER` 是一个非保留关键字。

```
+------+----------+
| WORD | RESERVED |
+------+----------+
| ADD  |        1 |
| USER |        0 |
+------+----------+
2 rows in set (0.00 sec)
```
