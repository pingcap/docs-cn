---
title: SHOW CHARACTER SET | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW CHARACTER SET 的使用概述。
---

# SHOW CHARACTER SET

此语句提供 TiDB 中可用字符集的静态列表。输出不反映当前连接或用户的任何属性。

## 语法图

```ebnf+diagram
ShowCharsetStmt ::=
    "SHOW" ( ("CHARACTER" | "CHAR") "SET" | "CHARSET" ) ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
SHOW CHARACTER SET;
```

```
+---------+-------------------------------------+-------------------+--------+
| Charset | Description                         | Default collation | Maxlen |
+---------+-------------------------------------+-------------------+--------+
| ascii   | US ASCII                            | ascii_bin         |      1 |
| binary  | binary                              | binary            |      1 |
| gbk     | Chinese Internal Code Specification | gbk_chinese_ci    |      2 |
| latin1  | Latin1                              | latin1_bin        |      1 |
| utf8    | UTF-8 Unicode                       | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode                       | utf8mb4_bin       |      4 |
+---------+-------------------------------------+-------------------+--------+
6 rows in set (0.00 sec)
```

```sql
SHOW CHARACTER SET LIKE 'utf8%';
```

```
+---------+---------------+-------------------+--------+
| Charset | Description   | Default collation | Maxlen |
+---------+---------------+-------------------+--------+
| utf8    | UTF-8 Unicode | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode | utf8mb4_bin       |      4 |
+---------+---------------+-------------------+--------+
2 rows in set (0.00 sec)
```

```sql
SHOW CHARACTER SET WHERE Description='UTF-8 Unicode';
```

```
+---------+---------------+-------------------+--------+
| Charset | Description   | Default collation | Maxlen |
+---------+---------------+-------------------+--------+
| utf8    | UTF-8 Unicode | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode | utf8mb4_bin       |      4 |
+---------+---------------+-------------------+--------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中 `SHOW CHARACTER SET` 语句的用法与 MySQL 完全兼容。但是，TiDB 中的字符集可能与 MySQL 相比具有不同的默认排序规则。详情请参考[与 MySQL 的兼容性](/mysql-compatibility.md)。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [SHOW COLLATION](/sql-statements/sql-statement-show-collation.md)
* [字符集和排序规则](/character-set-and-collation.md)
