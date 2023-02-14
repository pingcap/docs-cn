---
title: Backup & Restore FAQs
summary: Learn about Frequently Asked Questions (FAQs) and the solutions of backup and restore.
aliases: ['/docs/dev/br/backup-and-restore-faq/','/tidb/dev/pitr-troubleshoot/','/tidb/dev/pitr-known-issues/']
---

# Backup & Restore FAQs

This document lists the frequently asked questions (FAQs) and the solutions of TiDB Backup & Restore (BR).

## What should I do to quickly recover data after mistakenly deleting or updating data?

TiDB v6.4.0 introduces the flashback feature. You can use this feature to quickly recover data within the GC time to a specified point in time. Therefore, if misoperations occur, you can use this feature to recover data. For details, see [Flashback Cluster](/sql-statements/sql-statement-flashback-to-timestamp.md) and [Flashback Database](/sql-statements/sql-statement-flashback-database.md).

## In TiDB v5.4.0 and later versions, when backup tasks are performed on the cluster under a heavy workload, why does the speed of backup tasks become slow?

Starting from TiDB v5.4.0, BR introduces the auto-tune feature for backup tasks. For clusters in v5.4.0 or later versions, this feature is enabled by default. When the cluster workload is heavy, the feature limits the resources used by backup tasks to reduce the impact on the online cluster. For more information, refer to [Backup Auto-Tune](/br/br-auto-tune.md).

