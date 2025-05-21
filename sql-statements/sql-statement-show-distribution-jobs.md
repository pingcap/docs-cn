---
title: SHOW DISTRIBUTION JOBS
summary: 介绍 TiDB 数据库中 SHOW DISTRIBUTION JOBS 的使用概况。
---

# SHOW DISTRIBUTION JOBS

`SHOW DISTRIBUTION JOBS` 语句用于显示当前所有的 Region 调度任务。

## 语法图

```ebnf+diagram
ShowDistributionJobsStmt ::=
    "SHOW" "DISTRIBUTION" "JOBS"
```

## 示例

显示当前所有的 Region 调度任务：

```sql
SHOW DISTRIBUTION JOBS;
```

```
+---------+------------+------------+-----------------+------------+-----------+----------+-------------+---------------+
| JOB_ID  |  DB_NAME   | TABLE_NAME | PARTITION_NAMES | ENGINE_TYPE | ROLE_TYPE | STATUS  | CREATE_USER | CREATE_TIME   |
+---------+------------+------------+-----------------+------------+-----------+--------+---------------+---------------+
|    1    |   db_1     |    t1      |                 | TIKV       | LEADER    | RUNNING  | ADMIN       | 20240712      |
|    2    |   db_1     |    t2      |                 | TIFLASH    | LEARNER   | FINISHED | ADMIN       | 20240715      |
|    3    |   db_1     |    t3      |                 | TiKV       | VOTER     | STOPPED  | ADMIN       | 20240713      |
|    4    |   db_1     |    t4      |                 | TIFLASH    | LEARNER   | FINISHED | ADMIN       | 20240713      |
+---------+------------+------------+-----------------+------------+-----------+----------+-------------+---------------+
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
- [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)