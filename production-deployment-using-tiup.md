---
title: Deploy a TiDB Cluster Using TiUP
summary: Learn how to easily deploy a TiDB cluster using TiUP.
aliases: ['/docs/dev/production-deployment-using-tiup/','/docs/dev/how-to/deploy/orchestrated/tiup/','/docs/dev/tiflash/deploy-tiflash/','/docs/dev/reference/tiflash/deploy/','/tidb/dev/deploy-tidb-from-dbdeployer/','/docs/dev/deploy-tidb-from-dbdeployer/','/docs/dev/how-to/get-started/deploy-tidb-from-dbdeployer/','/tidb/dev/deploy-tidb-from-homebrew/','/docs/dev/deploy-tidb-from-homebrew/','/docs/dev/how-to/get-started/deploy-tidb-from-homebrew/','/tidb/dev/production-offline-deployment-using-tiup','/docs/dev/production-offline-deployment-using-tiup/','/tidb/dev/deploy-tidb-from-binary','/tidb/dev/production-deployment-from-binary-tarball','/tidb/dev/test-deployment-from-binary-tarball','/tidb/dev/deploy-test-cluster-using-docker-compose','/tidb/dev/test-deployment-using-docker']
---

# Deploy a TiDB Cluster Using TiUP

[TiUP](https://github.com/pingcap/tiup) is a cluster operation and maintenance tool introduced in TiDB 4.0. TiUP provides [TiUP cluster](https://github.com/pingcap/tiup/tree/master/components/cluster), a cluster management component written in Golang. By using TiUP cluster, you can easily perform daily database operations, including deploying, starting, stopping, destroying, scaling, and upgrading a TiDB cluster, and manage TiDB cluster parameters.

TiUP supports deploying TiDB, TiFlash, TiDB Binlog, TiCDC, and the monitoring system. This document introduces how to deploy TiDB clusters of different topologies.

## Step 1: Prerequisites and precheck

Make sure that you have read the following documents:

- [Hardware and software requirements](/hardware-and-software-requirements.md)
- [Environment and system configuration check](/check-before-deployment.md)

## Step 2: Install TiUP on the control machine

You can install TiUP on the control machine in either of the two ways: online deployment and offline deployment.

### Method 1: Deploy TiUP online

Log in to the control machine using a regular user account (take the `tidb` user as an example). All the following TiUP installation and cluster management operations can be performed by the `tidb` user.

1. Install TiUP by executing the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Set the TiUP environment variables:

    Redeclare the global environment variables:

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

    Confirm whether TiUP is installed:

    {{< copyable "shell-regular" >}}

    ```shell
    which tiup
    ```

3. Install the TiUP cluster component:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

4. If TiUP is already installed, update the TiUP cluster component to the latest version:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update --self && tiup update cluster
    ```

    Expected output includes `“Update successfully!”`.

5. Verify the current version of your TiUP cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup --binary cluster
    ```

### Method 2: Deploy TiUP offline

Perform the following steps in this section to deploy a TiDB cluster offline using TiUP:

#### Step 1: Prepare the TiUP offline component package

To prepare the TiUP offline component package, manually pack an offline component package using `tiup mirror clone`.

1. Install the TiUP package manager online.

    1. Install the TiUP tool:

        {{< copyable "shell-regular" >}}

        ```shell
        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
        ```

    2. Redeclare the global environment variables:

        {{< copyable "shell-regular" >}}

        ```shell
        source .bash_profile
        ```

    3. Confirm whether TiUP is installed:

        {{< copyable "shell-regular" >}}

        ```shell
        which tiup
        ```

2. Pull the mirror using TiUP.

    1. Pull the needed components on a machine that has access to the Internet:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup mirror clone tidb-community-server-${version}-linux-amd64 ${version} --os=linux --arch=amd64
        ```

        The command above creates a directory named `tidb-community-server-${version}-linux-amd64` in the current directory, which contains the component package necessary for starting a cluster.

    2. Pack the component package by using the `tar` command and send the package to the control machine in the isolated environment:

        {{< copyable "shell-regular" >}}

        ```bash
        tar czvf tidb-community-server-${version}-linux-amd64.tar.gz tidb-community-server-${version}-linux-amd64
        ```

        `tidb-community-server-${version}-linux-amd64.tar.gz` is an independent offline environment package.

#### Step 2: Deploy the offline TiUP component

After sending the package to the control machine of the target cluster, install the TiUP component by running the following commands:

{{< copyable "shell-regular" >}}

```bash
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz && \
sh tidb-community-server-${version}-linux-amd64/local_install.sh && \
source /home/tidb/.bash_profile
```

The `local_install.sh` script automatically executes the `tiup mirror set tidb-community-server-${version}-linux-amd64` command to set the current mirror address to `tidb-community-server-${version}-linux-amd64`.

To switch the mirror to another directory, you can manually execute the `tiup mirror set <mirror-dir>` command. To switch the mirror to the online environment, you can execute the `tiup mirror set https://tiup-mirrors.pingcap.com` command.

## Step 3: Initialize cluster topology file

According to the intended cluster topology, you need to manually create and edit the cluster initialization configuration file.

To create the cluster initialization configuration file, you can create a YAML-formatted configuration file on the control machine using TiUP:

{{< copyable "shell-regular" >}}

```shell
tiup cluster template > topology.yaml
```

> **Note:**
>
> For the hybrid deployment scenarios, you can also execute `tiup cluster template --full > topology.yaml` to create the recommended topology template. For the geo-distributed deployment scenarios, you can execute `tiup cluster template --multi-dc > topology.yaml` to create the recommended topology template.

Execute `vi topology.yaml` to see the configuration file content:

```shell
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"
server_configs: {}
pd_servers:
  - host: 10.0.1.4
  - host: 10.0.1.5
  - host: 10.0.1.6
tidb_servers:
  - host: 10.0.1.7
  - host: 10.0.1.8
  - host: 10.0.1.9
tikv_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2
  - host: 10.0.1.3
monitoring_servers:
  - host: 10.0.1.4
grafana_servers:
  - host: 10.0.1.4
alertmanager_servers:
  - host: 10.0.1.4
```

The following examples cover six common scenarios. You need to modify the configuration file (named `topology.yaml`) according to the topology description and templates in the corresponding links. For other scenarios, edit the configuration template accordingly.

- [Minimal deployment topology](/minimal-deployment-topology.md)

    This is the basic cluster topology, including tidb-server, tikv-server, and pd-server. It is suitable for OLTP applications.

- [TiFlash deployment topology](/tiflash-deployment-topology.md)

    This is to deploy TiFlash along with the minimal cluster topology. TiFlash is a columnar storage engine, and gradually becomes a standard cluster topology. It is suitable for real-time HTAP applications.

- [TiCDC deployment topology](/ticdc-deployment-topology.md)

    This is to deploy TiCDC along with the minimal cluster topology. TiCDC is a tool for replicating the incremental data of TiDB, introduced in TiDB 4.0. It supports multiple downstream platforms, such as TiDB, MySQL, and MQ. Compared with TiDB Binlog, TiCDC has lower latency and native high availability. After the deployment, start TiCDC and [create the replication task using `cdc cli`](/ticdc/manage-ticdc.md).

- [TiDB Binlog deployment topology](/tidb-binlog-deployment-topology.md)

    This is to deploy TiDB Binlog along with the minimal cluster topology. TiDB Binlog is the widely used component for replicating incremental data. It provides near real-time backup and replication.

- [TiSpark deployment topology](/tispark-deployment-topology.md)

    This is to deploy TiSpark along with the minimal cluster topology. TiSpark is a component built for running Apache Spark on top of TiDB/TiKV to answer the OLAP queries. Currently, TiUP cluster's support for TiSpark is still **experimental**.

- [Hybrid deployment topology](/hybrid-deployment-topology.md)

    This is to deploy multiple instances on a single machine. You need to add extra configurations for the directory, port, resource ratio, and label.

- [Geo-distributed deployment topology](/geo-distributed-deployment-topology.md)

    This topology takes the typical architecture of three data centers in two cities as an example. It introduces the geo-distributed deployment architecture and the key configuration that requires attention.

> **Note:**
>
> - For parameters that should be globally effective, configure these parameters of corresponding components in the `server_configs` section of the configuration file.
> - For parameters that should be effective on a specific node, configure these parameters in the `config` of this node.
> - Use `.` to indicate the subcategory of the configuration, such as `log.slow-threshold`. For more formats, see [TiUP configuration template](https://github.com/pingcap/tiup/blob/master/embed/templates/examples/topology.example.yaml).
> - For more parameter description, see [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example), [TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/master/etc/config-template.toml), [PD `config.toml.example`](https://github.com/pingcap/pd/blob/master/conf/config.toml), and [TiFlash configuration](/tiflash/tiflash-configuration.md).

## Step 4: Execute the deployment command

> **Note:**
>
> You can use secret keys or interactive passwords for security authentication when you deploy TiDB using TiUP:
>
> - If you use secret keys, you can specify the path of the keys through `-i` or `--identity_file`;
> - If you use passwords, add the `-p` flag to enter the password interaction window;
> - If password-free login to the target machine has been configured, no authentication is required.
>
> In general, TiUP creates the user and group specified in the `topology.yaml` file on the target machine, with the following exceptions:
>
> - The user name configured in `topology.yaml` already exists on the target machine.
> - You have used the `--skip-create-user` option in the command line to explicitly skip the step of creating the user.

Before you execute the `deploy` command, use the `check` and `check --apply` commands to detect and automatically repair the potential risks in the cluster:

{{< copyable "shell-regular" >}}

```shell
tiup cluster check ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
tiup cluster check ./topology.yaml --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

Then execute the `deploy` command to deploy the TiDB cluster:

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy tidb-test v5.1.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

In the above command:

- The name of the deployed TiDB cluster is `tidb-test`.
- You can see the latest supported versions by running `tiup list tidb`. This document takes `v5.1.0` as an example.
- The initialization configuration file is `topology.yaml`.
- `--user root`: Log in to the target machine through the `root` key to complete the cluster deployment, or you can use other users with `ssh` and `sudo` privileges to complete the deployment.
- `[-i]` and `[-p]`: optional. If you have configured login to the target machine without password, these parameters are not required. If not, choose one of the two parameters. `[-i]` is the private key of the `root` user (or other users specified by `--user`) that has access to the target machine. `[-p]` is used to input the user password interactively.
- If you need to specify the user group name to be created on the target machine, see [this example](https://github.com/pingcap/tiup/blob/master/embed/templates/examples/topology.example.yaml#L7).

At the end of the output log, you will see ```Deployed cluster `tidb-test` successfully```. This indicates that the deployment is successful.

## Step 5: Check the clusters managed by TiUP

{{< copyable "shell-regular" >}}

```shell
tiup cluster list
```

TiUP supports managing multiple TiDB clusters. The command above outputs information of all the clusters currently managed by TiUP, including the name, deployment user, version, and secret key information:

```log
Starting /home/tidb/.tiup/components/cluster/v1.5.0/cluster list
Name              User  Version        Path                                                        PrivateKey
----              ----  -------        ----                                                        ----------
tidb-test         tidb  v5.1.0      /home/tidb/.tiup/storage/cluster/clusters/tidb-test         /home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa
```

## Step 6: Check the status of the deployed TiDB cluster

For example, execute the following command to check the status of the `tidb-test` cluster:

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

Expected output includes the instance ID, role, host, listening port, and status (because the cluster is not started yet, so the status is `Down`/`inactive`), and directory information.

## Step 7: Start the TiDB cluster

{{< copyable "shell-regular" >}}

```shell
tiup cluster start tidb-test
```

If the output log includes ```Started cluster `tidb-test` successfully```, the start is successful.

## Step 8: Verify the running status of the TiDB cluster

For the specific operations, see [Verify Cluster Status](/post-installation-check.md).

## What's next

If you have deployed [TiFlash](/tiflash/tiflash-overview.md) along with the TiDB cluster, see the following documents:

- [Use TiFlash](/tiflash/use-tiflash.md)
- [Maintain a TiFlash Cluster](/tiflash/maintain-tiflash.md)
- [TiFlash Alert Rules and Solutions](/tiflash/tiflash-alert-rules.md)
- [Troubleshoot TiFlash](/tiflash/troubleshoot-tiflash.md)

If you have deployed [TiCDC](/ticdc/ticdc-overview.md) along with the TiDB cluster, see the following documents:

- [Manage TiCDC Cluster and Replication Tasks](/ticdc/manage-ticdc.md)
- [Troubleshoot TiCDC](/ticdc/troubleshoot-ticdc.md)

> **Note:**
>
> By default, TiDB, TiUP and TiDB Dashboard share usage details with PingCAP to help understand how to improve the product. For details about what is shared and how to disable the sharing, see [Telemetry](/telemetry.md).
