---
title: TRAFFIC REPLAY
summary: TiDB 数据库中 TRAFFIC REPLAY 的使用概况。
---

# TRAFFIC REPLAY

TiDB v9.0.0 引入了 `TRAFFIC REPLAY` 语法，用于向集群中所有 [TiProxy](/tiproxy/tiproxy-overview.md) 实例发送请求，让 TiProxy 从流量文件回放流量到 TiDB。

回放流量需要当前用户具有 `SUPER` 或 [`TRAFFIC_REPLAY_ADMIN`](/privilege-management.md#动态权限) 权限。

`TRAFFIC REPLAY` 支持以下选项：

- `USER`：（必填）指定回放时使用的 TiDB 用户名。
- `PASSWORD`：（可选）指定以上用户名的密码，默认为空字符串 `""`。
- `SPEED`：（可选）指定回放速率的倍数，范围为 `[0.1, 10]`，默认为 `1`，表示原速回放。
- `READ_ONLY`：（可选）指定是否仅回放只读 SQL 语句。`true` 表示仅回放只读 SQL 语句，`false` 表示回放只读和写入 SQL 语句。默认值为 `false`。

## 语法图

```ebnf+diagram
TrafficStmt ::=
    "TRAFFIC" "REPLAY" "FROM" stringLit TrafficReplayOptList

TrafficReplayOptList ::=
    TrafficReplayOpt
|   TrafficReplayOptList TrafficReplayOpt

TrafficReplayOpt ::=
    "USER" EqOpt stringLit
|   "PASSWORD" EqOpt stringLit
|   "SPEED" EqOpt NumLiteral
|   "READ_ONLY" EqOpt Boolean
```

## 示例

从 TiProxy 实例的本地 `/tmp/traffic` 目录回放流量，使用 TiDB 用户 `u1` 回放，其密码为 `"123456"`：

```sql
TRAFFIC REPLAY FROM "/tmp/traffic" USER="u1" PASSWORD="123456";
```

从存放在 S3 的流量文件回放流量：

```sql
TRAFFIC REPLAY FROM "s3://external/traffic?access-key=${access-key}&secret-access-key=${secret-access-key}" USER="u1" PASSWORD="123456";
```

2 倍速回放流量：

```sql
TRAFFIC REPLAY FROM "/tmp/traffic" USER="u1" PASSWORD="123456" SPEED=2;
```

仅回放只读语句，不回放写入语句：

```sql
TRAFFIC REPLAY FROM "/tmp/traffic" USER="u1" PASSWORD="123456" READONLY=true;
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [TiProxy 流量回放](/tiproxy/tiproxy-traffic-replay.md)
* [`TRAFFIC CAPTURE`](/sql-statements/sql-statement-traffic-capture.md)
* [`SHOW TRAFFIC JOBS`](/sql-statements/sql-statement-show-traffic-jobs.md)
* [`CANCEL TRAFFIC JOBS`](/sql-statements/sql-statement-cancel-traffic-jobs.md)
