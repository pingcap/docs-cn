---
title: TiDB Ecosystem Tools User Guide
category: reference
aliases: ['/docs/dev/how-to/migrate/from-mysql/','/docs/dev/how-to/migrate/incrementally-from-mysql/','/docs/dev/how-to/migrate/overview/']
---

# TiDB Ecosystem Tools User Guide

Currently, TiDB has multiple ecosystem tools. Some of them have overlapping functionality, and some are different versions of the same tool. This document introduces each of these tools, illustrates their relationship, and describes when to use which tool for each TiDB version.

## TiDB ecosystem tools overview

TiDB ecosystem tools can be divided into:

- Data import tools, including full import tools, backup and restore tools, incremental import tools, and so forth.
- Data export tools, including full export tools. incremental export tools, and so forth.

The two types of tools are discussed in detail below.

### Data import tools

#### Full import tool TiDB Lightning

[TiDB Lightning](/reference/tools/tidb-lightning/overview.md) is a tool used for fast full import of data into a TiDB cluster.

> **Note:**
>
> When you import data into TiDB using TiDB Lightning, there are two modes:
>
> - The default mode: Use `tikv-importer` as the backend. In this mode, the cluster can not provide normal services during the data import process. It is used when you import large amounts (TBs) of data.
> - The second mode: Use `TiDB` as the backend (similar to Loader). The import speed is slower than that in the default mode. However, the second mode supports online import.

The following are the basics of TiDB Lightning:

- Input:
    - Files output by Mydumper;
    - CSV files.
- Compatibility: Compatible with TiDB v2.1 and later versions.
- Kubernetes: Supported. See [Quickly restore data into a TiDB cluster in Kubernetes using TiDB Lightning](/tidb-in-kubernetes/maintain/lightning.md).

#### Backup and restore tool BR

[BR](/reference/tools/br/br.md) is a command-line tool used for distributed data backup and restoration for a TiDB cluster. Compared with Mydumper and Loader, BR allows you to finish backup and restore tasks with greater efficiency in scenarios of huge data volume.

The following are the basics of BR:

