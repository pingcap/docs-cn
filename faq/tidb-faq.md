---
title: TiDB Architecture FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB.
aliases: ['/docs/dev/faq/tidb-faq/','/docs/dev/faq/tidb/','/docs/dev/tiflash/tiflash-faq/','/docs/dev/reference/tiflash/faq/','/tidb/dev/tiflash-faq']
---

# TiDB Architecture FAQs

<!-- markdownlint-disable MD026 -->

This document lists the Most Frequently Asked Questions about TiDB.

## TiDB introduction and architecture

### What is TiDB?

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

[TiDB](https://github.com/pingcap/tidb) is an open-source distributed SQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. It is MySQL compatible and features horizontal scalability, strong consistency, and high availability. The goal of TiDB is to provide users with a one-stop database solution that covers OLTP (Online Transactional Processing), OLAP (Online Analytical Processing), and HTAP services. TiDB is suitable for various use cases that require high availability and strong consistency with large-scale data.

### What is TiDB's architecture?

The TiDB cluster has three components: the TiDB server, the PD (Placement Driver) server, and the TiKV server. For more details, see [TiDB architecture](/tidb-architecture.md), [TiDB storage](/tidb-storage.md), [TiDB computing](/tidb-computing.md), and [TiDB scheduling](/tidb-scheduling.md).

### Is TiDB based on MySQL?

No. TiDB supports MySQL syntax and protocol, but it is a new open source database that is developed and maintained by PingCAP, Inc.

### What is the respective responsibility of TiDB, TiKV and PD (Placement Driver)?

- TiDB works as the SQL computing layer, mainly responsible for parsing SQL, specifying query plan, and generating executor.
- TiKV works as a distributed Key-Value storage engine, used to store the real data. In short, TiKV is the storage engine of TiDB.
- PD works as the cluster manager of TiDB, which manages TiKV metadata, allocates timestamps, and makes decisions for data placement and load balancing.

### Is it easy to use TiDB?

Yes, it is. When all the required services are started, you can use TiDB as easily as a MySQL server. You can replace MySQL with TiDB to power your applications without changing a single line of code in most cases. You can also manage TiDB using the popular MySQL management tools.

### How is TiDB compatible with MySQL?

Currently, TiDB supports the majority of MySQL 5.7 syntax, but does not support triggers, stored procedures, and user-defined functions. For more details, see [Compatibility with MySQL](/mysql-compatibility.md).

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

- [TiDB documentation](https://docs.pingcap.com/): the most important and timely way to get TiDB related knowledge.
- [TiDB blogs](https://www.pingcap.com/blog/): learn technical articles, product insights, and case studies.
- [PingCAP Education](https://www.pingcap.com/education/?from=en): take online courses and certification programs.

### What is the length limit for the TiDB user name?

32 characters at most.

### What are the limits on the number of columns and row size in TiDB?

- The maximum number of columns in TiDB defaults to 1017. You can adjust the number up to 4096.
- The maximum size of a single row defaults to 6 MB. You can increase the number up to 120 MB.

For more information, see [TiDB Limitations](/tidb-limitations.md).

### Does TiDB support XA?

No. The JDBC driver of TiDB is MySQL Connector/J. When using Atomikos, set the data source to `type="com.mysql.jdbc.jdbc2.optional.MysqlXADataSource"`. TiDB does not support the connection with MySQL JDBC XADataSource. MySQL JDBC XADataSource only works for MySQL (for example, using DML to modify the `redo` log).

After you configure the two data sources of Atomikos, set the JDBC drives to XA. When Atomikos operates TM and RM (DB), Atomikos sends the command including XA to the JDBC layer. Taking MySQL for an example, when XA is enabled in the JDBC layer, JDBC will send a series of XA logic operations to InnoDB, including using DML to change the `redo` log. This is the operation of the two-phase commit. The current TiDB version does not support the upper application layer JTA/XA and does not parse XA operations sent by Atomikos.

As a standalone database, MySQL can only implement across-database transactions using XA; while TiDB supports distributed transactions using Google Percolator transaction model and its performance stability is higher than XA, so TiDB does not support JTA/XA and there is no need for TiDB to support XA.

### How could TiDB support high concurrent `INSERT` or `UPDATE` operations to the columnar storage engine (TiFlash) without hurting performance?

- [TiFlash](/tiflash/tiflash-overview.md) introduces a special structure named DeltaTree to process the modification of the columnar engine.
- TiFlash acts as the learner role in a Raft group, so it does not vote for the log commit or writes. This means that DML operations do not have to wait for the acknowledgment of TiFlash, which is why TiFlash does not slow down the OLTP performance. In addition, TiFlash and TiKV work in separate instances, so they do not affect each other.

### Is TiFlash eventually consistent?

Yes. TiFlash maintains strong data consistency by default.

## TiDB techniques

### TiKV for data storage

See [TiDB Internal (I) - Data Storage](https://www.pingcap.com/blog/tidb-internal-data-storage/?from=en).

### TiDB for data computing

See [TiDB Internal (II) - Computing](https://www.pingcap.com/blog/tidb-internal-computing/?from=en).

### PD for scheduling

See [TiDB Internal (III) - Scheduling](https://www.pingcap.com/blog/tidb-internal-scheduling/?from=en).
