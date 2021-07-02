---
title: 日志脱敏
summary: 了解 TiDB 各组件中的日志脱敏。
---

# 日志脱敏

TiDB 在提供详细的日志信息时，可能会把数据库敏感的数据（例如用户数据）打印出来，造成数据安全方面的风险。因此 TiDB、TiKV、PD 等组件各提供了一个配置项开关，开关打开后，会隐藏日志中包含的用户数据值。

## TiDB 组件日志脱敏

TiDB 侧的日志脱敏需要将 [`global.tidb_redact_log`](/system-variables.md#tidb_redact_log) 的值设为 `1`。该变量值默认为 `0`，即关闭脱敏。

可以通过 `set` 语法，设置全局系统变量 `tidb_redact_log`，示例如下：

```sql
set @@global.tidb_redact_log=1;
```

设置后，所有新 session 产生的日志都会脱敏：

```sql
create table t (a int, unique key (a));
Query OK, 0 rows affected (0.00 sec)

insert into t values (1),(1);
ERROR 1062 (23000): Duplicate entry '1' for key 'a'
```

打印出的错误日志如下：

```
[2020/10/20 11:45:49.539 +08:00] [INFO] [conn.go:800] ["command dispatched failed"] [conn=5] [connInfo="id:5, addr:127.0.0.1:57222 status:10, collation:utf8_general_ci,  user:root"] [command=Query] [status="inTxn:0, autocommit:1"] [sql="insert into t values ( ? ) , ( ? )"] [txn_mode=OPTIMISTIC] [err="[kv:1062]Duplicate entry '?' for key 'a'"]
```

从以上报错日志可以看到，开启 `tidb_redact_log` 后，报错信息里的敏感内容被隐藏掉了（目前是用问号替代）。TiDB 日志中会把敏感信息隐藏掉，以此规避数据安全风险。

## TiKV 组件日志脱敏

TiKV 侧的日志脱敏需要将 [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-从-v408-版本开始引入) 的值设为 `true`。该配置项值默认为 `false`，即关闭脱敏。

## PD 组件日志脱敏

PD 侧的日志脱敏需要将 [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-从-v50-版本开始引入) 的值设为 `true`。该配置项值默认为 `false`，即关闭脱敏。

## TiFlash 组件日志脱敏

TiFlash 侧的日志脱敏需要将 tiflash-server 中 [`security.redact_info_log`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) 配置项的值以及 tiflash-learner 中 [`security.redact-info-log`](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) 配置项的值均设为 `true`。两配置项默认值均为 `false`，即关闭脱敏。
