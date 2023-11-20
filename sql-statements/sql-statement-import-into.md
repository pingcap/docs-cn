---
title: IMPORT INTO
summary: TiDB 数据库中 IMPORT INTO 的使用概况。
---

# IMPORT INTO

`IMPORT INTO` 语句使用 TiDB Lightning 的[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)，用于将 `CSV`、`SQL`、`PARQUET` 等格式的数据导入到 TiDB 的一张空表中。

`IMPORT INTO` 支持导入存储在 Amazon S3、GCS、Azure Blob Storage 和 TiDB 本地的数据文件。

- 对于存储在 S3、GCS 或 Azure Blob Storage 的数据文件，`IMPORT INTO` 支持通过[后端任务分布式框架](/tidb-distributed-execution-framework.md)运行。

    - 当此框架功能开启时（即 [tidb_enable_dist_task](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入) 为 `ON`），`IMPORT INTO` 会将一个数据导入任务拆分成多个子任务并分配到各个 TiDB 节点上运行，以提高导入效率。
    - 当此框架功能关闭时，`IMPORT INTO` 仅支持在当前用户连接的 TiDB 节点上运行。

- 对于存储在 TiDB 本地的数据文件，`IMPORT INTO` 仅支持在当前用户连接的 TiDB 节点上运行，因此数据文件需要存放在当前用户连接的 TiDB 节点上。如果是通过 PROXY 或者 Load Balancer 访问 TiDB，则无法导入存储在 TiDB 本地的数据文件。

## 使用限制

