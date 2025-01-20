---
title: TiDB 数据库快速上手指南
summary: 了解如何快速上手使用 TiDB 数据库。
---

# TiDB 数据库快速上手指南

本指南介绍如何快速上手体验 TiDB 数据库。对于非生产环境，你可以选择以下任意一种方式部署 TiDB 数据库：

- [部署本地测试集群](#部署本地测试集群)（支持 macOS 和 Linux）
- [在单机上模拟部署生产环境集群](#在单机上模拟部署生产环境集群)（支持 Linux）

> **注意：**
>
> 本指南中的 TiDB 部署方式仅适用于快速上手体验，不适用于生产环境。
>
> - 如需在生产环境部署 TiDB，请参考[在生产环境中部署 TiDB 指南](/production-deployment-using-tiup.md)。
> - 如需在 Kubernetes 上部署 TiDB，请参考[快速上手 TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/get-started)。
> - 如需在云上管理 TiDB，请参考 [TiDB Cloud 快速上手指南](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart)。

要快速了解 TiUP 的基本功能、使用 TiUP 快速搭建 TiDB 集群的方法与连接 TiDB 集群并执行 SQL 的方法，建议先观看下面的培训视频（时长 15 分钟）。注意本视频只作为学习参考，如需了解 [TiUP](/tiup/tiup-overview.md) 的具体使用方法和 [TiDB 快速上手具体操作步骤](#部署本地测试集群)，请以文档内容为准。

<video src="https://download.pingcap.com/docs-cn%2FLesson07_quick_start.mp4" width="100%" height="100%" controls="controls" poster="https://download.pingcap.com/docs-cn/poster_lesson7.png"></video>

## 部署本地测试集群

本节介绍如何利用本地 macOS 或者单机 Linux 环境快速部署 TiDB 测试集群。通过部署 TiDB 集群，你可以了解 TiDB 的基本架构，以及 TiDB、TiKV、PD、监控等基础组件的运行。

<SimpleTab>
<div label="macOS">

TiDB 是一个分布式系统。最基础的 TiDB 测试集群通常由 2 个 TiDB 实例、3 个 TiKV 实例、3 个 PD 实例和可选的 TiFlash 实例构成。通过 TiUP Playground，可以快速搭建出上述的一套基础测试集群，步骤如下：

1. 下载并安装 TiUP。

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    安装完成后会提示如下信息：

    ```log
    Successfully set mirror to https://tiup-mirrors.pingcap.com
    Detected shell: zsh
    Shell profile:  /Users/user/.zshrc
    /Users/user/.zshrc has been modified to add tiup to PATH
    open a new terminal or source /Users/user/.zshrc to use it
    Installed path: /Users/user/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

    请注意上述输出中的 Shell profile 文件路径，下一步中需要使用该路径。

    > **注意：**
    >
    > v5.2.0 及以上版本的 TiDB 支持在 Apple silicon 芯片的机器上运行 `tiup playground`。

2. 声明全局环境变量。

    > **注意：**
    >
    > TiUP 安装完成后会提示 Shell profile 文件的绝对路径。在执行以下 `source` 命令前，需要将 `${your_shell_profile}` 修改为 Shell profile 文件的实际位置。

    {{< copyable "shell-regular" >}}

    ```shell
    source ${your_shell_profile}
    ```

3. 在当前 session 执行以下命令启动集群。

    > **注意：**
    >
    > - 如果按以下方式执行 playground，在结束部署测试后，TiUP 会自动清理掉原集群数据，重新执行命令会得到一个全新的集群。
    > - 如果希望持久化数据，需要在启动集群时添加 TiUP 的 `--tag` 参数，详见[启动集群时指定 `tag` 以保留数据](/tiup/tiup-playground.md#启动集群时指定-tag-以保留数据)。
    >
    >     ```shell
    >     tiup playground --tag ${tag_name}
    >     ```

    - 直接执行 `tiup playground` 命令会运行最新版本的 TiDB 集群，其中 TiDB、TiKV、PD 和 TiFlash 实例各 1 个：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground
        ```

        如果这是你第一次运行该命令，TiUP 会下载最新版本的 TiDB 并启动集群。命令输出中将显示集群的端点列表：

        ```log
        🎉 TiDB Playground Cluster is started, enjoy!

        Connect TiDB:    mysql --comments --host 127.0.0.1 --port 4000 -u root
        TiDB Dashboard:  http://127.0.0.1:2379/dashboard
        Grafana:         http://127.0.0.1:3000
        ```

    - 也可以指定 TiDB 版本以及各组件实例个数，命令类似于：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground v8.5.1 --db 2 --pd 3 --kv 3
        ```

<<<<<<< HEAD
        上述命令会在本地下载并启动某个版本的集群（例如 v8.5.1）。最新版本可以通过执行 `tiup list tidb` 来查看。运行结果将显示集群的访问方式：
=======
        如果要查看当前支持部署的所有 TiDB 版本，执行 `tiup list tidb`。
>>>>>>> 1473bf4d99 (Update TiDB quick start (#19570))

4. 新开启一个 session 以访问 TiDB 数据库和集群端点。

    + 连接 TiDB 数据库：

        - 使用 TiUP `client` 连接 TiDB：

            ```shell
            tiup client
            ```

        - 或者使用 MySQL 客户端连接 TiDB：

            ```shell
            mysql --host 127.0.0.1 --port 4000 -u root
            ```

    - 访问 Prometheus 管理界面：<http://127.0.0.1:9090>。

    - 访问 [TiDB Dashboard](/dashboard/dashboard-intro.md) 页面：<http://127.0.0.1:2379/dashboard>，默认用户名为 `root`，密码为空。

    - 访问 Grafana 界面：<http://127.0.0.1:3000>，默认用户名和密码都为 `admin`。

5. （可选）[将数据加载到 TiFlash](/tiflash/tiflash-overview.md#使用-tiflash) 进行分析。

6. 测试完成之后，可以通过执行以下步骤来清理集群：

    1. 按下 <kbd>Control</kbd>+<kbd>C</kbd> 键停掉上述启用的 TiDB 服务。

    2. 等待服务退出操作完成后，执行以下命令：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup clean --all
        ```

> **注意：**
>
> TiUP Playground 默认监听 `127.0.0.1`，服务仅本地可访问；若需要使服务可被外部访问，可使用 `--host` 参数指定监听网卡绑定外部可访问的 IP。

</div>
<div label="Linux">

TiDB 是一个分布式系统。最基础的 TiDB 测试集群通常由 2 个 TiDB 实例、3 个 TiKV 实例、3 个 PD 实例和可选的 TiFlash 实例构成。通过 TiUP Playground，可以快速搭建出上述的一套基础测试集群，步骤如下：

1. 下载并安装 TiUP。

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    安装完成后会提示如下信息：

    ```log
    Successfully set mirror to https://tiup-mirrors.pingcap.com
    Detected shell: bash
    Shell profile:  /home/user/.bashrc
    /home/user/.bashrc has been modified to add tiup to PATH
    open a new terminal or source /home/user/.bashrc to use it
    Installed path: /home/user/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

    请注意上述输出中的 Shell profile 文件路径，下一步中需要使用该路径。

2. 声明全局环境变量。

    > **注意：**
    >
    > TiUP 安装完成后会提示 Shell profile 文件的绝对路径。在执行以下 `source` 命令前，需要将 `${your_shell_profile}` 修改为 Shell profile 文件的实际位置。

    {{< copyable "shell-regular" >}}

    ```shell
    source ${your_shell_profile}
    ```

3. 在当前 session 执行以下命令启动集群。

    > **注意：**
    >
    > - 如果按以下方式执行 playground，在结束部署测试后，TiUP 会自动清理掉原集群数据，重新执行命令会得到一个全新的集群。
    > - 如果希望持久化数据，需要在启动集群时添加 TiUP 的 `--tag` 参数，详见[启动集群时指定 `tag` 以保留数据](/tiup/tiup-playground.md#启动集群时指定-tag-以保留数据)。
    >
    >     ```shell
    >     tiup playground --tag ${tag_name}
    >     ```

    - 直接运行 `tiup playground` 命令会运行最新版本的 TiDB 集群，其中 TiDB、TiKV、PD 和 TiFlash 实例各 1 个：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground
        ```

        如果这是你第一次运行该命令，TiUP 会下载最新版本的 TiDB 并启动集群。命令输出中将显示集群的端点列表：

        ```log
        🎉 TiDB Playground Cluster is started, enjoy!

        Connect TiDB:    mysql --comments --host 127.0.0.1 --port 4000 -u root
        TiDB Dashboard:  http://127.0.0.1:2379/dashboard
        Grafana:         http://127.0.0.1:3000
        ```

    - 或者指定 TiDB 版本以及各组件实例个数，命令类似于：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground v8.5.1 --db 2 --pd 3 --kv 3
        ```

<<<<<<< HEAD
        上述命令会在本地下载并启动某个版本的集群（例如 v8.5.1）。最新版本可以通过执行 `tiup list tidb` 来查看。运行结果将显示集群的访问方式：
=======
        如果要查看当前支持部署的所有 TiDB 版本，执行 `tiup list tidb`。
>>>>>>> 1473bf4d99 (Update TiDB quick start (#19570))

4. 新开启一个 session 以访问 TiDB 数据库和集群端点。

    + 连接 TiDB 数据库：

        - 使用 TiUP `client` 连接 TiDB：

            ```shell
            tiup client
            ```

        - 或者使用 MySQL 客户端连接 TiDB：

            ```shell
            mysql --host 127.0.0.1 --port 4000 -u root
            ```

    - 访问 Prometheus 管理界面：<http://127.0.0.1:9090>。

    - 访问 [TiDB Dashboard](/dashboard/dashboard-intro.md) 页面：<http://127.0.0.1:2379/dashboard>，默认用户名为 `root`，密码为空。

    - 访问 Grafana 界面：<http://127.0.0.1:3000>，默认用户名和密码都为 `admin`。

5. （可选）[将数据加载到 TiFlash](/tiflash/tiflash-overview.md#使用-tiflash) 进行分析。

6. 测试完成之后，可以通过执行以下步骤来清理集群：

    1. 按下 <kbd>Control</kbd>+<kbd>C</kbd> 键停掉上述启用的 TiDB 服务。

    2. 等待服务退出操作完成后，执行以下命令：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup clean --all
        ```

> **注意：**
>
> TiUP Playground 默认监听 `127.0.0.1`，服务仅本地可访问。若需要使服务可被外部访问，可使用 `--host` 参数指定监听网卡绑定外部可访问的 IP。

</div>
</SimpleTab>

## 在单机上模拟部署生产环境集群

本节介绍如何在单台 Linux 服务器上体验 TiDB 最小的完整拓扑的集群，并模拟生产环境下的部署步骤。

下文将参照 TiUP 最小拓扑的一个 YAML 文件部署 TiDB 集群。

### 准备环境

开始部署 TiDB 集群前，准备一台部署主机，确保其软件满足需求：

- 推荐安装 CentOS 7.3 及以上版本
- 运行环境可以支持互联网访问，用于下载 TiDB 及相关软件安装包

最小规模的 TiDB 集群拓扑包含以下实例：

| 实例 | 个数 | IP | 配置 |
|:-- | :-- | :-- | :-- |
| TiKV | 3 | 10.0.1.1 | 使用递增的端口号以避免冲突 |
| TiDB | 1 | 10.0.1.1 | 使用默认端口和其他配置 |
| PD | 1 | 10.0.1.1 | 使用默认端口和其他配置 |
| TiFlash | 1 | 10.0.1.1 | 使用默认端口和其他配置 |
| Monitor | 1 | 10.0.1.1 | 使用默认端口和其他配置 |

> **注意：**
>
> 该表中拓扑实例的 IP 为示例 IP。在实际部署时，请替换为实际的 IP。

部署主机软件和环境要求如下：

- 部署需要使用部署主机的 root 用户及密码
- 部署主机[关闭防火墙](/check-before-deployment.md#检测及关闭目标部署机器的防火墙)或者开放 TiDB 集群的节点间所需端口
- 目前 TiUP Cluster 支持在 x86_64（AMD64）和 ARM 架构上部署 TiDB 集群
    - 在 AMD64 架构下，建议使用 CentOS 7.3 及以上版本 Linux 操作系统
    - 在 ARM 架构下，建议使用 CentOS 7.6 (1810) 版本 Linux 操作系统

### 实施部署

> **注意：**
>
> 你可以使用 Linux 系统的任一普通用户或 root 用户登录主机，以下步骤以 root 用户为例。

1. 下载并安装 TiUP：

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 声明全局环境变量：

    > **注意：**
    >
    > TiUP 安装完成后会提示对应 Shell profile 文件的绝对路径。在执行以下 `source` 命令前，需要将 `${your_shell_profile}` 修改为 Shell profile 文件的实际位置。

    {{< copyable "shell-regular" >}}

    ```shell
    source ${your_shell_profile}
    ```

3. 安装 TiUP 的 cluster 组件：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

4. 如果机器已经安装 TiUP cluster，需要更新软件版本：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update --self && tiup update cluster
    ```

5. 由于模拟多机部署，需要通过 root 用户调大 sshd 服务的连接数限制：

    1. 修改 `/etc/ssh/sshd_config` 将 `MaxSessions` 调至 20。
    2. 重启 sshd 服务：

        {{< copyable "shell-root" >}}

        ```shell
        service sshd restart
        ```

6. 创建并启动集群：

    按下面的配置模板，创建并编辑[拓扑配置文件](/tiup/tiup-cluster-topology-reference.md)，命名为 `topo.yaml`。其中：

    - `user: "tidb"`：表示通过 `tidb` 系统用户（部署会自动创建）来做集群的内部管理，默认使用 22 端口通过 ssh 登录目标机器
    - `replication.enable-placement-rules`：设置这个 PD 参数来确保 TiFlash 正常运行
    - `host`：设置为本部署主机的 IP

    配置模板如下：

    {{< copyable "" >}}

    ```yaml
    # # Global variables are applied to all deployments and used as the default value of
    # # the deployments if a specific deployment value is missing.
    global:
     user: "tidb"
     ssh_port: 22
     deploy_dir: "/tidb-deploy"
     data_dir: "/tidb-data"

    # # Monitored variables are applied to all the machines.
    monitored:
     node_exporter_port: 9100
     blackbox_exporter_port: 9115

    server_configs:
     tidb:
       instance.tidb_slow_log_threshold: 300
     tikv:
       readpool.storage.use-unified-pool: false
       readpool.coprocessor.use-unified-pool: true
     pd:
       replication.enable-placement-rules: true
       replication.location-labels: ["host"]
     tiflash:
       logger.level: "info"

    pd_servers:
     - host: 10.0.1.1

    tidb_servers:
     - host: 10.0.1.1

    tikv_servers:
     - host: 10.0.1.1
       port: 20160
       status_port: 20180
       config:
         server.labels: { host: "logic-host-1" }

     - host: 10.0.1.1
       port: 20161
       status_port: 20181
       config:
         server.labels: { host: "logic-host-2" }

     - host: 10.0.1.1
       port: 20162
       status_port: 20182
       config:
         server.labels: { host: "logic-host-3" }

    tiflash_servers:
     - host: 10.0.1.1

    monitoring_servers:
     - host: 10.0.1.1

    grafana_servers:
     - host: 10.0.1.1
    ```

7. 执行集群部署命令：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster deploy <cluster-name> <version> ./topo.yaml --user root -p
    ```

    - 参数 `<cluster-name>` 表示设置集群名称
    - 参数 `<version>` 表示设置集群版本，例如 `v8.5.1`。可以通过 `tiup list tidb` 命令来查看当前支持部署的 TiDB 版本
    - 参数 `-p` 表示在连接目标机器时使用密码登录

        > **注意：**
        >
        > 如果主机通过密钥进行 SSH 认证，请使用 `-i` 参数指定密钥文件路径，`-i` 与 `-p` 不可同时使用。

    按照引导，输入”y”及 root 密码，来完成部署：

    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

8. 启动集群：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster start <cluster-name>
    ```

9. 访问集群端点：

    - 安装 MySQL 客户端。如果已安装，则跳过这一步骤。

        {{< copyable "shell-regular" >}}

        ```shell
        yum -y install mysql
        ```

    - 使用 MySQL 客户端访问 TiDB 数据库，密码为空：

        ```shell
        mysql -h 10.0.1.1 -P 4000 -u root
        ```

    - 访问 Grafana 监控页面：<http://{grafana-ip}:3000>，默认用户名和密码均为 `admin`。

    - 访问集群 [TiDB Dashboard](/dashboard/dashboard-intro.md) 监控页面：<http://{pd-ip}:2379/dashboard>，默认用户名为 `root`，密码为空。

10. （可选）查看集群列表和拓扑结构：

    - 执行以下命令确认当前已经部署的集群列表：

        ```shell
        tiup cluster list
        ```

    - 执行以下命令查看集群的拓扑结构和状态：

        ```shell
        tiup cluster display <cluster-name>
        ```

    要了解更多 `tiup cluster` 命令，请参阅 [TiUP 集群命令](/tiup/tiup-component-cluster.md)。

11. 测试完成之后，可以通过执行以下步骤来清理集群：

    1. 按下 <kbd>Control</kbd>+<kbd>C</kbd> 键停掉上述启用的 TiDB 服务。

    2. 等待服务退出操作完成后，执行以下命令：

        ```shell
        tiup clean --all
        ```

## 探索更多

如果你刚刚部署好一套 TiDB 本地测试集群，你可以继续：

- 学习 [TiDB SQL 操作](/basic-sql-operations.md)
- [迁移数据到 TiDB](/migration-overview.md)
- 使用 [TiUP](/tiup/tiup-overview.md) 管理 TiDB 集群

如果你准备好在生产环境部署 TiDB，你可以继续：

- [使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)
- [使用 TiDB Operator 在 Kubernetes 上部署 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable)

如果你是应用开发者，想要快速使用 TiDB 构建应用，可参阅以下文档：

- [开发者手册概览](/develop/dev-guide-overview.md)
- [使用 TiDB Cloud Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)
- [示例程序](/develop/dev-guide-sample-application-java-jdbc.md)

如果你想使用 TiFlash 作为数据分析的解决方案，可参阅以下文档：

- [使用 TiFlash](/tiflash/tiflash-overview.md#使用-tiflash)
- [TiFlash 简介](/tiflash/tiflash-overview.md)
