---
title: TiDB FAQ
category: faq
---

- [Product](#product)
    - [General](#general)
        - [What is TiDB?](#what-is-tidb)
        - [Is TiDB based on MySQL?](#is-tidb-based-on-mysql)
        - [How do TiDB and TiKV work together? What is the relationship between the two?](#how-do-tidb-and-tikv-work-together-what-is-the-relationship-between-the-two)
        - [What does Placement Driver (PD) do?](#what-does-placement-driver-pd-do)
        - [Is it easy to use TiDB?](#is-it-easy-to-use-tidb)
        - [When to use TiDB?](#when-to-use-tidb)
        - [When not to use TiDB?](#when-not-to-use-tidb)
        - [How is TiDB strongly-consistent?](#how-is-tidb-strongly-consistent)
        - [Does TiDB support distributed transactions?](#does-tidb-support-distributed-transactions)
        - [What programming language can I use to work with TiDB?](#what-programming-language-can-i-use-to-work-with-tidb)
        - [How does TiDB compare to traditional relational databases like Oracle and MySQL?](#how-does-tidb-compare-to-traditional-relational-databases-like-oracle-and-mysql)
        - [How does TiDB compare to NoSQL databases like Cassandra, Hbase, or MongoDB?](#how-does-tidb-compare-to-nosql-databases-like-cassandra-hbase-or-mongodb)
        - [An error message is displayed when using `go get` to install TiDB.](#an-error-message-is-displayed-when-using-go-get-to-install-tidb)
        - [How is TiDB highly available?](#how-is-tidb-highly-available)
    - [PD](#pd)
        - [The `TiKV cluster is not bootstrapped` message is displayed when accessing PD.](#the-tikv-cluster-is-not-bootstrapped-message-is-displayed-when-accessing-pd)
        - [The `etcd cluster ID mismatch` message is displayed when starting PD.](#the-etcd-cluster-id-mismatch-message-is-displayed-when-starting-pd)
        - [How to update the startup parameters of PD?](#how-to-update-the-startup-parameters-of-pd)
        - [What's the maximum tolerance for time synchronization error of PD?](#whats-the-maximum-tolerance-for-time-synchronization-error-of-pd)
    - [TiDB](#tidb)
        - [How to choose the lease parameter in TiDB?](#how-to-choose-the-lease-parameter-in-tidb)
        - [Can I use other key-value storage engines with TiDB?](#can-i-use-other-key-value-storage-engines-with-tidb)
        - [Where is the Raft log stored in TiDB?](#where-is-the-raft-log-stored-in-tidb)
    - [TiKV](#tikv)
        - [Why the TiKV data directory is gone?](#why-the-tikv-data-directory-is-gone)
        - [The `cluster ID mismatch` message is displayed when starting TiKV.](#the-cluster-id-mismatch-message-is-displayed-when-starting-tikv)
        - [The `duplicated store address` message is displayed when starting TiKV.](#the-duplicated-store-address-message-is-displayed-when-starting-tikv)
        - [Would the key be too long according to the TiDB setting?](#would-the-key-be-too-long-according-to-the-tidb-setting)
    - [TiSpark](#tispark)
        - [Where is the user guide of TiSpark?](#where-is-the-user-guide-of-tispark)
- [Operations](#operations)
    - [Install](#install)
        - [Why the modified `toml` configuration for TiKV/PD does not take effect?](#why-the-modified-toml-configuration-for-tikvpd-does-not-take-effect)
        - [What can I do if the file system of my data disk is XFS and cannot be changed?](#what-can-i-do-if-the-file-system-of-my-data-disk-is-xfs-and-cannot-be-changed)
        - [Can chrony meet the requirement of time synchronization?](#can-chrony-meet-the-requirement-of-time-synchronization)
    - [Scale](#scale)
        - [How does TiDB scale?](#how-does-tidb-scale)
    - [Monitor](#monitor)
        - [The monitor can't show all the metrics.](#the-monitor-cant-show-all-the-metrics)
    - [Migrate](#migrate)
        - [Can a MySQL application be migrated to TiDB?](#can-a-mysql-application-be-migrated-to-tidb)
    - [Performance tuning](#performance-tuning)
    - [Backup and restore](#backup-and-restore)
    - [Misc](#misc)
        - [How does TiDB manage user account?](#how-does-tidb-manage-user-account)
        - [Where are the TiDB/PD/TiKV logs?](#where-are-the-tidbpdtikv-logs)
        - [How to safely stop TiDB?](#how-to-safely-stop-tidb)
        - [Can `kill` be executed in TiDB?](#can-kill-be-executed-in-tidb)
- [SQL](#sql)
    - [SQL syntax](#sql-syntax)
        - [The error message `transaction too large` is displayed.](#the-error-message-transaction-too-large-is-displayed)
        - [Check the running DDL job](#check-the-running-ddl-job)
    - [SQL optimization](#sql-optimization)
        - [How to optimize `select count(1)`?](#how-to-optimize-select-count1)

## Product

### General

#### What is TiDB?

TiDB is a distributed SQL database that features in horizontal scalability, high availability and consistent distributed transactions. It also enables you to use MySQL’s SQL syntax and protocol to manage and retrieve data.

#### Is TiDB based on MySQL?

No. TiDB supports MySQL syntax and protocol, but it is a new open source database that is developed and maintained by PingCAP, Inc.

#### How do TiDB and TiKV work together? What is the relationship between the two?

TiDB works as the SQL layer and TiKV works as the Key-Value layer. TiDB is mainly responsible for parsing SQL, specifying query plan, and generating executor while TiKV is to store the actual data and works as the storage engine.

TiDB provides TiKV the SQL enablement and turns TiKV into a NewSQL database. TiDB and TiKV work together to be as scalable as a NoSQL database while maintains the ACID transactions of a relational database.

#### What does Placement Driver (PD) do?

Placement Driver (PD) works as the cluster manager of TiDB. It manages the TiKV metadata and makes decisions for data placement and load balancing. PD periodically checks replication constraints to balance load and data automatically.

#### Is it easy to use TiDB?

Yes, it is. When all the required services are started, you can use TiDB as easily as a MySQL server. You can replace MySQL with TiDB to power your applications without changing a single line of code in most cases. You can also manage TiDB using the popular MySQL management tools.

#### When to use TiDB?

TiDB is at your service if your applications require any of the following:

- Horizontal scalability
- High availability
- Strong consistency
- Support for distributed ACID transactions

#### When not to use TiDB?

TiDB is not a good choice if the number of the rows in your database table is less than 100GB and there is no requirement for high availability, strong consistency and cross-datacenter replication.

#### How is TiDB strongly-consistent?

Strong consistency means all replicas return the same value when queried for the attribute of an object. TiDB uses the [Raft consensus algorithm](https://raft.github.io/) to ensure consistency among multiple replicas. TiDB allows a collection of machines to work as a coherent group that can survive the failures of some of its members.

#### Does TiDB support distributed transactions?

Yes. The transaction model in TiDB is inspired by Google’s Percolator, a paper published in 2006. It’s mainly a two-phase commit protocol with some practical optimizations. This model relies on a timestamp allocator to assign monotone increasing timestamp for each transaction, so the conflicts can be detected. PD works as the timestamp allocator in a TiDB cluster.

#### What programming language can I use to work with TiDB?

Any language that has MySQL client or driver.

#### How does TiDB compare to traditional relational databases like Oracle and MySQL?

TiDB scores in horizontal scalability while still maintains the traditional relation database features. You can easily increase the capacity or balance the load by adding more machines.

#### How does TiDB compare to NoSQL databases like Cassandra, Hbase, or MongoDB?

TiDB is as scalable as NoSQL databases but features in the usability and functionality of traditional SQL databases, such as SQL syntax and consistent distributed transactions.

#### An error message is displayed when using `go get` to install TiDB.

Manually clone TiDB to the GOPATH directory and run the `make` command. TiDB uses `Makefile` to manage the dependencies.

If you are a developer and familiar with Go, you can run `make parser; ln -s _vendor/src vendor` in the root directory of TiDB and then run commands like `go run`, `go test` and `go install`. However, this is not recommended.

#### How is TiDB highly available?

TiDB is self-healing. All of the three components, TiDB, TiKV and PD, can tolerate failures of some of their instances. With its strong consistency guarantee, whether it’s data machine failures or even downtime of an entire data center, your data can be recovered automatically.

### PD

#### The `TiKV cluster is not bootstrapped` message is displayed when accessing PD.

Most of the APIs of PD are available only when the TiKV cluster is initialized. This message is displayed if PD is accessed when PD is started while TiKV is not started when a new cluster is deployed. If this message is displayed, start the TiKV cluster. When TiKV is initialized, PD is accessible.

#### The `etcd cluster ID mismatch` message is displayed when starting PD.

This is because the `--initial-cluster` in the PD startup parameter contains a member that doesn't belong to this cluster. To solve this problem, check the corresponding cluster of each member, remove the wrong member, and then restart PD.

#### How to update the startup parameters of PD?

If you want to update PD's startup parameters, such as `--client-url`, `--advertise-client-url` or `--name`, you just need to restart PD with the updated parameters.

However, if you want to update `--peer-url` or `--advertise-peer-url`, pay attention to the following situations:

- The previous startup parameter has `--advertise-peer-url` and you just want to update `--peer-url`: restart PD with the updated parameter.
- The previous startup parameter doesn't have `--advertise-peer-url`: update the PD information with [etcdctl](https://coreos.com/etcd/docs/latest/op-guide/runtime-configuration.html#update-a-member) and then restart PD with the updated parameter.

#### What's the maximum tolerance for time synchronization error of PD?

Theoretically, the smaller of the tolerance, the better. During leader changes, if the clock goes back, the process won't proceed until it catches up with the previous leader.

### TiDB

#### How to choose the lease parameter in TiDB?

The lease parameter (`--lease=60`) is set from the command line when starting a TiDB server. The value of the lease parameter impacts the Database Schema Changes (DDL) speed of the current session. In the testing environments, you can set the value to 1s for to speed up the testing cycle. But in the production environments, it is recommended to set the value to minutes (for example, 60) to ensure the DDL safety.

#### Can I use other key-value storage engines with TiDB?

Yes. Besides TiKV, TiDB supports many popular standalone storage engines, such as GolevelDB, RocksDB and BoltDB. If the storage engine is a KV engine that supports transactions and it provides a client that meets the interface requirement of TiDB, then it can connect to TiDB.

#### Where is the Raft log stored in TiDB?

In RocksDB.

### TiKV

#### Why the TiKV data directory is gone?

For TiKV, the default value of the `--data-dir` parameter is `/tmp/tikv/store`. In some virtual machines, restarting the operating system results in removing all the data under the `/tmp` directory. It is recommended to set the TiKV data directory explicitly by setting the `--data-dir` parameter.

#### The `cluster ID mismatch` message is displayed when starting TiKV.

This is because the cluster ID stored in local TiKV is different from the cluster ID specified by PD. When a new PD cluster is deployed, PD generates random cluster IDs. TiKV gets the cluster ID from PD and stores the cluster ID locally when it is initialized. The next time when TiKV is started, it checks the local cluster ID with the cluster ID in PD. If the cluster IDs don't match, the `cluster ID mismatch` message is displayed and TiKV exits.

If you previously deploy a PD cluster, but then you remove the PD data and deploy a new PD cluster, this error occurs because TiKV uses the old data to connect to the new PD cluster.

#### The `duplicated store address` message is displayed when starting TiKV.

This is because the address in the startup parameter has been registered in the PD cluster by other TiKVs. This error occurs when there is no data folder under the directory that TiKV `--store` specifies, but you use the previous parameter to restart the TiKV.

To solve this problem, use the [store delete](https://github.com/pingcap/pd/tree/master/pdctl#store-delete-) function to delete the previous store and then restart TiKV.

#### Would the key be too long according to the TiDB setting?

The RocksDB compresses the key.

### TiSpark

#### Where is the user guide of TiSpark?

See the [TiSpark User Guide](https://github.com/pingcap/tispark/blob/master/docs/userguide.md).

## Operations

### Install

#### Why the modified `toml` configuration for TiKV/PD does not take effect?

You need to set the `--config` parameter in TiKV/PD to make the `toml` configuration effective. TiKV/PD does not read the configuration by default.

#### What can I do if the file system of my data disk is XFS and cannot be changed?

Because of the [bug](https://github.com/facebook/rocksdb/pull/2038) in RocksDB for the XFS system and certain Linux kernel, we do not recommend using the XFS file system.

Currently, you can run the following test script on the TiKV deployment disk. If the result is 5000, you can try to use it, but it is not recommended for production use.

    #!/bin/bash
    touch tidb_test
    fallocate -n -o 0 -l 9192 tidb_test
    printf 'a%.0s' {1..5000} > tidb_test
    truncate -s 5000 tidb_test
    fallocate -p -n -o 5000 -l 4192 tidb_test
    LANG=en_US.UTF-8 stat tidb_test |awk 'NR==2{print $2}'
    rm -rf tidb_test

#### Can chrony meet the requirement of time synchronization?

Yes. Only if you can guarantee the time synchronization of PD machines.

### Scale

#### How does TiDB scale?

As your business grows, your database might face the following three bottlenecks:

- Lack of storage resources which means that the disk space is not enough.

- Lack of computing resources such as high CPU occupancy.

- Not enough throughputs.

You can scale TiDB as your business grows.

- If the disk space is not enough, you can increase the capacity simply by adding more TiKV nodes. When the new node is started, PD will migrate the data from other nodes to the new node automatically.

- If the computing resources are not enough, check the CPU consumption situation first before adding more TiDB nodes or TiKV nodes. When a TiDB node is added, you can configure it in the Load Balancer.

- If the throughputs are not enough, you can add both TiDB nodes and TiKV nodes.

### Monitor

#### The monitor can't show all the metrics.

Check the time difference between the machine time of the monitor and the time within the cluster. If it is large, you can correct the time and the monitor will display all the metrics.

### Migrate

#### Can a MySQL application be migrated to TiDB?

Yes. Your applications can be migrated to TiDB without changing a single line of code in most cases. You can use [checker](https://github.com/pingcap/tidb-tools/tree/master/checker) to check whether the Schema in MySQL is compatible with TiDB.

### Performance tuning

### Backup and restore

### Misc

#### How does TiDB manage user account?

TiDB follows MySQL user authentication mechanism. You can create user accounts and authorize them.

- You can use MySQL grammar to create user accounts. For example, you can create a user account by using the following statement:

  ```
  CREATE USER 'test'@'localhost' identified by '123';
  ```

  The user name of this account is "test"; the password is “123" and this user can login from localhost only.

  You can use the `Set Password` statement to set and change the password. For example, to set the password for the default "root" account, you can use the following statement:

  ```
  SET PASSWORD FOR 'root'@'%' = '123';
  ```

- You can also use MySQL grammar to authorize this user. For example, you can grant the read privilege to the "test" user by using the following statement:

  ```
  GRANT SELECT ON \*.\* TO  'test'@'localhost';
  ```

See more about [privilege management](sql/privilege.md).

#### Where are the TiDB/PD/TiKV logs?

By default, TiDB/PD/TiKV outputs the logs to standard error. If a file is specified using `--log--file` during the startup, the log is output to the file and rotated daily.

#### How to safely stop TiDB?

If the cluster is deployed through ansible, you can use the command `ansible-playbook stop.yml` to stop the TiDB cluster. If the cluster is not deployed through ansible, `kill` all the services directly. The components of TiDB will do `graceful shutdown`.

#### Can `kill` be executed in TiDB?

You can `kill` DML statements. First use `show processlist` to find the id corresponding with the session, and then execute `kill tidb connection id`.

But currently, you cannot `kill` DDL statements. Once you start executing DDL statements, you cannot stop them unless something goes wrong. If something goes wrong, the DDL statements will stop executing.

## SQL

### SQL syntax

#### The error message `transaction too large` is displayed.

As distributed transactions need to conduct two-phase commit and the bottom layer performs Raft replication, if a transaction is very large, the commit process would be quite slow and the following Raft replication flow is thus struck. To avoid this problem, we limit the transaction size:

- Each Key-Value entry is no more than 6MB
- The total number of Key-Value entry is no more than 300,000 rows
- The total size of Key-Value entry is no more than 100MB

There are [similar limits](https://cloud.google.com/spanner/docs/limits) on Google Cloud Spanner.

**Solution:**

1. When you import data, insert in batches and it'd be better keep the number of one batch within 10,000 rows.

2. As for `insert` and `select`, you can open the hidden parameter `set @@session.tidb_batch_insert=1;`, and `insert` will execute large transactions in batches. In this way, you can avoid the timeout caused by large transactions, but this may lead to the loss of atomicity. An error in the process of execution leads to partly inserted transaction. Therefore, use this parameter only when necessary, and use it in session to avoid affecting other statements. When the transaction is finished, use `set @@session.tidb_batch_insert=0` to close it.

3. As for `delete` and `update`, you can use `limit` plus circulation to operate.

#### Check the running DDL job

```sql
admin show ddl
```

Note: The DDL cannot be cancelled unless it goes wrong.

### SQL optimization

#### How to optimize `select count(1)`?

The `count(1)` statement counts the total number of rows in a table. Improving the degree of concurrency can significantly improve the speed. To modify the concurrency, refer to the [document](sql/tidb-specific.md#tidb_distsql_scan_concurrency). But it also depends on the CPU and I/O resources. TiDB accesses TiKV in every query. When the amount of data is small, all MySQL is in memory, and TiDB needs to conduct a network access.

**Note**:

1. See the [system requirements](op-guide/recommendation.md).
2. Improve the concurrency. The default value is 10. You can improve it to 50 and have a try. But usually the improvement is 2-4 times of the default value.
3. Test the `count` in the case of large amount of data.
4. Optimize [TiKV configuration](op-guide/tune-TiKV.md).
