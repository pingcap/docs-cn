---
title: TiDB 环境与系统配置检查
summary: 了解部署 TiDB 前的环境检查操作。
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

   - 若返回 `Unit ntpd.service could not be found.` 的报错信息，请尝试运行以下命令，查看你是否使用 `chronyd` 而不是 `ntpd` 的系统配置来与 NTP 的时钟同步：

        {{< copyable "shell-regular" >}}

        ```bash
        sudo systemctl status cronyd.service
        ```

        ```
        chronyd.service - NTP client/server
        Loaded: loaded (/usr/lib/systemd/system/chronyd.service; enabled; vendor preset: enabled)
        Active: active (running) since Mon 2021-04-05 09:55:29 EDT; 3 days ago
        ```

        如果你使用 `chronyd` 的系统配置，请继续执行步骤 3。

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

3. 运行 `chronyc tracking` 命令查看 Chrony 服务是否与 NTP 服务器同步。

    > **注意：**
    >
    > 该操作仅适用于使用 Chrony 而不是 ntpd 的系统。

    {{< copyable "shell-regular" >}}

    ```bash
    chronyc tracking
    ```

    - 如果该命令返回结果为 `Leap status : Normal`，则代表同步过程正常。

        ```
        Reference ID    : 5EC69F0A (ntp1.time.nl)
        Stratum         : 2
        Ref time (UTC)  : Thu May 20 15:19:08 2021
        System time     : 0.000022151 seconds slow of NTP time
        Last offset     : -0.000041040 seconds
        RMS offset      : 0.000053422 seconds
        Frequency       : 2.286 ppm slow
        Residual freq   : -0.000 ppm
        Skew            : 0.012 ppm
        Root delay      : 0.012706812 seconds
        Root dispersion : 0.000430042 seconds
        Update interval : 1029.8 seconds
        Leap status     : Normal
        ```

    - 如果该命令返回结果如下，则表示同步过程出错：

        ```
        Leap status    : Not synchronised
        ```

    - 如果该命令返回结果如下，则表示 `chronyd` 服务未正常运行：

        ```
        506 Cannot talk to daemon
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

## 检查和配置操作系统优化参数

在生产系统的 TiDB 中，建议对操作系统进行如下的配置优化：

1. 关闭透明大页（即 Transparent Huge Pages，缩写为 THP）。数据库的内存访问模式往往是稀疏的而非连续的。当高阶内存碎片化比较严重时，分配 THP 页面会出现较高的延迟。
2. 将存储介质的 I/O 调度器设置为 noop。对于高速 SSD 存储介质，内核的 I/O 调度操作会导致性能损失。将调度器设置为 noop 后，内核不做任何操作，直接将 I/O 请求下发给硬件，以获取更好的性能。同时，noop 调度器也有较好的普适性。
3. 为调整 CPU 频率的 cpufreq 模块选用 performance 模式。将 CPU 频率固定在其支持的最高运行频率上，不进行动态调节，可获取最佳的性能。

采用如下步骤检查操作系统的当前配置，并配置系统优化参数：

1. 执行以下命令查看透明大页的开启状态。

    {{< copyable "shell-regular" >}}

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    [always] madvise never
    ```

    > **注意：**
    >
    > `[always] madvise never` 表示透明大页处于启用状态，需要关闭。

2. 执行以下命令查看数据目录所在磁盘的 I/O 调度器。假设在 sdb、sdc 两个磁盘上创建了数据目录。

    {{< copyable "shell-regular" >}}

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

    ```
    noop [deadline] cfq
    noop [deadline] cfq
    ```

    > **注意：**
    >
    > `noop [deadline] cfq` 表示磁盘的 I/O 调度器使用 `deadline`，需要进行修改。

