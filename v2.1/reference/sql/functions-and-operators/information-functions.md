---
title: Information Functions
summary: Learn about the information functions.
category: reference
---

# Information Functions

In TiDB, the usage of information functions is similar to MySQL. For more information, see [Information Functions](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html).

## Information function descriptions

| Name | Description |
|:-----|:------------|
| [`CONNECTION_ID()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_connection-id) | Return the connection ID (thread ID) for the connection  |
| [`CURRENT_USER()`, `CURRENT_USER`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_current-user) | Return the authenticated user name and host name |
| [`DATABASE()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_database) | Return the default (current) database name  |
| [`FOUND_ROWS()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_found-rows) | For a `SELECT` with a `LIMIT` clause, the number of the rows that are returned if there is no `LIMIT` clause |
| [`LAST_INSERT_ID()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_last-insert-id) | Return the value of the `AUTOINCREMENT` column for the last `INSERT`   |
| [`SCHEMA()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_schema) | Synonym for `DATABASE()`  |
| [`SESSION_USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_session-user) | Synonym for `USER()`    |
| [`SYSTEM_USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_system-user) | Synonym for `USER()`   |
| [`USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_user) | Return the user name and host name provided by the client    |
| [`VERSION()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_version) | Return a string that indicates the MySQL server version   |
| `TIDB_VERSION()` | Return a string that indicates the TiDB server version |
