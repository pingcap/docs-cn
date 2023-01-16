---
title: CSV Configurations for Importing Data
summary: Learn how to use CSV configurations for the Import Data service on TiDB Cloud.
---

# CSV Configurations for Importing Data

This document introduces CSV configurations for the Import Data service on TiDB Cloud.

The following is the CSV Configuration window when you use the Import Data service on TiDB Cloud to import CSV files. For more information, see [Import CSV Files from Amazon S3 or GCS into TiDB Cloud](/tidb-cloud/import-csv-files.md).

![CSV Configurations](/media/tidb-cloud/import-data-csv-config.png)

## Separator

- Definition: defines the field separator. It can be one or multiple characters, but must not be empty.

- Common values:

    * `,` for CSV (comma-separated values). As shown in the above screenshot, "1", "Michael", and "male" represent three fields.
    * `"\t"` for TSV (tab-separated values).

- Default: `,`

## Header

- Definition: whether *all* CSV files contain a header row. If **Header** is `True`, the first row is used as the column names. If **Header** is `False`, the first row is treated as an ordinary data row.

- Default: `True`

## Delimiter

- Definition: defines the delimiter used for quoting. If **Delimiter** is empty, all fields are unquoted.

- Common values:

    * `'"'` quotes fields with double-quote. As shown in the above screenshot, `"Michael","male"` represents two fields. Note that there must be a `,` between the two fields. If the data is `"Michael""male"` (without `,`), the import task will fail to parse. If the data is `"Michael,male"` (with only one double-quote), it is parsed as one field.
    * `''` disables quoting.

- Default: `"`

## Backslash-escape

- Definition: whether to parse backslash inside fields as escape characters. If **Backslash-escape** is `True`, the following sequences are recognized and converted:

    | Sequence | Converted to             |
    |----------|--------------------------|
    | `\0`     | Null character (`U+0000`)  |
    | `\b`     | Backspace (`U+0008`)       |
    | `\n`     | Line feed (`U+000A`)       |
    | `\r`     | Carriage return (`U+000D`) |
    | `\t`     | Tab (`U+0009`)             |
    | `\Z`     | Windows EOF (`U+001A`)     |

    In all other cases (for example, `\"`), the backslash is stripped, leaving the next character (`"`) in the field. The character left has no special roles (for example, delimiters) and is just an ordinary character. Quoting does not affect whether backslash is parsed as an escape character.

    Take the fields in the screenshot as an example.

    - If the value is `True`, `"nick name is \"Mike\""` will be parsed as `nick name is "Mike"` and written to the target table.
    - If the value is `False`, it will be parsed as three fields: `"nick name is \"` , `Mike\`, and `""`. But it cannot be parsed correctly because the fields are not separated from each other.

    For standard CSV files, if there are double-quoted characters in a field to be recorded, you need to use two double-quotes for escaping. In this case, using `Backslash-escape = True` will result in a parsing error, while using `Backslash-escape = False` will correctly parse. A typical scenario is when the imported field contains JSON content. A standard CSV JSON field is normally stored as follows:

    `"{""key1"":""val1"", ""key2"": ""val2""}"`

    In this case, you can set `Backslash-escape = False` and the field will be correctly escaped to the database as follows:

    `{"key1": "val1", "key2": "val2"}`

    If the content of the CSV source file is saved as JSON in the following way, then consider setting `Backslash-escape = True` as follows. But this is not the standard format for CSV.

    `"{\"key1\": \"val1\", \"key2\":\"val2\" }"`

- Default: `True`

## Not-null and Null

> **Note:**
>
> You cannot configure the **Not-null** and **Null** settings when [importing local files](/tidb-cloud/tidb-cloud-import-local-files.md) to TiDB Cloud.

- Definition: the **Not-null** setting controls whether all fields are non-nullable. If **Not-null** is `False`, the string specified by **Null** is transformed to the SQL NULL instead of a specific value.

- Quoting does not affect whether a field is null.

    For example, in the following CSV file:

    ```csv
    column_A,column_B,column_C
    \N,"\N",
    ```

    In the default settings (`Not-null = False; Null = '\N'`), the columns `column_A` and `column_B` are both converted to NULL after being imported to TiDB. The column `column_C` is an empty string `''` but not NULL.

- Default: Not-null=False, Null=\\N

## Trim-last-separator

- Definition: whether to treat `Separator` as the line terminator and trim all trailing separators.

    For example, in the following CSV file:

    ```csv
    A,,B,,
    ```

    - When `Trim-last-separator = False`, this is interpreted as a row of 5 fields `('A', '', 'B', '', '')`.
    - When `Trim-last-separator = True`, this is interpreted as a row of 3 fields `('A', '', 'B')`.

- Default: `False`
