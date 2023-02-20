---
title: Deploy a TiDB Cluster Using TiUP
summary: Learn how to easily deploy a TiDB cluster using TiUP.
aliases: ['/docs/dev/production-deployment-using-tiup/','/docs/dev/how-to/deploy/orchestrated/tiup/','/docs/dev/tiflash/deploy-tiflash/','/docs/dev/reference/tiflash/deploy/','/tidb/dev/deploy-tidb-from-dbdeployer/','/docs/dev/deploy-tidb-from-dbdeployer/','/docs/dev/how-to/get-started/deploy-tidb-from-dbdeployer/','/tidb/dev/deploy-tidb-from-homebrew/','/docs/dev/deploy-tidb-from-homebrew/','/docs/dev/how-to/get-started/deploy-tidb-from-homebrew/','/tidb/dev/production-offline-deployment-using-tiup','/docs/dev/production-offline-deployment-using-tiup/','/tidb/dev/deploy-tidb-from-binary','/tidb/dev/production-deployment-from-binary-tarball','/tidb/dev/test-deployment-from-binary-tarball','/tidb/dev/deploy-test-cluster-using-docker-compose','/tidb/dev/test-deployment-using-docker']
---

# Deploy a TiDB Cluster Using TiUP

[TiUP](https://github.com/pingcap/tiup) is a cluster operation and maintenance tool introduced in TiDB 4.0. TiUP provides [TiUP cluster](https://github.com/pingcap/tiup/tree/master/components/cluster), a cluster management component written in Golang. By using TiUP cluster, you can easily perform daily database operations, including deploying, starting, stopping, destroying, scaling, and upgrading a TiDB cluster, and manage TiDB cluster parameters.

TiUP supports deploying TiDB, TiFlash, TiDB Binlog, TiCDC, and the monitoring system. This document introduces how to deploy TiDB clusters of different topologies.

## Step 1. Prerequisites and precheck

Make sure that you have read the following documents:

- [Hardware and software requirements](/hardware-and-software-requirements.md)
- [Environment and system configuration check](/check-before-deployment.md)

## Step 2. Deploy TiUP on the control machine

You can deploy TiUP on the control machine in either of the two ways: online deployment and offline deployment.

### Deploy TiUP online

Log in to the control machine using a regular user account (take the `tidb` user as an example). Subsequent TiUP installation and cluster management can be performed by the `tidb` user.

1. Install TiUP by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Set TiUP environment variables:

    1. Redeclare the global environment variables:

        {{< copyable "shell-regular" >}}

        ```shell
        source .bash_profile
        ```

    2. Confirm whether TiUP is installed:

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

    If `Update successfully!` is displayed, the TiUP cluster is updated successfully.

5. Verify the current version of your TiUP cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup --binary cluster
    ```

### Deploy TiUP offline

Perform the following steps in this section to deploy a TiDB cluster offline using TiUP:

#### Prepare the TiUP offline component package

Method 1: On the [official download page](https://www.pingcap.com/download/), select the offline mirror package (TiUP offline package included) of the target TiDB version. Note that you need to download the server package and toolkit package at the same time.

Method 2: Manually pack an offline component package using `tiup mirror clone`. The detailed steps are as follows:

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

3. Customize the offline mirror, or adjust the contents of an existing offline mirror.

    If you want to adjust an existing offline mirror (such as adding a new version of a component), take the following steps:

    1. When pulling an offline mirror, you can get an incomplete offline mirror by specifying specific information via parameters, such as the component and version information. For example, you can pull an offline mirror that includes only the offline mirror of TiUP v1.11.3 and TiUP Cluster v1.11.3 by running the following command:

        {{< copyable "shell-regular" >}}

        ```bash
        tiup mirror clone tiup-custom-mirror-v1.11.3 --tiup v1.11.3 --cluster v1.11.3
        ```

        If you only need the components for a particular platform, you can specify them using the `--os` or `--arch` parameters.

    2. Refer to the step 2 of "Pull the mirror using TiUP", and send this incomplete offline mirror to the control machine in the isolated environment.

    3. Check the path of the current offline mirror on the control machine in the isolated environment. If your TiUP tool is of a recent version, you can get the current mirror address by running the following command:

        {{< copyable "shell-regular" >}}

        ```bash
        tiup mirror show
        ```

        If the output of the above command indicates that the `show` command does not exist, you might be using an older version of TiUP. In this case, you can get the current mirror address from `$HOME/.tiup/tiup.toml`. Record this mirror address. In the following steps, `${base_mirror}` is used to refer to this address.

    4. Merge an incomplete offline mirror into an existing offline mirror:

        First, copy the `keys` directory in the current offline mirror to the `$HOME/.tiup` directory:

        {{< copyable "shell-regular" >}}

        ```bash
        cp -r ${base_mirror}/keys $HOME/.tiup/
        ```

        Then use the TiUP command to merge the incomplete offline mirror into the mirror in use:

        {{< copyable "shell-regular" >}}

        ```bash
        tiup mirror merge tiup-custom-mirror-v1.11.3
        ```

    5. When the above steps are completed, check the result by running the `tiup list` command. In this document's example, the outputs of both `tiup list tiup` and `tiup list cluster` show that the corresponding components of `v1.11.3` are available.

#### Deploy the offline TiUP component

After sending the package to the control machine of the target cluster, install the TiUP component by running the following commands:

{{< copyable "shell-regular" >}}

```bash
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz && \
sh tidb-community-server-${version}-linux-amd64/local_install.sh && \
source /home/tidb/.bash_profile
```

The `local_install.sh` script automatically runs the `tiup mirror set tidb-community-server-${version}-linux-amd64` command to set the current mirror address to `tidb-community-server-${version}-linux-amd64`.

#### Merge offline packages

If you download the offline packages from the [official download page](https://www.pingcap.com/download/), you need to merge the server package and the toolkit package into an offline mirror. If you manually package the offline component packages using the `tiup mirror clone` command, you can skip this step.

Run the following commands to merge the offline toolkit package into the server package directory:

```bash
tar xf tidb-community-toolkit-${version}-linux-amd64.tar.gz
ls -ld tidb-community-server-${version}-linux-amd64 tidb-community-toolkit-${version}-linux-amd64
cd tidb-community-server-${version}-linux-amd64/
cp -rp keys ~/.tiup/
tiup mirror merge ../tidb-community-toolkit-${version}-linux-amd64
```

To switch the mirror to another directory, run the `tiup mirror set <mirror-dir>` command. To switch the mirror to the online environment, run the `tiup mirror set https://tiup-mirrors.pingcap.com` command.

## Step 3. Initialize cluster topology file

Run the following command to create a cluster topology file:

{{< copyable "shell-regular" >}}

```shell
tiup cluster template > topology.yaml
```

In the following two common scenarios, you can generate recommended topology templates by running commands:

- For hybrid deployment: Multiple instances are deployed on a single machine. For details, see [Hybrid Deployment Topology](/hybrid-deployment-topology.md).

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster template --full > topology.yaml
    ```

- For geo-distributed deployment: TiDB clusters are deployed in geographically distributed data centers. For details, see [Geo-Distributed Deployment Topology](/geo-distributed-deployment-topology.md).

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster template --multi-dc > topology.yaml
    ```

Run `vi topology.yaml` to see the configuration file content:

{{< copyable "shell-regular" >}}

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

The following examples cover seven common scenarios. You need to modify the configuration file (named `topology.yaml`) according to the topology description and templates in the corresponding links. For other scenarios, edit the configuration template accordingly.

| Application | Configuration task | Configuration file template | Topology description |
| :-- | :-- | :-- | :-- |
| OLTP | [Deploy minimal topology](/minimal-deployment-topology.md) | [Simple minimal configuration template](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml) <br/> [Full minimal configuration template](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml) | This is the basic cluster topology, including tidb-server, tikv-server, and pd-server. |
| HTAP | [Deploy the TiFlash topology](/tiflash-deployment-topology.md) | [Simple TiFlash configuration template](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiflash.yaml) <br/> [Full TiFlash configuration template](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml) | This is to deploy TiFlash along with the minimal cluster topology. TiFlash is a columnar storage engine, and gradually becomes a standard cluster topology. |
| Replicate incremental data using [TiCDC](/ticdc/ticdc-overview.md) | [Deploy the TiCDC topology](/ticdc-deployment-topology.md) | [Simple TiCDC configuration template](https://github.com/pingcap/docs/blob/master/config-templates/simple-cdc.yaml) <br/> [Full TiCDC configuration template](https://github.com/pingcap/docs/blob/master/config-templates/complex-cdc.yaml) | This is to deploy TiCDC along with the minimal cluster topology. TiCDC supports multiple downstream platforms, such as TiDB, MySQL, and MQ. |
| Replicate incremental data using [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) | [Deploy the TiDB Binlog topology](/tidb-binlog-deployment-topology.md) | [Simple TiDB Binlog configuration template (MySQL as downstream)](https://github.com/pingcap/docs/blob/master/config-templates/simple-tidb-binlog.yaml) <br/> [Simple TiDB Binlog configuration template (Files as downstream)](https://github.com/pingcap/docs/blob/master/config-templates/simple-file-binlog.yaml) <br/> [Full TiDB Binlog configuration template](https://github.com/pingcap/docs/blob/master/config-templates/complex-tidb-binlog.yaml) | This is to deploy TiDB Binlog along with the minimal cluster topology. |
| Use OLAP on Spark | [Deploy the TiSpark topology](/tispark-deployment-topology.md) | [Simple TiSpark configuration template](https://github.com/pingcap/docs/blob/master/config-templates/simple-tispark.yaml) <br/> [Full TiSpark configuration template](https://github.com/pingcap/docs/blob/master/config-templates/complex-tispark.yaml) |  This is to deploy TiSpark along with the minimal cluster topology. TiSpark is a component built for running Apache Spark on top of TiDB/TiKV to answer the OLAP queries. Currently, TiUP cluster's support for TiSpark is still **experimental**. |
| Deploy multiple instances on a single machine | [Deploy a hybrid topology](/hybrid-deployment-topology.md) | [Simple configuration template for hybrid deployment](https://github.com/pingcap/docs/blob/master/config-templates/simple-multi-instance.yaml) <br/> [Full configuration template for hybrid deployment](https://github.com/pingcap/docs/blob/master/config-templates/complex-multi-instance.yaml) | The deployment topologies also apply when you need to add extra configurations for the directory, port, resource ratio, and label. |
| Deploy TiDB clusters across data centers | [Deploy a geo-distributed deployment topology](/geo-distributed-deployment-topology.md) | [Configuration template for geo-distributed deployment](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml) | This topology takes the typical architecture of three data centers in two cities as an example. It introduces the geo-distributed deployment architecture and the key configuration that requires attention. |

> **Note:**
>
> - For parameters that should be globally effective, configure these parameters of corresponding components in the `server_configs` section of the configuration file.
> - For parameters that should be effective on a specific node, configure these parameters in the `config` of this node.
> - Use `.` to indicate the subcategory of the configuration, such as `log.slow-threshold`. For more formats, see [TiUP configuration template](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml).
> - If you need to specify the user group name to be created on the target machine, see [this example](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml#L7).

For more configuration description, see the following configuration examples:

- [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example)
- [TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/master/etc/config-template.toml)
- [PD `config.toml.example`](https://github.com/pingcap/pd/blob/master/conf/config.toml)
- [TiFlash `config.toml.example`](https://github.com/pingcap/tiflash/blob/master/etc/config-template.toml)

## Step 4. Run the deployment command

> **Note:**
>
> You can use secret keys or interactive passwords for security authentication when you deploy TiDB using TiUP:
>
> - If you use secret keys, specify the path of the keys through `-i` or `--identity_file`.
> - If you use passwords, add the `-p` flag to enter the password interaction window.
> - If password-free login to the target machine has been configured, no authentication is required.
>
> In general, TiUP creates the user and group specified in the `topology.yaml` file on the target machine, with the following exceptions:
>
> - The user name configured in `topology.yaml` already exists on the target machine.
> - You have used the `--skip-create-user` option in the command line to explicitly skip the step of creating the user.

Before you run the `deploy` command, use the `check` and `check --apply` commands to detect and automatically repair potential risks in the cluster:

1. Check for potential risks:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster check ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2. Enable automatic repair:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster check ./topology.yaml --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

3. Deploy a TiDB cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster deploy tidb-test v6.6.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

In the `tiup cluster deploy` command above:

- `tidb-test` is the name of the TiDB cluster to be deployed.
- `v6.6.0` is the version of the TiDB cluster to be deployed. You can see the latest supported versions by running `tiup list tidb`.
- `topology.yaml` is the initialization configuration file.
- `--user root` indicates logging into the target machine as the `root` user to complete the cluster deployment. The `root` user is expected to have `ssh` and `sudo` privileges to the target machine. Alternatively, you can use other users with `ssh` and `sudo` privileges to complete the deployment.
- `[-i]` and `[-p]` are optional. If you have configured login to the target machine without password, these parameters are not required. If not, choose one of the two parameters. `[-i]` is the private key of the root user (or other users specified by `--user`) that has access to the target machine. `[-p]` is used to input the user password interactively.

At the end of the output log, you will see ```Deployed cluster `tidb-test` successfully```. This indicates that the deployment is successful.

## Step 5. Check the clusters managed by TiUP

{{< copyable "shell-regular" >}}

```shell
tiup cluster list
```

TiUP supports managing multiple TiDB clusters. The preceding command outputs information of all the clusters currently managed by TiUP, including the cluster name, deployment user, version, and secret key information:

## Step 6. Check the status of the deployed TiDB cluster

For example, run the following command to check the status of the `tidb-test` cluster:

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

Expected output includes the instance ID, role, host, listening port, and status (because the cluster is not started yet, so the status is `Down`/`inactive`), and directory information.

## Step 7. Start a TiDB cluster

Since TiUP cluster v1.9.0, safe start is introduced as a new start method. Starting a database using this method improves the security of the database. It is recommended that you use this method.

After safe start, TiUP automatically generates a password for the TiDB root user and returns the password in the command-line interface.

> **Note:**
>
> - After safe start of a TiDB cluster, you cannot log in to TiDB using a root user without a password. Therefore, you need to record the password returned in the command output for future logins.
>
> - The password is generated only once. If you do not record it or you forgot it, refer to [Forget the `root` password](/user-account-management.md#forget-the-root-password) to change the password.

Method 1: Safe start

{{< copyable "shell-regular" >}}

```shell
tiup cluster start tidb-test --init
```

If the output is as follows, the start is successful:

{{< copyable "shell-regular" >}}

```shell
Started cluster `tidb-test` successfully.
The root password of TiDB database has been changed.
The new password is: 'y_+3Hwp=*AWz8971s6'.
Copy and record it to somewhere safe, it is only displayed once, and will not be stored.
The generated password can NOT be got again in future.
```

Method 2: Standard start

{{< copyable "shell-regular" >}}

```shell
tiup cluster start tidb-test
```

If the output log includes ```Started cluster `tidb-test` successfully```, the start is successful. After standard start, you can log in to a database using a root user without a password.

## Step 8. Verify the running status of the TiDB cluster

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

If the output log shows `Up` status, the cluster is running properly.

## See also

If you have deployed [TiFlash](/tiflash/tiflash-overview.md) along with the TiDB cluster, see the following documents:

- [Use TiFlash](/tiflash/tiflash-overview.md#use-tiflash)
- [Maintain a TiFlash Cluster](/tiflash/maintain-tiflash.md)
- [TiFlash Alert Rules and Solutions](/tiflash/tiflash-alert-rules.md)
- [Troubleshoot TiFlash](/tiflash/troubleshoot-tiflash.md)

If you have deployed [TiCDC](/ticdc/ticdc-overview.md) along with the TiDB cluster, see the following documents:

- [Changefeed Overview](/ticdc/ticdc-changefeed-overview.md)
- [Manage Changefeed](/ticdc/ticdc-manage-changefeed.md)
- [Troubleshoot TiCDC](/ticdc/troubleshoot-ticdc.md)
- [TiCDC FAQs](/ticdc/ticdc-faq.md)
