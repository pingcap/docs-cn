---
title: Data Migration Overview
summary: Learn the overview of data migration scenarios and the solutions.
---

# Data Migration Overview

This document gives an overview of the data migration solutions that you can use with TiDB. The data migration solutions are as follows:

- Full data migration.
    - To import Amazon Aurora snapshots, CSV files, or Mydumper SQL files into TiDB, you can use TiDB Lightning to perform the full migration.
    - To export all TiDB data as CSV files or Mydumper SQL files, you can use Dumpling to perform the full migration, which makes data migration from MySQL or MariaDB easier.
    - To migrate all data from a database with a small data size volume (for example, less than 1 TiB), you can also use TiDB Data Migration (DM).

- Quick initialization of TiDB. TiDB Lightning supports quickly importing data and can quickly initialize a specific table in TiDB. Before you use this feature, pay attention that the quick initialization has a great impact on TiDB and the cluster does not provide services during the initialization period.

- Incremental replication. You can use TiDB DM to replicate binlogs from MySQL, MariaDB, or Aurora to TiDB, which greatly reduces the window downtime during the replication period.

- Data replication between TiDB clusters. TiDB supports backup and restore. This feature can initialize a snapshot in an existing TiDB cluster to a new TiDB cluster.

- Incremental replication between TiDB clusters. TiDB supports disaster recovery between homogeneous databases to ensure eventual data consistency of primary and secondary databases after a disaster event. It works only when both primary and secondary clusters are TiDB.

You might choose different migration solutions according to the database type, deployment location, application data size, and application needs. The following sections introduce some common migration scenarios, and you can refer to these sections to determine the most suitable solution according to your needs.

## Migrate data from Aurora MySQL to TiDB

When you migrate data from Aurora to a TiDB cluster deployed on AWS, your data migration takes two operations: full data migration and incremental replication. You can choose the corresponding operation according to your application needs.

- [Migrate Data from Amazon Aurora to TiDB](/migrate-aurora-to-tidb.md).

## Migrate data from MySQL to TiDB

If cloud storage (S3) service is not used, the network connectivity is good, and the network latency is low, you can use the following method to migrate data from MySQL to TiDB.

- [Migrate MySQL of Small Datasets to TiDB](/migrate-small-mysql-to-tidb.md)

If you have a high demand on migration speed, or if the data size is large (for example, larger than 1 TiB), and you do not allow other applications to write to TiDB during the migration period, you can use TiDB Lightning to quickly import data. Then, you can use DM to replicate incremental data (binlog) based on your application needs.

- [Migrate MySQL of Large Datasets to TiDB](/migrate-large-mysql-to-tidb.md)

## Migrate and merge MySQL shards into TiDB

Suppose that your application uses MySQL shards for data storage, and you need to migrate these shards into TiDB as one table. In this case, you can use DM to perform the shard merge and migration.

- [Migrate and Merge MySQL Shards of Small Datasets to TiDB](/migrate-small-mysql-shards-to-tidb.md)

If the data size of the sharded tables is large (for example, larger than 1 TiB), and you do not allow other applications to write to TiDB during the migration period, you can use TiDB Lightning to quickly merge and import the sharded tables. Then, you can use DM to replicate incremental sharding data (binlog) based on your application needs.

- [Migrate and Merge MySQL Shards of Large Datasets to TiDB](/migrate-large-mysql-shards-to-tidb.md)

## Migrate data from files to TiDB

- [Migrate data from CSV files to TiDB](/migrate-from-csv-files-to-tidb.md)
- [Migrate data from SQL files to TiDB](/migrate-from-sql-files-to-tidb.md)
- [Migrate data from Parquet files to TiDB](/migrate-from-parquet-files-to-tidb.md)

## Incremental replication between TiDB clusters

You can use TiCDC for incremental data replication between TiDB clusters. For details, refer to [TiCDC Overview](/ticdc/ticdc-overview.md).

## More advanced migration solutions

The following features can improve the migration process and might meet more needs in your application.

- [Continuous Replication from Databases that Use gh-ost or pt-osc](/migrate-with-pt-ghost.md)
- [Migrate Data to a Downstream TiDB Table with More Columns](/migrate-with-more-columns-downstream.md)
- [Filter Binlog Events](/filter-binlog-event.md)
- [Filter DML Events Using SQL Expressions](/filter-dml-event.md)