---
title: TiDB FAQ
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB.
aliases: ['/docs/dev/faq/tidb-faq/','/docs/dev/faq/tidb/','/docs/dev/tiflash/tiflash-faq/','/docs/dev/reference/tiflash/faq/','/tidb/dev/tiflash-faq']
---

# TiDB FAQ

<!-- markdownlint-disable MD026 -->

This document lists the Most Frequently Asked Questions about TiDB.

## About TiDB

### TiDB introduction and architecture

#### What is TiDB?

TiDB is a distributed SQL database that features in horizontal scalability, high availability and consistent distributed transactions. It also enables you to use MySQL's SQL syntax and protocol to manage and retrieve data.

#### What is TiDB's architecture?

The TiDB cluster has three components: the TiDB server, the PD (Placement Driver) server, and the TiKV server. For more details, see [TiDB architecture](/tidb-architecture.md).

#### Is TiDB based on MySQL?

No. TiDB supports MySQL syntax and protocol, but it is a new open source database that is developed and maintained by PingCAP, Inc.

#### What is the respective responsibility of TiDB, TiKV and PD (Placement Driver)?

- TiDB works as the SQL computing layer, mainly responsible for parsing SQL, specifying query plan, and generating executor.
- TiKV works as a distributed Key-Value storage engine, used to store the real data. In short, TiKV is the storage engine of TiDB.
- PD works as the cluster manager of TiDB, which manages TiKV metadata, allocates timestamps, and makes decisions for data placement and load balancing.

#### Is it easy to use TiDB?

Yes, it is. When all the required services are started, you can use TiDB as easily as a MySQL server. You can replace MySQL with TiDB to power your applications without changing a single line of code in most cases. You can also manage TiDB using the popular MySQL management tools.

#### How is TiDB compatible with MySQL?

Currently, TiDB supports the majority of MySQL 5.7 syntax, but does not support trigger, stored procedures, user-defined functions, and foreign keys. For more details, see [Compatibility with MySQL](/mysql-compatibility.md).

If you use the MySQL 8.0 client and it fails to connect to TiDB, try to add the `default-auth` and `default-character-set` options:

{{< copyable "shell-regular" >}}

```shell
mysql -h 127.0.0.1 -u root -P 4000 --default-auth=mysql_native_password --default-character-set=utf8
```

This problem occurs because MySQL 8.0 changes the [authentication plugin](/security-compatibility-with-mysql.md) default in MySQL 5.7. To solve this problem, you need to add the options above to specify using the old encryption method.

#### How is TiDB highly available?

TiDB is self-healing. All of the three components, TiDB, TiKV and PD, can tolerate failures of some of their instances. With its strong consistency guarantee, whether it’s data machine failures or even downtime of an entire data center, your data can be recovered automatically. For more information, see [TiDB architecture](/tidb-architecture.md).

#### How is TiDB strongly consistent?

