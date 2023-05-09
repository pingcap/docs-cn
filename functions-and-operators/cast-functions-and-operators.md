---
title: Cast 函数和操作符
aliases: ['/docs-cn/dev/functions-and-operators/cast-functions-and-operators/','/docs-cn/dev/reference/sql/functions-and-operators/cast-functions-and-operators/']
---

# Cast 函数和操作符

Cast 函数和操作符用于将某种数据类型的值转换为另一种数据类型。TiDB 支持使用 MySQL 5.7 中提供的所有 [Cast 函数和操作符](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html)。

## Cast 函数和操作符表

| 函数和操作符名 | 功能描述 |
| --------------- | ----------------------------------- |
| [`BINARY`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#operator_binary) | 将一个字符串转换成一个二进制字符串 |
| [`CAST()`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#function_cast) | 将一个值转换成一个确定类型 |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#function_convert) | 将一个值转换成一个确定类型 |

## MySQL 兼容性

TiDB 不支持部分数据类型的变更，例如部分时间类型、Bit、Set、Enum 和 JSON 等。

```sql
CREATE TABLE t (a DECIMAL(13, 7));
ALTER TABLE t CHANGE COLUMN a a DATETIME;
ERROR 8200 (HY000): Unsupported modify column: [ddl:8200]Unsupported modify column: change from original type decimal(13,7) to datetime is currently unsupported yet
```
