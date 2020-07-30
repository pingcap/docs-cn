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

3. Use the `tidb` user to log in to the control machine, and run the following command. Replace `10.0.1.1` with the IP of your target machine, and enter the `tidb` user password of the target machine as prompted. After the command is executed, SSH mutual trust is already created. This applies to other machines as well.

    {{< copyable "shell-regular" >}}

    ```bash
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
