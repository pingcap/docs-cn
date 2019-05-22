---
title: CSV 支持
category: reference
aliases: ['/docs-cn/tools/lightning/csv/']
---

# CSV 支持

TiDB-Lightning 支持读取 CSV（逗号分隔值）的数据源，以及其他定界符格式如 TSV（制表符分隔值）。

## 文件名

包含整张表的 CSV 文件需命名为 `db_name.table_name.csv`，该文件会被解析为数据库 `db_name` 里名为 `table_name` 的表。

如果一个表分布于多个 CSV 文件，这些 CSV 文件命名需加上文件编号的后缀，如 `db_name.table_name.003.csv`。

文件扩展名必须为 `*.csv`，即使文件的内容并非逗号分隔。

## 表结构 

CSV 文件是没有表结构的。要导入 TiDB，就必须为其提供表结构。可以通过以下任一方法实现：

* 创建包含 DDL 语句 `CREATE TABLE` 的文件 `db_name.table_name-schema.sql`。
* 首先在 TiDB 中直接创建空表，然后在 `tidb-lightning.toml` 中设置 `[mydumper] no-schema = true`。

## 配置

CSV 格式可在 `tidb-lightning.toml` 文件中 `[mydumper.csv]` 下配置。
大部分设置项在 MySQL [`LOAD DATA`] 语句中都有对应的项目。

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

    其他情况下（如 `\"`）反斜线会被移除，仅在字段中保留其后面的字符（`"`）。

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

Lightning 并不完全支持 `LOAD DATA` 语句中的所有配置项。例如：

* 行终止符只能是 CR（`\r`），LF（`\n`）或 CRLF（`\r\n`），也就是说，无法自定义 `LINES TERMINATED BY`。
* 不可使用行前缀 （`LINES STARTING BY`）。
* 不可跳过表头（`IGNORE n LINES`）。如有表头，必须是有效的列名。
* 定界符和分隔符只能为单个 ASCII 字符。 

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
