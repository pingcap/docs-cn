---
title: 部署 TiDB Dashboard
aliases: ['/docs-cn/stable/dashboard/dashboard-ops-deploy/','/docs-cn/v4.0/dashboard/dashboard-ops-deploy/']
---

# 部署 TiDB Dashboard

TiDB Dashboard 界面内置于 TiDB 4.0 或更高版本的 PD 组件中，无需额外部署。只需部署标准 TiDB 集群，TiDB Dashboard 就会原生集成。

请参阅下列文档了解如何部署标准 TiDB 集群：

- [快速试用 TiDB 集群](/quick-start-with-tidb.md)
- [生产环境部署](/production-deployment-using-tiup.md)
- [Kubernetes 环境部署](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.1/access-dashboard/)

> **注意：**
>
> TiDB Dashboard 目前不能在低于 4.0 版本的集群中部署或使用。

## 多 PD 实例部署

当集群中部署了多个 PD 实例时，其中仅有一个 PD 实例会固定地提供 TiDB Dashboard 服务。

各个 PD 首次运行时会自动协商出其中某一个实例提供 TiDB Dashboard 服务。协商完毕后，无论重启或扩容，都会固定在这个实例上运行 TiDB Dashboard 服务，除非该实例被手动缩容。其他 PD 实例不会运行 TiDB Dashboard 服务。这个协商过程无需用户介入，会自动完成。

当用户访问不提供 TiDB Dashboard 服务的 PD 实例时，浏览器将会收到重定向指令，自动引导用户重新访问提供了 TiDB Dashboard 服务的 PD 实例，从而能正常使用。流程如下图所示。

![流程示意](/media/dashboard/dashboard-ops-multiple-pd.png)

> **注意：**
>
> 提供 TiDB Dashboard 服务的 PD 实例不一定与 PD leader 一致。

### 查询实际运行 TiDB Dashboard 服务的 PD 实例

使用 TiUP 部署时，对于已启动的集群，可通过 `tiup cluster display` 命令查看哪个 PD 节点提供了 TiDB Dashboard 服务（将 `CLUSTER_NAME` 替换为集群名称）：

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

输出样例如下：

```
http://192.168.0.123:2379/dashboard/
```

> **注意：**
>
> 该功能在 TiUP Cluster v1.0.3 或更高版本部署工具中提供。
>
> <details>
> <summary>升级 TiUP Cluster 步骤</summary>
>
> ```shell
> tiup update --self
> tiup update cluster --force
> ```
>
> </details>

### 切换其他 PD 实例提供 TiDB Dashboard 服务

使用 TiUP 部署时，对于已启动的集群，可使用 `tiup ctl pd` 命令切换其他 PD 实例运行 TiDB Dashboard，或在禁用 TiDB Dashboard 的情况下重新指定一个 PD 实例运行 TiDB Dashboard：

```bash
tiup ctl pd -u http://127.0.0.1:2379 config set dashboard-address http://9.9.9.9:2379
```

其中：

- 将 `127.0.0.1:2379` 替换为任意 PD 实例的 IP 和端口
- 将 `9.9.9.9:2379` 替换为想运行 TiDB Dashboard 服务的新 PD 实例的 IP 和端口

修改完毕后，可使用 `tiup cluster display` 命令确认修改是否生效（将 `CLUSTER_NAME` 替换为集群名称）：

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

> **警告：**
>
> 切换 TiDB Dashboard 将会丢失之前 TiDB Dashboard 实例所存储的本地数据，包括流量可视化历史、历史搜索记录等。

## 禁用 TiDB Dashboard

使用 TiUP 部署时，对于已启动的集群，可使用 `tiup ctl pd` 命令在所有 PD 实例上禁用 TiDB Dashboard（将 `127.0.0.1:2379` 替换为任意 PD 实例的 IP 和端口）：

```bash
tiup ctl pd -u http://127.0.0.1:2379 config set dashboard-address none
```

禁用 TiDB Dashboard 后，查询哪个 PD 实例提供 TiDB Dashboard 服务将会失败：

```
Error: TiDB Dashboard is disabled
```

浏览器访问任意 PD 实例的 TiDB Dashboard 地址也将提示失败：

```
Dashboard is not started.
```

## 重新启用 TiDB Dashboard

使用 TiUP 部署时，对于已启动的集群，可使用 `tiup ctl pd` 命令，要求 PD 重新协商出某一个实例运行 TiDB Dashboard（将 `127.0.0.1:2379` 替换为任意 PD 实例的 IP 和端口）：

```bash
tiup ctl pd -u http://127.0.0.1:2379 config set dashboard-address auto
```

修改完毕后，使用 `tiup cluster display` 命令查看 PD 自动协商出的 TiDB Dashboard 实例地址（将 `CLUSTER_NAME` 替换为集群名称）：

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

还可以通过手动指定哪个 PD 实例运行 TiDB Dashboard 服务的方式重新启用 TiDB Dashboard，具体操作参见上文[切换其他 PD 实例提供 TiDB Dashboard 服务](#切换其他-pd-实例提供-tidb-dashboard-服务)。

> **警告：**
>
> 若新启用的 TiDB Dashboard 实例与禁用前的实例不一致，将会丢失之前 TiDB Dashboard 实例所存储的本地数据，包括流量可视化历史、历史搜索记录等。

## 下一步

- 参阅[访问 TiDB Dashboard](/dashboard/dashboard-access.md) 章节了解如何访问及登录集群上的 TiDB Dashboard 界面。
- 参阅[提高 TiDB Dashboard 安全性](/dashboard/dashboard-ops-security.md) 章节了解如何增强 TiDB Dashboard 的安全性，如配置防火墙等。
