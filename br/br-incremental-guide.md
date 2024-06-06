---
title: TiDB 增量备份与恢复使用指南
summary: 了解 TiDB 的增量备份与恢复功能使用。
---

# TiDB 增量备份与恢复使用指南

TiDB 集群增量数据包含在某个时间段的起始和结束两个快照的变化差异的数据，以及之间的 DDL。增量备份的数据相对比全量备份数据而言数据量更小，适合配合快照备份一起使用，减少备份的数据量。进行增量备份的时候，需要保证备份时间范围内的多版本数据没有被 [TiDB GC 机制](/garbage-collection-overview.md)回收。例如，每个小时进行一次增量备份，则需要[调整 TiDB 集群的 GC Lifetime 设置](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入)至少大于 1 小时。

> **警告：**
>
> 当前该功能已经停止开发迭代，推荐你选择[日志备份与恢复功能](/br/br-pitr-guide.md)代替。

## 使用限制

由于增量备份的恢复依赖于备份时间点的库表快照来过滤增量 DDL，因此对于增量备份过程中删除的表，在恢复后可能仍然存在，需要手动删除。

增量备份尚不支持批量重命名表的操作。如果在增量备份过程中发生了批量重命名表的操作，则有可能造成恢复失败。建议在批量重命名表后进行一次全量备份，并在恢复时使用最新的全量备份替代增量数据。

## 对集群进行增量备份

使用 `br backup` 进行增量备份只需要指定**上一次的备份时间戳** `--lastbackupts`，br 命令行工具会判定需要备份 `lastbackupts` 和当前时间之间增量数据。使用 `validate` 指令获取上一次备份的时间戳，示例如下：

```shell
LAST_BACKUP_TS=`tiup br validate decode --field="end-version" --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"| tail -n1`
```

备份 `(LAST_BACKUP_TS, current timestamp]` 之间的增量数据，以及这段时间内的 DDL：

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330/incr?access-key=${access-key}&secret-access-key=${secret-access-key}" \
--lastbackupts ${LAST_BACKUP_TS} \
--ratelimit 128
```

以上命令会中：

- `--lastbackupts`：上一次的备份时间戳。
- `--ratelimit`：**每个 TiKV** 执行备份任务的速度上限（单位 MiB/s）。
- `storage`：数据备份到存储地址。增量备份数据需要与快照备份数据保存在不同的路径下，例如上例保存在全量备份数据下的 `incr` 目录中。关于 URI 格式的详细信息，请参考[外部存储服务的 URI 格式](/external-storage-uri.md)。

## 恢复增量备份数据

恢复增量数据的时候，需要保证备份时指定的 `LAST_BACKUP_TS` 之前备份的数据已经全部恢复到目标集群。同时，因为增量恢复的时候会更新数据，因此你需要保证此时不会有其他写入，避免出现冲突。

恢复全量备份数据，备份数据存储在 `backup-101/snapshot-202209081330` 目录下：

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

恢复全量备份后的增量备份数据，备份数据存储在 `backup-101/snapshot-202209081330/incr` 目录下：

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330/incr?access-key=${access-key}&secret-access-key=${secret-access-key}"
```
