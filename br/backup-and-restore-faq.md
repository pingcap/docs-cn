---
title: Backup & Restore FAQs
summary: Learn about Frequently Asked Questions (FAQs) and the solutions of BR.
aliases: ['/docs/dev/br/backup-and-restore-faq/']
---

# Backup & Restore FAQs

This document lists the frequently asked questions (FAQs) and the solutions about Backup & Restore (BR).

## In TiDB v5.4.0 and later versions, when backup tasks are performed on the cluster under high workload, why does the speed of backup tasks become slow?

Starting from TiDB v5.4.0, BR introduces the auto-tune feature for backup tasks. For clusters in v5.4.0 or later versions, this feature is enabled by default. When the cluster workload is heavy, the feature limits the resources used by backup tasks to reduce the impact on the online cluster. For more information, refer to [BR Auto-Tune](/br/br-auto-tune.md).

TiKV supports [dynamically configuring](/tikv-control.md#modify-the-tikv-configuration-dynamically) the auto-tune feature. You can enable or disable the feature by the following methods without restarting your cluster:

- Disable auto-tune: Set the TiKV configuration item [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540) to `false`.
- Enable auto-tune: Set `backup.enable-auto-tune` to `true`. For clusters upgraded from v5.3.x to v5.4.0 or later versions, the auto-tune feature is disabled by default. You need to manually enable it.

To use `tikv-ctl` to enable or disable auto-tune, refer to [Use auto-tune](/br/br-auto-tune.md#use-auto-tune).

In addition, auto-tune reduces the default number of threads used by backup tasks. For details, see `backup.num-threads`](/tikv-configuration-file.md#num-threads-1). Therefore, on the Grafana Dashboard, the speed, CPU usage, and I/O resource utilization used by backup tasks are lower than those of versions earlier than v5.4.0. Before v5.4.0, the default value of `backup.num-threads` was `CPU * 0.75`, that is, the number of threads used by backup tasks makes up 75% of the logical CPU cores. The maximum value of it was `32`. Starting from v5.4.0, the default value of this configuration item is `CPU * 0.5`, and its maximum value is `8`.

When you perform backup tasks on an offline cluster, to speed up the backup, you can modify the value of `backup.num-threads` to a larger number using `tikv-ctl`.

## What should I do if the error message `could not read local://...:download sst failed` is returned during data restoration?

When you restore data, each node must have access to **all** backup files (SST files). By default, if `local` storage is used, you cannot restore data because the backup files are scattered among different nodes. Therefore, you have to copy the backup file of each TiKV node to the other TiKV nodes.

It is recommended that you mount an NFS disk as a backup disk during backup. For details, see [Back up a single table to a network disk](/br/backup-and-restore-use-cases.md#back-up-a-single-table-to-a-network-disk-recommended-for-production-environments).

## How much impact does a backup operation have on the cluster?

For TiDB v5.4.0 or later versions, BR not only reduces the default CPU utilization used by backup tasks, but also introduces the [BR Auto-tune](/br/br-auto-tune.md) feature to limit the resources used by backup tasks in the cluster with heavy workloads. Therefore, when you use the default configuration for backup tasks in a v5.4.0 cluster with heavy workloads, the impact of the tasks on the cluster performance is significantly less than that on the clusters earlier than v5.4.0.

The following is an internal test on a single node. The test results show that when you use the default configuration of v5.4.0 and v5.3.0 in the **full-speed backup** scenario, the impact of backup using BR on cluster performance is quite different. The detailed test results are as follows:

- When BR uses the default configuration of v5.3.0, the QPS of write-only workload is reduced by 75%.
- When BR uses the default configuration of v5.4.0, the QPS for the same workload is reduced by 25%. However, when this configuration is used, the duration of backup tasks using BR becomes correspondingly longer. The time required is 1.7 times that of the v5.3.0 configuration.

You can use either of the following solutions to manually control the impact of backup tasks on cluster performance. Note that these methods reduce the impact of backup tasks on the cluster, but they also reduce the speed of backup tasks.

- Use the `--ratelimit` parameter to limit the speed of backup tasks. Note that this parameter limits the speed of **saving backup files to external storage**. When calculating the total size of backup files, use the `backup data size(after compressed)` in the backup log as a benchmark.
- Adjust the TiKV configuration item [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) to limit the number of threads used by backup tasks. When BR uses no more than `8` threads for backup tasks, and the total CPU utilization of the cluster does not exceed 60%, the backup tasks have little impact on the cluster, regardless of the read and write workload.

## Does BR back up system tables? During data restoration, do they raise conflicts?

Before v5.1.0, BR filters out data from the system schemas `mysql.*` during the backup. Since v5.1.0, BR **backs up** all data by default, including the system schemas `mysql.*`.

The technical implementation of restoring the system tables in `mysql.*` is not complete yet, so the tables in the system schema `mysql` are **not restored** by default, which means no conflicts will be raised. For more details, refer to [Restore tables in the `mysql` schema (experimental)](/br/br-usage-restore.md#restore-tables-in-the-mysql-schema).

## What should I do to handle the `Permission denied` or `No such file or directory` error, even if I have tried to run BR using root in vain?

You need to confirm whether TiKV has access to the backup directory. To back up data, confirm whether TiKV has the write permission. To restore data, confirm whether it has the read permission.

During the backup operation, if the storage medium is the local disk or a network file system (NFS), make sure that the user to start BR and the user to start TiKV are consistent (if BR and TiKV are on different machines, the users' UIDs must be consistent). Otherwise, the `Permission denied` issue might occur.

Running BR with the root access might fail due to the disk permission, because the backup files (SST files) are saved by TiKV.

> **Note:**
>
> You might encounter the same problem during data restoration. When the SST files are read for the first time, the read permission is verified. The execution duration of DDL suggests that there might be a long interval between checking the permission and running BR. You might receive the error message `Permission denied` after waiting for a long time.
>
> Therefore, it is recommended to check the permission before data restore according to the following steps:

1. Run the Linux-native command for process query:

    {{< copyable "shell-regular" >}}

    ```bash
    ps aux | grep tikv-server
    ```

    The output of the above command:

    ```shell
    tidb_ouo  9235 10.9  3.8 2019248 622776 ?      Ssl  08:28   1:12 bin/tikv-server --addr 0.0.0.0:20162 --advertise-addr 172.16.6.118:20162 --status-addr 0.0.0.0:20188 --advertise-status-addr 172.16.6.118:20188 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20162 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20162/log/tikv.log
    tidb_ouo  9236  9.8  3.8 2048940 631136 ?      Ssl  08:28   1:05 bin/tikv-server --addr 0.0.0.0:20161 --advertise-addr 172.16.6.118:20161 --status-addr 0.0.0.0:20189 --advertise-status-addr 172.16.6.118:20189 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20161 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20161/log/tikv.log
    ```

    Or you can run the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    ps aux | grep tikv-server | awk '{print $1}'
    ```

    The output of the above command:

    ```shell
    tidb_ouo
    tidb_ouo
    ```

2. Query the startup information of the cluster using the TiUP command:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster list
    ```

    The output of the above command:

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

    The output of the above command:

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 user1]# ls -al backup
    total 0
    drwxr-xr-x  2 root root   6 Jun 28 17:48 .
    drwxr-xr-x 11 root root 310 Jul  4 10:35 ..
    ```

    From the above output, you can find that the `tikv-server` instance is started by the user `tidb_ouo`. But the user `tidb_ouo` does not have the write permission for `backup`. Therefore, the backup fails.

## What should I do to handle the `Io(Os...)` error?

Almost all of these problems are system call errors that occur when TiKV writes data to the disk, for example, `Io(Os {code: 13, kind: PermissionDenied...})` or `Io(Os {code: 2, kind: NotFound...})`.

To address such problems, first check the mounting method and the file system of the backup directory, and try to back up data to another folder or another hard disk.

For example, you might encounter the `Code: 22(invalid argument)` error when backing up data to the network disk built by `samba`.

## What should I do to handle the `rpc error: code = Unavailable desc =...` error occurred in BR?

This error might occur when the capacity of the cluster to restore (using BR) is insufficient. You can further confirm the cause by checking the monitoring metrics of this cluster or the TiKV log.

To handle this issue, you can try to scale out the cluster resources, reduce the concurrency during restoration, and enable the `RATE_LIMIT` option.

## Where are the backed up files stored when I use `local` storage?

When you use `local` storage, `backupmeta` is generated on the node where BR is running, and backup files are generated on the Leader nodes of each Region.

## How about the size of the backup data? Are there replicas of the backup?

During data backup, backup files are generated on the Leader nodes of each Region. The size of the backup is equal to the data size, with no redundant replicas. Therefore, the total data size is approximately the total number of TiKV data divided by the number of replicas.

However, if you want to restore data from local storage, the number of replicas is equal to that of the TiKV nodes, because each TiKV must have access to all backup files.

## What should I do when BR restores data to the upstream cluster of TiCDC/Drainer?

+ **The data restored using BR cannot be replicated to the downstream**. This is because BR directly imports SST files but the downstream cluster currently cannot obtain these files from the upstream.

+ Before v4.0.3, DDL jobs generated during the BR restore might cause unexpected DDL executions in TiCDC/Drainer. Therefore, if you need to perform restore on the upstream cluster of TiCDC/Drainer, add all tables restored using BR to the TiCDC/Drainer block list.

You can use [`filter.rules`](https://github.com/pingcap/tiflow/blob/7c3c2336f98153326912f3cf6ea2fbb7bcc4a20c/cmd/changefeed.toml#L16) to configure the block list for TiCDC and use [`syncer.ignore-table`](/tidb-binlog/tidb-binlog-configuration-file.md#ignore-table) to configure the block list for Drainer.

## Does BR back up the `SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS` information of a table? Does the restored table have multiple Regions?

Yes. BR backs up the [`SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) information of a table. The data of the restored table is also split into multiple Regions.

## What should I do if the restore fails with the error message `the entry too large, the max entry size is 6291456, the size of data is 7690800`?

You can try to reduce the number of tables to be created in a batch by setting `--ddl-batch-size` to `128` or a smaller value.

When using BR to restore the backup data with the value of [`--ddl-batch-size`](/br/br-batch-create-table.md#how to use) greater than `1`, TiDB writes a DDL job of table creation to the DDL jobs queue that is maintained by TiKV. At this time, the total size of all tables schema sent by TiDB at one time should not exceed 6 MB, because the maximum value of job messages is `6 MB` by default (it is **not recommended** to modify this value. For details, see [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50) and [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)). Therefore, if you set `--ddl-batch-size` to an excessively large value, the schema size of the tables sent by TiDB in a batch at one time exceeds the specified value, which causes BR to report the `entry too large, the max entry size is 6291456, the size of data is 7690800` error.

## Why is the `region is unavailable` error reported for a SQL query after I use BR to restore the backup data?

If the cluster backed up using BR has TiFlash, `TableInfo` stores the TiFlash information when BR restores the backup data. If the cluster to be restored does not have TiFlash, the `region is unavailable` error is reported.

## Does BR support in-place full restoration of some historical backup?

No. BR does not support in-place full restoration of some historical backup.

## How can I use BR for incremental backup in the Kubernetes environment?

To get the `commitTs` field of the last BR backup, run the `kubectl -n ${namespace} get bk ${name}` command using kubectl. You can use the content of this field as `--lastbackupts`.

## How can I convert BR backupTS to Unix time?

BR `backupTS` defaults to the latest timestamp obtained from PD before the backup starts. You can use `pd-ctl tso timestamp` to parse the timestamp to obtain an accurate value, or use `backupTS >> 18` to quickly obtain an estimated value.

## After BR restores the backup data, do I need to execute the `ANALYZE` statement on the table to update the statistics of TiDB on the tables and indexes?

BR does not back up statistics (except in v4.0.9). Therefore, after restoring the backup data, you need to manually execute `ANALYZE TABLE` or wait for TiDB to automatically execute `ANALYZE`.

In v4.0.9, BR backs up statistics by default, which consumes too much memory. To ensure that the backup process goes well, the backup for statistics is disabled by default starting from v4.0.10.

If you do not execute `ANALYZE` on the table, TiDB will fail to select the optimized execution plan due to inaccurate statistics. If query performance is not a key concern, you can ignore `ANALYZE`.

## Can I use multiple BR processes at the same time to restore the data of a single cluster?

**It is strongly not recommended** to use multiple BR processes at the same time to restore the data of a single cluster for the following reasons:

+ When BR restores data, it modifies some global configurations of PD. Therefore, if you use multiple BR processes for data restore at the same time, these configurations might be mistakenly overwritten and cause abnormal cluster status.
+ BR consumes a lot of cluster resources to restore data, so in fact, running BR processes in parallel improves the restore speed only to a limited extent.
+ There has been no test for running multiple BR processes in parallel for data restore, so it is not guaranteed to succeed.

## What should I do if the backup log reports `key locked Error`?

Error message in the log: `log - ["backup occur kv error"][error="{\"KvError\":{\"locked\":`

If a key is locked during the backup process, BR tries to resolve the lock. If this error occurs only occasionally, the correctness of the backup is not affected.

## What should I do if a backup operation fails?

Error message in the log: `log - Error: msg:"Io(Custom { kind: AlreadyExists, error: \"[5_5359_42_123_default.sst] is already exists in /dir/backup_local/\" })"`

If a backup operation fails and the preceding message occurs, perform one of the following operations and then start the backup again:

- Change the directory for the backup. For example, change `/dir/backup_local/` to `/dir/backup-2020-01-01/`.
- Delete the backup directories of all TiKV nodes and BR nodes.

## What should I do if the disk usage shown on the monitoring node is inconsistent after BR backup or restoration?

This inconsistency is caused by the fact that the data compression rate used in backup is different from the default rate used in restoration. If the checksum succeeds, you can ignore this issue.

## Why does an error occur when I restore placement rules to a cluster?

Before v6.0.0, BR does not support [placement rules](/placement-rules-in-sql.md). Starting from v6.0.0, BR supports placement rules and introduces a command-line option `--with-tidb-placement-mode=strict/ignore` to control the backup and restore mode of placement rules. With the default value `strict`, BR imports and validates placement rules, but ignores all placement rules when the value is `ignore`.

## Why does BR report `new_collations_enabled_on_first_bootstrap` mismatch?

Since TiDB v6.0.0, the default value of [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) has changed from `false` to `true`. BR backs up the `new_collations_enabled_on_first_bootstrap` configuration of the upstream cluster and then checks whether the value of this configuration is consistent between the upstream and downstream clusters. If the value is consistent, BR safely restores the data backed up in the upstream cluster to the downstream cluster. If the value is inconsistent, BR does not perform the data restore and reports an error.

Suppose that you have backed up the data in a TiDB cluster of an earlier version of v6.0.0, and you want to restore this data to a TiDB cluster of v6.0.0 or later versions. In this situation, you need to manually check whether the value of `new_collations_enabled_on_first_bootstrap` is consistent between the upstream and downstream clusters:

- If the value is consistent, you can add `--check-requirements=false` to the restoration command to skip this configuration check.
- If the value is inconsistent, and you forcibly perform the restoration, BR reports a data validation error.
