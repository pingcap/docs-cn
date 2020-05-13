---
title: 管理集群和同步任务
category: reference
aliases: ['/docs-cn/dev/reference/tools/ticdc/manage/']
---

# 管理集群和同步任务

目前 TiCDC 提供命令行工具 `cdc cli` 和 HTTP 接口两种方式来管理集群和同步任务。

## 使用 `cdc cli` 工具来管理集群状态和数据同步

以下内容介绍如何使用 `cdc cli` 工具来管理集群状态和数据同步。

### 管理 TiCDC 服务进程 (`capture`)

- 查询 `capture` 列表：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli capture list
    ```

    ```
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

### 管理同步任务 (`changefeed`)

- 创建 `changefeed`：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed create --sink-uri="mysql://root:123456@127.0.0.1:3306/"
    create changefeed ID: 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f info {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"config":{"filter-case-sensitive":false,"filter-rules":null,"ignore-txn-commit-ts":null}}
    ```

- 查询 `changefeed` 列表：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed list
    ```

    ```
    [
            {
                    "id": "28c43ffc-2316-4f4f-a70b-d1a7c59ba79f"
            }
    ]
    ```

- 查询特定 `changefeed`，对应于某个同步任务的信息和状态：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed query --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
    ```

    ```
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

### 管理同步子任务处理单元 (`processor`)

- 查询 `processor` 列表：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli processor list
    ```

    ```
    [
            {
                    "id": "9f84ff74-abf9-407f-a6e2-56aa35b33888",
                    "capture-id": "b293999a-4168-4988-a4f4-35d9589b226b",
                    "changefeed-id": "28c43ffc-2316-4f4f-a70b-d1a7c59ba79f"
            }
    ]
    ```

- 查询特定 `processor`，对应于某个节点处理的同步子任务信息和状态：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli processor query --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f --capture-id=b293999a-4168-4988-a4f4-35d9589b226b
    ```

    ```
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

目前 HTTP 接口提供一些基础的查询和运维功能。在以下接口描述中，假设 TiCDC server 的状态查询接口 IP 地址为 `127.0.0.1`，状态端口地址为 `8300`（在启动 TiCDC server 时通过 `--status-addr=ip:port` 指定绑定的 IP 和端口）。在后续版本中这部分功能也会集成到 `cdc cli` 中。

### 获取 TiCDC server 状态信息的接口

使用以下命令获取 CDC server 状态信息的接口：

{{< copyable "shell-regular" >}}

```shell
curl http://127.0.0.1:8300/status
```

```
{
 "version": "0.0.1",
 "git_hash": "863f8ea889b144244ff53593a45c47ad22d37396",
 "id": "6d92386a-73fc-43f3-89de-4e337a42b766", # capture id
 "pid": 12102    # cdc server pid
}
```

### 驱逐 owner 节点

{{< copyable "shell-regular" >}}

```shell
curl -X POST http://127.0.0.1:8300/capture/owner/resign
```

以上命令仅对 owner 节点请求有效。

```
{
 "status": true,
 "message": ""
}
```

{{< copyable "shell-regular" >}}

```shell
curl -X POST http://127.0.0.1:8301/capture/owner/resign
```

以上命令对非 owner 节点请求返回错误。

```
election: not leader
```

### 停止同步任务

使用以下命令来停止同步任务：

{{< copyable "shell-regular" >}}

```shell
curl -X POST -d "admin-job=1&cf-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f" http://127.0.0.1:8301/capture/owner/admin
```

```
{
 "status": true,
 "message": ""
}
```

以上命令中：

- `admin-job=1` 表示停止任务。停止任务后所有同步 `processor` 会结束退出，同步任务的配置和同步状态都会保留，可以从 `checkpoint-ts` 恢复任务。
- `cf-id=xxx` 为需要操作的 `changefeed` ID。

### 恢复同步任务

使用以下命令恢复同步任务：

{{< copyable "shell-regular" >}}

```shell
curl -X POST -d "admin-job=2&cf-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f" http://127.0.0.1:8301/capture/owner/admin
```

```
{
 "status": true,
 "message": ""
}
```

以上命令中：

- `admin-job=2` 表示恢复任务，同步任务从 `checkpoint-ts` 继续同步。
- `cf-id=xxx` 为需要操作的 `changefeed` ID。

### 删除同步任务

使用以下命令删除同步任务：

{{< copyable "shell-regular" >}}

```shell
curl -X POST -d "admin-job=3&cf-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f" http://127.0.0.1:8301/capture/owner/admin
```

```
{
 "status": true,
 "message": ""
}
```

- `admin-job=3`，表示删除任务，接口请求后会结束所有同步 `processor`，并清理同步任务配置信息。同步状态保留，只提供查询，没有其他实际功能。
- `cf-id=xxx` 为需要操作的 `changefeed` ID。
