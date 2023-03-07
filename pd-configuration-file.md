---
title: PD 配置文件描述
aliases: ['/docs-cn/stable/pd-configuration-file/','/docs-cn/v4.0/pd-configuration-file/','/docs-cn/stable/reference/configuration/pd-server/configuration-file/','/docs-cn/v4.0/reference/configuration/pd-server/configuration-file/']
---

# PD 配置文件描述

<!-- markdownlint-disable MD001 -->

PD 配置文件比命令行参数支持更多的选项。你可以在 [conf/config.toml](https://github.com/tikv/pd/blob/release-4.0/conf/config.toml) 找到默认的配置文件。

本文档只阐述未包含在命令行参数中的参数，命令行参数参见 [PD 配置参数](/command-line-flags-for-pd-configuration.md)。

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

+ 元信息数据库存储空间的大小，默认 8GiB。
+ 默认：8589934592

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

## security

安全相关配置项。

### `cacert-path`

+ CA 文件路径
+ 默认：""

### `cert-path`

+ 包含 X509 证书的 PEM 文件路径
+ 默认：""

### `key-path`

+ 包含 X509 key 的 PEM 文件路径
+ 默认：""

### `redact-info-log` <span class="version-mark">从 v4.0.10 版本开始引入</span>

+ 控制 PD 日志脱敏的开关
+ 该配置项值设为 true 时将对 PD 日志脱敏，遮蔽日志中的用户信息。
+ 默认值：false

## log

日志相关的配置项。

### `level`

+ 日志等级，可指定为 "DEBUG"，"INFO"，"WARNING"，"ERROR"，"CRITICAL"。
+ 默认值："INFO"

### `format`

+ 日志格式，可指定为"text"，"json"，"console"。
+ 默认值："text"

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
+ 默认：0

### `max-backups`

+ 日志文件保留的最大个数。
+ 默认：0

## metric

监控相关的配置项。

### `interval`

+ 向 Prometheus 推送监控指标数据的间隔时间。
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
+ 默认：2048

### `hot-region-schedule-limit`

+ 控制同时进行的 hot Region 任务。该配置项独立于 Region 调度。
+ 默认值：4

### `hot-region-cache-hits-threshold`

+ 设置识别热点 Region 所需的分钟数。只有当 Region 处于热点状态持续时间超过此分钟数时，PD 才会参与热点调度。
+ 默认值：3

### `replica-schedule-limit`

+ 同时进行 replica 调度的任务个数。
+ 默认：64

### `merge-schedule-limit`

+ 同时进行的 Region Merge 调度的任务，设置为 0 则关闭 Region Merge。
+ 默认：8

### `high-space-ratio`

+ 设置 store 空间充裕的阈值。当节点的空间占用比例小于该阈值时，PD 调度时会忽略节点的剩余空间，主要根据实际数据量进行均衡。此配置仅在 `region-score-formula-version = v1` 时生效。
+ 默认：0.7
+ 最小值：大于 0
+ 最大值：小于 1

### `low-space-ratio`

+ 设置 store 空间不足的阈值。当某个节点的空间占用比例超过该阈值时，PD 会尽可能避免往该节点迁移数据，同时主要根据节点剩余空间大小进行调度，避免对应节点的磁盘空间被耗尽。
+ 默认：0.8
+ 最小值：大于 0
+ 最大值：小于 1

### `tolerant-size-ratio`

+ 控制 balance 缓冲区大小。
+ 默认：0 (为 0 为自动调整缓冲区大小)
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

### `store-balance-rate`

+ 控制 TiKV 每分钟最多允许做 add peer 相关操作的次数。
+ 默认：15

## replication

副本相关的配置项。

### `max-replicas`

+ 所有副本数量，即 leader 与 follower 数量之和。默认为 `3`，即 1 个 leader 和 2 个 follower。
+ 默认：3

### `location-labels`

+ TiKV 集群的拓扑信息。
+ 默认：[]
+ [配置集群拓扑](/schedule-replicas-by-topology-labels.md)

### `strictly-match-label`

+ 打开强制 TiKV Label 和 PD 的 location-labels 是否匹配的检查
+ 默认：false

### `enable-placement-rules`

+ 打开 `placement-rules`
+ 默认：false
+ 参考[Placement Rules 使用文档](/configure-placement-rules.md)
+ 4.0 实验性特性

## label-property

标签相关的配置项。

### `key`

+ 拒绝 leader 的 store 带有的 label key。
+ 默认：""

### `value`

+ 拒绝 leader 的 store 带有的 label value。
+ 默认：""

## dashboard

PD 中内置的 [TiDB Dashboard](/dashboard/dashboard-intro.md) 相关配置项。

### `tidb-cacert-path`

+ CA 根证书文件路径。可配置该路径来使用 TLS 连接 TiDB 的 SQL 服务。
+ 默认值：""

### `tidb-cert-path`

+ SSL 证书文件路径。可配置该路径来使用 TLS 连接 TiDB 的 SQL 服务。
+ 默认值：""

### `tidb-key-path`

+ SSL 私钥文件路径。可配置该路径来使用 TLS 连接 TiDB 的 SQL 服务。
+ 默认值：""

### `public-path-prefix`

+ 通过反向代理访问 TiDB Dashboard 时，配置反向代理提供服务的路径前缀。
+ 默认："/dashboard"
+ 若不通过反向代理访问 TiDB Dashboard，**请勿配置该项**，否则可能导致 TiDB Dashboard 无法正常访问。关于该配置的详细使用场景，参见[通过反向代理使用 TiDB Dashboard](/dashboard/dashboard-ops-reverse-proxy.md)。

### `enable-telemetry`

+ 是否启用 TiDB Dashboard 遥测功能。
+ 默认：true
+ 参阅[遥测](/telemetry.md)了解该功能详情。
