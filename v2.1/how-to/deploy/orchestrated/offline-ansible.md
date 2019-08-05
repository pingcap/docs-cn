---
title: Deploy TiDB Offline Using Ansible
summary: Use Ansible to deploy a TiDB cluster offline.
category: how-to
---

# Deploy TiDB Offline Using Ansible

This guide describes how to deploy a TiDB cluster offline using Ansible.

## Prepare

Before you start, make sure that you have:

1. A download machine

    - The machine must have access to the Internet in order to download TiDB-Ansible, TiDB and related packages.
    - For Linux operating system, it is recommended to install CentOS 7.3 or later.

2. Several target machines and one Control Machine

    - For system requirements and configuration, see [Prepare the environment](/how-to/deploy/orchestrated/ansible.md#prepare).
    - It is acceptable without access to the Internet.

## Step 1: Install system dependencies on the Control Machine

Take the following steps to install system dependencies on the Control Machine installed with the CentOS 7 system.

1. Download the [`pip`](https://download.pingcap.org/ansible-system-rpms.el7.tar.gz) offline installation package to the Control Machine.

    ```
    # tar -xzvf ansible-system-rpms.el7.tar.gz
    # cd ansible-system-rpms.el7
    # chmod u+x install_ansible_system_rpms.sh
    # ./install_ansible_system_rpms.sh
    ```

    > **Note:**
    >
    > This offline installation package includes `pip` and `sshpass`, and only supports the CentOS 7 system.

2. After the installation is finished, you can use `pip -V` to check whether it is successfully installed.

    ```bash
    # pip -V
     pip 8.1.2 from /usr/lib/python2.7/site-packages (python 2.7)
    ```

    > **Note:**
    >
    > If `pip` is already installed to your system, make sure that the version is 8.1.2 or later. Otherwise, compatibility error occurs when you install Ansible and its dependencies offline.

## Step 2: Create the `tidb` user on the Control Machine and generate the SSH key

See [Create the `tidb` user on the Control Machine and generate the SSH key](/how-to/deploy/orchestrated/ansible.md#step-2-create-the-tidb-user-on-the-control-machine-and-generate-the-ssh-key).

## Step 3: Install Ansible and its dependencies offline on the Control Machine

Currently, the TiDB 2.0 GA version and the master version are compatible with Ansible 2.5. Ansible and the related dependencies are in the `tidb-ansible/requirements.txt` file.

1. Download [Ansible 2.5 offline installation package](https://download.pingcap.org/ansible-2.5.0-pip.tar.gz).

2. Install Ansible and its dependencies offline.

    ```
    # tar -xzvf ansible-2.5.0-pip.tar.gz
    # cd ansible-2.5.0-pip/
    # chmod u+x install_ansible.sh
    # ./install_ansible.sh
    ```

3. View the version of Ansible.

    After Ansible is installed, you can view the version using `ansible --version`.

    ```
    # ansible --version
     ansible 2.5.0
    ```

## Step 4: Download TiDB-Ansible and TiDB packages on the download machine

The relationship between the `tidb-ansible` version and the TiDB version is as follows:

| TiDB version | tidb-ansible tag | Note |
| -------- | ---------------- | --- |
| 2.0 version | v2.0.10, v2.0.11 | It is the latest 2.0 stable version which can be used in the production environment. |
| 2.1 version | v2.1.1 ~ v2.1.6 | It is the latest 2.1 stable version which can be used in the production environment (recommended). |
| 3.0 version | v3.0.0-beta, v3.0.0-beta.1 | It is currently a beta version which is not recommended to use in the production environment. |
| `master` branch | None | It includes the newest features and is updated on a daily basis, so it is not recommended to use it in the production environment. |

> **Note:**
>
> If you have questions regarding which version to use, email to info@pingcap.com for more information or [file an issue](https://github.com/pingcap/tidb-ansible/issues/new).

1. Install Ansible on the download machine.

    Use the following method to install Ansible online on the download machine installed with the CentOS 7 system. After Ansible is installed, you can view the version using `ansible --version`.

    ```bash
    # yum install epel-release
    # yum install ansible curl
    # ansible --version
      ansible 2.5.0
    ```

    > **Note:**
    >
    > Make sure that the version of Ansible is 2.5, otherwise a compatibility issue occurs.

2. Download TiDB-Ansible.

    Use the following command to download the corresponding version of TiDB-Ansible from the GitHub [TiDB-Ansible project](https://github.com/pingcap/tidb-ansible). The default folder name is `tidb-ansible`.

    > **Note:**
    >
    > It is required to use the corresponding tidb-ansible version when you deploy and upgrade the TiDB cluster. If you deploy TiDB using a mismatched version of tidb-ansible (such as using tidb-ansible v2.1.4 to deploy TiDB v2.1.6), an error might occur.

    - Download the tidb-ansible version with a specified tag:

        ```
        $ git clone -b $tag https://github.com/pingcap/tidb-ansible.git
        ```

    - Download the tidb-ansible version that corresponds to the `master` branch of TiDB:

        ```
        $ git clone https://github.com/pingcap/tidb-ansible.git
        ```

3. Run the `local_prepare.yml` playbook, and download TiDB binary online to the download machine.

    ```
    cd tidb-ansible
    ansible-playbook local_prepare.yml
    ```

4. After running the above command, copy the `tidb-ansible` folder to the `/home/tidb` directory of the Control Machine. The ownership authority of the file must be the `tidb` user.

## Step 5: Configure the SSH mutual trust and sudo rules on the Control Machine

See [Configure the SSH mutual trust and sudo rules on the Control Machine](/how-to/deploy/orchestrated/ansible.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine).

## Step 6: Install the NTP service on the target machines

See [Install the NTP service on the target machines](/how-to/deploy/orchestrated/ansible.md#step-6-install-the-ntp-service-on-the-target-machines).

> **Note:** If the time and time zone of all your target machines are same, the NTP service is on and is normally synchronizing time, you can ignore this step. See [How to check whether the NTP service is normal](#how-to-check-whether-the-ntp-service-is-normal).

## Step 7: Configure the CPUfreq governor mode on the target machine

See [Configure the CPUfreq governor mode on the target machine](/how-to/deploy/orchestrated/ansible.md#step-7-configure-the-cpufreq-governor-mode-on-the-target-machine).

## Step 8: Mount the data disk ext4 filesystem with options on the target machines

See [Mount the data disk ext4 filesystem with options on the target machines](/how-to/deploy/orchestrated/ansible.md#step-8-mount-the-data-disk-ext4-filesystem-with-options-on-the-target-machines).

## Step 9: Edit the `inventory.ini` file to orchestrate the TiDB cluster

See [Edit the `inventory.ini` file to orchestrate the TiDB cluster](/how-to/deploy/orchestrated/ansible.md#step-9-edit-the-inventory-ini-file-to-orchestrate-the-tidb-cluster).

## Step 10: Deploy the TiDB cluster

1. You do not need to run the playbook in `ansible-playbook local_prepare.yml`.

2. You can use the `Report` button on the Grafana Dashboard to generate the PDF file. This function depends on the `fontconfig` package and English fonts. To use this function, download the offline installation package, upload it to the `grafana_servers` machine, and install it. This package includes `fontconfig` and `open-sans-fonts`, and only supports the CentOS 7 system.

    ```
    $ tar -xzvf grafana-font-rpms.el7.tar.gz
    $ cd grafana-font-rpms.el7
    $ chmod u+x install_grafana_font_rpms.sh
    $ ./install_grafana_font_rpms.sh
    ```

3. See [Deploy the TiDB cluster](/how-to/deploy/orchestrated/ansible.md#step-11-deploy-the-tidb-cluster).

## Test the TiDB cluster

See [Test the TiDB cluster](/how-to/deploy/orchestrated/ansible.md#test-the-tidb-cluster).
