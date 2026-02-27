---
title: TiDB 环境与系统配置检查
summary: 了解部署 TiDB 前的环境检查操作。
aliases: ['/docs-cn/dev/check-before-deployment/']
---

# TiDB 环境与系统配置检查

本文介绍部署 TiDB 前的环境检查操作，以下各项操作按优先级排序。

## 在 TiKV 部署目标机器上添加数据盘 EXT4 文件系统挂载参数

生产环境部署，建议使用 EXT4 类型文件系统的 NVMe 类型的 SSD 磁盘存储 TiKV 数据文件。这个配置方案为最佳实施方案，其可靠性、安全性、稳定性已经在大量线上场景中得到证实。

使用 `root` 用户登录目标机器，将部署目标机器数据盘格式化成 ext4 文件系统，挂载时添加 `nodelalloc` 和 `noatime` 挂载参数。`nodelalloc` 是必选参数，否则 TiUP 安装时检测无法通过；`noatime` 是可选建议参数。

> **注意：**
>
> 如果你的数据盘已经格式化成 ext4 并挂载了磁盘，可先执行 `umount /dev/nvme0n1p1` 命令卸载，从编辑 `/etc/fstab` 文件步骤开始执行，添加挂载参数重新挂载即可。

以 `/dev/nvme0n1` 数据盘为例，具体操作步骤如下：

1. 查看数据盘。

    ```bash
    fdisk -l
    ```

    ```
    Disk /dev/nvme0n1: 1000 GB
    ```

2. 创建分区。

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
    ```

    如果 NVMe 设备容量较大，可以创建多个分区。

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 2000GB
    parted -s -a optimal /dev/nvme0n1 -- mkpart primary ext4 2000GB -1
    ```

    > **注意：**
    >
    > 使用 `lsblk` 命令查看分区的设备号：对于 NVMe 磁盘，生成的分区设备号一般为 `nvme0n1p1`；对于普通磁盘（例如 `/dev/sdb`），生成的分区设备号一般为 `sdb1`。

3. 格式化文件系统。

    ```bash
    mkfs.ext4 /dev/nvme0n1p1
    ```

4. 查看数据盘分区 UUID。

    本例中 `nvme0n1p1` 的 UUID 为 `c51eb23b-195c-4061-92a9-3fad812cc12f`。

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

    ```bash
    vi /etc/fstab
    ```

    ```
    UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2
    ```

6. 挂载数据盘。

    ```bash
    mkdir /data1 && \
    systemctl daemon-reload && \
    mount -a
    ```

7. 执行以下命令，如果文件系统为 ext4，并且挂载参数中包含 `nodelalloc`，则表示已生效。

    ```bash
    mount -t ext4
    ```

    ```
    /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
    ```

## 检测及关闭系统 swap

TiDB 需要充足的内存来运行。如果 TiDB 使用的内存被换出 (swapped out) 然后再换入 (swapped back in)，这可能会导致延迟激增。如果您想保持稳定的性能，建议永久禁用系统 swap，但可能在内存偏小时触发 OOM 问题。如果想避免此类 OOM 问题，则可只将 swap 优先级调低，但不做永久关闭。

- 开启并使用 swap 可能会引入性能抖动问题，对于低延迟、稳定性要求高的数据库服务，建议永久关闭操作系统层 swap。要永久关闭 swap，可使用以下方法：

    - 在操作系统初始化阶段，不单独划分 swap 分区盘。
    - 如果在操作系统初始化阶段，已经单独划分了 swap 分区盘，并且启用了 swap，则使用以下命令进行关闭：

        ```bash
        echo "vm.swappiness = 0">> /etc/sysctl.conf
        sysctl -p
        swapoff -a && swapon -a
        ```

- 如果主机内存偏小，关闭系统 swap 可能会更容易触发 OOM 问题，可参考以如下方法将 swap 优先级调低，但不做永久关闭：

    ```bash
    echo "vm.swappiness = 0">> /etc/sysctl.conf
    sysctl -p
    ```

## 设置 TiDB 节点的临时空间（推荐）

