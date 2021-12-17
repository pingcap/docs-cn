---
title: TiDB Tools Overview
aliases: ['/docs/dev/ecosystem-tool-user-guide/','/docs/dev/reference/tools/user-guide/','/docs/dev/how-to/migrate/from-mysql/','/docs/dev/how-to/migrate/incrementally-from-mysql/','/docs/dev/how-to/migrate/overview/']
---

# TiDB Tools Overview

TiDB provides a rich set of tools to help you with deployment operations, data management (such as import and export, data migration, backup & recovery), and complex OLAP queries. You can select the applicable tools according to your needs.

## Deployment and operation Tools

To meet your deployment and operation needs in different system environments, TiDB provides two deployment and Operation tools, TiUP and TiDB Operator.

### Deploy and operate TiDB on physical or virtual machines

[TiUP](/tiup/tiup-overview.md) is a TiDB package manager on physical or virtual machines. TiUP can manage multiple TiDB components such as TiDB, PD, TiKV. To start any component in the TiDB ecosystem, you just need to execute a single TiUP command.

TiUP provides [TiUP cluster](https://github.com/pingcap/tiup/tree/master/components/cluster), a cluster management component written in Golang. By using TiUP cluster, you can easily perform daily database operations, including deploying, starting, stopping, destroying, scaling, and upgrading a TiDB cluster, and manage TiDB cluster parameters.

The following are the basics of TiUP:

- [Terminology and Concepts](/tiup/tiup-terminology-and-concepts.md)
- [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md)
- [Manage TiUP Components with TiUP Commands](/tiup/tiup-component-management.md)
- Applicable TiDB versions: v4.0 and above

### Deploy and operate TiDB in Kubernetes

[TiDB Operator](https://github.com/pingcap/tidb-operator) is an automatic operation system for TiDB clusters in Kubernetes. It provides full life-cycle management for TiDB including deployment, upgrades, scaling, backup, fail-over, and configuration changes. With TiDB Operator, TiDB can run seamlessly in the Kubernetes clusters deployed on a public or private cloud.

The following are the basics of TiDB Operator:

- [TiDB Operator Architecture](https://docs.pingcap.com/tidb-in-kubernetes/stable/architecture)
- [Get Started with TiDB Operator in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/)
- Applicable TiDB versions: v2.1 and above

## Data management tools

 TiDB provides multiple data management tools, such as import and export, backup and restore, data replication, data migration, incremental synchronization, and data validation.

### Full data export

[Dumpling](/dumpling-overview.md) is a tool for the logical full data export from MySQL or TiDB.

The following are the basics of Dumpling:

- Input: MySQL/TiDB cluster
- Output: SQL/CSV file
- Supported TiDB versions: all versions
- Kubernetes support: No

> **Note:**
>
> PingCAP previously maintained a fork of the [mydumper project](https://github.com/maxbube/mydumper) with enhancements specific to TiDB. This fork has since been replaced by [Dumpling](/dumpling-overview.md), which has been rewritten in Go, and supports more optimizations that are specific to TiDB. It is strongly recommended that you use Dumpling instead of mydumper.

### Full data import

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
- Kubernetes support: Yes. See [Quickly restore data into a TiDB cluster in Kubernetes using TiDB Lightning](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning) for details.

> **Note:**
>
> The Loader tool is no longer maintained. For scenarios related to Loader, it is recommended that you use the `tidb` mode of TiDB Lighting instead. For details, see [TiDB Lightning TiDB backends](/tidb-lightning/tidb-lightning-backends.md#migrating-from-loader-to-tidb-lightning-tidb-backend).

### Backup and restore

[Backup & Restore](/br/backup-and-restore-tool.md) (BR) is a command-line tool for distributed backup and restore of the TiDB cluster data. BR can effectively back up and restore TiDB clusters of huge data volume.

The following are the basics of BR:

- [Input and output data source](/br/backup-and-restore-tool.md#types-of-backup-files): SST + `backupmeta` file
- Supported TiDB versions: v3.1 and v4.0
- Kubernetes support: Yes. See [Back up Data to S3-Compatible Storage Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br) and [Restore Data from S3-Compatible Storage Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br) for details.

### Incremental data replication

[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) is a tool that collects binlog for TiDB clusters and provides near real-time sync and backup. It can be used for incremental data replication between TiDB clusters, such as making a TiDB cluster the secondary cluster of the primary TiDB cluster.

The following are the basics of TiDB Binlog:

- Input/Output:
    - Input: TiDB cluster
    - Output: TiDB cluster, MySQL, Kafka or incremental backup files
- Supported TiDB versions: v2.1 or later
- Kubernetes support: Yes. See [TiDB Binlog Cluster Operations](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-binlog) and [TiDB Binlog Drainer Configurations in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer) for details.

### Data migration

[TiDB Data Migration](https://docs.pingcap.com/tidb-data-migration/stable) (DM) is an integrated data replication task management platform that supports the full data migration and the incremental data replication from MySQL/MariaDB to TiDB.

The following are the basics of DM:

- Input: MySQL/MariaDB
- Output: TiDB cluster
- Supported TiDB versions: all versions
- Kubernetes support: No, under development

If the data volume is below the TB level, it is recommended to migrate data from MySQL/MariaDB to TiDB directly using DM. The migration process includes the full data import and export and the incremental data replication.

If the data volume is at the TB level, take the following steps:

1. Use [Dumpling](/dumpling-overview.md) to export the full data from MySQL/MariaDB.
2. Use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import the data exported in Step 1 to the TiDB cluster.
3. Use DM to replicate the incremental data from MySQL/MariaDB to TiDB.

> **Note:**
>
> The Syncer tool is no longer maintained. For scenarios related to Syncer, it is recommended that you use DM's incremental task mode instead.

## OLAP Query tool

TiDB provides the OLAP query tool TiSpark, which allows you to query TiDB tables as if you were using native Spark.

### Query TiKV data source using Spark

[TiSpark](/tispark-overview.md) is a thin layer built for running Apache Spark on top of TiKV to answer the complex OLAP queries. It takes advantages of both the Spark platform and the distributed TiKV cluster and seamlessly glues to TiDB, and provides a one-stop Hybrid Transactional and Analytical Processing (HTAP) solution.