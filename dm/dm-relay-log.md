---
title: DM relay log 
summary: 介绍 DM relay log 的作用及原理
---


# DM relay log

relay log 是 DM 的一项可供选择性开启的特性。在执行增量数据同步过程中，DM 会将自己的伪装成 Mysql 的 Slave，从上游 Mysql 拉取 binlog。未开启 relay log 的情况下，多个迁移任务共用上游将会从上游 MySQL 拉取重复的 binlog，造成额外的压力。开启 relay log 后 DM 则会将 binlog 写入到本地硬盘，不仅可以减轻上游压力，而且在上游 binlog 存储空间不足的情况下，DM 还可以缓存足够的 binlog 避免同步中断。

![reley](/media/dm/dm-relay-log.png)

Relay log 的使用场景:

- Mysql 的存储空间是有限制的，一般都会设置 binlog 的最长保存时间，当上游把 binlog 清除掉之后，如果 DM 还需要对应位置的 binlog 就会拉取失败，导致同步任务出错；
- DM 在没开启 relay log 时，每增加一个同步任务都会在上游建立一条链接用于拉取 binlog，这样会对上游造成比较大的负载，开启 relay log 后同一个上游的多个同步任务可以复用已经拉倒本地的 relay log，这样就减少了对上游的压力；
- all 类型的迁移任务中，DM 需要先进行全量数据迁移，再根据 binlog 增量同步。若全量阶段持续时间较长，上游 binlog 可能会被清除，导致增量同步无法进行。若先开启了 relay log，则 DM 会自动在本地保留足够的日志，保证增量任务正常进行。

一般情况下建议开启 relay log ，但仍需知晓其可能导致的负面作用：

- 由于写 relay log 有一个落盘的过程，这里产生了外部 IO 和一些 CPU 消耗，可能导致整个同步链路变长从而增加数据同步的时延，如果是对时延要求十分敏感的同步任务暂时还不推荐使用 relay log。注意：在最新版本的 DM（>v2.0.7） 中，对这里进行了优化，增加的时延和 CPU 消耗已经相对较小了。

## Relay log 的结构

DM 的 relay log  类似 Mysql 的 relay log ，是指一组包含了数据库变更事件的文件，DM 针对数据源开启 relay log  之后，DM-Worker 的`relay-dir`目录下会产生如下文件：

```
data/worker1/relay-dir
├── 3b96fdee-f4cd-11eb-b8e5-4167400b7735.000001
│   ├── mysql-bin.000007
│   └── relay.meta
└── server-uuid.index
```

- server-uuid.index 是当前有效的 relay log  子目录列表索引文件，DM 需要利用该文件去找到对应上游的 relay log  的存放目录
- 3b96fdee-f4cd-11eb-b8e5-4167400b7735.000001 是存放当前上游的 relay log 文件的文件夹
- mysql-bin.000007 是当前正在写入的 relay log  文件
- relay.meta 记录了当前写入的 relay log  的进度信息，具体内容如下

```
binlog-name = "mysql-bin.000007" # 当前写的 binlog 文件
binlog-pos = 2415 # 当前 binlog 的位点
binlog-gtid = "3b96fdee-f4cd-11eb-b8e5-4167400b7735:1-168" # 当前 binlog 的 gtid
```

## Relay log  的清理策略

relay log  的清理 DM 提供了两种方式，手动清理和自动清理，需要注意的是这两种清理方法都不会清理活跃的 relay log 。

> **注意：**
> 
> 活跃的 relay log  定义：该 relay log  正在被同步任务使用。
> 
> 过期的 relay log  定义：该 relay log  文件最后被改动的时间与当前时间差值大于配置文件中的 `expires` 字段。
> 
> 活跃的 relay log  当前只在 Syncer Unit 被更新和写入，假设一个为 All 模式的同步任务在全量导出/导入阶段花费了超过数据源 purge 里配置的过期时间，该 relay log  依旧会被清除

1. 用 dmctl 手动清理指定的 relay log  文件：

    ```
    dmctl purge-relay -s mysql-replica-01 -f mysql-bin.000007

    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": ""
            }
        ]
    }
    ```

2. 根据上游数据源的 [purge 字段](/dm/dm-source-configuration-file.md#relay-log-清理策略配置purge-配置项)配置自动清理 relay log：

    ```
    source-id: mysql-replica-01
    enable-gtid: true
    from:
        host: 127.0.0.1
        user: root
        password: /Q7B9DizNLLTTfiZHv9WoEAKamfpIUs=
        port: 3306
    purge:
        interval: 10 # 单位秒
        expires: 100 # 单位小时
        remain-space: 15 # 单位 GB
    ```

    当该数据源被添加到 DM 集群中时并手动开启 relay log 时 DM-Worker 会每隔 `interval`即 10s 对所有的 relay log  文件进行过期检查。当发现文件过期或者磁盘空间小于`remain-space`即 15G 时，会删除该 relay log。

## DM 从什么位置开始拉取 binlog 呢？

开始拉取 relay log 的位点有以下三种情况，优先级从高到低：

1. 当前 worker 上已经有同步任务时，会从所有同步任务中找到当前需要的最小的同步位点开始拉取 binlog；
2. 当 Source/Worker 的配置文件中配置了 relay log  的位点时，会从该位点开始拉取；
3. 当不满足上述条件时，从当前上游的最新位点（show master status）开始拉取。