---
title: SET [GLOBAL|SESSION] <variable>
summary: TiDB 数据库中 SET [GLOBAL|SESSION] <variable> 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-set-variable/','/docs-cn/dev/reference/sql/statements/set-variable/']
---

# `SET [GLOBAL|SESSION] <variable>`

`SET [GLOBAL|SESSION]` 语句用于对某个 TiDB 的内置变量进行更改。这些变量可以是范围为 `SESSION` 或 `GLOBAL` 的[系统变量](/system-variables.md)或是[用户自定义变量](/user-defined-variables.md)。

> **警告：**
>
> 用户自定义变量为实验特性，不建议在生产环境中使用。

> **注意：**
>
> 与 MySQL 类似，对 `GLOBAL` 变量的更改不适用于已有连接或本地连接，只有新会话才会反映值的变化。

## 语法图

```ebnf+diagram
SetVariableStmt ::=
    "SET" Variable "=" Expression ("," Variable "=" Expression )*

Variable ::=
    ("GLOBAL" | "SESSION") SystemVariable
|   UserVariable
```

## 示例

获取 `sql_mode` 的值：

```sql
SHOW GLOBAL VARIABLES LIKE 'sql_mode';
```

```
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SHOW SESSION VARIABLES LIKE 'sql_mode';
```

```
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

更新全局的 `sql_mode`：

```sql
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
```

```
Query OK, 0 rows affected (0.03 sec)
```

检查更新之后的 `sql_mode` 的取值，可以看到 SESSION 级别的值没有更新：

```sql
SHOW GLOBAL VARIABLES LIKE 'sql_mode';
```

```
+---------------+-----------------------------------------+
| Variable_name | Value                                   |
+---------------+-----------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER |
+---------------+-----------------------------------------+
1 row in set (0.00 sec)
```

```sql
SHOW SESSION VARIABLES LIKE 'sql_mode';
```

```
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

`SET SESSION` 则可以立即生效：

```sql
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
SHOW SESSION VARIABLES LIKE 'sql_mode';
```

```
+---------------+-----------------------------------------+
| Variable_name | Value                                   |
+---------------+-----------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER |
+---------------+-----------------------------------------+
1 row in set (0.00 sec)
```

以 `@` 开头的用户变量：

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

使用 `SET [GLOBAL|SESSION] <variable>` 更改系统变量上，TiDB 与 MySQL 存在以下差异

* 在 MySQL 中，使用 `SET GLOBAL` 所作的修改不会应用于副本。而 TiDB 中，`SET GLOBAL` 语句的作用范围取决于具体的系统变量：

    * 全局生效的变量：对于大部分系统变量（例如影响集群行为或优化器行为的变量），`SET GLOBAL` 所作的修改会应用于集群中的全部 TiDB 实例。
    * 仅当前实例生效的变量：对于一些系统变量（例如 `max_connections`），`SET GLOBAL` 所作的修改仅适用于当前连接的 TiDB 实例。

    因此，在使用 `SET GLOBAL` 修改变量前，请务必查阅该变量的[文档](/system-variables.md)，特别是其“是否持久化到集群”属性，以确认其作用范围。

* TiDB 中的若干变量可读又可设置，这是与 MySQL 相兼容的要求，因为应用程序和连接器常读取 MySQL 变量。例如：JDBC 连接器同时读取和设置缓存查询的参数，尽管并不依赖这一行为。
* 即使在 TiDB 服务器重启后，`SET GLOBAL` 的更改也仍然有效。这样，TiDB 中的 `SET GLOBAL` 更类似于 MySQL 8.0 及更高版本中的 `SET PERSIST`。
* TiDB 会持久化全局变量，因此 TiDB 不支持 `SET PERSIST` 和 `SET PERSIST_ONLY`。

## 另请参阅

* [SHOW \[GLOBAL|SESSION\] VARIABLES](/sql-statements/sql-statement-show-variables.md)
