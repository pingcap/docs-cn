---
title: SHOW TRAFFIC JOBS
summary: TiDB 数据库中 SHOW TRAFFIC JOBS 的使用概况。
---

# SHOW TRAFFIC JOBS

TiDB v9.0.0 引入了 `SHOW TRAFFIC JOBS` 语法，用于查看集群中所有 [TiProxy](/tiproxy/tiproxy-overview.md) 的流量捕获或回放任务。输出结果中，每行代表一台 TiProxy 实例的一个任务。每台 TiProxy 实例最多保存最近的 10 个任务。

执行该语句的结果取决于当前用户的权限：

- 具有 [`TRAFFIC_CAPTURE_ADMIN`](/privilege-management.md#动态权限) 权限的用户可查看流量捕获任务。
- 具有 [`TRAFFIC_REPLAY_ADMIN`](/privilege-management.md#动态权限) 权限的用户可查看流量回放任务。
- 具有 `SUPER` 权限或同时拥有上述两种权限的用户可同时查看流量捕获和流量回放任务。

`SHOW TRAFFIC JOBS` 返回以下列：

| 列名 | 说明   |
| :-------- | :------------- |
| `START_TIME` | 该任务的开始时间 |
| `END_TIME` | 如果该任务已结束，该列为结束时间，否则为空 |
| `INSTANCE` | TiProxy 的实例地址 |
| `TYPE` | 表示任务类型，`capture` 代表流量捕获任务，`replay` 代表流量回放任务 |
| `PROGRESS` | 该任务的完成百分比 |
| `STATUS` | 该任务当前的状态，`running` 表示正在运行，`done` 表示正常完成，`canceled` 表示任务失败 |
| `FAIL_REASON` | 如果该任务失败，该列为失败的原因，否则为空。例如 `manually stopped` 表示用户执行 `CANCEL TRAFFIC JOBS` 手动取消任务 |
| `PARAMS` | 该任务的参数 |

## 语法图

```ebnf+diagram
TrafficStmt ::=
    "SHOW" "TRAFFIC" "JOBS"
```

## 示例

查看流量捕获或回放任务：

```sql
SHOW TRAFFIC JOBS;
```

下面输出示例表示有 2 台 TiProxy 正在捕获流量，进度都为 45%：

```
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
| START_TIME                 | END_TIME | INSTANCE       | TYPE    | PROGRESS | STATUS  | FAIL_REASON | PARAMS                                                                     |
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
| 2024-12-17 10:54:41.000000 |          | 10.1.0.10:3080 | capture | 45%      | running |             | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
| 2024-12-17 10:54:41.000000 |          | 10.1.0.11:3080 | capture | 45%      | running |             | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
2 rows in set (0.01 sec)
```

下面输出示例表示 2 台 TiProxy 的流量回放任务被手动取消：

```
+----------------------------+----------------------------+----------------+--------+----------+----------+------------------+--------------------------------------------------------------------+
| START_TIME                 | END_TIME                   | INSTANCE       | TYPE   | PROGRESS | STATUS   | FAIL_REASON      | PARAMS                                                             |
+----------------------------+----------------------------+----------------+--------+----------+----------+------------------+--------------------------------------------------------------------+
| 2024-12-17 10:54:41.000000 | 2024-12-17 11:34:42.000000 | 10.1.0.10:3080 | replay | 70%      | canceled | manually stopped | INPUT="/tmp/traffic", USER="root", SPEED=0.000000, READ_ONLY=false |
| 2024-12-17 10:54:41.000000 | 2024-12-17 11:34:43.000000 | 10.1.0.11:3080 | replay | 69%      | canceled | manually stopped | INPUT="/tmp/traffic", USER="root", SPEED=0.000000, READ_ONLY=false |
+----------------------------+----------------------------+----------------+--------+----------+----------+------------------+--------------------------------------------------------------------+
2 rows in set (0.01 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [TiProxy 流量回放](/tiproxy/tiproxy-traffic-replay.md)
* [`TRAFFIC CAPTURE`](/sql-statements/sql-statement-traffic-capture.md)
* [`TRAFFIC REPLAY`](/sql-statements/sql-statement-traffic-replay.md)
* [`CANCEL TRAFFIC JOBS`](/sql-statements/sql-statement-cancel-traffic-jobs.md)
