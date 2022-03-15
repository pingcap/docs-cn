---
title: Data Migration Scenarios
summary: Learn how to configure a data migration task in different scenarios.
---

# Data Migration Scenario Overview

> **Note:**
>
> Before creating a data migration task, you need to perform the following operations:
>
> 1. [Deploy a DM Cluster Using TiUP](/dm/deploy-a-dm-cluster-using-tiup.md).
> 2. [Create a Data Source](/dm/quick-start-create-source.md).

This document introduces how to perform data migration tasks in different scenarios.

In addition to scenario-based documents, you can also refer to the following documents:

- For a complete example of data migration task configuration, refer to [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md).
- For a data migration task configuration guide, refer to [Data Migration Task Configuration Guide](/dm/dm-task-configuration-guide.md).

## Migrate data from Amazon Aurora to TiDB

When you migrate data from Aurora to a TiDB cluster deployed on AWS, your data migration takes two operations: full data migration and incremental replication. You can choose the corresponding operation according to your application needs.

-[Migrate Data from Amazon Aurora to TiDB](/migrate-aurora-to-tidb.md)

## Migrate data from MySQL to TiDB

If a cloud storage (S3) service is not used, the network connectivity is good, and the network latency is low, you can use the following method to migrate data from MySQL to TiDB.

- [Migrate MySQL of Small Datasets to TiDB](/migrate-small-mysql-to-tidb.md)

If you have a high demand on migration speed, or if the data size is large (for example, larger than 1 TiB), and you do not allow other applications to write to TiDB during the migration period, you can use TiDB Lightning to quickly import data. Then, you can use DM to replicate incremental data (binlog) based on your application needs.

[Migrate MySQL of Large Datasets to TiDB](/migrate-large-mysql-to-tidb.md)

## Migrate and merge MySQL shards into TiDB

Suppose that your application uses MySQL shards for data storage, and you need to migrate these shards into TiDB as one table. In this case, you can use DM to perform the shard merge and migration.

- [Migrate and Merge MySQL Shards of Small Datasets to TiDB](/migrate-small-mysql-shards-to-tidb.md)

If the data size of the sharded tables is large (for example, larger than 1 TiB), and you do not allow other applications to write to TiDB during the migration period, you can use TiDB Lightning to quickly merge and import the sharded tables. Then, you can use DM to replicate incremental sharding data (binlog) based on your application needs.

- [Migrate and Merge MySQL Shards of Large Datasets to TiDB](/migrate-large-mysql-shards-to-tidb.md)

## More advanced migration solutions

The following features can improve the migration process and meet more needs in your application.

- [Continuous Replication from Databases that Use gh-ost or pt-osc](/migrate-with-pt-ghost.md)
- [Migrate Data to a Downstream TiDB Table with More Columns](/migrate-with-more-columns-downstream.md)
- [Filter Binlog Events](/filter-binlog-event.md)
- [Filter DML Events Using SQL Expressions](/filter-dml-event.md)