---
title: Deploy TiDB Using Ansible
category: operations
---

# Deploy TiDB Using Ansible

## Overview

Ansible is an IT automation tool that can configure systems, deploy software, and orchestrate more advanced IT tasks such as continuous deployments or zero downtime rolling updates.

[TiDB-Ansible](https://github.com/pingcap/tidb-ansible) is a TiDB cluster deployment tool developed by PingCAP, based on Ansible playbook. TiDB-Ansible enables you to quickly deploy a new TiDB cluster which includes PD, TiDB, TiKV, and the cluster monitoring modules.

You can use the TiDB-Ansible configuration file to set up the cluster topology, completing all operation tasks with one click, including:

- Initializing operating system parameters
- Deploying the components
- Rolling upgrade, including module survival detection
- Cleaning data
- Cleaning environment
- Configuring monitoring modules

## Prepare

Before you start, make sure that you have:

1. Several target machines that meet the following requirements:

    - 4 or more machines
    
        A standard TiDB cluster contains 6 machines. You can use 4 machines for testing.

    - CentOS 7.3 (64 bit) or later with Python 2.7 installed, x86_64 architecture (AMD64), ext4 filesystem

        Use ext4 filesystem for your data disks. Mount ext4 filesystem with the `nodelalloc` mount option. See [Mount the data disk ext4 filesystem with options](#mount-the-data-disk-ext4-filesystem-with-options).

    - Network between machines.

    - Same time and time zone for all machines with the NTP service on to synchronize the correct time
    
        See [How to check whether the NTP service is normal](#how-to-check-whether-the-ntp-service-is-normal).

    - Create a normal `tidb` user account as the user who runs the service
    
        The `tidb` user can sudo to the root user without a password. See [How to configure SSH mutual trust and sudo without password](#how-to-configure-ssh-mutual-trust-and-sudo-without-password).

    > **Note:** When you deploy TiDB using Ansible, use SSD disks for the data directory of TiKV and PD nodes.

2. A Control Machine with the following requirements:

    > **Note:** The Control Machine can be one of the target machines.
    
    - CentOS 7.3 (64 bit) or later with Python 2.7 installed
    - Access to the Internet
    - Git installed
    - SSH Mutual Trust configured
    
        In the Control Machine, you can log in to the deployment target machine using the `tidb` user account without a password. See [How to configure SSH mutual trust and sudo without password](#how-to-configure-ssh-mutual-trust-and-sudo-without-password).

## Step 1: Download TiDB-Ansible to the Control Machine

1. Log in to the Control Machine using the `tidb` user account and enter the `/home/tidb` directory.

2. Download the corresponding TiDB-Ansible version. The default folder name is `tidb-ansible`.

    - Download the 2.0 GA version:

        ```bash
        git clone -b release-2.0 https://github.com/pingcap/tidb-ansible.git
        ```
    
    - Download the master version:

        ```bash
        git clone https://github.com/pingcap/tidb-ansible.git
        ```

    If you have questions regarding which version to use, email to info@pingcap.com for more information or [file an issue](https://github.com/pingcap/tidb-ansible/issues/new).

## Step 2: Install Ansible and dependencies on the Control Machine

1. Install Ansible and the dependencies on the Control Machine:

    ```bash
    sudo yum -y install epel-release
    sudo yum -y install python-pip curl
    cd tidb-ansible
    sudo pip install -r ./requirements.txt
    ```

    Ansible and related dependencies are in the `tidb-ansible/requirements.txt` file.

2. View the version of Ansible:

    ```bash
    ansible --version
    ```

    Currently, the 1.0 GA version depends on Ansible 2.4, while the 2.0 GA version and the master version are compatible with Ansible 2.4 and Ansible 2.5.

For other systems, see [Install Ansible](ansible-deployment.md#install-ansible).

## Step 3: Edit the `inventory.ini` file to orchestrate the TiDB cluster

Edit the `tidb-ansible/inventory.ini` file to orchestrate the TiDB cluster. The standard TiDB cluster contains 6 machines: 2 TiDB modes, 3 PD nodes and 3 TiKV nodes.

- Deploy at least 3 instances for TiKV.
- Do not deploy TiKV together with TiDB or PD on the same machine.
- Use the first TiDB machine as the monitoring machine.

> **Note:** It is required to use the internal IP address to deploy.

You can choose one of the following two types of cluster topology according to your scenario:

- [The cluster topology of a single TiKV instance on each TiKV node](#option-1-use-the-cluster-topology-of-a-single-tikv-instance-on-each-tikv-node)

    In most cases, it is recommended to deploy one TiKV instance on each TiKV node for better performance. However, if the CPU and memory of your TiKV machines are much better than the required in [Hardware and Software Requirements](../op-guide/recommendation.md), and you have more than two disks in one node or the capacity of one SSD is larger than 2 TB, you can deploy no more than 2 TiKV instances on a single TiKV node.

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

[pd_servers:vars]
location_labels = ["host"]
```

**Edit the parameters in the service configuration file:**

1. For the cluster topology of multiple TiKV instances on each TiKV node, you need to edit the `block-cache-size` parameter in `tidb-ansible/conf/tikv.yml`:

    - `rocksdb defaultcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 30%
    - `rocksdb writecf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 45%
    - `rocksdb lockcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 2.5% (128 MB at a minimum)
    - `raftdb defaultcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 2.5% (128 MB at a minimum)

2. For the cluster topology of multiple TiKV instances on each TiKV node, you need to edit the `high-concurrency`, `normal-concurrency` and `low-concurrency` parameters in the `tidb-ansible/conf/tikv.yml` file:

    ```
    readpool:
    coprocessor:
        # Notice: if CPU_NUM > 8, default thread pool size for coprocessors
        # will be set to CPU_NUM * 0.8.
        # high-concurrency: 8
        # normal-concurrency: 8
        # low-concurrency: 8
    ```

    Recommended configuration: `number of instances * parameter value = CPU_Vcores * 0.8`.

3. If multiple TiKV instances are deployed on a same physical disk, edit the `capacity` parameter in `conf/tikv.yml`:

    - `capacity`: (total disk capacity - log space) / TiKV instance number (the unit is GB)

## Step 4: Edit variables in the `inventory.ini` file

Edit the `deploy_dir` variable to configure the deployment directory.

The global variable is set to `/home/tidb/deploy` by default, and it applies to all services. If the data disk is mounted on the `/data1` directory, you can set it to `/data1/deploy`. For example:

```bash
## Global variables
[all:vars]
deploy_dir = /data1/deploy
```

**Note:** To separately set the deployment directory for a service, you can configure the host variable while configuring the service host list in the `inventory.ini` file. It is required to add the first column alias, to avoid confusion in scenarios of mixed services deployment.

```bash
TiKV1-1 ansible_host=172.16.10.4 deploy_dir=/data1/deploy
```

### Description of other variables

To enable the following control variables, use the capitalized `True`. To disable the following control variables, use the capitalized `False`.

| Variable | Description |
| ---- | ------- |
| cluster_name | the name of a cluster, adjustable |
| tidb_version | the version of TiDB, configured by default in TiDB-Ansible branches |
| process_supervision | the supervision way of processes, systemd by default, supervise optional |
| timezone | the timezone of the managed node, adjustable, `Asia/Shanghai` by default, used with the `set_timezone` variable |
| set_timezone | to edit the timezone of the managed node, True by default; False means closing |
| enable_elk | currently not supported |
| enable_firewalld | to enable the firewall, closed by default |
| enable_ntpd | to monitor the NTP service of the managed node, True by default; do not close it |
| set_hostname | to edit the hostname of the mananged node based on the IP, False by default |
| enable_binlog | whether to deploy Pump and enable the binlog, False by default, dependent on the Kafka cluster; see the `zookeeper_addrs` variable |
| zookeeper_addrs | the zookeeper address of the binlog Kafka cluster |
| enable_slow_query_log | to record the slow query log of TiDB into a single file: ({{ deploy_dir }}/log/tidb_slow_query.log). False by default, to record it into the TiDB log |
| deploy_without_tidb | the Key-Value mode, deploy only PD, TiKV and the monitoring service, not TiDB; set the IP of the tidb_servers host group to null in the `inventory.ini` file |
| alertmanager_target | optional: If you have deployed `alertmanager` separately, you can configure this variable using the `alertmanager_host:alertmanager_port` format |
| grafana_admin_user | the username of Grafana administrator; default `admin` |
| grafana_admin_password | the password of Grafana administrator account; default `admin`; used to import Dashboard and create the API key using Ansible; update this variable after you modify it through Grafana web |

## Step 5: Deploy the TiDB cluster

When `ansible-playbook` runs Playbook, the default concurrent number is 5. If many deployment target machines are deployed, you can add the `-f` parameter to specify the concurrency, such as `ansible-playbook deploy.yml -f 10`.

The following example uses `tidb` as the user who runs the service.

1. Edit the `tidb-ansible/inventory.ini` file to make sure `ansible_user = tidb`.

    ```
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

    Run the following command and if all servers return `tidb`, then the SSH mutual trust is successfully configured:

    ```
    ansible -i inventory.ini all -m shell -a 'whoami'
    ```

    Run the following command and if all servers return `root`, then sudo without password of the `tidb` user is successfully configured:

    ```
    ansible -i inventory.ini all -m shell -a 'whoami' -b
    ```

2. Run the `local_prepare.yml` playbook, connect to the Internet and download TiDB binary to the Control Machine.

    ```
    ansible-playbook local_prepare.yml
    ```

3. Initialize the system environment and modify the kernel parameters.

    ```
    ansible-playbook bootstrap.yml
    ```

4. Deploy the TiDB cluster software.

    ```
    ansible-playbook deploy.yml
    ```

    > **Note:** You can use the `Report` button on the Grafana Dashboard to generate the PDF file. This function depends on the `fontconfig` package. To use this function, login to the `grafana_servers` machine and install it using the following command:
    >
    > ```
    > $ sudo yum install fontconfig
    > ```

5. Start the TiDB cluster.

    ```
    ansible-playbook start.yml
    ```

> **Note:** If you want to deploy TiDB using the root user account, see [Ansible Deployment Using the Root User Account](root-ansible-deployment.md).

## Test the cluster

Because TiDB is compatible with MySQL, you must use the MySQL client to connect to TiDB directly. It is recommended to configure load balancing to provide uniform SQL interface.

1. Connect to the TiDB cluster using the MySQL client.

    ```sql
    mysql -u root -h 172.16.10.1 -P 4000
    ```

    > **Note**: The default port of TiDB service is 4000.

2. Access the monitoring platform using a web browser.

    ```
    http://172.16.10.1:3000
    ```

    > **Note**: The default account and password: `admin`/`admin`.

## Perform rolling update

- The rolling update of the TiDB service does not impact the ongoing business. Minimum requirements: `pd*3, tidb*2, tikv*3`.
- **If the `pump`/`drainer` services are running in the cluster, stop the `drainer` service before rolling update. The rolling update of the TiDB service automatically updates the `pump` service.**

### Download the binary automatically

1. Edit the value of the `tidb_version` parameter in `inventory.ini`, and specify the version number you need to update to. The following example specifies the version number as `v1.0.2`:

    ```
    tidb_version = v1.0.2
    ```

2. Delete the existing downloads directory `tidb-ansible/downloads/`.

    ```
    rm -rf downloads
    ```

3. Use `playbook` to download the TiDB 1.0 binary and replace the existing binary in `tidb-ansible/resource/bin/` automatically.

    ```
    ansible-playbook local_prepare.yml
    ```

### Download the binary manually

You can also download the binary manually. Use `wget` to download the binary and replace the existing binary in `tidb-ansible/resource/bin/` manually.

```
wget http://download.pingcap.org/tidb-v1.0.0-linux-amd64-unportable.tar.gz
```

> **Note:** Remember to replace the version number in the download link.

### Use Ansible for rolling update

- Apply rolling update to the TiKV node (only update the TiKV service).

    ```
    ansible-playbook rolling_update.yml --tags=tikv
    ```

- Apply rolling update to the PD node (only update single PD service).

    ```
    ansible-playbook rolling_update.yml --tags=pd
    ```

- Apply rolling update to the TiDB node (only update single TiDB service).

    ```
    ansible-playbook rolling_update.yml --tags=tidb
    ```

- Apply rolling update to all services.

    ```
    ansible-playbook rolling_update.yml
    ```

## Summary of common operations

| Job                               | Playbook                                 |
|:----------------------------------|:-----------------------------------------|
| Start the cluster                 | `ansible-playbook start.yml`             |
| Stop the cluster                  | `ansible-playbook stop.yml`              |
| Destroy the cluster               | `ansible-playbook unsafe_cleanup.yml` (If the deployment directory is a mount point, an error will be reported, but implementation results will remain unaffected) |
| Clean data (for test)             | `ansible-playbook unsafe_cleanup_data.yml` |
| Rolling Upgrade                   | `ansible-playbook rolling_update.yml`    |
| Rolling upgrade TiKV              | `ansible-playbook rolling_update.yml --tags=tikv` |
| Rolling upgrade modules except PD | `ansible-playbook rolling_update.yml --skip-tags=pd` |
| Rolling update the monitoring components | `ansible-playbook rolling_update_monitor.yml` |

## FAQ

### How to download and install TiDB of a specified version?

If you need to install the TiDB 1.0.4 version, download the `TiDB-Ansible release-1.0` branch and make sure `tidb_version = v1.0.4` in the `inventory.ini` file. For installation procedures, see the above description in this document.

Download the `TiDB-Ansible release-1.0` branch from GitHub:

```
git clone -b release-1.0 https://github.com/pingcap/tidb-ansible.git
```

### How to customize the port?

Edit the `inventory.ini` file and add the following host variable after the IP of the corresponding service:

| Component     | Variable Port      | Default Port | Description              |
|:--------------|:-------------------|:-------------|:-------------------------|
| TiDB          | tidb_port          | 4000         | the communication port for the application and DBA tools |
| TiDB          | tidb_status_port   | 10080        | the communication port to report TiDB status |
| TiKV          | tikv_port          | 20160        | the TiKV communication port |
| PD            | pd_client_port     | 2379         | the communication port between TiDB and PD |
| PD            | pd_peer_port       | 2380         | the inter-node communication port within the PD cluster |
| Pump          | pump_port          | 8250         | the pump communication port |
| Prometheus    | prometheus_port    | 9090         | the communication port for the Prometheus service |
| Pushgateway   | pushgateway_port   | 9091         | the aggregation and report port for TiDB, TiKV, and PD monitor |
| node_exporter | node_exporter_port | 9100         | the communication port to report the system information of every TiDB cluster node |
| Grafana       | grafana_port       | 3000         | the port for the external Web monitoring service and client (Browser) access |
| Grafana | grafana_collector_port | 8686 | the grafana_collector communication port, used to export Dashboard as the PDF format |

### How to customize the deployment directory?

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
| pushgateway   | pushgateway_log_dir   | {{ deploy_dir }}/log          | the pushgateway log directory |
| node_exporter | node_exporter_log_dir | {{ deploy_dir }}/log          | the node_exporter log directory |
| Grafana       | grafana_log_dir       | {{ deploy_dir }}/log          | the Grafana log directory |
| Grafana       | grafana_data_dir      | {{ deploy_dir }}/data.grafana | the Grafana data directory |

### How to check whether the NTP service is normal?

Run the following command. If it returns `running`, then the NTP service is running:

```
$ sudo systemctl status ntpd.service
  ntpd.service - Network Time Service
   Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
   Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago
```

Run the ntpstat command. If it returns `synchronised to NTP server` (synchronizing with the NTP server), then the synchronization process is normal.

```
$ ntpstat
synchronised to NTP server (85.199.214.101) at stratum 2
   time correct to within 91 ms
   polling server every 1024 s
```

> **Note:** For the Ubuntu system, install the `ntpstat` package.

The following condition indicates the NTP service is not synchronized normally:

```
$ ntpstat
unsynchronised
```

The following condition indicates the NTP service is not running normally:

```
$ ntpstat
Unable to talk to NTP daemon. Is it running?
```

Running the following command can promote the starting of the NTP service synchronization. You can replace `pool.ntp.org` with other NTP server.

```
$ sudo systemctl stop ntpd.service
$ sudo ntpdate pool.ntp.org
$ sudo systemctl start ntpd.service
```

### How to deploy the NTP service using Ansible?

Refer to [Download TiDB-Ansible to the Control Machine](#download-tidb-ansible-to-the-control-machine) and download TiDB-Ansible. Add the IP of the deployment target machine to `[servers]`. You can replace the `ntp_server` variable value `pool.ntp.org` with other NTP server. Before starting the NTP service, the system `ntpdate` the NTP server. The NTP service deployed by Ansible uses the default server list in the package. See the `server` parameter in the `cat /etc/ntp.conf` file.

```
$ vi hosts.ini
[servers]
172.16.10.49
172.16.10.50
172.16.10.61
172.16.10.62

[all:vars]
username = tidb
ntp_server = pool.ntp.org
```

Run the following command, and enter the root password of the deployment target machine as prompted:

```
$ ansible-playbook -i hosts.ini deploy_ntp.yml -k
```

### How to install the NTP service manually?

Run the following command on the CentOS 7 system:

```
$ sudo yum install ntp ntpdate
$ sudo systemctl start ntpd.service
```

### How to adjust the supervision method of a process from supervise to systemd?

```
# process supervision, [systemd, supervise]
process_supervision = systemd
```

For versions earlier than TiDB 1.0.4, the TiDB-Ansible supervision method of a process is supervise by default. The previously installed cluster can remain the same. If you need to change the supervision method to systemd, close the cluster and run the following command:

```
ansible-playbook stop.yml
ansible-playbook deploy.yml -D
ansible-playbook start.yml
```

#### How to install Ansible?

- For the CentOS system, install Ansible following the method described at the beginning of this document.
- For the Ubuntu system, install Ansible as follows:

    ```bash
    $ sudo apt-get install python-pip curl
    $ cd tidb-ansible
    $ sudo pip install -r ./requirements.txt
    ```

### Mount the data disk ext4 filesystem with options

Format your data disks to ext4 filesystem and mount the filesystem with the `nodelalloc` and `noatime` options. It is required to mount the `nodelalloc` option, or else the Ansible deployment cannot pass the detection. The `noatime` option is optional.

Take the `/dev/nvme0n1` data disk as an example:

1. Edit the `/etc/fstab` file and add the `nodelalloc` mount option:

    ```
    # vi /etc/fstab
    /dev/nvme0n1 /data1 ext4 defaults,nodelalloc,noatime 0 2
    ```

2. Umount the mount directory and remount using the following command:

    ```
    # umount /data1
    # mount -a
    ```

3. Check using the following command: 

    ```
    # mount -t ext4
    /dev/nvme0n1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
    ```

### How to configure SSH mutual trust and sudo without password?

#### Create the `tidb` user on the Control Machine and generate the SSH key.

```
# useradd tidb
# passwd tidb
# su - tidb
$
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

#### How to automatically configure SSH mutual trust and sudo without password using Ansible?

Refer to [Download TiDB-Ansible to the Control Machine](#download-tidb-ansible-to-the-control-machine) and download TiDB-Ansible. Add the IP of the deployment target machine to `[servers]`.

```
$ vi hosts.ini
[servers]
172.16.10.49
172.16.10.50
172.16.10.61
172.16.10.62

[all:vars]
username = tidb
```

Run the following command, and enter the `root` password of the deployment target machine as prompted:

```
$ ansible-playbook -i hosts.ini create_users.yml -k
```

#### How to manually configure SSH mutual trust and sudo without password?

Use the `root` user to login to the deployment target machine, create the `tidb` user and set the login password.

```
# useradd tidb
# passwd tidb
```

To configure sudo without password, run the following command, and add `tidb ALL=(ALL) NOPASSWD: ALL` to the end of the file:

```
# visudo
tidb ALL=(ALL) NOPASSWD: ALL
```

Use the `tidb` user to login to the Control Machine, and run the following command. Replace `172.16.10.61` with the IP of your deployment target machine, and enter the `tidb` user password of the deployment target machine. Successful execution indicates that SSH mutual trust is already created. This applies to other machines as well.

```
[tidb@172.16.10.49 ~]$ ssh-copy-id -i ~/.ssh/id_rsa.pub 172.16.10.61
```

#### Authenticate SSH mutual trust and sudo without password

Use the `tidb` user to login to the Control Machine, and login to the IP of the target machine using SSH. If you do not need to enter the password and can successfully login, then SSH mutual trust is successfully configured.

```
[tidb@172.16.10.49 ~]$ ssh 172.16.10.61
[tidb@172.16.10.61 ~]$
```

After you login to the deployment target machine using the `tidb` user, run the following command. If you do not need to enter the password and can switch to the `root` user, then sudo without password of the `tidb` user is successfully configured.

```
[tidb@172.16.10.61 ~]$ sudo -su root
[root@172.16.10.61 tidb]#
```

### Error: You need to install jmespath prior to running json_query filter

See [Install Ansible and dependencies in the Control Machine](#install-ansible-and-dependencies-in-the-control-machine) and use `pip` to install Ansible and the related specific dependencies in the Control Machine. The `jmespath` dependent package is installed by default.

For the CentOS 7 system, you can install `jmespath` separately using the following command:

```
$ sudo yum -y install epel-release
$ sudo yum -y install python-pip
$ sudo pip install jmespath
$ pip show jmespath
Name: jmespath
Version: 0.9.0
```

Enter `import jmespath` in the Python interactive window of the Control Machine.

- If no error displays, the dependency is successfully installed.
- If the `ImportError: No module named jmespath` error displays, the Python `jmespath` module is not successfully installed.

```
$ python
Python 2.7.5 (default, Nov  6 2016, 00:28:07)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import jmespath
```

For the Ubuntu system, you can install `jmespath` separately using the following command:

```
$ sudo apt-get install python-pip
$ sudo pip install jmespath
```

### The `zk: node does not exist` error when starting Pump/Drainer

Check whether the `zookeeper_addrs` configuration in `inventory.ini` is the same with the configuration in the Kafka cluster, and whether the namespace is filled in. The description about namespace configuration is as follows:

```
# ZooKeeper connection string (see ZooKeeper docs for details).
# ZooKeeper address of the Kafka cluster. Example:
# zookeeper_addrs = "192.168.0.11:2181,192.168.0.12:2181,192.168.0.13:2181"
# You can also append an optional chroot string to the URLs to specify the root directory for all Kafka znodes. Example:
# zookeeper_addrs = "192.168.0.11:2181,192.168.0.12:2181,192.168.0.13:2181/kafka/123"
```
