---
title: CHARACTER_SETS
summary: 了解 `CHARACTER_SETS` INFORMATION_SCHEMA 表。
---

# CHARACTER_SETS

`CHARACTER_SETS` 表提供了关于[字符集](/character-set-and-collation.md)的信息。目前，TiDB 仅支持部分字符集。

```sql
USE INFORMATION_SCHEMA;
DESC CHARACTER_SETS;
```

输出结果如下：

```
+----------------------+-------------+------+------+---------+-------+
| Field                | Type        | Null | Key  | Default | Extra |
+----------------------+-------------+------+------+---------+-------+
| CHARACTER_SET_NAME   | varchar(32) | YES  |      | NULL    |       |
| DEFAULT_COLLATE_NAME | varchar(32) | YES  |      | NULL    |       |
| DESCRIPTION          | varchar(60) | YES  |      | NULL    |       |
| MAXLEN               | bigint(3)   | YES  |      | NULL    |       |
+----------------------+-------------+------+------+---------+-------+
4 rows in set (0.00 sec)
```

查看 `CHARACTER_SETS` 表：

```sql
SELECT * FROM `CHARACTER_SETS`;
```

输出结果如下：

```sql
+--------------------+----------------------+-------------------------------------+--------+
| CHARACTER_SET_NAME | DEFAULT_COLLATE_NAME | DESCRIPTION                         | MAXLEN |
+--------------------+----------------------+-------------------------------------+--------+
| ascii              | ascii_bin            | US ASCII                            |      1 |
| binary             | binary               | binary                              |      1 |
| gbk                | gbk_chinese_ci       | Chinese Internal Code Specification |      2 |
| latin1             | latin1_bin           | Latin1                              |      1 |
| utf8               | utf8_bin             | UTF-8 Unicode                       |      3 |
| utf8mb4            | utf8mb4_bin          | UTF-8 Unicode                       |      4 |
+--------------------+----------------------+-------------------------------------+--------+
6 rows in set (0.00 sec)
```

`CHARACTER_SETS` 表中各列的描述如下：

* `CHARACTER_SET_NAME`：字符集的名称。
* `DEFAULT_COLLATE_NAME`：字符集的默认排序规则名称。
* `DESCRIPTION`：字符集的描述。
* `MAXLEN`：在此字符集中存储一个字符所需的最大长度。

## 另请参阅

- [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
- [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)
- [`INFORMATION_SCHEMA.COLLATIONS`](/information-schema/information-schema-collations.md)
- [`INFORMATION_SCHEMA.COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md)
