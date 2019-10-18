---
title: TiDB 3.0 Upgrade Guide
summary: Learn how to upgrade to TiDB 3.0 versions.
category: how-to
---

# TiDB 3.0 Upgrade Guide

This document is targeted for users who want to upgrade from TiDB 2.0 (above V2.0.1) or TiDB 2.1 RC to TiDB 3.0. TiDB 3.0 is compatible with [TiDB Binlog of Kafka Version](/dev/reference/tools/tidb-binlog/tidb-binlog-kafka.md) and [TiDB Binlog of Cluster Version](/dev/reference/tidb-binlog-overview.md).

## Upgrade caveat

- Rolling back to 2.1.x or earlier versions after upgrading is not supported
- Before upgrading to 3.0 from 2.0.6 or earlier versions, verify if there are any running DDL operations, especially time-consuming ones like `Add Index`. If there are any, wait for the DDL to finish before you upgrade.
- Parallel DDL is enabled in TiDB 2.1, so the clusters with TiDB version earlier than 2.0.1 cannot upgrade to 2.1 using rolling update. You can choose either of the following two options:

    - Stop the cluster and upgrade to 2.1 directly
    - Roll update to 2.0.1 or later 2.0.x versions, and then roll update to the 2.1 version

> **Note:**
>
> Do not execute any DDL statements during the upgrading process, otherwise the undefined behavior error might occur.

## Step 1: Install Ansible and dependencies on the Control Machine

> **Note:**
>
> If you have installed Ansible and its dependencies, you can skip this step.

TiDB Ansible release-3.0 depends on Ansible 2.4.2 and the later versions (`ansible>=2.4.2`, Ansible 2.7.11 recommended) and the Python module `jinja2>=2.9.6` and `jmespath>=0.9.0`.

