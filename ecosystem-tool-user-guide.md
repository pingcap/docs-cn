---
title: TiDB Ecosystem Tools Overview
aliases: ['/docs/dev/ecosystem-tool-user-guide/','/docs/dev/reference/tools/user-guide/','/docs/dev/how-to/migrate/from-mysql/','/docs/dev/how-to/migrate/incrementally-from-mysql/','/docs/dev/how-to/migrate/overview/']
---

# TiDB Ecosystem Tools Overview

This document introduces the functionalities of TiDB ecosystem tools and their relationship.

## Full data export

[Dumpling](/dumpling-overview.md) is a tool for the logical full data export from MySQL or TiDB.

The following are the basics of Dumpling:

- Input: MySQL/TiDB cluster
- Output: SQL/CSV file
- Supported TiDB versions: all versions
- Kubernetes support: No

## Full data import

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) (Lightning) is a tool used for the full import of large amounts of data into a TiDB cluster. Currently, TiDB Lightning supports reading SQL dump exported via Dumpling or CSV data source.

TiDB Lightning supports three modes:

- `local`: TiDB Lightning parses data into ordered key-value pairs and directly imports them into TiKV. This mode is usually for importing a large amount of data (at the TB level) to a new cluster. During the import, the cluster cannot provide services.
- `importer`: This mode is similar to the `local` mode. To use this mode, you need to deploy an additional component `tikv-importer` to help import key-value pairs. If the target cluster is in v4.0 or later versions, it is recommended to use the `local` mode.
- `tidb`: This mode uses TiDB/MySQL as the backend, which is slower than the `local` mode and `importer` mode but can be performed online. It also supports importing data to MySQL.

The following are the basics of TiDB Lightning:

- Input data source:
    - The output file of Dumpling
    - Other compatible CSV file
- Supported TiDB versions: v2.1 or later
- Kubernetes support: Yes. See [Quickly restore data into a TiDB cluster in Kubernetes using TiDB Lightning](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/restore-data-using-tidb-lightning) for details.

> **Note:**
>
> The Loader tool is no longer maintained. For scenarios related to Loader, it is recommended that you use the `tidb` mode of TiDB Lighting instead. For details, see [TiDB Lightning TiDB backends](/tidb-lightning/tidb-lightning-backends.md#migrating-from-loader-to-tidb-lightning-tidb-backend).

## Backup and restore

[Backup & Restore](/br/backup-and-restore-tool.md) (BR) is a command-line tool for distributed backup and restore of the TiDB cluster data. BR can effectively back up and restore TiDB clusters of huge data volume.

The following are the basics of BR:

- [Input and output data source](/br/backup-and-restore-tool.md#types-of-backup-files): SST + `backupmeta` file
- Supported TiDB versions: v3.1 and v4.0
- Kubernetes support: Yes. See [Back up Data to S3-Compatible Storage Using BR](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/backup-to-aws-s3-using-br) and [Restore Data from S3-Compatible Storage Using BR](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/restore-from-aws-s3-using-br) for details.

## Incremental data replication

[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) is a tool that collects binlog for TiDB clusters and provides near real-time sync and backup. It can be used for incremental data replication between TiDB clusters, such as making a TiDB cluster the secondary cluster of the primary TiDB cluster.

The following are the basics of TiDB Binlog:

- Input/Output:
    - Input: TiDB cluster
    - Output: TiDB cluster, MySQL, Kafka or incremental backup files
- Supported TiDB versions: v2.1 or later
- Kubernetes support: Yes. See [TiDB Binlog Cluster Operations](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/deploy-tidb-binlog) and [TiDB Binlog Drainer Configurations in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/configure-tidb-binlog-drainer) for details.

### Data migration

[TiDB Data Migration](https://docs.pingcap.com/tidb-data-migration/v1.0) (DM) is an integrated data replication task management platform that supports the full data migration and the incremental data migration from MySQL/MariaDB to TiDB.

The following are the basics of DM:

- Input: MySQL/MariaDB
- Output: TiDB cluster
- Supported TiDB versions: all versions
- Kubernetes support: No, under development

If the data volume is below the TB level, it is recommended to migrate data from MySQL/MariaDB to TiDB directly using DM. The migration process includes the full data import and export and the incremental data replication.

If the data volume is at the TB level, take the following steps:

1. Use [Dumpling](/dumpling-overview.md) to export the full data from MySQL/MariaDB.
2. Use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import the data exported in Step 1 to the TiDB cluster.
3. Use DM to migrate the incremental data from MySQL/MariaDB to TiDB.

> **Note:**
>
> The Syncer tool is no longer maintained. For scenarios related to Syncer, it is recommended that you use DM's incremental task mode instead.
