---
title: PD Control 使用说明
category: reference
aliases: ['/docs-cn/tools/pd-control/']
---

# PD Control 使用说明

PD Control 是 PD 的命令行工具，用于获取集群状态信息和调整集群。

## 源码编译

1. [Go](https://golang.org/) Version 1.9 以上
2. 在 PD 项目根目录使用 `make` 命令进行编译，生成 bin/pd-ctl

## 简单例子

单命令模式：

{{< copyable "shell-regular" >}}

```bash
./pd-ctl store -u http://127.0.0.1:2379
```

交互模式：

{{< copyable "shell-regular" >}}

```bash
./pd-ctl -i -u http://127.0.0.1:2379
```

使用环境变量：

{{< copyable "shell-regular" >}}

```bash
export PD_ADDR=http://127.0.0.1:2379 &&
./pd-ctl
```

使用 TLS 加密：

{{< copyable "shell-regular" >}}

```bash
./pd-ctl -u https://127.0.0.1:2379 --cacert="path/to/ca" --cert="path/to/cert" --key="path/to/key"
```

## 命令行参数(flags)

### --cacert

- 指定 PEM 格式的受信任 CA 的证书文件路径
- 默认值: ""

### --cert

- 指定 PEM 格式的 SSL 证书文件路径
- 默认值: ""

### \-\-detach,-d

+ 使用单命令行模式(不进入 readline)
+ 默认值：true

### \-\-interact,-i

+ 使用交互模式（进入 readline）
+ 默认值：false

### --key

- 指定 PEM 格式的 SSL 证书密钥文件路径，即 `--cert` 所指定的证书的私钥
- 默认值: ""

### \-\-pd,-u

+ 指定 PD 的地址
+ 默认地址：`http://127.0.0.1:2379`
+ 环境变量：`PD_ADDR`

### --version,-V

- 打印版本信息并退出
- 默认值: false

## 命令(command)

### cluster

用于显示集群基本信息。

示例：

{{< copyable "" >}}

```bash
>> cluster
```

```
{
  "id": 6493707687106161130,
  "max_peer_count": 3
}
```

### config [show | set \<option> \<value>]

用于显示或调整配置信息。示例如下。

显示 scheduler 的相关 config 信息：

{{< copyable "" >}}

```bash
>> config show
```

```
{
  "max-snapshot-count": 3,
  "max-pending-peer-count": 16,
  "max-merge-region-size": 50,
  "max-merge-region-keys": 200000,
  "split-merge-interval": "1h",
  "patrol-region-interval": "100ms",
  "max-store-down-time": "1h0m0s",
  "leader-schedule-limit": 4,
  "region-schedule-limit": 4,
  "replica-schedule-limit":8,
  "merge-schedule-limit": 8,
  "tolerant-size-ratio": 5,
  "low-space-ratio": 0.8,
  "high-space-ratio": 0.6,
  "disable-raft-learner": "false",
  "disable-remove-down-replica": "false",
  "disable-replace-offline-replica": "false",
  "disable-make-up-replica": "false",
  "disable-remove-extra-replica": "false",
  "disable-location-replacement": "false",
  "disable-namespace-relocation": "false",
  "schedulers-v2": [
    {
      "type": "balance-region",
      "args": null
    },
    {
      "type": "balance-leader",
      "args": null
    },
    {
      "type": "hot-region",
      "args": null
    }
  ]
}
```

显示所有的 config 信息：

{{< copyable "" >}}

```bash
>> config show all
```

显示名为 ts1 的 namespace 的相关 config 信息：

{{< copyable "" >}}

```bash
>> config show namespace ts1
```

```
{
  "leader-schedule-limit": 4,
  "region-schedule-limit": 4,
  "replica-schedule-limit": 8,
  "max-replicas": 3,
}
```

显示 replication 的相关 config 信息：

{{< copyable "" >}}

```bash
>> config show replication
```

```
{
  "max-replicas": 3,
  "location-labels": ""
}
```

显示目前集群版本，是目前集群 TiKV 节点的最低版本，并不对应 binary 的版本：

{{< copyable "" >}}

```bash
>> config show cluster-version
```

```
"2.0.0"
```

`max-snapshot-count` 控制单个 store 最多同时接收或发送的 snapshot 数量，调度受制于这个配置来防止抢占正常业务的资源。
当需要加快补副本或 balance 速度时可以调大这个值。

设置最大 snapshot 为 16：

{{< copyable "" >}}

```bash
>> config set max-snapshot-count 16
```

`max-pending-peer-count` 控制单个 store 的 pending peer 上限，调度受制于这个配置来防止在部分节点产生大量日志落后的 Region。需要加快补副本或 balance 速度可以适当调大这个值，设置为 0 则表示不限制。

设置最大 pending peer 数量为 64：

{{< copyable "" >}}

```bash
>> config set max-pending-peer-count 64
```

`max-merge-region-size` 控制 Region Merge 的 size 上限（单位是 M）。当 Region Size 大于指定值时 PD 不会将其与相邻的 Region 合并。设置为 0 表示不开启 Region Merge 功能。

设置 Region Merge 的 size 上限为 16 M：

{{< copyable "" >}}

```bash
>> config set max-merge-region-size 16
```

`max-merge-region-keys` 控制 Region Merge 的 keyCount 上限。当 Region KeyCount 大于指定值时 PD 不会将其与相邻的 Region 合并。

设置 Region Merge 的 keyCount 上限为 50000：

{{< copyable "" >}}

```bash
>> config set max-merge-region-keys 50000
```

`split-merge-interval` 控制对同一个 Region 做 `split` 和 `merge` 操作的间隔，即对于新 `split` 的 Region 一段时间内不会被 `merge`。

设置 `split` 和 `merge` 的间隔为 1 天：

{{< copyable "" >}}

```bash
>> config set split-merge-interval 24h
```

`patrol-region-interval` 控制 replicaChecker 检查 Region 健康状态的运行频率，越短则运行越快，通常状况不需要调整。

设置 replicaChecker 的运行频率为 10 毫秒：

{{< copyable "" >}}

```bash
>> config set patrol-region-interval 10ms
```

`max-store-down-time` 为 PD 认为失联 store 无法恢复的时间，当超过指定的时间没有收到 store 的心跳后，PD 会在其他节点补充副本。

设置 store 心跳丢失 30 分钟开始补副本：

{{< copyable "" >}}

```bash
>> config set max-store-down-time 30m
```

通过调整 `leader-schedule-limit` 可以控制同时进行 leader 调度的任务个数。
这个值主要影响 *leader balance* 的速度，值越大调度得越快，设置为 0 则关闭调度。
Leader 调度的开销较小，需要的时候可以适当调大。

最多同时进行 4 个 leader 调度：

{{< copyable "" >}}

```bash
>> config set leader-schedule-limit 4
```

通过调整 `region-schedule-limit` 可以控制同时进行 Region 调度的任务个数。
这个值主要影响 *Region balance* 的速度，值越大调度得越快，设置为 0 则关闭调度。
Region 调度的开销较大，所以这个值不宜调得太大。

最多同时进行 2 个 Region 调度：

{{< copyable "" >}}

```bash
>> config set region-schedule-limit 2
```

通过调整 `replica-schedule-limit` 可以控制同时进行 replica 调度的任务个数。
这个值主要影响节点挂掉或者下线的时候进行调度的速度，值越大调度得越快，设置为 0 则关闭调度。
Replica 调度的开销较大，所以这个值不宜调得太大。

最多同时进行 4 个 replica 调度：

{{< copyable "" >}}

```bash
>> config set replica-schedule-limit 4
```

`merge-schedule-limit` 控制同时进行的 Region Merge 调度的任务，设置为 0 则关闭 Region Merge。
Merge 调度的开销较大，所以这个值不宜调得过大。

最多同时进行 16 个 merge 调度：

{{< copyable "" >}}

```bash
>> config set merge-schedule-limit 16
```

以上对配置的修改是全局性的，还可以通过对不同 namespace 的配置，进行细化调整。当 namespace 未设置相应配置时，使用全局配置。注：namespace 的配置只支持对 leader-schedule-limit，region-schedule-limit，replica-schedule-limit，max-replicas 的调整，否则不生效。

设置名为 ts1 的 namespace 最多同时进行 4 个 leader 调度：

{{< copyable "" >}}

```bash
>> config set namespace ts1 leader-schedule-limit 4
```

设置名为 ts2 的 namespace 最多同时进行 2 个 Region 调度：

{{< copyable "" >}}

```bash
>> config set namespace ts2 region-schedule-limit 2
```

`tolerant-size-ratio` 控制 balance 缓冲区大小。
当两个 store 的 leader 或 Region 的得分差距小于指定倍数的 Region size 时，PD 会认为此时 balance 达到均衡状态。

设置缓冲区为约 20 倍平均 RegionSize：

{{< copyable "" >}}

```bash
>> config set tolerant-size-ratio 20
```

`low-space-ratio` 用于设置 store 空间不足的阈值。
当节点的空间占用比例超过指定值时，PD 会尽可能避免往对应节点迁移数据，同时主要针对剩余空间大小进行调度，避免对应节点磁盘空间被耗尽。

设置空间不足阈值为 0.9：

{{< copyable "" >}}

```bash
config set low-space-ratio 0.9
```

`high-space-ratio` 用于设置 store 空间充裕的阈值。
当节点的空间占用比例小于指定值时，PD 调度时会忽略剩余空间这个指标，主要针对实际数据量进行均衡。

设置空间充裕阈值为 0.5：

{{< copyable "" >}}

```bash
config set high-space-ratio 0.5
```

`disable-raft-learner` 用于关闭 raft learner 功能。
默认配置下 PD 在添加副本时会使用 raft learner 来降低宕机或网络故障带来的不可用风险。

关闭 raft learner 功能：

{{< copyable "" >}}

```bash
config set disable-raft-learner true
```

`cluster-version` 集群的版本，用于控制某些 Feature 是否开启，处理兼容性问题。
通常是集群正常运行的所有 TiKV 节点中的最低版本，需要回滚到更低的版本时才进行手动设置。

设置 cluster version 为 1.0.8：

{{< copyable "" >}}

```bash
config set cluster-version 1.0.8
```

`disable-remove-down-replica` 用于关闭自动删除 DownReplica 的特性。
当设置为 true 时，PD 不会自动清理宕机状态的副本。

`disable-replace-offline-replica` 用于关闭迁移 OfflineReplica 的特性。
当设置为 true 时，PD 不会迁移下线状态的副本。

`disable-make-up-replica` 用于关闭补充副本的特性。
当设置为 true 时，PD 不会为副本数不足的 Region 补充副本。

`disable-remove-extra-replica` 用于关闭删除多余副本的特性。
当设置为 true 时，PD 不会为副本数过多的 Region 删除多余副本。

`disable-location-replacement` 用于关闭隔离级别检查。
当设置为 true 时，PD 不会通过调度来提升 Region 副本的隔离级别。

`disable-namespace-relocation` 用于关闭 Region 的 namespace 调度。当设置为 true 时，PD 不会把 Region 调度到它所属的 Store 上。

### config delete namespace \<name> [\<option>]

用于删除 namespace 的配置信息。

示例：

在对 namespace 相关配置进行设置后，若想让该 namespace 继续使用全局配置，可删除该 namespace 的配置信息，之后便使用全局配置。

删除名为 ts1 的 namespace 的相关配置：

{{< copyable "" >}}

```bash
>> config delete namespace ts1
```

若只想让 namespace 中的某项配置使用全局配置而不影响其他配置，则可使用如下命令：

删除名为 ts2 的 namespace 的 region-schedule-limit 配置：

{{< copyable "" >}}

```bash
>> config delete namespace region-schedule-limit ts2
```

### health

用于显示集群健康信息。示例如下。

显示健康信息：

{{< copyable "" >}}

```bash
>> health
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

### hot [read | write | store]

用于显示集群热点信息。示例如下。

显示读热点信息：

{{< copyable "" >}}

```bash
>> hot read
```

显示写热点信息：

{{< copyable "" >}}

```bash
>> hot write
```

显示所有 store 的读写信息：

{{< copyable "" >}}

```bash
>> hot store
```

### label [store \<name> \<value>]

用于显示集群标签信息。示例如下。

显示所有 label：

{{< copyable "" >}}

```bash
>> label
```

显示所有包含 label 为 "zone":"cn" 的 store：

{{< copyable "" >}}

```bash
>> label store zone cn
```

### member [delete | leader_priority | leader [show | resign | transfer <member_name>]]

用于显示 PD 成员信息，删除指定成员，设置成员的 leader 优先级。示例如下。

显示所有成员的信息：

{{< copyable "" >}}

```bash
>> member
```

```
{
  "members": [......],
  "leader": {......},
  "etcd_leader": {......},
}
```

下线 "pd2"：

{{< copyable "" >}}

```bash
>> member delete name pd2
```

```
Success!
```

使用 id 下线节点：

{{< copyable "" >}}

```bash
>> member delete id 1319539429105371180
```

```
Success!
```

显示 leader 的信息：

{{< copyable "" >}}

```bash
>> member leader show
```

```
{
  "name": "pd",
  "addr": "http://192.168.199.229:2379",
  "id": 9724873857558226554
}
```

将 leader 从当前成员移走：

{{< copyable "" >}}

```bash
>> member leader resign
```

```
......
```

将 leader 迁移至指定成员：

{{< copyable "" >}}

```bash
>> member leader transfer pd3
```

```
......
```

### operator [show | add | remove]

用于显示和控制调度操作，或者对 Region 进行分裂或合并。

示例：

{{< copyable "" >}}

```bash
>> operator show                                        // 显示所有的 operators
>> operator show admin                                  // 显示所有的 admin operators
>> operator show leader                                 // 显示所有的 leader operators
>> operator show region                                 // 显示所有的 Region operators
>> operator add add-peer 1 2                            // 在 store 2 上新增 Region 1 的一个副本
>> operator add remove-peer 1 2                         // 移除 store 2 上的 Region 1 的一个副本
>> operator add transfer-leader 1 2                     // 把 Region 1 的 leader 调度到 store 2
>> operator add transfer-region 1 2 3 4                 // 把 Region 1 调度到 store 2,3,4
>> operator add transfer-peer 1 2 3                     // 把 Region 1 在 store 2 上的副本调度到 store 3
>> operator add merge-region 1 2                        // 将 Region 1 与 Region 2 合并
>> operator add split-region 1 --policy=approximate     // 将 Region 1 对半拆分成两个 Region，基于粗略估计值
>> operator add split-region 1 --policy=scan            // 将 Region 1 对半拆分成两个 Region，基于精确扫描值
>> operator remove 1                                    // 把 Region 1 的调度操作删掉
```

其中，Region 的分裂都是尽可能地从靠近中间的位置开始。对这个位置的选择支持两种策略，即 scan 和 approximate。它们之间的区别是，前者通过扫描这个 Region 的方式来确定中间的 key，而后者是通过查看 SST 文件中记录的统计信息，来得到近似的位置。一般来说，前者更加精确，而后者消耗更少的 I/O，可以更快地完成。

### ping

用于显示`ping` PD 所需要花费的时间

示例：

{{< copyable "" >}}

```bash
>> ping
```

```
time: 43.12698ms
```

### region <region_id> [--jq="\<query string>"]

用于显示 Region 信息。使用 jq 格式化输出请参考 [jq-格式化-json-输出示例](#jq-格式化-json-输出示例)。示例如下。

显示所有 Region 信息：

{{< copyable "" >}}

```bash
>> region
```

```
{
  "count": 1,
  "regions": [......]
}
```

显示 Region id 为 2 的信息：

{{< copyable "" >}}

```bash
>> region 2
```

```
{
  "region": {
      "id": 2,
      ......
  }
  "leader": {
      ......
  }
}
```

### region key [--format=raw|encode] \<key>

用于查询某个 key 在哪个 Region 上，支持 raw 和 encoding 格式。使用 encoding 格式时，key 需要使用单引号。

Raw 格式（默认）示例：

{{< copyable "" >}}

```bash
>> region key abc
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

{{< copyable "" >}}

```bash
>> region key --format=encode 't\200\000\000\000\000\000\000\377\035_r\200\000\000\000\000\377\017U\320\000\000\000\000\000\372'
```

```
{
  "region": {
    "id": 2,
    ......
  }
}
```

### region sibling <region_id>

用于查询某个 Region 相邻的 Region。

示例：

{{< copyable "" >}}

```bash
>> region sibling 2
```

```
{
  "count": 2,
  "regions": [......],
}
```

### `region store <store_id>`

用于查询某个 store 上面所有的 Region。

示例：

{{< copyable "" >}}

```bash
>> region store 2
```

```
{
  "count": 10,
  "regions": [......],
}
```

### `region topread [limit]`

用于查询读流量最大的 Region。limit 的默认值是 16。

示例：

{{< copyable "" >}}

```bash
>> region topread
```

```
{
  "count": 16,
  "regions": [......],
}
```

### `region topwrite [limit]`

用于查询写流量最大的 Region。limit 的默认值是 16。

示例：

{{< copyable "" >}}

```bash
>> region topwrite
```

```
{
  "count": 16,
  "regions": [......],
}
```

### `region topconfver [limit]`

用于查询 conf version 最大的 Region。limit 的默认值是 16。

示例：

{{< copyable "" >}}

```bash
>> region topconfver
```

```
{
  "count": 16,
  "regions": [......],
}
```

### `region topversion [limit]`

用于查询 version 最大的 Region。limit 的默认值是 16。

示例：

{{< copyable "" >}}

```bash
>> region topversion
```

```
{
  "count": 16,
  "regions": [......],
}
```

### `region topsize [limit]`

用于查询 approximate size 最大的 Region。limit 的默认值是 16。

示例：

{{< copyable "" >}}

```bash
>> region topsize
```

```
{
    "count": 16,
    "regions": [......],
}
```

### region check [miss-peer | extra-peer | down-peer | pending-peer | incorrect-ns]

用于查询处于异常状态的 Region，各类型的意义如下

- miss-peer：缺副本的 Region
- extra-peer：多副本的 Region
- down-peer：有副本状态为 Down 的 Region
- pending-peer：有副本状态为 Pending 的 Region
- incorrect-ns：有副本不符合 namespace 约束的 Region

示例：

{{< copyable "" >}}

```bash
>> region check miss-peer
```

```
{
  "count": 2,
  "regions": [......],
}
```

### scheduler [show | add | remove]

用于显示和控制调度策略。

示例：

{{< copyable "" >}}

```bash
>> scheduler show                             // 显示所有的 schedulers
>> scheduler add grant-leader-scheduler 1     // 把 store 1 上的所有 Region 的 leader 调度到 store 1
>> scheduler add evict-leader-scheduler 1     // 把 store 1 上的所有 Region 的 leader 从 store 1 调度出去
>> scheduler add shuffle-leader-scheduler     // 随机交换不同 store 上的 leader
>> scheduler add shuffle-region-scheduler     // 随机调度不同 store 上的 Region
>> scheduler remove grant-leader-scheduler-1  // 把对应的 scheduler 删掉
```

### store [delete | label | weight] <store_id>  [--jq="\<query string>"]

用于显示 store 信息或者删除指定 store。使用 jq 格式化输出请参考 [jq-格式化-json-输出示例](#jq-格式化-json-输出示例)。示例如下。

显示所有 store 信息：

{{< copyable "" >}}

```bash
>> store
```

```
{
  "count": 3,
  "stores": [...]
}
```

获取 store id 为 1 的 store：

{{< copyable "" >}}

```bash
>> store 1
```

```
  ......
```

下线 store id 为 1 的 store：

{{< copyable "" >}}

```bash
>> store delete 1
```

```
  ......
```

设置 store id 为 1 的 store 的键为 "zone" 的 label 的值为 "cn"：

{{< copyable "" >}}

```bash
>> store label 1 zone cn
```

设置 store id 为 1 的 store 的 leader weight 为 5，Region weight 为 10：

{{< copyable "" >}}

```bash
>> store weight 1 5 10
```

### table_ns [create | add | remove | set_store | rm_store | set_meta | rm_meta]

用于显示 table 的 namespace 的相关信息

示例：

{{< copyable "" >}}

```bash
>> table_ns add ts1 1            // 将 table id 为 1 的 table 添加到名为 ts1 的 namespace
>> table_ns create ts1           // 添加名为 ts1 的 namespace
>> table_ns remove ts1 1         // 将 table id 为 1 的 table 从名为 ts1 的 namespace 中移除
>> table_ns rm_meta ts1          // 将 meta 信息从名为 ts1 的 namespace 中移除
>> table_ns rm_store 1 ts1       // 将 store id 为 1 的 table 从名为 ts1 的 namespace 中移除
>> table_ns set_meta ts1         // 将 meta 信息添加到名为 ts1 的 namespace
>> table_ns set_store 1 ts1      // 将 store id 为 1 的 table 添加到名为 ts1 的 namespace
```

### tso

用于解析 TSO 到物理时间和逻辑时间。示例如下。

解析 TSO：

{{< copyable "" >}}

```bash
>> tso 395181938313123110
```

```
system:  2017-10-09 05:50:59 +0800 CST
logic:  120102
```

## jq 格式化 json 输出示例

### 简化 `store` 的输出

{{< copyable "" >}}

```bash
» store --jq=".stores[].store | { id, address, state_name}"
```

```
{"id":1,"address":"127.0.0.1:20161","state_name":"Up"}
{"id":30,"address":"127.0.0.1:20162","state_name":"Up"}
...
```

### 查询节点剩余空间

{{< copyable "" >}}

```bash
» store --jq=".stores[] | {id: .store.id, available: .status.available}"
```

```
{"id":1,"available":"10 GiB"}
{"id":30,"available":"10 GiB"}
...
```

### 查询 Region 副本的分布情况

{{< copyable "" >}}

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id]}"
```

```
{"id":2,"peer_stores":[1,30,31]}
{"id":4,"peer_stores":[1,31,34]}
...
```

### 根据副本数过滤 Region

例如副本数不为 3 的所有 Region：

{{< copyable "" >}}

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length != 3)}"
```

