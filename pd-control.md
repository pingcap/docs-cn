---
title: PD Control 使用说明
summary: PD Control 是 PD 的命令行工具，用于获取集群状态信息和调整集群。
---

# PD Control 使用说明

PD Control 是 PD 的命令行工具，用于获取集群状态信息和调整集群。

## 安装方式

> **注意：**
>
> 建议使用的 Control 工具版本与集群版本保持一致。

### 使用 TiUP

可直接通过 `tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> [-i]` 使用。

### 下载安装包

如需下载最新版本的 `pd-ctl`，直接下载 TiDB 安装包即可。`pd-ctl` 位于 TiDB 安装包的 `ctl-{version}-linux-{arch}.tar.gz` 包中。

| 安装包                                                                    | 操作系统 | 架构  | SHA256 校验和                                                    |
| :------------------------------------------------------------------------ | :------- | :---- | :--------------------------------------------------------------- |
| `https://download.pingcap.org/tidb-community-server-{version}-linux-amd64.tar.gz` (pd-ctl) | Linux    | amd64 | `https://download.pingcap.org/tidb-community-server-{version}-linux-amd64.tar.gz.sha256` |
| `https://download.pingcap.org/tidb-community-server-{version}-linux-arm64.tar.gz` (pd-ctl) | Linux | arm64 | `https://download.pingcap.org/tidb-community-server-{version}-linux-arm64.tar.gz.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 TiDB 的版本号。例如，amd64 架构的 `v8.5.1` 版本的下载链接为 `https://download.pingcap.org/tidb-community-server-v8.5.1-linux-amd64.tar.gz`。

### 源码编译

