---
title: Data Migration Configuration File Overview
summary: This document gives an overview of Data Migration configuration files. 
category: tools
---

# Data Migration Configuration File Overview

This document gives an overview of configuration files of DM (Data Migration). 

## DM process configuration files

- `inventory.ini`: The configuration file of deploying DM using DM-Ansible. You need to edit it based on your machine topology. For details, see [Edit the `inventory.ini` file to orchestrate the DM cluster](../tools/data-migration-deployment.md#step-7-edit-the-inventoryini-file-to-orchestrate-the-dm-cluster).
- `dm-master.toml`: The configuration file of running the DM-master process, including the topology information of the DM cluster and the corresponding relationship between the MySQL instance and DM-worker (must be one-to-one relationship). When you use DM-Ansible to deploy DM, `dm-master.toml` is generated automatically.
- `dm-worker.toml`: The configuration file of running the DM-worker process, including the configuration information of upstream MySQL instance. When you use DM-Ansible to deploy DM, `dm-worker.toml` is generated automatically.

## DM replication task configuration

### DM task configuration file

When you use DM-Ansible to deploy DM, you can find the following task configuration file template in `<path-to-dm-ansible>/conf`:

- `task.yaml.exmaple`: The standard configuration file of the data replication task (a specific task corresponds to a `task.yaml`). For the introduction of the configuration file, see [Task Configuration File](../tools/dm-task-configuration-file-intro.md).

### Data replication task creation

You can perform the following steps to create a data replication task based on `task.yaml.example`:

1. Copy `task.yaml.example` as `your_task.yaml`.
2. Refer to the description in the [Task Configuration File](../tools/dm-task-configuration-file-intro.md) and modify the configuration in `your_task.yaml`.
3. Create your data replication task using dmctl.

### Important concepts

This section shows description of some important concepts.

| Concept         | Description                                                         | Configuration File                                                     |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `instance-id`  | Specifies a MySQL/MariaDB instance (if you deploy DM using DM-ansible, `host:port` is used to construct this ID) | `mysql-instance` of `dm-master.toml`;<br> `instance-id` of `task.yaml` |
| DM-worker ID | Specifies a DM-worker (from the `worker-addr` parameter of `dm-worker.toml`) | `worker-addr` of `dm-worker.toml`;<br> the `-worker`/`-w` flag of the dmctl command line |

> **Note:**
>
> You must keep `mysql-instance` and DM-worker at a one-to-one relationship. 
