---
title: Log Redaction
summary: Learn the log redaction in TiDB components.
---

# Log Redaction

When TiDB provides detailed log information, it might print sensitive data (for example, user data) in the log, which causes data security risks. To avoid such risks, each component (TiDB, TiKV, and PD) provides a configuration item that enables log redaction to shield user data values.

## Log redaction in TiDB side

To enable log redaction in the TiDB side, set the value of [`global.tidb_redact_log`](/system-variables.md#tidb_redact_log) to `1`. This configuration value defaults to `0`, which means that log redaction is disabled.

You can use the `set` syntax to set the global variable `tidb_redact_log`:

{{< copyable "sql" >}}

```sql
set @@global.tidb_redact_log=1;
```

After the setting, all logs generated in new sessions are redacted:

```sql
create table t (a int, unique key (a));
Query OK, 0 rows affected (0.00 sec)

insert into t values (1),(1);
ERROR 1062 (23000): Duplicate entry '1' for key 't.a'
```

The error log for the `INSERT` statement above is printed as follows:

```
[2020/10/20 11:45:49.539 +08:00] [INFO] [conn.go:800] ["command dispatched failed"] [conn=5] [connInfo="id:5, addr:127.0.0.1:57222 status:10, collation:utf8_general_ci,  user:root"] [command=Query] [status="inTxn:0, autocommit:1"] [sql="insert into t values ( ? ) , ( ? )"] [txn_mode=OPTIMISTIC] [err="[kv:1062]Duplicate entry '?' for key 't.a'"]
```

From the error log above, you can see that all sensitive information is shielded using `?` after `tidb_redact_log` is enabled. In this way, data security risks are avoided.

## Log redaction in TiKV side

To enable log redaction in the TiKV side, set the value of [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408) to `true`. This configuration value defaults to `false`, which means that log redaction is disabled.

## Log redaction in PD side

To enable log redaction in the PD side, set the value of [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50) to `true`. This configuration value defaults to `false`, which means that log redaction is disabled.

## Log redaction in TiFlash side

To enable log redaction in the TiFlash side, set both the [`security.redact_info_log`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) value in tiflash-server and the [`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) value in tiflash-learner to `true`. Both configuration values default to `false`, which means that log redaction is disabled.
