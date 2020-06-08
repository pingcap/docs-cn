---
title: TiDB 数据库快速上手指南
category: how-to
aliases: ['/docs-cn/dev/test-deployment-using-docker/']
---

# TiDB 数据库快速上手指南

> **警告：**
>
> 对于生产环境，不要使用本文介绍的方式进行部署，而应使用 [TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。

本文介绍如何快速上手体验 TiDB 分布式数据库。有以下 3 种体验方式供用户选择。

- [第一种：使用 TiUP Playground 快速部署本地测试环境](#第一种使用-tiup-playground-快速部署本地测试环境)
- [第二种：使用 TiUP cluster 在单机上模拟生产环境部署步骤](#第二种使用-tiup-cluster-在单机上模拟生产环境部署步骤)
- [第三种：使用 TiDB-Wasm 一键体验 TiDB 数据库](#第三种使用-tidb-wasm-一键体验-tidb-数据库)

## 第一种：使用 TiUP Playground 快速部署本地测试环境

- 适用场景：利用本地 Mac 或者单机 Linux 环境快速部署 TiDB 集群。可以体验 TiDB 集群的基本架构，以及 TiDB、TiKV、PD、监控等基础组件的运行。
- 耗时：1 分钟

作为一个分布式系统，最基础的 TiDB 测试集群通常由 2 个 TiDB 实例、3 个 TiKV 实例和 3 个 PD 实例来构成。通过 TiUP Playground，可以快速搭建出上述的一套基础测试集群。

1. 下载并安装 TiUP。

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 声明全局环境变量。

    > **注意：**
    >
    > TiUP 安装完成会提示对应的 profile 文件的绝对路径，以下 source 操作需要根据实际位置进行操作。

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ``` 

3. 在当前 session 执行以下命令启动集群。

    - 直接运行 `tiup playground` 命令会运行最新版本的 TiDB 集群，其中 TiDB、TiKV 和 PD 实例各 1 个：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground
        ```

    - 也可以指定 TiDB 版本以及各组件实例个数，命令类似于：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground v4.0.0 --db 2 --pd 3 --kv 3 --monitor
        ```

        上述命令会在本地下载并启动一个 `v4.0.0` 版本的集群，`--monitor` 表示同时部署监控组件。
        最新版本可以通过执行 `tiup list tidb` 来查看。
        运行结果将显示集群的访问方式：
        
        ```log
        CLUSTER START SUCCESSFULLY, Enjoy it ^-^
        To connect TiDB: mysql --host 127.0.0.1 --port 4000 -u root
        To connect TiDB: mysql --host 127.0.0.1 --port 4001 -u root
        To view the dashboard: http://127.0.0.1:2379/dashboard
        To view the monitor: http://127.0.0.1:9090
        ```

4. 新开启一个 session 以访问 TiDB 数据库。

    {{< copyable "shell-regular" >}}

    ```shell
    mysql --host 127.0.0.1 --port 4000 -u root
    ```

5. 通过 <http://127.0.0.1:9090> 访问 TiDB 的 Prometheus 管理界面。

6. 通过 <http://127.0.0.1:2379/dashboard> 访问 TiDB 的 Dashboard 页面，默认用户名为 root，密码为空。

7. 测试完成后清理集群，绿色环保。通过 `ctrl-c` 停掉进程后，执行以下命令：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup clean --all
    ```

## 第二种：使用 TiUP cluster 在单机上模拟生产环境部署步骤

- 适用场景：希望用单台 Linux 服务器，体验 TiDB 最小的完整拓扑的集群，并模拟生产的部署步骤。
- 耗时：10 分钟

本节介绍如何参照 TiUP 最小拓扑的一个 YAML 文件部署 TiDB 集群。

### 准备环境

准备一台部署主机，确保其软件满足需求：

- 推荐安装 CentOS 7.3 及以上版本
- Linux 操作系统开放外网访问，用于下载 TiDB 及相关软件安装包

最小规模的 TiDB 集群拓扑：

| 实例 | 个数 | IP | 配置 |
|:-- | :-- | :-- | :-- |
| TiKV | 3 | 10.0.1.1 <br/> 10.0.1.1 <br/> 10.0.1.1 | 避免端口和目录冲突 |
| TiDB | 1 | 10.0.1.1 | 默认端口 <br/> 全局目录配置 |
| PD | 1 | 10.0.1.1 | 默认端口 <br/> 全局目录配置 |
| TiFlash | 1 | 10.0.1.1 | 默认端口 <br/> 全局目录配置 |
| Monitor | 1 | 10.0.1.1 | 默认端口 <br/> 全局目录配置 |

部署主机软件和环境要求：

- 部署需要使用部署主机的 root 用户及密码
- 部署主机[关闭防火墙](/production-deployment-using-tiup.md#如何关闭部署机器的防火墙)或者开放 TiDB 集群的节点间所需端口
- 目前 TiUP 仅支持在 x86_64 (AMD64) 架构上部署 TiDB 集群（TiUP 将在 4.0 GA 时支持在 ARM 架构上部署）
    - 在 AMD64 架构下，建议使用 CentOS 7.3 及以上版本 Linux 操作系统
    - 在 ARM 架构下，建议使用 CentOS 7.6 1810 版本 Linux 操作系统

### 实施部署

> **注意：**
>
> 你可以使用 Linux 系统的任一普通用户或 root 用户登录主机，以下步骤以 root 用户为例。

1. 下载并安装 TiUP：

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 安装 TiUP 的 cluster 组件：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

3. 如果机器已经安装 TiUP cluster，需要更新软件版本：

    {{< copyable "shell-regular" >}}
    
    ```shell
    tiup update --self && tiup update cluster
    ```

4. 由于模拟多机部署，需要通过 `root` 用户调大 sshd 服务的连接数限制：

    1. 修改 `/etc/ssh/sshd_config` 将 `MaxSessions` 调至 20。
    2. 重启 sshd 服务：

        {{< copyable "shell-regular" >}}
        
        ```shell
        service sshd restart
        ```

5. 创建并启动集群

    按下面的配置模板，编辑配置文件，命名为 `topo.yaml`，其中：

    - `user: "tidb"`：表示通过 `tidb` 系统用户（部署会自动创建）来做集群的内部管理，默认使用 22 端口通过 ssh 登录目标机器
    - `replication.enable-placement-rules`：设置这个 PD 参数来确保 TiFlash 正常运行
    - `host`：设置为本部署主机的 IP

    配置模板如下：

    {{< copyable "shell-regular" >}}
    
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
       log.slow-threshold: 300
     tikv:
       readpool.storage.use-unified-pool: false
       readpool.coprocessor.use-unified-pool: true
     pd:
       replication.enable-placement-rules: true
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
     
     - host: 10.0.1.1
       port: 20161
       status_port: 20181
     
     - host: 10.0.1.1
       port: 20162
       status_port: 20182
     
    tiflash_servers:
     - host: 10.0.1.1
     
    monitoring_servers:
     - host: 10.0.1.1
     
    grafana_servers:
     - host: 10.0.1.1
    ```

6. 执行集群部署命令：

    {{< copyable "shell-regular" >}}
    
    ```shell
    tiup cluster deploy <cluster-name> <tidb-version> ./topo.yaml --user root -p
    ```

    - 参数 `<cluster-name>` 表示设置集群名称
    - 参数 `<tidb-version>` 表示设置集群版本，可以通过 `tiup list tidb` 命令来查看当前支持部署的 TiDB 版本

    按照引导，输入”y”及 root 密码，来完成部署：
    
    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

7. 启动集群：

    {{< copyable "shell-regular" >}}
    
    ```shell
    tiup cluster start <cluster-name>
    ```

8. 访问集群：

    - 访问 TiDB 数据库，密码为空：

        ```shell
        mysql -h 10.0.1.1 -P 4000 -u root
        ```

    - 访问 TiDB 的 Grafana 监控：
    
        通过 <http://{grafana-ip}:3000> 访问集群 Grafana 监控页面，默认用户名和密码均为 admin。
    
    - 访问 TiDB 的 Dashboard：
    
        通过 <http://{pd-ip}:2379/dashboard> 访问集群 TiDB Dashboard 监控页面，默认用户名为 root，密码为空。
    
    - 执行以下命令确认当前已经部署的集群列表：

        ```shell
        tiup cluster list
        ```
    
    - 执行以下命令查看集群的拓扑结构和状态：

        ```shell
        tiup cluster display <cluster-name>
        ```
        
## 第三种：使用 TiDB-Wasm 一键体验 TiDB 数据库

- 适用场景：初步极速体验 TiDB 数据库的语法、兼容性等基本功能
- 耗时：即时体验

TiDB-Wasm 是运行在浏览器中的 TiDB 数据库，打开网页即可使用。TiDB-Wasm 可直接进行 SQL 执行、兼容性验证等基本操作。

直接点击网址试用 TiDB-Wasm：<https://tour.pingcap.com>，之后会在内存中构建 TiDB 数据库，预计耗时 10 秒左右。

## 探索更多

- 如果你刚刚部署好一套 TiDB 本地测试集群：
    - 学习 [TiDB SQL 操作](/basic-sql-operations.md)
    - [迁移数据到 TiDB](/data-migration-route.md)
    - 了解 [TiDB 的核心特性与核心应用场景](/overview.md)
    - 了解 [TiDB 的整体架构](/tidb-architecture.md)
    - 了解 [TiDB 与 MySQL 的兼容性](/mysql-compatibility.md)

- 如果你准备好在生产环境部署 TiDB 了：
    - 在线部署：[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)
    - 离线部署：[使用 TiUP 离线部署 TiDB 集群](/production-offline-deployment-using-tiup.md)
    - [使用 TiDB Operator 在云上部署 TiDB](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/)
