---
title: 字符串类型
summary: 了解 TiDB 支持的字符串类型。
---

# 字符串类型

TiDB 支持所有 MySQL 字符串类型，包括 `CHAR`、`VARCHAR`、`BINARY`、`VARBINARY`、`BLOB`、`TEXT`、`ENUM` 和 `SET`。更多信息，请参见 [MySQL 中的字符串类型](https://dev.mysql.com/doc/refman/8.0/en/string-types.html)。

## 支持的类型

### `CHAR` 类型

`CHAR` 是固定长度的字符串。M 表示列长度（以字符为单位，而不是字节）。M 的范围是 0 到 255。与 `VARCHAR` 类型不同，当数据插入到 `CHAR` 列时，尾部的空格会被截断。

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `VARCHAR` 类型

`VARCHAR` 是可变长度的字符串。M 表示最大列长度（以字符为单位，而不是字节）。`VARCHAR` 的最大大小不能超过 65,535 字节。最大行长度和使用的字符集决定了 `VARCHAR` 的长度。

不同字符集中单个字符占用的空间可能不同。下表显示了每个字符集中单个字符消耗的字节数，以及 `VARCHAR` 列长度的范围：

| 字符集 | 每个字符的字节数 | 最大 `VARCHAR` 列长度的范围 |
| ----- | ---- | ---- |
| ascii | 1 | (0, 65535] |
| latin1 | 1 | (0, 65535] |
| binary | 1 | (0, 65535] |
| utf8 | 3 | (0, 21845] |
| utf8mb4 | 4 | (0, 16383] |

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TEXT` 类型

`TEXT` 是可变长度的字符串。最大列长度为 65,535 字节。可选参数 M 以字符为单位，用于自动选择最适合的 `TEXT` 列类型。例如，`TEXT(60)` 将生成一个 `TINYTEXT` 数据类型，可以存储最多 255 字节，这足以容纳一个最多有 60 个字符的 UTF-8 字符串（每个字符最多 4 字节，4×60=240）。不建议使用 M 参数。

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TINYTEXT` 类型

`TINYTEXT` 类型与 [`TEXT` 类型](#text-类型)类似。区别在于 `TINYTEXT` 的最大列长度为 255。

```sql
TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `MEDIUMTEXT` 类型

<CustomContent platform="tidb">

`MEDIUMTEXT` 类型与 [`TEXT` 类型](#text-类型)类似。区别在于 `MEDIUMTEXT` 的最大列长度为 16,777,215。但由于 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过更改配置增加到 120 MiB。

</CustomContent>
<CustomContent platform="tidb-cloud">

`MEDIUMTEXT` 类型与 [`TEXT` 类型](#text-类型)类似。区别在于 `MEDIUMTEXT` 的最大列长度为 16,777,215。但由于 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过更改配置增加到 120 MiB。

</CustomContent>

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `LONGTEXT` 类型

<CustomContent platform="tidb">

`LONGTEXT` 类型与 [`TEXT` 类型](#text-类型)类似。区别在于 `LONGTEXT` 的最大列长度为 4,294,967,295。但由于 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过更改配置增加到 120 MiB。

</CustomContent>
<CustomContent platform="tidb-cloud">

`LONGTEXT` 类型与 [`TEXT` 类型](#text-类型)类似。区别在于 `LONGTEXT` 的最大列长度为 4,294,967,295。但由于 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过更改配置增加到 120 MiB。

</CustomContent>

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `BINARY` 类型

`BINARY` 类型与 [`CHAR` 类型](#char-类型)类似。区别在于 `BINARY` 存储二进制字节字符串。

```sql
BINARY(M)
```

### `VARBINARY` 类型

`VARBINARY` 类型与 [`VARCHAR` 类型](#varchar-类型)类似。区别在于 `VARBINARY` 存储二进制字节字符串。

```sql
VARBINARY(M)
```

### `BLOB` 类型

`BLOB` 是大型二进制文件。M 表示最大列长度（以字节为单位），范围从 0 到 65,535。

```sql
BLOB[(M)]
```

### `TINYBLOB` 类型

`TINYBLOB` 类型与 [`BLOB` 类型](#blob-类型)类似。区别在于 `TINYBLOB` 的最大列长度为 255。

```sql
TINYBLOB
```

### `MEDIUMBLOB` 类型

<CustomContent platform="tidb">

`MEDIUMBLOB` 类型与 [`BLOB` 类型](#blob-类型)类似。区别在于 `MEDIUMBLOB` 的最大列长度为 16,777,215。但由于 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过更改配置增加到 120 MiB。

</CustomContent>
<CustomContent platform="tidb-cloud">

`MEDIUMBLOB` 类型与 [`BLOB` 类型](#blob-类型)类似。区别在于 `MEDIUMBLOB` 的最大列长度为 16,777,215。但由于 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过更改配置增加到 120 MiB。

</CustomContent>

```sql
MEDIUMBLOB
```

### `LONGBLOB` 类型

<CustomContent platform="tidb">

`LONGBLOB` 类型与 [`BLOB` 类型](#blob-类型)类似。区别在于 `LONGBLOB` 的最大列长度为 4,294,967,295。但由于 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过更改配置增加到 120 MiB。

</CustomContent>
<CustomContent platform="tidb-cloud">

`LONGBLOB` 类型与 [`BLOB` 类型](#blob-类型)类似。区别在于 `LONGBLOB` 的最大列长度为 4,294,967,295。但由于 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过更改配置增加到 120 MiB。

</CustomContent>

```sql
LONGBLOB
```

### `ENUM` 类型

`ENUM` 是一个字符串对象，其值必须是在创建表时在列规格中明确枚举的允许值列表中选择的。语法为：

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# 例如：
ENUM('apple', 'orange', 'pear')
```

`ENUM` 数据类型的值以数字形式存储。每个值根据定义顺序转换为数字。在前面的示例中，每个字符串映射到一个数字：

| 值 | 数字 |
| ---- | ---- |
| NULL | NULL |
| '' | 0 |
| 'apple' | 1 |
| 'orange' | 2 |
| 'pear' | 3 |

更多信息，请参见 [MySQL 中的 ENUM 类型](https://dev.mysql.com/doc/refman/8.0/en/enum.html)。

### `SET` 类型

`SET` 是一个字符串对象，可以有零个或多个值，每个值都必须从创建表时指定的允许值列表中选择。语法为：

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# 例如：
SET('1', '2') NOT NULL
```

在示例中，以下任何值都可以是有效的：

```
''
'1'
'2'
'1,2'
```

在 TiDB 中，`SET` 类型的值在内部转换为 `Int64`。每个元素的存在使用二进制表示：0 或 1。对于指定为 `SET('a','b','c','d')` 的列，成员具有以下十进制和二进制值。

| 成员 | 十进制值 | 二进制值 |
| ---- | ---- | ------ |
| 'a' | 1 | 0001 |
| 'b' | 2 | 0010 |
| 'c' | 4 | 0100 |
| 'd' | 8 | 1000 |

在这种情况下，对于元素 `('a', 'c')`，它在二进制中是 `0101`。

更多信息，请参见 [MySQL 中的 SET 类型](https://dev.mysql.com/doc/refman/8.0/en/set.html)。
