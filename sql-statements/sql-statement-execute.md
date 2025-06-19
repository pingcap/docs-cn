---
title: EXECUTE | TiDB SQL 语句参考
summary: TiDB 数据库中 EXECUTE 的使用概述。
---

# EXECUTE

`EXECUTE` 语句为服务器端预处理语句提供 SQL 接口。

## 语法图

```ebnf+diagram
ExecuteStmt ::=
    'EXECUTE' Identifier ( 'USING' UserVariable ( ',' UserVariable )* )?
```

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

TiDB 中的 `EXECUTE` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [PREPARE](/sql-statements/sql-statement-prepare.md)
* [DEALLOCATE](/sql-statements/sql-statement-deallocate.md)
