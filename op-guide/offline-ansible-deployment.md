---
title: 离线 TiDB Ansible 部署方案
category: deployment
---

# 离线 TiDB Ansible 部署方案


## 准备机器

1. 部署中控机一台:

    - Python 2.6 或 Python 2.7，安装有 Ansible 2.3 版本或以上版本。
    - 依赖 Python Jinja2 及 MarkupSafe 指定版本模块：`pip install Jinja2==2.7.2 MarkupSafe==0.11`
    - 可通过 ssh 登录目标机器，支持密码登录或 ssh authorized_key 登录。
    - 中控机可以是部署目标机器中的某一台，该机器需开放外网访问，并且安装 curl 软件包，用于下载 binary。

2. 部署目标机器若干

    - 建议4台及以上，TiKV 至少3实例，且与 TiDB、PD 模块不位于同一主机，详见[部署建议](recommendation.md)。
    - Linux 操作系统，x86_64 架构 (amd64)，内核版本建议 3.10 以上，推荐 CentOS 7.3 及以上版本，文件系统推荐 ext4（部分内核版本 xfs 文件系统有 bug，本工具检查到 xfs 文件系统有 bug 会退出）。
    - 机器之间网络互通，防火墙、iptables 等可以在部署验证时关闭，后期开启。
    - 机器的时间、时区设置正确（要求机器时间同步），有 NTP 服务可以同步正确时间，ubuntu 系统需单独安装 ntpstat 软件包。
    - 若使用普通用户作为 Ansible SSH 远程连接用户，该用户需要有 sudo 到 root 权限，或直接使用 root 用户远程连接。
    - Python 2.6 或 Python 2.7。

## 在中控机器上安装配置 Ansible

1. CentOS 7 Ansible 离线安装方式：

    ```ini
    tar -xzvf ansible-2.3-rpms.el7.tar.gz
    
    cd ansible-2.3-rpms.el7
    
    rpm -ivh PyYAML*.rpm libtomcrypt*.rpm libtommath*.rpm libyaml*.rpm python-
    babel*.rpm python-backports*.rpm python-backports-ssl_match_hostname*.rpm
    python-httplib2*.rpm python-jinja2*.rpm python-keyczar*.rpm python-
    markupsafe*.rpm python-setuptools*.rpm python-six*.rpm python2-crypto*.rpm
    python2-ecdsa*.rpm python2-paramiko*.rpm python2-pyasn1*.rpm sshpass*.rpm
    rpm -ivh ansible-2.3.1.0-1.el7.noarch.rpm
    ```

2. 安装完成后，可通过 `ansible --version` 查看版本：

    ```
    ansible --version
    # ansible 2.3.1.0
    ```

## 安装准备

> 在一台有外网，并且安装有 ansible 的机器执行如下命令：

1. 下载 tidb-ansible：

    - 下载 master 分支的 tidb-ansible，用来安装 master 版本的 tidb 集群（binlog 为 kafka 版本）

        `git clone https://github.com/pingcap/tidb-ansible`

    - 下载 release-1.0 分支的 tidb-ansible，用来安装 release-1.0（GA 版本）版本的 tidb 集群（binlog 为 kafka 版本）

        `git clone -b release-1.0 https://github.com/pingcap/tidb-ansible`

    - 下载 release-1.0-binlog-local 分支的 tidb-ansible，用来安装 release-1.0-binlog-local 版本的 tidb 集群（binlog 为 local 版本）

        `git clone -b release-1.0-binlog-local https://github.com/pingcap/tidb-ansible`

2. 下载 TiDB 相关依赖包：

    ```
    cd tidb-ansible
    ansible-playbook local_prepare.yml
    ```

3. 将执行完以上命令之后的 tidb-ansible 安装包拷贝到中控机。

## 分配机器资源，编辑 inventory.ini 文件

> inventory.ini 文件路径为 tidb-ansible/inventory.ini。

标准 TiDB 集群需要6台机器:

