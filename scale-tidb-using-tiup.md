---
title: 使用 TiUP 扩容缩容 TiDB 集群
aliases: ['/docs-cn/stable/scale-tidb-using-tiup/','/docs-cn/v4.0/scale-tidb-using-tiup/','/docs-cn/stable/how-to/scale/with-tiup/','/docs-cn/stable/reference/tiflash/scale/','/docs-cn/v4.0/reference/tiflash/scale/']
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

## 扩容 TiDB/PD/TiKV 节点

如果要添加一个 TiDB 节点，IP 地址为 10.0.1.5，可以按照如下步骤进行操作。

> **注意：**
>
> 添加 PD 节点和添加 TiDB 节点的步骤类似。添加 TiKV 节点前，建议预先根据集群的负载情况调整 PD 调度参数。

### 1. 编写扩容拓扑配置

> **注意：**
>
> - 默认情况下，可以不填写端口以及目录信息。但在单机多实例场景下，则需要分配不同的端口以及目录，如果有端口或目录冲突，会在部署或扩容时提醒。
>
> - 从 TiUP v1.0.0 开始，扩容配置会继承原集群配置的 global 部分。

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
```

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
```

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

可以使用 `tiup cluster edit-config <cluster-name>` 查看当前集群的配置信息，因为其中的 `global` 和 `server_configs` 参数配置默认会被 `scale-out.yaml` 继承，因此也会在 `scale-out.yaml` 中生效。

### 2. 执行扩容命令

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-out <cluster-name> scale-out.yaml
```

> **注意：**
>
> 此处假设当前执行命令的用户和新增的机器打通了互信，如果不满足已打通互信的条件，需要通过 `-p` 来输入新机器的密码，或通过 `-i` 指定私钥文件。

预期输出 Scaled cluster `<cluster-name>` out successfully 信息，表示扩容操作成功。

### 3. 检查集群状态

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

## 扩容 TiFlash 节点

如果要添加一个 TiFlash 节点，其 IP 地址为 `10.0.1.4`，可以按照如下步骤进行操作。

> **注意：**
>
> 在原有 TiDB 集群上新增 TiFlash 组件需要注意：
>
> 1. 首先确认当前 TiDB 的版本支持 TiFlash，否则需要先升级 TiDB 集群至 4.0 RC 以上版本。
> 2. 执行 `tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> config set enable-placement-rules true` 命令，以开启 PD 的 Placement Rules 功能。或通过 [pd-ctl](/pd-control.md) 执行对应的命令。

### 1. 添加节点信息到 scale-out.yaml 文件

编写 scale-out.yaml 文件，添加该 TiFlash 节点信息（目前只支持 ip，不支持域名）：

{{< copyable "" >}}

```ini
tiflash_servers:
  - host: 10.0.1.4
```

### 2. 运行扩容命令

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-out <cluster-name> scale-out.yaml
```

> **注意：**
>
> 此处假设当前执行命令的用户和新增的机器打通了互信，如果不满足已打通互信的条件，需要通过 `-p` 来输入新机器的密码，或通过 `-i` 指定私钥文件。

### 3. 查看集群状态

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

## 扩容 TiCDC 节点

如果要添加 TiCDC 节点，IP 地址为 10.0.1.3、10.0.1.4，可以按照如下步骤进行操作。

### 1. 添加节点信息到 scale-out.yaml 文件

编写 scale-out.yaml 文件：

{{< copyable "" >}}

```ini
cdc_servers:
  - host: 10.0.1.3
  - host: 10.0.1.4
```

### 2. 运行扩容命令

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-out <cluster-name> scale-out.yaml
```

> **注意：**
>
> 此处假设当前执行命令的用户和新增的机器打通了互信，如果不满足已打通互信的条件，需要通过 `-p` 来输入新机器的密码，或通过 `-i` 指定私钥文件。

### 3. 查看集群状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

打开浏览器访问监控平台 <http://10.0.1.5:3000>，监控整个集群和新增节点的状态。

扩容后，集群拓扑结构如下所示：

| 主机 IP   | 服务   | 
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash + **TiCDC**  |
| 10.0.1.4   | TiDB + PD + TiFlash + **TiCDC**  | 
| 10.0.1.5   | TiDB+ TiKV + Monitor   | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 

## 缩容 TiDB/PD/TiKV 节点

如果要移除 IP 地址为 10.0.1.5 的一个 TiKV 节点，可以按照如下步骤进行操作。

> **注意：**
>
> 移除 TiDB、PD 节点和移除 TiKV 节点的步骤类似。

> **注意：**
>
> TiKV 中的 PD Client 会缓存 PD 节点列表，但目前不会定期自动更新，只有在 PD leader 发生切换或 TiKV 重启加载最新配置后才会更新；为避免 TiKV 缓存的 PD 节点列表过旧的风险，在扩缩容 PD 完成后，PD 集群中应至少包含两个扩缩容操作前就已经存在的 PD 节点成员，如果不满足该条件需要手动执行 PD transfer leader 操作，更新 TiKV 中的 PD 缓存列表。

### 1. 查看节点 ID 信息

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

```
Starting /root/.tiup/components/cluster/v0.4.6/cluster display <cluster-name> 

TiDB Cluster: <cluster-name>

