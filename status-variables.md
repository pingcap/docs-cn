---
title: Server Status Variables
summary: Use status variables to see the system and session status
---

# Server Status Variables

Server status variables provide information about the global status of the server and the status of the current session in TiDB. Most of these variables are designed to be compatible with MySQL.

You can retrieve the global status using the [SHOW GLOBAL STATUS](/sql-statements/sql-statement-show-status.md) command, and the status of the current session using the [SHOW SESSION STATUS](/sql-statements/sql-statement-show-status.md) command. 

Additionally, the [FLUSH STATUS](/sql-statements/sql-statement-flush-status.md) command is supported for MySQL compatibility.

## Variable reference

### Compression

- Scope: SESSION
- Type: Boolean
- Indicates if the MySQL Protocol uses compression or not.

### Compression_algorithm

- Scope: SESSION
- Type: String
- Indicates the compression algorithm that is used for the MySQL Protocol.

### Compression_level

- Scope: SESSION
- Type: Integer
- The compression level that is used for the MySQL Protocol.

### Ssl_cipher

- Scope: SESSION | GLOBAL
- Type: String
- TLS Cipher that is in use.

### Ssl_cipher_list

- Scope: SESSION | GLOBAL
- Type: String
- The list of TLS Ciphers that the server supports.

### Ssl_server_not_after

- Scope: SESSION | GLOBAL
- Type: Date
- The expiration date of the X.509 certificate of the server that is used for TLS connections.

### Ssl_server_not_before

- Scope: SESSION | GLOBAL
- Type: String
- The start date of the X.509 certificate of the server that is used for TLS connections.

### Ssl_verify_mode

- Scope: SESSION | GLOBAL
- Type: Integer
- The TLS verification mode bitmask.

### Ssl_version

- Scope: SESSION | GLOBAL
- Type: String
- The version of the TLS protocol that is used

### Uptime

- Scope: SESSION | GLOBAL
- Type: Integer
- Uptime of the server in seconds.

### ddl_schema_version

- Scope: SESSION | GLOBAL
- Type: Integer
- The version of the DDL schema that is used.

### last_plan_binding_update_time <span class="version-mark">New in v5.2.0</span>

- Scope: SESSION
- Type: Timestamp
- The time and date of the last plan binding update.

### server_id

- Scope: SESSION | GLOBAL
- Type: String
- The UUID of the server.
