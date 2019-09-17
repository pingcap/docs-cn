---
title: GC Configuration
summary: Learn about GC configuration parameters.
category: reference
---

# GC Configuration

The GC (Garbage Collection) configuration and operational status are recorded in the `mysql.tidb` system table. You can use SQL statements to query or modify them:

```plain
mysql> select VARIABLE_NAME, VARIABLE_VALUE from mysql.tidb;
+--------------------------+----------------------------------------------------------------------------------------------------+
| VARIABLE_NAME            | VARIABLE_VALUE                                                                                     |
+--------------------------+----------------------------------------------------------------------------------------------------+
| bootstrapped             | True                                                                                               |
| tidb_server_version      | 33                                                                                                 |
| system_tz                | UTC                                                                                                |
| tikv_gc_leader_uuid      | 5afd54a0ea40005                                                                                    |
| tikv_gc_leader_desc      | host:tidb-cluster-tidb-0, pid:215, start at 2019-07-15 11:09:14.029668932 +0000 UTC m=+0.463731223 |
| tikv_gc_leader_lease     | 20190715-12:12:14 +0000                                                                            |
| tikv_gc_enable           | true                                                                                               |
| tikv_gc_run_interval     | 10m0s                                                                                              |
| tikv_gc_life_time        | 10m0s                                                                                              |
| tikv_gc_last_run_time    | 20190715-12:09:14 +0000                                                                            |
| tikv_gc_safe_point       | 20190715-11:59:14 +0000                                                                            |
| tikv_gc_auto_concurrency | true                                                                                               |
| tikv_gc_mode             | distributed                                                                                        |
+--------------------------+----------------------------------------------------------------------------------------------------+
13 rows in set (0.00 sec)
```

For example, the following statement makes GC keep history data for the most recent 24 hours:

```sql
update mysql.tidb set VARIABLE_VALUE="24h" where VARIABLE_NAME="tikv_gc_life_time";
```

> **Note:**
>
> In addition to the following GC configuration parameters, the `mysql.tidb` system table also contains records that store the status of the storage components in a TiDB cluster, among which GC related ones are included, as listed below:
>
> - `tikv_gc_leader_uuid`, `tikv_gc_leader_desc` and `tikv_gc_leader_lease`: Records the information of the GC leader
> - `tikv_gc_last_run_time`: The duration of the previous GC
> - `tikv_gc_safe_point`: The safe point for the current GC

## `tikv_gc_enable`

- Enables or disables GC
- Default: `true`

## `tikv_gc_run_interval`

- Specifies the GC interval, in the format of Go Duration, for example, `"1h30m"`, and `"15m"`
- Default: `"10m0s"`

## `tikv_gc_life_time`

- The time limit during which data is retained for each GC, in the format of Go Duration. When a GC happens, the current time minus this value is the safe point.
- Default: `"10m0s"`

    > **Note:**
    >
    > - The value of `tikv_gc_life_time` must be greater than that of [`max-txn-time-use`](/v3.0/reference/configuration/tidb-server/configuration-file.md#max-txn-time-use) in the TiDB configuration file by at least 10 seconds, and must than or equal to 10 minutes.
    > - In scenarios of frequent updates, a large value (days or even months) for `tikv_gc_life_time` may cause potential issues, such as:
    >     - Larger storage use
    >     - A large amount of history data may affect performance to a certain degree, especially for range queries such as `select count(*) from t`

## `tikv_gc_mode`

- Specifies the GC mode. Possible values are:

    - `"distributed"` (default): Distributed GC mode. In the [Do GC](/v3.0/reference/garbage-collection/overview.md#do-gc) step, the GC leader on the TiDB side uploads the safe point to PD. Each TiKV node obtains the safe point respectively and performs GC on all leader Regions on the current node. This mode is is supported from TiDB 3.0.

    - `"central"`: Central GC mode. In the [Do GC](/v3.0/reference/garbage-collection/overview.md#do-gc) step, the GC leader sends GC requests to all Regions. This mode is adopted by TiDB 2.1 or earlier versions.

## `tikv_gc_auto_concurrency`

- Controls whether to let TiDB automatically specify the GC concurrency, or the maximum number of GC threads allowed concurrently.

    When `tikv_gc_mode` is set to `"distributed"`, GC concurrency works in the [Resolve Locks](/v3.0/reference/garbage-collection/overview.md#resolve-locks) step. When `tikv_gc_mode` is set to `"central"`, it is applied to both the Resolve Locks and [Do GC](/v3.0/reference/garbage-collection/overview.md#do-gc) steps.

    - `true`(default): Automatically use the number of TiKV nodes in the cluster as the GC concurrency
    - `false`: Use the value of [`tikv_gc_concurrency`](#tikv_gc_concurrency) as the GC concurrency

## `tikv_gc_concurrency`

- Specifies the GC concurrency manually. This parameter works only when you set [`tikv_gc_auto_concurrency`](#tikv_gc_auto_concurrency) to `false`.
- Default: 2
