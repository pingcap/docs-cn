#PD Control 使用说明

PD Control 是 PD 的命令行工具，用于获取集群状态信息和调整集群

## 源码编译
1. [*Go*](https://golang.org/) Version 1.7 以上 
2. 在 PD 项目根目录使用 `make` 命令进行编译，生成 bin/pd-ctl

## 参数说明及示例

### 简单例子:

单命令模式：

    ./pd-ctl store -d -u 127.0.0.1:2379

交互模式:

    ./pd-ctl -u 127.0.0.1:2379

使用环境变量:

``` 
export PD_ADDR=http://127.0.0.1:2379
./pd-ctl
```

### 标志(flags)
#### --pd,-u
+ 指定 PD 的地址 
+ 默认地址: http://127.0.0.1:2379
+ 环境变量: PD_ADDR

#### --detach,-d
+ 使用单命令行模式(不进入 readline ) 
+ 默认值: false

### 命令(command)
#### store [delete] <store_id>
用于显示 store 信息或者删除指定 store

##### 示例
``` 
>> store            // 显示所有 store 信息
{
  "count": 3,
  "stores": [...]
}
>> store 1          // 获取 store id 为 1 的store
  ......
>> store delete 1   // 下线 store id 为 1 的 store
  ......
```

#### config [show | set  \<option\> \<value\>]
用于调整配置信息
##### 示例
``` 
>> config show                             //　显示 config 的信息
{
  "min-region-count": 10,
  "min-leader-count": 10,
  "max-snapshot-count": 3,
  "min-balance-diff-ratio": 0.01,
  "max-store-down-duration": "30m0s",
  "leader-schedule-limit": 8,
  "leader-schedule-interval": "10s",
  "storage-schedule-limit": 4,
  "storage-schedule-interval": "30s"
}
>> config set leader-schedule-interval 20s  // 设置 leader-schedule-interval 为 20 s
Success!
```
#### Member [leader | delete]
用于显示 PD 成员信息或删除指定成员
##### 示例
```
>> member                              // 显示所有成员的信息
{
  "members": [......] 
}
>> member leader                        // 显示 leader 的信息
{
  "name": "pd",
  "addr": "http://192.168.199.229:2379",
  "id": 9724873857558226554
}
>> member delete pd2                     // 下线 PD2
Success!
```

#### Region <region_id>
用于显示 Region 信息
##### 示例
```
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