TiKV supports [dynamically configuring](/tikv-control.md#modify-the-tikv-configuration-dynamically) the auto-tune feature. You can enable or disable the feature by the following methods without restarting your cluster:

- Disable auto-tune: Set the TiKV configuration item [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540) to `false`.
- Enable auto-tune: Set `backup.enable-auto-tune` to `true`. For clusters upgraded from v5.3.x to v5.4.0 or later versions, the auto-tune feature is disabled by default. You need to manually enable it.

To use `tikv-ctl` to enable or disable auto-tune, refer to [Use auto-tune](/br/br-auto-tune.md#use-auto-tune).

In addition, auto-tune reduces the default number of threads used by backup tasks. For details, see `backup.num-threads`](/tikv-configuration-file.md#num-threads-1). Therefore, on the Grafana Dashboard, the speed, CPU usage, and I/O resource utilization used by backup tasks are lower than those of versions earlier than v5.4.0. Before v5.4.0, the default value of `backup.num-threads` was `CPU * 0.75`, that is, the number of threads used by backup tasks makes up 75% of the logical CPU cores. The maximum value of it was `32`. Starting from v5.4.0, the default value of this configuration item is `CPU * 0.5`, and its maximum value is `8`.

When you perform backup tasks on an offline cluster, to speed up the backup, you can modify the value of `backup.num-threads` to a larger number using `tikv-ctl`.

## PITR issues

### What is the difference between [PITR](/br/br-pitr-guide.md) and [cluster flashback](/sql-statements/sql-statement-flashback-to-timestamp.md)?

From the perspective of use cases, PITR is usually used to restore the data of a cluster to a specified point in time when the cluster is completely out of service or the data is corrupted and cannot be recovered using other solutions. To use PITR, you need a new cluster for data recovery. The cluster flashback feature is specifically designed for the data error scenarios caused by user mis-operations or other factors, which allows you to restore the data of a cluster in-place to the latest timestamp before the data errors occur.

In most cases, flashback is a better recovery solution than PITR for data errors caused by human mistakes, as it has a much shorter RPO (close to zero) and RTO. However, when a cluster is completely unavailable, because flashback cannot run at this time, PITR is the only solution to recover the cluster in this case. Therefore, PITR is always a must-have solution when you develop database disaster recovery strategies, even though it has a longer RPO (up to 5 minutes) and RTO than flashback.

### When the upstream database imports data using TiDB Lightning in the physical import mode, the log backup feature becomes unavailable. Why?

Currently, the log backup feature is not fully adapted to TiDB Lightning. Therefore, data imported in the physical mode of TiDB Lightning cannot be backed up into log data

In upstream clusters where you create log backup tasks, avoid using the TiDB Lightning physical mode to import data. Instead, you can use TiDB Lightning logical mode. If you do need to use the physical mode, perform a snapshot backup after the import is complete, so that PITR can be restored to the time point after the snapshot backup.

### Why is the acceleration of adding indexes feature incompatible with PITR?

Issue: [#38045](https://github.com/pingcap/tidb/issues/38045)

Currently, the [acceleration of adding indexes](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) feature is not compatible with PITR. When using index acceleration, you need to ensure that there are no PITR log backup tasks running in the background. Otherwise, unexpected behaviors might occur, including:

- If you start a log backup task first, and then add an index. The adding index process is not accelerated even if index acceleration is enabled. But the index is added in a slow way.
- If you start an index acceleration task first, and then start a log backup task. The log backup task returns an error. But the index acceleration is not affected.
- If you start a log backup task and an index acceleration task at the same time, the two tasks might not be aware of each other. This might result in PITR failing to back up the newly added index.

### The cluster has recovered from the network partition failure, but the checkpoint of the log backup task progress still does not resume. Why?

Issue: [#13126](https://github.com/tikv/tikv/issues/13126)

After a network partition failure in the cluster, the backup task cannot continue backing up logs. After a certain retry time, the task will be set to `ERROR` state. At this point, the backup task has stopped.

To resolve this issue, you need to manually execute the `br log resume` command to resume the log backup task.

### What should I do if the error `execute over region id` is returned when I perform PITR?

Issue: [#37207](https://github.com/pingcap/tidb/issues/37207)

This issue usually occurs when you enable log backup during a full data import and afterward perform a PITR to restore data at a time point during the data import.

Specifically, there is a probability that this issue occurs if there are a large number of hotspot writes for a long time (such as 24 hours) and if the OPS of each TiKV node is larger than 50k/s (you can view the metrics in Grafana: **TiKV-Details** -> **Backup Log** -> **Handle Event Rate**).

It is recommended that you perform a snapshot backup after the data import and perform PITR based on this snapshot backup.

## After restoring a downstream cluster using the `br restore point` command, data cannot be accessed from TiFlash. What should I do?

Currently, PITR does not support writing data directly to TiFlash during the restore phase. Instead, br command-line tool executes the `ALTER TABLE table_name SET TIFLASH REPLICA ***` DDL to replicate the data. Therefore, TiFlash replicas are not available immediately after PITR completes data restore. Instead, you need to wait for a certain period of time for the data to be replicated from TiKV nodes. To check the replication progress, check the `progress` information in the `INFORMATION_SCHEMA.tiflash_replica` table.

### What should I do if the `status` of a log backup task becomes `ERROR`?

During a log backup task, the task status becomes `ERROR` if it fails and cannot be recovered after retrying. The following is an example:

```shell
br log status --pd x.x.x.x:2379

● Total 1 Tasks.
> #1 <
                    name: task1
                  status: ○ ERROR
                   start: 2022-07-25 13:49:02.868 +0000
                     end: 2090-11-18 14:07:45.624 +0000
                 storage: s3://tmp/br-log-backup0ef49055-5198-4be3-beab-d382a2189efb/Log
             speed(est.): 0.00 ops/s
      checkpoint[global]: 2022-07-25 14:46:50.118 +0000; gap=11h31m29s
          error[store=1]: KV:LogBackup:RaftReq
error-happen-at[store=1]: 2022-07-25 14:54:44.467 +0000; gap=11h23m35s
  error-message[store=1]: retry time exceeds: and error failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }: failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }: failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }
```

To address this problem, check the error message for the cause and perform as instructed. After the problem is addressed, run the following command to resume the task:

```shell
br log resume --task-name=task1 --pd x.x.x.x:2379
```

After the backup task is resumed, you can check the status using `br log status`. The backup task continues when the task status becomes `NORMAL`.

```shell
● Total 1 Tasks.
> #1 <
              name: task1
            status: ● NORMAL
             start: 2022-07-25 13:49:02.868 +0000
               end: 2090-11-18 14:07:45.624 +0000
           storage: s3://tmp/br-log-backup0ef49055-5198-4be3-beab-d382a2189efb/Log
       speed(est.): 15509.75 ops/s
checkpoint[global]: 2022-07-25 14:46:50.118 +0000; gap=6m28s
```

> **Note:**
>
> This feature backs up multiple versions of data. When a long backup task fails and the status becomes `ERROR`, the checkpoint data of this task is set as a `safe point`, and the data of the `safe point` will not be garbage collected within 24 hours. Therefore, the backup task continues from the last checkpoint after resuming the error. If the task fails for more than 24 hours and the last checkpoint data has been garbage collected, an error will be reported when you resume the task. In this case, you can only run the `br log stop` command to stop the task first and then start a new backup task.

### What should I do if the error message `ErrBackupGCSafepointExceeded` is returned when using the `br log resume` command to resume a suspended task?

```shell
Error: failed to check gc safePoint, checkpoint ts 433177834291200000: GC safepoint 433193092308795392 exceed TS 433177834291200000: [BR:Backup:ErrBackupGCSafepointExceeded]backup GC safepoint exceeded
```

After you pause a log backup task, to prevent the MVCC data from being garbage collected, the pausing task program sets the current checkpoint as the service safepoint automatically. This ensures that the MVCC data generated within 24 hours can remain. If the MVCC data of the backup checkpoint has been generated for more than 24 hours, the data of the checkpoint will be garbage collected, and the backup task is unable to resume.

To address this problem, delete the current task using `br log stop`, and then create a log backup task using `br log start`. At the same time, you can perform a full backup for subsequent PITR.

## Feature compatibility issues

### Why does data restored using br command-line tool cannot be replicated to the upstream cluster of TiCDC or Drainer?

+ **The data restored using BR cannot be replicated to the downstream**. This is because BR directly imports SST files but the downstream cluster currently cannot obtain these files from the upstream.

+ Before v4.0.3, DDL jobs generated during the restore might cause unexpected DDL executions in TiCDC/Drainer. Therefore, if you need to perform restore on the upstream cluster of TiCDC/Drainer, add all tables restored using br command-line tool to the TiCDC/Drainer block list.

You can use [`filter.rules`](https://github.com/pingcap/tiflow/blob/7c3c2336f98153326912f3cf6ea2fbb7bcc4a20c/cmd/changefeed.toml#L16) to configure the block list for TiCDC and use [`syncer.ignore-table`](/tidb-binlog/tidb-binlog-configuration-file.md#ignore-table) to configure the block list for Drainer.

### Why is `new_collations_enabled_on_first_bootstrap` mismatch reported during restore?

Since TiDB v6.0.0, the default value of [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) has changed from `false` to `true`. BR backs up the `new_collations_enabled_on_first_bootstrap` configuration of the upstream cluster and then checks whether the value of this configuration is consistent between the upstream and downstream clusters. If the value is consistent, BR safely restores the data backed up in the upstream cluster to the downstream cluster. If the value is inconsistent, BR does not perform the data restore and reports an error.

Suppose that you have backed up the data in a TiDB cluster of an earlier version of v6.0.0, and you want to restore this data to a TiDB cluster of v6.0.0 or later versions. In this situation, you need to manually check whether the value of `new_collations_enabled_on_first_bootstrap` is consistent between the upstream and downstream clusters:

- If the value is consistent, you can add `--check-requirements=false` to the restore command to skip this configuration check.
- If the value is inconsistent, and you forcibly perform the restore, BR reports a data validation error.

### Why does an error occur when I restore placement rules to a cluster?

Before v6.0.0, BR does not support [placement rules](/placement-rules-in-sql.md). Starting from v6.0.0, BR supports placement rules and introduces a command-line option `--with-tidb-placement-mode=strict/ignore` to control the backup and restore mode of placement rules. With the default value `strict`, BR imports and validates placement rules, but ignores all placement rules when the value is `ignore`.

## Data restore issues

### What should I do to handle the `Io(Os...)` error?

Almost all of these problems are system call errors that occur when TiKV writes data to the disk, for example, `Io(Os {code: 13, kind: PermissionDenied...})` or `Io(Os {code: 2, kind: NotFound...})`.

To address such problems, first check the mounting method and the file system of the backup directory, and try to back up data to another folder or another hard disk.

For example, you might encounter the `Code: 22(invalid argument)` error when backing up data to the network disk built by `samba`.

### What should I do to handle the `rpc error: code = Unavailable desc =...` error occurred in restore?

This error might occur when the capacity of the cluster to restore is insufficient. You can further confirm the cause by checking the monitoring metrics of this cluster or the TiKV log.

To handle this issue, you can try to scale out the cluster resources, reduce the concurrency during restore, and enable the `RATE_LIMIT` option.

### What should I do if the restore fails with the error message `the entry too large, the max entry size is 6291456, the size of data is 7690800`?

You can try to reduce the number of tables to be created in a batch by setting `--ddl-batch-size` to `128` or a smaller value.

When using BR to restore the backup data with the value of [`--ddl-batch-size`](/br/br-batch-create-table.md#how to use) greater than `1`, TiDB writes a DDL job of table creation to the DDL jobs queue that is maintained by TiKV. At this time, the total size of all tables schema sent by TiDB at one time should not exceed 6 MB, because the maximum value of job messages is `6 MB` by default (it is **not recommended** to modify this value. For details, see [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50) and [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)). Therefore, if you set `--ddl-batch-size` to an excessively large value, the schema size of the tables sent by TiDB in a batch at one time exceeds the specified value, which causes BR to report the `entry too large, the max entry size is 6291456, the size of data is 7690800` error.

### Where are the backed up files stored when I use `local` storage?

> **Note:**
>
> If no Network File System (NFS) is mounted to a BR or TiKV node, or if you use external storage that supports Amazon S3, GCS, or Azure Blob Storage protocols, the data backed up by BR is generated at each TiKV node.**Note that this is not the recommended way to deploy BR**, because the backup data are scattered in the local file system of each node. Collecting the backup data might result in data redundancy and operation and maintenance problems. Meanwhile, if you restore data directly before collecting the backup data, you will encounter the `SST file not found` error.

When you use local storage, `backupmeta` is generated on the node where BR is running, and backup files are generated on the Leader nodes of each Region.

### What should I do if the error message `could not read local://...:download sst failed` is returned during data restore?

When you restore data, each node must have access to **all** backup files (SST files). By default, if `local` storage is used, you cannot restore data because the backup files are scattered among different nodes. Therefore, you have to copy the backup file of each TiKV node to the other TiKV nodes. **It is recommended that you store backup data to Amazon S3, Google Cloud Storage (GCS), Azure Blob Storage, or NFS**.

### What should I do to handle the `Permission denied` or `No such file or directory` error, even if I have tried to run `br` using root in vain?

You need to confirm whether TiKV has access to the backup directory. To back up data, confirm whether TiKV has the write permission. To restore data, confirm whether it has the read permission.

During the backup operation, if the storage medium is the local disk or a network file system (NFS), make sure that the user to start `br` and the user to start TiKV are consistent (if `br` and TiKV are on different machines, the users' UIDs must be consistent). Otherwise, the `Permission denied` issue might occur.

Running `br` as the `root` user might fail due to the disk permission, because the backup files (SST files) are saved by TiKV.

> **Note:**
>
> You might encounter the same problem during data restore. When the SST files are read for the first time, the read permission is verified. The execution duration of DDL suggests that there might be a long interval between checking the permission and running `br`. You might receive the error message `Permission denied` after waiting for a long time.

Therefore, it is recommended to check the permission before data restore according to the following steps:

1. Run the Linux command for process query:

    {{< copyable "shell-regular" >}}

    ```bash
    ps aux | grep tikv-server
    ```

    The output is as follows:

    ```shell
    tidb_ouo  9235 10.9  3.8 2019248 622776 ?      Ssl  08:28   1:12 bin/tikv-server --addr 0.0.0.0:20162 --advertise-addr 172.16.6.118:20162 --status-addr 0.0.0.0:20188 --advertise-status-addr 172.16.6.118:20188 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20162 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20162/log/tikv.log
    tidb_ouo  9236  9.8  3.8 2048940 631136 ?      Ssl  08:28   1:05 bin/tikv-server --addr 0.0.0.0:20161 --advertise-addr 172.16.6.118:20161 --status-addr 0.0.0.0:20189 --advertise-status-addr 172.16.6.118:20189 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20161 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20161/log/tikv.log
    ```

    Or you can run the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    ps aux | grep tikv-server | awk '{print $1}'
    ```

    The output is as follows:

    ```shell
    tidb_ouo
    tidb_ouo
    ```

2. Query the startup information of the cluster using the `tiup` command:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster list
    ```

    The output is as follows:

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 br]# tiup cluster list
    Starting component `cluster`: /root/.tiup/components/cluster/v1.5.2/tiup-cluster list
    Name          User      Version  Path                                               PrivateKey
    ----          ----      -------  ----                                               ----------
    tidb_cluster  tidb_ouo  v5.0.2   /root/.tiup/storage/cluster/clusters/tidb_cluster  /root/.tiup/storage/cluster/clusters/tidb_cluster/ssh/id_rsa
    ```

3. Check the permission for the backup directory. For example, `backup` is for backup data storage:

    {{< copyable "shell-regular" >}}

    ```bash
    ls -al backup
    ```

    The output is as follows:

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 user1]# ls -al backup
    total 0
    drwxr-xr-x  2 root root   6 Jun 28 17:48 .
    drwxr-xr-x 11 root root 310 Jul  4 10:35 ..
    ```

    From the output of step 2, you can find that the `tikv-server` instance is started by the user `tidb_ouo`. But the user `tidb_ouo` does not have the write permission for `backup`. Therefore, the backup fails.

### Why are tables in the `mysql` schema not restored?

Starting from BR v5.1.0, when you perform a full backup, BR backs up the **tables in the `mysql` schema**. Before BR v6.2.0, under default configuration, BR only restores user data, but does not restore tables in the **`mysql` schema**.

To restore a table created by the user in the `mysql` schema (not system tables), you can explicitly include the table using [table filters](/table-filter.md#syntax). The following example shows how to restore the `mysql.usertable` table when BR performs a normal restore.

{{< copyable "shell-regular" >}}

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

In the preceding command,

- `-f '*.*'` is used to override the default rules
- `-f '!mysql.*'` instructs BR not to restore tables in `mysql` unless otherwise stated.
- `-f 'mysql.usertable'` indicates that `mysql.usertable` should be restored.

If you only need to restore `mysql.usertable`, run the following command:

{{< copyable "shell-regular" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

Note that even if you configures [table filter](/table-filter.md#syntax), **BR does not restore the following system tables**:

- Statistics tables (`mysql.stat_*`)
- System variable tables (`mysql.tidb`, `mysql.global_variables`)
- [Other system tables](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)

## Other things you may want to know about backup and restore

### What is the size of the backup data? Are there replicas of the backup?

During data backup, backup files are generated on the Leader nodes of each Region. The size of the backup is equal to the data size, with no redundant replicas. Therefore, the total data size is approximately the total number of TiKV data divided by the number of replicas.

However, if you want to restore data from local storage, the number of replicas is equal to that of the TiKV nodes, because each TiKV must have access to all backup files.

### Why is the disk usage shown on the monitoring node inconsistent after backup or restore using BR?

This inconsistency is caused by the fact that the data compression rate used in backup is different from the default rate used in restore. If the checksum succeeds, you can ignore this issue.

### After BR restores the backup data, do I need to execute the `ANALYZE` statement on the table to update the statistics of TiDB on the tables and indexes?

BR does not back up statistics (except in v4.0.9). Therefore, after restoring the backup data, you need to manually execute `ANALYZE TABLE` or wait for TiDB to automatically execute `ANALYZE`.

In v4.0.9, BR backs up statistics by default, which consumes too much memory. To ensure that the backup process goes well, the backup for statistics is disabled by default starting from v4.0.10.

If you do not execute `ANALYZE` on the table, TiDB will fail to select the optimal execution plan due to inaccurate statistics. If query performance is not a key concern, you can ignore `ANALYZE`.

### Can I start multiple restore tasks at the same time to restore the data of a single cluster?

**It is strongly not recommended** to start multiple restore tasks at the same time to restore the data of a single cluster for the following reasons:

- When BR restores data, it modifies some global configurations of PD. Therefore, if you start multiple restore tasks for data restore at the same time, these configurations might be mistakenly overwritten and cause abnormal cluster status.
- BR consumes a lot of cluster resources to restore data, so in fact, running restore tasks in parallel improves the restore speed only to a limited extent.
- There has been no test for running multiple restore tasks in parallel for data restore, so it is not guaranteed to succeed.

### Does BR back up the `SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS` information of a table? Does the restored table have multiple Regions?

Yes. BR backs up the [`SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) information of a table. The data of the restored table is also split into multiple Regions.
