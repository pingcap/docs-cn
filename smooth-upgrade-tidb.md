---
title: TiDB Smooth Upgrade
summary: This document introduces the smooth upgrade feature of TiDB, which supports upgrading TiDB clusters without manually canceling DDL operations.
---

# TiDB Smooth Upgrade

> **Warning:**
>
> Smooth upgrade is still an experimental feature.

This document introduces the smooth upgrade feature of TiDB, which supports upgrading TiDB clusters without manually canceling DDL operations.

Starting from v7.1.0, when you upgrade TiDB to a later version, TiDB supports smooth upgrade. This feature removes the limitations during the upgrade process and provides a more user-friendly upgrade experience. This feature is enabled by default and cannot be disabled.

## Feature introduction

Before the smooth upgrade feature is introduced, there are the following limitations on DDL operations during the upgrade process (see the *Warning* content in [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md#upgrade-tidb-using-tiup)):

- Running DDL operations during the upgrade process might cause undefined behavior in TiDB.
- Upgrading TiDB during the DDL operations might cause undefined behavior in TiDB.

After the smooth upgrade feature is introduced, the upgrade process is no longer subject to the preceding limitations.

During the upgrade process, TiDB automatically performs the following operations without user intervention:

1. Pause user DDL operations.
2. Perform system DDL operations for the upgrade.
3. Resume the paused user DDL operations.
4. Complete the upgrade.

The resumed DDL jobs are still executed in the order before the upgrade.

## Limitations

When using the smooth upgrade feature, note the following limitations.

### Limitations on user operations

* Before the upgrade, if there is a canceling DDL job in the cluster, that is, an ongoing DDL job is being canceled by a user, because the job in the canceling state cannot be paused, TiDB will retry canceling the job. If the retry fails, an error is reported and the upgrade is exited.

* In scenarios of using TiUP to upgrade TiDB, because TiUP upgrade has a timeout period, if the cluster has a large number of DDL jobs (more than 300) waiting in queues before the upgrade, the upgrade might fail.

* During the upgrade, the following operations are not allowed:

    * Run DDL operations on system tables (`mysql.*`, `information_schema.*`, `performance_schema.*`, and `metrics_schema.*`).
    * Manually cancel DDL jobs: `ADMIN CANCEL DDL JOBS job_id [, job_id] ...;`.
    * Import data.

### Limitations on tools

* During the upgrade, use of the following tools is not supported:

    * BR: BR might replicate the paused DDL jobs to TiDB. The paused DDL jobs cannot be automatically resumed, which might cause the DDL jobs to be stuck later.

    * DM and TiCDC: If you use DM or TiCDC to import SQL statements to TiDB during the upgrade process, and if one of the SQL statements contains DDL operations, the import operation is blocked and undefined errors might occur.
