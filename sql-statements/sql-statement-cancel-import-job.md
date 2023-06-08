---
title: CANCEL IMPORT
summary: TiDB 数据库中 CANCEL IMPORT 的使用概况。
---

# CANCEL IMPORT

`CANCEL IMPORT` 语句用于取消系统中创建的 IMPORT 任务。

## 所需权限

用户需要是该 job 的创建者或有 `SUPER` 权限，才能够 CANCEL 该 job。

## 语法图

```ebnf+diagram
CancelImportJobsStmt ::=
    'CANCEL' 'IMPORT' 'JOB' JobID
```

## 示例

```sql
CANCEL IMPORT JOB 1;
```

```
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [IMPORT INTO](/sql-statements/sql-statement-import-into.md)
* [SHOW IMPORT JOB](/sql-statements/sql-statement-show-import-job.md)
