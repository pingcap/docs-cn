---
title: CSV 支持
aliases: ['/docs-cn/dev/tidb-lightning/migrate-from-csv-using-tidb-lightning/','/docs-cn/dev/reference/tools/tidb-lightning/csv/']
---

本文介绍如何使用 TiDB Lightning 从 CSV 文件迁移数据到 TiDB。关于如何从 MySQL 生成 CSV 文件，可以参考[使用 Dumpling 导出到 CSV 文件](/dumpling-overview.md#导出到-csv-文件)。

# CSV 支持与限制

TiDB Lightning 支持读取 CSV（逗号分隔值）的数据源，以及其他定界符格式如 TSV（制表符分隔值）。

## 文件名

包含整张表的 CSV 文件需命名为 `db_name.table_name.csv`，该文件会被解析为数据库 `db_name` 里名为 `table_name` 的表。

如果一个表分布于多个 CSV 文件，这些 CSV 文件命名需加上文件编号的后缀，如 `db_name.table_name.003.csv`。数字部分不需要连续但必须递增，并用零填充。

文件扩展名必须为 `*.csv`，即使文件的内容并非逗号分隔。

## 表结构

CSV 文件是没有表结构的。要导入 TiDB，就必须为其提供表结构。可以通过以下任一方法实现：

* 创建包含 DDL 语句 `CREATE TABLE` 的文件 `db_name.table_name-schema.sql` 以及包含 `CREATE DATABASE` DDL 语句的文件 `db_name-schema-create.sql`。
* 首先在 TiDB 中直接创建空表，然后在 `tidb-lightning.toml` 中设置 `[mydumper] no-schema = true`。

## 配置

CSV 格式可在 `tidb-lightning.toml` 文件中 `[mydumper.csv]` 下配置。大部分设置项在 MySQL [`LOAD DATA`] 语句中都有对应的项目。

```toml
[mydumper.csv]
# 字段分隔符，必须为 ASCII 字符。
separator = ','
# 引用定界符，可以为 ASCII 字符或空字符。
delimiter = '"'
# CSV 文件是否包含表头。
# 如果为 true，首行将会被跳过。
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

[`LOAD DATA`]: https://dev.mysql.com/doc/refman/8.0/en/load-data.html

### `separator`

- 指定字段分隔符。
- 必须为单个 ASCII 字符。
- 常用值：

    * CSV 用 `','`
    * TSV 用 `"\t"`

- 对应 LOAD DATA 语句中的 `FIELDS TERMINATED BY` 项。

### `delimiter`

- 指定引用定界符。
- 如果 `delimiter` 为空，所有字段都会被取消引用。
- 常用值：

    * `'"'` 使用双引号引用字段，和 [RFC 4180] 一致。
    * `''` 不引用

- 对应 LOAD DATA 语句中的 `FIELDS ENCLOSED BY` 项。

[RFC 4180]: https://tools.ietf.org/html/rfc4180

### `header`

- 是否*所有* CSV 文件都包含表头行。
- 如为 true，第一行会被用作*列名*。如为 false，第一行并无特殊性，按普通的数据行处理。

### `not-null` 和 `null`

- `not-null` 决定是否所有字段不能为空。
- 如果 `not-null` 为 false，设定了 `null` 的字符串会被转换为 SQL NULL 而非具体数值。
- 引用不影响字段是否为空。

    例如有如下 CSV 文件：

    ```csv
    A,B,C
    \N,"\N",
    ```

    在默认设置（`not-null = false; null = '\N'`）下，列 `A` and `B` 导入 TiDB 后都将会转换为 NULL。列 `C` 是空字符串 `''`，但并不会解析为 NULL。

### `backslash-escape`

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

### `trim-last-separator`

- 将 `separator` 字段当作终止符，并移除尾部所有分隔符。

    例如有如下 CSV 文件：

    ```csv
    A,,B,,
    ```

- 当 `trim-last-separator = false`，该文件会被解析为包含 5 个字段的行 `('A', '', 'B', '', '')`。
- 当 `trim-last-separator = true`，该文件会被解析为包含 3 个字段的行 `('A', '', 'B')`。

### 不可配置项

TiDB Lightning 并不完全支持 `LOAD DATA` 语句中的所有配置项。例如：

* 行终止符只能是 CR（`\r`），LF（`\n`）或 CRLF（`\r\n`），也就是说，无法自定义 `LINES TERMINATED BY`。
* 不可使用行前缀 （`LINES STARTING BY`）。
* 不可跳过表头（`IGNORE n LINES`）。如有表头，必须是有效的列名。
* 定界符和分隔符只能为单个 ASCII 字符。

## 设置 `strict-format` 启用严格格式

导入文件的大小统一约为 256 MB 时，TiDB Lightning 可达到最佳工作状态。如果导入单个 CSV 大文件，TiDB Lightning 只能使用一个线程来处理，这会降低导入速度。

要解决此问题，可先将 CSV 文件分割为多个文件。对于通用格式的 CSV 文件，在没有读取整个文件的情况下无法快速确定行的开始和结束位置。因此，默认情况下 TiDB Lightning 不会自动分割 CSV 文件。但如果你确定待导入的 CSV 文件符合特定的限制要求，则可以启用 `strict-format` 设置。启用后，TiDB Lightning 会将单个 CSV 大文件分割为单个大小为 256 MB 的多个文件块进行并行处理。

```toml
[mydumper]
strict-format = true
```

严格格式的 CSV 文件中，每个字段仅占一行，即必须满足以下条件之一：

* 分隔符为空；
* 每个字段不包含 CR (`\r`）或 LF（`\n`）。

如果 CSV 文件不是严格格式但 `strict-format` 被误设为 `true`，跨多行的单个完整字段会被分割成两部分，导致解析失败，甚至不报错地导入已损坏的数据。

## 通用配置

### CSV

默认设置已按照 RFC 4180 调整。

```toml
[mydumper.csv]
separator = ','
delimiter = '"'
header = true
not-null = false
null = '\N'
backslash-escape = true
trim-last-separator = false
```

示例内容：

```
ID,Region,Count
1,"East",32
2,"South",\N
3,"West",10
4,"North",39
```

### TSV

```toml
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
trim-last-separator = false
```

示例内容：

```
ID    Region    Count
1     East      32
2     South     NULL
3     West      10
4     North     39
```

### TPC-H DBGEN

```toml
[mydumper.csv]
separator = '|'
delimiter = ''
header = false
not-null = true
backslash-escape = false
trim-last-separator = true
```

示例内容：

```
1|East|32|
2|South|0|
3|West|10|
4|North|39|
```
