---
title: TiDB 环境与系统配置检查
summary: 了解部署 TiDB 前的环境检查操作。
aliases: ['/docs-cn/dev/check-before-deployment/']
---

# TiDB 环境与系统配置检查

本文介绍部署 TiDB 前的环境检查操作，以下各项操作按优先级排序。

## 在 TiKV 部署目标机器上添加数据盘 EXT4 文件系统挂载参数

生产环境部署，建议使用 EXT4 类型文件系统的 NVME 类型的 SSD 磁盘存储 TiKV 数据文件。这个配置方案为最佳实施方案，其可靠性、安全性、稳定性已经在大量线上场景中得到证实。

使用 `root` 用户登录目标机器，将部署目标机器数据盘格式化成 ext4 文件系统，挂载时添加 `nodelalloc` 和 `noatime` 挂载参数。`nodelalloc` 是必选参数，否则 TiUP 安装时检测无法通过；`noatime` 是可选建议参数。

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

2. 创建分区。

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

## 检测及关闭系统 swap

本段介绍 swap 关闭方法。TiDB 运行需要有足够的内存，并且不建议使用 swap 作为内存不足的缓冲，这会降低性能。因此建议永久关闭系统 swap，并且不要使用 `swapoff -a` 方式关闭，否则重启机器后该操作会失效。

建议执行以下命令关闭系统 swap：

{{< copyable "shell-regular" >}}

```bash
echo "vm.swappiness = 0">> /etc/sysctl.conf 
swapoff -a && swapon -a
sysctl -p
```

## 检测及关闭目标部署机器的防火墙

