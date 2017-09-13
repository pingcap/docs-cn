---
title: TiDB 数据类型
category: user guide
---

# TiDB 数据类型

## 目录
+ [概述](#概述)
+ [数值类型](#数值类型)
+ [日期时间类型](#日期时间类型)
+ [字符串类型](#字符串类型)
+ [Json 类型](#json-类型)
+ 其他类型
    - [枚举](#枚举类型)
    - [集合](#集合类型)

## 概述

TiDB 支持 MySQL 除空间类型之外的所有数据类型，包括数值型类型、字符串类型、时间&日期类型、Json 类型。

数据类型定义一般为 T(M[, D])，其中:

* T 表示具体的类型
* M 对于整数类型表示最大显示长度；对于浮点数或者定点数表示精度；对于字符类型表示最大长度。M 的最大值取决于具体的类型。
* D 表示浮点数/定点数的小数位长度
* 对于时间&日期类型中的 TIME、DATETIME 以及 TIMESTAMP，定义中可以包含 Fsp 表示秒的精度，其取值范围是0到6，默认的精度为0

## 数值类型

### 概述

TiDB 支持 MySQL 所有的数值类型，按照精度可以分为:

+ [整数类型（精确值)](#整数类型)
+ [浮点类型（近似值)](#浮点类型)
+ [定点类型（精确值)](#定点类型)

### 整数类型

TiDB 支持 MySQL 所有的整数类型，包括 INTEGER/INT、TINYINT、SMALLINT、MEDIUMINT 以及 BIGINT，完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/numeric-type-overview.html)文档。

#### 类型定义
语法：

```sql
BIT[(M)]
> 比特值类型。M 表示比特位的长度，取值范围从1到64，其默认值是1。

TINYINT[(M)] [UNSIGNED] [ZEROFILL]
> TINYINT 类型。有符号数的范围是[-128, 127]。无符号数的范围是[0, 255]。

BOOL, BOOLEAN
> 布尔类型，和 TINYINT(1) 等价。零值被认为是 False，非零值认为是 True。在 TiDB 内部，True 存储为1， False 存储为0。

SMALLINT[(M)] [UNSIGNED] [ZEROFILL]
> SMALLINT 类型。有符号数的范围是[-32768, 32767]。无符号数的范围是[0, 65535]。

MEDIUMINT[(M)] [UNSIGNED] [ZEROFILL]
> MEDIUMINT 类型。有符号数的范围是[-8388608, 8388607]。无符号数的范围是[0, 16777215]。

INT[(M)] [UNSIGNED] [ZEROFILL]
> INT 类型。 有符号数的范围是[-2147483648, 2147483647]。无符号数的范围是[0, 4294967295]。

INTEGER[(M)] [UNSIGNED] [ZEROFILL]
> 和 INT 相同。

BIGINT[(M)] [UNSIGNED] [ZEROFILL]
> BIGINT 类型。 有符号数的范围是[-9223372036854775808, 9223372036854775807]。无符号数的范围是[0, 18446744073709551615]。
```

字段意义:

| 语法元素 | 说明                            |
| -------- | ------------------------------- |
| M        | 类型长度，可选的                |
| UNSIGNED | 无符号数，如果不加这个标识，则为有符号数 |
| ZEROFILL | 补零标识，如果有这个标识，TiDB 会自动给类型增加 UNSIGNED 标识，但是没有做补零的操作 |

#### 存储空间以及取值范围

每种类型对存储空间的需求以及最大/最小值如下表所示:

| 类型        | 存储空间 | 最小值(有符号/无符号) | 最大值(有符号/无符号) |
| ----------- |----------|-----------------------| --------------------- |
| `TINYINT`   | 1        | -128 / 0              | 127 / 255             |
| `SMALLINT`  | 2        | -32768 / 0            | 32767 / 65535         |
| `MEDIUMINT` | 3        | -8388608 / 0          | 8388607 / 16777215    |
| `INT`       | 4        | -2147483648 / 0       | 2147483647 / 4294967295 |
| `BIGINT`    | 8        | -9223372036854775808 / 0 | 9223372036854775807 / 18446744073709551615 |

### 浮点类型

TODO

### 定点类型

TODO


## 日期时间类型

### 概述

TiDB 支持 MySQL 所有的日期时间类型，包括 DATE、DATETIME、TIMESTAMP、TIME 以及 YEAR，完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-types.html)文档。

### 类型定义

语法：
```sql
DATE
> 日期。支持的范围为`1000-01-01`到`9999-12-31`。以`YYYY-MM-DD`格式显示 DATE 值。

DATETIME[(fsp)]
> 日期和时间的组合。支持的范围是`1000-01-01 00:00:00.000000`到`9999-12-31 23:59:59.000000`。
以`YYYY-MM-DD HH:MM:SS[.fraction]`格式显示 DATETIME 值。fsp 参数是表示秒精度，取值范围为 0-6，默认值取 0。

TIMESTAMP[(fsp)]
> 时间戳。支持的范围是`1970-01-01 00:00:01.000000`到`2038-01-19 03:14:07.999999`。
fsp 参数是表示秒精度，取值范围为 0-6，默认值取 0。

TIME[(fsp)]
> 时间。范围是`-838:59:59.000000`到`838:59:59.000000`。以`HH:MM:SS[.fraction]`格式显示 TIME 值。
fsp 参数是表示秒精度，取值范围为：0-6。默认值取 0。

YEAR[(2|4)]
> 两位或四位格式的年。默认是四位格式。在四位格式中，允许的值是 1901 到 2155 和 0000。在两位格式中，允许的值是 70 到 69，表示从 1970 年到 2069 年。
```

## 字符串类型

### 概述

TiDB 支持 MySQL 所有的字符串类型，包括 CHAR、VARCHAR、BINARY、VARBINARY、BLOB、TEXT、ENUM 以及 SET，
完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/string-types.html)文档。

### 类型定义

语法：
```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
> 定长字符串。CHAR 列的长度固定为创建表时声明的长度。长度可以为从 0 到 255 的任何值。当保存 CHAR 值时，在它们的右边填充空格以达到指定的长度。

[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
> 变长字符串。M 表示最大列长度，范围是 0 到 65535。VARCHAR 的最大实际长度由最长的行的大小和使用的字符集确定。

BINARY(M)
> 类似于 CHAR， 区别在于 BINARY 存储的是二进制字符串。

VARBINARY(M)
> 类似于 VARCHAR， 区别在于 VARBINARY 存储的是二进制字符串。

BLOB[(M)]
> 二进制大文件。M 表示最大列长度，范围是 0 到 65535。

TINYBLOB
> 类似于 BLOB, 区别在于最大列长度为 255。

MEDIUMBLOB
> 类似于 BLOB, 区别在于最大列长度为 16777215。

LONGBLOB
> 类似于 BLOB, 区别在于最大列长度为 4294967295。

TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
> 文本串。M 表示最大列长度，范围是 0 到 65535。TEXT 的最大实际长度由最长的行的大小和使用的字符集确定。

TINYTEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
> 类似于 TEXT, 区别在于最大列长度为 255。

MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
> 类似于 TEXT, 区别在于最大列长度为 16777215。

LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
> 类似于 TEXT, 区别在于最大列长度为 4294967295。

ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]
> 枚举。只能有一个值的字符串对象，其值通常选自允许值列表中，在某些情况下也可以是空串或者 NULL。

SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]
> 集合。可以有零或者多个值的字符串对象，每一个值必须选自允许值列表中。
```

## Json 类型

### 概述


## 枚举类型

## 集合类型