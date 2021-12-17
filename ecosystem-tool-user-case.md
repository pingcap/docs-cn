---
title: TiDB Tools Use Cases
summary: Learn the common use cases of TiDB tools and how to choose the tools.
aliases: ['/docs/dev/ecosystem-tool-user-case/']
---

# TiDB Tools Use Cases

This document introduces the common use cases of TiDB tools and how to choose the right tool for your scenario.

## Deploy and operate TiDB on physical or virtual machines

If you need to deploy and operate TiDB on physical or virtual machines, you can install [TiUP](/tiup/tiup-overview.md), and then use TiUP to manage TiDB components such as TiDB, PD, and TiKV.

## Deploy and operate TiDB in Kubernetes

If you need to deploy and operate TiDB in Kubernetes, you can deploy a Kubernetes cluster, and then deploy [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable). After that, you can use TiDB Operator to deploy and operate a TiDB cluster.

## Import data from CSV to TiDB

If you need to import the compatible CSV files exported by other tools to TiDB, use [TiDB Lightning](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md).

## Import full data from MySQL/Aurora

If you need to import full data from MySQL/Aurora, use [Dumpling](/dumpling-overview.md) first to export data as SQL dump files, and then use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import data into the TiDB cluster.

## Migrate data from MySQL/Aurora

If you need to migrate both full data and incremental data from MySQL/Aurora, use [TiDB Data Migration](https://docs.pingcap.com/tidb-data-migration/v2.0/overview) (DM) to perform the [full and incremental data migration](https://docs.pingcap.com/tidb-data-migration/v2.0/migrate-from-mysql-aurora).

If the full data volume is large (at the TB level), you can first use [Dumpling](/dumpling-overview.md) and [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to perform the full data migration, and then use DM to perform the incremental data migration.

## Back up and restore TiDB cluster

If you need to back up a TiDB cluster or restore backed up data to the cluster, use [BR](/br/backup-and-restore-tool.md) (Backup & Restore).

In addition, BR can also be used to perform [incremental backup](/br/use-br-command-line-tool.md#back-up-incremental-data) and [incremental restore](/br/use-br-command-line-tool.md#restore-incremental-data) of TiDB cluster data.

## Migrate data to TiDB

If you need to migrate data from a TiDB cluster to another TiDB cluster, use [Dumpling](/dumpling-overview.md) to export full data from TiDB as SQL dump files, and then use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import data to another TiDB cluster.

If you also need to migrate incremental data, use [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md).

## TiDB incremental data subscription

If you need to subscribe to TiDB's incremental changes, use [TiDB Binlog](/tidb-binlog/binlog-consumer-client.md).
