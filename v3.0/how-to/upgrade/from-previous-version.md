---
title: TiDB 3.0 升级操作指南
category: how-to
aliases: ['/docs-cn/op-guide/tidb-v3.0-upgrade-guide/','/docs-cn/v3.0/how-to/upgrade/to-tidb-3.0']
---

# TiDB 3.0 升级操作指南

本文档适用于从 TiDB 2.0 版本（v2.0.1 及之后版本）或 TiDB 2.1 RC 版本升级到 TiDB 3.0 版本。TiDB 3.0 版本兼容 [Kafka 版本的 TiDB Binlog](/reference/tools/tidb-binlog/tidb-binlog-kafka.md) 以及[TiDB Binlog Cluster 版本](/reference/tidb-binlog-overview.md)。

## 升级兼容性说明

- 不支持在升级后回退至 2.1.x 或更旧版本
- 从 2.0.6 之前的版本升级到 3.0 之前，需要确认集群中是否存在正在运行中的 DDL 操作，特别是耗时的 `Add Index` 操作，等 DDL 操作完成后再执行升级操作
- 2.1 及之后版本启用了并行 DDL，早于 2.0.1 版本的集群，无法滚动升级到 3.0，可以选择下面两种方案：
    - 停机升级，直接从早于 2.0.1 的 TiDB 版本升级到 3.0
    - 先滚动升级到 2.0.1 或者之后的 2.0.x 版本，再滚动升级到 3.0 版本

> **注意：**
>
> 在升级的过程中不要执行 DDL 请求，否则可能会出现行为未定义的问题。

## 在中控机器上安装 Ansible 及其依赖

> **注意：**
>
> 如果已经安装了 Ansible 及其依赖，可跳过该步骤。

TiDB Ansible release-3.0 版本依赖 Ansible 2.4.2 及以上版本（`ansible>=2.4.2`，最好是 2.7.11 版本），另依赖 Python 模块：`jinja2>=2.9.6` 和 `jmespath>=0.9.0`。为方便管理依赖，建议使用 `pip` 安装 Ansible 及其依赖，可参照[在中控机器上安装 Ansible 及其依赖](/how-to/deploy/orchestrated/ansible.md#在中控机器上安装-ansible-及其依赖) 进行安装。离线环境参照[在中控机器上离线安装 Ansible 及其依赖](/how-to/deploy/orchestrated/offline-ansible.md#在中控机器上离线安装-ansible-及其依赖)。

安装完成后，可通过以下命令查看版本：

```
$ ansible --version
ansible 2.7.11
$ pip show jinja2
Name: Jinja2
Version: 2.10
$ pip show jmespath
Name: jmespath
Version: 0.9.0
```

> **注意：**
>
> 请务必按以上文档安装 Ansible 及其依赖。确认 Jinja2 版本是否正确，否则启动 Grafana 时会报错。确认 jmespath 版本是否正确，否则滚动升级 TiKV 时会报错。

## 在中控机器上下载 TiDB Ansible

以 `tidb` 用户登录中控机并进入 `/home/tidb` 目录，备份 TiDB 2.0 版本或 TiDB 2.1 版本的 tidb-ansible 文件夹：

```
$ mv tidb-ansible tidb-ansible-bak
```

下载 TiDB 3.0 版本对应 tag 的 tidb-ansible  [**下载 TiDB Ansible**](/how-to/deploy/orchestrated/ansible.md#在中控机器上下载-tidb-ansible)，默认的文件夹名称为 `tidb-ansible`。

```
$ git clone -b $tag https://github.com/pingcap/tidb-ansible.git
```

## 编辑 inventory.ini 文件和配置文件

以 `tidb` 用户登录中控机并进入 `/home/tidb/tidb-ansible` 目录。

### 编辑 `inventory.ini` 文件

编辑 `inventory.ini` 文件，IP 信息参照备份文件 `/home/tidb/tidb-ansible-bak/inventory.ini`。

以下变量配置，需要重点确认，变量含义可参考 [inventory.ini 变量调整](/how-to/deploy/orchestrated/ansible.md#其他变量调整)。

1. 请确认 `ansible_user` 配置的是普通用户。为统一权限管理，不再支持使用 root 用户远程安装。默认配置中使用 `tidb` 用户作为 SSH 远程用户及程序运行用户。

    ```
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

    可参考[如何配置 ssh 互信及 sudo 规则](/how-to/deploy/orchestrated/ansible.md#在中控机上配置部署机器-ssh-互信及-sudo-规则)自动配置主机间互信。

2. `process_supervision` 变量请与之前版本保持一致，默认推荐使用 `systemd`。

    ```
    # process supervision, [systemd, supervise]
    process_supervision = systemd
    ```

    如需变更，可参考 [如何调整进程监管方式从 supervise 到 systemd](/how-to/deploy/orchestrated/ansible.md#如何调整进程监管方式从-supervise-到-systemd)，先使用备份 `/home/tidb/tidb-ansible-bak/` 分支变更进程监管方式再升级。

### 编辑 TiDB 集群组件配置文件

如之前自定义过 TiDB 集群组件配置文件，请参照备份文件修改 `/home/tidb/tidb-ansible/conf` 下对应配置文件。

**注意以下参数变更：**

- TiKV 配置中 `end-point-concurrency` 变更为 `high-concurrency`、`normal-concurrency` 和 `low-concurrency` 三个参数：

    ```
    readpool:
      coprocessor:
        # Notice: if CPU_NUM > 8, default thread pool size for coprocessors
        # will be set to CPU_NUM * 0.8.
        # high-concurrency: 8
        # normal-concurrency: 8
        # low-concurrency: 8
    ```

    > **注意：**
    >
    > 单机多 TiKV 实例（进程）情况下，需要修改这三个参数。
    >
    > 推荐设置：TiKV 实例数量 \* 参数值 = CPU 核心数量 \* 0.8

- TiKV 配置中不同 CF 中的 `block-cache-size` 参数变更为 `block-cache`

    ```
    storage:
      block-cache:
        capacity: "1GB"
    ```

    > **注意：**
    >
    > 单机多 TiKV 实例（进程）情况下，需要修改 `capacity` 参数。
    >
    > 推荐设置：`capacity` = (MEM_TOTAL * 0.5 / TiKV 实例数量)

## 下载 TiDB 3.0 binary 到中控机

确认 `tidb-ansible/inventory.ini` 文件中 `tidb_version = v3.0.0`，然后执行以下命令下载 TiDB 3.0 binary 到中控机。

```
$ ansible-playbook local_prepare.yml
```

## 滚动升级 TiDB 集群组件

如果当前 `process_supervision` 变量使用默认的 `systemd` 参数，则通过 `excessive_rolling_update.yml` 滚动升级 TiDB 集群。

```
$ ansible-playbook excessive_rolling_update.yml
```

如果当前 `process_supervision` 变量使用 `supervise` 参数，则通过 `rolling_update.yml` 滚动升级 TiDB 集群。

```
$ ansible-playbook rolling_update.yml
```

> **注意：**
>
> 为优化 TiDB 集群组件的运维管理，TiDB 3.0 版本对 `systemd` 模式下的 `PD service` 名称进行了调整。在升级到 TiDB 3.0 版本后，滚动升级及日常滚动重启 TiDB 集群统一使用 `rolling_update.yml` 操作，不再使用 `excessive_rolling_update.yml`。

## 滚动升级 TiDB 监控组件

```
$ ansible-playbook rolling_update_monitor.yml
```
