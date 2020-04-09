---
title: Scale the TiFlash Cluster
summary: Learn how to scale in and out nodes in the TiFlash cluster.
category: reference
---

# Scale the TiFlash Cluster

This document describes how to scale in and out nodes in the TiFlash cluster.

## Scale out a TiFlash node

If you need to add a TiFlash node to the `172.19.0.104` host, take the following steps:

1. Create the `scale-out.yaml` file to add the TiFlash node information:

    Currently, you can only add IP but not domain name.

    {{< copyable "" >}}

    ```ini
    tiflash_servers:
      - host: 172.19.0.104
    ```

2. Run the scale-out command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out test scale-out.yaml
    ```

3. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

4. Access the monitoring platform using your browser, and view the status of the cluster and the new node.

## Scale in a TiFlash node

If you want to stop the TiFlash service on the `172.19.0.104` node, take the following steps:

> **Note:**
>
> The offline process described in this section does not delete the data on the offline node. If you need to take the node online again, delete the data manually.

1. Take down the node to be scaled in. See [Take a TiFlash node down](/reference/tiflash/maintain.md#take-a-tiflash-node-down) for details.

2. Check whether the node has been offline successfully using Grafana or pd-ctl (the offline process takes some time).

3. After the `store` corresponding to TiFlash disappears, or the `state_name` becomes `Tombstone`, execute the following command to shutdown the TiFlash process:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-in test --node 172.19.0.104:9000
    ```

4. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

5. Access the monitoring platform using your browser, and view the status of the cluster.
