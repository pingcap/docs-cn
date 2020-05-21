---
title: 使用 TiUP 扩容缩容 TiDB 集群
category: how-to
aliases: ['/docs-cn/dev/how-to/scale/with-tiup/']
---

# 使用 TiUP 扩容缩容 TiDB 集群

TiDB 集群可以在不中断线上服务的情况下进行扩容和缩容。

本文介绍如何使用 TiUP 扩容缩容集群中的 TiDB、TiKV、PD、TiCDC 或者 TiFlash 节点。如未安装 TiUP，可参考[升级文档中的步骤](/upgrade-tidb-using-tiup.md#2-在中控机器上安装-tiup)，将集群 Import 到 TiUP 环境中，再使用 TiUP 进行扩容缩容。

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
> 添加 PD、TiCDC 节点和添加 TiDB 节点的步骤类似。添加 TiKV 节点前，建议预先根据集群的负载情况调整 PD 调度参数。

### 1.1 编写扩容拓扑配置

> **注意：**
>
> 默认情况下，可以不填写端口以及目录信息。但在单机多实例场景下，则需要分配不同的端口以及目录，如果有端口或目录冲突，会在部署或扩容时提醒。

在 scale-out.yaml 文件添加扩容拓扑配置：

{{< copyable "shell-regular" >}}

```shell
vi scale-out.yaml
```

{{< copyable "" >}}

```ini
tidb_servers:

 - host: 10.0.1.5

   ssh_port: 22

   port: 4000

   status_port: 10080

   deploy_dir: /data/deploy/install/deploy/tidb-4000

   log_dir: /data/deploy/install/log/tidb-4000
TiKV 配置文件参考：

{{< copyable "" >}}

```ini
tikv_servers:

 - host: 10.0.1.5

   ssh_port: 22

   port: 20160
  
   status_port: 20180

   deploy_dir: /data/deploy/install/deploy/tikv-20160

   data_dir: /data/deploy/install/data/tikv-20160

   log_dir: /data/deploy/install/log/tikv-20160
PD 配置文件参考：

{{< copyable "" >}}

```ini
pd_servers:

 - host: 10.0.1.5

   ssh_port: 22

   name: pd-1

   client_port: 2379

   peer_port: 2380

   deploy_dir: /data/deploy/install/deploy/pd-2379

   data_dir: /data/deploy/install/data/pd-2379

   log_dir: /data/deploy/install/log/pd-2379
```

可以使用 `tiup cluster edit-config <cluster-name>` 查看当前集群的配置信息，因为其中的 `global` 和 `server_configs` 参数配置，默认会被 `scale-out.yaml` 继承。


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

打开浏览器访问监控平台 <http://10.0.1.5:3000>，监控整个集群和新增节点的状态。

扩容后，集群拓扑结构如下所示：

| 主机 IP   | 服务   | 
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD   | 
| 10.0.1.5   | **TiDB** + TiKV + Monitor   | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 

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

打开浏览器访问监控平台 <http://10.0.1.5:3000>，监控整个集群和新增节点的状态。

扩容后，集群拓扑结构如下所示：

| 主机 IP   | 服务   | 
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD + **TiFlash**    | 
| 10.0.1.5   | TiDB+ TiKV + Monitor   | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 

## 3. 缩容 TiDB/TiKV/PD/TiCDC 节点

如果要移除 IP 地址为 10.0.1.5 的一个 TiKV 节点，可以按照如下步骤进行操作。

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

10.0.1.5:9090   prometheus   10.0.1.5    9090                             Up      data/prometheus-9090    deploy/prometheus-9090

10.0.1.5:3000   grafana      10.0.1.5    3000                             Up      -                       deploy/grafana-3000

10.0.1.5:9093   alertmanager 10.0.1.5    9093/9094                        Up      data/alertmanager-9093  deploy/alertmanager-9093
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

打开浏览器访问监控平台 <http://10.0.1.5:3000>，监控整个集群的状态。

调整后，拓扑结构如下：

| Host IP   | Service   | 
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD + TiFlash   | 
| 10.0.1.5   | TiDB + Monitor**（TiKV 已删除）**   | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 

## 4. 缩容 TiFlash 节点

如果要缩容 IP 地址为 10.0.1.4 的一个 TiFlash 节点，，可以按照如下步骤进行操作。

> **注意：**
>
> 本节介绍的缩容流程不会删除缩容节点上的数据文件，如需再次上线该节点，请先手动删除原来的数据文件。

### 4.1 下线该 TiFlash 节点

参考[下线 TiFlash 节点](/tiflash/maintain-tiflash.md#下线-tiflash-节点)一节，对要进行缩容的 TiFlash 节点进行下线操作。

### 4.2 检查节点是否下线成功

使用 Grafana 或者 pd-ctl 检查节点是否下线成功（下线需要一定时间）。

### 4.3 缩容 TiFlash 

TiFlash 对应的 `store` 消失，或者 `state_name` 变成 `Tombstone` 后，表示 TiFlash 节点已经下线成功，这个时候可以执行如下命令缩容 TiFlash ：

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:9000
```

### 4.4 查看集群状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

打开浏览器访问监控平台 <http://10.0.1.5:3000>，监控整个集群的状态。

调整后，拓扑结构如下：

| Host IP   | Service   | 
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD**（TiFlash 已删除）**  | 
| 10.0.1.5   | TiDB + Monitor  | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 
