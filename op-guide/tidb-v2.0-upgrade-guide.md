---
title: TiDB 2.0 Upgrade Guide
summary: Learn how to upgrade from TiDB 1.0/TiDB 2.0 RC version to TiDB 2.0 GA version.
category: deployment
---

# TiDB 2.0 Upgrade Guide

This document describes how to upgrade from TiDB 1.0 or TiDB 2.0 RC version to TiDB 2.0 GA version.

## Step 1: Install Ansible and dependencies in the Control Machine

TiDB-Ansible release-2.0 depends on Ansible 2.4.2 or later, and is compatible with the latest Ansible 2.5. In addition, TiDB-Ansible release-2.0 depends on the Python module: `jinja2>=2.9.6` and `jmespath>=0.9.0`.

To make it easy to manage dependencies, use `pip` to install Ansible and its dependencies. For details, see [Install Ansible and its dependencies on the Control Machine](../op-guide/ansible-deployment.md#step-4-install-ansible-and-its-dependencies-on-the-control-machine). For offline environment, see [Install Ansible and its dependencies offline on the Control Machine](../op-guide/offline-ansible-deployment.md#step-3-install-ansible-and-its-dependencies-offline-on-the-control-machine).

After the installation is finished, you can view the version information using the following command:

```bash
$ ansible --version
ansible 2.5.2
$ pip show jinja2
Name: Jinja2
Version: 2.9.6
$ pip show jmespath
Name: jmespath
Version: 0.9.0
```

> **Note:**
>
> - You must install Ansible and its dependencies following the above procedures.
> - Make sure that the Jinja2 version is correct, otherwise an error occurs when you start Grafana.
> - Make sure that the jmespath version is correct, otherwise an error occurs when you perform a rolling update for TiKV.

## Step 2: Download TiDB-Ansible to the Control Machine

1. Log in to the Control Machine using the `tidb` user account and enter the `/home/tidb` directory.

2. Back up the `tidb-ansible` folders of TiDB 1.0 or TiDB 2.0 RC versions using the following command:

    ```
    $ mv tidb-ansible tidb-ansible-bak
    ```

3. Download the latest tidb-ansible `release-2.0` branch using the following command. The default folder name is `tidb-ansible`.

    ```
    $ git clone -b release-2.0 https://github.com/pingcap/tidb-ansible.git
    ```

## Step 3: Edit the `inventory.ini` file and the configuration file

Log in to the Control Machine using the `tidb` user account and enter the `/home/tidb/tidb-ansible` directory.

### Edit the `inventory.ini` file

Edit the `inventory.ini` file. For IP information, see the `/home/tidb/tidb-ansible-bak/inventory.ini` backup file.

Pay special attention to the following variables configuration. For variable meaning, see [Description of other variables](../op-guide/ansible-deployment.md#edit-other-variables-optional).

1. Make sure that `ansible_user` is the normal user. For unified privilege management, remote installation using the root user is no longer supported. The default configuration uses the `tidb` user as the SSH remote user and the program running user.

    ```
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

    You can refer to [How to configure SSH mutual trust and sudo rules on the Control Machine](../op-guide/ansible-deployment.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine) to automatically configure the mutual trust among hosts.

2. Keep the `process_supervision` variable consistent with that in the previous version. It is recommended to use `systemd` by default.

    ```
    # process supervision, [systemd, supervise]
    process_supervision = systemd
    ```

    If you need to modify this variable, see [How to modify the supervision method of a process from `supervise` to `systemd`](../op-guide/ansible-deployment.md#how-to-modify-the-supervision-method-of-a-process-from-supervise-to-systemd). Before you upgrade, first use the `/home/tidb/tidb-ansible-bak/` backup branch to modify the supervision method of a process.

### Edit the configuration file of TiDB cluster components

If you have previously customized the configuration file of TiDB cluster components, refer to the backup file to modify the corresponding configuration file in `/home/tidb/tidb-ansible/conf`.

In TiKV configuration, `end-point-concurrency` is changed to three parameters: `high-concurrency`, `normal-concurrency` and `low-concurrency`.

```
readpool:
  coprocessor:
    # Notice: if CPU_NUM > 8, default thread pool size for coprocessors
    # will be set to CPU_NUM * 0.8.
    # high-concurrency: 8
    # normal-concurrency: 8
    # low-concurrency: 8
```

For the cluster topology of multiple TiKV instances on a single machine, you need to modify the three parameters above. Recommended configuration: `number of instances * parameter value = number of CPU cores * 0.8`.

## Step 4: Download TiDB 2.0 binary to the Control Machine

Make sure that `tidb_version = v2.0.4` in the `tidb-ansible/inventory.ini` file, and then run the following command to download TiDB 2.0 binary to the Control Machine:

```
$ ansible-playbook local_prepare.yml
```

## Step 5: Perform a rolling update to TiDB cluster components

```
$ ansible-playbook rolling_update.yml
```

## Step 6: Perform a rolling update to TiDB monitoring component

To meet the users' demand on mixed deployment, the systemd service of the monitoring component is distinguished by port.

1. Check the `process_supervision` variable in the `inventory.ini` file.

    ```
    # process supervision, [systemd, supervise]
    process_supervision = systemd
    ```

    - If `process_supervision = systemd`, to make it compatible with versions earlier than `v2.0.0-rc.6`, you need to run `migrate_monitor.yml` Playbook.

        ```
        $ ansible-playbook migrate_monitor.yml
        ```

    - If `process_supervision = supervise`, you do not need to run the above command.

2. Perform a rolling update to the TiDB monitoring component using the following command:

    ```
    $ ansible-playbook rolling_update_monitor.yml
    ```