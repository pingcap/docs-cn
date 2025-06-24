---
title: LOAD DATA | TiDB SQL 语句参考
summary: TiDB 数据库中 LOAD DATA 的使用概览。
---

# LOAD DATA

`LOAD DATA` 语句用于批量将数据加载到 TiDB 表中。

从 TiDB v7.0.0 开始，`LOAD DATA` SQL 语句支持以下功能：

- 支持从 S3 和 GCS 导入数据
- 添加新参数 `FIELDS DEFINED NULL BY`

> **警告：**
>
> 新参数 `FIELDS DEFINED NULL BY` 以及从 S3 和 GCS 导入数据的支持是实验性功能。不建议在生产环境中使用。此功能可能会在没有预先通知的情况下发生变更或移除。如果发现 bug，你可以在 GitHub 上提交[问题](https://github.com/pingcap/tidb/issues)。

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 对于 `LOAD DATA INFILE` 语句，TiDB Cloud Dedicated 支持 `LOAD DATA LOCAL INFILE` 和从 Amazon S3 或 Google Cloud Storage 导入数据的 `LOAD DATA INFILE`，而 TiDB Cloud Serverless 仅支持 `LOAD DATA LOCAL INFILE`。

</CustomContent>

## 语法

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt

LocalOpt ::= ('LOCAL')?

Fields ::=
    ('TERMINATED' 'BY' stringLit
    | ('OPTIONALLY')? 'ENCLOSED' 'BY' stringLit
    | 'ESCAPED' 'BY' stringLit
    | 'DEFINED' 'NULL' 'BY' stringLit ('OPTIONALLY' 'ENCLOSED')?)?
```

## 参数

### `LOCAL`

你可以使用 `LOCAL` 来指定要导入的客户端上的数据文件，其中文件参数必须是客户端上的文件系统路径。

如果你使用 TiDB Cloud，要使用 `LOAD DATA` 语句加载本地数据文件，你需要在连接到 TiDB Cloud 时在连接字符串中添加 `--local-infile` 选项。

- 以下是 TiDB Cloud Serverless 的示例连接字符串：

    ```
    mysql --connect-timeout 15 -u '<user_name>' -h <host_name> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p<your_password> --local-infile
    ```

- 以下是 TiDB Cloud Dedicated 的示例连接字符串：

    ```
    mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_path> --tls-version="TLSv1.2" -u root -h <host_name> -P 4000 -D test -p<your_password> --local-infile
    ```

### S3 和 GCS 存储

<CustomContent platform="tidb">

如果不指定 `LOCAL`，文件参数必须是有效的 S3 或 GCS 路径，详见[外部存储](/br/backup-and-restore-storages.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果不指定 `LOCAL`，文件参数必须是有效的 S3 或 GCS 路径，详见[外部存储](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)。

</CustomContent>

当数据文件存储在 S3 或 GCS 上时，你可以导入单个文件或使用通配符 `*` 匹配多个要导入的文件。注意，通配符不会递归处理子目录中的文件。以下是一些示例：

- 导入单个文件：`s3://<bucket-name>/path/to/data/foo.csv`
- 导入指定路径下的所有文件：`s3://<bucket-name>/path/to/data/*`
- 导入指定路径下所有以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/*.csv`
- 导入指定路径下所有以 `foo` 开头的文件：`s3://<bucket-name>/path/to/data/foo*`
- 导入指定路径下所有以 `foo` 开头且以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/foo*.csv`

### `Fields`、`Lines` 和 `Ignore Lines`

你可以使用 `Fields` 和 `Lines` 参数来指定如何处理数据格式。

- `FIELDS TERMINATED BY`：指定数据分隔符。
- `FIELDS ENCLOSED BY`：指定数据的包围字符。
- `LINES TERMINATED BY`：指定行终止符，如果你想用某个字符结束一行。

你可以使用 `DEFINED NULL BY` 来指定在数据文件中如何表示 NULL 值。

- 与 MySQL 行为一致，如果 `ESCAPED BY` 不为空，例如使用默认值 `\`，则 `\N` 将被视为 NULL 值。
- 如果你使用 `DEFINED NULL BY`，例如 `DEFINED NULL BY 'my-null'`，则 `my-null` 被视为 NULL 值。
- 如果你使用 `DEFINED NULL BY ... OPTIONALLY ENCLOSED`，例如 `DEFINED NULL BY 'my-null' OPTIONALLY ENCLOSED`，则 `my-null` 和 `"my-null"`（假设 `ENCLOSED BY '"'`）被视为 NULL 值。
- 如果你不使用 `DEFINED NULL BY` 或 `DEFINED NULL BY ... OPTIONALLY ENCLOSED`，但使用 `ENCLOSED BY`，例如 `ENCLOSED BY '"'`，则 `NULL` 被视为 NULL 值。这种行为与 MySQL 一致。
- 在其他情况下，不被视为 NULL 值。

以下面的数据格式为例：

```
"bob","20","street 1"\r\n
"alice","33","street 1"\r\n
```

如果你想提取 `bob`、`20` 和 `street 1`，需要指定字段分隔符为 `','`，包围字符为 `'\"'`：

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

如果你不指定上述参数，导入的数据默认按以下方式处理：

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

你可以通过配置 `IGNORE <number> LINES` 参数来忽略文件的前 `number` 行。例如，如果你配置 `IGNORE 1 LINES`，文件的第一行将被忽略。

## 示例

以下示例使用 `LOAD DATA` 导入数据。指定逗号为字段分隔符。包围数据的双引号被忽略。文件的第一行被忽略。

<CustomContent platform="tidb">

如果你看到 `ERROR 1148 (42000): the used command is not allowed with this TiDB version`，请参考 [ERROR 1148 (42000): the used command is not allowed with this TiDB version](/error-codes.md#mysql-native-error-messages) 进行故障排除。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果你看到 `ERROR 1148 (42000): the used command is not allowed with this TiDB version`，请参考 [ERROR 1148 (42000): the used command is not allowed with this TiDB version](https://docs.pingcap.com/tidb/stable/error-codes#mysql-native-error-messages) 进行故障排除。

</CustomContent>

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```sql
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

`LOAD DATA` 还支持使用十六进制 ASCII 字符表达式或二进制 ASCII 字符表达式作为 `FIELDS ENCLOSED BY` 和 `FIELDS TERMINATED BY` 的参数。请参见以下示例：

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

在上面的示例中，`x'2c'` 是 `,` 字符的十六进制表示，`b'100010'` 是 `"` 字符的二进制表示。

<CustomContent platform="tidb-cloud">

以下示例展示如何使用 `LOAD DATA INFILE` 语句从 Amazon S3 将数据导入到 TiDB Cloud Dedicated 集群：

```sql
LOAD DATA INFILE 's3://<your-bucket-name>/your-file.csv?role_arn=<你为 TiDB Cloud 导入创建的 IAM 角色的 ARN>&external_id=<TiDB Cloud external ID（可选）>'
INTO TABLE <your-db-name>.<your-table-name>
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```

</CustomContent>

## MySQL 兼容性

`LOAD DATA` 语句的语法与 MySQL 兼容，但字符集选项会被解析但忽略。如果发现任何语法兼容性差异，你可以[报告问题](https://docs.pingcap.com/tidb/stable/support)。

<CustomContent platform="tidb">

> **注意：**
>
> - 对于 TiDB v4.0.0 之前的版本，`LOAD DATA` 每 20000 行提交一次，这个数值不可配置。
> - 对于 TiDB v4.0.0 到 v6.6.0 的版本，TiDB 默认在一个事务中提交所有行。但如果你需要 `LOAD DATA` 语句每固定行数提交一次，你可以将 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 设置为所需的行数。
> - 从 TiDB v7.0.0 开始，`tidb_dml_batch_size` 不再对 `LOAD DATA` 生效，TiDB 在一个事务中提交所有行。
> - 从 TiDB v4.0.0 或更早版本升级后，可能会出现 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058`。建议通过增加 `tidb.toml` 文件中的 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 值来解决此错误。
> - 对于 TiDB v7.6.0 之前的版本，无论在一个事务中提交多少行，`LOAD DATA` 都不会被显式事务中的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。
> - 对于 TiDB v7.6.0 之前的版本，`LOAD DATA` 语句始终在乐观事务模式下执行，不受 TiDB 事务模式配置的影响。
> - 从 v7.6.0 开始，TiDB 处理事务中的 `LOAD DATA` 的方式与其他 DML 语句相同：
>     - `LOAD DATA` 语句不会提交当前事务或开始新事务。
>     - `LOAD DATA` 语句受 TiDB 事务模式设置（乐观或悲观事务）的影响。
>     - 事务中的 `LOAD DATA` 语句可以被事务中的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 对于 TiDB v4.0.0 之前的版本，`LOAD DATA` 每 20000 行提交一次，这个数值不可配置。
> - 对于 TiDB v4.0.0 到 v6.6.0 的版本，TiDB 默认在一个事务中提交所有行。但如果你需要 `LOAD DATA` 语句每固定行数提交一次，你可以将 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 设置为所需的行数。
> - 从 v7.0.0 开始，`tidb_dml_batch_size` 不再对 `LOAD DATA` 生效，TiDB 在一个事务中提交所有行。
> - 从 TiDB v4.0.0 或更早版本升级后，可能会出现 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058`。要解决此错误，你可以联系 [TiDB Cloud 支持团队](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)以增加 [`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) 值。
> - 对于 TiDB v7.6.0 之前的版本，无论在一个事务中提交多少行，`LOAD DATA` 都不会被显式事务中的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。
> - 对于 TiDB v7.6.0 之前的版本，`LOAD DATA` 语句始终在乐观事务模式下执行，不受 TiDB 事务模式配置的影响。
> - 从 v7.6.0 开始，TiDB 处理事务中的 `LOAD DATA` 的方式与其他 DML 语句相同：
>     - `LOAD DATA` 语句不会提交当前事务或开始新事务。
>     - `LOAD DATA` 语句受 TiDB 事务模式设置（乐观或悲观事务）的影响。
>     - 事务中的 `LOAD DATA` 语句可以被事务中的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。

</CustomContent>

## 另请参阅

<CustomContent platform="tidb">

* [INSERT](/sql-statements/sql-statement-insert.md)
* [TiDB 乐观事务模型](/optimistic-transaction.md)
* [TiDB 悲观事务模式](/pessimistic-transaction.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

* [INSERT](/sql-statements/sql-statement-insert.md)
* [TiDB 乐观事务模型](/optimistic-transaction.md)
* [TiDB 悲观事务模式](/pessimistic-transaction.md)

</CustomContent>
