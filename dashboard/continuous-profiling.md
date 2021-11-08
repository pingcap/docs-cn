---
title: TiDB Dashboard 实例性能持续分析页面
summary: TiDB Dashboard 持续性能分析功能，continuous profiling
aliases: ['/docs-cn/dev/dashboard/dashboard-profiling/']
---

# TiDB Dashboard 实例性能分析 - 持续分析页面

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。

持续性能分析是一种从系统调用层面解读资源开销的方法。引入该方法后，TiDB 可提供数据库源码级性能观测，通过火焰图的形式帮助研发、运维人员定位性能问题的根因。
该功能以低于 0.5% 的性能损耗，对数据库内部运行状态持续打快照（类似 CT 扫描），让原本“黑盒”的数据库变成“白盒”，具备更高的可观测性。该功能一键开启后自动运行，存储结果提供了保留时长的设定，过期的结果将会被回收，确保存储空间的有效利用。

## 分析内容

持续性能分析功能允许用户对各个 TiDB、TiKV、PD、TiFlash 实例在不重启的情况下，持续进行内部性能数据收集，并且持久化在监控节点。收集到的性能数据可显示为有向无环图，直观展现实例在性能收集的时间段内执行的各种内部操作及比例，快速了解该实例 CPU 资源消耗的主要内容。目前支持的性能信息内容：
TiDB/PD: CPU profile、Heap、Mutex、Goroutine（debug=2）
TiKV/TiFlash: CPU Profile

> **注意：**
>
> 在 TiDB v5.3 版本，持续性能分析功能可在 x86 架构下完整使用，可作为实验特性开启；而在 ARM 框架下还未完全兼容，不建议开启。

## 启用持续性能分析

持续性能分析功能在 TiDB v5.3.0 引入，在实验特性阶段，需要经由 2 阶段操作启用该功能。

### 由 TiUP 部署/升级的集群

#### 启动前检查

> **注意：**
>
> - 使用持续性能分析功能需 TiDB v5.3.0 及以上版本的集群，可前往 TiDB Dashboard [集群信息页面](/daily-check#实时面板)，查看当前版本信息。
> - 若不是 TiDB v5.3.0 及以上版本集群，请先升级 TiDB 版本到 v5.3.0 及以上。

在启动前，需要先检查 TiUP Cluster 版本，若版本低于 v1.7.0 则需要先升级 TiUP Cluster，再对 Prometheus 节点进行 reload 操作。

1. 检查 TiUP 版本：

        {{< copyable "shell-regular" >}}
        
        ```shell-regular
        tiup cluster --version
        ```

    上述命令可查看 TiUP 的具体版本。显示为：

        ```
        tiup version 1.7.0 tiup
        Go Version: go1.17.2
        Git Ref: v1.7.0
        ```
        
    若低于 v1.7.0，需要先升级 TiUP Cluster。若已经是 v1.7.0 及以上版本，可直接重启 Prometheus 节点。

2. 升级 TiUP 和 TiUP Cluster 版本至最新。
    
    - 升级 TiUP：

        {{< copyable "shell-regular" >}}

        ```shell-regular
        tiup update --self
        ```
        
    - 升级 TiUP Cluster：

        {{< copyable "shell-regular" >}}

        ```shell-regular
        tiup update cluster
        ```

升级后，完成启动前检查。

#### 启动功能流程

1. 在中控机上，通过 TiUP 添加 ng_port 配置项，并对 Prometheus 节点进行 reload 操作。

    - 使用集群中控机，使用 TiUP 工具，以编辑模式打开该集群的配置文件：

        {{< copyable "shell-regular" >}}

        ```shell-regular
        tiup cluster edit-config ${cluster-name}
        ```
        
    - 设置参数，在 [monitoring_servers](/tiup/tiup-cluster-topology-reference.md#monitoring_servers) 下面增加 “ng_port:${port}”：

        ```
        monitoring_servers:
        - host: 172.16.6.6
          ng_port: ${port}
        ```

    - 重启 Prometheus 节点：

        {{< copyable "shell-regular" >}}

        ```shell-regular
        tiup cluster reload ${cluster-name} --role prometheus
        ```

    重启后，完成中控机所需的操作。

2. 在 TiDB Dashboard 的"**高级调试**" → "**实例性能分析**" → "**持续分析**"页面，点击**设置**，进入设置弹窗，打开**启用功能**开关，点击**保存** (Save) 按钮，即可开启功能：

![界面]()

可以修改保留时间。分析结果会持久化到磁盘中，超过保留时间会被回收。该配置对所有结果生效，包括历史结果。

### 由 TiDB Operator 或二进制部署/升级的集群
暂时还不支持 TiDB Operator 或二进制部署/升级的集群。

## 访问页面

该功能默认关闭，需要手动打开启用。

可以通过以下两种方法访问实例性能分析页面：

- 登录后，左侧导航条点击 "**高级调试**" → "**实例性能分析**" → "**持续分析**"：

  ![访问]()

- 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/continuous_profiling>（将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）。


## 查看性能分析历史结果

开始持续性能分析后，可以在列表中看到已经完成的性能分析结果：

![界面]()

性能分析会在后台运行，刷新或退出当前页面不会终止已经运行的性能分析任务。

## 下载性能分析结果

进入某次分析结果后，可点击右上角下载按钮 (Download Profiling Result) 打包下载所有性能分析结果：

![界面]()

也可以点击列表中的单个实例，直接查看其性能分析结果：

![界面]()


## 停用持续性能分析

在 TiDB Dashboard 的"**高级调试**" → "**实例性能分析**" → "**持续分析**"页面，点击**设置**，进入设置弹窗，关闭**启用功能**开关，点击**保存** (Save) 按钮，即可停用该功能。
