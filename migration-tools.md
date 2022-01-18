---
title: TiDB Ecosystem Tools Overview
summary: Learn an overview of the TiDB ecosystem tools.
---

# TiDB Ecosystem Tools Overview

TiDB provides multiple data migration tools for different scenarios such as full data migration, incremental data migration, backup and restore, and data replication.

This document introduces the user scenarios, advantages, and limitations of these tools. You can choose the right tool according to your needs.

<!--The following diagram shows the user scenario of each migration tool.

!TiDB Migration Tools media/migration-tools.png-->

The following table introduces the user scenarios, the supported upstreams and downstreams of migration tools.

| Tool name | User scenario | Upstream (or the imported source file) | Downstream (or the output file) | Advantages | Limitation |
|:---|:---|:---|:---|:---|:---|
|  [TiDB Data Migration (DM)](/dm/dm-overview.md)| Data migration from MySQL-compatible databases to TiDB |  MySQL, MariaDB, Aurora, MySQL| TiDB   | <ul><li>A convenient and unified data migration task management tool that supports full data migration and incremental replication</li><li>Support filtering tables and operations</li><li>Support shard merge and migration</li></ul>  | Data import speed is roughly the same as that of TiDB Lighting's TiDB-backend, and much lower than that of TiDB Lighting's Local-backend. So it is recommended to use DM to migrate full data with a size of less than 1 TiB. |
| [Dumpling](/dumpling-overview.md) | Full data export from MySQL or TiDB | MySQL, TiDB| SQL, CSV  | <ul><li>Support the table-filter feature that enables you to filter data easier</li><li>Support exporting data to Amazon S3</li></ul>|<ul><li>If you want to restore the exported data to a database other than TiDB, it is recommended to use Dumpling.</li><li>If you want to restore the exported data to another TiDB cluster, it is recommended to use Backup & Restore (BR).</li></ul> |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)| Full data import into TiDB | <ul><li>Files exported from Dumpling</li><li>CSV files</li><li>Data read from local disks or Amazon S3</li></ul> | TiDB | <ul><li>Support quickly importing a large amount of data and quickly initializing a specific table in a TiDB cluster </li><li>Support checkpoints to store the import progress, so that `tidb-lightning` continues importing from where it lefts off after restarting</li><li>Support data filtering</li></ul> | <ul><li>If Local-backend is used for data import, during the import process, the TiDB cluster cannot provide services.</li><li> If you do not want the TiDB services to be impacted, perform the data import according to TiDB Lightning TiDB-backend.</li></ul> |
|[Backup & Restore (BR)](/br/backup-and-restore-tool.md) | Backup and restore for TiDB clusters with a huge data size | TiDB| SST, backup.meta files, backup.lock files|<ul><li>Suitable for restoring data to another TiDB cluster</li><li>Support backing up data to an external storage for disaster recovery</li></ul> | <ul><li>When BR restores data to the upstream cluster of TiCDC or Drainer, the restored data cannot be replicated to the downstream by TiCDC or Drainer.</li><li>BR supports operations only between clusters that have the same `new_collations_enabled_on_first_bootstrap` value.</li></ul> |
| [TiCDC](/ticdc/ticdc-overview.md)| This tool is implemented by pulling TiKV change logs. It can restore data to a consistent state with any upstream TSO, and support other systems to subscribe to data changes.|TiDB | TiDB, MySQL, Apache Pulsar, Kafka, Confluent| Provide TiCDC Open Protocol  | TiCDC only replicates tables that have at least one valid index. The following scenarios are not supported:<ul><li>the TiKV cluster that uses RawKV alone.</li><li>the DDL operation `CREATE SEQUENCE` and the `SEQUENCE` function in TiDB.</li></ul>|
|[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) | Incremental replication between TiDB clusters, such as using one TiDB cluster as the secondary cluster of another TiDB cluster | TiDB | TiDB, MySQL, Kafka, incremental backup files | Support real-time backup and restore. Back up TiDB cluster data to be restored for disaster recovery | Incompatible with some TiDB versions |
|[sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) | Comparing data stored in the databases with the MySQL protocol |TiDB, MySQL | TiDB, MySQL| Can be used to repair data in the scenario where a small amount of data is inconsistent | <ul><li>Online check is not supported for data migration between MySQL and TiDB.</li><li>JSON, BIT, BINARY, BLOB and other types of data are not supported.</li></ul> |

## Install tools using TiUP

Since TiDB v4.0, TiUP acts as a package manager that helps you manage different cluster components in the TiDB ecosystem. Now you can manage any cluster component using a single command.

### Step 1. Install TiUP

{{< copyable "shell-regular" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

Redeclare the global environment variable:

{{< copyable "shell-regular" >}}

```shell
source ~/.bash_profile
```

### Step 2. Install components

You can use the following command to see all the available components:

{{< copyable "shell-regular" >}}

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

{{< copyable "shell-regular" >}}

```shell
tiup install dumpling tidb-lightning
```

> **Note:**
>
> To install a component of a specific version, use the `tiup install <component>[:version]` command.

### Step 3. Update TiUP and its components (optional)

It is recommended to see the release log and compatibility notes of the new version.

{{< copyable "shell-regular" >}}

```shell
tiup update --self && tiup update dm
```

## See also

- [Deploy TiUP offline](/production-deployment-using-tiup.md#method-2-deploy-tiup-offline)
- [Download and install tools in binary](/download-ecosystem-tools.md)
