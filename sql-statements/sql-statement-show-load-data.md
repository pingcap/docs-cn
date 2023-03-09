---
title: SHOW LOAD DATA
summary: TiDB 数据库中 SHOW LOAD DATA 的使用概况。
---

# SHOW LOAD DATA

`SHOW LOAD DATA` 语句用于显示系统中创建的 LOAD DATA JOB

## 语法图

```ebnf+diagram
ShowLoadDataJobsStmt ::=
    'SHOW' 'LAOD' 'DATA' 'JOBS'

ShowLoadDataJobStmt ::=
    'SHOW' 'LAOD' 'DATA' 'JOB' JobID
```

## 示例

{{< copyable "sql" >}}

```sql
SHOW LOAD DATA JOBS;
```

```

```

{{< copyable "sql" >}}

```sql
SHOW LOAD DATA JOB 1;
```

```

```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [LOAD DATA](/sql-statements/sql-statement-load-data.md)
* [OPERATE LOAD DATA JOB](/sql-statements/sql-statement-operate-load-data-job.md)
