---
title: 使用 DM-Ansible 部署 DM 集群
category: tools
---

# 使用 DM-Ansible 部署 DM 集群

DM-Ansible 是 PingCAP 基于 [Ansible](https://docs.ansible.com/ansible/latest/index.html) 的 [Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#about-playbooks) 研发的 DM (Data Migration) 集群部署工具。本文将介绍如何使用 DM-Ansible 快速部署 DM 集群。

## 准备工作

在开始之前，先确保您准备好了以下配置的机器：

1. 部署目标机器若干，配置如下：

    - CentOS 7.3 (64-bit) 或更高版本，x86_64 架构（AMD64）
    - 机器之间内网互通
    - 关闭防火墙，或开放服务端口

2. 一台中控机，配置如下：

    - 包含 Python 2.7 的 CentOS 7.3（64-bit）或更高版本
    - Ansible 2.5 或更高版本
    - 互联网访问

## 第 1 步：在中控机上安装依赖包

> **注意：**
>
> 请确保使用 `root` 账户登录中控机。

根据中控机的操作系统版本，运行相应命令如下：

- CentOS 7：

    ```
    # yum -y install epel-release git curl sshpass
    # yum -y install python-pip
    ```

- Ubuntu：

    ```
    # apt-get -y install git curl sshpass python-pip
    ```

## 第 2 步：在中控机上创建 `tidb` 用户，并生成 SSH 密钥

> **注意：**
>
> 请确保使用 `root` 账户登录中控机。

1. 创建 `tidb` 用户。

    ```
    # useradd -m -d /home/tidb tidb
    ```

2. 为 `tidb` 用户设置密码。

    ```
    # passwd tidb
    ```

3. 在 sudo 文件尾部加上 `tidb ALL=(ALL) NOPASSWD: ALL`，为 `tidb` 用户设置免密使用 sudo。

    ```
    # visudo
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

4. 生成 SSH 密钥。

    执行以下 `su` 命令，将登录用户从 `root` 切换至 `tidb`。

    ```
    # su - tidb
    ```

    为 `tidb` 用户创建 SSH 密钥。当提示 `Enter passphrase` 时，按 <kbd>Enter</kbd> 键。命令成功执行后，生成的 SSH 私钥文件为 `/home/tidb/.ssh/id_rsa`，SSH 公钥文件为`/home/tidb/.ssh/id_rsa.pub`。

    ```
    $ ssh-keygen -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/tidb/.ssh/id_rsa):
    Created directory '/home/tidb/.ssh'.
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /home/tidb/.ssh/id_rsa.
    Your public key has been saved in /home/tidb/.ssh/id_rsa.pub.
    The key fingerprint is:
    SHA256:eIBykszR1KyECA/h0d7PRKz4fhAeli7IrVphhte7/So tidb@172.16.10.49
    The key's randomart image is:
    +---[RSA 2048]----+
    |=+o+.o.          |
    |o=o+o.oo         |
    | .O.=.=          |
    | . B.B +         |
    |o B * B S        |
    | * + * +         |
    |  o + .          |
    | o  E+ .         |
    |o   ..+o.        |
    +----[SHA256]-----+
    ```

## 第 3 步：下载 DM-Ansible 至中控机

> **注意：**
>
> 请确保使用 `tidb` 账户登录中控机。

1. 打开 `/home/tidb` 目录。
2. 执行以下命令下载 DM-Ansible。

    ```bash
    $ wget http://download.pingcap.org/dm-ansible-{version}.tar.gz
    ```

    `{version}` 为期望下载的 DM 版本，如 `v1.0.0-alpha`、`latest` 等。

## 第 4 步：安装 DM-Ansible 及其依赖至中控机

> **注意：**
>
> - 请确保使用 `tidb` 账户登录中控机。
> - 您需要使用 `pip` 方式下载安装 Ansible 及其依赖，否则可能会遇到兼容性问题。 DM-Ansible 当前与 Ansible 2.5 或更高版本兼容。

1. 在中控机上安装 DM-Ansible 及其依赖包：

    ```bash
    $ tar -xzvf dm-ansible-latest.tar.gz
    $ mv dm-ansible-latest dm-ansible
    $ cd /home/tidb/dm-ansible
    $ sudo pip install -r ./requirements.txt
    ```

    Ansible 和相关依赖包含于 `dm-ansible/requirements.txt` 文件中。

2. 查看 Ansible 版本：

    ```bash
    $ ansible --version
    ansible 2.5.0
    ```

## 第 5 步：在中控机上配置 SSH 互信和 sudo 规则

> **注意：**
>
> 请确保使用 `tidb` 账户登录至中控机。

1. 将您部署的目标机器的 IP 地址加至 `hosts.ini` 文件中的 `[servers]` 部分。

    ```
    $ cd /home/tidb/dm-ansible
    $ vi hosts.ini
    [servers]
    172.16.10.71
    172.16.10.72
    172.16.10.73

    [all:vars]
    username = tidb
    ```

2. 运行如下命令，然后输入部署目标机器的 `root` 用户密码。
   
    ```bash
    $ ansible-playbook -i hosts.ini create_users.yml -u root -k
    ```

   该步骤将在部署目标机器上创建 `tidb` 用户，创建 sudo 规则，并为中控机和部署目标机器之间配置 SSH 互信。

## 第 6 步：下载 DM 及监控组件安装包至中控机

> **注意：**
>
> 请确保中控机接入互联网。

在中控机上，运行如下命令：

```bash
ansible-playbook local_prepare.yml
```

## 第 7 步：编辑 `inventory.ini` 配置文件

> **注意：**
>
> 请确保使用 `tidb` 账户登录中控机。

打开并编辑 `/home/tidb/dm-ansible/inventory.ini` 文件如下，以管控 DM 集群。

```ini
dm_worker1 ansible_host=172.16.10.72 server_id=101 source_id="mysql-replica-01" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

