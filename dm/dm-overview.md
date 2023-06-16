---
title: TiDB Data Migration Overview
summary: Learn about the Data Migration tool, the architecture, the key components, and features.
aliases: ['/docs/tidb-data-migration/dev/overview/','/docs/tidb-data-migration/dev/feature-overview/','/tidb/dev/dm-key-features']
---

<!-- markdownlint-disable MD007 -->

# TiDB Data Migration Overview

<!--
![star](https://img.shields.io/github/stars/pingcap/tiflow?style=for-the-badge&logo=github) ![license](https://img.shields.io/github/license/pingcap/tiflow?style=for-the-badge) ![forks](https://img.shields.io/github/forks/pingcap/tiflow?style=for-the-badge)
-->

[TiDB Data Migration](https://github.com/pingcap/tiflow/tree/master/dm) (DM) is an integrated data migration task management platform, which supports the full data migration and the incremental data replication from MySQL-compatible databases (such as MySQL, MariaDB, and Aurora MySQL) into TiDB. It can help to reduce the operation cost of data migration and simplify the troubleshooting process.

## Basic features

- **Compatibility with MySQL.** DM is compatible with MySQL 5.7 protocols and most of the features and syntax of MySQL 5.7.
- **Replicating DML and DDL events.** It supports parsing and replicating DML and DDL events in MySQL binlog.
- **Migrating and merging MySQL shards.** DM supports migrating and merging multiple MySQL database instances upstream to one TiDB database downstream. It supports customizing replication rules for different migration scenarios. It can automatically detect and handle DDL changes of upstream MySQL shards, which greatly reduces the operational cost.
- **Various types of filters.** You can predefine event types, regular expressions, and SQL expressions to filter out MySQL binlog events during the data migration process.
- **Centralized management.** DM supports thousands of nodes in a cluster. It can run and manage a large number of data migration tasks concurrently.
- **Optimization of the third-party Online Schema Change process.** In the MySQL ecosystem, tools such as gh-ost and pt-osc are widely used. DM optimizes its change process to avoid unnecessary migration of intermediate data. For details, see [online-ddl](/dm/dm-online-ddl-tool-support.md).
- **High availability.** DM supports data migration tasks to be scheduled freely on different nodes. The running tasks are not affected when a small number of nodes crash.

## Quick installation

Run the following command to install DM:

{{< copyable "shell-regular" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
tiup install dm dmctl
```

## Usage restrictions

Before using the DM tool, note the following restrictions:

+ Database version requirements

    - MySQL version 5.5 ~ 5.7
    - MySQL version 8.0 (experimental features)
    - MariaDB version >= 10.1.2 (experimental features)

    > **Note:**
    >
    > If there is a primary-secondary migration structure between the upstream MySQL/MariaDB servers, then choose the following version.
    >
    > - MySQL version > 5.7.1
    > - MariaDB version >= 10.1.3

+ DDL syntax compatibility

    - Currently, TiDB is not compatible with all the DDL statements that MySQL supports. Because DM uses the TiDB parser to process DDL statements, it only supports the DDL syntax supported by the TiDB parser. For details, see [MySQL Compatibility](/mysql-compatibility.md#ddl-operations).

    - DM reports an error when it encounters an incompatible DDL statement. To solve this error, you need to manually handle it using dmctl, either skipping this DDL statement or replacing it with specified DDL statements. For details, see [Skip or replace abnormal SQL statements](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements).

    - DM does not replicate view-related DDL statements and DML statements to the downstream TiDB cluster. It is recommended that you create the view in the downstream TiDB cluster manually.

+ GBK character set compatibility

    - DM does not support migrating `charset=GBK` tables to TiDB clusters earlier than v5.4.0.

## Contributing

You are welcome to participate in the DM open sourcing project. Your contribution would be highly appreciated. For more details, see [CONTRIBUTING.md](https://github.com/pingcap/tiflow/blob/master/dm/CONTRIBUTING.md).

## Community support

You can learn about DM through the online documentation. If you have any questions, contact us on [GitHub](https://github.com/pingcap/tiflow/tree/master/dm).

## License

DM complies with the Apache 2.0 license. For more details, see [LICENSE](https://github.com/pingcap/tiflow/blob/master/LICENSE).

## DM versions

Before v5.4, the DM documentation is independent of the TiDB documentation. To access these earlier versions of the DM documentation, click one of the following links:

- [DM v5.3 documentation](https://docs.pingcap.com/tidb-data-migration/v5.3)
- [DM v2.0 documentation](https://docs.pingcap.com/tidb-data-migration/v2.0/)
- [DM v1.0 documentation](https://docs.pingcap.com/tidb-data-migration/v1.0/)

> **Note:**
>
> - Since October 2021, DM's GitHub repository has been moved to [pingcap/tiflow](https://github.com/pingcap/tiflow/tree/master/dm). If you see any issues with DM, submit your issue to the `pingcap/tiflow` repository for feedback.
> - In earlier versions (v1.0 and v2.0), DM uses version numbers that are independent of TiDB. Since v5.3, DM uses the same version number as TiDB. The next version of DM v2.0 is DM v5.3. There are no compatibility changes from DM v2.0 to v5.3, and the upgrade process is the same as a normal upgrade, only an increase in version number.