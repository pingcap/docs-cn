---
title: 服务器状态变量
summary: 使用状态变量查看系统和会话状态
---

# 服务器状态变量

服务器状态变量提供有关服务器全局状态和 TiDB 中当前会话状态的信息。大多数变量与 MySQL 兼容。

你可以使用 [SHOW GLOBAL STATUS](/sql-statements/sql-statement-show-status.md) 命令检索全局状态, 当前会话状态可以使用 [SHOW SESSION STATUS](/sql-statements/sql-statement-show-status.md) 命令。 

此外, [FLUSH STATUS](/sql-statements/sql-statement-flush-status.md) 命令与 MySQL 兼容。

## 系统变量

### Compression

- 作用域: SESSION
- 类型: 字符串
- MySQL 是否使用压缩协议。

### Compression_algorithm

- 作用域: SESSION
- 类型: 字符串
- MySQL 压缩协议使用的算法。

### Compression_level

- 作用域: SESSION
- 类型: 整数型
- MySQL 压缩协议使用的等级。

### Ssl_cipher

- 作用域: SESSION | GLOBAL
- 类型: 字符串
- 正在使用的 TLS 加密套件.

### Ssl_cipher_list

- 作用域: SESSION | GLOBAL
- 类型: 字符串
- 服务器支持的 TLS 加密套件列表.

### Ssl_server_not_after

- 作用域: SESSION | GLOBAL
- 类型: 时间
- c

### Ssl_server_not_before

- 作用域: SESSION | GLOBAL
- 类型: 字符串
- 服务器用于 TLS 连接的 X.509 证书的过期时间。

### Ssl_verify_mode

- 作用域: SESSION | GLOBAL
- 类型: 整数型
- TLS 验证模式掩码。

### Ssl_version

- 作用域: SESSION | GLOBAL
- 类型: 字符串
-  TLS 协议使用的版本。

### Uptime

- 作用域: SESSION | GLOBAL
- 类型: 整数型
- 服务器正常运行时间（秒）。

### ddl_schema_version

- 作用域: SESSION | GLOBAL
- 类型: 整数型
- DDL schema 使用的版本。

### last_plan_binding_update_time <span class="version-mark">New in v5.2.0</span>

- 作用域: SESSION
- 类型: 时间戳
- 上次计划更新的日期时间。

### server_id

- 作用域: SESSION | GLOBAL
- 类型: 字符串
- 服务器的通用唯一识别码（UUID）。