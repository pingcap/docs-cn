---
title: Deploy Data Migration Using DM-Ansible
summary: Use DM-Ansible to deploy the Data Migration cluster.
category: how-to
aliases: ['/docs/tools/dm/deployment/'] 
---

# Deploy Data Migration Using DM-Ansible

DM-Ansible is a cluster deployment tool developed by PingCAP based on the [Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#about-playbooks) feature of [Ansible](https://docs.ansible.com/ansible/latest/index.html) (an IT automation tool). This guide shows how to quickly deploy a Data Migration (DM) cluster using DM-Ansible.

## Prepare

Before you start, make sure you have the following machines as required.

1. Several target machines that meet the following requirements:

    - CentOS 7.3 (64-bit) or later, x86_64 architecture (AMD64)
    - Network between machines
    - Closing the firewall, or opening the service port

2. A Control Machine that meets the following requirements:

    > **Note:**
    >
    > The Control Machine can be one of the target machines.

    - CentOS 7.3 (64-bit) or later, with Python 2.7 installed
    - Ansible 2.5 or later installed
    - Access to the Internet

## Step 1: Install system dependencies on the Control Machine

Log in to the Control Machine using the `root` user account, and run the corresponding command according to your operating system.

- If you use a Control Machine installed with CentOS 7, run the following command:

    ```
    # yum -y install epel-release git curl sshpass
    # yum -y install python-pip
    ```

- If you use a Control Machine installed with Ubuntu, run the following command:

    ```
    # apt-get -y install git curl sshpass python-pip
    ```

## Step 2: Create the `tidb` user on the Control Machine and generate the SSH key

Make sure you have logged in to the Control Machine using the `root` user account, and then perform the following steps.

1. Create the `tidb` user.

    ```
    # useradd -m -d /home/tidb tidb
    ```

2. Set a password for the `tidb` user account.

    ```
    # passwd tidb
    ```

3. Configure sudo without password for the `tidb` user account by adding `tidb ALL=(ALL) NOPASSWD: ALL` to the end of the sudo file:

    ```
    # visudo
    tidb ALL=(ALL) NOPASSWD: ALL
    ```
4. Generate the SSH key.

    Execute the `su` command to switch the user from `root` to `tidb`.

    ```
    # su - tidb
    ```

    Create the SSH key for the `tidb` user account and hit the <kbd>Enter</kbd> key when `Enter passphrase` is prompted. After successful execution, the SSH private key file is `/home/tidb/.ssh/id_rsa`, and the SSH public key file is `/home/tidb/.ssh/id_rsa.pub`.
    
    ```
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

## Step 3: Download DM-Ansible to the Control Machine

Make sure you have logged in to the Control Machine using the `tidb` user account.

1. Go to the `/home/tidb` directory.

2. Run the following command to download DM-Ansible.

    ```bash
    $ wget http://download.pingcap.org/dm-ansible-{version}.tar.gz
    ```

    `{version}` is the DM version that you expect to download, like `v1.0.0-alpha` and `latest`.

## Step 4: Install DM-Ansible and its dependencies on the Control Machine

Make sure you have logged in to the Control Machine using the `tidb` user account.

It is required to use `pip` to install Ansible and its dependencies, otherwise a compatibility issue occurs. Currently, DM-Ansible is compatible with Ansible 2.5 or later.

1. Install DM-Ansible and the dependencies on the Control Machine:

    ```bash
    $ tar -xzvf dm-ansible-latest.tar.gz
    $ mv dm-ansible-latest dm-ansible
    $ cd /home/tidb/dm-ansible
    $ sudo pip install -r ./requirements.txt
    ```

    Ansible and the related dependencies are in the `dm-ansible/requirements.txt` file.

2. View the version of Ansible:

    ```bash
    $ ansible --version
    ansible 2.5.0
    ```

## Step 5: Configure the SSH mutual trust and sudo rules on the Control Machine

Make sure you have logged in to the Control Machine using the `tidb` user account.

1. Add the IPs of your deployment target machines to the `[servers]` section of the `hosts.ini` file.

    ```
    $ cd /home/tidb/dm-ansible
    $ vi hosts.ini
    [servers]
    172.16.10.71
    172.16.10.72
    172.16.10.73

    [all:vars]
    username = tidb
    ```

2. Run the following command and input the password of the `root` user account of your deployment target machines.

    ```bash
    $ ansible-playbook -i hosts.ini create_users.yml -u root -k
    ```

    This step creates the `tidb` user account on the deployment target machines, configures the sudo rules and the SSH mutual trust between the Control Machine and the deployment target machines.

## Step 6: Download DM and the monitoring component installation package to the Control Machine

Make sure the Control Machine is connected to the Internet and run the following command:

```bash
ansible-playbook local_prepare.yml
```

## Step 7: Edit the `inventory.ini` file to orchestrate the DM cluster

Log in to the Control Machine using the `tidb` user account, and edit the `/home/tidb/dm-ansible/inventory.ini` file to orchestrate the DM cluster.

> **Note:**
>
> It is required to use the internal IP address to deploy. If the SSH port of the target machines is not the default 22 port, you need to add the `ansible_port` variable, as shown in the following example:

```ini
dm-worker1 ansible_host=172.16.10.72 ansible_port=5555 server_id=101 mysql_host=172.16.10.72 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

You can choose one of the following two types of cluster topology according to your scenario:

- [The cluster topology of a single DM-worker instance on each node](#option-1-use-the-cluster-topology-of-a-single-dm-worker-instance-on-each-node)

- [The cluster topology of multiple DM-worker instances on each node](#option-2-use-the-cluster-topology-of-multiple-dm-worker-instances-on-each-node)

    Generally, it is recommended to deploy one DM-worker instance on each node. However, if the CPU and memory of your machine are much better than the required in [Hardware and Software Requirements](/dev/how-to/deploy/hardware-recommendations.md), and you have more than 2 disks in one node or the capacity of one SSD is larger than 2 TB, you can deploy no more than 2 DM-worker instances on a single node.

### Option 1: Use the cluster topology of a single DM-worker instance on each node

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.71 | DM-master, Prometheus, Grafana, Alertmanager |
| node2 | 172.16.10.72 | DM-worker1 |
| node3 | 172.16.10.73 | DM-worker2 |
| mysql-replica-01| 172.16.10.81 | MySQL |
| mysql-replica-02| 172.16.10.82 | MySQL |

```ini
# DM modules.
[dm_master_servers]
dm_master ansible_host=172.16.10.71

[dm_worker_servers]
dm_worker1 ansible_host=172.16.10.72 server_id=101 source_id="mysql-replica-01" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

dm_worker2 ansible_host=172.16.10.73 server_id=102 source_id="mysql-replica-02" mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

# Monitoring modules.
[prometheus_servers]
prometheus ansible_host=172.16.10.71

[grafana_servers]
grafana ansible_host=172.16.10.71

[alertmanager_servers]
alertmanager ansible_host=172.16.10.71

# Global variables.
[all:vars]
cluster_name = test-cluster

ansible_user = tidb

dm_version = latest

deploy_dir = /data1/dm

grafana_admin_user = "admin"
grafana_admin_password = "admin"
```

For details about DM-worker parameters, see [DM-worker configuration parameters description](#dm-worker-configuration-parameters-description).

### Option 2: Use the cluster topology of multiple DM-worker instances on each node

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.71 | DM-master, Prometheus, Grafana, Alertmanager |
| node2 | 172.16.10.72 | DM-worker1-1, DM-worker1-2 |
| node3 | 172.16.10.73 | DM-worker2-1, DM-worker2-2 |

When you edit the `inventory.ini` file, pay attention to distinguish between the following variables: `server_id`, `deploy_dir`, and `dm_worker_port`.

```ini
# DM modules.
[dm_master_servers]
dm_master ansible_host=172.16.10.71

[dm_worker_servers]
dm_worker1_1 ansible_host=172.16.10.72 server_id=101 deploy_dir=/data1/dm_worker dm_worker_port=8262 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
dm_worker1_2 ansible_host=172.16.10.72 server_id=102 deploy_dir=/data2/dm_worker dm_worker_port=8263 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

dm_worker2_1 ansible_host=172.16.10.73 server_id=103 deploy_dir=/data1/dm_worker dm_worker_port=8262 mysql_host=172.16.10.83 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
dm_worker2_2 ansible_host=172.16.10.73 server_id=104 deploy_dir=/data2/dm_worker dm_worker_port=8263 mysql_host=172.16.10.84 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

# Monitoring modules.
[prometheus_servers]
prometheus ansible_host=172.16.10.71

[grafana_servers]
grafana ansible_host=172.16.10.71

[alertmanager_servers]
alertmanager ansible_host=172.16.10.71

# Global variables.
[all:vars]
cluster_name = test-cluster

ansible_user = tidb

dm_version = latest

deploy_dir = /data1/dm

grafana_admin_user = "admin"
grafana_admin_password = "admin"
```

### DM-worker configuration parameters description

| Variable name | Description |
| ------------- | ------- |
| source_id | DM-worker binds to a unique database instance or a replication group with the master-slave architecture. When the master and slave switch, you only need to update `mysql_host` or `mysql_port` and do not need to update the `source_id`. |
| server_id | DM-worker connects to MySQL as a slave. This variable is the `server_id` of the slave. Keep it globally unique in the MySQL cluster, and the value range is 0 ~ 4294967295. |
| mysql_host | The upstream MySQL host. |
| mysql_user | The upstream MySQL username; default "root". |
| mysql_password | The upstream MySQL user password. You need to encrypt the password using the `dmctl` tool. See [Encrypt the upstream MySQL user password using dmctl](#encrypt-the-upstream-mysql-user-password-using-dmctl). |
| mysql_port | The upstream MySQL port; default 3306. |
| enable_gtid | Whether DM-worker uses GTID to pull the binlog. The prerequisite is that the upstream MySQL has enabled the GTID mode. |
| relay_binlog_name | Whether DM-worker pulls the binlog starting from the specified binlog file. Only used when the local has no valid relay log. |
| relay_binlog_gtid | Whether DM-worker pulls the binlog starting from the specified GTID. Only used when the local has no valid relay log and `enable_gtid` is true. |
| flavor | "flavor" indicates the release type of MySQL. For the official version, Percona, and cloud MySQL, fill in "mysql"; for MariaDB, fill in "mariadb". It is "mysql" by default. |

For details about the `deploy_dir` configuration, see [Configure the deployment directory](#configure-the-deployment-directory).

### Encrypt the upstream MySQL user password using dmctl

Assuming that the upstream MySQL user password is `123456`, configure the generated string to the `mysql_password` variable of DM-worker.

```bash
$ cd /home/tidb/dm-ansible/resources/bin
$ ./dmctl -encrypt 123456
VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=
```

## Step 8: Edit variables in the `inventory.ini` file

This step shows how to edit the variable of the deployment directory, how to configure the relay log synchronization position and the relay log GTID synchronization mode, and explains the global variables in the `inventory.ini` file.

### Configure the deployment directory

Edit the `deploy_dir` variable to configure the deployment directory.

- The global variable is set to `/home/tidb/deploy` by default, and it applies to all services. If the data disk is mounted on the `/data1` directory, you can set it to `/data1/dm`. For example:

    ```ini
    ## Global variables.
    [all:vars]
    deploy_dir = /data1/dm
    ```

- If you need to set a separate deployment directory for a service, you can configure the host variable while configuring the service host list in the `inventory.ini` file. It is required to add the first column alias, to avoid confusion in scenarios of mixed services deployment.

    ```ini
    dm-master ansible_host=172.16.10.71 deploy_dir=/data1/deploy
    ```

### Configure the relay log synchronization position

When you start DM-worker for the first time, you need to configure `relay_binlog_name` to specify the position where DM-worker starts to pull the corresponding upstream MySQL or MariaDB binlog.

```yaml
[dm_worker_servers]
dm-worker1 ansible_host=172.16.10.72 source_id="mysql-replica-01" server_id=101 relay_binlog_name="binlog.000011" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

dm-worker2 ansible_host=172.16.10.73 source_id="mysql-replica-02" server_id=102 relay_binlog_name="binlog.000002" mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

> **Note:**
>
> If `relay_binlog_name` is not set, DM-worker pulls the binlog starting from the earliest existing binlog file of the upstream MySQL or MariaDB. In this case, it can take a long period of time to pull the latest binlog for the data synchronization task.

### Enable the relay log GTID synchronization mode

In a DM cluster, the relay log processing unit of DM-worker communicates with the upstream MySQL or MariaDB to pull its binlog to the local file system.

You can enable the relay log GTID synchronization mode by configuring the following items. Currently, DM supports MySQL GTID and MariaDB GTID.

- `enable_gtid`: to enable the relay log GTID synchronization mode to deal with scenarios like master-slave switch
- `relay_binlog_gtid`: to specify the position where DM-worker starts to pull the corresponding upstream MySQL or MariaDB binlog

```yaml
[dm_worker_servers]
dm-worker1 ansible_host=172.16.10.72 source_id="mysql-replica-01" server_id=101 enable_gtid=true relay_binlog_gtid="aae3683d-f77b-11e7-9e3b-02a495f8993c:1-282967971,cc97fa93-f5cf-11e7-ae19-02915c68ee2e:1-284361339" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

dm-worker2 ansible_host=172.16.10.73 source_id="mysql-replica-02" server_id=102 relay_binlog_name=binlog.000002 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

### Global variables description

| Variable name            | Description                                |
| --------------- | ---------------------------------------------------------- |
| cluster_name | The name of a cluster, adjustable |
| dm_version | The version of DM, configured by default |
| grafana_admin_user | The username of the Grafana administrator; default `admin` |
| grafana_admin_password | The password of the Grafana administrator account; default `admin`; used to import Dashboard by Ansible; update this variable if you have modified it through the Grafana web |

## Step 9: Deploy the DM cluster

When `ansible-playbook` runs Playbook, the default concurrent number is 5. If many deployment target machines are deployed, you can add the `-f` parameter to specify the concurrency, such as `ansible-playbook deploy.yml -f 10`.

The following example uses `tidb` as the user who runs the service.

1. Edit the `dm-ansible/inventory.ini` file to make sure `ansible_user = tidb`.

    ```ini
    ansible_user = tidb
    ```

    > **Note:**
    >
    > Do not configure `ansible_user` to `root`, because `tidb-ansible` limits the user that runs the service to the normal user.

    Run the following command and if all servers return `tidb`, then the SSH mutual trust is successfully configured:

    ```bash
    ansible -i inventory.ini all -m shell -a 'whoami'
    ```

    Run the following command and if all servers return `root`, then sudo without password of the `tidb` user is successfully configured:

    ```bash
    ansible -i inventory.ini all -m shell -a 'whoami' -b
    ```

2. Modify kernel parameters, and deploy the DM cluster components and monitoring components.

    ```bash
    ansible-playbook deploy.yml
    ```

3. Start the DM cluster.

    ```bash
    ansible-playbook start.yml
    ```

    This operation starts all the components in the entire DM cluster in order, which include DM-master, DM-worker, and the monitoring components. You can use this command to start a DM cluster after it is stopped.

## Step 10: Stop the DM cluster

If you need to stop the DM cluster, run the following command:

```bash
$ ansible-playbook stop.yml
```

This operation stops all the components in the entire DM cluster in order, which include DM-master, DM-worker, and the monitoring components.

## Common deployment issues

### Service default ports

| Component | Port variable | Default port | Description |
| :-- | :-- | :-- | :-- |
| DM-master | `dm_master_port` | 8261  | DM-master service communication port |
| DM-worker | `dm_worker_port` | 8262  | DM-worker service communication port |
| Prometheus | `prometheus_port` | 9090 | Prometheus service communication port |
| Grafana | `grafana_port` |  3000 | The port for the external service of web monitoring service and client (browser) access |
| Alertmanager | `alertmanager_port` |  9093 | Alertmanager service communication port |

### Customize ports

Edit the `inventory.ini` file and add the related host variable of the corresponding service port after the service IP:

```ini
dm_master ansible_host=172.16.10.71 dm_master_port=18261
```

### Update DM-Ansible

1. Log in to the Control Machine using the `tidb` account, enter the `/home/tidb` directory, and back up the `dm-ansible` folder.

    ```
    $ cd /home/tidb
    $ mv dm-ansible dm-ansible-bak
    ```

2. Download the specified version of DM-Ansible and extract it.

    ```
    $ cd /home/tidb
    $ wget http://download.pingcap.org/dm-ansible-{version}.tar.gz
    $ tar -xzvf dm-ansible-latest.tar.gz
    $ mv dm-ansible-latest dm-ansible
    ```

3. Migrate the `inventory.ini` configuration file.

    ```
    $ cd /home/tidb
    $ cp dm-ansible-bak/inventory.ini dm-ansible/inventory.ini
    ```

4. Migrate the `dmctl` configuration.

    ```
    $ cd /home/tidb/dm-ansible-bak/dmctl
    $ cp * /home/tidb/dm-ansible/dmctl/
    ```

5. Use Playbook to download the latest DM binary file, which substitutes for the binary file in the  `/home/tidb/dm-ansible/resource/bin/` directory automatically.

    ```
    $ ansible-playbook local_prepare.yml
    ```
