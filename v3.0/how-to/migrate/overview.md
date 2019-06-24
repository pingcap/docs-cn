---
title: Migration Overview
summary: Learn how to migrate data into TiDB.
category: how-to
aliases: ['/docs/op-guide/migration-overview/']
---

# Migration Overview

This document describes scenarios for migrating data into TiDB from either MySQL or another data source via CSV format.

## Tools overview

Migrations will often make use of the following tools. The following is a brief overview of their usage:

- [`mydumper`](/reference/tools/mydumper.md) exports data from MySQL. It is recommended over using mysqldump.
- [`loader`](/reference/tools/loader.md) imports data in mydumper format into TiDB.
- [`syncer`](/reference/tools/syncer.md) acts like a MySQL replication slave and pushes data from MySQL into TiDB.
- [DM](/reference/tools/data-migration/overview.md) (Data Migration) integrates the functions of mydumper, Loader and syncer to support the export and import of full-size data, as well as incremental replication of MySQL Binlog data, and supports data replication of a more complete pooled table scenario.
- [TiDB-Lightning](/reference/tools/tidb-lightning/overview.md) imports data to TiDB in an optimized way. For example, a 1TiB backup could take 24+ hours to import with loader, while it will typically complete at least 3 times faster in TiDB-Lightning.

## Scenarios

The following example scenarios show how you can put to use the tools mentioned above.

#### Full data migration from MySQL

To migrate the full data, you can use one of the following three solutions:

- mydumper + Loader: use mydumper to export data from MySQL and use Loader to import the data into TiDB.
- mydumper + TiDB-Lightning: use mydumper to export data from MySQL and use TiDB-Lightning to import the data into TiDB.
- DM: use DM to export data from MySQL and import the data into TiDB.

For detailed operations, follow the steps in [Migrate Data from MySQL to TiDB](/how-to/migrate/from-mysql.md).

#### Full data migration and incremental replication

To migrate the full data and then replicate data incrementally, you can use one of the following three solutions:

- mydumper + Loader + Syncer: use mydumper to export data from MySQL, use Loader to import the data into TiDB, and then use Syncer to replicate the incremental binlog data from MySQL into TiDB.
- mydumper + TiDB-Lightning + Syncer: use mydumper to export data from MySQL, use TiDB-Lightning to import the data into TiDB, and then use Syncer to replicate the incremental binlog data from MySQL into TiDB.
- DM: use DM to migrate the full data from MySQL to TiDB and then replicate the incremental data from MySQL into TiDB.

For detailed operations, follow the steps in [Incremental Migration](/how-to/migrate/incrementally-from-mysql.md).
    
  > **Note:**
  >
  > To replicate data from MySQL to TiDB, binary logging [must be enabled](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html) with the [row format](https://dev.mysql.com/doc/refman/5.7/en/binary-log-formats.html) enabled.

#### Dump and restore from database other than MySQL

To import data from another database, it is recommended to:

- Export the data as CSV format.
- Import the data using TiDB-Lightning.

For more information, refer to [CSV support for TiDB-Lightning](/reference/tools/tidb-lightning/csv.md).
