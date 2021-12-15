---
title: TiDB Data Migration
summary: Learn about the TiDB Data Migration tool.
---

# TiDB Data Migration

[TiDB Data Migration](https://github.com/pingcap/dm) (DM) is an integrated data migration task management platform, which supports the full data migration and the incremental data replication from MySQL-compatible databases (such as MySQL, MariaDB, and Aurora MySQL) into TiDB. DM can help simplify the data migration process and reduce the operation cost of data migration.

## DM versions

The stable versions of DM include v1.0, v2.0, and v5.3. It is recommended to use DM v5.3 (the latest stable version of DM) and not recommended to use v1.0 (the earliest stable version of DM).

Currently, the DM documentation is independent of the TiDB documentation. To access the DM documentation, click one of the following links:

- [DM v5.3 documentation](https://docs.pingcap.com/tidb-data-migration/v5.3)
- [DM v2.0 documentation](https://docs.pingcap.com/tidb-data-migration/v2.0/)
- [DM v1.0 documentation](https://docs.pingcap.com/tidb-data-migration/v1.0/)

> **Note:**
>
> - Since October 2021, DM's GitHub repository has been moved to [pingcap/ticdc](https://github.com/pingcap/ticdc/tree/master/dm). If you see any issues with DM, submit your issue to the `pingcap/ticdc` repository for feedback.
> - In earlier versions (v1.0 and v2.0), DM uses version numbers that are independent of TiDB. Since v5.3, DM uses the same version number as TiDB. The next version of DM v2.0 is DM v5.3. There are no compatibility changes from DM v2.0 to v5.3, and the upgrade process is no different from a normal upgrade, only an increase in version number.

## Basic features

This section describes the basic data migration features provided by DM.

![DM Core Features](/media/dm/dm-core-features.png)

### Block and allow lists migration at the schema and table levels

The [block and allow lists filtering rule](https://docs.pingcap.com/tidb-data-migration/stable/key-features#block-and-allow-table-lists) is similar to the `replication-rules-db`/`replication-rules-table` feature of MySQL, which can be used to filter or replicate all operations of some databases only or some tables only.

### Binlog event filtering

The [binlog event filtering](https://docs.pingcap.com/tidb-data-migration/stable/key-features#binlog-event-filter) feature means that DM can filter certain types of SQL statements from certain tables in the source database. For example, you can filter all `INSERT` statements in the table `test`.`sbtest` or filter all `TRUNCATE TABLE` statements in the schema `test`.

### Schema and table routing

The [schema and table routing](https://docs.pingcap.com/tidb-data-migration/stable/key-features#table-routing) feature means that DM can migrate a certain table of the source database to the specified table in the downstream. For example, you can migrate the table structure and data from the table `test`.`sbtest1` in the source database to the table `test`.`sbtest2` in TiDB. This is also a core feature for merging and migrating sharded databases and tables.

## Advanced features

### Shard merge and migration

DM supports merging and migrating the original sharded instances and tables from the source databases into TiDB, but with some restrictions. For details, see [Sharding DDL usage restrictions in the pessimistic mode](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge-pessimistic#restrictions) and [Sharding DDL usage restrictions in the optimistic mode](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge-optimistic#restrictions).

### Optimization for third-party online-schema-change tools in the migration process

In the MySQL ecosystem, tools such as `gh-ost` and `pt-osc` are widely used. DM provides support for these tools to avoid migrating unnecessary intermediate data. For details, see [Online DDL Tools](https://docs.pingcap.com/tidb-data-migration/stable/key-features#online-ddl-tools)

### Filter certain row changes using SQL expressions

In the phase of incremental replication, DM supports the configuration of SQL expressions to filter out certain row changes, which lets you replicate the data with a greater granularity. For more information, refer to [Filter Certain Row Changes Using SQL Expressions](https://docs.pingcap.com/tidb-data-migration/stable/feature-expression-filter).

## Usage restrictions

Before using the DM tool, note the following restrictions:

+ Database version requirements

    - MySQL version > 5.5
    - MariaDB version >= 10.1.2

    > **Note:**
    >
    > If there is a primary-secondary migration structure between the upstream MySQL/MariaDB servers, then choose the following version.
    >
    > - MySQL version > 5.7.1
    > - MariaDB version >= 10.1.3

    > **Warning:**
    >
    > Migrating data from MySQL 8.0 to TiDB using DM is an experimental feature (introduced since DM v2.0). It is **NOT** recommended that you use it in a production environment.

+ DDL syntax compatibility

    - Currently, TiDB is not compatible with all the DDL statements that MySQL supports. Because DM uses the TiDB parser to process DDL statements, it only supports the DDL syntax supported by the TiDB parser. For details, see [MySQL Compatibility](/mysql-compatibility.md#ddl).

    - DM reports an error when it encounters an incompatible DDL statement. To solve this error, you need to manually handle it using dmctl, either skipping this DDL statement or replacing it with a specified DDL statement(s). For details, see [Skip or replace abnormal SQL statements](https://docs.pingcap.com/tidb-data-migration/stable/faq#how-to-handle-incompatible-ddl-statements).

+ Sharding merge with conflicts

    - If conflict exists between sharded tables, solve the conflict by referring to [handling conflicts of auto-increment primary key](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices#handle-conflicts-of-auto-increment-primary-key). Otherwise, data migration is not supported. Conflicting data can cover each other and cause data loss.

    - For other sharding DDL migration restrictions, see [Sharding DDL usage restrictions in the pessimistic mode](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge-pessimistic#restrictions) and [Sharding DDL usage restrictions in the optimistic mode](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge-optimistic#restrictions).

+ Switch of MySQL instances for data sources

    When DM-worker connects the upstream MySQL instance via a virtual IP (VIP), if you switch the VIP connection to another MySQL instance, DM might connect to the new and old MySQL instances at the same time in different connections. In this situation, the binlog migrated to DM is not consistent with other upstream status that DM receives, causing unpredictable anomalies and even data damage. To make necessary changes to DM manually, see [Switch DM-worker connection via virtual IP](https://docs.pingcap.com/tidb-data-migration/stable/usage-scenario-master-slave-switch#switch-dm-worker-connection-via-virtual-ip).
