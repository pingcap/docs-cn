---
title: 离线 TiDB Ansible 部署方案
category: deployment
---

#离线 TiDB Ansible 部署方案


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

1.  CentOS 7 Ansible 离线安装方式：

> 下载 [ Ansible ]( https://download.pingcap.org/ansible-2.3-rpms.el7.tar.gz ) 离线安装包 ，上传至中控机。

```ini
  
  tar -xzvf ansible-2.3-rpms.el7.tar.gz
  
  cd ansible-2.3-rpms.el7
  
  rpm -ivh PyYAML*.rpm libtomcrypt*.rpm libtommath*.rpm libyaml*.rpm python-
  babel*.rpm python-backports*.rpm python-backports-ssl_match_hostname*.rpm
  python-httplib2*.rpm python-jinja2*.rpm python-keyczar*.rpm python-
  markupsafe*.rpm python-setuptools*.rpm python-six*.rpm python2-crypto*.rpm
  python2-ecdsa*.rpm python2-paramiko*.rpm python2-pyasn1*.rpm sshpass*.rpm
  rpm -ivh ansible-2.3.1.0-1.el7.noarch.rpm
  
  ansible --version
  # ansible 2.3.1.0
      
```
2.  安装完成后，可通过 `ansible --version` 查看版本。

## TiDB 软件包下载

| 组件类别 | 下载地址 | 说明 |
| -------- | ----  | -------- |
|**部署**| [ tidb-ansible-master ](https://github.com/pingcap/tidb-ansible/archive/master.zip) |  |
|**TiDB**| [ tidb-latest ](http://download.pingcap.org/tidb-latest-linux-amd64-unportable.tar.gz) | |
| | [ tidb-tools-latest ](http://download.pingcap.org/tidb-tools-latest-linux-amd64.tar.gz) |  |
| | [ tidb-binlog-latest ](http://download.pingcap.org/tidb-binlog-latest-linux-amd64.tar.gz) |  |
|**监控**| [ prometheus-1.5.2 ](https://github.com/prometheus/prometheus/releases/download/v1.5.2/prometheus-1.5.2.linux-amd64.tar.gz) |  |
| | [ grafana-4.1.2 ](https://grafanarel.s3.amazonaws.com/builds/grafana-4.1.2-1486989747.linux-x64.tar.gz) |  |
| | [ node_exporter-0.14.0-rc.1 ](http://download.pingcap.org/node_exporter-0.14.0-rc.1.linux-amd64.tar.gz) |  |
| | [ pushgateway-0.3.1 ](http://download.pingcap.org/pushgateway-0.3.1.linux-amd64.tar.gz) |  |
| | [ alertmanager-0.5.1 ](https://github.com/prometheus/alertmanager/releases/download/v0.5.1/alertmanager-0.5.1.linux-amd64.tar.gz) |  |
| | [ daemontools-0.53 ](http://oifici4co.bkt.gdipper.com/daemontools-0.53.tar.gz) |  |
|**测试**| [ fio-2.16 ](https://download.pingcap.org/fio-2.16.tar.gz) |  |
|**Spark**| [ spark-2.1.1-bin-hadoop ](http://download.pingcap.org/spark-2.1.1-bin-hadoop2.7.tgz) |  |
| | [ tispark-SNAPSHOT-jar-with-dependencies ](http://download.pingcap.org/tispark-SNAPSHOT-jar-with-dependencies.jar) |  |
| | [ tispark-sample-data ](http://download.pingcap.org/tispark-sample-data.tar.gz) |  |

> 下载所有软件安装包，上传至中控机。

## 安装部署

1.  解压集群部署工具 `tidb-ansible`

2.  将其它所有组件复制到 `tidb-ansible-master` 下的 `downloads` 目录

3.  将 TiDB 安装包名称变更：

    ```ini
    
    cd tidb-ansible-master/
    
    mv tidb-latest-linux-amd64-unportable.tar.gz tidb-latest.tar.gz
    
    mv tidb-tools-latest-linux-amd64.tar.gz tidb-tools-latest.tar.gz
    
    mv tidb-binlog-latest-linux-amd64.tar.gz tidb-binlog-latest.tar.gz
    
    mv prometheus-1.5.2.linux-amd64.tar.gz prometheus-1.5.2.tar.gz
    
    mv grafana-4.1.2-1486989747.linux-x64.tar.gz grafana-4.1.2.tar.gz
    
    mv node_exporter-0.14.0-rc.1.linux-amd64.tar.gz node_exporter-0.14.0.tar.gz
    
    mv pushgateway-0.3.1.linux-amd64.tar.gz pushgateway-0.3.1.tar.gz
    
    mv alertmanager-0.5.1.linux-amd64.tar.gz alertmanager-0.5.1.tar.gz
  
    ```

## 分配机器资源，编辑 inventory.ini 文件

> inventory.ini 文件路径为 tidb-ansible-master/inventory.ini。

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

`tidb-ansible` 解压后默认的文件夹名称为 `tidb-ansible-master`，该文件夹包含用 TiDB-Ansible 来部署 TiDB 集群所需要的所有文件。

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

    2.  使用 `local_prepare.yml` playbook， 离线环境将检查 `downloads` 目录下各个集群组件并完成复制解压：

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
