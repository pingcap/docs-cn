---
title: SHOW CHARACTER SET
summary: TiDB 数据库中 SHOW CHARACTER SET 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-character-set/','/docs-cn/dev/reference/sql/statements/show-character-set/']
---

# SHOW CHARACTER SET

`SHOW CHARACTER SET` 语句提供 TiDB 中可用字符集的静态列表。此列表不反映当前连接或用户的任何属性。

## 语法图

**ShowCharsetStmt:**

![ShowCharsetStmt](/media/sqlgram/ShowCharsetStmt.png)

**CharsetKw:**

![CharsetKw](/media/sqlgram/CharsetKw.png)

## 示例

{{< copyable "sql" >}}

```sql
SHOW CHARACTER SET;
```

```
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

`SHOW CHARACTER SET` 语句功能与 MySQL 完全兼容。注意，TiDB 中字符集的默认排序规则与 MySQL 有所不同，具体可以参考[与 MySQL 兼容性对比](/mysql-compatibility.md#默认设置)。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [SHOW COLLATION](/sql-statements/sql-statement-show-collation.md)
* [字符集和排序规则](/character-set-and-collation.md)
