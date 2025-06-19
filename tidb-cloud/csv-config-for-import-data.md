---
title: 导入数据的 CSV 配置
summary: 了解如何在 TiDB Cloud 上使用导入数据服务的 CSV 配置。
---

# 导入数据的 CSV 配置

本文档介绍 TiDB Cloud 上导入数据服务的 CSV 配置。

以下是在 TiDB Cloud 上使用导入数据服务导入 CSV 文件时的 CSV 配置窗口。更多信息，请参见[从云存储导入 CSV 文件到 TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md)。

![CSV 配置](/media/tidb-cloud/import-data-csv-config.png)

## 分隔符（Separator）

- 定义：定义字段分隔符。可以是一个或多个字符，但不能为空。

- 常用值：

    * `,` 用于 CSV（逗号分隔值）。如上图所示，"1"、"Michael" 和 "male" 代表三个字段。
    * `"\t"` 用于 TSV（制表符分隔值）。

- 默认值：`,`

## 定界符（Delimiter）

- 定义：定义用于引用的定界符。如果**定界符**为空，则所有字段都不带引号。

- 常用值：

    * `'"'` 使用双引号引用字段。如上图所示，`"Michael","male"` 代表两个字段。注意两个字段之间必须有 `,`。如果数据是 `"Michael""male"`（没有 `,`），导入任务将无法解析。如果数据是 `"Michael,male"`（只有一个双引号），它将被解析为一个字段。
    * `''` 禁用引用。

- 默认值：`"`

## 反斜杠转义（Backslash escape）

- 定义：是否将字段内的反斜杠解析为转义字符。如果**反斜杠转义**为 `True`，则识别并转换以下序列：

    | 序列 | 转换为             |
    |----------|--------------------------|
    | `\0`     | 空字符 (`U+0000`)  |
    | `\b`     | 退格 (`U+0008`)       |
    | `\n`     | 换行 (`U+000A`)       |
    | `\r`     | 回车 (`U+000D`) |
    | `\t`     | 制表符 (`U+0009`)             |
    | `\Z`     | Windows EOF (`U+001A`)     |

    在所有其他情况下（例如，`\"`），反斜杠会被去除，只留下下一个字符（`"`）在字段中。剩下的字符没有特殊作用（例如，定界符），只是一个普通字符。引用不影响反斜杠是否被解析为转义字符。

    以下面的字段为例：

    - 如果值为 `True`，`"nick name is \"Mike\""` 将被解析为 `nick name is "Mike"` 并写入目标表。
    - 如果值为 `False`，它将被解析为三个字段：`"nick name is \"` 、`Mike\` 和 `""`。但由于字段之间没有分隔，无法正确解析。

    对于标准的 CSV 文件，如果要记录的字段中有双引号字符，需要使用两个双引号进行转义。在这种情况下，使用 `Backslash escape = True` 会导致解析错误，而使用 `Backslash escape = False` 则可以正确解析。一个典型的场景是导入的字段包含 JSON 内容。标准的 CSV JSON 字段通常存储如下：

    `"{""key1"":""val1"", ""key2"": ""val2""}"`

    在这种情况下，你可以设置 `Backslash escape = False`，字段将被正确转义并存储到数据库中，如下所示：

    `{"key1": "val1", "key2": "val2"}`

    如果 CSV 源文件的内容以以下方式保存为 JSON，则考虑设置 `Backslash escape = True`。但这不是 CSV 的标准格式。

    `"{\"key1\": \"val1\", \"key2\":\"val2\" }"`

- 默认值：`True`

## 空值（NULL value）

- 定义：定义 CSV 文件中表示 `NULL` 值的字符串。

- 默认值：`\N`

- 控制台不支持自定义空值。你可以使用 [TiDB Cloud CLI](/tidb-cloud/get-started-with-cli.md) 代替。更多信息，请参见 [`ticloud serverless import start`](/tidb-cloud/ticloud-import-start.md)。
