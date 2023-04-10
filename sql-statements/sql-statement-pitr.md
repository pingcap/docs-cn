---
title: TiDB 日志备份与 PITR 语句
summary: 介绍 TiDB 日志备份与 PITR 的 SQL 语句。
aliases: ['/zh/tidb/dev/br-log-statement/']
---

# TiDB 日志备份与 PITR

> **警告：**
>
> TiDB 日志备份与 PITR SQL 语句支持在 v7.1.0 是实验特性，其语法或者行为表现在 GA 前可能会发生变化。

本文介绍 TiDB 日志备份和 PITR (Point-in-time recovery) SQL 语句。

TiDB 日志备份与 PITR SQL 语句的大部分功能功能以及使用的参数的含义，和 BR 工具命令行基本是一致的，不同的是 SQL 语句备份恢复过程是由 TiDB 本身驱动，而非单独的 BR 工具。BR 工具的优势和警告也适用。如果你想了解如何进行日志备份与 PITR，可以参考以下教程：

- [ TiDB 日志备份与 PITR 命令行手册](/br/br-pitr-manual.md)
- [TiDB 日志备份与 PITR 使用指南](/br/br-pitr-guide.md)
- [TiDB 集群备份与恢复实践示例](/br/backup-and-restore-use-cases.md)
对于命令行已经存在功能，本文档重点是描述语法图和参数列表，对于 SQL 语句特有的功能会在本文档中做详细描述。

## 日志备份语句

执行日志备份语句需要 `BACKUP_ADMIN` 或 `SUPER` 权限。此外，执行备份的 TiDB 节点和集群中的所有 TiKV 节点都必须有对目标存储的读或写权限。

```sql
  BACKUP LOGS TO                  --start a log backup task
  SHOW BACKUP LOGS STATUS         --get status for the log backup task\
  PAUSE BACKUP LOGS               --pause a log backup task
  RESUME BACKUP LOGS              --resume a log backup task
  STOP BACKUP LOGS                --stop a log backup task
  SHOW BACKUP LOGS METADATA FROM  --get the metadata of log dir
  PURGE BACKUP JOBS FROM          --purge the log data until sometime
```

### 启动日志备份

等价于执行 `br log start` 命令，你可以在备份集群启动一个日志备份任务。该任务在 TiDB 集群持续地运行，及时地将 KV 变更日志保存到备份存储中。

#### 语法图

```ebnf+diagram
StreamStartStmt ::=
    "BACKUP" "LOGS" "TO" stringLit StreamStartOption*

StreamStartOption ::=
    "START_TS" '='? StartTSO

StartTSO ::=
    LengthNum | stringLit
```

#### 示例

{{< copyable "sql" >}}

```sql
BACKUP LOGS TO 'local:///mnt/backup/2020/07/26';
BACKUP LOGS TO 'local:///mnt/backup/2022/07/26' START_TS = '2022-07-26 21:20:00+0800';
```

### 查询日志备份任务

等价于执行 `br log status` 命令，查询日志备份任务状态。

#### 语法图

```ebnf+diagram
StreamStatusStmt ::=
    "SHOW" "BACKUP" "LOGS" "STATUS"
```

#### 示例

{{< copyable "sql" >}}

```sql
SHOW BACKUP LOGS STATUS;
```

### 暂停日志备份任务

等价于执行 `br log pause` 命令，暂停正在运行的日志备份任务。

#### 语法图

```ebnf+diagram
StreamPauseStmt ::=
    "PAUSE" "BACKUP" "LOGS" StreamPauseOption*
    
StreamPauseOption ::=
    "GC_TTL" '='? GCTTLTSO

GCTTLTSO ::=
    LengthNum | stringLit    
```

#### 示例

{{< copyable "sql" >}}

```sql
PAUSE BACKUP LOGS;
PAUSE BACKUP LOGS GC_TTL = '2022-08-26 21:20:00+0800';
```

### 恢复日志备份任务

等价于执行 `br log resume` 命令，恢复被暂停的日志备份任务。

#### 语法图

