---
title: Scale the TiFlash Cluster
summary: Learn how to scale in and out nodes in the TiFlash cluster.
category: reference
---

# Scale the TiFlash Cluster

This document describes how to scale in and out nodes in the TiFlash cluster.

## Scale out a TiFlash node

The following example shows how to scale out a TiFlash node if you deploy TiFlash on the `192.168.1.1` node.

1. Edit the `inventory.ini` file to add the TiFlash node information:

    Currently, you can only add IP but not domain name.

    {{< copyable "" >}}

    ```ini
    [tiflash_servers]
    192.168.1.1
    ```

2. Edit the `hosts.ini` file to add the node information:

    {{< copyable "" >}}

    ```ini
    [servers]
    192.168.1.1
    [all:vars]
    username = tidb
    ntp_server = pool.ntp.org
    ```

3. Initialize the new node:

    - Configure the SSH mutual trust and sudo rules on the Control Machine:

        {{< copyable "shell-regular" >}}

        ```shell
        ansible-playbook -i hosts.ini create_users.yml -l 192.168.1.1 -u root -k
        ```

    - Install the NTP service on the target machine:

        {{< copyable "shell-regular" >}}

        ```shell
        ansible-playbook -i hosts.ini deploy_ntp.yml -u tidb -b
        ```

    - Initialize the node on the target machine:

        {{< copyable "shell-regular" >}}

        ```shell
        ansible-playbook bootstrap.yml -l 192.168.1.1
        ```
    
4. Deploy the new node:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook deploy.yml -l 192.168.1.1
    ```

5. Start the new node:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook start.yml -l 192.168.1.1
    ```

6. Update the configuration of Prometheus and restart it:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

7. Access the monitoring platform using your browser, and view the status of the cluster and the new node.

## Scale in a TiFlash node

The following example shows how to scale in a TiFlash node if you stop the TiFlash service on the `192.168.1.1` node.

> **Note:**
>
> The offline process described in this section does not delete the data on the offline node. If you need to take the node online again, delete the data manually.

1. Take down the node to be scaled in. See [Take a TiFlash node down](/reference/tiflash/maintain.md#take-a-tiflash-node-down) for details.

2. Check whether the node has been offline successfully using Grafana or pd-ctl (the offline process takes some time).

3. After the `store` corresponding to TiFlash disappears, or the `state_name` becomes `Tombstone`, execute the following command to shutdown the TiFlash process:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook stop.yml -l 192.168.1.1
    ```

    If the node still has other services and you want to stop TiFlash only, use the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook stop.yml -t tiflash -l 192.168.1.1
    ```

4. Edit the `inventory.ini` and `hosts.ini` files to remove the node information.

5. Update the configuration of Prometheus and restart it:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

6. Access the monitoring platform using your browser, and view the status of the cluster.
