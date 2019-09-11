---
title: 字符串类型
category: reference
---

# 字符串类型

TiDB 支持 MySQL 所有的字符串类型，包括 `CHAR`、`VARCHAR`、`BINARY`、`VARBINARY`、`BLOB`、`TEXT`、`ENUM` 以及 `SET`，完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/string-types.html)文档。

## 类型定义

### `CHAR` 类型

定长字符串。`CHAR` 列的长度固定为创建表时声明的长度。长度可以为从 0 到 255 的任何值。当保存 CHAR 值时，在它们的右边填充空格以达到指定的长度。

{{< copyable "sql" >}}

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `VARCHAR` 类型

变长字符串。M 表示最大列长度，范围是 0 到 65535。VARCHAR 的最大实际长度由最长的行的大小和使用的字符集确定。

{{< copyable "sql" >}}

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TEXT` 类型

文本串。M 表示最大列长度，范围是 0 到 65535。TEXT 的最大实际长度由最长的行的大小和使用的字符集确定。

{{< copyable "sql" >}}

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TINYTEXT` 类型

类似于 `TEXT`，区别在于最大列长度为 255。

{{< copyable "sql" >}}

```sql
TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `MEDIUMTEXT` 类型

类似于 TEXT，区别在于最大列长度为 16,777,215。

{{< copyable "sql" >}}

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `LONGTEXT` 类型

类似于 `TEXT`，区别在于最大列长度为 4,294,967,295。

{{< copyable "sql" >}}

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `BINARY` 类型

类似于 `CHAR`，区别在于 BINARY 存储的是二进制字符串。

{{< copyable "sql" >}}

```sql
BINARY(M)
```

### `VARBINARY` 类型

类似于 `VARCHAR`，区别在于 VARBINARY 存储的是二进制字符串。

{{< copyable "sql" >}}

```sql
VARBINARY(M)
```

### `TINYBLOB` 类型

类似于 BLOB，区别在于最大列长度为 255。

{{< copyable "sql" >}}

```sql
TINYBLOB
```

### `BLOB` 类型

二进制大文件。M 表示最大列长度，范围是 0 到 65535。

{{< copyable "sql" >}}

```sql
BLOB[(M)]
```

### `MEDIUMBLOB` 类型

类似于 `BLOB`，区别在于最大列长度为 16,777,215。

{{< copyable "sql" >}}

```sql
MEDIUMBLOB
```

### `LONGBLOB` 类型

类似于 `BLOB`，区别在于最大列长度为 4,294,967,295。

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
