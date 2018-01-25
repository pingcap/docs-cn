---
title: Ansible Deployment
category: operations
---

# Ansible Deployment

## Overview

Ansible is an IT automation tool. It can configure systems, deploy software, and orchestrate more advanced IT tasks such as continuous deployments or zero downtime rolling updates.

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

1. Several managed nodes with the following requirements:

    - 4 or more machines. At least 3 instances for TiKV. Do not deploy TiKV together with TiDB or PD on the same machine. See [Software and Hardware Requirements](recommendation.md).

    - Recommended Operating system:

      - CentOS 7.3 or later Linux
      - x86_64 architecture (AMD64)
      - ext4 filesystem

          Use ext4 filesystem for your data disks. Mount ext4 filesystem with the `nodelalloc` mount option. See [Mount the data disk ext4 filesystem with options](#mount-the-data-disk-ext4-filesystem-with-options).
    
    - The network between machines. Turn off the firewalls and iptables when deploying and turn them on after the deployment.

    - The same time and time zone for all machines with the NTP service on to synchronize the correct time. See [How to check whether the NTP service is normal](#how-to-check-whether-the-ntp-service-is-normal).

    - Create a normal user account as the user who runs the service. The user can sudo to root without a password.

2. A Control Machine with the following requirements:

    - The Control Machine can be one of the managed nodes.
    - It is recommended to install CentOS 7.3 or later version of Linux operating system (Python 2.7 involved by default).
    - The machine has access to the external network, used to download TiDB and relevant packages.
    - Configure mutual trust of `ssh authorized_key`. In the Control Machine, you can login the deployed target machine using `tidb` user account without a password.

## Install Ansible and dependencies in the Control Machine

Use the following method to install Ansible on the Control Machine of CentOS 7 system. Installation from the EPEL source includes Ansible dependencies automatically (such as `Jinja2==2.7.2 MarkupSafe==0.11`). After installation, you can view the version using `ansible --version`. 

> **Note:** Make sure that the Ansible version is **Ansible 2.3** or later, otherwise a compatibility issue occurs.

```bash
  # yum install epel-release
  # yum install ansible curl
  # ansible --version
    ansible 2.4.2.0
```

For other systems, see [Install Ansible](ansible-deployment.md#install-ansible).

## Download TiDB-Ansible to the Control Machine

Use the following command to download the corresponding version of TiDB-Ansible from GitHub [TiDB-Ansible project](https://github.com/pingcap/tidb-ansible). The default folder name is `tidb-ansible`.

Download the 1.0 version:

```
git clone -b release-1.0 https://github.com/pingcap/tidb-ansible.git
```

or

Download the master version:

```
git clone https://github.com/pingcap/tidb-ansible.git
```

> **Note:** For the production environment, download the 1.0 version to deploy TiDB.

## Orchestrate the TiDB cluster

The file path of `inventory.ini`: `tidb-ansible/inventory.ini`

The standard cluster has 6 machines:

- 2 TiDB nodes, the first TiDB machine is used as a monitor
- 3 PD nodes
- 3 TiKV nodes

### The cluster topology of single TiKV instance on a single machine

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

[monitored_servers:children]
tidb_servers
tikv_servers
pd_servers

[monitoring_servers]
172.16.10.1

[grafana_servers]
172.16.10.1
```


### The cluster topology of multiple TiKV instances on a single machine

Take three TiKV instances as an example:

| Name  | Host IP     | Services                  |
|:------|:------------|:--------------------------|
| node1 | 172.16.10.1 | PD1, TiDB1                |
| node2 | 172.16.10.2 | PD2, TiDB2                |
| node3 | 172.16.10.3 | PD3                       |
| node4 | 172.16.10.4 | TiKV1-1, TiKV1-2, TiKV1-3 |
| node5 | 172.16.10.5 | TiKV2-1, TiKV2-2, TiKV2-3 |
| node6 | 172.16.10.6 | TiKV3-1, TiKV3-2, TiKV3-3 |

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

[monitored_servers]
172.16.10.1
172.16.10.2
172.16.10.3
172.16.10.4
172.16.10.5
172.16.10.6

[monitoring_servers]
172.16.10.1

[grafana_servers]
172.16.10.1

......

[pd_servers:vars]
location_labels = ["host"]
```

> **Note:** For multiple TiKV instances on a single machine, it is required to modify `[monitored_servers:children]` to `[monitored_servers]`, with one IP address in a single row.

**Edit the parameters:**

1. For multiple TiKV instances, edit the `end-point-concurrency` and `block-cache-size` parameters in `conf/tikv.yml`:

    - `end-point-concurrency`: keep the number lower than CPU Vcores
    - `rocksdb defaultcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 30%
    - `rocksdb writecf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 45%
    - `rocksdb lockcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 2.5% (128 MB at a minimum)
    - `raftdb defaultcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 2.5% (128 MB at a minimum)

2. If multiple TiKV instances are deployed on a same physical disk, edit the `capacity` parameter in `conf/tikv.yml`:

    - `capacity`: (DISK - log space) / TiKV instance number (the unit is GB)

### Description of inventory.ini variables

| Variable | Description |
| ---- | ------- |
| cluster_name | the name of a cluster, adjustable |
| tidb_version | the version of TiDB, configured by default in TiDB-Ansible branches |
| deployment_method | the method of deployment, binary by default, Docker optional |
| process_supervision | the supervision way of processes, systemd by default, supervise optional |
| timezone | the timezone of the managed node, adjustable, `Asia/Shanghai` by default, used with the `set_timezone` variable |
| set_timezone | to edit the timezone of the managed node, True by default; False means closing |
| enable_elk | currently not supported |
| enable_firewalld | to enable the firewall, closed by default |
| enable_ntpd | to monitor the NTP service of the managed node, True by default; do not close it |
| machine_benchmark | to monitor the disk IOPS of the managed node, True by default; do not close it |
| set_hostname | to edit the hostname of the mananged node based on the IP, False by default |
| enable_binlog | whether to deploy Pump and enable the binlog, False by default, dependent on the Kafka cluster; see the `zookeeper_addrs` variable |
| zookeeper_addrs | the zookeeper address of the binlog Kafka cluster |
| enable_slow_query_log | to record the slow query log of TiDB into a single file: ({{ deploy_dir }}/log/tidb_slow_query.log). False by default, to record it into the TiDB log |
| deploy_without_tidb | the Key-Value mode, deploy only PD, TiKV and the monitoring service, not TiDB; set the IP of the tidb_servers host group to null in the `inventory.ini` file |

## Deploy the TiDB cluster

When `ansible-playbook` runs Playbook, the default concurrent number is 5. If many target machines are deployed, you can add the `-f` parameter to specify the concurrency, such as `ansible-playbook deploy.yml -f 10`.

The following example uses the `tidb` user account as the user who runs the service.

To deploy TiDB using a normal user account, take the following steps:

1. Edit the `tidb-ansible/inventory.ini` file to make sure `ansible_user = tidb`. 

    ```
    ## Connection
    # ssh via root:
    # ansible_user = root
    # ansible_become = true
    # ansible_become_user = tidb
    
    # ssh via normal user
    ansible_user = tidb
    ```

2. Connect to the network and download TiDB binary to the Control Machine using `local_prepare.yml` playbook.

    ```
    ansible-playbook local_prepare.yml
    ```

3. Initialize the system environment and modify the kernel parameters.

    ```
    ansible-playbook bootstrap.yml
    ```

    - If the remote connection using the normal user requires a password, add the `-k` (lower case) parameter.
    - If a password is required when the normal user gets root privileges from sudo, add the `-K` (upper case) parameter.
    - This applies to other playbooks as well.

        ```
        ansible-playbook bootstrap.yml -k -K
        ```

4. Deploy the TiDB cluster software.

    ```
    ansible-playbook deploy.yml
    ```

5. Start the TiDB cluster.

    ```
    ansible-playbook start.yml
    ```

> **Note:** If you want to deploy TiDB using the root user account, see [Ansible Deployment Using the Root User Account](op-guide/root-ansible-deployment.md).

## Test the cluster

It is recommended to configure load balancing to provide uniform SQL interface.

1. Connect to the TiDB cluster using the MySQL client.

    ```sql
    mysql -u root -h 172.16.10.1 -P 4000
    ```

    > **Note**: The default port of TiDB service is 4000.

2. Access the monitoring platform using a web browser.

    ```
    http://172.16.10.1:3000
    ```

    The default account and password: `admin`/`admin`.

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

1. To apply rolling update to a specific service, such as TiKV.

    ```
    ansible-playbook rolling_update.yml --tags=tikv
    ```

2. To apply rolling update to all the services.

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
● ntpd.service - Network Time Service
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

Running the following command can promote the starting of the NTP service synchronization. You can replace `pool.ntp.org` with the NTP server.

```
$ sudo systemctl stop ntpd.service
$ sudo ntpdate pool.ntp.org
$ sudo systemctl start ntpd.service
```

### How to deploy TiDB using Docker?

- Install Docker on the Control Machine and the managed node. The normal user (such as `ansible_user = tidb`) account in `inventory.ini` must have the sudo privileges or [running Docker privileges](https://docs.docker.com/engine/installation/linux/linux-postinstall/).
- Install the `docker-py` module on the Control Machine and the managed node.

    ```
    sudo pip install docker-py
    ```

- Edit the `inventory.ini` file:

    ```
    # deployment methods, [binary, docker]
    deployment_method = docker
    
    # process supervision, [systemd, supervise]
    process_supervision = systemd
    ```

The Docker installation process is similar to the binary method.

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
- For the Ubuntu system, install Ansible using PPA source:

    ```bash
    sudo add-apt-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible
    ```

- For other systems, see the [official Ansible document](http://docs.ansible.com/ansible/intro_installation.html).

### Mount the data disk ext4 filesystem with options

Format your data disks to ext4 filesystem and mount the filesystem with the `nodelalloc` and `noatime` options. It is required to mount the `nodelalloc` option, or else the Ansible deployment cannot pass the detection. The `noatime` option is optional. 

Take the `/dev/nvme0n1` data disk as an example:

```
# vi /etc/fstab
/dev/nvme0n1 /data1 ext4 defaults,nodelalloc,noatime 0 2
```
