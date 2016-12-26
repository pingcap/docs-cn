PD Control 使用说明 
========

PD Control 是 PD 的命令行工具，用于获取集群状态信息和调整集群

## 源码编译
1. [*Go*](https://golang.org/) Version 1.5 以上 
2. 在 PD 项目根目录使用 make 命令进行编译

## 参数说明及示例

### 简单例子:

    ./pd-ctl store  -u 127.0.0.1:2379

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
>> store
{
  "count": 3,
  "stores": [...]
}
>> store 1
  ......
>> store delete 1
  ......
```

#### config [show | set  \<option\> \<value\>]
用于调整配置信息
##### 示例
``` 
>> config show
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
>> config set leader-schedule-interval 20s
Success!
```
#### Member [leader | delete]
用于显示 PD 成员信息或删除指定成员
##### 示例
```
>> member
{
  "members": [......] 
}
>> member leader
{
  "name": "pd",
  "addr": "http://192.168.199.229:2379",
  "id": 9724873857558226554
}
>> member delete pd2
Success!
```

#### Region <region_id>
用于显示 Region 信息
#### 示例
```
>> region
{
  "count": 1,
  "regions": [......]
}

>> region 2
{
  "region": {
      "id": 2,
      ......
  }
  "leader": {
      ......
  }
}
