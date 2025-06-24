---
title: TiDB 数据类型
summary: 了解 TiDB 中数据类型的默认值。
---

# 默认值

数据类型规范中的 `DEFAULT` 值子句表示列的默认值。

你可以为所有数据类型设置默认值。通常，默认值必须是常量，不能是函数或表达式，但有一些例外：

- 对于时间类型，你可以使用 `NOW`、`CURRENT_TIMESTAMP`、`LOCALTIME` 和 `LOCALTIMESTAMP` 函数作为 `TIMESTAMP` 和 `DATETIME` 列的默认值。
- 对于整数类型，你可以使用 `NEXT VALUE FOR` 函数将序列的下一个值设置为列的默认值，并使用 [`RAND()`](/functions-and-operators/numeric-functions-and-operators.md) 函数生成随机浮点值作为列的默认值。
- 对于字符串类型，你可以使用 [`UUID()`](/functions-and-operators/miscellaneous-functions.md) 函数生成[通用唯一标识符 (UUID)](/best-practices/uuid.md) 作为列的默认值。
- 对于二进制类型，你可以使用 [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md) 函数将 UUID 转换为二进制格式，并将转换后的值设置为列的默认值。
- 从 v8.0.0 开始，TiDB 额外支持为 [`BLOB`](/data-type-string.md#blob-type)、[`TEXT`](/data-type-string.md#text-type) 和 [`JSON`](/data-type-json.md#json-data-type) 数据类型[指定默认值](#指定表达式作为默认值)，但你只能使用表达式为它们设置[默认值](#默认值)。

如果列定义中不包含显式的 `DEFAULT` 值，TiDB 将按如下方式确定默认值：

- 如果列可以接受 `NULL` 作为值，则该列使用显式的 `DEFAULT NULL` 子句定义。
- 如果列不能接受 `NULL` 作为值，则 TiDB 定义该列时不使用显式的 `DEFAULT` 子句。

对于没有显式 `DEFAULT` 子句的 `NOT NULL` 列，如果 `INSERT` 或 `REPLACE` 语句没有为该列包含值，TiDB 将根据当时生效的 SQL 模式处理该列：

- 如果启用了严格 SQL 模式，对于事务表会发生错误并回滚语句。对于非事务表，会发生错误。
- 如果未启用严格模式，TiDB 将该列设置为该列数据类型的隐式默认值。

隐式默认值定义如下：

- 对于数值类型，默认值为 0。如果声明了 `AUTO_INCREMENT` 属性，默认值为序列中的下一个值。
- 对于除 `TIMESTAMP` 以外的日期和时间类型，默认值为该类型的适当"零"值。对于 `TIMESTAMP`，默认值为当前日期和时间。
- 对于除 `ENUM` 以外的字符串类型，默认值为空字符串。对于 `ENUM`，默认值为第一个枚举值。

## 指定表达式作为默认值

从 8.0.13 开始，MySQL 支持在 `DEFAULT` 子句中指定表达式作为默认值。更多信息，请参见 [MySQL 8.0.13 中的显式默认值处理](https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html#data-type-defaults-explicit)。

从 v8.0.0 开始，TiDB 额外支持在 `DEFAULT` 子句中指定以下表达式作为默认值。

* `UPPER(SUBSTRING_INDEX(USER(), '@', 1))`
* `REPLACE(UPPER(UUID()), '-', '')`
* 以下格式的 `DATE_FORMAT` 表达式：
    * `DATE_FORMAT(NOW(), '%Y-%m')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d %H.%i.%s')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s')`
* `STR_TO_DATE('1980-01-01', '%Y-%m-%d')`

从 v8.0.0 开始，TiDB 额外支持为 `BLOB`、`TEXT` 和 `JSON` 数据类型分配默认值。但是，你只能使用表达式为这些数据类型设置默认值。以下是 `BLOB` 的示例：

```sql
CREATE TABLE t2 (b BLOB DEFAULT (RAND()));
```
