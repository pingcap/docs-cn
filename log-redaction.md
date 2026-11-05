---
title: 日志脱敏
summary: 了解 TiDB 各组件中的日志脱敏。
---

# 日志脱敏

TiDB 在提供详细的日志信息时，可能会把数据库敏感的数据（例如用户数据）打印出来，造成数据安全方面的风险。因此 TiDB、TiKV、PD 等组件各提供了一个配置项开关，开关打开后，会隐藏日志中包含的用户数据值。

## TiDB 组件日志脱敏

TiDB 侧的日志脱敏需要将 [`global.tidb_redact_log`](/system-variables.md#tidb_redact_log) 的值设为 `ON` 或 `MARKER`。该变量值默认为 `OFF`，即关闭脱敏。

可以通过 `set` 语法，设置全局系统变量 `tidb_redact_log`，示例如下：

```sql
set @@global.tidb_redact_log = ON;
```

设置后，所有新 session 产生的日志都会脱敏：

```sql
create table t (a int, unique key (a));
Query OK, 0 rows affected (0.00 sec)

insert into t values (1),(1);
ERROR 1062 (23000): Duplicate entry '1' for key 't.a'
```

打印出的错误日志如下：

```
[2024/07/02 11:35:32.686 +08:00] [INFO] [conn.go:1146] ["command dispatched failed"] [conn=1482686470] [session_alias=] [connInfo="id:1482686470, addr:127.0.0.1:52258 status:10, collation:utf8mb4_0900_ai_ci, user:root"] [command=Query] [status="inTxn:0, autocommit:1"] [sql="insert into `t` values ( ... )"] [txn_mode=PESSIMISTIC] [timestamp=450859193514065921] [err="[kv:1062]Duplicate entry '?' for key 't.a'"]
```

从以上报错日志可以看到，当把 `tidb_redact_log` 的值设为 `ON` 后，TiDB 日志中会把敏感信息隐藏掉（以问号 `?` 替换），以此规避数据安全风险。

此外，TiDB 还提供了 `MARKER` 选项，当设置 `tidb_redact_log` 的值为 `MARKER` 时，TiDB 会在日志中用 `‹ ›` 符号标记出敏感信息，而不是直接隐藏，以便用户能够自定义脱敏规则。

```sql
set @@global.tidb_redact_log = MARKER;
```

设置后，所有新 session 产生的日志都会对敏感信息进行标记，而不进行替换：

```sql
create table t (a int, unique key (a));
Query OK, 0 rows affected (0.07 sec)

insert into t values (1),(1);
ERROR 1062 (23000): Duplicate entry '‹1›' for key 't.a'
```

打印出的错误日志如下：

```
[2024/07/02 11:35:01.426 +08:00] [INFO] [conn.go:1146] ["command dispatched failed"] [conn=1482686470] [session_alias=] [connInfo="id:1482686470, addr:127.0.0.1:52258 status:10, collation:utf8mb4_0900_ai_ci, user:root"] [command=Query] [status="inTxn:0, autocommit:1"] [sql="insert into `t` values ( ‹1› ) , ( ‹1› )"] [txn_mode=PESSIMISTIC] [timestamp=450859185309483010] [err="[kv:1062]Duplicate entry '‹1›' for key 't.a'"]
```

从以上报错日志可以看到，当把 `tidb_redact_log` 的值设为 `MARKER` 后，TiDB 日志中会用 `‹ ›` 符号标记出敏感信息，你可以根据自己的需求自定义脱敏规则来处理日志中的敏感信息。

## TiKV 组件日志脱敏

TiKV 侧的日志脱敏需要将 [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-从-v408-版本开始引入) 的值设为 `true` 或 `"marker"`。该配置项值默认为 `false`，即关闭脱敏。

## PD 组件日志脱敏

PD 侧的日志脱敏需要将 [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-从-v50-版本开始引入) 的值设为 `true` 或 `"marker"`。从 v9.0.0 版本开始，未在配置文件中显式设置时，该配置项默认为 `true`，即开启脱敏；在 v9.0.0 版本之前，默认值为 `false`。

开启后，脱敏仅对支持脱敏的日志和输出生效，包括 PD 日志、operator 附加信息、[Online Unsafe Recovery](/online-unsafe-recovery.md) 计划和返回给客户端的部分错误信息。operator 附加信息中的 key 会显示为脱敏占位符，而非真实 key。审计（audit）日志不受此配置项影响，仍记录原始请求内容；少量其他日志仍可能包含原始 key，见 [#11406](https://github.com/tikv/pd/issues/11406)。

该配置项不支持在线修改，修改后需重启 PD 生效。TSO、Scheduling 等 PD 微服务读取同一配置，未在各自配置文件中显式设置时也默认为 `true`。TiKV 和 TiDB 的日志脱敏默认仍为关闭；排查问题时如需查看原始 key，需要分别关闭各组件的脱敏并重启对应组件。

## TiFlash 组件日志脱敏

TiFlash 侧的日志脱敏需要将 tiflash-server 中 [`security.redact_info_log`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) 配置项的值以及 tiflash-learner 中 [`security.redact-info-log`](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) 配置项的值均设为 `true` 或者 `"marker"`。两配置项默认值均为 `false`，即关闭脱敏。

## DM-worker 组件日志脱敏

DM-worker 侧的日志脱敏需要将 [`log.redact-info-log`](/dm/dm-worker-configuration-file.md#redact-info-log-从-v900-版本开始引入) 的值设为 `true`。该配置项值默认为 `false`，即关闭脱敏。
