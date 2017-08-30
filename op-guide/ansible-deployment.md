---
title: TiDB Ansible Deployment
category: deployment
---

# TiDB Ansible Deployment

## Table of Content

-   [Overview](#overview)
-   [1. Prepare](#prepare)
-   [2. Install Ansible in the Control
    Machine](#install-ansible-in-the-control-machine)
-   [3. Download TiDB-Ansible to the Control
    Machine](#download-tidb-ansible-to-the-control-machine)
-   [4. Orchestrate the TiDB cluster](#orchestrate-the-tidb-cluster)
-   [5. Deploy the TiDB cluster](#deploy-the-tidb-cluster)
-   [6 Test the cluster](#test-the-cluster)
-   [7. Rolling Update](#perform-rolling-update)
-   [Summary of common operations](#summary-of-common-operations)

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

 
## 1. Prepare
Before you start, make sure that you have:

1.1 A Control Machine with the following requirements:

- Python 2.6 or Python 2.7

- Python Jinja2 2.7.2 and MarkupSafe 0.11 packages. You can use the following commands to install the packages:
	```
	pip install Jinja2==2.7.2 MarkupSafe==0.11
	```
	
- Access to the managed nodes via SSH using password login or SSH authorized_key login. 
	
1.2  Several managed nodes with the following requirements:

- 4 or more machines. At least 3 instances for TiKV. Don’t deploy TiKV together with TiDB or PD on the same machine. See [deploying recommendations](https://github.com/pingcap/docs/blob/master/op-guide/recommendation.md).
   
- Operating system:
   		
	- CentOS 7.3 or later
	   		
	- X86_64 architecture (AMD64)
	   		
	- Kernel version 3.10 or later
			
	- Ext4 file system. 

- The network between machines. Turn off the firewalls and iptables when deploying and turn them on after the deployment.

- The same time and time zone for all machines with the NTP service on to synchronize the correct time.

- A remote user account which you can use to login from the Control Machine to connect to the managed nodes via SSH. It can be the root user or a user account with sudo privileges. 

- Python 2.6 or Python 2.7

**Note:** The Control Machine can be one of the managed nodes with access to the external network to download binary.

## 2. Install Ansible in the Control Machine

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
 
- Homebrew on macOS:
	
	To install Homebrew, see [Homebrew]( https://brew.sh ).
	 
	```
	brew update
	brew install ansible
	```
 
- Docker
	
	Install and configure Docker for your own platform.
	```
	docker run -v `pwd`:/playbook --rm -it williamyeh/ansible:ubuntu16.04 /bin/bash
	cd /playbook # 
	```
	**Note:** The above command mounts the current working directory as the /playbook directory in the container.
		
 You can use the `ansible --version` command to see the version information.

For more information, see [Ansible Documentation](http://docs.ansible.com/ansible/intro_installation.html).


## 3. Download TiDB-Ansible to the Control Machine
Download the latest master version of the ZIP package from GitHub [TiDB-Ansible project](https://github.com/pingcap/tidb-ansible) or [click to download]( https://github.com/pingcap/tidb-ansible/archive/master.zip). 

You can then unzip the package and the default folder name is `tidb-ansible-master`. The `tidb-ansible-master` directory contains all the files you need to get started with TiDB-Ansible. 
 
## 4. Orchestrate the TiDB cluster

The standard Cluster has 6 machines: 

- 2 TiDB instances, the first TiDB instance is used as a monitor 
- 3 PD instances
- 3 TiKV instances
 
The cluster topology is as follows:

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3 |
| node4 | 172.16.10.4 | TiKV1 |
| node5 | 172.16.10.5 | TiKV2 |
| node6 | 172.16.10.6 | TiKV3 |
 
Edit the `inventory.ini` file from the `tidb-ansible-master` directory as follows:
 
```
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
 
## 5. Deploy the TiDB cluster

- If you use the normal user with the sudo privileges to deploy TiDB:
	
	5.1 Edit the `inventory.ini` file as follows:
		
	```
	## Connection
	# ssh via root:
	# ansible_user = root
	# ansible_become = true
	# ansible_become_user = tidb

	# ssh via normal user
	ansible_user = tidb
	```
  
	5.2 Connect to the network and download the TiDB, TiKV, and PD binaries:
		
		ansible-playbook local_prepare.yml
	                                           
	5.3 Initialize the system environment of the target machines and modify the kernel parameters:
	
		ansible-playbook bootstrap.yml -k -K
	 
	**Note:** 
	- Add the `-k` (lower case) parameter if a password is needed to connect to the managed node. This applies to other playbooks as well.
	- Add the `-K`(upper case) parameter because this playbook needs root privileges.
	            
	5.4 Deploy the TiDB cluster:
	 
	    ansible-playbook deploy.yml -k
	 
	5.5 Start the TiDB cluster:
	 
	    ansible-playbook start.yml -k

- If you use the root user to deploy TiDB:
	
	5.1 Edit `inventory.ini` as follows:
	
	```
	## Connection
	# ssh via root:
	ansible_user = root
	ansible_become = true
	ansible_become_user = tidb
	  
	# ssh via normal user
	# ansible_user = tidb
	```

	5.2 Connect to the network and download the TiDB, TiKV, and PD binaries.
	
		ansible-playbook local_prepare.yml 
	
	5.3 Initialize the system environment of the target machines and update the kernel parameters.
	 
		ansible-playbook bootstrap.yml -k
		
	**Note:** 
	- If the service user does not exist, the initialization operation will automatically create the user.
	- Add the `-k` (lower case) parameter if a password is needed to connect to the managed node. This applies to other playbooks as well.
	 
	5.4 Run the following command:
	
		ansible-playbook deploy.yml -k
	 
	5.5 Start the TiDB cluster: 
		
		ansible-playbook start.yml -k

**Note:** If an error containing "Permission denied" is displayed, you can use the `chmod` command to change the permissions of the specified file. For example: 

```
chmod 777 tidb-ansible-master/scripts/grafana-config-copy.py
```

## 6 Test the cluster
	
6.1 Use the MySQL client to connect to the TiDB cluster:
	  	
	  	mysql -u root-h 172.16.10.1 -P 4000	  

**Note:** The TiDB service default port is 4000.
	  
6.2 Open a browser to access the monitoring platform:

	    http://172.16.10.1:3000
  
The default account and password: admin/admin.

## 7. Perform Rolling Update
The rolling update of the TiDB service does not impact the ongoing business. The environment with the minimum number of instances is as follows:

+ 2 TiDB instances
+ 3 TiKV instances
+ 3 PD instances

**Note:** For remote connections, add the `-k` (lower case) parameter if the password is needed to connect to the managed node. But if the mutual authentication is already set up, you don't need to add the `-k` parameter.

**Note:** If the `pump`/`drainer` services are running in the cluster, it is recommended to stop the `drainer` service first before the rolling update. The rolling update of the TiDB service automatically updates the `pump` service.
	
7.1. Download the binary

- Use playbook to download the latest master binary and replace the existing binary in `tidb-ansible/resource/bin/` automatically:

	```
	ansible-playbook local_prepare.yml
	```
- Use `wget` to download the binary and replace  the existing binary in `tidb-ansible/resource/bin/` manually:

	```
	wget http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
	```

7.2. Use Ansible for rolling update

- To apply rolling update to a specific service, such as TiKV:

	```
	ansible-playbook rolling_update.yml --tags=tikv
	```
- To apply rolling update to all the services:

	```
	ansible-playbook rolling_update.yml
	```
 
## Summary of common operations
| Job | Playbook |
|----|--------|
| Start the cluster | `ansible-playbook start.yml` |
| Stop the cluster | `ansible-playbook stop.yml` |
| Destroy the cluster | `ansible-playbook unsafe_cleanup.yml`	 (If the deployment directory is a mount point, an error will be reported, but implementation results will remain unaffected) | 
| Clean data (for test) | `ansible-playbook cleanup_data.yml` |
| Rolling Upgrade | `ansible-playbook rolling_update.yml` |
| Rolling upgrade TiKV | `ansible-playbook rolling_update.yml --tags=tikv` |
| Rolling upgrade modules except PD | `ansible-playbook rolling_update.yml --skip-tags=pd` |
 
For more advanced features of TiDB including data migration, performance tuning, etc., see [TiDB Documents](https://github.com/pingcap/docs). 
