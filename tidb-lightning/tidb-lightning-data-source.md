---
title: TiDB Lightning 数据源
summary: 了解 TiDB Lightning 支持的各类型数据源。
aliases: ['/zh/tidb/dev/migrate-from-csv-using-tidb-lightning/','/docs-cn/dev/tidb-lightning/migrate-from-csv-using-tidb-lightning/','/docs-cn/dev/reference/tools/tidb-lightning/csv/']
---

# TiDB Lightning 数据源

TiDB Lightning 支持从多种类型的文件导入数据到 TiDB 集群。通过以下配置为 Lightning 指定数据文件所在位置。

```toml
[mydumper]
# 本地源数据目录或 S3 等外部存储 URL
data-source-dir = "/data/my_database"
```

Lightning 运行时将查找 `data-source-dir` 中所有符合命令规则的文件。

| 文件类型 | 分类 | 命名规则 |
|:--|:--|:---|
|Schema 文件|包含 DDL 语句 `CREATE TABLE` 的文件|`${db_name}.${table_name}-schema.sql`|
|Schema 文件|包含 `CREATE DATABASE` DDL 语句的文件|`${db_name}-schema-create.sql`|
|数据文件|包含整张表的数据文件，该文件会被导入 `${db_name}.${table_name}` 表 | `${db_name}.${table_name}.${csv|sql|parquet}`|
|数据文件| 如果一个表分布于多个数据文件，这些文件命名需加上文件编号的后缀 | `${db_name}.${table_name}.001.${csv|sql|parquet}` |

Lightning 尽量并行处理数据，由于文件必须顺序读取，所以数据处理协程是文件级别的并发（通过 `region-concurrency` 配置控制）。因此导入大文件时性能比较差。通常建议单个文件尺寸为 256MiB，以获得最好的性能。

## CSV

### 表结构

CSV 文件是没有表结构的。要导入 TiDB，就必须为其提供表结构。可以通过以下任一方法实现：

* 创建包含 DDL 语句的 `${db_name}.${table_name}-schema.sql` 和 `${db_name}-schema-create.sql`。
* 在 TiDB 中手动创建。

### 配置

CSV 格式可在 `tidb-lightning.toml` 文件中 `[mydumper.csv]` 下配置。大部分设置项在 MySQL [`LOAD DATA`] 语句中都有对应的项目。

```toml
[mydumper.csv]
# 字段分隔符，支持一个或多个字符，默认值为 ','。如果数据中可能有逗号，建议源文件导出时分隔符使用非常见组合字符例如'|+|'。
separator = ','
# 引用定界符，设置为空表示字符串未加引号。
delimiter = '"'
# 行尾定界字符，支持一个或多个字符。设置为空（默认值）表示 "\n"（换行）和 "\r\n" （回车+换行），均表示行尾。
terminator = ""
# CSV 文件是否包含表头。
# 如果为 true，首行将会被跳过，且基于首行映射目标表的列。
header = true
# CSV 是否包含 NULL。
# 如果为 true，CSV 文件的任何列都不能解析为 NULL。
not-null = false
# 如果 `not-null` 为 false（即 CSV 可以包含 NULL），
# 为以下值的字段将会被解析为 NULL。
null = '\N'
# 是否解析字段内的反斜线转义符。
backslash-escape = true
# 是否移除以分隔符结束的行。
trim-last-separator = false
```

对于诸如 `separator`，`delimiter` 和 `terminator` 等取值为字符串的配置项，如果需要设置的字符串中包含特殊字符，可以通过使用反斜杠 `\` 转义的方式进行输入，输入的转义序列必须被包含在一对*双引号* `"` 之间。例如，设置 `separator = "\u001f"` 表示使用 ASCII 字符 0X1F 作为字符串定界符。

你也可以使用*单引号*字符串 `'...'` 禁止对字符进行转义。