TiDB implements Snapshot Isolation consistency, which it advertises as `REPEATABLE-READ` for compatibility with MySQL. Data is redundantly copied between TiKV nodes using the [Raft consensus algorithm](https://raft.github.io/) to ensure recoverability should a node failure occur.

At the bottom layer, TiKV uses a model of replication log + State Machine to replicate data. For the write requests, the data is written to a Leader and the Leader then replicates the command to its Followers in the form of log. When the majority of nodes in the cluster receive this log, this log is committed and can be applied into the State Machine.

#### Does TiDB support distributed transactions?

Yes. TiDB distributes transactions across your cluster, whether it is a few nodes in a single location or many [nodes across multiple data centers](/multi-data-centers-in-one-city-deployment.md).

Inspired by Google's Percolator, the transaction model in TiDB is mainly a two-phase commit protocol with some practical optimizations. This model relies on a timestamp allocator to assign the monotone increasing timestamp for each transaction, so conflicts can be detected. [PD](/tidb-architecture.md#placement-driver-pd-server) works as the timestamp allocator in a TiDB cluster.

#### What programming language can I use to work with TiDB?

Any language supported by MySQL client or driver.

#### Can I use other Key-Value storage engines with TiDB?

Yes. TiKV and TiDB support many popular standalone storage engines, such as GolevelDB and BoltDB. If the storage engine is a KV engine that supports transactions and it provides a client that meets the interface requirement of TiDB, then it can connect to TiDB.

#### In addition to the TiDB documentation, are there any other ways to acquire TiDB knowledge?

Currently [TiDB documentation](/overview.md#tidb-introduction) is the most important and timely way to get TiDB related knowledge. In addition, we also have some technical communication groups. If you have any needs, contact [info@pingcap.com](mailto:info@pingcap.com).

#### What is the length limit for the TiDB user name?

32 characters at most.

#### Does TiDB support XA?

No. The JDBC driver of TiDB is MySQL JDBC (Connector/J). When using Atomikos, set the data source to `type="com.mysql.jdbc.jdbc2.optional.MysqlXADataSource"`. TiDB does not support the connection with MySQL JDBC XADataSource. MySQL JDBC XADataSource only works for MySQL (for example, using DML to modify the `redo` log).

After you configure the two data sources of Atomikos, set the JDBC drives to XA. When Atomikos operates TM and RM (DB), Atomikos sends the command including XA to the JDBC layer. Taking MySQL for an example, when XA is enabled in the JDBC layer, JDBC will send a series of XA logic operations to InnoDB, including using DML to change the `redo` log. This is the operation of the two-phase commit. The current TiDB version does not support the upper application layer JTA/XA and does not parse XA operations sent by Atomikos.

As a standalone database, MySQL can only implement across-database transactions using XA; while TiDB supports distributed transactions using Google Percolator transaction model and its performance stability is higher than XA, so TiDB does not support XA and there is no need for TiDB to support XA.

#### Does `show processlist` display the system process ID?

The display content of TiDB `show processlist` is almost the same as that of MySQL `show processlist`. TiDB `show processlist` does not display the system process ID. The ID that it displays is the current session ID. The differences between TiDB `show processlist` and MySQL `show processlist` are as follows:

- As TiDB is a distributed database, the `tidb-server` instance is a stateless engine for parsing and executing the SQL statements (for details, see [TiDB architecture](/tidb-architecture.md)). `show processlist` displays the session list executed in the `tidb-server` instance that the user logs in to from the MySQL client, not the list of all the sessions running in the cluster. But MySQL is a standalone database and its `show processlist` displays all the SQL statements executed in MySQL.
- The `State` column in TiDB is not continually updated during query execution. As TiDB supports parallel query, each statement may be in multiple _states_ at once, and thus it is difficult to simplify to a single value.

#### How to modify the user password and privilege?

To modify the user password in TiDB, it is recommended to use `set password for 'root'@'%' = '0101001';` or `alter`, not `update mysql.user` which might lead to the condition that the password in other nodes is not refreshed timely.

It is recommended to use the official standard statements when modifying the user password and privilege. For details, see [TiDB user account management](/user-account-management.md).

#### Why does the auto-increment ID of the later inserted data is smaller than that of the earlier inserted data in TiDB?

The auto-increment ID feature in TiDB is only guaranteed to be automatically incremental and unique but is not guaranteed to be allocated sequentially. Currently, TiDB is allocating IDs in batches. If data is inserted into multiple TiDB servers simultaneously, the allocated IDs are not sequential. When multiple threads concurrently insert data to multiple `tidb-server` instances, the auto-increment ID of the later inserted data may be smaller. TiDB allows specifying `AUTO_INCREMENT` for the integer field, but allows only one `AUTO_INCREMENT` field in a single table. For details, see [MySQL Compatibility](/mysql-compatibility.md#auto-increment-id).

#### How to modify the `sql_mode` in TiDB except using the `set` command?

The configuration method of TiDB `sql_mode` is different from that of MySQL `sql_mode`. TiDB does not support using the configuration file to configure `sql\_mode` of the database; it only supports using the `set` command to configure `sql\_mode` of the database. You can use `set @@global.sql_mode = 'STRICT_TRANS_TABLES';` to configure it.

#### Does TiDB support modifying the MySQL version string of the server to a specific one that is required by the security vulnerability scanning tool?

Since v3.0.8, TiDB supports modifying the version string of the server by modifying [`server-version`](/tidb-configuration-file.md#server-version) in the configuration file. When you deploy TiDB using TiDB Ansible, you can also specify the proper version string by configuring `server-version` in the `conf/tidb.yml` configuration file to avoid the failure of security vulnerability scan.

#### What authentication protocols does TiDB support? What's the process?

- Like MySQL, TiDB supports the SASL protocol for user login authentication and password processing.

- When the client connects to TiDB, the challenge-response authentication mode starts. The process is as follows:

    1. The client connects to the server.
    2. The server sends a random string challenge to the client.
    3. The client sends the username and response to the server.
    4. The server verifies the response.

### TiDB techniques

#### TiKV for data storage

See [TiDB Internal (I) - Data Storage](https://pingcap.com/blog/2017-07-11-tidbinternal1/).

#### TiDB for data computing

See [TiDB Internal (II) - Computing](https://pingcap.com/blog/2017-07-11-tidbinternal2/).

#### PD for scheduling

See [TiDB Internal (III) - Scheduling](https://pingcap.com/blog/2017-07-20-tidbinternal3/).

## Deployment on the cloud

### Public cloud

#### What cloud vendors are currently supported by TiDB?

TiDB supports deployment on [Google GKE](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-gcp-gke), [AWS EKS](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-aws-eks) and [Alibaba Cloud ACK](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-alibaba-cloud).

In addition, TiDB is currently available on JD Cloud and UCloud, and has the first-level database entries on them.

## Troubleshoot

### TiDB custom error messages

#### ERROR 8005 (HY000): Write Conflict, txnStartTS is stale

Check whether `tidb_disable_txn_auto_retry` is set to `on`. If so, set it to `off`; if it is already `off`, increase the value of `tidb_retry_limit` until the error no longer occurs.

#### ERROR 9001 (HY000): PD Server Timeout

A PD request timeout. Check the status, monitoring data and log of the PD server, and the network between the TiDB server and the PD server.

#### ERROR 9002 (HY000): TiKV Server Timeout

A TiKV request timeout. Check the status, monitoring data and log of the TiKV server, and the network between the TiDB server and the TiKV server.

#### ERROR 9003 (HY000): TiKV Server is Busy

The TiKV server is busy. This usually occurs when the database load is very high. Check the status, monitoring data and log of the TiKV server.

#### ERROR 9004 (HY000): Resolve Lock Timeout

A lock resolving timeout. This usually occurs when a large number of transaction conflicts exist. Check the application code to see whether lock contention exists in the database.

#### ERROR 9005 (HY000): Region is unavailable

The accessed Region is not available. A Raft Group is not available, with possible reasons like an inadequate number of replicas. This usually occurs when the TiKV server is busy or the TiKV node is shut down. Check the status, monitoring data and log of the TiKV server.

#### ERROR 9006 (HY000): GC life time is shorter than transaction duration

The interval of `GC Life Time` is too short. The data that should have been read by long transactions might be deleted. You can add `GC Life Time` using the following command:

{{< copyable "sql" >}}

```sql
update mysql.tidb set variable_value='30m' where variable_name='tikv_gc_life_time';
```

> **Note:**
>
> "30m" means only cleaning up the data generated 30 minutes ago, which might consume some extra storage space.

#### ERROR 9007 (HY000): Write Conflict

Check whether `tidb_disable_txn_auto_retry` is set to `on`. If so, set it to `off`; if it is already `off`, increase the value of `tidb_retry_limit` until the error no longer occurs.

### MySQL native error messages

#### ERROR 2013 (HY000): Lost connection to MySQL server during query

- Check whether panic is in the log.
- Check whether OOM exists in dmesg using `dmesg -T | grep -i oom`.
- A long time of no access might also lead to this error. It is usually caused by TCP timeout. If TCP is not used for a long time, the operating system kills it.

#### ERROR 1105 (HY000): other error: unknown error Wire Error(InvalidEnumValue(4004))

This error usually occurs when the version of TiDB does not match with the version of TiKV. To avoid version mismatch, upgrade all components when you upgrade the version.

#### ERROR 1148 (42000): the used command is not allowed with this TiDB version

When you execute the `LOAD DATA LOCAL` statement but the MySQL client does not allow executing this statement (the value of the `local_infile` option is 0), this error occurs.

The solution is to use the `--local-infile=1` option when you start the MySQL client. For example, use command like `mysql --local-infile=1 -u root -h 127.0.0.1 -P 4000`. The default value of `local-infile` is different in different versions of MySQL client, therefore you need to configure it in some MySQL clients and do not need to configure it in some others.

#### ERROR 9001 (HY000): PD server timeout start timestamp may fall behind safe point

This error occurs when TiDB fails to access PD. A worker in the TiDB background continuously queries the safepoint from PD and this error occurs if it fails to query within 100s. Generally, it is because the disk on PD is slow and busy or the network failed between TiDB and PD. For the details of common errors, see [Error Number and Fault Diagnosis](/error-codes.md).

### TiDB log error messages

#### EOF error

When the client or proxy disconnects from TiDB, TiDB does not immediately notice that the connection has been disconnected. Instead, TiDB can only notice the disconnection when it begins to return data to the connection. At this time, the log prints an EOF error.
