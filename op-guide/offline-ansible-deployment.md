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

## Install Ansible and dependencies offline in the Control Machine

Take the following steps to install Ansible offline on the CentOS 7 system:

1. Install `pip` offline.

    > Download the [`pip`](https://download.pingcap.org/pip-rpms.el7.tar.gz) offline installation package to the Control Machine.

    ```bash
    # tar -xzvf pip-rpms.el7.tar.gz
    # cd pip-rpms.el7
    # chmod u+x install_pip.sh
    # ./install_pip.sh
    ```

    After the installation is finished, you can use `pip -V` to check whether it is successfully installed:

    ```bash
    # pip -V
     pip 8.1.2 from /usr/lib/python2.7/site-packages (python 2.7)
    ```

    > **Note:** If `pip` is already installed to your system, make sure that the version is 8.1.2 or later. Otherwise, compatibility error occurs when you install Ansible and its dependencies offline.

2. Install Ansible and its dependencies offline.

    Currently releases-1.0 depends on Ansible 2.4, while release-2.0 and the master version are compatible with Ansible 2.4 and Ansible 2.5. Ansible and related dependencies are recorded in the `tidb-ansible/requirements.txt` file. Download the corresponding offline installation version to the Control Machine.

    - Download [Ansible 2.4 offline installation package](https://download.pingcap.org/ansible-2.4.2-pip.tar.gz)
    - Download [Ansible 2.5 offline installation package](https://download.pingcap.org/ansible-2.5.0-pip.tar.gz)

    The installing methods of Ansible 2.4 and Ansible 2.5 are similar. Take Ansible 2.5 as an example:

    ```
    # tar -xzvf ansible-2.5.0-pip.tar.gz
    # cd ansible-2.5.0-pip/
    # chmod install_ansible.sh
    # ./install_ansible.sh
    ```

    After Ansible is installed, you can view the version using `ansible --version`.

    ```bash
    # ansible --version
     ansible 2.5.0
    ```

## Download TiDB-Ansible and TiDB packages on the download machine

1. Install Ansible on the download machine.

    Use the following method to install Ansible online on the download machine installed with the CentOS 7 system. After Ansible is installed, you can view the version using `ansible --version`.

    ```bash
    # yum install epel-release
    # yum install ansible curl
    # ansible --version
      ansible 2.5.0
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

1. You do not need to run the `ansible-playbook local_prepare.yml` playbook again.
2. You can use the `Report` button on the Grafana Dashboard to generate the PDF file. This function depends on the `fontconfig` package. To use this function, download the [`fontconfig` offline installation package](https://download.pingcap.org/fontconfig-rpms.el7.tar.gz) and upload it to the `grafana_servers` machine to install.

    ```
    $ tar -xzvf fontconfig-rpms.el7.tar.gz
    $ cd fontconfig-rpms.el7/offline_packages
    $ chmod u+x install_fontconfig.sh
    $ ./install_fontconfig.sh
    ```

3. Refer to [Deploy the TiDB cluster](ansible-deployment.md#deploy-the-tidb-cluster).

## Test the cluster

See [Test the cluster](ansible-deployment.md#test-the-cluster).