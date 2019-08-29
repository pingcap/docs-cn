---
title: 离线 TiDB-Ansible 部署方案
category: how-to
aliases: ['/docs-cn/op-guide/offline-ansible-deployment/']
---

# 离线 TiDB-Ansible 部署方案

## 准备机器

1. 下载机一台

    - 该机器需开放外网访问，用于下载 TiDB-Ansible、TiDB 及相关软件安装包。
    - 推荐安装 CentOS 7.3 及以上版本 Linux 操作系统。

2. 部署目标机器若干及部署中控机一台

    - 系统要求及配置参考[准备机器](/how-to/deploy/orchestrated/ansible.md#准备机器)。
    - 可以无法访问外网。

## 在中控机上安装系统依赖包

> 下载[系统依赖离线安装包](https://download.pingcap.org/ansible-system-rpms.el7.tar.gz)，上传至中控机。该离线包仅支持 CentOS 7 系统，包含 `pip` 及 `sshpass`。

{{< copyable "shell-root" >}}

```bash
tar -xzvf ansible-system-rpms.el7.tar.gz &&
cd ansible-system-rpms.el7 &&
chmod u+x install_ansible_system_rpms.sh &&
./install_ansible_system_rpms.sh
```

安装完成后，可通过 `pip -V` 验证 pip 是否安装成功：

{{< copyable "shell-root" >}}

```bash
pip -V
```

```
pip 8.1.2 from /usr/lib/python2.7/site-packages (python 2.7)
```

> 如果你的系统已安装 pip，请确认版本 >= 8.1.2，否则离线安装 ansible 及其依赖时，会有兼容问题。

## 在中控机上创建 tidb 用户，并生成 ssh key

参考[在中控机上创建 tidb 用户，并生成 ssh key](/how-to/deploy/orchestrated/ansible.md#在中控机上创建-tidb-用户-并生成-ssh-key) 即可。

## 在中控机器上离线安装 Ansible 及其依赖

以下是 CentOS 7 系统 Ansible 离线安装方式：

目前 release-2.0 及 master 版本兼容 Ansible 2.5 版本，Ansible 及相关依赖版本记录在 `tidb-ansible/requirements.txt` 文件中，请下载 Ansible 2.5 离线安装包上传至中控机。

> 下载 [Ansible 2.5 离线安装包](https://download.pingcap.org/ansible-2.5.0-pip.tar.gz)

下面以安装 Ansible 2.5 为例：

{{< copyable "shell-root" >}}

```bash
tar -xzvf ansible-2.5.0-pip.tar.gz &&
cd ansible-2.5.0-pip/ &&
chmod u+x install_ansible.sh &&
./install_ansible.sh
```

安装完成后，可通过 `ansible --version` 查看版本：

{{< copyable "shell-root" >}}

```bash
ansible --version
```

```
ansible 2.5.0
```

## 在下载机上下载 TiDB-Ansible 及 TiDB 安装包

以下为 tidb-ansible 与 TiDB 的版本对应关系，版本选择可以咨询官方。

| TiDB 版本 | tidb-ansible tag | 备注 |
| -------- | ---------------- | --- |
| 2.0 版本 | v2.0.10、v2.0.11 | 最新 2.0 稳定版本，可用于生产环境。 |
| 2.1 版本 | v2.1.1 ~ v2.1.6 | 最新 2.1 稳定版本，可用于生产环境（建议）。 |
| 3.0 版本 | v3.0.0-beta、v3.0.0-beta.1 | 目前是 beta 版本，不建议用于生产环境。 |
| latest 版本 | None | 包含最新特性，每日更新，不建议用于生产环境。 |

1. 在下载机上安装 Ansible

    请按以下方式在 CentOS 7 系统的下载机上在线安装 Ansible。安装完成后，可通过 `ansible --version` 查看版本，请务必确认是 **Ansible 2.5.0** 版本，否则会有兼容问题。

    {{< copyable "shell-root" >}}

    ```bash
    yum install epel-release &&
    yum install ansible curl &&
    ansible --version
    ```

    ```
    ansible 2.5.0
    ```

2. 下载 tidb-ansible

    使用以下命令从 Github [TiDB-Ansible 项目](https://github.com/pingcap/tidb-ansible)上下载 TiDB-Ansible 相应版本，默认的文件夹名称为 `tidb-ansible`。

    > **注意：**
    >
    > 部署和升级 TiDB 集群需使用对应的 tidb-ansible 版本，通过改 `inventory.ini` 文件中的版本来混用可能会产生一些错误。

    - 下载指定 tag 的 tidb-ansible：

        {{< copyable "shell-regular" >}}

        ```bash
        git clone -b $tag https://github.com/pingcap/tidb-ansible.git
        ```

    - 下载 latest 版本对应的 tidb-ansible：

        {{< copyable "shell-regular" >}}

        ```bash
        git clone https://github.com/pingcap/tidb-ansible.git
        ```

3. 执行 `local_prepare.yml` playbook，联网下载 TiDB binary 到下载机

    {{< copyable "shell-regular" >}}

    ```bash
    cd tidb-ansible &&
    ansible-playbook local_prepare.yml
    ```

4. 将执行完以上命令之后的 `tidb-ansible` 文件夹拷贝到中控机 `/home/tidb` 目录下，文件属主权限需是 `tidb` 用户。

## 在中控机上配置部署机器 ssh 互信及 sudo 规则

参考[在中控机上配置部署机器 ssh 互信及 sudo 规则](/how-to/deploy/orchestrated/ansible.md#在中控机上配置部署机器-ssh-互信及-sudo-规则)即可。

## 在部署目标机器上安装 NTP 服务

> 如果你的部署目标机器时间、时区设置一致，已开启 NTP 服务且在正常同步时间，此步骤可忽略，可参考[如何检测 NTP 服务是否正常](/how-to/deploy/orchestrated/ansible.md#如何检测-ntp-服务是否正常)。

参考[在部署目标机器上安装 NTP 服务](/how-to/deploy/orchestrated/ansible.md#在部署目标机器上安装-ntp-服务)即可。

## 在部署目标机器上配置 CPUfreq 调节器模式

参考[在部署目标机器上配置 CPUfreq 调节器模式](/how-to/deploy/orchestrated/ansible.md#在部署目标机器上配置-cpufreq-调节器模式)即可。

## 在部署目标机器上添加数据盘 ext4 文件系统挂载参数

参考[在部署目标机器上添加数据盘 ext4 文件系统挂载参数](/how-to/deploy/orchestrated/ansible.md#在部署目标机器上添加数据盘-ext4-文件系统挂载参数)即可。

## 分配机器资源，编辑 inventory.ini 文件

参考[分配机器资源，编辑 inventory.ini 文件](/how-to/deploy/orchestrated/ansible.md#分配机器资源-编辑-inventory-ini-文件)即可。

## 部署任务

1. `ansible-playbook local_prepare.yml` 该 playbook 不需要再执行。

2. Grafana Dashboard 上的 Report 按钮可用来生成 PDF 文件，此功能依赖 `fontconfig` 包及英文字体，如需使用该功能，请下载 [font 离线安装包](https://download.pingcap.org/grafana-font-rpms.el7.tar.gz)上传至 **grafana_servers** 机器上安装。该离线包仅支持 CentOS 7 系统，包含 `fontconfig` 及 `open-sans-fonts`。

    {{< copyable "shell-regular" >}}

    ```bash
    tar -xzvf grafana-font-rpms.el7.tar.gz &&
    cd grafana-font-rpms.el7 &&
    chmod u+x install_grafana_font_rpms.sh &&
    ./install_grafana_font_rpms.sh
    ```

3. 参考[部署任务](/how-to/deploy/orchestrated/ansible.md#部署任务)即可。

## 测试集群

参考[测试集群](/how-to/deploy/orchestrated/ansible.md#测试集群)即可。