3. 执行以下命令查看磁盘的唯一标识 `ID_SERIAL`。

    {{< copyable "shell-regular" >}}

    ```bash
    udevadm info --name=/dev/sdb | grep ID_SERIAL
    ```

    ```
    E: ID_SERIAL=36d0946606d79f90025f3e09a0c1f9e81
    E: ID_SERIAL_SHORT=6d0946606d79f90025f3e09a0c1f9e81
    ```

    > **注意：**
    >
    > 如果多个磁盘都分配了数据目录，需要多次执行以上命令，记录所有磁盘各自的唯一标识。

4. 执行以下命令查看 cpufreq 模块选用的节能策略。

    {{< copyable "shell-regular" >}}

    ```bash
    cpupower frequency-info --policy
    ```

    ```
    analyzing CPU 0:
    current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                  The governor "powersave" may decide which speed to use within this range.
    ```

    > **注意：**
    >
    > `The governor "powersave"` 表示 cpufreq 的节能策略使用 powersave，需要调整为 performance 策略。如果是虚拟机或者云主机，则不需要调整，命令输出通常为 `Unable to determine current policy`。

5. 配置系统优化参数。

    + 方法一：使用 tuned（推荐）

        1. 执行 `tuned-adm list` 命令查看当前操作系统的 tuned 策略。

            {{< copyable "shell-regular" >}}

            ```bash
            tuned-adm list
            ```

            ```
            Available profiles:
            - balanced                    - General non-specialized tuned profile
            - desktop                     - Optimize for the desktop use-case
            - hpc-compute                 - Optimize for HPC compute workloads
            - latency-performance         - Optimize for deterministic performance at the cost of increased power consumption
            - network-latency             - Optimize for deterministic performance at the cost of increased power consumption, focused on low latency network performance
            - network-throughput          - Optimize for streaming network throughput, generally only necessary on older CPUs or 40G+ networks
            - powersave                   - Optimize for low power consumption
            - throughput-performance      - Broadly applicable tuning that provides excellent performance across a variety of common server workloads
            - virtual-guest               - Optimize for running inside a virtual guest
            - virtual-host                - Optimize for running KVM guests
            Current active profile: balanced
            ```

            `Current active profile: balanced` 表示当前操作系统的 tuned 策略使用 balanced，建议在当前策略的基础上添加操作系统优化配置。

        2. 创建新的 tuned 策略。

            {{< copyable "shell-regular" >}}

            ```bash
            mkdir /etc/tuned/balanced-tidb-optimal/
            vi /etc/tuned/balanced-tidb-optimal/tuned.conf
            ```

            ```
            [main]
            include=balanced

            [cpu]
            governor=performance

            [vm]
            transparent_hugepages=never

            [disk]
            devices_udev_regex=(ID_SERIAL=36d0946606d79f90025f3e09a0c1fc035)|(ID_SERIAL=36d0946606d79f90025f3e09a0c1f9e81)
            elevator=noop
            ```

            `include=balanced` 表示在现有的 balanced 策略基础上添加操作系统优化配置。

        3. 应用新的 tuned 策略。

            {{< copyable "shell-regular" >}}

            ```bash
            tuned-adm profile balanced-tidb-optimal
            ```

    + 方法二：使用脚本方式。如果已经使用 tuned 方法，请跳过本方法。

        1. 执行 `grubby` 命令查看默认内核版本。

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

        2. 执行 `grubby --update-kernel` 命令修改内核配置。

            {{< copyable "shell-regular" >}}

            ```bash
            grubby --args="transparent_hugepage=never" --update-kernel /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

            > **注意：**
            >
            > `--update-kernel` 后需要使用实际的默认内核版本。

        3. 执行 `grubby --info` 命令查看修改后的默认内核配置。

            {{< copyable "shell-regular" >}}

            ```bash
            grubby --info /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

            > **注意：**
            >
            > `--info` 后需要使用实际的默认内核版本。

            ```
            index=0
            kernel=/boot/vmlinuz-3.10.0-957.el7.x86_64
            args="ro crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet LANG=en_US.UTF-8 transparent_hugepage=never"
            root=/dev/mapper/centos-root
            initrd=/boot/initramfs-3.10.0-957.el7.x86_64.img
            title=CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)
            ```

        4. 修改当前的内核配置立即关闭透明大页。

            {{< copyable "shell-regular" >}}

            ```bash
            echo never > /sys/kernel/mm/transparent_hugepage/enabled
            echo never > /sys/kernel/mm/transparent_hugepage/defrag
            ```

        5. 配置 udev 脚本应用 IO 调度器策略。

            {{< copyable "shell-regular" >}}

            ```bash
            vi /etc/udev/rules.d/60-tidb-schedulers.rules
            ```

            ```
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1fc035", ATTR{queue/scheduler}="noop"
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1f9e81", ATTR{queue/scheduler}="noop"

            ```

        6. 应用 udev 脚本。

            {{< copyable "shell-regular" >}}

            ```bash
            udevadm control --reload-rules
            udevadm trigger --type=devices --action=change
            ```

        7. 创建 CPU 节能策略配置服务。

            {{< copyable "shell-regular" >}}

            ```bash
            cat  >> /etc/systemd/system/cpupower.service << EOF
            [Unit]
            Description=CPU performance
            [Service]
            Type=oneshot
            ExecStart=/usr/bin/cpupower frequency-set --governor performance
            [Install]
            WantedBy=multi-user.target
            EOF
            ```

        8. 应用 CPU 节能策略配置服务。

            {{< copyable "shell-regular" >}}

            ```bash
            systemctl daemon-reload
            systemctl enable cpupower.service
            systemctl start cpupower.service
            ```

