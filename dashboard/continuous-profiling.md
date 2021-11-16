---
title: TiDB Dashboard 实例性能持续分析页面
summary: TiDB Dashboard 持续性能分析功能 (Continuous Profiling)
---

# TiDB Dashboard 实例性能分析 - 持续分析页面

> **警告：**
>
> 持续性能分析目前为实验特性，不建议在生产环境中使用。

持续性能分析是 TiDB v5.3.0 引入的一种从系统调用层面解读资源开销的方法。引入该方法后，TiDB 可提供数据库源码级性能观测，通过火焰图的形式帮助研发、运维人员定位性能问题的根因。

该功能以低于 0.5% 的性能损耗，对数据库内部运行状态持续打快照（类似 CT 扫描），让原本“黑盒”的数据库变成“白盒”，具备更高的可观测性。该功能一键开启后自动运行，存储结果提供了保留时长的设定，过期的结果将会被回收，确保存储空间的有效利用。

## 使用限制

使用持续性能分析时，应留意如下使用限制：

- 该功能可在 x86 架构下支持 TiDB、TiKV、PD ，暂不支持 TiFlash；而在 ARM 框架下还未完全兼容，不可开启。

- 该功能暂时只用于使用 TiUP 部署和升级的集群，不支持 TiDB Operator 或二进制包部署和升级的集群。

## 分析内容

持续性能分析允许用户在不重启的情况下持续收集 TiDB、TiKV、PD 各个实例的性能数据，并且持久监控节点。收集到的性能数据可显示为有向无环图，直观展现实例在性能收集的时间段内执行的各种内部操作及其比例，方便用户快速了解该实例 CPU 资源消耗细节。目前支持的性能信息：

- TiDB/PD: CPU profile、Heap、Mutex、Goroutine（debug=2）
- TiKV: CPU Profile

## 启用持续性能分析

启用持续性能分析，需要首先检查 TiUP 版本信息，然后配置中控机和 TiDB Dashboard 相关参数。

### 检查版本

检查 TiUP Cluster 版本，若版本低于 1.7.0，则需要先升级 TiUP Cluster。

1. 检查 TiUP 版本：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster --version
    ```

    上述命令可查看 TiUP 的具体版本。显示为：

    ```
    tiup version 1.7.0 tiup
    Go Version: go1.17.2
    Git Ref: v1.7.0
    ```

    若低于 v1.7.0，需要先升级 TiUP Cluster。

2. 升级 TiUP 和 TiUP Cluster 版本至最新。

    - 升级 TiUP：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup update --self
        ```

    - 升级 TiUP Cluster：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup update cluster
        ```

升级后，完成启动前检查。

### 配置中控机和 TiDB Dashboard

1. 在中控机上，通过 TiUP 添加 ng_port 配置项，并对 Prometheus 节点进行 reload 操作。

    1. 使用集群中控机，使用 TiUP 工具，以编辑模式打开该集群的配置文件：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster edit-config ${cluster-name}
        ```

    2. 设置参数，在 [monitoring_servers](/tiup/tiup-cluster-topology-reference.md#monitoring_servers) 下面增加 “ng_port:${port}”：

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

    重启后，完成中控机所需的操作。

2. 启用持续性能分析。

    1. 进入 TiDB Dashboard，选择**高级调试** (Advanced Debugging) > **实例性能分析** (Profile Instances) > **持续分析** (Continuous Profile)。
    2. 点击**打开设置** (Open Settings)。在右侧**设置** (Settings) 页面，将**启用特性** (Enable Feature) 下方的开关打开。设置**保留时间** (Retention Period) 或保留默认值。
    3. 点击**保存** (Save)。

    ![启用功能](/media/dashboard/dashboard-conprof-start.png)

## 访问页面

启用持续性能分析功能后，你可以通过以下任一方式访问实例性能分析页面：

- 登录后，左侧导航条点击**高级调试** (Advanced Debugging) > **实例性能分析** (Profile Instances) > **持续分析** (Continuous Profile)：

  ![访问页面](/media/dashboard/dashboard-conprof-access.png)

- 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/continuous_profiling>（将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）。

## 查看性能分析历史结果

开始持续性能分析后，可以在列表中看到已经完成的性能分析结果：

![历史结果](/media/dashboard/dashboard-conprof-history.png)

性能分析会在后台运行，刷新或退出当前页面不会终止已经运行的性能分析任务。

## 下载性能分析结果

进入某次分析结果后，可点击右上角下载按钮 (Download Profiling Result) 打包下载所有性能分析结果：

![下载某次分析结果](/media/dashboard/dashboard-conprof-download.png)

也可以点击列表中的单个实例，直接查看其性能分析结果：

![查看单个实例分析结果](/media/dashboard/dashboard-conprof-single.png)

## 停用持续性能分析

1. 进入 TiDB Dashboard，选择**高级调试** (Advanced Debugging) > **实例性能分析** (Profile Instances) > **持续分析** (Continuous Profile)。
2. 点击**设置** (Settings)，将**启用特性** (Enable Feature) 下方的开关关闭。
3. 在弹出的**停用持续分析** (Disable Continuous Profiling Feature) 对话框中，选择**停用** (Disable)。
4. 点击**保存** (Save)。

![停用功能](/media/dashboard/dashboard-conprof-stop.png)
