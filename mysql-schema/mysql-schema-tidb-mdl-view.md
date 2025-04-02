---
title: mysql.tidb_mdl_view
summary: 了解 `mysql` 库中的 `tidb_mdl_view` 表。
---

该表提供了有关[元数据锁](/metadata-lock.md)视图的详细信息，这些视图用于监控和管理系统中的元数据锁信息。

```sql
DESC mysql.tidb_mdl_view;
```

输出如下：

```
+-------------+-----------------+------+------+---------+-------+
| Field       | Type            | Null | Key  | Default | Extra |
+-------------+-----------------+------+------+---------+-------+
| job_id      | bigint          | NO   | PRI  | NULL    |       |
| db_name     | longtext        | YES  |      | NULL    |       |
| table_name  | longtext        | YES  |      | NULL    |       |
| query       | longtext        | YES  |      | NULL    |       |
| session_id  | bigint unsigned | YES  |      | NULL    |       |
| start_time  | timestamp(6)    | YES  |      | NULL    |       |
| SQL_DIGESTS | varchar(5)      | YES  |      | NULL    |       |
+-------------+-----------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

## 字段

* `job_id`：作业的标识符。
* `db_name`：数据库名称。
* `table_name`：表名称。
* `query`：查询语句。
* `session_id`：会话的标识符。
* `start_time`：开始时间。此列在早期版本中称为 `TxnStart`。
* `SQL_DIGESTS`：SQL 语句的摘要。
