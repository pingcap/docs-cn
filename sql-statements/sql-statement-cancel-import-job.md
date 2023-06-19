---
title: CANCEL IMPORT
summary: TiDB 数据库中 CANCEL IMPORT 的使用概况。
---

# CANCEL IMPORT

`CANCEL IMPORT` 语句用于取消 TiDB 中创建的数据导入任务。

## 所需权限

只有导入任务的创建者或拥有 `SUPER` 权限的用户才能够取消任务。

## 语法图

```ebnf+diagram
CancelImportJobsStmt ::=
    'CANCEL' 'IMPORT' 'JOB' JobID
```

## 示例

下面示例取消 ID 为 1 的导入任务：

```sql
CANCEL IMPORT JOB 1;
```

输出结果如下：

```
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)
* [`SHOW IMPORT JOB`](/sql-statements/sql-statement-show-import-job.md)
