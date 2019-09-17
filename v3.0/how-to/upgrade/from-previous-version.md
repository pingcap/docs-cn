---
title: TiDB 3.0 升级操作指南
category: how-to
aliases: ['/docs-cn/op-guide/tidb-v3.0-upgrade-guide/','/docs-cn/v3.0/how-to/upgrade/to-tidb-3.0']
---

# TiDB 3.0 升级操作指南

本文档仅适用于从 TiDB 2.0.1 版本或者 TiDB 2.1 RC1 版本升级到 TiDB 3.0.x 版本。如果版本早于 TiDB 2.0.1 请选择如下两个方案：

1. 停机升级，从当前版本直接升级到 TiDB 3.0.x。
2. 先从当前版本滚动升级到 TiDB 2.0.1， 再按照本文档滚动升级到 TiDB 3.0.x。

## 注意事项

1. TiDB 3.0.x 版本兼容 [Kafka 版本的 TiDB Binlog](/reference/tools/tidb-binlog/tidb-binlog-kafka.md) 以及[TiDB Binlog Cluster 版本](/reference/tidb-binlog-overview.md)。
2. 不支持在升级后版本的回退。
3. 如果版本早于 TiDB 2.0.6 升级到 TiDB 3.0.x ，在升级之前请确保集群中的所有 DDL 都执行完成之后再执行升级操作，否则会有行为未定义的异常。
4. 在升级过程中，请不要执行任何 DDL，否则会有行为未定义的异常。

## 在中控机器上安装 Ansible 及其依赖

1. 安装 Ansible ，要求 `ansible>=2.4.2`，推荐 2.7.11 版本。
2. 安装 Python 模块，要求 `jinja2 >= 2.9.6`和 `jmespath>=0.9.0`。
3. 安装完成后，请检查版本号是否符合要求，命令如下：

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
> * 如果已经安装了 Ansible 及其依赖，则可以跳过该步骤。
> * 建议使用 `pip` 安装 Ansible 及其依赖， 可参考[在中控机器上安装 Ansible 及其依赖](/how-to/deploy/orchestrated/ansible.md#在中控机器上安装-ansible-及其依赖) 及[在中控机器上离线安装 Ansible 及其依赖](/how-to/deploy/orchestrated/offline-ansible.md#在中控机器上离线安装-ansible-及其依赖) 安装 Ansbile 及其相关依赖
> * 请正确安装Ansible 及其依赖，否则会出现以下两种问题
>     * 如果 Jinja2 版本不正确，启动 Grafana 时会报错。
>     * 如果 jmespath 版本不正确，升级 TiKV 时会报错。

## 在中控机器上下载 TiDB-Ansible 并备份老版本文件

1. 以 `tidb` 用户登录中控机并进入 `/home/tidb` 目录
2. 备份当前版本的 tidb-ansible ，命令如下：

    ```
    $ mv tidb-ansible tidb-ansible-bak
    ```

3. 根据 TiDB 3.0 版本对应 tag  [**下载 TiDB-Ansible**](/how-to/deploy/orchestrated/ansible.md#在中控机器上下载-tidb-ansible)，默认下载的文件夹名称为 `tidb-ansible`，命令如下：

    ```
    $ git clone -b $tag https://github.com/pingcap/tidb-ansible.git
    ```

## 修改配置文件

>**注意:**
>
>* 请以 `tidb` 用户登录中控机。
>
>* TiDB Ansible 工作目录在 `/home/tidb/tidb-ansible` 目录。

### 修改 `inventory.ini` 文件

1. 从备份的 Ansible 文件中的 inventory.ini 文件拷贝 IP 信息到新的 inventory.ini。
2. 请确认 `ansible_user`  变量的值是普通用户，例如： `tidb` 。TiDB Ansible 默认使用 `tidb` 用户作为 SSH 远程用户及程序运行用户，如果主机之间互信未建立，请参考[如何配置 ssh 互信及 sudo 规则](/how-to/deploy/orchestrated/ansible.md#在中控机上配置部署机器-ssh-互信及-sudo-规则)。
3. 请确认`process_supervision` 变量与之前版本保持一致，如果要变更请参考 [如何调整进程监管方式从 supervise 到 systemd](/how-to/deploy/orchestrated/ansible.md#如何调整进程监管方式从-supervise-到-systemd)，请变更完成后再升级版本。

>**注意：**
>
>* 请以 `tidb` 用户登录中控机
>
>* TiDB Ansible 配置文件在 `/home/tidb/tidb-ansible` 目录

### 修改 TiDB 集群组件配置文件

1. 从备份的 Ansible 文件中拷贝集群的配置信息到新的配置文件，配置文件名称是`/home/tidb/tidb-ansible/conf`
2. TiKV 配置中 `end-point-concurrency` 变更为 `high-concurrency`、`normal-concurrency` 和 `low-concurrency` 三个参数：

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

3. TiKV 配置中不同 CF 中的 `block-cache-size` 参数变更为 `block-cache`

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

1. 请确认 `tidb-ansible/inventory.ini` 文件中 `tidb_version = v3.0.x`。
2. 执行以下命令下载 TiDB 3.0 binary 到中控机。

```
$ ansible-playbook local_prepare.yml
```

## 滚动升级 TiDB 集群组件

1. 滚动升级 TiDB 集群组件，根据 `process_supervision` 变量值不同，需要执行不同的命令，如下：

   如果变量的值是 `systemd` ，则执行：

```
$ ansible-playbook excessive_rolling_update.yml
```

   如果变量的值是 `systemd` ，则执行：

```
$ ansible-playbook rolling_update.yml
```

> **注意：**
>
> 版本升级到 TiDB 3.0.x 以后，滚动升级及滚动重启 TiDB 统一使用 `rolling_update.yml` 完成相关操作

## 滚动升级 TiDB 监控组件

1. 滚动升级 TiDB 集群监控组件，命令如下：

```
$ ansible-playbook rolling_update_monitor.yml
```
