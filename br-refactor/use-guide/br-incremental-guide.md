---
title: TiDB 增量备份和恢复功能使用
summary: 了解 TiDB 的增量备份和恢复功能使用。
---

# 使用增量备份和恢复功能

TiDB 集群增量数据包含在某个时间段的起始和结束两个快照的变化差异的数据。 增量数据相对比全量数据而言数据量更小，适合配合快照备份一起使用，减少备份的数据量。进行增量备份的时候，需要保证备份时间范围内的多版本数据没有被 [TiDB GC 机制](/garbage-collection-overview.md)回收掉。例如，每个小时进行一次增量备份，则需要[调整 TiDB 集群的 GC Lifetime 设置](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入) 至少大于 1h。

> **警告：**
>
> 当前该功能已经停止开发迭代，推荐你选择日志备份和恢复功能(xxx) 代替。

## 对集群进行增量备份

使用 `br backup` 进行备份的时候需要指定**上一次的备份时间戳** `--lastbackupts`。 使用 `validate` 指令获取上一次备份的时间戳，示例如下：

```shell
LAST_BACKUP_TS=`br validate decode --field="end-version" -s s3://backup-data/2022-01-30/ | tail -n1`
```

备份 `(LAST_BACKUP_TS, current PD timestamp]` 之间的增量数据，以及这段时间内的 DDL：

```
br backup full --pd ${PDIP}:2379 --ratelimit 128 --storage "s3://backup-data/2022-01-30/incr" --lastbackupts ${LAST_BACKUP_TS}
```

以上命令会中：

- `--lastbackupts`：上一次的备份时间戳.
- `--ratelimit`：**每个 TiKV** 执行备份任务的速度上限（单位 MiB/s）。
- `storage`: 数据备份到存储地址, 增量备份数据需要与快照备份数据保存在不同的路径下.详细配置参考[备份存储](xxx) 

## 恢复增量备份数据

恢复增量数据的时候，需要保证备份时指定的 `last backup ts` 之前备份的数据已经全部恢复到目标集群。同时因为增量恢复的时候会更新 ts 数据，因此你需要保证此时不会有其他写入，避免出现冲突。

```shell
br restore full --pd "${PDIP}:2379" --storage "s3://backup-data/2022-01-30/incr"
```
