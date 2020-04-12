---
title: 使用 TiUP cluster 快速构建 TiDB 集群
category: how-to
---

# 使用 TiUP cluster 快速构建 TiDB 集群

本文档介绍如何通过 TiUP 快速一键部署单机 TiDB 测试集群以及最小拓扑的 TiDB 集群。[TiUP 最小拓扑](https://github.com/pingcap-incubator/tiup-cluster/blob/master/examples/minimal.yaml) 可以通过一个 YAML 文件定义多个服务，然后一键部署、启动、停止、销毁。

> **警告：**
>
> 对于生产环境，不要使用 TiUP 单机版或者最小拓扑模版进行部署，而应使用 [TiUP 部署 TiDB 集群](/how-to/deploy/orchestrated/tiup.md)。

## 准备环境

确保你的主机（中控机或者单机搭建环境）的软件满足需求：

- 推荐安装 CentOS 7.3 及以上版本 Linux 操作系统
- 开放外网访问，用于下载 TiDB 及相关软件安装包
- 安装 TiUP 组件

## 快速部署

1. 下载 `TiUP`

    {{< copyable "shell-regular" >}}

    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    预期输出 

    ```shell
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100 3418k  100 3418k    0     0  2878k      0  0:00:01  0:00:01 --:--:-- 2880k
    Detected shell: /bin/bash
    Shell profile:  /home/tidb/.bash_profile
    Installed path: /home/tidb/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

2. 声明全局环境变量

    {{< copyable "shell-regular" >}}

    ```bash
    source .bash_profile
    ```

3. 在当前 session 启动集群

    {{< copyable "shell-regular" >}}

    ```bash
    tiup playground
    ```

4. 创建新的会话来访问集群

- 访问 TiDB 数据库

    {{< copyable "shell-regular" >}}

    ```bash
    mysql -h 10.0.1.1 -P 4000 -u root
    ```

- 访问 TiDB 的 Grafana 监控

    访问集群 Grafana 监控页面：<http://localhost:3000> 默认用户名和密码均为 admin。

- 访问 TiDB 的 Dashboard
  
    访问集群 TiDB-Dashboard 监控页面：<http://localhost:2379/dashboard> 默认用户名 root 密码为空。

## 部署最小规模的 TiDB 集群

- 部署集群信息

|实例 | 个数 | IP |配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiKV | 3 | 10.0.1.1 <br> 10.0.1.2 <br> 10.0.1.3 | 默认端口 <br> 全局目录配置 |
| TiDB |1 | 10.0.1.1 | 默认端口 <br>  全局目录配置 |
| PD | 3 |10.0.1.1 <br> 10.0.1.2 <br> 10.0.1.3 | 默认端口 <br> 全局目录配置 |
| TiFlash | 1 | 10.0.1.2 | 默认端口 <br> 全局目录配置 |

- 部署节点软件和环境要求

  - 中控机可以使用部署节点的 root 用户或者具体 sudo 权限的用户的密钥或者密码可以直接 ssh 登陆；

  - 所有的机器关闭防火墙或者开放 TiDB 集群的节点间所需端口

  - 目前 TiUP 仅支持在 x86_64 (AMD64) 架构上部署 TiDB 集群（TiUP 将在 4.0 GA 时支持在 ARM 架构上部署）

    - 在 AMD64 架构下，建议使用 CentOS 7.3 及以上版本 Linux 操作系统

    - 在 ARM 架构下，建议使用 CentOS 7.6 1810 版本 Linux 操作系统

1. 安装 TiUP 的 cluster 组件（TiUP 已经安装完成）

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster
    ```

2. 如果已经安装 TiUP cluster 的机器更新软件版本

    {{< copyable "shell-regular" >}}

    ```bash
    tiup update cluster
    ```

3. 创建并启动集群

    - 复制[最小集群拓扑的 YAML](https://github.com/pingcap-incubator/tiup-cluster/blob/master/examples/minimal.yaml) 文件到目标机器，创建 topo.yaml 文件。

      - 通过 tidb 用户部署集群（如部署前未创建，部署命令会自动创建），默认使用 22 端口通过 ssh 登陆目标机器，在 tidb 用户 `/home/tidb` 目录下面创建部署目录 `/home/tidb/deploy` 和数据目录 `/home/tidb/data`。

      - 设置 PD 参数 `replication.enable-placement-rules` 参数来确保 TiFlash 正常运行。

      - 所有节点服务均采用默认配置（包括：端口、目录、参数文件）。

    {{< copyable "shell-regular" >}}

    ```yaml
    # The topology template is used deploy a minimal TiDB cluster, which suitable
    # for scenarios with only three machinescontains. The minimal cluster contains
    # - 3 PD nodes
    # - 3 TiKV nodes
    # - 1 TiDB nodes
    # You can change the hosts according your environment
    
    global:
      user: "tidb"
      ssh_port: 22
      deploy_dir: "deploy"
      data_dir: "data"
    
    server_configs:
      pd:
        replication.enable-placement-rules: true

    pd_servers:
      - host: 10.0.1.1
      - host: 10.0.1.2
      - host: 10.0.1.2
    
    tikv_servers:
      - host: 10.0.1.1
      - host: 10.0.1.2
      - host: 10.0.1.3
    
    tidb_servers:
      - host: 10.0.1.1
    
    tiflash_servers:
      - host: 10.0.1.2

    monitoring_servers:
      - host: 10.0.1.3
    
    grafana_servers:
      - host: 10.0.1.3
    
    alertmanager_servers:
      - host: 10.0.1.3
    ```
   
4. 部署集群

    - <cluster-name> 设置集群名称,可以通过 `tiup cluster list` 命令来确认当前已经部署的集群信息。
    - <tidb-version> 设置部署集群的 TiDB 版本，可以通过 `tiup list tidb --refresh` 命令来确认当前支持部署的 TiDB 版本情况。
    - <Private Key>  设置密钥登陆，如果使用密码登陆，可以去掉 `-i` 配置，`Entered` 可以直接进入密码交互窗口。

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster deploy <cluster-name> <tidb-version> ./topo.yaml --user root -i <Private Key>
    ```  

5. 启动集群

   {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster start <cluster-name>
    ```    

6. 访问集群

- 访问 TiDB 数据库

    {{< copyable "shell-regular" >}}

    ```bash
    mysql -h 10.0.1.1 -P 4000 -u root
    ```

- 访问 TiDB 的 Grafana 监控

    访问集群 Grafana 监控页面：<http://10.0.1.3:3000> 默认用户名和密码均为 admin。

- 访问 TiDB 的 Dashboard
  
    访问集群 TiDB-Dashboard 监控页面：<http://{pd-leader-ip}:2379/dashboard> 默认用户名 root 密码为空。