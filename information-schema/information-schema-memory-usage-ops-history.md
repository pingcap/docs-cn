---
title: MEMORY_USAGE_OPS_HISTORY
summary: Learn the `MEMORY_USAGE_OPS_HISTORY` information_schema system table.
---

# MEMORY_USAGE_OPS_HISTORY

The `MEMORY_USAGE_OPS_HISTORY` table describes the history of memory-related operations and the execution basis of the current TiDB instance.

```sql
USE information_schema;
DESC memory_usage_ops_history;
```

```sql
+----------------+---------------------+------+------+---------+-------+
| Field          | Type                | Null | Key  | Default | Extra |
+----------------+---------------------+------+------+---------+-------+
| TIME           | datetime            | NO   |      | NULL    |       |
| OPS            | varchar(20)         | NO   |      | NULL    |       |
| MEMORY_LIMIT   | bigint(21)          | NO   |      | NULL    |       |
| MEMORY_CURRENT | bigint(21)          | NO   |      | NULL    |       |
| PROCESSID      | bigint(21) unsigned | YES  |      | NULL    |       |
| MEM            | bigint(21) unsigned | YES  |      | NULL    |       |
| DISK           | bigint(21) unsigned | YES  |      | NULL    |       |
| CLIENT         | varchar(64)         | YES  |      | NULL    |       |
| DB             | varchar(64)         | YES  |      | NULL    |       |
| USER           | varchar(16)         | YES  |      | NULL    |       |
| SQL_DIGEST     | varchar(64)         | YES  |      | NULL    |       |
| SQL_TEXT       | varchar(256)        | YES  |      | NULL    |       |
+----------------+---------------------+------+------+---------+-------+
12 rows in set (0.000 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.memory_usage_ops_history;
```

```sql
+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
| TIME                | OPS         | MEMORY_LIMIT | MEMORY_CURRENT | PROCESSID           | MEM        | DISK | CLIENT          | DB   | USER | SQL_DIGEST                                                       | SQL_TEXT                                                             |
+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
| 2022-10-17 22:46:25 | SessionKill |  10737418240 |    10880237568 | 6718275530455515543 | 7905028235 |    0 | 127.0.0.1:34394 | test | root | 146b3d812852663a20635fbcf02be01688f52c8d433dafec0d496a14f0b59df6 | desc analyze select * from t t1 join t t2 on t1.a=t2.a order by t1.a |
+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
2 rows in set (0.002 sec)
```

The columns in the `MEMORY_USAGE_OPS_HISTORY` table are described as follows:

* `TIME`: The timestamp when the session is terminated.
* `OPS`: "SessionKill"
* `MEMORY_LIMIT`: The memory usage limit of TiDB at the time of termination, in bytes. Its value is the same as that of the system variable `tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640).
* `MEMORY_CURRENT`: The current memory usage of TiDB, in bytes.
* `PROCESSID`: The connection ID of the terminated session.
* `MEM`: The memory usage of the terminated session, in bytes.
* `DISK`: The disk usage of the terminated session, in bytes.
* `CLIENT`: The client connection address of the terminated session.
* `DB`: The name of the database connected to the terminated session.
* `USER`: The user name of the terminated session.
* `SQL_DIGEST`: The digest of the SQL statement being executed in the terminated session.
* `SQL_TEXT`: The SQL statement being executed in the terminated session.
