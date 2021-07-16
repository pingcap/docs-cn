---
title: TiDB Environment and System Configuration Check
summary: Learn the environment check operations before deploying TiDB.
aliases: ['/docs/dev/check-before-deployment/']
---

# TiDB Environment and System Configuration Check

This document describes the environment check operations before deploying TiDB. The following steps are ordered by priorities.

## Mount the data disk ext4 filesystem with options on the target machines that deploy TiKV

For production deployments, it is recommended to use NVMe SSD of EXT4 filesystem to store TiKV data. This configuration is the best practice, whose reliability, security, and stability have been proven in a large number of online scenarios.

Log in to the target machines using the `root` user account.

Format your data disks to the ext4 filesystem and add the `nodelalloc` and `noatime` mount options to the filesystem. It is required to add the `nodelalloc` option, or else the TiUP deployment cannot pass the precheck. The `noatime` option is optional.

> **Note:**
>
> If your data disks have been formatted to ext4 and have added the mount options, you can uninstall it by running the `umount /dev/nvme0n1p1` command, skip directly to the fifth step below to edit the `/etc/fstab` file, and add the options again to the filesystem.

Take the `/dev/nvme0n1` data disk as an example:

1. View the data disk.

    {{< copyable "shell-root" >}}

    ```bash
    fdisk -l
    ```

    ```
    Disk /dev/nvme0n1: 1000 GB
    ```

2. Create the partition.

    {{< copyable "shell-root" >}}

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
    ```

    > **Note:**
    >
    > Use the `lsblk` command to view the device number of the partition: for a NVMe disk, the generated device number is usually `nvme0n1p1`; for a regular disk (for example, `/dev/sdb`), the generated device number is usually `sdb1`.

3. Format the data disk to the ext4 filesystem.

    {{< copyable "shell-root" >}}

    ```bash
    mkfs.ext4 /dev/nvme0n1p1
    ```

4. View the partition UUID of the data disk.

    In this example, the UUID of nvme0n1p1 is `c51eb23b-195c-4061-92a9-3fad812cc12f`.

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

5. Edit the `/etc/fstab` file and add the `nodelalloc` mount options.

    {{< copyable "shell-root" >}}

    ```bash
    vi /etc/fstab
    ```

    ```
    UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2
    ```

6. Mount the data disk.

    {{< copyable "shell-root" >}}

    ```bash
    mkdir /data1 && \
    mount -a
    ```

7. Check using the following command.

    {{< copyable "shell-root" >}}

    ```bash
    mount -t ext4
    ```

    ```
    /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
    ```

    If the filesystem is ext4 and `nodelalloc` is included in the mount options, you have successfully mount the data disk ext4 filesystem with options on the target machines.

## Check and disable system swap

This section describes how to disable swap.

TiDB requires sufficient memory space for operation. It is not recommended to use swap as a buffer for insufficient memory, which might reduce performance. Therefore, it is recommended to disable the system swap permanently.

Do not disable the system swap by executing `swapoff -a`, or this setting will be invalid after the machine is restarted.

To disable the system swap, execute the following command:

{{< copyable "shell-regular" >}}

```bash
echo "vm.swappiness = 0">> /etc/sysctl.conf
swapoff -a && swapon -a
sysctl -p
```

## Check and stop the firewall service of target machines

In TiDB clusters, the access ports between nodes must be open to ensure the transmission of information such as read and write requests and data heartbeats. In common online scenarios, the data interaction between the database and the application service and between the database nodes are all made within a secure network. Therefore, if there are no special security requirements, it is recommended to stop the firewall of the target machine. Otherwise, refer to [the port usage](/hardware-and-software-requirements.md#network-requirements) and add the needed port information to the allowlist of the firewall service.

The rest of this section describes how to stop the firewall service of a target machine.

1. Check the firewall status. Take CentOS Linux release 7.7.1908 (Core) as an example.

    {{< copyable "shell-regular" >}}

    ```shell
    sudo firewall-cmd --state
    sudo systemctl status firewalld.service
    ```

2. Stop the firewall service.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl stop firewalld.service
    ```

3. Disable automatic start of the firewall service.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl disable firewalld.service
    ```

4. Check the firewall status.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl status firewalld.service
    ```

## Check and install the NTP service

TiDB is a distributed database system that requires clock synchronization between nodes to guarantee linear consistency of transactions in the ACID model.

