---
title: TiDB Ecosystem Tools Use Cases
summary: Learn the common use cases of TiDB ecosystem tools and how to choose the tools.
aliases: ['/docs/dev/ecosystem-tool-user-case/']
---

# TiDB Ecosystem Tools Use Cases

This document introduces the common use cases of TiDB ecosystem tools and how to choose the right tool for your scenario.

## Import data from CSV to TiDB

If you need to import the compatible CSV files exported by other tools to TiDB, use [TiDB Lightning](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md).

## Import full data from MySQL/Aurora

If you need to import full data from MySQL or Aurora, use [Dumpling](/export-or-backup-using-dumpling.md) first to export data as SQL dump files, and then use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import data into the TiDB cluster.

## Migrate data from MySQL/Aurora

If you need to migrate both full data and incremental data from MySQL/Aurora, use [TiDB Data Migration](https://docs.pingcap.com/tidb-data-migration/v1.0/overview) (DM) to perform the full and incremental data migration.

If the full data volume is large (at the TB level), you can first use [Dumpling](/export-or-backup-using-dumpling.md) and [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to perform the full data migration, and then use DM to perform the incremental data migration.

## Back up and restore TiDB cluster

If you need to back up a TiDB cluster or restore backed up data to the cluster, use [BR](/br/backup-and-restore-tool.md) (Backup & Restore).

In addition, BR can also be used to perform [incremental backup](/br/backup-and-restore-tool.md#back-up-incremental-data) and [incremental restore](/br/backup-and-restore-tool.md#restore-incremental-data) of TiDB cluster data.

## Migrate data from TiDB

If you need to migrate data from a TiDB cluster to MySQL or to another TiDB cluster, use [Dumpling](/export-or-backup-using-dumpling.md) to export full data from TiDB as SQL dump files, and then use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import data to MySQL or another TiDB cluster.

If you also need to migrate incremental data, use [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md).

## TiDB incremental data subscription

If you need to subscribe to TiDB's incremental changes, use [TiDB Binlog](/tidb-binlog/binlog-slave-client.md).
