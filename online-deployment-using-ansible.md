---
title: 使用 TiDB Ansible 部署 TiDB 集群
aliases: ['/docs-cn/v3.1/online-deployment-using-ansible/','/docs-cn/v3.1/how-to/deploy/orchestrated/ansible/']
---

# 使用 TiDB Ansible 部署 TiDB 集群

## 概述

Ansible 是一款自动化运维工具，[TiDB Ansible](https://github.com/pingcap/tidb-ansible) 是 PingCAP 基于 Ansible playbook 功能编写的集群部署工具。本文档介绍如何使用 TiDB Ansible 部署一个完整的 TiDB 集群。

本部署工具可以通过配置文件设置集群拓扑，完成以下各项运维工作：

- 初始化操作系统参数
- 部署 TiDB 集群（包括 PD、TiDB、TiKV 等组件和监控组件）
- [启动集群](/maintain-tidb-using-ansible.md#启动集群)
- [关闭集群](/maintain-tidb-using-ansible.md#关闭集群)
- [变更组件配置](/upgrade-tidb-using-ansible.md#编辑-tidb-集群组件配置文件)
- [集群扩容缩容](/scale-tidb-using-ansible.md)
- [升级组件版本](/upgrade-tidb-using-ansible.md#滚动升级-tidb-集群组件)
- [集群开启 binlog](/tidb-binlog/tidb-binlog-overview.md)
- [清除集群数据](/maintain-tidb-using-ansible.md#清除集群数据)
- [销毁集群](/maintain-tidb-using-ansible.md#销毁集群)

> **注意：**
>
> 对于生产环境，须使用 TiDB Ansible 部署 TiDB 集群。如果只是用于测试 TiDB 或体验 TiDB 的特性，建议[使用 Docker Compose 在单机上快速部署 TiDB 集群](/deploy-test-cluster-using-docker-compose.md)。

## 准备机器

1. 部署目标机器若干

    - 建议 4 台及以上，TiKV 至少 3 实例，且与 TiDB、PD 模块不位于同一主机，详见[部署建议](/hardware-and-software-requirements.md)。
    - 推荐安装 CentOS 7.3 及以上版本 Linux 操作系统，x86_64 架构 (amd64)。
    - 机器之间内网互通。

    > **注意：**
    >
    > 使用 TiDB Ansible 方式部署时，TiKV 及 PD 节点数据目录所在磁盘请使用 SSD 磁盘，否则无法通过检测。**如果仅验证功能，建议使用 [Docker Compose 部署方案](/deploy-test-cluster-using-docker-compose.md)单机进行测试。**

2. 部署中控机一台

    - 中控机可以是部署目标机器中的某一台。
    - 推荐安装 CentOS 7.3 及以上版本 Linux 操作系统（默认包含 Python 2.7）。
    - 该机器需开放外网访问，用于下载 TiDB 及相关软件安装包。

## 第 1 步：在中控机上安装系统依赖包

以 `root` 用户登录中控机，然后根据操作系统类型执行相应的安装命令。

- 如果中控机使用的是 CentOS 7 系统，执行以下命令：

    {{< copyable "shell-root" >}}

    ```bash
    yum -y install epel-release git curl sshpass && \
    yum -y install python2-pip
    ```

- 如果是中控机使用的是 Ubuntu 系统，执行以下命令：

    {{< copyable "shell-root" >}}

    ```bash
    apt-get -y install git curl sshpass python-pip
    ```

## 第 2 步：在中控机上创建 `tidb` 用户，并生成 SSH key

以 `root` 用户登录中控机，执行以下步骤：

1. 创建 `tidb` 用户。

    {{< copyable "shell-root" >}}

    ```bash
    useradd -m -d /home/tidb tidb
    ```

2. 设置 `tidb` 用户密码。

    {{< copyable "shell-root" >}}

    ```bash
    passwd tidb
    ```

3. 配置 `tidb` 用户 sudo 免密码，将 `tidb ALL=(ALL) NOPASSWD: ALL` 添加到文件末尾即可。

    {{< copyable "shell-root" >}}

    ```bash
    visudo
    ```

    ```
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

4. 生成 SSH key。

    执行 `su` 命令，从 `root` 用户切换到 `tidb` 用户下。

    {{< copyable "shell-root" >}}

    ```bash
    su - tidb
    ```

    创建 `tidb` 用户 SSH key，提示 `Enter passphrase` 时直接回车即可。执行成功后，SSH 私钥文件为 `/home/tidb/.ssh/id_rsa`，SSH 公钥文件为 `/home/tidb/.ssh/id_rsa.pub`。

    {{< copyable "shell-regular" >}}

    ```bash
    ssh-keygen -t rsa
    ```

    ```
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

## 第 3 步：在中控机器上下载 TiDB Ansible

以 `tidb` 用户登录中控机并进入 `/home/tidb` 目录。使用以下命令从 [TiDB Ansible 项目](https://github.com/pingcap/tidb-ansible)上下载 TiDB Ansible 3.0 [相应 TAG 版本](https://github.com/pingcap/tidb-ansible/tags)，默认的文件夹名称为 `tidb-ansible`。

{{< copyable "shell-regular" >}}

```bash
git clone -b $tag https://github.com/pingcap/tidb-ansible.git
```

> **注意：**
>
> - `$tag` 替换为选定的 TAG 版本的值，例如 `v3.0.2`。
> - 部署和升级 TiDB 集群需使用对应的 tidb-ansible 版本，通过改 `inventory.ini` 文件中的版本来混用可能会产生一些错误。
> - 请务必按文档操作，将 `tidb-ansible` 下载到 `/home/tidb` 目录下，权限为 `tidb` 用户，不要下载到 `/root` 下，否则会遇到权限问题。

## 第 4 步：在中控机器上安装 TiDB Ansible 及其依赖

以 `tidb` 用户登录中控机，请务必按以下方式通过 `pip` 安装 TiDB Ansible 及其相关依赖的指定版本，否则会有兼容问题。目前，TiDB release-2.0、release-2.1、release-3.0、release-3.1 以及最新开发版本兼容 Ansible 2.4 ~ 2.7.11 (2.4 ≤ Ansible ≤ 2.7.11)。

1. 在中控机器上安装 TiDB Ansible 及其依赖。

    {{< copyable "shell-regular" >}}

    ```bash
    cd /home/tidb/tidb-ansible && \
    sudo pip install -r ./requirements.txt
    ```

    Ansible 及相关依赖的版本信息记录在 `tidb-ansible/requirements.txt` 文件中。

2. 查看 Ansible 的版本。

    {{< copyable "shell-regular" >}}

    ```bash
    ansible --version
    ```

    ```
    ansible 2.7.11
    ```

## 第 5 步：在中控机上配置部署机器 SSH 互信及 sudo 规则

以 `tidb` 用户登录中控机，然后执行以下步骤：

1. 将你的部署目标机器 IP 添加到 `hosts.ini` 文件的 `[servers]` 区块下。

    {{< copyable "shell-regular" >}}

    ```bash
    cd /home/tidb/tidb-ansible && \
    vi hosts.ini
    ```

    ```ini
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

2. 执行以下命令，按提示输入部署目标机器的 `root` 用户密码。

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook -i hosts.ini create_users.yml -u root -k
    ```

    该步骤将在部署目标机器上创建 `tidb` 用户，并配置 sudo 规则，配置中控机与部署目标机器之间的 SSH 互信。

如果要手工配置 SSH 互信及 sudo 免密码，可参考[如何手工配置 ssh 互信及 sudo 免密码](#如何手工配置-ssh-互信及-sudo-免密码)。

## 第 6 步：在部署目标机器上安装 NTP 服务

> **注意：**
>
> 如果你的部署目标机器时间、时区设置一致，已开启 NTP 服务且在正常同步时间，此步骤可忽略。可参考[如何检测 NTP 服务是否正常](#如何检测-ntp-服务是否正常)。

以 `tidb` 用户登录中控机，执行以下命令：

{{< copyable "shell-regular" >}}

```bash
cd /home/tidb/tidb-ansible && \
ansible-playbook -i hosts.ini deploy_ntp.yml -u tidb -b
```

该步骤将在部署目标机器上使用系统自带软件源联网安装并启动 NTP 服务，服务使用安装包默认的 NTP server 列表，见配置文件 `/etc/ntp.conf` 中 server 参数。如果使用默认的 NTP server，你的机器需要连接外网。

为了让 NTP 尽快开始同步，启动 NTP 服务前，系统会执行 `ntpdate` 命令，与用户在 `hosts.ini` 文件中指定的 `ntp_server` 同步日期与时间。默认的服务器为 `pool.ntp.org`，也可替换为你的 NTP server。

## 第 7 步：在部署目标机器上配置 CPUfreq 调节器模式

为了让 CPU 发挥最大性能，请将 CPUfreq 调节器模式设置为 `performance` 模式。如需了解 CPUfreq 的更多信息，可查看[使用 CPUFREQ 调控器](https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/power_management_guide/cpufreq_governors#cpufreq_setup)文档。

### 查看系统支持的调节器模式

执行以下 `cpupower` 命令，可查看系统支持的调节器模式：

{{< copyable "shell-root" >}}

```bash
cpupower frequency-info --governors
```

```
analyzing CPU 0:
  available cpufreq governors: performance powersave
```

> **注意：**
>
> 本例中系统支持设置 `performance` 和 `powersave` 模式。如果返回 `Not Available`，表示当前系统不支持配置 CPUfreq，跳过该步骤即可。

{{< copyable "shell-root" >}}

```bash
cpupower frequency-info --governors
```

```
analyzing CPU 0:
  available cpufreq governors: Not Available
```

### 查看系统当前的 CPUfreq 调节器模式

执行以下 `cpupower` 命令，可查看系统当前的 CPUfreq 调节器模式：

{{< copyable "shell-root" >}}

```bash
cpupower frequency-info --policy
```

```
analyzing CPU 0:
  current policy: frequency should be within 1.20 GHz and 3.20 GHz.
                  The governor "powersave" may decide which speed to use
                  within this range.
```

如上述代码所示，本例中的当前配置是 `powersave` 模式。

### 修改调节器模式

你可以通过以下两种方法来修改调节器模式。本例中，当前调节器模式为 `powersave`，以下命令会将模式变更为 `performance`。

- 使用 `cpupower frequency-set --governor` 命令来修改。

    {{< copyable "shell-root" >}}

    ```bash
    cpupower frequency-set --governor performance
    ```

- 使用以下命令在部署目标机器上批量设置。

    {{< copyable "shell-regular" >}}

    ```bash
    ansible -i hosts.ini all -m shell -a "cpupower frequency-set --governor performance" -u tidb -b
    ```

## 第 8 步：在部署目标机器上添加数据盘 ext4 文件系统挂载参数

使用 `root` 用户登录目标机器，将部署目标机器数据盘格式化成 ext4 文件系统，挂载时添加 `nodelalloc` 和 `noatime` 挂载参数。`nodelalloc` 是必选参数，否则 Ansible 安装时检测无法通过；`noatime` 是可选建议参数。

> **注意：**
>
> 如果你的数据盘已经格式化成 ext4 并挂载了磁盘，可先执行 `umount /dev/nvme0n1p1` 命令卸载，从编辑 `/etc/fstab` 文件步骤开始执行，添加挂载参数重新挂载即可。

以 `/dev/nvme0n1` 数据盘为例，具体操作步骤如下：

1. 查看数据盘。

    {{< copyable "shell-root" >}}

    ```bash
    fdisk -l
    ```

    ```
    Disk /dev/nvme0n1: 1000 GB
    ```

2. 创建分区表。

    {{< copyable "shell-root" >}}

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
    ```

    > **注意：**
    >
    > 使用 `lsblk` 命令查看分区的设备号：对于 nvme 磁盘，生成的分区设备号一般为 `nvme0n1p1`；对于普通磁盘（例如 `/dev/sdb`），生成的的分区设备号一般为 `sdb1`。

3. 格式化文件系统。

    {{< copyable "shell-root" >}}

    ```bash
    mkfs.ext4 /dev/nvme0n1p1
    ```

4. 查看数据盘分区 UUID。

    本例中 `nvme0n1p1` 的 UUID 为 `c51eb23b-195c-4061-92a9-3fad812cc12f`。

    {{< copyable "shell-root" >}}

    ```bash
    lsblk -f
    ```

    ```
    NAME    FSTYPE LABEL UUID                                 MOUNTPOINT
    sda
    ├─sda1  ext4         237b634b-a565-477b-8371-6dff0c41f5ab /boot
    ├─sda2  swap         f414c5c0-f823-4bb1-8fdf-e531173a72ed
    └─sda3  ext4         547909c1-398d-4696-94c6-03e43e317b60 /
    sr0
    nvme0n1
    └─nvme0n1p1 ext4         c51eb23b-195c-4061-92a9-3fad812cc12f
    ```

5. 编辑 `/etc/fstab` 文件，添加 `nodelalloc` 挂载参数。

    {{< copyable "shell-root" >}}

    ```bash
    vi /etc/fstab
    ```

    ```
    UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2
    ```

6. 挂载数据盘。

    {{< copyable "shell-root" >}}

    ```bash
    mkdir /data1 && \
    mount -a
    ```

7. 执行以下命令，如果文件系统为 ext4，并且挂载参数中包含 `nodelalloc`，则表示已生效。

    {{< copyable "shell-root" >}}

    ```bash
    mount -t ext4
    ```

    ```
    /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
    ```

## 第 9 步：编辑 `inventory.ini` 文件，分配机器资源

以 `tidb` 用户登录中控机，编辑 `/home/tidb/tidb-ansible/inventory.ini` 文件为 TiDB 集群分配机器资源。一个标准的 TiDB 集群需要 6 台机器：2 个 TiDB 实例，3 个 PD 实例，3 个 TiKV 实例。

- 至少需部署 3 个 TiKV 实例。
- 不要将 TiKV 实例与 TiDB 或 PD 实例混合部署在同一台机器上。
- 将第一台 TiDB 机器同时用作监控机。

> **注意：**
>
> 请使用内网 IP 来部署集群，如果部署目标机器 SSH 端口非默认的 22 端口，需添加 `ansible_port` 变量，如 `TiDB1 ansible_host=172.16.10.1 ansible_port=5555`。

你可以根据实际场景从以下两种集群拓扑中选择一种：

- [单机单 TiKV 实例集群拓扑](#单机单-tikv-实例集群拓扑)

    默认情况下，建议在每个 TiKV 节点上仅部署一个 TiKV 实例，以提高性能。但是，如果你的 TiKV 部署机器的 CPU 和内存配置是[部署建议](/hardware-and-software-requirements.md)的两倍或以上，并且一个节点拥有两块 SSD 硬盘或者单块 SSD 硬盘的容量大于 2 TB，则可以考虑部署两实例，但不建议部署两个以上实例。

- [单机多 TiKV 实例集群拓扑](#单机多-tikv-实例集群拓扑)

### 单机单 TiKV 实例集群拓扑

| Name | Host IP | Services |
| :---- | :------- | :-------- |
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
| :---- | :------- | :-------- |
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

# 注意：要使用 TiKV 的 labels，必须同时配置 PD 的 location_labels 参数，否则 labels 设置不生效。
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

# 注意：为使 TiKV 的 labels 设置生效，部署集群时必须设置 PD 的 location_labels 参数。
[pd_servers:vars]
location_labels = ["host"]
```

- 服务配置文件参数调整

    1. 多实例情况下，需要修改 `tidb-ansible/conf/tikv.yml` 中 `block-cache-size` 下面的 `capacity` 参数：

        ```yaml
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

        ```yaml
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
        > 推荐配置：TiKV 实例数量 \* 参数值 = CPU 核心数量 \* 0.8

    3. 如果多个 TiKV 实例部署在同一块物理磁盘上，需要修改 `conf/tikv.yml` 中的 `capacity` 参数：

        ```yaml
        raftstore:
          capacity: 0
        ```

        > **注意：**
        >
        > 推荐配置：`capacity` = 磁盘总容量 / TiKV 实例数量，例如：`capacity: "100GB"`。

## 第 10 步：调整 `inventory.ini` 文件中的变量

本小节介绍如何编辑部署目录的变量和 `inventory.ini` 文件中的其它变量。

### 调整部署目录

部署目录通过 `deploy_dir` 变量控制，默认全局变量已设置为 `/home/tidb/deploy`，对所有服务生效。如数据盘挂载目录为 `/data1`，可设置为 `/data1/deploy`，样例如下：

```ini
## Global variables
[all:vars]
deploy_dir = /data1/deploy
```

如为某一服务单独设置部署目录，可在配置服务主机列表时配置主机变量，以 TiKV 节点为例，其他服务类推，请务必添加第一列别名，以免服务混布时混淆。

```ini
TiKV1-1 ansible_host=172.16.10.4 deploy_dir=/data1/deploy
```

### 调整其它变量（可选）

> **注意：**
>
> 以下控制变量开启请使用首字母大写 `True`，关闭请使用首字母大写 `False`。

| 变量            | 含义                                                        |
| :--------------- | :---------------------------------------------------------- |
| `cluster_name` | 集群名称，可调整 |
| `tidb_version` | TiDB 版本，TiDB Ansible 各分支默认已配置 |
| `process_supervision` | 进程监管方式，默认为 `systemd`，可选 `supervise` |
| `timezone` | 新安装 TiDB 集群第一次启动 bootstrap（初始化）时，将 TiDB 全局默认时区设置为该值。TiDB 使用的时区后续可通过 `time_zone` 全局变量和 session 变量来修改，参考[时区支持](/configure-time-zone.md)。默认为 `Asia/Shanghai`，可选值参考 [timzone 列表](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)。 |
| `enable_firewalld` | 开启防火墙，默认不开启，如需开启，请将[部署建议-网络要求](/hardware-and-software-requirements.md#网络要求) 中的端口加入白名单 |
| `enable_ntpd` | 检测部署目标机器 NTP 服务，默认为 `True`，请勿关闭 |
| `set_hostname` | 根据 IP 修改部署目标机器主机名，默认为 `False` |
| `enable_binlog` | 是否部署 Pump 并开启 binlog，默认为 `False`，依赖 Kafka 集群，参见 `zookeeper_addrs` 变量 |
| `zookeeper_addrs` | binlog Kafka 集群的 zookeeper 地址 |
| `deploy_without_tidb` | KV 模式，不部署 TiDB 服务，仅部署 PD、TiKV 及监控服务，请将 `inventory.ini` 文件中 `tidb_servers` 主机组的 IP 设置为空。|
| `alertmanager_target` | 可选：如果你已单独部署 alertmanager，可配置该变量，格式：`alertmanager_host:alertmanager_port` |
| `grafana_admin_user` | Grafana 管理员帐号用户名，默认为 admin |
| `grafana_admin_password` | Grafana 管理员帐号密码，默认为 admin，用于 Ansible 导入 Dashboard 和创建 API Key，如后期通过 grafana web 修改了密码，请更新此变量 |
| `collect_log_recent_hours` | 采集日志时，采集最近几个小时的日志，默认为 2 小时 |
| `enable_bandwidth_limit` | 在中控机上从部署目标机器拉取诊断数据时，是否限速，默认为 `True`，与 `collect_bandwidth_limit` 变量结合使用 |
| `collect_bandwidth_limit` | 在中控机上从部署目标机器拉取诊断数据时限速多少，单位: Kbit/s，默认 10000，即 10Mb/s，如果是单机多 TiKV 实例部署方式，需除以单机实例个数 |
| `prometheus_storage_retention` | Prometheus 监控数据的保留时间（默认为 30 天）；2.1.7、3.0 以及之后的 tidb-ansible 版本中，`group_vars/monitoring_servers.yml` 文件里新增的配置 |

## 第 11 步：部署 TiDB 集群

`ansible-playbook` 执行 Playbook 时，默认并发为 5。部署目标机器较多时，可添加 `-f` 参数指定并发数，例如 `ansible-playbook deploy.yml -f 10`。以下示例使用 `tidb` 用户作为服务运行用户：

1. 在 `tidb-ansible/inventory.ini` 文件中，确认 `ansible_user = tidb`。

    ```ini
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

    > **注意：**
    >
    > 不要将 `ansible_user` 设置为 `root` 用户，因为 `tidb-ansible` 限制了服务以普通用户运行。

    执行以下命令，如果所有 server 均返回 `tidb`，表示 SSH 互信配置成功：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible -i inventory.ini all -m shell -a 'whoami'
    ```

    执行以下命令，如果所有 server 均返回 `root`，表示 `tidb` 用户 sudo 免密码配置成功。

    {{< copyable "shell-regular" >}}

    ```bash
    ansible -i inventory.ini all -m shell -a 'whoami' -b
    ```

2. 执行 `local_prepare.yml` playbook，联网下载 TiDB binary 到中控机。

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook local_prepare.yml
    ```

3. 初始化系统环境，修改内核参数。

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook bootstrap.yml
    ```

4. 部署 TiDB 集群软件。

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook deploy.yml
    ```

    > **注意：**
    >
    > Grafana Dashboard 上的 **Report** 按钮可用来生成 PDF 文件，此功能依赖 `fontconfig` 包和英文字体。如需使用该功能，登录 **grafana_servers** 机器，用以下命令安装：
    >
    > {{< copyable "shell-regular" >}}
    >
    > ```bash
    > sudo yum install fontconfig open-sans-fonts
    > ```

5. 启动 TiDB 集群。

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook start.yml
    ```

## 测试集群

TiDB 兼容 MySQL，因此可使用 MySQL 客户端直接连接 TiDB。推荐配置负载均衡以提供统一的 SQL 接口。

1. 使用 MySQL 客户端连接 TiDB 集群。TiDB 服务的默认端口为 `4000`。

    {{< copyable "sql" >}}

    ```sql
    mysql -u root -h 172.16.10.1 -P 4000
    ```

2. 通过浏览器访问监控平台。

    - 地址：<http://172.16.10.1:3000>
    - 默认帐号与密码：`admin`；`admin`

## 常见部署问题

本小节介绍使用 TiDB Ansible 部署 TiDB 集群过程中的常见问题与解决方案。

### 如何自定义端口

修改 `inventory.ini` 文件，在相应服务 IP 后添加以下主机变量即可：

| 组件 | 端口变量 | 默认端口 | 说明 |
| :-- | :-- | :-- | :-- |
| TiDB | tidb_port | 4000  | 应用及 DBA 工具访问通信端口 |
| TiDB | tidb_status_port | 10080  | TiDB 状态信息上报通信端口 |
| TiKV | tikv_port | 20160 |  TiKV 通信端口  |
| TiKV | tikv_status_port   | 20180     | 上报 TiKV 状态的通信端口 |
| PD | pd_client_port | 2379 | 提供 TiDB 和 PD 通信端口 |
| PD | pd_peer_port | 2380 | PD 集群节点间通信端口 |
| Pump | pump_port | 8250  | Pump 通信端口 |
| Prometheus | prometheus_port | 9090 | Prometheus 服务通信端口 |
| Pushgateway | pushgateway_port | 9091 | TiDB， TiKV， PD 监控聚合和上报端口 |
| Node_exporter | node_exporter_port | 9100 | TiDB 集群每个节点的系统信息上报通信端口 |
| Blackbox_exporter | blackbox_exporter_port | 9115 | Blackbox_exporter 通信端口，用于 TiDB 集群端口监控 |
| Grafana | grafana_port |  3000 | Web 监控服务对外服务和客户端(浏览器)访问端口 |
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

1. 执行以下命令，如果输出 `running` 表示 NTP 服务正在运行：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl status ntpd.service
    ```

    ```
    ntpd.service - Network Time Service
    Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
    Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago
    ```

2. 执行 `ntpstat` 命令，如果输出 `synchronised to NTP server`（正在与 NTP server 同步），表示在正常同步：

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    ```
    synchronised to NTP server (85.199.214.101) at stratum 2
    time correct to within 91 ms
    polling server every 1024 s
    ```

> **注意：**
>
> Ubuntu 系统需安装 `ntpstat` 软件包。

- 以下情况表示 NTP 服务未正常同步：

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    ```
    unsynchronised
    ```

- 以下情况表示 NTP 服务未正常运行：

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    ```
    Unable to talk to NTP daemon. Is it running?
    ```

- 如果要使 NTP 服务尽快开始同步，执行以下命令。可以将 `pool.ntp.org` 替换为你的 NTP server：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl stop ntpd.service && \
    sudo ntpdate pool.ntp.org && \
    sudo systemctl start ntpd.service
    ```

- 如果要在 CentOS 7 系统上手动安装 NTP 服务，可执行以下命令：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo yum install ntp ntpdate && \
    sudo systemctl start ntpd.service && \
    sudo systemctl enable ntpd.service
    ```

### 如何调整进程监管方式从 supervise 到 systemd

{{< copyable "shell-root" >}}

```shell
process supervision, [systemd, supervise]
```

```
process_supervision = systemd
```

TiDB Anisble 在 TiDB v1.0.4 版本之前进程监管方式默认为 `supervise`。之前安装的集群可保持不变，如需更新为 `systemd`，需关闭集群，按以下方式变更：

{{< copyable "shell-regular" >}}

```bash
ansible-playbook stop.yml && \
ansible-playbook deploy.yml -D && \
ansible-playbook start.yml
```

### 如何手工配置 SSH 互信及 sudo 免密码

1. 以 `root` 用户依次登录到部署目标机器创建 `tidb` 用户并设置登录密码。

    {{< copyable "shell-root" >}}

    ```bash
    useradd tidb && \
    passwd tidb
    ```

2. 执行以下命令，将 `tidb ALL=(ALL) NOPASSWD: ALL` 添加到文件末尾，即配置好 sudo 免密码。

    {{< copyable "shell-root" >}}

    ```bash
    visudo
    ```

    ```
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

3. 以 `tidb` 用户登录到中控机，执行以下命令。将 `172.16.10.61` 替换成你的部署目标机器 IP，按提示输入部署目标机器 `tidb` 用户密码，执行成功后即创建好 SSH 互信，其他机器同理。

    {{< copyable "shell-regular" >}}

    ```bash
    ssh-copy-id -i ~/.ssh/id_rsa.pub 172.16.10.61
    ```

4. 以 `tidb` 用户登录到中控机，通过 `ssh` 的方式登录目标机器 IP。如果不需要输入密码并登录成功，即表示 SSH 互信配置成功。

    {{< copyable "shell-regular" >}}

    ```bash
    ssh 172.16.10.61
    ```

    ```
    [tidb@172.16.10.61 ~]$
    ```

5. 以 `tidb` 用户登录到部署目标机器后，执行以下命令，不需要输入密码并切换到 `root` 用户，表示 `tidb` 用户 sudo 免密码配置成功。

    {{< copyable "shell-regular" >}}

    ```bash
    sudo -su root
    ```

    ```
    [root@172.16.10.61 tidb]#
    ```

### You need to install jmespath prior to running json_query filter 报错

1. 请参照[在中控机器上安装 TiDB Ansible 及其依赖](#第-4-步在中控机器上安装-tidb-ansible-及其依赖) 在中控机上通过 `pip` 安装 TiDB Ansible 及相关依赖的指定版本，默认会安装 `jmespath`。

2. 执行以下命令，验证 `jmespath` 是否安装成功：

    {{< copyable "shell-regular" >}}

    ```bash
    pip show jmespath
    ```

    ```
    Name: jmespath
    Version: 0.9.0
    ```

3. 在中控机上 Python 交互窗口里 `import jmespath`。

    - 如果没有报错，表示依赖安装成功。
    - 如果有 `ImportError: No module named jmespath` 报错，表示未成功安装 Python `jmespath` 模块。

    {{< copyable "shell-regular" >}}

    ```bash
    python
    ```

    ```
    Python 2.7.5 (default, Nov  6 2016, 00:28:07)
    [GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    import jmespath
    ```

### 启动 Pump/Drainer 报 `zk: node does not exist` 错误

请检查 `inventory.ini` 里的 `zookeeper_addrs` 参数配置与 Kafka 集群内的配置是否相同、是否填写了命名空间。关于命名空间的配置说明如下：

```ini
# ZooKeeper connection string (see ZooKeeper docs for details).
# ZooKeeper address of Kafka cluster, example:
# zookeeper_addrs = "192.168.0.11:2181,192.168.0.12:2181,192.168.0.13:2181"
# You can also append an optional chroot string to the URLs to specify the root directory for all Kafka znodes. Example:
# zookeeper_addrs = "192.168.0.11:2181,192.168.0.12:2181,192.168.0.13:2181/kafka/123"
```
