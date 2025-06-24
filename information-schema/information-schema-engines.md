---
title: ENGINES
summary: 了解 `ENGINES` information_schema 表。
---

# ENGINES

`ENGINES` 表提供了存储引擎的相关信息。为了保持兼容性，TiDB 将始终将 InnoDB 描述为唯一支持的引擎。此外，`ENGINES` 表中的其他列值也都是固定值。

```sql
USE information_schema;
DESC engines;
```

```sql
+--------------+-------------+------+------+---------+-------+
| Field        | Type        | Null | Key  | Default | Extra |
+--------------+-------------+------+------+---------+-------+
| ENGINE       | varchar(64) | YES  |      | NULL    |       |
| SUPPORT      | varchar(8)  | YES  |      | NULL    |       |
| COMMENT      | varchar(80) | YES  |      | NULL    |       |
| TRANSACTIONS | varchar(3)  | YES  |      | NULL    |       |
| XA           | varchar(3)  | YES  |      | NULL    |       |
| SAVEPOINTS   | varchar(3)  | YES  |      | NULL    |       |
+--------------+-------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

```sql
SELECT * FROM engines;
```

```
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| ENGINE | SUPPORT | COMMENT                                                    | TRANSACTIONS | XA   | SAVEPOINTS |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| InnoDB | DEFAULT | Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
1 row in set (0.01 sec)
```

`ENGINES` 表中各列的描述如下：

* `ENGINES`：存储引擎的名称。
* `SUPPORT`：服务器对该存储引擎的支持级别。在 TiDB 中，该值始终为 `DEFAULT`。
* `COMMENT`：关于该存储引擎的简短说明。
* `TRANSACTIONS`：该存储引擎是否支持事务。
* `XA`：该存储引擎是否支持 XA 事务。
* `SAVEPOINTS`：该存储引擎是否支持 `savepoints`。

## 另请参阅

- [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md)
