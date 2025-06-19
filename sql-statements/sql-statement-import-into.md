---
title: IMPORT INTO
summary: TiDB 中 IMPORT INTO 的使用概述。
---

# IMPORT INTO

`IMPORT INTO` 语句允许你通过 TiDB Lightning 的[物理导入模式](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)将数据导入到 TiDB。你可以通过以下两种方式使用 `IMPORT INTO`：

- `IMPORT INTO ... FROM FILE`：将 `CSV`、`SQL` 和 `PARQUET` 等格式的数据文件导入到 TiDB 的空表中。
- `IMPORT INTO ... FROM SELECT`：将 `SELECT` 语句的查询结果导入到 TiDB 的空表中。你还可以使用它导入通过 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

<CustomContent platform="tidb">

> **注意：**
>
> 与 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 相比，`IMPORT INTO` 可以直接在 TiDB 节点上执行，支持自动分布式任务调度和 [TiDB 全局排序](/tidb-global-sort.md)，在部署、资源利用、任务配置便利性、调用和集成便利性、高可用性和可扩展性等方面都有显著改进。建议你在适当的场景下考虑使用 `IMPORT INTO` 替代 TiDB Lightning。

</CustomContent>

## 限制

- `IMPORT INTO` 只支持将数据导入到数据库中已存在的空表中。
- `IMPORT INTO` 不支持在表的其他分区已包含数据的情况下将数据导入到空分区。目标表必须完全为空才能进行导入操作。
- `IMPORT INTO` 不支持将数据导入到[临时表](/temporary-tables.md)或[缓存表](/cached-tables.md)中。
- `IMPORT INTO` 不支持事务或回滚。在显式事务（`BEGIN`/`END`）中执行 `IMPORT INTO` 将返回错误。
- `IMPORT INTO` 不支持与[备份恢复](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)、[`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)、[加速添加索引](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)、使用 TiDB Lightning 导入数据、使用 TiCDC 复制数据或[时间点恢复 (PITR)](https://docs.pingcap.com/tidb/stable/br-log-architecture) 等功能同时工作。有关更多兼容性信息，请参见 [TiDB Lightning 和 `IMPORT INTO` 与 TiCDC 和日志备份的兼容性](https://docs.pingcap.com/tidb/stable/tidb-lightning-compatibility-and-scenarios)。
- 在数据导入过程中，不要对目标表执行 DDL 或 DML 操作，也不要对目标数据库执行 [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)。这些操作可能导致导入失败或数据不一致。此外，**不建议**在导入过程中执行读取操作，因为读取的数据可能不一致。只有在导入完成后才执行读写操作。
- 导入过程会显著消耗系统资源。对于 TiDB Self-Managed，为获得更好的性能，建议使用至少 32 核和 64 GiB 内存的 TiDB 节点。TiDB 在导入期间会将排序后的数据写入 TiDB [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)，因此建议为 TiDB Self-Managed 配置高性能存储介质，如闪存。更多信息，请参见[物理导入模式限制](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode#requirements-and-restrictions)。
- 对于 TiDB Self-Managed，TiDB [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)预期至少有 90 GiB 的可用空间。建议分配等于或大于要导入的数据量的存储空间。
- 一个导入任务只支持导入数据到一个目标表。
- 在 TiDB 集群升级期间不支持 `IMPORT INTO`。
- 确保要导入的数据不包含主键或非空唯一索引冲突的记录。否则，冲突可能导致导入任务失败。
- 已知问题：如果 TiDB 节点配置文件中的 PD 地址与集群当前的 PD 拓扑不一致，`IMPORT INTO` 任务可能会失败。这种不一致可能出现在以下情况：例如之前进行了 PD 缩容，但 TiDB 配置文件未相应更新，或者在配置文件更新后 TiDB 节点未重启。
### `IMPORT INTO ... FROM FILE` 限制

- 对于 TiDB Self-Managed，每个 `IMPORT INTO` 任务支持导入 10 TiB 以内的数据。如果启用[全局排序](/tidb-global-sort.md)功能，每个 `IMPORT INTO` 任务支持导入 40 TiB 以内的数据。
- 对于 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)，如果要导入的数据超过 500 GiB，建议使用至少 16 核的 TiDB 节点并启用[全局排序](/tidb-global-sort.md)功能，此时每个 `IMPORT INTO` 任务支持导入 40 TiB 以内的数据。如果要导入的数据在 500 GiB 以内，或者 TiDB 节点的核数少于 16，则不建议启用[全局排序](/tidb-global-sort.md)功能。
- `IMPORT INTO ... FROM FILE` 的执行会阻塞当前连接，直到导入完成。要异步执行该语句，可以添加 `DETACHED` 选项。
- 每个集群最多可以同时运行 16 个 `IMPORT INTO` 任务（参见 [TiDB 分布式执行框架 (DXF) 使用限制](/tidb-distributed-execution-framework.md#limitation)）。当集群资源不足或达到最大任务数时，新提交的导入任务将排队等待执行。
- 当使用[全局排序](/tidb-global-sort.md)功能进行数据导入时，`THREAD` 选项的值必须至少为 `8`。
- 当使用[全局排序](/tidb-global-sort.md)功能进行数据导入时，单行数据编码后的大小不能超过 32 MiB。
- 所有在未启用 [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md) 时创建的 `IMPORT INTO` 任务都直接在提交任务的节点上运行，即使后来启用了 DXF，这些任务也不会被调度到其他 TiDB 节点执行。启用 DXF 后，只有新创建的从 S3 或 GCS 导入数据的 `IMPORT INTO` 任务才会自动调度或故障转移到其他 TiDB 节点执行。

### `IMPORT INTO ... FROM SELECT` 限制

- `IMPORT INTO ... FROM SELECT` 只能在当前用户连接的 TiDB 节点上执行，并且会阻塞当前连接直到导入完成。
- `IMPORT INTO ... FROM SELECT` 只支持两个[导入选项](#withoptions)：`THREAD` 和 `DISABLE_PRECHECK`。
- `IMPORT INTO ... FROM SELECT` 不支持任务管理语句，如 `SHOW IMPORT JOB(s)` 和 `CANCEL IMPORT JOB <job-id>`。
- TiDB 的[临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)需要足够的空间来存储 `SELECT` 语句的整个查询结果（目前不支持配置 `DISK_QUOTA` 选项）。
- 不支持使用 [`tidb_snapshot`](/read-historical-data.md) 导入历史数据。
- 由于 `SELECT` 子句的语法复杂，`IMPORT INTO` 中的 `WITH` 参数可能与之冲突并导致解析错误，例如 `GROUP BY ... [WITH ROLLUP]`。建议为复杂的 `SELECT` 语句创建视图，然后使用 `IMPORT INTO ... FROM SELECT * FROM view_name` 进行导入。或者，可以用括号明确 `SELECT` 子句的范围，例如 `IMPORT INTO ... FROM (SELECT ...) WITH ...`。

## 导入前提条件

在使用 `IMPORT INTO` 导入数据之前，请确保满足以下要求：

- 要导入的目标表已在 TiDB 中创建，且为空表。
- 目标集群有足够的空间存储要导入的数据。
- 对于 TiDB Self-Managed，当前会话连接的 TiDB 节点的[临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)至少有 90 GiB 的可用空间。如果启用了 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 且导入数据来自 S3 或 GCS，还要确保集群中每个 TiDB 节点的临时目录都有足够的磁盘空间。

## 所需权限

执行 `IMPORT INTO` 需要目标表的 `SELECT`、`UPDATE`、`INSERT`、`DELETE` 和 `ALTER` 权限。要导入 TiDB 本地存储中的文件，还需要 `FILE` 权限。
## 语法

```ebnf+diagram
ImportIntoStmt ::=
    'IMPORT' 'INTO' TableName ColumnNameOrUserVarList? SetClause? FROM fileLocation Format? WithOptions?
    |
    'IMPORT' 'INTO' TableName ColumnNameList? FROM SelectStatement WithOptions?

ColumnNameOrUserVarList ::=
    '(' ColumnNameOrUserVar (',' ColumnNameOrUserVar)* ')'

ColumnNameList ::=
    '(' ColumnName (',' ColumnName)* ')'

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

指定数据文件中的每个字段如何对应目标表中的列。你还可以使用它将字段映射到变量以跳过某些字段的导入，或在 `SetClause` 中使用它。

- 如果未指定此参数，数据文件中每行的字段数必须与目标表的列数匹配，并且字段将按顺序导入到对应的列中。
- 如果指定了此参数，指定的列或变量数必须与数据文件中每行的字段数匹配。

### SetClause

指定如何计算目标列的值。在 `SET` 表达式的右侧，你可以引用在 `ColumnNameOrUserVarList` 中指定的变量。

在 `SET` 表达式的左侧，你只能引用不包含在 `ColumnNameOrUserVarList` 中的列名。如果目标列名已存在于 `ColumnNameOrUserVarList` 中，则 `SET` 表达式无效。

### fileLocation

指定数据文件的存储位置，可以是 Amazon S3 或 GCS 的 URI 路径，或者是 TiDB 本地文件路径。

- Amazon S3 或 GCS URI 路径：有关 URI 配置详情，请参见[外部存储服务的 URI 格式](/external-storage-uri.md)。

- TiDB 本地文件路径：必须是绝对路径，且文件扩展名必须是 `.csv`、`.sql` 或 `.parquet`。确保此路径对应的文件存储在当前用户连接的 TiDB 节点上，且用户具有 `FILE` 权限。

> **注意：**
>
> 如果目标集群启用了 [SEM](/system-variables.md#tidb_enable_enhanced_security)，则 `fileLocation` 不能指定为本地文件路径。

在 `fileLocation` 参数中，你可以指定单个文件，或使用 `*` 和 `[]` 通配符匹配多个文件进行导入。注意，通配符只能用于文件名，因为它不匹配目录或递归匹配子目录中的文件。以存储在 Amazon S3 上的文件为例，你可以按以下方式配置参数：

- 导入单个文件：`s3://<bucket-name>/path/to/data/foo.csv`
- 导入指定路径中的所有文件：`s3://<bucket-name>/path/to/data/*`
- 导入指定路径中所有扩展名为 `.csv` 的文件：`s3://<bucket-name>/path/to/data/*.csv`
- 导入指定路径中所有以 `foo` 为前缀的文件：`s3://<bucket-name>/path/to/data/foo*`
- 导入指定路径中所有以 `foo` 为前缀且扩展名为 `.csv` 的文件：`s3://<bucket-name>/path/to/data/foo*.csv`
- 导入指定路径中的 `1.csv` 和 `2.csv`：`s3://<bucket-name>/path/to/data/[12].csv`
### Format

`IMPORT INTO` 语句支持三种数据文件格式：`CSV`、`SQL` 和 `PARQUET`。如果未指定，默认格式为 `CSV`。

### WithOptions

你可以使用 `WithOptions` 指定导入选项并控制数据导入过程。例如，要在后台异步执行数据文件的导入，可以通过在 `IMPORT INTO` 语句中添加 `WITH DETACHED` 选项来启用导入的 `DETACHED` 模式。

支持的选项如下：

| 选项名称 | 支持的数据源和格式 | 描述 |
|:---|:---|:---|
| `CHARACTER_SET='<string>'` | CSV | 指定数据文件的字符集。默认字符集为 `utf8mb4`。支持的字符集包括 `binary`、`utf8`、`utf8mb4`、`gb18030`、`gbk`、`latin1` 和 `ascii`。 |
| `FIELDS_TERMINATED_BY='<string>'` | CSV | 指定字段分隔符。默认分隔符为 `,`。 |
| `FIELDS_ENCLOSED_BY='<char>'` | CSV | 指定字段定界符。默认定界符为 `"`。 |
| `FIELDS_ESCAPED_BY='<char>'` | CSV | 指定字段转义字符。默认转义字符为 `\`。 |
| `FIELDS_DEFINED_NULL_BY='<string>'` | CSV | 指定字段中表示 `NULL` 的值。默认值为 `\N`。 |
| `LINES_TERMINATED_BY='<string>'` | CSV | 指定行终止符。默认情况下，`IMPORT INTO` 自动识别 `\n`、`\r` 或 `\r\n` 作为行终止符。如果行终止符是这三个之一，则不需要显式指定此选项。 |
| `SKIP_ROWS=<number>` | CSV | 指定要跳过的行数。默认值为 `0`。你可以使用此选项跳过 CSV 文件中的标题。如果你使用通配符指定导入的源文件，此选项适用于 `fileLocation` 中通配符匹配的所有源文件。 |
| `SPLIT_FILE` | CSV | 将单个 CSV 文件拆分为多个大约 256 MiB 的小块进行并行处理，以提高导入效率。此参数仅适用于**未压缩**的 CSV 文件，并且具有与 TiDB Lightning [`strict-format`](https://docs.pingcap.com/tidb/stable/tidb-lightning-data-source#strict-format) 相同的使用限制。注意，对于此选项，你需要显式指定 `LINES_TERMINATED_BY`。 |
| `DISK_QUOTA='<string>'` | 所有文件格式 | 指定数据排序期间可以使用的磁盘空间阈值。默认值为 TiDB [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)中磁盘空间的 80%。如果无法获取总磁盘大小，默认值为 50 GiB。显式指定 `DISK_QUOTA` 时，确保该值不超过 TiDB 临时目录中磁盘空间的 80%。 |
| `DISABLE_TIKV_IMPORT_MODE` | 所有文件格式 | 指定是否在导入过程中禁用将 TiKV 切换到导入模式。默认情况下，不禁用将 TiKV 切换到导入模式。如果集群中有正在进行的读写操作，你可以启用此选项以避免导入过程的影响。 |
| `THREAD=<number>` | 所有文件格式和 `SELECT` 的查询结果 | 指定导入的并发度。对于 `IMPORT INTO ... FROM FILE`，`THREAD` 的默认值是 TiDB 节点 CPU 核数的 50%，最小值为 `1`，最大值为 CPU 核数。对于 `IMPORT INTO ... FROM SELECT`，`THREAD` 的默认值为 `2`，最小值为 `1`，最大值为 TiDB 节点 CPU 核数的两倍。要将数据导入到没有任何数据的新集群中，建议适当增加此并发度以提高导入性能。如果目标集群已在生产环境中使用，建议根据应用程序要求调整此并发度。 |
| `MAX_WRITE_SPEED='<string>'` | 所有文件格式 | 控制对 TiKV 节点的写入速度。默认情况下，没有速度限制。例如，你可以将此选项指定为 `1MiB` 以将写入速度限制为 1 MiB/s。 |
| `CHECKSUM_TABLE='<string>'` | 所有文件格式 | 配置是否在导入后对目标表执行校验和检查以验证导入完整性。支持的值包括 `"required"`（默认）、`"optional"` 和 `"off"`。`"required"` 表示在导入后执行校验和检查。如果校验和检查失败，TiDB 将返回错误并退出导入。`"optional"` 表示在导入后执行校验和检查。如果发生错误，TiDB 将返回警告并忽略错误。`"off"` 表示在导入后不执行校验和检查。 |
| `DETACHED` | 所有文件格式 | 控制是否异步执行 `IMPORT INTO`。启用此选项时，执行 `IMPORT INTO` 会立即返回导入作业的信息（如 `Job_ID`），作业在后台异步执行。 |
| `CLOUD_STORAGE_URI` | 所有文件格式 | 指定用于存储[全局排序](/tidb-global-sort.md)编码 KV 数据的目标地址。当未指定 `CLOUD_STORAGE_URI` 时，`IMPORT INTO` 根据系统变量 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 的值决定是否使用全局排序。如果该系统变量指定了目标存储地址，`IMPORT INTO` 使用该地址进行全局排序。当指定了非空的 `CLOUD_STORAGE_URI` 时，`IMPORT INTO` 使用该值作为目标存储地址。当指定了空的 `CLOUD_STORAGE_URI` 时，强制使用本地排序。目前，目标存储地址仅支持 S3。有关 URI 配置的详细信息，请参见 [Amazon S3 URI 格式](/external-storage-uri.md#amazon-s3-uri-format)。使用此功能时，所有 TiDB 节点必须具有目标 S3 存储桶的读写访问权限，至少包括以下权限：`s3:ListBucket`、`s3:GetObject`、`s3:DeleteObject`、`s3:PutObject`、`s3: AbortMultipartUpload`。 |
| `DISABLE_PRECHECK` | 所有文件格式和 `SELECT` 的查询结果 | 设置此选项将禁用非关键项目的预检查，例如检查是否存在 CDC 或 PITR 任务。 |
## `IMPORT INTO ... FROM FILE` 使用方法

对于 TiDB Self-Managed，`IMPORT INTO ... FROM FILE` 支持从存储在 Amazon S3、GCS 和 TiDB 本地存储中的文件导入数据。对于 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)，`IMPORT INTO ... FROM FILE` 支持从存储在 Amazon S3 和 GCS 中的文件导入数据。对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)，`IMPORT INTO ... FROM FILE` 支持从存储在 Amazon S3 和阿里云 OSS 中的文件导入数据。

- 对于存储在 Amazon S3 或 GCS 中的数据文件，`IMPORT INTO ... FROM FILE` 支持在 [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md) 中运行。

    - 当启用 DXF（[tidb_enable_dist_task](/system-variables.md#tidb_enable_dist_task-new-in-v710) 为 `ON`）时，`IMPORT INTO` 将数据导入作业拆分为多个子作业，并将这些子作业分配给不同的 TiDB 节点执行，以提高导入效率。
    - 当禁用 DXF 时，`IMPORT INTO ... FROM FILE` 只支持在当前用户连接的 TiDB 节点上运行。

- 对于存储在 TiDB 本地的数据文件，`IMPORT INTO ... FROM FILE` 只支持在当前用户连接的 TiDB 节点上运行。因此，数据文件需要放置在当前用户连接的 TiDB 节点上。如果你通过代理或负载均衡器访问 TiDB，则无法导入存储在 TiDB 本地的数据文件。

### 压缩文件

`IMPORT INTO ... FROM FILE` 支持导入压缩的 `CSV` 和 `SQL` 文件。它可以根据文件扩展名自动判断文件是否压缩以及压缩格式：

| 扩展名 | 压缩格式 |
|:---|:---|
| `.gz`、`.gzip` | gzip 压缩格式 |
| `.zstd`、`.zst` | ZStd 压缩格式 |
| `.snappy` | snappy 压缩格式 |

> **注意：**
>
> - Snappy 压缩文件必须采用[官方 Snappy 格式](https://github.com/google/snappy)。不支持其他变体的 Snappy 压缩。
> - 由于 TiDB Lightning 无法并发解压单个大型压缩文件，压缩文件的大小会影响导入速度。建议源文件解压后不要超过 256 MiB。

### 全局排序

> **注意：**
>
> 全局排序在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

`IMPORT INTO ... FROM FILE` 将源数据文件的数据导入作业拆分为多个子作业，每个子作业独立编码和排序数据后再导入。如果这些子作业的编码 KV 范围有显著重叠（要了解 TiDB 如何将数据编码为 KV，请参见 [TiDB 计算](/tidb-computing.md)），TiKV 需要在导入期间持续进行 compaction，导致导入性能和稳定性下降。

在以下场景中，KV 范围可能会有显著重叠：

- 如果分配给每个子作业的数据文件中的行具有重叠的主键范围，则每个子作业编码生成的数据 KV 也会重叠。
    - `IMPORT INTO` 根据数据文件的遍历顺序拆分子作业，通常按文件名的字典序排序。
- 如果目标表有很多索引，或者索引列的值在数据文件中分散，则每个子作业编码生成的索引 KV 也会重叠。

当启用 [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md) 时，你可以通过在 `IMPORT INTO` 语句中指定 `CLOUD_STORAGE_URI` 选项或使用系统变量 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 指定编码 KV 数据的目标存储地址来启用[全局排序](/tidb-global-sort.md)。目前，全局排序支持使用 Amazon S3 作为存储地址。启用全局排序后，`IMPORT INTO` 将编码的 KV 数据写入云存储，在云存储中执行全局排序，然后并行将全局排序后的索引和表数据导入到 TiKV。这可以防止由 KV 重叠引起的问题，并提高导入稳定性和性能。

全局排序会消耗大量内存资源。在数据导入之前，建议配置 [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640) 和 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) 变量，这可以避免 golang GC 频繁触发从而影响导入效率。

```sql
SET GLOBAL tidb_server_memory_limit_gc_trigger=1;
SET GLOBAL tidb_server_memory_limit='75%';
```

> **注意：**
>
> - 如果源数据文件中的 KV 范围重叠较低，启用全局排序可能会降低导入性能。这是因为启用全局排序后，TiDB 需要等待所有子作业完成本地排序后才能进行全局排序操作和后续导入。
> - 使用全局排序的导入作业完成后，用于全局排序的云存储中的文件会在后台线程中异步清理。
### 输出

当 `IMPORT INTO ... FROM FILE` 完成导入或启用 `DETACHED` 模式时，TiDB 在输出中返回当前作业信息，如以下示例所示。有关每个字段的说明，请参见 [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)。

当 `IMPORT INTO ... FROM FILE` 完成导入时，示例输出如下：

```sql
IMPORT INTO t FROM '/path/to/small.csv';
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status   | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time                 | End_Time                   | Created_By |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
|  60002 | /path/to/small.csv | `test`.`t`   |      363 |       | finished | 16B              |             2 |                | 2023-06-08 16:01:22.095698 | 2023-06-08 16:01:22.394418 | 2023-06-08 16:01:26.531821 | root@%     |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
```

当启用 `DETACHED` 模式时，执行 `IMPORT INTO ... FROM FILE` 语句将立即在输出中返回作业信息。从输出中可以看到，作业的状态为 `pending`，表示等待执行。

```sql
IMPORT INTO t FROM '/path/to/small.csv' WITH DETACHED;
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status  | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time | End_Time | Created_By |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
|  60001 | /path/to/small.csv | `test`.`t`   |      361 |       | pending | 16B              |          NULL |                | 2023-06-08 15:59:37.047703 | NULL       | NULL     | root@%     |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
```

### 查看和管理导入作业

对于启用了 `DETACHED` 模式的导入作业，你可以使用 [`SHOW IMPORT`](/sql-statements/sql-statement-show-import-job.md) 查看其当前作业进度。

在导入作业启动后，你可以使用 [`CANCEL IMPORT JOB <job-id>`](/sql-statements/sql-statement-cancel-import-job.md) 取消它。

### 示例

#### 导入带有标题的 CSV 文件

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### 在 `DETACHED` 模式下异步导入文件

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH DETACHED;
```

#### 跳过导入数据文件中的特定字段

假设你的数据文件是 CSV 格式，其内容如下：

```
id,name,age
1,Tom,23
2,Jack,44
```

并且假设导入的目标表架构为 `CREATE TABLE t(id int primary key, name varchar(100))`。要跳过导入数据文件中的 `age` 字段到表 `t`，你可以执行以下 SQL 语句：

```sql
IMPORT INTO t(id, name, @1) FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### 使用通配符导入多个数据文件

假设在 `/path/to/` 目录下有三个文件，名为 `file-01.csv`、`file-02.csv` 和 `file-03.csv`。要使用 `IMPORT INTO` 将这三个文件导入到目标表 `t`，你可以执行以下 SQL 语句：

```sql
IMPORT INTO t FROM '/path/to/file-*.csv';
```

如果你只需要将 `file-01.csv` 和 `file-03.csv` 导入到目标表，执行以下 SQL 语句：

```sql
IMPORT INTO t FROM '/path/to/file-0[13].csv';
```

#### 从 Amazon S3 或 GCS 导入数据文件

- 从 Amazon S3 导入数据文件：

    ```sql
    IMPORT INTO t FROM 's3://bucket-name/test.csv?access-key=XXX&secret-access-key=XXX';
    ```

- 从 GCS 导入数据文件：

    ```sql
    IMPORT INTO t FROM 'gs://import/test.csv?credentials-file=${credentials-file-path}';
    ```

有关 Amazon S3 或 GCS 的 URI 路径配置详情，请参见[外部存储服务的 URI 格式](/external-storage-uri.md)。

#### 使用 SetClause 计算列值

假设你的数据文件是 CSV 格式，其内容如下：

```
id,name,val
1,phone,230
2,book,440
```

并且假设导入的目标表架构为 `CREATE TABLE t(id int primary key, name varchar(100), val int)`。如果你想在导入过程中将 `val` 列的值乘以 100，你可以执行以下 SQL 语句：

```sql
IMPORT INTO t(id, name, @1) SET val=@1*100 FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### 导入 SQL 格式的数据文件

```sql
IMPORT INTO t FROM '/path/to/file.sql' FORMAT 'sql';
```

#### 限制对 TiKV 的写入速度

要将对 TiKV 节点的写入速度限制为 10 MiB/s，执行以下 SQL 语句：

```sql
IMPORT INTO t FROM 's3://bucket/path/to/file.parquet?access-key=XXX&secret-access-key=XXX' FORMAT 'parquet' WITH MAX_WRITE_SPEED='10MiB';
```

## `IMPORT INTO ... FROM SELECT` 使用方法

`IMPORT INTO ... FROM SELECT` 允许你将 `SELECT` 语句的查询结果导入到 TiDB 的空表中。你还可以使用它导入通过 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

### 导入 `SELECT` 的查询结果

要将 `UNION` 结果导入到目标表 `t`，并指定导入并发度为 `8`，配置禁用非关键项目的预检查，执行以下 SQL 语句：

```sql
IMPORT INTO t FROM SELECT * FROM src UNION SELECT * FROM src2 WITH THREAD = 8, DISABLE_PRECHECK;
```

### 导入指定时间点的历史数据

要将指定时间点的历史数据导入到目标表 `t`，执行以下 SQL 语句：

```sql
IMPORT INTO t FROM SELECT * FROM src AS OF TIMESTAMP '2024-02-27 11:38:00';
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)
* [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
* [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)
* [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md)
