---
title: Offline Deployment Using Ansible
category: operations
---

# Offline Deployment Using Ansible

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

    - 4 or more machines. At least 3 instances for TiKV. Don't deploy TiKV together with TiDB or PD on the same machine. See [deploying recommendations](https://github.com/pingcap/docs/blob/master/op-guide/recommendation.md).

    - Recommended Operating system:

      - CentOS 7.3 or later

      - X86_64 architecture (AMD64)

      - Kernel version 3.10 or later

      - Ext4 file system

    - The network between machines. Turn off the firewalls and iptables when deploying and turn them on after the deployment.

    - The same time and time zone for all machines with the NTP service on to synchronize the correct time. If you are using the Ubuntu platform, install the ntpstat package.

    - A remote user account which you can use to login from the Control Machine to connect to the managed nodes via SSH. It can be the root user or a user account with sudo privileges.

    - Python 2.6 or Python 2.7

    > **Note**: The Control Machine can be one of the managed nodes.

## Install Ansible in the Control Machine

1. Install Ansible offline on CentOS:

    > Download the [Ansible](https://download.pingcap.org/ansible-2.3-rpms.el7.tar.gz) offline installation package to the Control Machine.
  
    ```ini
    tar -xzvf ansible-2.3-rpms.el7.tar.gz
    
    cd ansible-2.3-rpms.el7
    
    rpm -ivh PyYAML*.rpm libtomcrypt*.rpm libtommath*.rpm libyaml*.rpm python-
    babel*.rpm python-backports*.rpm python-backports-ssl_match_hostname*.rpm
    python-httplib2*.rpm python-jinja2*.rpm python-keyczar*.rpm python-
    markupsafe*.rpm python-setuptools*.rpm python-six*.rpm python2-crypto*.rpm
    python2-ecdsa*.rpm python2-paramiko*.rpm python2-pyasn1*.rpm sshpass*.rpm
    rpm -ivh ansible-2.3.1.0-1.el7.noarch.rpm
    ```

2. After Ansible is installed, you can view the version using `ansible --version`.
  
    ```
    ansible --version
    # ansible 2.3.1.0
    ```

## Download TiDB packages

Run the following command on a machine installed with Ansible and connected to network:

1. Download TiDB-Ansible:

    - Download TiDB-Ansible of the master branch, used to install the master version of TiDB cluster (Binlog is the Kafka version)

        ```
        git clone https://github.com/pingcap/tidb-ansible
        ```
    
    - Download TiDB-Ansible of the release-1.0 branch, used to install the release-1.0 (GA) version of TiDB cluster (Binlog is the Kafka version)

        ```
        git clone -b release-1.0 https://github.com/pingcap/tidb-ansible
        ```
    
    - Download TiDB-Ansible of the release-1.0-binlog-local branch, used to install the release-1.0-binlog-local version of TiDB cluster (Binlog is the local version)

       ```
       git clone -b release-1.0-binlog-local https://github.com/pingcap/tidb-ansible
       ```

2. Download TiDB dependencies:

    ```
    cd tidb-ansible
    ansible-playbook local_prepare.yml
    ```

3. After running the above command, copy the TiDB-Ansible packages to the Control Machine.

## Orchestrate the TiDB cluster

The file path of `inventory.ini` is: `tidb-ansible/inventory.ini`

The standard cluster has 6 machines:

- 2 TiDB nodes, the first TiDB machine is used as a monitor
- 3 PD nodes
- 3 TiKV nodes

### The cluster topology of single TiKV instance on a single machine 

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3 |
| node4 | 172.16.10.4 | TiKV1 |
| node5 | 172.16.10.5 | TiKV2 |
| node6 | 172.16.10.6 | TiKV3 |

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

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3 |
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

**Edit the parameters:**

1. For multiple TiKV instances, edit the `end-point-concurrency` and `block-cache-size` parameters in `conf/tikv.yml`:

    - `end-point-concurrency`: keep the number less than CPU Vcores
    - `rocksdb defaultcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 30% 
    - `rocksdb writecf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 45%
    - `rocksdb lockcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 2.5% (128 MB at a minimum)
    - `raftdb defaultcf block-cache-size(GB)`: MEM * 80% / TiKV instance number * 2.5% (128 MB at a minimum)

2. If multiple TiKV instances are deployed on a same physical disk, edit the `capacity` parameter in `conf/tikv.yml`:

    - `capaticy`: (DISK - log space) / TiKV instance number (the unit is GB)

## Deploy the TiDB cluster

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
    
    2. Initialize the system environment and edit the kernel parameters.

        ```
        ansible-playbook bootstrap.yml
        ```
        
        > **Note**: If the service user does not exist, the initialization operation will automatically create the user.
        
        If the remote connection using the root user requires a password, use the `-k` (lower case) parameter. This applies to other playbooks as well:
        
        ```
        ansible-playbook bootstrap.yml -k
        ```
    
    3. Deploy the TiDB cluster.

        ```
        ansible-playbook deploy.yml -k
        ```
    
    4. Start the TiDB cluster.

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
    
    2. Use the `local_prepare.yml` playbook, and each cluster component in the downloads directory is examined, copied and extracted.

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

## Test the cluster

It is recommended to configure load balancing to provide uniform SQL interface.

1. Connect to the TiDB cluster using the MySQL client.

    ```
    mysql -u root-h 172.16.10.1 -P 4000
    ```
    
    > **Note**: The default port of TiDB service is 4000.

2. Access the monitoring platform using a web browser.

    ```
    http://172.16.10.1:3000
    ```
    
    The default account and password: `admin/admin`.
