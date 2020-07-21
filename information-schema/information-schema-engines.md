---
title: ENGINES
summary: Learn the `ENGINES` information_schema table.
---

# ENGINES

The `ENGINES` table provides information about storage engines. For compatibility, TiDB will always describe InnoDB as the only supported engine. In addition, other column values in the `ENGINES` table are also fixed values.

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

```
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| ENGINE | SUPPORT | COMMENT                                                    | TRANSACTIONS | XA   | SAVEPOINTS |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| InnoDB | DEFAULT | Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
1 row in set (0.01 sec)
```

The description of columns in the `ENGINES` table is as follows:

* `ENGINES`: The name of the storage engine.
* `SUPPORT`: The level of support that the server has on the storage engine. In TiDB, the value is always `DEFAULT`.
* `COMMENT`: The brief comment on the storage engine.
* `TRANSACTIONS`: Whether the storage engine supports transactions.
* `XA`: Whether the storage engine supports XA transactions.
* `SAVEPOINTS`: Whether the storage engine supports `savepoints`.