---
title: TiDB 审计日志
summary: 了解使用 TiDB 的审计日志功能。
aliases: ['/docs-cn/dev/audit-log/']
---

# TiDB 审计日志

审计日志功能是 TiDB 的企业版特性，可以灵活地记录对 TiDB 服务器的各种操作，方便安全、运维人员查看 SQL 操作日志，及时发现问题。

> **注意：**
>
> TiDB 社区版用户无法使用审计日志功能，请[选择 TiDB 企业版](https://cn.pingcap.com/product/#SelectProduct)以使用该功能并享受商业专家的支持服务。

## 概念介绍

### 日志事件

TiDB 审计日志根据 SQL 语句的类型将 SQL 操作分为若干事件类型（Event Class）。一条 SQL 语句对应一种或多种事件类型，一种事件类型可以是另一种事件类型的子类型（Subclass），比如：

* `SELECT * FROM t` 对应的事件类型是 `QUERY` 和 `SELECT`。`SELECT` 属于 `QUERY` 的子类型
* `INSERT INTO t VALUES (1),(2),(3)` 对应的事件类型是 `QUERY`、`QUERY_DML` 和 `INSERT`。`INSERT` 属于 `QUERY_DML` 的子类型，`QUERY_DML` 属于 `QUERY` 的子类型
* `SET GLOBAL tidb_audit_enabled = 1` 对应的事件类型是 `AUDIT`、`AUDIT_SET_SYS_VAR` 和 `AUDIT_ENABLE`。`AUDIT_ENABLE` 属于 `AUDIT_SET_SYS_VAR` 的子类型，`AUDIT_SET_SYS_VAR` 属于 `AUDIT` 的子类型

使用事件类型来区别不同的 SQL 操作有以下的优点：

* 不同的事件类型的审计日志记录[不同的信息](#日志记录信息)，比如 `CONNETION` 事件需要记录客户端的 IP 地址、端口等信息，而 `SELECT` 事件则需要记录查询的 SQL 语句、访问的表等信息。
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

所有类型的审计日志均包含以下日志信息：

| **信息** | **描述** |
|---|---|
| ID | 标识该操作审计记录的唯一标识符 |
| EVENT | 该操作审计记录对应的事件类型，多个事件类型之间以逗号（`,`）分隔 |
| USER | 该操作审计记录对应的用户名 |
| ROLES | 上述用户所拥有的角色列表 |
| CONNECTION_ID | 上述用户所在连接的标识符 |
| TABLES | 该操作审计记录相关的所有表的表名 |
| STATUS_CODE | 该操作审计记录对应的操作是否成功，`1` 表示成功，`0` 表示失败 |
| REASON | 该操作审计记录对应的错误信息，仅当该操作出现错误时才会记录该信息 |

#### SQL 语句信息

当事件类型为 `QUERY` 或其子类型时，审计日志将记录以下信息：

| **信息** | **描述** |
|---|---|
| CURRENT_DB | 当前选择的数据库名 |
| SQL_TEXT | 记录执行的 SQL 语句。如果已经开启日志脱敏，则记录脱敏后的 SQL 语句。 |
| EXECUTE_PARAMS | 记录传入 [`EXECUTE` 语句](/sql-statements/sql-statement-execute.md)的参数。仅当事件类型包含 `EXECUTE`，且未开启日志脱敏时才会记录该信息 |
| AFFECTED_ROWS | 该 SQL 语句影响的行数，仅当事件类型包含 `QUERY_DML` 时记录该信息 |

> **注意：**
>
> 对于包含用户密码的 SQL 语句（`CREATE USER ... IDENTIFIED BY ...`, `SET PASSWORD` 和 `ALTER USER ... IDENTIFIED BY ...`），无论是否开启日志脱敏，审计日志均会对其进行脱敏。
>
> 但是如果一条包含密码的 SQL 语句出现语法错误，则密码信息可能泄漏在 REASON 信息中。
> 一个避免此泄漏风险的方法是，使用过滤器将出现错误的 SQL 语句（即 STATUS_CODE 为 `0`、EVENT 包含 `QUERY` 的记录）从审计日志中过滤掉。

#### 连接信息

当事件类型为 `CONNECTION` 或其子类型时，审计日志将记录以下信息：

| **信息** | **描述** |
|---|---|
| CURRENT_DB | 当前选择的数据库名。当事件类型包含 `DISCONNECT` 时，不记录该信息 |
| CONNECTION_TYPE | 连接的类型，包括 `Socket`、`UnixSocket` 和 `SSL/TLS` |
| PID | 当前连接的[进程 ID](https://zh.wikipedia.org/wiki/%E8%BF%9B%E7%A8%8BID) |
| SERVER_VERSION | 当前连接的 TiDB 服务器版本 |
| SSL_VERSION | 当前连接使用的 SSL 版本 |
| HOST_IP | 当前连接的 TiDB 服务器的 IP 地址 |
| HOST_PORT | 当前连接的 TiDB 服务器的端口 |
| CLIENT_IP | 当前连接的客户端的 IP 地址 |
| CLIENT_PORT | 当前连接的客户端的端口 |

#### 审计操作信息

当事件类型为 `AUDIT` 或其子类型时，审计日志将记录以下信息：

| **信息** | **描述** |
|---|---|
| AUDIT_OP_TARGET | TiDB 审计日志相关设置的对象，包括系统变量（比如 `tidb_audit_enabled`）和函数（比如 `audit_log_create_filter`） |
| AUDIT_OP_ARGS | TiDB 审计日志相关设置的参数，比如开启审计日志功能时设置 `tidb_audit_enabled` 为 `ON`；或者通过 `audit_log_remove_filter` 删除过滤器时，参数为删除的过滤器的名字 |

### 日志过滤与规则

TODO

### 日志文件格式

TODO
### 日志轮替

TODO

[日志轮替（log rotation）](https://zh.wikipedia.org/wiki/%E6%97%A5%E5%BF%97%E8%BD%AE%E6%9B%BF)

### 日志文件保留数量与时间

TODO

### 日志脱敏

TODO

## 审计日志相关系统表

### `mysql.audit_log_filters`

记录审计日志可用的过滤器：

* `FILTER_NAME`：过滤器名
* `CONTENT`：以 JSON 为格式的过滤器内容

```sql
desc mysql.audit_log_filters;
```

```
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| FILTER_NAME | varchar(128) | NO   | PRI  | NULL    |       |
| CONTENT     | text         | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
```

以下查询及其结果表示，当前有两个过滤器：

* `all_query` 选出所有 `QUERY` 事件类型的日志记录
* `all_connect` 选出所有 `CONNECT` 事件类型的日志记录

```sql
select * from mysql.audit_log_filters;
```

```
+-------------+---------------------------------------+
| FILTER_NAME | CONTENT                               |
+-------------+---------------------------------------+
| all_query   | {"filter":[{"class":["QUERY"]}]}       |
| all_connect | {"filter":[{"class":["CONNECT"]}]}     |
+-------------+---------------------------------------+
```

### `mysql.audit_log_filter_rules`

记录审计日志的过滤规则，即用户与过滤器的对应关系。该表中一条记录代表一条过滤规则。

一个用户可以使用多个过滤器，一个过滤器也可以被多个用户使用。

* `USER`：该过滤规则作用的用户，包括用户名与用户地址
* `FILTER_NAME`：该过滤规则使用的过滤器名，必须是 `mysql.audit_log_filters` 中存在的过滤器
* `ENABLED`：是否开启该过滤规则

```sql
desc mysql.audit_log_filter_rules;
```

```
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| USER        | varchar(64)  | NO   | PRI  | NULL    |       |
| FILTER_NAME | varchar(128) | NO   | PRI  | NULL    |       |
| ENABLED     | tinyint(4)   | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
```

以下查询及其结果表示，当前有两条过滤规则：

* 过滤规则 1 对所有用户开启过滤器 `all_query`，且当前开启该过滤规则
* 过滤规则 2 对所有名为 `u` 的用户开启过滤器 `all_connect`，且当前关闭该过滤规则

```sql
select * from mysql.audit_log_filter_rules;
```

```
+------+-------------+---------+
| USER | FILTER_NAME | ENABLED |
+------+-------------+---------+
| %@%  | all_query   |       1 |
| u@%  | all_connect |       0 |
+------+-------------+---------+
```

## 审计日志相关系统变量

### `tidb_audit_enabled`

TODO

### `tidb_audit_log`

TODO

### `tidb_audit_log_format`

TODO

### `tidb_audit_log_max_size`

TODO

### `tidb_audit_log_max_lifetime`

TODO

### `tidb_audit_log_reserved_backups`

TODO

### `tidb_audit_log_reserved_days`

TODO

### `tidb_audit_redact_log`

TODO

## 审计日志相关函数

### `audit_log_rotate`

TODO

### `audit_log_create_filter`

TODO

### `audit_log_remove_filter`

TODO

### `audit_log_create_rule`

TODO

### `audit_log_remove_rule`

TODO

### `audit_log_enable_rule`

TODO

### `audit_log_disable_rule`

TODO

## 审计日志相关权限

### `AUDIT_ADMIN`

TODO

### `RESTRICTED_VARIABLES_ADMIN`

TODO