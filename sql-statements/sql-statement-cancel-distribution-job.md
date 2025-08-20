---
title: CANCEL DISTRIBUTION JOB
summary: TiDB 数据库中 CANCEL DISTRIBUTION JOB 的使用情况。
---

# CANCEL DISTRIBUTION JOB <span class="version-mark">从 v9.0.0 开始引入</span>

`CANCEL DISTRIBUTION JOB` 语句用于取消 TiDB 中通过 [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md) 语句创建的 Region 调度任务。

## 语法图

```ebnf+diagram
CancelDistributionJobsStmt ::=
    'CANCEL' 'DISTRIBUTION' 'JOB' JobID
```

## 示例

下面示例取消 ID 为 1 的导入任务：

```sql
CANCEL DISTRIBUTION JOB 1;
```

输出结果如下：

```
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
* [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
