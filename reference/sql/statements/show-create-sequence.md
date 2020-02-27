---
title: SHOW CREATE SEQUENCE
summary: TiDB 数据库中 SHOW CREATE SEQUENCE 的使用概况。
category: reference
---

# SHOW CREATE SEQUENCE

`SHOW CREATE SEQUENCE` 语句用于查看一个 SEQUENCE 的详细信息，类似于 `SHOW CREATE TABLE` 语句。

## 语法图

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE seq;
```

```
Query OK, 0 rows affected (0.03 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE SEQUENCE seq;
```

```
+-------+----------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                               |
+-------+----------------------------------------------------------------------------------------------------------------------------+
| seq   | CREATE SEQUENCE `seq` start with 1 minvalue 1 maxvalue 9223372036854775806 increment by 1 cache 1000 nocycle ENGINE=InnoDB |
+-------+----------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

* MySQL 暂无 SEQUENCE 选项。TiDB Sequence 借鉴自 MariaDB，但是 setval 会保持原有的步调。

## 另请参阅

* [CREATE SEQUENCE](/reference/sql/statements/create-sequence.md)
* [DROP SEQUENCE](/reference/sql/statements/drop-sequence.md)
