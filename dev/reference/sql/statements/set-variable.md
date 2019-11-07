---
title: SET [GLOBAL|SESSION] <variable>
summary: TiDB 数据库中 SET [GLOBAL|SESSION] <variable> 的使用概况。
category: reference
---

# SET [GLOBAL|SESSION] <variable>

`SET [GLOBAL|SESSION]` 语句用于在 `SESSION` 或 `GLOBAL` 的范围内，对某个 TiDB 的内置变量进行更改。需注意，对 `GLOBAL` 变量的更改不适用于已有连接或本地连接，这与 MySQL 类似。只有新会话才会反映值的变化。

## 语法图

**SetStmt:**

![SetStmt](/media/sqlgram/SetStmt.png)

## 示例

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

{{< copyable "sql" >}}

```sql
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
```

```
Query OK, 0 rows affected (0.03 sec)
```

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

`SET [GLOBAL|SESSION]` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/dev/report-issue.md)。

## 另请参阅

* [SHOW \[GLOBAL|SESSION\] VARIABLES](/dev/reference/sql/statements/show-variables.md)
