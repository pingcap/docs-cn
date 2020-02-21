---
title: Upgrade Data Migration
summary: Learn how to upgrade a Data Migration version to an incompatible version.
category: how-to
aliases: ['/docs/dev/how-to/upgrade/data-migration/']
---

# Upgrade Data Migration

This document introduces how to upgrade your Data Migration (DM) version to an incompatible version.

> **Note:**
>
> - Unless otherwise stated, DM version upgrade means upgrading DM from the previous version with an upgrade procedure to the current version.
> - Unless otherwise stated, all the following upgrade examples assume that you have downloaded the corresponding DM version and DM-Ansible version, and the DM binary exists in the corresponding directory of DM-Ansible. (For how to download the DM binary, see [Upgrade the component version](/reference/tools/data-migration/cluster-operations.md#upgrade-the-component-version)).
> - Unless otherwise stated, all the following upgrade examples assume that all the data replication tasks have been stopped before the upgrade and all the replication tasks are restarted manually after DM upgrade is finished.
> - The following shows the upgrade procedure of DM versions in reverse chronological order.

## Upgrade to v1.0.3

### Version information

```bash
Release Version: v1.0.3
Git Commit Hash: 41426af6cffcff9a325697a3bdebeadc9baa8aa6
Git Branch: release-1.0
UTC Build Time: 2019-12-13 07:04:53
Go Version: go version go1.13 linux/amd64
```

### Main changes

- Add the command mode in dmctl
- Support replicating the `ALTER DATABASE` DDL statement
- Optimize the error message output
- Fix the panic-causing data race issue occurred when the full import unit pauses or exits
- Fix the issue that `stop-task` and `pause-task` might not take effect when retrying SQL operations to the downstream

### Upgrade operation example

1. Download the new version of DM-Ansible, and confirm that there is `dm_version = v1.0.3` in the `inventory.ini` file.
2. Run `ansible-playbook local_prepare.yml` to download the new DM binary file to the local disk.
3. Run `ansible-playbook rolling_update.yml` to perform a rolling update for the DM cluster components.
4. Run `ansible-playbook rolling_update_monitor.yml` to perform a rolling update for the DM monitoring components.

> **Note:**
>
> When you upgrade DM to the 1.0.3 version, you must make sure that all DM cluster components (dmctl, DM-master, and DM-worker) are upgraded. Do not upgrade only a part of the components. Otherwise, an error might occur.

## Upgrade to v1.0.2

### Version information

```bash
Release Version: v1.0.2
Git Commit Hash: affc6546c0d9810b0630e85502d60ed5c800bf25
Git Branch: release-1.0
UTC Build Time: 2019-10-30 05:08:50
Go Version: go version go1.12 linux/amd64
```

### Main changes

- Support automatically generating some configuration items for DM-worker to reduce manual configuration cost
- Support automatically generating the parameters of Mydumper database and tables to reduce manual configuration cost
- Optimize the default output of `query-status` to highlight important information
- Directly manage the DB connection to the downstream instead of using the built-in connection pool to optimize the handling of and retry for SQL errors
- Fix the panic that might occur when the DM-worker process is started or when the DML statement is failed to execute
- Fix the bug that the timeout of executing the sharding DDL statements (for example, `ADD INDEX`) might cause that the subsequent sharding DDL statements cannot be correctly coordinated
- Fix the bug that the `start-task` command cannot be executed when some DM-workers are inaccessible
- Improve the automatic retry policy for the `1105` error

### Upgrade operation example

1. Download the new version of DM-Ansible, and confirm that there is `dm_version = v1.0.2` in the `inventory.ini` file.
2. Run `ansible-playbook local_prepare.yml` to download the new DM binary file to the local disk.
3. Run `ansible-playbook rolling_update.yml` to perform a rolling update for the DM cluster components.
4. Run `ansible-playbook rolling_update_monitor.yml` to perform a rolling update for the DM monitoring components.

> **Note:**
>
> When you upgrade DM to the 1.0.2 version, you must make sure that all DM cluster components (dmctl, DM-master, and DM-worker) are upgraded. Do not upgrade only a part of the components. Otherwise, an error might occur.

## Upgrade to v1.0.1

### Version information

```bash
Release Version: v1.0.1
Git Commit Hash: e63c6cdebea0edcf2ef8c91d84cff4aaa5fc2df7
Git Branch: release-1.0
UTC Build Time: 2019-09-10 06:15:05
Go Version: go version go1.12 linux/amd64
```

### Main changes

- Fix the issue that DM frequently re-establishes the database connection in some situations
- Fix the panic that might occur when using the `query-status` command

### Upgrade operation example

1. Download the new version of DM-Ansible, and confirm that there is `dm_version = v1.0.1` in the `inventory.ini` file.
2. Run `ansible-playbook local_prepare.yml` to download the new DM binary file to the local disk.
3. Run `ansible-playbook rolling_update.yml` to perform a rolling update for the DM cluster components.
4. Run `ansible-playbook rolling_update_monitor.yml` to perform a rolling update for the DM monitoring components.

> **Note:**
>
> When you upgrade DM to the 1.0.1 version, you must make sure that all DM cluster components (dmctl, DM-master, and DM-worker) are upgraded. Do not upgrade only a part of the components. Otherwise, an error might occur.

## Upgrade to v1.0.0-10-geb2889c9 (1.0 GA)

### Version information

```bash
Release Version: v1.0.0-10-geb2889c9
Git Commit Hash: eb2889c9dcfbff6653be9c8720a32998b4627db9
Git Branch: release-1.0
UTC Build Time: 2019-09-06 03:18:48
Go Version: go version go1.12 linux/amd64
```

### Main changes

- Support automatically recovering replication tasks for some abnormal situations
- Improve compatibility with DDL syntaxes
- Fix the bug that the abnormal connection to the upstream database might cause data loss

### Upgrade operation example

1. Download the new version of DM-Ansible, and confirm that there is `dm_version = v1.0.0` in the `inventory.ini` file.
2. Run `ansible-playbook local_prepare.yml` to download the new DM binary file to the local disk.
3. Run `ansible-playbook rolling_update.yml` to perform a rolling update for the DM cluster components.
4. Run `ansible-playbook rolling_update_monitor.yml` to perform a rolling update for the DM monitoring components.

> **Note:**
>
> When you upgrade DM to the 1.0 GA version, you must make sure that all DM cluster components (dmctl, DM-master, and DM-worker) are upgraded. Do not upgrade only a part of the components. Otherwise, an error might occur.

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

Starting from this release, DM checks all configurations strictly. Unrecognized configuration triggers an error. This is to ensure that users always know exactly what the configuration is.

### Upgrade notes

Before starting the DM-master or DM-worker, ensure that the obsolete configuration information has been deleted and there are no redundant configuration items.

Otherwise, the starting might fail. In this situation, you can delete the deprecated configuration based on the failure information. These are two possible deprecated configurations:

- `meta-file` in `dm-worker.toml`
- `server-id` in `mysql-instances` in `task.yaml`
