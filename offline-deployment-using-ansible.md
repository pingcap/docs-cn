---
title: Deploy TiDB Offline Using TiDB Ansible
summary: Use TiDB Ansible to deploy a TiDB cluster offline.
aliases: ['/docs/dev/offline-deployment-using-ansible/','/docs/dev/how-to/deploy/orchestrated/offline-ansible/']
---

# Deploy TiDB Offline Using TiDB Ansible

This guide describes how to deploy a TiDB cluster offline using TiDB Ansible.

## Prepare

Before you start, make sure that you have:

1. A download machine

    - The machine must have access to the Internet in order to download TiDB Ansible, TiDB and related packages.
    - For Linux operating system, it is recommended to install CentOS 7.3 or later.

2. Several target machines and one control machine

    - For system requirements and configuration, see [Prepare the environment](/online-deployment-using-ansible.md#prepare).
    - It is acceptable without access to the Internet.

## Step 1: Install system dependencies on the control machine

Take the following steps to install system dependencies on the control machine installed with the CentOS 7 system.

1. Download the [`pip`](https://download.pingcap.org/ansible-system-rpms.el7.tar.gz) offline installation package on the download machine and then upload it to the control machine.

    > **Note:**
    >
    > This offline installation package includes `pip` and `sshpass`, and only supports the CentOS 7 system.

2. Install system dependencies on the control machine.

    {{< copyable "shell-root" >}}

    ```bash
    tar -xzvf ansible-system-rpms.el7.tar.gz &&
    cd ansible-system-rpms.el7 &&
    chmod u+x install_ansible_system_rpms.sh &&
    ./install_ansible_system_rpms.sh
    ```

3. After the installation is finished, you can use `pip -V` to check whether it is successfully installed.

    {{< copyable "shell-root" >}}

    ```bash
    pip -V
    ```

    ```
    pip 8.1.2 from /usr/lib/python2.7/site-packages (python 2.7)
    ```

> **Note:**
>
> If `pip` is already installed to your system, make sure that the version is 8.1.2 or later. Otherwise, compatibility error occurs when you install TiDB Ansible and its dependencies offline.

## Step 2: Create the `tidb` user on the control machine and generate the SSH key

See [Create the `tidb` user on the control machine and generate the SSH key](/online-deployment-using-ansible.md#step-2-create-the-tidb-user-on-the-control-machine-and-generate-the-ssh-key).

## Step 3: Install TiDB Ansible and its dependencies offline on the control machine

Currently, all the versions of TiDB Ansible from 2.4 to 2.7.11 are supported. The versions of TiDB Ansible and the related dependencies are listed in the `tidb-ansible/requirements.txt` file. The following installation steps take Ansible 2.5 as an example.

1. Download [Ansible 2.5 offline installation package](https://download.pingcap.org/ansible-2.5.0-pip.tar.gz) on the download machine and then upload it to the control machine.

2. Install TiDB Ansible and its dependencies offline.

    {{< copyable "shell-root" >}}

    ```bash
    tar -xzvf ansible-2.5.0-pip.tar.gz &&
    cd ansible-2.5.0-pip/ &&
    chmod u+x install_ansible.sh &&
    ./install_ansible.sh
    ```

3. View the version of TiDB Ansible.

    After TiDB Ansible is installed, you can view the version using `ansible --version`.

    {{< copyable "shell-root" >}}

    ```bash
    ansible --version
    ```

    ```
    ansible 2.5.0
    ```

## Step 4: Download TiDB Ansible and TiDB packages on the download machine

1. Install TiDB Ansible on the download machine.

    Use the following method to install Ansible online on the download machine installed with the CentOS 7 system. After TiDB Ansible is installed, you can view the version using `ansible --version`.

    {{< copyable "shell-root" >}}

    ```bash
    yum install epel-release &&
    yum install ansible curl &&
    ansible --version
    ```

    ```
    ansible 2.5.0
    ```

    > **Note:**
    >
    > Make sure that the version of Ansible is 2.5, otherwise a compatibility issue occurs.

2. Download TiDB Ansible.

    Use the following command to download the corresponding version of TiDB Ansible from the [TiDB Ansible project](https://github.com/pingcap/tidb-ansible) GitHub repo. The default folder name is `tidb-ansible`.

    {{< copyable "shell-regular" >}}

    ```bash
    git clone https://github.com/pingcap/tidb-ansible.git
    ```

    > **Note:**
    >
    > It is required to use the corresponding tidb-ansible version when you deploy and upgrade the TiDB cluster. If you deploy TiDB using a mismatched version of tidb-ansible (such as using tidb-ansible v2.1.4 to deploy TiDB v2.1.6), an error might occur.

3. Run the `local_prepare.yml` playbook, and download TiDB binary online to the download machine.

    {{< copyable "shell-regular" >}}

    ```bash
    cd tidb-ansible &&
    ansible-playbook local_prepare.yml
    ```

4. After running the above command, copy the `tidb-ansible` folder to the `/home/tidb` directory of the control machine. The ownership authority of the file must be the `tidb` user.

## Step 5: Configure the SSH mutual trust and sudo rules on the control machine

See [Configure the SSH mutual trust and sudo rules on the control machine](/online-deployment-using-ansible.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine).

## Step 6: Install the NTP service on the target machines

See [Install the NTP service on the target machines](/online-deployment-using-ansible.md#step-6-install-the-ntp-service-on-the-target-machines).

> **Note:**
>
> If the time and time zone of all your target machines are same, the NTP service is on and is normally synchronizing time, you can skip this step. See [How to check whether the NTP service is normal](/online-deployment-using-ansible.md#how-to-check-whether-the-ntp-service-is-normal).

## Step 7: Configure the CPUfreq governor mode on the target machine

See [Configure the CPUfreq governor mode on the target machine](/online-deployment-using-ansible.md#step-7-configure-the-cpufreq-governor-mode-on-the-target-machine).

## Step 8: Mount the data disk ext4 filesystem with options on the target machines

See [Mount the data disk ext4 filesystem with options on the target machines](/online-deployment-using-ansible.md#step-8-mount-the-data-disk-ext4-filesystem-with-options-on-the-target-machines).

## Step 9: Edit the `inventory.ini` file to orchestrate the TiDB cluster

See [Edit the `inventory.ini` file to orchestrate the TiDB cluster](/online-deployment-using-ansible.md#step-9-edit-the-inventoryini-file-to-orchestrate-the-tidb-cluster).

## Step 10: Deploy the TiDB cluster

1. You do not need to run the playbook in `ansible-playbook local_prepare.yml`.

2. See [Deploy the TiDB cluster](/online-deployment-using-ansible.md#step-11-deploy-the-tidb-cluster).

## Test the TiDB cluster

See [Test the TiDB cluster](/online-deployment-using-ansible.md#test-the-tidb-cluster).

> **Note:**
>
> By default, TiDB periodically shares usage details with PingCAP to help understand how to improve the product. For details about what is shared and how to disable the sharing, see [Telemetry](/telemetry.md).
