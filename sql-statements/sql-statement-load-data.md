---
title: LOAD DATA
summary: TiDB 数据库中 LOAD DATA 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-load-data/','/docs-cn/dev/reference/sql/statements/load-data/']
---

# LOAD DATA

`LOAD DATA` 语句用于将数据批量加载到 TiDB 表中。

从 v7.0.0 开始，`LOAD DATA` 集成 TiDB Lightning 的逻辑导入模式 (Logical Import Mode)，使 `LOAD DATA` 语句更加强大，包括：

- 支持从 S3、GCS 导入数据
- 支持导入 Parquet 格式的数据
- 新增参数 `FORMAT`、`FIELDS DEFINED NULL BY` 和 `WITH batch_size=<number>,detached`

从 v7.1.0 开始，`LOAD DATA` 支持以下特性：

- 支持导入压缩的 `DELIMITED DATA` 和 `SQL FILE` 数据文件
- 逻辑导入支持并发导入
- 支持通过 `CharsetOpt` 来指定数据文件的编码格式
- `LOAD DATA` 集成 TiDB Lightning 的物理导入模式 (Physical Import Mode)。该模式不经过 SQL 接口，而是直接将数据以键值对的形式插入 TiKV 节点，是一种高效且快速的导入模式。

> **警告：**
>
> v7.1.0 新增的并发导入和物理导入模式为实验特性，不建议在生产环境中使用。

## 语法图

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit FormatOpt DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt LoadDataOptionListOpt

LocalOpt ::= ('LOCAL')?

FormatOpt ::=
    ('FORMAT' ('DELIMITED DATA' | 'SQL FILE' | 'PARQUET'))?

DuplicateOpt ::=
    ('IGNORE' | 'REPLACE')?

Fields ::=
    ('TERMINATED' 'BY' stringLit
    | ('OPTIONALLY')? 'ENCLOSED' 'BY' stringLit
    | 'ESCAPED' 'BY' stringLit
    | 'DEFINED' 'NULL' 'BY' stringLit ('OPTIONALLY' 'ENCLOSED')?)?

LoadDataOptionListOpt ::=
    ('WITH' (LoadDataOption (',' LoadDataOption)*))?

LoadDataOption ::=
    import_mode '=' ('LOGICAL' | 'PHYSICAL')
    | thread '=' numberLiteral
    | batch_size '=' numberLiteral
    | max_write_speed '=' stringLit
    | detached
