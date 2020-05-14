---
title: TiDB Ecosystem Tools User Guide
category: reference
aliases: ['/docs/dev/reference/tools/user-guide/','/docs/dev/how-to/migrate/from-mysql/','/docs/dev/how-to/migrate/incrementally-from-mysql/','/docs/dev/how-to/migrate/overview/']
---

# TiDB Ecosystem Tools User Guide

The TiDB ecosystem has a wealth of tools for data migration, backup & restore for users with different use cases to choose from. 

- Some of the functionalities of these tools might overlap. For example, TiDB Loader, TiDB Lightning and TiDB DM can all do full data loading. 
- Some of the tools might have evolved. For example, TiDB Binlog will be evolved to CDC (Change Data Capture). 
- Some of the tools are designed to support specific TiDB versions and the others might be deprecated as user requirements change.

This guide is specifically designed to help you better understand these tools and therefore make an informed decision while choosing these tools to support your business.

## Data import (restore or data replication)

### Full data import tools

#### TiDB Lightning

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) (Lightning) is a tool used for the fast full import of large amounts of data into a TiDB cluster. Currently, TiDB Lightning supports reading SQL dump exported via Mydumper or CSV data source.

TiDB Lightning supports two back ends: "Importer" and "TiDB". It determines how tidb-lightning delivers data into the target cluster. The two back ends are as follows:

