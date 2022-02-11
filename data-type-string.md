---
title: 字符串类型
---

# 字符串类型

TiDB 支持 MySQL 所有的字符串类型，包括 `CHAR`、`VARCHAR`、`BINARY`、`VARBINARY`、`BLOB`、`TEXT`、`ENUM` 以及 `SET`，完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/string-types.html)文档。

## 类型定义

### `CHAR` 类型

定长字符串。`CHAR` 列的长度固定为创建表时声明的长度。当保存 CHAR 值时，不足固定长度的字符串在后面填充空格，以达到指定的长度。M 表示列长度（字符的个数，不是字节的个数）。长度可以为从 0 到 255 的任何值。

{{< copyable "sql" >}}

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `VARCHAR` 类型

变长字符串。M 表示最大列长度（字符的最大个数）。`VARCHAR` 的空间占用大小不得超过 65535 字节。在选择 `VARCHAR` 长度时，应当根据最长的行的大小和使用的字符集确定。

对于不同的字符集，单个字符所占用的空间可能有所不同。以下表格是各个字符集下单个字符占用的字节数，以及 `VARCHAR` 列长度的取值范围：

| 字符集 | 单个字符字节数 | VARCHAR 最大列长度的取值范围 |
| ----- | ---- | ---- |
| ascii | 1 | (0, 65535] |
| latin1 | 1 | (0, 65535] |
| binary | 1 | (0, 65535] |
| utf8 | 3 | (0, 21845] |
| utf8mb4 | 4 | (0, 16383] |

{{< copyable "sql" >}}

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TEXT` 类型

文本串。M 表示最大列长度（字符的最大个数），范围是 0 到 65535。在选择 `TEXT` 长度时，应当根据最长的行的大小和使用的字符集确定。

{{< copyable "sql" >}}

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TINYTEXT` 类型

类似于 [`TEXT`](#text-类型)，区别在于最大列长度为 255。

{{< copyable "sql" >}}

```sql
TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `MEDIUMTEXT` 类型

类似于 [`TEXT`](#text-类型)，区别在于最大列长度为 16,777,215。

{{< copyable "sql" >}}

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `LONGTEXT` 类型

类似于 [`TEXT`](#text-类型)，区别在于最大列长度为 4,294,967,295。

{{< copyable "sql" >}}

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `BINARY` 类型

类似于 [`CHAR`](#char-类型)，区别在于 `BINARY` 存储的是二进制字符串。

{{< copyable "sql" >}}

```sql
BINARY(M)
```

### `VARBINARY` 类型

类似于 [`VARCHAR`](#varchar-类型)，区别在于 `VARBINARY` 存储的是二进制字符串。

{{< copyable "sql" >}}

```sql
VARBINARY(M)
```

### `BLOB` 类型

二进制大文件。M 表示最大列长度，单位是字节，范围是 0 到 65535。

{{< copyable "sql" >}}

```sql
BLOB[(M)]
```

### `TINYBLOB` 类型

类似于 [`BLOB`](#blob-类型)，区别在于最大列长度为 255。

{{< copyable "sql" >}}

```sql
TINYBLOB
```

### `MEDIUMBLOB` 类型

类似于 [`BLOB`](#blob-类型)，区别在于最大列长度为 16777215。

{{< copyable "sql" >}}

```sql
MEDIUMBLOB
```

### `LONGBLOB` 类型

类似于 [`BLOB`](#blob-类型)，区别在于最大列长度为 4,294,967,295。

{{< copyable "sql" >}}

```sql
LONGBLOB
```

### `ENUM` 类型

枚举类型是一个字符串，它只能有一个值的字符串对象。其值必须是从一个固定集合中选取，这个固定集合在创建表的时候定义，语法是：

{{< copyable "sql" >}}

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]
```

例如：

{{< copyable "sql" >}}

```sql
ENUM('apple', 'orange', 'pear')
```

枚举类型的值在 TiDB 内部使用数值来存储，每个值会按照定义的顺序转换为一个数字，比如上面的例子中，每个字符串值都会映射为一个数字：

| 值 | 数字 |
| ---- | ---- |
| NULL  | NULL |
| '' | 0 |
| 'apple' | 1 |
| 'orange' | 2 |
| 'pear' | 3 |

更多信息参考 [MySQL 枚举文档](https://dev.mysql.com/doc/refman/5.7/en/enum.html)。

### `SET` 类型

集合类型是一个包含零个或多个值的字符串，其中每个值必须是从一个固定集合中选取，这个固定集合在创建表的时候定义，语法是：

{{< copyable "sql" >}}

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]
```

例如：

{{< copyable "sql" >}}

```sql
SET('1', '2') NOT NULL
```

上面的例子中，这列的有效值可以是：

```
''
'1'
'2'
'1,2'
```

集合类型的值在 TiDB 内部会转换为一个 Int64 数值，每个元素是否存在用一个二进制位的 0/1 值来表示，比如这个例子 `SET('a','b','c','d')`，每一个元素都被映射为一个数字，且每个数字的二进制表示只会有一位是 1：

| 成员 | 十进制表示 | 二进制表示 |
| ---- | ---- | ------ |
| 'a'  | 1 | 0001 |
| 'b' | 2 | 0010 |
| 'c' | 4 | 0100 |
| 'd' | 8 | 1000 |

这样对于值为 `('a', 'c')` 的元素，其二进制表示即为 0101。

更多信息参考 [MySQL 集合文档](https://dev.mysql.com/doc/refman/5.7/en/set.html)。
