---
title: TIDB_CHECK_CONSTRAINTS
summary: 了解 `TIDB_CHECK_CONSTRAINTS` INFORMATION_SCHEMA 表。
---

# TIDB\_CHECK\_CONSTRAINTS

`TIDB_CHECK_CONSTRAINTS` 表提供了表上 [`CHECK` 约束](/constraints.md#check)的信息。除了 [`CHECK_CONSTRAINTS`](/information-schema/information-schema-check-constraints.md) 中的列外，`TIDB_CHECK_CONSTRAINTS` 还提供了定义 `CHECK` 约束的表的名称和 ID。

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_CHECK_CONSTRAINTS;
```

输出如下：

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| CONSTRAINT_CATALOG | varchar(64) | NO   |      | NULL    |       |
| CONSTRAINT_SCHEMA  | varchar(64) | NO   |      | NULL    |       |
| CONSTRAINT_NAME    | varchar(64) | NO   |      | NULL    |       |
| CHECK_CLAUSE       | longtext    | NO   |      | NULL    |       |
| TABLE_NAME         | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID           | bigint(21)  | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

以下示例使用 `CREATE TABLE` 语句添加一个 `CHECK` 约束：

```sql
SET GLOBAL tidb_enable_check_constraint = ON;
CREATE TABLE test.t1 (id INT PRIMARY KEY, CHECK (id%2 = 0));
SELECT * FROM TIDB_CHECK_CONSTRAINTS\G
```

输出如下：

```sql
*************************** 1. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: test
   CONSTRAINT_NAME: t1_chk_1
      CHECK_CLAUSE: (`id` % 2 = 0)
        TABLE_NAME: t1
          TABLE_ID: 107
1 row in set (0.02 sec)
```

`TIDB_CHECK_CONSTRAINTS` 表中的字段说明如下：

* `CONSTRAINT_CATALOG`：约束的目录，始终为 `def`。
* `CONSTRAINT_SCHEMA`：约束的模式。
* `CONSTRAINT_NAME`：约束的名称。
* `CHECK_CLAUSE`：检查约束的子句。
* `TABLE_NAME`：约束所在表的名称。
* `TABLE_ID`：约束所在表的 ID。
