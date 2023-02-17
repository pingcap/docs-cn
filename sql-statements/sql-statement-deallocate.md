---
title: DEALLOCATE
summary: TiDB 数据库中 DEALLOCATE 的使用概况。
---

# DEALLOCATE

`DEALLOCATE` 语句用于为服务器端预处理语句提供 SQL 接口。

## 语法图

```ebnf+diagram
DeallocateStmt ::=
    DeallocateSym 'PREPARE' Identifier

DeallocateSym ::=
    'DEALLOCATE'
|   'DROP'

Identifier ::=
    identifier
|   UnReservedKeyword
|   NotKeywordToken
|   TiDBKeyword
```

## 示例

{{< copyable "sql" >}}

```sql
PREPARE mystmt FROM 'SELECT ? as num FROM DUAL';
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SET @number = 5;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
EXECUTE mystmt USING @number;
```

```
+------+
| num  |
+------+
| 5    |
+------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DEALLOCATE PREPARE mystmt;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

`DEALLOCATE` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [PREPARE](/sql-statements/sql-statement-prepare.md)
* [EXECUTE](/sql-statements/sql-statement-execute.md)
