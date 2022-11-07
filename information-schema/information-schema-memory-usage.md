---
title: MEMORY_USAGE
summary: Learn the `MEMORY_USAGE` information_schema system table.
---

# MEMORY_USAGE

The `MEMORY_USAGE` table describes the current memory usage of the current TiDB instance.

```sql
USE information_schema;
DESC memory_usage;
```

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| MEMORY_TOTAL       | bigint(21)  | NO   |      | NULL    |       |
| MEMORY_LIMIT       | bigint(21)  | NO   |      | NULL    |       |
| MEMORY_CURRENT     | bigint(21)  | NO   |      | NULL    |       |
| MEMORY_MAX_USED    | bigint(21)  | NO   |      | NULL    |       |
| CURRENT_OPS        | varchar(50) | YES  |      | NULL    |       |
| SESSION_KILL_LAST  | datetime    | YES  |      | NULL    |       |
| SESSION_KILL_TOTAL | bigint(21)  | NO   |      | NULL    |       |
| GC_LAST            | datetime    | YES  |      | NULL    |       |
| GC_TOTAL           | bigint(21)  | NO   |      | NULL    |       |
| DISK_USAGE         | bigint(21)  | NO   |      | NULL    |       |
| QUERY_FORCE_DISK   | bigint(21)  | NO   |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
11 rows in set (0.000 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.memory_usage;
```

```sql
+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
| MEMORY_TOTAL | MEMORY_LIMIT | MEMORY_CURRENT | MEMORY_MAX_USED | CURRENT_OPS | SESSION_KILL_LAST   | SESSION_KILL_TOTAL | GC_LAST             | GC_TOTAL | DISK_USAGE | QUERY_FORCE_DISK |
+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
|  33674170368 |  10737418240 |     5097644032 |     10826604544 | NULL        | 2022-10-17 22:47:47 |                  1 | 2022-10-17 22:47:47 |       20 |          0 |                0 |
+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
2 rows in set (0.002 sec)
```

The columns in the `MEMORY_USAGE` table are described as follows:

* MEMORY_TOTAL: The total available memory of TiDB, in bytes.
* MEMORY_LIMIT: The memory usage limit of TiDB, in bytes. The value is the same as that of the system variable [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640).
* MEMORY_CURRENT: The current memory usage of TiDB, in bytes.
* MEMORY_MAX_USED: The maximum memory usage of TiDB from the time it is started to the current time, in bytes.
* CURRENT_OPS: "shrinking" | null. "shrinking" means that TiDB is performing operations that shrink memory usage.
* SESSION_KILL_LAST: The timestamp of the last time a session is terminated.
* SESSION_KILL_TOTAL: The number of times sessions are terminated, from the time TiDB is started to the current time.
* GC_LAST: The timestamp of the last time Golang GC is triggered by memory usage.
* GC_TOTAL: The number of times Golang GC is triggered by memory usage, from the time TiDB is started to the current time.
* DISK_USAGE: The disk usage for the current data spill operation, in bytes.
* QUERY_FORCE_DISK: The number of times data is spilled to disk, from the time TiDB is started to the current time.
