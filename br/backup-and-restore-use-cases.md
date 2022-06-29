---
title: BR Use Cases
summary: Learn the use cases of backing up and restoring data using BR.
aliases: ['/docs/dev/br/backup-and-restore-use-cases/','/docs/dev/reference/tools/br/use-cases/']
---

# BR Use Cases

[Backup & Restore (BR)](/br/backup-and-restore-overview.md) is a tool for distributed backup and restoration of the TiDB cluster data.

This document describes common backup and restoration scenarios:

- [Back up a single table to a network disk (recommended for production environments)](#back-up-a-single-table-to-a-network-disk-recommended-for-production-environments)
- [Restore data from a network disk (recommended for production environments)](#restore-data-from-a-network-disk-recommended-for-production-environments)
- [Back up a single table to a local disk](#back-up-a-single-table-to-a-local-disk-recommended-for-testing-environments)
- [Restore data from a local disk](#restore-data-from-a-local-disk-recommended-for-testing-environments)

This document aims to help you achieve the following goals:

- Back up and restore data using a network disk or local disk correctly.
- Get the status of a backup or restoration operation through monitoring metrics.
- Learn how to tune performance during the backup or restoration operation.
- Troubleshoot the possible anomalies during the backup operation.

## Audience

You are expected to have a basic understanding of TiDB and [TiKV](https://tikv.org/).

Before reading on, make sure you have read [BR Overview](/br/backup-and-restore-overview.md), especially [Usage Restrictions](/br/backup-and-restore-overview.md#usage-restrictions) and [Some tips](/br/backup-and-restore-overview.md#some-tips).

## Prerequisites

This section introduces the recommended method of deploying TiDB, cluster versions, the hardware information of the TiKV cluster, and the cluster configuration for the use case demonstrations.

You can estimate the performance of your backup or restoration operation based on your own hardware and configuration. It is recommended that you use a network disk to back up and restore data. This spares you from collecting backup files and greatly improves the backup efficiency especially when the TiKV cluster is in a large scale.

### Deployment method

It is recommended that you deploy the TiDB cluster using [TiUP](/tiup/tiup-cluster.md) and install BR using TiUP.

### Cluster versions

- TiDB: v6.1.0
- TiKV: v6.1.0
- PD: v6.1.0
- BR: v6.1.0

> **Note:**
>
> It is recommended that you use the latest version of [TiDB/TiKV/PD/BR](/releases/release-notes.md) and make sure that the BR version is **consistent with** the TiDB version.

### TiKV hardware information

- Operating system: CentOS Linux release 7.6.1810 (Core)
- CPU: 16-Core Common KVM processor
- RAM: 32 GB
- Disk: 500 GB SSD * 2
- NIC: 10 Gigabit network card

### Cluster configuration

BR directly sends commands to the TiKV cluster and are not dependent on the TiDB server, so you do not need to configure the TiDB server when using BR.

- TiKV: default configuration
- PD: default configuration

### Others

In addition to the preceding prerequisites, you should also perform the following checks before performing the backup and restoration.

#### Check before backup

Before running the [`br backup` command](/br/use-br-command-line-tool.md#br-command-line-description), make sure the following conditions are met:

- No DDL statements are running on the TiDB cluster.
- The target storage device has required space (no less than 1/3 of the disk space of the backup cluster).

#### Check before restoration

Before running the [`br restore` command](/br/use-br-command-line-tool.md#br-command-line-description), check the target cluster to ensure that the table in this cluster does not have a duplicate name.

## Back up a single table to a network disk (recommended for production environments)

Run the `br backup` command to back up the single table data `--db batchmark --table order_line` to the specified path `local:///br_data` in the network disk.

### Backup prerequisites

- [Check before backup](#check-before-backup)
- Configure a high-performance SSD hard disk host as the NFS server to store data, and all BR nodes, TiKV nodes, and TiFlash nodes as NFS clients. Mount the same path (for example, `/br_data`) to the NFS server for NFS clients to access the server.
- The total transfer rate between the NFS server and all NFS clients must reach at least `the number of TiKV instances * 150MB/s`. Otherwise, the network I/O might become the performance bottleneck.

> **Note:**
>
> - During data backup, because only the data of leader replicas are backed up, even if there is a TiFlash replica in the cluster, BR can complete the backup without mounting TiFlash nodes.
> - When restoring data, BR will restore the data of all replicas. Also, TiFlash nodes need access to the backup data for BR to complete the restore. Therefore, before the restore, you must mount TiFlash nodes to the NFS server.

### Topology

The following diagram shows the typology of BR:

![img](/media/br/backup-nfs-deploy.png)

### Backup operation

Run the `br backup` command:

{{< copyable "shell-regular" >}}

```shell
bin/br backup table \
    --db batchmark \
    --table order_line \
    -s local:///br_data \
    --pd ${PD_ADDR}:2379 \
    --log-file backup-nfs.log
```

### Monitoring metrics for the backup

During the backup process, pay attention to the following metrics on the monitoring panels to get the status of the backup process.

**Backup CPU Utilization**: the CPU usage rate of each working TiKV node in the backup operation (for example, backup-worker and backup-endpoint).

![img](/media/br/backup-cpu.png)

**IO Utilization**: the I/O usage rate of each working TiKV node in the backup operation.

![img](/media/br/backup-io.png)

**BackupSST Generation Throughput**: the backupSST generation throughput of each working TiKV node in the backup operation, which is normally around 150 MB/s.

![img](/media/br/backup-throughput.png)

**One Backup Range Duration**: the duration of backing up a range, which is the total time cost of scanning KVs and storing the range as the backupSST file.

![img](/media/br/backup-range-duration.png)

**One Backup Subtask Duration**: the duration of each sub-task into which a backup task is divided.

> **Note:**
>
> - In this task, the single table to be backed up has three indexes and the task is normally divided into four sub-tasks.
> - The panel in the following image has 20 points on it, 10 blue and 10 yellow, indicating that there are 10 sub-tasks. Region scheduling might occur during the backup process, so a few retries is normal.

![img](/media/br/backup-subtask-duration.png)

**Backup Errors**: the errors occurred during the backup process. No error occurs in normal situations. Even if a few errors occur, the backup operation has the retry mechanism which might increase the backup time but does not affect the operation correctness.

![img](/media/br/backup-errors.png)

**Checksum Request Duration**: the duration of the admin checksum request in the backup cluster.

![img](/media/br/checksum-duration.png)

### Backup results explanation

When finishing the backup, BR outputs the backup summary to the console.

In the log specified before running the backup command, you can get the statistical information of the backup operation from this log. Search "summary" in this log, you can see the following information:

```
["Full backup Success summary:
    total backup ranges: 2,
    total success: 2,
    total failed: 0,
    total take(Full backup time): 31.802912166s,
    total take(real time): 49.799662427s,
    total size(MB): 5997.49,
    avg speed(MB/s): 188.58,
    total kv: 120000000"]
    ["backup checksum"=17.907153678s]
    ["backup fast checksum"=349.333µs]
    ["backup total regions"=43]
    [BackupTS=422618409346269185]
    [Size=826765915]
```

The preceding log includes the following information:

- `total take(Full backup time)`: Backup duration
- `total take(real time)`: Total runtime of the application
- `total size(MB)`: The size of the backup data
- `avg speed(MB/s)`: Backup throughput
- `total kv`: The number of backed-up KV pairs
- `backup checksum`: Backup checksum duration
- `backup fast checksum`: The total duration of calculating the checksum, KV pairs, and bytes of each table
- `backup total regions`: The total number of backup Regions
- `BackupTS`: The snapshot timestamp of the backup data
- `Size`: The actual size of the backup data in the disk after compression

From the preceding information, the throughput of a single TiKV instance can be calculated: `avg speed(MB/s)`/`tikv_count` = `62.86`.

### Performance tuning

If the resource usage of TiKV does not become an obvious bottleneck during the backup process (for example, in the [Monitoring metrics for the backup](#monitoring-metrics-for-the-backup), the highest CPU usage rate of backup-worker is around `1500%` and the overall I/O usage rate is below `30%`), you can try to increase the value of `--concurrency` (`4` by default) to tune the performance. But this performance tuning method is not suitable for the use cases of many small tables. See the following example:

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

- Backup duration (`total take(s)`): reduced from `986.43` to `535.53`
- Backup throughput (`avg speed(MB/s)`): increased from `358.09` to `659.59`
- Throughput of a single TiKV instance (`avg speed(MB/s)/tikv_count`): increased from `89` to `164.89`

## Restore data from a network disk (recommended for production environments)

Use the `br restore` command to restore the complete backup data to an offline cluster. Currently, BR does not support restoring data to an online cluster.

### Restoration prerequisites

- [Check before restore](#check-before-restoration)

### Topology

The following diagram shows the typology of BR:

![img](/media/br/restore-nfs-deploy.png)

### Restoration operation

Run the `br restore` command:

{{< copyable "shell-regular" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///br_data --pd 172.16.5.198:2379 --log-file restore-nfs.log
```

### Monitoring metrics for the restoration

During the restoration process, pay attention to the following metrics on the monitoring panels to get the status of the restoration process.

**CPU**: the CPU usage rate of each working TiKV node in the restoration operation.

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

**Checksum Request Duration**: the duration of the admin checksum request. This duration for the restoration is longer than that for the backup.

![img](/media/br/restore-checksum.png)

### Restoration results explanation

In the log specified before running the restoration command, you can get the statistical information of the restoration operation from this log. Search "summary" in this log, you can see the following information:

```
["Table Restore summary:
    total restore tables: 1,
    total success: 1,
    total failed: 0,
    total take(Full restore time): 17m1.001611365s,
    total take(real time): 16m1.371611365s,
    total kv: 5659888624,
    total size(MB): 353227.18,
    avg speed(MB/s): 367.42"]
    ["restore files"=9263]
    ["restore ranges"=6888]
    ["split region"=49.049182743s]
    ["restore checksum"=6m34.879439498s]
    [Size=48693068713]
```

The preceding log includes the following information:

- `total take(Full restore time)`: The restoration duration
- `total take(real time)`: The total runtime of the application
- `total size(MB)`: The size of the data to be restored
- `total kv`: The number of restored KV pairs
- `avg speed(MB/s)`: The restoration throughput
- `split region`: The Region split duration
- `restore checksum`: The restoration checksum duration
- `Size`: The actual size of the restored data in the disk

From the preceding information, the following items can be calculated:

- The throughput of a single TiKV instance: `avg speed(MB/s)`/`tikv_count` = `91.8`
- The average restore speed of a single TiKV instance: `total size(MB)`/(`split time` + `restore time`)/`tikv_count` = `87.4`

#### Performance tuning

If the resource usage of TiKV does not become an obvious bottleneck during the restore process, you can increase the value of `--concurrency` (defaults to `128`). See the following example:

{{< copyable "shell-regular" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///br_data/ --pd 172.16.5.198:2379 --log-file restore-concurrency.log --concurrency 1024
```

The tuned performance results are as follows (with the same data size):

- Restoration duration (`total take(s)`): reduced from `961.37` to `443.49`
- Restoration throughput (`avg speed(MB/s)`): increased from `367.42` to `796.47`
- Throughput of a single TiKV instance (`avg speed(MB/s)`/`tikv_count`): increased from `91.8` to `199.1`
- Average restore speed of a single TiKV instance (`total size(MB)`/(`split time` + `restore time`)/`tikv_count`): increased from `87.4` to `162.3`

## Back up a single table to a local disk (recommended for testing environments)

Run the `br backup` command to back up a single table `--db batchmark --table order_line` to the specified path `local:///home/tidb/backup_local` in the local disk.

### Backup prerequisites

* [Check before backup](#check-before-backup)
* Each TiKV node has a separate disk to store backupSST files.
* The `backup_endpoint` node has a separate disk to store `backupmeta` files.
* TiKV and the `backup_endpoint` node share the same directory (for example, `/home/tidb/backup_local`) for backup.

### Topology

The following diagram shows the typology of BR:

![img](/media/br/backup-local-deploy.png)

### Backup operation

Run the `br backup` command:

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

In the log specified before running the backup command, you can get the statistical information of the restoration operation from this log. Search "summary" in this log, you can see the following information:

```
["Table backup summary:
    total backup ranges: 4,
    total success: 4,
    total failed: 0,
    total take(s): 551.31,
    total kv: 5659888624,
    total size(MB): 353227.18,
    avg speed(MB/s): 640.71"]
    ["backup total regions"=6795]
    ["backup checksum"=6m33.962719217s]
    ["backup fast checksum"=22.995552ms]
```

The preceding log includes the following information:

- `total take(s)`: The backup duration
- `total size(MB)`: The data size
- `avg speed(MB/s)`: The backup throughput
- `backup checksum`: The backup checksum duration

From the preceding information, the throughput of a single TiKV instance can be calculated: `avg speed(MB/s)`/`tikv_count` = `160`.

## Restore data from a local disk (recommended for testing environments)

Run the `br restore` command to restore the complete backup data to an offline cluster. Currently, BR does not support restoring data to an online cluster.

### Restoration prerequisites

- [Check before restore](#check-before-restoration)
- The TiKV cluster and the backup data do not have a duplicate database or table. Currently, BR does not support table route.
- Each TiKV node has a separate disk to store backupSST files.
- The `restore_endpoint` node has a separate disk to store `backupmeta` files.
- TiKV and the `restore_endpoint` node share the same directory (for example, `/home/tidb/backup_local/`) for restoration.

Before the restoration, follow these steps:

1. Collect all backupSST files into the same directory.
2. Copy the collected backupSST files to all TiKV nodes of the cluster.
3. Copy the `backupmeta` files to the `restore endpoint` node.

### Topology

The following diagram shows the typology of BR:

![img](/media/br/restore-local-deploy.png)

### Restoration operation

Run the `br restore` command:

{{< copyable "shell-regular" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///home/tidb/backup_local/ --pd 172.16.5.198:2379 --log-file restore_local.log
```

During the restoration process, pay attention to the metrics on the monitoring panels to get the status of the restoration process. See [Monitoring metrics for the restoration](#monitoring-metrics-for-the-restoration) for details.

### Restoration results explanation

In the log specified before running the restoration command, you can get the statistical information of the restoration operation from this log. Search "summary" in this log, you can see the following information:

```
["Table Restore summary:
    total restore tables: 1,
    total success: 1,
    total failed: 0,
    total take(s): 908.42,
    total kv: 5659888624,
    total size(MB): 353227.18,
    avg speed(MB/s): 388.84"]
    ["restore files"=9263]
    ["restore ranges"=6888]
    ["split region"=58.7885518s]
    ["restore checksum"=6m19.349067937s]
```

The preceding log includes the following information:

- `total take(s)`: The restoration duration
- `total size(MB)`: The data size
- `avg speed(MB/s)`: The restoration throughput
- `split region`: The region split duration
- `restore checksum`: The restoration checksum duration

From the preceding information, the following items can be calculated:

- The throughput of a single TiKV instance: `avg speed(MB/s)`/`tikv_count` = `97.2`
- The average restoration speed of a single TiKV instance: `total size(MB)`/(`split time` + `restore time`)/`tikv_count` = `92.4`

## Error handling during backup

This section introduces the common errors that might occur during the backup process.

### `key locked Error` in the backup log

Error message in the log: `log - ["backup occur kv error"][error="{\"KvError\":{\"locked\":`

If a key is locked during the backup process, BR tries to resolve the lock. A small number of this error do not affect the correctness of the backup.

### Backup failure

Error message in the log: `log - Error: msg:"Io(Custom { kind: AlreadyExists, error: \"[5_5359_42_123_default.sst] is already exists in /dir/backup_local/\" })"`

If the backup operation fails and the preceding message occurs, perform one of the following operations and then start the backup operation again:

- Change the directory for the backup. For example, change `/dir/backup-2020-01-01/` to `/dir/backup_local/`.
- Delete the backup directory of all TiKV nodes and BR nodes.
