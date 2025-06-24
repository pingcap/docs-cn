---
title: KEYWORDS
summary: 了解 `KEYWORDS` INFORMATION_SCHEMA 表。
---

# KEYWORDS

从 v7.5.3 和 v7.6.0 版本开始，TiDB 提供了 `KEYWORDS` 表。你可以使用此表获取 TiDB 中[关键字](/keywords.md)的相关信息。

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

字段说明：

- `WORD`：关键字。
- `RESERVED`：表示该关键字是否为保留关键字。

以下语句查询 `ADD` 和 `USER` 关键字的信息：

```sql
SELECT * FROM INFORMATION_SCHEMA.KEYWORDS WHERE WORD IN ('ADD','USER');
```

从输出结果可以看出，`ADD` 是保留关键字，而 `USER` 是非保留关键字。

```
+------+----------+
| WORD | RESERVED |
+------+----------+
| ADD  |        1 |
| USER |        0 |
+------+----------+
2 rows in set (0.00 sec)
```
