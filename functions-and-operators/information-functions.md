---
title: 信息函数
category: reference
---

# 信息函数

TiDB 中信息函数的使用方法与 MySQL 基本一致，详情参见：[Information Functions](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html)。

## 信息函数表

| 函数名 | 功能描述                                 |
| ------ | ---------------------------------------- |
| [`CONNECTION_ID()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_connection-id) | 返回当前连接的连接 ID (线程 ID)                     |
| [`CURRENT_USER()`, `CURRENT_USER`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_current-user) | 返回当前用户的用户名和主机名                           |
| [`DATABASE()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_database) | 返回默认(当前)的数据库名                            |
| [`FOUND_ROWS()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_found-rows) | 该函数返回对于一个包含 LIMIT 的 SELECT 查询语句，在不包含 LIMIT 的情况下回返回的记录数 |
| [`LAST_INSERT_ID()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_last-insert-id) | 返回最后一条 INSERT 语句中自增列的值                   |
| [`SCHEMA()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_schema) | 与 DATABASE() 同义                          |
| [`SESSION_USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_session-user) | 与 USER() 同义                              |
| [`SYSTEM_USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_system-user) | 与 USER() 同义                              |
| [`USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_user) | 返回客户端提供的用户名和主机名                          |
| [`VERSION()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_version) | 返回当前 MySQL 服务器的版本信息                      |
| `TIDB_VERSION()`                           | 返回当前 TiDB 服务器的版本信息                       |
