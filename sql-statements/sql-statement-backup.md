---
title: BACKUP
summary: TiDB 数据库中 BACKUP 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-backup/']
---

# BACKUP

> **警告：**
>
> `BACKUP` 语句目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

`BACKUP` 语句用于对 TiDB 集群执行分布式备份操作。

`BACKUP` 语句使用的引擎与 [BR](/br/backup-and-restore-overview.md) 相同，但备份过程是由 TiDB 本身驱动，而非单独的 BR 工具。BR 工具的优势和警告也适用于 `BACKUP` 语句。

执行 `BACKUP` 需要 `BACKUP_ADMIN` 或 `SUPER` 权限。此外，执行备份的 TiDB 节点和集群中的所有 TiKV 节点都必须有对目标存储的读或写权限。

`BACKUP` 语句开始执行后将会被阻塞，直到整个备份任务完成、失败或取消。因此，执行 `BACKUP` 时需要准备一个持久的连接。如需取消任务，可执行 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句。

一次只能执行一个 `BACKUP` 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 任务。如果 TiDB server 上已经在执行一个 `BACKUP` 或 `RESTORE` 语句，新的 `BACKUP` 将等待前面所有的任务完成后再执行。

## 语法图

```ebnf+diagram
BackupStmt ::=
    "BACKUP" BRIETables "TO" stringLit BackupOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

BackupOption ::=
    "CHECKSUM" '='? Boolean
|   "CHECKSUM_CONCURRENCY" '='? LengthNum
|   "COMPRESSION_LEVEL" '='? LengthNum
|   "COMPRESSION_TYPE" '='? stringLit
|   "CONCURRENCY" '='? LengthNum
|   "IGNORE_STATS" '='? Boolean
|   "LAST_BACKUP" '='? BackupTSO
|   "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean
|   "SNAPSHOT" '='? ( BackupTSO | LengthNum TimestampUnit "AGO" )

Boolean ::=
    NUM | "TRUE" | "FALSE"

BackupTSO ::=
    LengthNum | stringLit
```

## 示例

### 备份数据库

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 'local:///mnt/backup/2020/04/';
```

```sql
+------------------------------+-----------+-----------------+---------------------+---------------------+
| Destination                  | Size      | BackupTS        | Queue Time          | Execution Time      |
+------------------------------+-----------+-----------------+---------------------+---------------------+
| local:///mnt/backup/2020/04/ | 248665063 | 416099531454472 | 2020-04-12 23:09:48 | 2020-04-12 23:09:48 |
+------------------------------+-----------+-----------------+---------------------+---------------------+
1 row in set (58.453 sec)
```

上述示例中，`test` 数据库被备份到本地，数据以 SST 文件的形式存储在分布于所有 TiDB 和 TiKV 节点的 `/mnt/backup/2020/04/` 目录中。

输出结果的第一行描述如下：

| 列名 | 描述 |
| :-------- | :--------- |
| `Destination` | 目标存储的 URL |
| `Size` |  备份文件的总大小，单位为字节 |
| `BackupTS` | 创建备份时的快照 TSO（用于[增量备份](#增量备份)） |
| `Queue Time` | `BACKUP` 任务开始排队的时间戳（当前时区） |
| `Execution Time` | `BACKUP` 任务开始执行的时间戳（当前时区） |

### 备份表

{{< copyable "sql" >}}

```sql
BACKUP TABLE `test`.`sbtest01` TO 'local:///mnt/backup/sbtest01/';
```

{{< copyable "sql" >}}

```sql
BACKUP TABLE sbtest02, sbtest03, sbtest04 TO 'local:///mnt/backup/sbtest/';
```

### 备份集群

{{< copyable "sql" >}}

```sql
BACKUP DATABASE * TO 'local:///mnt/backup/full/';
```

注意，备份中不包含系统表（`mysql.*`、`INFORMATION_SCHEMA.*`、`PERFORMANCE_SCHEMA.*` 等）。

### 外部存储

BR 支持备份数据到 Amazon S3 或 Google Cloud Storage (GCS)：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

有关详细的 URL 语法，见[外部存储服务的 URI 格式](/external-storage-uri.md)。

当运行在云环境中时，不能分发凭证，可设置 `SEND_CREDENTIALS_TO_TIKV` 选项为 `FALSE`：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### 性能调优

如果你需要减少网络带宽占用，可以通过 `RATE_LIMIT` 来限制每个 TiKV 节点的平均上传速度。

在备份完成之前，`BACKUP` 默认将对集群上的数据执行校验和以验证数据正确性。对单张表做数据校验作业的并发度默认为 4，你可以通过 `CHECKSUM_CONCURRENCY` 参数调整该并发度。如果你确定数据无需进行校验，可以通过将 `CHECKSUM` 参数设置为 `FALSE` 来禁用该检查。 

要指定 BR 可以同时执行的备份表和索引的任务数量，可使用 `CONCURRENCY`。该参数控制 BR 的线程池大小，可以优化备份操作的性能和效率。根据备份类型不同，一个任务代表一个表范围或一个索引范围。如果有一个表带有一个索引，则会有两个任务来备份这个表。参数 `CONCURRENCY` 的默认值为 `4`，如果你要备份许多表或索引，需调大该参数的值。

统计信息默认不会备份，如果你确定需要备份统计信息，可以将 `IGNORE_STATS` 参数设置为 `FALSE`。

备份生成的 SST 文件默认使用 `zstd` 压缩算法。你可以根据需求， 通过 `COMPRESSION_TYPE` 参数指定压缩算法。可选的算法包括 `lz4`、`zstd`、`snappy`。你还可以通过 `COMPRESSION_LEVEL` 设置压缩级别，压缩级别数字越高，压缩比越高，但 CPU 消耗越大。

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### 快照

可以指定一个时间戳、TSO 或相对时间，来备份历史数据。

{{< copyable "sql" >}}

```sql
-- 相对时间
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist01'
    SNAPSHOT = 36 HOUR AGO;
-- 时间戳（当前时区）
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    SNAPSHOT = '2020-04-01 12:00:00';
-- TSO
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    SNAPSHOT = 415685305958400;
```

对于相对时间，支持以下时间单位：

* MICROSECOND（微秒）
* SECOND（秒）
* MINUTE（分钟）
* HOUR（小时）
* DAY（天）
* WEEK（周）

注意，相对时间的单位遵循 SQL 标准，永远使用单数。

### 增量备份

提供 `LAST_BACKUP` 选项，只备份从上一次备份到当前快照之间的增量数据。

{{< copyable "sql" >}}

```sql
-- 时间戳（当前时区）
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    LAST_BACKUP = '2020-04-01 12:00:00';

-- TSO
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    LAST_BACKUP = 415685305958400;
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [RESTORE](/sql-statements/sql-statement-restore.md)
* [SHOW BACKUPS](/sql-statements/sql-statement-show-backups.md)
