---
title: 数据类型概述
category: reference
---

# 数据类型概述

TiDB 支持除空间类型 (`SPATIAL`) 之外的所有 MySQL 数据类型，包括[数值型类型](dev/reference/sql/data-types/numeric.md)、[字符串类型](dev/reference/sql/data-types/string.md)、[时间和日期类型](dev/reference/sql/data-types/date-and-time.md)、[JSON 类型](dev/reference/sql/data-types/json.md)。

数据类型定义一般为 `T(M[, D])`，其中：

* `T` 表示具体的类型。
* `M` 在整数类型中表示最大显示长度；在浮点数或者定点数中表示精度；在字符类型中表示最大长度。`M` 的最大值取决于具体的类型。
* `D` 表示浮点数、定点数的小数位长度。
* `fsp` 在时间和日期类型里的 `TIME`、`DATETIME` 以及 `TIMESTAMP` 中表示秒的精度，其取值范围是 0 到 6。值为 0 表示没有小数部分。如果省略，则默认精度为 0。
