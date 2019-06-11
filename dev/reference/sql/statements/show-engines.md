---
title: SHOW ENGINES
summary: TiDB 数据库中 SHOW ENGINES 的使用概况。
category: reference
---

# SHOW ENGINES

`SHOW ENGINES` 语句仅提供 MySQL 兼容性。

## 总览

```sql
SHOW ENGINES
```

## 实例

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

* `SHOW ENGINES` 语句始终只返回 InnoDB 作为其支持的引擎。但 TiDB 内部通常使用 TiKV 作为存储引擎。