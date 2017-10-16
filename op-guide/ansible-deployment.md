---
title: TiDB Ansible 部署方案
category: deployment
---

# TiDB Ansible 部署方案

## 概述

Ansible 是一款自动化运维工具，[TiDB-Ansible](https://github.com/pingcap/tidb-ansible) 是 PingCAP 基于 Ansible playbook 功能编写的集群部署工具。使用 TiDB-Ansible 可以快速部署一个完整的 TiDB 集群（包括 PD、TiDB、TiKV 和集群监控模块)。

本部署工具可以通过配置文件设置集群拓扑，一键完成以下各项运维工作：

- 初始化操作系统，包括创建部署用户、设置 hostname 等
- 部署组件
- 滚动升级，滚动升级时支持模块存活检测
- 数据清理
- 环境清理
- 配置监控模块

## 准备机器

1.  部署中控机一台:

    - Python 2.6 或 Python 2.7，安装有 Ansible 2.3 版本或以上版本。
    - 依赖 Python Jinja2 及 MarkupSafe 指定版本模块: `pip install Jinja2==2.7.2 MarkupSafe==0.11`
    - 可通过 ssh 登录目标机器，支持密码登录或 ssh authorized_key 登录。
    - 中控机可以是部署目标机器中的某一台，该机器需开放外网访问，并且安装 curl 软件包，用于下载 binary。

2.  部署目标机器若干

    - 建议4台及以上，TiKV 至少3实例，且与 TiDB、PD 模块不位于同一主机,详见[部署建议](https://github.com/pingcap/docs-cn/blob/master/op-guide/recommendation.md)。
    - Linux 操作系统，x86_64 架构(amd64)，内核版本建议 3.10 以上，推荐 CentOS 7.3 及以上版本, 文件系统推荐 ext4(部分内核版本 xfs 文件系统有 bug, 本工具检查到 xfs 文件系统有 bug 会退出)。
    - 机器之间网络互通，防火墙、iptables 等可以在部署验证时关闭，后期开启。
    - 机器的时间、时区设置正确(要求机器时间同步)，有 NTP 服务可以同步正确时间, ubuntu 系统需单独安装 ntpstat 软件包。
    - 若使用普通用户作为 Ansible SSH 远程连接用户，该用户需要有 sudo 到 root 权限，或直接使用 root 用户远程连接。
    - Python 2.6 或 Python 2.7。

## 在中控机器上安装配置 Ansible

按照 [官方手册](http://docs.ansible.com/ansible/intro_installation.html) 安装 Ansible，推荐使用 Ansible 2.3 及以上版本。
安装完成后，可通过 `ansible --version` 查看版本。

以下是各操作系统 Anisble 简单安装说明：

-   CentOS 使用 epel 源安装:

    ```bash
    yum install epel-release
    yum update
    yum install ansible
    ```

-   Ubuntu 通过 PPA 源安装:

    ```bash
    sudo add-apt-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible
    ```

## 下载 TiDB-Ansible

使用以下命令从 Github [TiDB-Ansible 项目](https://github.com/pingcap/tidb-ansible) 上下载 release-1.0 分支，默认的文件夹名称为 `tidb-ansible`。该文件夹包含用 TiDB-Ansible 来部署 TiDB 集群所需要的所有文件。
```
git clone -b release-1.0 https://github.com/pingcap/tidb-ansible.git
```
## 分配机器资源，编辑 inventory.ini 文件

> inventory.ini 文件路径为 tidb-ansible/inventory.ini。

标准 TiDB 集群需要6台机器:

- 2个 TiDB 实例
- 3个 PD 实例
- 3个 TiKV 实例，第一台 TiDB 机器同时用作监控机

集群拓扑如下：

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3 |
| node4 | 172.16.10.4 | TiKV1 |
| node5 | 172.16.10.5 | TiKV2 |
| node6 | 172.16.10.6 | TiKV3 |

```ini
[tidb_servers]
172.16.10.1
172.16.10.2

[pd_servers]
172.16.10.1
172.16.10.2
172.16.10.3

[tikv_servers]
172.16.10.4
172.16.10.5
172.16.10.6

[monitored_servers:children]
tidb_servers
tikv_servers
pd_servers

[monitoring_servers]
172.16.10.1

[grafana_servers]
172.16.10.1
```

## 部署任务

> TiDB 服务不推荐使用 root 用户运行, 本例使用 `tidb` 普通用户作为服务运行用户。

> Ansible 远程连接用户(即 incentory.ini 文件中的 ansible_user)可使用 root 用户或普通用户(该用户需要有 sudo 到 root 权限)。

以下根据这两种情况作说明：

-   Ansible 通过 root 用户远程连接部署

    1.  修改 `inventory.ini`, 本例使用 `tidb` 帐户作为服务运行用户：

        取消 `ansible_user = root` 、`ansible_become = true` 及 `ansible_become_user` 注释，给 `ansible_user = tidb` 添加注释：

        ```ini
        ## Connection
        # ssh via root:
        ansible_user = root
        ansible_become = true
        ansible_become_user = tidb

        # ssh via normal user
        # ansible_user = tidb
        ```

    2.  使用 `local_prepare.yml` playbook, 联网下载 TiDB binary 到中控机：

        ```
        ansible-playbook local_prepare.yml
        ```

    3.  初始化系统环境，修改内核参数

        > 如服务运行用户尚未建立，此初始化操作会自动创建该用户。

        ```
        ansible-playbook bootstrap.yml
        ```

        如果 ansible 使用 root 用户远程连接需要密码, 使用 -k 参数，执行其他 playbook 同理：

        ```
        ansible-playbook bootstrap.yml -k
        ```

    4.  部署 TiDB 集群软件

        ```
        ansible-playbook deploy.yml -k
        ```

    5.  启动 TiDB 集群

        ```
        ansible-playbook start.yml -k
        ```


-   Ansible 通过普通用户远程连接部署

    > 本例中系统需提前创建 tidb 普通用户，并添加 sudo 权限，本例 tidb 帐户同时作为服务运行用户。

    1.  修改 `inventory.ini`, 本例使用 `tidb` 用户作为服务运行用户，配置如下：

        ```ini
        ## Connection
        # ssh via root:
        # ansible_user = root
        # ansible_become = true
        # ansible_become_user = tidb

        # ssh via normal user
        ansible_user = tidb
        ```

    2.  使用 `local_prepare.yml` playbook, 联网下载 TiDB binary 到中控机：

        ```
        ansible-playbook local_prepare.yml
        ```

    3.  初始化系统环境，修改内核参数

        ```
        ansible-playbook bootstrap.yml
        ```

        如果 Ansible 使用普通用户远程连接需要密码, 需添加 -k 参数，执行其他 playbook 同理：

        ```
        ansible-playbook bootstrap.yml -k
        ```

        本 playbook 需要使用 root 权限执行，如果该普通用户 sudo 到 root 需要密码，需添加 -K 参数：

        ```
        ansible-playbook bootstrap.yml -k -K
        ```

    4.  部署 TiDB 集群软件

        ```
        ansible-playbook deploy.yml -k
        ```

    5.  启动 TiDB 集群

        ```
        ansible-playbook start.yml -k
        ```

## 测试集群

> 测试连接 TiDB 集群，推荐在 TiDB 前配置负载均衡来对外统一提供 SQL 接口。

-   使用 MySQL 客户端连接测试, TCP 4000 端口是 TiDB 服务默认端口。

    ```sql
    mysql -u root -h 172.16.10.1 -P 4000
    ```

-   通过浏览器访问监控平台。

    地址：`http://172.16.10.1:3000`  默认帐号密码是：`admin`/`admin`

## 滚动升级

> - 滚动升级 TiDB 服务，滚动升级期间不影响业务运行(最小环境 ：`pd*3 、tidb*2、tikv*3`)
> - 远程连接权限问题，参考以上步骤( 已建立互信无需加 `-k` )
> - 如果集群环境中有 pump / drainer 服务，建议先停止 drainer 后滚动升级 (升级 TiDB 时会升级 pump)。

### 下载 binary

1.  使用 playbook 下载 TiDB 1.0 binary，自动替换 binary 到 `tidb-ansible/resource/bin/`

    ```
    ansible-playbook local_prepare.yml
    ```

2.  使用 wget 下载 binary，解压后手动替换 binary 到 `tidb-ansible/resource/bin/`

    ```
    wget http://download.pingcap.org/tidb-v1.0.0-linux-amd64-unportable.tar.gz
    ```

### 使用 Ansible 滚动升级

1.  滚动升级 TiKV 节点( 只升级单独服务 )

    ```
    ansible-playbook rolling_update.yml --tags=tikv
    ```

2.  滚动升级所有服务

    ```
    ansible-playbook rolling_update.yml
    ```

## 常见运维操作汇总

|任务|Playbook|
|----|--------|
|启动集群|`ansible-playbook start.yml`|
|停止集群|`ansible-playbook stop.yml`|
|销毁集群|`ansible-playbook unsafe_cleanup.yml` (若部署目录为挂载点，会报错，可忽略）|
|清除数据(测试用)|`ansible-playbook cleanup_data.yml`|
|滚动升级|`ansible-playbook rolling_update.yml`|
|滚动升级 TiKV|`ansible-playbook rolling_update.yml --tags=tikv`|
|滚动升级除 pd 外模块|`ansible-playbook rolling_update.yml --skip-tags=pd`|

> TiDB 服务数据迁移、性能调优等更多高级功能请参考 [https://github.com/pingcap/docs-cn](https://github.com/pingcap/docs-cn)

## 常见部署问题

### TiDB 各版本下载链接

- 1.0 版本:
    - [TiDB 1.0-CentOS7](http://download.pingcap.org/tidb-v1.0.0-linux-amd64-unportable.tar.gz)
    - [TiDB 1.0-CentOS6](http://download.pingcap.org/tidb-v1.0.0-linux-amd64-unportable-centos6.tar.gz)

### 如何下载安装指定版本 TiDB

如需安装 TiDB 1.0 版本，需要先下载 TiDB-Ansible release-1.0 分支，确认 inventory.ini 文件中 `tidb_version = v1.0.0`, 安装步骤同上。

从 github 下载 TiDB-Ansible release-1.0 分支:

```
git clone -b release-1.0 https://github.com/pingcap/tidb-ansible.git
```

### 自定义端口
| 组件 | 端口变量 | 默认端口 | 说明 |
| :-- | :-- | :-- | :-- |
| TiDB |  tidb_port | 4000  | 应用及 DBA 工具访问通信端口 |
| TiDB | tidb_status_port | 10080  | TiDB 状态信息上报通信端口 |
| TiKV | tikv_port | 20160 |  TiKV 通信端口  |
| PD | pd_client_port | 2379 | 提供 TiDB 和 PD 通信端口 |
| PD | pd_peer_port | 2380 | PD 集群节点间通信端口 |
| pump | pump_port | 8250  | pump 通信端口 |
| prometheus | prometheus_port | 9090 | Prometheus 服务通信端口  |
| pushgateway | pushgateway_port | 9091 | TiDB, TiKV, PD 监控聚合和上报端口 |
| node_exporter | node_exporter_port | 9100 | TiDB 集群每个节点的系统信息上报通信端口 |
| grafana | grafana_port|  3000 | Web 监控服务对外服务和客户端(浏览器)访问端口 |

### 自定义部署目录
| 组件 | 目录变量 | 默认目录 | 说明 |
| :-- | :-- | :-- | :-- |
| 全局 | deploy_dir | /home/tidb/deploy | 部署目录 |
| TiDB | tidb_log_dir | {{ deploy_dir }}/log  | 日志目录 |
| TiKV | tikv_log_dir | {{ deploy_dir }}/log | 日志目录 |
| TiKV | tikv_data_dir | {{ deploy_dir }}/data | 数据目录 |
| TiKV | wal_dir | "" | rocksdb write-ahead 日志目录，为空时与 TiKV 数据目录一致 |
| TiKV | raftdb_path | "" | raftdb 目录，为空时为 tikv_data_dir/raft |
| PD | pd_log_dir | {{ deploy_dir }}/log | 日志目录 |
| PD | pd_data_dir | {{ deploy_dir }}/data.pd | 数据目录 |
| pump | pump_log_dir | {{ deploy_dir }}/log  | 日志目录 |
| pump | pump_data_dir | {{ deploy_dir }}/data.pump  | 数据目录 |
| prometheus | prometheus_log_dir | {{ deploy_dir }}/log | 日志目录 |
| prometheus | prometheus_data_dir | {{ deploy_dir }}/data.metrics | 数据目录 |
| pushgateway | pushgateway_log_dir | {{ deploy_dir }}/log | 日志目录 |
| node_exporter | node_exporter_log_dir | {{ deploy_dir }}/log | 日志目录 |
| grafana | grafana_log_dir | {{ deploy_dir }}/log | 日志目录 |
| grafana | grafana_data_dir | {{ deploy_dir }}/data.grafana | 数据目录 |
