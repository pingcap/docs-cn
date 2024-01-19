---
title: SHOW [GLOBAL|SESSION] STATUS | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [GLOBAL|SESSION] STATUS for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-status/','/docs/dev/reference/sql/statements/show-status/']
---

# SHOW [GLOBAL|SESSION] STATUS

This statement is included for compatibility with MySQL. TiDB uses Prometheus and Grafana for centralized metrics collection instead of `SHOW STATUS` for most metrics.

A full description of the variables can be found here: [status variables](/status-variables.md)

## Synopsis

```ebnf+diagram
ShowStatusStmt ::=
    'SHOW' Scope? 'STATUS' ShowLikeOrWhere?

Scope ::=
    ( 'GLOBAL' | 'SESSION' )

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## Examples

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

## MySQL compatibility

* This statement is compatible with MySQL.

## See also

* [FLUSH STATUS](/sql-statements/sql-statement-flush-status.md)
* [Server Status Variables](/status-variables.md)
