---
title: 服务器状态变量
summary: 使用状态变量查看系统和会话状态
---

# 服务器状态变量

服务器状态变量提供了 TiDB 中服务器全局状态和当前会话状态的信息。这些变量中的大多数都是为了与 MySQL 兼容而设计的。

你可以使用 [SHOW GLOBAL STATUS](/sql-statements/sql-statement-show-status.md) 命令查看全局状态，使用 [SHOW SESSION STATUS](/sql-statements/sql-statement-show-status.md) 命令查看当前会话的状态。

此外，为了与 MySQL 兼容，还支持 [FLUSH STATUS](/sql-statements/sql-statement-flush-status.md) 命令。

## 变量参考

### Compression

- 作用域：SESSION
- 类型：Boolean
- 表示 MySQL 协议是否使用压缩。

### Compression_algorithm

- 作用域：SESSION
- 类型：String
- 表示 MySQL 协议使用的压缩算法。

### Compression_level

- 作用域：SESSION
- 类型：Integer
- MySQL 协议使用的压缩级别。

### Ssl_cipher

- 作用域：SESSION | GLOBAL
- 类型：String
- 当前使用的 TLS 加密算法。

### Ssl_cipher_list

- 作用域：SESSION | GLOBAL
- 类型：String
- 服务器支持的 TLS 加密算法列表。

### Ssl_server_not_after

- 作用域：SESSION | GLOBAL
- 类型：Date
- 用于 TLS 连接的服务器 X.509 证书的过期日期。

### Ssl_server_not_before

- 作用域：SESSION | GLOBAL
- 类型：String
- 用于 TLS 连接的服务器 X.509 证书的生效日期。

### Ssl_verify_mode

- 作用域：SESSION | GLOBAL
- 类型：Integer
- TLS 验证模式位掩码。

### Ssl_version

- 作用域：SESSION | GLOBAL
- 类型：String
- 使用的 TLS 协议版本。

### Uptime

- 作用域：SESSION | GLOBAL
- 类型：Integer
- 服务器运行时间，以秒为单位。

### ddl_schema_version

- 作用域：SESSION | GLOBAL
- 类型：Integer
- 使用的 DDL schema 版本。

### last_plan_binding_update_time <span class="version-mark">New in v5.2.0</span>

- 作用域：SESSION
- 类型：Timestamp
- 最后一次执行计划绑定更新的时间和日期。

### server_id

- 作用域：SESSION | GLOBAL
- 类型：String
- 服务器的 UUID。

### tidb_gc_last_run_time

- 作用域：SESSION | GLOBAL
- 类型：String
- 最后一次运行 [GC](/garbage-collection-overview.md) 的时间戳。

### tidb_gc_leader_desc

- 作用域：SESSION | GLOBAL
- 类型：String
- [GC](/garbage-collection-overview.md) leader 的信息，包括主机名和进程 ID (pid)。

### tidb_gc_leader_lease

- 作用域：SESSION | GLOBAL
- 类型：String
- [GC](/garbage-collection-overview.md) lease 的时间戳。

### tidb_gc_leader_uuid

- 作用域：SESSION | GLOBAL
- 类型：String
- [GC](/garbage-collection-overview.md) leader 的 UUID。

### tidb_gc_safe_point

- 作用域：SESSION | GLOBAL
- 类型：String
- [GC](/garbage-collection-overview.md) safe point 的时间戳。
