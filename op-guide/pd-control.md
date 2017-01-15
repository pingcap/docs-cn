# PD Control 使用说明

PD Control 是 PD 的命令行工具，用于获取集群状态信息和调整集群。

## 源码编译

1. [*Go*](https://golang.org/) Version 1.7 以上
2. 在 PD 项目根目录使用 `make` 命令进行编译，生成 bin/pd-ctl

## 简单例子

单命令模式：

    ./pd-ctl store -d -u 127.0.0.1:2379

交互模式：

    ./pd-ctl -u 127.0.0.1:2379

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
  "min-region-count": 10,
  "min-leader-count": 10,
  "max-snapshot-count": 3,
  "min-balance-diff-ratio": 0.01,
  "max-store-down-duration": "30m0s",
  "leader-schedule-limit": 8,
  "leader-schedule-interval": "1s",
  "storage-schedule-limit": 4,
  "storage-schedule-interval": "1s",
  "replica-schedule-limit": 8,
  "replica-schedule-interval": "1s",
}
```

通过调整 `min-balance-diff-ratio` 可以控制什么时候开始调度。

```bash
>> config set min-balance-diff-ratio 0.1    // 磁盘使用率相差 10% 的时候开始调度
```

通过调整 `leader-schedule-limit` 可以控制同时进行 leader 调度的任务个数。
这个值主要影响 *leader balance* 的速度，值越大调度得越快，设置为 0 则关闭调度。
Leader 调度的开销较小，需要的时候可以适当调大。

```bash
>> config set leader-schedule-limit 4       // 最多同时进行 4 个 leader 调度
```

通过调整 `storage-schedule-limit` 可以控制同时进行 storage 调度的任务个数。
这个值主要影响 *storage balance* 的速度，值越大调度得越快，设置为 0 则关闭调度。
Storage 调度的开销较大，所以这个值不宜调得太大。

```bash
>> config set storage-schedule-limit 2      // 最多同时进行 2 个 storage 调度
```

通过调整 `replica-schedule-limit` 可以控制同时进行 replica 调度的任务个数。
这个值主要影响节点挂掉或者下线的时候进行调度的速度，值越大调度得越快，设置为 0 则关闭调度。
Replica 调度的开销较大，所以这个值不宜调得太大。

```bash
>> config set replica-schedule-limit 4      // 最多同时进行 4 个 replica 调度
```