另外，设置 `separator = '\n'` 表示使用两个字符 `\` + `n` 作为字符串定界符，而不是转义后的换行符 `\n`。

更多详细的内容请参考 [TOML v1.0.0 标准](https://toml.io/cn/v1.0.0#%E5%AD%97%E7%AC%A6%E4%B8%B2)。

#### `separator`

- 指定字段分隔符。
- 可以为一个或多个字符，不能为空。
- 常用值：

    * CSV 用 `','`
    * TSV 用 `"\t"`
    * "\u0001" 表示使用 ASCII 字符 0x01

- 对应 LOAD DATA 语句中的 `FIELDS TERMINATED BY` 项。

#### `delimiter`

- 指定引用定界符。
- 如果 `delimiter` 为空，所有字段都会被取消引用。
- 常用值：

    * `'"'` 使用双引号引用字段，和 [RFC 4180] 一致。
    * `''` 不引用

- 对应 LOAD DATA 语句中的 `FIELDS ENCLOSED BY` 项。

参考 [RFC 4180](https://tools.ietf.org/html/rfc4180)。

#### `terminator`

- 指定行尾定界符。
- 如果 `terminator` 为空，则 "\\n"（换行）和 "\\r\\n" （回车+换行）均表示行尾。
- 对应 LOAD DATA 语句中的 `LINES TERMINATED BY` 项。

#### `header`

- 是否*所有* CSV 文件都包含表头行。
- 如为 true，第一行会被用作*列名*。如为 false，第一行并无特殊性，按普通的数据行处理。

#### `not-null` 和 `null`

- `not-null` 决定是否所有字段不能为空。
- 如果 `not-null` 为 false，设定了 `null` 的字符串会被转换为 SQL NULL 而非具体数值。
- 引用不影响字段是否为空。

    例如有如下 CSV 文件：

    ```csv
    A,B,C
    \N,"\N",
    ```

    在默认设置（`not-null = false; null = '\N'`）下，列 `A` and `B` 导入 TiDB 后都将会转换为 NULL。列 `C` 是空字符串 `''`，但并不会解析为 NULL。

#### `backslash-escape`

- 是否解析字段内的反斜线转义符。
- 如果 `backslash-escape` 为 true，下列转义符会被识别并转换。

    | 转义符   | 转换为            |
    |----------|--------------------------|
    | `\0`     | 空字符 (U+0000)  |
    | `\b`     | 退格 (U+0008)       |
    | `\n`     | 换行 (U+000A)       |
    | `\r`     | 回车 (U+000D) |
    | `\t`     | 制表符 (U+0009)             |
    | `\Z`     | Windows EOF (U+001A)     |

    其他情况下（如 `\"`）反斜线会被移除，仅在字段中保留其后面的字符（`"`），这种情况下，保留的字符仅作为普通字符，特殊功能（如界定符）都会失效。

- 引用不会影响反斜线转义符的解析与否。

- 对应 LOAD DATA 语句中的 `FIELDS ESCAPED BY '\'` 项。

#### `trim-last-separator`

- 将 `separator` 字段当作终止符，并移除尾部所有分隔符。

    例如有如下 CSV 文件：

    ```csv
    A,,B,,
    ```

- 当 `trim-last-separator = false`，该文件会被解析为包含 5 个字段的行 `('A', '', 'B', '', '')`。
- 当 `trim-last-separator = true`，该文件会被解析为包含 3 个字段的行 `('A', '', 'B')`。
- 此配置项已被弃用，建议使用兼容性更好的 `terminator`。

    如果有如下旧的配置：

    ```toml
    separator = ','
    trim-last-separator = true
    ```

    建议修改为：

    ```toml
    separator = ','
    terminator = ",\n" # 请根据文件实际使用的换行符指定为 ",\n" 或 ",\r\n"
    ```

#### 不可配置项

TiDB Lightning 并不完全支持 `LOAD DATA` 语句中的所有配置项。例如：

* 不可使用行前缀 (`LINES STARTING BY`)。
* 不可跳过表头 (`IGNORE n LINES`)。如有表头，必须是有效的列名。

### 启用严格格式

导入文件的大小统一约为 256 MB 时，TiDB Lightning 可达到最佳工作状态。如果导入单个 CSV 大文件，TiDB Lightning 只能使用一个线程来处理，这会降低导入速度。

要解决此问题，可先将 CSV 文件分割为多个文件。对于通用格式的 CSV 文件，在没有读取整个文件的情况下无法快速确定行的开始和结束位置。因此，默认情况下 TiDB Lightning 不会自动分割 CSV 文件。但如果你确定待导入的 CSV 文件符合特定的限制要求，则可以启用 `strict-format` 设置。启用后，TiDB Lightning 会将单个 CSV 大文件分割为单个大小为 256 MB 的多个文件块进行并行处理。

```toml
[mydumper]
strict-format = true
```

严格格式的 CSV 文件中，每个字段仅占一行，即必须满足以下条件之一：

