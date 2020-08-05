---
title: CHARACTER_SETS
summary: 了解 information_schema 表 `CHARACTER_SETS`。
---

# CHARACTER_SETS

`CHARACTER_SETS` 表提供[字符集](/character-set-and-collation.md)相关的信息。TiDB 目前仅支持部分字符集。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC character_sets;
```

```sql
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

{{< copyable "sql" >}}

```sql
SELECT * FROM `character_sets`;
```

```sql
+--------------------+----------------------+---------------+--------+
| CHARACTER_SET_NAME | DEFAULT_COLLATE_NAME | DESCRIPTION   | MAXLEN |
+--------------------+----------------------+---------------+--------+
| utf8               | utf8_bin             | UTF-8 Unicode |      3 |
| utf8mb4            | utf8mb4_bin          | UTF-8 Unicode |      4 |
| ascii              | ascii_bin            | US ASCII      |      1 |
| latin1             | latin1_bin           | Latin1        |      1 |
| binary             | binary               | binary        |      1 |
+--------------------+----------------------+---------------+--------+
5 rows in set (0.00 sec)
```

`CHARACTER_SETS` 表中列的含义如下：

* `CHARACTER_SET_NAME`：字符集名称
* `DEFAULT_COLLATE_NAME`：字符集的默认排序规则名称
* `DESCRIPTION`：字符集的描述信息
* `MAXLEN`：该字符集存储一个字符所需要的最大字节数
