---
title: 数据类型的默认值
---

# 数据类型的默认值

在一个数据类型描述中的 `DEFAULT value` 段描述了一个列的默认值。

所有数据类型都可以设置默认值。这个默认值通常情况下必须是常量，不可以是一个函数或者是表达式，但也存在以下例外情况：

- 对于时间类型，可以使用 `NOW`、`CURRENT_TIMESTAMP`、`LOCALTIME`、`LOCALTIMESTAMP` 等函数作为 `DATETIME` 或者 `TIMESTAMP` 列的默认值。
- 对于整数类型，可以使用 `NEXT VALUE FOR` 函数将序列的下一个值作为列的默认值，使用 [`RAND()`](/functions-and-operators/numeric-functions-and-operators.md) 函数生成随机浮点值作为列的默认值。
- 对于字符串类型，可以使用 [`UUID()`](/functions-and-operators/miscellaneous-functions.md) 函数生成[通用唯一标识符 (UUID)](/best-practices/uuid.md) 作为列的默认值。
- 对于二进制类型，可以使用 [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md) 函数将 UUID 转换为二进制格式后作为列的默认值。
- 从 v8.0.0 开始，新增支持 [`BLOB`](/data-type-string.md#blob-类型)、[`TEXT`](/data-type-string.md#text-类型) 以及 [`JSON`](/data-type-json.md#json-类型) 这三种数据类型设置默认值，但仅支持使用表达式设置[默认值](#表达式默认值)。

如果一个列的定义中没有 `DEFAULT` 的设置。TiDB 按照如下的规则决定：

* 如果该类型可以使用 `NULL` 作为值，那么这个列会在定义时添加隐式的默认值设置 `DEFAULT NULL`。
* 如果该类型无法使用 `NULL` 作为值，那么这个列在定义时不会添加隐式的默认值设置。

对于一个设置了 `NOT NULL` 但是没有显式设置 `DEFAULT` 的列，当 `INSERT`、`REPLACE` 没有涉及到该列的值时，TiDB 根据当时的 `SQL_MODE` 进行不同的行为：

* 如果此时是 `strict sql mode`，在事务中的语句会导致事务失败并回滚，非事务中的语句会直接报错。
* 如果此时不是 `strict sql mode`，TiDB 会为这列赋值为列数据类型的隐式默认值。

此时隐式默认值的设置按照如下规则：

* 对于数值类型，它们的默认值是 0。当有 `AUTO_INCREMENT` 参数时，默认值会按照增量情况赋予正确的值。
* 对于除了时间戳外的日期时间类型，默认值会是该类型的“零值”。时间戳类型的默认值会是当前的时间。
* 对于除枚举以外的字符串类型，默认值会是空字符串。对于枚举类型，默认值是枚举中的第一个值。

## 表达式默认值

> **警告：**
>
> 该特性为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

MySQL 从 8.0.13 开始支持在 `DEFAULT` 子句中指定表达式为默认值。具体可参考 [Explicit Default Handling as of MySQL 8.0.13](https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html#data-type-defaults-explicit)。

从 v8.0.0 开始，TiDB 在 `DEFAULT` 子句中新增支持指定以下表达式作为字段的默认值：

* `UPPER(SUBSTRING_INDEX(USER(), '@', 1))`
* `REPLACE(UPPER(UUID()), '-', '')`
* `DATE_FORMAT` 相关表达式，具体格式如下：
    * `DATE_FORMAT(NOW(), '%Y-%m')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d %H.%i.%s')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s')`
* `STR_TO_DATE('1980-01-01', '%Y-%m-%d')`

此外，从 v8.0.0 开始，TiDB 额外支持 `BLOB`、`TEXT` 以及 `JSON` 数据类型分配默认值，但是默认值仅支持通过表达式来设置。以下是 `BLOB` 的示例：

```sql
CREATE TABLE t2 (b BLOB DEFAULT (RAND()));
```

> **注意：**
>
> 目前 `ADD COLUMN` 语句不支持使用表达式来设置默认值。
