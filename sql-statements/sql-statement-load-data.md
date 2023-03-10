---
title: LOAD DATA
summary: TiDB 数据库中 LOAD DATA 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-load-data/','/docs-cn/dev/reference/sql/statements/load-data/']
---

# LOAD DATA

`LOAD DATA` 语句用于将数据批量加载到 TiDB 表中。

## 语法图

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit FormatOpt DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt LoadDataOptionListOpt

LocalOpt ::= ('LOCAL')?

FormatOpt ::=
    ('FORMAT' ('DELIMITED FILE' | 'SQL FILE' | 'PARQUET'))?

Fields ::=
    ('TERMINATED' 'BY' stringLit
    | ('OPTIONALLY')? 'ENCLOSED' 'BY' stringLit
    | 'ESCAPED' 'BY' stringLit
    | 'DEFINED' 'NULL' 'BY' stringLit ('OPTIONALLY' 'ENCLOSED')?)?

LoadDataOptionListOpt ::=
    ('WITH' detached)?
```

## 参数说明

用户可以使用 `LOCAL` 来指定导入的数据文件位于客户端，此时传入文件参数必须为客户的文件路径。当用户不指定 `LOCAL` 时，文件参数可以是存放在服务器端的文件，此时该参数为磁盘文件路径；也可以是存储在 `S3` 上的文件。

当数据文件存储在 `S3` 上时，用户可以导入单个文件，也可使用通配符 `*` 指定需要导入的多个文件，实例如下
- 导入单个文件: `s3://<bucket-name>/path/to/data/foo.csv`.
- 导入指定目录下的所有文件: `s3://<bucket-name>/path/to/data/*`.
- 导入指定路径下的所有以 `.csv`结尾的文件: `s3://<bucket-name>/path/to/data/*.csv`.
- 导入指定路径下所有以 `foo` 为前缀的文件: `s3://<bucket-name>/path/to/data/foo*`.
- 导入指定路径下以 `foo` 开头，以 `.csv`结尾的文件: `s3://<bucket-name>/path/to/data/foo*.csv`.

用户可以通过 `FormatOpt` 参数来指定数据文件的格式，当不指定该语句时格式为 `DELIMITED DATA`，该格式即 MySQL `LOAD DATA` 支持的数据格式。当数据格式不为 `DELIMITED DATA` 时，不能指定 `Fields` `Lines` `IgnoreLines` 等语句。

当数据格式为 `TSV` 时，用户可以使用 `Fields` 和 `Lines` 参数来指定如何处理数据格式，使用 `FIELDS TERMINATED BY` 来指定每个数据的分隔符号，使用 `FIELDS ENCLOSED BY` 来指定消除数据的包围符号。如果用户希望以某个字符为结尾切分每行数据，可以使用 `LINES TERMINATED BY` 来指定行的终止符，可以使用 `DEFINED NULL BY` 来指定数据文件中如何表示 NULL 值。

例如对于以下格式的数据：

```
"bob","20","street 1"\r\n
"alice","33","street 1"\r\n
```

如果想分别提取 `bob`、`20`、`street 1`，可以指定数据的分隔符号为 `','`，数据的包围符号为 `'\"'`。可以写成：

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

当数据格式为 `DELIMITED DATA`，且不指定处理数据的参数，将会按以下参数处理

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

用户可以通过 `IGNORE number LINES` 参数来忽略文件开始的 `number` 行，例如可以使用 `IGNORE 1 LINES` 来忽略文件的首行。

当用户不指定 `LocalOpt` 参数时，用户可以通过 `WITH detached` 来让 `LOAD DATA` 在后台运行，用户可通过 [SHOW LOAD DATA](/sql-statements/sql-statement-show-load-data.md) 查看创建的 JOB，也可以使用 [OPERATE LOAD DATA JOB](/sql-statements/sql-statement-operate-load-data-job.md) 来取消或删除创建的 JOB。

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE trips (
    trip_id bigint NOT NULL PRIMARY KEY AUTO_INCREMENT,
    duration integer not null,
    start_date datetime,
    end_date datetime,
    start_station_number integer,
    start_station varchar(255),
    end_station_number integer,
    end_station varchar(255),
    bike_number varchar(255),
    member_type varchar(255)
    );
```

```
Query OK, 0 rows affected (0.14 sec)
```

通过 `LOAD DATA` 导入数据，指定数据的分隔符为逗号，忽略包围数据的引号，并且忽略文件的第一行数据。

如果此时遇到 `ERROR 1148 (42000): the used command is not allowed with this TiDB version` 报错信息。可以参考以下文档解决：

[ERROR 1148 (42000): the used command is not allowed with this TiDB version 问题的处理方法](/error-codes.md#mysql-原生报错汇总)

{{< copyable "sql" >}}

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

`LOAD DATA` 也支持使用十六进制 ASCII 字符表达式或二进制 ASCII 字符表达式作为 `FIELDS ENCLOSED BY` 和 `FIELDS TERMINATED BY` 的参数。示例如下：

{{< copyable "sql" >}}

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

以上示例中 `x'2c'` 是字符 `,` 的十六进制表示，`b'100010'` 是字符 `"` 的二进制表示。

## MySQL 兼容性

TiDB 中的 `LOAD DATA` 语句应该完全兼容 MySQL（除字符集选项被解析但会被忽略以外）。若发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

> **注意：**
>
> 在 TiDB 的早期版本中，`LOAD DATA` 语句每 20000 行进行一次提交。新版本的 TiDB 默认在一个事务中提交所有行。从 TiDB 4.0 及以前版本升级后，可能出现 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058` 错误。
>
> 要解决该问题，建议调大 `tidb.toml` 文件中的 `txn-total-size-limit` 值。如果无法增加此限制，还可以将 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 的值设置为 `20000` 来恢复升级前的行为。

## 另请参阅

* [INSERT](/sql-statements/sql-statement-insert.md)
* [乐观事务模型](/optimistic-transaction.md)
* [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)
* [SHOW LOAD DATA](/sql-statements/sql-statement-show-load-data.md)
* [OPERATE LOAD DATA JOB](/sql-statements/sql-statement-operate-load-data-job.md)