```

## 参数说明

### `LOCAL`

你可以使用 `LOCAL` 来指定导入位于客户端的数据文件，此时传入文件参数必须为客户端文件系统路径。

### S3/GCS 路径

如果你不指定 `LOCAL`，则文件参数必须是有效的 S3/GCS URI 路径，详见[外部存储](/br/backup-and-restore-storages.md)。

当数据文件存储在 S3/GCS 上时，你可以导入单个文件，也可使用通配符 `*` 来匹配需要导入的多个文件。注意通配符不会递归处理子目录下相关的文件。以数据存储在 S3 为例，示例如下:

- 导入单个文件：`s3://<bucket-name>/path/to/data/foo.csv`
- 导入指定路径下的所有文件：`s3://<bucket-name>/path/to/data/*`
- 导入指定路径下的所有以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/*.csv`
- 导入指定路径下所有以 `foo` 为前缀的文件：`s3://<bucket-name>/path/to/data/foo*`
- 导入指定路径下以 `foo` 为前缀、以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/foo*.csv`

### `FORMAT`

你可以通过 `FORMAT` 参数来指定数据文件的格式。如果不指定该参数，需要使用的格式为 `DELIMITED DATA`，该格式即 MySQL `LOAD DATA` 支持的数据格式。

数据格式 `DELIMITED DATA` 和 `SQL FILE` 支持压缩文件。`LOAD DATA` 会根据文件名称的后缀来自动决定压缩格式。目前支持的压缩格式如下：

| 文件后缀 | 压缩格式 | 示例 |
|:---|:---|:---|
| `.gz` 或 `.gzip`  | gzip 压缩格式   | `tbl.0001.csv.gz`     |
| `.zstd` 或 `.zst` | zstd 压缩格式   | `tbl.0001.csv.zstd`   |
| `.snappy`      | snappy 压缩格式 | `tbl.0001.csv.snappy` |

### `DuplicateOpt`

该参数与 MySQL 行为一致，具体请参考 [MySQL LOAD DATA 文档](https://dev.mysql.com/doc/refman/8.0/en/load-data.html#load-data-error-handling)。

该参数只适用于逻辑导入模式，对物理导入模式不生效。

### `CharsetOpt`

当数据格式是 `DELIMITED DATA` 时，可以通过 `CharsetOpt` 指定数据文件的编码格式。目前支持下列编码格式：`ascii`、`latin1`、`binary`、`utf8`、`utf8mb4` 和 `gbk`。

```sql
LOAD DATA INFILE 's3://<bucket-name>/path/to/data/foo.csv' INTO TABLE load_charset.latin1 CHARACTER SET latin1
```

### `Fields`、`Lines`、`Ignore Lines`

只有数据格式是 `DELIMITED DATA` 时，才能指定 `Fields`、`Lines`、`Ignore Lines` 等语句。

你可以使用 `Fields` 和 `Lines` 参数来指定如何处理数据格式：

- 使用 `FIELDS TERMINATED BY` 来指定数据的分隔符号。
- 使用 `FIELDS ENCLOSED BY` 来指定数据的包围符号。
- 如果你希望以某个字符为结尾来切分行数据，可以使用 `LINES TERMINATED BY` 来指定行的终止符。

可以使用 `DEFINED NULL BY` 来指定数据文件中如何表示 NULL 值。

- 与 MySQL 行为一致，如果 `ESCAPED BY` 不为空时，例如是默认值 `\`，那么 `\N` 会被认为是 NULL 值。
- 如果使用 `DEFINED NULL BY`，例如 `DEFINED NULL BY 'my-null'`，`my-null` 会被认为是 NULL 值。
- 如果使用 `DEFINED NULL BY ... OPTIONALLY ENCLOSED`，例如 `DEFINED NULL BY 'my-null' OPTIONALLY ENCLOSED`，`my-null` 和 `"my-null"`（假设 `ENCLOSED BY '"'`）会被认为是 NULL 值。
- 如果没有使用 `DEFINED NULL BY` 或者 `DEFINED NULL BY ... OPTIONALLY ENCLOSED`，但使用了 `ENCLOSED BY`，例如 `ENCLOSED BY '"'`，那么 `NULL` 会被认为是 NULL 值。这个行为与 MySQL 一致。
- 其他情况不会被认为是 NULL 值。

例如对于以下格式的数据：

```
"bob","20","street 1"\r\n
"alice","33","street 1"\r\n
```

如果想分别提取 `bob`、`20`、`street 1`，可以指定数据的分隔符号为 `','`，数据的包围符号为 `'\"'`。可以写成：

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

当数据格式为 `DELIMITED DATA` 且不指定处理数据的参数时，将按以下参数处理：

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

你可以通过 `IGNORE <number> LINES` 参数来忽略文件开始的 `<number>` 行。例如，可以使用 `IGNORE 1 LINES` 来忽略文件的第一行。

### `WITH import_mode = ('LOGICAL' | 'PHYSICAL')`

可以通过 `import_mode = ('LOGICAL' | 'PHYSICAL')` 来指定数据导入的模式，默认值为 `LOGICAL`，即逻辑导入。从 v7.1.0 开始，`LOAD DATA` 集成 TiDB Lightning 的物理导入模式，可通过 `WITH import_mode = 'PHYSICAL'` 开启。

物理导入模式只能在非 `LOCAL` 模式下使用，采用单线程执行。目前物理导入尚未接入[冲突监测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#冲突数据检测)，因此遇到数据主键或唯一键冲突时会报 checksum 不一致错误。建议在导入前检查数据文件是否存在键值冲突。其他的限制和必要条件，请参考 [TiDB Lightning Physical Import Mode 简介](/tidb-lightning/tidb-lightning-physical-import-mode.md)。

物理导入模式下，`LOAD DATA` 将本地排序后的数据写入 TiDB [`temp-dir`](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入) 子目录中。子目录命名规则为 `import-<tidb-port>/<job-id>`。

物理导入模式目前尚未接入[磁盘资源配额](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#磁盘资源配额-从-v620-版本开始引入)。请确保对应磁盘有足够的空间，具体可参考[必要条件及限制](/tidb-lightning/tidb-lightning-physical-import-mode.md#必要条件及限制)中存储空间的部分。

### `WITH thread=<number>`

目前该参数仅对逻辑导入生效。

可以通过 `WITH thread=<number>` 指定数据导入的并发度。默认值与 `FORMAT` 有关：

- 当 `FORMAT` 为 `PARQUET` 时，默认值为 CPU 核数的 75%。
- 对于其他 `FORMAT`，默认值为 CPU 的逻辑核数。

### `WITH batch_size=<number>`

可以通过 `WITH batch_size=<number>` 来指定批量写入 TiDB 时的行数，默认值为 `1000`。如果不希望分批写入，可以指定为 `0`。

### `WITH max_write_speed = stringLit`

在使用物理导入模式时，可以通过该参数指定写入单个 TiKV 的速率限制。默认值为 `0`，表示无限制。

该参数支持 [go-units](https://pkg.go.dev/github.com/docker/go-units#example-RAMInBytes) 格式。例如，`WITH max_write_speed = '1MB'` 表示写入单个 TiKV 的最大速率为 `1MB/s`。

### `WITH detached`

如果你指定了 S3/GCS 路径（且未指定 `LOCAL` 参数），可以通过 `WITH detached` 让 `LOAD DATA` 任务在后台运行。此时 `LOAD DATA` 会返回任务的 ID。

你可以执行 [`SHOW LOAD DATA`](/sql-statements/sql-statement-show-load-data.md) 查看创建的任务，也可以使用 [`CANCEL LOAD DATA` 和 `DROP LOAD DATA`](/sql-statements/sql-statement-operate-load-data-job.md) 取消或删除创建的任务。

## 示例

后台运行 job，执行后会输出对应的 job id：

```sql
LOAD DATA INFILE 's3://bucket-name/test.csv?access_key=XXX&secret_access_key=XXX' INTO TABLE my_db.my_table FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n' WITH detached;
```

```sql
+--------+
| Job_ID |
+--------+
|      150063  |
+--------+
1 row in set (3.14 sec)
```

```sql
SHOW LOAD DATA JOB 1;
```

```sql
+--------+----------------------------+----------------------------+---------------------+---------------------------+--------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
| Job_ID | Create_Time                | Start_Time                 | End_Time            | Data_Source               | Target_Table       | Import_Mode | Created_By | Job_State | Job_Status | Source_File_Size | Loaded_File_Size | Result_Code | Result_Message |
+--------+----------------------------+----------------------------+---------------------+---------------------------+-------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
|      1 | 2023-03-16 22:29:12.990576 | 2023-03-16 22:29:12.991951 | 0000-00-00 00:00:00 | s3://bucket-name/test.csv | `my_db`.`my_table` | logical     | root@%     | loading   | running    | 52.43MB          | 43.58MB          |             |                |
+--------+----------------------------+----------------------------+---------------------+---------------------------+--------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
1 row in set (0.01 sec)
```

通过 `LOAD DATA` 导入数据，指定数据的分隔符为逗号，忽略包围数据的引号，并且忽略文件的第一行数据。

如果此时遇到 `ERROR 1148 (42000): the used command is not allowed with this TiDB version` 报错信息。可以参考文档解决：[ERROR 1148 (42000): the used command is not allowed with this TiDB version 问题的处理方法](/error-codes.md#mysql-原生报错汇总)

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```sql
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

`LOAD DATA` 也支持使用十六进制 ASCII 字符表达式或二进制 ASCII 字符表达式作为 `FIELDS ENCLOSED BY` 和 `FIELDS TERMINATED BY` 的参数。示例如下：

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

以上示例中 `x'2c'` 是字符 `,` 的十六进制表示，`b'100010'` 是字符 `"` 的二进制表示。

## MySQL 兼容性

TiDB 中的 `LOAD DATA` 语句语法上兼容 MySQL（除字符集选项被解析但会被忽略以外）。若发现任何语法兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

> **注意：**
>
> - 在 TiDB v4.0.0 之前的版本中，`LOAD DATA` 语句每 20000 行进行一次提交。
> - 从 TiDB v4.0.0 开始一直到 TiDB v6.6.0 的版本，TiDB 默认在一个事务中提交所有行。
> - 从 TiDB v7.0.0 开始，批量提交的行数由 `LOAD DATA` 语句的 `WITH batch_size=<number>` 参数控制，默认 1000 行提交一次。
> - 从 TiDB v4.0.0 及以前版本升级后，可能出现 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058` 错误。要解决该问题，建议调大 `tidb.toml` 文件中的 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 值。如果无法增加此限制，还可以将 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 的值设置为 `20000` 来恢复升级前的行为。
> - 无论以多少行为一个事务提交，`LOAD DATA` 都不会被显式事务中的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。
> - `LOAD DATA` 语句始终以乐观事务模式执行，不受 TiDB 事务模式设置的影响。

## 另请参阅

* [INSERT](/sql-statements/sql-statement-insert.md)
* [乐观事务模型](/optimistic-transaction.md)
* [悲观事务模式](/pessimistic-transaction.md)
* [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)
* [`SHOW LOAD DATA`](/sql-statements/sql-statement-show-load-data.md)
* [`CANCEL LOAD DATA` 和 `DROP LOAD DATA`](/sql-statements/sql-statement-operate-load-data-job.md)