1. [Go](https://golang.org/) 1.23 或以上版本
2. 在 PD 项目根目录使用 `make` 或者 `make pd-ctl` 命令进行编译，生成 bin/pd-ctl

## 简单例子

单命令模式：

```bash
tiup ctl:v<CLUSTER_VERSION> pd store -u http://127.0.0.1:2379
```

交互模式：

```bash
tiup ctl:v<CLUSTER_VERSION> pd -i -u http://127.0.0.1:2379
```

使用环境变量：

```bash
export PD_ADDR=http://127.0.0.1:2379 &&
tiup ctl:v<CLUSTER_VERSION> pd
```

使用 TLS 加密：

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u https://127.0.0.1:2379 --cacert="path/to/ca" --cert="path/to/cert" --key="path/to/key"
```

## 命令行参数 (flags)

### `--cacert`

- 指定 PEM 格式的受信任 CA 证书的文件路径
- 默认值：""

### `--cert`

- 指定 PEM 格式的 SSL 证书的文件路径
- 默认值：""

### `--detach` / `-d`

+ 使用单命令行模式（不进入 readline）
+ 默认值：true

### `--help` / `-h`

+ 输出帮助信息
+ 默认值：false

### `--interact`/`-i`

+ 使用交互模式（进入 readline）
+ 默认值：false

### `--key`

- 指定 PEM 格式的 SSL 证书密钥文件路径，即 `--cert` 所指定的证书的私钥
- 默认值：""

### `--pd`/`-u`

+ 指定 PD 的地址
+ 默认地址：`http://127.0.0.1:2379`
+ 环境变量：`PD_ADDR`

### `--version`/`-V`

- 打印版本信息并退出
- 默认值：false

## 命令 (command)

### cluster

用于显示集群基本信息。

示例：

```bash
cluster
```

```
{
  "id": 6493707687106161130,
  "max_peer_count": 3
}
```

### `config [show | set <option> <value> | placement-rules]`

用于显示或调整配置信息。示例如下。

显示 scheduling 的相关 config 信息：

```bash
config show
```

```
{
  "replication": {
    "enable-placement-rules": "true",
    "isolation-level": "",
    "location-labels": "",
    "max-replicas": 3,
    "strictly-match-label": "false"
  },
  "schedule": {
    "enable-cross-table-merge": "true",
    "high-space-ratio": 0.7,
    "hot-region-cache-hits-threshold": 3,
    "hot-region-schedule-limit": 4,
    "leader-schedule-limit": 4,
    "leader-schedule-policy": "count",
    "low-space-ratio": 0.8,
    "max-merge-region-keys": 540000,
    "max-merge-region-size": 54,
    "max-pending-peer-count": 64,
    "max-snapshot-count": 64,
    "max-store-down-time": "30m0s",
    "merge-schedule-limit": 8,
    "patrol-region-interval": "10ms",
    "region-schedule-limit": 2048,
    "region-score-formula-version": "v2",
    "replica-schedule-limit": 64,
    "scheduler-max-waiting-operator": 5,
    "split-merge-interval": "1h0m0s",
    "tolerant-size-ratio": 0
  }
}
```

显示所有的 config 信息：

```bash
config show all
```

显示 replication 的相关 config 信息：

```bash
config show replication
```

```
{
  "max-replicas": 3,
  "isolation-level": "",
  "location-labels": "",
  "strictly-match-label": "false",
  "enable-placement-rules": "true"
}
```

显示目前集群版本，是目前集群 TiKV 节点的最低版本，并不对应 binary 的版本：

```bash
config show cluster-version
```

```
"8.5.1"
```

- `max-snapshot-count` 控制单个 store 最多同时接收或发送的 snapshot 数量，调度受制于这个配置来防止抢占正常业务的资源。当需要加快补副本或 balance 速度时可以调大这个值。

    设置最大 snapshot 为 `64`：

    ```bash
    config set max-snapshot-count 64
    ```

- `max-pending-peer-count` 控制单个 store 的 pending peer 上限，调度受制于这个配置来防止在部分节点产生大量日志落后的 Region。需要加快补副本或 balance 速度可以适当调大这个值，设置为 0 则表示不限制。

    设置最大 pending peer 数量为 `64`：

    ```bash
    config set max-pending-peer-count 64
    ```

- `max-merge-region-size` 控制 Region Merge 的 size 上限（单位是 MiB）。当 Region Size 大于指定值时 PD 不会将其与相邻的 Region 合并。设置为 `0` 表示不开启 Region Merge 功能。

    设置 Region Merge 的 size 上限为 16 MiB：

    ```bash
    config set max-merge-region-size 16
    ```

- `max-merge-region-keys` 控制 Region Merge 的 keyCount 上限。当 Region KeyCount 大于指定值时 PD 不会将其与相邻的 Region 合并。

    设置 Region Merge 的 keyCount 上限为 `50000`：

    ```bash
    config set max-merge-region-keys 50000
    ```

- `split-merge-interval` 控制对同一个 Region 做 `split` 和 `merge` 操作的间隔，即对于新 `split` 的 Region 一段时间内不会被 `merge`。

    设置 `split` 和 `merge` 的间隔为 `24h`（1 天）：

    ```bash
    config set split-merge-interval 24h
    ```

- `enable-one-way-merge` 用于控制是否只允许和相邻的后一个 Region 进行合并。当设置为 `false` 时，PD 允许与相邻的前后 Region 进行合并。

    设置只允许和相邻的后一个 Region 合并：

    ```bash
    config set enable-one-way-merge true
    ```

- `enable-cross-table-merge` 用于开启跨表 Region 的合并。当设置为 `false` 时，PD 不会合并不同表的 Region。该选项只在键类型为 "table" 时生效。

    设置允许跨表合并：

    ```bash
    config set enable-cross-table-merge true
    ```

- `key-type` 用于指定集群的键编码类型。支持的类型有 `["table", "raw", "txn"]`，默认值为 "table"。

    - 如果集群中不存在 TiDB 实例，`key-type` 的值为 "raw" 或 "txn"。此时，无论 `enable-cross-table-merge` 设置为何，PD 均可以跨表合并 Region。
    - 如果集群中存在 TiDB 实例，`key-type` 的值应当为 "table"。此时，`enable-cross-table-merge` 的设置决定了 PD 是否能跨表合并 Region。如果 `key-type` 的值为 "raw"，placement rules 不生效。

    启用跨表合并：

    ```bash
    config set key-type raw
    ```

- `region-score-formula-version` 用于设置 Region 算分公式的版本，支持的值有 `["v1", "v2"]`。v2 版本公式有助于减少上下线等场景下冗余的 balance Region 调度。

    开启 v2 版本 Region 算分公式：

    ```bash
    config set region-score-formula-version v2
    ```

- `patrol-region-interval` 控制 checker 检查 Region 健康状态的运行频率，越短则运行越快，通常状况不需要调整。

    设置 checker 的运行频率为 10 毫秒：

    ```bash
    config set patrol-region-interval 10ms
    ```

- `patrol-region-worker-count` 控制 checker 检查 Region 健康状态时，创建 [operator](/glossary.md#operator) 的并发数。通常情况下，无需调整此配置项。将该配置项设置为大于 1 将启用并发检查。目前该功能为实验特性，不建议在生产环境中使用。

    设置 checker 的并发数为 `2`：

    ```bash
    config set patrol-region-worker-count 2
    ```

- `max-store-down-time` 为 PD 认为失联 store 无法恢复的时间，当超过指定的时间没有收到 store 的心跳后，PD 会在其他节点补充副本。

    设置 store 心跳丢失 `30` 分钟开始补副本：

    ```bash
    config set max-store-down-time 30m
    ```

- `max-store-preparing-time` 控制 store 上线阶段的最长等待时间。在 store 的上线阶段，PD 可以查询该 store 的上线进度。当超过该配置项指定的时间后，PD 会认为该 store 已完成上线，无法再次查询这个 store 的上线进度，但是不影响 Region 向这个新上线 store 的迁移。通常用户无需修改该配置项。

    设置 store 上线阶段最多等待 `4` 小时：

    ```bash
    config set max-store-preparing-time 4h
    ```

- 通过调整 `leader-schedule-limit` 可以控制同时进行 leader 调度的任务个数。这个值主要影响 *leader balance* 的速度，值越大调度得越快，设置为 0 则关闭调度。Leader 调度的开销较小，需要的时候可以适当调大。

    最多同时进行 `4` 个 leader 调度：

    ```bash
    config set leader-schedule-limit 4
    ```

- 通过调整 `region-schedule-limit` 可以控制同时进行 Region 调度的任务个数。这个值可以避免创建过多的 Region balance operator。默认值为 `2048`，对所有大小的集群都足够。设置为 `0` 则关闭调度。Region 调度的速度通常受到 `store-limit` 的限制，但除非你熟悉该设置，否则不推荐自定义该参数。

    最多同时进行 `2` 个 Region 调度：

    ```bash
    config set region-schedule-limit 2
    ```

- 通过调整 `replica-schedule-limit` 可以控制同时进行 replica 调度的任务个数。这个值主要影响节点挂掉或者下线的时候进行调度的速度，值越大调度得越快，设置为 0 则关闭调度。Replica 调度的开销较大，所以这个值不宜调得太大。注意：该参数通常保持为默认值。如需调整，需要根据实际情况反复尝试设置该值大小。

    最多同时进行 `4` 个 replica 调度：

    ```bash
    config set replica-schedule-limit 4
    ```

- `merge-schedule-limit` 控制同时进行的 Region Merge 调度的任务，设置为 0 则关闭 Region Merge。Merge 调度的开销较大，所以这个值不宜调得过大。注意：该参数通常保持为默认值。如需调整，需要根据实际情况反复尝试设置该值大小。

    最多同时进行 `16` 个 merge 调度：

    ```bash
    config set merge-schedule-limit 16
    ```

- `hot-region-schedule-limit` 控制同时进行的 Hot Region 调度的任务，设置为 0 则关闭调度。这个值不宜调得过大，否则可能对系统性能造成影响。注意：该参数通常保持为默认值。如需调整，需要根据实际情况反复尝试设置该值大小。

    最多同时进行 `4` 个 Hot Region 调度：

    ```bash
    config set hot-region-schedule-limit 4
    ```

- `hot-region-cache-hits-threshold` 用于设置识别热点 Region 所需的分钟数，只有 Region 处于热点状态持续时间超过该分钟数后，才能参与热点调度。

- `tolerant-size-ratio` 控制 balance 缓冲区大小。当两个 store 的 leader 或 Region 的得分差距小于指定倍数的 Region size 时，PD 会认为此时 balance 达到均衡状态。

    设置缓冲区为约 `20` 倍平均 RegionSize：

    ```bash
    config set tolerant-size-ratio 20
    ```

- `low-space-ratio` 用于设置 store 空间不足的阈值。当节点的空间占用比例超过指定值时，PD 会尽可能避免往对应节点迁移数据，同时主要针对剩余空间大小进行调度，避免对应节点磁盘空间被耗尽。

    设置空间不足阈值为 `0.9`：

    ```bash
    config set low-space-ratio 0.9
    ```

- `high-space-ratio` 用于设置 store 空间充裕的阈值，此配置仅的在 `region-score-formula-version = v1` 时生效。当节点的空间占用比例小于指定值时，PD 调度时会忽略剩余空间这个指标，主要针对实际数据量进行均衡。

    设置空间充裕阈值为 `0.5`：

    ```bash
    config set high-space-ratio 0.5
    ```

- `cluster-version` 集群的版本，用于控制某些 Feature 是否开启，处理兼容性问题。通常是集群正常运行的所有 TiKV 节点中的最低版本，需要回滚到更低的版本时才进行手动设置。

    设置 cluster version 为 8.5.1：

    ```bash
    config set cluster-version 8.5.1
    ```

- `leader-schedule-policy` 用于选择 Leader 的调度策略，可以选择按照 `size` 或者 `count` 来进行调度。

- `scheduler-max-waiting-operator` 用于控制每个调度器同时存在的 operator 的个数。

- `enable-remove-down-replica` 用于开启自动删除 DownReplica 的特性。当设置为 false 时，PD 不会自动清理宕机状态的副本。

- `enable-replace-offline-replica` 用于开启迁移 OfflineReplica 的特性。当设置为 false 时，PD 不会迁移下线状态的副本。

- `enable-make-up-replica` 用于开启补充副本的特性。当设置为 false 时，PD 不会为副本数不足的 Region 补充副本。

- `enable-remove-extra-replica` 用于开启删除多余副本的特性。当设置为 false 时，PD 不会为副本数过多的 Region 删除多余副本。

- `enable-location-replacement` 用于开启隔离级别检查。当设置为 false 时，PD 不会通过调度来提升 Region 副本的隔离级别。

- `enable-debug-metrics` 用于开启 debug 的 metrics。当设置为 true 时，PD 会开启一些 metrics，比如 `balance-tolerant-size` 等。

- `enable-placement-rules` 用于开启 placement rules，在 v5.0 及以上的版本默认开启。

- `store-limit-mode` 用于控制 store 限速机制的模式。主要有两种模式：`auto` 和 `manual`。`auto` 模式下会根据 load 自动进行平衡调整（弃用）。

- `store-limit-version` 用于设置 `store limit` 限制模式，目前提供两种方式：`v1` 和 `v2`。默认值为 `v1`。在 `v1` 模式下，你可以手动修改 `store limit` 以限制单个 TiKV 调度速度。在 `v2` 模式下，你无需关注 `store limit` 值，PD 将根据 TiKV Snapshot 执行情况动态调整 TiKV 调度速度。详情请参考 [Store Limit v2 原理](/configure-store-limit.md#store-limit-v2-原理)。

    ```bash
    config set store-limit-version v2       // 使用 Store Limit v2
    ```

- PD 会对流量信息的末尾数字进行四舍五入处理，减少 Region 流量信息变化引起的统计信息更新。该配置项用于指定对 Region 流量信息的末尾进行四舍五入的位数。例如流量 `100512` 会归约到 `101000`。默认值为 `3`。该配置替换了 `trace-region-flow`。

    示例：将 `flow-round-by-digit` 的值设为 `4`：

    ```bash
    config set flow-round-by-digit 4
    ```

### `config [show | set service-middleware <option> [<key> <value> | <label> <qps|concurrency> <value>]]`

`service-middleware` 是 PD 中的一个配置模块，主要用于管理和控制 PD 服务的中间件功能，如审计日志、请求速率限制和并发限制等。从 v8.5.0 起，PD 支持通过 `pd-ctl` 修改 `service-middleware` 的以下配置：

- `audit`：控制是否开启 PD 处理 HTTP 请求的审计日志（默认开启）。开启时，`service-middleware` 会在 PD 日志中记录 HTTP 请求的相关信息。
- `rate-limit`：用于限制 PD 处理 HTTP API 请求的最大速率和最大并发。
- `grpc-rate-limit`：用于限制 PD 处理 gRPC API 请求的最大速率和最大并发。

> **注意：**
>
> 为了避免请求速率限制和并发限制对 PD 性能的影响，不建议修改 `service-middleware` 中的配置。

显示 `service-middleware` 的相关 config 信息：

```bash
config show service-middleware
```

```bash
{
  "audit": {
    "enable-audit": "true"
  },
  "rate-limit": {
    "enable-rate-limit": "true",
    "limiter-config": {}
  },
  "grpc-rate-limit": {
    "enable-grpc-rate-limit": "true",
    "grpc-limiter-config": {}
  }
}
```

`service-middleware audit` 用于开启或关闭 HTTP 请求的日志审计功能。以关闭该功能为例：

```bash
config set service-middleware audit enable-audit false
```

`service-middleware grpc-rate-limit` 用于控制以下 gRPC API 请求的最大速率和并发度：

- `GetRegion`：获取指定 Region 的信息
- `GetStore`：获取指定 Store 的信息
- `GetMembers`：获取 PD 集群成员的信息

控制某个 gRPC API 请求的最大速率，以 `GetRegion` API 请求为例：

```bash
config set service-middleware grpc-rate-limit GetRegion qps 100
```

控制某个 gRPC API 请求的最大并发度，以 `GetRegion` API 请求为例：

```bash
config set service-middleware grpc-rate-limit GetRegion concurrency 10
```

查看修改后的配置：

```bash
config show service-middleware
```

```bash
{
  "audit": {
    "enable-audit": "true"
  },
  "rate-limit": {
    "enable-rate-limit": "true",
    "limiter-config": {}
  },
  "grpc-rate-limit": {
    "enable-grpc-rate-limit": "true",
    "grpc-limiter-config": {
      "GetRegion": {
        "QPS": 100,
        "QPSBurst": 100, // 根据 QPS 设置自动调整，仅作展示
        "ConcurrencyLimit": 10
      }
    }
  }
}
```

重置上述设置：

```bash
config set service-middleware grpc-rate-limit GetRegion qps 0
config set service-middleware grpc-rate-limit GetRegion concurrency 0
```

`service-middleware rate-limit` 用于控制以下 HTTP API 请求的最大速率和并发度：

- `GetRegion`：获取指定 Region 的信息
- `GetStore`：获取指定 Store 的信息

控制某个 HTTP API 请求的最大速率，以 `GetRegion` API 请求为例：

```bash
config set service-middleware rate-limit GetRegion qps 100
```

控制某个 HTTP API 请求的最大并发度，以 `GetRegion` API 请求为例：

```bash
config set service-middleware rate-limit GetRegion concurrency 10
```

重置上述设置：

```bash
config set service-middleware rate-limit GetRegion qps 0
config set service-middleware rate-limit GetRegion concurrency 0
```

### `config placement-rules [disable | enable | load | save | show | rule-group]`

关于 `config placement-rules` 的具体用法，参考 [Placement Rules 使用文档](/configure-placement-rules.md#配置规则操作步骤)。

### health

用于显示集群健康信息。示例如下。

显示健康信息：

```bash
health
```

```
[
  {
    "name": "pd",
    "member_id": 13195394291058371180,
    "client_urls": [
      "http://127.0.0.1:2379"
      ......
    ],
    "health": true
  }
  ......
]
```

### `hot [read | write | store| history <start_time> <end_time> [<key> <value>]]`

用于显示集群热点信息。示例如下。

显示读热点信息：

```bash
hot read
```

显示写热点信息：

```bash
hot write
```

显示所有 store 的读写信息：

```bash
hot store
```

显示历史读写热点信息:

```
hot history startTime endTime [ <name> <value> ]
```

例如查询时间 `1629294000000` 到 `1631980800000` （毫秒）之间的历史热点 Region 信息:

```
hot history 1629294000000 1631980800000
```

```
{
  "history_hot_region": [
    {
      "update_time": 1630864801948,
      "region_id": 103,
      "peer_id": 1369002,
      "store_id": 3,
      "is_leader": true,
      "is_learner": false,
      "hot_region_type": "read",
      "hot_degree": 152,
      "flow_bytes": 0,
      "key_rate": 0,
      "query_rate": 305,
      "start_key": "7480000000000000FF5300000000000000F8",
      "end_key": "7480000000000000FF5600000000000000F8"
    },
    ...
  ]
}
```

对于参数的值为数组的请用 `x, y, ...` 的形式进行参数值的设置，所有支持的参数如下所示:

```
hot history 1629294000000 1631980800000 hot_region_type read region_id 1,2,3 store_id 1,2,3 peer_id 1,2,3 is_leader true is_learner true
```

```
{
  "history_hot_region": [
    {
      "update_time": 1630864801948,
      "region_id": 103,
      "peer_id": 1369002,
      "store_id": 3,
      "is_leader": true,
      "is_learner": false,
      "hot_region_type": "read",
      "hot_degree": 152,
      "flow_bytes": 0,
      "key_rate": 0,
      "query_rate": 305,
      "start_key": "7480000000000000FF5300000000000000F8",
      "end_key": "7480000000000000FF5600000000000000F8"
    },
    ...
  ]
}
```

### `label [store <name> <value>]`

用于显示集群标签信息。示例如下。

显示所有 label：

```bash
label
```

显示所有包含 label 为 "zone":"cn" 的 store：

```bash
label store zone cn
```

### `member [delete | leader_priority | leader [show | resign | transfer <member_name>]]`

> **注意：**
>
> 不要使用 `member delete` 命令在生产环境中缩容 PD 节点。如需缩容 PD 节点，请参考[使用 TiUP 扩容缩容 TiDB 集群](/scale-tidb-using-tiup.md)和[手动扩缩容 Kubernetes 上的 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/scale-a-tidb-cluster/)。

用于显示 PD 成员信息，删除指定成员，设置成员的 leader 优先级。示例如下。

显示所有成员的信息：

```bash
member
```

```
{
  "header": {......},
  "members": [......],
  "leader": {......},
  "etcd_leader": {......},
}
```

下线 `pd2`：

```bash
member delete name pd2
```

```
Success!
```

使用 ID 下线节点：

```bash
member delete id 1319539429105371180
```

```
Success!
```

显示 leader 的信息：

```bash
member leader show
```

```
{
  "name": "pd",
  "member_id": 13155432540099656863,
  "peer_urls": [......],
  "client_urls": [......]
}
```

将 leader 从当前成员移走：

```bash
member leader resign
```

```
......
```

将 leader 迁移至指定成员：

```bash
member leader transfer pd3
```

```
......
```

指定 PD leader 的优先级：

```bash
member leader_priority  pd-1 4
member leader_priority  pd-2 3
member leader_priority  pd-3 2
member leader_priority  pd-4 1
member leader_priority  pd-5 0
```

> **注意：**
>
> 在可用的 PD 节点中，优先级数值最大的节点会直接当选 leader。

### `operator [check | show | add | remove]`

用于显示和控制调度操作。

示例：

```bash
>> operator show                                        // 显示所有的 operators
>> operator show admin                                  // 显示所有的 admin operators
>> operator show leader                                 // 显示所有的 leader operators
>> operator show region                                 // 显示所有的 Region operators
>> operator add add-peer 1 2                            // 在 store 2 上新增 Region 1 的一个副本
>> operator add add-learner 1 2                         // 在 store 2 上新增 Region 1 的一个 learner 副本
>> operator add remove-peer 1 2                         // 移除 store 2 上的 Region 1 的一个副本
>> operator add transfer-leader 1 2                     // 把 Region 1 的 leader 调度到 store 2
>> operator add transfer-region 1 2 3 4                 // 把 Region 1 调度到 store 2,3,4
>> operator add transfer-peer 1 2 3                     // 把 Region 1 在 store 2 上的副本调度到 store 3
>> operator add merge-region 1 2                        // 将 Region 1 与 Region 2 合并
>> operator add split-region 1 --policy=approximate     // 将 Region 1 对半拆分成两个 Region，基于粗略估计值
>> operator add split-region 1 --policy=scan            // 将 Region 1 对半拆分成两个 Region，基于精确扫描值
>> operator remove 1                                    // 把 Region 1 的调度操作删掉
>> operator check 1                                     // 查看 Region 1 相关 operator 的状态
```

其中，Region 的分裂都是尽可能地从靠近中间的位置开始。对这个位置的选择支持两种策略，即 scan 和 approximate。它们之间的区别是，前者通过扫描这个 Region 的方式来确定中间的 key，而后者是通过查看 SST 文件中记录的统计信息，来得到近似的位置。一般来说，前者更加精确，而后者消耗更少的 I/O，可以更快地完成。

### `ping`

用于显示`ping` PD 所需要花费的时间

示例：

```bash
ping
```

```
time: 43.12698ms
```

### `region <region_id> [--jq="<query string>"]`

用于显示 Region 信息。使用 jq 格式化输出请参考 [jq 格式化 json 输出示例](#jq-格式化-json-输出示例)。示例如下。

显示所有 Region 信息：

```bash
region
```

```
{
  "count": 1,
  "regions": [......]
}
```

显示 Region ID 为 2 的信息：

```bash
region 2
```

```
{
  "id": 2,
  "start_key": "7480000000000000FF1D00000000000000F8",
  "end_key": "7480000000000000FF1F00000000000000F8",
  "epoch": {
    "conf_ver": 1,
    "version": 15
  },
  "peers": [
    {
      "id": 40,
      "store_id": 3
    }
  ],
  "leader": {
    "id": 40,
    "store_id": 3
  },
  "written_bytes": 0,
  "read_bytes": 0,
  "written_keys": 0,
  "read_keys": 0,
  "approximate_size": 1,
  "approximate_keys": 0
}
```

### `region key [--format=raw|encode|hex] <key>`

用于查询某个 key 位于哪一个 Region 上，支持 raw、encoding 和 hex 格式。使用 encoding 格式时，key 需要使用单引号。

Hex 格式（默认）示例：

```bash
region key 7480000000000000FF1300000000000000F8
{
  "region": {
    "id": 2,
    ......
  }
}
```

Raw 格式示例：

```bash
region key --format=raw abc
```

```
{
  "region": {
    "id": 2,
    ......
  }
}
```

Encoding 格式示例：

```bash
region key --format=encode 't\200\000\000\000\000\000\000\377\035_r\200\000\000\000\000\377\017U\320\000\000\000\000\000\372'
```

```
{
  "region": {
    "id": 2,
    ......
  }
}
```

### `region scan`

用于获取所有 Region。

示例：

```bash
region scan
```

```
{
  "count": 20,
  "regions": [......],
}
```

### `region sibling <region_id>`

用于查询某个 Region 相邻的 Region。

示例：

```bash
region sibling 2
```

```
{
  "count": 2,
  "regions": [......],
}
```

### `region keys [--format=raw|encode|hex] <start_key> <end_key> <limit>`

用于查询某个 key 范围内的所有 Region。支持不带 `endKey` 的范围。`limit` 的默认值是 `16`，设为 `-1` 则表示无数量限制。示例如下：

显示从 a 开始的所有 Region 信息，数量上限为 `16`：

```bash
region keys --format=raw a
```

```
{
  "count": 16,
  "regions": [......],
}
```

显示 [a, z) 范围内的所有 Region 信息，数量上限为 `16`：

```bash
region keys --format=raw a z
```

```
{
  "count": 16,
  "regions": [......],
}
```

显示 [a, z) 范围内的所有 Region 信息，无数量上限：

```bash
region keys --format=raw a z -1
```

```
{
  "count": ...,
  "regions": [......],
}
```

显示从 a 开始的所有 Region 信息，数量上限为 `20`：

```bash
region keys --format=raw a "" 20
```

```
{
  "count": 20,
  "regions": [......],
}
```

### `region store <store_id>`

用于查询某个 store 上面所有的 Region。

示例：

```bash
region store 2
```

```
{
  "count": 10,
  "regions": [......],
}
```

### `region topread [limit]`

用于查询读流量最大的 Region。limit 的默认值是 `16`。

示例：

```bash
region topread
```

```
{
  "count": 16,
  "regions": [......],
}
```

### `region topwrite [limit]`

用于查询写流量最大的 Region。limit 的默认值是 `16`。

示例：

```bash
region topwrite
```

```
{
  "count": 16,
  "regions": [......],
}
```

### `region topconfver [limit]`

用于查询 conf version 最大的 Region。limit 的默认值是 `16`。

示例：

```bash
region topconfver
```

```
{
  "count": 16,
  "regions": [......],
}
```

### `region topversion [limit]`

用于查询 version 最大的 Region。limit 的默认值是 `16`。

示例：

```bash
region topversion
```

```
{
  "count": 16,
  "regions": [......],
}
```

### `region topsize [limit]`

用于查询 approximate size 最大的 Region。limit 的默认值是 `16`。

示例：

```bash
region topsize
```

```
{
  "count": 16,
  "regions": [......],
}
```

### `region check [miss-peer | extra-peer | down-peer | pending-peer | offline-peer | empty-region | hist-size | hist-keys] [--jq="<query string>"]`

用于查询处于异常状态的 Region，使用 jq 格式化输出请参考 [jq 格式化 JSON 输出示例](#jq-格式化-json-输出示例)。

各类型的意义如下：

- miss-peer：缺副本的 Region
- extra-peer：多副本的 Region
- down-peer：有副本状态为 Down 的 Region
- pending-peer：有副本状态为 Pending 的 Region

示例：

```bash
region check miss-peer
```

```
{
  "count": 2,
  "regions": [......],
}
```

### `resource-manager [command]`

#### 查看资源管控 (Resource Control) 的 controller 配置

```bash
resource-manager config controller show
```

```bash
{
    "degraded-mode-wait-duration": "0s",
    "ltb-max-wait-duration": "30s", 
    "request-unit": {          # RU 的配置，请勿修改
        "read-base-cost": 0.125,
        "read-per-batch-base-cost": 0.5,
        "read-cost-per-byte": 0.0000152587890625,
        "write-base-cost": 1,
        "write-per-batch-base-cost": 1,
        "write-cost-per-byte": 0.0009765625,
        "read-cpu-ms-cost": 0.3333333333333333
    },
    "enable-controller-trace-log": "false"
}
```

- `ltb-max-wait-duration`：本地令牌桶 (Local Token Bucket, LTB) 的最大等待时间。默认值为 `30s`，取值范围为 `[0, 24h]`。如果 SQL 请求预估消耗的 [Request Unit (RU)](/tidb-resource-control-ru-groups.md#什么是-request-unit-ru) 超过了当前 LTB 积累的 RU，则需要等待一定时间。如果预估等待时间超过了此最大等待时间，则会提前向应用返回错误 [`ERROR 8252 (HY000) : Exceeded resource group quota limitation`](/error-codes.md)。增大该值可以减少某些突发并发增加、大事务和大查询的情况下容易报错 `ERROR 8252` 的问题。
- `enable-controller-trace-log`：controller 诊断日志开关。

#### 修改 Resource Control 的 controller 配置

修改 `ltb-max-wait-duration` 的方法如下：

```bash
pd-ctl resource-manager config controller set ltb-max-wait-duration 30m
```

### `scheduler [show | add | remove | pause | resume | config | describe]`

用于显示和控制调度策略。

示例：

```bash
>> scheduler show                                         // 显示所有已经创建的 schedulers
>> scheduler add grant-leader-scheduler 1                 // 把 store 1 上的所有 Region 的 leader 调度到 store 1
>> scheduler add evict-leader-scheduler 1                 // 把 store 1 上的所有 Region 的 leader 从 store 1 调度出去
>> scheduler config evict-leader-scheduler                // v4.0.0 起，展示该调度器具体在哪些 store 上
>> scheduler config evict-leader-scheduler add-store 2    // 为 store 2 添加 leader 驱逐调度
>> scheduler config evict-leader-scheduler delete-store 2 // 为 store 2 移除 leader 驱逐调度
>> scheduler add evict-slow-store-scheduler               // 当有且仅有一个 slow store 时将该 store 上的所有 Region 的 leader 驱逐出去
>> scheduler remove grant-leader-scheduler-1              // 把对应的调度器删掉，`-1` 对应 store ID
>> scheduler pause balance-region-scheduler 10            // 暂停运行 balance-region 调度器 10 秒
>> scheduler pause all 10                                 // 暂停运行所有的调度器 10 秒
>> scheduler resume balance-region-scheduler              // 继续运行 balance-region 调度器
>> scheduler resume all                                   // 继续运行所有的调度器
>> scheduler config balance-hot-region-scheduler          // 显示 balance-hot-region 调度器的配置
>> scheduler describe balance-region-scheduler            // 显示 balance-region 的运行状态和相应的诊断信息
```

### `scheduler describe balance-region-scheduler`

用于查看 `balance-region-scheduler` 的运行状态和相应的诊断信息。

从 TiDB v6.3.0 起，PD 为 `balance-region-scheduler` 和 `balance-leader-scheduler` 提供了运行状态和简要诊断信息的功能，其余 scheduler 和 checker 暂未支持。你可以通过 `pd-ctl` 修改 [`enable-diagnostic`](/pd-configuration-file.md#enable-diagnostic-从-v630-版本开始引入) 配置项开启该功能。

调度器运行状态有以下几种类型：

- `disabled`：表示当前调度器不可用或被移除。
- `paused`：表示当前调度器暂停工作。
- `scheduling`：表示当前调度器正在生成调度。
- `pending`：表示当前调度器无法产生调度。`pending` 状态的调度器，会返回一个概览信息，来帮助用户诊断。概览信息包含了 store 的一些状态信息，解释了它们为什么不能被选中进行调度。
- `normal`：表示当前调度器无需进行调度。

### `scheduler config balance-leader-scheduler`

用于查看和控制 `balance-leader-scheduler` 策略。

从 TiDB v6.0.0 起，PD 为 `balance-leader-scheduler` 引入了 `Batch` 参数，用于控制 balance-leader 执行任务的速度。你可以通过 pd-ctl 修改 `balance-leader batch` 配置项设置该功能。

在 v6.0.0 前，PD 不带有该配置（即 `balance-leader batch=1`）。在 v6.0.0 或更高版本中，`balance-leader batch` 的默认值为 `4`。如果你想为该配置项设置大于 `4` 的值，你需要同时调大 [`scheduler-max-waiting-operator`](#config-show--set-option-value--placement-rules)（默认值 `5`）。同时调大两个配置项后，你才能体验预期的加速效果。

```bash
scheduler config balance-leader-scheduler set batch 3  // 将 balance-leader 调度器可以批量执行的算子大小设置为 3
```

### `scheduler config balance-hot-region-scheduler`

用于查看和控制 `balance-hot-region-scheduler` 策略。

示例：

```bash
scheduler config balance-hot-region-scheduler  // 显示 balance-hot-region 调度器的所有配置
{
  "min-hot-byte-rate": 100,
  "min-hot-key-rate": 10,
  "min-hot-query-rate": 10,
  "max-zombie-rounds": 3,
  "max-peer-number": 1000,
  "byte-rate-rank-step-ratio": 0.05,
  "key-rate-rank-step-ratio": 0.05,
  "query-rate-rank-step-ratio": 0.05,
  "count-rank-step-ratio": 0.01,
  "great-dec-ratio": 0.95,
  "minor-dec-ratio": 0.99,
  "src-tolerance-ratio": 1.05,
  "dst-tolerance-ratio": 1.05,
  "read-priorities": [
    "query",
    "byte"
  ],
  "write-leader-priorities": [
    "key",
    "byte"
  ],
  "write-peer-priorities": [
    "byte",
    "key"
  ],
  "strict-picking-store": "true",
  "enable-for-tiflash": "true",
  "rank-formula-version": "v2"
}
```

- `min-hot-byte-rate` 指计数的最小字节数，通常为 100。

    ```bash
    scheduler config balance-hot-region-scheduler set min-hot-byte-rate 100
    ```

- `min-hot-key-rate` 指计数的最小 key 数，通常为 10。

    ```bash
    scheduler config balance-hot-region-scheduler set min-hot-key-rate 10
    ```

- `min-hot-query-rate` 指计数的最小 query 数，通常为 10。

    ```bash
    scheduler config balance-hot-region-scheduler set min-hot-query-rate 10
    ```

- `max-zombie-rounds` 指一个 operator 可被纳入 pending influence 所允许的最大心跳次数。如果将它设置为更大的值，更多的 operator 可能会被纳入 pending influence。通常用户不需要修改这个值。pending influence 指的是在调度中产生的、但仍生效的影响。

    ```bash
    scheduler config balance-hot-region-scheduler set max-zombie-rounds 3
    ```

- `max-peer-number` 指最多要被解决的 peer 数量。这个配置可避免调度器处理速度过慢。

    ```bash
    scheduler config balance-hot-region-scheduler set max-peer-number 1000
    ```

- `byte-rate-rank-step-ratio`、`key-rate-rank-step-ratio`、`query-rate-rank-step-ratio` 和 `count-rank-step-ratio` 分别控制 byte、key、query 和 count 的 step ranks。rank-step-ratio 决定了计算 rank 时的 step 值。`great-dec-ratio` 和 `minor-dec-ratio` 控制 `dec` 的 rank。通常用户不需要修改这些配置项。

    ```bash
    scheduler config balance-hot-region-scheduler set byte-rate-rank-step-ratio 0.05
    ```

- `src-tolerance-ratio` 和 `dst-tolerance-ratio` 是期望调度器的配置项。`tolerance-ratio` 的值越小，调度就越容易。当出现冗余调度时，你可以适当调大这个值。

    ```bash
    scheduler config balance-hot-region-scheduler set src-tolerance-ratio 1.1
    ```

- `read-priorities`、`write-leader-priorities` 和 `write-peer-priorities` 用于控制调度器优先从哪些维度进行热点均衡，支持配置两个维度。

    - `read-priorities` 和 `write-leader-priorities` 用于控制调度器在处理 read 和 write-leader 类型的热点时优先均衡的维度，可选的维度有 `query`、`byte` 和 `key`。
    - `write-peer-priorities` 用于控制调度器在处理 write-peer 类型的热点时优先均衡的维度，支持配置 `byte` 和 `key` 维度。

    > **注意：**
    >
    > 若集群的所有组件未全部升级到 v5.2 及以上版本，`query` 维度的配置不生效，部分组件升级完成后调度器仍默认优先从 `byte` 和 `key` 维度进行热点均衡，集群的所有组件全部升级完成后，也会继续保持这样的兼容配置，可通过 `pd-ctl` 查看实时配置。通常用户不需要修改这些配置项。

    ```bash
    scheduler config balance-hot-region-scheduler set read-priorities query,byte
    ```

- `strict-picking-store` 是控制热点调度搜索空间的开关，通常为打开。该配置项仅影响 `rank-formula-version` 为 `v1` 时的行为。当打开时，热点调度的目标是保证所配置的两个维度的热点均衡。当关闭后，热点调度只保证处于第一优先级的维度的热点均衡表现更好，但可能会导致其他维度的热点不再那么均衡。通常用户不需要修改这个配置项。

    ```bash
    scheduler config balance-hot-region-scheduler set strict-picking-store true
    ```

- `rank-formula-version` 适用于热点调度，其用来确定调度策略的算法版本，支持的值有 `["v1", "v2"]`。目前该配置的默认值为 `v2`。

    - `v1` 版本为 v6.3.0 之前的策略，主要关注调度是否降低了不同 Store 之间的负载差值，以及是否在另一维度引入副作用。
    - `v2` 版本是 v6.3.0 引入的实验特性算法，在 v6.4.0 正式发布，主要关注 Store 之间均衡度的提升率，同时降低了对副作用的关注度。对比 `strict-picking-store` 为 `true` 的 `v1` 算法，`v2` 版本更注重优先均衡第一维度。对比 `strict-picking-store` 为 `false` 的 `v1` 算法，`v2` 版本兼顾了第二维度的均衡。
    - `strict-picking-store` 为 `true` 的 `v1` 版本算法较为保守，只有当存在两个维度的负载都偏高的 Store 时才能产生调度。在特定场景下有可能因为维度冲突导致无法继续均衡，需要将 `strict-picking-store` 改为 `false` 才能在第一维度取得更好的均衡效果。`v2` 版本算法则可以在两个维度都取得更好的均衡效果，并减少无效调度。

    ```bash
    scheduler config balance-hot-region-scheduler set rank-formula-version v2
    ```

- `enable-for-tiflash` 是控制热点调度是否对 TiFlash 生效的开关。通常为打开，关闭后将不会产生 TiFlash 实例之间的热点调度。

    ```bash
    scheduler config balance-hot-region-scheduler set enable-for-tiflash true
    ```

### `scheduler config evict-leader-scheduler`

用于查看和管理 `evict-leader-scheduler` 的配置。

- 在已有 `evict-leader-scheduler` 时，使用 `add-store` 子命令，为指定的 store 添加 leader 驱逐调度：

    ```bash
    scheduler config evict-leader-scheduler add-store 2       // 为 store 2 添加 leader 驱逐调度
    ```

- 在已有 `evict-leader-scheduler` 时，使用 `delete-store` 子命令，移除指定 store 的 leader 驱逐调度：

    ```bash
    scheduler config evict-leader-scheduler delete-store 2    // 为 store 2 移除 leader 驱逐调度
    ```

    当一个 `evict-leader-scheduler` 的所有 store 配置都被移除后，该调度器也会自动被移除。

- 在已有 `evict-leader-scheduler` 时，使用 `set batch` 子命令修改 `batch` 值。其中，`batch` 用于调整单次调度过程中生成的 Operator 数量，默认值为 `3`，取值范围为 `[1, 10]`。`batch` 值越大，调度速度越快。

    ```bash
    scheduler config evict-leader-scheduler set batch 10 // 设置 batch 值为 10
    ```

### `service-gc-safepoint`

用于查询当前的 GC safepoint 与 service GC safepoint，输出结果示例如下：

```bash
{
  "service_gc_safe_points": [
    {
      "service_id": "gc_worker",
      "expired_at": 9223372036854775807,
      "safe_point": 439923410637160448
    }
  ],
  "gc_safe_point": 0
}
```

### `store [delete | cancel-delete | label | weight | remove-tombstone | limit ] <store_id> [--jq="<query string>"]`

使用 jq 格式化输出请参考 [jq 格式化 json 输出示例](#jq-格式化-json-输出示例)。

#### 查询 store

显示所有 store 信息：

```bash
store
```

```
{
  "count": 3,
  "stores": [...]
}
```

获取 ID 为 1 的 store：

```bash
store 1
```

```
......
```

#### 下线 store

下线 ID 为 1 的 store：

```bash
store delete 1
```

执行 `store cancel-delete` 命令，你可以撤销已使用 `store delete` 下线并处于 `Offline` 状态的 store。撤销后，该 store 会从 `Offline` 状态变为 `Up` 状态。注意，`store cancel-delete` 命令无法使 `Tombstone` 状态的 store 变回 `Up` 状态。

撤销通过 `store delete` 下线 ID 为 1 的 store：

```bash
store cancel-delete 1
```

删除所有 Tombstone 状态的 store：

```bash
store remove-tombstone
```

> **注意：**
>
> 若下线过程中切换了 PD leader，需要使用 `store limit` 命令修改 [store 调度限速](#设置-store-调度限速)。

#### 管理 store label

`store label` 命令用于管理 store label。

- 为 ID 为 1 的 store 设置键为 `"zone"`、值为 `"cn"` 的 label：

    ```bash
    store label 1 zone=cn
    ```

- 更新 ID 为 1 的 store 的 label：

    ```bash
    store label 1 zone=us
    ```

- 通过 `--rewrite` 选项重写 ID 为 1 的 store 的所有 label，之前的 label 会被覆盖：

    ```bash
    store label 1 region=us-est-1 disk=ssd --rewrite
    ```

- 删除 ID 为 1 的 store 的键为 `"disk"` 的 label ：

    ```bash
    store label 1 disk --delete
    ```

> **注意：**
>
> - store 的 label 更新采用合并策略。TiKV 进程重启后，其配置文件中的 store label 将会与 PD 自身存储的 store label 进行合并，并持久化合并后的结果。在合并过程中，如果 PD 侧的 store label 与 TiKV 配置文件有重复项，TiKV 配置将覆盖 PD 侧的标签。例如，如果通过 `store label 1 zone=cn` 将 store 1 的 `"zone"` 设置为 `"cn"`，但 TiKV 配置文件中已设置 `zone = "us"`，则在 TiKV 重启后，`"zone"` 将被更新为 `"us"`。
> - 如果希望使用 TiUP 统一管理 store label，你可以在集群重启前，使用 PD Control 的 `store label <id> --force` 命令将 PD 存储的 store label 清空。

#### 设置 store weight

将 ID 为 1 的 store 的 leader weight 设为 5，Region weight 设为 `10`：

```bash
store weight 1 5 10
```

#### 设置 store 调度限速

通过 `store-limit`，你可以设置 store 的调度速度。关于 `store limit` 的原理和使用方法，请参考 [`store limit`](/configure-store-limit.md)。

```bash
>> store limit                         // 显示所有 store 添加和删除 peer 的速度上限
>> store limit add-peer                // 显示所有 store 添加 peer 的速度上限
>> store limit remove-peer             // 显示所有 store 删除 peer 的速度上限
>> store limit all 5                   // 设置所有 store 添加和删除 peer 的速度上限为每分钟 5 个
>> store limit 1 5                     // 设置 store 1 添加和删除 peer 的速度上限为每分钟 5 个
>> store limit all 5 add-peer          // 设置所有 store 添加 peer 的速度上限为每分钟 5 个
>> store limit 1 5 add-peer            // 设置 store 1 添加 peer 的速度上限为每分钟 5 个
>> store limit 1 5 remove-peer         // 设置 store 1 删除 peer 的速度上限为每分钟 5 个
>> store limit all 5 remove-peer       // 设置所有 store 删除 peer 的速度上限为每分钟 5 个
```

> **注意：**
>
> 使用 `pd-ctl` 可以查看 TiKV 节点的状态信息，即 `Up`、`Disconnect`、`Offline`、`Down`、或 `Tombstone`。如需查看各个状态之间的关系，请参考 [TiKV Store 状态之间的关系](/tidb-scheduling.md#信息收集)。

### `log [fatal | error | warn | info | debug]`

用于设置 PD leader 的日志级别。

```bash
log warn
```

### `tso`

用于解析 TSO 到物理时间和逻辑时间。示例如下。

解析 TSO：

```bash
tso 395181938313123110
```

```
system:  2017-10-09 05:50:59 +0800 CST
logic:  120102
```

### `unsafe remove-failed-stores [store-ids | show]`

> **警告：**
>
> - 此功能为有损恢复，无法保证数据和数据索引完整性。
> - 建议在 TiDB 团队支持下进行相关操作，操作不当可能导致集群难以恢复。

用于在多数副本永久损坏造成数据不可用时进行有损恢复。示例如下。详见 [Online Unsafe Recovery](/online-unsafe-recovery.md)。

执行 Online Unsafe Recovery，移除永久损坏的节点 (Store):

```bash
unsafe remove-failed-stores 101,102,103
```

```bash
Success!
```

显示正在运行的 Online Unsafe Recovery 的当前状态或历史状态。

```bash
unsafe remove-failed-stores show
```

```bash
[
  "Collecting cluster info from all alive stores, 10/12.",
  "Stores that have reports to PD: 1, 2, 3, ...",
  "Stores that have not reported to PD: 11, 12",
]
```

## jq 格式化 JSON 输出示例

### 简化 `store` 的输出

```bash
store --jq=".stores[].store | {id, address, state_name}"
```

```
{"id":1,"address":"127.0.0.1:20161","state_name":"Up"}
{"id":30,"address":"127.0.0.1:20162","state_name":"Up"}
...
```

### 查询节点剩余空间

```bash
store --jq=".stores[] | {id: .store.id, available: .status.available}"
```

```
{"id":1,"available":"10 GiB"}
{"id":30,"available":"10 GiB"}
...
```

### 查询状态不为 Up 的所有节点

```bash
store --jq='.stores[].store | select(.state_name!="Up") | {id, address, state_name}'
```

```
{"id":1,"address":"127.0.0.1:20161""state_name":"Offline"}
{"id":5,"address":"127.0.0.1:20162""state_name":"Offline"}
...
```

### 查询所有的 TiFlash 节点

```bash
store --jq='.stores[].store | select(.labels | length>0 and contains([{"key":"engine","value":"tiflash"}])) | {id, address, state_name}'
```

```
{"id":1,"address":"127.0.0.1:20161""state_name":"Up"}
{"id":5,"address":"127.0.0.1:20162""state_name":"Up"}
...
```

### 查询 Region 副本的分布情况

```bash
region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id]}"
```

```
{"id":2,"peer_stores":[1,30,31]}
{"id":4,"peer_stores":[1,31,34]}
...
```

### 根据副本数过滤 Region

例如副本数不为 3 的所有 Region：

```bash
region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length != 3)}"
```

```
{"id":12,"peer_stores":[30,32]}
{"id":2,"peer_stores":[1,30,31,32]}
```

### 根据副本 store ID 过滤 Region

例如在 store30 上有副本的所有 Region：

```bash
region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(any(.==30))}"
```

```
{"id":6,"peer_stores":[1,30,31]}
{"id":22,"peer_stores":[1,30,32]}
...
```

还可以像这样找出在 store30 或 store31 上有副本的所有 Region：

```bash
region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(any(.==(30,31)))}"
```

```
{"id":16,"peer_stores":[1,30,34]}
{"id":28,"peer_stores":[1,30,32]}
{"id":12,"peer_stores":[30,32]}
...
```

### 恢复数据时寻找相关 Region

例如当 `[store1, store30, store31]` 宕机时不可用时，我们可以通过查找所有 Down 副本数量大于正常副本数量的所有 Region：

```bash
region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length as $total | map(if .==(1,30,31) then . else empty end) | length>=$total-length) }"
```

```
{"id":2,"peer_stores":[1,30,31,32]}
{"id":12,"peer_stores":[30,32]}
{"id":14,"peer_stores":[1,30,32]}
...
```

或者在 `[store1, store30, store31]` 无法启动时，找出 `store1` 上可以安全手动移除数据的 Region。我们可以这样过滤出所有在 `store1` 上有副本并且没有其他 DownPeer 的 Region：

```bash
region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length>1 and any(.==1) and all(.!=(30,31)))}"
```

```
{"id":24,"peer_stores":[1,32,33]}
```

在 `[store30, store31]` 宕机时，找出能安全地通过创建 `remove-peer` Operator 进行处理的所有 Region，即有且仅有一个 DownPeer 的 Region：

```bash
region --jq=".regions[] | {id: .id, remove_peer: [.peers[].store_id] | select(length>1) | map(if .==(30,31) then . else empty end) | select(length==1)}"
```

```
{"id":12,"remove_peer":[30]}
{"id":4,"remove_peer":[31]}
{"id":22,"remove_peer":[30]}
...
```
