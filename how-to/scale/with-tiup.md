---
title: 使用 TiUP 扩容缩容 TiDB 集群
category: how-to
---

# 使用 TiUP 扩容缩容 TiDB 集群

TiDB 集群可以在不影响线上服务的情况下进行扩容和缩容。

本文介绍如何使用 TiUP 扩容缩容集群中的 TiDB、TiKV 或者 PD 节点。

原拓扑结构如下所示：

| 主机 IP   | 服务   | 
|:----|:----|
| 10.0.1.4   | TiDB + PD    | 
| 10.0.1.5   | TiKV + Monitor   | 
| 10.0.1.1   | TiKV   | 
| 10.0.1.2   | TiKV    | 

## 1. 扩容 TiDB/TiKV/PD 节点

如果要添加一个 TiDB 节点，IP 地址为 10.0.1.5，可以按照如下步骤进行操作。

> **注意：**
>
> 添加 TiKV 和 PD 节点和添加 TiDB 节点的步骤类似。

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

配置后，现拓扑结构如下所示：

| 主机 IP   | 服务   | 
|:----|:----|
| 10.0.1.4   | TiDB + PD    | 
| 10.0.1.5   | **TiDB** + TiKV + Monitor   | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 

### 1.2 执行扩容命令

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-out test scale-out.yaml
```

预期输出 Scaled cluster `test` in successfully 信息，表示扩容操作成功。

### 1.3 检查集群状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display testy
```

打开浏览器访问监控平台 <http://10.0.1.5:3200>，监控整个集群和新增节点的状态。

## 2. 缩容 TiDB/TiKV/PD 节点

如果要移除一个 TiKV 节点，IP 地址为 10.0.1.5，可以按照如下步骤进行操作。

> **注意：**
>
> 移除 TiKV 和 PD 节点和移除 TiDB 节点的步骤类似。

### 2.1 查看节点 ID 信息

{{< copyable "shell-regular" >}}

```shell
tiup cluster display test
```

```
Starting /root/.tiup/components/cluster/v0.3.3/cluster display testy 

TiDB Cluster: test

TiDB Version: v4.0.0-beta.1

ID              Role Host              Ports        Status  Data Dir                Deploy Dir

--              ---- ----              -----        ------  --------                ----------

10.0.1.4:2379   pd 10.0.1.4            2379/2380    Healthy data/pd-2379            deploy/pd-2379

10.0.1.1:20160  tikv 10.0.1.1          20160/20180  Up      data/tikv-20160         deploy/tikv-20160

10.0.1.2:20160  tikv 10.0.1.2          20160/20180  Up      data/tikv-20160         deploy/tikv-20160

10.0.1.5:20160  tikv 10.0.1.5          20160/20180  Up      data/tikv-20160         deploy/tikv-20160

10.0.1.4:4000   tidb 10.0.1.4          4000/10080   Up      -                       deploy/tidb-4000

10.0.1.5:4000   tidb 10.0.1.5          4000/10080   Up      -                       deploy/tidb-4000

10.0.1.5:9290   prometheus 10.0.1.5    9290         Up      data/prometheus-9290    deploy/prometheus-9290

10.0.1.5:3200   grafana 10.0.1.5       3200         Up      -                       deploy/grafana-3200

10.0.1.5:9293   alertmanager 10.0.1.5  9293/9294    Up      data/alertmanager-9293  deploy/alertmanager-9293
```

### 2.2 执行缩容操作

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-in testy --node 10.0.1.5:20160
```

其中 `--node` 参数为需要下线节点的 ID。

预期输出 Scaled cluster `test` in successfully 信息，表示扩容操作成功。

### 2.3 检查集群状态

下线需要一定时间，下线节点的状态变为 Tombstone 就说明下线成功。

执行如下命令检查节点是否下线成功：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display testy
```

现拓扑结构如下：

| Host IP   | Service   | 
|:----|:----|
| 10.0.1.4   | TiDB + PD    | 
| 10.0.1.5   | TiDB + Monitor**（TiKV 已删除）**   | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 

打开浏览器访问监控平台 <http://10.0.1.5:3200>，监控整个集群和新增节点的状态。