At present, the common solution to clock synchronization is to use the Network Time Protocol (NTP) services. You can use the `pool.ntp.org` timing service on the Internet, or build your own NTP service in an offline environment.

To check whether the NTP service is installed and whether it synchronizes with the NTP server normally, take the following steps:

1. Run the following command. If it returns `running`, then the NTP service is running.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl status ntpd.service
    ```

    ```
    ntpd.service - Network Time Service
    Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
    Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago
    ```

    - If it returns `Unit ntpd.service could not be found.`, then try the following command to see whether your system is configured to use `chronyd` instead of `ntpd` to perform clock synchronization with NTP:

        {{< copyable "shell-regular" >}}
    
        ```bash
        sudo systemctl status cronyd.service
        ```
    
        ```
        chronyd.service - NTP client/server
        Loaded: loaded (/usr/lib/systemd/system/chronyd.service; enabled; vendor preset: enabled)
        Active: active (running) since Mon 2021-04-05 09:55:29 EDT; 3 days ago
        ```
    
        If your system is configured to use `chronyd`, proceed to step 3.

2. Run the `ntpstat` command to check whether the NTP service synchronizes with the NTP server.

    > **Note:**
    >
    > For the Ubuntu system, you need to install the `ntpstat` package.

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    - If it returns `synchronised to NTP server` (synchronizing with the NTP server), then the synchronization process is normal.

        ```
        synchronised to NTP server (85.199.214.101) at stratum 2
        time correct to within 91 ms
        polling server every 1024 s
        ```

    - The following situation indicates the NTP service is not synchronizing normally:

        ```
        unsynchronised
        ```

    - The following situation indicates the NTP service is not running normally:

        ```
        Unable to talk to NTP daemon. Is it running?
        ```

3. Run the `chronyc tracking` command to check wheter the Chrony service synchronizes with the NTP server.

    > **Note:**
    >
    > This only applies to systems that use Chrony instead of NTPd.

    {{< copyable "shell-regular" >}}

    ```bash
    chronyc tracking
    ```

    - If the command returns `Leap status     : Normal`, the synchronization process is normal.

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

    - If the command returns the following result, an error occurs in the synchronization:

        ```
        Leap status    : Not synchronised
        ```

    - If the command returns the following result, the `chronyd` service is not running normally:

        ```
        506 Cannot talk to daemon
        ```

To make the NTP service start synchronizing as soon as possible, run the following command. Replace `pool.ntp.org` with your NTP server.

{{< copyable "shell-regular" >}}

```bash
sudo systemctl stop ntpd.service && \
sudo ntpdate pool.ntp.org && \
sudo systemctl start ntpd.service
```

To install the NTP service manually on the CentOS 7 system, run the following command:

{{< copyable "shell-regular" >}}

```bash
sudo yum install ntp ntpdate && \
sudo systemctl start ntpd.service && \
sudo systemctl enable ntpd.service
```

## Check and configure the optimal parameters of the operating system

For TiDB in the production environment, it is recommended to optimize the operating system configuration in the following ways:

1. Disable THP (Transparent Huge Pages). The memory access pattern of databases tends to be sparse rather than consecutive. If the high-level memory fragmentation is serious, higher latency will occur when THP pages are allocated. 
2. Set the I/O Scheduler of the storage media to `noop`. For the high-speed SSD storage media, the kernel's I/O scheduling operations can cause performance loss. After the Scheduler is set to `noop`, the performance is better because the kernel directly sends I/O requests to the hardware without other operations. Also, the noop Scheduler is better applicable.
3. Choose the `performance` mode for the cpufrequ module which controls the CPU frequency. The performance is maximized when the CPU frequency is fixed at its highest supported operating frequency without dynamic adjustment.

Take the following steps to check the current operating system configuration and configure optimal parameters:

1. Execute the following command to see whether THP is enabled or disabled:

    {{< copyable "shell-regular" >}}

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    [always] madvise never
    ```

    > **Note:**
    >
    > If `[always] madvise never` is output, THP is enabled. You need to disable it.

2. Execute the following command to see the I/O Scheduler of the disk where the data directory is located. Assume that you create data directories on both sdb and sdc disks:

    {{< copyable "shell-regular" >}}

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

    ```
    noop [deadline] cfq
    noop [deadline] cfq
    ```

    > **Note:**
    >
    > If `noop [deadline] cfq` is output, the I/O Scheduler for the disk is in the `deadline` mode. You need to change it to `noop`.

