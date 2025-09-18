---
title: LOAD DATA
summary: TiDB 数据库中 LOAD DATA 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-load-data/','/docs-cn/dev/reference/sql/statements/load-data/','/zh/tidb/dev/sql-statement-operate-load-data-job','/zh/tidb/dev/sql-statement-show-load-data']
---

# LOAD DATA

`LOAD DATA` 语句用于将数据批量加载到 TiDB 表中。

在 v7.0.0 版本支持以下功能：

- 支持从 S3、GCS 导入数据
- 新增参数 `FIELDS DEFINED NULL BY`

> **警告：**
>
> v7.0.0 新增支持从 S3、GCS 导入数据和 `FIELDS DEFINED NULL BY` 参数为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 语法图

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt

LocalOpt ::= ('LOCAL')?

DuplicateOpt ::=
    ( 'IGNORE' | 'REPLACE' )?

Fields ::=
    ('TERMINATED' 'BY' stringLit
    | ('OPTIONALLY')? 'ENCLOSED' 'BY' stringLit
    | 'ESCAPED' 'BY' stringLit
    | 'DEFINED' 'NULL' 'BY' stringLit ('OPTIONALLY' 'ENCLOSED')?)?
```

## 参数说明

### `LOCAL`

你可以使用 `LOCAL` 来指定导入位于客户端的数据文件，此时传入文件参数必须为客户端文件系统路径。

### `REPLACE` 和 `IGNORE`

你可以使用 `REPLACE` 和 `IGNORE` 参数来指定遇到重复数据时的处理方式。

- `REPLACE`：遇到重复数据时，覆盖现有数据。
- `IGNORE`：遇到重复数据时，忽略新导入的行，保留已存在的数据。

默认情况下，遇到重复数据会报错。

### S3/GCS 路径

如果你不指定 `LOCAL`，则文件参数必须是有效的 S3/GCS URI 路径，详见[外部存储](/br/backup-and-restore-storages.md)。

当数据文件存储在 S3/GCS 上时，你可以导入单个文件，也可使用通配符 `*` 来匹配需要导入的多个文件。注意通配符不会递归处理子目录下相关的文件。以数据存储在 S3 为例，示例如下:

- 导入单个文件：`s3://<bucket-name>/path/to/data/foo.csv`
- 导入指定路径下的所有文件：`s3://<bucket-name>/path/to/data/*`
- 导入指定路径下的所有以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/*.csv`
- 导入指定路径下所有以 `foo` 为前缀的文件：`s3://<bucket-name>/path/to/data/foo*`
- 导入指定路径下以 `foo` 为前缀、以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/foo*.csv`

### `Fields`、`Lines`、`Ignore Lines`

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

当不指定处理数据的参数时，将按以下参数处理：

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

你可以通过 `IGNORE <number> LINES` 参数来忽略文件开始的 `<number>` 行。例如，可以使用 `IGNORE 1 LINES` 来忽略文件的第一行。

## 示例

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

TiDB 中的 `LOAD DATA` 语句语法上兼容 MySQL（除字符集选项被解析但会被忽略以外）。若发现任何语法兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

> **注意：**
>
> - 在 TiDB v4.0.0 之前的版本中，`LOAD DATA` 语句每 20000 行进行一次提交。该行数不支持更改。
> - 从 TiDB v4.0.0 开始一直到 TiDB v6.6.0 的版本，TiDB 默认在一个事务中提交所有行。如需 `LOAD DATA` 语句按照每固定的行数进行一次提交，可以设置 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 为所需的行数。
> - 从 TiDB v7.0.0 起，`tidb_dml_batch_size` 对 `LOAD DATA` 语句不再生效，TiDB 将在一个事务中提交所有行。
> - 从 TiDB v4.0.0 及以前版本升级后，可能出现 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058` 错误。要解决该问题，建议调大 `tidb.toml` 文件中的 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 值。
> - 在 TiDB v7.6.0 之前的版本中，无论以多少行为一个事务提交，`LOAD DATA` 都不会被显式事务中的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。
> - 在 TiDB v7.6.0 之前的版本中，`LOAD DATA` 语句始终以乐观事务模式执行，不受 TiDB 事务模式设置的影响。
> - 从 TiDB v7.6.0 开始，`LOAD DATA` 在事务中与其它普通 DML 的处理方式一致：
>     - `LOAD DATA` 语句本身不会提交当前事务，也不会开启新事务。
>     - `LOAD DATA` 语句会受 TiDB 事务模式设置（乐观/悲观）影响。
>     - 事务内的 `LOAD DATA` 语句可以被事务的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。

## 另请参阅

* [INSERT](/sql-statements/sql-statement-insert.md)
* [乐观事务模型](/optimistic-transaction.md)
* [悲观事务模式](/pessimistic-transaction.md)