To make it easy to manage dependencies, use `pip` to install Ansible and its dependencies. For details, see [Install Ansible and its dependencies on the Control Machine](/dev/how-to/deploy/orchestrated/ansible.md#step-4-install-ansible-and-its-dependencies-on-the-control-machine). For offline environment, see [Install Ansible and its dependencies offline on the Control Machine](/dev/how-to/deploy/orchestrated/offline-ansible.md#step-3-install-ansible-and-its-dependencies-offline-on-the-control-machine).

After the installation is finished, you can view the version information using the following command:

{{< copyable "shell-regular" >}}

```bash
$ ansible --version
```

```
ansible 2.7.11
```

{{< copyable "shell-regular" >}}

```bash
$ pip show jinja2
```

```
Name: Jinja2
Version: 2.10
```

{{< copyable "shell-regular" >}}

```bash
$ pip show jmespath
```

```
Name: jmespath
Version: 0.9.0
```

> **Note:**
>
> - You must install Ansible and its dependencies following the above procedures.
> - Make sure that the Jinja2 version is correct, otherwise an error occurs when you start Grafana.
> - Make sure that the jmespath version is correct, otherwise an error occurs when you perform a rolling update for TiKV.

## Step 2: Download TiDB Ansible to the Control Machine

1. Log in to the Control Machine using the `tidb` user account and enter the `/home/tidb` directory.

2. Back up the `tidb-ansible` folders of TiDB 2.0 or TiDB 2.1 versions using the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    $ mv tidb-ansible tidb-ansible-bak
    ```

3. Download the tidb-ansible with the tag corresponding to TiDB 3.0. For more details, See [Download TiDB-Ansible to the Control Machine](/dev/how-to/deploy/orchestrated/ansible.md#step-3-download-tidb-ansible-to-the-control-machine). The default folder name is `tidb-ansible`.

    {{< copyable "shell-regular" >}}

    ```bash
    $ git clone -b $tag https://github.com/pingcap/tidb-ansible.git
    ```

## Step 3: Edit the `inventory.ini` file and the configuration file

Log in to the Control Machine using the `tidb` user account and enter the `/home/tidb/tidb-ansible` directory.

### Edit the `inventory.ini` file

Edit the `inventory.ini` file. For IP information, see the `/home/tidb/tidb-ansible-bak/inventory.ini` backup file.

> **Note:**
>
> Pay special attention to the following variables configuration. For variable meaning, see [Description of other variables](/dev/how-to/deploy/orchestrated/ansible.md#edit-other-variables-optional).

1. Make sure that `ansible_user` is the normal user. For unified privilege management, remote installation using the root user is no longer supported. The default configuration uses the `tidb` user as the SSH remote user and the program running user.

    ```
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

    You can refer to [How to configure SSH mutual trust and sudo rules on the Control Machine](/dev/how-to/deploy/orchestrated/ansible.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine) to automatically configure the mutual trust among hosts.

2. Keep the `process_supervision` variable consistent with that in the previous version. It is recommended to use `systemd` by default.

    ```
    # process supervision, [systemd, supervise]
    process_supervision = systemd
    ```

    If you need to modify this variable, see [How to modify the supervision method of a process from `supervise` to `systemd`](/dev/how-to/deploy/orchestrated/ansible.md#how-to-modify-the-supervision-method-of-a-process-from-supervise-to-systemd). Before you upgrade, first use the `/home/tidb/tidb-ansible-bak/` backup branch to modify the supervision method of a process.

### Edit the configuration file of TiDB cluster components

If you have previously customized the configuration file of TiDB cluster components, refer to the backup file to modify the corresponding configuration file in `/home/tidb/tidb-ansible/conf`.

**Note the following parameter changes:**

- In TiKV configuration, `end-point-concurrency` is changed to three parameters: `high-concurrency`, `normal-concurrency` and `low-concurrency`.

    ```yaml
    readpool:
      coprocessor:
        # Notice: if CPU_NUM > 8, default thread pool size for coprocessors
        # will be set to CPU_NUM * 0.8.
        # high-concurrency: 8
        # normal-concurrency: 8
        # low-concurrency: 8
    ```

    > **Note:**
    >
    > For the cluster topology of multiple TiKV instances (processes) on a single machine, you need to modify the three parameters above.

    Recommended configuration: the number of TiKV instances \* the parameter value = the number of CPU cores \* 0.8.

- In the TiKV configuration, the `block-cache-size` parameter of different CFs is changed to `block-cache`.

    ```
    storage:
      block-cache:
        capacity: "1GB"
    ```

    > **Note:**
    >
    > For the cluster topology of multiple TiKV instances (processes) on a single machine, you need to modify the `capacity` parameter.

    Recommended configuration: `capacity` = MEM_TOTAL \* 0.5 / the number of TiKV instances.

## Step 4: Download TiDB 3.0 binary to the Control Machine

Make sure that `tidb_version = v3.0.0` in the `tidb-ansible/inventory.ini` file, and then run the following command to download TiDB 2.1 binary to the Control Machine:

{{< copyable "shell-regular" >}}

```bash
$ ansible-playbook local_prepare.yml
```

## Step 5: Perform a rolling update to TiDB cluster components

- If the `process_supervision` variable uses the default `systemd` parameter, perform a rolling update to the TiDB cluster using `excessive_rolling_update.yml`.

    {{< copyable "shell-regular" >}}

    ```bash
    $ ansible-playbook excessive_rolling_update.yml
    ```

- If the `process_supervision` variable uses the `supervise` parameter, perform a rolling update to the TiDB cluster using `rolling_update.yml`.

    {{< copyable "shell-regular" >}}

    ```bash
    $ ansible-playbook rolling_update.yml
    ```

> **Note:**
>
> To optimize operation and maintenance management over TiDB cluster components, the `PD service` name in the `systemd` mode is adjusted in TiDB 3.0. After upgrading the version to TiDB 3.0, you can use `rolling_update.yml` for both rolling updates and daily rolling restarts. Do not use `excessive_rolling_update.yml` any longer.

## Step 6: Perform a rolling update to TiDB monitoring components

{{< copyable "shell-regular" >}}

```bash
$ ansible-playbook rolling_update_monitor.yml
```