本段介绍如何关闭目标主机防火墙配置，因为在 TiDB 集群中，需要将节点间的访问端口打通才可以保证读写请求、数据心跳等信息的正常的传输。在普遍线上场景中，数据库到业务服务和数据库节点的网络联通都是在安全域内完成数据交互。如果没有特殊安全的要求，建议将目标节点的防火墙进行关闭。否则建议[按照端口使用规则](/hardware-and-software-requirements.md#网络要求)，将端口信息配置到防火墙服务的白名单中。

1. 检查防火墙状态（以 CentOS Linux release 7.7.1908 (Core) 为例）

    {{< copyable "shell-regular" >}}

    ```shell
    sudo firewall-cmd --state
    sudo systemctl status firewalld.service
    ```

2. 关闭防火墙服务

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl stop firewalld.service
    ```

3. 关闭防火墙自动启动服务

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl disable firewalld.service
    ```

4. 检查防火墙状态

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl status firewalld.service
    ```

## 检测及安装 NTP 服务

TiDB 是一套分布式数据库系统，需要节点间保证时间的同步，从而确保 ACID 模型的事务线性一致性。目前解决授时的普遍方案是采用 NTP 服务，可以通过互联网中的 `pool.ntp.org` 授时服务来保证节点的时间同步，也可以使用离线环境自己搭建的 NTP 服务来解决授时。

采用如下步骤检查是否安装 NTP 服务以及与 NTP 服务器正常同步：

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

2. 执行 `ntpstat` 命令检测是否与 NTP 服务器同步：

    > **注意：**
    >
    > Ubuntu 系统需安装 `ntpstat` 软件包。

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    - 如果输出 `synchronised to NTP server`，表示正在与 NTP 服务器正常同步：

        ```
        synchronised to NTP server (85.199.214.101) at stratum 2
        time correct to within 91 ms
        polling server every 1024 s
        ```

    - 以下情况表示 NTP 服务未正常同步：

        ```
        unsynchronised
        ```

    - 以下情况表示 NTP 服务未正常运行：

        ```
        Unable to talk to NTP daemon. Is it running?
        ```

如果要使 NTP 服务尽快开始同步，执行以下命令。可以将 `pool.ntp.org` 替换为你的 NTP 服务器：

{{< copyable "shell-regular" >}}

```bash
sudo systemctl stop ntpd.service && \
sudo ntpdate pool.ntp.org && \
sudo systemctl start ntpd.service
```

如果要在 CentOS 7 系统上手动安装 NTP 服务，可执行以下命令：

{{< copyable "shell-regular" >}}

```bash
sudo yum install ntp ntpdate && \
sudo systemctl start ntpd.service && \
sudo systemctl enable ntpd.service
```

## 检测和关闭透明大页

对于数据库应用，不推荐使用透明大页（即 Transparent Huge Pages，缩写为 THP），因为数据库的内存访问模式往往是稀疏的而非连续的。而且当高阶内存碎片化比较严重时，分配 THP 页面会出现较大的延迟。若开启针对 THP 的直接内存规整功能，也会出现系统 CPU 使用率激增的现象，因此建议关闭透明大页。

采用如下步骤检查是否已经关闭透明大页，并进行关闭：

1. 执行以下命令查看透明大页的开启状态。如果返回 `[always] madvise never` 则表示处于启用状态：

    {{< copyable "shell-regular" >}}

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    [always] madvise never
    ```

2. 执行 `grubby` 命令查看默认内核版本：

    > **注意：**
    >
    > 需安装 `grubby` 软件包。

    {{< copyable "shell-regular" >}}

    ```bash
    grubby --default-kernel
    ```

    ```bash
    /boot/vmlinuz-3.10.0-957.el7.x86_64
    ```

3. 执行 `grubby --update-kernel` 命令修改内核配置：

    {{< copyable "shell-regular" >}}

    ```bash
    grubby --args="transparent_hugepage=never" --update-kernel /boot/vmlinuz-3.10.0-957.el7.x86_64
    ```

    > **注意：**
    >
    > `--update-kernel` 后需要使用实际的默认内核版本。

4. 执行 `grubby --info` 命令查看修改后的默认内核配置：

    {{< copyable "shell-regular" >}}

    ```bash
    grubby --info /boot/vmlinuz-3.10.0-957.el7.x86_64
    ```

    > **注意：**
    >
    > `--info` 后需要使用实际的默认内核版本。

    ```bash
    index=0
    kernel=/boot/vmlinuz-3.10.0-957.el7.x86_64
    args="ro crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet LANG=en_US.UTF-8 transparent_hugepage=never"
    root=/dev/mapper/centos-root
    initrd=/boot/initramfs-3.10.0-957.el7.x86_64.img
    title=CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)
    ```

5. 执行 `reboot` 命令进行重启或者修改当前的内核配置：

    - 如果需要重启验证，执行 `reboot` 命令：

        {{< copyable "shell-regular" >}}

        ```bash
        reboot
        ```

    - 如果不希望重启机器，也可以修改当前的内核配置来立即生效：

        {{< copyable "shell-regular" >}}

        ```bash
        echo never > /sys/kernel/mm/transparent_hugepage/enabled
        echo never > /sys/kernel/mm/transparent_hugepage/defrag
        ```

6. 查看重启或者修改后已生效的默认内核配置。如果输出 `always madvise [never]` 表示透明大页处于禁用状态。

    {{< copyable "shell-regular" >}}

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```bash
    always madvise [never]
    ```

7. 如果透明大页禁用未生效，需要使用 tuned 或 ktune 动态内核调试工具修改透明大页的配置。操作步骤如下：

    1. 启用 tuned 工具：

        {{< copyable "shell-regular" >}}

        ```bash
        tuned-adm active
        ```

        ```bash
        Current active profile: virtual-guest
        ```

    2. 创建一个新的定制 profile：

        {{< copyable "shell-regular" >}}

        ```bash
        mkdir /etc/tuned/virtual-guest-no-thp
        vi /etc/tuned/virtual-guest-no-thp/tuned.conf
        ```

        ```bash
        [main]
        include=virtual-guest

        [vm]
        transparent_hugepages=never
        ```

    3. 应用新的定制 profile：

        {{< copyable "shell-regular" >}}

        ```bash
        tuned-adm profile virtual-guest-no-thp
        ```

    应用后再重新检查透明大页的状态。

## 手动配置 SSH 互信及 sudo 免密码

对于有需求，通过手动配置中控机至目标节点互信的场景，可参考本段。通常推荐使用 TiUP 部署工具会自动配置 SSH 互信及免密登陆，可忽略本段内容。

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

3. 以 `tidb` 用户登录到中控机，执行以下命令。将 `10.0.1.1` 替换成你的部署目标机器 IP，按提示输入部署目标机器 `tidb` 用户密码，执行成功后即创建好 SSH 互信，其他机器同理。

    {{< copyable "shell-regular" >}}

    ```bash
    ssh-copy-id -i ~/.ssh/id_rsa.pub 10.0.1.1
    ```

4. 以 `tidb` 用户登录中控机，通过 `ssh` 的方式登录目标机器 IP。如果不需要输入密码并登录成功，即表示 SSH 互信配置成功。

    {{< copyable "shell-regular" >}}

    ```bash
    ssh 10.0.1.1
    ```

    ```
    [tidb@10.0.1.1 ~]$
    ```

5. 以 `tidb` 用户登录到部署目标机器后，执行以下命令，不需要输入密码并切换到 `root` 用户，表示 `tidb` 用户 sudo 免密码配置成功。

    {{< copyable "shell-regular" >}}

    ```bash
    sudo -su root
    ```

    ```
    [root@10.0.1.1 tidb]#
    ```

## 安装 numactl 工具

本段主要介绍如果安装 NUMA 工具。在生产环境中，因为硬件机器配置往往高于需求，为了更合理规划资源，会考虑单机多实例部署 TiDB 或者 TiKV。NUMA 绑核工具的使用，主要为了防止 CPU 资源的争抢，引发性能衰退。

> **注意：**
>
> - NUMA 绑核是用来隔离 CPU 资源的一种方法，适合高配置物理机环境部署多实例使用。
> - 通过 `tiup cluster deploy` 完成部署操作，就可以通过 `exec` 命令来进行集群级别管理工作。

1. 登录到目标节点进行安装（以 CentOS Linux release 7.7.1908 (Core) 为例）

    {{< copyable "shell-regular" >}}

    ```bash
    sudo yum -y install numactl
    ```

2. 通过 TiUP 的 cluster 执行完 exec 命令来完成批量安装

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster exec --help
    ```

    ```
    Run shell command on host in the tidb cluster

    Usage:
    cluster exec <cluster-name> [flags]

    Flags:
        --command string   the command run on cluster host (default "ls")
    -h, --help             help for exec
        --sudo             use root permissions (default false)
    ```

    将 tidb-test 集群所有目标主机通过 sudo 权限执行安装命令

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster exec tidb-test --sudo --command "yum -y install numactl"
    ```
