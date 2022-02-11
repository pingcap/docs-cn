---
title: RESTORE
summary: TiDB 数据库中 RESTORE 的使用概况。
---

# RESTORE

`RESTORE` 语句用于执行分布式恢复，把 [`BACKUP` 语句](/sql-statements/sql-statement-backup.md)生成的备份文件恢复到 TiDB 集群中。

`RESTORE` 语句使用的引擎与 [BR](/br/backup-and-restore-use-cases.md) 相同，但恢复过程是由 TiDB 本身驱动，而非单独的 BR 工具。BR 工具的优势和警告也适用于 `RESTORE` 语句。需要注意的是，**`RESTORE` 语句目前不遵循 ACID 原则**。

执行 `RESTORE` 语句前，确保集群已满足以下要求：

* 集群处于“下线”状态，当前的 TiDB 会话是唯一在访问待恢复表的活跃 SQL 连接。
* 执行全量恢复时，确保即将恢复的表不存在于集群中，因为现有的数据可能被覆盖，从而导致数据与索引不一致。
* 执行增量恢复时，表的状态应该与创建备份时 `LAST_BACKUP` 时间戳的状态完全一致。

执行 `RESTORE` 需要 `RESTORE_ADMIN` 或 `SUPER` 权限。此外，执行恢复操作的 TiDB 节点和集群中的所有 TiKV 节点都必须有对目标存储的读权限。

`RESTORE` 语句开始执行后将会被阻塞，直到整个恢复任务完成、失败或取消。因此，执行 `RESTORE` 时需要准备一个持久的连接。如需取消任务，可执行 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句。

一次只能执行一个 `BACKUP` 和 `RESTORE` 任务。如果 TiDB server 上已经在执行一个 `BACKUP` 或 `RESTORE` 语句，新的 `RESTORE` 将等待前面所有的任务完成后再执行。

`RESTORE` 只能在 "tikv" 存储引擎上使用，如果使用 "unistore" 存储引擎，`RESTORE` 操作会失败。

## 语法图

```ebnf+diagram
RestoreStmt ::=
    "RESTORE" BRIETables "FROM" stringLit RestoreOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

RestoreOption ::=
    "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "CONCURRENCY" '='? LengthNum
|   "CHECKSUM" '='? Boolean
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean

Boolean ::=
    NUM | "TRUE" | "FALSE"
```

## 示例

### 从备份文件恢复

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 'local:///mnt/backup/2020/04/';
```

```sql
+------------------------------+-----------+----------+---------------------+---------------------+
| Destination                  | Size      | BackupTS | Queue Time          | Execution Time      |
+------------------------------+-----------+----------+---------------------+---------------------+
| local:///mnt/backup/2020/04/ | 248665063 | 0        | 2020-04-21 17:16:55 | 2020-04-21 17:16:55 |
+------------------------------+-----------+----------+---------------------+---------------------+
1 row in set (28.961 sec)
```

上述示例中，所有数据均从本地的备份文件中恢复到集群中。`RESTORE` 从 SST 文件里读取数据，SST 文件存储在所有 TiDB 和 TiKV 节点的 `/mnt/backup/2020/04/` 目录下。

输出结果的第一行描述如下：

| 列名 | 描述 |
| :-------- | :--------- |
| `Destination` | 读取的目标存储 URL |
| `Size` |  备份文件的总大小，单位为字节 |
| `BackupTS` | 不适用 |
| `Queue Time` | `RESTORE` 任务开始排队的时间戳（当前时区） |
| `Execution Time` | `RESTORE` 任务开始执行的时间戳（当前时区） |

### 部分恢复

你可以指定恢复部分数据库或部分表数据。如果备份文件中缺失了某些数据库或表，缺失的部分将被忽略。此时，`RESTORE` 语句不进行任何操作即完成执行。

{{< copyable "sql" >}}

```sql
RESTORE DATABASE `test` FROM 'local:///mnt/backup/2020/04/';
```

{{< copyable "sql" >}}

```sql
RESTORE TABLE `test`.`sbtest01`, `test`.`sbtest02` FROM 'local:///mnt/backup/2020/04/';
```

### 外部存储

BR 支持从 Amazon S3 或 Google Cloud Storage (GCS) 恢复数据：

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/?region=us-west-2';
```

有关详细的 URL 语法，见[外部存储](/br/backup-and-restore-storages.md)。

当运行在云环境中时，不能分发凭证，可设置 `SEND_CREDENTIALS_TO_TIKV` 选项为 `FALSE`：

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/?region=us-west-2'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### 性能调优

如果你需要减少网络带宽占用，可以通过 `RATE_LIMIT` 来限制每个 TiKV 节点的平均下载速度。

默认情况下，每个 TiKV 节点上运行 128 个恢复线程。可以通过 `CONCURRENCY` 选项来调整这个值。

在恢复完成之前，`RESTORE` 将对备份文件中的数据进行校验，以验证数据的正确性。如果你确信无需进行校验，可以通过 `CHECKSUM` 选项禁用这一步骤。

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### 增量恢复

增量恢复没有特殊的语法。TiDB 将识别备份文件属于全量备份或增量备份，然后执行对应的恢复操作，用户只需按照正确顺序进行增量恢复。

假设按照如下方式创建一个备份任务：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/full-backup'  SNAPSHOT = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-1' SNAPSHOT = 414971854848000 LAST_BACKUP = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-2' SNAPSHOT = 416353458585600 LAST_BACKUP = 414971854848000;
```

在恢复备份时，需要采取同样的顺序：

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket/full-backup';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-1';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-2';
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [SHOW RESTORES](/sql-statements/sql-statement-show-backups.md)
