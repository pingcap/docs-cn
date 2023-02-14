---
title: Deploy and Maintain TiCDC
summary: Learn the hardware and software recommendations for deploying and running TiCDC, and how to deploy and maintain it.
---

# Deploy and Maintain TiCDC

This document describes how to deploy and maintain a TiCDC cluster, including the hardware and software recommendations. You can either deploy TiCDC along with a new TiDB cluster or add the TiCDC component to an existing TiDB cluster.

## Software and hardware recommendations

In production environments, the recommendations of software and hardware for TiCDC are as follows:

| Linux OS       | Version         |
| :----------------------- | :----------: |
| Red Hat Enterprise Linux | 7.3 or later versions   |
| CentOS                   | 7.3 or later versions   |

| CPU | Memory | Disk type | Network | Number of TiCDC cluster instances (minimum requirements for production environment) |
| :--- | :--- | :--- | :--- | :--- |
| 16 core+ | 64 GB+ | SSD | 10 Gigabit network card (2 preferred） | 2 |

For more information, see [Software and Hardware Recommendations](/hardware-and-software-requirements.md).

## Deploy a new TiDB cluster that includes TiCDC using TiUP

When you deploy a new TiDB cluster using TiUP, you can also deploy TiCDC at the same time. You only need to add the `cdc_servers` section in the configuration file that TiUP uses to start the TiDB cluster. The following is an example:

```shell
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
    data_dir: "/cdc-data"
  - host: 10.0.1.21
    gc-ttl: 86400
    data_dir: "/cdc-data"
```

More references:

- For detailed operations, see [Edit the initialization configuration file](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file).
- For detailed configurable fields, see [Configure `cdc_servers` using TiUP](/tiup/tiup-cluster-topology-reference.md#cdc_servers).
- For detailed steps to deploy a TiDB cluster, see [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md).

> **Note:**
>
> Before installing TiCDC, ensure that you have [manually configured the SSH mutual trust and sudo without password](/check-before-deployment.md#manually-configure-the-ssh-mutual-trust-and-sudo-without-password) between the TiUP control machine and the TiCDC host.

## Add or scale out TiCDC to an existing TiDB cluster using TiUP

The method of scaling out a TiCDC cluster is similar to that of deploying one. It is recommended to use TiUP to perform the scale-out.

1. Create a `scale-out.yaml` file to add the TiCDC node information. The following is an example:

    ```shell
    cdc_servers:
      - host: 10.1.1.1
        gc-ttl: 86400
        data_dir: /data/deploy/install/data/cdc-8300
      - host: 10.1.1.2
        gc-ttl: 86400
        data_dir: /data/deploy/install/data/cdc-8300
      - host: 10.0.1.4:8300
        gc-ttl: 86400
        data_dir: /data/deploy/install/data/cdc-8300
    ```

2. Run the scale-out command on the TiUP control machine:

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yaml
    ```

For more use cases, see [Scale out a TiCDC cluster](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster).

## Delete or scale in TiCDC from an existing TiDB cluster using TiUP

It is recommended that you use TiUP to scale in TiCDC nodes. The following is the scale-in command:

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
```

For more use cases, see [Scale in a TiCDC cluster](/scale-tidb-using-tiup.md#scale-in-a-ticdc-cluster).

## Upgrade TiCDC using TiUP

You can upgrade TiDB clusters using TiUP, during which TiCDC is upgraded as well. After you execute the upgrade command, TiUP automatically upgrades the TiCDC component. The following is an example:

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> <cluster-version> --transfer-timeout 600
```

> **Note:**
>
> In the preceding command, you need to replace `<cluster-name>` and `<cluster-version>` with the actual cluster name and cluster version. For example, the version can be v6.5.0.

### Upgrade cautions

When you upgrade a TiCDC cluster, you need to pay attention to the following:

- TiCDC v4.0.2 reconfigured `changefeed`. For details, see [Configuration file compatibility notes](/ticdc/ticdc-compatibility.md#cli-and-configuration-file-compatibility).
- If you encounter any problem during the upgrade, you can refer to [upgrade FAQs](/upgrade-tidb-using-tiup.md#faq) for solutions.
- Since v6.3.0, TiCDC supports rolling upgrade. During the upgrade, the replication latency is stable and does not fluctuate significantly. Rolling upgrade takes effect automatically if the following conditions are met:

- TiCDC is v6.3.0 or later.
    - TiUP is v1.11.0 or later.
    - At least two TiCDC instances are running in the cluster.

## Modify TiCDC cluster configurations using TiUP

This section describes how to use the [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) command to modify the configurations of TiCDC. In the following example, it is assumed that you need to change the default value of `gc-ttl` from `86400` to `172800` (48 hours).

1. Run the `tiup cluster edit-config` command. Replace `<cluster-name>` with the actual cluster name:

   ```shell
    tiup cluster edit-config <cluster-name>
    ```

2. In the vi editor, modify the `cdc` [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs):

    ```shell
    server_configs:
      tidb: {}
      tikv: {}
      pd: {}
      tiflash: {}
      tiflash-learner: {}
      pump: {}
      drainer: {}
      cdc:
        gc-ttl: 172800
    ```

    In the preceding command, `gc-ttl` is set to 48 hours.

3. Run the `tiup cluster reload -R cdc` command to reload the configuration.

## Stop and start TiCDC using TiUP

You can use TiUP to easily stop and start TiCDC nodes. The commands are as follows:

- Stop TiCDC: `tiup cluster stop -R cdc`
- Start TiCDC: `tiup cluster start -R cdc`
- Restart TiCDC: `tiup cluster restart -R cdc`

## Enable TLS for TiCDC

See [Enable TLS Between TiDB Components](/enable-tls-between-components.md).

## View TiCDC status using the command-line tool

Run the following command to view the TiCDC cluster status. Note that you need to replace `v<CLUSTER_VERSION>` with the TiCDC cluster version:

```shell
tiup ctl:v<CLUSTER_VERSION> cdc capture list --server=http://10.0.10.25:8300
```

```shell
[
  {
    "id": "806e3a1b-0e31-477f-9dd6-f3f2c570abdd",
    "is-owner": true,
    "address": "127.0.0.1:8300",
    "cluster-id": "default"
  },
  {
    "id": "ea2a4203-56fe-43a6-b442-7b295f458ebc",
    "is-owner": false,
    "address": "127.0.0.1:8301",
    "cluster-id": "default"
  }
]
```

- `id`: Indicates the ID of the service process.
- `is-owner`: Indicates whether the service process is the owner node.
- `address`: Indicates the address via which the service process provides interface to the outside.
- `cluster-id`: Indicates the ID of the TiCDC cluster. The default value is `default`.
