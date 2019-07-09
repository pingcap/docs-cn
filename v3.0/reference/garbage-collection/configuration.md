---
title: GC Configuration
summary: Learn about GC configuration parameters.
category: reference
---

# GC Configuration

The GC (Garbage Collection) configuration and operational status are recorded in the `mysql.tidb` system table. This documents lists these parameters with their descriptions. You can use SQL statements to query or modify them. For example, the following statement adjusts the GC interval to 30 minutes:

```sql
update mysql.tidb set VARIABLE_VALUE="30m" where VARIABLE_NAME="tikv_gc_run_interval";
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
    > - The value of `tikv_gc_life_time` must be greater than that of [`max-txn-time-use`](/reference/configuration/tidb-server/configuration-file#max-txn-time-use) in the TiDB configuration file by at least 10 seconds, and must than or equal to 10 minutes.
    > - In scenarios of frequent updates, a large value (days or even months) for `tikv_gc_life_time` may cause potential issues, such as:
    >    - Larger storage use
    >    - A large amount of history data may affect performance to a certain degree, especially for range queries such as `select count(*) from t`

## `tikv_gc_mode`

- Specifies the GC mode. Possible values are:

    - `"distributed"` (default): Distributed GC mode. In the [Do GC](/reference/garbage-collection/overview.md#do-gc) step, the GC leader on the TiDB side uploads the safe point to PD. Each TiKV node obtains the safe point respectively and performs GC on all leader Regions on the current node. This mode is is supported from TiDB 3.0.

    - `"central"`: Central GC mode. In the [Do GC](/reference/garbage-collection/overview.md#do-gc) step, the GC leader sends GC requests to all Regions. This mode is adopted by TiDB 2.1 or earlier versions.

## `tikv_gc_auto_concurrency`

- Controls whether to let TiDB automatically specify the GC concurrency, or the maximum number of GC threads allowed concurrently.

    When `tikv_gc_mode` is set to `"distributed"`, GC concurrency works in the [Resolve Locks](/reference/garbage-collection/overview.md#resolve-locks) step. When `tikv_gc_mode` is set to `"central"`, it is applied to both the Resolve Locks and [Do GC](/reference/garbage-collection/overview.md#do-gc) steps.

    - `true`(default): Automatically use the number of TiKV nodes in the cluster as the GC concurrency
    - `false`: Use the value of [`tikv_gc_concurrency`](#tikv-gc-concurrency) as the GC concurrency

## `tikv_gc_concurrency`

- Specifies the GC concurrency manually. This parameter works only when you set [`tikv_gc_auto_concurrency`](#tikv-gc-auto-concurrency) to `false`.
- Default: 2
