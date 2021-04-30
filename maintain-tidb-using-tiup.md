---
title: TiUP Common Operations
summary: Learn the common operations to operate and maintain a TiDB cluster using TiUP.
aliases: ['/docs/dev/maintain-tidb-using-tiup/','/docs/dev/how-to/maintain/tiup-operations/']
---

# TiUP Common Operations

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

    For the parameter format, see the [TiUP parameter template](https://github.com/pingcap/tiup/blob/master/embed/templates/examples/topology.example.yaml).

    **Use `.` to represent the hierarchy of the configuration items**.

    For more information on the configuration parameters of components, refer to [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example), [TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/master/etc/config-template.toml), and [PD `config.toml.example`](https://github.com/tikv/pd/blob/master/conf/config.toml).

3. Rolling update the configuration and restart the corresponding components by running the `reload` command:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster reload ${cluster-name} [-N <nodes>] [-R <roles>]
    ```

### Example

If you want to set the transaction size limit parameter (`txn-total-size-limit` in the [performance](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) module) to `1G` in tidb-server, edit the configuration as follows:

```
server_configs:
  tidb:
    performance.txn-total-size-limit: 1073741824
```

Then, run the `tiup cluster reload ${cluster-name} -R tidb` command to rolling restart the TiDB component.

## Replace with a hotfix package

For normal upgrade, see [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md). But in some scenarios, such as debugging, you might need to replace the currently running component with a temporary package. To achieve this, use the `patch` command:

{{< copyable "shell-root" >}}

```bash
tiup cluster patch --help
```

```
Replace the remote package with a specified package and restart the service

Usage:
  cluster patch <cluster-name> <package-path> [flags]

Flags:
  -h, --help                   help for patch
  -N, --node strings           Specify the nodes
      --overwrite              Use this package in the future scale-out operations
  -R, --role strings           Specify the role
      --transfer-timeout int   Timeout in seconds when transferring PD and TiKV store leaders (default 300)

Global Flags:

      --native-ssh        Use the system's native SSH client
      --wait-timeout int  Timeout of waiting the operation
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

If a TiDB hotfix package is in `/tmp/tidb-hotfix.tar.gz` and you want to replace all the TiDB packages in the cluster, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -R tidb
```

You can also replace only one TiDB package in the cluster:

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## Rename the cluster

After deploying and starting the cluster, you can rename the cluster using the `tiup cluster rename` command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster rename ${cluster-name} ${new-name}
```

> **Note:**
>
> + The operation of renaming a cluster restarts the monitoring system (Prometheus and Grafana).
> + After a cluster is renamed, some panels with the old cluster name might remain on Grafana. You need to delete them manually.

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

## Clean up cluster data

The operation of cleaning up cluster data stops all the services and cleans up the data directory or/and log directory. The operation cannot be reverted, so proceed **with caution**.

- Clean up the data of all services in the cluster, but keep the logs:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster clean ${cluster-name} --data
    ```

- Clean up the logs of all services in the cluster, but keep the data:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster clean ${cluster-name} --log
    ```

- Clean up the data and logs of all services in the cluster:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster clean ${cluster-name} --all
    ```

- Clean up the logs and data of all services except Prometheus:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-role prometheus
    ```

- Clean up the logs and data of all services except the `172.16.13.11:9000` instance:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-node 172.16.13.11:9000
    ```

- Clean up the logs and data of all services except the `172.16.13.12` node:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-node 172.16.13.12
    ```

## Destroy the cluster

The destroy operation stops the services and clears the data directory and deployment directory. The operation cannot be reverted, so proceed **with caution**.

{{< copyable "shell-regular" >}}

```bash
tiup cluster destroy ${cluster-name}
```
