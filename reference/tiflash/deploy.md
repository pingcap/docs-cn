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

Currently, the testing of TiFlash is based on the related components of TiDB 4.0 (including TiDB, PD, TiKV, and TiFlash). For the download method of TiDB 4.0, refer to the following installation and deployment steps.

## Install and deploy TiFlash

This section describes how to install and deploy TiFlash in the following scenarios:

- [Fresh TiFlash deployment](#fresh-tiflash-deployment)
- [Add TiFlash component to an existing TiDB cluster](#add-tiflash-component-to-an-existing-tidb-cluster)

> **Note:**
>
> 1. Before starting the TiFlash process, you must ensure that PD's Placement Rules feature is enabled (For how to enable it, see the **second step** in the [Add TiFlash component to an existing TiDB cluster](#add-tiflash-component-to-an-existing-tidb-cluster) section).
> 2. When TiFlash is running, you must ensure that PD's Placement Rules feature remains enabled.

### Fresh TiFlash deployment

TiUP cluster is the deployment tool for TiDB 4.0 or later versions. It is recommended that you use TiUP cluster to install and deploy TiFlash. The steps are as follows:

1. [Install TiUP](/how-to/deploy/orchestrated/tiup.md#step-2-install-tiup-on-the-control-machine).

2. Install the TiUP cluster component.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

3. Write the topology configuration file and save it as `topology.yaml`.

    You can refer to [the topology configuration file template](https://github.com/pingcap-incubator/tiops/blob/master/topology.example.yaml).

    In addition to configuring the TiDB cluster, you also need to configure the IP of TiFlash servers in `tiflash_servers`. Currently the configuration only supports IP but not domain name.

    If you need to deploy TiFlash, set `replication.enable-placement-rules` in the `pd` section to `true`.

    {{< copyable "" >}}

    ```ini
    server_configs:
      pd:
        replication.enable-placement-rules: true
    pd_servers:
      - host: 172.19.0.101
      - host: 172.19.0.102
      - host: 172.19.0.103
    tidb_servers:
      - host: 172.19.0.101
    tikv_servers:
      - host: 172.19.0.101
      - host: 172.19.0.102
      - host: 172.19.0.103
    tiflash_servers:
      - host: 172.19.0.103
    ```

    If you want to customize the deployment directory, configure the `data_dir` parameter. If you want to deploy TiFlash on multiple disks, separate each directory with commas. For example:

    {{< copyable "" >}}

    ```ini
    tiflash_servers:
      - host: 172.19.0.103
        data_dir: /data1/tiflash/data,/data2/tiflash/data
    ```

4. Refer to the TiUP deployment process, and complete the following steps:

    * Deploy the TiDB cluster (`test` is the cluster name):
    
        {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster deploy test v4.0.0-rc topology.yaml  -i ~/.ssh/id_rsa
        ```
    
    * Start the TiDB cluster:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster start test
        ```

5. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ``` 

### Add TiFlash component to an existing TiDB cluster

1. First, confirm that your current TiDB version supports TiFlash; otherwise, you need to upgrade your TiDB cluster to 4.0 rc or higher versions.

2. Execute the `config set enable-placement-rules true` command in [pd-ctl](/reference/tools/pd-control.md) (`resources/bin` in the tidb-ansible directory includes the pd-ctl binary file) to enable PD's Placement Rules feature.

    Currently, pd-ctl is not connected to TiUP cluster, you need to [manually download pd-ctl](https://download.pingcap.org/tidb-v4.0.0-rc-linux-amd64.tar.gz).

3. Refer to [Scale out a TiFlash node](/how-to/scale/with-tiup.md#2-scale-out-a-tiflash-node) and deploy TiFlash.