- [Types of backup files](/reference/tools/br/br.md#types-of-backup-files): The SST file and the `backupmeta` file.
- Compatibility: Compatible with TiDB v3.1 and v4.0 versions.
- Kubernetes: Supported. Relevant documents are on the way.

#### Incremental and full import tool TiDB Data Migration

[TiDB Data Migration (DM)](/reference/tools/data-migration/overview.md) is an tool used for data migration from MySQL/MariaDB into TiDB. It supports both the full and incremental data replication.

The following are the basics of DM:

- Input: Full data and binlog data of MySQL/MariaDB.
- Output: SQL statements written to TiDB.
- Compatibility: Compatible with all TiDB versions.
- Kubernetes: In development.

#### Full import tool Loader (Stop maintenance, not recommended)

[Loader](/reference/tools/loader.md) is a lightweight full data import tool. Data is imported into TiDB in the form of SQL statements. Currently, this tool is gradually replaced by [TiDB Lightning](#full-import-tool-tidb-lightning), see [TiDB Lightning TiDB-backend Document](/reference/tools/tidb-lightning/tidb-backend.md#migrating-from-loader-to-tidb-lightning-tidb-backend).

The following are the basics of Loader:

- Input: Files output by Mydumper.
- Output: SQL statements written to TiDB.
- Compatibility: Compatible with all TiDB versions.
- Kubernetes: Supported. See [Backup and restore](/tidb-in-kubernetes/maintain/backup-and-restore.md).

#### Incremental import tool Syncer (Stop maintenance, not recommended)

[Syncer](/reference/tools/syncer.md) is a tool used for incremental import of real-time binlog data from MySQL/MariaDB into TiDB. It is recommended to use [TiDB Data Migration](#Incremental-import-tool-tidb-data-migration) to replace Syncer.

The following are the basics of Syncer:

- Input: Binlog data of MySQL/MariaDB.
- Output: SQL statements written to TiDB.
- Compatibility: Compatible with all TiDB versions.
- Kubernetes: Not supported.

### Data export tools

#### Full export tool Mydumper

[Mydumper](/reference/tools/mydumper.md) is a MySQL community tool used for full logical backups of MySQL that also works with TiDB.

The following are the basics of Mydumper:

- Input: MySQL/TiDB clusters.
- Output: SQL files.
- Compatibility: Compatible with all TiDB versions.
- Kubernetes: Supported. See [Backup and Restore](/tidb-in-kubernetes/maintain/backup-and-restore.md).

#### Full export tool TiDB Binlog

[TiDB Binlog](/reference/tidb-binlog/overview.md) is a tool used to collect binlog data from TiDB. It provides near real-time backup and replication to downstream platforms.

The following are the basics of TiDB Binlog:

- Input: TiDB clusters.
- Output: MySQL, TiDB, Kafka or incremental backup files.
- Compatibility: Compatible with TiDB v2.1 and later versions.
- Kubernetes: Supported. See [TiDB Binlog Cluster Operations](/tidb-in-kubernetes/maintain/tidb-binlog.md) and [TiDB Binlog Drainer Configurations in Kubernetes](/tidb-in-kubernetes/reference/configuration/tidb-drainer.md).

## Tools development roadmap

To help you understand the relationships between the above tools, here is a brief introduction to TiDB ecosystem tools development roadmap.

### TiDB backup and restore

Mydumper and Loader -> BR:

Mydumper and Loader are inefficient since they back up and restore data on the logical level. BR is much more efficient because it takes advantage of TiDB features for backup and restore tasks. BR can be applied in huge data volume scenarios.

### TiDB full data restore

Loader -> TiDB Lightning:

Loader is inefficient since it performs full data restoration using SQL. TiDB Lightning imports data into TiKV directly, so it is much more efficient and can be used for fast full import of large amounts (more than TBs) of data into a new TiDB cluster.

TiDB Lightning also integrates the logical data import function of Loader and supports online data import. For details, see [TiDB Lightning TiDB-backend Document](/reference/tools/tidb-lightning/tidb-backend.md#migrating-from-loader-to-tidb-lightning-tidb-backend).

### MySQL data migration

- Mydumper, Loader and Syncer -> DM:

    It is tedious to migrate MySQL data to TiDB using Mydumper, Loader, and Syncer. DM provides an integrated data migration approach that improves usability. DM can be also used to merge the sharded schemas and tables.

- Loader -> TiDB Lightning:

    TiDB Lightning integrates the logical data import function of Loader. See [TiDB Lightning TiDB-backend document](/reference/tools/tidb-lightning/tidb-backend.md#migrating-from-loader-to-tidb-lightning-tidb-backend) for details. It is used to perform full data restoration.

## Data migration solutions

For TiDB 2.1, 3.0, and 3.1 versions, this section introduces data migration solutions in typical application scenarios.

### Full link data migration solutions for v3.0

#### Migrating MySQL data to TiDB

If the volume is more than TBs of data, the recommended migration steps are:

1. Export full MySQL data using Mydumper;
2. Import full backup data from MySQL into a TiDB cluster using TiDB Lightning;
3. Replicate the incremental data of MySQL into TiDB.

If the volume is less than TBs of data, it is recommended to migrate MySQL data to TiDB using DM (the migrating process includes full data import and incremental data replication).

#### Replication of TiDB cluster data

It is recommended that you use TiDB Binlog to replicate TiDB data to downstream TiDB/MySQL.

#### Full backup and restore of TiDB cluster data

The recommended steps are:

1. Back up full data using Mydumper;
2. Restore full data into TiDB/MySQL using TiDB Lightning.

### Full link data migration solutions for v3.1

#### Migrating MySQL data to TiDB

If the volume is more than TBs of data, the recommended migration steps are:

1. Export full MySQL data using Mydumper;
2. Import full backup data from MySQL into a TiDB cluster using TiDB Lightning;
3. Replicate the incremental data of MySQL into TiDB.

If the volume is less than TBs of data, it is recommended to migrate MySQL data to TiDB using DM (the migrating process includes full data import and incremental data replication).

#### Replication of TiDB cluster data

It is recommended that you use TiDB Binlog to replicate TiDB data to downstream TiDB/MySQL.

#### Full backup and restore of TiDB cluster data

- Restore to TiDB

    - Back up full data using BR;
    - Restore full data using BR.

- Restore to MySQL

    - Back up full data using Mydumper;
    - Restore full data using TiDB Lightning.
