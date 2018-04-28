---
title: 从 TiDB 1.0 升级到 2.0 操作指南
category: deployment
---

# 从 TiDB 1.0 升级到 2.0 操作指南

## 在中控机器上安装 Ansible 及其依赖

TiDB-Ansible release-2.0 版本依赖 Ansible 2.4.2 及以上版本，兼容最新的 Ansible 2.5 版本，另依赖 Python 模块: jinja2>=2.9.6 和 jmespath>=0.9.0 。为方便管理依赖，新版本使用 pip 安装 Ansible 及其依赖, 请参照[在中控机器上安装 Ansible 及其依赖](https://github.com/pingcap/docs-cn/blob/master/op-guide/ansible-deployment.md#在中控机器上安装-ansible-及其依赖) 安装。离线环境请参照[在中控机器上离线安装 Ansible 及其依赖](https://github.com/pingcap/docs-cn/blob/master/op-guide/offline-ansible-deployment.md#在中控机器上离线安装-ansible-及其依赖) 。

安装完成后，可通过以下命令查看版本：

```
$ ansible --version
ansible 2.5.2
$ pip show jinja2
Name: Jinja2
Version: 2.9.6
$ pip show jmespath
Name: jmespath
Version: 0.9.0
```

## 在中控机器上下载 TiDB-Ansible

以 `tidb` 用户登录中控机并进入 `/home/tidb` 目录

备份 tidb-ansible release-1.0 分支文件夹:

```
$ mv tidb-ansible tidb-ansible-bak
```

下载最新 tidb-ansible release-2.0 分支，默认的文件夹名称为 `tidb-ansible`。

```
$ git clone -b release-2.0 https://github.com/pingcap/tidb-ansible.git
```

## 编辑 inventory.ini 文件和配置文件

以 `tidb` 用户登录中控机并进入 `/home/tidb/tidb-ansible` 目录。

### 编辑 `inventory.ini` 文件
编辑 `inventory.ini` 文件，IP 信息参照备份文件 `/home/tidb/tidb-ansible-bak/inventory.ini`。

以下变量配置，需要重点确认，变量含义可参考 [inventory.ini 变量调整](https://github.com/pingcap/docs-cn/blob/master/op-guide/ansible-deployment.md#其他变量调整)。

1. 请确认 `ansible_user` 配置的是普通用户。为统一权限管理，不再支持使用 root 用户远程安装。 默认配置中使用 `tidb` 用户作为 SSH 远程用户及程序运行用户。

    ```
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

    可参考[如何配置 ssh 互信及 sudo 免密码](https://github.com/pingcap/docs-cn/blob/master/op-guide/ansible-deployment.md#如何配置-ssh-互信及-sudo-免密码) 自动配置主机间互信。

2. `process_supervision` 变量请与之前版本保持一致，默认推荐使用 systemd。

    ```
    # process supervision, [systemd, supervise]
    process_supervision = systemd
    ```

    如需变更，可参考 [如何调整进程监管方式从 supervise 到 systemd](https://github.com/pingcap/docs-cn/blob/master/op-guide/ansible-deployment.md#如何调整进程监管方式从-supervise-到-systemd), 先使用备份 `/home/tidb/tidb-ansible-bak/` 分支变更进程监管方式再升级。

### 编辑 TiDB 集群组件配置文件
如之前自定义过 TiDB 集群组件配置文件，请参照备份文件修改 `/home/tidb/tidb-ansible/conf` 下对应配置文件。

  > TiKV 配置中 `end-point-concurrency` 变更为 `high-concurrency`、`normal-concurrency` 和 `low-concurrency` 三个参数:

  ```
  readpool:
    coprocessor:
      # Notice: if CPU_NUM > 8, default thread pool size for coprocessors
      # will be set to CPU_NUM * 0.8.
      # high-concurrency: 8
      # normal-concurrency: 8
      # low-concurrency: 8
  ```

  > 单机多 TiKV 实例情况下，需要修改这三个参数，推荐设置：实例数*参数值 = CPU_Vcores * 0.8。

## 下载 TiDB 2.0 binary 到中控机

确认 `tidb-ansible/inventory.ini` 文件中 `tidb_version = v2.0.0`, 然后执行以下命令下载 TiDB 2.0 binary 到中控机。

```
$ ansible-playbook local_prepare.yml
```

## 滚动升级 TiDB 集群组件

```
$ ansible-playbook rolling_update.yml
```

## 滚动升级 TiDB 监控组件

为满足客户监控组件混布需求，监控组件 systemd service 开始按端口区分。

查看 `inventory.ini` 文件中 `process_supervision` 变量: 

```
# process supervision, [systemd, supervise]
process_supervision = systemd
```

如果 `process_supervision = systemd`, 为兼容之前的版本，你需要执行 `migrate_monitor.yml` Playbook。

```
$ ansible-playbook migrate_monitor.yml
```

滚动升级 TiDB 监控组件：

```
$ ansible-playbook rolling_update_monitor.yml
```