根据场景需要，您可以在以下两种集群拓扑中任选一种：

- [单节点上单个 DM-worker 实例的集群拓扑](#选项-1使用单节点上单个-dm-worker-实例的集群拓扑)
- [单节点上多个 DM-worker 实例的集群拓扑](#选项-2使用单节点上多个-dm-worker-实例的集群拓扑)

通常情况下，我们推荐每个节点上部署单个 DM-Worker 实例。但如果您的机器拥有性能远超 [TiDB 软件和硬件环境要求](/op-guide/recommendation.md)中推荐配置的 CPU 和内存，并且每个节点配置 2 块以上的硬盘或大于 2T 的 SSD，您可以在单个节点上部署不超过 2 个 DM-Worker 实例。

### 选项 1：使用单节点上单个 DM-Worker 实例的集群拓扑

| 节点 | 主机 IP | 服务 |
| ---- | ------- | -------- |
| node1 | 172.16.10.71 | DM-master, Prometheus, Grafana, Alertmanager |
| node2 | 172.16.10.72 | DM-worker1 |
| node3 | 172.16.10.73 | DM-worker2 |
| mysql-replica-01| 172.16.10.81 | MySQL |
| mysql-replica-02| 172.16.10.82 | MySQL |

```ini
# DM 模块
[dm_master_servers]
dm_master ansible_host=172.16.10.71

[dm_worker_servers]
dm_worker1 ansible_host=172.16.10.72 server_id=101 source_id="mysql-replica-01" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

dm_worker2 ansible_host=172.16.10.73 server_id=102 source_id="mysql-replica-02" mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

# 监控模块
[prometheus_servers]
prometheus ansible_host=172.16.10.71

[grafana_servers]
grafana ansible_host=172.16.10.71

[alertmanager_servers]
alertmanager ansible_host=172.16.10.71

# 全局变量
[all:vars]
cluster_name = test-cluster

ansible_user = tidb

dm_version = latest

deploy_dir = /data1/dm

grafana_admin_user = "admin"
grafana_admin_password = "admin"
```

关于 DM-worker 参数的更多信息，请参考 [DM-worker 配置及参数描述](#dm-worker-配置及参数描述)。

### 选项 2：使用单节点上多个 DM-worker 实例的集群拓扑

| 节点 | 主机 IP | 服务 |
| ---- | ------- | -------- |
| node1 | 172.16.10.71 | DM-master, Prometheus, Grafana, Alertmanager |
| node2 | 172.16.10.72 | DM-worker1-1, DM-worker1-2 |
| node3 | 172.16.10.73 | DM-worker2-1, DM-worker2-2 |

编辑 `inventory.ini` 文件时，请注意区分这些变量：`server_id`，`deploy_dir`，和 `dm_worker_port`。

```ini
# DM 模块
[dm_master_servers]
dm_master ansible_host=172.16.10.71

[dm_worker_servers]
dm_worker1_1 ansible_host=172.16.10.72 server_id=101 deploy_dir=/data1/dm_worker dm_worker_port=8262 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
dm_worker1_2 ansible_host=172.16.10.72 server_id=102 deploy_dir=/data2/dm_worker dm_worker_port=8263 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

dm_worker2_1 ansible_host=172.16.10.73 server_id=103 deploy_dir=/data1/dm_worker dm_worker_port=8262 mysql_host=172.16.10.83 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
dm_worker2_2 ansible_host=172.16.10.73 server_id=104 deploy_dir=/data2/dm_worker dm_worker_port=8263 mysql_host=172.16.10.84 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

# 监控模块
[prometheus_servers]
prometheus ansible_host=172.16.10.71

[grafana_servers]
grafana ansible_host=172.16.10.71

[alertmanager_servers]
alertmanager ansible_host=172.16.10.71

# 全局变量
[all:vars]
cluster_name = test-cluster

ansible_user = tidb

dm_version = latest

deploy_dir = /data1/dm

grafana_admin_user = "admin"
grafana_admin_password = "admin"
```

### DM-worker 配置及参数描述 

| 变量名称 | 描述 |
| ------------- | ------- 
| source_id | DM-worker 绑定到的一个数据库实例或是具有主从架构的复制组。当发生主从切换的时候，只需要更新 `mysql_host` 或 `mysql_port` 而不用更改该 ID 标识。 |
| server_id | DM-worker 伪装成一个 MySQL slave，该变量即为这个 slave 的 server ID，在 MySQL 集群中需保持全局唯一。取值范围 0 ~ 4294967295。|
| mysql_host | 上游 MySQL 主机 |
| mysql_user | 上游 MySQL 用户名，默认值为 “root”。|
| mysql_password | 上游 MySQL 用户密码，需使用 `dmctl` 工具加密。请参考[使用 dmctl 加密上游 MySQL 用户密码](#使用-dmctl-加密上游-mysql-用户密码)。 |
| mysql_port | 上游 MySQL 端口， 默认 3306。 |
| enable_gtid | DM-worker 是否使用全局事务标识符（GTID）拉取 binlog。使用前提是在上游 MySQL 已开启 GTID 模式。 |
| relay_binlog_name | DM-worker 是否从指定 binlog 文件位置开始拉取 binlog。仅适用于本地无有效 relay log 的情况。|
| relay_binlog_gtid | DM-worker 是否从指定 GTID 位置开始拉取 binlog。仅适用于本地无有效 relay log，且 `enable_gtid` 设置为 true 的情况。 |
| flavor | 代表 MySQL 的版本发布类型。 如果是官方版本，Percona 版，或 Cloud MySQL 版，其值为 “mysql”。 如果是 MariaDB，其值为 "mariadb"。默认值是 "mysql"。 |

关于 `deploy_dir` 配置的更多信息，请参考[配置部署目录](#配置部署目录)。

### 使用 dmctl 加密上游 MySQL 用户密码

假定上游 MySQL 的用户密码为 `123456`，运行以下命令，并将生成的字符串添加至 DM-worker 的 `mysql_password` 变量。

```bash
$ cd /home/tidb/dm-ansible/resources/bin
$ ./dmctl -encrypt 123456
VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=
```

## 第 8 步：编辑 `inventory.ini` 文件中的变量

此步介绍如何编辑部署目录中的变量，如何配置 relay log 同步位置以及 relay log GTID 的同步模式。此外，还会描述 `inventory.ini` 中的全局变量。

### 配置部署目录

编辑 `deploy_dir` 变量以配置部署目录。

- 全局变量默认设为 `/home/tidb/deploy`，适用于所有服务。如果数据盘挂载于 `/data1` 目录，您可以通过以下修改将其变更至 `/data1/dm`。

    ```ini
    ## Global variables.
    [all:vars]
    deploy_dir = /data1/dm
    ```

- 如果需要为某个服务创建单独的部署目录，您可以在 `inventory.ini` 中配置服务主机列表的同时设置 host 变量。此操作需要您添加第一列别名，以避免在混合服务部署场景下产生混淆。

    ```ini
    dm-master ansible_host=172.16.10.71 deploy_dir=/data1/deploy
    ```

### 配置 relay log 同步位置

首次启动 DM-worker 时，您需要配置 `relay_binlog_name` 变量以指定 DM-worker 拉取上游 MySQL 或 MariaDB binlog 的起始位置。

```yaml
[dm_worker_servers]
dm-worker1 ansible_host=172.16.10.72 source_id="mysql-replica-01" server_id=101 relay_binlog_name="binlog.000011" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

dm-worker2 ansible_host=172.16.10.73 source_id="mysql-replica-02" server_id=102 relay_binlog_name="binlog.000002" mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

> **注意：**
>
> 如未设定 `relay_binlog_name`，DM-worker 将从上游 MySQL 或 MariaDB 现有最早时间点的 binlog 文件开始拉取 binlog。拉取到数据同步任务需要的最新 binlog 可能需要很长时间。

### 开启 relay log GTID 同步模式

在 DM 集群中，DM-worker 的 relay log 处理单元负责与上游 MySQL 或 MariaDB 通信，从而将 binlog 拉取至本地文件系统。

DM 目前支持 MySQL GTID 和 MariaDB GTID。您可以通过配置以下项目开启 relay log GTID 同步模式：

- `enable_gtid`：打开 relay log GTID 同步模式以处理 master 和 slave 易位的场景

- `relay_binlog_gtid`：指定 DM-worker 开始拉取对应上游 MySQL 或 MariaDB binlog 的起始位置

示例配置如下：

```yaml
[dm_worker_servers]
dm-worker1 ansible_host=172.16.10.72 source_id="mysql-replica-01" server_id=101 enable_gtid=true relay_binlog_gtid="aae3683d-f77b-11e7-9e3b-02a495f8993c:1-282967971,cc97fa93-f5cf-11e7-ae19-02915c68ee2e:1-284361339" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

dm-worker2 ansible_host=172.16.10.73 source_id="mysql-replica-02" server_id=102 relay_binlog_name=binlog.000002 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

### 全局变量

| 变量名称             | 描述                                |
| --------------- | ---------------------------------------------------------- |
| cluster_name | 集群名称，可调整 |
| dm_version | DM 版本，默认已配置 |
| grafana_admin_user | Grafana 管理员用户名称，默认值 `admin` |
| grafana_admin_password | Grafana 管理员账户的密码，用于通过 Ansible 导入 Dashboard。默认值为 `admin`。如果您在 Grafana 网页端修改了密码，请更新此变量。 |

## 第 9 步：部署 DM 集群

使用 `ansible-playbook` 运行 Playbook，默认并发数量是 5。如果部署目标机器较多，您可以使用 `-f` 参数增加并发数量，例如，`ansible-playbook deploy.yml -f 10`。

以下部署操作示例使用中运行服务的用户为 `tidb`：

1. 编辑 `dm-ansible/inventory.ini` 文件，确保 `ansible_user = tidb`。

    ```ini
    ansible_user = tidb
    ```
   > **注意：**
   >
   > 请勿将 `ansible_user` 设为 `root`，因为 `tidb-ansible` 限制服务需以普通用户运行。

    运行以下命令。如果所有服务都返回 `tidb`，则 SSH 互信配置成功。

    ```bash
    ansible -i inventory.ini all -m shell -a 'whoami'
    ```

    运行以下命令。如果所有服务都返回 `root`，则 `tidb` 用户免密 sudo 操作配置成功。

    ```bash
    ansible -i inventory.ini all -m shell -a 'whoami' -b
    ```

2. 修改内核参数，并部署 DM 集群组件和监控组件。

    ```bash
    ansible-playbook deploy.yml
    ```

3. 启动 DM 集群。

    ```bash
    ansible-playbook start.yml
    ```
    此操作会按顺序启动 DM 集群的所有组件，包括 DM-master，DM-worker，以及监控组件。当一个 DM 集群被关闭后，您可以使用该命令将其开启。

## 第 10 步：关闭 DM 集群

如果您需要关闭一个 DM 集群，运行以下命令：

```bash
$ ansible-playbook stop.yml
```

该操作会按顺序关闭整个 DM 集群中的所有组件，包括 DM-master，DM-worker，以及监控组件。

## 常见部署问题

### 默认服务端口


| 组件 | 端口变量 | 默认端口 | 描述 |
| :-- | :-- | :-- | :-- |
| DM-master | `dm_master_port` | 8261  | DM-master 服务交流端口  |
| DM-worker | `dm_worker_port` | 8262  | DM-worker 服务交流端口 |
| Prometheus | `prometheus_port` | 9090 | Prometheus 服务交流端口 |
| Grafana | `grafana_port` |  3000 | 外部 Web 监控服务及客户端（浏览器）访问端口 |
| Alertmanager | `alertmanager_port` |  9093 | Alertmanager 服务交流端口 |

### 自定义端口

编辑 `inventory.ini` 文件，将服务端口的相关主机变量添加在对应服务 IP 地址后：

```ini
dm_master ansible_host=172.16.10.71 dm_master_port=18261
```

### 更新 DM-Ansible

1. 使用 `tidb` 账户登录至中控机，进入 `/home/tidb` 目录，然后备份`dm-ansible` 文件夹。

    ```
    $ cd /home/tidb
    $ mv dm-ansible dm-ansible-bak
    ```

2. 下载指定版本 DM-Ansible，解压。

    ```
    $ cd /home/tidb
    $ wget http://download.pingcap.org/dm-ansible-{version}.tar.gz
    $ tar -xzvf dm-ansible-latest.tar.gz
    $ mv dm-ansible-latest dm-ansible
    ```

3. 迁移 `inventory.ini` 配置文件。

    ```
    $ cd /home/tidb
    $ cp dm-ansible-bak/inventory.ini dm-ansible/inventory.ini
    ```

4. 迁移 `dmctl` 配置。

    ```
    $ cd /home/tidb/dm-ansible-bak/dmctl
    $ cp * /home/tidb/dm-ansible/dmctl/
    ```

5. 用 Playbook 下载最新的 DM 二进制文件。此文件会自动替换 `/home/tidb/dm-ansible/resource/bin/` 目录下的二进制文件。

    ```
    $ ansible-playbook local_prepare.yml
    ```
