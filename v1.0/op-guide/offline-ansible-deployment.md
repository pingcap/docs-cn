---
title: Offline Deployment Using Ansible
category: operations
---

# Offline Deployment Using Ansible

## Prepare

Before you start, make sure that you have:

1. A download machine

    - The machine must have access to the Internet in order to download TiDB-Ansible, TiDB and related packages.
    - For Linux operating system, it is recommended to install CentOS 7.3 or later.

2. Several target machines and one Control Machine

    - For system requirements and configuration, see [Prepare the environment](ansible-deployment.md#prepare).
    - It is acceptable without access to the Internet.

## Install Ansible and dependencies in the Control Machine

1. Install Ansible offline on the CentOS 7 system:

    > Download the [Ansible](http://download.pingcap.org/ansible-2.4-rpms.el7.tar.gz) offline installation package to the Control Machine.
  
    ```bash
    # tar -xzvf ansible-2.4-rpms.el7.tar.gz

    # cd ansible-2.4-rpms.el7

    # rpm -ivh PyYAML*rpm libyaml*rpm python-babel*rpm python-backports*rpm python-backports-ssl_match_hostname*rpm python-cffi*rpm python-enum34*rpm python-httplib2*rpm python-idna*rpm python-ipaddress*rpm python-jinja2*rpm python-markupsafe*rpm python-paramiko*rpm python-passlib*rpm python-ply*rpm python-pycparser*rpm python-setuptools*rpm python-six*rpm python2-cryptography*rpm python2-jmespath*rpm python2-pyasn1*rpm sshpass*rpm

    # rpm -ivh ansible-2.4.2.0-2.el7.noarch.rpm
    ```

2. After Ansible is installed, you can view the version using `ansible --version`.
  
    ```bash
    # ansible --version
     ansible 2.4.2.0
    ```

## Download TiDB-Ansible and TiDB packages on the download machine

1. Install Ansible on the download machine.

    Use the following method to install Ansible online on the download machine installed with the CentOS 7 system. Installing using the EPEL source automatically installs the related Ansible dependencies (such as `Jinja2==2.7.2 MarkupSafe==0.11`). After Ansible is installed, you can view the version using `ansible --version`.

    ```bash
    # yum install epel-release
    # yum install ansible curl
    # ansible --version

     ansible 2.4.2.0
    ```
    > **Note:**
    >
    > Make sure that the version of Ansible is 2.4 or later, otherwise compatibility problem might occur.

2. Download TiDB-Ansible.

    Use the following command to download the corresponding version of TiDB-Ansible from the GitHub [TiDB-Ansible project](https://github.com/pingcap/tidb-ansible). The default folder name is `tidb-ansible`.

    Download the 1.0 (GA) version:
    
    ```
    git clone -b release-1.0 https://github.com/pingcap/tidb-ansible.git
    ```

    OR

    Download the master version:

    ```
    git clone https://github.com/pingcap/tidb-ansible.git
    ```
    > **Note:**
    >
    > For production environment, download TiDB-Ansible 1.0 to deploy TiDB.

3. Run the `local_prepare.yml` playbook, and download TiDB binary online to the download machine.

    ```
    cd tidb-ansible
    ansible-playbook local_prepare.yml
    ```

4. After running the above command, copy the `tidb-ansible` folder to the `/home/tidb` directory of the Control Machine. The ownership authority of the file must be the `tidb` user.

## Orchestrate the TiDB cluster

See [Orchestrate the TiDB cluster](op-guide/ansible-deployment.md#orchestrate-the-tidb-cluster).

## Deploy the TiDB cluster

1. See [Deploy the TiDB cluster](op-guide/ansible-deployment.md#deploy-the-tidb-cluster).
2. You do not need to run the `ansible-playbook local_prepare.yml` playbook again.

## Test the cluster

See [Test the cluster](op-guide/ansible-deployment.md#test-the-cluster).