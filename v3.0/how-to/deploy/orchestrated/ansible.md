---
title: TiDB-Ansible 部署方案
category: how-to
aliases: ['/docs-cn/op-guide/ansible-deployment/']
---

# TiDB-Ansible 部署方案

## 概述

Ansible 是一款自动化运维工具，[TiDB-Ansible](https://github.com/pingcap/tidb-ansible) 是 PingCAP 基于 Ansible playbook 功能编写的集群部署工具。本文档介绍如何使用 TiDB-Ansible 部署一个完整的 TiDB 集群。

本部署工具可以通过配置文件设置集群拓扑，完成以下各项运维工作：

- 初始化操作系统参数
- 部署 TiDB 集群（包括 PD、TiDB、TiKV 等组件和监控组件）
- [启动集群](/how-to/maintain/ansible-operations.md#启动集群)
- [关闭集群](/how-to/maintain/ansible-operations.md#关闭集群)
- [变更组件配置](/how-to/upgrade/rolling-updates-with-ansible.md#变更组件配置)
- [集群扩容缩容](/how-to/scale/with-ansible.md)
- [升级组件版本](/how-to/upgrade/rolling-updates-with-ansible.md#升级组件版本)
- [集群开启 binlog](/reference/tidb-binlog-overview.md)
- [清除集群数据](/how-to/maintain/ansible-operations.md#清除集群数据)
- [销毁集群](/how-to/maintain/ansible-operations.md#销毁集群)

> **注意：**
>
> 对于生产环境，须使用 TiDB-Ansible 部署 TiDB 集群。如果只是用于测试 TiDB 或体验 TiDB 的特性，建议[使用 Docker Compose 在单机上快速部署 TiDB 集群](/how-to/get-started/deploy-tidb-from-docker-compose.md)。

## 准备机器

1. 部署目标机器若干

    - 建议 4 台及以上，TiKV 至少 3 实例，且与 TiDB、PD 模块不位于同一主机，详见[部署建议](/how-to/deploy/hardware-recommendations.md)。
    - 推荐安装 CentOS 7.3 及以上版本 Linux 操作系统，x86_64 架构 (amd64)。
    - 机器之间内网互通。

    > **注意：**
    >
    > 使用 Ansible 方式部署时，TiKV 及 PD 节点数据目录所在磁盘请使用 SSD 磁盘，否则无法通过检测。** 如果仅验证功能，建议使用 [Docker Compose 部署方案](/how-to/get-started/deploy-tidb-from-docker-compose.md)单机进行测试。

2. 部署中控机一台:

    - 中控机可以是部署目标机器中的某一台。
    - 推荐安装 CentOS 7.3 及以上版本 Linux 操作系统（默认包含 Python 2.7）。
    - 该机器需开放外网访问，用于下载 TiDB 及相关软件安装包。

## 在中控机上安装系统依赖包

以 `root` 用户登录中控机

如果中控机是 CentOS 7 系统，执行以下命令：

```
# yum -y install epel-release git curl sshpass
# yum -y install python2-pip
```

如果是中控机是 Ubuntu 系统，执行以下命令：

```
# apt-get -y install git curl sshpass python2-pip
```

## 在中控机上创建 tidb 用户，并生成 ssh key

以 `root` 用户登录中控机，执行以下命令

创建 `tidb` 用户

```
# useradd -m -d /home/tidb tidb
```

设置 `tidb` 用户密码

```
# passwd tidb
```

配置 `tidb` 用户 sudo 免密码，将 `tidb ALL=(ALL) NOPASSWD: ALL` 添加到文件末尾即可。

```
# visudo
tidb ALL=(ALL) NOPASSWD: ALL
```

生成 ssh key: 执行 `su` 命令从 `root` 用户切换到 `tidb` 用户下。

```
# su - tidb
```

创建 `tidb` 用户 ssh key， 提示 `Enter passphrase` 时直接回车即可。执行成功后，ssh 私钥文件为 `/home/tidb/.ssh/id_rsa`， ssh 公钥文件为 `/home/tidb/.ssh/id_rsa.pub`。

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

## 在中控机器上下载 TiDB-Ansible

以 `tidb` 用户登录中控机并进入 `/home/tidb` 目录。以下为 tidb-ansible 与 TiDB 的版本对应关系，版本选择可以咨询官方。

| TiDB 版本 | tidb-ansible tag | 备注 |
| -------- | ---------------- | --- |
| 2.0 版本 | v2.0.10、v2.0.11 | 最新 2.0 稳定版本，可用于生产环境。 |
| 2.1 版本 | v2.1.1 ~ v2.1.8 等 | 最新 2.1 稳定版本，可用于生产环境（建议）。 |
| 3.0 版本 | v3.0.0-beta、v3.0.0-beta.1 等 | 目前是 beta 版本，不建议用于生产环境。 |
| latest 版本 | None | 包含最新特性，每日更新，不建议用于生产环境。 |

使用以下命令从 Github [TiDB-Ansible 项目](https://github.com/pingcap/tidb-ansible)上下载 TiDB-Ansible [相应版本](https://github.com/pingcap/tidb-ansible/tags)，默认的文件夹名称为 `tidb-ansible`。

> **注意：**
>
> 部署和升级 TiDB 集群需使用对应的 tidb-ansible 版本，通过改 `inventory.ini` 文件中的版本来混用可能会产生一些错误。

- 下载指定 tag 的 tidb-ansible：

    ```
    $ git clone -b $tag https://github.com/pingcap/tidb-ansible.git
    ```

- 下载 latest 版本对应的 tidb-ansible：

    ```
    $ git clone https://github.com/pingcap/tidb-ansible.git
    ```

> **注意：**
>
> 请务必按文档操作，将 `tidb-ansible` 下载到 `/home/tidb` 目录下，权限为 `tidb` 用户，不要下载到 `/root` 下，否则会遇到权限问题。

## 在中控机器上安装 Ansible 及其依赖

以 `tidb` 用户登录中控机，请务必按以下方式通过 pip 安装 Ansible 及其相关依赖的指定版本，否则会有兼容问题。安装完成后，可通过 `ansible --version` 查看 Ansible 版本。目前 release-2.0、release-2.1 及 master 版本兼容 Ansible 2.4 及 Ansible 2.5 版本，Ansible 及相关依赖版本记录在 `tidb-ansible/requirements.txt` 文件中。

  ```bash
  $ cd /home/tidb/tidb-ansible
  $ sudo pip install -r ./requirements.txt
  $ ansible --version
    ansible 2.5.0
  ```

## 在中控机上配置部署机器 ssh 互信及 sudo 规则

以 `tidb` 用户登录中控机，将你的部署目标机器 IP 添加到 `hosts.ini` 文件 `[servers]` 区块下。

```
$ cd /home/tidb/tidb-ansible
$ vi hosts.ini
[servers]
172.16.10.1
172.16.10.2
172.16.10.3
172.16.10.4
172.16.10.5
172.16.10.6

[all:vars]
username = tidb
ntp_server = pool.ntp.org
```

执行以下命令，按提示输入部署目标机器 `root` 用户密码。该步骤将在部署目标机器上创建 `tidb` 用户，并配置 sudo 规则，配置中控机与部署目标机器之间的 ssh 互信。

```
$ ansible-playbook -i hosts.ini create_users.yml -u root -k
```

> 手工配置 ssh 互信及 sudo 免密码可参考[如何手工配置 ssh 互信及 sudo 免密码](#如何手工配置-ssh-互信及-sudo-免密码)。

## 在部署目标机器上安装 NTP 服务

> 如果你的部署目标机器时间、时区设置一致，已开启 NTP 服务且在正常同步时间，此步骤可忽略。可参考[如何检测 NTP 服务是否正常](#如何检测-ntp-服务是否正常)。
> 该步骤将在部署目标机器上使用系统自带软件源联网安装并启动 NTP 服务，服务使用安装包默认的 NTP server 列表，见配置文件 `/etc/ntp.conf` 中 server 参数，如果使用默认的 NTP server，你的机器需要连接外网。
> 为了让 NTP 尽快开始同步，启动 NTP 服务前，系统会 ntpdate `hosts.ini` 文件中的 `ntp_server` 一次，默认为 `pool.ntp.org`，也可替换为你的 NTP server。

以 `tidb` 用户登录中控机，执行以下命令：

```
$ cd /home/tidb/tidb-ansible
$ ansible-playbook -i hosts.ini deploy_ntp.yml -u tidb -b
```

## 在部署目标机器上配置 CPUfreq 调节器模式

为了让 CPU 发挥最大性能，请将 CPUfreq 调节器模式设置为 `performance` 模式。

> 你可以查看[使用 CPUFREQ 调控器](https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/power_management_guide/cpufreq_governors#cpufreq_setup)文档, 了解更多 CPUFREQ 相关信息。

你可以通过 `cpupower` 命令查看系统支持的调节器模式：

```
# cpupower frequency-info --governors
analyzing CPU 0:
  available cpufreq governors: performance powersave
```

本例中系统支持设置 `performance` 和 `powersave` 模式。如果返回 “Not Available”，表示当前系统不支持配置 CPUfreq，跳过该步骤即可。

```
# cpupower frequency-info --governors
analyzing CPU 0:
  available cpufreq governors: Not Available
```

你可以通过 `cpupower` 命令查看系统当前的 CPUfreq 调节器模式：

```
# cpupower frequency-info --policy
analyzing CPU 0:
  current policy: frequency should be within 1.20 GHz and 3.20 GHz.
                  The governor "powersave" may decide which speed to use
                  within this range.
```

本例中当前配置是 `powersave` 模式，你可以通过以下命令设置为 `performance` 模式。

```
# cpupower frequency-set --governor performance
```

你也可以通过以下命令在部署目标机器上批量设置：

```
$ ansible -i hosts.ini all -m shell -a "cpupower frequency-set --governor performance" -u tidb -b
```

## 在部署目标机器上添加数据盘 ext4 文件系统挂载参数

部署目标机器数据盘请格式化成 ext4 文件系统，挂载时请添加 nodelalloc 和 noatime 挂载参数。`nodelalloc` 是必选参数，否则 Ansible 安装时检测无法通过，noatime 是可选建议参数。

> 如果你的数据盘已经格式化成 ext4 并挂载，可先执行 `umount` 命令卸载，从编辑 `/etc/fstab` 文件步骤开始执行，添加挂载参数重新挂载即可。

  ```
  # umount /dev/nvme0n1
  ```

下面以 /dev/nvme0n1 数据盘为例：

查看数据盘

```
# fdisk -l
Disk /dev/nvme0n1: 1000 GB
```

创建分区表

```
# parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
```

格式化文件系统

```
# mkfs.ext4 /dev/nvme0n1
```

查看数据盘分区 UUID，本例中 nvme0n1 的 UUID 为 c51eb23b-195c-4061-92a9-3fad812cc12f。

```
# lsblk -f
NAME    FSTYPE LABEL UUID                                 MOUNTPOINT
sda
├─sda1  ext4         237b634b-a565-477b-8371-6dff0c41f5ab /boot
├─sda2  swap         f414c5c0-f823-4bb1-8fdf-e531173a72ed
└─sda3  ext4         547909c1-398d-4696-94c6-03e43e317b60 /
sr0
nvme0n1 ext4         c51eb23b-195c-4061-92a9-3fad812cc12f
```

编辑 `/etc/fstab` 文件，添加 `nodelalloc` 挂载参数

```
# vi /etc/fstab
UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2
```

挂载数据盘

```
# mkdir /data1
# mount -a
```

执行以下命令，如果文件系统为 ext4，并且挂载参数中包含 nodelalloc 表示生效：

```
# mount -t ext4
/dev/nvme0n1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
```

## 分配机器资源，编辑 inventory.ini 文件

以 `tidb` 用户登录中控机，`inventory.ini` 文件路径为 `/home/tidb/tidb-ansible/inventory.ini`。

> **注意：**
>
> 请使用内网 IP 来部署集群，如果部署目标机器 SSH 端口非默认 22 端口，需添加 `ansible_port` 变量，如 `TiDB1 ansible_host=172.16.10.1 ansible_port=5555`。

标准 TiDB 集群需要 6 台机器:

- 2 个 TiDB 节点
- 3 个 PD 节点
- 3 个 TiKV 节点，第一台 TiDB 机器同时用作监控机

默认情况下，单台机器上只需部署一个 TiKV 实例。如果你的 TiKV 部署机器 CPU 及内存配置是[部署建议](/how-to/deploy/hardware-recommendations.md)的两倍或以上，并且拥有两块 SSD 硬盘或单块容量超 2T 的 SSD 硬盘，可以考虑部署两实例，但不建议部署两个以上实例。

### 单机单 TiKV 实例集群拓扑

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

[monitoring_servers]
172.16.10.1

[grafana_servers]
172.16.10.1

[monitored_servers]
172.16.10.1
172.16.10.2
172.16.10.3
172.16.10.4
172.16.10.5
172.16.10.6
```

### 单机多 TiKV 实例集群拓扑

以两实例为例：

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3 |
| node4 | 172.16.10.4 | TiKV1-1, TiKV1-2 |
| node5 | 172.16.10.5 | TiKV2-1, TiKV2-2 |
| node6 | 172.16.10.6 | TiKV3-1, TiKV3-2 |

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
TiKV2-1 ansible_host=172.16.10.5 deploy_dir=/data1/deploy tikv_port=20171 labels="host=tikv2"
TiKV2-2 ansible_host=172.16.10.5 deploy_dir=/data2/deploy tikv_port=20172 labels="host=tikv2"
TiKV3-1 ansible_host=172.16.10.6 deploy_dir=/data1/deploy tikv_port=20171 labels="host=tikv3"
TiKV3-2 ansible_host=172.16.10.6 deploy_dir=/data2/deploy tikv_port=20172 labels="host=tikv3"

# 部署 3.0 版本的 TiDB 集群时，多实例场景需要额外配置 status 端口，示例如下：
# TiKV1-1 ansible_host=172.16.10.4 deploy_dir=/data1/deploy tikv_port=20171 tikv_status_port=20181 labels="host=tikv1"
# TiKV1-2 ansible_host=172.16.10.4 deploy_dir=/data2/deploy tikv_port=20172 tikv_status_port=20182 labels="host=tikv1"
# TiKV2-1 ansible_host=172.16.10.5 deploy_dir=/data1/deploy tikv_port=20171 tikv_status_port=20181 labels="host=tikv2"
# TiKV2-2 ansible_host=172.16.10.5 deploy_dir=/data2/deploy tikv_port=20172 tikv_status_port=20182 labels="host=tikv2"
# TiKV3-1 ansible_host=172.16.10.6 deploy_dir=/data1/deploy tikv_port=20171 tikv_status_port=20181 labels="host=tikv3"
# TiKV3-2 ansible_host=172.16.10.6 deploy_dir=/data2/deploy tikv_port=20172 tikv_status_port=20182 labels="host=tikv3"

[monitoring_servers]
172.16.10.1

[grafana_servers]
172.16.10.1

[monitored_servers]
172.16.10.1
172.16.10.2
172.16.10.3
172.16.10.4
172.16.10.5
172.16.10.6

[pd_servers:vars]
location_labels = ["host"]
```

- 服务配置文件参数调整

    1. 多实例情况下，需要修改 `tidb-ansible/conf/tikv.yml` 中 `block-cache-size` 下面的 `capacity` 参数：

        ```
        storage:
          block-cache:
            capacity: "1GB"
        ```

        > **注意：**
        >
        > TiKV 实例数量指每个服务器上 TiKV 的进程数量。
        >
        > 推荐设置：`capacity` = MEM_TOTAL * 0.5 / TiKV 实例数量

    2. 多实例情况下，需要修改 `tidb-ansible/conf/tikv.yml` 中 `high-concurrency`、`normal-concurrency` 和 `low-concurrency` 三个参数：

        ```
        readpool:
          coprocessor:
            # Notice: if CPU_NUM > 8, default thread pool size for coprocessors
            # will be set to CPU_NUM * 0.8.
            # high-concurrency: 8
            # normal-concurrency: 8
            # low-concurrency: 8
        ```

        > **注意：**
        >
        > 推荐设置：TiKV 实例数量 \* 参数值 = CPU 核心数量 \* 0.8

    3. 如果多个 TiKV 实例部署在同一块物理磁盘上，需要修改 `conf/tikv.yml` 中的 `capacity` 参数:

        ```
        raftstore:
          capacity: 0
        ```

        > **注意**
        >
        > 推荐配置：`capacity` = 磁盘总容量 / TiKV 实例数量
        >
        > 例如：`capacity: "100GB"`

### inventory.ini 变量调整

#### 部署目录调整

部署目录通过 `deploy_dir` 变量控制，默认全局变量已设置为 `/home/tidb/deploy`，对所有服务生效。如数据盘挂载目录为 `/data1`，可设置为 `/data1/deploy`，样例如下:

```
## Global variables
[all:vars]
deploy_dir = /data1/deploy
```

如为某一服务单独设置部署目录，可在配置服务主机列表时配置主机变量，以 TiKV 节点为例，其他服务类推，请务必添加第一列别名，以免服务混布时混淆。

```
TiKV1-1 ansible_host=172.16.10.4 deploy_dir=/data1/deploy
```

#### 其他变量调整

> **注意：**
>
> 以下控制变量开启请使用首字母大写 `True`，关闭请使用首字母大写 `False`。

| 变量            | 含义                                                        |
| --------------- | ---------------------------------------------------------- |
| cluster_name | 集群名称，可调整 |
| tidb_version | TiDB 版本，TiDB-Ansible 各分支默认已配置 |
| process_supervision | 进程监管方式，默认为 systemd，可选 supervise |
| timezone | 新安装 TiDB 集群第一次启动 bootstrap（初始化）时，将 TiDB 全局默认时区设置为该值。TiDB 使用的时区后续可通过 `time_zone` 全局变量和 session 变量来修改，参考[时区支持](../sql/time-zone.md)。 默认为 `Asia/Shanghai`，可选值参考 [timzone 列表](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)。 |
| enable_firewalld | 开启防火墙，默认不开启，如需开启，请将[部署建议-网络要求](/how-to/deploy/hardware-recommendations.md#网络要求) 中的端口加入白名单 |
| enable_ntpd | 检测部署目标机器 NTP 服务，默认为 True，请勿关闭 |
| set_hostname | 根据 IP 修改部署目标机器主机名，默认为 False |
| enable_binlog | 是否部署 pump 并开启 binlog，默认为 False，依赖 Kafka 集群，参见 `zookeeper_addrs` 变量 |
| zookeeper_addrs | binlog Kafka 集群的 zookeeper 地址 |
| enable_slow_query_log | TiDB 慢查询日志记录到单独文件({{ deploy_dir }}/log/tidb_slow_query.log)，默认为 False，记录到 tidb 日志 |
| deploy_without_tidb | KV 模式，不部署 TiDB 服务，仅部署 PD、TiKV 及监控服务，请将 `inventory.ini` 文件中 tidb_servers 主机组 IP 设置为空。|
| alertmanager_target | 可选：如果你已单独部署 alertmanager，可配置该变量，格式：alertmanager_host:alertmanager_port |
| grafana_admin_user | Grafana 管理员帐号用户名，默认为 admin |
| grafana_admin_password | Grafana 管理员帐号密码，默认为 admin，用于 Ansible 导入 Dashboard 和创建 API Key，如后期通过 grafana web 修改了密码，请更新此变量 |
| collect_log_recent_hours | 采集日志时，采集最近几个小时的日志，默认为 2 小时 |
| enable_bandwidth_limit | 在中控机上从部署目标机器拉取诊断数据时，是否限速，默认为 True，与 collect_bandwidth_limit 变量结合使用 |
| collect_bandwidth_limit | 在中控机上从部署目标机器拉取诊断数据时限速多少，单位: Kbit/s，默认 10000，即 10Mb/s，如果是单机多 TiKV 实例部署方式，需除以单机实例个数 |
| prometheus_storage_retention | Prometheus 监控数据的保留时间（默认为 30 天）；2.1.7、3.0 以及之后的 tidb-ansible 版本中，`group_vars/monitoring_servers.yml` 文件里新增的配置 |

## 部署任务

> ansible-playbook 执行 Playbook 时默认并发为 5，部署目标机器较多时可添加 -f 参数指定并发，如 `ansible-playbook deploy.yml -f 10`

1. 确认 `tidb-ansible/inventory.ini` 文件中 `ansible_user = tidb`，本例使用 `tidb` 用户作为服务运行用户，配置如下：

    > `ansible_user` 不要设置成 `root` 用户，`tidb-ansible` 限制了服务以普通用户运行。

    ```ini
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

    执行以下命令如果所有 server 返回 `tidb` 表示 ssh 互信配置成功。

    ```
    ansible -i inventory.ini all -m shell -a 'whoami'
    ```

    执行以下命令如果所有 server 返回 `root` 表示 `tidb` 用户 sudo 免密码配置成功。

    ```
    ansible -i inventory.ini all -m shell -a 'whoami' -b
    ```

2. 执行 `local_prepare.yml` playbook，联网下载 TiDB binary 到中控机：

    ```
    ansible-playbook local_prepare.yml
    ```

3. 初始化系统环境，修改内核参数

    ```
    ansible-playbook bootstrap.yml
    ```

4. 部署 TiDB 集群软件

    ```
    ansible-playbook deploy.yml
    ```

    > **注意：**
    >
    > Grafana Dashboard 上的 Report 按钮可用来生成 PDF 文件，此功能依赖 `fontconfig` 包和英文字体。如需使用该功能，登录 **grafana_servers** 机器，用以下命令安装：
    >
    > ```
    > $ sudo yum install fontconfig open-sans-fonts
    > ```

5. 启动 TiDB 集群

    ```
    ansible-playbook start.yml
    ```

## 测试集群

> 测试连接 TiDB 集群，推荐在 TiDB 前配置负载均衡来对外统一提供 SQL 接口。

- 使用 MySQL 客户端连接测试，TCP 4000 端口是 TiDB 服务默认端口。

    ```sql
    mysql -u root -h 172.16.10.1 -P 4000
    ```

- 通过浏览器访问监控平台。

    地址：`http://172.16.10.1:3000`  默认帐号密码是：`admin`/`admin`

## 常见部署问题

### 如何自定义端口

修改 `inventory.ini` 文件，在相应服务 IP 后添加以下主机变量即可：

| 组件 | 端口变量 | 默认端口 | 说明 |
| :-- | :-- | :-- | :-- |
| TiDB | tidb_port | 4000  | 应用及 DBA 工具访问通信端口 |
| TiDB | tidb_status_port | 10080  | TiDB 状态信息上报通信端口 |
| TiKV | tikv_port | 20160 |  TiKV 通信端口  |
| PD | pd_client_port | 2379 | 提供 TiDB 和 PD 通信端口 |
| PD | pd_peer_port | 2380 | PD 集群节点间通信端口 |
| Pump | pump_port | 8250  | Pump 通信端口 |
| Prometheus | prometheus_port | 9090 | Prometheus 服务通信端口 |
| Pushgateway | pushgateway_port | 9091 | TiDB， TiKV， PD 监控聚合和上报端口 |
| Node_exporter | node_exporter_port | 9100 | TiDB 集群每个节点的系统信息上报通信端口 |
| Blackbox_exporter | blackbox_exporter_port | 9115 | Blackbox_exporter 通信端口，用于 TiDB 集群端口监控 |
| Grafana | grafana_port |  3000 | Web 监控服务对外服务和客户端(浏览器)访问端口 |
| Grafana | grafana_collector_port |  8686 | grafana_collector 通信端口，用于将 Dashboard 导出为 PDF 格式 |
| Kafka_exporter | kafka_exporter_port | 9308 | Kafka_exporter 通信端口，用于监控 binlog Kafka 集群 |

### 如何自定义部署目录

修改 `inventory.ini` 文件，在相应服务 IP 后添加以下主机变量即可：

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

### 如何检测 NTP 服务是否正常

执行以下命令输出 `running` 表示 NTP 服务正在运行:

```
$ sudo systemctl status ntpd.service
● ntpd.service - Network Time Service
   Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
   Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago
```

执行 ntpstat 命令，输出 synchronised to NTP server(正在与 NTP server 同步)表示在正常同步：

```
$ ntpstat
synchronised to NTP server (85.199.214.101) at stratum 2
   time correct to within 91 ms
   polling server every 1024 s
```

> **注意：**
>
> Ubuntu 系统需安装 ntpstat 软件包。

以下情况表示 NTP 服务未正常同步：

```
$ ntpstat
unsynchronised
```

以下情况表示 NTP 服务未正常运行：

```
$ ntpstat
Unable to talk to NTP daemon. Is it running?
```

使用以下命令可使 NTP 服务尽快开始同步，pool.ntp.org 可替换为你的 NTP server：

```
$ sudo systemctl stop ntpd.service
$ sudo ntpdate pool.ntp.org
$ sudo systemctl start ntpd.service
```

在 CentOS 7 系统上执行以下命令，可手工安装 NTP 服务：

```
$ sudo yum install ntp ntpdate
$ sudo systemctl start ntpd.service
$ sudo systemctl enable ntpd.service
```

### 如何调整进程监管方式从 supervise 到 systemd

```
# process supervision, [systemd, supervise]
process_supervision = systemd
```

TiDB-Anisble 在 TiDB v1.0.4 版本之前进程监管方式默认为 supervise， 之前安装的集群可保持不变，如需更新为 systemd，需关闭集群按以下方式变更：

```
ansible-playbook stop.yml
ansible-playbook deploy.yml -D
ansible-playbook start.yml
```

### 如何手工配置 ssh 互信及 sudo 免密码

以 `root` 用户依次登录到部署目标机器创建 `tidb` 用户并设置登录密码。

```
# useradd tidb
# passwd tidb
```

执行以下命令，将 `tidb ALL=(ALL) NOPASSWD: ALL` 添加到文件末尾，即配置好 sudo 免密码。

```
# visudo
tidb ALL=(ALL) NOPASSWD: ALL
```

以 `tidb` 用户登录到中控机，执行以下命令，将 `172.16.10.61` 替换成你的部署目标机器 IP，按提示输入部署目标机器 tidb 用户密码，执行成功后即创建好 ssh 互信，其他机器同理。

```
[tidb@172.16.10.49 ~]$ ssh-copy-id -i ~/.ssh/id_rsa.pub 172.16.10.61
```

以 `tidb` 用户登录到中控机，ssh 登录目标机器 IP，不需要输入密码并登录成功，表示 ssh 互信配置成功。

```
[tidb@172.16.10.49 ~]$ ssh 172.16.10.61
[tidb@172.16.10.61 ~]$
```

以 `tidb` 用户登录到部署目标机器后，执行以下命令，不需要输入密码并切换到 root 用户，表示 `tidb` 用户 sudo 免密码配置成功。

```
[tidb@172.16.10.61 ~]$ sudo -su root
[root@172.16.10.61 tidb]#
```

### You need to install jmespath prior to running json_query filter 报错

请参照 [在中控机器上安装 Ansible 及其依赖](#在中控机器上安装-ansible-及其依赖) 在中控机上通过 pip 安装 Ansible 及相关依赖的指定版本，默认会安装 `jmespath`。

可通过以下命令验证 `jmespath` 是否安装成功：

```
$ pip show jmespath
Name: jmespath
Version: 0.9.0
```

在中控机上 python 交互窗口里 `import jmespath`，如果没有报错，表示依赖安装成功，如果有 `ImportError: No module named jmespath` 报错，表示未安装 python `jmespath` 模块。

```
$ python
Python 2.7.5 (default, Nov  6 2016, 00:28:07)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import jmespath
```

### 启动 Pump/Drainer 报 `zk: node does not exist` 错误

请检查 `inventory.ini` 里的 `zookeeper_addrs` 参数配置与 Kafka 集群内的配置是否相同、是否填写了命名空间。关于命名空间的配置说明如下：

```
# ZooKeeper connection string (see ZooKeeper docs for details).
# ZooKeeper address of Kafka cluster, example:
# zookeeper_addrs = "192.168.0.11:2181,192.168.0.12:2181,192.168.0.13:2181"
# You can also append an optional chroot string to the URLs to specify the root directory for all Kafka znodes. Example:
# zookeeper_addrs = "192.168.0.11:2181,192.168.0.12:2181,192.168.0.13:2181/kafka/123"
```