```ebnf+diagram
StreamResumeStmt ::=
    "Resume" "BACKUP" "LOGS" 
```

#### 示例

{{< copyable "sql" >}}

```sql
RESUME BACKUP LOGS;
```

### 停止日志备份任务

等价于执行 `br log stop` 命令，停止日志备份任务。

#### 语法图

```ebnf+diagram
StreamStopStmt ::=
    "Stop" "BACKUP" "LOGS" 
```

#### 示例

{{< copyable "sql" >}}

```sql
STOP BACKUP LOGS;
```

### 查看备份数据元信息

等价于执行 `br log metadata` 命令，查看备份存储中保存的日志备份的元信息，例如最早和最近的可恢复时间点。

#### 语法图

```ebnf+diagram
StreamMetaDataStmt ::=
    "SHOW" "BACKUP" "LOGS" "METADATA" "FROM" stringLit 
```

#### 示例

{{< copyable "sql" >}}

```sql
SHOW BACKUP LOGS METADATA FROM 's3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"';
```

### 清理日志备份数据

等价于执行 `br log truncate` 命令，从备份存储中删除过期或不再需要的备份日志数据。

#### 语法图

```ebnf+diagram
StreamMetaPurgeStmt ::=
    "PURGE" "BACKUP" "LOGS" "METADATA" "FROM" stringLit StreamPurgeOption*
    
StreamPurgeOption ::=
    "UNTIL_TS" '='? UNTILTSO

UNTILTSO ::=
    LengthNum | stringLit    
```

#### 示例

{{< copyable "sql" >}}

```sql
PURGE BACKUP LOGS METADATA FROM 's3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"';
PURGE BACKUP LOGS METADATA FROM 's3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"' UNTIL_TS = '2022-08-26 21:20:00+0800' ;
```

## 恢复到指定时间点 PITR

执行 PITR 语句需要 `RESTORE_ADMIN` 或 `SUPER` 权限。此外，执行恢复的 TiDB 节点和集群中的所有 TiKV 节点都必须有对目标存储的读或写权限。

```sql
  RESTORE POINT FROM              --restore cluster to a point
```

### 恢复到指定时间点

等价于执行 `br restore point` 命令，在新集群上进行 PITR，或者只恢复日志备份数据。

#### 语法图

```ebnf+diagram
StreamRestorePITStmt ::=
    "RESTORE" "POINT" "FROM" stringLit StreamRestorePITOption*

StreamRestorePITOption ::=
    "START_TS" '='? StartTSO
|   "FULL_BACKUP_STORAGE" '='? stringLit
|   "START_TS" '='? StartTSO
|   "STORED_TS" '='? StoredTSO

StartTSO ::=
    LengthNum | stringLit
    
StoredTSO ::=
    LengthNum | stringLit    
```

#### 示例

{{< copyable "sql" >}}

```sql
RESTORE POINT FROM 's3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"' FULL_BACKUP_STORAGE = 's3://backup-101/snapshot-202205120000?access-key=${access-key}&secret-access-key=${secret-access-key}"';

```
> **注意：**
>
> - 不支持重复恢复某段时间区间的日志，如多次重复恢复 `[t1=10, t2=20)` 区间的日志数据，可能会造成恢复后的数据不正确。
> - 多次恢复不同时间区间的日志时，需保证恢复日志的连续性。如先后恢复 `[t1, t2)`、`[t2, t3)` 和 `[t3, t4)` 三个区间的日志可以保证正确性，而在恢复 `[t1, t2)` 后跳过 `[t2, t3)` 直接恢复 `[t3, t4)` 的区间可能导致恢复之后的数据不正确。


## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [SHOW BACKUPS](/sql-statements/sql-statement-show-backups.md)
* [SHOW RESTORES](/sql-statements/sql-statement-show-backups.md)
* [RESTORE](/sql-statements/sql-statement-restore.md)
* [BR_JOB_ADMIN](/sql-statements/sql-statement-br-job-admin.md)
* [SHOW_BACKUP_META](/sql-statements/show-backp-meta.md)