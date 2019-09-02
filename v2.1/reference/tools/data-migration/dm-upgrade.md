---
title: DM 版本升级
category: reference
---

# DM 版本升级

本文档主要介绍各不完全兼容的 DM (Data Migration) 版本间的升级操作步骤。

假设依时间先后顺序存在 V-A、V-B、V-C 3 个互不兼容的版本，现在需要从 V-A 升级到 V-C。定义从 V-A 升级到 V-B 的操作为 Upgrade-A-B，从 V-B 升级到 V-C 的操作为 Upgrade-B-C。

- 如果 Upgrade-A-B 与 Upgrade-B-C 之间存在交叠（如同一个配置项的不同变更），则推荐先执行 Upgrade-A-B 升级到 V-B，升级完成后再执行 Upgrade-B-C 升级到 V-C。
- 如果 Upgrade-A-B 与 Upgrade-B-C 之间不存在交叠，则可将 Upgrade-A-B 与 Upgrade-B-C 的操作合并为 Upgrade-A-C，执行后直接从 V-A 升级到 V-C。

> **注意：**
>
> - 若无特殊说明，各版本的升级操作均为从前一个有升级指引的版本向当前版本升级。
> - 若无特殊说明，各升级操作示例均假定已经下载了对应版本的 DM 和 DM-Ansible 且 DM binary 存在于 DM-Ansible 的相应目录中（下载 DM binary 可以参考[更新组件版本](/v2.1/reference/tools/data-migration/cluster-operations.md#更新组件版本)）。
> - 若无特殊说明，各升级操作示例均假定升级前已停止所有同步任务，升级完成后手动重新启动所有同步任务。
> - 以下版本升级指引逆序展示。

## 升级到 v1.0.0-rc.1-12-gaa39ff9

### 版本信息

```bash
Release Version: v1.0.0-rc.1-12-gaa39ff9
Git Commit Hash: aa39ff981dfb3e8c0fa4180127246b253604cc34
Git Branch: dm-master
UTC Build Time: 2019-07-24 02:26:08
Go Version: go version go1.11.2 linux/amd64
```

### 主要变更

从此版本开始，将对所有的配置进行严格检查，遇到不识别的配置会报错，以确保用户始终准确地了解自己的配置。

### 升级操作示例

启动 DM-master 或 DM-worker 前，必须确保已经删除废弃的配置信息，且没有多余的配置项，否则会启动失败。可根据失败信息删除多余的配置。
可能遗留的废弃配置:

- `dm-worker.toml` 中的 `meta-file`
- `task.yaml` 中的 `mysql-instances` 中的 `server-id`

## 升级到 v1.0.0-143-gcd753da

### 版本信息

```bash
Release Version: v1.0.0-143-gcd753da
Git Commit Hash: cd753da958ea9a0d5686abc9f1988b61c9d36a89
Git Branch: dm-master
UTC Build Time: 2018-12-25 06:03:11
Go Version: go version go1.11.2 linux/amd64
```

### 主要变更

在此版本前，DM-worker 使用两个端口向外提供不同的信息或服务：

- `dm_worker_port`：默认 10081，提供与 DM-master 通信的 RPC 服务。
- `dm_worker_status_port`：默认 10082，提供 metrics 和 status 等信息。

从此版本开始，DM-worker 使用同一个端口（默认 8262）同时提供上述两类信息或服务。

### 升级操作示例

1. 变更 `inventory.ini` 配置信息。

    - 移除所有 `dm_worker_status_port` 配置项，根据需要变更 `dm_worker_port` 配置项。
    - 移除所有 `dm_master_status_port` 配置项，根据需要变更 `dm_master_port` 配置项。

    如将

    ```ini
    dm_worker1_1 ansible_host=172.16.10.72 server_id=101 deploy_dir=/data1/dm_worker dm_worker_port=10081 dm_worker_status_port=10082 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

    变更为

    ```ini
    dm_worker1_1 ansible_host=172.16.10.72 server_id=101 deploy_dir=/data1/dm_worker dm_worker_port=8262 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

    将

    ```ini
    dm_master ansible_host=172.16.10.71 dm_master_port=12080 dm_master_status_port=12081
    ```

    变更为

    ```ini
    dm_master ansible_host=172.16.10.71 dm_master_port=8261
    ```

2. 使用 DM-Ansible 滚动升级 DM、Prometheus 与 Grafana。

## 升级到 v1.0.0-133-g2f9fe82

### 版本信息

```bash
Release Version: v1.0.0-133-g2f9fe82
Git Commit Hash: 2f9fe827d668add6493b2a3da107e0a01b94c6d1
Git Branch: dm-master
UTC Build Time: 2018-12-19 04:58:46
Go Version: go version go1.11.2 linux/amd64
```

### 主要变更

在此版本前，任务配置文件 (`task.yaml`) 中的 `mysql-instances` 包含以下信息：

- `config`：上游 MySQL 的地址、用户名、密码等。
- `instance-id`：标识一个上游 MySQL。

从此版本开始，上述两项配置信息被移除，并增加了如下配置信息：

- `source_id`：存在于 `inventory.ini` 中，用于标识一个上游 MySQL 实例或一个主从复制组。
- `source-id`：存在于任务配置文件的 `mysql-instances` 中，其取值与 `inventory.ini` 中的 `source_id` 对应。

> **注意：**
>
> 如果需要确保已有任务存储在下游数据库的断点信息能继续被使用，`source_id`/`source-id` 的值需要与对应 DM-worker 变更前的 `instance-id` 一致。

### 升级操作示例

1. 变更 `inventory.ini` 的配置信息。

    为所有 DM-worker 实例设置对应的 `source_id`。

    如将

    ```ini
    dm-worker1 ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.72 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

    变更为

    ```ini
    dm-worker1 ansible_host=172.16.10.72 source_id="mysql-replica-01" server_id=101 mysql_host=172.16.10.72 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

2. 使用 DM-Ansible 滚动升级 DM。

3. 变更任务配置文件 (`task.yaml`)。

    移除其中的 `config` 与 `instance-id` 配置项，增加 `source-id` 配置项（与 `inventory.ini` 中的 `source_id` 对应）。

    如将

    ```yaml
    config:
          host: "192.168.199.118"
          port: 4306
          user: "root"
          password: "1234"
    instance-id: "instance118-4306" # 此值具有唯一性，当保存 checkpoint、配置和其他信息时，作为 ID 使用。
    ```

    变更为

    ```yaml
    source-id: "instance118-4306" # 如需要重用之前任务的 checkpoint，需要与原 `instance-id` 取值一致。
    ```

4. 使用变更后的任务配置重新启动任务。
