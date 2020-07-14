---
title: Upgrade TiDB Using TiDB Ansible
summary: Learn how to upgrade TiDB using TiDB Ansible.
aliases: ['/docs/dev/upgrade-tidb-using-ansible/','/docs/dev/how-to/upgrade/from-previous-version/','/docs/dev/how-to/upgrade/rolling-updates-with-ansible/']
---

# Upgrade TiDB Using TiDB Ansible

This document is targeted for users who want to upgrade from TiDB 2.0, 2.1, 3.0, or 3.1 versions to the latest development version (`latest`), or from an earlier development version to the latest development version. The latest development version is compatible with [TiDB Binlog of the cluster version](/tidb-binlog/tidb-binlog-overview.md).

> **Warning:**
>
> The latest development version of TiDB is not a stable version. Do not use it in the production environment.

## Upgrade caveat

- Rolling back to 2.1.x or earlier versions after upgrading is not supported.
- Before upgrading to `latest` from 2.0.6 or earlier versions, check if there are any running DDL operations, especially time-consuming ones like `Add Index`. If there are any, wait for the DDL operations to finish before you upgrade.
- Parallel DDL is supported in TiDB 2.1 and later versions. Therefore, for clusters with a TiDB version earlier than 2.0.1, rolling update to `latest` is not supported. To upgrade, you can choose either of the following two options:

    - Stop the cluster and upgrade to `latest` directly.
    - Roll update to 2.0.1 or later 2.0.x versions, and then roll update to the `latest` version.

> **Note:**
>
> Do not execute any DDL statements during the upgrading process, otherwise the undefined behavior error might occur.

## Step 1: Install Ansible and dependencies on the control machine

> **Note:**
>
> If you have installed Ansible and its dependencies, you can skip this step.

The latest development version of TiDB Ansible depends on Ansible 2.4.2 ~ 2.7.11 (`2.4.2 ≦ ansible ≦ 2.7.11`, Ansible 2.7.11 recommended) and the Python modules of `jinja2 ≧ 2.9.6` and `jmespath ≧ 0.9.0`.

