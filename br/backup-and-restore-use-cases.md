---
title: BR Use Cases
summary: Learn the use cases of backing up and restoring data using BR.
aliases: ['/docs/dev/br/backup-and-restore-use-cases/','/docs/dev/reference/tools/br/use-cases/']
---

# BR Use Cases

[Backup & Restore](/br/backup-and-restore-tool.md) (BR) is a command-line tool for distributed backup and restoration of the TiDB cluster data. This document describes the processes of operating BR in [four use cases](#use-cases) that aims to help you achieve the following goals:

* Back up and restore data using a network disk or local disk correctly.
* Get the status of a backup or restoration operation through monitoring metrics.
* Learn how to tune performance during the operation.
* Troubleshoot the possible anomalies during the backup operation.

> **Note:**
>
> Pay attention to the [usage restrictions](/br/backup-and-restore-tool.md#usage-restrictions) before using BR.

## Audience

You are expected to have a basic understanding of [TiDB](https://docs.pingcap.com/tidb/v4.0) and [TiKV](https://tikv.org/). Before reading this document, it is recommended that you read [Use BR to Back up and Restore Data](/br/backup-and-restore-tool.md) first.

## Prerequisites

This section introduces the recommended method of deploying TiDB, cluster versions, the hardware information of the TiKV cluster, and the cluster configuration for the use case demonstrations. You can estimate the performance of your backup or restoration operation based on your own hardware and configuration.

### Deployment method

It is recommended that you deploy the TiDB cluster using [TiUP](/tiup/tiup-cluster.md) and get BR by downloading [TiDB Toolkit](/download-ecosystem-tools.md#br-backup-and-restore).

### Cluster versions

* TiDB: v4.0.2
* TiKV: v4.0.2
* PD: v4.0.2
* BR: v4.0.2

> **Note:**
>
> v4.0.2 was the latest version at the time this document was written. It is recommended that you use the latest version of [TiDB/TiKV/PD/BR](/releases/release-notes.md) and make sure that the BR version is **consistent with** the TiDB version.

### TiKV hardware information

* Operating system: CentOS Linux release 7.6.1810 (Core)
* CPU: 16-Core Common KVM processor
* RAM: 32GB
* Disk: 500G SSD * 2
* NIC: 10000MB/s

### Cluster configuration

BR directly sends commands to the TiKV cluster and are not dependent on the TiDB server, so you do not need to configure the TiDB server when using BR.

* TiKV: default configuration
* PD: default configuration

## Use cases

This document describes the following four use cases:

* [Back up a single table to a network disk (recommended)](#back-up-a-single-table-to-a-network-disk-recommended)
* [Restore data from a network disk (recommended)](#restore-data-from-a-network-disk-recommended)
* [Back up a single table to a local disk](#back-up-a-single-table-to-a-local-disk)
* [Restore data from a local disk](#restore-data-from-a-local-disk)

It is recommended that you use a network disk to back up and restore data. This spares you from collecting backup files and greatly improves the backup efficiency especially when the TiKV cluster is in a large scale.

> **Note:**
>
> Before the backup or restoration operation, you need to do some preparations. See [Preparation for backup](#preparation-for-backup) and [Preparation for restoration](#preparation-for-restoration) for details.

### Preparation for backup

For the detailed usage of the `br backup` command, refer to [BR command-line description](/br/backup-and-restore-tool.md#command-line-description).

1. Before executing the `br backup` command, check the value of the [`tikv_gc_life_time`](/garbage-collection-configuration.md#tikv_gc_life_time) configuration item, and adjust the value appropriately in the MySQL client to make sure that [Garbage Collection](/garbage-collection-overview.md) (GC) does not run during the backup operation.

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    UPDATE mysql.tidb SET VARIABLE_VALUE = '720h' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. After the backup operation, set the parameter back to the original value.

    {{< copyable "sql" >}}

    ```sql
    UPDATE mysql.tidb SET VARIABLE_VALUE = '10m' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

### Preparation for restoration

For the detailed usage of the `br restore` command, refer to [BR command-line description](/br/backup-and-restore-tool.md#command-line-description).

> **Note:**
>
> Before executing the `br restore` command, check the new cluster to make sure that the table in the cluster does not have a duplicate name.

### Back up a single table to a network disk (recommended)

Use the `br backup` command to back up the single table data `--db batchmark --table order_line` to the specified path `local:///br_data` in the network disk.

#### Backup prerequisites

* Configure a high-performance SSD hard disk host as the NFS server to store data, and all BR nodes and TiKV nodes as NFS clients. Mount the same path (for example, `/br_data`) to the NFS server for NFS clients to access the server.
* The total transfer rate between the NFS server and all NFS clients must reach at least `the number of TiKV instances * 150MB/s`. Otherwise the network I/O might become the performance bottleneck.

#### Topology

The following diagram shows the typology of BR:

![img](/media/br/backup-nfs-deploy.png)

#### Backup operation

Before the backup operation, execute the `admin checksum table order_line` command to get the statistical information of the table to be backed up (`--db batchmark --table order_line`). The following image shows an example of this information:

![img](/media/br/total-data.png)

Execute the `br backup` command:

{{< copyable "shell-regular" >}}

```shell
bin/br backup table \
    --db batchmark \
    --table order_line \
    -s local:///br_data \
    --pd ${PD_ADDR}:2379 \
    --log-file backup-nfs.log
```

#### Monitoring metrics for the backup

During the backup process, pay attention to the following metrics on the monitoring panels to get the status of the backup process.

**Backup CPU Utilization**: the CPU usage rate of each working TiKV node in the backup operation (for example, backup-worker and backup-endpoint).

![img](/media/br/backup-cpu.png)

**IO Utilization**: the I/O usage rate of each working TiKV node in the backup operation.

![img](/media/br/backup-io.png)

**BackupSST Generation Throughput**: the backupSST generation throughput of each working TiKV node in the backup operation, which is normally around 150MB/s.

![img](/media/br/backup-throughput.png)

**One Backup Range Duration**: the duration of backing up a range, which is the total time cost of scanning KVs and storing the range as the backupSST file.

![img](/media/br/backup-range-duration.png)

**One Backup Subtask Duration**: the duration of each sub-task into which a backup task is divided.

> **Note:**
>
> * In this task, the single table to be backed up has three indexes and the task is normally divided into four sub-tasks.
> * The panel in the following image has thirteen points on it, which means nine (namely, 13-4) retries. Region scheduling might occur during the backup process, so a few retries is normal.

![img](/media/br/backup-subtask-duration.png)

**Backup Errors**: the errors occurred during the backup process. No error occurs in normal situations. Even if a few errors occur, the backup operation has the retry mechanism which might increase the backup time but does not affect the operation correctness.

![img](/media/br/backup-errors.png)

**Checksum Request Duration**: the duration of the admin checksum request in the backup cluster.

![img](/media/br/checksum-duration.png)

#### Backup results explanation

Before executing the backup command, a path in which the log is stored has been specified. You can get the statistical information of the backup operation from this log. Search "summary" in this log, you can see the following information:

```
["Table backup summary:
    total backup ranges: 4,
    total success: 4,
    total failed: 0,
    total take(s): 986.43,
    total kv: 5659888624,
    total size(MB): 353227.18,
    avg speed(MB/s): 358.09"]
    ["backup total regions"=7196]
    ["backup checksum"=6m28.291772955s]
    ["backup fast checksum"=24.950298ms]
```

The above log includes the following information:

* Backup duration: `total take(s): 986.43`
* Data size: `total size(MB): 353227.18`
* Backup throughput: `avg speed(MB/s): 358.09`
* Backup checksum duration: `take=6m28.29s`

From the above information, the throughput of a single TiKV instance can be calculated: `avg speed(MB/s)`/`tikv_count` = `89`.

#### Performance tuning

If the resource usage of TiKV does not become an obvious bottleneck during the backup process (for example, in the [Monitoring metrics for the backup](#monitoring-metrics-for-the-backup), the highest CPU usage rate of backup-worker is around `1500%` and the overall I/O usage rate is below `30%`), you can try to increase the value of `--concurrency` to tune the performance. But this performance tuning method is not suitable for the use cases of many small tables. See the following example:

{{< copyable "shell-regular" >}}

```shell
bin/br backup table \
    --db batchmark \
    --table order_line \
    -s local:///br_data/ \
    --pd ${PD_ADDR}:2379 \
    --log-file backup-nfs.log \
    --concurrency 16
```

![img](/media/br/backup-diff.png)

![img](/media/br/backup-diff2.png)

The tuned performance results are as follows (with the same data size):

* Backup duration: `total take(s)` reduced from `986.43` to `535.53`
* Backup throughput: `avg speed(MB/s)` increased from `358.09` to `659.59`
* Throughput of a single TiKV instance: `avg speed(MB/s)/tikv_count` increased from `89` to `164.89`

### Restore data from a network disk (recommended)

Use the `br restore` command to restore the complete backup data to an offline cluster. Currently, BR does not support restoring data to an online cluster.

#### Restoration prerequisites

None

#### Topology

The following diagram shows the typology of BR:

![img](/media/br/restore-nfs-deploy.png)

#### Restoration operation

Before the restoration, refer to [Preparation for restoration](#preparation-for-restoration) for the preparation.

Execute the `br restore` command:

{{< copyable "shell-regular" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///br_data --pd 172.16.5.198:2379 --log-file restore-nfs.log
```

#### Monitoring metrics for the restoration

During the restoration process, pay attention to the following metrics on the monitoring panels to get the status of the restoration process.

**CPU Utilization**: the CPU usage rate of each working TiKV node in the restoration operation.

![img](/media/br/restore-cpu.png)

**IO Utilization**: the I/O usage rate of each working TiKV node in the restoration operation.

![img](/media/br/restore-io.png)

**Region**: the Region distribution. The more even Regions are distributed, the better the restoration resources are used.

![img](/media/br/restore-region.png)

**Process SST Duration**: the delay of processing the SST files. When restoring a table, if `tableID` is changed, you need to rewrite `tableID`. Otherwise, `tableID` is renamed. Generally, the delay of rewriting is longer than that of renaming.

![img](/media/br/restore-process-sst.png)

**DownLoad SST Throughput**: the throughput of downloading SST files from External Storage.

![img](/media/br/restore-download-sst.png)

**Restore Errors**: the errors occurred during the restoration process.

![img](/media/br/restore-errors.png)

**Checksum Request duration**: the duration of the admin checksum request. This duration for the restoration is longer than that for the backup.

![img](/media/br/restore-checksum.png)

#### Restoration results explanation

Before executing the restoration command, a path in which the log is stored has been specified. You can get the statistical information of the restoration operation from this log. Search "summary" in this log, you can see the following information:

```
["Table Restore summary:
    total restore tables: 1,
    total success: 1,
    total failed: 0,
    total take(s): 961.37,
    total kv: 5659888624,
    total size(MB): 353227.18,
    avg speed(MB/s): 367.42"]
    ["restore files"=9263]
    ["restore ranges"=6888]
    ["split region"=49.049182743s]
    ["restore checksum"=6m34.879439498s]
```

The above log includes the following information:

* Restoration duration: `total take(s):961.37`
* Data size: `total size(MB): 353227.18`
* Restoration throughput: `avg speed(MB/s): 367.42`
* `Region Split` duration: `take=49.049182743s`
* Restoration checksum duration: `take=6m34.879439498s`

From the above information, the following items can be calculated:

* The throughput of a single TiKV instance: `avg speed(MB/s)`/`tikv_count` = `91.8`
* The average restoration speed of a single TiKV instance: `total size(MB)`/(`split time` + `restore time`)/`tikv_count` = `87.4`

#### Performance tuning

If the resource usage of TiKV does not become an obvious bottleneck during the restoration process, you can try to increase the value of `--concurrency` which is `128` by default. See the following example:

{{< copyable "shell-regular" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///br_data/ --pd 172.16.5.198:2379 --log-file restore-concurrency.log --concurrency 1024
```

The tuned performance results are as follows (with the same data size):

+ Restoration duration: `total take(s)` reduced from `961.37` to `443.49`
+ Restoration throughput: `avg speed(MB/s)` increased from `367.42` to `796.47`
+ Throughput of a single TiKV instance: `avg speed(MB/s)`/`tikv_count` increased from `91.8` to `199.1`
+ Average restoration speed of a single TiKV instance: `total size(MB)`/(`split time` + `restore time`)/`tikv_count` increased from `87.4` to `162.3`

### Back up a single table to a local disk

Use the `br backup` command to back up the single table `--db batchmark --table order_line` to the specified path `local:///home/tidb/backup_local` in the local disk.

#### Backup prerequisites

* Each TiKV node has a separate disk to store the backupSST file.
* The `backup_endpoint` node has a separate disk to store the `backupmeta` file.
* TiKV and the `backup_endpoint` node must have the same directory for the backup (for example, `/home/tidb/backup_local`).

#### Topology

The following diagram shows the typology of BR:

![img](/media/br/backup-local-deploy.png)

#### Backup operation

Before the backup operation, execute the `admin checksum table order_line` command to get the statistical information of the table to be backed up (`--db batchmark --table order_line`). The following image shows an example of this information:

![img](/media/br/total-data.png)

Execute the `br backup` command:

{{< copyable "shell-regular" >}}

```shell
bin/br backup table \
    --db batchmark \
    --table order_line \
    -s local:///home/tidb/backup_local/ \
    --pd ${PD_ADDR}:2379 \
    --log-file backup_local.log
```

During the backup process, pay attention to the metrics on the monitoring panels to get the status of the backup process. See [Monitoring metrics for the backup](#monitoring-metrics-for-the-backup) for details.

#### Backup results explanation

Before executing the backup command, a path in which the log is stored has been specified. You can get the statistical information of the backup operation from this log. Search "summary" in this log, you can see the following information:

```
["Table backup summary: total backup ranges: 4, total success: 4, total failed: 0, total take(s): 551.31, total kv: 5659888624, total size(MB): 353227.18, avg speed(MB/s): 640.71"] ["backup total regions"=6795] ["backup checksum"=6m33.962719217s] ["backup fast checksum"=22.995552ms]
```

The information from the above log includes:

+ Backup duration: `total take(s): 551.31`
+ Data size: `total size(MB): 353227.18`
+ Backup throughput: `avg speed(MB/s): 640.71`
+ Backup checksum duration: `take=6m33.962719217s`

From the above information, the throughput of a single TiKV instance can be calculated: `avg speed(MB/s)`/`tikv_count` = `160`.

### Restore data from a local disk

Use the `br restore` command to restore the complete backup data to an offline cluster. Currently, BR does not support restoring data to an online cluster.

#### Restoration prerequisites

* The TiKV cluster and the backup data do not have a duplicate database or table. Currently, BR does not support table route.
* Each TiKV node has a separate disk to store the backupSST file.
* The `restore_endpoint` node has a separate disk to store the `backupmeta` file.
* TiKV and the `restore_endpoint` node must have the same directory for the restoration (for example, `/home/tidb/backup_local/`).

Before the restoration, follow these steps:

1. Collect all backupSST files into the same directory.
2. Copy the collected backupSST files to all TiKV nodes of the cluster.
3. Copy the `backupmeta` file to the `restore endpoint` node.

#### Topology

The following diagram shows the typology of BR:

![img](/media/br/restore-local-deploy.png)

#### Restoration operation

Execute the `br restore` command:

{{< copyable "shell-regular" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///home/tidb/backup_local/ --pd 172.16.5.198:2379 --log-file restore_local.log
```

During the restoration process, pay attention to the metrics on the monitoring panels to get the status of the restoration process. See [Monitoring metrics for the restoration](#monitoring-metrics-for-the-restoration) for details.

#### Restoration results explanation

Before executing the restoration command, a path in which the log is stored has been specified. You can get the statistical information of the restoration operation from this log. Search "summary" in this log, you can see the following information:

```
["Table Restore summary: total restore tables: 1, total success: 1, total failed: 0, total take(s): 908.42, total kv: 5659888624, total size(MB): 353227.18, avg speed(MB/s): 388.84"] ["restore files"=9263] ["restore ranges"=6888] ["split region"=58.7885518s] ["restore checksum"=6m19.349067937s]
```

The above log includes the following information:

+ Restoration duration: `total take(s): 908.42`
+ Data size: `total size(MB): 353227.18`
+ Restoration throughput: `avg speed(MB/s):  388.84`
+ `Region Split` duration: `take=58.7885518s`
+ Restoration checksum duration: `take=6m19.349067937s`

From the above information, the following items can be calculated:

* The throughput of a single TiKV instance: `avg speed(MB/s)`/`tikv_count` = `97.2`
* The average restoration speed of a single TiKV instance: `total size(MB)`/(`split time` + `restore time`)/`tikv_count` = `92.4`

### Error handling

This section introduces the common errors occurred during the backup process.

#### `key locked Error` in the backup log

Error message in the log: `log - ["backup occur kv error"][error="{\"KvError\":{\"locked\":`

If a key is locked during the backup process, BR tries to resolve the lock. A small number of this error does not affect the correctness of the backup.

#### Backup failure

Error message in the log: `log - Error: msg:"Io(Custom { kind: AlreadyExists, error: \"[5_5359_42_123_default.sst] is already exists in /dir/backup_local/\" })"`

If the backup operation fails and the above message occurs, perform one of the following operations and then start the backup operation again:

* Change the directory for the backup. For example, change `/dir/backup-2020-01-01/` to `/dir/backup_local/`.
* Delete the backup directory of all TiKV nodes and BR nodes.
