---
title: 离线 TiDB Ansible 部署方案
category: deployment
---

# 离线 TiDB Ansible 部署方案

## 准备机器

1.  下载机一台

    - 该机器需开放外网访问，用于下载 TiDB-Ansible、TiDB 及相关软件安装包。
    - 推荐安装 CentOS 7.3 及以上版本 Linux 操作系统。

2.  部署目标机器若干及部署中控机一台

    - 系统要求及配置参考[准备机器](ansible-deployment.md#准备机器)。
    - 可以无法访问外网。

## 在中控机器上离线安装 Ansible 及其依赖

以下是 CentOS 7 系统 Ansible 离线安装方式：

1.  离线安装 pip :
    > 下载 [ pip 离线安装包 ](https://download.pingcap.org/pip-rpms.el7.tar.gz), 上传至中控机。

    ```bash
    # tar -xzvf pip-rpms.el7.tar.gz
    # cd pip-rpms.el7
    # chmod u+x install_pip.sh
    # ./install_pip.sh
    ```

    安装完成后，可通过 `pip -V` 验证 pip 是否安装成功：

    ```bash
    # pip -V
     pip 8.1.2 from /usr/lib/python2.7/site-packages (python 2.7)
    ```

    > 如果你的系统已安装 pip, 请确认版本 >= 8.1.2, 否则离线安装 ansible 及其依赖时，会有兼容问题。

2.  离线安装 Ansible 及其依赖：

    目前 release-1.0 版本依赖 Ansible 2.4，release-2.0 及 master 版本兼容 Ansible 2.4 及 Ansible 2.5 版本，Ansible 及相关依赖版本记录在 `tidb-ansible/requirements.txt` 文件中，请下载对应版本离线安装包上传至中控机。

    > 下载 [Ansible 2.4 离线安装包](https://download.pingcap.org/ansible-2.4.2-pip.tar.gz)

    > 下载 [Ansible 2.5 离线安装包](https://download.pingcap.org/ansible-2.5.0-pip.tar.gz)

    下面以安装 Ansible 2.5 为例，Ansible 2.4 安装方式与之一致：

    ```
    # tar -xzvf ansible-2.5.0-pip.tar.gz
    # cd ansible-2.5.0-pip/
    # chmod install_ansible.sh
    # ./install_ansible.sh
    ```

    安装完成后，可通过 `ansible --version` 查看版本：

    ```bash
    # ansible --version
     ansible 2.5.0
    ```

## 在下载机上下载 TiDB-Ansible 及 TiDB 安装包

1.  在下载机上安装 Ansible

    请按以下方式在 CentOS 7 系统的下载机上在线安装 Ansible。安装完成后，可通过 `ansible --version` 查看版本，请务必确认是 **Ansible 2.4** 及以上版本，否则会有兼容问题。

    ```bash
    # yum install epel-release
    # yum install ansible curl
    # ansible --version   
      ansible 2.5.0
    ```

2.  下载 tidb-ansible

    使用以下命令从 Github [TiDB-Ansible 项目](https://github.com/pingcap/tidb-ansible) 上下载 TiDB-Ansible 相应版本，默认的文件夹名称为 `tidb-ansible`，以下为各版本下载示例，版本选择可以咨询官方。

    下载 2.0 GA 版本：
    ```
    git clone -b release-2.0 https://github.com/pingcap/tidb-ansible.git
    ```

    或

    下载 master 版本：
    ```
    git clone https://github.com/pingcap/tidb-ansible.git
    ```

3.  执行 `local_prepare.yml` playbook，联网下载 TiDB binary 到下载机

    ```
    cd tidb-ansible
    ansible-playbook local_prepare.yml
    ```

4.  将执行完以上命令之后的 `tidb-ansible` 文件夹拷贝到中控机 `/home/tidb` 目录下，文件属主权限需是 `tidb` 用户。

## 分配机器资源，编辑 inventory.ini 文件

参考[分配机器资源，编辑 inventory.ini 文件](ansible-deployment.md#分配机器资源编辑-inventoryini-文件)即可。

## 部署任务

1.  `ansible-playbook local_prepare.yml` 该 playbook 不需要再执行。

2.  Grafana Dashboard 上的 Report 按钮可用来生成 PDF 文件, 此功能依赖 `fontconfig` 包, 如需使用该功能，请下载 [fontconfig 离线安装包](https://download.pingcap.org/fontconfig-rpms.el7.tar.gz) 上传至 grafana_servers 机器安装。

    ```
    $ tar -xzvf fontconfig-rpms.el7.tar.gz
    $ cd fontconfig-rpms.el7/offline_packages
    $ chmod u+x install_fontconfig.sh
    $ ./install_fontconfig.sh
    ```

3.  参考[部署任务](ansible-deployment.md#部署任务)即可。

## 测试集群

参考[测试集群](ansible-deployment.md#测试集群)即可。
