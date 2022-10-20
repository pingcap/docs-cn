---
title: TiDB 快照备份和恢复使用指南
summary: 了解 TiDB 的快照备份和恢复功能使用。
---

# TiDB 快照备份和恢复使用指南

本教程介绍快照备份和恢复功能的使用。快照备份是集群全量备份的一种实现。它基于 TiDB 的 [MVCC](/tidb-storage.md#mvcc) 实现，将指定快照包含的所有数据备份到目标存储中。备份下来的数据大小约等于集群（压缩后的）单副本数据大小。 备份完成之后，你可以在一个空集群上恢复备份的数据，将集群恢复到与快照备份对应的数据状态，同时恢复功能会依据集群副本设置恢复出多副本。

除了基础的备份和恢复功能，快照备份恢复还提供以下的功能

* 支持配置备份指定时间点的快照数据
* 只恢复指定 db/table 数据

## 对集群进行快照备份

使用 `br backup full` 可以进行一次快照备份。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00' \
    --storage "s3://backup-101/snapshot-202209081330?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --ratelimit 128 \
```

以上命令中：

- `--backupts`：快照对应的物理时间点。如果该快照的数据被 GC 了，那么 `br backup` 命令会报错退出；如果你没有指定该参数，那么 br 会选取备份开始的时间点所对应的快照。
- `--ratelimit`：**每个 TiKV** 备份数据的速度上限（单位 MiB/s）。
- `storage`: 数据备份到的存储地址。快照备份支持以 S3/GCS/Azure Blob Storage 为备份存储，以上命令以 S3 为示例。详细参考[备份存储 URL 配置](/br/backup-and-restore-storages.md#url-格式)。

备份时间有进度条会在终端显示，进度条效果如下。在备份完成后，br 会输出备份耗时、速度、备份数据大小等信息。

```shell
Full Backup <-------------------------------------------------------------------------------> 100.00%
Checksum <----------------------------------------------------------------------------------> 100.00%
*** ["Full Backup success summary"] *** [backup-checksum=3.597416ms] [backup-fast-checksum=2.36975ms] *** [total-take=4.715509333s] [BackupTS=435844546560000000] [total-kv=1131] [total-kv-size=250kB] [average-speed=53.02kB/s] [backup-data-size(after-compressed)=71.33kB] [Size=71330]
```

## 查询快照备份的时间点信息

出于管理备份数的需要，如果你需要查看某个快照备份对应的快照物理时间点，可以执行下面的命令：

```shell
tiup br validate decode --field="end-version" -s "s3://backup-101/snapshot-202209081330?access_key=${access_key}&secret_access_key=${secret_access_key}" | tail -n1
```

结果输出，对应物理时间 `2022-09-08 13:30:00 +0800 CST`

```
435844546560000000
```

## 恢复快照备份数据

如果你需要恢复备份的快照数据，则可以使用 `br restore full`。该命令的详细使用帮助可以通过执行 `br restore full --help` 查看。

用例：将上文备份的快照数据恢复到目标机群。

```shell
tiup br restore full --pd "${PD_IP}:2379" --storage "s3://backup-101/snapshot-202209081330?access_key=${access_key}&secret_access_key=${secret_access_key}"
```

恢复期间有进度条会在终端中显示，进度条效果如下。在完成恢复后, br 会输出恢复耗时、速度、恢复数据大小等信息。

```shell
Full Restore <------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] *** [total-take=4.344617542s] [total-kv=5] [total-kv-size=327B] [average-speed=75.27B/s] [restore-data-size(after-compressed)=4.813kB] [Size=4813] [BackupTS=435844901803917314]
```

### 恢复备份数据中指定库表的数据

BR 支持只恢复备份数据中指定库/表的局部数据，该功能在恢复过程中过滤掉不需要的数据。

**恢复单个数据库的数据**

要将备份数据中的某个数据库恢复到集群中，可以使用 `br restore db` 命令。 以下示例只恢复 `test` 库的相关数据：

```shell
tiup br restore db --pd "${PD_IP}:2379" --db "test" --storage "s3://backup-101/snapshot-202209081330?access_key=${access_key}&secret_access_key=${secret_access_key}"
```

以上命令中 `--db` 选项指定了需要恢复的数据库名字。

**恢复单张表的数据**

要将备份数据中的某张数据表恢复到集群中，可以使用 `br restore table` 命令。以下示例只恢复 `test`.`usertable` 表的相关的数据

```shell
tiup br restore table --pd "${PD_IP}:2379" --db "test" --table "usertable" \
--storage "s3://backup-101/snapshot-202209081330?access_key=${access_key}&secret_access_key=${secret_access_key}"
```

以上命令中 `--db` 选项指定了需要恢复的数据库名字，`--table` 选项指定了需要恢复的表名。

**使用表库功能过滤恢复数据**

如果你需要用复杂的过滤条件来恢复多个表，执行 `br restore full` 命令，并用 `--filter` 或 `-f` 指定使用[表库过滤](/table-filter.md)。

以下示例恢复 `db*.tbl*`的表的相关的数据。

```shell
tiup br restore full --pd "${PD_IP}:2379" --filter 'db*.tbl*' --storage "s3://backup-101/snapshot-202209081330?access_key=${access_key}&secret_access_key=${secret_access_key}"
```

### 恢复 `mysql` 数据库下的表

自 BR v5.1.0 开始，快照备份会备份**mysql schema 下的系统表数据**，而不会默认恢复这些数据。自 BR v6.2.0 开始，在设置 `--with-sys-table` 下，恢复数据时将同时恢复**部分系统表相关数据**。

**BR 可恢复的部分系统表**：

```
+----------------------------------+
| mysql.columns_priv               |
| mysql.db                         |
| mysql.default_roles              |
| mysql.global_grants              |
| mysql.global_priv                |
| mysql.role_edges                 |
| mysql.tables_priv                |
| mysql.user                       |
+----------------------------------+
```

**BR 不能恢复以下系统表**：

- 统计信息表（`mysql.stat_*`）
- 系统变量表（`mysql.tidb`、`mysql.global_variables`）
- [其他系统表](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)

当恢复系统权限相关数据的时候，请注意：

- BR 不会恢复 `user` 为 `cloud_admin` 并且 `host` 为 `'%'` 的用户数据，该用户是 TiDB Cloud 预留账户。请不要在你的环境中创建 `cloud_admin` 的用户或者角色，因为依赖 `cloud_admin` 的用户的权限将不能被完整恢复。
- 在恢复数据前会检查目标集群的系统表是否跟备份数据中的系统表兼容。这里的兼容是指满足以下所有条件:
    - 目标集群需要存在备份中的系统权限表。
    - 目标集群系统权限表**列数**需要跟备份数据中一致，列顺序可以有差异。
    - 目标集群系统权限表列需要跟备份数据兼容，如果为带长度类型（包括整形、字符等类型），前者长度需 >= 后者，如果为 enum 类型，则应该为后者超集。

## 性能与影响

### 快照备份的性能与影响

TiDB 备份功能对集群性能（事务延迟和 QPS）有一定的影响，但是可以通过调整备份的线程数 [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) ，以及增加集群配置，来降低备份对集群性能的影响。

为了更加具体说明备份对集群的影响，这里列举了多次快照备份测试结论来说明影响的范围：

- （使用 5.3 及之前版本）BR 在默认配置下，单 TiKV 存储节点上备份线程数量是节点 CPU 总数量的 75% 的时候，QPS 会下降到备份之前的 35% 左右。
- （使用 5.4 及以后版本）当 BR 在单 TiKV 存储节点上备份的线程数量不大于 `8`、集群总 CPU 利用率不超过 80% 时，BR 备份任务对集群（无论读写负载）影响最大在 20% 左右。
- （使用 5.4 及以后版本）当 BR 在单 TiKV 存储节点上备份的线程数量不大于 `8`、集群总 CPU 利用率不超过 75% 时，BR 备份任务对集群（无论读写负载）影响最大在 10% 左右。
- （使用 5.4 及以后版本）当 BR 在单 TiKV 存储节点上备份的线程数量不大于 `8`、集群总 CPU 利用率不超过 60% 时，BR 备份任务对集群（无论读写负载）几乎没有影响。

你可以通过如下方案手动控制 br 备份对集群性能带来的影响。但是，这两种方案在减少 BR 备份对集群的影响的同时，也会降低备份任务的速度。

- 使用 `--ratelimit` 参数对备份任务进行限速。请注意，这个参数限制的是**把备份文件存储到外部存储**的速度。计算备份文件的大小时，请以备份日志中的 `backup data size(after compressed)` 为准。
- 调节 TiKV 配置项 [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)，限制备份任务使用的工作线程数量。过往的测试数据表明，当 BR 备份的线程数量不大于 `8`、集群总 CPU 利用率不超过 60% 时，BR 备份任务对集群（无论读写负载）几乎没有影响。

通过限制备份的线程数量可以降低备份对集群性能的影响，但是这会影响到备份的性能，以上的多次备份测试结果显示:（单 TiKV 存储节点上）备份速度和备份线程数量呈正比，在线程数量量较少的时候，速度大概是 20M/线程数。例如，单节点 5 个备份线程可达到 100M/s。

### 快照恢复的性能与影响

- TiDB 恢复的时候会尽可能打满 TiKV CPU、磁盘 IO、网络带宽等资源，所以推荐在空的集群上执行备份数据的恢复，避免对正在运行的业务产生影响；
- 备份数据的恢复速度，与集群配置、部署、运行的业务都有比较大的关系。一般情况下，备份数据恢复速度能够达到（单台 TiKV 节点） 100 MB/s。。

> **注意：**
>
> 影响和性能，与集群配置、部署、运行的业务都有比较大的关系，以上结论，经过多个场景的仿真测试，并且在部分合作用户场景中，得到验证，具有一定的参考意义。 但是在不同用户场景中最大影响和性能，最好以用户自己的测试结论为准。

## 进一步阅读

* [TiDB 集群备份和恢复实践示例](/br/backup-and-restore-use-cases.md)
* [br 命令行手册](/br/use-br-command-line-tool.md)
* [快照备份和恢复架构设计](/br/br-snapshot-architecture.md)