---
title: 数据类型
summary: 了解 TiDB 支持的数据类型。
---

# 数据类型

TiDB 支持除 `SPATIAL` 类型外的所有 MySQL 数据类型。这包括所有[数值类型](/data-type-numeric.md)、[字符串类型](/data-type-string.md)、[日期和时间类型](/data-type-date-and-time.md)以及 [JSON 类型](/data-type-json.md)。

数据类型的定义使用 `T(M[, D])` 格式指定。其中：

- `T` 表示具体的数据类型。
- `M` 表示整数类型的最大显示宽度。对于浮点数和定点数类型，`M` 是可以存储的总位数（精度）。对于字符串类型，`M` 是最大长度。`M` 的最大允许值取决于数据类型。
- `D` 适用于浮点数和定点数类型，表示小数点后的位数（标度）。
- `fsp` 适用于 `TIME`、`DATETIME` 和 `TIMESTAMP` 类型，表示小数秒的精度。如果指定了 `fsp` 值，必须在 0 到 6 的范围内。值为 0 表示没有小数部分。如果省略，默认精度为 0。
