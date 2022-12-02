---
title: TiDB Cluster Management FAQs
summary: Learn about the FAQs related to TiDB cluster management.
---

# TiDB Cluster Management FAQs

This document summarizes the FAQs related to TiDB cluster management.

## Daily management

This section describes common problems you might encounter during daily cluster management, their causes, and solutions.

### How to log into TiDB?

You can log into TiDB like logging into MySQL. For example:

```bash
mysql -h 127.0.0.1 -uroot -P4000
```

### How to modify the system variables in TiDB?

Similar to MySQL, TiDB includes static and solid parameters. You can directly modify static parameters using `SET GLOBAL xxx = n`, but the new value of a parameter is only effective within the life cycle in this instance.

### Where and what are the data directories in TiDB (TiKV)?

TiKV data is located in the [`--data-dir`](/command-line-flags-for-tikv-configuration.md#--data-dir), which include four directories of backup, db, raft, and snap, used to store backup, data, Raft data, and mirror data respectively.

### What are the system tables in TiDB?

Similar to MySQL, TiDB includes system tables as well, used to store the information required by the server when it runs. See [TiDB system table](/mysql-schema.md).

### Where are the TiDB/PD/TiKV logs?

By default, TiDB/PD/TiKV outputs standard error in the logs. If a log file is specified by `--log-file` during the startup, the log is output to the specified file and executes rotation daily.

### How to safely stop TiDB?

- If a load balancer is running (recommended): Stop the load balancer and execute the SQL statement `SHUTDOWN`. Then TiDB waits for a period as specified by [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50) until all sessions are terminated. Then TiDB stops running.

- If no load balancer is running: Execute the `SHUTDOWN` statement. Then TiDB components are gracefully stopped.

### Can `kill` be executed in TiDB?

- Kill DML statements:

    First use `information_schema.cluster_processlist` to find TiDB instance address and session ID, and then run the kill command.

    TiDB v6.1.0 introduces the Global Kill feature (controlled by the `enable-global-kill` configuration, which is enabled by default). If Global Kill is enabled, just execute `kill session_id`.

    If the TiDB version is earlier than v6.1.0, or the Global Kill feature is not enabled, `kill session_id` does not take effect by default. To terminate a DML statement, you should connect the client directly to the TiDB instance that is executing the DML statement and then execute the `kill tidb session_id` statement. If the client connects to another TiDB instance or there is a proxy between the client and the TiDB cluster, the `kill tidb session_id` statement might be routed to another TiDB instance, which might incorrectly terminate another session. For details, see [`KILL`](/sql-statements/sql-statement-kill.md).

- Kill DDL statements: First use `admin show ddl jobs` to find the ID of the DDL job you need to terminate, and then run `admin cancel ddl jobs 'job_id' [, 'job_id'] ...`. For more details, see the [`ADMIN` statement](/sql-statements/sql-statement-admin.md).

### Does TiDB support session timeout?

TiDB currently supports two timeouts, [`wait_timeout`](/system-variables.md#wait_timeout) and [`interactive_timeout`](/system-variables.md#interactive_timeout).

### What is the TiDB version management strategy?

For details about TiDB version management, see [TiDB versioning](/releases/versioning.md).

### How about the operating cost of deploying and maintaining a TiDB cluster?

TiDB provides a few features and [tools](/ecosystem-tool-user-guide.md), with which you can manage the clusters easily at a low cost:

- For maintenance operations, [TiUP](/tiup/tiup-documentation-guide.md) works as the package manager, which simplifies the deployment, scaling, upgrade, and other maintenance tasks.
- For monitoring, the [TiDB monitoring framework](/tidb-monitoring-framework.md) uses [Prometheus](https://prometheus.io/) to store the monitoring and performance metrics, and uses [Grafana](https://grafana.com/grafana/) to visualize these metrics. Dozens of built-in panels are available with hundreds of metrics.
- For troubleshooting, the [TiDB Troubleshooting Map](/tidb-troubleshooting-map.md) summarizes common issues of the TiDB server and other components. You can use this map to diagnose and resolve issues when you encounter related problems.

### What's the difference between various TiDB master versions?

The TiDB community is highly active. The engineers have been keeping optimizing features and fixing bugs. Therefore, the TiDB version is updated quite fast. If you want to keep informed of the latest version, see [TiDB Release Timeline](/releases/release-timeline.md).

It is recommeneded to deploy TiDB [using TiUP](/production-deployment-using-tiup.md) or [using TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable). TiDB has a unified management of the version number. You can view the version number using one of the following methods:

- `select tidb_version()`
- `tidb-server -V`

### Is there a graphical deployment tool for TiDB?

Currently no.

### How to scale out a TiDB cluster?

You can scale out your TiDB cluster without interrupting the online services.

- If your cluster is deployed using [TiUP](/production-deployment-using-tiup.md), refer to [Scale a TiDB Cluster Using TiUP](/scale-tidb-using-tiup.md).
- If your cluster is deployed using [TiDB Operator](/tidb-operator-overview.md) on Kubernetes, refer to [Manually Scale TiDB on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/scale-a-tidb-cluster).

### How to scale TiDB horizontally?

As your business grows, your database might face the following three bottlenecks:

- Lack of storage resources which means that the disk space is not enough.

- Lack of computing resources such as high CPU occupancy.

- Not enough write and read capacity.

You can scale TiDB as your business grows.

- If the disk space is not enough, you can increase the capacity simply by adding more TiKV nodes. When the new node is started, PD will migrate the data from other nodes to the new node automatically.

- If the computing resources are not enough, check the CPU consumption situation first before adding more TiDB nodes or TiKV nodes. When a TiDB node is added, you can configure it in the Load Balancer.

- If the capacity is not enough, you can add both TiDB nodes and TiKV nodes.

### If Percolator uses distributed locks and the crash client keeps the lock, will the lock not be released?

For more details, see [Percolator and TiDB Transaction Algorithm](https://pingcap.com/blog-cn/percolator-and-txn/) in Chinese.

### Why does TiDB use gRPC instead of Thrift? Is it because Google uses it?

Not really. We need some good features of gRPC, such as flow control, encryption and streaming.

### What does the 92 indicate in `like(bindo.customers.name, jason%, 92)`?

The 92 indicates the escape character, which is ASCII 92 by default.

### Why does the data length shown by `information_schema.tables.data_length` differ from the store size on the TiKV monitoring panel?

Two reasons:

- The two results are calculated in different ways. `information_schema.tables.data_length` is an estimated value by calculating the averaged length of each row, while the store size on the TiKV monitoring panel sums up the length of the data files (the SST files of RocksDB) in a single TiKV instance.
- `information_schema.tables.data_length` is a logical value, while the store size is a physical value. The redundant data generated by multiple versions of the transaction is not included in the logical value, while the redundant data is compressed by TiKV in the physical value.

### Why does the transaction not use the Async Commit or the one-phase commit feature?

In the following situations, even you have enabled the [Async Commit](/system-variables.md#tidb_enable_async_commit-new-in-v50) feature and the [one-phase commit](/system-variables.md#tidb_enable_1pc-new-in-v50) feature using the system variables, TiDB will not use these features:

- If you have enabled TiDB Binlog, restricted by the implementation of TiDB Binlog, TiDB does not use the Async Commit or one-phase commit feature.
- TiDB uses the Async Commit or one-phase commit features only when no more than 256 key-value pairs are written in the transaction and the total size of keys is no more than 4 KB. This is because, for transactions with a large amount of data to write, using Async Commit cannot greatly improve the performance.

## PD management

This section describes common problems you may encounter during PD management, their causes, and solutions.

### The `TiKV cluster is not bootstrapped` message is displayed when I access PD

Most of the APIs of PD are available only when the TiKV cluster is initialized. This message is displayed if PD is accessed when PD is started while TiKV is not started when a new cluster is deployed. If this message is displayed, start the TiKV cluster. When TiKV is initialized, PD is accessible.

### The `etcd cluster ID mismatch` message is displayed when starting PD

This is because the `--initial-cluster` in the PD startup parameter contains a member that doesn't belong to this cluster. To solve this problem, check the corresponding cluster of each member, remove the wrong member, and then restart PD.

### What's the maximum tolerance for time synchronization error of PD?

PD can tolerate any synchronization error, but a larger error value means a larger gap between the timestamp allocated by the PD and the physical time, which will affect functions such as read of historical versions.

### How does the client connection find PD?

The client connection can only access the cluster through TiDB. TiDB connects PD and TiKV. PD and TiKV are transparent to the client. When TiDB connects to any PD, the PD tells TiDB who is the current leader. If this PD is not the leader, TiDB reconnects to the leader PD.

### What is the relationship between each status (Up, Disconnect, Offline, Down, Tombstone) of a TiKV store?

For the relationship between each status, refer to [Relationship between each status of a TiKV store](/tidb-scheduling.md#information-collection).

You can use PD Control to check the status information of a TiKV store.

### What is the difference between the `leader-schedule-limit` and `region-schedule-limit` scheduling parameters in PD?

- The `leader-schedule-limit` scheduling parameter is used to balance the Leader number of different TiKV servers, affecting the load of query processing.
- The `region-schedule-limit` scheduling parameter is used to balance the replica number of different TiKV servers, affecting the data amount of different nodes.

### Is the number of replicas in each region configurable? If yes, how to configure it?

Yes. Currently, you can only update the global number of replicas. When started for the first time, PD reads the configuration file (conf/pd.yml) and uses the max-replicas configuration in it. If you want to update the number later, use the pd-ctl configuration command `config set max-replicas $num` and view the enabled configuration using `config show all`. The updating does not affect the applications and is configured in the background.

Make sure that the total number of TiKV instances is always greater than or equal to the number of replicas you set. For example, 3 replicas need 3 TiKV instances at least. Additional storage requirements need to be estimated before increasing the number of replicas. For more information about pd-ctl, see [PD Control User Guide](/pd-control.md).

### How to check the health status of the whole cluster when lacking command line cluster management tools?

You can determine the general status of the cluster using the pd-ctl tool. For detailed cluster status, you need to use the monitor to determine.

### How to delete the monitoring data of a cluster node that is offline?

The offline node usually indicates the TiKV node. You can determine whether the offline process is finished by the pd-ctl or the monitor. After the node is offline, perform the following steps:

1. Manually stop the relevant services on the offline node.
2. Delete the `node_exporter` data of the corresponding node from the Prometheus configuration file.

## TiDB server management

This section describes common problems you may encounter during TiDB server management, their causes, and solutions.

### How to set the `lease` parameter in TiDB?

The lease parameter (`--lease=60`) is set from the command line when starting a TiDB server. The value of the lease parameter impacts the Database Schema Changes (DDL) speed of the current session. In the testing environments, you can set the value to 1s for to speed up the testing cycle. But in the production environments, it is recommended to set the value to minutes (for example, 60) to ensure the DDL safety.

### What is the processing time of a DDL operation?

The processing time is different for different scenarios. Generally, you can consider the following three scenarios:

1. The `Add Index` operation with a relatively small number of rows in the corresponding data table: about 3s
2. The `Add Index` operation with a relatively large number of rows in the corresponding data table: the processing time depends on the specific number of rows and the QPS at that time (the `Add Index` operation has a lower priority than ordinary SQL operations)
3. Other DDL operations: about 1s

If the TiDB server instance that receives the DDL request is the same TiDB server instance that the DDL owner is in, the first and third scenarios above may cost only dozens to hundreds of milliseconds.

### Why it is very slow to run DDL statements sometimes?

Possible reasons:

- If you run multiple DDL statements together, the last few DDL statements might run slowly. This is because the DDL statements are executed serially in the TiDB cluster.
- After you start the cluster successfully, the first DDL operation may take a longer time to run, usually around 30s. This is because the TiDB cluster is electing the leader that processes DDL statements.
- The processing time of DDL statements in the first ten minutes after starting TiDB would be much longer than the normal case if you meet the following conditions: 1) TiDB cannot communicate with PD as usual when you are stopping TiDB (including the case of power failure); 2) TiDB fails to clean up the registration data from PD in time because TiDB is stopped by the `kill -9` command. If you run DDL statements during this period, for the state change of each DDL, you need to wait for 2 * lease (lease = 45s).
- If a communication issue occurs between a TiDB server and a PD server in the cluster, the TiDB server cannot get or update the version information from the PD server in time. In this case, you need to wait for 2 * lease for the state processing of each DDL.

### Can I use S3 as the backend storage engine in TiDB?

No. Currently, TiDB only supports the distributed storage engine and the Goleveldb/RocksDB/BoltDB engine.

### Can the `Information_schema` support more real information?

As part of MySQL compatibility, TiDB supports a number of `INFORMATION_SCHEMA` tables. Many of these tables also have a corresponding SHOW command. For more information, see [Information Schema](/information-schema/information-schema.md).

### What's the explanation of the TiDB Backoff type scenario?

In the communication process between the TiDB server and the TiKV server, the `Server is busy` or `backoff.maxsleep 20000ms` log message is displayed when processing a large volume of data. This is because the system is busy while the TiKV server processes data. At this time, usually you can view that the TiKV host resources usage rate is high. If this occurs, you can increase the server capacity according to the resources usage.

### What is the main reason of TiDB TiClient type?

The TiClient Region Error indicator describes the error types and metrics that appear when the TiDB server as a client accesses the TiKV server through the KV interface to perform data operations. The error types include `not_leader` and `stale_epoch`. These errors occur when the TiDB server manipulates the Region leader data according to its own cache information, the Region leader has migrated, or the current TiKV Region information and the routing information of the TiDB cache are inconsistent. Generally, in this case, the TiDB server will automatically retrieve the latest routing data from PD and redo the previous operation.

### What's the maximum number of concurrent connections that TiDB supports?

By default, there is no limit on the maximum number of connections per TiDB server. If needed, you can limit the maximum number of connections by setting `instance.max_connections` in the `config.toml` file, or changing the value of the system variable [`max_connections`](/system-variables.md#max_connections). If too large concurrency leads to an increase of response time, it is recommended to increase the capacity by adding TiDB nodes.

### How to view the creation time of a table?

The `create_time` of tables in the `information_schema` is the creation time.

### What is the meaning of `EXPENSIVE_QUERY` in the TiDB log?

When TiDB is executing a SQL statement, the query will be `EXPENSIVE_QUERY` if each operator is estimated to process over 10,000 rows. You can modify the `tidb-server` configuration parameter to adjust the threshold and then restart the `tidb-server`.

### How do I estimate the size of a table in TiDB?

To estimate the size of a table in TiDB, you can use the following query statement.

```sql
SELECT
  db_name,
  table_name,
  ROUND(SUM(total_size / cnt), 2) Approximate_Size,
  ROUND(
    SUM(
      total_size / cnt / (
        SELECT
          ROUND(AVG(value), 2)
        FROM
          METRICS_SCHEMA.store_size_amplification
        WHERE
          value > 0
      )
    ),
    2
  ) Disk_Size
FROM
  (
    SELECT
      db_name,
      table_name,
      region_id,
      SUM(Approximate_Size) total_size,
      COUNT(*) cnt
    FROM
      information_schema.TIKV_REGION_STATUS
    WHERE
      db_name = @dbname
      AND table_name IN (@table_name)
    GROUP BY
      db_name,
      table_name,
      region_id
  ) tabinfo
GROUP BY
  db_name,
  table_name;
```

When using the above statement, you need to fill in and replace the following fields in the statement as appropriate.

- `@dbname`: the name of the database.
- `@table_name`: the name of the target table.

In addition, in the above statement:

- `store_size_amplification` indicates the average of the cluster compression ratio. In addition to using `SELECT * FROM METRICS_SCHEMA.store_size_amplification;` to query this information, you can also check the **Size amplification** metric for each node on the **Grafana Monitoring PD - statistics balance** panel. The average of the cluster compression ratio is the average of the Size amplification for all nodes.
- `Approximate_Size` indicates the size of the table in a replica before compression. Note that this is an approximate value, not an accurate one.
- `Disk_Size` indicates the size of the table after compression. This is an approximate value and can be calculated according to `Approximate_Size` and `store_size_amplification`.

## TiKV server management

This section describes common problems you might encounter during TiKV server management, their causes, and solutions.

### How to specify the location of data for compliance or multi-tenant applications?

You can use [Placement Rules](/placement-rules-in-sql.md) to specify the location of data for compliance or multi-tenant applications.

Placement Rules in SQL is designed to control the attributes of any continuous data range, such as the number of replicas, the Raft role, the placement location, and the key ranges in which the rules take effect.

### What is the recommended number of replicas in the TiKV cluster? Is it better to keep the minimum number for high availability?

3 replicas for each Region is sufficient for a testing environment. However, you should never operate a TiKV cluster with under 3 nodes in a production scenario. Depending on infrastructure, workload, and resiliency needs, you may wish to increase this number. It is worth noting that the higher the copy, the lower the performance, but the higher the security.

### The `cluster ID mismatch` message is displayed when starting TiKV

This is because the cluster ID stored in local TiKV is different from the cluster ID specified by PD. When a new PD cluster is deployed, PD generates random cluster IDs. TiKV gets the cluster ID from PD and stores the cluster ID locally when it is initialized. The next time when TiKV is started, it checks the local cluster ID with the cluster ID in PD. If the cluster IDs don't match, the `cluster ID mismatch` message is displayed and TiKV exits.

If you previously deploy a PD cluster, but then you remove the PD data and deploy a new PD cluster, this error occurs because TiKV uses the old data to connect to the new PD cluster.

### The `duplicated store address` message is displayed when starting TiKV

This is because the address in the startup parameter has been registered in the PD cluster by other TiKVs. Common conditions that cause this error: There is no data folder in the path specified by TiKV `--data-dir` (no update --data-dir after deleting or moving), restart the TiKV with the previous parameters.Please try [store delete](https://github.com/pingcap/pd/tree/55db505e8f35e8ab4e00efd202beb27a8ecc40fb/tools/pd-ctl#store-delete--label--weight-store_id----jqquery-string) function of pd-ctl, delete the previous store, and then restart TiKV.

### TiKV primary node and secondary node use the same compression algorithm, why the results are different?

Currently, some files of TiKV primary node have a higher compression rate, which depends on the underlying data distribution and RocksDB implementation. It is normal that the data size fluctuates occasionally. The underlying storage engine adjusts data as needed.

### What are the features of TiKV block cache?

TiKV implements the Column Family (CF) feature of RocksDB. By default, the KV data is eventually stored in the 3 CFs (default, write and lock) within RocksDB.

- The default CF stores real data and the corresponding parameter is in `[rocksdb.defaultcf]`.
- The write CF stores the data version information (MVCC) and index-related data, and the corresponding parameter is in `[rocksdb.writecf]`.
- The lock CF stores the lock information and the system uses the default parameter.
- The Raft RocksDB instance stores Raft logs. The default CF mainly stores Raft logs and the corresponding parameter is in `[raftdb.defaultcf]`.
- All CFs have a shared block-cache to cache data blocks and improve RocksDB read speed. The size of block-cache is controlled by the `block-cache-size` parameter. A larger value of the parameter means more hot data can be cached and is more favorable to read operation. At the same time, it consumes more system memory.
- Each CF has an individual write-buffer and the size is controlled by the `write-buffer-size` parameter.

### Why is the TiKV channel full?

- The Raftstore thread is too slow or blocked by I/O. You can view the CPU usage status of Raftstore.
- TiKV is too busy (such as CPU and disk I/O) and cannot manage to handle it.

### Why does TiKV frequently switch Region leader?

- Network problem results in the communication stuck among nodes. You can check Report failures monitoring.
- The node of the original main Leader is stuck, resulting in failure to reach out to the Follower in time.
- Raftstore thread stuck.

### If a node is down, will the service be affected? If yes, how long?

TiKV uses Raft to replicate data among multiple replicas (by default 3 replicas for each Region). If one replica goes wrong, the other replicas can guarantee data safety. Based on the Raft protocol, if a single leader fails as the node goes down, a follower in another node is soon elected as the Region leader after a maximum of 2 * lease time (lease time is 10 seconds).

### What are the TiKV scenarios that take up high I/O, memory, CPU, and exceed the parameter configuration?

Writing or reading a large volume of data in TiKV takes up high I/O, memory and CPU. Executing very complex queries costs a lot of memory and CPU resources, such as the scenario that generates large intermediate result sets.

### Does TiKV support SAS/SATA disks or mixed deployment of SSD/SAS disks?

No. For OLTP scenarios, TiDB requires high I/O disks for data access and operation. As a distributed database with strong consistency, TiDB has some write amplification such as replica replication and bottom layer storage compaction. Therefore, it is recommended to use NVMe SSD as the storage disks in TiDB best practices. Mixed deployment of TiKV and PD is not supported.

### Is the Range of the Key data table divided before data access?

No. It differs from the table splitting rules of MySQL. In TiKV, the table Range is dynamically split based on the size of Region.

### How does Region split?

Region is not divided in advance, but it follows a Region split mechanism. When the Region size exceeds the value of the `region-max-size` or `region-max-keys` parameters, split is triggered. After the split, the information is reported to PD.

### Does TiKV have the `innodb_flush_log_trx_commit` parameter like MySQL, to guarantee the security of data?

Yes. Currently, the standalone storage engine uses two RocksDB instances. One instance is used to store the raft-log. When the `sync-log` parameter in TiKV is set to true, each commit is mandatorily flushed to the raft-log. If a crash occurs, you can restore the KV data using the raft-log.

### What is the recommended server configuration for WAL storage, such as SSD, RAID level, cache strategy of RAID card, NUMA configuration, file system, I/O scheduling strategy of the operating system?

WAL belongs to ordered writing, and currently, we do not apply a unique configuration to it. Recommended configuration is as follows:

- SSD
- RAID 10 preferred
- Cache strategy of RAID card and I/O scheduling strategy of the operating system: currently no specific best practices; you can use the default configuration in Linux 7 or later
- NUMA: no specific suggestion; for memory allocation strategy, you can use `interleave = all`
- File system: ext4

### How is the write performance in the most strict data available mode (`sync-log = true`)?

Generally, enabling `sync-log` reduces about 30% of the performance. For write performance when `sync-log` is set to `false`, see [Performance test result for TiDB using Sysbench](/benchmark/v3.0-performance-benchmarking-with-sysbench.md).

### Can Raft + multiple replicas in the TiKV architecture achieve absolute data safety? Is it necessary to apply the most strict mode (`sync-log = true`) to a standalone storage?

Data is redundantly replicated between TiKV nodes using the [Raft Consensus Algorithm](https://raft.github.io/) to ensure recoverability should a node failure occur. Only when the data has been written into more than 50% of the replicas will the application return ACK (two out of three nodes). However, theoretically, two nodes might crash. Therefore, except for scenarios with less strict requirement on data safety but extreme requirement on performance, it is strongly recommended that you enable the `sync-log` mode.

As an alternative to using `sync-log`, you may also consider having five replicas instead of three in your Raft group. This would allow for the failure of two replicas, while still providing data safety.

For a standalone TiKV node, it is still recommended to enable the `sync-log` mode. Otherwise, the last write might be lost in case of a node failure.

### Since TiKV uses the Raft protocol, multiple network roundtrips occur during data writing. What is the actual write delay?

Theoretically, TiDB has a write delay of 4 more network roundtrips than standalone databases.

### Does TiDB have an InnoDB memcached plugin like MySQL which can directly use the KV interface and does not need the independent cache?

TiKV supports calling the interface separately. Theoretically, you can take an instance as the cache. Because TiDB is a distributed relational database, we do not support TiKV separately.

### What is the Coprocessor component used for?

- Reduce the data transmission between TiDB and TiKV
- Make full use of the distributed computing resources of TiKV to execute computing pushdown.

### The error message `IO error: No space left on device While appending to file` is displayed

This is because the disk space is not enough. You need to add nodes or enlarge the disk space.

### Why does the OOM (Out of Memory) error occur frequently in TiKV?

The memory usage of TiKV mainly comes from the block-cache of RocksDB, which is 40% of the system memory size by default. When the OOM error occurs frequently in TiKV, you should check whether the value of `block-cache-size` is set too high. In addition, when multiple TiKV instances are deployed on a single machine, you need to explicitly configure the parameter to prevent multiple instances from using too much system memory that results in the OOM error.

### Can both TiDB data and RawKV data be stored in the same TiKV cluster?

No. TiDB (or data created from the transactional API) relies on a specific key format. It is not compatible with data created from RawKV API (or data from other RawKV-based services).

## TiDB testing

This section describes common problems you might encounter during TiDB testing, their causes, and solutions.

### What is the performance test result for TiDB using Sysbench?

At the beginning, many users tend to do a benchmark test or a comparison test between TiDB and MySQL. We have also done a similar official test and find the test result is consistent at large, although the test data has some bias. Because the architecture of TiDB differs greatly from MySQL, it is hard to find a benchmark point. The suggestions are as follows:

- Do not spend too much time on the benchmark test. Pay more attention to the difference of scenarios using TiDB.
- See [Performance test result for TiDB using Sysbench](/benchmark/v3.0-performance-benchmarking-with-sysbench.md).

### What's the relationship between the TiDB cluster capacity (QPS) and the number of nodes? How does TiDB compare to MySQL?

- Within 10 nodes, the relationship between TiDB write capacity (Insert TPS) and the number of nodes is roughly 40% linear increase. Because MySQL uses single-node write, its write capacity cannot be scaled.
- In MySQL, the read capacity can be increased by adding secondary database, but the write capacity cannot be increased except using sharding, which has many problems.
- In TiDB, both the read and write capacity can be easily increased by adding more nodes.

### The performance test of MySQL and TiDB by our DBA shows that the performance of a standalone TiDB is not as good as MySQL

TiDB is designed for scenarios where sharding is used because the capacity of a MySQL standalone is limited, and where strong consistency and complete distributed transactions are required. One of the advantages of TiDB is pushing down computing to the storage nodes to execute concurrent computing.

TiDB is not suitable for tables of small size (such as below ten million level), because its strength in concurrency cannot be shown with a small size of data and limited Regions. A typical example is the counter table, in which records of a few lines are updated high frequently. In TiDB, these lines become several Key-Value pairs in the storage engine, and then settle into a Region located on a single node. The overhead of background replication to guarantee strong consistency and operations from TiDB to TiKV leads to a poorer performance than a MySQL standalone.

## Backup and restoration

This section describes common problems you may encounter during backup and restoration, their causes, and solutions.

### How to back up data in TiDB?

Currently, for the backup of a large volume of data (more than 1 TB), the preferred method is using [Backup & Restore (BR)](/br/backup-and-restore-overview.md). Otherwise, the recommended tool is [Dumpling](/dumpling-overview.md). Although the official MySQL tool `mysqldump` is also supported in TiDB to back up and restore data, its performance is no better than BR and it needs much more time to back up and restore large volumes of data.

For more FAQs about BR, see [BR FAQs](/faq/backup-and-restore-faq.md).

### How is the speed of backup and restore?

When [BR](/br/backup-and-restore-overview.md) is used to perform backup and restore tasks, the backup is processed at about 40 MB/s per TiKV instance, and restore is processed at about 100 MB/s per TiKV instance.
