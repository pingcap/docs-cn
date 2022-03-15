---
title: TiDB Dashboard 常见问题
aliases: ['/docs-cn/dev/dashboard/dashboard-faq/']
---

# TiDB Dashboard 常见问题

本文汇总了使用 TiDB Dashboard 过程中的常见问题与解决办法。若无法找到对应问题，或者根据指引操作后问题仍然存在，请联系 PingCAP 技术支持获取帮助。

## 访问

### 已配置防火墙或反向代理，但访问后被跳转到一个内部地址无法访问 TiDB Dashboard

集群部署有多个 PD 实例的情况下，只有其中某一个 PD 实例会真正运行 TiDB Dashbaord 服务，访问其他 PD 实例时会发生浏览器端重定向。若防火墙或反向代理没有为此进行正确配置，就可能出现访问后被重定向到一个被防火墙或反向代理保护的内部地址的情况。

- 参阅 [TiDB Dashboard 多 PD 实例部署](/dashboard/dashboard-ops-deploy.md#多-pd-实例部署)章节了解多 PD 实例下 TiDB Dashboard 的工作原理。
- 参阅[通过反向代理使用 TiDB Dashboard](/dashboard/dashboard-ops-reverse-proxy.md) 章节了解如何正确配置反向代理。
- 参阅[提高 TiDB Dashboard 安全性](/dashboard/dashboard-ops-security.md)章节了解如何正确配置防火墙。

### 双网卡部署时无法通过另一个网卡访问 TiDB Dashboard

PD 中的 TiDB Dashboard 出于安全考虑仅监听部署时所指定的 IP 地址（即只监听在一个网卡上），而非 `0.0.0.0`，因此当主机上安装了多个网卡时，通过另一个网卡将无法访问。

当你使用 `tiup cluster` 或 `tiup playground` 命令部署时，目前尚没有方法改变该行为。推荐使用反向代理将 TiDB Dashboard 安全地暴露给另一个网卡，具体参见[通过反向代理使用 TiDB Dashboard](/dashboard/dashboard-ops-reverse-proxy.md) 章节。

## 界面功能

### 概况页面中 QPS 及 Latency 显示 `prometheus_not_found` 错误

QPS 及 Latency 监控依赖于集群中已正常部署 Prometheus 监控实例，没有部署的情况下就会显示为错误。向集群中新部署 Prometheus 实例即可解决该问题。

若已经部署 Prometheus 监控实例但仍然显示为错误，可能的原因是您使用的部署工具（TiUP 或 TiDB Operator）版本比较旧，没有自动汇报监控地址，导致 TiDB Dashboard 无法感知并查询监控数据。可以升级到最新的部署工具并重试。

以下给出 TiUP 部署工具的操作方法，对于其他部署工具，请参阅工具对应文档。

1. 升级 TiUP、TiUP Cluster：

   ```bash
   tiup update --self
   tiup update cluster --force
   ```

2. 升级后，部署包含监控节点的新集群时，应当能正常显示监控。

3. 升级后，对于现有集群，可通过再次启动集群的方法汇报监控地址（将 `CLUSTER_NAME` 替换为实际集群名称）：

   ```bash
   tiup cluster start CLUSTER_NAME
   ```

   即使集群已经启动，请仍然执行该命令。该命令不会影响集群上正常的业务，但会刷新并上报监控地址，从而能让监控在 TiDB Dashboard 中正常显示。

### 概况页面中 Top SQL 语句、最近慢查询显示 `invalid connection` 错误

可能的原因是你开启了 TiDB 的 `prepared-plan-cache` 功能。`prepared-plan-cache` 是实验性功能，在某些版本的 TiDB 中可能无法正常运行，开启后可能会导致 TiDB Dashboard（及其他应用）出现该问题。可以通过修改 [TiDB 配置文件](/tidb-configuration-file.md#prepared-plan-cache)来关闭 `prepared-plan-cache` 功能。

### 慢查询页面显示 `unknown field` 错误

集群升级后，如果慢查询页面出现 `unknown field` 错误，是由于升级后新版本 TiDB Dashboard 字段与浏览器缓存内的用户偏好设置的字段不兼容导致的。该问题已修复。如果你的集群版本低于 v5.0.3 或 v4.0.14，可以根据以下步骤进行处理：

1. 打开 TiDB Dashboard 页面。

2. 打开浏览器的开发者工具。各浏览器的打开方式不同。

    - Firefox：**菜单** > **Web 开发者** > **切换工具箱**（译者注：此处修改为最新的 Firefox Quantum），或者**工具栏** > **切换工具箱**。
    - Chrome：**菜单** > **更多工具** > **开发者工具**。
    - Safari：**Develop** > **Show Web Inspector**。如果你看不到 Develop 菜单，选择 **Preferences** > **Advanced**，然后点击 **Show Develop menu in menu bar** 复选框。

    以 Chrome 为例：

    ![打开开发者工具](/media/dashboard/dashboard-faq-devtools.png)

3. 选中 **Application** 面板，展开 **Local Storage** 菜单并选中 **TiDB Dashboard 页面的域名**，点击 **Clear All**。

    ![清理 Local Storage](/media/dashboard/dashboard-faq-devtools-application.png)

### 界面提示 `集群中未启动必要组件 NgMonitoring`

NgMonitoring 是 TiDB v5.4.0 及以上集群中内置的高级监控组件，用于支撑 TiDB Dashboard 的 **持续分析** (Continuous Profiling) 和 **Top SQL** 等功能。使用 TiUP 部署集群时，NgMonitoring 会自动部署；使用 TiDB Operator 部署集群时，需要依据[启用持续性能分析](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/access-dashboard/#%E5%90%AF%E7%94%A8%E6%8C%81%E7%BB%AD%E6%80%A7%E8%83%BD%E5%88%86%E6%9E%90)手动部署 NgMonitoring。

如果界面提示 `集群中未启动必要组件 NgMonitoring`，需要按 TiDB 集群部署方式排查问题。

#### 使用 TiUP 部署的集群

第 1 步：检查 TiUP Cluster 版本

  1. 检查 TiUP Cluster 版本，NgMonitoring 组件需要较高版本的部署工具支持（TiUP v1.9.0 及以上）：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster --version
        ```

        上述命令可查看 TiUP Cluster 的具体版本。例如：

        ```
        tiup version 1.9.0 tiup
        Go Version: go1.17.2
        Git Ref: v1.9.0
        ```

  2. 如果 TiUP 版本低于 v1.9.0，升级 TiUP 和 TiUP Cluster 版本至最新。

        {{< copyable "shell-regular" >}}

        ```shell
        tiup update --all
        ```

第 2 步：在中控机上，通过 TiUP 添加 ng_port 配置项，然后重启 Prometheus 节点。

  1. 以编辑模式打开集群的配置文件：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster edit-config ${cluster-name}
        ```

  2. 在 `monitoring_servers` 下面增加 `ng_port:${port}` 参数：

        ```
        monitoring_servers:
        - host: 172.16.6.6
          ng_port: ${port}
        ```

  3. 重启 Prometheus 节点：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster reload ${cluster-name} --role prometheus
        ```

执行完以上操作后，在 TiDB Dashboard 上启用持续性能分析特性。如果 NgMonitoring 依然无法加载，请联系 PingCAP 技术支持获取帮助。

#### 使用 TiDB Operator 部署的集群

参考[启用持续性能分析](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/access-dashboard/#%E5%90%AF%E7%94%A8%E6%8C%81%E7%BB%AD%E6%80%A7%E8%83%BD%E5%88%86%E6%9E%90)中的步骤部署 NgMonitoring。
