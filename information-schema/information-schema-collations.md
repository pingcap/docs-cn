---
title: COLLATIONS
summary: 了解 information_schema 表 `COLLATIONS`。
---

# COLLATIONS

`COLLATIONS` 表提供了 `CHARACTER_SETS` 表中字符集对应的排序规则列表。目前 TiDB 包含该表仅为兼容 MySQL。

```sql
USE information_schema;
DESC collations;
```

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | YES  |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | YES  |      | NULL    |       |
| ID                 | bigint      | YES  |      | NULL    |       |
| IS_DEFAULT         | varchar(3)  | YES  |      | NULL    |       |
| IS_COMPILED        | varchar(3)  | YES  |      | NULL    |       |
| SORTLEN            | bigint      | YES  |      | NULL    |       |
| PAD_ATTRIBUTE      | varchar(9)  | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
7 rows in set (0.001 sec)
```

```sql
SELECT * FROM collations WHERE character_set_name='utf8mb4';
```

```sql
+--------------------+--------------------+------+------------+-------------+---------+---------------+
| COLLATION_NAME     | CHARACTER_SET_NAME | ID   | IS_DEFAULT | IS_COMPILED | SORTLEN | PAD_ATTRIBUTE |
+--------------------+--------------------+------+------------+-------------+---------+---------------+
| utf8mb4_0900_ai_ci | utf8mb4            |  255 |            | Yes         |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4            |  309 |            | Yes         |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4            |   46 | Yes        | Yes         |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4            |   45 |            | Yes         |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4            |  224 |            | Yes         |       8 | PAD SPACE     |
+--------------------+--------------------+------+------------+-------------+---------+---------------+
5 rows in set (0.001 sec)
```

`COLLATIONS` 表中列的含义如下：

* `COLLATION_NAME`：排序规则名称。
* `CHARACTER_SET_NAME`：排序规则所属的字符集名称。
* `ID`：排序规则的 ID。
* `IS_DEFAULT`：该排序规则是否是所属字符集的默认排序规则。
* `IS_COMPILED`：字符集是否编译到服务器中。
* `SORTLEN`：排序规则在对字符进行排序时，所分配内存的最小长度。
* `PAD_ATTRIBUTE`：在比较字符串时是否忽略末尾空格。`PAD SPACE` 表示忽略末尾空格（例如 `'abc'` 等于 `'abc '`），而 `NO PAD` 表示末尾空格会影响比较结果（例如 `'abc'` 不等于 `'abc '`）。

## 另请参阅

- [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
- [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)
- [`INFORMATION_SCHEMA.CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)
- [`INFORMATION_SCHEMA.COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md)