```
{"id":12,"peer_stores":[30,32]}
{"id":2,"peer_stores":[1,30,31,32]}
```

### 根据副本 store ID 过滤 Region

例如在 store30 上有副本的所有 Region：

{{< copyable "" >}}

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(any(.==30))}"
```

```
{"id":6,"peer_stores":[1,30,31]}
{"id":22,"peer_stores":[1,30,32]}
...
```

还可以像这样找出在 store30 或 store31 上有副本的所有 Region：

{{< copyable "" >}}

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(any(.==(30,31)))}"
```

```
{"id":16,"peer_stores":[1,30,34]}
{"id":28,"peer_stores":[1,30,32]}
{"id":12,"peer_stores":[30,32]}
...
```

### 恢复数据时寻找相关 Region

例如当 [store1, store30, store31] 宕机时不可用时，我们可以通过查找所有 Down 副本数量大于正常副本数量的所有 Region：

{{< copyable "" >}}

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length as $total | map(if .==(1,30,31) then . else empty end) | length>=$total-length) }"
```

```
{"id":2,"peer_stores":[1,30,31,32]}
{"id":12,"peer_stores":[30,32]}
{"id":14,"peer_stores":[1,30,32]}
...
```

或者在 [store1, store30, store31] 无法启动时，找出 store1 上可以安全手动移除数据的 Region。我们可以这样过滤出所有在 store1 上有副本并且没有其他 DownPeer 的 Region：

{{< copyable "" >}}

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length>1 and any(.==1) and all(.!=(30,31)))}"
```

```
{"id":24,"peer_stores":[1,32,33]}
```

在 [store30, store31] 宕机时，找出能安全地通过创建 `remove-peer` Operator 进行处理的所有 Region，即有且仅有一个 DownPeer 的 Region：

{{< copyable "" >}}

```bash
» region --jq=".regions[] | {id: .id, remove_peer: [.peers[].store_id] | select(length>1) | map(if .==(30,31) then . else empty end) | select(length==1)}"
```

```
{"id":12,"remove_peer":[30]}
{"id":4,"remove_peer":[31]}
{"id":22,"remove_peer":[30]}
...
```
