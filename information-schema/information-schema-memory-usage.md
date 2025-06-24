---
title: MEMORY_USAGE
summary: 了解 `MEMORY_USAGE` information_schema 系统表。
---

# MEMORY_USAGE

`MEMORY_USAGE` 表描述了当前 TiDB 实例的内存使用情况。

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

`MEMORY_USAGE` 表中各列的描述如下：

* MEMORY_TOTAL：TiDB 可用的总内存，单位为字节。
* MEMORY_LIMIT：TiDB 的内存使用限制，单位为字节。该值与系统变量 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) 的值相同。
* MEMORY_CURRENT：TiDB 当前的内存使用量，单位为字节。
* MEMORY_MAX_USED：从 TiDB 启动到当前时间的最大内存使用量，单位为字节。
* CURRENT_OPS："shrinking" | null。"shrinking" 表示 TiDB 正在执行收缩内存使用的操作。
* SESSION_KILL_LAST：最后一次终止会话的时间戳。
* SESSION_KILL_TOTAL：从 TiDB 启动到当前时间，终止会话的总次数。
* GC_LAST：最后一次由内存使用触发 Golang GC 的时间戳。
* GC_TOTAL：从 TiDB 启动到当前时间，由内存使用触发 Golang GC 的总次数。
* DISK_USAGE：当前数据溢出操作的磁盘使用量，单位为字节。
* QUERY_FORCE_DISK：从 TiDB 启动到当前时间，数据溢出到磁盘的总次数。

## 另请参阅

<CustomContent platform="tidb">

- [TiDB 内存控制](/configure-memory-usage.md)
- [调优 TiKV 内存参数性能](/tune-tikv-memory-performance.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [TiDB 内存控制](https://docs.pingcap.com/tidb/stable/configure-memory-usage)
- [调优 TiKV 内存参数性能](https://docs.pingcap.com/tidb/stable/tune-tikv-memory-performance)

</CustomContent>
