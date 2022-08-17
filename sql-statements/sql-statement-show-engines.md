---
title: SHOW ENGINES
summary: TiDB 数据库中 SHOW ENGINES 的使用概况。
---

# SHOW ENGINES

`SHOW ENGINES` 语句用于列出所有支持的存储引擎，该语法仅提供 MySQL 兼容性。

## 语法图

**ShowEnginesStmt:**

![ShowEnginesStmt](/media/sqlgram/ShowEnginesStmt.png)

```sql
SHOW ENGINES;
```

## 示例

{{< copyable "sql" >}}

```sql
SHOW ENGINES;
```

```
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| Engine | Support | Comment                                                    | Transactions | XA   | Savepoints |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| InnoDB | DEFAULT | Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

* `SHOW ENGINES` 语句始终只返回 InnoDB 作为其支持的引擎。但 TiDB 内部通常使用 TiKV 作为存储引擎。