TiDB 的部分操作需要向服务器写入临时文件，因此需要确保运行 TiDB 的操作系统用户具有足够的权限对目标目录进行读写。如果 TiDB 实例不是以 `root` 权限启动，则需要检查目录权限并进行正确设置。

- TiDB 临时工作区

    哈希表构建、排序等内存消耗较大的操作可能会向磁盘写入临时数据，用来减少内存消耗，提升稳定性。写入的磁盘位置由配置项 [`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path) 定义。在默认设置下，确保运行 TiDB 的用户对操作系统临时文件夹（通常为 `/tmp`）有读写权限。

- Fast Online DDL 工作区

    当变量 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 被设置为 `ON`（v6.5.0 及以上版本中默认值为 `ON`）时，会激活 Fast Online DDL，这时部分 DDL 要对临时文件进行读写。临时文件位置由配置 [`temp-dir`](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入) 定义，需要确保运行 TiDB 的用户对操作系统中该目录有读写权限。默认目录 `/tmp/tidb` 使用 tmpfs (temporary file system)，建议显式指定为磁盘上的目录，以 `/data/tidb-deploy/tempdir` 为例：

    > **注意：**
    >
    > 如果业务中可能存在针对大对象的 DDL 操作，推荐为 [`temp-dir`](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入) 配置独立文件系统及更大的临时空间。

    ```shell
    sudo mkdir -p /data/tidb-deploy/tempdir
    ```

    如果目录 `/data/tidb-deploy/tempdir` 已经存在，需确保有写入权限。

    ```shell
    sudo chmod -R 777 /data/tidb-deploy/tempdir
    ```

    > **注意：**
    >
    > 如果目录不存在，TiDB 在启动时会自动创建该目录。如果目录创建失败，或者 TiDB 对该目录没有读写权限，[Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 在运行时会被禁用。

## 检测目标部署机器的防火墙

在 TiDB 集群中，必须将节点间的访问端口打通才可以保证读写请求、数据心跳等信息的正常的传输。在普遍线上场景中，数据库到业务服务和数据库节点的网络联通都是在安全域内完成数据交互。如果没有特殊安全的要求，建议将目标节点的防火墙进行关闭。如不关闭防火墙，建议[按照端口使用规则](/hardware-and-software-requirements.md#网络要求)，将端口信息配置到防火墙服务的白名单中。

### 停止并禁用防火墙

本节介绍如何停止并禁用目标部署机器的防火墙服务。

1. 检查防火墙状态（以 CentOS Linux release 7.7.1908 (Core) 为例）

    ```shell
    sudo firewall-cmd --state
    sudo systemctl status firewalld.service
    ```

2. 停止防火墙服务

    ```bash
    sudo systemctl stop firewalld.service
    ```

3. 禁用防火墙自动启动服务

    ```bash
    sudo systemctl disable firewalld.service
    ```

4. 检查防火墙状态

    ```bash
    sudo systemctl status firewalld.service
    ```

### 更改防火墙区域

如果不希望完全禁用防火墙，可以使用限制较少的区域。默认的 `public` 区域仅允许特定的服务和端口，而 `trusted` 区域默认允许所有流量。

将默认区域设置为 `trusted`：

```bash
firewall-cmd --set-default-zone trusted
```

查看默认区域：

```bash
firewall-cmd --get-default-zone
# trusted
```

列出某个区域的策略：

```bash
firewall-cmd --zone=trusted --list-all
# trusted
#   target: ACCEPT
#   icmp-block-inversion: no
#   interfaces:
#   sources:
#   services:
#   ports:
#   protocols:
#   forward: yes
#   masquerade: no
#   forward-ports:
#   source-ports:
#   icmp-blocks:
#   rich rules:
```

### 配置防火墙

使用以下命令为 TiDB 集群组件配置防火墙。这些示例仅供参考，请根据实际环境调整区域名称、端口和服务。

为 TiDB 组件配置防火墙：

```bash
firewall-cmd --permanent --new-service tidb
firewall-cmd --permanent --service tidb --set-description="TiDB Server"
firewall-cmd --permanent --service tidb --set-short="TiDB"
firewall-cmd --permanent --service tidb --add-port=4000/tcp
firewall-cmd --permanent --service tidb --add-port=10080/tcp
firewall-cmd --permanent --zone=public --add-service=tidb
```

为 TiKV 组件配置防火墙：

```bash
firewall-cmd --permanent --new-service tikv
firewall-cmd --permanent --service tikv --set-description="TiKV Server"
firewall-cmd --permanent --service tikv --set-short="TiKV"
firewall-cmd --permanent --service tikv --add-port=20160/tcp
firewall-cmd --permanent --service tikv --add-port=20180/tcp
firewall-cmd --permanent --zone=public --add-service=tikv
```

为 PD 组件配置防火墙：

```bash
firewall-cmd --permanent --new-service pd
firewall-cmd --permanent --service pd --set-description="PD Server"
firewall-cmd --permanent --service pd --set-short="PD"
firewall-cmd --permanent --service pd --add-port=2379/tcp
firewall-cmd --permanent --service pd --add-port=2380/tcp
firewall-cmd --permanent --zone=public --add-service=pd
```

为 Prometheus 配置防火墙：

```bash
firewall-cmd --permanent --zone=public --add-service=prometheus
firewall-cmd --permanent --service=prometheus --add-port=12020/tcp
```

为 Grafana 配置防火墙：

```bash
firewall-cmd --permanent --zone=public --add-service=grafana
```

## 检测及安装 NTP 服务

TiDB 是一套分布式数据库系统，需要节点间保证时间的同步，从而确保 ACID 模型的事务线性一致性。目前解决授时的普遍方案是采用 NTP 服务，可以通过互联网中的 `pool.ntp.org` 授时服务来保证节点的时间同步，也可以使用离线环境自己搭建的 NTP 服务来解决授时。

采用如下步骤检查是否安装 NTP 服务以及与 NTP 服务器正常同步：

1. 执行以下命令，如果输出 `running` 表示 NTP 服务正在运行：

    ```bash
    sudo systemctl status ntpd.service
    ```

    ```
    ntpd.service - Network Time Service
    Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
    Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago
    ```

    - 若返回报错信息 `Unit ntpd.service could not be found.`，请尝试执行以下命令，以查看与 NTP 进行时钟同步所使用的系统配置是 `chronyd` 还是 `ntpd`：

        ```bash
        sudo systemctl status chronyd.service
        ```

        ```
        chronyd.service - NTP client/server
        Loaded: loaded (/usr/lib/systemd/system/chronyd.service; enabled; vendor preset: enabled)
        Active: active (running) since Mon 2021-04-05 09:55:29 EDT; 3 days ago
        ```

      若发现系统既没有配置 `chronyd` 也没有配置 `ntpd`，则表示系统尚未安装任一服务。此时，应先安装其中一个服务，并保证它可以自动启动，默认使用 `ntpd`。

        如果你使用的系统配置是 `chronyd`，请直接执行步骤 3。

2. 执行 `ntpstat` 命令检测是否与 NTP 服务器同步：

    > **注意：**
    >
    > Ubuntu 系统需安装 `ntpstat` 软件包。

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

3. 执行 `chronyc tracking` 命令查看 Chrony 服务是否与 NTP 服务器同步。

    > **注意：**
    >
    > 该操作仅适用于使用 Chrony 的系统，不适用于使用 NTPd 的系统。

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

    - 如果该命令返回结果如下，则表示 Chrony 服务未正常运行：

        ```
        506 Cannot talk to daemon
        ```

如果要使 NTP 服务尽快开始同步，执行以下命令。可以将 `pool.ntp.org` 替换为你的 NTP 服务器：

```bash
sudo systemctl stop ntpd.service && \
sudo ntpdate pool.ntp.org && \
sudo systemctl start ntpd.service
```

如果要在 CentOS 7 系统上手动安装 NTP 服务，可执行以下命令：

```bash
sudo yum install ntp ntpdate && \
sudo systemctl start ntpd.service && \
sudo systemctl enable ntpd.service
```

## 检查和配置操作系统优化参数

在生产系统的 TiDB 中，建议对操作系统进行如下的配置优化：

- 关闭[内存——透明大页](/tune-operating-system.md#内存透明大页) (Transparent Huge Pages, THP)。数据库的内存访问通常较为稀疏，当高阶内存出现明显碎片化时，THP 分配可能导致较高的内存分配延迟，因此建议关闭 THP 以避免性能抖动。
- 设置存储介质的 [I/O 调度器](/tune-operating-system.md#io-调度器)。

    - 对于高速 SSD 存储介质，内核默认的 I/O 调度器可能会导致性能损失。建议将闪存存储的 I/O 调度器设置为先入先出 (First-in-first-out, FIFO) 的调度器，如 `noop` 或 `none`，这样内核将不做调度操作，直接将 I/O 请求传递给硬件，从而提升性能。
    - 对于 NVMe 存储介质，默认的 I/O 调度器为 `none`，无需进行调整。

- 将动态调整 CPU 频率的 [cpufreq 模块](/tune-operating-system.md#处理器动态节能技术)设置为 `performance` 模式。该模式会将 CPU 频率固定在其支持的最高运行频率上，不进行动态调节，因此可获得最佳性能。

具体的检查和配置步骤如下：

1. 执行以下命令查看透明大页的开启状态。

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    [always] madvise never
    ```

    > **注意：**
    >
    > `[always] madvise never` 表示透明大页处于启用状态，需要关闭。

2. 执行以下命令查看数据目录所在磁盘的 I/O 调度器。

    如果数据目录所在磁盘使用的是 SD 或 VD 设备，可以执行以下命令查看当前 I/O 调度器的配置：

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

    如果数据目录使用 NVMe 设备，可以执行以下命令查看 I/O 调度器：

    ```bash
    cat /sys/block/nvme[01]*/queue/scheduler
    ```

    ```
    [none] mq-deadline kyber bfq
    [none] mq-deadline kyber bfq
    ```

    > **注意：**
    >
    > `[none] mq-deadline kyber bfq` 表示 NVMe 设备的 I/O 调度器使用 `none`，不需要进行修改。

3. 执行以下命令查看磁盘的唯一标识 `ID_SERIAL`。

    ```bash
    udevadm info --name=/dev/sdb | grep ID_SERIAL
    ```

    ```
    E: ID_SERIAL=36d0946606d79f90025f3e09a0c1f9e81
    E: ID_SERIAL_SHORT=6d0946606d79f90025f3e09a0c1f9e81
    ```

    > **注意：**
    >
    > - 如果多个磁盘都分配了数据目录，需要为每个磁盘都执行以上命令，记录所有磁盘各自的唯一标识。
    > - 已经使用 `noop` 或者 `none` 调度器的设备不需要记录标识，无需配置 udev 规则和 tuned 策略中的相关内容。

4. 执行以下命令查看 cpufreq 模块选用的节能策略。

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

5. 配置系统优化参数

    + 方法一：使用 tuned（推荐）

        1. 执行 `tuned-adm list` 命令查看当前操作系统的 tuned 策略。

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

            > **注意：**
            >
            > 如果已经使用 `noop` 或 `none` I/O 调度器，则无需在 tuned 策略中配置调度器相关的内容，可以跳过此步骤。

            ```bash
            tuned-adm profile balanced-tidb-optimal
            ```

    + 方法二：使用脚本方式。如果已经使用 tuned 方法，请跳过本方法。

        1. 执行 `grubby` 命令查看默认内核版本。

            > **注意：**
            >
            > 需安装 `grubby` 软件包。

            ```bash
            grubby --default-kernel
            ```

            ```bash
            /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

        2. 执行 `grubby --update-kernel` 命令修改内核配置。

            ```bash
            grubby --args="transparent_hugepage=never" --update-kernel `grubby --default-kernel`
            ```

            > **注意：**
            >
            > 你也可以在 `--update-kernel` 后指定实际的版本号，例如：`--update-kernel /boot/vmlinuz-3.10.0-957.el7.x86_64` 或 `ALL`。

        3. 执行 `grubby --info` 命令查看修改后的默认内核配置。

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

            ```bash
            echo never > /sys/kernel/mm/transparent_hugepage/enabled
            echo never > /sys/kernel/mm/transparent_hugepage/defrag
            ```

        5. 配置 udev 脚本应用 IO 调度器策略。

            ```bash
            vi /etc/udev/rules.d/60-tidb-schedulers.rules
            ```

            ```
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1fc035", ATTR{queue/scheduler}="noop"
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1f9e81", ATTR{queue/scheduler}="noop"

            ```

        6. 应用 udev 脚本。

            > **注意：**
            >
            > 对于已经使用 `noop` 或 `none` I/O 调度器的设备，无需配置 udev 规则，可以跳过此步骤。

            ```bash
            udevadm control --reload-rules
            udevadm trigger --type=devices --action=change
            ```

        7. 创建 CPU 节能策略配置服务。

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

            ```bash
            systemctl daemon-reload
            systemctl enable cpupower.service
            systemctl start cpupower.service
            ```

6. 执行以下命令验证透明大页的状态。

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    always madvise [never]
    ```

7. 执行以下命令验证数据目录所在磁盘的 I/O 调度器。

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

    ```
    [noop] deadline cfq
    [noop] deadline cfq
    ```

8. 执行以下命令查看 cpufreq 模块选用的节能策略。

    ```bash
    cpupower frequency-info --policy
    ```

    ```
    analyzing CPU 0:
    current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                  The governor "performance" may decide which speed to use within this range.
    ```

9. 执行以下命令修改 sysctl 参数。

    ```bash
    echo "fs.file-max = 1000000">> /etc/sysctl.conf
    echo "net.core.somaxconn = 32768">> /etc/sysctl.conf
    echo "net.ipv4.tcp_syncookies = 0">> /etc/sysctl.conf
    echo "vm.overcommit_memory = 1">> /etc/sysctl.conf
    echo "vm.min_free_kbytes = 1048576">> /etc/sysctl.conf
    sysctl -p
    ```

    > **警告：**
    >
    > 不建议在内存小于 16 GiB 的系统上调大 `vm.min_free_kbytes` 的值，否则可能导致系统不稳定或启动失败。

    > **注意：**
    >
    > - `vm.min_free_kbytes` 是 Linux 内核的一个参数，用于控制系统预留的最小空闲内存量，单位为 KiB。
    > - `vm.min_free_kbytes` 的设置会影响内存回收机制。设置得过大，会导致可用内存变少，设置得过小，可能会导致内存的申请速度超过后台的回收速度，进而导致内存回收并引起内存分配延迟。
    > - 建议将 `vm.min_free_kbytes` 最小设置为 `1048576` KiB（即 1 GiB）。如果[安装了 NUMA](/check-before-deployment.md#安装-numactl-工具)，建议设置为 `NUMA 节点个数 * 1048576` KiB。
    > - 对于运行 Linux 内核 4.11 或更早版本的系统，建议将 `net.ipv4.tcp_tw_recycle` 设置为 `0`。

10. 执行以下命令配置用户的 limits.conf 文件。

    ```bash
    cat << EOF >>/etc/security/limits.conf
    tidb           soft    nofile         1000000
    tidb           hard    nofile         1000000
    tidb           soft    stack          32768
    tidb           hard    stack          32768
    tidb           soft    core           unlimited
    tidb           hard    core           unlimited
    EOF
    ```

## 手动配置 SSH 互信及 sudo 免密码

本节介绍如何手动配置中控机到目标节点的 SSH 互信。如果你使用 TiUP 部署工具，SSH 互信和免密码登录会自动完成配置，可跳过本节。

在配置 SSH 互信时，建议在所有目标节点上创建并使用 `tidb` 用户。一般情况下，系统并不强制要求各节点上的用户相同。但在以下场景中，请注意用户一致性的要求：

- 使用备份恢复工具 (BR)：强烈建议使用同一用户执行所有 BR 和 TiDB 相关操作。
- 使用 NFS 等网络存储：需要确保该用户在所有节点上的 UID 和 GID 相同。NFS 通过底层 UID 和 GID 来识别文件访问权限，如果各节点的 UID 或 GID 不一致，或者执行 BR 的用户与运行 TiDB 的用户不同（尤其是在没有 `sudo` 权限时），备份或恢复过程中可能会出现权限被拒绝 (Permission Denied) 错误。

1. 以 `root` 用户依次登录到部署目标机器创建 `tidb` 用户并设置登录密码。

    ```bash
    useradd -m -d /home/tidb tidb
    passwd tidb
    ```

2. 执行以下命令，将 `tidb ALL=(ALL) NOPASSWD: ALL` 添加到文件末尾，即配置好 sudo 免密码。

    ```bash
    visudo
    ```

    ```
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

3. 以 `tidb` 用户登录到中控机，执行以下命令。将 `10.0.1.1` 替换成你的部署目标机器 IP，按提示输入部署目标机器 `tidb` 用户密码，执行成功后即创建好 SSH 互信，其他机器同理。新建的 `tidb` 用户下没有 `.ssh` 目录，需要执行生成 rsa 密钥的命令来生成 `.ssh` 目录。如果要在中控机上部署 TiDB 组件，需要为中控机和中控机自身配置互信。

    ```bash
    ssh-keygen -t rsa
    ssh-copy-id -i ~/.ssh/id_rsa.pub 10.0.1.1
    ```

4. 以 `tidb` 用户登录中控机，通过 `ssh` 的方式登录目标机器 IP。如果不需要输入密码并登录成功，即表示 SSH 互信配置成功。

    ```bash
    ssh 10.0.1.1
    ```

    ```
    [tidb@10.0.1.1 ~]$
    ```

5. 以 `tidb` 用户登录到部署目标机器后，执行以下命令，不需要输入密码并切换到 `root` 用户，表示 `tidb` 用户 sudo 免密码配置成功。

    ```bash
    sudo -su root
    ```

    ```
    [root@10.0.1.1 tidb]#
    ```

## 安装 numactl 工具

本段主要介绍如何安装 NUMA 工具。在生产环境中，因为硬件机器配置往往高于需求，为了更合理规划资源，会考虑单机多实例部署 TiDB 或者 TiKV。NUMA 绑核工具的使用，主要为了防止 CPU 资源的争抢，引发性能衰退。

> **注意：**
>
> - NUMA 绑核是用来隔离 CPU 资源的一种方法，适合高配置物理机环境部署多实例使用。
> - 通过 `tiup cluster deploy` 完成部署操作，就可以通过 `exec` 命令来进行集群级别管理工作。

安装 NUMA 工具有两种方法：

方法 1：登录到目标节点进行安装（以 CentOS Linux release 7.7.1908 (Core) 为例）。

```bash
sudo yum -y install numactl
```

方法 2：通过 `tiup cluster exec` 在集群上批量安装 NUMA。

1. 使用 TiUP 安装 TiDB 集群，参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)完成 `tidb-test` 集群的部署。如果本地已有集群，可跳过这一步。

    ```bash
    tiup cluster deploy tidb-test v6.1.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2. 执行 `tiup cluster exec` 命令，以 `sudo` 权限在 `tidb-test` 集群所有目标主机上安装 NUMA。

    ```bash
    tiup cluster exec tidb-test --sudo --command "yum -y install numactl"
    ```

    你可以执行 `tiup cluster exec --help` 查看的 `tiup cluster exec` 命令的说明信息。

## 关闭 SELinux

SELinux 必须关闭或设置为 `permissive` 模式。你可以使用 [getenforce(8)](https://linux.die.net/man/8/getenforce) 工具来检查 SELinux 的当前状态。

如果 SELinux 未关闭，请打开 `/etc/selinux/config` 文件，找到以 `SELINUX=` 开头的行，并将其修改为 `SELINUX=disabled`。修改完成后，你需要重启系统，因为从 `enforcing` 或 `permissive` 切换到 `disabled` 模式只有在重启后才会生效。

在某些系统（如 Ubuntu）上，`/etc/selinux/config` 文件可能不存在，且 getenforce 工具可能未安装。在这种情况下，可以跳过此检查步骤。
