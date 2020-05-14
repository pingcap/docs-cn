---
title: Upgrade TiFlash Nodes
summary: Learn how to upgrade TiFlash nodes.
category: reference
---

# Upgrade TiFlash Nodes

> **Note:**
>
> To upgrade TiFlash from the Pre-RC version to a later version, contact [PingCAP](mailto:info@pingcap.com) for more information and help.

Currently, you cannot upgrade TiFlash by running the `tiup cluster upgrade` command. Instead, take the following steps to upgrade TiFlash:

Before the upgrade, make sure that the cluster is started. To upgrade TiFlash nodes, take the following steps:

1. Refer to [Scale in a TiFlash node](/scale-tidb-using-tiup.md#sclale-in-a-tiflash-node), and scale in all the TiFlash nodes.

2. Run the upgrade command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster upgrade test v4.0.0-rc
    ```

3. Run the scale-out command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out test scale-out.yaml
    ```

4. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

5. Access the monitoring platform using your browser, and view the status of the cluster.
