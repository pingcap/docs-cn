---
title: TiDB 数据类型
category: user guide
---

# 目录
+ [概述](#概述)
+ [数值类型](numeric-type.md)
+ [字符串类型](string-type.md)
+ [Json 类型](json.md)
+ [其他类型](other.md)
    - [枚举](other.md#枚举类型)
    - [集合](other.md#集合类型)

## 概述

TiDB 支持 MySQL 除空间类型之外的所有数据类型，包括数值型类型、字符串类型、时间&日期类型、Json 类型。

数据类型定义一般为 T(M[, D])，其中:
* T 表示具体的类型
* M 对于整数类型表示最大显示长度；对于浮点数或者定点数表示精度；对于字符类型表示最大长度。M 的最大值取决于具体的类型。
* D 表示浮点数/定点数的小数位长度
* 对于时间&日期类型中的 TIME、DATETIME 以及 TIMESTAMP，定义中可以包含 Fsp 表示秒的精度，其取值范围是0到6，默认的精度为0