---
title: TiDB Tools Overview
summary: Learn the tools and applicable scenarios.
aliases: ['/docs/dev/ecosystem-tool-user-guide/','/docs/dev/reference/tools/user-guide/','/docs/dev/how-to/migrate/from-mysql/','/docs/dev/how-to/migrate/incrementally-from-mysql/','/docs/dev/how-to/migrate/overview/']
---

# TiDB Tools Overview

TiDB provides a rich set of tools to help you deploy and maintain TiDB, manage data (such as data migration, backup & restore, and data comparison), and run Spark SQL on TiKV. You can select the applicable tools according to your needs.

## Deployment and operation Tools

TiDB provides TiUP and TiDB Operator to meet your deployment and operation needs in different system environments.

### Deploy and operate TiDB on physical or virtual machines - TiUP

[TiUP](/tiup/tiup-overview.md) is a TiDB package manager on physical or virtual machines. TiUP can manage multiple TiDB components such as TiDB, PD, and TiKV. To start any component in the TiDB ecosystem, you just need to execute a single line of TiUP command.

TiUP provides [TiUP cluster](https://github.com/pingcap/tiup/tree/master/components/cluster), a cluster management component written in Golang. By using TiUP cluster, you can easily perform daily database operations, including deploying, starting, stopping, destroying, scaling, and upgrading a TiDB cluster, and manage TiDB cluster parameters.

The following are the basics of TiUP:

- [Terminology and Concepts](/tiup/tiup-terminology-and-concepts.md)
- [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md)
- [Manage TiUP Components with TiUP Commands](/tiup/tiup-component-management.md)
- Applicable TiDB versions: v4.0 and later versions

### Deploy and operate TiDB on Kubernetes - TiDB Operator

[TiDB Operator](https://github.com/pingcap/tidb-operator) is an automatic operation system for managing TiDB clusters on Kubernetes. It provides full life-cycle management for TiDB including deployment, upgrades, scaling, backup, and configuration changes. With TiDB Operator, TiDB can run seamlessly in the Kubernetes clusters deployed on a public or private cloud.

The following are the basics of TiDB Operator:

- [TiDB Operator Architecture](https://docs.pingcap.com/tidb-in-kubernetes/stable/architecture)
- [Get Started with TiDB Operator on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/)
- Applicable TiDB versions: v2.1 and later versions

## Data management tools

 TiDB provides multiple data management tools, such as import and export, backup and restore, incremental data replication, and data validation.

### Data migration - TiDB Data Migration (DM)

[TiDB Data Migration](/dm/dm-overview.md) (DM) is a tool that supports full data migration and incremental data replication from MySQL/MariaDB to TiDB.

The following are the basics of DM:

- Source: MySQL/MariaDB
- Target: TiDB clusters
- Supported TiDB versions: all versions
- Kubernetes support: use [TiDB Operator](https://github.com/pingcap/tidb-operator) to deploy TiDB DM on Kubernetes.

If the data volume is less than 1 TB, it is recommended to migrate data from MySQL/MariaDB to TiDB directly using DM. The migration process includes full data migration and incremental data replication.

If the data volume is greater than 1 TB , take the following steps:

1. Use [Dumpling](/dumpling-overview.md) to export the full data from MySQL/MariaDB.
2. Use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import the data exported in Step 1 to the TiDB cluster.
3. Use TiDB DM to replicate the incremental data from MySQL/MariaDB to TiDB.

> **Note:**
>
> The Syncer tool is no longer maintained. For scenarios related to Syncer, it is recommended that you use DM to perform incremental replication.

### Full data export - Dumpling

[Dumpling](/dumpling-overview.md) supports logical full data export from MySQL or TiDB.

The following are the basics of Dumpling:

- Source: MySQL/TiDB clusters
- Output: SQL/CSV files
- Supported TiDB versions: all versions
- Kubernetes support: No

> **Note:**
>
> PingCAP previously maintained a fork of the [mydumper project](https://github.com/maxbube/mydumper) with enhancements specific to TiDB. This fork has since been replaced by [Dumpling](/dumpling-overview.md), which has been rewritten in Golang, and provides more optimizations specific to TiDB. It is strongly recommended that you use Dumpling instead of mydumper.

### Full data import - TiDB Lightning

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) supports full data import of a large dataset into a TiDB cluster.

TiDB Lightning supports the following modes:

- `Physical Import Mode`: TiDB Lightning parses data into ordered key-value pairs and directly imports them into TiKV. This mode is usually for importing a large amount of data (at the TB level) to a new cluster. During the import, the cluster cannot provide services.
- `Logical Import Mode`: This mode uses TiDB/MySQL as the backend, which is slower than the `Physical Import Mode` but can be performed online. It also supports importing data to MySQL.

The following are the basics of TiDB Lightning:

- Data source:
    - The output files of Dumpling
    - Other compatible CSV files
    - Parquet files exported from Amazon Aurora or Apache Hive
- Supported TiDB versions: v2.1 and later versions
- Kubernetes support: Yes. See [Quickly restore data into a TiDB cluster on Kubernetes using TiDB Lightning](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning) for details.

> **Note:**
>
> The Loader tool is no longer maintained. For scenarios related to Loader, it is recommended that you use `Logical Import Mode` instead.

### Backup and restore - Backup & Restore (BR)

[Backup & Restore](/br/backup-and-restore-overview.md) (BR) is a command-line tool for distributed backup and restore of the TiDB cluster data. BR can effectively back up and restore TiDB clusters of huge data volume.

The following are the basics of BR:

- Input and output data source

    - Snapshot backup and restore: [SST + `backupmeta` file](/br/br-snapshot-architecture.md#backup-files)
    - Log backup and PITR: [Log backup files](/br/br-log-architecture.md#log-backup-files)

- Supported TiDB versions: v4.0 and later versions
- Kubernetes support: Yes. See [Back up Data to S3-Compatible Storage Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br) and [Restore Data from S3-Compatible Storage Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br) for details.

### Incremental data replication - TiCDC

[TiCDC](/ticdc/ticdc-overview.md) is a tool used for replicating incremental data of TiDB by pulling change logs from TiKV. It can restore data to a state consistent with any TSO in upstream. TiCDC also provides the TiCDC Open Protocol to support other systems to subscribe to data changes.

The following are the basics of TiCDC:

- Source: TiDB clusters
- Target: TiDB clusters, MySQL, Kafka, and Confluent
- Supported TiDB versions: v4.0.6 and later versions

### Incremental log replication - TiDB Binlog

[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) is a tool that collects binlog for TiDB clusters and provides nearly real-time data replication and backup. You can use it for incremental data replication between TiDB clusters, such as making a TiDB cluster the secondary cluster of the primary TiDB cluster.

The following are the basics of TiDB Binlog:

- Source: TiDB clusters
- Target: TiDB clusters, MySQL, Kafka, or incremental backup files
- Supported TiDB versions: v2.1 and later versions
- Kubernetes support: Yes. See [TiDB Binlog Cluster Operations](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-binlog) and [TiDB Binlog Drainer Configurations on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer) for details.

### sync-diff-inspector

[sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) is a tool that compares data stored in the MySQL or TiDB databases. In addition, you can also use sync-diff-inspector to repair data in the scenario where a small amount of data is inconsistent.

The following are the basics of sync-diff-inspector:

- Source: MySQL/TiDB clusters
- Target: MySQL/TiDB clusters
- Supported TiDB versions: all versions

## OLAP Query tool - TiSpark

[TiSpark](/tispark-overview.md) is a product developed by PingCAP to address the complexiy of OLAP queries. It combines strengths of Spark, and the features of distributed TiKV clusters and TiDB to provide a one-stop Hybrid Transactional and Analytical Processing (HTAP) solution.
