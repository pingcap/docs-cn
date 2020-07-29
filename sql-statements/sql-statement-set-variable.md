---
title: SET [GLOBAL|SESSION] <variable>
summary: TiDB 数据库中 SET [GLOBAL|SESSION] <variable> 的使用概况。
aliases: ['/docs-cn/dev/reference/sql/statements/set-variable/']
---

# `SET [GLOBAL|SESSION] <variable>`

`SET [GLOBAL|SESSION]` 语句用于在 `SESSION` 或 `GLOBAL` 的范围内，对某个 TiDB 的内置变量进行更改。

> **注意：**
>
> 与 MySQL 类似，对 `GLOBAL` 变量的更改不适用于已有连接或本地连接，只有新会话才会反映值的变化。

## 语法图

**SetStmt:**

![SetStmt](/media/sqlgram/SetStmt.png)

**VariableAssignment:**

![VariableAssignment](/media/sqlgram/VariableAssignment.png)

## 示例

获取 `sql_mode` 的值：

{{< copyable "sql" >}}

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

{{< copyable "sql" >}}

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

{{< copyable "sql" >}}

```sql
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
```

```
Query OK, 0 rows affected (0.03 sec)
```

检查更新之后的 `sql_mode` 的取值，可以看到 SESSION 级别的值没有更新：

{{< copyable "sql" >}}

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

{{< copyable "sql" >}}

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

{{< copyable "sql" >}}

```sql
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
```

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

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

## MySQL 兼容性

以下表现差异适用于：

* 集群中的所有 TiDB 实例会获取 `SET GLOBAL` 所做的更改。这点与 MySQL 不同，在 MySQL 中的更改不会应用到副本。
* TiDB 提供了几个既可读又可设置，同时是 MySQL 兼容性必需的变量。因为通常都是应用程序和连接器读取 MySQL 变量。例如：尽管不依赖表现差异，JDBC 连接器会同时读取和设置缓存查询。
* 在 TiDB 服务器中，`SET GLOBAL` 的更改即使重启后也仍然有效。相当于 TiDB 中的 `SET GLOBAL` 与 MySQL 8.0 及更高版本中的 `SET PERSIST`设置更加类似。

## 另请参阅

* [SHOW \[GLOBAL|SESSION\] VARIABLES](/sql-statements/sql-statement-show-variables.md)