* delimiter 为空；
* 每个字段不包含 `terminator` 对应的字符串。在默认配置下，对应每个字段不包含 CR (`\r`）或 LF（`\n`）。

如果 CSV 文件不是严格格式但 `strict-format` 被误设为 `true`，跨多行的单个完整字段会被分割成两部分，导致解析失败，甚至不报错地导入已损坏的数据。

### 常见配置示例

#### CSV

默认设置已按照 RFC 4180 调整。

```toml
[mydumper.csv]
separator = ',' # 如果数据中可能有逗号，建议源文件导出时分隔符使用非常见组合字符例如'|+|'
delimiter = '"'
header = true
not-null = false
null = '\N'
backslash-escape = true
```

示例内容：

```
ID,Region,Count
1,"East",32
2,"South",\N
3,"West",10
4,"North",39
```

#### TSV

```toml
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
```

示例内容：

```
ID    Region    Count
1     East      32
2     South     NULL
3     West      10
4     North     39
```

#### TPC-H DBGEN

```toml
[mydumper.csv]
separator = '|'
delimiter = ''
terminator = "|\n"
header = false
not-null = true
backslash-escape = false
```

示例内容：

```
1|East|32|
2|South|0|
3|West|10|
4|North|39|
```

## SQL

Lightning 在处理 SQL 文件时，由于无法对单个文件进行快速分割，因此无法通过增加并发提高单个文件的导入速度。鉴于此，导出数据为 SQL 文件时应尽量避免单个 SQL 文件过大，通常单文件在 256MiB 左右可以达到最佳性能。

## Parquet

Lightning 目前仅支持由 Amazon Aurora 导出快照生成的 Parquet 文件。要识别其在 S3 的文件组织形式，需要使用如下配置匹配到所有的数据文件：

```
[[mydumper.files]]
# 解析 AWS Aurora parquet 文件所需的表达式
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

注意，此处仅说明 Aurora snapshot 导出的 parquet 文件如何匹配。Schema 文件需要单独导出及处理。

关于 `mydumper.files`，请参考[自定义文件匹配](/tidb-lightning/tidb-lightning-data-source.md#自定义文件匹配)。

## 自定义文件匹配

Lightning 仅识别符合命名要求的数据文件，但在某些情况下已提供的数据文件并不符合要求，因此可能出现 Lightning 在极短的时间结束，处理文件数量为 0 的情况。

为了解决此类问题，Lightning 提供了 `[[mydumper.files]]` 配置用于通过自定义表达式匹配数据文件。

以 AWS Aurora 导出至 S3 的快照文件为例，Parquet 文件的完整路径为：`S3://some-bucket/some-subdir/some-database/some-database.some-table/part-00000-c5a881bb-58ff-4ee6-1111-b41ecff340a3-c000.gz.parquet`。

通常 `data-source-dir` 会被配置为`S3://some-bucket/some-subdir/some-database/` 以导入 `some-database` 库。

根据上述 Parquet 文件的路径，你可以编写正则表达式 `(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$`，得到的 match group 中 index=1 的内容为 `some-database` ，index=2 的内容为 `some-table`，index=3 的内容为 `parquet`。

根据上述正则表达式及相应的 index 编写配置文件，Lightning 即可识别非默认命名规则的文件，最终实际配置如下：

```
[[mydumper.files]]
# 解析 AWS Aurora parquet 文件所需的表达式
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

- **schema**：目标库名称，值可以为：
    - 正则表达式匹配到的 group 序号，例如 “$1”。
    - 直接填写期望导入的库名，例如 “db1”。所有匹配到的文件均会导入 “db1”。
- **table**：目标表名称，值可以为：
    - 正则表达式匹配到的 group 序号，例如 “$2”。
    - 直接填写期望导入的库名，例如“table1”。所有匹配到的文件均会导入“table1”。
- **type**：文件类型，支持`sql`，`parquet`，`csv`，值可以为：
    - 正则表达式匹配到的 group 序号，例如 “$3”。
- **key**：文件的序号，即前文所述`${db_name}.${table_name}.001.csv`中的`001`。
    - 正则表达式匹配到的 group 序号，例如 “$4”。

## 更多

- [使用 Dumpling 导出到 CSV 文件](/dumpling-overview.md#导出为-csv-文件)
- [`LOAD DATA`](https://dev.mysql.com/doc/refman/8.0/en/load-data.html)