---
title: 集群和同步任务管理
category: reference
---

# 集群和同步任务管理

目前 TiCDC 提供命令行工具 `cdc cli` 和 HTTP 接口两种方式管理集群和同步任务。

## 使用 cdc cli 工具管理集群状态和数据同步

### TiCDC 服务进程 (capture) 管理

- 查询 capture 列表

```
$ cdc cli capture list
[
        {
                "id": "6d92386a-73fc-43f3-89de-4e337a42b766",
                "is-owner": true
        },
        {
                "id": "b293999a-4168-4988-a4f4-35d9589b226b",
                "is-owner": false
        }
]
```

### 同步任务 (changefeed) 管理

- 创建 changefeed

```
$ cdc cli changefeed create --sink-uri="mysql://root:123456@127.0.0.1:3306/"
create changefeed ID: 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f info {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"config":{"filter-case-sensitive":false,"filter-rules":null,"ignore-txn-commit-ts":null}}
```

- 查询 changefeed 列表

```
$ cdc cli changefeed list
[
        {
                "id": "28c43ffc-2316-4f4f-a70b-d1a7c59ba79f"
        }
]
```

- 查询特定 changefeed，对应于某个同步任务的信息和状态

```
$ cdc cli changefeed query --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
{
        "info": {
                "sink-uri": "mysql://root:123456@127.0.0.1:3306/",
                "opts": {},
                "create-time": "2020-03-12T22:04:08.103600025+08:00",
                "start-ts": 415241823337054209,
                "target-ts": 0,
                "admin-job-type": 0,
                "config": {
                        "filter-case-sensitive": false,
                        "filter-rules": null,
                        "ignore-txn-commit-ts": null
                }
        },
        "status": {
                "resolved-ts": 415241860902289409,
                "checkpoint-ts": 415241860640145409,
                "admin-job-type": 0
        }
}
```

### 同步子任务处理单元 (processor) 管理

- 查询 processor 列表

```
$ cdc cli processor list
[
        {
                "id": "9f84ff74-abf9-407f-a6e2-56aa35b33888",
                "capture-id": "b293999a-4168-4988-a4f4-35d9589b226b",
                "changefeed-id": "28c43ffc-2316-4f4f-a70b-d1a7c59ba79f"
        }
]
```

- 查询特定 processor，对应于某个节点处理的同步子任务信息和状态

```
$ cdc cli processor query --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f --capture-id=b293999a-4168-4988-a4f4-35d9589b226b
{
        "status": {
                "table-infos": [
                        {
                                "id": 45,
                                "start-ts": 415241823337054209
                        }
                ],
                "table-p-lock": null,
                "table-c-lock": null,
                "admin-job-type": 0
        },
        "position": {
                "checkpoint-ts": 415241893447467009,
                "resolved-ts": 415241893971492865
        }
}
```

## 使用 HTTP 接口管理集群状态和数据同步

目前 HTTP 接口提供一些基础的查询和运维功能。在以下接口描述中，假设 CDC server 的 状态查询接口 ip 地址为 127.0.0.1，8300 状态端口地址（在启动 CDC server 时通过 --status-addr=ip:port 指定绑定的 ip 和端口）。在后续版本中我们也会将这部分功能集成到 `cdc cli` 中。

### 获取 CDC server 状态信息的接口

```
$ curl http://127.0.0.1:8300/status
{
 "version": "0.0.1",
 "git_hash": "863f8ea889b144244ff53593a45c47ad22d37396",
 "id": "6d92386a-73fc-43f3-89de-4e337a42b766", # capture id
 "pid": 12102    # cdc server pid
}
```

### 驱逐 owner 节点

```
// 仅对 owner 节点请求有效
$ curl -X POST http://127.0.0.1:8300/capture/owner/resign
{
 "status": true,
 "message": ""
}

// 对非 owner 节点请求返回错误
$ curl -X POST http://127.0.0.1:8301/capture/owner/resign
election: not leader
```

### 停止同步任务

```
$ curl -X POST -d "admin-job=1&cf-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f" http://127.0.0.1:8301/capture/owner/admin
{
 "status": true,
 "message": ""
}
```

- admin-job=1，表示停止任务，停止任务后所有同步 processor 会结束退出，同步任务的配置和同步状态都会保留，可以从 CheckpointTs 恢复任务
- cf-id=xxx，为需要操作的 changefeed ID

### 恢复同步任务

```
$ curl -X POST -d "admin-job=2&cf-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f" http://127.0.0.1:8301/capture/owner/admin
{
 "status": true,
 "message": ""
}
```

- admin-job=2，表示恢复任务，同步任务从 CheckpointTs 继续同步
- cf-id=xxx，为需要操作的 changefeed ID

### 删除同步任务

```
$ curl -X POST -d "admin-job=3&cf-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f" http://127.0.0.1:8301/capture/owner/admin
{
 "status": true,
 "message": ""
}
```

- admin-job=3，表示删除任务，接口请求后会结束所有同步 processor，并清理同步任务配置信息。同步状态保留，只提供查询，没有其他实际功能。
- cf-id=xxx，为需要操作的 changefeed ID

## 异常管理

### TiCDC 向下游同步语句出错

TiCDC 向下游执行 DDL/DML 出错后会自动停止同步任务，

- 如果是因为下游异常、网络抖动等情况，可以直接恢复任务重试；
- 如果是因为下游不兼容的 SQL 问题，重试不会成功，可以通过同步配置的 ignore-txn-commit-ts 参数跳过指定 CommitTs 对应的事务，然后恢复同步任务
