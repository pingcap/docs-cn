---
title: PD Control 使用说明
category: monitoring
---

# PD Control 使用说明

PD Control 是 PD 的命令行工具，用于获取集群状态信息和调整集群。

## 源码编译

1. [Go](https://golang.org/) Version 1.7 以上
2. 在 PD 项目根目录使用 `make` 命令进行编译，生成 bin/pd-ctl

## 简单例子

单命令模式：

    ./pd-ctl store -d -u http://127.0.0.1:2379

交互模式：

    ./pd-ctl -u http://127.0.0.1:2379

使用环境变量：

```bash
export PD_ADDR=http://127.0.0.1:2379
./pd-ctl
```

## 命令行参数(flags)

### \-\-pd,-u

+ 指定 PD 的地址
+ 默认地址: http://127.0.0.1:2379
+ 环境变量: PD_ADDR

### \-\-detach,-d

+ 使用单命令行模式(不进入 readline )
+ 默认值: false

## 命令(command)

### store [delete] \<store_id\>

用于显示 store 信息或者删除指定 store。

示例：

```bash
>> store            // 显示所有 store 信息
{
  "count": 3,
  "stores": [...]
}
>> store 1          // 获取 store id 为 1 的 store
  ......
>> store delete 1   // 下线 store id 为 1 的 store
  ......
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

### member [leader | delete]

用于显示 PD 成员信息或删除指定成员。

示例：

```bash
>> member                               // 显示所有成员的信息
{
  "members": [......]
}
>> member leader                        // 显示 leader 的信息
{
  "name": "pd",
  "addr": "http://192.168.199.229:2379",
  "id": 9724873857558226554
}
>> member delete pd2                    // 下线 "pd2"
Success!
```

### config [show | set \<option\> \<value\>]

用于显示或调整配置信息。

示例：

```bash
>> config show                             //　显示 config 的信息
{
  "max-snapshot-count": 3,
  "max-store-down-time": "1h",
  "leader-schedule-limit": 8,
  "region-schedule-limit": 4,
  "replica-schedule-limit": 8,
}
```

通过调整 `leader-schedule-limit` 可以控制同时进行 leader 调度的任务个数。
这个值主要影响 *leader balance* 的速度，值越大调度得越快，设置为 0 则关闭调度。
Leader 调度的开销较小，需要的时候可以适当调大。

```bash
>> config set leader-schedule-limit 4       // 最多同时进行 4 个 leader 调度
```

通过调整 `region-schedule-limit` 可以控制同时进行 region 调度的任务个数。
这个值主要影响 *region balance* 的速度，值越大调度得越快，设置为 0 则关闭调度。
Region 调度的开销较大，所以这个值不宜调得太大。

```bash
>> config set region-schedule-limit 2       // 最多同时进行 2 个 region 调度
```

通过调整 `replica-schedule-limit` 可以控制同时进行 replica 调度的任务个数。
这个值主要影响节点挂掉或者下线的时候进行调度的速度，值越大调度得越快，设置为 0 则关闭调度。
Replica 调度的开销较大，所以这个值不宜调得太大。

```bash
>> config set replica-schedule-limit 4      // 最多同时进行 4 个 replica 调度
```

### operator [show | add | remove]

用于显示和控制调度操作。

示例：

```bash
>> operator show                            // 显示所有的 operators
>> operator show admin                      // 显示所有的 admin operators
>> operator show leader                     // 显示所有的 leader operators
>> operator show region                     // 显示所有的 region operators
>> operator add transfer-leader 1 2         // 把 region 1 的 leader 调度到 store 2
>> operator add transfer-region 1 2 3 4     // 把 region 1 调度到 store 2,3,4
>> operator add transfer-peer 1 2 3         // 把 region 1 在 store 2 上的副本调度到 store 3
>> operator remove 1                        // 把 region 1 的调度操作删掉
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
