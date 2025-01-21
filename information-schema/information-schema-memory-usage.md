---
title: MEMORY_USAGE
summary: 了解 information_schema 表 `MEMORY_USAGE`。
---

# MEMORY_USAGE

`MEMORY_USAGE` 表描述了 TiDB 实例当前的内存使用情况。

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

`MEMORY_USAGE` 表中列的含义如下：

* MEMORY_TOTAL：TiDB 的可用内存总量，单位为 byte。
* MEMORY_LIMIT：TiDB 的内存使用限制，单位为 byte。其值与系统变量 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 的值相同。
* MEMORY_CURRENT：TiDB 当前的内存使用量，单位为 byte。
* MEMORY_MAX_USED：从 TiDB 启动到当前的最大内存使用量，单位为 byte。
* CURRENT_OPS："shrinking" | null。"shrinking" 表示 TiDB 正在执行收缩内存用量的操作。
* SESSION_KILL_LAST：上一次终止会话的时间戳。
* SESSION_KILL_TOTAL：从 TiDB 启动到当前累计终止会话的次数。
* GC_LAST：上一次由内存使用触发 Golang GC 的时间戳。
* GC_TOTAL：从 TiDB 启动到当前累计由内存使用触发 Golang GC 的次数。
* DISK_USAGE：当前数据落盘的硬盘使用量，单位为 byte。
* QUERY_FORCE_DISK：从 TiDB 启动到当前累计的落盘次数。

## 另请参阅

- [TiDB 内存控制](/configure-memory-usage.md)
- [TiKV 内存参数性能调优](/tune-tikv-memory-performance.md)