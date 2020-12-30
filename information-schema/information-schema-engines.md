---
title: ENGINES
summary: 了解 information_schema 表 `ENGINES`。
aliases: ['/docs-cn/dev/information-schema/information-schema-engines/']
---

# ENGINES

`ENGINES` 表提供了关于存储引擎的信息。从和 MySQL 兼容性上考虑，TiDB 会一直将 InnoDB 描述为唯一支持的引擎。此外，`ENGINES` 表中其它列值也都是定值。

{{< copyable "sql" >}}

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

{{< copyable "sql" >}}

```sql
SELECT * FROM engines;
```

```sql
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| ENGINE | SUPPORT | COMMENT                                                    | TRANSACTIONS | XA   | SAVEPOINTS |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| InnoDB | DEFAULT | Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
1 row in set (0.01 sec)
```

`ENGINES` 表中列的含义如下：

* `ENGINE`：存储引擎的名称。
* `SUPPORT`：服务器对存储引擎的支持级别，在 TiDB 中此值一直是 `DEFAULT`。
* `COMMENT`：存储引擎的简要描述。
* `TRANSACTIONS`：存储引擎是否支持事务。
* `XA`：存储引擎是否支持 XA 事务。
* `SAVEPOINTS`：存储引擎是否支持 `savepoints`。
