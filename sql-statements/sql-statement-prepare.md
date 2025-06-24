---
title: PREPARE | TiDB SQL 语句参考
summary: TiDB 数据库中 PREPARE 的使用概览。
---

# PREPARE

`PREPARE` 语句为服务器端预处理语句提供了 SQL 接口。

## 语法图

```ebnf+diagram
PreparedStmt ::=
    'PREPARE' Identifier 'FROM' PrepareSQL

PrepareSQL ::=
    stringLit
|   UserVariable
```

> **注意：**
>
> 对于每个 `PREPARE` 语句，占位符的最大数量是 65535。

要限制当前 TiDB 实例中 `PREPARE` 语句的数量，你可以使用 [`max_prepared_stmt_count`](/system-variables.md#max_prepared_stmt_count) 系统变量。

## 示例

```sql
mysql> PREPARE mystmt FROM 'SELECT ? as num FROM DUAL';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @number = 5;
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE mystmt USING @number;
+------+
| num  |
+------+
| 5    |
+------+
1 row in set (0.00 sec)

mysql> DEALLOCATE PREPARE mystmt;
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `PREPARE` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [EXECUTE](/sql-statements/sql-statement-execute.md)
* [DEALLOCATE](/sql-statements/sql-statement-deallocate.md)
