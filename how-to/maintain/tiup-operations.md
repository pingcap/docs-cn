---
title: Common TiUP Operations
summary: Learn the common operations to operate and maintain a TiDB cluster using TiUP.
category: how-to
---

# Common TiUP Operations

This document describes the following common operations when you operate and maintain a TiDB cluster using TiUP.

- View the cluster list
- Start the cluster
- View the cluster status
- Modify the configuration
- Stop the cluster
- Destroy the cluster

## View the cluster list

You can manage multiple TiDB clusters using the TiUP cluster component. When a TiDB cluster is deployed, the cluster appears in the TiUP cluster list.

To view the list, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster list
```

## Start the cluster

The components in the TiDB cluster are started in the following order (The monitoring component is also started):

**PD -> TiKV -> Pump -> TiDB -> TiFlash -> Drainer**

To start the cluster, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster start ${cluster-name}
```

> **Note:**
>
> Replace `${cluster-name}` with the name of your cluster. If you forget the cluster name, check it by running `tiup cluster list`.

You can start only some of the components by adding the `-R` or `-N` parameters in the command. For example:

- This command starts only the PD component:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster start ${cluster-name} -R pd
    ```

- This command starts only the PD components on the `1.2.3.4` and `1.2.3.5` hosts:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster start ${cluster-name} -N 1.2.3.4:2379,1.2.3.5:2379
    ```

> **Note:**
>
> If you start the specified component by using the `-R` or `-N` parameters, make sure the starting order is correct. For example, start the PD component before the TiKV component. Otherwise, the start might fail.

## View the cluster status

After starting the cluster, check the status of each component to ensure that they work normally. TiUP provides the `display` command, so you do not have to log in to every machine to view the component status.

{{< copyable "shell-regular" >}}

```bash
tiup cluster display ${cluster-name}
```

## Modify the configuration

When the cluster is in operation, if you need to modify the parameters of a component, run the `edit-config` command. The detailed steps are as follows:

1. Open the configuration file of the cluster in the editing mode:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster edit-config ${cluster-name}
    ```

2. Configure the parameters:

    - If the configuration is globally effective for a component, edit `server_configs`:
    
        ```
        server_configs:
        tidb:
            log.slow-threshold: 300
        ```

    - If the configuration takes effect on a specific node, edit the configuration in `config` of the node:

        ```
        tidb_servers:
        - host: 10.0.1.11
            port: 4000
            config:
                log.slow-threshold: 300
        ```
    
    For the parameter format, see the [TiUP parameter template](https://github.com/pingcap-incubator/tiup-cluster/blob/master/topology.example.yaml).

    **Use `.` to represent the hierarchy of the configuration items**.

    For more information on the configuration parameters of components, refer to [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/v4.0.0-rc/config/config.toml.example), [TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/v4.0.0-rc/etc/config-template.toml), and [PD `config.toml.example`](https://github.com/pingcap/pd/blob/v4.0.0-rc/conf/config.toml).

3. Rolling update the configuration and restart the corresponding components by running the `reload` command:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster reload ${cluster-name} [-N <nodes>] [-R <roles>]
    ```

### Example

If you want to set the transaction size limit parameter (`txn-total-size-limit` in the [performance](https://github.com/pingcap/tidb/blob/v4.0.0-rc/config/config.toml.example) module) to `1G` in tidb-server, edit the configuration as follows:

```
server_configs:
  tidb:
    performance.txn-total-size-limit: 1073741824
```

Then run the `tiup cluster reload ${cluster-name} -N tidb` command to rolling restart the TiDB component.

## Stop the cluster

The components in the TiDB cluster are stopped in the following order (The monitoring component is also stopped):

**Drainer -> TiFlash -> TiDB -> Pump -> TiKV -> PD**

To stop the cluster, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster stop ${cluster-name}
```

Similar to the `start` command, the `stop` command supports stopping some of the components by adding the `-R` or `-N` parameters. For example:

- This command stops only the TiDB component:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster stop ${cluster-name} -R tidb
    ```

- This command stops only the TiDB components on the `1.2.3.4` and `1.2.3.5` hosts:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster stop ${cluster-name} -N 1.2.3.4:4000,1.2.3.5:4000
    ```

## Destroy the cluster

The destroy operation stops the services and clears the data directory and deployment directory. The operation cannot be reverted, so proceed **with caution**.

{{< copyable "shell-regular" >}}

```bash
tiup cluster destroy ${cluster-name}
```
