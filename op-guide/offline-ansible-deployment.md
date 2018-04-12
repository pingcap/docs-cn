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

    > Download the [Ansible 2.4.2](https://download.pingcap.org/ansible-2.4.2-rpms.el7.tar.gz) offline installation package to the Control Machine.

    ```bash
    # tar -xzvf ansible-2.4.2-rpms.el7.tar.gz

    # cd ansible-2.4-rpms.el7

    # chmod u+x install_ansible.sh

    # ./install_ansible.sh
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
    > **Note:** Make sure that the version of Ansible is 2.4 or later, otherwise compatibility problem might occur.

2. Download TiDB-Ansible.

    Use the following command to download the corresponding version of TiDB-Ansible from the GitHub [TiDB-Ansible project](https://github.com/pingcap/tidb-ansible). The default folder name is `tidb-ansible`. The following are examples of downloading various versions, and you can turn to the official team for advice on which version to choose.

    Download the 1.0 GA version:

    ```
    git clone -b release-1.0 https://github.com/pingcap/tidb-ansible.git
    ```

    Download the 2.0 version:

    ```
    git clone -b release-2.0 https://github.com/pingcap/tidb-ansible.git
    ```

    or

    Download the master version:

    ```
    git clone https://github.com/pingcap/tidb-ansible.git
    ```

3. Run the `local_prepare.yml` playbook, and download TiDB binary online to the download machine.

    ```
    cd tidb-ansible
    ansible-playbook local_prepare.yml
    ```

4. After running the above command, copy the `tidb-ansible` folder to the `/home/tidb` directory of the Control Machine. The ownership authority of the file must be the `tidb` user.

## Orchestrate the TiDB cluster

See [Orchestrate the TiDB cluster](ansible-deployment.md#orchestrate-the-tidb-cluster).

## Deploy the TiDB cluster

1. See [Deploy the TiDB cluster](ansible-deployment.md#deploy-the-tidb-cluster).
2. You do not need to run the `ansible-playbook local_prepare.yml` playbook again.

## Test the cluster

See [Test the cluster](ansible-deployment.md#test-the-cluster).
