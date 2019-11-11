---
title: PD Control 使用说明
category: tools
---

# PD Control 使用说明

PD Control 是 PD 的命令行工具，用于获取集群状态信息和调整集群。

## 源码编译

1. [Go](https://golang.org/) Version 1.7 以上
2. 在 PD 项目根目录使用 `make` 命令进行编译，生成 bin/pd-ctl

## 简单例子

单命令模式：

```bash
./pd-ctl store -d -u http://127.0.0.1:2379
```

交互模式：

```bash
./pd-ctl -u http://127.0.0.1:2379
```

使用环境变量：

```bash
export PD_ADDR=http://127.0.0.1:2379
./pd-ctl
```

使用 TLS 加密：

```bash
./pd-ctl -u https://127.0.0.1:2379 --cacert="path/to/ca" --cert="path/to/cert" --key="path/to/key"
```

## 命令行参数(flags)

### \-\-pd,-u

+ 指定 PD 的地址
+ 默认地址: `http://127.0.0.1:2379`
+ 环境变量: PD_ADDR

### \-\-detach,-d

+ 使用单命令行模式（不进入 readline）
+ 默认值: false

### --cacert

- 指定 PEM 格式的受信任 CA 的证书文件路径
- 默认值: ""

### --cert

- 指定 PEM 格式的 SSL 证书文件路径
- 默认值: ""

### --key

- 指定 PEM 格式的 SSL 证书密钥文件路径，即 `--cert` 所指定的证书的私钥
- 默认值: ""

### --version,-V

- 打印版本信息并退出
- 默认值: false

## 命令(command)

### cluster

用于显示集群基本信息。

示例：

```bash
>> cluster                                     // 显示 cluster 的信息
{
  "id": 6493707687106161130,
  "max_peer_count": 3
}
```

### config [show | set \<option\> \<value\>]

用于显示或调整配置信息。

示例：

```bash
>> config show                                //　显示 scheduler 的相关 config 信息
{
  "max-snapshot-count": 3,
  "max-pending-peer-count": 16,
  "max-store-down-time": "1h0m0s",
  "leader-schedule-limit": 64,
  "region-schedule-limit": 16,
  "replica-schedule-limit": 24,
  "tolerant-size-ratio": 2.5,
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
>> config show all                            // 显示所有的 config 信息
>> config show namespace ts1                  // 显示名为 ts1 的 namespace 的相关 config 信息
{
  "leader-schedule-limit": 64,
  "region-schedule-limit": 16,
  "replica-schedule-limit": 24,
  "max-replicas": 3,
}
>> config show replication                    // 显示 replication 的相关 config 信息
{
  "max-replicas": 3,
  "location-labels": ""
}
```

通过调整 `leader-schedule-limit` 可以控制同时进行 leader 调度的任务个数。
这个值主要影响 *leader balance* 的速度，值越大调度得越快，设置为 0 则关闭调度。
Leader 调度的开销较小，需要的时候可以适当调大。

```bash
>> config set leader-schedule-limit 4         // 最多同时进行 4 个 leader 调度
```

通过调整 `region-schedule-limit` 可以控制同时进行 region 调度的任务个数。
这个值主要影响 *region balance* 的速度，值越大调度得越快，设置为 0 则关闭调度。
Region 调度的开销较大，所以这个值不宜调得太大。

```bash
>> config set region-schedule-limit 2         // 最多同时进行 2 个 region 调度
```

通过调整 `replica-schedule-limit` 可以控制同时进行 replica 调度的任务个数。
这个值主要影响节点挂掉或者下线的时候进行调度的速度，值越大调度得越快，设置为 0 则关闭调度。
Replica 调度的开销较大，所以这个值不宜调得太大。

```bash
>> config set replica-schedule-limit 4        // 最多同时进行 4 个 replica 调度
```

以上对配置的修改是全局性的，还可以通过对不同 namespace 的配置，进行细化调整。当 namespace 未设置相应配置时，使用全局配置。注：namespace 的配置只支持对 leader-schedule-limit，region-schedule-limit，replica-schedule-limit，max-replicas 的调整，否则不生效。

```bash
>> config set namespace ts1 leader-schedule-limit 4 // 设置名为 ts1 的 namespace 最多同时进行 4 个 leader 调度
>> config set namespace ts2 region-schedule-limit 2 // 设置名为 ts2 的 namespace 最多同时进行  2 个 region 调度
```

### config delete namespace \<name\> [\<option\>]

用于删除 namespace 的配置信息。

示例：

在对 namespace 相关配置进行设置后，若想让该 namespace 继续使用全局配置，可删除该 namespace 的配置信息，之后便使用全局配置。

```bash
>> config delete namespace ts1                      // 删除名为 ts1 的 namespace 的相关配置
```

若只想让 namespace 中的某项配置使用全局配置而不影响其他配置，则可使用如下命令：

```bash
>> config delete namespace region-schedule-limit ts2 // 删除名为 ts2 的 namespace 的 region-schedule-limit 配置
```

### health

用于显示集群健康信息。

示例：

```bash
>> health                                // 显示健康信息
{"health": "true"}
```

### hot [read | write | store]

用于显示集群热点信息。

示例：

```bash
>> hot read                             // 显示读热点信息
>> hot write                            // 显示写热点信息
>> hot store                            // 显示所有 store 的读写信息
```

### label [store]

用于显示集群标签信息

示例：

```bash
>> label                                // 显示所有 label
>> label store zone cn                  // 显示所有包含 label 为 "zone":"cn" 的 store
```

### member [leader | delete]

用于显示 PD 成员信息或删除指定成员。

示例：

```bash
>> member                               // 显示所有成员的信息
{
  "members": [......]
}
>> member leader show                   // 显示 leader 的信息
{
  "name": "pd",
  "addr": "http://192.168.199.229:2379",
  "id": 9724873857558226554
}
>> member delete name pd2               // 下线 "pd2"
Success!
>> member delete id 1319539429105371180 // 使用 id 下线节点
Success!
```

### operator [show | add | remove]

用于显示和控制调度操作。

示例：

```bash
>> operator show                            // 显示所有的 operators
>> operator show admin                      // 显示所有的 admin operators
>> operator show leader                     // 显示所有的 leader operators
>> operator show region                     // 显示所有的 region operators
>> operator add add-peer 1 2                // 在 store 2 上新增 region 1 的一个副本
>> operator remove remove-peer 1 2          // 移除 store 2 上的 region 1 的一个副本
>> operator add transfer-leader 1 2         // 把 region 1 的 leader 调度到 store 2
>> operator add transfer-region 1 2 3 4     // 把 region 1 调度到 store 2,3,4
>> operator add transfer-peer 1 2 3         // 把 region 1 在 store 2 上的副本调度到 store 3
>> operator remove 1                        // 把 region 1 的调度操作删掉
```

### ping

用于显示`ping` PD 所需要花费的时间

示例：

```bash
>> ping
time: 43.12698ms
```

### region \<region_id\>

用于显示 region 信息。

示例：

```bash
>> region                               //　显示所有 region 信息
{
  "count": 1,
  "regions": [......]
}

>> region 2                             // 显示 region id 为 2 的信息
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

### region key [--format=raw|pb|proto|protobuf] \<key\>

用于查询某个 key 在哪个 region 上，支持 raw 和 protobuf 格式。

Raw 格式（默认）示例：

```bash
>> region key abc
{
  "region": {
    "id": 2,
    ......
  }
}
```

Protobuf 格式示例：

```bash
>> region key --format=pb t\200\000\000\000\000\000\000\377\035_r\200\000\000\000\000\377\017U\320\000\000\000\000\000\372
{
  "region": {
    "id": 2,
    ......
  }
}
```

### scheduler [show | add | remove]

用于显示和控制调度策略。

示例：

```bash
>> scheduler show                             // 显示所有的 schedulers
>> scheduler add grant-leader-scheduler 1     // 把 store 1 上的所有 region 的 leader 调度到 store 1
>> scheduler add evict-leader-scheduler 1     // 把 store 1 上的所有 region 的 leader 从 store 1 调度出去
>> scheduler add shuffle-leader-scheduler     // 随机交换不同 store 上的 leader
>> scheduler add shuffle-region-scheduler     // 随机调度不同 store 上的 region
>> scheduler remove grant-leader-scheduler-1  // 把对应的 scheduler 删掉
```

### store [delete | label | weight] \<store_id\>

用于显示 store 信息或者删除指定 store。

示例：

```bash
>> store                        // 显示所有 store 信息
{
  "count": 3,
  "stores": [...]
}
>> store 1                      // 获取 store id 为 1 的 store
  ......
>> store delete 1               // 下线 store id 为 1 的 store
  ......
>> store label 1 zone cn        // 设置 store id 为 1 的 store 的键为 "zone" 的 label 的值为 "cn"
>> store weight 1 5 10          // 设置 store id 为 1 的 store 的 leader weight 为 5，region weight 为 10
```

### table_ns [create | add | remove | set_store | rm_store | set_meta | rm_meta]

用于显示 table 的 namespace 的相关信息

示例：

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

用于解析 TSO 到物理时间和逻辑时间

示例：

```bash
>> tso 395181938313123110        // 解析 TSO
system:  2017-10-09 05:50:59 +0800 CST
logic:  120102
```
