---
title: TiFlash 集群扩缩容
category: reference
---

# TiFlash 集群扩缩容

本文介绍扩缩容 TiFlash 集群节点的步骤。

## 扩容 TiFlash 节点

假如需要在 172.19.0.104 上新增 TiFlash 节点，步骤如下：

1. 编写 scale-out.yaml 文件，添加该 TiFlash 节点信息（目前只支持 ip，不支持域名）：

    {{< copyable "" >}}

    ```ini
    tiflash_servers:
      - host: 172.19.0.104
    ```

2. 运行扩容命令

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out test scale-out.yaml
    ```

3. 查看集群状态

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

4. 打开浏览器访问监控平台，监控整个集群和新增节点的状态。

## 缩容 TiFlash 节点

以停止 172.19.0.104 节点的服务为例，缩容该 TiFlash 节点的步骤如下。

> **注意：**
>
> 本节介绍的下线流程不会删除下线节点上的数据文件，如需再次上线，请先手动删除。

1. 首先参考[下线 TiFlash 节点](/reference/tiflash/maintain.md#下线-tiflash-节点)章节，对要进行缩容的 TiFlash 节点进行下线操作。

2. 使用 Grafana 或者 pd-ctl 检查节点是否下线成功（下线需要一定时间）。

3. 等待 TiFlash 对应的 `store` 消失，或者 `state_name` 变成 `Tombstone` 后，执行如下命令关闭 TiFlash 进程：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-in test --node 172.19.0.104:9000
    ```

4. 查看集群状态

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

5. 打开浏览器访问监控平台，监控整个集群的状态。
