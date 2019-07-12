---
title: 日期和时间类型
category: reference
---

# 日期和时间类型

TiDB 支持 MySQL 所有的日期和时间类型，包括 DATE、DATETIME、TIMESTAMP、TIME 以及 YEAR，完整信息参考[这篇](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-types.html)文档。

<!-- markdownlint-disable MD001 -->

## 类型定义

### `DATE` 类型

`DATE` 类型的格式为 `YYYY-MM-DD`，支持的范围是 `1000-01-01` 到 `9999-12-31`。

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
> 注意 `TIME` 的缩写形式。例如，'11:12' 表示 '11:12:00' 而不是 '00:11:12'。但是，'1112' 表示 '00:11:12'。这些差异取决于 `:` 字符的存在与否。

### `DATETIME` 类型

`DATETIME` 类型是日期和时间的组合，格式为 `YYYY-MM-DD HH:MM:SS[.fraction]`。支持的范围是 `1000-01-01 00:00:00.000000` 到 `9999-12-31 23:59:59.000000`。`fsp` 参数表示秒精度，取值范围为 0~6，默认值为 0。

{{< copyable "sql" >}}

```sql
DATETIME[(fsp)]
```

### `TIMESTAMP` 类型

`TIMESTAMP` 类型包含日期和时间，支持的范围是 `1970-01-01 00:00:01.000000` 到 `2038-01-19 03:14:07.999999`。`fsp` 参数表示秒精度，取值范围为 0~6，默认值为 0。在 `TIMESTAMP` 中，不允许零出现在月份部分或日期部分，唯一的例外是零值本身 '0000-00-00 00:00:00'。

{{< copyable "sql" >}}

```sql
TIMESTAMP[(fsp)]
```

### `YEAR` 类型

`YEAR` 类型的格式为 'YYYY'，支持的值范围是 1901 到 2155，或零值 0000。

{{< copyable "sql" >}}

```sql
YEAR[(4)]
```
