---
title: PD 配置文件描述
category: reference
---

# PD 配置文件描述

PD 配置文件比命令行参数支持更多的选项。你可以在 [conf/config.toml](https://github.com/pingcap/pd/blob/master/conf/config.toml) 找到默认的配置文件。

本文档只阐述未包含在命令行参数中的参数，命令行参数参见[这里](/reference/configuration/pd-server/configuration.md)。

<!-- markdownlint-disable MD001 -->
### `lease`

+ PD Leader Key 租约超时时间，超时系统重新选举 Leader。
+ 默认：3
+ 单位：秒

### `tso-save-interval`

+ TSO 分配的时间窗口,实时持久存储。
+ 默认：3s

### `initial-cluster-state`

+ 集群初始状态
+ 默认：new

### `enable-prevote`

+ 开启 raft prevote 的开关。
+ 默认：true

### `quota-backend-bytes`

+ 元信息数据库存储空间的大小，默认 2GB。
+ 默认：2147483648

### `auto-compaction-mod`

+ 元信息数据库自动压缩的模式，可选项为 periodic（按周期），revision（按版本数）。
+ 默认：periodic

### `auto-compaction-retention`

+ compaction-mode 为 periodic 时为元信息数据库自动压缩的间隔时间；compaction-mode 设置为 revision 时为自动压缩的版本数。
+ 默认：1h

### `force-new-cluster`

+ 强制让该 PD 以一个新集群启动，且修改 raft 成员数为 1。
+ 默认：false

### `tick-interval`

+ etcd raft 的 tick 周期。
+ 默认：100ms

### `election-interval`

+ etcd leader 选举的超时时间。
+ 默认：3s

### `use-region-storage`

+ 开启独立的 region 存储。
+ 默认：false

## log

日志相关的配置项。

### `format`

+ 日志格式，可指定为"text"，"json"， "console"。
+ 默认：text

### `disable-timestamp`

+ 是否禁用日志中自动生成的时间戳。
+ 默认：false

## log.file

日志文件相关的配置项。

### `max-size`

+ 单个日志文件最大大小，超过该值系统自动切分成多个文件。
+ 默认：300
+ 单位：MiB
+ 最小值为 1

### `max-days`

+ 日志保留的最长天数。
+ 默认: 28
+ 最小值为 1

### `max-backups`

+ 日志文件保留的最大个数。
+ 默认: 7
+ 最小值为 1

## metric

监控相关的配置项。

### `interval`

+ 向 promethus 推送监控指标数据的间隔时间。
+ 默认: 15s

## schedule

调度相关的配置项。

### `max-merge-region-size`

+ 控制 Region Merge 的 size 上限，当 Region Size 大于指定值时 PD 不会将其与相邻的 Region 合并。
+ 默认: 20

### `max-merge-region-keys`

+ 控制 Region Merge 的 key 上限，当 Region key 大于指定值时 PD 不会将其与相邻的 Region 合并。
+ 默认: 200000

### `patrol-region-interval`

+ 控制 replicaChecker 检查 Region 健康状态的运行频率，越短则运行越快，通常状况不需要调整
+ 默认: 100ms

### `split-merge-interval`

+ 控制对同一个 Region 做 split 和 merge 操作的间隔，即对于新 split 的 Region 一段时间内不会被 merge。
+ 默认: 1h

### `max-snapshot-count`

+ 控制单个 store 最多同时接收或发送的 snapshot 数量，调度受制于这个配置来防止抢占正常业务的资源。
+ 默认: 3

### `max-pending-peer-count`

+ 控制单个 store 的 pending peer 上限，调度受制于这个配置来防止在部分节点产生大量日志落后的 Region。
+ 默认：16

### `max-store-down-time`

+ PD 认为失联 store 无法恢复的时间，当超过指定的时间没有收到 store 的心跳后，PD 会在其他节点补充副本。
+ 默认：30m

### `leader-schedule-limit`

+ 同时进行 leader 调度的任务个数。
+ 默认：4

### `region-schedule-limit`

+ 同时进行 Region 调度的任务个数
+ 默认：4

### `replica-schedule-limit`

+ 同时进行 replica 调度的任务个数。
+ 默认：8

### `merge-schedule-limit`

+ 同时进行的 Region Merge 调度的任务，设置为 0 则关闭 Region Merge。
+ 默认：8

### `high-space-ratio`

+ 设置 store 空间充裕的阈值。
+ 默认：0.6
+ 最小值：大于 0
+ 最大值：小于 1

### `low-space-ratio`

+ 设置 store 空间不足的阈值。
+ 默认：0.8
+ 最小值：大于 0
+ 最大值：小于

### `tolerant-size-ratio`

+ 控制 balance 缓冲区大小。
+ 默认：5
+ 最小值：0

### `disable-remove-down-replica`

+ 关闭自动删除 DownReplica 的特性的开关，当设置为 true 时，PD 不会自动清理宕机状态的副本。
+ 默认：false

### `disable-replace-offline-replica`

+ 关闭迁移 OfflineReplica 的特性的开关，当设置为 true 时，PD 不会迁移下线状态的副本。
+ 默认：false

### `disable-make-up-replica`

+ 关闭补充副本的特性的开关，当设置为 true 时，PD 不会为副本数不足的 Region 补充副本。
+ 默认：false

### `disable-remove-extra-replica`

+ 关闭删除多余副本的特性开关，当设置为 true 时，PD 不会为副本数过多的 Region 删除多余副本。
+ 默认：false

### `disable-location-replacement`

+ 关闭隔离级别检查的开关，当设置为 true 时，PD 不会通过调度来提升 Region 副本的隔离级别。
+ 默认：false

## replication

副本相关的配置项。

### `max-replicas`

+ 副本数量。
+ 默认：3

### `location-labels`

+ TiKV 集群的拓扑信息。
+ 默认：[]

## label-property

标签相关的配置项。

### `key`

+ 拒绝 leader 的 store 带有的 label key。
+ 默认：""

### `value`

+ 拒绝 leader 的 store 带有的 label value。
+ 默认：""
