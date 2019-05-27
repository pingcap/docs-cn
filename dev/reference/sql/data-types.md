---
title: TiDB 数据类型
category: reference
aliases: ['/docs-cn/sql/datatype/']
---

# TiDB 数据类型

## 概述

TiDB 支持 MySQL 除空间类型之外的所有数据类型，包括数值型类型、字符串类型、时间&日期类型、Json 类型。

数据类型定义一般为 T(M[, D])，其中：

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

| 语法元素 | 说明 |
| ---- | --------|
| M | 类型显示宽度，可选 |
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

TiDB 支持 MySQL 所有的浮点类型，包括 FLOAT、DOUBLE，完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/floating-point-types.html)文档。

#### 类型定义

语法：

```sql
FLOAT[(M,D)] [UNSIGNED] [ZEROFILL]
> 单精度浮点数。允许的值范围为 -2^128 ~ +2^128，也即 -3.402823466E+38 到 -1.175494351E-38、0 和 1.175494351E-38 到 3.402823466E+38。这些是理论限制，基于 IEEE 标准。实际的范围根据硬件或操作系统的不同可能稍微小些。

DOUBLE[(M,D)] [UNSIGNED] [ZEROFILL]
> 双精度浮点数。允许的值范围为：-2^1024 ~ +2^1024，也即是 -1.7976931348623157E+308 到 -2.2250738585072014E-308、0 和 2.2250738585072014E-308 到 1.7976931348623157E+308。这些是理论限制，基于 IEEE 标准。实际的范围根据硬件或操作系统的不同可能稍微小些。
 
DOUBLE PRECISION [(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED] [ZEROFILL]
> 为 DOUBLE 的同义词。

FLOAT(p) [UNSIGNED] [ZEROFILL]
> 浮点数。p 表示精度（以位数表示），只使用该值来确定是否结果列的数据类型为 FLOAT 或 DOUBLE。如果 p 为从 0 到 24，数据类型变为没有 M 或 D 值的 FLOAT。如果 p 为从 25 到 53，数据类型变为没有 M 或 D 值的 DOUBLE。结果列范围与本节前面描述的单精度 FLOAT 或双精度 DOUBLE 数据类型相同。
```

字段意义:

| 语法元素 | 说明                            |
| -------- | ------------------------------- |
| M        | 小数总位数 |
| D        | 小数点后位数 |
| UNSIGNED | 无符号数，如果不加这个标识，则为有符号数 |
| ZEROFILL | 补零标识，如果有这个标识，TiDB 会自动给类型增加 UNSIGNED 标识 |

#### 存储空间

每种类型对存储空间的需求如下表所示:

| 类型        | 存储空间 |
| ----------- |----------|
| `FLOAT`     | 4        |
| `FLOAT(p)`  | 如果 0 <= p <= 24 为 4 个字节, 如果 25 <= p <= 53 为 8 个字节|
| `DOUBLE`    | 8        |


### 定点类型

TiDB 支持 MySQL 所有的定点类型，包括 DECIMAL、NUMERIC，完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/fixed-point-types.html)文档。

#### 类型定义

语法：

```sql
DECIMAL[(M[,D])] [UNSIGNED] [ZEROFILL]
> 定点数。M 是小数位数(精度)的总数，D 是小数点(标度)后面的位数。小数点和‘-’(负数)符号不包括在M中。如果 D 是 0，则值没有小数点或分数部分。如果 D 被省略， 默认是 0。如果 M 被省略， 默认是 10。

NUMERIC[(M[,D])] [UNSIGNED] [ZEROFILL]
> DECIMAL的同义词。
```

字段意义:

| 语法元素 | 说明                            |
| -------- | ------------------------------- |
| M        | 小数总位数 |
| D        | 小数点后位数 |
| UNSIGNED | 无符号数，如果不加这个标识，则为有符号数 |
| ZEROFILL | 补零标识，如果有这个标识，TiDB 会自动给类型增加 UNSIGNED 标识 |

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

YEAR[(4)]
> 四位格式的年。允许的值是 1901 到 2155 和 0000。
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

Json 类型可以存储 Json 这种半结构化的数据，相比于直接将 Json 存储为字符串，它的好处在于：

1. 使用 Binary 格式进行序列化，对 Json 的内部字段的查询、解析加快；
2. 多了 Json 合法性验证的步骤，只有合法的 Json 文档才可以放入这个字段中；

Json 字段本身上，并不能创建索引。相反，可以对 Json 文档中的某个子字段创建索引。例如：

```sql
CREATE TABLE city (
    id INT PRIMARY KEY,
    detail JSON,
    population INT AS (JSON_EXTRACT(detail, '$.population')
);
INSERT INTO city VALUES (1, '{"name": "Beijing", "population": 100}');
SELECT id FROM city WHERE population >= 100;
```

## 枚举类型

集合类型是一个字符串，其值必须是从一个固定集合中选取，这个固定集合在创建表的时候定义，语法是：

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# 例子
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

## 集合类型

集合类型是一个包含零个或多个值的字符串，其中每个值必须是从一个固定集合中选取，这个固定集合在创建表的时候定义，语法是：

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# 例子
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

## 数据类型的默认值

在一个数据类型描述中的 `DEFAULT value` 段描述了一个列的默认值。这个默认值必须是常量，不可以是一个函数或者是表达式。但是对于时间类型，可以例外的使用 `NOW`、`CURRENT_TIMESTAMP`、`LOCALTIME`、`LOCALTIMESTAMP` 等函数作为 `DATETIME` 或者 `TIMESTAMP` 的默认值。

`BLOB`、`TEXT` 以及 `JSON` 不可以设置默认值。

如果一个列的定义中没有 `DEFAULT` 的设置。TiDB 按照如下的规则决定:

* 如果该类型可以使用 `NULL` 作为值，那么这个列会在定义时添加隐式的默认值设置 `DEFAULT NULL`。
* 如果该类型无法使用 `NULL` 作为值，那么这个列在定义时不会添加隐式的默认值设置。

对于一个设置了 `NOT NULL` 但是没有显式设置 `DEFAULT` 的列，当 `INSERT`、`REPLACE` 没有涉及到该列的值时，TiDB 根据当时的 `SQL_MODE` 进行不同的行为：

* 如果此时是 `strict sql mode`，在事务中的语句会导致事务失败并回滚，非事务中的语句会直接报错。
* 如果此时不是 `strict sql mode`，TiDB 会为这列赋值为列数据类型的隐式默认值。

此时隐式默认值的设置按照如下规则：

* 对于数值类型，它们的默认值是 0。当有 `AUTO_INCREMENT` 参数时，默认值会按照增量情况赋予正确的值。
* 对于除了时间戳外的日期时间类型，默认值会是该类型的“零值”。时间戳类型的默认值会是当前的时间。
* 对于除枚举以外的字符串类型，默认值会是空字符串。对于枚举类型，默认值是枚举中的第一个值。
