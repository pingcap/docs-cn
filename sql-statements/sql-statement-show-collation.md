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

**ShowCollationStmt:**

![ShowCollationStmt](/media/sqlgram/ShowCollationStmt.png)

## 示例

若未开启新排序规则框架，仅展示二进制排序规则：

{{< copyable "sql" >}}

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

若开启了新排序规则框架，则在二进制排序规则之外，额外支持 `utf8_general_ci` 和 `utf8mb4_general_ci` 两种大小写和口音不敏感的排序规则：

{{< copyable "sql" >}}

```sql

SHOW COLLATION;
```

```
+--------------------+---------+------+---------+----------+---------+
| Collation          | Charset | Id   | Default | Compiled | Sortlen |
+--------------------+---------+------+---------+----------+---------+
| ascii_bin          | ascii   |   65 | Yes     | Yes      |       1 |
| binary             | binary  |   63 | Yes     | Yes      |       1 |
| latin1_bin         | latin1  |   47 | Yes     | Yes      |       1 |
| utf8_bin           | utf8    |   83 | Yes     | Yes      |       1 |
| utf8_general_ci    | utf8    |   33 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
7 rows in set (0.00 sec)
```

## MySQL 兼容性

`SHOW COLLATION` 语句功能与 MySQL 完全兼容。注意，TiDB 中字符集的默认排序规则与 MySQL 有所不同，具体可参考[与 MySQL 兼容性对比](/mysql-compatibility.md#默认设置)。如发现任何其他兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [SHOW CHARACTER SET](/sql-statements/sql-statement-show-character-set.md)
* [字符集和排序规则](/character-set-and-collation.md)
