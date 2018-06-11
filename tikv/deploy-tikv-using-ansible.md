---
title: Install and Deploy TiKV Using Ansible
category: user guide
---

# Install and Deploy TiKV Using Ansible

This guide describes how to install and deploy TiKV using Ansible. Ansible is an IT automation tool that can configure systems, deploy software, and orchestrate more advanced IT tasks such as continuous deployments or zero downtime rolling updates.

[TiDB-Ansible](https://github.com/pingcap/tidb-ansible) is a TiDB cluster deployment tool developed by PingCAP, based on Ansible playbook. TiDB-Ansible enables you to quickly deploy a new TiKV cluster which includes PD, TiKV, and the cluster monitoring modules.

## Prerequisites

1. Several target machines that meet the following requirements:

    - 4 or more machines

        A standard TiKV cluster contains 6 machines. You can use 4 machines for testing.

    - CentOS 7.3 (64 bit) or later with Python 2.7 installed, x86_64 architecture (AMD64), ext4 filesystem

        Use ext4 filesystem for your data disks. Mount ext4 filesystem with the `nodelalloc` mount option. See [Mount the data disk ext4 filesystem with options](../op-guide/ansible-deployment#mount-the-data-disk-ext4-filesystem-with-options).

    - Network between machines
    
    - Same time and time zone for all machines with the NTP service on to synchronize the correct time
    
        See [How to check whether the NTP service is normal](../op-guide/ansible-deployment#how-to-check-whether-the-ntp-service-is-normal).

    - Create a normal `tidb` user account as the user who runs the service
    
        The `tidb` user can sudo to the root user without a password. See [How to configure SSH mutual trust and sudo without password](../op-guide/ansible-deployment#how-to-configure-ssh-mutual-trust-and-sudo-without-password).
    
    > **Note:** When you deploy TiKV using Ansible, use SSD disks for the data directory of TiKV and PD nodes.

2. A Control Machine that meets the following requirements:

    > **Note:** The Control Machine can be one of the target machines.
    
    - CentOS 7.3 (64 bit) or later with Python 2.7 installed
    - Access to the Internet
    - Git installed
    - SSH Mutual Trust configured

        In the Control Machine, you can log in to the deployment target machine using the `tidb` user account without a password. See [How to configure SSH mutual trust and sudo without password](../op-guide/ansible-deployment#how-to-configure-ssh-mutual-trust-and-sudo-without-password).

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

## Step 2: Install Ansible and the dependencies on the Control Machine

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

## Step 3: Edit the `inventory.ini` file to orchestrate the TiKV cluster

Edit the `tidb-ansible/inventory.ini` file to orchestrate the TiKV cluster. The standard TiKV cluster contains 6 machines: 3 PD nodes and 3 TiKV nodes.

- Deploy at least 3 instances for TiKV.
- Do not deploy TiKV together with PD on the same machine.
- Use the first PD machine as the monitoring machine.

> **Note:**
>
> - Leave `[tidb_servers]` in the `inventory.ini` file empty, because this deployment is for the TiKV cluster, not the TiDB cluster.
> - It is required to use the internal IP address to deploy.

You can choose one of the following two types of cluster topology according to your scenario:

- [The cluster topology of a single TiKV instance on each TiKV node](#option-1-use-the-cluster-topology-of-a-single-tikv-instance-on-each-tikv-node)

    In most cases, it is recommended to deploy one TiKV instance on each TiKV node for better performance. However, if the CPU and memory of your TiKV machines are much better than the required in [Hardware and Software Requirements](../op-guide/recommendation.md), and you have more than two disks in one node or the capacity of one SSD is larger than 2 TB, you can deploy no more than 2 TiKV instances on a single TiKV node.

- [The cluster topology of multiple TiKV instances on each TiKV node](#option-2-use-the-cluster-topology-of-multiple-tikv-instances-on-each-tikv-node)

### Option 1: Use the cluster topology of a single TiKV instance on each TiKV node

| Name  | Host IP     | Services |
|-------|-------------|----------|
| node1 | 172.16.10.1 | PD1      |
| node2 | 172.16.10.2 | PD2      |
| node3 | 172.16.10.3 | PD3      |
| node4 | 172.16.10.4 | TiKV1    |
| node5 | 172.16.10.5 | TiKV2    |
| node6 | 172.16.10.6 | TiKV3    |

Edit the `inventory.ini` file as follows:

```ini
[tidb_servers]

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

| Name  | Host IP     | Services         |
|-------|-------------|------------------|
| node1 | 172.16.10.1 | PD1              |
| node2 | 172.16.10.2 | PD2              |
| node3 | 172.16.10.3 | PD3              |
| node4 | 172.16.10.4 | TiKV1-1, TiKV1-2 |
| node5 | 172.16.10.5 | TiKV2-1, TiKV2-2 |
| node6 | 172.16.10.6 | TiKV3-1, TiKV3-2 |

```ini
[tidb_servers]

[pd_servers]
172.16.10.1
172.16.10.2
172.16.10.3

[tikv_servers]
TiKV1-1 ansible_host=172.16.10.4 deploy_dir=/data1/deploy tikv_port=20171 labels="host=tikv1"
TiKV1-2 ansible_host=172.16.10.4 deploy_dir=/data2/deploy tikv_port=20172 labels="host=tikv1"
TiKV2-1 ansible_host=172.16.10.5 deploy_dir=/data1/deploy tikv_port=20171 labels="host=tikv2"
TiKV2-2 ansible_host=172.16.10.5 deploy_dir=/data2/deploy tikv_port=20172 labels="host=tikv2"
TiKV3-1 ansible_host=172.16.10.6 deploy_dir=/data1/deploy tikv_port=20171 labels="host=tikv3"
TiKV3-2 ansible_host=172.16.10.6 deploy_dir=/data2/deploy tikv_port=20172 labels="host=tikv3"

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

...

[pd_servers:vars]
location_labels = ["host"]
```

Edit the parameters in the service configuration file:

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

1. Edit the `deploy_dir` variable to configure the deployment directory.

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

2. Set the `deploy_without_tidb` variable to `True`.

    ```bash
    deploy_without_tidb = True
    ```

## Step 5: Deploy the TiKV cluster

When `ansible-playbook` executes the Playbook, the default concurrent number is 5. If many target machines are deployed, you can add the `-f` parameter to specify the concurrency, such as `ansible-playbook deploy.yml -f 10`.

The following example uses `tidb` as the user who runs the service.

1. Check the `tidb-ansible/inventory.ini` file to make sure `ansible_user = tidb`.

    ```bash
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

2. Make sure the SSH mutual trust and sudo without password are successfully configured.

    - Run the following command and if all servers return `tidb`, then the SSH mutual trust is successfully configured:

        ```bash
        ansible -i inventory.ini all -m shell -a 'whoami'
        ```

    - Run the following command and if all servers return `root`, then sudo without password of the `tidb` user is successfully configured:

        ```bash
        ansible -i inventory.ini all -m shell -a 'whoami' -b
        ```

3. Download the TiKV binary to the Control Machine.

    ```bash
    ansible-playbook local_prepare.yml
    ```

4. Initialize the system environment and modify the kernel parameters.

    ```bash
    ansible-playbook bootstrap.yml
    ```

5. Deploy the TiKV cluster.

    ```bash
    ansible-playbook deploy.yml
    ```

6. Start the TiKV cluster.

    ```bash
    ansible-playbook start.yml
    ```

You can check whether the TiKV cluster has been successfully deployed using the following command:

```bash
curl 172.16.10.1:2379/pd/api/v1/stores
```

## Stop the TiKV cluster

If you want to stop the TiKV cluster, run the following command:

```bash
ansible-playbook stop.yml
```

## Destroy the TiKV cluster

> **Warning:** Before you clean the cluster data or destroy the TiKV cluster, make sure you do not need it any more.

- If you do not need the data any more, you can clean up the data for test using the following command:

    ```
    ansible-playbook unsafe_cleanup_data.yml
    ```

- If you do not need the TiKV cluster any more, you can destroy it using the following command:

    ```bash
    ansible-playbook unsafe_cleanup.yml
    ```
    
    > **Note:** If the deployment directory is a mount point, an error might be reported, but the implementation result remains unaffected. You can just ignore the error.