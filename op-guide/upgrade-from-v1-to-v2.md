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

编辑 `inventory.ini` 文件，IP 信息参照备份文件 `/home/tidb/tidb-ansible-bak/inventory.ini`。

如之前自定义过 TiDB 集群组件配置，请参照备份文件修改 `/home/tidb/tidb-ansible/conf` 下对应配置文件。

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
