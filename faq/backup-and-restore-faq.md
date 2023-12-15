---
title: 备份与恢复常见问题
summary: 了解备份恢复相关的常见问题以及解决方法。
aliases: ['/docs-cn/dev/br/backup-and-restore-faq/','/zh/tidb/dev/pitr-troubleshoot/','/zh/tidb/dev/pitr-known-issues/']
---

# 备份与恢复常见问题

本文列出了在使用 Backup & Restore (BR) 完成备份与恢复任务时，可能会遇到的问题及相应的解决方法。

如果遇到未包含在此文档且无法解决的问题，可以在 [AskTUG](https://asktug.com/) 社区中提问。

## 当误删除或误更新数据后，如何原地快速恢复？

从 TiDB v6.4.0 引入了完整的 Flashback 功能，可以支持原地快速恢复 GC 时间内的数据到指定时间点。在误操作场景下，推荐使用 Flashback 来恢复数据，具体可以参考 [Flashback 集群](/sql-statements/sql-statement-flashback-to-timestamp.md) 和 [Flashback 数据库](/sql-statements/sql-statement-flashback-database.md)语法。

## 在 TiDB v5.4.0 及后续版本中，当在有负载的集群进行备份时，备份速度为什么会变得很慢？

从 TiDB v5.4.0 起，TiKV 的备份新增了自动调节功能。对于 v5.4.0 及以上版本，该功能会默认开启。当集群负载较高时，该功能会自动限制备份任务使用的资源，从而减少备份对在线集群的性能造成的影响。如需了解关于自动调节功能的更多信息，请参见[自动调节](/br/br-auto-tune.md)。

TiKV 支持[动态配置](/tikv-control.md#动态修改-tikv-的配置)自动调节功能。因此，在开启或关闭该功能时，你不需要重启集群。以下为该功能的具体使用方法：

- 关闭功能：把 TiKV 配置项 [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-从-v54-版本开始引入) 设置为 `false`。
- 开启功能：把 `backup.enable-auto-tune` 设置为 `true`。对于 v5.3.x 版本的集群，当 TiDB 升级到 v5.4.0 及以上版本后，自动调节功能会默认关闭。这时，你可以通过该方式手动开启此功能。

如需了解通过 `tikv-ctl` 在线修改自动调节功能的命令行，请参阅[自动调节功能的使用方法](/br/br-auto-tune.md#使用方法)。

另外，自动调节功能减少了进行备份任务时默认使用的工作线程数量（详见 [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)）。因此，你通过 Grafana 监控面板看到的备份速度、CPU 使用率、I/O 资源利用率都会小于 v5.4 之前的版本。在 v5.4.0 之前的版本中，`backup.num-threads` 的默认值为 `CPU * 0.75`，即处理备份任务的工作线程数量占了 75% 的逻辑 CPU，最大值为 `32`；在 v5.4.0 及之后的版本中，该配置项的默认值为 `CPU * 0.5`，最大值为 `8`。

在离线备份场景中，你也可以使用 `tikv-ctl` 把 `backup.num-threads` 修改为更大的数字，从而提升备份任务的速度。

## PITR 问题

### [PITR 功能](/br/br-pitr-guide.md)和 [flashback 集群](/sql-statements/sql-statement-flashback-to-timestamp.md)有什么区别?

从使用场景角度来看，PITR 通常用于在集群完全停止服务或数据损坏且无法使用其他方案恢复时，将集群的数据恢复到指定的时间点。使用 PITR 时，你需要通过一个新的集群来完成数据恢复。而 flashback 集群则通常用于发生误操作或其他因素导致的数据错误时，将集群的数据恢复到数据错误发生前的最近时间点。

在大多数情况下，因为 flashback 具有更短的 RPO（接近零）和 RTO，flashback 比 PITR 更适合由于人为错误导致的数据错误场景。但当集群完全不可用时，flashback 集群功能也无法运行，此时 PITR 是恢复集群的唯一方案。因此，相比于 flashback，虽然 PITR 的 RPO（最长 5 分钟）和 RTO 时间较长，但 PITR 是制定数据库灾难恢复策略时必须考虑的数据安全基础。

### 上游数据库使用 TiDB Lightning 物理导入模式导入数据时，为什么无法使用日志备份功能？

目前日志备份功能还没有完全适配 TiDB Lightning，导致 TiDB Lightning 物理导入模式导入的数据无法备份到日志中。

在创建日志备份任务的上游集群中，请尽量避免使用 TiDB Lightning 物理导入模式导入数据。可以选择使用 TiDB Lightning 逻辑导入模式导入数据。若确实需要使用物理导入模式，可在导入完成之后做一次快照备份操作，这样，PITR 就可以恢复到快照备份之后的时间点。

### 集群已经恢复了网络分区故障，为什么日志备份任务进度 checkpoint 仍然不推进？

Issue 链接：[#13126](https://github.com/tikv/tikv/issues/13126)

在集群出现网络分区故障后，备份任务难以继续备份日志，并且在超过一定的重试时间后，任务会被置为 `ERROR` 状态。此时备份任务已经停止，需要手动执行 `br log resume` 命令来恢复日志备份任务。

### 在使用 `br restore point` 命令恢复下游集群后，TiFlash 引擎数据没有恢复？

PITR 目前不支持在恢复阶段直接将数据写入 TiFlash，在数据恢复完成后，br 会执行 `ALTER TABLE table_name SET TIFLASH REPLICA ***`，因此 TiFlash 副本在 PITR 完成恢复之后并不能马上可用，而是需要等待一段时间从 TiKV 节点同步数据。要查看同步进度，可以查询 `INFORMATION_SCHEMA.tiflash_replica` 表中的 `progress` 信息。

### 日志备份任务的 `status` 变为 `ERROR`，该如何处理？

在运行日志备份过程中，遇到错误后经过重试也无法恢复的故障场景，任务会被设置为 `ERROR` 状态，如：

``` shell
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

此时，你需要根据错误提示来确认故障的原因并恢复故障。确认故障恢复之后，可执行下面的命令来恢复备份任务：

```shell
br log resume --task-name=task1 --pd x.x.x.x:2379
```

备份任务恢复后，再次查询 `br log status`，任务状态变为正常，备份任务继续执行。

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

> **注意：**
>
> 由于此功能会备份集群的多版本数据，当任务发生错误且状态变更为 `ERROR` 时，同时会将当前任务的备份进度点的数据设为一个 `safe point`，`safe point` 的数据将保证 24 小时不被 GC 掉。所以，当任务恢复之后，会从上一个备份点继续备份日志。如果任务失败时间超过 24 小时，前一次备份进度点的数据就已经 GC，此时恢复任务操作会提示失败。这种场景下，只能执行 `br log stop` 命令先停止本次任务，然后重新开启新的备份任务。

### 执行 `br log resume` 命令恢复处于暂停状态的任务时报 `ErrBackupGCSafepointExceeded` 错误，该如何处理？

```shell
Error: failed to check gc safePoint, checkpoint ts 433177834291200000: GC safepoint 433193092308795392 exceed TS 433177834291200000: [BR:Backup:ErrBackupGCSafepointExceeded]backup GC safepoint exceeded
```

暂停日志备份任务后，备份程序为了防止生成变更日志的 MVCC 数据被 GC，暂停任务程序会自动将当前备份点 checkpoint 设置为 service safepoint，允许保留最近 24 小时内的 MVCC 数据。当超过 24 小时后，备份点 checkpoint 的 MVCC 数据已经被 GC，此时程序会拒绝恢复备份任务。

此场景的处理办法是：先执行 `br log stop` 命令来删除当前的任务，然后执行 `br log start` 重新创建新的日志备份任务，同时做一个全量备份，便于后续做 PITR 恢复操作。

## 功能兼容性问题

### 为什么 BR 恢复的数据无法同步到 TiCDC / Drainer 的上游集群？

- **BR 恢复的数据无法被同步到下游**，因为恢复时 BR 直接导入 SST 文件，而下游集群目前没有办法获得上游的 SST 文件。
- 在 4.0.3 版本之前，恢复时产生的 DDL jobs 还可能会让 TiCDC / Drainer 执行异常的 DDL。所以，如果一定要在 TiCDC / Drainer 的上游集群执行恢复，请将 BR 恢复的所有表加入 TiCDC / Drainer 的阻止名单。

TiCDC 可以通过配置项中的 [`filter.rules`](https://github.com/pingcap/tiflow/blob/7c3c2336f98153326912f3cf6ea2fbb7bcc4a20c/cmd/changefeed.toml#L16) 项完成，Drainer 则可以通过 [`syncer.ignore-table`](/tidb-binlog/tidb-binlog-configuration-file.md#ignore-table) 完成。

### 恢复时为什么会报 `new_collation_enabled` 不匹配？

从 TiDB v6.0.0 版本开始，[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 配置项的默认值由 `false` 改为 `true`。BR 会备份上游集群的 `mysql.tidb` 表中的 `new_collation_enabled` 配置项。当上下游集群的此项配置相同时，BR 才会将上游集群的备份数据安全地恢复到下游集群中。若上下游的该配置不相同，BR 会拒绝恢复，并报此配置项不匹配的错误。

如果需要将旧版本的备份数据恢复到 TiDB v6.0.0 或更新版本的 TiDB 集群中，你需要检查上下游集群中的该配置项是否相同：

- 若该配置项相同，则可在恢复命令中添加 `--check-requirements=false` 以跳过此项配置检查。
- 若该配置项不相同，且进行强行恢复，BR 会报数据校验错误。

### 恢复 Placement Rule 到集群时为什么会报错？

BR 在 v6.0.0 之前不支持[放置规则](/placement-rules-in-sql.md)，在 v6.0.0 及以上版本开始支持并提供了命令行选项 `--with-tidb-placement-mode=strict/ignore` 来控制放置规则的导入模式。默认值为 `strict`，代表导入并检查放置规则，当`--with-tidb-placement-mode` 设置为 `ignore` 时，BR 会忽略所有的放置规则。

## 进行数据恢复的问题

### 使用 BR 时遇到错误信息 `Io(Os...)`，该如何处理？

这类问题几乎都是 TiKV 在写盘的时候遇到的系统调用错误。例如遇到 `Io(Os { code: 13, kind: PermissionDenied...})` 或者 `Io(Os { code: 2, kind: NotFound...})`。

首先检查备份目录的挂载方式和文件系统，尝试备份到其它文件夹或者硬盘。

目前已知备份到 samba 搭建的网盘时可能会遇到 `Code: 22(invalid argument)` 错误。

### 恢复时遇到错误信息 `rpc error: code = Unavailable desc =...`，该如何处理？

该问题一般是因为恢复数据的时候，恢复集群的性能不足导致的。可以从恢复集群的监控或者 TiKV 日志来辅助确认。

要解决这类问题，可以尝试扩大集群资源，以及调小恢复时的并发度 (concurrency)，打开限速 (ratelimit) 设置。

### 恢复备份数据时，BR 会报错 `entry too large, the max entry size is 6291456, the size of data is 7690800`

你可以尝试降低并发批量建表的大小，将 `--ddl-batch-size` 设置为 `128` 或者更小的值。

在 [`--ddl-batch-size`](/br/br-batch-create-table.md#使用方法) 的值大于 `1` 的情况下，使用 BR 恢复数据时，TiDB 会把执行创建表任务的 DDL job 队列写到 TiKV 上。由于 TiDB 能够一次性发送的 job message 的最大值默认为 `6 MB`（**不建议**修改此值，具体内容，参考 [txn-entry-size-limit](/tidb-configuration-file.md#txn-entry-size-limit-从-v50-版本开始引入) 和 [raft-entry-max-size](/tikv-configuration-file.md#raft-entry-max-size)），TiDB 单次发送的所有表的 schema 大小总和也不应该超过 6 MB。因此，如果你设置的 `--ddl-batch-size` 的值过大，TiDB 单次发送的批量表的 schema 大小就会超出规定值，从而导致 BR 报 `entry too large, the max entry size is 6291456, the size of data is 7690800` 错误。

### 使用 local storage 的时候，备份的文件会存在哪里？

> **注意：**
>
> 如果没有挂载 NFS 到 br 工具或 TiKV 节点，或者使用了支持 S3、GCS 或 Azure Blob Storage 协议的远端存储，那么 br 工具备份的数据会在各个 TiKV 节点生成。**注意这不是推荐的备份和恢复使用方式**，因为备份数据会分散在各个节点的本地文件系统中，聚集这些备份数据可能会造成数据冗余和运维上的麻烦，而且在不聚集这些数据便直接恢复的时候会遇到 `SST file not found` 报错。

在使用 local storage 的时候，会在运行 br 命令行工具的节点生成 `backupmeta`，在各个 Region 的 Leader 所在 TiKV 节点生成备份文件。

### 恢复的时候，报错 `could not read local://...:download sst failed`，该如何处理？

在恢复的时候，每个节点都必须能够访问到**所有**的备份文件 (SST files)。默认情况下，假如使用 local storage，备份文件会分散在各个节点中，此时是无法直接恢复的，必须将每个 TiKV 节点的备份文件拷贝到其它所有 TiKV 节点才能恢复。 所以**建议使用 S3/GCS/Azure Blob Storage/NFS 作为备份存储**。

### 遇到 Permission denied 或者 No such file or directory 错误，即使用 root 运行 br 命令行工具也无法解决，该如何处理？

需要确认 TiKV 是否有访问备份目录的权限。如果是备份，确认是否有写权限；如果是恢复，确认是否有读权限。

在进行备份操作时，如果使用本地磁盘或 NFS 作为存储介质，请确保执行 br 命令行工具的用户和启动 TiKV 的用户相同（如果 br 工具和 TiKV 位于不同的机器，则需要用户的 UID 相同），否则备份可能会出现该问题。

使用 root 运行 br 命令行工具仍旧有可能会因为磁盘权限而失败，因为备份文件 (SST) 的保存是由 TiKV 执行的。

> **注意：**
>
> 在恢复的时候也可能遇到同样的问题。
>
> 使用 br 命令行工具进行数据的恢复时，检验读权限的时机是在第一次读取 SST 文件时，考虑到执行 DDL 的耗时，这个时刻可能会离开始运行 br 命令行工具的时间很远。这样可能会出现等了很长时间之后遇到 Permission denied 错误失败的情况。
>
> 因此，最好在恢复前提前检查权限。

你可以按照如下步骤进行权限检查：

1. 执行 Linux 原生的进程查询命令

    {{< copyable "shell-regular" >}}

    ```bash
    ps aux | grep tikv-server
    ```

    命令输出示例如下:

    ```shell
    tidb_ouo  9235 10.9  3.8 2019248 622776 ?      Ssl  08:28   1:12 bin/tikv-server --addr 0.0.0.0:20162 --advertise-addr 172.16.6.118:20162 --status-addr 0.0.0.0:20188 --advertise-status-addr 172.16.6.118:20188 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20162 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20162/log/tikv.log
    tidb_ouo  9236  9.8  3.8 2048940 631136 ?      Ssl  08:28   1:05 bin/tikv-server --addr 0.0.0.0:20161 --advertise-addr 172.16.6.118:20161 --status-addr 0.0.0.0:20189 --advertise-status-addr 172.16.6.118:20189 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20161 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20161/log/tikv.log
    ```

    或者执行以下命令：

    {{< copyable "shell-regular" >}}

    ```bash
    ps aux | grep tikv-server | awk '{print $1}'
    ```

    命令输出示例如下:

    ```shell
    tidb_ouo
    tidb_ouo
    ```

2. 使用 TiUP 命令查询集群的启动信息

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster list
    ```

    命令输出示例如下：

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 br]# tiup cluster list
    Starting component `cluster`: /root/.tiup/components/cluster/v1.5.2/tiup-cluster list
    Name          User      Version  Path                                               PrivateKey
    ----          ----      -------  ----                                               ----------
    tidb_cluster  tidb_ouo  v5.0.2   /root/.tiup/storage/cluster/clusters/tidb_cluster  /root/.tiup/storage/cluster/clusters/tidb_cluster/ssh/id_rsa
    ```

3. 检查备份目录的权限，例如 `backup` 目录是备份数据存储目录。命令示例如下：

    {{< copyable "shell-regular" >}}

    ```bash
    ls -al backup
    ```

    命令输出示例如下：

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 user1]# ls -al backup
    total 0
    drwxr-xr-x  2 root root   6 Jun 28 17:48 .
    drwxr-xr-x 11 root root 310 Jul  4 10:35 ..
    ```

    由以上命令输出结果可知，`tikv-server` 实例由用户 `tidb_ouo` 启动，但该账号没有 `backup` 目录的写入权限，所以备份失败。

### 恢复集群的时候，在 MySQL 下的业务表为什么没有恢复？

自 `br` v5.1.0 开始，全量备份会备份 **mysql schema 下的表**。`br` v6.2.0 以前的版本，在默认设置不会恢复 **mysql schema 下的表**。

如果需要恢复 `mysql` 下的用户创建的表（非系统表），可以通过 [table filter](/table-filter.md#表库过滤语法) 来显式地包含目标表。以下示例中命令会在执行正常的恢复的同时恢复 `mysql.usertable`。

{{< copyable "shell-regular" >}}

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

在上面的命令中，

- `-f '*.*'` 用于覆盖掉默认的规则。
- `-f '!mysql.*'` 指示 BR 不要恢复 `mysql` 中的表，除非另有指定。
- `-f 'mysql.usertable'` 则指定需要恢复 `mysql.usertable`。

如果只需要恢复 `mysql.usertable`，而无需恢复其他表，可以使用以下命令：

{{< copyable "shell-regular" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

此外请注意，即使设置了 [table filter](/table-filter.md#表库过滤语法)，**BR 也不会恢复以下系统表**：

- 统计信息表（`mysql.stat_*`）
- 系统变量表（`mysql.tidb`、`mysql.global_variables`）
- [其他系统表](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)

## 备份恢复功能相关知识

### 备份数据有多大，备份会有副本吗？

备份的时候仅仅在每个 Region 的 Leader 处生成该 Region 的备份文件。因此备份的大小等于数据大小，不会有多余的副本数据。所以最终的总大小大约是 TiKV 数据总量除以副本数。

但是假如想要从本地恢复数据，因为每个 TiKV 都必须要能访问到所有备份文件，在最终恢复的时候会有等同于恢复时 TiKV 节点数量的副本。

### BR 备份恢复后，为什么监控显示磁盘使用空间不一致？

这个情况多数是因为备份时集群的数据压缩比率和恢复时的默认值不一致导致的，只要恢复的 checksum 阶段顺利通过，可以忽略这个问题，不影响正常使用。

### 使用 BR 恢复数据后是否需要对表执行 `ANALYZE` 以更新 TiDB 在表和索引上留下的统计信息？

BR 不会备份统计信息（v4.0.9 除外）。所以在恢复存档后需要手动执行 `ANALYZE TABLE` 或等待 TiDB 自动进行 `ANALYZE`。

BR v4.0.9 备份统计信息使 br 工具消耗过多内存，为保证备份过程正常，从 v4.0.10 开始默认关闭备份统计信息的功能。

如果不对表执行 `ANALYZE`，TiDB 会因统计信息不准确而选不中最优化的执行计划。如果查询性能不是重点关注项，可以忽略 `ANALYZE`。

### 可以同时启动多个恢复任务对单个集群进行恢复吗？

**强烈不建议**在单个集群中同时启动多个恢复任务进行数据恢复，原因如下：

- BR 在恢复数据时，会修改 PD 的一些全局配置。如果同时使用多个 BR 命令进行恢复，这些配置可能会被错误地覆写，导致集群状态异常。
- 因为 BR 在恢复数据的时候会占用大量集群资源，事实上并行恢复能获得的速度提升也非常有限。
- 多个恢复任务同时进行的场景没有经过测试，无法保证成功。

### BR 会备份表的 `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS` 信息吗？恢复出来的表会有多个 Region 吗？

会，BR 会备份表的 [`SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 信息，并恢复成多个 Region。