3. Execute the following command to see the `ID_SERIAL` of the disk:

    {{< copyable "shell-regular" >}}

    ```bash
    udevadm info --name=/dev/sdb | grep ID_SERIAL
    ```

    ```
    E: ID_SERIAL=36d0946606d79f90025f3e09a0c1f9e81
    E: ID_SERIAL_SHORT=6d0946606d79f90025f3e09a0c1f9e81
    ```

    > **Note:**
    >
    > If multiple disks are allocated with data directories, you need to execute the above command several times to record the `ID_SERIAL` of each disk.

4. Execute the following command to see the power policy of the cpufreq module:

    {{< copyable "shell-regular" >}}

    ```bash
    cpupower frequency-info --policy
    ```

    ```
    analyzing CPU 0:
    current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                  The governor "powersave" may decide which speed to use within this range.
    ```

    > **Note:**
    >
    > If `The governor "powersave"` is output, the power policy of the cpufreq module is `powersave`. You need to modify it to `performance`. If you use a virtual machine or a cloud host, the output is usually `Unable to determine current policy`, and you do not need to change anything.

5. Configure optimal parameters of the operating system:

    + Method one: Use tuned (Recommended)

        1. Execute the `tuned-adm list` command to see the tuned profile of the current operating system:

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

            The output `Current active profile: balanced` means that the tuned profile of the current operating system is `balanced`. It is recommended to optimize the configuration of the operating system based on the current profile.

        2. Create a new tuned profile:

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

            The output `include=balanced` means to add the optimization configuration of the operating system to the current `balanced` profile.

        3. Apply the new tuned profile:

            {{< copyable "shell-regular" >}}

            ```bash
            tuned-adm profile balanced-tidb-optimal
            ```

    + Method two: Configure using scripts. Skip this method if you already use method one.

        1. Execute the `grubby` command to see the default kernel version:

            > **Note:**
            >
            > Install the `grubby` package first before you execute `grubby`.

            {{< copyable "shell-regular" >}}

            ```bash
            grubby --default-kernel
            ```

            ```bash
            /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

        2. Execute `grubby --update-kernel` to modify the kernel configuration:

            {{< copyable "shell-regular" >}}

            ```bash
            grubby --args="transparent_hugepage=never" --update-kernel /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

            > **Note:**
            >
            > `--update-kernel` is followed by the actual default kernel version.

        3. Execute `grubby --info` to see the modified default kernel configuration:

            {{< copyable "shell-regular" >}}

            ```bash
            grubby --info /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

            > **Note:**
            >
            > `--info` is followed by the actual default kernel version.

            ```
            index=0
            kernel=/boot/vmlinuz-3.10.0-957.el7.x86_64
            args="ro crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet LANG=en_US.UTF-8 transparent_hugepage=never"
            root=/dev/mapper/centos-root
            initrd=/boot/initramfs-3.10.0-957.el7.x86_64.img
            title=CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)
            ```

        4. Modify the current kernel configuration to immediately disable THP:

            {{< copyable "shell-regular" >}}

            ```bash
            echo never > /sys/kernel/mm/transparent_hugepage/enabled
            echo never > /sys/kernel/mm/transparent_hugepage/defrag
            ```

        5. Configure the I/O Scheduler in the udev script:

            {{< copyable "shell-regular" >}}

            ```bash
            vi /etc/udev/rules.d/60-tidb-schedulers.rules
            ```

            ```
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1fc035", ATTR{queue/scheduler}="noop"
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1f9e81", ATTR{queue/scheduler}="noop"

            ```

        6. Apply the udev script:

            {{< copyable "shell-regular" >}}

            ```bash
            udevadm control --reload-rules
            udevadm trigger --type=devices --action=change
            ```

        7. Create a service to configure the CPU power policy:

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

        8. Apply the CPU power policy configuration service:

            {{< copyable "shell-regular" >}}

            ```bash
            systemctl daemon-reload
            systemctl enable cpupower.service
            systemctl start cpupower.service
            ```

6. Execute the following command to verify the THP status:

    {{< copyable "shell-regular" >}}

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    always madvise [never]
    ```

