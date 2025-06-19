---
title: SHOW COLLATION | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW COLLATION 的使用概述。
---

# SHOW COLLATION

此语句提供排序规则的静态列表，包含它是为了与 MySQL 客户端库保持兼容。

> **注意：**
>
> 当启用["新的排序规则框架"](/character-set-and-collation.md#new-framework-for-collations)时，`SHOW COLLATION` 的结果会有所不同。有关新排序规则框架的详细信息，请参阅[字符集和排序规则](/character-set-and-collation.md)。

## 语法

```ebnf+diagram
ShowCollationStmt ::=
    "SHOW" "COLLATION" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

当禁用新的排序规则框架时，只显示二进制排序规则。

```sql
SHOW COLLATION;
```

```
+-------------+---------+------+---------+----------+---------+
| Collation   | Charset | Id   | Default | Compiled | Sortlen |
+-------------+---------+------+---------+----------+---------+
| utf8mb4_bin | utf8mb4 |   46 | Yes     | Yes      |       1 |
| latin1_bin  | latin1  |   47 | Yes     | Yes      |       1 |
| binary      | binary  |   63 | Yes     | Yes      |       1 |
| ascii_bin   | ascii   |   65 | Yes     | Yes      |       1 |
| utf8_bin    | utf8    |   83 | Yes     | Yes      |       1 |
+-------------+---------+------+---------+----------+---------+
5 rows in set (0.02 sec)
```

当启用新的排序规则框架时，还额外支持 `utf8_general_ci` 和 `utf8mb4_general_ci`。

```sql
SHOW COLLATION;
```

```
+--------------------+---------+------+---------+----------+---------+
| Collation          | Charset | Id   | Default | Compiled | Sortlen |
+--------------------+---------+------+---------+----------+---------+
| ascii_bin          | ascii   |   65 | Yes     | Yes      |       1 |
| binary             | binary  |   63 | Yes     | Yes      |       1 |
| gbk_bin            | gbk     |   87 |         | Yes      |       1 |
| gbk_chinese_ci     | gbk     |   28 | Yes     | Yes      |       1 |
| latin1_bin         | latin1  |   47 | Yes     | Yes      |       1 |
| utf8_bin           | utf8    |   83 | Yes     | Yes      |       1 |
| utf8_general_ci    | utf8    |   33 |         | Yes      |       1 |
| utf8_unicode_ci    | utf8    |  192 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 |  224 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
11 rows in set (0.001 sec)
```

要筛选字符集，你可以添加 `WHERE` 子句。

```sql
SHOW COLLATION WHERE Charset="utf8mb4";
```

```sql
+--------------------+---------+-----+---------+----------+---------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen |
+--------------------+---------+-----+---------+----------+---------+
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       1 |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       1 |
+--------------------+---------+-----+---------+----------+---------+
5 rows in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中 `SHOW COLLATION` 语句的用法与 MySQL 完全兼容。但是，TiDB 中的字符集可能与 MySQL 相比有不同的默认排序规则。详情请参阅[与 MySQL 的兼容性](/mysql-compatibility.md)。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [SHOW CHARACTER SET](/sql-statements/sql-statement-show-character-set.md)
* [字符集和排序规则](/character-set-and-collation.md)
