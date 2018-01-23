---
title: TiDB FAQ
category: faq
---

# TiDB FAQ

This document lists the Most Frequently Asked Questions about TiDB.

## Product

### General

#### What is TiDB?

TiDB is a distributed SQL database that features in horizontal scalability, high availability and consistent distributed transactions. It also enables you to use MySQL’s SQL syntax and protocol to manage and retrieve data.

#### Is TiDB based on MySQL?

No. TiDB supports MySQL syntax and protocol, but it is a new open source database that is developed and maintained by PingCAP, Inc.

#### What is the difference between TiDB and MySQL Group Replication?

MySQL Group Replication (MGR) is a high available solution based on the standalone MySQL, but it does not solve the scalability problem. TiDB is more suitable for distributed scenarios in architecture, and the various decisions in the development process are also based on distributed scenarios.

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

TiDB uses the [Raft consensus algorithm](https://raft.github.io/) to ensure consistency among multiple replicas. At the bottom layer, TiDB uses a model of replication log + State Machine to replicate data. For the write requests, the data is written to a Leader and the Leader then replicates the command to its Followers in the form of log. When the majority of nodes in the cluster receive this log, this log is committed and can be applied into the State Machine. TiDB has the latest data even if a minority of the replicas are lost.

#### Does TiDB support distributed transactions?

Yes. The transaction model in TiDB is inspired by Google’s Percolator, a paper published in 2006. It’s mainly a two-phase commit protocol with some practical optimizations. This model relies on a timestamp allocator to assign monotone increasing timestamp for each transaction, so the conflicts can be detected. PD works as the timestamp allocator in a TiDB cluster.

#### Does the conflict of multiple transactions (such as updating the same row at the same time) cause commit failure of some transactions?

Yes. The transaction that fails to commit in a transaction conflict retreats and retries at the appropriate time. The number of retries in TiDB is 10 times by default.

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

TiDB is self-healing. All of the three components, TiDB, TiKV and PD, can tolerate failures of some of their instances. With its strong consistency guarantee, whether it’s data machine failures or even downtime of an entire data center, your data can be recovered automatically. For more information, see [High availability](overview.md#high-availability).

#### Does TiDB release space immediately after deleting data?

`DELETE`, `TRUNCATE` and `DROP` do not release space immediately. For `TRUNCATE` and `DROP` operations, TiDB deletes the data and releases the space after reaching the GC (garbage collection) time (10 minutes by default). For the `DELETE` operation, TiDB deletes the data and does not release the space based on the GC mechanism, but reuses the space when subsequent data is committed to RocksDB and compacted.

#### Can I execute DDL operations on the target table when loading data?

No. None of the DDL operations can be executed on the target table when you load data, otherwise the data fails to load.

#### Does TiDB support the `replace into` syntax?

Yes. But the `load data` does not support the `replace into` syntax.

#### How to export the data in TiDB?

Currently, TiDB does not support `select into outfile`. You can use the following methods to export the data in TiDB:

- See [MySQL uses mysqldump to export part of the table data](http://blog.csdn.net/xin_yu_xin/article/details/7574662) in Chinese and export data using mysqldump and the WHERE condition.
- Use the MySQL client to export the results of `select` to a file.

#### Does TiDB support session timeout?

Currently, TiDB does not support session timeout in the database level. If you want to implement session timeout, use the session id started by side records in the absence of LB (Load Balancing), and customize the session timeout on the application. After timeout, kill sql using `kill tidb id` on the node that starts the query. It is currently recommended to implement session timeout using applications. When the timeout time is reached, the application layer reports an exception and continues to execute subsequent program segments.

#### What is the TiDB version management strategy for production environment? How to avoid frequent upgrade?

Currently, TiDB has a standard management of various versions. Each release contains a detailed change log and [release notes](https://github.com/pingcap/TiDB/releases). Whether it is necessary to upgrade in the production environment depends on the application system. It is recommended to learn the details about the functional differences between the previous and later versions before upgrading.

Take `Release Version: v1.0.3-1-ga80e796` as an example of version number description:

- `v1.0.3` indicates the standard GA version.
- `-1` indicates the current version has one commit.
- `ga80e796` indicates the version `git-hash`.

#### What's the difference between various TiDB master versions? How to avoid using the wrong TiDB-Ansible version?

The TiDB community is highly active. After the GA release, the engineers have been keeping optimizing and fixing bugs. Therefore, the TiDB version is updated quite fast. If you want to keep informed of the latest version, see [TiDB Weekly update](https://pingcap.com/weekly/).

It is recommended to deploy the TiDB cluster using the latest version of TiDB-Ansible, which will also be updated along with the TiDB version. Besides, TiDB has a unified management of the version number after GA release. You can view the version number using the following two methods:

- `select tidb_version()`
- `tidb-server -V`

#### What's the recommended solution for the deployment of three geo-distributed data centers?

The architecture of TiDB guarantees that it fully supports geo-distribution and multi-activeness. Your data and applications are always-on. All the outages are transparent to your applications and your data can recover automatically. The operation depends on the network latency and stability. It is recommended to keep the latency within 5ms. Currently, we already have similar use cases. For details, contact info@pingcap.com. 

#### Does TiDB provide any other knowledge resource besides the documentation?

Currently, [TiDB documentation](https://www.pingcap.com/docs/) is the most important and timely way to get knowledge of TiDB. In addition, we also have some technical communication groups. If you have any needs, contact info@pingcap.com.

#### What's the relationship between the TiDB cluster capacity (QPS) and the number of nodes? How to predict the capacity?

The relationship is roughly linear. For the current QPS that each cluster node can bear, see [TiDB official test document](benchmark/sysbench.md).

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

Theoretically, the smaller of the tolerance, the better. During leader changes, if the clock goes back, the process won't proceed until it catches up with the previous leader. PD can tolerate any synchronization error, but a larger error value means a longer period of service stop during the leader change.

#### How does the client connection find PD?

The client connection can only access the cluster through TiDB. TiDB connects PD and TiKV. PD and TiKV are transparent to the client. When TiDB connects to any PD, the PD tells TiDB who is the current leader. If this PD is not the leader, TiDB reconnects to the leader PD.

#### What is the difference between the `leader-schedule-limit` and `region-schedule-limit` scheduling parameters in PD?

The `leader-schedule-limit` scheduling parameter is used to balance the leader number of different TiKV servers, affecting the load of query processing. The `region-schedule-limit` scheduling parameter is used to balance the replica number of different TiKV servers, affecting the data amount of different nodes.

#### Is the number of replicas in each region configurable? If yes, how to configure it?

Yes. Currently, you can only update the global number of replicas. When started for the first time, PD reads the configuration file (conf/pd.yml) and uses the max-replicas configuration in it. If you want to update the number later, use the pd-ctl configuration command `config set max-replicas $num` and view the enabled configuration using `config show all`. The updating does not affect the applications and is configured in the background.

Make sure that the total number of TiKV instances is always greater than or equal to the number of replicas you set. For example, 3 replicas need 3 TiKV instances at least. Additional storage requirements need to be estimated before increasing the number of replicas. For more information about pd-ctl, see [PD Control User Guide](tools/pd-control.md).

#### How to delete the monitoring data of a cluster node that is offline?

The offline node usually indicates the TiKV node. You can determine whether the offline process is finished by the pd-ctl or the monitor. After the node is offline, perform the following steps:

1. Manually stop the relevant services on the offline node.
2. Delete the `node_exporter` data of the corresponding node from the Prometheus configuration file.
3. Delete the data of the corresponding node from Ansible `inventory.ini`.

#### How to check the health status of the whole cluster when lacking command line cluster management tools?

You can determine the general status of the cluster using the pd-ctl tool. For detailed cluster status, you need to use the monitor to determine.

### TiDB

#### How to choose the lease parameter in TiDB?

The lease parameter (`--lease=60`) is set from the command line when starting a TiDB server. The value of the lease parameter impacts the Database Schema Changes (DDL) speed of the current session. In the testing environments, you can set the value to 1s for to speed up the testing cycle. But in the production environments, it is recommended to set the value to minutes (for example, 60) to ensure the DDL safety.

#### Can I use other key-value storage engines with TiDB?

Yes. Besides TiKV, TiDB supports many popular standalone storage engines, such as GolevelDB and BoltDB. If the storage engine is a KV engine that supports transactions and it provides a client that meets the interface requirement of TiDB, then it can connect to TiDB.

#### Where is the Raft log stored in TiDB?

In RocksDB.

#### Why it is very slow to run DDL statements sometimes?

Possible reasons:

- If you run multiple DDL statements together, the last few DDL statements might run slowly. This is because the DDL statements are executed serially in the TiDB cluster.
- After you start the cluster successfully, the first DDL operation may take a longer time to run, usually around 30s. This is because the TiDB cluster is electing the leader that processes DDL statements.
- In rolling update or shutdown update, the processing time of DDL statements in the first ten minutes after starting TiDB is affected by the server stop sequence (stopping PD -> TiDB), and the condition where TiDB does not clean up the registration data in time because TiDB is stopped using the `kill -9` command. When you run DDL statements during this period, for the state change of each DDL, you need to wait for 2 * lease (lease = 10s).
- If a communication issue occurs between a TiDB server and a PD server in the cluster, the TiDB server cannot get or update the version information from the PD server in time. In this case, you need to wait for 2 * lease for the state processing of each DDL.

#### ERROR 2013 (HY000): Lost connection to MySQL server during query.

Troubleshooting methods:

- Check whether `panic` exists in the log.
- Check whether `oom` exists in `dmesg` using the `dmesg |grep -i oom` command.
- A long time of not accessing can also lead to this error, usually caused by the tcp timeout. If not used for a long time, the tcp is killed by the operating system.

#### Can I use S3 as the backend storage in TiDB?

No. Currently, TiDB only supports the distributed storage engine and the Goleveldb/Rocksdb/Boltdb engine.

Does TiDB support the following DDL?

```
CREATE TABLE ... LOCATION "s3://xxx/yyy"
```

If you can implement the S3 storage engine client, it should be based on the TiKV interface.

#### Can the `Infomation_schema` support more real information?

The tables in `Infomation_schema` exist mainly for compatibility with MySQL, and some third-party software queries information in the tables. Currently, most of those tables are null. More parameter information is to be involved in the tables as TiDB updates later.

For the `Infomation_schema` that TiDB currently supports, see [The TiDB System Database](sql/system-database.md).

#### What's the optimization advice on different TiDB storage?

For OLTP scenarios, TiDB requires high I/O disks for data access and operation. Therefore, it is recommended to use NVMe SSD as the storage disks in TiDB best practices.

#### What's the explanation of the TiDB Backoff type scenario?

In the communication process between the TiDB server and the TiKV server, the `Server is busy` or `backoff.maxsleep 20000ms` log message is displayed when processing a large volume of data. This is because the system is busy while the TiKV server processes data. At this time, usually you can view that the TiKV host resources usage rate is high. If this occurs, you can increase the server capacity according to the resources usage.

#### What's the explanation of the TiClient type scenario?

In the process of the TiDB server accesses the TiKV server through the KV interface as a client, `TiClient Region Error` describes the error type and metrics generated when the TiDB server operates the Region data in the TiKV server. The error types include `not_leader` and `stale_epoch`. When the TiDB server handles the Region leader data based on its caches, if the Region leader is migrated or the current Region information in TiKV is inconsistent with the routing information in TiDB, error occurs. Generally in this case, the TiDB server automatically regains the latest routing information from PD and redos the previous operation.

### TiKV

#### What is the recommended number of replicas in the TiKV cluster? Is it better to keep the minimum number for high availability?

Use 3 replicas for test. If you increase the number of replicas, the performance declines but it is more secure. Whether to configure more replicas depends on the specific business needs.

#### Can TiKV specify a standalone replica machine (to separate cluster data and replicas)?

No.

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

#### TiKV master and slave use the same compression algorithm, why the results are different?

Currently, some files of TiKV master have a higher compression rate, which depends on the underlying data distribution and RocksDB implementation. It is normal that the data size fluctuates occasionally. The underlying storage engine adjusts data as needed.

#### What are the features of TiKV block cache?

TiKV implements the Column Family (CF) feature of RocksDB. By default, the KV data is eventually stored in the 3 CFs (default, write and lock) within RocksDB.

- The default CF stores real data and the corresponding parameter is in [rocksdb.defaultcf]. The write CF stores the data version information (MVCC) and index-related data, and the corresponding parameter is in `[rocksdb.writecf]`. The lock CF stores the lock information and the system uses the default parameter.
- The Raft RocksDB instance stores Raft logs. The default CF mainly stores Raft logs and the corresponding parameter is in `[raftdb.defaultcf]`.
- Each CF has an individual block-cache to cache data blocks and improve RocksDB read speed. The size of block-cache is controlled by the `block-cache-size` parameter. A larger value of the parameter means more hot data can be cached and is more favorable to read operation. At the same time, it consumes more system memory.
- Each CF has an individual write-buffer and the size is controlled by the `write-buffer-size` parameter.

#### Explanation of TiKV threads

- View the threads number in the TiKV server using `ps -Tp ${tikvPID}`.
- Login the TiKV server and view the status of CPU used by threads.
- Login Grafana and view the Thread-CPU tab in the TiKV dashboard, where the status of CPU used by all threads is involved.

| Thread name | Description |
| ---- | ----- |
| grpc-server-* | the network communication thread between TiKV and neighbors, TiDB, PD |
| raftstore-* |  the thread used to handle the Raft information; the CPU used by this thread rises when writing a large volume of data |
| sched-worker-* | the thread that TiKV writing data passes; the CPU used by this thread rises when writing a large volume of data |
| endpoint-* | the thread that TiKV reading data passes; the CPU used by this thread rises when reading a large volume of data or TableScan occurs in `explain` |
| apply worker | the thread that the writing data passes into RocksDB after finishing data writing |
| rocksdb:bg* | the thread that RocksDB executes compaction on data |

#### Why it occurs that "TiKV channel full"?

- The Raftstore thread is too slow. You can view the CPU usage status of Raftstore.
- TiKV is too busy (read, write, disk I/O, etc.) and cannot manage to handle it.

#### Why does TiKV frequently switch Region leader?

- Network problem leads to the failure of communication between nodes. You can view the monitoring information of Report failures.
- The original main leader node fails, and cannot send information to the follower in time.
- The Raftstore thread fails.

#### If the leader node is down, will the service be affected? How long?

TiDB uses Raft to synchronize data among multiple replicas and guarantees the strong consistency of data. If one replica goes wrong, the other replicas can guarantee data security. The default number of replicas in each Region is 3. Based on the Raft protocol, a leader is elected in each Region, and if a single Region leader fails, a new Region leader is soon elected after a maximum of 2 * lease time (lease time is 10 seconds).

#### What are the TiKV scenarios that take up high I/O, memory, CPU, and exceed the parameter configuration?

Writing or reading a large volume of data in TiKV takes up high I/O, memory and CPU. Executing very complex queries costs a lot of memory and CPU resources, such as the scenario that generates large intermediate result sets.

### TiSpark

#### Where is the user guide of TiSpark?

See the [TiSpark User Guide](tispark/tispark-user-guide.md).

#### TiSpark cases

See [TiSpark Cases](https://github.com/zhexuany/tispark_examples).

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

#### Can I configure chrony to meet the requirement of time synchronization in TiDB?

Yes. Only if you can guarantee the time synchronization of PD machines. If you use chrony to configure time synchronization, before you run the `deploy` scripts, set the `enable_ntpd` in the `inventory.ini` configuration file to `False` (`enable_ntpd = False`).

#### Does TiDB support SAS/SATA disks or mixed deployment of SSD/SAS disks?

No. For OLTP scenarios, TiDB requires high I/O disks for data access and operation. As a distributed database with strong consistency, TiDB has some write amplification such as replica replication and bottom layer storage compaction. Therefore, it is recommended to use NVMe SSD as the storage disks in TiDB best practices. Besides, the mixed deployment of TiKV and PD is not supported.

#### Is there a graphical deployment tool for TiDB?

Currently no.

#### Is there any other way of deploying TiDB if I don't want to use Ansible?

Besides Ansible, you can also use Docker to deploy TiDB. See [Docker Deployment](op-guide/docker-deployment.md). It is recommended to deploy TiDB using Ansible, which can optimize and monitor the cluster host, automatically generate scripts of startup, stop and upgrade that are easy for later management, and deploy the monitoring system, making it more clear when testing, tuning and debugging.

#### Can I deploy the development environment on a single machine?

Yes. You can use `docker-compose` to deploy a cluster locally, which includes the cluster monitor. You can also customize the software version of each component, the number of instances, and the configuration files based on your need. For details, see [TiDB Docker Compose documents](https://github.com/pingcap/tidb-docker-compose).

#### What's the maximum number of concurrent connections that TiDB supports?

The current TiDB version has no limit for the maximum number of concurrent connections. If too large concurrency leads to an increase of response time, you can increase the capacity by adding TiDB nodes.

#### Can I deploy TiDB and TiKV together?

Because both TiDB and TiKV have a high demand on CPU and memory, it is not recommended to deploy them on a same node.

#### Why it is recommended to deploy the TiDB cluster on CentOS 7?

As an open source distributed NewSQL database with high performance, TiDB can be deployed in the Intel architecture server and major virtualization environments and runs well. TiDB supports most of the major hardware networks and Linux operating systems. For details, see [Software and Hardware Requirements](op-guide/recommendation.md) for deploying TiDB.

We have done a lot of TiDB testing on CentOS 7 and have plenty of best practices for deploying TiDB on this system. Therefore, it is recommended to deploy TiDB on Linux operating systems of CentOS 7 or later versions.

#### What's the purposes of 2 network cards of 10 gigabit?

As a distributed cluster, TiDB has a high demand on time, especially for PD, because PD needs to distribute unique timestamps. If the time in PD is not consistent, it takes longer waiting time when switching PD. The bond of two network cards guarantees the stability of data transmission, and 10 gigabit guarantees the transmission speed. Gigabit network cards are prone to meet bottlenecks, therefore it is strongly recommended to use 10 gigabit netword cards.

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

#### Should I deploy the TiDB monitoring framework (Prometheus + Grafana) on a standalone machine or on multiple machines? What is the recommended CPU and memory?

The monitoring machine is recommended to use standalone deployment. It is recommended to use 8 core CPU, 32 GB+ memory and 500 GB+ hard disk.

#### The monitor can't show all the metrics.

Check the time difference between the machine time of the monitor and the time within the cluster. If it is large, you can correct the time and the monitor will display all the metrics.

#### How to configure to monitor Syncer status?

Download and import [Syncer Json](https://github.com/pingcap/docs/blob/master/etc/Syncer.json) to Grafana. Edit the Prometheus configuration file and add the following content:

```
- job_name: ‘syncer_ops’ // task name
    static_configs:
      - targets: [’10.10.1.1:10096’] // Syncer monitoring address and port, informing Prometheus to pull the data of Syncer
```

Restart Prometheus.

#### Is there a better way of monitoring the key metrics?

The monitoring system of TiDB consists of Prometheus and Grafana. From the dashboard in Grafana, you can monitor various running metrics of TiDB which include the monitoring metrics of system resources, of client connection and SQL operation, of internal communication and Region scheduling. With these metrics, the database administrator can better understand the system running status, running bottlenecks and so on. In the practice of monitoring these metrics, we list the key metrics of each TiDB component. Generally you only need to pay attention to these common metrics. For details, see [Key Metrics](op-guide/dashboard-overview-info.md).

### Migrate

#### Can a MySQL application be migrated to TiDB?

Yes. Your applications can be migrated to TiDB without changing a single line of code in most cases. You can use [checker](https://github.com/pingcap/tidb-tools/tree/master/checker) to check whether the Schema in MySQL is compatible with TiDB.

#### Accidentally import the MySQL user table into TiDB and cannot login, how to restore?

Restart the TiDB service, add the `-skip-grant-table=true` parameter in the configuration file. Login the cluster and recreate the mysql.user table using the following statement:

```sql
DROP TABLE IF EXIST mysql.user;

CREATE TABLE if not exists mysql.user (
    Host        CHAR(64),
    User        CHAR(16),
    Password      CHAR(41),
    Select_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Insert_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Update_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Delete_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Create_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Drop_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Process_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Grant_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    References_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Alter_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Show_db_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Super_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Create_tmp_table_priv   ENUM('N','Y') NOT NULL DEFAULT 'N',
    Lock_tables_priv    ENUM('N','Y') NOT NULL DEFAULT 'N',
    Execute_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Create_view_priv    ENUM('N','Y') NOT NULL DEFAULT 'N',
    Show_view_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Create_routine_priv   ENUM('N','Y') NOT NULL DEFAULT 'N',
    Alter_routine_priv    ENUM('N','Y') NOT NULL DEFAULT 'N',
    Index_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Create_user_priv    ENUM('N','Y') NOT NULL DEFAULT 'N',
    Event_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Trigger_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    PRIMARY KEY (Host, User));

INSERT INTO mysql.user VALUES ("%", "root", "", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y");
```

#### How to import data into or export data from TiDB?

TiDB complies with MySQL protocol. You can use Mydumper to export data and Loader to import data, which is similar to MySQL.

#### How long does it take to reclaim disk space after deleting data?

None of the `Delete`, `Truncate` and `Drop` operations releases data immediately. For the `Truncate` and `Drop` operations, after the TiDB GC (Garbage Collection) time (10 minutes by default), the data is deleted and the space is released. For the `Delete` operation, the data is deleted but the space is not released according to TiDB GC. When data is written into RocksDB and executes `Compact`, the space is reused.

#### Why does the query speed getting slow after deleting data?

Deleting a large amount of data leaves a lot of useless keys, affecting the query efficiency. Currently the Region Merge feature is in development, which is expected to solve this problem. For details, see the [deleting data section in TiDB Best Practices](https://pingcap.com/blog/2017-07-24-tidbbestpractice/#write). 

#### What is the most efficient way of deleting data?

When deleting a large amount of data, it is recommended to use `Delete * from t where xx limit 5000;`. It deletes through the loop and uses `Affected Rows == 0` as a condition to end the loop, so as not to exceed the limit of transaction size. With the prerequisite of meeting business filtering logic, it is recommended to add a strong filter index column or directly use the primary key to select the range, such as `id >= 5000*n+m and id < 5000*(n+1)+m`.

If the amount of data that needs to be deleted at a time is very large, this loop method will get slower and slower because each deletion traverses backward. After deleting the previous data, lots of deleted flags will remain for a short period (then all will be Garbage Collected) and influence the following Delete statement. If possible, it is recommended to refine the Where condition. See [details in TiDB Best Practices](https://pingcap.com/blog/2017-07-24-tidbbestpractice/#write).

#### How to deal with synchronization error or interrupt of Syncer/Drainer?

- View the log and analyze the reason.
- View the [Syncer](tools/syncer.md)/[Drainer](tools/tidb-binlog-kafka.md#configure-pumpdrainer) documents.
- Update Syncer/Drainer to the latest version.

### Performance tuning

#### How to improve the data loading speed in TiDB?

- Currently Lightning is in development for distributed data import. It should be noted that the data import process does not perform a complete transaction process for performance reasons. Therefore, the ACID constraint of the data being imported during the import process cannot be guaranteed. The ACID constraint of the imported data can only be guaranteed after the entire import process ends. Therefore, the applicable scenarios mainly include importing new data (such as a new table or a new index) or the full backup and restoring (Truncate the original table and then import data).
- Data loading in TiDB is related to the status of disks and the whole cluster. When loading data, pay attention to metrics like the disk usage rate of the host, TiClient Error, Backoff, Thread CPU and so on. You can analyze the bottlenecks using these metrics.

### Backup and restore

### Misc

#### How does TiDB manage user account?

TiDB follows MySQL user authentication mechanism. You can create user accounts and authorize them.

- You can use MySQL grammar to create user accounts. For example, you can create a user account by using the following statement:

    ```
    CREATE USER 'test'@'localhost' identified by '123';
    ```
    
    The user name of this account is "test"; the password is “123" and this user can login from localhost only.

- You can use the `Set Password` statement to set and change the password. For example, to set the password for the default "root" account, you can use the following statement:
    
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

#### What is the function of supervise/svc/svstat service?

- supervise: the daemon process, to manage the processes
- svc: to start and stop the service
- svstat: to check the process status

#### How to locate the problem when it is very slow to write data using JDBC prepare?

When you write data using `prepareStatement` of JDBC, the `addBatch` operation does not access the database, and only the `executeBatch` operation accesses the database. Getting the accurate execution time of `addBatch` and `executeBatch` helps to determine whether the cause of slow data writing is in the database or in other components such as front end caches.

## SQL

### SQL syntax

#### The error message `transaction too large` is displayed.

As distributed transactions need to conduct two-phase commit and the bottom layer performs Raft replication, if a transaction is very large, the commit process would be quite slow and the following Raft replication flow is thus struck. To avoid this problem, we limit the transaction size:

- Each Key-Value entry is no more than 6MB
- The total number of Key-Value entry is no more than 300,000 rows
- The total size of Key-Value entry is no more than 100MB

There are [similar limits](https://cloud.google.com/spanner/docs/limits) on Google Cloud Spanner.

**Solution:**

1. When you import data, insert in batches and keep the number of rows within 10,000 for each batch.

2. As for `insert` and `select`, you can open the hidden parameter `set @@session.tidb_batch_insert=1;`, and `insert` will execute large transactions in batches. In this way, you can avoid the timeout caused by large transactions, but this may lead to the loss of atomicity. An error in the process of execution leads to partly inserted transaction. Therefore, use this parameter only when necessary, and use it in session to avoid affecting other statements. When the transaction is finished, use `set @@session.tidb_batch_insert=0` to close it.

3. As for `delete` and `update`, you can use `limit` plus circulation to operate.

#### View the DDL job.

- `admin show ddl`: to view the running DDL job
- `admin show ddl jobs`: to view all the results in the current DDL job queue (including tasks that are running and waiting to run) and the last ten results in the completed DDL job queue

#### View the progress of adding an index.

Use `admin show ddl` to view the current job of adding an index:

```sql
mysql> admin show ddl;
+------------+--------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+
| SCHEMA_VER | OWNER                                | JOB                                                                                                                             | SELF_ID                              |
+------------+--------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+
|         69 | 9deb4179-fb5c-4040-b3b3-2e8fc585d8db | ID:102, Type:add index, State:running, SchemaState:write reorganization, SchemaID:81, TableID:90, RowCount:1293344122, ArgLen:0 | 9deb4179-fb5c-4040-b3b3-2e8fc585d8db |
+------------+--------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+

```

- The `OWNER` represents the TiDB server that is running this DDL statement.
- The `JOB` lists the detailed information of the task.
- The `SchemaID:81, TableID:90` in `JOB` represents the database ID and the user table ID.
- The `RowCount:1293344122` in `JOB` represents the numer of rows that have been processed currently.

#### The `column Show_db_priv not found` message is displayed when executing `grant SHOW DATABASES on db.*`.

`SHOW DATABASES` is a global privilege rather than a database-level privilege. Therefore, you cannot grant this privilege to a database. You need to grant all databases:

```
grant SHOW DATABASES on *.*
```

### SQL optimization

#### How to view the query execution plan of TiDB?

See [Understand the Query Execution Plan](sql/understanding-the-query-execution-plan.md).

#### How to optimize `select count(1)`?

The `count(1)` statement counts the total number of rows in a table. Improving the degree of concurrency can significantly improve the speed. To modify the concurrency, refer to the [document](sql/tidb-specific.md#tidb_distsql_scan_concurrency). But it also depends on the CPU and I/O resources. TiDB accesses TiKV in every query. When the amount of data is small, all MySQL is in memory, and TiDB needs to conduct a network access.

Recommendations:

1. Improve the hardware configuration. See [Software and Hardware Requirements](op-guide/recommendation.md).
2. Improve the concurrency. The default value is 10. You can improve it to 50 and have a try. But usually the improvement is 2-4 times of the default value.
3. Test the `count` in the case of large amount of data.
4. Optimize the TiKV configuration. See [Performance Tuning for TiKV](op-guide/tune-TiKV.md).

#### The efficiency of `FROM_UNIXTIME` is low.

Do not use `FROM_UNIXTIME` to get the system time. It is recommended to convert `datetime` to timestamp and compare. Currently, `FROM_UNIXTIME` does not support indexes.

#### It's troublesome to manually analyze or set timing for the Analyze table. When will automatic analysis be supported?

The automatic analysis hasn't been listed on the plan, but we are developing the feature of automatically and incrementally updating histograms.
