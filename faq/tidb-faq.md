---
title: TiDB FAQ
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB.
aliases: ['/docs/dev/faq/tidb-faq/','/docs/dev/faq/tidb/','/docs/dev/tiflash/tiflash-faq/','/docs/dev/reference/tiflash/faq/','/tidb/dev/tiflash-faq']
---

# TiDB FAQ

<!-- markdownlint-disable MD026 -->

This document lists the Most Frequently Asked Questions about TiDB.

## TiDB introduction and architecture

### What is TiDB?

TiDB is a distributed SQL database that features in horizontal scalability, high availability and consistent distributed transactions. It also enables you to use MySQL's SQL syntax and protocol to manage and retrieve data.

### What is TiDB's architecture?

The TiDB cluster has three components: the TiDB server, the PD (Placement Driver) server, and the TiKV server. For more details, see [TiDB architecture](/tidb-architecture.md).

### Is TiDB based on MySQL?

No. TiDB supports MySQL syntax and protocol, but it is a new open source database that is developed and maintained by PingCAP, Inc.

### What is the respective responsibility of TiDB, TiKV and PD (Placement Driver)?

- TiDB works as the SQL computing layer, mainly responsible for parsing SQL, specifying query plan, and generating executor.
- TiKV works as a distributed Key-Value storage engine, used to store the real data. In short, TiKV is the storage engine of TiDB.
- PD works as the cluster manager of TiDB, which manages TiKV metadata, allocates timestamps, and makes decisions for data placement and load balancing.

### Is it easy to use TiDB?

Yes, it is. When all the required services are started, you can use TiDB as easily as a MySQL server. You can replace MySQL with TiDB to power your applications without changing a single line of code in most cases. You can also manage TiDB using the popular MySQL management tools.

### How is TiDB compatible with MySQL?

Currently, TiDB supports the majority of MySQL 5.7 syntax, but does not support triggers, stored procedures, user-defined functions, and foreign keys. For more details, see [Compatibility with MySQL](/mysql-compatibility.md).

### Does TiDB support distributed transactions?

Yes. TiDB distributes transactions across your cluster, whether it is a few nodes in a single location or many [nodes across multiple data centers](/multi-data-centers-in-one-city-deployment.md).

Inspired by Google's Percolator, the transaction model in TiDB is mainly a two-phase commit protocol with some practical optimizations. This model relies on a timestamp allocator to assign the monotone increasing timestamp for each transaction, so conflicts can be detected. [PD](/tidb-architecture.md#placement-driver-pd-server) works as the timestamp allocator in a TiDB cluster.

### What programming language can I use to work with TiDB?

Any language supported by MySQL client or driver.

### Can I use other Key-Value storage engines with TiDB?

Yes. In addition to TiKV, TiDB supports standalone storage engines such as UniStore and MockTiKV. Note that in later TiDB releases, MockTiKV might NO LONGER be supported.

To check all TiDB-supported storage engines, use the following command:

{{< copyable "shell-regular" >}}

```shell
./bin/tidb-server -h
```

The output is as follows:

```shell
Usage of ./bin/tidb-server:
  -L string
        log level: info, debug, warn, error, fatal (default "info")
  -P string
        tidb server port (default "4000")
  -V    print version information and exit (default false)
.........
  -store string
        registered store name, [tikv, mocktikv, unistore] (default "unistore")
  ......
```

### In addition to the TiDB documentation, are there any other ways to acquire TiDB knowledge?

Currently [TiDB documentation](/overview.md#tidb-introduction) is the most important and timely way to get TiDB related knowledge. In addition, we also have some technical communication groups. If you have any needs, contact [info@pingcap.com](mailto:info@pingcap.com).

### What is the length limit for the TiDB user name?

32 characters at most.

### Does TiDB support XA?

No. The JDBC driver of TiDB is MySQL JDBC (Connector/J). When using Atomikos, set the data source to `type="com.mysql.jdbc.jdbc2.optional.MysqlXADataSource"`. TiDB does not support the connection with MySQL JDBC XADataSource. MySQL JDBC XADataSource only works for MySQL (for example, using DML to modify the `redo` log).

After you configure the two data sources of Atomikos, set the JDBC drives to XA. When Atomikos operates TM and RM (DB), Atomikos sends the command including XA to the JDBC layer. Taking MySQL for an example, when XA is enabled in the JDBC layer, JDBC will send a series of XA logic operations to InnoDB, including using DML to change the `redo` log. This is the operation of the two-phase commit. The current TiDB version does not support the upper application layer JTA/XA and does not parse XA operations sent by Atomikos.

As a standalone database, MySQL can only implement across-database transactions using XA; while TiDB supports distributed transactions using Google Percolator transaction model and its performance stability is higher than XA, so TiDB does not support XA and there is no need for TiDB to support XA.

## TiDB techniques

### TiKV for data storage

See [TiDB Internal (I) - Data Storage](https://en.pingcap.com/blog/tidb-internal-data-storage/).

### TiDB for data computing

See [TiDB Internal (II) - Computing](https://en.pingcap.com/blog/tidb-internal-computing/).

### PD for scheduling

See [TiDB Internal (III) - Scheduling](https://en.pingcap.com/blog/tidb-internal-scheduling/).
