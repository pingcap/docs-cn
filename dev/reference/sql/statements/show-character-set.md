---
title: SHOW CHARACTER SET
summary: TiDB 数据库中 SHOW CHARACTER SET 的使用概况。
category: reference
---

# SHOW CHARACTER SET

`SHOW CHARACTER SET` 语句提供 TiDB 中可用字符集的静态列表。此列表不反映当前连接或用户的任何属性。

## 语法图

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

**CharsetKw:**

![CharsetKw](/media/sqlgram/CharsetKw.png)

## 示例

```sql
mysql> SHOW CHARACTER SET;
+---------+---------------+-------------------+--------+
| Charset | Description   | Default collation | Maxlen |
+---------+---------------+-------------------+--------+
| utf8    | UTF-8 Unicode | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode | utf8mb4_bin       |      4 |
| ascii   | US ASCII      | ascii_bin         |      1 |
| latin1  | Latin1        | latin1_bin        |      1 |
| binary  | binary        | binary            |      1 |
+---------+---------------+-------------------+--------+
5 rows in set (0.00 sec)
```

## MySQL 兼容性

`SHOW CHARACTER SET` 语句可视为与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上 提交 [issue](/report-issue.md)。

## 另请参阅

* [SHOW COLLATION](/dev/reference/sql/statements/show-collation.md)