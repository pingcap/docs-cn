---
title: SHOW DISTRIBUTION JOBS
summary: 介绍 TiDB 数据库中 SHOW DISTRIBUTION JOBS 的使用概况。
---

# SHOW DISTRIBUTION JOBS

<span class="version-mark">从 v9.0.0 开始引入</span>

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
+--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
| Job_ID | Database | Table | Partition_List | Engine | Rule           | Status    | Create_Time         | Start_Time          | Finish_Time         |
+--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
|    100 | test     | t1    | NULL           | tikv   | leader-scatter | finished  | 2025-04-24 16:09:55 | 2025-04-24 16:09:55 | 2025-04-24 17:09:59 |
|    101 | test     | t2    | NULL           | tikv   | learner-scatter| cancelled | 2025-05-08 15:33:29 | 2025-05-08 15:33:29 | 2025-05-08 15:33:37 |
|    102 | test     | t5    | p1,p2          | tikv   | peer-scatter   | cancelled | 2025-05-21 15:32:44 | 2025-05-21 15:32:47 | 2025-05-21 15:32:47 |
+--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
- [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
- [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)