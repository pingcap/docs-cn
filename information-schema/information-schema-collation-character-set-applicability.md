---
title: COLLATION_CHARACTER_SET_APPLICABILITY
summary: 了解 INFORMATION_SCHEMA 表 `COLLATION_CHARACTER_SET_APPLICABILITY`。
---

# COLLATION_CHARACTER_SET_APPLICABILITY

`COLLATION_CHARACTER_SET_APPLICABILITY` 表将排序规则映射至适用的字符集名称。和 `COLLATIONS` 表一样，包含此表只是为了兼容 MySQL。

```sql
USE INFORMATION_SCHEMA;
DESC COLLATION_CHARACTER_SET_APPLICABILITY;
```

输出结果如下：

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | NO   |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | NO   |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

查看 `COLLATION_CHARACTER_SET_APPLICABILITY` 表中 `utf8mb4` 字符集的排序规则映射：

```sql
SELECT * FROM COLLATION_CHARACTER_SET_APPLICABILITY WHERE character_set_name='utf8mb4';
```

输出结果如下：

```sql
+--------------------+--------------------+
| COLLATION_NAME     | CHARACTER_SET_NAME |
+--------------------+--------------------+
| utf8mb4_bin        | utf8mb4            |
| utf8mb4_general_ci | utf8mb4            |
| utf8mb4_unicode_ci | utf8mb4            |
+--------------------+--------------------+
3 rows in set (0.00 sec)
```

`COLLATION_CHARACTER_SET_APPLICABILITY` 表中列的含义如下：

* `COLLATION_NAME`：排序规则名称
* `CHARACTER_SET_NAME`：排序规则所属的字符集名称

## 另请参阅

- [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
- [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)
- [`INFORMATION_SCHEMA.CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)
- [`INFORMATION_SCHEMA.COLLATIONS`](/information-schema/information-schema-collations.md)