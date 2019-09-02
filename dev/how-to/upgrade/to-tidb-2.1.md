---
title: TiDB 2.1 升级操作指南
category: how-to
---

# TiDB 2.1 升级操作指南

本文档适用于从 TiDB 2.0 版本（v2.0.1 及之后版本）或 TiDB 2.1 RC 版本升级到 TiDB 2.1 GA 版本。TiDB 2.1 版本不兼容 Kafka 版本的 TiDB Binlog，如果当前集群已经使用 [Kafka 版本的 TiDB Binlog](/dev/reference/tools/tidb-binlog/tidb-binlog-kafka.md)，须参考 [TiDB Binlog Cluster 版本升级方法](/dev/how-to/upgrade/tidb-binlog.md) 升级到 Cluster 版本。

## 升级兼容性说明

- 新版本存储引擎更新，不支持在升级后回退至 2.0.x 或更旧版本
- 从 2.0.6 之前的版本升级到 2.1 之前，需要确认集群中是否存在正在运行中的 DDL 操作，特别是耗时的 `Add Index` 操作，等 DDL 操作完成后再执行升级操作
- 2.1 版本启用了并行 DDL，早于 2.0.1 版本的集群，无法滚动升级到 2.1，可以选择下面两种方案：
    - 停机升级，直接从早于 2.0.1 的 TiDB 版本升级到 2.1
    - 先滚动升级到 2.0.1 或者之后的 2.0.x 版本，再滚动升级到 2.1 版本

## 注意事项

在升级的过程中不要执行 DDL 请求，否则可能会出现行为未定义的问题。

## 在中控机器上安装 Ansible 及其依赖

TiDB Ansible release-2.1 版本依赖 2.4.2 及以上但不高于 2.7.0 的 Ansible 版本（`ansible>=2.4.2,<2.7.0`），另依赖 Python 模块：`jinja2>=2.9.6` 和 `jmespath>=0.9.0`。为方便管理依赖，新版本使用 `pip` 安装 Ansible 及其依赖，可参照[在中控机器上安装 Ansible 及其依赖](/dev/how-to/deploy/orchestrated/ansible.md#在中控机器上安装-ansible-及其依赖) 进行安装。离线环境参照[在中控机器上离线安装 Ansible 及其依赖](/dev/how-to/deploy/orchestrated/offline-ansible.md#在中控机器上离线安装-ansible-及其依赖)。

安装完成后，可通过以下命令查看版本：

```
$ ansible --version
ansible 2.6.8
$ pip show jinja2
Name: Jinja2
Version: 2.10
$ pip show jmespath
Name: jmespath
Version: 0.9.3
```

> **注意：**
>
> 请务必按以上文档安装 Ansible 及其依赖。确认 Jinja2 版本是否正确，否则启动 Grafana 时会报错。确认 jmespath 版本是否正确，否则滚动升级 TiKV 时会报错。

## 在中控机器上下载 TiDB Ansible

以 `tidb` 用户登录中控机并进入 `/home/tidb` 目录，备份 TiDB 2.0 版本或 TiDB 2.1 rc 版本的 tidb-ansible 文件夹：

```
$ mv tidb-ansible tidb-ansible-bak
```

下载最新 tidb-ansible release-2.1 分支，默认的文件夹名称为 `tidb-ansible`。

```
$ git clone -b release-2.1 https://github.com/pingcap/tidb-ansible.git
```

## 编辑 inventory.ini 文件和配置文件

以 `tidb` 用户登录中控机并进入 `/home/tidb/tidb-ansible` 目录。

### 编辑 `inventory.ini` 文件

编辑 `inventory.ini` 文件，IP 信息参照备份文件 `/home/tidb/tidb-ansible-bak/inventory.ini`。

以下变量配置，需要重点确认，变量含义可参考 [inventory.ini 变量调整](/dev/how-to/deploy/orchestrated/ansible.md#其他变量调整)。

1. 请确认 `ansible_user` 配置的是普通用户。为统一权限管理，不再支持使用 root 用户远程安装。默认配置中使用 `tidb` 用户作为 SSH 远程用户及程序运行用户。

    ```
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

    可参考[如何配置 ssh 互信及 sudo 规则](/dev/how-to/deploy/orchestrated/ansible.md#在中控机上配置部署机器-ssh-互信及-sudo-规则) 自动配置主机间互信。

2. `process_supervision` 变量请与之前版本保持一致，默认推荐使用 `systemd`。

    ```
    # process supervision, [systemd, supervise]
    process_supervision = systemd
    ```

    如需变更，可参考 [如何调整进程监管方式从 supervise 到 systemd](/dev/how-to/deploy/orchestrated/ansible.md#如何调整进程监管方式从-supervise-到-systemd)，先使用备份 `/home/tidb/tidb-ansible-bak/` 分支变更进程监管方式再升级。

### 编辑 TiDB 集群组件配置文件

如之前自定义过 TiDB 集群组件配置文件，请参照备份文件修改 `/home/tidb/tidb-ansible/conf` 下对应配置文件。

TiKV 配置中 `end-point-concurrency` 变更为 `high-concurrency`、`normal-concurrency` 和 `low-concurrency` 三个参数：

```
readpool:
  coprocessor:
    # Notice: if CPU_NUM > 8, default thread pool size for coprocessors
    # will be set to CPU_NUM * 0.8.
    # high-concurrency: 8
    # normal-concurrency: 8
    # low-concurrency: 8
```

单机多 TiKV 实例情况下，需要修改这三个参数，推荐设置：`实例数 * 参数值 = CPU 核数 * 0.8`。

## 下载 TiDB 2.1 binary 到中控机

确认 `tidb-ansible/inventory.ini` 文件中 `tidb_version = v2.1.0`，然后执行以下命令下载 TiDB 2.1 binary 到中控机。

```
$ ansible-playbook local_prepare.yml
```

## 滚动升级 TiDB 集群组件

```
$ ansible-playbook rolling_update.yml
```

## 滚动升级 TiDB 监控组件

```
$ ansible-playbook rolling_update_monitor.yml
```
