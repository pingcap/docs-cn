---
title: Upgrade Data Migration
summary: Learn how to upgrade a Data Migration version to an incompatible version.
category: how-to
---

# Upgrade Data Migration

This document introduces how to upgrade your Data Migration (DM) version to an incompatible version.

Assuming that V-A, V-B, V-C are three DM versions in chronological order and they are not compatible with each other, you need to upgrade V-A to V-C. Upgrade-A-B means upgrading V-A to V-B and Upgrade-B-C means upgrading V-B to V-C.

- If Upgrade-A-B overlaps with Upgrade-B-C (e.g. different changes of a same configuration item), it is recommended to perform Upgrade-A-B to V-B and then perform Upgrade-B-C to V-C.
- If Upgrade-A-B does not overlap with Upgrade-B-C, you can merge Upgrade-A-B and Upgrade-B-C as Upgrade-A-C to upgrade DM from V-A to V-C.

> **Note:**
>
> - Unless otherwise stated, DM version upgrade means upgrading DM from the previous version with an upgrade procedure to the current version.
> - Unless otherwise stated, all the following upgrade examples assume that you have downloaded the corresponding DM version and DM-Ansible version, and the DM binary exists in the corresponding directory of DM-Ansible. (For how to download the DM binary, see [Upgrade the component version](/v2.1/reference/tools/data-migration/cluster-operations.md#upgrade-the-component-version)).
> - Unless otherwise stated, all the following upgrade examples assume that all the data replication tasks have been stopped before the upgrade and all the replication tasks are restarted manually after DM upgrade is finished.
> - The following shows the upgrade procedure of DM versions in reverse chronological order.

## Upgrade to v1.0.0-rc.1-12-gaa39ff9

### Version information

```bash
Release Version: v1.0.0-rc.1-12-gaa39ff9
Git Commit Hash: aa39ff981dfb3e8c0fa4180127246b253604cc34
Git Branch: dm-master
UTC Build Time: 2019-07-24 02:26:08
Go Version: go version go1.11.2 linux/amd64
```

### Main changes

Starting from this release, TiDB DM checks all configurations rigorously. Unrecognized configuration triggers an error. This is to ensure that users always know exactly what the configuration is.

### Upgrade operation example

Before starting the DM-master or DM-worker, ensure that the obsolete configuration information has been deleted and there are no redundant configuration items.

Otherwise, the starting might fail. In this situation, you can delete the redundant configuration based on the failure information. These are two possible redundant configurations:

- `meta-file` in `dm-worker.toml`
- `server-id` in `mysql-instances` in `task.yaml`

## Upgrade to v1.0.0-143-gcd753da

### Version information

```bash
Release Version: v1.0.0-143-gcd753da
Git Commit Hash: cd753da958ea9a0d5686abc9f1988b61c9d36a89
Git Branch: dm-master
UTC Build Time: 2018-12-25 06:03:11
Go Version: go version go1.11.2 linux/amd64
```

### Main changes

Before this version, DM-worker uses the following two ports to provide different information or services to the outside.

- `dm_worker_port`: 10081 by default. Provides the RPC service to communicate with DM-master.
- `dm_worker_status_port`: 10082 by default. Provides metrics and status information.

Starting from this version, DM-worker uses a same port (8262 by default) to provide the above two kinds of information or services simultaneously.

### Upgrade operation example

1. Modify the `inventory.ini` configuration information.

    - Remove all the `dm_worker_status_port` configuration items and modify the `dm_worker_port` configuration item as needed.
    - Remove all the `dm_master_status_port` configuration items and modify the `dm_master_port` configuration item as needed.

    For example, modify

    ```ini
    dm_worker1_1 ansible_host=172.16.10.72 server_id=101 deploy_dir=/data1/dm_worker dm_worker_port=10081 dm_worker_status_port=10082 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

    to

    ```ini
    dm_worker1_1 ansible_host=172.16.10.72 server_id=101 deploy_dir=/data1/dm_worker dm_worker_port=8262 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

    and modify

    ```ini
    dm_master ansible_host=172.16.10.71 dm_master_port=12080 dm_master_status_port=12081
    ```

    to

    ```ini
    dm_master ansible_host=172.16.10.71 dm_master_port=8261
    ```

2. Use DM-Ansible to perform a rolling update on DM, Prometheus and Grafana.

## Upgrade to v1.0.0-133-g2f9fe82

### Version information

```bash
Release Version: v1.0.0-133-g2f9fe82
Git Commit Hash: 2f9fe827d668add6493b2a3da107e0a01b94c6d1
Git Branch: dm-master
UTC Build Time: 2018-12-19 04:58:46
Go Version: go version go1.11.2 linux/amd64
```

### Main changes

Before this version, `mysql-instances` in the task configuration file (`task.yaml`) contains the following information:

- `config`: the upstream MySQL address, user name and password.
- `instance-id`: identifies an upstream MySQL.

Starting from this version, the above two kinds of information are removed and the following information is added:

- `source_id`: exists in `inventory.ini`, used to identify an upstream MySQL instance or a master-slave replication group.
- `source-id`: exists in `mysql-instances` of the task configuration file. Its value corresponds to `source_id` of `inventory.ini`.

> **Note:**
>
> To guarantee that the checkpoint information of the existing task stored in the downstream database can still be used, the value of `source_id`or `source-id` should be consistent with that of `instance-id` of the corresponding DM-worker.

### Upgrade operation example

1. Modify the `inventory.ini` configuration information.

    Set the corresponding `source_id` for all DM-worker instances.

    For example, modify

    ```ini
    dm-worker1 ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.72 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

    to

    ```ini
    dm-worker1 ansible_host=172.16.10.72 source_id="mysql-replica-01" server_id=101 mysql_host=172.16.10.72 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

2. Use DM-Ansible to perform a rolling update on DM.

3. Modify the task configuration file (`task.yaml`).

    Remove the `config` and `instance-id` configuration items and add the `source-id` configuration item (corresponding to `source_id` in `inventory.ini`).

    For example, modify

    ```yaml
    config:
          host: "192.168.199.118"
          port: 4306
          user: "root"
          password: "1234"
    instance-id: "instance118-4306" # It is unique. It is used as the ID when storing the checkpoint, configuration and other information.
    ```

    to

    ```yaml
    source-id: "instance118-4306" # It should be consistent with the original `source_id` value when the checkpoint of the original task needs to be reused.
    ```

4. Restart the task.