6. 执行以下命令验证透明大页的状态。

    {{< copyable "shell-regular" >}}

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    always madvise [never]
    ```

7. 执行以下命令验证数据目录所在磁盘的 I/O 调度器。

    {{< copyable "shell-regular" >}}

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

    ```
    [noop] deadline cfq
    [noop] deadline cfq
    ```

8. 执行以下命令查看 cpufreq 模块选用的节能策略。

    {{< copyable "shell-regular" >}}

    ```bash
    cpupower frequency-info --policy
    ```

    ```
    analyzing CPU 0:
    current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                  The governor "performance" may decide which speed to use within this range.
    ```

9. 执行以下命令修改 sysctl 参数。

    {{< copyable "shell-regular" >}}

    ```bash
    echo "fs.file-max = 1000000">> /etc/sysctl.conf
    echo "net.core.somaxconn = 32768">> /etc/sysctl.conf
    echo "net.ipv4.tcp_tw_recycle = 0">> /etc/sysctl.conf
    echo "net.ipv4.tcp_syncookies = 0">> /etc/sysctl.conf
    echo "vm.overcommit_memory = 1">> /etc/sysctl.conf
    sysctl -p
    ```

10. 执行以下命令配置用户的 limits.conf 文件。

    {{< copyable "shell-regular" >}}

    ```bash
    cat << EOF >>/etc/security/limits.conf
    tidb           soft    nofile          1000000
    tidb           hard    nofile          1000000
    tidb           soft    stack          32768
    tidb           hard    stack          32768
    EOF
    ```

## 手动配置 SSH 互信及 sudo 免密码

对于有需求，通过手动配置中控机至目标节点互信的场景，可参考本段。通常推荐使用 TiUP 部署工具会自动配置 SSH 互信及免密登录，可忽略本段内容。

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

3. 以 `tidb` 用户登录到中控机，执行以下命令。将 `10.0.1.1` 替换成你的部署目标机器 IP，按提示输入部署目标机器 `tidb` 用户密码，执行成功后即创建好 SSH 互信，其他机器同理。新建的 `tidb` 用户下没有 `.ssh` 目录，需要执行生成 rsa 密钥的命令来生成 `.ssh` 目录。如果要在中控机上部署 TiDB 组件，需要为中控机和中控机自身配置互信。

    {{< copyable "shell-regular" >}}

    ```bash
    ssh-keygen -t rsa
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
