---
title: SHOW COLLATION
summary: TiDB 数据库中 SHOW COLLATION 的使用概况。
---

# SHOW COLLATION

`SHOW COLLATION` 语句用于提供一个静态的排序规则列表，确保与 MySQL 客户端库的兼容性。

> **注意：**
>
> `SHOW COLLATION` 所展示的排序规则列表与 TiDB 集群是否开启[新排序规则框架](/character-set-and-collation.md#新框架下的排序规则支持)有关，详情请见 [TiDB 字符集和排序规则](/character-set-and-collation.md)。

## 语法图

```ebnf+diagram
ShowCollationStmt ::=
    "SHOW" "COLLATION" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

如果启用了[新排序规则框架](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)（默认启用），输出如下：

```sql
SHOW COLLATION;
```

```
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 | PAD SPACE     |
| binary             | binary  |  63 | Yes     | Yes      |       1 | NO PAD        |
| gbk_bin            | gbk     |  87 |         | Yes      |       1 | PAD SPACE     |
| gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 | PAD SPACE     |
| latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_general_ci    | utf8    |  33 |         | Yes      |       1 | PAD SPACE     |
| utf8_unicode_ci    | utf8    | 192 |         | Yes      |       8 | PAD SPACE     |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
13 rows in set (0.00 sec)
```

若未开启新排序规则框架，仅展示二进制排序规则：

```sql
SHOW COLLATION;
```

```sql
+-------------+---------+----+---------+----------+---------+---------------+
| Collation   | Charset | Id | Default | Compiled | Sortlen | Pad_attribute |
+-------------+---------+----+---------+----------+---------+---------------+
| utf8mb4_bin | utf8mb4 | 46 | Yes     | Yes      |       1 | PAD SPACE     |
| latin1_bin  | latin1  | 47 | Yes     | Yes      |       1 | PAD SPACE     |
| binary      | binary  | 63 | Yes     | Yes      |       1 | NO PAD        |
| ascii_bin   | ascii   | 65 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_bin    | utf8    | 83 | Yes     | Yes      |       1 | PAD SPACE     |
| gbk_bin     | gbk     | 87 | Yes     | Yes      |       1 | PAD SPACE     |
+-------------+---------+----+---------+----------+---------+---------------+
6 rows in set (0.00 sec)
```

要过滤字符集，可以添加 `WHERE` 子句。

```sql
SHOW COLLATION WHERE Charset="utf8mb4";
```

```
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

`SHOW COLLATION` 语句功能与 MySQL 完全兼容。注意，TiDB 中字符集的默认排序规则与 MySQL 有所不同，具体可参考[与 MySQL 兼容性对比](/mysql-compatibility.md#默认设置)。如发现任何其他兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
* [字符集和排序规则](/character-set-and-collation.md)
