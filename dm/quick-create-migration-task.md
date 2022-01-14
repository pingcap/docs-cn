---
title: Data Migration Scenario Overview
summary: Learn how to configure a data migration task in different scenarios.
---

# Data Migration Scenario Overview

> **Note:**
>
> Before creating a data migration task, you need to perform the following operations:
>
> 1. [Deploy a DM Cluster Using TiUP](/dm/deploy-a-dm-cluster-using-tiup.md).
> 2. [Create a Data Source](/dm/quick-start-create-source.md).

This document introduces how to configure a data migration task in different scenarios. You can choose suitable documents to create your data migration task according to the specific scenario.

In addition to scenario-based documents, you can also refer to the following ones:

- For a complete example of data migration task configuration, refer to [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md).
- For a data migration task configuration guide, refer to [Data Migration Task Configuration Guide](/dm/dm-task-configuration-guide.md).

## Migrate Data from Multiple Data Sources to TiDB

If you need to migrate data from multiple data sources to TiDB, and to rename tables to avoid migration conflicts caused by duplicate table names in different data sources, or to disable some DDL/DML operations in some tables, refer to [Migrate Data from Multiple Data Sources to TiDB](/dm/usage-scenario-simple-migration.md).

## Migrate Sharded Schemas and Sharded Tables to TiDB

If you need to migrate sharded schemas and sharded tables to TiDB, refer to [Data Migration Shard Merge Scenario](/dm/usage-scenario-shard-merge.md).

## Migrate Incremental Data to TiDB

If you have already migrated full data using other tools like TiDB Lightning and you need to migrate incremental data, refer to [Migrate Incremental Data to TiDB](/dm/usage-scenario-incremental-migration.md).

## Migration when the Downstream Table Has More Columns

If you need to customize your table schema in TiDB to include not only all the columns from the source but also additional columns, refer to [Migration when the Downstream Table Has More Columns](/dm/usage-scenario-downstream-more-columns.md).
