---
title: DM 配置简介
category: reference
---

# DM 配置简介

本文档简要介绍 DM (Data Migration) 的配置文件和数据同步任务的配置。

## 配置文件

- `inventory.ini`：使用 DM-Ansible 部署 DM 集群的配置文件。需要根据所选用的集群拓扑来进行编辑。详见[编辑 `inventory.ini` 配置文件](/dev/how-to/deploy/data-migration-with-ansible.md#第-7-步编辑-inventoryini-配置文件)。
- `dm-master.toml`：DM-master 进程的配置文件，包括 DM 集群的拓扑信息、MySQL 实例与 DM-worker 之间的关系（必须为一对一的关系）。使用 DM-Ansible 部署 DM 集群时，会自动生成 `dm-master.toml` 文件。
- `dm-worker.toml`：DM-worker 进程的配置文件，包括上游 MySQL 实例的配置和 relay log 的配置。使用 DM-Ansible 部署 DM 集群时，会自动生成 `dm-worker.toml` 文件。

## 同步任务配置

### 任务配置文件

使用 DM-Ansible 部署 DM 集群时，`<path-to-dm-ansible>/conf` 中提供了任务配置文件模板：`task.yaml.exmaple` 文件。该文件是 DM 同步任务配置的标准文件，每一个具体的任务对应一个 `task.yaml` 文件。关于该配置文件的详细介绍，参见 [任务配置文件](/dev/reference/tools/data-migration/configure/task-configuration-file.md)。

### 创建数据同步任务

你可以基于 `task.yaml.example` 文件来创建数据同步任务，具体步骤如下：

1. 复制 `task.yaml.example` 为 `your_task.yaml`。
2. 参考[任务配置文件](/dev/reference/tools/data-migration/configure/task-configuration-file.md)来修改 `your_task.yaml` 文件。
3. [使用 dmctl 创建数据同步任务](/dev/reference/tools/data-migration/manage-tasks.md#创建数据同步任务)。

### 关键概念

DM 配置的关键概念如下：

| 概念         | 解释          | 配置文件        |
| :------------ | :------------ | :------------------ |
| source-id  | 唯一确定一个 MySQL 或 MariaDB 实例，或者一个具有主从结构的复制组，字符串长度不大于 32 | `inventory.ini` 的 `source_id`；<br> `dm-master.toml` 的 `source-id`；<br> `task.yaml` 的 `source-id` |
| DM-worker ID | 唯一确定一个 DM-worker（取值于 `dm-worker.toml` 的 `worker-addr` 参数） | `dm-worker.toml` 的 `worker-addr`；<br> dmctl 命令行的 `-worker` / `-w` flag |