TiDB Version: v4.0.13

ID              Role         Host        Ports                            Status  Data Dir                Deploy Dir

--              ----         ----        -----                            ------  --------                ----------

10.0.1.3:8300   cdc         10.0.1.3     8300                                Up      -                       deploy/cdc-8300
10.0.1.4:8300   cdc         10.0.1.4     8300                                Up      -                       deploy/cdc-8300
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

### 2. 执行缩容操作

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.5:20160
```

其中 `--node` 参数为需要下线节点的 ID。

预期输出 Scaled cluster `<cluster-name>` in successfully 信息，表示缩容操作成功。

### 3. 检查集群状态

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
| 10.0.1.3   | TiDB + TiFlash + TiCDC  |
| 10.0.1.4   | TiDB + PD + TiFlash + TiCDC | 
| 10.0.1.5   | TiDB + Monitor**（TiKV 已删除）**   | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 

## 缩容 TiFlash 节点

如果要缩容 IP 地址为 10.0.1.4 的一个 TiFlash 节点，可以按照如下步骤进行操作。

### 1. 根据 TiFlash 剩余节点数调整数据表的副本数

在下线节点之前，确保 TiFlash 集群剩余节点数大于等于所有数据表的最大副本数，否则需要修改相关表的 TiFlash 副本数。

1. 在 TiDB 客户端中针对所有副本数大于集群剩余 TiFlash 节点数的表执行：

    {{< copyable "sql" >}}

    ```sql
    alter table <db-name>.<table-name> set tiflash replica 0;
    ```

2. 等待相关表的 TiFlash 副本被删除（按照[查看表同步进度](/tiflash/use-tiflash.md#查看表同步进度)一节操作，查不到相关表的同步信息时即为副本被删除）。

### 2. 执行缩容操作

接下来，请任选下列方案其一进行缩容。

#### 方案一：通过 TiUP 缩容 TiFlash 节点

1. 通过以下命令确定需要下线的节点名称：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

2. 执行 scale-in 命令来下线节点，假设步骤 1 中获得该节点名为 `10.0.1.4:9000`

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:9000
    ```

#### 方案二：手动缩容 TiFlash 节点

在特殊情况下（比如需要强制下线节点），或者 TiUP 操作失败的情况下，可以使用以下方法手动下线 TiFlash 节点。

1. 使用 pd-ctl 的 store 命令在 PD 中查看该 TiFlash 节点对应的 store id。

    * 在 [pd-ctl](/pd-control.md) (tidb-ansible 目录下的 `resources/bin` 包含对应的二进制文件) 中输入 store 命令。

    * 若使用 TiUP 部署，可以调用以下命令代替 `pd-ctl`：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> store
        ```

        > **注意：**
        >
        > 如果集群中有多个 PD 实例，只需在以上命令中指定一个活跃 PD 实例的 IP:端口即可。

2. 在 pd-ctl 中下线该 TiFlash 节点。

    * 在 pd-ctl 中输入 `store delete <store_id>`，其中 `<store_id>` 为上一步查到的该 TiFlash 节点对应的 store id。

    * 若通过 TiUP 部署，可以调用以下命令代替 `pd-ctl`：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> store delete <store_id>
        ```

        > **注意：**
        >
        > 如果集群中有多个 PD 实例，只需在以上命令中指定一个活跃 PD 实例的 IP:端口即可。

3. 等待该 TiFlash 节点对应的 store 消失或者 state_name 变成 Tombstone 再关闭 TiFlash 进程。

    如果等待较长时间后，该节点仍然无法正常消失或者状态变成 Tombstone，可以考虑以下命令，把节点强制踢出集群：

    **注意以下命令会直接丢弃该 TiFlash 节点上的副本，有可能导致查询失败**

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST 'http://<pd-address>/pd/api/v1/store/<store_id>/state?state=Tombstone'
    ```

4. 手动删除 TiFlash 的数据文件，具体位置可查看在集群拓扑配置文件中 TiFlash 配置部分下的 data_dir 目录。

5. 手动更新 TiUP 的集群配置文件，在编辑模式中手动删除我们已经下线的 TiFlash 节点信息：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

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

### 3. 查看集群状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

打开浏览器访问监控平台 <http://10.0.1.5:3000>，监控整个集群的状态。

调整后，拓扑结构如下：

| Host IP   | Service   | 
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash + TiCDC  |
| 10.0.1.4   | TiDB + PD + TiCDC **（TiFlash 已删除）**  | 
| 10.0.1.5   | TiDB + Monitor  | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 

## 缩容 TiCDC 节点

如果要缩容 IP 地址为 10.0.1.4 的一个 TiCDC 节点，可以按照如下步骤进行操作。

### 1. 下线该 TiCDC 节点

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
```

### 2. 查看集群状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

打开浏览器访问监控平台 <http://10.0.1.5:3000>，监控整个集群的状态。

调整后，拓扑结构如下：

| Host IP   | Service   | 
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash + TiCDC  |
| 10.0.1.4   | TiDB + PD + **(TiCDC 已删除）**  | 
| 10.0.1.5   | TiDB + Monitor  | 
| 10.0.1.1   | TiKV    | 
| 10.0.1.2   | TiKV    | 
