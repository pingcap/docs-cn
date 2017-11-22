---
title: TiDB Ansible Deployment
category: operations
---

# Ansible Deployment

## Overview

Ansible is an IT automation tool. It can configure systems, deploy software, and orchestrate more advanced IT tasks such as continuous deployments or zero downtime rolling updates.

[TiDB-Ansible](https://github.com/pingcap/tidb-ansible) is a TiDB cluster deployment tool developed by PingCAP, based on Ansible playbook. TiDB-Ansible enables you to quickly deploy a new TiDB cluster which includes PD, TiDB, TiKV, and the cluster monitoring modules.

You can use the TiDB-Ansible configuration file to set up the cluster topology, completing all operation tasks with one click, including:

- Initializing the system, including creating a user for deployment, setting up a hostname, etc.
- Deploying the components
- Rolling upgrade, including module survival detection
- Cleaning data
- Cleaning environment
- Configuring monitoring modules


## Prepare

Before you start, make sure that you have:

1. A Control Machine with the following requirements:

    - Python 2.6 or Python 2.7
    - Python Jinja2 2.7.2 and MarkupSafe 0.11 packages. You can use the following commands to install the packages:

      ```
      pip install Jinja2==2.7.2 MarkupSafe==0.11
      ```

    - Access to the external network to install curl package and download binary.
    - Access to the managed nodes via SSH using password login or SSH authorized_key login.

2. Several managed nodes with the following requirements:

    - 4 or more machines. At least 3 instances for TiKV. Don’t deploy TiKV together with TiDB or PD on the same machine. See [deploying recommendations](https://github.com/pingcap/docs/blob/master/op-guide/recommendation.md).

    - Recommended Operating system:

      - CentOS 7.3 or later

      - X86_64 architecture (AMD64)

      - Kernel version 3.10 or later

      - Ext4 file system.

    - The network between machines. Turn off the firewalls and iptables when deploying and turn them on after the deployment.

    - The same time and time zone for all machines with the NTP service on to synchronize the correct time. If you are using the Ubuntu platform, install the ntpstat package.

    - A remote user account which you can use to login from the Control Machine to connect to the managed nodes via SSH. It can be the root user or a user account with sudo privileges.

    - Python 2.6 or Python 2.7

> **Note**: The Control Machine can be one of the managed nodes.

## Install Ansible in the Control Machine

Install Ansible 2.3 or later to your platform:

- PPA source on Ubuntu:

    ```
    sudo add-apt-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible
    ```

- EPEL source on CentOS:

    ```
    yum install epel-release
    yum update
    yum install ansible
    ```

You can use the `ansible --version` command to see the version information.

For more information, see [Ansible Documentation](http://docs.ansible.com/ansible/intro_installation.html).

## Download TiDB-Ansible to the Control Machine

Use the following command to download the TiDB-Ansible `release-1.0` branch from GitHub [TiDB-Ansible project](https://github.com/pingcap/tidb-ansible).
The default folder name is `tidb-ansible`. The `tidb-ansible` directory contains all files you need to get started with TiDB-Ansible.

```
git clone -b release-1.0 https://github.com/pingcap/tidb-ansible.git
```


## Orchestrate the TiDB cluster

The file path of `inventory.ini`: `tidb-ansible/inventory.ini`

The standard cluster has 6 machines:

- 2 TiDB nodes, the first TiDB machine is used as a monitor
- 3 PD nodes
- 3 TiKV nodes

### The Cluster Topology of Single TiKV Instance on a Single Machine

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


### The Cluster Topology of Multiple TiKV Instances on a Single Machine

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

[monitored_servers:children]
tidb_servers
tikv_servers
pd_servers

[monitoring_servers]
172.16.10.1

[grafana_servers]
172.16.10.1

......

[pd_servers:vars]
location_labels = ["host"]
```

**Edit the parameters:**

1. For multiple TiKV instances, edit the `end-point-concurrency` and `block-cache-size` parameters in `conf/tikv.yml`:

    - `end-point-concurrency`: keep the number lower than CPU Vcores
    - `rocksdb defaultcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 30%
    - `rocksdb writecf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 45%
    - `rocksdb lockcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 2.5% (128 MB at a minimum)
    - `raftdb defaultcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 2.5% (128 MB at a minimum)

2. If multiple TiKV instances are deployed on a same physical disk, edit the `capacity` parameter in `conf/tikv.yml`:

    - `capaticy`: (DISK - log space) / TiKV instance number (the unit is GB)

## Deploy the TiDB Cluster

> **Note**:
>
> 1. It is not recommended to use the root user account to deploy TiDB.
> 2. The remote Ansible user (the `ansible_user` in the `incentory.ini` file) can use either the root user account or a normal user account with sudo privileges to deploy TiDB.

Descriptions about the two circumstances are as follows.

- Use the root user account to deploy TiDB.

    > **Note**: The following example uses the `tidb` user account as the user who runs the service.

    1. Edit `inventory.ini` as follows.

        Remove the code comments for `ansible_user = root`, `ansible_become = true` and `ansible_become_user`. Add comments for `ansible_user = tidb`.

        ```
        ## Connection
        # ssh via root:
        ansible_user = root
        ansible_become = true
        ansible_become_user = tidb

        # ssh via normal user
        # ansible_user = tidb
        ```

    2. Connect to the network and download TiDB binary to the Control Machine.

        ```
        ansible-playbook local_prepare.yml
        ```

    3. Initialize the system environment and edit the kernel parameters.

        ```
        ansible-playbook bootstrap.yml
        ```

        > **Note**: If the service user does not exist, the initialization operation will automatically create the user.

        If the remote connection using the root user requires a password, use the `-k` (lower case) parameter. This applies to other playbooks as well:

        ```
        ansible-playbook bootstrap.yml -k
        ```

    4. Deploy the TiDB cluster.

        ```
        ansible-playbook deploy.yml -k
        ```

    5. Start the TiDB cluster.

        ```
        ansible-playbook start.yml -k
        ```

- Use the normal user with  to deploy TiDB.

    > **Note**: Before the deployment, you should create the normal `tidb` user account and add the sudo privileges. The following example uses the `tidb` user account as the user who runs the service.

    1. Edit the `inventory.ini` file.

        ```
        ## Connection
        # ssh via root:
        # ansible_user = root
        # ansible_become = true
        # ansible_become_user = tidb
        # ssh via normal user
        ansible_user = tidb
        ```

    2. Connect to the network and download TiDB binary to the Control Machine.

        ```
        ansible-playbook local_prepare.yml
        ```

    3. Initialize the system environment and modify the kernel parameters.

        ```
        ansible-playbook bootstrap.yml -k -K
        ```

        If the remote connection using the normal user requires a password, add the `-k` (lower case) parameter. This applies to other playbooks as well:

        ```
        ansible-playbook bootstrap.yml -k
        ```

        The execution of this playbook requires root privileges. If a password is needed when the normal user gets root privileges from sudo, add the `-K` (upper case) parameter:

        ```
        ansible-playbook bootstrap.yml -k -K
        ```

    4. Deploy the TiDB cluster.

        ```
        ansible-playbook deploy.yml -k
        ```

    5. Start the TiDB cluster.

        ```
        ansible-playbook start.yml -k
        ```

## Test the Cluster

It is recommended to configure load balancing to provide uniform SQL interface.

1. Connect to the TiDB cluster using the MySQL client.

    ```
    mysql -u root -h 172.16.10.1 -P 4000
    ```

    > **Note**: The default port of TiDB service is 4000.

2. Access the monitoring platform using a web browser.

    ```
    http://172.16.10.1:3000
    ```

    The default account and password: `admin/admin`.

## Perform Rolling Update

- The rolling update of the TiDB service does not impact the ongoing business. Minimum requirements: `pd*3, tidb*2, tikv*3`.
- For remote connection privileges, see the procedures described in the above section. But if the mutual authentication is already set up, you don't need to add the `-k` parameter.
- If the `pump`/`drainer` services are running in the cluster, it is recommended to stop the `drainer` service first before the rolling update. The rolling update of the TiDB service automatically updates the `pump` service.

### Download the Binary

1. Use `playbook` to download the TiDB 1.0 binary and replace the existing binary in `tidb-ansible/resource/bin/` automatically.

    ```
    ansible-playbook local_prepare.yml
    ```

2. Use `wget` to download the binary and replace the existing binary in `tidb-ansible/resource/bin/` manually.

    ```
    wget http://download.pingcap.org/tidb-v1.0.0-linux-amd64-unportable.tar.gz
    ```

### Use Ansible for Rolling Update

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
| Clean data (for test)             | `ansible-playbook cleanup_data.yml`      |
| Rolling Upgrade                   | `ansible-playbook rolling_update.yml`    |
| Rolling upgrade TiKV              | `ansible-playbook rolling_update.yml --tags=tikv` |
| Rolling upgrade modules except PD | `ansible-playbook rolling_update.yml --skip-tags=pd` |

For more advanced features of TiDB including data migration, performance tuning, etc., see [TiDB Documents](https://github.com/pingcap/docs).

## FAQ

### The download links for various TiDB versions.

- 1.0 version:
  - [TiDB 1.0-CentOS7](http://download.pingcap.org/tidb-v1.0.0-linux-amd64-unportable.tar.gz)
  - [TiDB 1.0-CentOS6](http://download.pingcap.org/tidb-v1.0.0-linux-amd64-unportable-centos6.tar.gz)

### How to download and install TiDB of a specified version?

If you need to install TiDB 1.0 version, download the `TiDB-Ansible release-1.0` branch and make sure `tidb_version = v1.0.0` in the `inventory.ini` file. For installation procedures, see the above description in this document.

Download the `TiDB-Ansible release-1.0` branch from GitHub:

```
git clone -b release-1.0 https://github.com/pingcap/tidb-ansible.git
```

### Custom Port

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

### Custom Deployment Directory

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
