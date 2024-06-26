---
title: 使用 TiUP 扩容缩容集群中的 PD 微服务节点
summary: 介绍如何使用 TiUP 扩容缩容集群中的 PD 微服务节点。
---

# 使用 TiUP 扩容缩容集群中的 PD 微服务节点

本文介绍如何使用 TiUP 扩容缩容集群中的 PD 微服务节点，包括 TSO 节点和 Scheduling 节点。

你可以通过 `tiup cluster list` 查看当前的集群名称列表。

例如，集群原拓扑结构如下所示：

| 主机 IP   | 服务   |
|:----|:----|
| 10.0.1.4   | TiDB + PD   |
| 10.0.1.5   | TiKV + Monitor   |
| 10.0.1.1   | TiKV   |
| 10.0.1.2   | TiKV   |
| 10.0.1.6   | TSO   |
| 10.0.1.7   | Scheduling   |

## 扩容 TSO/Scheduling 节点

如果要添加一个 IP 地址为 10.0.1.8 的 TSO 节点和一个 IP 地址为 10.0.1.9 的 Scheduling 节点，可以按照如下步骤进行操作。

### 1. 编写扩容拓扑配置

> **注意：**
>
> - 默认情况下，可以不填写端口以及目录信息。但在单机多实例场景下，则需要分配不同的端口以及目录，如果有端口或目录冲突，会在部署或扩容时提醒。
>
> - 从 TiUP v1.0.0 开始，扩容配置会继承原集群配置的 global 部分。

在 scale-out.yml 文件添加扩容拓扑配置：

```shell
vi scale-out.yml
```

TSO 配置参考：

```ini
tso_servers:
  - host: 10.0.1.8
    port: 3379
```

Scheduling 配置参考：

```ini
scheduling_servers:
  - host: 10.0.1.9
    port: 3379
```

可以使用 `tiup cluster edit-config <cluster-name>` 查看当前集群的配置信息，因为其中的 `global` 和 `server_configs` 参数配置默认会被 `scale-out.yml` 继承，因此也会在 `scale-out.yml` 中生效。

### 2. 执行扩容命令

执行 scale-out 命令前，先使用 `check` 及 `check --apply` 命令，检查和自动修复集群存在的潜在风险：

1. 检查集群存在的潜在风险：

    ```shell
    tiup cluster check <cluster-name> scale-out.yml --cluster --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2. 自动修复集群存在的潜在风险：

    ```shell
    tiup cluster check <cluster-name> scale-out.yml --cluster --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

3. 执行 `scale-out` 命令扩容 TiDB 集群：

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

以上操作示例中：

- 扩容配置文件为 `scale-out.yml`。
- `--user root` 表示通过 root 用户登录到目标主机完成集群部署，该用户需要有 ssh 到目标机器的权限，并且在目标机器有 sudo 权限。也可以用其他有 ssh 和 sudo 权限的用户完成部署。
- [-i] 及 [-p] 为可选项，如果已经配置免密登录目标机，则无需填写。否则选择其一即可，[-i] 为可登录到目标机的 root 用户（或 --user 指定的其他用户）的私钥，也可使用 [-p] 交互式输入该用户的密码。

预期日志结尾输出 ```Scaled cluster `<cluster-name>` out successfully``` 信息，表示扩容操作成功。

### 3. 查看集群状态

```shell
tiup cluster display <cluster-name>
```

打开浏览器访问监控平台 <http://10.0.1.5:3000>，监控整个集群和新增节点的状态。

扩容后，集群拓扑结构如下所示：

| 主机 IP   | 服务   |
|:----|:----|
| 10.0.1.4   | TiDB + PD   |
| 10.0.1.5   | TiKV + Monitor   |
| 10.0.1.1   | TiKV   |
| 10.0.1.2   | TiKV   |
| 10.0.1.6   | TSO   |
| 10.0.1.7   | Scheduling   |
| 10.0.1.8   | TSO   |
| 10.0.1.9   | Scheduling   |

## 缩容 TSO/Scheduling 节点

如果要移除一个 IP 地址为 10.0.1.8 的 TSO 节点和一个 IP 地址为 10.0.1.9 的 Scheduling 节点，可以按照如下步骤进行操作。

### 1. 查看节点 ID 信息

```shell
tiup cluster display <cluster-name>
```

