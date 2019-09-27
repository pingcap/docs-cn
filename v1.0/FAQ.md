---
title: TiDB FAQ
category: faq
---

# TiDB FAQ

This document lists the Most Frequently Asked Questions about TiDB.

## About TiDB

### TiDB introduction and architecture

#### What is TiDB?

TiDB is a distributed SQL database that features in horizontal scalability, high availability and consistent distributed transactions. It also enables you to use MySQL’s SQL syntax and protocol to manage and retrieve data.

#### What is TiDB's architecture?

The TiDB cluster has three components: the TiDB server, the PD (Placement Driver) server, and the TiKV server. For more details, see [TiDB architecture](overview/#tidb-architecture).

#### Is TiDB based on MySQL?

No. TiDB supports MySQL syntax and protocol, but it is a new open source database that is developed and maintained by PingCAP, Inc.

#### What is the respective responsibility of TiDB, TiKV and PD (Placement Driver)?

- TiDB works as the SQL computing layer, mainly responsible for parsing SQL, specifying query plan, and generating executor.
- TiKV works as a distributed Key-Value storage engine, used to store the real data. In short, TiKV is the storage engine of TiDB.
- PD works as the cluster manager of TiDB, which manages TiKV metadata, allocates timestamps, and makes decisions for data placement and load balancing.

#### Is it easy to use TiDB?

Yes, it is. When all the required services are started, you can use TiDB as easily as a MySQL server. You can replace MySQL with TiDB to power your applications without changing a single line of code in most cases. You can also manage TiDB using the popular MySQL management tools.

#### How is TiDB compatible with MySQL?

Currently, TiDB supports the majority of MySQL 5.7 syntax, but does not support trigger, stored procedures, user-defined functions, and foreign keys. For more details, see [Compatibility with MySQL](sql/mysql-compatibility.md).

#### How is TiDB highly available?

TiDB is self-healing. All of the three components, TiDB, TiKV and PD, can tolerate failures of some of their instances. With its strong consistency guarantee, whether it’s data machine failures or even downtime of an entire data center, your data can be recovered automatically. For more information, see [High availability](overview.md#high-availability).

#### How is TiDB strongly consistent?

TiDB uses the [Raft consensus algorithm](https://raft.github.io/) to ensure consistency among multiple replicas. At the bottom layer, TiDB uses a model of replication log + State Machine to replicate data. For the write requests, the data is written to a Leader and the Leader then replicates the command to its Followers in the form of log. When the majority of nodes in the cluster receive this log, this log is committed and can be applied into the State Machine. TiDB has the latest data even if a minority of the replicas are lost.

#### Does TiDB support distributed transactions?

Yes. The transaction model in TiDB is inspired by Google’s Percolator, a paper published in 2006. It’s mainly a two-phase commit protocol with some practical optimizations. This model relies on a timestamp allocator to assign monotone increasing timestamp for each transaction, so the conflicts can be detected. PD works as the timestamp allocator in a TiDB cluster.

#### What programming language can I use to work with TiDB?

Any language supported by MySQL client or driver.

#### Can I use other Key-Value storage engines with TiDB?

Yes. Besides TiKV, TiDB supports many popular standalone storage engines, such as GolevelDB and BoltDB. If the storage engine is a KV engine that supports transactions and it provides a client that meets the interface requirement of TiDB, then it can connect to TiDB.

#### What's the recommended solution for the deployment of three geo-distributed data centers?

The architecture of TiDB guarantees that it fully supports geo-distribution and multi-activeness. Your data and applications are always-on. All the outages are transparent to your applications and your data can recover automatically. The operation depends on the network latency and stability. It is recommended to keep the latency within 5ms. Currently, we already have similar use cases. For details, contact info@pingcap.com. 

#### Does TiDB provide any other knowledge resource besides the documentation?

Currently, [TiDB documentation](https://pingcap.com/docs/) is the most important and timely way to get knowledge of TiDB. In addition, we also have some technical communication groups. If you have any needs, contact info@pingcap.com.

#### What are the MySQL variables that TiDB is compatible with?

See [The System Variables](sql/variable.md).

#### Does TiDB support `select for update`?

Yes. But it differs from MySQL in syntax. As a distributed database, TiDB uses the optimistic lock. `select for update` does not lock data when the transaction is started, but checks conflicts when the transaction is committed. If the check reveals conflicts, the committing transaction rolls back.

#### Can the codec of TiDB guarantee that the UTF-8 string is memcomparable? Is there any coding suggestion if our key needs to support UTF-8?

The character sets of TiDB use UTF-8 by default and currently only support UTF-8. The string of TiDB uses the memcomparable format.

### TiDB techniques

#### TiKV for data storage

See [TiDB Internal (I) - Data Storage](https://pingcap.com/blog/2017-07-11-tidbinternal1/).

#### TiDB for data computing

See [TiDB Internal (II) - Computing](https://pingcap.com/blog/2017-07-11-tidbinternal2/).

#### PD for scheduling

See [TiDB Internal (III) - Scheduling](https://pingcap.com/blog/2017-07-20-tidbinternal3/).

## Install, deploy and upgrade

### Prepare

#### Operating system version requirements

| Linux OS Platform        | Version      |
| :-----------------------:| :----------: |
| Red Hat Enterprise Linux | 7.3 or later |
| CentOS                   | 7.3 or later |
| Oracle Enterprise Linux  | 7.3 or later |

##### Why it is recommended to deploy the TiDB cluster on CentOS 7?

As an open source distributed NewSQL database with high performance, TiDB can be deployed in the Intel architecture server and major virtualization environments and runs well. TiDB supports most of the major hardware networks and Linux operating systems. For details, see [Software and Hardware Requirements](op-guide/recommendation.md) for deploying TiDB.

#### Server requirements

You can deploy and run TiDB on the 64-bit generic hardware server platform in the Intel x86-64 architecture. The requirements and recommendations about server hardware configuration for development, testing and production environments are as follows:

##### Development and testing environments

| Component | CPU | Memory | Local Storage  | Network  | Instance Number (Minimum Requirement) |
| :------: | :-----: | :-----: | :----------: | :------: | :----------------: |
| TiDB    | 8 core+   | 16 GB+  | SAS, 200 GB+ | Gigabit network card | 1 (can be deployed on the same machine with PD)      |
| PD      | 8 core+   | 16 GB+  | SAS, 200 GB+ | Gigabit network card | 1 (can be deployed on the same machine with TiDB)       |
| TiKV    | 8 core+   | 32 GB+  | SAS, 200 GB+ | Gigabit network card | 3  |
|         |         |         |              | Total Server Number |  4  |

##### Production environment

| Component | CPU | Memory | Hard Disk Type | Network | Instance Number (Minimum Requirement) |
| :-----: | :------: | :------: | :------: | :------: | :-----: |
|  TiDB  | 16 core+ | 48 GB+ | SAS | 10 Gigabit network card (2 preferred) | 2 |
| PD | 8 core+ | 16 GB+ | SSD | 10 Gigabit network card (2 preferred) | 3 |
| TiKV | 16 core+ | 48 GB+ | SSD | 10 Gigabit network card (2 preferred) | 3 |
| Monitor | 8 core+ | 16 GB+ | SAS | Gigabit network card | 1 |
|     |     |     |      |  Total Server Number   |    9   |

##### What's the purposes of 2 network cards of 10 gigabit?

As a distributed cluster, TiDB has a high demand on time, especially for PD, because PD needs to distribute unique timestamps. If the time in the PD servers is not consistent, it takes longer waiting time when switching the PD server. The bond of two network cards guarantees the stability of data transmission, and 10 gigabit guarantees the transmission speed. Gigabit network cards are prone to meet bottlenecks, therefore it is strongly recommended to use 10 gigabit network cards.

##### Is it feasible if we don't use RAID for SSD?

If the resources are adequate, it is recommended to use RAID for SSD. If the resources are inadequate, it is acceptable not to use RAID for SSD.

### Install and deploy

#### Deploy TiDB using Ansible (recommended)

See [Ansible Deployment](op-guide/ansible-deployment.md).

##### Why the modified `toml` configuration for TiKV/PD does not take effect?

You need to set the `--config` parameter in TiKV/PD to make the `toml` configuration effective. TiKV/PD does not read the configuration by default. Currently, this issue only occurs when deploying using Binary. For TiKV, edit the configuration and restart the service. For PD, the configuration file is only read when PD is started for the first time, after which you can modify the configuration using pd-ctl. For details, see [PD Control User Guide](tools/pd-control.md).

##### Should I deploy the TiDB monitoring framework (Prometheus + Grafana) on a standalone machine or on multiple machines? What is the recommended CPU and memory?

The monitoring machine is recommended to use standalone deployment. It is recommended to use a 8 core CPU with 16 GB+ memory and a 500 GB+ hard disk.

##### Why the monitor cannot display all metrics?

Check the time difference between the machine time of the monitor and the time within the cluster. If it is large, you can correct the time and the monitor will display all the metrics.

##### What is the function of supervise/svc/svstat service?

- supervise: the daemon process, to manage the processes
- svc: to start and stop the service
- svstat: to check the process status

##### Description of inventory.ini variables

| Variable | Description |
| ---- | ------- |
| cluster_name | the name of a cluster, adjustable |
| tidb_version | the version of TiDB, configured by default in TiDB-Ansible branches |
| deployment_method | the method of deployment, binary by default, Docker optional |
| process_supervision | the supervision way of processes, systemd by default, supervise optional |
| timezone | the timezone of the managed node, adjustable, `Asia/Shanghai` by default, used with the `set_timezone` variable |
| set_timezone | to edit the timezone of the managed node, True by default; False means closing |
| enable_elk | currently not supported |
| enable_firewalld | to enable the firewall, closed by default |
| enable_ntpd | to monitor the NTP service of the managed node, True by default; do not close it |
| machine_benchmark | to monitor the disk IOPS of the managed node, True by default; do not close it |
| set_hostname | to edit the hostname of the mananged node based on the IP, False by default |
| enable_binlog | whether to deploy Pump and enable the binlog, False by default, dependent on the Kafka cluster; see the `zookeeper_addrs` variable |
| zookeeper_addrs | the ZooKeeper address of the binlog Kafka cluster |
| enable_slow_query_log | to record the slow query log of TiDB into a single file: ({{ deploy_dir }}/log/tidb_slow_query.log). False by default, to record it into the TiDB log |
| deploy_without_tidb | the Key-Value mode, deploy only PD, TiKV and the monitoring service, not TiDB; set the IP of the tidb_servers host group to null in the `inventory.ini` file |

#### Deploy TiDB offline using Ansible

It is not recommended to deploy TiDB offline using Ansible. If the Control Machine has no access to external network, you can deploy TiDB offline using Ansible. For details, see [Offline Deployment Using Ansible](op-guide/offline-ansible-deployment.md).

### Upgrade

#### How to perform rolling updates using Ansible?

- Apply rolling updates to the TiKV node (only update the TiKV service).
    
    ```
    ansible-playbook rolling_update.yml --tags=tikv
    ```

- Apply rolling updates to all services.

    ```
    ansible-playbook rolling_update.yml
    ```

#### What is the effect of rolling udpates?

When you apply rolling updates to TiDB services, the running application is not affected. You need to configure the minimum cluster topology (TiDB * 2, PD * 3, TiKV * 3). If the Pump/Drainer service is involved in the cluster, it is recommended to stop Drainer before rolling updates. When you update TiDB, Pump is also updated.

#### How to upgrade when I deploy TiDB using Binary?

It is not recommended to deploy TiDB using Binary. The support for upgrading using Binary is not as friendly as using Ansible. It is recommended to deploy TiDB using Ansible.

#### Should I upgrade TiKV or all components generally?

Generally you should upgrade all components, because the whole version is tested together. Upgrade a single component only when an emergent issue occurs and you need to upgrade this component.

#### What causes "Timeout when waiting for search string 200 OK" when starting or upgrading a cluster? How to deal with it?

Possible reasons:

- The process did not start normally.
- The port is occupied.
- The process did not stop normally.
- You use `rolling_update.yml` to upgrade the cluster when the cluster is stopped (operation error).

Solution:

- Log into the node to check the status of the process or port.
- Correct the incorrect operation procedure.

## Manage the cluster

### Daily management

#### What are the common operations?

| Job                               | Playbook                                 |
|:----------------------------------|:-----------------------------------------|
| Start the cluster                 | `ansible-playbook start.yml`             |
| Stop the cluster                  | `ansible-playbook stop.yml`              |
| Destroy the cluster               | `ansible-playbook unsafe_cleanup.yml` (If the deployment directory is a mount point, an error will be reported, but implementation results will remain unaffected) |
| Clean data (for test)             | `ansible-playbook unsafe_cleanup_data.yml` |
| Apply rolling updates                  | `ansible-playbook rolling_update.yml`    |
| Apply rolling updates to TiKV   | `ansible-playbook rolling_update.yml --tags=tikv` |
| Apply rolling updates to components except PD | `ansible-playbook rolling_update.yml --skip-tags=pd` |
| Apply rolling updates to the monitoring components | `ansible-playbook rolling_update_monitor.yml` |

#### How to log into TiDB?

You can log into TiDB like logging into MySQL. For example:

```
mysql -h 127.0.0.1 -uroot -P4000
```

#### How to modify the system variables in TiDB?

Similar to MySQL, TiDB includes static and solid parameters. You can directly modify static parameters using `set global xxx = n`, but the new value of a parameter is only effective within the life cycle in this instance.

#### Where and what are the data directories in TiDB (TiKV)?

TiDB data directories are in `${[data-dir](https://pingcap.com/docs-cn/op-guide/configuration/#data-dir-1)}/data/` by default, which include four directories of backup, db, raft, and snap, used to store backup, data, Raft data, and mirror data respectively.

#### What are the system tables in TiDB?

Similar to MySQL, TiDB includes system tables as well, used to store the information required by the server when it runs.

#### Where are the TiDB/PD/TiKV logs?

By default, TiDB/PD/TiKV outputs standard error in the logs. If a log file is specified by `--log-file` during the startup, the log is output to the specified file and executes rotation daily.

#### How to safely stop TiDB?

If the cluster is deployed using Ansible, you can use the `ansible-playbook stop.yml` command to stop the TiDB cluster. If the cluster is not deployed using Ansible, `kill` all the services directly. The components of TiDB will do `graceful shutdown`.

#### Can `kill` be executed in TiDB?

- You can `kill` DML statements. First use `show processlist` to find the ID corresponding with the session, and then run `kill id`.
- You can `kill` DDL statements. First use `admin show ddl jobs` to find the ID of the DDL job you need to kill, and then run `admin cancel ddl jobs 'job_id' [, 'job_id'] ...`. For more details, see the [`ADMIN` statement](sql/admin.md#admin-statement).

#### Does TiDB support session timeout?

Currently, TiDB does not support session timeout in the database level. If you want to implement session timeout, use the session ID started by side records in the absence of LB (Load Balancing), and customize the session timeout on the application. After timeout, kill SQL using `kill id` on the node that starts the query. It is currently recommended to implement session timeout using applications. When the timeout time is reached, the application layer reports an exception and continues to execute subsequent program segments.

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

#### Is there a graphical deployment tool for TiDB?

Currently no.

#### How to scale TiDB horizontally?

As your business grows, your database might face the following three bottlenecks:

- Lack of storage resources which means that the disk space is not enough.

- Lack of computing resources such as high CPU occupancy.

- Not enough write and read capacity.

You can scale TiDB as your business grows.

- If the disk space is not enough, you can increase the capacity simply by adding more TiKV nodes. When the new node is started, PD will migrate the data from other nodes to the new node automatically.

- If the computing resources are not enough, check the CPU consumption situation first before adding more TiDB nodes or TiKV nodes. When a TiDB node is added, you can configure it in the Load Balancer.

- If the capacity is not enough, you can add both TiDB nodes and TiKV nodes.

#### Why does TiDB use gRPC instead of Thrift? Is it because Google uses it?

Not really. We need some good features of gRPC, such as flow control, encryption and streaming.

#### What does the 92 indicate in `like(bindo.customers.name, jason%, 92)`?

The 92 indicates the escape character, which is ASCII 92 by default.

### Manage the PD server

#### The `TiKV cluster is not bootstrapped` message is displayed when I access PD.

Most of the APIs of PD are available only when the TiKV cluster is initialized. This message is displayed if PD is accessed when PD is started while TiKV is not started when a new cluster is deployed. If this message is displayed, start the TiKV cluster. When TiKV is initialized, PD is accessible.

#### The `etcd cluster ID mismatch` message is displayed when starting PD.

This is because the `--initial-cluster` in the PD startup parameter contains a member that doesn't belong to this cluster. To solve this problem, check the corresponding cluster of each member, remove the wrong member, and then restart PD.

#### What's the maximum tolerance for time synchronization error of PD?

Theoretically, the smaller of the tolerance, the better. During leader changes, if the clock goes back, the process won't proceed until it catches up with the previous leader. PD can tolerate any synchronization error, but a larger error value means a longer period of service stop during the leader change.

#### How does the client connection find PD?

The client connection can only access the cluster through TiDB. TiDB connects PD and TiKV. PD and TiKV are transparent to the client. When TiDB connects to any PD, the PD tells TiDB who is the current leader. If this PD is not the leader, TiDB reconnects to the leader PD.

#### What is the difference between the `leader-schedule-limit` and `region-schedule-limit` scheduling parameters in PD?

- The `leader-schedule-limit` scheduling parameter is used to balance the Leader number of different TiKV servers, affecting the load of query processing.
- The `region-schedule-limit` scheduling parameter is used to balance the replica number of different TiKV servers, affecting the data amount of different nodes.

#### Is the number of replicas in each region configurable? If yes, how to configure it?

Yes. Currently, you can only update the global number of replicas. When started for the first time, PD reads the configuration file (conf/pd.yml) and uses the max-replicas configuration in it. If you want to update the number later, use the pd-ctl configuration command `config set max-replicas $num` and view the enabled configuration using `config show all`. The updating does not affect the applications and is configured in the background.

Make sure that the total number of TiKV instances is always greater than or equal to the number of replicas you set. For example, 3 replicas need 3 TiKV instances at least. Additional storage requirements need to be estimated before increasing the number of replicas. For more information about pd-ctl, see [PD Control User Guide](tools/pd-control.md).

#### How to check the health status of the whole cluster when lacking command line cluster management tools?

You can determine the general status of the cluster using the pd-ctl tool. For detailed cluster status, you need to use the monitor to determine.

#### How to delete the monitoring data of a cluster node that is offline?

The offline node usually indicates the TiKV node. You can determine whether the offline process is finished by the pd-ctl or the monitor. After the node is offline, perform the following steps:

1. Manually stop the relevant services on the offline node.
2. Delete the `node_exporter` data of the corresponding node from the Prometheus configuration file.
3. Delete the data of the corresponding node from Ansible `inventory.ini`.

### Manage the TiDB server

#### How to set the `lease` parameter in TiDB?

The lease parameter (`--lease=60`) is set from the command line when starting a TiDB server. The value of the lease parameter impacts the Database Schema Changes (DDL) speed of the current session. In the testing environments, you can set the value to 1s for to speed up the testing cycle. But in the production environments, it is recommended to set the value to minutes (for example, 60) to ensure the DDL safety.

#### Why it is very slow to run DDL statements sometimes?

Possible reasons:

- If you run multiple DDL statements together, the last few DDL statements might run slowly. This is because the DDL statements are executed serially in the TiDB cluster.
- After you start the cluster successfully, the first DDL operation may take a longer time to run, usually around 30s. This is because the TiDB cluster is electing the leader that processes DDL statements.
- In rolling updates or shutdown updates, the processing time of DDL statements in the first ten minutes after starting TiDB is affected by the server stop sequence (stopping PD -> TiDB), and the condition where TiDB does not clean up the registration data in time because TiDB is stopped using the `kill -9` command. When you run DDL statements during this period, for the state change of each DDL, you need to wait for 2 * lease (lease = 10s).
- If a communication issue occurs between a TiDB server and a PD server in the cluster, the TiDB server cannot get or update the version information from the PD server in time. In this case, you need to wait for 2 * lease for the state processing of each DDL.

#### Can I use S3 as the backend storage engine in TiDB?

No. Currently, TiDB only supports the distributed storage engine and the Goleveldb/Rocksdb/Boltdb engine.

#### Can the `Information_schema` support more real information?

The tables in `Information_schema` exist mainly for compatibility with MySQL, and some third-party software queries information in the tables. Currently, most of those tables are null. More parameter information is to be involved in the tables as TiDB updates later.

For the `Information_schema` that TiDB currently supports, see [The TiDB System Database](sql/system-database.md).

#### What's the explanation of the TiDB Backoff type scenario?

In the communication process between the TiDB server and the TiKV server, the `Server is busy` or `backoff.maxsleep 20000ms` log message is displayed when processing a large volume of data. This is because the system is busy while the TiKV server processes data. At this time, usually you can view that the TiKV host resources usage rate is high. If this occurs, you can increase the server capacity according to the resources usage.

#### What's the maximum number of concurrent connections that TiDB supports?

The current TiDB version has no limit for the maximum number of concurrent connections. If too large concurrency leads to an increase of response time, you can increase the capacity by adding TiDB nodes.

### Manage the TiKV server

#### What is the recommended number of replicas in the TiKV cluster? Is it better to keep the minimum number for high availability?

Use 3 replicas for test. If you increase the number of replicas, the performance declines but it is more secure. Whether to configure more replicas depends on the specific business needs.

#### The `cluster ID mismatch` message is displayed when starting TiKV.

This is because the cluster ID stored in local TiKV is different from the cluster ID specified by PD. When a new PD cluster is deployed, PD generates random cluster IDs. TiKV gets the cluster ID from PD and stores the cluster ID locally when it is initialized. The next time when TiKV is started, it checks the local cluster ID with the cluster ID in PD. If the cluster IDs don't match, the `cluster ID mismatch` message is displayed and TiKV exits.

If you previously deploy a PD cluster, but then you remove the PD data and deploy a new PD cluster, this error occurs because TiKV uses the old data to connect to the new PD cluster.

#### The `duplicated store address` message is displayed when starting TiKV.

This is because the address in the startup parameter has been registered in the PD cluster by other TiKVs. This error occurs when there is no data folder under the directory that TiKV `--store` specifies, but you use the previous parameter to restart the TiKV.

To solve this problem, use the [store delete](https://github.com/pingcap/pd/tree/master/pdctl#store-delete-) function to delete the previous store and then restart TiKV.

#### TiKV master and slave use the same compression algorithm, why the results are different?

Currently, some files of TiKV master have a higher compression rate, which depends on the underlying data distribution and RocksDB implementation. It is normal that the data size fluctuates occasionally. The underlying storage engine adjusts data as needed.

#### What are the features of TiKV block cache?

TiKV implements the Column Family (CF) feature of RocksDB. By default, the KV data is eventually stored in the 3 CFs (default, write and lock) within RocksDB.

- The default CF stores real data and the corresponding parameter is in [rocksdb.defaultcf]. The write CF stores the data version information (MVCC) and index-related data, and the corresponding parameter is in `[rocksdb.writecf]`. The lock CF stores the lock information and the system uses the default parameter.
- The Raft RocksDB instance stores Raft logs. The default CF mainly stores Raft logs and the corresponding parameter is in `[raftdb.defaultcf]`.
- Each CF has an individual block-cache to cache data blocks and improve RocksDB read speed. The size of block-cache is controlled by the `block-cache-size` parameter. A larger value of the parameter means more hot data can be cached and is more favorable to read operation. At the same time, it consumes more system memory.
- Each CF has an individual write-buffer and the size is controlled by the `write-buffer-size` parameter.

#### Why it occurs that "TiKV channel full"?

- The Raftstore thread is too slow. You can view the CPU usage status of Raftstore.
- TiKV is too busy (read, write, disk I/O, etc.) and cannot manage to handle it.

#### Why does TiKV frequently switch Region leader?

- Network problem leads to the failure of communication between nodes. You can view the monitoring information of Report failures.
- The original main leader node fails, and cannot send information to the follower in time.
- The Raftstore thread fails.

#### If the leader node is down, will the service be affected? How long?

TiDB uses Raft to replicate data among multiple replicas and guarantees the strong consistency of data. If one replica goes wrong, the other replicas can guarantee data safety. The default number of replicas in each Region is 3. Based on the Raft protocol, a leader is elected in each Region, and if a single Region leader fails, a new Region leader is soon elected after a maximum of 2 * lease time (lease time is 10 seconds).

#### What are the TiKV scenarios that take up high I/O, memory, CPU, and exceed the parameter configuration?

Writing or reading a large volume of data in TiKV takes up high I/O, memory and CPU. Executing very complex queries costs a lot of memory and CPU resources, such as the scenario that generates large intermediate result sets.

#### Does TiKV support SAS/SATA disks or mixed deployment of SSD/SAS disks?

No. For OLTP scenarios, TiDB requires high I/O disks for data access and operation. As a distributed database with strong consistency, TiDB has some write amplification such as replica replication and bottom layer storage compaction. Therefore, it is recommended to use NVMe SSD as the storage disks in TiDB best practices. Besides, the mixed deployment of TiKV and PD is not supported.

#### Is the Range of the Key data table divided before data access?

No. It differs from the table splitting rules of MySQL. In TiKV, the table Range is dynamically split based on the size of Region.

#### How does Region split?

Region is not divided in advance, but it follows a Region split mechanism. When the Region size exceeds the value of the `region_split_size` parameter, split is triggered. After the split, the information is reported to PD.

#### Does TiKV have the `innodb_flush_log_trx_commit` parameter like MySQL, to guarantee the security of data?

Yes. Currently, the standalone storage engine uses two RocksDB instances. One instance is used to store the raft-log. When the `sync-log` parameter in TiKV is set to true, each commit is mandatorily flushed to the raft-log. If a crash occurs, you can restore the KV data using the raft-log.

#### What is the recommended server configuration for WAL storage, such as SSD, RAID level, cache strategy of RAID card, NUMA configuration, file system, I/O scheduling strategy of the operating system?

WAL belongs to ordered writing, and currently, we do not apply a unique configuration to it. Recommended configuration is as follows:

- SSD
- RAID 10 preferred
- Cache strategy of RAID card and I/O scheduling strategy of the operating system: currently no specific best practices; you can use the default configuration in Linux 7 or later
- NUMA: no specific suggestion; for memory allocation strategy, you can use `interleave = all`
- File system: ext4

#### How is the write performance in the most strict data available mode of `sync-log = true`?

Generally, enabling `sync-log` reduces about 30% of the performance. For the test about `sync-log = false`, see [Performance test result for TiDB using Sysbench](benchmark/sysbench.md).

#### Can the Raft + multiple replicas in the upper layer implement complete data safety? Is it required to apply the most strict mode to standalone storage?

Raft uses strong consistency, and only when the data has been written into more than 50% of the nodes, the application returns ACK (two out of three nodes). In this case, data consistency is guaranteed. However, theoretically, two nodes might crash. Therefore, for scenarios that have a strict requirement on data safety, such as scenarios in financial industry, you need to enable the `sync-log`.

#### In data writing using the Raft protocol, multiple network roundtrips occur. What is the actual write delay?

Theoretically, TiDB has 4 more network roundtrips than standalone databases.

#### Does TiDB have a InnoDB memcached plugin like MySQL which can directly use the KV interface and does not need the independent cache?

TiKV supports calling the interface separately. Theoretically, you can take an instance as the cache. Because TiDB is a distributed relational database, we do not support TiKV separately.

#### What is the Coprocessor component used for?

- Reduce the data transmission between TiDB and TiKV
- Make full use of the distributed computing resources of TiKV to execute computing pushdown

### TiDB test

#### What is the performance test result for TiDB using Sysbench?

At the beginning, many users tend to do a benchmark test or a comparison test between TiDB and MySQL. We have also done a similar official test and find the test result is consistent at large, although the test data has some bias. Because the architecture of TiDB differs greatly from MySQL, it is hard to find a benchmark point. The suggestions are as follows:

- Do not spend too much time on the benchmark test. Pay more attention to the difference of scenarios using TiDB.
- See the official test. For the Sysbench test and comparison test between TiDB and MySQL, see [Performance test result for TiDB using Sysbench](benchmark/sysbench.md).

#### What's the relationship between the TiDB cluster capacity (QPS) and the number of nodes? How does TiDB compare to MySQL?

- Within 10 nodes, the relationship between TiDB write capacity (Insert TPS) and the number of nodes is roughly 40% linear increase. Because MySQL uses single-node write, its write capacity cannot be scaled.
- In MySQL, the read capacity can be increased by adding slave, but the write capacity cannot be increased except using sharding, which has many problems.
- In TiDB, both the read and write capacity can be easily increased by adding more nodes.

#### The performance test of MySQL and TiDB by our DBA shows that the performance of a standalone TiDB is not as good as MySQL.

TiDB is designed for scenarios where sharding is used because the capacity of a MySQL standalone is limited, and where strong consistency and complete distributed transactions are required. One of the advantages of TiDB is pushing down computing to the storage nodes to execute concurrent computing.

TiDB is not suitable for tables of small size (such as below ten million level), because its strength in concurrency cannot be showed with small size data and limited Region. A typical example is the counter table, in which records of a few lines are updated high frequently. In TiDB, these lines become several Key-Value pairs in the storage engine, and then settle into a Region located on a single node. The overhead of background replication to guarantee strong consistency and operations from TiDB to TiKV leads to a poorer performance than a MySQL standalone.

### Backup and restore

#### How to back up data in TiDB?

Currently, the major way of backing up data in TiDB is using `mydumper`. For details, see [mydumper repository](https://github.com/maxbube/mydumper). Although the official MySQL tool `mysqldump` is also supported in TiDB to back up and restore data, its performance is poorer than `mydumper`/`loader` and it needs much more time to back up and restore large volumes of data. Therefore, it is not recommended to use `mysqldump`. 

Keep the size of the data file exported from `mydumper` as small as possible. It is recommended to keep the size within 64M. You can set value of the `-F` parameter to 64.

You can edit the `t` parameter of `loader` based on the number of TiKV instances and load status. For example, in scenarios of three TiKV instances, you can set its value to `3 * (1 ～ n)`. When the TiKV load is very high and `backoffer.maxSleep 15000ms is exceeded` displays a lot in `loader` and TiDB logs, you can adjust the parameter to a smaller value. When the TiKV load is not very high, you can adjust the parameter to a larger value accordingly.

## Migrate the data and traffic

### Full data export and import

#### Mydumper

See the [mydumper repository](https://github.com/maxbube/mydumper).

#### Loader

See [Loader Instructions](tools/loader.md).

#### How to migrate an application running on MySQL to TiDB?

Because TiDB supports most MySQL syntax, generally you can migrate your applications to TiDB without changing a single line of code in most cases. You can use [checker](https://github.com/pingcap/tidb-tools/tree/master/checker) to check whether the Schema in MySQL is compatible with TiDB.

#### If I accidentally import the MySQL user table into TiDB, or forget the password and cannot log in, how to deal with it?

Restart the TiDB service, add the `-skip-grant-table=true` parameter in the configuration file. Log into the cluster without password and recreate the user, or recreate the `mysql.user` table using the following statement:

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

#### How to export the data in TiDB?

Currently, TiDB does not support `select into outfile`. You can use the following methods to export the data in TiDB:

- See [MySQL uses mysqldump to export part of the table data](http://blog.csdn.net/xin_yu_xin/article/details/7574662) in Chinese and export data using mysqldump and the WHERE condition.
- Use the MySQL client to export the results of `select` to a file.

#### How to migrate from DB2 or Oracle to TiDB?

To migrate all the data or migrate incrementally from DB2 or Oracle to TiDB, see the following solution:

- Use the official migration tool of Oracle, such as OGG, Gateway, CDC (Change Data Capture).
- Develop a program for importing and exporting data.
- Export Spool as text file, and import data using Load infile.
- Use a third-party data migration tool.

Currently, it is recommended to use OGG.

### Migrate the data incrementally

#### Syncer 

##### Syncer user guide

See [Syncer User Guide](docs/tools/syncer.md).

##### How to configure to monitor Syncer status?

Download and import [Syncer Json](https://github.com/pingcap/tidb-ansible/blob/master/scripts/syncer.json) to Grafana. Edit the Prometheus configuration file and add the following content:

```
- job_name: ‘syncer_ops’ // task name
    static_configs:
      - targets: [’10.10.1.1:10096’] // Syncer monitoring address and port, informing Prometheus to pull the data of Syncer
```

Restart Prometheus.

##### Is there a current solution to replicating data from TiDB to other databases like HBase and Elasticsearch?

No. Currently, the data replication depends on the application itself.

#### Wormhole

Wormhole is a data replication service, which enables the user to easily replicate all the data or replicate incrementally using Web console. It supports multiple types of data migration, such as from MySQL to TiDB, and from MongoDB to TiDB.

### Migrate the traffic

#### How to migrate the traffic quickly?

It is recommended to build a multi-source MySQL, MongoDB -> TiDB real-time replication environment using Syncer or Wormhole. You can migrate the read and write traffic in batches by editing the network configuration as needed. Deploy a stable network LB (HAproxy, LVS, F5, DNS, etc.) on the upper layer, in order to implement seamless migration by directly editing the network configuration.

#### Is there a limit for the total write and read capacity in TiDB?

The total read capacity has no limit. You can increase the read capacity by adding more TiDB servers. Generally the write capacity has no limit as well. You can increase the write capacity by adding more TiKV nodes.

#### The error message `transaction too large` is displayed.

As distributed transactions need to conduct two-phase commit and the bottom layer performs Raft replication, if a transaction is very large, the commit process would be quite slow and the following Raft replication flow is thus struck. To avoid this problem, we limit the transaction size:

- Each Key-Value entry is no more than 6MB
- The total number of Key-Value entry is no more than 300,000 rows
- The total size of Key-Value entry is no more than 100MB

There are [similar limits](https://cloud.google.com/spanner/docs/limits) on Google Cloud Spanner.

#### How to import data in batches?

1. When you import data, insert in batches and keep the number of rows within 10,000 for each batch.

2. As for `insert` and `select`, you can open the hidden parameter `set @@session.tidb_batch_insert=1;`, and `insert` will execute large transactions in batches. In this way, you can avoid the timeout caused by large transactions, but this may lead to the loss of atomicity. An error in the process of execution leads to partly inserted transaction. Therefore, use this parameter only when necessary, and use it in session to avoid affecting other statements. When the transaction is finished, use `set @@session.tidb_batch_insert=0` to close it.

3. As for `delete` and `update`, you can use `limit` plus circulation to operate.

#### Does TiDB release space immediately after deleting data?

`DELETE`, `TRUNCATE` and `DROP` do not release space immediately. For `TRUNCATE` and `DROP` operations, TiDB deletes the data and releases the space after reaching the GC (garbage collection) time (10 minutes by default). For the `DELETE` operation, TiDB deletes the data and does not release the space based on the GC mechanism, but reuses the space when subsequent data is committed to RocksDB and compacted.

#### Can I execute DDL operations on the target table when loading data?

No. None of the DDL operations can be executed on the target table when you load data, otherwise the data fails to be loaded.

#### Does TiDB support the `replace into` syntax?

Yes. But the `load data` does not support the `replace into` syntax.

#### How long does it take to reclaim disk space after deleting data?

None of the `Delete`, `Truncate` and `Drop` operations releases data immediately. For the `Truncate` and `Drop` operations, after the TiDB GC (Garbage Collection) time (10 minutes by default), the data is deleted and the space is released. For the `Delete` operation, the data is deleted but the space is not released according to TiDB GC. When data is written into RocksDB and executes `Compact`, the space is reused.

#### Why does the query speed getting slow after deleting data?

Deleting a large amount of data leaves a lot of useless keys, affecting the query efficiency. Currently the Region Merge feature is in development, which is expected to solve this problem. For details, see the [deleting data section in TiDB Best Practices](https://pingcap.com/blog/2017-07-24-tidbbestpractice/#write).

#### What is the most efficient way of deleting data?

When deleting a large amount of data, it is recommended to use `Delete * from t where xx limit 5000;`. It deletes through the loop and uses `Affected Rows == 0` as a condition to end the loop, so as not to exceed the limit of transaction size. With the prerequisite of meeting business filtering logic, it is recommended to add a strong filter index column or directly use the primary key to select the range, such as `id >= 5000*n+m and id < 5000*(n+1)+m`.

If the amount of data that needs to be deleted at a time is very large, this loop method will get slower and slower because each deletion traverses backward. After deleting the previous data, lots of deleted flags remain for a short period (then all will be processed by Garbage Collection) and influence the following Delete statement. If possible, it is recommended to refine the Where condition. See [details in TiDB Best Practices](https://pingcap.com/blog/2017-07-24-tidbbestpractice/#write).

#### How to improve the data loading speed in TiDB?

- Currently Lightning is in development for distributed data import. It should be noted that the data import process does not perform a complete transaction process for performance reasons. Therefore, the ACID constraint of the data being imported during the import process cannot be guaranteed. The ACID constraint of the imported data can only be guaranteed after the entire import process ends. Therefore, the applicable scenarios mainly include importing new data (such as a new table or a new index) or the full backup and restoring (truncate the original table and then import data).
- Data loading in TiDB is related to the status of disks and the whole cluster. When loading data, pay attention to metrics like the disk usage rate of the host, TiClient Error, Backoff, Thread CPU and so on. You can analyze the bottlenecks using these metrics.

## SQL optimization

### TiDB execution plan description

See [Understand the Query Execution Plan](sql/understanding-the-query-execution-plan.md).

### Statistics collection

See [Introduction to Statistics](sql/statistics.md).

#### How to optimize `select count(1)`?

The `count(1)` statement counts the total number of rows in a table. Improving the degree of concurrency can significantly improve the speed. To modify the concurrency, refer to the [document](sql/tidb-specific.md#tidb_distsql_scan_concurrency). But it also depends on the CPU and I/O resources. TiDB accesses TiKV in every query. When the amount of data is small, all MySQL is in memory, and TiDB needs to conduct a network access.

Recommendations:

1. Improve the hardware configuration. See [Software and Hardware Requirements](op-guide/recommendation.md).
2. Improve the concurrency. The default value is 10. You can improve it to 50 and have a try. But usually the improvement is 2-4 times of the default value.
3. Test the `count` in the case of large amount of data.
4. Optimize the TiKV configuration. See [Performance Tuning for TiKV](op-guide/tune-TiKV.md).

#### How to view the progress of adding an index?

Use `admin show ddl` to view the current job of adding an index.

#### How to view the DDL job?

- `admin show ddl`: to view the running DDL job
- `admin show ddl jobs`: to view all the results in the current DDL job queue (including tasks that are running and waiting to run) and the last ten results in the completed DDL job queue

#### Does TiDB support CBO (Cost-Based Optimization)? If yes, to what extent?

Yes. TiDB uses the cost-based optimizer. The cost model and statistics are constantly optimized. Besides, TiDB also supports correlation algorithms like hash join and soft merge.

## Database optimization

### TiDB

#### Edit TiDB options

See [The TiDB Command Options](sql/server-command-option.md).

### TiKV

#### Tune TiKV performance

See [Tune TiKV Performance](op-guide/tune-tikv.md).

## Monitor

### Prometheus monitoring framework

See [Overview of the Monitoring Framework](op-guide/monitor-overview.md).

### Key metrics of monitoring

See [Key Metrics](op-guide/dashboard-overview-info.md).

#### Is there a better way of monitoring the key metrics?

The monitoring system of TiDB consists of Prometheus and Grafana. From the dashboard in Grafana, you can monitor various running metrics of TiDB which include the monitoring metrics of system resources, of client connection and SQL operation, of internal communication and Region scheduling. With these metrics, the database administrator can better understand the system running status, running bottlenecks and so on. In the practice of monitoring these metrics, we list the key metrics of each TiDB component. Generally you only need to pay attention to these common metrics. For details, see [Key Metrics](op-guide/dashboard-overview-info.md).

#### The Prometheus monitoring data is deleted each month by default. Could I set it to two months or delete the monitoring data manually?

Yes. Find the startup script on the machine where Prometheus is started, edit the startup parameter and restart Prometheus.

## Troubleshoot

### TiDB custom error messages

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

#### ERROR 9006 (HY000): GC Too Early

The interval of `GC Life Time` is too short. The data that should have been read by long transactions might be deleted. You can add the `GC Life Time`.

### MySQL native error messages

#### ERROR 2013 (HY000): Lost connection to MySQL server during query

- Check whether panic is in the log.
- Check whether OOM exists in dmesg using `dmesg -T | grep -i oom`.
- A long time of no access might also lead to this error. It is usually caused by TCP timeout. If TCP is not used for a long time, the operating system kills it.

#### ERROR 1105 (HY000): other error: unknown error Wire Error(InvalidEnumValue(4004))

This error usually occurs when the version of TiDB does not match with the version of TiKV. To avoid version mismatch, upgrade all components when you upgrade the version.
