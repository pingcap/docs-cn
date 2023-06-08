---
title: IMPORT INTO
summary: TiDB 数据库中 IMPORT INTO 的使用概况。
---

# IMPORT INTO

`IMPORT INTO` 语句使用 TiDB Lightning 的 [物理导入](/tidb-lightning/tidb-lightning-physical-import-mode.md) 机制，用于将 `CSV`, `SQL`, `PARQUET` 等格式的数据导入到一张空表中。

> **警告：**
>
> 目前该语句为实验特性，不建议在生产环境中使用。

## 使用限制
- `IMPORT INTO` 只能导入导入到数据库中已有的表，且该表需要是空表。
- `IMPORT INTO` 不支持事务，也无法回滚，在显示事务(`BEGIN`/`END`)中执行会报错。
- `IMPORT INTO` 在导入完成前会阻塞当前连接，如果需要异步执行，可以添加 `DETACHED` 选项。
- `IMPORT INTO` 执行开始前会删除当前表的所有二级索引，等数据导入完成后，再将索引添加回来。
- `IMPORT INTO` 不支持跟 CDC, PiTR 等程序一起工作。
- `IMPORT INTO` 每个集群上同时只能有一个 `IMPORT INTO` 任务在运行。
- `IMPORT INTO` 导入数据的过程中，请勿在目标表进行 DDL 和 DML 操作，否则会导致导入失败或数据不一致。导入期间也不建议进行读操作，因为读取的数据可能不一致。请在导入操作完成后再进行读写操作。
- `IMPORT INTO` 导入期间会占用大量系统资源，建议使用 32 核以上的 CPU 和 64 GiB 以上内存以获得更好的性能。导入期间会将排序好的数据写入到 TiDB [临时目录](/tidb-configuration-file.md#temp-dir-new-in-v630) 下，建议优先考虑配置闪存等高性能存储介质，详细请参考 [物理导入使用限制](/tidb-lightning/tidb-lightning-physical-import-mode.md#requirements-and-restrictions)。

## 导入前准备
在使用 `IMPORT INTO` 开始导入数据前，请确保：
- 要导入的目标表在下游已经创建，并且是空表。
- 当前集群有足够的剩余空间能容纳要导入的数据。
- 确保当前连接的 TiDB 节点的 [临时目录](/tidb-configuration-file.md#temp-dir-new-in-v630) 有至少 90GiB 的磁盘空间。如果开启了 [tidb_enable_dist_task](/system-variables.md#tidb_enable_dist_task-new-in-v710) 需要确保集群中所有的 TiDB 节点都有足够的磁盘空间。

## 需要的权限

执行 `IMPORT INTO` 的用户需要有目标表的 `SELECT`、`UPDATE`、`INSERT`、`DELETE`、`ALTER` 权限，如果是导入 TiDB 服务器本地文件，还需要有 `FILE` 权限。

## 语法图

```ebnf+diagram
ImportIntoStmt ::=
    'IMPORT' 'INTO' TableName ColumnNameOrUserVarList? SetSpec? FROM fileLocation Format? WithOptions?

ColumnNameOrUserVarList ::=
    '(' ColumnNameOrUserVar (',' ColumnNameOrUserVar)* ')'

SetSpec ::=
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

用于指定数据文件中每行的各个字段如何对应到目标表列，也可以将字段对应到某个变量，用来跳过某些字段或者在 SetSpec 中使用。

当指定该参数时，指定的列或变量个数需要跟数据文件每行的字段数一致。

当不指定该参数，数据文件每行的字段数需要跟目标表列数一致，且各个字段会按顺序导入到对应的列，

### SetSpec

用于指定目标列值的计算方式，在 SET 表达式右侧中可以引用 `ColumnNameOrUserVarList` 中保存的变量。

SET 表达式左侧只能引用 `ColumnNameOrUserVarList` 没有的列名，如果在 `ColumnNameOrUserVarList` 中已经有了目标列名，则该 SET 无效。

### fileLocation

用于指定数据文件的位置，该位置可以有效是 S3/GCS URI 路径，详见[外部存储](/br/backup-and-restore-storages.md)；也可以是本地文件路径，此时该路径对应的文件必须在当前连接的 TiDB 实例上。

当 fileLocation 为本地文件路径时，必须是绝对路径，且数据文件必须以 `.csv`, `.sql`, `.parquet` 为后缀。且此时当前连接用户需要有 `FILE` 权限。

如果目标集群开启了 [SEM](/system-variables.md#tidb_enable_enhanced_security)，则 fileLocation 不能指定为本地文件路径。

使用 fileLocation 可以指定单个文件，也可使用通配符 `*` 来匹配需要导入的多个文件。注意通配符只能用在文件名部分，不会匹配目录，也不会递归处理子目录下相关的文件。以数据存储在 S3 为例，示例如下:

- 导入单个文件：`s3://<bucket-name>/path/to/data/foo.csv`
- 导入指定路径下的所有文件：`s3://<bucket-name>/path/to/data/*`
- 导入指定路径下的所有以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/*.csv`
- 导入指定路径下所有以 `foo` 为前缀的文件：`s3://<bucket-name>/path/to/data/foo*`
- 导入指定路径下以 `foo` 为前缀、以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/foo*.csv`

### Format

`IMPORT INTO` 支持 3 种数据文件格式，`CSV`, `SQL`, `PARQUET`，当不指定该语句时，默认格式为 `CSV`。

### WithOptions

可通过 WithOptions 来指定选项值，来控制导入过程，目前支持的选项包括：

| 参数名 | 支持的数据格式 | 描述 |
|:---|:---|:---|
| CHARACTER_SET='<string>' | CSV | 指定数据文件的字符集，默认字符集为 utf8mb4。目前支持的字符集包括 `binary`, `utf8`, `utf8mb4`, `gb18030`, `gbk`, `latin1`, `ascii` |
| FIELDS_TERMINATED_BY='<string>' | CSV | 指定字段分隔符，默认为 `,` |
| FIELDS_ENCLOSED_BY='<char>' | CSV | 指定字段的定界符，默认为 `"` |
| FIELDS_ESCAPED_BY='<char>' | CSV | 指定字段的转义符，默认为 `\` |
| FIELDS_DEFINED_NULL_BY='<string>' | CSV | 指定字段为何值时将会被解析为 NULL，默认为 `\N` |
| LINES_TERMINATED_BY='<string>' | CSV | 指定行分隔符，默认 `IMPORT INTO` 会自动识别分隔符为 `\n` 或 `\r` 或 `\r\n`，如果行分隔符为以上三种，不需要显示设置 |
| SKIP_ROWS=<number> | CSV | 指定需要跳过的行数，默认为 0，可通过该参数跳过 CSV 中的 header，该参数会对 fileLocation 中匹配的所有文件生效 |
| DISK_QUOTA='<string>' | 所有格式 | 该参数指定数据排序期间，可使用的磁盘空间阈值。默认值为 TiDB [临时目录](/tidb-configuration-file.md#temp-dir-new-in-v630) 所在磁盘空间的 80%，如果无法获取磁盘总大小，默认值为 50GiB。当显示设置 DISK_QUOTA 时，该值同样不能超过 TiDB [临时目录](/tidb-configuration-file.md#temp-dir-new-in-v630) 所在磁盘空间的 80% |
| DISABLE_TIKV_IMPORT_MODE | 所有格式 | 该参数指定是否禁止导入期间将 TiKV 切换到 import mode，默认不禁止。如果当前集群存在正在运行的读写业务，为避免导入过程对这部分业务造成过多影响，可开启该参数 |
| THREAD=<number> | 所有格式 | 指定导入的并发度，当数据文件格式为 CSV 或 SQL 时，默认值为 CPU 核数，如果数据文件为 PARQUET，则默认为 CPU 核数的 75%。可以显示指定该参数来控制对资源的占用，但该值最大为 CPU 核数 |
| MAX_WRITE_SPEED='<string>' | 所有格式 | 该参数用于控制写入到单个 TiKV 的速度，默认无速度限制 |
| CHECKSUM_TABLE='<string>' | 所有格式 | 配置是否在导入完成后对目标表指定 checksum 对比操作来验证导入的完整性。可选的配置项： "required"（默认）。在导入完成后执行 CHECKSUM 检查，如果 CHECKSUM 检查失败，则会报错退出；"optional" 在导入完成后执行 CHECKSUM 检查，如果报错，会输出一条 WARN 日志并忽略错误；"off"。导入结束后不执行 CHECKSUM 检查。 |
| DETACHED | 所有格式 | 该参数用于控制 `IMPORT INTO` 是否异步执行，开启该参数后会输出任务 id，且该任务会在后台异步执行。 |

## 查看和控制导入任务

对于开启了 DETACHED 模式的任务，可通过 [`SHOW IMPORT JOB(s)`]() 来查看当前任务的执行进度。

任务启动后，可通过 [`CANCEL IMPORT JOB`]() 来取消对应任务。

## 使用示例

## MySQL 兼容性

该语句是对 MySQL 语法的扩展。

## 另请参阅

* [INSERT](/sql-statements/sql-statement-insert.md)
* [乐观事务模型](/optimistic-transaction.md)
* [悲观事务模式](/pessimistic-transaction.md)
