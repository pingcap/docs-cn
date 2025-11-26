---
title: PD 配置文件描述
aliases: ['/docs-cn/dev/pd-configuration-file/','/docs-cn/dev/reference/configuration/pd-server/configuration-file/']
summary: PD 配置文件包含了许多参数，如节点名称、数据路径、客户端 URL、广告客户端 URL、节点 URL 等。还包括了一些实验性特性的配置项，如内存限制、GC 触发阈值、GOGC Tuner 等。此外，还有监控、调度、副本、标签、Dashboard、同步模式和资源控制等相关配置项。
---

# PD 配置文件描述

<!-- markdownlint-disable MD001 -->

PD 配置文件比命令行参数支持更多的选项。你可以在 [conf/config.toml](https://github.com/pingcap/pd/blob/master/conf/config.toml) 找到默认的配置文件。

本文档只阐述未包含在命令行参数中的参数，命令行参数参见 [PD 配置参数](/command-line-flags-for-pd-configuration.md)。

> **Tip:**
>
> PD 初始化后，如果你需要调整配置项的值，请参考[修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数) 和 [PD Control 使用说明](/pd-control.md)进行操作。

### `name`

+ PD 节点名称。
+ 默认值：`"pd"`
+ 如果你需要启动多个 PD，一定要给 PD 使用不同的名字。

### `data-dir`

+ PD 存储数据路径。
+ 默认值：`"default.${name}"`

### `client-urls`

+ PD 监听的客户端 URL 列表。
+ 默认值：`"http://127.0.0.1:2379"`
+ 如果部署一个集群，client URLs 必须指定当前主机的 IP 地址，例如 `"http://192.168.100.113:2379"`，如果是运行在 Docker 则需要指定为 `"http://0.0.0.0:2379"`。

### `advertise-client-urls`

+ 用于外部访问 PD 的 URL 列表。
+ 默认值：`"${client-urls}"`
+ 在某些情况下，例如 Docker 或者 NAT 网络环境，客户端并不能通过 PD 自己监听的 client URLs 来访问到 PD，这时候，你就可以设置 advertise URLs 来让客户端访问。
+ 例如，Docker 内部 IP 地址为 `172.17.0.1`，而宿主机的 IP 地址为 `192.168.100.113` 并且设置了端口映射 `-p 2379:2379`，那么可以设置为 `advertise-client-urls="http://192.168.100.113:2379"`，客户端可以通过 `http://192.168.100.113:2379` 来找到这个服务。

### `peer-urls`

+ PD 节点监听其他 PD 节点的 URL 列表。
+ 默认：`"http://127.0.0.1:2380"`
+ 如果部署一个集群，peer URLs 必须指定当前主机的 IP 地址，例如 `"http://192.168.100.113:2380"`，如果是运行在 Docker 则需要指定为 `"http://0.0.0.0:2380"`。

### `advertise-peer-urls`

+ 用于其他 PD 节点访问某个 PD 节点的 URL 列表。
+ 默认值：`"${peer-urls}"`
+ 在某些情况下，例如 Docker 或者 NAT 网络环境，其他节点并不能通过 PD 自己监听的 peer URLs 来访问到 PD，这时候，你就可以设置 advertise URLs 来让其他节点访问
+ 例如，Docker 内部 IP 地址为 `172.17.0.1`，而宿主机的 IP 地址为 `192.168.100.113` 并且设置了端口映射 `-p 2380:2380`，那么可以设置为 `advertise-peer-urls="http://192.168.100.113:2380"`，其他 PD 节点可以通过 `http://192.168.100.113:2380` 来找到这个服务。

### `initial-cluster`

+ 初始化 PD 集群配置。
+ 默认值：`"{name}=http://{advertise-peer-url}"`
+ 例如，如果 name 是 "pd"，并且 `advertise-peer-urls` 是 `"http://192.168.100.113:2380"`，那么 `initial-cluster` 就是 `"pd=http://192.168.100.113:2380"`。
+ 如果启动三台 PD，那么 `initial-cluster` 可能就是 `pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380`。

### `initial-cluster-state`

+ 集群初始状态
+ 默认值："new"

### `initial-cluster-token`

+ 用于在集群初始化阶段标识不同的集群。
+ 默认值："pd-cluster"
+ 如果先后部署多个集群，且多个集群有相同配置的节点，应指定不同的 token 来隔离不同的集群。

### `lease`

+ PD Leader Key 租约超时时间，超时系统重新选举 Leader。
+ 默认值：从 v8.5.2 版本开始，默认值为 5。在 v8.5.2 版本之前，默认值为 3。
+ 单位：秒

### `quota-backend-bytes`

+ 元信息数据库存储空间的大小，默认 8GiB。
+ 默认值：8589934592

### `auto-compaction-mod`

+ 元信息数据库自动压缩的模式，可选项为 periodic（按周期），revision（按版本数）。
+ 默认值：periodic

### `auto-compaction-retention`

+ compaction-mode 为 periodic 时为元信息数据库自动压缩的间隔时间；compaction-mode 设置为 revision 时为自动压缩的版本数。
+ 默认值：1h

### `tick-interval`

+ 等价于 etcd 的 `heartbeat-interval` 配置项，用于控制不同 PD 节点中内嵌的 etcd 实例之间的 Raft 心跳间隔。较小的值可以提高故障检测速度，但会增加网络负载。
+ 默认值：500ms

### `election-interval`

+ 等价于 etcd 的 `election-timeout` 配置项，用于控制 PD 节点中内嵌的 etcd 实例的选举超时时间，即在超过该时间没有收到来自其他 etcd 实例的有效心跳后，当前 etcd 实例会发起 Raft 选举。
+ 默认值：3000ms
+ 该值必须至少为 [`tick-interval`](#tick-interval) 的 5 倍，例如 `tick-interval` 为 `500ms`，则 `election-interval` 必须大于等于 `2500ms`。

### `enable-prevote`

+ 等价于 etcd 的 `pre-vote` 配置项，用于控制 PD 节点中内嵌的 etcd 是否开启 Raft 预投票。启用后，etcd 会进行额外的选举阶段，以检查是否能获得足够的票数赢得选举，从而最大程度地减少服务中断。
+ 默认值：true

### `force-new-cluster`

+ 强制让该 PD 以一个新集群启动，且修改 raft 成员数为 1。
+ 默认值：false

### `tso-update-physical-interval`

+ TSO 物理时钟更新周期。
+ 在默认的一个 TSO 物理时钟更新周期内 (50ms)，PD 最多提供 262144 个 TSO。如果需要更多的 TSO，可以将这个参数调小。最小值为 `1ms`。
+ 缩短这个参数会增加 PD 的 CPU 消耗。根据测试，相比 `50ms` 更新周期，更新周期为 `1ms` 时，PD 的 CPU 占用率 ([CPU usage](https://man7.org/linux/man-pages/man1/top.1.html)) 将增加约 10%。
+ 默认值：50ms
+ 最小值：1ms

## pd-server

pd-server 相关配置项。

### `server-memory-limit` <span class="version-mark">从 v6.6.0 版本开始引入</span>

> **警告：**
>
> 在当前版本中，该配置项为实验特性，不建议在生产环境中使用。

+ PD 实例的内存限制比例。`0` 值表示不设内存限制。
+ 默认值：`0`
+ 最小值：`0`
+ 最大值：`0.99`

### `server-memory-limit-gc-trigger` <span class="version-mark">从 v6.6.0 版本开始引入</span>

> **警告：**
>
> 在当前版本中，该配置项为实验特性，不建议在生产环境中使用。

+ PD 尝试触发 GC 的阈值比例。当 PD 的内存使用达到 `server-memory-limit` 值 * `server-memory-limit-gc-trigger` 值时，则会主动触发一次 Golang GC。在一分钟之内只会主动触发一次 GC。
+ 默认值：`0.7`
+ 最小值：`0.5`
+ 最大值：`0.99`

### `enable-gogc-tuner` <span class="version-mark">从 v6.6.0 版本开始引入</span>

> **警告：**
>
> 在当前版本中，该配置项为实验特性，不建议在生产环境中使用。

+ 是否开启 GOGC Tuner。
+ 默认值：`false`

### `gc-tuner-threshold` <span class="version-mark">从 v6.6.0 版本开始引入</span>

> **警告：**
>
> 在当前版本中，该配置项为实验特性，不建议在生产环境中使用。

+ GOGC Tuner 自动调节的最大内存阈值比例，即 `server-memory-limit` 值 * `server-memory-limit-gc-trigger` 值，超过阈值后 GOGC Tuner 会停止工作。
+ 默认值：`0.6`
+ 最小值：`0`
+ 最大值：`0.9`

### `flow-round-by-digit` <span class="version-mark">从 v5.1 版本开始引入</span>

+ 默认值：3
+ PD 会对流量信息的末尾数字进行四舍五入处理，减少 Region 流量信息变化引起的统计信息更新。该配置项用于指定对 Region 流量信息的末尾进行四舍五入的位数。例如流量 `100512` 会归约到 `101000`。默认值为 `3`。该配置替换了 `trace-region-flow`。

> **注意：**
>
> 如果是从 v4.0 升级至当前版本，升级后的 `flow-round-by-digit` 行为和升级前的 `trace-region-flow` 行为默认保持一致：如果升级前 `trace-region-flow` 为 false，则升级后 `flow-round-by-digit` 为 127；如果升级前 `trace-region-flow` 为 true，则升级后 `flow-round-by-digit` 为 3。

### `min-resolved-ts-persistence-interval` <span class="version-mark">从 v6.0.0 版本开始引入</span>

+ 设置 PD leader 对集群中 Resolved TS 最小值进行持久化的间隔时间。如果该值设置为 `0`，表示禁用该功能。
+ 默认值：在 v6.3.0 之前版本中为 `"0s"`，在 v6.3.0 及之后的版本中为 `"1s"`，即最小正值。
+ 最小值：`"0s"`
+ 单位：秒

> **注意：**
>
> 对于从 v6.0.0~v6.2.0 升级上来的集群，`min-resolved-ts-persistence-interval` 的默认值在升级后将不会发生变化，即仍然为 `"0s"`。若要开启该功能，需要手动修改该配置项的值。

## security

安全相关配置项。

### `cacert-path`

+ CA 文件路径
+ 默认值：""

### `cert-path`

+ 包含 X509 证书的 PEM 文件路径
+ 默认值：""

### `key-path`

+ 包含 X509 key 的 PEM 文件路径
+ 默认值：""

### `redact-info-log` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 控制 PD 日志脱敏的开关
+ 可选值：`false`、`true`、`"marker"`
+ 默认值：`false`
+ 具体使用方法参见[日志脱敏](/log-redaction.md#pd-组件日志脱敏)。

## log

日志相关的配置项。

### `level`

+ 指定日志的输出级别。
+ 可选值："debug"，"info"，"warn"，"error"，"fatal"
+ 默认值："info"

### `format`

+ 日志格式。
+ 可选值："text"，"json"
+ 默认值："text"

### `disable-timestamp`

+ 是否禁用日志中自动生成的时间戳。
+ 默认值：false

## log.file

日志文件相关的配置项。

### `max-size`

+ 单个日志文件最大大小，超过该值系统自动切分成多个文件。
+ 默认值：300
+ 单位：MiB
+ 最小值为 1

### `max-days`

+ 日志保留的最长天数。
+ 如果未设置本参数或把本参数设置为默认值 `0`，PD 不清理日志文件。
+ 默认：0

### `max-backups`

+ 日志文件保留的最大个数。
+ 如果未设置本参数或把本参数设置为默认值 `0`，PD 会保留所有的日志文件。
+ 默认：0

## metric

监控相关的配置项。

### `interval`

+ 向 Prometheus 推送监控指标数据的间隔时间。
+ 默认：15s

## schedule

调度相关的配置项。

> **注意：**
> 
> 要修改与调度相关的 PD 配置项，请根据集群的情况选择以下方法之一：
>
> - 对于新部署集群，你可以直接在 PD 配置文件中进行修改。
> - 对于已有集群，请使用命令行工具 [PD Control](/pd-control.md) 进行修改。直接修改 PD 配置文件中与调度相关的配置项不会对已有集群生效。

### `max-merge-region-size`

+ 控制 Region Merge 的 size 上限，当 Region Size 大于指定值时 PD 不会将其与相邻的 Region 合并。
+ 默认：54。在 v8.4.0 之前，默认值为 20；从 v8.4.0 开始，默认值为 54。
+ 单位：MiB

### `max-merge-region-keys`

+ 控制 Region Merge 的 key 上限，当 Region key 大于指定值时 PD 不会将其与相邻的 Region 合并。
+ 默认：540000。在 v8.4.0 之前，默认值为 200000；从 v8.4.0 开始，默认值为 540000。

### `patrol-region-interval`

+ 控制 checker 检查 Region 健康状态的运行频率，越短则运行越快，通常状况不需要调整
+ 默认：10ms

### `patrol-region-worker-count` <span class="version-mark">从 v8.5.0 版本开始引入</span>

> **警告：**
>
> 将该配置项设置为大于 1 将启用并发检查。目前该功能为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/tikv/pd/issues)反馈。

+ 控制 checker 检查 Region 健康状态时，创建 [operator](/glossary.md#operator) 的并发数。通常情况下，无需调整此配置项。
+ 默认：1

### `split-merge-interval`

+ 控制对同一个 Region 做 split 和 merge 操作的间隔，即对于新 split 的 Region 一段时间内不会被 merge。
+ 默认：1h

### `max-movable-hot-peer-size` <span class="version-mark">从 v6.1.0 版本开始引入</span>

+ 控制热点调度可以调度的最大 Region size。
+ 默认：512
+ 单位：MiB

### `max-snapshot-count`

+ 控制单个 store 最多同时接收或发送的 snapshot 数量，调度受制于这个配置来防止抢占正常业务的资源。
+ 默认：64

### `max-pending-peer-count`

+ 控制单个 store 的 pending peer 上限，调度受制于这个配置来防止在部分节点产生大量日志落后的 Region。
+ 默认值：64

### `max-store-down-time`

+ PD 认为失联 store 无法恢复的时间，当超过指定的时间没有收到 store 的心跳后，PD 会在其他节点补充副本。
+ 默认值：30m

### `max-store-preparing-time` <span class="version-mark">从 v6.1.0 版本开始引入</span>

+ 控制 store 上线阶段的最长等待时间。在 store 的上线阶段，PD 可以查询该 store 的上线进度。当超过该配置项指定的时间后，PD 会认为该 store 已完成上线，无法再次查询这个 store 的上线进度，但是不影响 Region 向这个新上线 store 的迁移。通常用户无需修改该配置项。
+ 默认值：48h

### `leader-schedule-limit`

+ 同时进行 leader 调度的任务个数。
+ 默认值：4

### `region-schedule-limit`

+ 同时进行 Region 调度的任务个数
+ 默认值：2048

### `hot-region-schedule-limit`

+ 控制同时进行的 hot Region 任务。该配置项独立于 Region 调度。
+ 默认值：4

### `hot-region-cache-hits-threshold`

+ 设置识别热点 Region 所需的分钟数。只有当 Region 处于热点状态持续时间超过此分钟数时，PD 才会参与热点调度。
+ 默认值：3

### `replica-schedule-limit`

+ 同时进行 replica 调度的任务个数。
+ 默认值：64

### `merge-schedule-limit`

+ 同时进行的 Region Merge 调度的任务，设置为 0 则关闭 Region Merge。
+ 默认值：8

### `high-space-ratio`

+ 设置 store 空间充裕的阈值。当节点的空间占用比例小于该阈值时，PD 调度时会忽略节点的剩余空间，主要根据实际数据量进行均衡。此配置仅在 `region-score-formula-version = v1` 时生效。
+ 默认值：0.7
+ 最小值：大于 0
+ 最大值：小于 1

### `low-space-ratio`

+ 设置 store 空间不足的阈值。当某个节点的空间占用比例超过该阈值时，PD 会尽可能避免往该节点迁移数据，同时主要根据节点剩余空间大小进行调度，避免对应节点的磁盘空间被耗尽。
+ 默认值：0.8
+ 最小值：大于 0
+ 最大值：小于 1

### `tolerant-size-ratio`

+ 控制 balance 缓冲区大小。
+ 默认值：0（为 0 为自动调整缓冲区大小）
+ 最小值：0

### `enable-cross-table-merge`

+ 设置是否开启跨表 merge。
+ 默认值：true

### `region-score-formula-version` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 设置 Region 算分公式版本。
+ 默认值：v2
+ 可选值：v1，v2。v2 相比于 v1，变化会更平滑，空间回收引起的调度抖动情况会得到改善。

> **注意：**
>
> 如果是从 v4.0 升级至当前版本，默认不自动开启该算分公式新版本，以保证升级前后 PD 行为一致。若想切换算分公式的版本，使用需要手动通过 `pd-ctl` 设置切换，详见 [PD Control](/pd-control.md#config-show--set-option-value--placement-rules) 文档。

### `enable-joint-consensus` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 是否使用 Joint Consensus 进行副本调度。关闭该特性时，PD 将采用一次调度一个副本的方式进行调度。
+ 默认值：true

### `enable-diagnostic` <span class="version-mark">从 v6.3.0 版本开始引入</span>

+ 是否开启诊断功能。开启特性时，PD 将会记录调度中的一些状态来帮助诊断。开启时会略微影响调度速度，在 Store 数量较多时会消耗较大内存。
+ 默认值：从 v7.1.0 起，默认值从 `false` 变更为 `true`。如果从 v7.1.0 之前版本的集群升级至 v7.1.0 及之后的版本，该默认值不发生变化。

### `hot-regions-write-interval` <span class="version-mark">从 v5.4.0 版本开始引入</span>

* 设置 PD 存储 Hot Region 信息时间间隔。
* 默认值：10m

> **注意：**
>
> Hot Region 的信息一般 3 分钟更新一次。如果设置时间间隔小于 3 分钟，中间部分的更新可能没有意义。

### `hot-regions-reserved-days` <span class="version-mark">从 v5.4.0 版本开始引入</span>

* 设置 PD 保留的 Hot Region 信息的最长时间。单位为天。
* 默认值: 7

### `enable-heartbeat-breakdown-metrics` <span class="version-mark">从 v8.0.0 版本开始引入</span>

+ 是否开启 Region 心跳指标拆分，用于统计 Region 心跳处理各阶段所消耗的时间，便于在监控上进行分析。
+ 默认值：true

### `enable-heartbeat-concurrent-runner` <span class="version-mark">从 v8.0.0 版本开始引入</span>

+ 是否开启 Region 心跳异步并发处理功能。开启后会使用独立的执行器异步并发处理 Region 心跳请求，可提高心跳处理吞吐量，降低延迟。
+ 默认值：true

## replication

副本相关的配置项。

### `max-replicas`

+ 所有副本数量，即 leader 与 follower 数量之和。默认为 `3`，即 1 个 leader 和 2 个 follower。当此配置被在线修改后，PD 会在后台通过调度使得 Region 的副本数量符合配置。
+ 默认值：3

### `location-labels`

+ TiKV 集群的拓扑信息。
+ 默认值：[]
+ [配置集群拓扑](/schedule-replicas-by-topology-labels.md)

### `isolation-level`

+ TiKV 集群的最小强制拓扑隔离级别。
+ 默认值：""
+ [配置集群拓扑](/schedule-replicas-by-topology-labels.md)

### `strictly-match-label`

+ 打开强制 TiKV Label 和 PD 的 location-labels 是否匹配的检查
+ 默认值：false

### `enable-placement-rules`

+ 打开 `placement-rules`
+ 默认值：true
+ 参考 [Placement Rules 使用文档](/configure-placement-rules.md)

### `store-limit-version` <span class="version-mark">从 v7.1.0 版本开始引入</span>

+ 设置 `store limit` 工作模式
+ 默认值：v1
+ 可选值：
    + v1：在 v1 模式下，你可以手动修改 `store limit` 以限制单个 TiKV 调度速度。
    + v2：在 v2 模式下，你无需关注 `store limit` 值，PD 将根据 TiKV Snapshot 执行情况动态调整 TiKV 调度速度。详情请参考 [Store Limit v2 原理](/configure-store-limit.md#store-limit-v2-原理)。

## label-property（已废弃）

标签相关的配置项，只支持 `reject-leader` 类型。

> **注意：**
>
> 标签相关的配置项已从 v5.2 开始废弃，建议使用 [Placement Rules](/configure-placement-rules.md#场景二5-副本按-2-2-1-的比例放置在-3-个数据中心且第-3-个中心不产生-leader) 设置副本策略。

### `key`（已废弃）

+ 拒绝 leader 的 store 带有的 label key。
+ 默认值：""

### `value`（已废弃）

+ 拒绝 leader 的 store 带有的 label value。
+ 默认值：""

## dashboard

PD 中内置的 [TiDB Dashboard](/dashboard/dashboard-intro.md) 相关配置项。

### `disable-custom-prom-addr`

+ 是否禁止在 [TiDB Dashboard](/dashboard/dashboard-intro.md) 中配置自定义的 Prometheus 数据源地址。
+ 默认值：`false`
+ 当配置为 `true` 时，如果在 TiDB Dashboard 中配置自定义的 Prometheus 数据源地址，TiDB Dashboard 会报错。

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
+ 默认值："/dashboard"
+ 若不通过反向代理访问 TiDB Dashboard，**请勿配置该项**，否则可能导致 TiDB Dashboard 无法正常访问。关于该配置的详细使用场景，参见[通过反向代理使用 TiDB Dashboard](/dashboard/dashboard-ops-reverse-proxy.md)。

### `enable-telemetry`

> **警告：**
>
> 从 TiDB v8.1.0 开始，TiDB Dashboard 已移除遥测功能，该配置项已不再生效。保留该配置项仅用于与之前版本兼容。

+ 在 v8.1.0 之前，用于控制是否启用 TiDB Dashboard 遥测功能。
+ 默认值：false

## `replication-mode`

Region 同步模式相关的配置项。更多详情，请参阅[启用自适应同步模式](/two-data-centers-in-one-city-deployment.md#启用自适应同步模式)。

## controller

PD 中内置的 [Resource Control](/tidb-resource-control-ru-groups.md) 相关的配置项。

### `degraded-mode-wait-duration`

+ 触发降级模式需要等待的时间。降级模式是指在 Local Token Bucket (LTB) 和 Global Token Bucket (GTB) 失联的情况下，LTB 将回退到默认的资源组配置，不再有 GTB 授权 token，从而保证在网络隔离或者异常情况下，服务不受影响。
+ 默认值: 0s
+ 默认为不开启降级模式

### `request-unit`

下面是 [Request Unit (RU)](/tidb-resource-control-ru-groups.md#什么是-request-unit-ru) 相关的配置项。

#### `read-base-cost`

+ 每次读请求转换成 RU 的基准系数
+ 默认值：0.125

#### `write-base-cost`

+ 每次写请求转换成 RU 的基准系数
+ 默认值: 1

#### `read-cost-per-byte`

+ 读流量转换成 RU 的基准系数
+ 默认值: 1/(64 * 1024)
+ 1 RU = 64 KiB 读取字节

#### `write-cost-per-byte`

+ 写流量转换成 RU 的基准系数
+ 默认值: 1/1024
+ 1 RU = 1 KiB 写入字节

#### `read-cpu-ms-cost`

+ CPU 转换成 RU 的基准系数
+ 默认值: 1/3
+ 1 RU = 3 毫秒 CPU 时间
