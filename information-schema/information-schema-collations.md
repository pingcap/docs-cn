---
title: COLLATIONS
summary: 了解 information_schema 表 `COLLATIONS`。
---

# COLLATIONS

`COLLATIONS` 表提供了 `CHARACTER_SETS` 表中字符集对应的排序规则列表。目前 TiDB 包含该表仅为兼容 MySQL。

{{< copyable "sql" >}}

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
| ID                 | bigint(11)  | YES  |      | NULL    |       |
| IS_DEFAULT         | varchar(3)  | YES  |      | NULL    |       |
| IS_COMPILED        | varchar(3)  | YES  |      | NULL    |       |
| SORTLEN            | bigint(3)   | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM collations WHERE character_set_name='utf8mb4';
```

```sql
+----------------+--------------------+------+------------+-------------+---------+
| COLLATION_NAME | CHARACTER_SET_NAME | ID   | IS_DEFAULT | IS_COMPILED | SORTLEN |
+----------------+--------------------+------+------------+-------------+---------+
| utf8mb4_bin    | utf8mb4            |   46 | Yes        | Yes         |       1 |
+----------------+--------------------+------+------------+-------------+---------+
1 row in set (0.00 sec)
```

`COLLATION` 表中列的含义如下：

* `COLLATION_NAME`：排序规则名称
* `CHARACTER_SET_NAME`：排序规则所属的字符集名称
* `ID`：排序规则的 ID
* `IS_DEFAULT`：该排序规则是否是所属字符集的默认排序规则
* `IS_COMPILED`：字符集是否编译到服务器中
* `SORTLEN`：排序规则在对字符进行排序时，所分配内存的最小长度