1. The default one is [`Importer` back end](/tidb-lightning/tidb-lightning-overview.md). When using `Importer` as the back end, the cluster cannot provide normal services during the import process. It is used for a large amount of data importing (TB).
2. The second one is [`TiDB` back end](/tidb-lightning/tidb-lightning-tidb-backend.md) (just work as [Loader](#tidb-loader-to-be-deprecated)). It is much slower than `Importer` back end model. But the cluster could serve the application during the import process. It is used to handle tens/hundreds of GB data.

The following are the basics of TiDB Lightning:

- Input data source:
    - The output file of Mydumper
    - CSV file
- Supported TiDB versions: v2.1 or later
- Kubernetes support: Yes. See [Quickly restore data into a TiDB cluster in Kubernetes using TiDB Lightning](https://pingcap.com/docs/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning/) for details.

#### BR (beta)

[BR](/br/backup-and-restore-tool.md) (Backup & Restore) is a command-line tool for distributed backup and restoration of the TiDB cluster data. Compared with Mydumper/Loader/Lightning, BR is more suitable for scenarios of huge data volume.

The following are the basics of BR:

- Input data source: The output file of BR
- Supported TiDB versions: v3.1 or later
- Kubernetes support: Yes. The document is WIP.

#### TiDB Loader (to be deprecated)

> **Note:**
> 
> TiDB Loader is to be deprecated and replaced with [Lightning](/tidb-lightning/tidb-lightning-tidb-backend.md#migrating-from-loader-to-tidb-lightning-tidb-back-end).

[TiDB Loader](/loader-overview.md) is a lightweight full-data importing tool for TiDB. It reads the output file of Mydumper and loads the data into TiDB.

The following are the basics of Loader:

- Input data source: Mydumper’s output file
- Supported TiDB versions: all versions
- Kubernetes support: Yes. See [Backup and restore](https://pingcap.com/docs/tidb-in-kubernetes/stable/backup-and-restore-using-helm-charts/) for details.

### Incremental data import tools

#### Syncer (deprecated)

[Syncer](/syncer-overview.md) is a tool used to import data incrementally. It acts as a MySQL slave to read binlog from MySQL/MariaDB master and replicate the binlog to the downstream. It is recommended to use [TiDB Data Migration](#tidb-data-migration) to replace Syncer.

The following are the basics of Syncer:

- Input data source: MySQL/MariaDB binlog service
- Supported TiDB versions: all versions
- Kubernetes support: No

### Full and incremental data import tools

#### TiDB Data Migration

[TiDB Data Migration](https://pingcap.com/docs/tidb-data-migration/stable/) (DM) is an integrated data replication task management platform that supports the full data migration and the incremental data migration from MySQL/MariaDB into TiDB. It can help to reduce the operations cost and simplify the troubleshooting process. 

For the full data migration, it uses an embedded Loader and an embedded Mydumper. For the incremental data migration, it uses Syncer as its kernel.

The following are the basics of DM:

- Input data source: MySQL/MariaDB master host/port
- Supported TiDB versions: all versions
- Kubernetes support: No, under development (the estimated time is 2020 Q2)

## Data export (backup)

### Full data export tools

#### Mydumper

[Mydumper](/mydumper-overview.md) is a tool to create a logical full backup for TiDB.

The following are the basics of Mydumper:

- Input/Output
    - Input: TiDB/MySQL host:port 
    - Output: schema and insert statements file
- Supported TiDB versions: all versions
- Kubernetes support: Yes. See [Backup and Restore](https://pingcap.com/docs/tidb-in-kubernetes/stable/backup-and-restore-using-helm-charts/) for details.

#### BR (beta)

[BR](/br/backup-and-restore-tool.md) (Backup & Restore) is a command-line tool for distributed backup and restoration of the TiDB cluster data. Compared with Mydumper/loader, BR is more suitable for scenarios of huge data volume.

The following are the basics of BR:

- Input/Output
    - Input: TiDB cluster
    - Output: Full backup file
- Supported TiDB versions: v3.1 or v4.0
- Kubernetes support: Yes. The document is WIP.

### Incremental data export tools

#### TiDB Binlog

[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) is a system that collects binlog for TiDB clusters and provides tools for near real-time sync and backup.

The following are the basics of TiDB Binlog:

- Input/Output:
    - Input: TiDB Cluster
    - Output: MySQL, TiDB, Kafka or incremental backup files
- Supported TiDB versions: v2.1 or later
- Kubernetes support: Yes. See [TiDB Binlog Cluster Operations](https://pingcap.com/docs/tidb-in-kubernetes/stable/deploy-tidb-binlog/) and [TiDB Binlog Drainer Configurations in Kubernetes](https://pingcap.com/docs/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer/) for details.

#### CDC (Beta, under development, ETA May/June 2020 with TiDB 4.0)

[CDC](/ticdc/ticdc-overview.md) (Change Data Capture) is a system that collects changelog for key value pairs in TiKV and outputs to downstream systems in row changed order.

- Input/Output: 
    - Input: TiDB Cluster
    - Output: MySQL, TiDB, Kafka or incremental backup files
- Supported TiDB versions: v4.0
- Kubernetes support: On the development road map, ETA Q2 2020

## Recommended tools for TiDB versions

### Recommended tools for TiDB 3.0 or earlier

- MySQL full data backup: use Mydumper
- MySQL full data import to TiDB:
    - TB scale: use TiDB Lightning
    - Sub-TB scale: use DM
- MySQL incremental data sync to TiDB: use DM
- TiDB full data backup: use Mydumper
- TiDB full data restore:
    - TB scale: use TiDB Lightning
    - Sub-TB scale: use TiDB Lightning
- TiDB incremental backup & restore: use TiDB-Binlog

### Recommended tools for TiDB 3.1

- MySQL full data backup: use Mydumper
- MySQL full data import to TiDB:
    - TB scale: use TiDB Lightning
    - Sub-TB scale: use DM
- MySQL incremental data sync to TiDB: use DM
- TiDB full data backup: use BR
- TiDB full data restore: use BR
- TiDB incremental backup & restore: use TiDB-Binlog

### Recommended tools for TiDB 4.0

- MySQL full data backup: use Mydumper
- MySQL full data import to TiDB:
    - TB scale: use TiDB Lightning
    - Sub-TB scale: use DM
- MySQL incremental data sync to TiDB: use DM
- TiDB full data backup: use BR
- TiDB full data restore: use BR
- TiDB incremental backup & restore: use CDC

## Tools evolution roadmap 

- TiDB Full Data Backup:
    - Mydumper -> BR
    - Mydumper -> [dumpling](https://github.com/pingcap/dumpling) (under development, replace Lighting in lightweight scenarios)
- TiDB Full Data Restore:
    - Loader -> Lightning -> BR
- MySQL Data Migration:
    - Mydumper/Loader + Syncer  -> DM (in the next step, we will integrate Lightning into DM)
- TiDB Incremental Data Migration:
    - TiDB Binlog -> CDC

## Full-path data migration solution for TiDB 3.0, 3.1 and 4.0

TiDB 3.0 is the recommended version and is also the most widely adopted version. In addition, TiDB 3.1 GA and 4.0 GA will be released this year. The following sections will cover how to migrate data from MySQL to TiDB, between TiDB clusters, and from TiDB to MySQL for each version, as well as how to back up and restore data.

### For TiDB 3.0

#### Migrating MySQL data to TiDB

If the MySQL data volume is in TBs:

- Use Mydumper to export MySQL full data as a backup
- Use Lightning to import the full MySQL backup data into TiDB cluster
- Use DM to replicate incremental MySQL data to TiDB

If the MySQL data volume is in GBs:

- Use DM to migrate MySQL data to TiDB for both full and incremental data import

#### Data replication between TiDB/MySQL clusters

You can use TiDB Binlog to replicate data between TiDB clusters. You can also use TiDB Binlog to replicate data to the downstream MySQL cluster.

#### Full backup and restore of the data in TiDB/MySQL clusters

- Use the Mydumper tool for full data backup 
- Use the Lightning tool with `tidb` backend for full data restore

### For TiDB 3.1

#### Migrating MySQL data to TiDB

If the MySQL data volume is in TBs:

- Use Mydumper to export MySQL full data as a backup
- Use Lightning to import the full MySQL backup data into TiDB cluster
- Use DM to replicate incremental MySQL data to TiDB

If the MySQL data volume is in GBs:

- Use DM to migrate MySQL data to TiDB for both full and incremental data import

#### Data replication between TiDB/MySQL clusters

You can use TiDB Binlog to replicate data between TiDB clusters. You can also use TiDB Binlog to replicate data to the downstream MySQL cluster.

#### Full backup and restore of the data in TiDB/MySQL clusters

To restore data to a TiDB cluster:

- Use the BR tool for both full data backup and full data restore

To restore data to a MySQL cluster:

- Use the Mydumper tool for full data backup
- Use the Lightning tool with `tidb` backend for full data restore

### For TiDB 4.0

#### Migrating MySQL data to TiDB

If the MySQL data volume is in TBs:

- Use Mydumper to export MySQL full data as a backup
- Use Lightning to import full MySQL backup data into TiDB cluster
- Use DM to replicate incremental MySQL data to TiDB

If the MySQL data volume is in GBs:

- Use DM to migrate MySQL data to TiDB for both full and incremental data import

#### Data replication between TiDB/MySQL clusters

You can use the TiDB CDC tool to replicate data between TiDB clusters. You can also use the CDC tool to replicate data to the downstream MySQL cluster.

#### Full backup and restore of the data in TiDB/MySQL clusters

To restore data to a TiDB cluster:

- Use the BR tool for both full data backup and full data restore

To restore data to a MySQL cluster:

- Use the Mydumper tool for full data backup
- Use the Lightning tool with `tidb` backend for full data restore
