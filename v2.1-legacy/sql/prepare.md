---
title: Prepared SQL 语句语法
category: user guide
---

# Prepared SQL 语句语法

TiDB 支持服务器端的 Prepared 语句，这种方式可以降低语句解析以及查询优化的开销，提高执行效率。有两种方式可以使用 Prepared 语句：

## 通过应用程序

大多数 MySQL Driver 都支持 Prepared 语句，比如 [MySQL Connector/C](https://dev.mysql.com/doc/connector-c/en/)。这种方式可以通过 Binary 协议直接调用 Prepared 语句 API。

## 通过 SQL 语句

通过 `PREPARE`，`EXECUTE` 以及 `DEALLOCATE PREPARE` 这三个语句也可以实现 Prepared 语句，这种方式不如第一种方式效率高，但是不需要写程序即可使用。

### `PREPARE` 语句

```sql
PREPARE stmt_name FROM preparable_stmt
```

`PREPARE` 语句对 `preparable_stmt` 做预处理（语法解析、语义检查、查询优化）并将其处理结果命名为 `stmt_name`，后面的操作可以通过 `stmt_name` 来引用。处理好的语句可以通过 `EXECUTE` 语句执行或者是通过 `DEALLOCATE PREPARE` 语句释放。

### `EXECUTE` 语句

```sql
EXECUTE stmt_name [USING @var_name [, @var_name] ...]
```

`EXECUTE` 语句执行名字为 `stmt_name` 的预处理语句。如果预处理语句中有参数，则可以通过 `USING` 子句中的 User Variable 列表给参数赋值。

### `DEALLOCATE PREPARE` 语句

```sql
{DEALLOCATE | DROP} PREPARE stmt_name
```

`DEALLOCATE PREPARE` 语句删除 `PREPARE` 产生的预处理语句结果。

更多信息请参考 [MySQL Prepared Statement Syntax](https://dev.mysql.com/doc/refman/5.7/en/sql-syntax-prepared-statements.html)。