- 2个 TiDB 节点
- 3个 PD 节点
- 3个 TiKV 节点，第一台 TiDB 机器同时用作监控机

### 单机单 TiKV 实例集群拓扑如下

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

### 单机多 TiKV 实例集群拓扑如下(以三实例为例)

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3 |
| node4 | 172.16.10.4 | TiKV1-1, TiKV1-2, TiKV1-3 |
| node5 | 172.16.10.5 | TiKV2-1, TiKV2-2, TiKV2-3 |
| node6 | 172.16.10.6 | TiKV3-1, TiKV3-2, TiKV3-3 |

```ini
[tidb_servers]
172.16.10.1
172.16.10.2

[pd_servers]
172.16.10.1
172.16.10.2
172.16.10.3

[tikv_servers]
TiKV1-1 ansible_host=172.16.10.4 deploy_dir=/data1/deploy tikv_port=20171 labels="host=tikv1"
TiKV1-2 ansible_host=172.16.10.4 deploy_dir=/data2/deploy tikv_port=20172 labels="host=tikv1"
TiKV1-3 ansible_host=172.16.10.4 deploy_dir=/data3/deploy tikv_port=20173 labels="host=tikv1"
TiKV2-1 ansible_host=172.16.10.5 deploy_dir=/data1/deploy tikv_port=20171 labels="host=tikv2"
TiKV2-2 ansible_host=172.16.10.5 deploy_dir=/data2/deploy tikv_port=20172 labels="host=tikv2"
TiKV2-3 ansible_host=172.16.10.5 deploy_dir=/data3/deploy tikv_port=20173 labels="host=tikv2"
TiKV3-1 ansible_host=172.16.10.6 deploy_dir=/data1/deploy tikv_port=20171 labels="host=tikv3"
TiKV3-2 ansible_host=172.16.10.6 deploy_dir=/data2/deploy tikv_port=20172 labels="host=tikv3"
TiKV3-3 ansible_host=172.16.10.6 deploy_dir=/data3/deploy tikv_port=20173 labels="host=tikv3"

[monitored_servers:children]
tidb_servers
tikv_servers
pd_servers

[monitoring_servers]
172.16.10.1

[grafana_servers]
172.16.10.1

......

[pd_servers:vars]
location_labels = ["host"]
```

- 参数调整

    1.  多实例情况下, 需要修改 `conf/tikv.yml` 中的 `end-point-concurrency` 以及 `block-cache-size` 参数:
        - `end-point-concurrency`: 总数低于 CPU Vcores 即可
        - `rocksdb defaultcf block-cache-size(GB)` = MEM * 80% / TiKV 实例数量 * 30%
        - `rocksdb writecf block-cache-size(GB)` = MEM * 80% / TiKV 实例数量 * 45%
        - `rocksdb lockcf block-cache-size(GB)` = MEM * 80% / TiKV 实例数量 * 2.5% (最小 128 MB)
        - `raftdb defaultcf block-cache-size(GB)` = MEM * 80% / TiKV 实例数量 * 2.5% (最小 128 MB)
    2.  如果多个 TiKV 实例部署在同一块物理磁盘上, 需要修改 `conf/tikv.yml` 中的 `capacity` 参数:
        - `capaticy` = (DISK - 日志空间) / TiKV 实例数量, 单位为 GB

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

    2.  初始化系统环境，修改内核参数

        > 如服务运行用户尚未建立，此初始化操作会自动创建该用户。

        ```
        ansible-playbook bootstrap.yml
        ```

        如果 ansible 使用 root 用户远程连接需要密码, 使用 -k 参数，执行其他 playbook 同理：

        ```
        ansible-playbook bootstrap.yml -k
        ```

    3.  部署 TiDB 集群软件

        ```
        ansible-playbook deploy.yml -k
        ```

    4.  启动 TiDB 集群

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

    2.  使用 `local_prepare.yml` playbook， 离线环境将检查 `downloads` 目录下各个集群组件并完成复制解压：

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
