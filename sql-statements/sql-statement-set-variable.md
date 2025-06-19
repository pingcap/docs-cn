---
title: SET [GLOBAL|SESSION] <variable> | TiDB SQL 语句参考
summary: TiDB 数据库中 SET [GLOBAL|SESSION] <variable> 的使用概述。
---

# `SET [GLOBAL|SESSION] <variable>`

`SET [GLOBAL|SESSION]` 语句用于修改 TiDB 的内置变量。这些变量可以是作用域为 `SESSION` 或 `GLOBAL` 的[系统变量](/system-variables.md)或[用户变量](/user-defined-variables.md)。

> **警告：**
>
> 用户定义变量仍然是一个实验性功能。**不建议**在生产环境中使用它们。

> **注意：**
>
> 与 MySQL 类似，对 `GLOBAL` 变量的更改不会应用于现有连接或本地连接。只有新会话才会反映值的更改。

## 语法图

```ebnf+diagram
SetVariableStmt ::=
    "SET" Variable "=" Expression ("," Variable "=" Expression )*

Variable ::=
    ("GLOBAL" | "SESSION") SystemVariable
|   UserVariable 
```

## 示例

获取 `sql_mode` 的值。

```sql
mysql> SHOW GLOBAL VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

全局更新 `sql_mode` 的值。如果在更新后检查 `SQL_mode` 的值，你可以看到 `SESSION` 级别的值尚未更新：

```sql
mysql> SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GLOBAL VARIABLES LIKE 'sql_mode';
+---------------+-----------------------------------------+
| Variable_name | Value                                   |
+---------------+-----------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER |
+---------------+-----------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

使用 `SET SESSION` 会立即生效：

```sql
mysql> SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
Query OK, 0 rows affected (0.01 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-----------------------------------------+
| Variable_name | Value                                   |
+---------------+-----------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER |
+---------------+-----------------------------------------+
1 row in set (0.00 sec)
```

用户变量以 `@` 开头。

```sql
SET @myvar := 5;
Query OK, 0 rows affected (0.00 sec)

SELECT @myvar, @myvar + 1;
+--------+------------+
| @myvar | @myvar + 1 |
+--------+------------+
|      5 |          6 |
+--------+------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

存在以下行为差异：

* 使用 `SET GLOBAL` 进行的更改将传播到集群中的所有 TiDB 实例。这与 MySQL 不同，在 MySQL 中更改不会传播到副本。
* TiDB 将多个变量设置为既可读又可设置。这是 MySQL 兼容性所必需的，因为应用程序和连接器通常都会读取 MySQL 变量。例如：JDBC 连接器会读取和设置查询缓存设置，尽管不依赖该行为。
* 使用 `SET GLOBAL` 进行的更改将在 TiDB 服务器重启后保持。这意味着 TiDB 中的 `SET GLOBAL` 的行为更类似于 MySQL 8.0 及以上版本中的 `SET PERSIST`。
* TiDB 不支持 `SET PERSIST` 和 `SET PERSIST_ONLY`，因为 TiDB 会持久化全局变量。

## 另请参阅

* [SHOW \[GLOBAL|SESSION\] VARIABLES](/sql-statements/sql-statement-show-variables.md)
