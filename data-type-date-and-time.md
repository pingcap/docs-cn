---
title: 日期和时间类型
aliases: ['/docs-cn/stable/data-type-date-and-time/','/docs-cn/v4.0/data-type-date-and-time/','/docs-cn/stable/reference/sql/data-types/date-and-time/']
---

# 日期和时间类型

TiDB 支持 MySQL 所有的日期和时间类型，包括 [`DATE`](#date-类型)、[`TIME`](#time-类型)、[`DATETIME`](#datetime-类型)、[`TIMESTAMP`](#timestamp-类型) 以及 [`YEAR`](#year-类型)。完整信息可以参考 [MySQL 中的时间和日期类型](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-types.html)。

每种类型都有有效值范围，值为 0 表示无效值。此外，`TIMESTAMP` 和 `DATETIME` 类型能自动生成新的时间值。

关于日期和时间值类型，需要注意：

- 日期部分必须是“年-月-日”的格式（例如 `1998-09-04`），而不是“月-日-年”或“日-月-年”的格式。
- 如果日期的年份部分是 2 位数，TiDB 会根据[年份为两位数的具体规则](#年份为两位数)进行转换。
- 如果格式必须是数值类型，TiDB 会自动将日期或时间值转换为数值类型。例如：

    {{< copyable "sql" >}}

    ```sql
    SELECT NOW(), NOW()+0, NOW(3)+0;
    ```

    ```sql
    +---------------------+----------------+--------------------+
    | NOW()               | NOW()+0        | NOW(3)+0           |
    +---------------------+----------------+--------------------+
    | 2012-08-15 09:28:00 | 20120815092800 | 20120815092800.889 |
    +---------------------+----------------+--------------------+
    ```

- TiDB 可以自动将无效值转换同一类型的零值。是否进行转换取决于 SQL 模式的设置。比如：

    {{< copyable "sql" >}}

    ```sql
    show create table t1;
    ```

    ```sql
    +-------+---------------------------------------------------------------------------------------------------------+
    | Table | Create Table                                                                                            |
    +-------+---------------------------------------------------------------------------------------------------------+
    | t1    | CREATE TABLE `t1` (
      `a` time DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
    +-------+---------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    select @@sql_mode;
    ```

    ```sql
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    | @@sql_mode                                                                                                                                |
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    insert into t1 values (`2090-11-32:22:33:44`);
    ```

    ```sql
    ERROR 1292 (22007): Truncated incorrect time value: `2090-11-32:22:33:44`
    ```

    {{< copyable "sql" >}}

    ```sql
    set @@sql_mode=``;
    ```

    ```sql
    Query OK, 0 rows affected (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    insert into t1 values (`2090-11-32:22:33:44`);
    ```

    ```sql
    Query OK, 1 row affected, 1 warning (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    select * from t1;
    ```

    ```sql
    +----------+
    | a        |
    +----------+
    | 00:00:00 |
    +----------+
    1 row in set (0.01 sec)
    ```

- SQL 模式的不同设置，会改变 TiDB 对格式的要求。
- 如果 SQL 模式的 `NO_ZERO_DATE` 被禁用，TiDB 允许 `DATE` 和 `DATETIME` 列中的月份或日期为零。例如，`2009-00-00` 或 `2009-01-00`。如果使用函数计算这种日期类型，例如使用 `DATE_SUB()` 或 `DATE_ADD()` 函数，计算结果可能不正确。
- 默认情况下，TiDB 启用 `NO_ZERO_DATE` SQL 模式。该模式可以避免存储像 `0000-00-00` 这样的零值。

不同类型的零值如下表所示：

| 数据类型 | 零值 |
| :------   |  :----       |
| DATE      | `0000-00-00` |
| TIME      | `00:00:00`   |
| DATETIME  | `0000-00-00 00:00:00` |
| TIMESTAMP | `0000-00-00 00:00:00` |
| YEAR      | 0000         |

如果 SQL 模式允许使用无效的 `DATE`、`DATETIME`、`TIMESTAMP` 值，无效值会自动转换为相应的零值（`0000-00-00` 或 `0000-00-00 00:00:00`）。

## 类型定义

### `DATE` 类型

`DATE` 类型只包含日期部分，不包含时间部分。`DATE` 类型的格式为 `YYYY-MM-DD`，支持的范围是 `1000-01-01` 到 `9999-12-31`。

{{< copyable "sql" >}}

```sql
DATE
```

### `TIME` 类型

`TIME` 类型的格式为 `HH:MM:SS[.fraction]`，支持的范围是 `-838:59:59.000000` 到 `838:59:59.000000`。`TIME` 不仅可用于指示一天内的时间，还可用于指两个事件之间的时间间隔。`fsp` 参数表示秒精度，取值范围为：0 ~ 6，默认值为 0。

{{< copyable "sql" >}}

```sql
TIME[(fsp)]
```

> **注意：**
>
> 注意 `TIME` 的缩写形式。例如，`11:12` 表示 `11:12:00` 而不是 `00:11:12`。但是，`1112` 表示 `00:11:12`。这些差异取决于 `:` 字符的存在与否。

### `DATETIME` 类型

`DATETIME` 类型是日期和时间的组合，格式为 `YYYY-MM-DD HH:MM:SS[.fraction]`。支持的范围是 `1000-01-01 00:00:00.000000` 到 `9999-12-31 23:59:59.999999`。`fsp` 参数表示秒精度，取值范围为 0~6，默认值为 0。TiDB 支持字符串或数字转换为 `DATETIME` 类型。

{{< copyable "sql" >}}

```sql
DATETIME[(fsp)]
```

### `TIMESTAMP` 类型

`TIMESTAMP` 类型是日期和时间的组合，支持的范围是 UTC 时间从 `1970-01-01 00:00:01.000000` 到 `2038-01-19 03:14:07.999999`。`fsp` 参数表示秒精度，取值范围为 0~6，默认值为 0。在 `TIMESTAMP` 中，不允许零出现在月份部分或日期部分，唯一的例外是零值本身 `0000-00-00 00:00:00`。

{{< copyable "sql" >}}

```sql
TIMESTAMP[(fsp)]
```

#### 时区处理

当存储 `TIMESTAMP` 时，TiDB 会将当前时区的 `TIMESTAMP` 值转换为 UTC 时区。当读取 `TIMESTAMP` 时，TiDB 将存储的 `TIMESTAMP` 值从 UTC 时区转换为当前时区（注意：`DATETIME` 不会这样处理）。每次连接的默认时区是服务器的本地时区，可以通过环境变量 `time_zone` 进行修改。

> **警告：**
>
> 和 MySQL 一样，`TIMESTAMP` 数据类型受 [2038 年问题](https://zh.wikipedia.org/wiki/2038%E5%B9%B4%E9%97%AE%E9%A2%98)的影响。如果存储的值大于 2038，建议使用 `DATETIME` 类型。

### `YEAR` 类型

`YEAR` 类型的格式为 `YYYY`，支持的值范围是 `1901` 到 `2155`，也支持零值 `0000`。

{{< copyable "sql" >}}

```sql
YEAR[(4)]
```

`YEAR` 类型遵循以下格式规则：

+ 如果是四位数的数值，支持的范围是 `1901` 至 `2155`。
+ 如果是四位数的字符串，支持的范围是 `'1901'` 到 `'2155'`。
+ 如果是 1~99 之间的一位数或两位数的数字，1~69 换算成 2001~2069，70~99 换算成 1970~1999。
+ 支持 `'0'` 到 `'99'` 之间的一位数或两位数字符串的范围
+ 将数值 `0` 转换为 `0000`，将字符串 `'0'` 或 `'00'` 转换为 `'2000'`。

无效的 `YEAR` 值会自动转换为 `0000`（如果用户没有使用 `NO_ZERO_DATE` SQL 模式）。

## 自动初始化和更新 `TIMESTAMP` 或 `DATETIME`

带有 `TIMESTAMP` 或 `DATETIME` 数据类型的列可以自动初始化为或更新为当前时间。

对于表中任何带有 `TIMESTAMP` 或 `DATETIME` 数据类型的列，你可以设置默认值，或自动更新为当前时间戳。

在定义列的时候，`TIMESTAMP` 和 `DATETIME` 可以通过 `DEFAULT CURRENT_TIMESTAMP` 和 `ON UPDATE CURRENT_TIMESTAMP` 来设置。`DEFAULT` 也可以设置为一个特定的值，例如 `DEFAULT 0` 或 `DEFAULT '2000-01-01 00:00:00'`。

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

除非指定 `DATETIME` 的值为 `NOT NULL`，否则默认 `DATETIME` 的值为 `NULL`。指定 `DATETIME` 的值为 `NOT NULL` 时，如果没有设置默认值，则默认值为 `0`。

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
    dt1 DATETIME ON UPDATE CURRENT_TIMESTAMP,         -- default NULL
    dt2 DATETIME NOT NULL ON UPDATE CURRENT_TIMESTAMP -- default 0
);
```

## 时间值的小数部分

`DATETIME` 和 `TIMESTAMP` 值最多可以有 6 位小数，精确到毫秒。如果包含小数部分，值的格式为 `YYYY-MM-DD HH:MM:SS[.fraction]`，小数部分的范围为 `000000` 到`999999`。必须使用小数点分隔小数部分与其他部分。

+ 使用 `type_name(fsp)` 可以定义精确到小数的列，其中 `type_name` 可以是`TIME`、`DATETIME` 或 `TIMESTAMP`。例如：

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE t1 (t TIME(3), dt DATETIME(6));
    ```

    `fsp` 范围是 `0` 到 `6`。

    `0` 表示没有小数部分。如果省略了 `fsp` ，默认为 `0`。

+ 当插入包含小数部分的 `TIME`、`DATETIME` 或 `TIMESTAMP` 时，如果小数部分的位数过少或过多，可能需要进行四舍五入。例如：

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE fractest( c1 TIME(2), c2 DATETIME(2), c3 TIMESTAMP(2) );
    ```

    ```sql
    Query OK, 0 rows affected (0.33 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO fractest VALUES
         > ('17:51:04.777', '2014-09-08 17:51:04.777',   '2014-09-08 17:51:04.777');
    ```

    ```sql
    Query OK, 1 row affected (0.03 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM fractest;
    ```

    ```sql
    +-------------|------------------------|------------------------+
    | c1          | c2                     | c3                     |
    +-------------|------------------------|------------------------+
    | 17:51:04.78 | 2014-09-08 17:51:04.78 | 2014-09-08 17:51:04.78 |
    +-------------|------------------------|------------------------+
    1 row in set (0.00 sec)
    ```

## 日期和时间类型的转换

在日期和时间类型之间进行转换时，有些转换可能会导致信息丢失。例如，`DATE`、`DATETIME` 和 `TIMESTAMP` 都有各自的有效值范围。`TIMESTAMP` 不能早于 UTC 时间的 1970 年，也不能晚于 UTC 时间的 `2038-01-19 03:14:07`。根据这个规则，`1968-01-01` 对于 `DATE` 或 `DATETIME` 是有效的，但当 `1968-01-01` 转换为 `TIMESTAMP` 时，就会变成 0。

`DATE` 的转换：

+ 当 `DATE` 转换为 `DATETIME` 或 `TIMESTAMP` 时，会添加时间部分 `00:00:00`，因为 `DATE` 不包含任何时间信息。
+ 当 `DATE` 转换为 `TIME` 时，结果是 `00:00:00`。

`DATETIME` 或 `TIMESTAMP` 的转换：

+ 当 `DATETIME` 或 `TIMESTAMP` 转换为 `DATE` 时，时间和小数部分将被舍弃。例如，`1999-12-31 23:59:59.499` 被转换为 `1999-12-31`。
+ 当 `DATETIME` 或 `TIMESTAMP` 转换为 `TIME` 时，时间部分被舍弃，因为 `TIME` 不包含任何时间信息。

如果要将 `TIME` 转换为其他时间和日期格式，日期部分会自动指定为 `CURRENT_DATE()`。最终的转换结果是由 `TIME` 和 `CURRENT_DATE()` 组成的日期。也就是说，如果 `TIME` 的值超出了 `00:00:00` 到 `23:59:59` 的范围，那么转换后的日期部分并不表示当前的日期。

当 `TIME` 转换为 `DATE` 时，转换过程类似，时间部分被舍弃。

使用 `CAST()` 函数可以显式地将值转换为 `DATE` 类型。例如：

{{< copyable "sql" >}}

```sql
date_col = CAST(datetime_col AS DATE)
```

将 `TIME` 和 `DATETIME` 转换为数字格式。例如：

{{< copyable "sql" >}}

```sql
SELECT CURTIME(), CURTIME()+0, CURTIME(3)+0;
```

```sql
+-----------|-------------|--------------+
| CURTIME() | CURTIME()+0 | CURTIME(3)+0 |
+-----------|-------------|--------------+
| 09:28:00  |       92800 |    92800.887 |
+-----------|-------------|--------------+
```

{{< copyable "sql" >}}

```sql
SELECT NOW(), NOW()+0, NOW(3)+0;
```

```sql
+---------------------|----------------|--------------------+
| NOW()               | NOW()+0        | NOW(3)+0           |
+---------------------|----------------|--------------------+
| 2012-08-15 09:28:00 | 20120815092800 | 20120815092800.889 |
+---------------------|----------------|--------------------+
```

## 年份为两位数

如果日期中包含年份为两位数，这个年份是有歧义的，并不显式地表示实际年份。

对于 `DATETIME`、`DATE` 和 `TIMESTAMP` 类型，TiDB 使用如下规则来消除歧义。

- 将 01 至 69 之间的值转换为 2001 至 2069 之间的值。
- 将 70 至 99 之间的值转化为 1970 至 1999 之间的值。

上述规则也适用于 `YEAR` 类型，但有一个例外。将数字 `00` 插入到 `YEAR(4)` 中时，结果是 0000 而不是 2000。

如果想让结果是 2000，需要指定值为 `2000`。

对于 `MIN()` 和 `MAX()` 等函数，年份为两位数时可能会得到错误的计算结果。建议年份为四位数时使用这类函数。
