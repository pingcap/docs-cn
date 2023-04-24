---
title: CANCEL LOAD DATA 和 DROP LOAD DATA
summary: TiDB 数据库中 CANCEL LOAD DATA 和 DROP LOAD DATA 的使用概况。
---

# CANCEL LOAD DATA 和 DROP LOAD DATA

`CANCEL LOAD DATA` 语句用于取消系统中创建的 LOAD DATA 任务。

`DROP LOAD DATA` 语句用于删除系统中创建的 LOAD DATA 任务。

## 语法图

```ebnf+diagram
CancelLoadDataJobsStmt ::=
    'CANCEL' 'LAOD' 'DATA' 'JOB' JobID

DropLoadDataJobsStmt ::=
    'DROP' 'LAOD' 'DATA' 'JOB' JobID
```

## 示例

```sql
CANCEL LOAD DATA JOB 1;
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
DROP LOAD DATA JOB 1;
```

```
Query OK, 1 row affected (0.01 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [LOAD DATA](/sql-statements/sql-statement-load-data.md)
* [SHOW LOAD DATA](/sql-statements/sql-statement-show-load-data.md)
