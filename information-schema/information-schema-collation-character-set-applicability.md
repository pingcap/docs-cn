---
title: COLLATION_CHARACTER_SET_APPLICABILITY
summary: 了解 information_schema 表 `COLLATION_CHARACTER_SET_APPLICABILITY`。
---

# COLLATION_CHARACTER_SET_APPLICABILITY

`COLLATION_CHARACTER_SET_APPLICABILITY` 表将排序规则映射至适用的字符集名称。和 `COLLATIONS` 表一样，包含此表只是为了兼容 MySQL。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC collation_character_set_applicability;
```

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | NO   |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | NO   |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM collation_character_set_applicability WHERE character_set_name='utf8mb4';
```

```sql
+----------------+--------------------+
| COLLATION_NAME | CHARACTER_SET_NAME |
+----------------+--------------------+
| utf8mb4_bin    | utf8mb4            |
+----------------+--------------------+
1 row in set (0.00 sec)
```

`COLLATION_CHARACTER_SET_APPLICABILITY` 表中列的含义如下：

* `COLLATION_NAME`：排序规则名称
* `CHARACTER_SET_NAME`：排序规则所属的字符集名称
