---
title: CANCEL TRAFFIC JOBS
summary: TiDB 数据库中 CANCEL TRAFFIC JOBS 的使用概况。
---

# CANCEL TRAFFIC JOBS

TiDB v9.0.0 引入了 `CANCEL TRAFFIC JOBS` 语法，用于取消集群中所有 [TiProxy](/tiproxy/tiproxy-overview.md) 正在执行的流量捕获或回放任务。该操作需要如下权限：

- 取消流量捕获任务，需要有 `SUPER` 或 [`TRAFFIC_CAPTURE_ADMIN`](/privilege-management.md#动态权限) 权限。
- 取消流量回放任务，需要有 `SUPER` 或 [`TRAFFIC_REPLAY_ADMIN`](/privilege-management.md#动态权限) 权限。

## 语法图

```ebnf+diagram
TrafficStmt ::=
    "CANCEL" "TRAFFIC" "JOBS"
```

## 示例

假设当前有 2 台 TiProxy 正在进行流量捕获：

```sql
SHOW TRAFFIC JOBS;
```

```
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
| START_TIME                 | END_TIME | INSTANCE       | TYPE    | PROGRESS | STATUS  | FAIL_REASON | PARAMS                                                                     |
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
| 2024-12-17 10:54:41.000000 |          | 10.1.0.10:3080 | capture | 45%      | running |             | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
| 2024-12-17 10:54:41.000000 |          | 10.1.0.11:3080 | capture | 45%      | running |             | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
2 rows in set (0.01 sec)
```

取消当前的任务：

```sql
CANCEL TRAFFIC JOBS;
```

```
Query OK, 0 rows affected (0.13 sec)
```

再次查看任务，显示任务已被取消：

```sql
SHOW TRAFFIC JOBS;
```

```
+----------------------------+----------------------------+----------------+---------+----------+----------+------------------+----------------------------------------------------------------------------+
| START_TIME                 | END_TIME                   | INSTANCE       | TYPE    | PROGRESS | STATUS   | FAIL_REASON      | PARAMS                                                                     |
+----------------------------+----------------------------+----------------+---------+----------+----------+------------------+----------------------------------------------------------------------------+
| 2024-12-17 10:54:41.000000 | 2024-12-17 11:34:42.000000 | 10.1.0.10:3080 | capture | 45%      | canceled | manually stopped | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
| 2024-12-17 10:54:41.000000 | 2024-12-17 11:34:42.000000 | 10.1.0.11:3080 | capture | 45%      | canceled | manually stopped | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
+----------------------------+----------------------------+----------------+---------+----------+----------+------------------+----------------------------------------------------------------------------+
2 rows in set (0.01 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [TiProxy 流量回放](/tiproxy/tiproxy-traffic-replay.md)
* [`TRAFFIC CAPTURE`](/sql-statements/sql-statement-traffic-capture.md)
* [`TRAFFIC REPLAY`](/sql-statements/sql-statement-traffic-replay.md)
* [`SHOW TRAFFIC JOBS`](/sql-statements/sql-statement-show-traffic-jobs.md)
