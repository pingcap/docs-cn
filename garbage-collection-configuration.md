---
title: GC Configuration
summary: Learn about GC configuration parameters.
aliases: ['/docs/dev/garbage-collection-configuration/','/docs/dev/reference/garbage-collection/configuration/']
---

# GC Configuration

The GC (Garbage Collection) configuration and operational status are recorded in the `mysql.tidb` system table. You can use SQL statements to query or modify them:

{{< copyable "sql" >}}

```sql
select VARIABLE_NAME, VARIABLE_VALUE from mysql.tidb where VARIABLE_NAME like "tikv_gc%";
```

```sql
+--------------------------+----------------------------------------------------------------------------------------------------+
| VARIABLE_NAME            | VARIABLE_VALUE                                                                                     |
+--------------------------+----------------------------------------------------------------------------------------------------+
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
> - `tikv_gc_last_run_time`: The duration of the latest GC (updated at the beginning of each round of GC)
> - `tikv_gc_safe_point`: The current safe point (updated at the beginning of each round of GC)

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
    > - In scenarios of frequent updates, a large value (days or even months) for `tikv_gc_life_time` may cause potential issues, such as:
    >     - Larger storage use
    >     - A large amount of history data may affect performance to a certain degree, especially for range queries such as `select count(*) from t`
    > - If there is any transaction that has been running longer than `tikv_gc_life_time`, during GC, the data since `start_ts` is retained for this transaction to continue execution. For example, if `tikv_gc_life_time` is configured to 10 minutes, among all transactions being executed, the transaction that starts earliest has been running for 15 minutes, GC will retain data of the recent 15 minutes.

## `tikv_gc_mode`

- Specifies the GC mode. Possible values are:

    - `"distributed"` (default): Distributed GC mode. In the [Do GC](/garbage-collection-overview.md#do-gc) step, the GC leader on the TiDB side uploads the safe point to PD. Each TiKV node obtains the safe point respectively and performs GC on all leader Regions on the current node. This mode is is supported from TiDB 3.0.

    - `"central"`: Central GC mode. In the [Do GC](/garbage-collection-overview.md#do-gc) step, the GC leader sends GC requests to all Regions. This mode is adopted by TiDB 2.1 or earlier versions.

## `tikv_gc_auto_concurrency`

- Controls whether to let TiDB automatically specify the GC concurrency, or the maximum number of GC threads allowed concurrently.

    When `tikv_gc_mode` is set to `"distributed"`, GC concurrency works in the [Resolve Locks](/garbage-collection-overview.md#resolve-locks) step. When `tikv_gc_mode` is set to `"central"`, it is applied to both the Resolve Locks and [Do GC](/garbage-collection-overview.md#do-gc) steps.

    - `true`(default): Automatically use the number of TiKV nodes in the cluster as the GC concurrency
    - `false`: Use the value of [`tikv_gc_concurrency`](#tikv_gc_concurrency) as the GC concurrency

## `tikv_gc_concurrency`

- Specifies the GC concurrency manually. This parameter works only when you set [`tikv_gc_auto_concurrency`](#tikv_gc_auto_concurrency) to `false`.
- Default: 2

## `tikv_gc_scan_lock_mode` (**experimental feature**)

> **Warning:**
>
> Green GC is still an experimental feature. It is recommended **NOT** to use it in the production environment.

This parameter specifies the way of scanning locks in the Resolve Locks step of GC, that is, whether to enable Green GC (experimental feature) or not. In the Resolve Locks step of GC, TiKV needs to scan all locks in the cluster. With Green GC disabled, TiDB scans locks by Regions. Green GC provides the "physical scanning" feature, which means that each TiKV node can bypass the Raft layer to directly scan data. This feature can effectively mitigate the impact of GC wakening up all Regions when the [Hibernate Region](/tikv-configuration-file.md#raftstorehibernate-regions-experimental) feature is enabled, thus improving the execution speed in the Resolve Locks step.

- `"legacy"` (default): Uses the old way of scanning, that is, disable Green GC.
- `"physical"`: Uses the physical scanning method, that is, enable Green GC.

> **Note:**
>
> The configuration of Green GC is hidden. Execute the following statement when you enable Green GC for the first time:
>
> {{< copyable "sql" >}}
>
> ```sql
> insert into mysql.tidb values ('tikv_gc_scan_lock_mode', 'legacy', '');
> ```

## Notes on GC process changes

Since TiDB 3.0, some configuration options have changed with support for the distributed GC mode and concurrent Resolve Locks processing. The changes are shown in the following table:

| Version/Configuration          |  Resolve Locks          |  Do GC  |
|-------------------|---------------|----------------|
| 2.x               | Serial | Concurrent |
| 3.0 <br/> `tikv_gc_mode = centered` <br/> `tikv_gc_auto_concurrency = false` | Concurrent | Concurrent |
| 3.0 <br/> `tikv_gc_mode = centered` <br/> `tikv_gc_auto_concurrency = true` | Auto-concurrent | Auto-concurrent |
| 3.0 <br/> `tikv_gc_mode = distributed` <br/> `tikv_gc_auto_concurrency = false` | Concurrent | Distributed |
| 3.0 <br/> `tikv_gc_mode = distributed` <br/> `tikv_gc_auto_concurrency = true` <br/> (default) | Auto-concurrent | Distributed |

- Serial: requests are sent from TiDB Region by Region.
- Concurrent: requests are sent to each Region concurrently based on the number of threads specified in the `tikv_gc_concurrency`.
- Auto-concurrent: requests are sent to each Region concurrently with the number of TiKV nodes as concurrency value.
- Distributed: no need for TiDB to send requests to TiKV to trigger GC because each TiKV handles GC on its own.

In addition, if Green GC (experimental feature) is enabled, that is, setting the value of [`tikv_gc_scan_lock_mode`](#tikv_gc_scan_lock_mode-experimental-feature) to `physical`, the processing of Resolve Lock is not affected by the concurrency configuration above.

## GC I/O limit

TiKV supports the GC I/O limit. You can configure `gc.max-write-bytes-per-sec` to limit writes of a GC worker per second, and thus to reduce the impact on normal requests.

`0` indicates disabling this feature.

You can dynamically modify this configuration using tikv-ctl:

{{< copyable "shell-regular" >}}

```bash
tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB
```
