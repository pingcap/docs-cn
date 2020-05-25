---
title: 使用 TiUP 扩容缩容 TiDB 集群
category: how-to
aliases: ['/docs-cn/dev/how-to/scale/with-tiup/']
---

# 使用 TiUP 扩容缩容 TiDB 集群

TiDB 集群可以在不影响线上服务的情况下进行扩容和缩容。

本文介绍如何使用 TiUP 扩容缩容集群中的 TiDB、TiKV、PD、TiCDC 或者 TiFlash 节点。如未安装 TiUP，可参考[升级文档中的步骤](/upgrade-tidb-using-tiup.md#2-在中控机器上安装-tiup)，将集群 import 到 TiUP 环境中，再进行扩容缩容。

你可以通过 `tiup cluster list` 查看当前的集群名称列表。

例如，集群原拓扑结构如下所示：

| 主机 IP   | 服务   | 
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD   | 
| 10.0.1.5   | TiKV + Monitor   | 
| 10.0.1.1   | TiKV   | 
| 10.0.1.2   | TiKV    |

## 1. 扩容 TiDB/TiKV/PD/TiCDC 节点

如果要添加一个 TiDB 节点，IP 地址为 10.0.1.5，可以按照如下步骤进行操作。

> **注意：**
>
> 添加 TiKV、PD、TiCDC 节点和添加 TiDB 节点的步骤类似。

### 1.1 编写扩容拓扑配置

> **注意：**
>
> 默认情况下，可以不填端口信息。但在单机多实例场景下，你需要分配不同的端口，如果有端口或目录冲突，会在部署或扩容时提醒。

在 scale-out.yaml 文件添加扩容拓扑配置：

{{< copyable "shell-regular" >}}

```shell
vi scale-out.yaml
```

```
tidb_servers:

 - host: 10.0.1.5

   ssh_port: 22

   port: 4000

   status_port: 10080
```

你可以使用 `tiup cluster edit-config <cluster-name>` 查看当前集群的整体配置，其中 global 和 server_configs 的全局配置也会在 `scale-out.yaml` 中生效。

配置后，集群现拓扑结构如下所示：

| 主机 IP   | 服务   | 
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD   | 
| 10.0.1.5   | **TiDB** + TiKV + Monitor   | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 

### 1.2 执行扩容命令

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-out <cluster-name> scale-out.yaml
```

预期输出 Scaled cluster `<cluster-name>` out successfully 信息，表示扩容操作成功。

### 1.3 检查集群状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

打开浏览器访问监控平台 <http://10.0.1.5:3200>，监控整个集群和新增节点的状态。

## 2. 扩容 TiFlash 节点

如果要添加一个 TiFlash 节点，IP 地址为 10.0.1.4，可以按照如下步骤进行操作。

### 2.1 添加节点信息到 scale-out.yaml 文件

编写 scale-out.yaml 文件，添加该 TiFlash 节点信息（目前只支持 ip，不支持域名）：

{{< copyable "" >}}

```ini
tiflash_servers:
    - host: 10.0.1.4
```

### 2.2 运行扩容命令

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-out <cluster-name> scale-out.yaml
```

### 2.3 查看集群状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

打开浏览器访问监控平台 <http://10.0.1.5:3200>，监控整个集群和新增节点的状态。

## 3. 缩容 TiDB/TiKV/PD/TiCDC 节点

如果要移除一个 TiKV 节点，IP 地址为 10.0.1.5，可以按照如下步骤进行操作。

> **注意：**
>
> 移除 TiDB、PD、TiCDC 节点和移除 TiKV 节点的步骤类似。

### 3.1 查看节点 ID 信息

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

```
Starting /root/.tiup/components/cluster/v0.4.6/cluster display <cluster-name> 

TiDB Cluster: <cluster-name>

TiDB Version: v4.0.0-rc

ID              Role         Host        Ports                            Status  Data Dir                Deploy Dir

--              ----         ----        -----                            ------  --------                ----------

10.0.1.4:2379   pd           10.0.1.4    2379/2380                        Healthy data/pd-2379            deploy/pd-2379

10.0.1.1:20160  tikv         10.0.1.1    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160

10.0.1.2:20160  tikv         10.0.1.2    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160

10.0.1.5:20160  tikv         10.0.1.5    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160

10.0.1.3:4000   tidb         10.0.1.3    4000/10080                       Up      -                       deploy/tidb-4000

10.0.1.4:4000   tidb         10.0.1.4    4000/10080                       Up      -                       deploy/tidb-4000

10.0.1.5:4000   tidb         10.0.1.5    4000/10080                       Up      -                       deploy/tidb-4000

10.0.1.3:9000   tiflash      10.0.1.3    9000/8123/3930/20170/20292/8234  Up      data/tiflash-9000       deploy/tiflash-9000

10.0.1.4:9000   tiflash      10.0.1.4    9000/8123/3930/20170/20292/8234  Up      data/tiflash-9000       deploy/tiflash-9000

10.0.1.5:9290   prometheus   10.0.1.5    9290                             Up      data/prometheus-9290    deploy/prometheus-9290

10.0.1.5:3200   grafana      10.0.1.5    3200                             Up      -                       deploy/grafana-3200

10.0.1.5:9293   alertmanager 10.0.1.5    9293/9294                        Up      data/alertmanager-9293  deploy/alertmanager-9293
```

### 3.2 执行缩容操作

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.5:20160
```

其中 `--node` 参数为需要下线节点的 ID。

预期输出 Scaled cluster `<cluster-name>` in successfully 信息，表示缩容操作成功。

### 3.3 检查集群状态

下线需要一定时间，下线节点的状态变为 Tombstone 就说明下线成功。

执行如下命令检查节点是否下线成功：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

现拓扑结构如下：

| Host IP   | Service   | 
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD + TiFlash   | 
| 10.0.1.5   | TiDB + Monitor**（TiKV 已删除）**   | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 

打开浏览器访问监控平台 <http://10.0.1.5:3200>，监控整个集群的状态。

## 4. 缩容 TiFlash 节点

如果要下线一个 TiFlash 节点，IP 地址为 10.0.1.4，可以按照如下步骤进行操作。

> **注意：**
>
> 如果下线该 TiFlash 节点后，TiFlash 集群剩余节点数大于等于所有数据表的最大副本数，可跳过下列步骤。

1. 在 TiDB 客户端中针对所有副本数大于集群剩余 TiFlash 节点数的表执行：

    {{< copyable "sql" >}}

    ```sql
    alter table <db-name>.<table-name> set tiflash replica 0;
    ```

2. 等待相关表的 TiFlash 副本被删除（按照[查看表同步进度](/tiflash/use-tiflash.md#查看表同步进度)一节操作，查不到相关表的同步信息时即为副本被删除）。

接下来，请任选下列方案其一进行缩容。

### 4.1 通过 TiUP 缩容节点

1. 通过以下命令确定需要下线的节点名称：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

2. 调用 scale-in 命令执行下线节点，例如步骤 1 中获得该节点名为 `10.0.1.4:9000`

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:9000
    ```

### 4.2 手动缩容 TiFlash 节点

1. 在 [pd-ctl](/pd-control.md) (tidb-ansible 目录下的 `resources/bin` 包含对应的二进制文件) 中输入 store 命令，查看该 TiFlash 节点对应的 store id。

2. 在 pd-ctl 中输入 `store delete <store_id>`，其中 <store_id> 为上一步查到的该 TiFlash 节点对应的 store id。

3. 等待该 TiFlash 节点对应的 store 消失或者 state_name 变成 Tombstone 再关闭 TiFlash 进程。

> **注意：**
>
> 如果在集群中所有的 TiFlash 节点停止运行之前，没有取消所有同步到 TiFlash 的表，则需要手动在 PD 中清除同步规则，否则无法成功完成 TiFlash 节点的下线。

手动在 PD 中清除同步规则的步骤如下：

1. 查询当前 PD 实例中所有与 TiFlash 相关的的数据同步规则。

    {{< copyable "shell-regular" >}}

    ```shell
    curl http://<pd_ip>:<pd_port>/pd/api/v1/config/rules/group/tiflash
    ```

    ```
    [
      {
        "group_id": "tiflash",
        "id": "table-45-r",
        "override": true,
        "start_key": "7480000000000000FF2D5F720000000000FA",
        "end_key": "7480000000000000FF2E00000000000000F8",
        "role": "learner",
        "count": 1,
        "label_constraints": [
          {
            "key": "engine",
            "op": "in",
            "values": [
              "tiflash"
            ]
          }
        ]
      }
    ]
    ```

2. 删除所有与 TiFlash 相关的数据同步规则。以 `id` 为 `table-45-r` 的规则为例，通过以下命令可以删除该规则。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
    ```

### 4.3 查看集群状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

打开浏览器访问监控平台 <http://10.0.1.5:3200>，监控整个集群的状态。
