---
title: SHOW [GLOBAL|SESSION] STATUS | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW [GLOBAL|SESSION] STATUS 的使用概览。
---

# SHOW [GLOBAL|SESSION] STATUS

此语句是为了与 MySQL 兼容而包含的。对于大多数指标，TiDB 使用 Prometheus 和 Grafana 进行集中指标收集，而不是使用 `SHOW STATUS`。

变量的完整描述可以在这里找到：[状态变量](/status-variables.md)

## 语法

```ebnf+diagram
ShowStatusStmt ::=
    'SHOW' Scope? 'STATUS' ShowLikeOrWhere?

Scope ::=
    ( 'GLOBAL' | 'SESSION' )

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
mysql> SHOW SESSION STATUS;
+-------------------------------+--------------------------------------+
| Variable_name                 | Value                                |
+-------------------------------+--------------------------------------+
| Compression                   | OFF                                  |
| Compression_algorithm         |                                      |
| Compression_level             | 0                                    |
| Ssl_cipher                    |                                      |
| Ssl_cipher_list               |                                      |
| Ssl_server_not_after          |                                      |
| Ssl_server_not_before         |                                      |
| Ssl_verify_mode               | 0                                    |
| Ssl_version                   |                                      |
| Uptime                        | 1409                                 |
| ddl_schema_version            | 116                                  |
| last_plan_binding_update_time | 0000-00-00 00:00:00                  |
| server_id                     | 61160e73-ab80-40ff-8f33-27d55d475fd1 |
+-------------------------------+--------------------------------------+
13 rows in set (0.00 sec)

mysql> SHOW GLOBAL STATUS;
+-----------------------+--------------------------------------+
| Variable_name         | Value                                |
+-----------------------+--------------------------------------+
| Ssl_cipher            |                                      |
| Ssl_cipher_list       |                                      |
| Ssl_server_not_after  |                                      |
| Ssl_server_not_before |                                      |
| Ssl_verify_mode       | 0                                    |
| Ssl_version           |                                      |
| Uptime                | 1413                                 |
| ddl_schema_version    | 116                                  |
| server_id             | 61160e73-ab80-40ff-8f33-27d55d475fd1 |
+-----------------------+--------------------------------------+
9 rows in set (0.00 sec)
```

## MySQL 兼容性

* 此语句与 MySQL 兼容。

## 另请参阅

* [FLUSH STATUS](/sql-statements/sql-statement-flush-status.md)
* [服务器状态变量](/status-variables.md)