7. Execute the following command to verify the I/O Scheduler of the disk where the data directory is located:

    {{< copyable "shell-regular" >}}

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

    ```
    [noop] deadline cfq
    [noop] deadline cfq
    ```

8. Execute the following command to see the power policy of the cpufreq module:

    {{< copyable "shell-regular" >}}

    ```bash
    cpupower frequency-info --policy
      ```

    ```
    analyzing CPU 0:
    current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                  The governor "performance" may decide which speed to use within this range.
    ```

9. Execute the following commands to modify the `sysctl` parameters:

    {{< copyable "shell-regular" >}}

    ```bash
    echo "fs.file-max = 1000000">> /etc/sysctl.conf
    echo "net.core.somaxconn = 32768">> /etc/sysctl.conf
    echo "net.ipv4.tcp_tw_recycle = 0">> /etc/sysctl.conf
    echo "net.ipv4.tcp_syncookies = 0">> /etc/sysctl.conf
    echo "vm.overcommit_memory = 1">> /etc/sysctl.conf
    sysctl -p
    ```

10. Execute the following command to configure the user's `limits.conf` file:

    {{< copyable "shell-regular" >}}

    ```bash
    cat << EOF >>/etc/security/limits.conf
    tidb           soft    nofile          1000000
    tidb           hard    nofile          1000000
    tidb           soft    stack          32768
    tidb           hard    stack          32768
    EOF
    ```

## Manually configure the SSH mutual trust and sudo without password

This section describes how to manually configure the SSH mutual trust and sudo without password. It is recommended to use TiUP for deployment, which automatically configure SSH mutual trust and login without password. If you deploy TiDB clusters using TiUP, ignore this section.

1. Log in to the target machine respectively using the `root` user account, create the `tidb` user and set the login password.

    {{< copyable "shell-root" >}}

    ```bash
    useradd tidb && \
    passwd tidb
    ```

2. To configure sudo without password, run the following command, and add `tidb ALL=(ALL) NOPASSWD: ALL` to the end of the file:

    {{< copyable "shell-root" >}}

    ```bash
    visudo
    ```

    ```
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

3. Use the `tidb` user to log in to the control machine, and run the following command. Replace `10.0.1.1` with the IP of your target machine, and enter the `tidb` user password of the target machine as prompted. After the command is executed, SSH mutual trust is already created. This applies to other machines as well. Newly created `tidb` users do not have the `.ssh` directory. To create such a directory, execute the command that generates the RSA key. To deploy TiDB components on the control machine, configure mutual trust for the control machine and the control machine itself.

    {{< copyable "shell-regular" >}}

    ```bash
    ssh-keygen -t rsa
    ssh-copy-id -i ~/.ssh/id_rsa.pub 10.0.1.1
    ```

4. Log in to the control machine using the `tidb` user account, and log in to the IP of the target machine using `ssh`. If you do not need to enter the password and can successfully log in, then the SSH mutual trust is successfully configured.

    {{< copyable "shell-regular" >}}

    ```bash
    ssh 10.0.1.1
    ```

    ```
    [tidb@10.0.1.1 ~]$
    ```

5. After you log in to the target machine using the `tidb` user, run the following command. If you do not need to enter the password and can switch to the `root` user, then sudo without password of the `tidb` user is successfully configured.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo -su root
    ```

    ```
    [root@10.0.1.1 tidb]#
    ```

## Install the `numactl` tool

This section describes how to install the NUMA tool. In online environments, because the hardware configuration is usually higher than required, to better plan the hardware resources, multiple instances of TiDB or TiKV can be deployed on a single machine. In such scenarios, you can use NUMA tools to prevent the competition for CPU resources which might cause reduced performance.

> **Note:**
>
> - Binding cores using NUMA is a method to isolate CPU resources and is suitable for deploying multiple instances on highly configured physical machines.
> - After completing deployment using `tiup cluster deploy`, you can use the `exec` command to perform cluster level management operations.

1. Log in to the target node to install. Take CentOS Linux release 7.7.1908 (Core) as an example.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo yum -y install numactl
    ```

2. Run the `exec` command using `tiup cluster` to install in batches.

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

    To use the sudo privilege to execute the installation command for all the target machines in the `tidb-test` cluster, run the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster exec tidb-test --sudo --command "yum -y install numactl"
    ```
