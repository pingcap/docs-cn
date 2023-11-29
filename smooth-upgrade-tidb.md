---
title: TiDB Smooth Upgrade
summary: This document introduces the smooth upgrade feature of TiDB, which supports upgrading TiDB clusters without manually canceling DDL operations.
---

# TiDB Smooth Upgrade

This document introduces the smooth upgrade feature of TiDB, which supports upgrading TiDB clusters without manually canceling DDL operations.

Starting from v7.1.0, when you upgrade TiDB to a later version, TiDB supports smooth upgrade. This feature removes the limitations during the upgrade process and provides a more user-friendly upgrade experience. Note that you need to ensure that there are no user-initiated DDL operations during the upgrade process.

## Supported versions

Depending on whether the feature needs to be controlled by a switch, there are two ways to use smooth upgrade:

- The feature is enabled by default and does not need to be controlled by a switch. Currently, the versions that support this method are v7.1.0, v7.1.1, v7.2.0, and v7.3.0. The specific supported versions are as follows:
    - Upgrade from v7.1.0 to v7.1.1, v7.2.0, or v7.3.0
    - Upgrade from v7.1.1 to v7.2.0 or v7.3.0
    - Upgrade from v7.2.0 to v7.3.0

- The feature is disabled by default, and can be enabled by sending the `/upgrade/start` request. For details, see [TiDB HTTP API](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md). The supported versions are as follows:
    - Upgrade from v7.1.2 and later v7.1 versions (that is, v7.1.x, where x >= 2) to v7.4.0 and later versions
    - Upgrade from v7.4.0 to later versions

Refer to the following table for the upgrade methods supported by specific versions:

| Original version | Upgraded version | Upgrade methods | Note |
|------|--------|-------------|-------------|
| < v7.1.0  | Any version                 | Does not support smooth upgrade. | |
| v7.1.0    | v7.1.1、v7.2.0, or v7.3.0   | Smooth upgrade is automatically supported. No additional operations are required. | Experimental feature. It might encounter the issue [#44760](https://github.com/pingcap/tidb/pull/44760). |
| v7.1.1    | v7.2.0 or v7.3.0         | Smooth upgrade is automatically supported. No additional operations are required. | Experimental feature.  |
| v7.2.0    | v7.3.0                   | Smooth upgrade is automatically supported. No additional operations are required. | Experimental feature.  |
| [v7.1.2, v7.2.0)                     | [v7.1.2, v7.2.0) | Enable smooth upgrade by sending the `/upgrade/start` HTTP request. There are two methods: [Use TiUP](#use-tiup-to-upgrade) and [Other upgrade methods](#other-upgrade-methods) | When smooth upgrade is not enabled, ensure that no DDL operations are performed during the upgrade. |
| [v7.1.2, v7.2.0) or >= v7.4.0             | >= v7.4.0 | Enable smooth upgrade by sending the `/upgrade/start` HTTP request. There are two methods: [Use TiUP](#use-tiup-to-upgrade) and [Other upgrade methods](#other-upgrade-methods)  | When smooth upgrade is not enabled, ensure that no DDL operations are performed during the upgrade. |
| v7.1.0, v7.1.1, v7.2.0, and v7.3.0     | >= v7.4.0 | Does not support smooth upgrade. | |

## Feature introduction

Before the smooth upgrade feature is introduced, there are the following limitations on DDL operations during the upgrade process:

- Running DDL operations during the upgrade process might cause undefined behavior in TiDB.
- Upgrading TiDB during the DDL operations might cause undefined behavior in TiDB.

These limitations can be summarized as that you need to ensure that there are no user-initiated DDL operations during the upgrade process. After the smooth upgrade feature is introduced, TiDB is no longer subject to this limitation during the upgrade process.

For more information, see the **Warning** content in [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md#upgrade-tidb-using-tiup).

### Upgrade steps

#### Use TiUP to upgrade

Starting from v1.14.0, TiUP automatically supports this feature. That is, you can directly use the `tiup cluster upgrade` command to upgrade TiDB clusters. Note that the `tiup cluster patch` command is not supported currently.

#### Use TiDB Operator to upgrade

Currently, this feature is not supported. It will be supported as soon as possible.

#### Other upgrade methods

You can take the following steps to upgrade TiDB manually or by using a script:

1. Send the HTTP upgrade start request to any TiDB node in the cluster: `curl -X POST http://{TiDBIP}:10080/upgrade/start`.
   * The TiDB cluster enters the **Upgrading** state.
   * The DDL operations to be performed are paused.

2. Replace the TiDB binary and perform a rolling upgrade. This process is the same as the original upgrade process.
    * The system DDL operations are performed during the upgrade process.

3. After all TiDB nodes in the cluster are upgraded successfully, send the HTTP upgrade finish request to any TiDB node: `curl -X POST http://{TiDBIP}:10080/upgrade/finish`.
    * The paused DDL operations of users are resumed.

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

### Limitation on plugins

The plugins installed in TiDB might contain DDL operations. However, during the upgrade, if the DDL operations in the plugins are performed on non-system tables, the upgrade might fail.
