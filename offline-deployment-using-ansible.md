---
title: 离线 TiDB Ansible 部署方案
category: how-to
aliases: ['/docs-cn/dev/how-to/deploy/orchestrated/offline-ansible/']
---

# 离线 TiDB Ansible 部署方案

## 准备机器

1. 下载机一台

    - 该机器需开放外网访问，用于下载 TiDB Ansible、TiDB 及相关软件安装包。
    - 推荐安装 CentOS 7.3 及以上版本 Linux 操作系统。

2. 部署目标机器若干及部署中控机一台

    - 系统要求及配置参考[准备机器](/online-deployment-using-ansible.md#准备机器)。
    - 可以无法访问外网。

## 在中控机上安装系统依赖包

1. 在下载机上下载[系统依赖离线安装包](https://download.pingcap.org/ansible-system-rpms.el7.tar.gz)，然后上传至中控机。该离线包仅支持 CentOS 7 系统，包含 `pip` 及 `sshpass`。

2. 在中控机上安装系统依赖包：

    {{< copyable "shell-root" >}}

    ```bash
    tar -xzvf ansible-system-rpms.el7.tar.gz &&
    cd ansible-system-rpms.el7 &&
    chmod u+x install_ansible_system_rpms.sh &&
    ./install_ansible_system_rpms.sh
    ```

3. 安装完成后，可通过 `pip -V` 验证 pip 是否安装成功：

    {{< copyable "shell-root" >}}

    ```bash
    pip -V
    ```

    ```
    pip 8.1.2 from /usr/lib/python2.7/site-packages (python 2.7)
    ```

> **注意：**
>
> 如果你的系统已安装 pip，请确认版本 >= 8.1.2，否则离线安装 TiDB Ansible 及其依赖时，会有兼容问题。

## 在中控机上创建 tidb 用户，并生成 ssh key

参考[在中控机上创建 tidb 用户，并生成 ssh key](/online-deployment-using-ansible.md#第-2-步在中控机上创建-tidb-用户并生成-ssh-key) 即可。

## 在中控机器上离线安装 TiDB Ansible 及其依赖

以下是 CentOS 7 系统 Ansible 离线安装方式：

建议使用 Ansible 2.4 至 2.7.11 版本，Ansible 及相关依赖版本记录在 `tidb-ansible/requirements.txt` 文件中。下面步骤以安装 Ansible 2.5 为例。

1. 在下载机上下载 [Ansible 2.5 离线安装包](https://download.pingcap.org/ansible-2.5.0-pip.tar.gz)，然后上传至中控机。

2. 离线安装 TiDB Ansible 及相关依赖：

    {{< copyable "shell-root" >}}

    ```bash
    tar -xzvf ansible-2.5.0-pip.tar.gz &&
    cd ansible-2.5.0-pip/ &&
    chmod u+x install_ansible.sh &&
    ./install_ansible.sh
    ```

3. 安装完成后，可通过 `ansible --version` 查看版本：

    {{< copyable "shell-root" >}}

    ```bash
    ansible --version
    ```

    ```
    ansible 2.5.0
    ```

## 在下载机上下载 TiDB Ansible 及 TiDB 安装包

1. 在下载机上安装 TiDB Ansible：

    请按以下方式在 CentOS 7 系统的下载机上在线安装 TiDB Ansible。安装完成后，可通过 `ansible --version` 查看版本，请务必确认是 **Ansible 2.5.0** 版本，否则会有兼容问题。

    {{< copyable "shell-root" >}}

    ```bash
    yum install epel-release &&
    yum install ansible curl &&
    ansible --version
    ```

    ```
    ansible 2.5.0
    ```

2. 下载 tidb-ansible：

    使用以下命令从 Github [TiDB Ansible 项目](https://github.com/pingcap/tidb-ansible)上下载 TiDB Ansible 相应版本，默认的文件夹名称为 `tidb-ansible`。

    {{< copyable "shell-regular" >}}

    ```bash
    git clone https://github.com/pingcap/tidb-ansible.git
    ```

    > **注意：**
    >
    > 部署和升级 TiDB 集群需使用对应的 tidb-ansible 版本，通过改 `inventory.ini` 文件中的版本来混用可能会产生一些错误。

3. 执行 `local_prepare.yml` playbook，联网下载 TiDB binary 到下载机：

    {{< copyable "shell-regular" >}}

    ```bash
    cd tidb-ansible &&
    ansible-playbook local_prepare.yml
    ```

4. 将执行完以上命令之后的 `tidb-ansible` 文件夹拷贝到中控机 `/home/tidb` 目录下，文件属主权限需是 `tidb` 用户。

## 在中控机上配置部署机器 SSH 互信及 sudo 规则

参考[在中控机上配置部署机器 SSH 互信及 sudo 规则](/online-deployment-using-ansible.md#第-5-步在中控机上配置部署机器-ssh-互信及-sudo-规则)即可。

## 在部署目标机器上安装 NTP 服务

如果你的部署目标机器时间、时区设置一致，已开启 NTP 服务且在正常同步时间，此步骤可忽略，可参考[如何检测 NTP 服务是否正常](/online-deployment-using-ansible.md#如何检测-ntp-服务是否正常)。

参考[在部署目标机器上安装 NTP 服务](/online-deployment-using-ansible.md#第-6-步在部署目标机器上安装-ntp-服务)即可。

## 在部署目标机器上配置 CPUfreq 调节器模式

参考[在部署目标机器上配置 CPUfreq 调节器模式](/online-deployment-using-ansible.md#第-7-步在部署目标机器上配置-cpufreq-调节器模式)即可。

## 在部署目标机器上添加数据盘 ext4 文件系统挂载参数

参考[在部署目标机器上添加数据盘 ext4 文件系统挂载参数](/online-deployment-using-ansible.md#第-8-步在部署目标机器上添加数据盘-ext4-文件系统挂载参数)即可。

## 分配机器资源，编辑 inventory.ini 文件

参考[分配机器资源，编辑 inventory.ini 文件](/online-deployment-using-ansible.md#第-9-步编辑-inventoryini-文件分配机器资源)即可。

## 部署任务

1. `ansible-playbook local_prepare.yml` 该 playbook 不需要再执行。

2. 参考[部署任务](/online-deployment-using-ansible.md#第-11-步部署-tidb-集群)即可。

## 测试集群

参考[测试集群](/online-deployment-using-ansible.md#测试集群)即可。

> **注意：**
>
> TiDB 默认会定期收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品。若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)。
