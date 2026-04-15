---
title: SESSION_CONNECT_ATTRS
summary: 了解 performance_schema 表 `SESSION_CONNECT_ATTRS`。
---

# SESSION\_CONNECT\_ATTRS

`SESSION_CONNECT_ATTRS` 表提供了关于连接属性的信息。会话属性是在建立连接时由客户端发送的键值对。

常见属性：

| 属性名 | 示例 | 描述 |
|-------|-----|------|
| `_client_name` | `libmysql` | 客户端库名 |
| `_client_version` | `8.0.33` | 客户端库版本|
| `_os` | `Linux` | 操作系统 |
| `_pid` | `712927` | 进程 ID |
| `_platform` | `x86_64` | CPU 架构 |
| `program_name` | `mysqlsh` | 程序名  |

你可以通过以下方式查看 `SESSION_CONNECT_ATTRS` 表的列信息：

```sql
USE performance_schema;
DESCRIBE session_connect_attrs;
```

```
+------------------+-----------------+------+------+---------+-------+
| Field            | Type            | Null | Key  | Default | Extra |
+------------------+-----------------+------+------+---------+-------+
| PROCESSLIST_ID   | bigint unsigned | NO   |      | NULL    |       |
| ATTR_NAME        | varchar(32)     | NO   |      | NULL    |       |
| ATTR_VALUE       | varchar(1024)   | YES  |      | NULL    |       |
| ORDINAL_POSITION | int             | YES  |      | NULL    |       |
+------------------+-----------------+------+------+---------+-------+
```

你可以通过以下方式查看 `SESSION_CONNECT_ATTRS` 表中存储的会话属性信息：

```sql
USE performance_schema;
TABLE SESSION_CONNECT_ATTRS;
```

```
+----------------+-----------------+------------+------------------+
| PROCESSLIST_ID | ATTR_NAME       | ATTR_VALUE | ORDINAL_POSITION |
+----------------+-----------------+------------+------------------+
|        2097154 | _client_name    | libmysql   |                0 |
|        2097154 | _client_version | 8.5.0      |                1 |
|        2097154 | _os             | Linux      |                2 |
|        2097154 | _pid            | 1299203    |                3 |
|        2097154 | _platform       | x86_64     |                4 |
|        2097154 | program_name    | mysqlsh    |                5 |
+----------------+-----------------+------------+------------------+
```

`SESSION_CONNECT_ATTRS` 表的字段描述如下：

* `PROCESSLIST_ID`：会话的 Processlist ID。
* `ATTR_NAME`：属性名。
* `ATTR_VALUE`：属性值。
* `ORDINAL_POSITION`：属性名/属性值对的序号。

## 大小限制与截断

TiDB 使用全局系统变量 [`performance_schema_session_connect_attrs_size`](/system-variables.md#performance_schema_session_connect_attrs_size-从-v900-版本开始引入) 来控制每个会话连接属性的最大总大小。

- 默认值：`4096` 字节
- 取值范围：`[-1, 65536]`
- `-1` 表示不配置限制，TiDB 会将其视为最大 `65536` 字节。
- `0` 表示 TiDB 不会保留客户端提供的会话连接属性，禁用会话属性记录。

当总大小超过该限制时，TiDB 会截断超出的属性，并添加 `_truncated` 来表示被截断的字节数。

已接受的连接属性也会写入慢日志中的 `Session_connect_attrs` 字段，并可通过 [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md) 和 `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` 查询。若要控制写入慢日志的负载大小，可调整 `performance_schema_session_connect_attrs_size`。

此外，TiDB 还会对握手包中的连接属性负载强制施加 1 MiB 的硬性限制。若超过该硬性限制，连接将被拒绝。
