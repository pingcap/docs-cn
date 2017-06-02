### 1 概述
Ansible 是一款自动化运维工具，[TiDB-Ansible](https://github.com/pingcap/tidb-ansible) 是 PingCAP 基于 Ansible playbook 功能编写的集群部署工具。使用 TiDB-Ansible 可以快速部署一个完整的 TiDB 集群（包括 PD、TiDB、TiKV 和集群监控模块)。

本部署工具具有如下特性：
- 通过配置文件设置集群拓扑，一键完成各项运维工作：
  - 初始化机器
  - 部署组件
  - 滚动升级
  - 数据清理
  - 环境清理
  - 配置监控模块
- 支持对机器系统进行初始化，创建部署用户、设置 hostname 等。
- 滚动升级时支持模块存活检测。

### 2 准备机器
- 部署目标机器若干
    - 建议4台及以上，TiKV 建议至少3实例，且与 TiKV、PD 模块不位于同一主机,详见[部署建议](https://github.com/pingcap/docs-cn/blob/master/op-guide/recommendation.md)。
    - Linux 操作系统，x86_64 架构(amd64)，内核版本建议 3.10 以上，推荐 CentOS 7.2 及以上版本, 文件系统推荐 ext4(部分内核版本 xfs 文件系统有 bug, 本工具检查到数据目录非 ext4 会退出)。
  - 机器之间网络互通，防火墙、iptables 等可以在部署验证时关闭，后期开启。
  - 机器的时间、时区设置正确，有 NTP 服务可以同步正确时间。
  - 部署账户具有 sudo 权限，或直接通过 root 用户部署。
  - python 2.6 或 python 2.7。
- 部署中控机一台。
  - python 2.6 或 python 2.7，安装有 ansible 2.3 版本或以上版本。
  - 依赖 python Jinja2 及 MarkupSafe 指定版本模块: `pip install Jinja2==2.7.2 MarkupSafe==0.11`
  - 可通过 ssh 登录目标机器，支持密码登录或 ssh authorized_key 登录。
  - 可以是部署目标机器中的某一台，该机器需开放外网访问，用于下载 binary。

#### 2.1 在中控机器上安装配置 Ansible
按照 [官方手册](http://docs.ansible.com/ansible/intro_installation.html) 安装 Ansible，推荐使用 Ansible 2.3 及以上版本。
安装完成后，可通过 ansible --version 查看版本。

以下是各操作系统 anisble 简单安装说明：

Ubuntu 通过 PPA 源安装:
```
sudo add-apt-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```
CentOS 使用 epel 源安装:
```
yum install epel-release
yum update
yum install ansible
```
macOS 通过 Homebrew 安装:

安装 Homebrew 请参考 [官方主页](https://brew.sh)。
```
brew update
brew install ansible
```
Docker
根据自己的平台，安装并配置 Docker。
```
docker run -v `pwd`:/playbook --rm -it williamyeh/ansible:ubuntu16.04 /bin/bash
cd /playbook # 
```
注意以上命令将当前工作目录挂载为容器中 /playbook 目录。

#### 2.2 下载 TiDB-Ansible
从 Github [TiDB-Ansible 项目](https://github.com/pingcap/tidb-ansible)上下载最新master版本  ZIP包或[点击下载](https://github.com/pingcap/tidb-ansible/archive/master.zip)。

#### 2.3 分配机器资源，编辑 inventory.ini 文件
- 案例1: 标准集群部署

6台机器：2 个 TiDB 实例，3个 PD 实例, 3个 TiKV 实例，第一台 TiDB 机器同时用作监控机。

集群拓扑如下：

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3 |
| node4 | 172.16.10.4 | TiKV1 |
| node5 | 172.16.10.5 | TiKV2 |
| node6 | 172.16.10.6 | TiKV3 |

编辑 inventory.ini 文件：
```
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

### 3 部署任务
> Ansible 远程连接用户(即 ansible_user)可使用 root 或普通用户(用户需要有 sudo 到 root 权限)。

> **TiDB 服务不推荐使用 root 用户运行, 本例使用 tidb 普通用户**。

以下根据这两种情况作说明：
#### 3.1 ansible 通过 root 用户远程连接部署
- 修改 inventory.ini, 本例使用 tidb 帐户作为服务运行用户：
取消 `ansible_user = root` 和 `ansible_become_user`注释，给`ansible_user = tidb`添加注释：
  ```
  ## Connection
  # ssh via root:
  ansible_user = root
  # ansible_become = true
  ansible_become_user = tidb
  
  # ssh via normal user
  # ansible_user = tidb
  ```
- local prepare (联网下载 binary 到中控机)

                ansible-playbook local_prepare.yml

- 初始化系统环境，修改内核参数
  > 如服务运行用户尚未建立，此初始化操作会自动创建该用户。

                ansible-playbook bootstrap.yml
  如果 ansible 使用 root 用户远程连接需要密码, 使用 -k 参数，执行其他 playbook 同理：

                ansible-playbook bootstrap.yml -k

- 部署 TiDB 集群软件

                ansible-playbook deploy.yml

- 启动 TiDB 集群

                ansible-playbook start.yml


#### 3.2 ansible 通过普通用户远程连接部署
> 本例中系统需提前创建该普通用户，并添加 sudo 权限。
- 修改 inventory.ini, 本例使用 tidb 用户作为服务运行用户，配置如下：
  ```
  ## Connection
  # ssh via root:
  # ansible_user = root
  # ansible_become = true
  # ansible_become_user = tidb
  
  # ssh via normal user
  ansible_user = tidb
  ```
- local prepare (联网下载 binary 到中控机)

                ansible-playbook local_prepare.yml

- 初始化系统环境，修改内核参数

                ansible-playbook bootstrap.yml

  如果ansible使用普通用户远程连接需要密码, 需添加 -k 参数，执行其他 playbook 同理：

                ansible-playbook bootstrap.yml -k

  本playbook需要使用 root 权限执行，如果该普通用户 sudo 到 root 需要密码，需添加 -K 参数：

                ansible-playbook bootstrap.yml -k -K

- 部署 TiDB 集群软件

                ansible-playbook deploy.yml

- 启动 TiDB 集群

                ansible-playbook start.yml

#### 3.3 测试集群
- 测试连接 TiDB 集群，推荐在 TiDB 前配置负载均衡来对外统一提供 SQL 接口。

  使用 MySQL 客户端连接测试, 4000为 TiDB 服务默认端口。

                mysql -u root -h 172.16.10.1 -P 4000
- 通过浏览器访问监控平台, 默认帐号密码(admin/admin)。

                http://172.16.10.1:3000

### 4 常见运维操作汇总
|任务|Playbook|
|----|--------|
|启动集群|ansible-playbook start.yml|
|停止集群|ansible-playbook stop.yml|
|销毁集群|ansible-playbook unsafe_cleanup.yml| (若部署目录为挂载点，会报错，但不影响执行效果）|
|清除数据(测试用)|ansible-playbook cleanup_data.yml|
|滚动升级|ansible-playbook rolling_update.yml|
|滚动升级 TiKV|ansible-playbook rolling_update.yml --tags=tikv|
|滚动升级除 pd 外模块|ansible-playbook rolling_update.yml --skip-tags=pd|

> **TiDB 服务数据迁移、性能调优等更多高级功能请参考** https://github.com/pingcap/docs-cn。
