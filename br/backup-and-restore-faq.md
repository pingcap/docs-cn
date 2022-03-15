---
title: Backup & Restore 常见问题
summary: BR 相关的常见问题以及解决方法。
aliases: ['/docs-cn/dev/br/backup-and-restore-faq/']
---

# Backup & Restore 常见问题

本文列出了在使用 Backup & Restore (BR) 时，可能会遇到的问题及相应的解决方法。

如果遇到未包含在此文档且无法解决的问题，可以在 [AskTUG](https://asktug.com/) 社区中提问。

## 在 TiDB v5.4.0 及后续版本中，当在有负载的集群进行备份时，备份速度为什么会变得很慢？

从 TiDB v5.4.0 起，TiKV 的备份新增了自动调节功能。对于 v5.4.0 及以上版本，该功能会默认开启。当集群负载较高时，该功能会自动限制备份任务使用的资源，从而减少备份对在线集群的性能造成的影响。如需了解关于自动调节功能的更多信息，请参见[自动调节](/br/br-auto-tune.md)。

TiKV 支持[动态配置](/tikv-control.md#动态修改-tikv-的配置)自动调节功能。因此，在开启或关闭该功能时，你不需要重启集群。以下为该功能的具体使用方法：

- 关闭功能：把 TiKV 配置项 [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-从-v54-版本开始引入) 设置为 `false`。
- 开启功能：把 `backup.enable-auto-tune` 设置为 `true`。对于 v5.3.x 版本的集群，当 TiDB 升级到 v5.4.0 及以上版本后，自动调节功能会默认关闭。这时，你可以通过该方式手动开启此功能。

如需了解通过 `tikv-ctl` 在线修改自动调节功能的命令行，请参阅[自动调节功能的使用方法](/br/br-auto-tune.md#使用方法)。

另外，该功能也降低了进行备份任务时默认使用的工作线程数量（详见 [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)）。因此，你通过 Grafana 监控面板看到的备份速度、CPU 使用率、I/O 资源利用率都会小于 v5.4 之前的版本。在 v5.4 之前的版本中，`backup.num-threads` 的默认值为 CPU * 0.75，即处理备份任务的工作线程数量占了 75% 的逻辑 CPU，最大值为 `32`；在 v5.4 及之后的版本中，该配置项的默认值为 CPU * 0.5，最大值为 `8`。

在离线备份场景中，你也可以使用 `tikv-ctl` 把 `backup.num-threads` 修改为更大的数字，从而提升备份任务的速度。

## 恢复的时候，报错 `could not read local://...:download sst failed`，该如何处理？

在恢复的时候，每个节点都必须能够访问到**所有**的备份文件 (SST files)，默认情况下，假如使用 local storage，备份文件会分散在各个节点中，此时是无法直接恢复的，必须将每个 TiKV 节点的备份文件拷贝到其它所有 TiKV 节点才能恢复。

建议在备份的时候挂载一块 NFS 网盘作为备份盘，详见[将单表数据备份到网络盘](/br/backup-and-restore-use-cases.md#将单表数据备份到网络盘推荐生产环境使用)。

## BR 备份时，对集群影响多大？

对于 TiDB v5.4.0 及以后的版本，BR 不仅调低了备份任务会使用的默认 CPU 使用率，还引入了自动调节功能。开启该功能后，当在集群高负载的场景下进行备份时，BR 能够自动限制备份任务使用的资源，从而限制 BR 备份的速度。因此，在 v5.4.0 高负载集群中使用默认配置进行备份时，备份任务对其集群性能的影响会显著小于 v5.4.0 之前的版本。有关自动调节功能的具体内容，请参阅 [BR 自动调节](/br/br-auto-tune.md)。

以下为针对内部的一个单节点进行的内部测试。通过测试结果，可以确定在**全速备份**场景下使用 v5.4.0 版本及其前期版本的默认配置时，BR 备份对集群性能的影响有较大区别。具体测试结果如下：

- 使用 v5.3.0 的默认配置时，纯写负载的 QPS 降低了 75%；
- 使用 v5.4.0 的默认配置时，相同负载的 QPS 降低了 25%。不过，使用该配置时，BR 备份任务的耗时也相应得拉慢，其所需时间为 v5.3.0 配置下耗时的 1.7 倍。

如果需要手动控制 BR 备份对集群性能带来的影响，可以通过以下方案实现。这两种方案在减少 BR 备份对集群的影响的同时，也会降低备份任务的速度。

- 使用 `--ratelimit` 参数对备份任务进行限速。请注意，这个参数限制的是**把备份文件存储到外部存储**的速度。计算备份文件的总大小的时候，请以备份日志中的 `backup data size(after compressed)` 为基准。
- 调节 TiKV 配置项 [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)，限制备份任务使用的资源。该配置项决定处理备份任务的工作线程数量。过往的测试数据表明，当 BR 备份的线程数量不大于 `8`、集群总 CPU 利用率不超过 60% 时，BR 备份任务对集群（无论读写负载）几乎没有影响。

## BR 会备份系统表吗？在数据恢复的时候，这些系统表会冲突吗？

在 v5.1.0 之前，BR 备份时会过滤掉系统库 `mysql.*` 的表数据。自 v5.1.0 起，BR 默认**备份**集群内的全部数据，包括系统库 `mysql.*` 中的数据。

恢复数据时，系统表不会冲突。由于恢复 `mysql.*` 中系统表数据的技术实现尚不完善，因此 BR 默认**不恢复**系统库 `mysql` 中的表数据，也就不会产生任何冲突。详情参阅[备份和恢复 `mysql` 系统库下的表数据（实验特性）](/br/backup-and-restore-tool.md#备份和恢复-mysql-系统库下的表数据实验特性)。

## BR 遇到 Permission denied 或者 No such file or directory 错误，即使用 root 运行 BR 也无法解决，该如何处理？

需要确认 TiKV 是否有访问备份目录的权限。如果是备份，确认是否有写权限；如果是恢复，确认是否有读权限。

在进行备份操作时，如果使用本地磁盘或 NFS 作为存储介质，请确保执行 BR 的用户和启动 TiKV 的用户相同（如果 BR 和 TiKV 位于不同的机器，则需要用户的 UID 相同），否则备份可能会出现该问题。。

使用 root 运行 BR 仍旧有可能会因为磁盘权限而失败，因为备份文件 (SST) 的保存是由 TiKV 执行的。

> **注意：**
>
> 在恢复的时候也可能遇到同样的问题。
>
> 使用 BR 进行数据的恢复时，检验读权限的时机是在第一次读取 SST 文件时，考虑到执行 DDL 的耗时，这个时刻可能会离开始运行 BR 的时间很远。这样可能会出现等了很长时间之后遇到 Permission denied 错误失败的情况。
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

    由以上命令输出结果可知，`tikv-server` 实例由用户 `tidb_ouo` 启动，但用户账号 `tidb_ouo` 没有 `backup` 目录的写入权限， 所以备份失败。

## BR 遇到错误信息 `Io(Os...)`，该如何处理？

这类问题几乎都是 TiKV 在写盘的时候遇到的系统调用错误。例如遇到 `Io(Os { code: 13, kind: PermissionDenied...})` 或者 `Io(Os { code: 2, kind: NotFound...})` 这类错误信息，首先检查备份目录的挂载方式和文件系统，试试看备份到其它文件夹或者其它硬盘。

目前已知备份到 samba 搭建的网盘时可能会遇到 `Code: 22(invalid argument)` 错误。

## BR 遇到错误信息 `rpc error: code = Unavailable desc =...`，该如何处理？

该问题一般是因为使用 BR 恢复数据的时候，恢复集群的性能不足导致的。可以从恢复集群的监控或者 TiKV 日志来辅助确认。

要解决这类问题，可以尝试扩大集群资源，以及调小恢复时的并发度 (concurrency)，打开限速 (ratelimit) 设置。

## 使用 local storage 的时候，BR 备份的文件会存在哪里？

在使用 local storage 的时候，会在运行 BR 的节点生成 `backupmeta`，在各个 Region 的 Leader 节点生成备份文件。

## 备份数据有多大，备份会有副本吗？

备份的时候仅仅在每个 Region 的 Leader 处生成该 Region 的备份文件。因此备份的大小等于数据大小，不会有多余的副本数据。所以最终的总大小大约是 TiKV 数据总量除以副本数。

但是假如想要从本地恢复数据，因为每个 TiKV 都必须要能访问到所有备份文件，在最终恢复的时候会有等同于恢复时 TiKV 节点数量的副本。

## BR 恢复到 TiCDC / Drainer 的上游集群时，要注意些什么？

+ **BR 恢复的数据无法被同步到下游**，因为 BR 直接导入 SST 文件，而下游集群目前没有办法获得上游的 SST 文件。

+ 在 4.0.3 版本之前，BR 恢复时产生的 DDL jobs 还可能会让 TiCDC / Drainer 执行异常的 DDL。所以，如果一定要在 TiCDC / Drainer 的上游集群执行恢复，请将 BR 恢复的所有表加入 TiCDC / Drainer 的阻止名单。

TiCDC 可以通过配置项中的 [`filter.rules`](https://github.com/pingcap/tiflow/blob/7c3c2336f98153326912f3cf6ea2fbb7bcc4a20c/cmd/changefeed.toml#L16) 项完成，Drainer 则可以通过 [`syncer.ignore-table`](/tidb-binlog/tidb-binlog-configuration-file.md#ignore-table) 完成。

## BR 会备份表的 `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS` 信息吗？恢复出来的表会有多个 Region 吗？

会的，BR 会备份表的 [`SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 信息，并恢复成多个 Region。

## 使用 BR 恢复备份数据后，SQL 查询报错 `region is unavailable`

如果 BR 备份的集群有 TiFlash，恢复时会将 TiFlash 信息存进 `TableInfo`。此时如果恢复的集群没有 TiFlash，则会报该错误。计划在未来版本中修复该错误。

## BR 是否支持就地 (in-place) 全量恢复某个历史备份？

不支持。

## 在 Kubernetes 环境中如何使用 BR 进行增量备份？

可以使用 kubectl 执行 `kubectl -n ${namespace} get bk ${name}` 以获得上次 BR 备份 `commitTs` 字段，该字段的内容可作为 `--lastbackupts` 使用。

## BR backupTS 如何转化成 Unix 时间？

BR `backupTS` 默认是在备份开始前，从 PD 获取到的最新时间戳。可以使用 `pd-ctl tso timestamp` 来解析该时间戳，以获得精确值，也可以通过 `backupTS >> 18` 来快速获取估计值。

## BR 恢复存档后是否需要对表执行 `ANALYZE` 以更新 TiDB 在表和索引上留下的统计信息？

BR 不会备份统计信息（v4.0.9 除外）。所以在恢复存档后需要手动执行 `ANALYZE TABLE` 或等待 TiDB 自动进行 `ANALYZE`。

BR v4.0.9 备份统计信息使 BR 消耗过多内存，为保证备份过程正常，从 v4.0.10 开始默认关闭备份统计信息的功能。

如果不对表执行 `ANALYZE`，TiDB 会因统计信息不准确而选不中最优化的执行计划。如果查询性能不是重点关注项，可以忽略 `ANALYZE`。

## 是否可以同时使用多个 BR 进程对单个集群进行恢复？

**强烈不建议**在单个集群中同时使用多个 BR 进程进行恢复，原因如下：

+ BR 在恢复数据时，会修改 PD 的一些全局配置。如果同时使用多个 BR 进程进行恢复，这些配置可能会被错误地覆写，导致集群状态异常。
+ 因为 BR 在恢复数据的时候会占用大量集群资源，事实上并行恢复能获得的速度提升也非常有限。
+ 多个 BR 并行恢复的场景没有经过测试，无法保证成功。
