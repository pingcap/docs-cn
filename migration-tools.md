---
title: TiDB Migration Tools Overview
summary: Learn an overview of the TiDB migration tools.
---

# TiDB Migration Tools Overview

TiDB provides multiple data migration tools for different scenarios such as full data migration, incremental data migration, backup and restore, and data replication.

This document introduces the user scenarios, supported upstreams and downstreams, advantages, and limitations of these tools. You can choose the right tool according to your needs.

<!--The following diagram shows the user scenario of each migration tool.

!TiDB Migration Tools media/migration-tools.png-->

## [TiDB Data Migration (DM)](/dm/dm-overview.md)

- **User scenario**: Data migration from MySQL-compatible databases to TiDB
- **Upstream**: MySQL, MariaDB, Aurora
- **Downstream**: TiDB
- **Advantages**:
    - A convenient and unified data migration task management tool that supports full data migration and incremental replication
    - Support filtering tables and operations
    - Support shard merge and migration
- **Limitation**: Data import speed is roughly the same as that of TiDB Lightning's [logical import mode](/tidb-lightning/tidb-lightning-logical-import-mode.md), and a lot lower than that of TiDB Lightning's [physical import mode](/tidb-lightning/tidb-lightning-physical-import-mode.md). So it is recommended to use DM to migrate full data with a size of less than 1 TiB.

## [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)

- **User scenario**: Full data import into TiDB
- **Upstream (the imported source file)**:
    - Files exported from Dumpling
    - Parquet files exported by Amazon Aurora or Apache Hive
    - CSV files
    - Data from local disks or Amazon S3
- **Downstream**: TiDB
- **Advantages**:
    - Support quickly importing a large amount of data and quickly initializing a specific table in a TiDB cluster
    - Support checkpoints to store the import progress, so that `tidb-lightning` continues importing from where it lefts off after restarting
    - Support data filtering
- **Limitation**:
    - If [physical import mode](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md) is used for data import, during the import process, the TiDB cluster cannot provide services.
    - If you do not want the TiDB services to be impacted, perform the data import according to TiDB Lightning [logical import mode](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md).

## [Dumpling](/dumpling-overview.md)

- **User scenario**: Full data export from MySQL or TiDB
- **Upstream**: MySQL, TiDB
- **Downstream (the output file)**: SQL, CSV
- **Advantages**:
    - Support the table-filter feature that enables you to filter data easier
    - Support exporting data to Amazon S3
- **Limitation**:
    - If you want to restore the exported data to a database other than TiDB, it is recommended to use Dumpling.
    - If you want to restore the exported data to another TiDB cluster, it is recommended to use Backup & Restore (BR).

## [TiCDC](/ticdc/ticdc-overview.md)

- **User scenario**: This tool is implemented by pulling TiKV change logs. It can restore cluster data to a consistent state with any upstream TSO, and support other systems to subscribe to data changes.
- **Upstream**: TiDB
- **Downstream**: TiDB, MySQL, Kafka, Confluent
- **Advantages**: Provide TiCDC Open Protocol
- **Limitation**: TiCDC only replicates tables that have at least one valid index. The following scenarios are not supported:
    - The TiKV cluster that uses RawKV alone.
    - The DDL operation `CREATE SEQUENCE` and the `SEQUENCE` function in TiDB.

## [Backup & Restore (BR)](/br/backup-and-restore-overview.md)

- **User scenario**: Migrate a large amount of TiDB cluster data by backing up and restoring data
- **Upstream**: TiDB
- **Downstream (the output file)**: SST, backup.meta files, backup.lock files
- **Advantages**:
    - Suitable for migrating data to another TiDB cluster
    - Support backing up data to an external storage for disaster recovery
- **Limitation**:
    - When BR restores data to the upstream cluster of TiCDC or Drainer, the restored data cannot be replicated to the downstream by TiCDC or Drainer.
    - BR supports operations only between clusters that have the same `new_collations_enabled_on_first_bootstrap` value.

## [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)

- **User scenario**: Comparing data stored in the databases with the MySQL protocol
- **Upstream**: TiDB, MySQL
- **Downstream**: TiDB, MySQL
- **Advantages**: Can be used to repair data in the scenario where a small amount of data is inconsistent
- **Limitation**:
    - Online check is not supported for data migration between MySQL and TiDB.
    - JSON, BIT, BINARY, BLOB and other types of data are not supported.

## Install tools using TiUP

Since TiDB v4.0, TiUP acts as a package manager that helps you manage different cluster components in the TiDB ecosystem. Now you can manage any cluster component using a single command.

### Step 1. Install TiUP

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

Redeclare the global environment variable:

```shell
source ~/.bash_profile
```

### Step 2. Install components

You can use the following command to see all the available components:

```shell
tiup list
```

The command output lists all the available components:

```bash
Available components:
Name            Owner    Description
----            -----    -----------
bench           pingcap  Benchmark database with different workloads
br              pingcap  TiDB/TiKV cluster backup restore tool
cdc             pingcap  CDC is a change data capture tool for TiDB
client          pingcap  Client to connect playground
cluster         pingcap  Deploy a TiDB cluster for production
ctl             pingcap  TiDB controller suite
dm              pingcap  Data Migration Platform manager
dmctl           pingcap  dmctl component of Data Migration Platform
errdoc          pingcap  Document about TiDB errors
pd-recover      pingcap  PD Recover is a disaster recovery tool of PD, used to recover the PD cluster which cannot start or provide services normally
playground      pingcap  Bootstrap a local TiDB cluster for fun
tidb            pingcap  TiDB is an open source distributed HTAP database compatible with the MySQL protocol
tidb-lightning  pingcap  TiDB Lightning is a tool used for fast full import of large amounts of data into a TiDB cluster
tiup            pingcap  TiUP is a command-line component management tool that can help to download and install TiDB platform components to the local system
```

Choose the components to install:

```shell
tiup install dumpling tidb-lightning
```

> **Note:**
>
> To install a component of a specific version, use the `tiup install <component>[:version]` command.

### Step 3. Update TiUP and its components (optional)

It is recommended to see the release log and compatibility notes of the new version.

```shell
tiup update --self && tiup update dm
```

## See also

- [Deploy TiUP offline](/production-deployment-using-tiup.md#deploy-tiup-offline)
- [Download and install tools in binary](/download-ecosystem-tools.md)
