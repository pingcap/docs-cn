---
title: Deploy TiDB Using TiDB Ansible
summary: Use TiDB Ansible to deploy a TiDB cluster.
aliases: ['/docs/dev/online-deployment-using-ansible/','/docs/dev/how-to/deploy/orchestrated/ansible/']
---

# Deploy TiDB Using TiDB Ansible

> **Warning:**
>
> For production environments, it is recommended that you [deploy TiDB using TiUP](/production-deployment-using-tiup.md). Since v4.0, PingCAP no longer provides support for deploying TiDB using TiDB Ansible (deprecated). If you really need to use it for deployment, be aware of any risk. You can [import the TiDB cluster deployed by TiDB Ansible to TiUP](/upgrade-tidb-using-tiup.md#import-the-tidb-ansible-cluster-to-tiup).
>
> If you only want to try out TiDB and explore new features, refer to [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md).

This guide describes how to deploy a TiDB cluster using TiDB Ansible. For the production environment, it is recommended to deploy TiDB using TiUP.

## Overview

Ansible is an IT automation tool that can configure systems, deploy software, and orchestrate more advanced IT tasks such as continuous deployments or zero downtime rolling updates.

[TiDB Ansible](https://github.com/pingcap/tidb-ansible) is a TiDB cluster deployment tool developed by PingCAP, based on Ansible playbook. TiDB Ansible enables you to quickly deploy a new TiDB cluster which includes PD, TiDB, TiKV, and the cluster monitoring modules.

You can use the TiDB Ansible configuration file to set up the cluster topology and complete all the following operation tasks:

- Initialize operating system parameters
- Deploy the whole TiDB cluster
- [Start the TiDB cluster](/maintain-tidb-using-ansible.md#start-a-cluster)
- [Stop the TiDB cluster](/maintain-tidb-using-ansible.md#stop-a-cluster)
- [Modify component configuration](/upgrade-tidb-using-ansible.md#edit-the-configuration-file-of-tidb-cluster-components)
- [Scale the TiDB cluster](/scale-tidb-using-ansible.md)
- [Upgrade the component version](/upgrade-tidb-using-ansible.md#step-5-perform-a-rolling-update-to-tidb-cluster-components)
- [Enable the cluster binlog](/tidb-binlog/tidb-binlog-overview.md)
- [Clean up data of the TiDB cluster](/maintain-tidb-using-ansible.md#clean-up-cluster-data)
- [Destroy the TiDB cluster](/maintain-tidb-using-ansible.md#destroy-a-cluster)

## Prepare

Before you start, make sure you have:

1. Several target machines that meet the following requirements:

    - 4 or more machines

        A standard TiDB cluster contains 6 machines. You can use 4 machines for testing. For more details, see [Software and Hardware Recommendations](/hardware-and-software-requirements.md).

    - x86_64 architecture (AMD64) with CentOS 7.3 (64 bit) or later; Or x86_64 architecture (ARM64) with CentOS 7.6 1810 or later.
    - Network between machines

    > **Note:**
    >
    > When you deploy TiDB using TiDB Ansible, **use SSD disks for the data directory of TiKV and PD nodes**. Otherwise, it cannot pass the check. If you only want to try TiDB out and explore the features, it is recommended to [deploy TiDB using Docker Compose](/deploy-test-cluster-using-docker-compose.md) on a single machine.

2. A control machine that meets the following requirements:

    > **Note:**
    >
    > The control machine can be one of the target machines.

    - CentOS 7.3 (64 bit) or later with Python 2.7 installed
    - Access to the Internet

## Step 1: Install system dependencies on the control machine

Log in to the control machine using the `root` user account, and run the corresponding command according to your operating system.

- If you use a control machine installed with CentOS 7, run the following command:

    {{< copyable "shell-root" >}}

    ```shell
    yum -y install epel-release git curl sshpass && \
    yum -y install python2-pip
    ```

- If you use a control machine installed with Ubuntu, run the following command:

    {{< copyable "shell-root" >}}

    ```shell
    apt-get -y install git curl sshpass python-pip
    ```

## Step 2: Create the `tidb` user on the control machine and generate the SSH key

Make sure you have logged in to the control machine using the `root` user account, and then run the following command.

1. Create the `tidb` user.

    {{< copyable "shell-root" >}}

    ```shell
    useradd -m -d /home/tidb tidb
    ```

2. Set a password for the `tidb` user account.

    {{< copyable "shell-root" >}}

    ```shell
    passwd tidb
    ```

3. Configure sudo without password for the `tidb` user account by adding `tidb ALL=(ALL) NOPASSWD: ALL` to the end of the sudo file:

    {{< copyable "shell-root" >}}

    ```shell
    visudo
    ```

    ```
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

4. Generate the SSH key.

    Execute the `su` command to switch the user from `root` to `tidb`.

    {{< copyable "shell-root" >}}

    ```shell
    su - tidb
    ```

    Create the SSH key for the `tidb` user account and hit the Enter key when `Enter passphrase` is prompted. After successful execution, the SSH private key file is `/home/tidb/.ssh/id_rsa`, and the SSH public key file is `/home/tidb/.ssh/id_rsa.pub`.

    {{< copyable "shell-regular" >}}

    ```shell
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

## Step 3: Download TiDB Ansible to the control machine

Log in to the control machine using the `tidb` user account and enter the `/home/tidb` directory. Run the following command to download TiDB Ansible from the master branch of the [TiDB Ansible project](https://github.com/pingcap/tidb-ansible). The default folder name is `tidb-ansible`.

{{< copyable "shell-regular" >}}

```shell
git clone https://github.com/pingcap/tidb-ansible.git
```

> **Note:**
>
> - To deploy and upgrade TiDB clusters, use the corresponding version of `tidb-ansible`. If you only modify the version in the `inventory.ini` file, errors might occur.
> - It is required to download `tidb-ansible` to the `/home/tidb` directory using the `tidb` user account. If you download it to the `/root` directory, a privilege issue occurs.

If you have questions regarding which version to use, email to info@pingcap.com for more information or [file an issue](https://github.com/pingcap/tidb-ansible/issues/new).

## Step 4: Install TiDB Ansible and its dependencies on the control machine

Make sure you have logged in to the control machine using the `tidb` user account.

It is required to use `pip` to install Ansible and its dependencies, otherwise a compatibility issue occurs. Currently, the release-2.0, release-2.1, release-3.1, and master branches of TiDB Ansible are compatible with Ansible 2.4 ~ 2.7.11 (2.4 ≤ Ansible ≤ 2.7.11).

1. Install TiDB Ansible and the dependencies on the control machine:

    {{< copyable "shell-regular" >}}

    ```bash
    cd /home/tidb/tidb-ansible && \
    sudo pip install -r ./requirements.txt
    ```

    The version information of Ansible and dependencies is in the `tidb-ansible/requirements.txt` file.

2. View the version of TiDB Ansible:

    {{< copyable "shell-regular" >}}

    ```bash
    ansible --version
    ```

    ```
    ansible 2.7.11
    ```

## Step 5: Configure the SSH mutual trust and sudo rules on the control machine

Make sure you have logged in to the control machine using the `tidb` user account.

1. Add the IPs of your target machines to the `[servers]` section of the `hosts.ini` file.

    {{< copyable "shell-regular" >}}

    ```bash
    cd /home/tidb/tidb-ansible && \
    vi hosts.ini
    ```

    ```
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

2. Run the following command and input the `root` user account password of your target machines.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook -i hosts.ini create_users.yml -u root -k
    ```

    This step creates the `tidb` user account on the target machines, configures the sudo rules and the SSH mutual trust between the control machine and the target machines.

To configure the SSH mutual trust and sudo without password manually, see [How to manually configure the SSH mutual trust and sudo without password](#how-to-manually-configure-the-ssh-mutual-trust-and-sudo-without-password).

## Step 6: Install the NTP service on the target machines

> **Note:**
>
> If the time and time zone of all your target machines are same, the NTP service is on and is normally synchronizing time, you can ignore this step. See [How to check whether the NTP service is normal](#how-to-check-whether-the-ntp-service-is-normal).

Make sure you have logged in to the control machine using the `tidb` user account, run the following command:

{{< copyable "shell-regular" >}}

```bash
cd /home/tidb/tidb-ansible && \
ansible-playbook -i hosts.ini deploy_ntp.yml -u tidb -b
```

The NTP service is installed and started using the software repository that comes with the system on the target machines. The default NTP server list in the installation package is used. The related `server` parameter is in the `/etc/ntp.conf` configuration file.

To make the NTP service start synchronizing as soon as possible, the system executes the `ntpdate` command to set the local date and time by polling `ntp_server` in the `hosts.ini` file. The default server is `pool.ntp.org`, and you can also replace it with your NTP server.

## Step 7: Configure the CPUfreq governor mode on the target machine

For details about CPUfreq, see [the CPUfreq Governor documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/power_management_guide/cpufreq_governors).

Set the CPUfreq governor mode to `performance` to make full use of CPU performance.

### Check the governor modes supported by the system

You can run the `cpupower frequency-info --governors` command to check the governor modes which the system supports:

{{< copyable "shell-root" >}}

```bash
cpupower frequency-info --governors
```

```
analyzing CPU 0:
  available cpufreq governors: performance powersave
```

Taking the above code for example, the system supports the `performance` and `powersave` modes.

> **Note:**
>
> As the following shows, if it returns `Not Available`, it means that the current system does not support CPUfreq configuration and you can skip this step.

{{< copyable "shell-root" >}}

```bash
cpupower frequency-info --governors
```

```
analyzing CPU 0:
   available cpufreq governors: Not Available
```

### Check the current governor mode

You can run the `cpupower frequency-info --policy` command to check the current CPUfreq governor mode:

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

As the above code shows, the current mode is `powersave` in this example.

### Change the governor mode

You can use either of the following two methods to change the governor mode. In the above example, the current governor mode is `powersave` and the following commands change it to `performance`.

- Use the `cpupower frequency-set --governor` command to change the current mode:

    {{< copyable "shell-root" >}}

    ```shell
    cpupower frequency-set --governor performance
    ```

- Run the following command to set the mode on the target machine in batches:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible -i hosts.ini all -m shell -a "cpupower frequency-set --governor performance" -u tidb -b
    ```

## Step 8: Mount the data disk ext4 filesystem with options on the target machines

Log in to the target machines using the `root` user account.

Format your data disks to the ext4 filesystem and add the `nodelalloc` and `noatime` mount options to the filesystem. It is required to add the `nodelalloc` option, or else the Ansible deployment cannot pass the test. The `noatime` option is optional.

> **Note:**
>
> If your data disks have been formatted to ext4 and have added the mount options, you can uninstall it by running the `umount /dev/nvme0n1p1` command, follow the steps starting from editing the `/etc/fstab` file, and add the options again to the filesystem.

Take the `/dev/nvme0n1` data disk as an example:

1. View the data disk.

    {{< copyable "shell-root" >}}

    ```shell
    fdisk -l
    ```

    ```
    Disk /dev/nvme0n1: 1000 GB
    ```

2. Create the partition table.

    {{< copyable "shell-root" >}}

    ```shell
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
    ```

    > **Note:**
    >
    > Use the `lsblk` command to view the device number of the partition: for a nvme disk, the generated device number is usually `nvme0n1p1`; for a regular disk (for example, `/dev/sdb`), the generated device number is usually `sdb1`.

3. Format the data disk to the ext4 filesystem.

    {{< copyable "shell-root" >}}

    ```shell
    mkfs.ext4 /dev/nvme0n1p1
    ```

4. View the partition UUID of the data disk.

    In this example, the UUID of `nvme0n1p1` is `c51eb23b-195c-4061-92a9-3fad812cc12f`.

    {{< copyable "shell-root" >}}

    ```shell
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

5. Edit the `/etc/fstab` file and add the mount options.

    {{< copyable "shell-root" >}}

    ```shell
    vi /etc/fstab
    ```

    ```
    UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2
    ```

6. Mount the data disk.

    {{< copyable "shell-root" >}}

    ```shell
    mkdir /data1 && \
    mount -a
    ```

7. Check using the following command.

    {{< copyable "shell-root" >}}

    ```shell
    mount -t ext4
    ```

    ```
    /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
    ```

    If the filesystem is ext4 and `nodelalloc` is included in the mount options, you have successfully mount the data disk ext4 filesystem with options on the target machines.

## Step 9: Edit the `inventory.ini` file to orchestrate the TiDB cluster

Log in to the control machine using the `tidb` user account, and edit the `tidb-ansible/inventory.ini` file to orchestrate the TiDB cluster. The standard TiDB cluster contains 6 machines: 2 TiDB instances, 3 PD instances, and 3 TiKV instances.

- Deploy at least 3 instances for TiKV.
- Do not deploy TiKV together with TiDB or PD on the same machine.
- Use the first TiDB machine as the monitoring machine.

> **Note:**
>
> It is required to use the internal IP address to deploy. If the SSH port of the target machines is not the default 22 port, you need to add the `ansible_port` variable. For example, `TiDB1 ansible_host=172.16.10.1 ansible_port=5555`.

You can choose one of the following two types of cluster topology according to your scenario:

- [The cluster topology of a single TiKV instance on each TiKV node](#option-1-use-the-cluster-topology-of-a-single-tikv-instance-on-each-tikv-node)

    In most cases, it is recommended to deploy one TiKV instance on each TiKV node for better performance. However, if the CPU and memory of your TiKV machines are much better than the required in [Hardware and Software Requirements](/hardware-and-software-requirements.md), and you have more than two disks in one node or the capacity of one SSD is larger than 2 TB, you can deploy no more than 2 TiKV instances on a single TiKV node.

- [The cluster topology of multiple TiKV instances on each TiKV node](#option-2-use-the-cluster-topology-of-multiple-tikv-instances-on-each-tikv-node)

### Option 1: Use the cluster topology of a single TiKV instance on each TiKV node

| Name  | Host IP     | Services   |
|:------|:------------|:-----------|
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3        |
| node4 | 172.16.10.4 | TiKV1      |
| node5 | 172.16.10.5 | TiKV2      |
| node6 | 172.16.10.6 | TiKV3      |

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

### Option 2: Use the cluster topology of multiple TiKV instances on each TiKV node

Take two TiKV instances on each TiKV node as an example:

| Name  | Host IP     | Services   |
|:------|:------------|:-----------|
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2  |
| node3 | 172.16.10.3 | PD3         |
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

# Note: To use labels in TiKV, you must also configure location_labels for PD at the same time.
[tikv_servers]
TiKV1-1 ansible_host=172.16.10.4 deploy_dir=/data1/deploy tikv_port=20171 tikv_status_port=20181 labels="host=tikv1"
TiKV1-2 ansible_host=172.16.10.4 deploy_dir=/data2/deploy tikv_port=20172 tikv_status_port=20182 labels="host=tikv1"
TiKV2-1 ansible_host=172.16.10.5 deploy_dir=/data1/deploy tikv_port=20171 tikv_status_port=20181 labels="host=tikv2"
TiKV2-2 ansible_host=172.16.10.5 deploy_dir=/data2/deploy tikv_port=20172 tikv_status_port=20182 labels="host=tikv2"
TiKV3-1 ansible_host=172.16.10.6 deploy_dir=/data1/deploy tikv_port=20171 tikv_status_port=20181 labels="host=tikv3"
TiKV3-2 ansible_host=172.16.10.6 deploy_dir=/data2/deploy tikv_port=20172 tikv_status_port=20182 labels="host=tikv3"

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

......

# Note: For labels in TiKV to work, you must also configure location_labels for PD when deploying the cluster.
[pd_servers:vars]
location_labels = ["host"]
```

**Edit the parameters in the service configuration file:**

1. For the cluster topology of multiple TiKV instances on each TiKV node, you need to edit the `capacity` parameter under `block-cache-size` in `tidb-ansible/conf/tikv.yml`:

    ```yaml
    storage:
      block-cache:
        capacity: "1GB"
    ```

    > **Note:**
    >
    > + The number of TiKV instances is the number of TiKV processes on each server.
    > + Recommended configuration: `capacity` = MEM_TOTAL \* 0.5 / the number of TiKV instances

2. For the cluster topology of multiple TiKV instances on each TiKV node, you need to edit the `high-concurrency`, `normal-concurrency` and `low-concurrency` parameters in the `tidb-ansible/conf/tikv.yml` file:

    ```yaml
    readpool:
    coprocessor:
        # Notice: if CPU_NUM > 8, default thread pool size for coprocessors
        # will be set to CPU_NUM * 0.8.
        # high-concurrency: 8
        # normal-concurrency: 8
        # low-concurrency: 8
    ```

    > **Note:**
    >
    > Recommended configuration: the number of TiKV instances \* the parameter value = the number of CPU cores \* 0.8.

3. If multiple TiKV instances are deployed on a same physical disk, edit the `capacity` parameter in `conf/tikv.yml`:

    ```yaml
    raftstore:
      capacity: 0
    ```

    > **Note:**
    >
    > Recommended configuration: `capacity` = total disk capacity / the number of TiKV instances. For example, `capacity: "100GB"`.

## Step 10: Edit variables in the `inventory.ini` file

This step describes how to edit the variable of deployment directory and other variables in the `inventory.ini` file.

### Configure the deployment directory

Edit the `deploy_dir` variable to configure the deployment directory.

The global variable is set to `/home/tidb/deploy` by default, and it applies to all services. If the data disk is mounted on the `/data1` directory, you can set it to `/data1/deploy`. For example:

```ini
## Global variables
[all:vars]
deploy_dir = /data1/deploy
```

> **Note:**
>
> To separately set the deployment directory for a service, you can configure the host variable while configuring the service host list in the `inventory.ini` file. It is required to add the first column alias, to avoid confusion in scenarios of mixed services deployment.

```ini
TiKV1-1 ansible_host=172.16.10.4 deploy_dir=/data1/deploy
```

### Edit other variables (Optional)

To enable the following control variables, use the capitalized `True`. To disable the following control variables, use the capitalized `False`.

| Variable Name | Description |
| :---- | :------- |
| cluster_name | the name of a cluster, adjustable |
| cpu_architecture | CPU architecture. `amd64` by default, `arm64` optional |
| tidb_version | the version of TiDB, configured by default in TiDB Ansible branches |
| process_supervision | the supervision way of processes, `systemd` by default, `supervise` optional |
| timezone | the global default time zone configured when a new TiDB cluster bootstrap is initialized; you can edit it later using the global `time_zone` system variable and the session `time_zone` system variable as described in [Time Zone Support](/configure-time-zone.md); the default value is `Asia/Shanghai` and see [the list of time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for more optional values |
| enable_firewalld | to enable the firewall, closed by default; to enable it, add the ports in [network requirements](/hardware-and-software-requirements.md#network-requirements) to the allowlist |
| enable_ntpd | to monitor the NTP service of the managed node, True by default; do not close it |
| set_hostname | to edit the hostname of the managed node based on the IP, False by default |
| enable_binlog | whether to deploy Pump and enable the binlog, False by default, dependent on the Kafka cluster; see the `zookeeper_addrs` variable |
| zookeeper_addrs | the zookeeper address of the binlog Kafka cluster |
| deploy_without_tidb | the Key-Value mode, deploy only PD, TiKV and the monitoring service, not TiDB; set the IP of the tidb_servers host group to null in the `inventory.ini` file |
| alertmanager_target | optional: If you have deployed `alertmanager` separately, you can configure this variable using the `alertmanager_host:alertmanager_port` format |
| grafana_admin_user | the username of Grafana administrator; default `admin` |
| grafana_admin_password | the password of Grafana administrator account; default `admin`; used to import Dashboard and create the API key using TiDB Ansible; update this variable if you have modified it through Grafana web |
| collect_log_recent_hours | to collect the log of recent hours; default the recent 2 hours |
| enable_bandwidth_limit | to set a bandwidth limit when pulling the diagnostic data from the target machines to the control machine; used together with the `collect_bandwidth_limit` variable |
| collect_bandwidth_limit | the limited bandwidth when pulling the diagnostic data from the target machines to the control machine; unit: Kbit/s; default 10000, indicating 10Mb/s; for the cluster topology of multiple TiKV instances on each TiKV node, you need to divide the number of the TiKV instances on each TiKV node |
| prometheus_storage_retention | the retention time of the monitoring data of Prometheus (30 days by default); this is a new configuration in the `group_vars/monitoring_servers.yml` file in 2.1.7, 3.0 and the later tidb-ansible versions |

## Step 11: Deploy the TiDB cluster

When `ansible-playbook` runs Playbook, the default concurrent number is 5. If many target machines are deployed, you can add the `-f` parameter to specify the concurrency, such as `ansible-playbook deploy.yml -f 10`.

The following example uses `tidb` as the user who runs the service.

1. Edit the `tidb-ansible/inventory.ini` file to make sure `ansible_user = tidb`.

    ```ini
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

    > **Note:**
    >
    > Do not configure `ansible_user` to `root`, because `tidb-ansible` limits the user that runs the service to the normal user.

    Run the following command and if all servers return `tidb`, then the SSH mutual trust is successfully configured:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible -i inventory.ini all -m shell -a 'whoami'
    ```

    Run the following command and if all servers return `root`, then sudo without password of the `tidb` user is successfully configured:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible -i inventory.ini all -m shell -a 'whoami' -b
    ```

2. Run the `local_prepare.yml` playbook and download TiDB binary to the control machine.

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook local_prepare.yml
    ```

3. Initialize the system environment and modify the kernel parameters.

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook bootstrap.yml
    ```

4. Deploy the TiDB cluster software.

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook deploy.yml
    ```

    > **Note:**
    >
    > You can use the `Report` button on the Grafana Dashboard to generate the PDF file. This function depends on the `fontconfig` package and English fonts. To use this function, log in to the `grafana_servers` machine and install it using the following command:
    >
    > {{< copyable "shell-regular" >}}
    >
    > ```bash
    > sudo yum install fontconfig open-sans-fonts
    > ```

5. Start the TiDB cluster.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook start.yml
    ```

## Test the TiDB cluster

Because TiDB is compatible with MySQL, you must use the MySQL client to connect to TiDB directly. It is recommended to configure load balancing to provide uniform SQL interface.

1. Connect to the TiDB cluster using the MySQL client.

    {{< copyable "shell-regular" >}}

    ```shell
    mysql -u root -h 172.16.10.1 -P 4000
    ```

    > **Note:**
    >
    > The default port of TiDB service is `4000`.

2. Access the monitoring platform using a web browser.

    - Address: <http://172.16.10.1:3000>
    - Default account and password: `admin`; `admin`

> **Note:**
>
> By default, TiDB periodically shares usage details with PingCAP to help understand how to improve the product. For details about what is shared and how to disable the sharing, see [Telemetry](/telemetry.md).

## Deployment FAQs

This section lists the common questions about deploying TiDB using TiDB Ansible.

### How to customize the port?

Edit the `inventory.ini` file and add the following host variable after the IP of the corresponding service:

| Component     | Variable Port      | Default Port | Description              |
|:--------------|:-------------------|:-------------|:-------------------------|
| TiDB          | tidb_port          | 4000         | the communication port for the application and DBA tools |
| TiDB          | tidb_status_port   | 10080        | the communication port to report TiDB status |
| TiKV          | tikv_port          | 20160        | the TiKV communication port |
| TiKV          | tikv_status_port   | 20180        | the communication port to report the TiKV status |
| PD            | pd_client_port     | 2379         | the communication port between TiDB and PD |
| PD            | pd_peer_port       | 2380         | the inter-node communication port within the PD cluster |
| Pump          | pump_port          | 8250         | the pump communication port |
| Prometheus    | prometheus_port    | 9090         | the communication port for the Prometheus service |
| Pushgateway   | pushgateway_port   | 9091         | the aggregation and report port for TiDB, TiKV, and PD monitor |
| Node_exporter | node_exporter_port | 9100         | the communication port to report the system information of every TiDB cluster node |
| Grafana       | grafana_port       | 3000         | the port for the external Web monitoring service and client (Browser) access |
| Kafka_exporter | kafka_exporter_port | 9308 | the communication port for Kafka_exporter, used to monitor the binlog Kafka cluster |

### How to customize the deployment directory?

Edit the `inventory.ini` file and add the following host variable after the IP of the corresponding service:

| Component     | Variable Directory    | Default Directory             | Description |
|:--------------|:----------------------|:------------------------------|:-----|
| Global        | deploy_dir            | /home/tidb/deploy             | the deployment directory |
| TiDB          | tidb_log_dir          | {{ deploy_dir }}/log          | the TiDB log directory |
| TiKV          | tikv_log_dir          | {{ deploy_dir }}/log          | the TiKV log directory |
| TiKV          | tikv_data_dir         | {{ deploy_dir }}/data         | the data directory |
| TiKV          | wal_dir               | ""                            | the rocksdb write-ahead log directory, consistent with the TiKV data directory when the value is null |
| TiKV          | raftdb_path           | ""                            | the raftdb directory, being tikv_data_dir/raft when the value is null |
| PD            | pd_log_dir            | {{ deploy_dir }}/log          | the PD log directory |
| PD            | pd_data_dir           | {{ deploy_dir }}/data.pd      | the PD data directory |
| Pump          | pump_log_dir          | {{ deploy_dir }}/log          | the Pump log directory |
| Pump          | pump_data_dir         | {{ deploy_dir }}/data.pump    | the Pump data directory |
| Prometheus    | prometheus_log_dir    | {{ deploy_dir }}/log          | the Prometheus log directory |
| Prometheus    | prometheus_data_dir   | {{ deploy_dir }}/data.metrics | the Prometheus data directory |
| Pushgateway   | pushgateway_log_dir   | {{ deploy_dir }}/log          | the pushgateway log directory |
| Node_exporter | node_exporter_log_dir | {{ deploy_dir }}/log          | the node_exporter log directory |
| Grafana       | grafana_log_dir       | {{ deploy_dir }}/log          | the Grafana log directory |
| Grafana       | grafana_data_dir      | {{ deploy_dir }}/data.grafana | the Grafana data directory |

### How to check whether the NTP service is normal?

1. Run the following command. If it returns `running`, then the NTP service is running:

    {{< copyable "shell-regular" >}}

    ```shell
    sudo systemctl status ntpd.service
    ```

    ```
    ntpd.service - Network Time Service
    Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
    Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago
    ```

2. Run the ntpstat command. If it returns `synchronised to NTP server` (synchronizing with the NTP server), then the synchronization process is normal.

    {{< copyable "shell-regular" >}}

    ```shell
    ntpstat
    ```

    ```
    synchronised to NTP server (85.199.214.101) at stratum 2
    time correct to within 91 ms
    polling server every 1024 s
    ```

> **Note:**
>
> For the Ubuntu system, you need to install the `ntpstat` package.

- The following condition indicates the NTP service is not synchronizing normally:

    {{< copyable "shell-regular" >}}

    ```shell
    ntpstat
    ```

    ```
    unsynchronised
    ```

- The following condition indicates the NTP service is not running normally:

    {{< copyable "shell-regular" >}}

    ```shell
    ntpstat
    ```

    ```
    Unable to talk to NTP daemon. Is it running?
    ```

- To make the NTP service start synchronizing as soon as possible, run the following command. You can replace `pool.ntp.org` with other NTP servers.

    {{< copyable "shell-regular" >}}

    ```shell
    sudo systemctl stop ntpd.service && \
    sudo ntpdate pool.ntp.org && \
    sudo systemctl start ntpd.service
    ```

- To install the NTP service manually on the CentOS 7 system, run the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    sudo yum install ntp ntpdate && \
    sudo systemctl start ntpd.service && \
    sudo systemctl enable ntpd.service
    ```

### How to modify the supervision method of a process from `supervise` to `systemd`?

Run the following command:

{{< copyable "shell-root" >}}

```shell
process supervision, [systemd, supervise]
```

```
process_supervision = systemd
```

For versions earlier than TiDB 1.0.4, the TiDB Ansible supervision method of a process is `supervise` by default. The previously installed cluster can remain the same. If you need to change the supervision method to `systemd`, stop the cluster and run the following command:

{{< copyable "shell-regular" >}}

```shell
ansible-playbook stop.yml && \
ansible-playbook deploy.yml -D && \
ansible-playbook start.yml
```

### How to manually configure the SSH mutual trust and sudo without password?

1. Log in to the target machine respectively using the `root` user account, create the `tidb` user and set the login password.

    {{< copyable "shell-root" >}}

    ```shell
    useradd tidb && \
    passwd tidb
    ```

2. To configure sudo without password, run the following command, and add `tidb ALL=(ALL) NOPASSWD: ALL` to the end of the file:

    {{< copyable "shell-root" >}}

    ```shell
    visudo
    ```

    ```
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

3. Use the `tidb` user to log in to the control machine, and run the following command. Replace `172.16.10.61` with the IP of your target machine, and enter the `tidb` user password of the target machine as prompted. Successful execution indicates that SSH mutual trust is already created. This applies to other machines as well.

    {{< copyable "shell-regular" >}}

    ```shell
    ssh-copy-id -i ~/.ssh/id_rsa.pub 172.16.10.61
    ```

4. Log in to the control machine using the `tidb` user account, and log in to the IP of the target machine using SSH. If you do not need to enter the password and can successfully log in, then the SSH mutual trust is successfully configured.

    {{< copyable "shell-regular" >}}

    ```shell
    ssh 172.16.10.61
    ```

    ```
    [tidb@172.16.10.61 ~]$
    ```

5. After you login to the target machine using the `tidb` user, run the following command. If you do not need to enter the password and can switch to the `root` user, then sudo without password of the `tidb` user is successfully configured.

    {{< copyable "shell-regular" >}}

    ```shell
    sudo -su root
    ```

    ```
    [root@172.16.10.61 tidb]#
    ```

### Error: You need to install jmespath prior to running json_query filter

1. See [Install TiDB Ansible and its dependencies on the control machine](#step-4-install-tidb-ansible-and-its-dependencies-on-the-control-machine) and use `pip` to install TiDB Ansible and the corresponding dependencies in the control machine. The `jmespath` dependent package is installed by default.

2. Run the following command to check whether `jmespath` is successfully installed:

    {{< copyable "shell-regular" >}}

    ```bash
    pip show jmespath
    ```

3. Enter `import jmespath` in the Python interactive window of the control machine.

    - If no error displays, the dependency is successfully installed.
    - If the `ImportError: No module named jmespath` error displays, the Python `jmespath` module is not successfully installed.

    {{< copyable "shell-regular" >}}

    ```shell
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

### The `zk: node does not exist` error when starting Pump/Drainer

Check whether the `zookeeper_addrs` configuration in `inventory.ini` is the same with the configuration in the Kafka cluster, and whether the namespace is filled in. The description about namespace configuration is as follows:

```ini
# ZooKeeper connection string (see ZooKeeper docs for details).
# ZooKeeper address of the Kafka cluster. Example:
# zookeeper_addrs = "192.168.0.11:2181,192.168.0.12:2181,192.168.0.13:2181"
# You can also append an optional chroot string to the URLs to specify the root directory for all Kafka znodes. Example:
# zookeeper_addrs = "192.168.0.11:2181,192.168.0.12:2181,192.168.0.13:2181/kafka/123"
```
