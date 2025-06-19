---
title: SHOW ENGINES | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW ENGINES 的使用概述。
---

# SHOW ENGINES

此语句用于列出所有支持的存储引擎。包含此语法仅是为了与 MySQL 保持兼容。

## 语法

```ebnf+diagram
ShowEnginesStmt ::=
    "SHOW" "ENGINES" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
mysql> SHOW ENGINES;
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| Engine | Support | Comment                                                    | Transactions | XA   | Savepoints |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| InnoDB | DEFAULT | Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

* 此语句将始终只返回 InnoDB 作为支持的引擎。在内部，TiDB 通常使用 [TiKV](/tikv-overview.md) 作为存储引擎。