```
Starting /root/.tiup/components/cluster/v1.16/cluster display <cluster-name>

TiDB Cluster: <cluster-name>

TiDB Version: v8.2.0

ID       Role         Host    Ports                            Status  Data Dir        Deploy Dir

--       ----         ----      -----                            ------  --------        ----------

10.0.1.4:2379  pd           10.0.1.4    2379/2380                        Healthy data/pd-2379      deploy/pd-2379

10.0.1.1:20160 tikv         10.0.1.1    20160/20180                      Up      data/tikv-20160     deploy/tikv-20160

10.0.1.2:20160 tikv         10.0.1.2    20160/20180                      Up      data/tikv-20160     deploy/tikv-20160

10.0.1.5:20160 tikv        10.0.1.5    20160/20180                     Up      data/tikv-20160     deploy/tikv-20160

10.0.1.4:4000  tidb        10.0.1.4    4000/10080                      Up      -                 deploy/tidb-4000

10.0.1.5:9090  prometheus   10.0.1.5    9090                             Up      data/prometheus-9090  deploy/prometheus-9090

10.0.1.5:3000  grafana      10.0.1.5    3000                             Up      -            deploy/grafana-3000

10.0.1.5:9093  alertmanager 10.0.1.5    9093/9094                        Up      data/alertmanager-9093 deploy/alertmanager-9093

10.0.1.6:3379  tso          10.0.1.6    3379                            Up|P     data/tso-3379     deploy/tso-3379

10.0.1.8:3379  tso          10.0.1.8    3379                            Up       data/tso-3379    deploy/tso-3379

10.0.1.7:3379  scheduling   10.0.1.7    3379                            Up|P     data/scheduling-3379     deploy/scheduling-3379

10.0.1.9:3379  scheduling   10.0.1.9    3379                            Up       data/scheduling-3379     deploy/scheduling-3379
```

### 2. 执行缩容操作

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.8:3379
tiup cluster scale-in <cluster-name> --node 10.0.1.9:3379
```

其中 `--node` 参数为需要下线节点的 ID。

预期输出 Scaled cluster `<cluster-name>` in successfully 信息，表示缩容操作成功。

### 3. 查看集群状态

执行如下命令检查节点是否下线成功：

```shell
tiup cluster display <cluster-name>
```

打开浏览器访问监控平台 <http://10.0.1.5:3000>，监控整个集群的状态。

调整后，拓扑结构如下：

| 主机 IP   | 服务   |
|:----|:----|
| 10.0.1.4   | TiDB + PD   |
| 10.0.1.5   | TiKV + Monitor   |
| 10.0.1.1   | TiKV   |
| 10.0.1.2   | TiKV   |
| 10.0.1.6   | TSO   |
| 10.0.1.7   | Scheduling   |

## 微服务切换

> **注意：**
>
> - 微服务的切换过程会伴随有短暂的服务不可用。

### 1. 从非微服务模式切换为微服务模式

1. 编写扩容配置：

    ```shell
    vi scale-out.yml
    ```

    配置参考：
    ```ini
    tso_servers:
      - host: 10.0.1.8
        port: 3379
    scheduling_servers:
      - host: 10.0.1.9
        port: 3379
    ```

2. 切换 PD 模式：

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

    添加 `pd_mode` 字段：
    ```ini
    global:
    user: tidb
    ssh_port: 22
    listen_host: 0.0.0.0
    deploy_dir: /tidb-deploy
    data_dir: /tidb-data
    os: linux
    arch: amd64
    systemd_mode: system
    pd_mode: ms
    ```

3. 滚动更新 PD：

    ```
    tiup cluster reload <cluster-name> -R pd
    ```

4. 扩容微服务节点：

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

### 2. 从微服务模式切换为非微服务模式

1. 切换 PD 模式：

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

    删除 `pd_mode` 字段：
    ```ini
    global:
    user: tidb
    ssh_port: 22
    listen_host: 0.0.0.0
    deploy_dir: /tidb-deploy
    data_dir: /tidb-data
    os: linux
    arch: amd64
    systemd_mode: system
    ```

2. 缩容微服务节点：

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.8:3379,10.0.1.9:3379
    ```

3. 滚动更新 PD：

    ```
    tiup cluster reload <cluster-name> -R pd
    ```
