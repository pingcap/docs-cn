---
title: Deploy a TiFlash Cluster
summary: Learn the requirements and methods of deploying a TiFlash cluster.
category: reference
---

# Deploy a TiFlash Cluster

> **Note:**
>
> If you want to get a first-hand experience on how to use the TiFlash RC version, contact [PingCAP](mailto:info@pingcap.com) for more information and assistance.

This document introduces the environment requirements for deploying a TiFlash cluster and the deployment methods in different scenarios.

## Recommended hardware configuration

This section provides hardware configuration recommendations based on different TiFlash deployment methods.

### TiFlash standalone deployment

* Minimum configuration: 32 VCore, 64 GB RAM, 1 SSD + n HDD
* Recommended configuration: 48 VCore, 128 GB RAM, 1 NVMe SSD + n SSD

There is no limit to the number of deployment machines (one at least). A single machine can use multiple disks, but deploying multiple instances on a single machine is not recommended.

It is recommended to use an SSD disk to buffer the real-time data being replicated and written to TiFlash. The performance of this disk need to be not lower than the hard disk used by TiKV. It is recommended that you use a better performance NVMe SSD and the SSD's capacity is not less than 10% of the total capacity. Otherwise, it might become the bottleneck of the amount of data that this node can handle.

For other hard disks, you can use multiple HDDs or regular SSDs. A better hard disk will surely bring better performance.

TiFlash supports multi-directory storage, so there is no need to use RAID.

### TiFlash and TiKV are deployed on the same node

See [Hardware recommendations for TiKV server](/how-to/deploy/hardware-recommendations.md#server-recommendations), and increase the memory capacity and the number of and CPU cores as needed.

It is **not** recommended to deploy TiFlash and TiKV on the same disk to prevent mutual interference.

Hard disk selection criteria are the same as [TiFlash standalone deployment](#tiflash-standalone-deployment). The total capacity of the hard disk is roughly: `the to-be-replicated data capacity of the entire TiKV cluster / the number of TiKV replicas / 2`.

For example, if the overall planned capacity of TiKV is three replicas, then the recommended capacity of TiFlash will be one sixth of the TiKV cluster. You can choose to replicate part of tables instead of all.

## TiDB version requirements

Currently, the testing of TiFlash is based on the related components of TiDB 3.1 (including TiDB, PD, TiKV, and TiFlash). For the download method of TiDB 3.1, refer to the following installation and deployment steps.

## Install and deploy TiFlash

This section describes how to install and deploy TiFlash in the following scenarios:

- [Fresh TiFlash deployment](#fresh-tiflash-deployment)
- [Add TiFlash component to an existing TiDB cluster](#add-tiflash-component-to-an-existing-tidb-cluster)

> **Note:**
>
> 1. Before starting the TiFlash process, you must ensure that PD's Placement Rules feature is enabled (For how to enable it, see the **second step** in the [Add TiFlash component to an existing TiDB cluster](#add-tiflash-component-to-an-existing-tidb-cluster) section).
> 2. When TiFlash is running, you must ensure that PD's Placement Rules feature remains enabled.

### Fresh TiFlash deployment

For fresh TiFlash deployment, it is recommended to deploy TiFlash by downloading an offline installation package. The steps are as follows:

1. Download the offline package of your desired version and unzip it.

    - If you are using TiDB 4.0 beta version, execute the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        curl -o tidb-ansible-tiflash-4.0-v3-20200331.tar.gz https://download.pingcap.org/tidb-ansible-tiflash-4.0-v3-20200331.tar.gz &&
        tar zxvf tidb-ansible-tiflash-4.0-v3-20200331.tar.gz
        ```

    - If you are using TiDB 3.1 rc version, execute the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        curl -o tidb-ansible-tiflash-3.1-rc.tar.gz https://download.pingcap.org/tidb-ansible-tiflash-3.1-rc.tar.gz &&
        tar zxvf tidb-ansible-tiflash-3.1-rc.tar.gz
        ```

2. Edit the `inventory.ini` configuration file. In addition to [configuring for TiDB cluster deployment](/how-to/deploy/orchestrated/ansible.md#step-9-edit-the-inventoryini-file-to-orchestrate-the-tidb-cluster), you also need to specify the IPs of your TiFlash servers under the `[tiflash_servers]` section (currently only IPs are supported; domain names are not supported).

    If you want to customize the deployment directory, configure the `data_dir` parameter. If you want multi-disk deployment, separate the deployment directories with commas (note that the parent directory of each `data_dir` directory needs to give the `tidb` user write permissions). For example:

    {{< copyable "" >}}

    ```ini
    [tiflash_servers]
    192.168.1.1 data_dir=/data1/tiflash/data,/data2/tiflash/data
    ```

3. Complete the [remaining steps](/how-to/deploy/orchestrated/ansible.md#step-10-edit-variables-in-the-inventoryini-file) of the TiDB Ansible deployment process.

4. To verify that TiFlash has been successfully deployed:
    
    1. Execute the `pd-ctl store http://your-pd-address` command in [pd-ctl](/reference/tools/pd-control.md) (`resources/bin` in the tidb-ansible directory includes the pd-ctl binary file).
    2. Observe that the status of the deployed TiFlash instance is "Up".

### Add TiFlash component to an existing TiDB cluster

1. First, confirm that your current TiDB version supports TiFlash, otherwise you need to upgrade your TiDB cluster to 3.1 rc or higher according to [TiDB Upgrade Guide](/how-to/upgrade/from-previous-version.md).

2. Execute the `config set enable-placement-rules true` command in [pd-ctl](/reference/tools/pd-control.md) (`resources/bin` in the tidb-ansible directory includes the pd-ctl binary file) to enable PD's Placement Rules feature.

3. Edit the `inventory.ini` configuration file. You need to specify the IPs of your TiFlash servers under the `[tiflash_servers]` section (currently only IPs are supported; domain names are not supported).

    If you want to customize the deployment directory, configure the `data_dir` parameter. If you want multi-disk deployment, separate the deployment directories with commas (note that the parent directory of each `data_dir` directory needs to give the `tidb` user write permissions). For example:

    {{< copyable "" >}}

    ```ini
    [tiflash_servers]
    192.168.1.1 data_dir=/data1/tiflash/data,/data2/tiflash/data
    ```

    > **Note:**
    >
    > Even if TiFlash and TiKV are deployed on the same machine, TiFlash uses a different default port from TiKV. TiFlash's default port is 9000. If you want to modify the port, add a new line `tcp_port=xxx` to the `inventory.ini` configuration file.

4. Execute the following ansible-playbook commands to deploy TiFlash:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook local_prepare.yml &&
    ansible-playbook -t tiflash deploy.yml &&
    ansible-playbook -t tiflash start.yml &&
    ansible-playbook rolling_update_monitor.yml
    ```

5. To verify that TiFlash has been successfully deployed:

    1. Execute the `pd-ctl store http://your-pd-address` command in [pd-ctl](/reference/tools/pd-control.md) (`resources/bin` in the tidb-ansible directory includes the pd-ctl binary file).
    2. Observe that the status of the deployed TiFlash instance is "Up".
