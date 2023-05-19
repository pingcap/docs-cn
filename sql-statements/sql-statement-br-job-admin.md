---
title: BR JOB ADMIN
summary: TiDB 数据库中 BR 作业管理语句的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-br-job-admin']
---

本文介绍 TiDB BR (BACKUP & RESTORE) 作业管理语句，包括下面几种语句：
```sql
  SHOW BR JOB                     --show information of a br task
  SHOW BR JOB QUERY               --show the query statement of a br task
  CANCEL BR JOB                   --cancel a br task
```
> **警告：**
>
> TiDB BR 作业管理语句在 v7.1.0 是实验特性，其语法或者行为表现在 GA 前可能会发生变化。
> 
### 显示 br 作业信息

按照 task id 展示一个 br 作业的信息

#### 语法图

```ebnf+diagram
StreamShowJobStmt ::=
    "SHOW" "BR" "JOB" Int64Num
```

#### 示例

{{< copyable "sql" >}}

```sql
SHOW BR JOB 13456;
```

### 显示 br 作业运行的 SQL 语句

按照 task id 展示一个 br 作业运行的 SQL 语句

#### 语法图

```ebnf+diagram
StreamShowQueryStmt ::=
    "SHOW" "BR" "JOB" "QUERY" Int64Num
```

#### 示例

{{< copyable "sql" >}}

```sql
SHOW BR JOB QUERY 13456;
```

### 取消一个 br 作业

按照 task id 取消一个 br 作业的运行

#### 语法图

```ebnf+diagram
StreamCancelJobStmt ::=
    "CANCEL" "BR" "JOB" Int64Num
```

#### 示例

{{< copyable "sql" >}}

```sql
CANCEL BR JOB 13456;
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [SHOW BACKUPS](/sql-statements/sql-statement-show-backups.md)
* [SHOW RESTORES](/sql-statements/sql-statement-show-backups.md)
* [RESTORE](/sql-statements/sql-statement-restore.md)
* [PITR](/sql-statements/sql-statement-pitr.md)
* [SHOW_BACKUP_META](/sql-statements/show-backp-meta.md)