- 目前该语句支持导入 10 TiB 以内的数据。
- 只支持导入数据到数据库中已有的空表。
- 不支持事务，也无法回滚。在显式事务 (`BEGIN`/`END`) 中执行会报错。
- 在导入完成前会阻塞当前连接，如果需要异步执行，可以添加 `DETACHED` 选项。
- 不支持和 [Backup & Restore](/br/backup-and-restore-overview.md)、[`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)、[创建索引加速](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)、TiDB Lightning 导入、TiCDC 数据同步、[Point-in-time recovery (PITR)](/br/br-log-architecture.md) 等功能同时工作。
- 每个集群上同时只能有一个 `IMPORT INTO` 任务在运行。`IMPORT INTO` 会 precheck 是否存在运行中的任务，但并非硬限制，如果多个客户端同时执行 `IMPORT INTO` 仍有可能启动多个任务，请避免该情况，否则可能导致数据不一致或者任务失败的问题。
- 导入数据的过程中，请勿在目标表上执行 DDL 和 DML 操作，也不要在目标数据库上执行 [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)，否则会导致导入失败或数据不一致。导入期间也不建议进行读操作，因为读取的数据可能不一致。请在导入完成后再进行读写操作。
- 导入期间会占用大量系统资源，建议 TiDB 节点使用 32 核以上的 CPU 和 64 GiB 以上内存以获得更好的性能。导入期间会将排序好的数据写入到 TiDB [临时目录](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入)下，建议优先考虑配置闪存等高性能存储介质。详情请参考[物理导入使用限制](/tidb-lightning/tidb-lightning-physical-import-mode.md#必要条件及限制)。
- TiDB [临时目录](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入)至少需要有 90 GiB 的可用空间。建议预留大于等于所需导入数据的存储空间，以保证最佳导入性能。
- 一个导入任务只支持导入数据到一张目标表中。如需导入数据到多张目标表，需要在一张目标表导入完成后，再新建一个任务导入下一张目标表。
- TiDB 集群升级期间不支持使用该语句。
- 当使用[全局排序](/tidb-global-sort.md)导入数据时，单行数据的总长度不能超过 32 MiB。
- 当使用全局排序导入数据时，如果 TiDB 集群在导入任务尚未完成时被删除了，Amazon S3 上可能会残留用于全局排序的临时数据。该场景需要手动删除这些数据，以免增加 S3 存储成本。
- 所需导入的数据不能存在主键或非空唯一索引冲突的记录，否则会导致任务失败。

## 导入前准备

在使用 `IMPORT INTO` 开始导入数据前，请确保：

- 要导入的目标表在 TiDB 中已经创建，并且是空表。
- 当前集群有足够的剩余空间能容纳要导入的数据。
- 当前连接的 TiDB 节点的[临时目录](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入)至少有 90 GiB 的磁盘空间。如果开启了 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入)，需要确保集群中所有 TiDB 节点的临时目录都有足够的磁盘空间。

## 需要的权限

执行 `IMPORT INTO` 的用户需要有目标表的 `SELECT`、`UPDATE`、`INSERT`、`DELETE` 和 `ALTER` 权限。如果是导入存储在 TiDB 本地的文件，还需要有 `FILE` 权限。

## 语法图

```ebnf+diagram
ImportIntoStmt ::=
    'IMPORT' 'INTO' TableName ColumnNameOrUserVarList? SetClause? FROM fileLocation Format? WithOptions?

ColumnNameOrUserVarList ::=
    '(' ColumnNameOrUserVar (',' ColumnNameOrUserVar)* ')'

SetClause ::=
    'SET' SetItem (',' SetItem)*

SetItem ::=
    ColumnName '=' Expr

Format ::=
    'CSV' | 'SQL' | 'PARQUET'

WithOptions ::=
    'WITH' OptionItem (',' OptionItem)*

OptionItem ::=
    optionName '=' optionVal | optionName
```

## 参数说明

### ColumnNameOrUserVarList

用于指定数据文件中每行的各个字段如何对应到目标表列，也可以将字段对应到某个变量，用来跳过导入某些字段或者在 `SetClause` 中使用。

- 当不指定该参数时，数据文件中每行的字段数需要和目标表的列数一致，且各个字段会按顺序导入到对应的列。
- 当指定该参数时，指定的列或变量个数需要和数据文件中每行的字段数一致。

### SetClause

用于指定目标列值的计算方式。在 SET 表达式的右侧，可以引用在 `ColumnNameOrUserVarList` 中指定的变量。

SET 表达式左侧只能引用 `ColumnNameOrUserVarList` 中没有的列名。如果目标列名已经在 `ColumnNameOrUserVarList` 中，则该 SET 表达式无效。

### fileLocation

用于指定数据文件的存储位置，该位置可以是 S3、GCS 或 Azure Blob Storage URI 路径，也可以是 TiDB 本地文件路径。

- S3、GCS 或 Azure Blob Storage URI 路径：配置详见[外部存储服务的 URI 格式](/external-storage-uri.md)。
- TiDB 本地文件路径：必须为绝对路径，数据文件后缀必须为 `.csv`、`.sql` 或 `.parquet`。确保该路径对应的文件存储在当前用户连接的 TiDB 节点上，且当前连接的用户有 `FILE` 权限。

> **注意：**
>
> 如果目标集群开启了 [SEM](/system-variables.md#tidb_enable_enhanced_security)，则 fileLocation 不能指定为本地文件路径。

使用 fileLocation 可以指定单个文件，也可使用通配符 `*` 来匹配需要导入的多个文件。注意通配符只能用在文件名部分，不会匹配目录，也不会递归处理子目录下相关的文件。下面以数据存储在 S3 为例：

- 导入单个文件：`s3://<bucket-name>/path/to/data/foo.csv`
- 导入指定路径下的所有文件：`s3://<bucket-name>/path/to/data/*`
- 导入指定路径下的所有以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/*.csv`
- 导入指定路径下所有以 `foo` 为前缀的文件：`s3://<bucket-name>/path/to/data/foo*`
- 导入指定路径下以 `foo` 为前缀、以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/foo*.csv`

### Format

`IMPORT INTO` 支持 3 种数据文件格式，包括 `CSV`、`SQL` 和 `PARQUET`。当不指定该参数时，默认格式为 `CSV`。

### WithOptions

你可以通过 WithOptions 来指定导入选项，控制数据导入过程。例如，如需使导入任务在后台异步执行，你可以通过在 `IMPORT INTO` 语句中添加 `WITH DETACHED` 选项来开启导入任务的 `DETACHED` 模式。

目前支持的选项包括：

| 选项名 | 支持的数据格式 | 描述 |
|:---|:---|:---|
| `CHARACTER_SET='<string>'` | CSV | 指定数据文件的字符集，默认为 `utf8mb4`。目前支持的字符集包括 `binary`、`utf8`、`utf8mb4`、`gb18030`、`gbk`、`latin1` 和 `ascii`。 |
| `FIELDS_TERMINATED_BY='<string>'` | CSV | 指定字段分隔符，默认为 `,`。 |
| `FIELDS_ENCLOSED_BY='<char>'` | CSV | 指定字段的定界符，默认为 `"`。 |
| `FIELDS_ESCAPED_BY='<char>'` | CSV | 指定字段的转义符，默认为 `\`。 |
| `FIELDS_DEFINED_NULL_BY='<string>'` | CSV | 指定字段为何值时将会被解析为 NULL，默认为 `\N`。 |
| `LINES_TERMINATED_BY='<string>'` | CSV | 指定行分隔符，默认 `IMPORT INTO` 会自动识别分隔符为 `\n`、`\r` 或 `\r\n`，如果行分隔符为以上三种，无须显式指定该选项。 |
| `SKIP_ROWS=<number>` | CSV | 指定需要跳过的行数，默认为 `0`。可通过该参数跳过 CSV 中的 header，如果是通过通配符来指定所需导入的源文件，该参数会对 fileLocation 中通配符匹配的所有源文件生效。 |
| `SPLIT_FILE` | CSV | 将单个 CSV 文件拆分为多个 256 MiB 左右的小文件块进行并行处理，以提高导入效率。该参数仅对**非**压缩的 CSV 文件生效，且该参数和 TiDB Lightning 的 [`strict-format`](/tidb-lightning/tidb-lightning-data-source.md#启用严格格式) 有相同的使用限制。 |
| `DISK_QUOTA='<string>'` | 所有格式 | 指定数据排序期间可使用的磁盘空间阈值。默认值为 TiDB [临时目录](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入)所在磁盘空间的 80%。如果无法获取磁盘总大小，默认值为 50 GiB。当显式指定 DISK_QUOTA 时，该值同样不能超过 TiDB [临时目录](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入)所在磁盘空间的 80%。 |
| `DISABLE_TIKV_IMPORT_MODE` | 所有格式 | 指定是否禁止导入期间将 TiKV 切换到导入模式。默认不禁止。如果当前集群存在正在运行的读写业务，为避免导入过程对这部分业务造成影响，可开启该参数。 |
| `THREAD=<number>` | 所有格式 | 指定导入的并发度。默认值为 TiDB 节点的 CPU 核数的 50%，最小值为 1。可以显示指定该参数来控制对资源的占用，但最大值不能超过 CPU 核数。如需导入数据到一个空集群，建议可以适当调大该值，以提升导入性能。如果目标集群已经用于生产环境，请根据业务要求按需调整该参数值。 |
| `MAX_WRITE_SPEED='<string>'` | 所有格式 | 控制写入到单个 TiKV 的速度，默认无速度限制。例如设置为 `1MiB`，则限制写入速度为 1 MiB/s。|
| `CHECKSUM_TABLE='<string>'` | 所有格式 | 配置是否在导入完成后对目标表是否执行 CHECKSUM 检查来验证导入的完整性。可选的配置项为 `"required"`（默认）、`"optional"` 和 `"off"`。`"required"` 表示在导入完成后执行 CHECKSUM 检查，如果 CHECKSUM 检查失败，则会报错退出。`"optional"` 表示在导入完成后执行 CHECKSUM 检查，如果报错，会输出一条警告日志并忽略报错。`"off"` 表示导入结束后不执行 CHECKSUM 检查。 |
| `DETACHED` | 所有格式 | 该参数用于控制 `IMPORT INTO` 是否异步执行。开启该参数后，执行 `IMPORT INTO` 会立即返回该导入任务的 `Job_ID` 等信息，且该任务会在后台异步执行。 |
| `CLOUD_STORAGE_URI` | 所有格式 | 指定编码后的 KV 数据[全局排序](/tidb-global-sort.md)的目标存储地址。未指定该参数时，`IMPORT INTO` 会根据系统变量 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-从-v740-版本开始引入) 的值来确定是否使用全局排序，如果该系统变量指定了目标存储地址，就使用指定的地址进行全局排序。当指定该参数时，如果参数值不为空，`IMPORT INTO` 会使用该参数值作为目标存储地址；如果参数值为空，则表示强制使用本地排序。目前目标存储地址仅支持 Amazon S3，具体 Amazon S3 URI 格式配置，请参见 [Amazon S3 URI 格式](/external-storage-uri.md#amazon-s3-uri-格式)。注意当使用该功能时，所有 TiDB 节点都需要有目标 Amazon S3 bucket 的读写权限。 |

## 压缩文件

`IMPORT INTO` 支持导入压缩的 `CSV` 和 `SQL` 文件，会自动根据数据文件后缀来确定该文件是否为压缩文件以及压缩格式：

| 后缀名 | 压缩格式 |
|:---|:---|
| `.gz`、`.gzip` | gzip 压缩格式 |
| `.zstd`、`.zst` | ZStd 压缩格式 |
| `.snappy` | snappy 压缩格式 |

> **注意：**
>
> Snappy 压缩文件必须遵循[官方 Snappy 格式](https://github.com/google/snappy)。不支持其他非官方压缩格式。

## 全局排序

> **警告：**
>
> 全局排序为实验特性，不建议在生产环境中使用。

`IMPORT INTO` 会将源数据文件的导入拆分到多个子任务中，各个子任务独立进行编码排序并导入。如果各个子任务编码后的 KV (TiDB 将数据编码为 KV 的方式，参考 [TiDB 数据库的计算](/tidb-computing.md)) range 重叠过多，导入时 TiKV 需要不断地进行 compaction，会降低导入的性能和稳定性。

在以下情况中，可能存在较多的 KV range 重叠：

- 如果分配到各子任务的数据文件中的行存在主键范围的重叠，那么各个子任务编码后产生的数据 KV 也会存在重叠。
    - 说明：`IMPORT INTO` 会按数据文件遍历顺序来划分子任务，一般遍历文件按文件名字典序来排列。
- 如果目标表索引较多，或索引列值在数据文件中较分散，那么各个子任务编码后产生的索引 KV 也会存在重叠。

当开启[后端任务分布式框架](/tidb-distributed-execution-framework.md) 时，可通过 `IMPORT INTO` 的 `CLOUD_STORAGE_URI` 参数，或者使用系统变量 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-从-v740-版本开始引入) 指定编码后的 KV 数据的目标存储地址来开启[全局排序](/tidb-global-sort.md)。注意目前仅支持使用 S3 作为全局排序存储地址。开启全局排序后，`IMPORT INTO` 会将编码后的 KV 数据写入云存储，并在云存储进行全局排序，之后再将全局排序后的索引数据和表数据并行导入到 TiKV，从而避免因 KV 重叠导致的问题，以提升导入的稳定性。

全局排序对内存资源的使用较高，在数据导入开始前，建议先设置 [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-从-v640-版本开始引入) 和 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 两个变量，避免频繁触发 golang GC 从而影响导入效率：

```sql
SET GLOBAL tidb_server_memory_limit_gc_trigger=0.99;
SET GLOBAL tidb_server_memory_limit='88%';
```

> **注意：**
>
> - 如果源数据文件 KV range 重叠较少，开启全局排序后可能会降低导入性能，因为全局排序需要等所有子任务的数据本地排序后，再进行额外的全局排序操作，之后才进行导入。
> - 使用全局排序的导入任务完成后，存放在云存储里用于全局排序的文件会在后台线程中异步清理。

## 输出内容

当 `IMPORT INTO` 导入完成，或者开启了 `DETACHED` 模式时，`IMPORT INTO` 会返回当前任务的信息。以下为一些示例，字段的含义描述请参考 [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)。

当 `IMPORT INTO` 导入完成时输出：

```sql
IMPORT INTO t FROM '/path/to/small.csv';
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status   | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time                 | End_Time                   | Created_By |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
|  60002 | /path/to/small.csv | `test`.`t`   |      363 |       | finished | 16B              |             2 |                | 2023-06-08 16:01:22.095698 | 2023-06-08 16:01:22.394418 | 2023-06-08 16:01:26.531821 | root@%     |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
```

开启了 `DETACHED` 模式时，执行 `IMPORT INTO` 语句会立即返回输出。从输出中，你可以看到该任务状态 `Status` 为 `pending`，表示等待执行。

```sql
IMPORT INTO t FROM '/path/to/small.csv' WITH DETACHED;
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status  | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time | End_Time | Created_By |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
|  60001 | /path/to/small.csv | `test`.`t`   |      361 |       | pending | 16B              |          NULL |                | 2023-06-08 15:59:37.047703 | NULL       | NULL     | root@%     |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
```

## 查看和控制导入任务

对于开启了 `DETACHED` 模式的任务，可通过 [`SHOW IMPORT`](/sql-statements/sql-statement-show-import-job.md) 来查看当前任务的执行进度。

任务启动后，可通过 [`CANCEL IMPORT JOB <job-id>`](/sql-statements/sql-statement-cancel-import-job.md) 来取消对应任务。

## 使用示例

### 导入带有 header 的 CSV 文件

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH skip_rows=1;
```

### 以 `DETACHED` 模式异步导入

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH DETACHED;
```

### 忽略数据文件中的特定字段

假设数据文件为以下 CSV 文件：

```
id,name,age
1,Tom,23
2,Jack,44
```

假设要导入的目标表结构为 `CREATE TABLE t(id int primary key, name varchar(100))`，则可通过以下方式来忽略导入文件中的 `age` 字段：

```sql
IMPORT INTO t(id, name, @1) FROM '/path/to/file.csv' WITH skip_rows=1;
```

### 使用通配符 `*` 导入多个数据文件

假设在 `/path/to/` 目录下有 `file-01.csv`、`file-02.csv` 和 `file-03.csv` 三个文件，如需通过 `IMPORT INTO` 将这三个文件导入到目标表 `t` 中，可使用如下 SQL 语句：

```sql
IMPORT INTO t FROM '/path/to/file-*.csv'
```

### 从 S3、GCS 或 Azure Blob Storage 导入数据

- 从 S3 导入数据

    ```sql
    IMPORT INTO t FROM 's3://bucket-name/test.csv?access-key=XXX&secret-access-key=XXX';
    ```

- 从 GCS 导入数据

    ```sql
    IMPORT INTO t FROM 'gs://import/test.csv?credentials-file=${credentials-file-path}';
    ```

- 从 Azure Blob Storage 导入数据

    ```sql
    IMPORT INTO t FROM 'azure://import/test.csv?credentials-file=${credentials-file-path}';
    ```

关于 Amazon S3、GCS 和 Azure Blob Storage 的 URI 路径配置，详见[外部存储服务的 URI 格式](/external-storage-uri.md)。

### 通过 SetClause 语句计算列值

假设数据文件为以下 CSV 文件：

```
id,name,val
1,phone,230
2,book,440
```

要导入的目标表结构为 `CREATE TABLE t(id int primary key, name varchar(100), val int)`，并且希望在导入时将 `val` 列值扩大 100 倍，则可通过以下方式来导入：

```sql
IMPORT INTO t(id, name, @1) SET val=@1*100 FROM '/path/to/file.csv' WITH skip_rows=1;
```

### 导入 SQL 格式的数据文件

```sql
IMPORT INTO t FROM '/path/to/file.sql' FORMAT 'sql';
```

### 限制写入 TiKV 的速度

限制写入单个 TiKV 的速度为 10 MiB/s：

```sql
IMPORT INTO t FROM 's3://bucket/path/to/file.parquet?access-key=XXX&secret-access-key=XXX' FORMAT 'parquet' WITH MAX_WRITE_SPEED='10MiB';
```

## MySQL 兼容性

该语句是对 MySQL 语法的扩展。

## 另请参阅

* [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)
* [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
