---
title: Upgrade TiFlash Nodes
summary: Learn how to upgrade TiFlash nodes.
category: reference
---

# Upgrade TiFlash Nodes

> **Note:**
>
> To upgrade TiFlash from the Pre-RC version to a later version, contact [PingCAP](mailto:info@pingcap.com) for more information and help.

Before the upgrade, make sure that the cluster is started. To upgrade TiFlash nodes, take the following steps:

1. Run the upgrade command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster upgrade test v4.0.0-rc
    ```

2. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

3. Access the monitoring platform using your browser, and view the status of the cluster.
