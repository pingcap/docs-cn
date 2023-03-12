---
title: TiDB 审计日志
summary: 了解使用 TiDB 的审计日志功能。
aliases: ['/docs-cn/dev/audit-log/']
---

# TiDB 审计日志

审计日志功能是 TiDB 的企业版特性，可以灵活地记录对 TiDB 服务器的各种操作，方便安全、运维人员查看 SQL 操作日志，及时发现问题。

> **注意：**
>
> TiDB 社区版用户无法使用审计日志功能，请[升级到 TiDB 企业版](https://cn.pingcap.com/product/#SelectProduct)以使用该功能并享受商业专家的支持服务。

## 概念介绍

### 日志事件

TiDB 审计日志根据 SQL 语句的类型将 SQL 操作分为若干事件类型（Event Class）。一条 SQL 语句对应一种或多种事件类型，一种事件类型可以是另一种事件类型的子类型（Subclass），比如：

* `SELECT * FROM t` 对应的事件类型是 `QUERY` 和 `SELECT`。`SELECT` 属于 `QUERY` 的子类型
* `INSERT INTO t VALUES (1),(2),(3)` 对应的事件类型是 `QUERY`、`QUERY_DML` 和 `INSERT`。`INSERT` 属于 `QUERY_DML` 的子类型，`QUERY_DML` 属于 `QUERY` 的子类型
* `SET GLOBAL tidb_audit_enabled = 1` 对应的事件类型是 `AUDIT`、`AUDIT_SET_SYS_VAR` 和 `AUDIT_ENABLE`。`AUDIT_ENABLE` 属于 `AUDIT_SET_SYS_VAR` 的子类型，`AUDIT_SET_SYS_VAR` 属于 `AUDIT` 的子类型

使用事件类型来区别不同的 SQL 操作有以下的优点：

* 不同的事件类型的审计日志记录[不同的信息](#日志记录信息)。
* 可以根据不同的事件类型来选择 TiDB 用户关心的 SQL 语句，[过滤掉不需要的审计日志](#日志过滤与规则)。

TiDB 审计日志有以下事件类型：

| **事件类型** | **描述** |
|---|---|
| `CONNECTION` | 记录所有与连接相关的操作，包括握手、建立连接、断开连接、重设连接、变更用户等 |
| `CONNECT` | 记录连接过程中的握手操作。属于 `CONNECTION` 的子类型 |
| `DISCONNECT` | 记录断开连接的操作。属于 `CONNECTION` 的子类型 |
| `CHANGE_USER` | 记录变更用户的操作。属于 `CONNECTION` 的子类型 |
| `QUERY` | 记录所有执行 SQL 语句的操作 |
| `EXECUTE` | 记录所有执行 [`EXECUTE` 语句](/sql-statements/sql-statement-execute.md)的操作。属于 `QUERY` 的子类型 |
| `QUERY_DML` | 记录所有 DML 语句的操作，包括 [`INSERT`](sql-statements/sql-statement-insert.md)、[`REPLACE`](sql-statements/sql-statement-replace.md)、[`UPDATE`](sql-statements/sql-statement-update.md)、[`DELETE`](sql-statements/sql-statement-delete.md) 和 [`LOAD DATA`](sql-statements/sql-statement-load-data.md)。属于 `QUERY` 的子类型 |
| `INSERT` | 记录所有 [`INSERT`](sql-statements/sql-statement-insert.md) 语句的操作。属于 `QUERY_DML` 的子类型 |
| `REPLACE` | 记录所有 [`REPLACE`](sql-statements/sql-statement-replace.md) 语句的操作。属于 `QUERY_DML` 的子类型 |
| `UPDATE` | 记录所有 [`UPDATE`](sql-statements/sql-statement-update.md) 语句的操作。属于 `QUERY_DML` 的子类型 |
| `DELETE` | 记录所有 [`DELETE`](sql-statements/sql-statement-delete.md) 语句的操作。属于 `QUERY_DML` 的子类型 |
| `LOAD DATA` | 记录所有 [`LOAD DATA`](sql-statements/sql-statement-load-data.md) 语句的操作。属于 `QUERY_DML` 的子类型 |
| `SELECT` | 记录所有 [`SELECT`](sql-statements/sql-statement-select.md) 语句的操作。属于 `QUERY` 的子类型 |
| `QUERY_DDL` | 记录所有 DDL 语句的操作。属于 `QUERY` 的子类型 |
| `AUDIT` | 记录所有 TiDB 审计日志相关设置语句的操作，包括系统变量和函数调用 |
| `AUDIT_SET_SYS_VAR` | 记录所有设置 [TiDB 审计日志相关系统变量](#审计日志相关系统变量)语句的操作。属于 `AUDIT` 的子类型 |
| `AUDIT_FUNC_CALL` | 记录所有调用 [TiDB 审计日志相关函数](#审计日志相关函数)的操作。属于 `AUDIT` 的子类型 |
| `AUDIT_ENABLE` | 记录所有[开启 TiDB 审计日志](#tidb_audit_enabled)的操作。属于 `AUDIT_SET_SYS_VAR` 的子类型 |
| `AUDIT_DISABLE` | 记录所有[关闭 TiDB 审计日志](#tidb_audit_enabled)的操作。属于 `AUDIT_SET_SYS_VAR` 的子类型 |

### 日志记录信息

#### 通用信息

所有类型的审计日志均包含的日志信息

| **信息** | **描述** |
|---|---|
| | |

#### 连接信息

| **信息** | **描述** |
|---|---|
| | |

#### 表操作信息

| **信息** | **描述** |
|---|---|
| | |

#### 审计操作信息

| **信息** | **描述** |
|---|---|
| | |

### 日志过滤与规则

### 日志文件格式

### 日志轮替

[日志轮替（log rotation）](https://zh.wikipedia.org/wiki/%E6%97%A5%E5%BF%97%E8%BD%AE%E6%9B%BF)

### 日志文件保留数量与时间

### 日志脱敏

## 审计日志相关系统表

### `mysql.audit_log_filters`

### `mysql.audit_log_filter_rules`

## 审计日志相关系统变量

### `tidb_audit_enabled`

### `tidb_audit_log`

### `tidb_audit_log_format`

### `tidb_audit_log_max_size`

### `tidb_audit_log_max_lifetime`

### `tidb_audit_log_reserved_backups`

### `tidb_audit_log_reserved_days`

### `tidb_audit_redact_log`

## 审计日志相关函数

### `audit_log_rotate`

### `audit_log_create_filter`

### `audit_log_remove_filter`

### `audit_log_create_rule`

### `audit_log_remove_rule`

### `audit_log_enable_rule`

### `audit_log_disable_rule`

## 审计日志相关权限

### `AUDIT_ADMIN`

### `RESTRICTED_VARIABLES_ADMIN`