To make it easy to manage dependencies, use `pip` to install Ansible and its dependencies. For details, see [Install Ansible and its dependencies on the control machine](/online-deployment-using-ansible.md#step-4-install-tidb-ansible-and-its-dependencies-on-the-control-machine). For offline environment, see [Install Ansible and its dependencies offline on the control machine](/offline-deployment-using-ansible.md#step-3-install-tidb-ansible-and-its-dependencies-offline-on-the-control-machine).

After the installation is finished, you can view the version information using the following command:

{{< copyable "shell-regular" >}}

```bash
ansible --version
```

```
ansible 2.7.11
```

{{< copyable "shell-regular" >}}

```bash
pip show jinja2
```

```
Name: Jinja2
Version: 2.10
```

{{< copyable "shell-regular" >}}

```bash
pip show jmespath
```

```
Name: jmespath
Version: 0.9.0
```

> **Note:**
>
> - You must install Ansible and its dependencies following the above procedures.
> - Make sure that the Jinja2 version is correct, otherwise an error occurs when you start Grafana.
> - Make sure that the jmespath version is correct, otherwise an error occurs when you perform a rolling update to TiKV.

## Step 2: Download TiDB Ansible to the control machine

1. Log in to the control machine using the `tidb` user account and enter the `/home/tidb` directory.

2. Back up the `tidb-ansible` folders of TiDB 2.0, 2.1, 3.0, or an earlier `latest` version using the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    mv tidb-ansible tidb-ansible-bak
    ```

3. Download the tidb-ansible with the tag corresponding to the `latest` version of TiDB. For more details, See [Download TiDB-Ansible to the control machine](/online-deployment-using-ansible.md#step-3-download-tidb-ansible-to-the-control-machine). The default folder name is `tidb-ansible`.

    {{< copyable "shell-regular" >}}

    ```bash
    git clone https://github.com/pingcap/tidb-ansible.git
    ```

## Step 3: Edit the `inventory.ini` file and the configuration file

Log in to the control machine using the `tidb` user account and enter the `/home/tidb/tidb-ansible` directory.

### Edit the `inventory.ini` file

Edit the `inventory.ini` file. For IP information, see the `/home/tidb/tidb-ansible-bak/inventory.ini` backup file.

> **Note:**
>
> Pay special attention to the following variables configuration. For variable meaning, see [Description of other variables](/online-deployment-using-ansible.md#edit-other-variables-optional).

1. Make sure that `ansible_user` is the normal user. For unified privilege management, remote installation using the root user is no longer supported. The default configuration uses the `tidb` user as the SSH remote user and the program running user.

    ```
    ## Connection
    # ssh via normal user
    ansible_user = tidb
    ```

    You can refer to [How to configure SSH mutual trust and sudo rules on the control machine](/online-deployment-using-ansible.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine) to automatically configure the mutual trust among hosts.

2. Keep the `process_supervision` variable consistent with that in the previous version. It is recommended to use `systemd` by default.

    ```
    # process supervision, [systemd, supervise]
    process_supervision = systemd
    ```

    If you need to modify this variable, see [How to modify the supervision method of a process from `supervise` to `systemd`](/online-deployment-using-ansible.md#how-to-modify-the-supervision-method-of-a-process-from-supervise-to-systemd). Before you upgrade, first use the `/home/tidb/tidb-ansible-bak/` backup branch to modify the supervision method of a process.

3. Add the `cpu_architecture` parameter according to the CPU architecture. The default value is `amd64`.

### Edit the configuration file of TiDB cluster components

If you have previously customized the configuration file of TiDB cluster components, refer to the backup file to modify the corresponding configuration file in the `/home/tidb/tidb-ansible/conf` directory.

**Note the following parameter changes:**

- In the TiKV configuration, `end-point-concurrency` is changed to three parameters: `high-concurrency`, `normal-concurrency` and `low-concurrency`.

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

    Recommended configuration: `capacity` = MEM_TOTAL \* 0.5 / the number of TiKV instances. If the `capacity` parameter is configured reasonably in the current version, it needs no modification.

- In the TiKV configuration, you need to configure the `tikv_status_port` port for the multiple instances on a single machine scenario. If the current version has the above configuration, it needs no modification.
- Before you configure `tikv_status_port`, check whether a port conflict exists.

    ```
    [tikv_servers]
    TiKV1-1 ansible_host=172.16.10.4 deploy_dir=/data1/deploy tikv_port=20171 tikv_status_port=20181 labels="host=tikv1"
    TiKV1-2 ansible_host=172.16.10.4 deploy_dir=/data2/deploy tikv_port=20172 tikv_status_port=20182 labels="host=tikv1"
    TiKV2-1 ansible_host=172.16.10.5 deploy_dir=/data1/deploy tikv_port=20171 tikv_status_port=20181 labels="host=tikv2"
    TiKV2-2 ansible_host=172.16.10.5 deploy_dir=/data2/deploy tikv_port=20172 tikv_status_port=20182 labels="host=tikv2"
    TiKV3-1 ansible_host=172.16.10.6 deploy_dir=/data1/deploy tikv_port=20171 tikv_status_port=20181 labels="host=tikv3"
    TiKV3-2 ansible_host=172.16.10.6 deploy_dir=/data2/deploy tikv_port=20172 tikv_status_port=20182 labels="host=tikv3"
    ```

## Step 4: Download TiDB latest binary to the control machine

Make sure that `tidb_version = latest` in the `tidb-ansible/inventory.ini` file, and then run the following command to download TiDB latest binary to the control machine:

{{< copyable "shell-regular" >}}

```bash
ansible-playbook local_prepare.yml
```

## Step 5: Perform a rolling update to TiDB cluster components

- If the `process_supervision` variable uses the default `systemd` parameter, perform a rolling update to the TiDB cluster using the following command corresponding to your current TiDB cluster version.

    - When the TiDB cluster version < 3.0.0, use `excessive_rolling_update.yml`.

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook excessive_rolling_update.yml
        ```

    - When the TiDB cluster version ≧ 3.0.0, use `rolling_update.yml` for both rolling updates and daily rolling restarts.

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook rolling_update.yml
        ```

- If the `process_supervision` variable uses the `supervise` parameter, perform a rolling update to the TiDB cluster using `rolling_update.yml`, no matter what version the current TiDB cluster is.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml
    ```

## Step 6: Perform a rolling update to TiDB monitoring components

{{< copyable "shell-regular" >}}

```bash
ansible-playbook rolling_update_monitor.yml
```

> **Note:**
>
> By default, TiDB (starting from v4.0.2) periodically shares usage details with PingCAP to help understand how to improve the product. For details about what is shared and how to disable the sharing, see [Telemetry](/telemetry.md).
