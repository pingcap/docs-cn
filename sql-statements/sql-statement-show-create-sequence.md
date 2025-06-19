---
title: SHOW CREATE SEQUENCE
summary: TiDB 数据库中 SHOW CREATE SEQUENCE 的使用概述。
---

# SHOW CREATE SEQUENCE

`SHOW CREATE SEQUENCE` 显示序列的详细信息，类似于 `SHOW CREATE TABLE`。

## 语法

```ebnf+diagram
ShowCreateSequenceStmt ::=
    "SHOW" "CREATE" "SEQUENCE" ( SchemaName "." )? TableName
```

## 示例

```sql
CREATE SEQUENCE seq;
```

```
Query OK, 0 rows affected (0.03 sec)
```

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

此语句是 TiDB 扩展语法。其实现参考了 MariaDB 中可用的序列功能。

## 另请参阅

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [ALTER SEQUENCE](/sql-statements/sql-statement-alter-sequence.md)
* [DROP SEQUENCE](/sql-statements/sql-statement-drop-sequence.md)
